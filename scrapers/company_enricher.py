#!/usr/bin/env python3
"""
Enhanced Company Enricher — Extracts contact info from Malaysian company websites.
Runs standalone or as GitHub Action. Outputs CSV/JSON for CRM import.
"""

import asyncio
import csv
import json
import re
import sqlite3
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "companies.db"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ms;q=0.8",
}

# Malaysian phone patterns
PHONE_PATTERNS = [
    r'\+?6?0?1[0-9][\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # Mobile
    r'\+?6?0?3[\s\-]?\d{3,4}[\s\-]?\d{4}',         # KL/Selangor landline
    r'\+?6?0?[4-9][\s\-]?\d{3,4}[\s\-]?\d{3,4}',   # Other states
    r'0[1-9][\s\-]?\d{3,4}[\s\-]?\d{3,4}',         # Local format
]

EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


@dataclass
class CompanyContact:
    company_name: str
    website: str
    phone: Optional[str] = None
    email: Optional[str] = None
    hr_email: Optional[str] = None
    contact_page: Optional[str] = None
    linkedin: Optional[str] = None
    address: Optional[str] = None
    source_url: str = ""
    scraped_at: str = ""
    confidence: str = "low"  # high, medium, low


class ContactExtractor:
    def __init__(self, timeout: int = 15, max_pages: int = 5):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_pages = max_pages
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        self.session = aiohttp.ClientSession(
            headers=HEADERS,
            timeout=self.timeout,
            connector=connector
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _normalize_url(self, url: str) -> str:
        if not url:
            return ""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')

    def _generate_contact_urls(self, base_url: str) -> list[str]:
        base = self._normalize_url(base_url)
        paths = [
            '', '/contact-us', '/contact', '/contactus', '/contact_us',
            '/about-us', '/about', '/careers', '/career', '/join-us',
            '/en/contact', '/en/contact-us', '/my/contact', '/my/contact-us'
        ]
        return [urljoin(base + '/', p.lstrip('/')) for p in paths]

    def _extract_phones(self, text: str) -> list[str]:
        phones = []
        for pattern in PHONE_PATTERNS:
            matches = re.findall(pattern, text)
            for m in matches:
                cleaned = re.sub(r'[\s\-\(\)]', '', m)
                if cleaned.startswith('60'):
                    cleaned = '+' + cleaned
                elif cleaned.startswith('0'):
                    cleaned = '+6' + cleaned
                if cleaned not in phones and len(cleaned) >= 10:
                    phones.append(cleaned)
        return phones

    def _extract_emails(self, text: str, html: str = "") -> tuple[list[str], list[str]]:
        all_emails = set(EMAIL_PATTERN.findall(text.lower()))
        # Also check mailto links
        mailto_matches = re.findall(r'mailto:([^"\'>\s]+)', html, re.IGNORECASE)
        all_emails.update(e.lower() for e in mailto_matches)

        general = []
        hr = []
        hr_keywords = ['hr', 'career', 'recruit', 'talent', 'hiring', 'people', 'personnel', 'jobs']
        
        for email in all_emails:
            # Filter noise
            if any(bad in email for bad in ['noreply', 'no-reply', 'donotreply', 'spam', 'example', 'test', 'admin@', 'info@host', 'webmaster']):
                continue
            if any(kw in email for kw in hr_keywords):
                hr.append(email)
            else:
                general.append(email)
        
        return general[:3], hr[:3]

    def _extract_linkedin(self, html: str) -> Optional[str]:
        matches = re.findall(r'linkedin\.com/(?:company|school)/([^/"\'>\s]+)', html, re.IGNORECASE)
        if matches:
            return f"https://linkedin.com/company/{matches[0]}"
        return None

    def _extract_address(self, text: str, html: str) -> Optional[str]:
        # Look for Malaysian address patterns
        address_patterns = [
            r'(?:No\.?\s*\d+[,\s]+)?(?:Jalan|Jln|Lorong|Persiaran)\s+[^,\n]{5,50}',
            r'\d{5}\s+[A-Za-z\s]+(?:Selangor|Kuala Lumpur|Johor|Penang|Perak|Negeri Sembilan|Melaka|Kedah|Pahang|Terengganu|Kelantan|Sabah|Sarawak|Putrajaya|Labuan)',
            r'(?:Suite|Unit|Level|Floor)\s+\d+[^,\n]{10,50}',
        ]
        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        return None

    async def _fetch_page(self, url: str) -> Optional[tuple[str, str]]:
        """Returns (text, html) or None"""
        try:
            async with self.session.get(url, allow_redirects=True) as resp:
                if resp.status != 200:
                    return None
                html = await resp.text()
                soup = BeautifulSoup(html, 'lxml')
                # Remove script/style
                for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                    tag.decompose()
                text = soup.get_text(' ', strip=True)
                return text[:50000], html[:100000]  # Limit size
        except Exception:
            return None

    async def enrich_company(self, company_name: str, website: str) -> CompanyContact:
        website = self._normalize_url(website)
        if not website:
            return CompanyContact(company_name=company_name, website="", scraped_at=datetime.now().isoformat())

        contact = CompanyContact(
            company_name=company_name,
            website=website,
            source_url=website,
            scraped_at=datetime.now().isoformat()
        )

        urls = self._generate_contact_urls(website)
        all_text = ""
        all_html = ""
        pages_scraped = 0

        for url in urls[:self.max_pages]:
            result = await self._fetch_page(url)
            if result:
                text, html = result
                all_text += " " + text
                all_html += " " + html
                pages_scraped += 1
                contact.contact_page = url
                # Early exit if we have good data
                if contact.phone and contact.email:
                    break
            await asyncio.sleep(0.5)  # Rate limit

        # Extract all contact info
        phones = self._extract_phones(all_text)
        if phones:
            contact.phone = phones[0]
            if len(phones) > 1:
                contact.phone += f" | {phones[1]}"

        general_emails, hr_emails = self._extract_emails(all_text, all_html)
        if general_emails:
            contact.email = general_emails[0]
        if hr_emails:
            contact.hr_email = hr_emails[0]

        linkedin = self._extract_linkedin(all_html)
        if linkedin:
            contact.linkedin = linkedin

        address = self._extract_address(all_text, all_html)
        if address:
            contact.address = address[:200]

        # Confidence scoring
        score = 0
        if contact.phone: score += 2
        if contact.email: score += 2
        if contact.hr_email: score += 2
        if contact.linkedin: score += 1
        if contact.address: score += 1
        if pages_scraped >= 3: score += 1

        if score >= 5: contact.confidence = "high"
        elif score >= 3: contact.confidence = "medium"
        else: contact.confidence = "low"

        return contact


async def enrich_from_database(limit: int = 0, priority_only: bool = False) -> list[CompanyContact]:
    """Enrich companies from local SQLite database"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT company_name, website, priority_score 
        FROM companies 
        WHERE website IS NOT NULL AND website != ''
    """
    if priority_only:
        query += " AND priority_score >= 70"
    query += " ORDER BY priority_score DESC"
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print(f"Found {len(rows)} companies to enrich")

    results = []
    async with ContactExtractor() as extractor:
        # Process in batches of 10
        for i in range(0, len(rows), 10):
            batch = rows[i:i+10]
            tasks = [
                extractor.enrich_company(row['company_name'], row['website'] or '')
                for row in batch
            ]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for row, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    print(f"  Error enriching {row['company_name']}: {result}")
                    results.append(CompanyContact(
                        company_name=row['company_name'],
                        website=row['website'] or '',
                        scraped_at=datetime.now().isoformat(),
                        confidence="error"
                    ))
                else:
                    results.append(result)
                    status = "✓" if result.confidence != "low" else "○"
                    print(f"  {status} {result.company_name}: phone={bool(result.phone)} email={bool(result.email)} conf={result.confidence}")

    return results


def save_results(contacts: list[CompanyContact], output_format: str = "both"):
    """Save to CSV and/or JSON"""
    DATA_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if output_format in ("csv", "both"):
        csv_path = DATA_DIR / f"enriched_contacts_{timestamp}.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Company Name', 'Website', 'Phone', 'Email', 'HR Email',
                'LinkedIn', 'Address', 'Contact Page', 'Source URL',
                'Scraped At', 'Confidence'
            ])
            for c in contacts:
                writer.writerow([
                    c.company_name, c.website, c.phone or '', c.email or '',
                    c.hr_email or '', c.linkedin or '', c.address or '',
                    c.contact_page or '', c.source_url, c.scraped_at, c.confidence
                ])
        print(f"Saved CSV: {csv_path}")

    if output_format in ("json", "both"):
        json_path = DATA_DIR / f"enriched_contacts_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(c) for c in contacts], f, indent=2, ensure_ascii=False)
        print(f"Saved JSON: {json_path}")

    # Also update the main companies.csv with latest enrichment
    main_csv = DATA_DIR / "companies_enriched.csv"
    with open(main_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Company Name', 'Website', 'Phone', 'Email', 'HR Email',
            'LinkedIn', 'Address', 'Confidence', 'Last Enriched'
        ])
        for c in contacts:
            writer.writerow([
                c.company_name, c.website, c.phone or '', c.email or '',
                c.hr_email or '', c.linkedin or '', c.address or '',
                c.confidence, c.scraped_at
            ])
    print(f"Updated master: {main_csv}")


def update_database(contacts: list[CompanyContact]):
    """Update SQLite database with enriched contacts"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    updated = 0
    for c in contacts:
        if c.confidence == "error":
            continue
        cursor.execute("""
            UPDATE companies 
            SET phone = COALESCE(?, phone),
                email = COALESCE(?, email),
                hr_contact = COALESCE(?, hr_contact),
                linkedin_url = COALESCE(?, linkedin_url),
                address = COALESCE(?, address)
            WHERE company_name = ?
        """, (c.phone, c.email, c.hr_email, c.linkedin, c.address, c.company_name))
        if cursor.rowcount > 0:
            updated += 1

    conn.commit()
    conn.close()
    print(f"Database updated: {updated} companies")


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Enrich Malaysian company contacts")
    parser.add_argument("--limit", type=int, default=0, help="Max companies to process (0 = all)")
    parser.add_argument("--priority-only", action="store_true", help="Only priority_score >= 70")
    parser.add_argument("--no-db-update", action="store_true", help="Don't update SQLite")
    parser.add_argument("--output", choices=["csv", "json", "both"], default="both")
    args = parser.parse_args()

    print("=" * 60)
    print("MALAYSIA CORRIDOR OPS — COMPANY CONTACT ENRICHER")
    print("=" * 60)
    print(f"Limit: {args.limit or 'All'}")
    print(f"Priority only: {args.priority_only}")
    print(f"Started: {datetime.now().isoformat()}")
    print()

    contacts = await enrich_from_database(args.limit, args.priority_only)

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    high = sum(1 for c in contacts if c.confidence == "high")
    medium = sum(1 for c in contacts if c.confidence == "medium")
    low = sum(1 for c in contacts if c.confidence == "low")
    error = sum(1 for c in contacts if c.confidence == "error")
    with_phone = sum(1 for c in contacts if c.phone)
    with_email = sum(1 for c in contacts if c.email)
    with_hr = sum(1 for c in contacts if c.hr_email)

    print(f"Total processed: {len(contacts)}")
    print(f"  High confidence: {high}")
    print(f"  Medium confidence: {medium}")
    print(f"  Low confidence: {low}")
    print(f"  Errors: {error}")
    print(f"  With phone: {with_phone} ({with_phone/len(contacts)*100:.1f}%)")
    print(f"  With email: {with_email} ({with_email/len(contacts)*100:.1f}%)")
    print(f"  With HR email: {with_hr} ({with_hr/len(contacts)*100:.1f}%)")

    save_results(contacts, args.output)

    if not args.no_db_update:
        update_database(contacts)

    print(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    asyncio.run(main())