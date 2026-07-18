"""
Multi-Channel Lead Generation — Malaysian Employers
=====================================================
Sources: Websites, LinkedIn, Government Directories, Job Portals, News
Output: Normalized leads for CRM import
"""

import asyncio
import csv
import json
import re
import sqlite3
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
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


@dataclass
class RawLead:
    company_name: str
    website: str = ""
    phone: str = ""
    email: str = ""
    hr_email: str = ""
    linkedin: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    industry: str = ""
    sub_industry: str = ""
    source: str = ""
    source_url: str = ""
    employee_count: int = 0
    foreign_worker_count: int = 0
    priority_score: float = 50.0
    notes: str = ""
    scraped_at: str = ""


class LeadSource:
    """Base class for lead sources"""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        self.session = aiohttp.ClientSession(
            headers=HEADERS,
            timeout=timeout,
            connector=connector
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch(self, url: str) -> Optional[str]:
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
        except Exception as e:
            print(f"  Fetch error {url}: {e}")
        return None
    
    async def get_leads(self, limit: int = 0) -> List[RawLead]:
        raise NotImplementedError


class DirectorySource(LeadSource):
    """Government/Industry directory scraper"""
    
    def __init__(self, name: str, base_url: str, selectors: Dict[str, str]):
        super().__init__(name, base_url)
        self.selectors = selectors
    
    async def get_leads(self, limit: int = 0) -> List[RawLead]:
        leads = []
        html = await self.fetch(self.base_url)
        if not html:
            return leads
        
        soup = BeautifulSoup(html, 'lxml')
        items = soup.select(self.selectors.get('item', 'tr, .company-item, .listing'))
        
        for i, item in enumerate(items):
            if limit and i >= limit:
                break
            
            lead = self._parse_item(item)
            if lead and lead.company_name:
                leads.append(lead)
        
        return leads
    
    def _parse_item(self, item) -> Optional[RawLead]:
        name_el = item.select_one(self.selectors.get('name', 'h3, h4, .name, .company-name, a'))
        if not name_el:
            return None
        
        name = name_el.get_text(strip=True)
        if len(name) < 3:
            return None
        
        website_el = item.select_one(self.selectors.get('website', 'a[href*="http"]'))
        website = website_el.get('href', '') if website_el else ''
        
        phone_el = item.select_one(self.selectors.get('phone', '.phone, .tel, [href^="tel:"]'))
        phone = phone_el.get_text(strip=True) if phone_el else ''
        
        email_el = item.select_one(self.selectors.get('email', '[href^="mailto:"]'))
        email = email_el.get('href', '').replace('mailto:', '') if email_el else ''
        
        address_el = item.select_one(self.selectors.get('address', '.address, .location'))
        address = address_el.get_text(strip=True) if address_el else ''
        
        return RawLead(
            company_name=name,
            website=website,
            phone=phone,
            email=email,
            address=address,
            source=self.name,
            source_url=self.base_url,
            scraped_at=datetime.now().isoformat()
        )


class LinkedInSource(LeadSource):
    """LinkedIn company search via public pages (limited without auth)"""
    
    async def get_leads(self, keywords: List[str], location: str = "Malaysia", limit: int = 50) -> List[RawLead]:
        leads = []
        # Note: LinkedIn requires auth for full access
        # This uses public company pages only
        for keyword in keywords:
            search_url = f"https://www.linkedin.com/search/results/companies/?keywords={keyword}%20{location}"
            html = await self.fetch(search_url)
            if not html:
                continue
            
            # Parse public results (very limited without auth)
            soup = BeautifulSoup(html, 'lxml')
            # LinkedIn heavily obfuscates - this is placeholder
            print(f"  LinkedIn search for '{keyword}': requires auth for full data")
        
        return leads


class JobPortalSource(LeadSource):
    """Job portals: JobStreet, LinkedIn Jobs, Indeed, Maukerja"""
    
    PORTALS = {
        "jobstreet": {
            "base": "https://www.jobstreet.com.my",
            "search": "/en/job-search/{keyword}-jobs/in-{location}",
            "item": 'article[data-automation="jobListing"]',
            "company": '[data-automation="jobCompany"]',
            "title": '[data-automation="jobTitle"]',
            "location": '[data-automation="jobLocation"]',
        },
        "indeed": {
            "base": "https://my.indeed.com",
            "search": "/jobs?q={keyword}&l={location}",
            "item": '.job_seen_beacon',
            "company": '.companyName',
            "title": '.jobTitle',
            "location": '.companyLocation',
        }
    }
    
    async def get_leads(self, keywords: List[str], location: str = "Kuala Lumpur", 
                        portals: List[str] = None, limit: int = 50) -> List[RawLead]:
        portals = portals or ["jobstreet", "indeed"]
        leads = []
        
        for portal_name in portals:
            portal = self.PORTALS.get(portal_name)
            if not portal:
                continue
            
            for keyword in keywords:
                search_url = portal["base"] + portal["search"].format(
                    keyword=keyword.replace(" ", "-"),
                    location=location.replace(" ", "-")
                )
                
                html = await self.fetch(search_url)
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'lxml')
                items = soup.select(portal["item"])
                
                for item in items[:limit]:
                    company_el = item.select_one(portal["company"])
                    title_el = item.select_one(portal["title"])
                    loc_el = item.select_one(portal["location"])
                    
                    if company_el:
                        lead = RawLead(
                            company_name=company_el.get_text(strip=True),
                            industry=keyword,
                            state=loc_el.get_text(strip=True) if loc_el else location,
                            source=f"{portal_name}_jobs",
                            source_url=search_url,
                            notes=f"Hiring: {title_el.get_text(strip=True) if title_el else ''}",
                            scraped_at=datetime.now().isoformat()
                        )
                        if lead.company_name and len(lead.company_name) > 3:
                            leads.append(lead)
                
                await asyncio.sleep(2)  # Rate limit
        
        return leads


class NewsSource(LeadSource):
    """News monitoring for company expansions, new factories, investments"""
    
    NEWS_SOURCES = [
        "https://www.theedgemarkets.com",
        "https://www.theedgemarkets.com/categories/companies",
        "https://www.freemalaysiatoday.com/category/business",
        "https://www.malaymail.com/news/malaysia",
        "https://www.thestar.com.my/business",
    ]
    
    EXPANSION_KEYWORDS = [
        "new factory", "new plant", "expansion", "investment", "groundbreaking",
        "facility", "manufacturing facility", "production line", "capacity expansion",
        "hiring", "jobs", "workforce", "foreign workers", "Bangladesh workers"
    ]
    
    async def get_leads(self, limit: int = 20) -> List[RawLead]:
        leads = []
        
        for source_url in self.NEWS_SOURCES:
            html = await self.fetch(source_url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'lxml')
            # Generic article extraction
            articles = soup.select('article, .post, .news-item, .story, h3 a, h2 a')
            
            for article in articles[:10]:
                text = article.get_text(strip=True)
                link = article.get('href') or article.find('a', href=True)
                
                if link and any(kw in text.lower() for kw in self.EXPANSION_KEYWORDS):
                    # Extract company name from title
                    title = text[:200]
                    # Simple extraction - look for capitalized words
                    companies = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Bhd|Berhad|Sdn|Sdn\.|Bhd\.|Ltd|Inc|Corp)\b', text)
                    for comp in companies:
                        lead = RawLead(
                            company_name=comp.strip(),
                            source="news_monitor",
                            source_url=link.get('href', source_url) if link else source_url,
                            notes=f"News: {title[:100]}",
                            priority_score=75.0,
                            scraped_at=datetime.now().isoformat()
                        )
                        leads.append(lead)
            
            await asyncio.sleep(1)
        
        return leads[:limit]


class DirectoryAggregator:
    """Aggregates leads from multiple directory sources"""
    
    SOURCES = {
        "fmm": DirectorySource(
            "FMM Directory",
            "https://www.fmm.org.my/members-directory",
            {
                'item': '.member-item, .company-listing, tr',
                'name': 'h3, h4, .company-name, .member-name, td:first-child',
                'website': 'a[href*="http"]',
                'phone': '.phone, .tel',
                'email': '[href^="mailto:"]',
                'address': '.address, .location'
            }
        ),
        "matrade": DirectorySource(
            "MATRADE Directory",
            "https://www.matrade.gov.my/en/directory",
            {
                'item': '.exporter-item, .company-listing',
                'name': '.exporter-name, .company-name, h3, h4',
                'website': 'a[href*="http"]',
                'phone': '.phone, .contact',
                'email': '[href^="mailto:"]',
                'address': '.address, .location'
            }
        ),
        "mpob": DirectorySource(
            "MPOB Plantation Directory",
            "https://www.mpob.gov.my",
            {
                'item': '.plantation-listing, .company-item',
                'name': '.name, .company-name, h3',
                'website': 'a[href*="http"]',
                'phone': '.phone, .tel',
                'email': '[href^="mailto:"]',
                'address': '.address, .location'
            }
        ),
        "cidb": DirectorySource(
            "CIDB Contractors",
            "https://www.cidb.gov.my",
            {
                'item': '.contractor-item, .grade-g7',
                'name': '.contractor-name, .company-name',
                'website': 'a[href*="http"]',
                'phone': '.phone, .contact',
                'email': '[href^="mailto:"]',
                'address': '.address, .location'
            }
        ),
    }
    
    def __init__(self):
        self.all_leads: List[RawLead] = []
    
    async def run_all(self, limit_per_source: int = 100) -> List[RawLead]:
        tasks = []
        for name, source in self.SOURCES.items():
            task = asyncio.create_task(self._run_source(source, limit_per_source))
            tasks.append((name, task))
        
        for name, task in tasks:
            try:
                leads = await task
                print(f"  {name}: {len(leads)} leads")
                self.all_leads.extend(leads)
            except Exception as e:
                print(f"  {name} failed: {e}")
        
        # Deduplicate by company name
        return self._deduplicate()
    
    async def _run_source(self, source: DirectorySource, limit: int) -> List[RawLead]:
        async with source:
            return await source.get_leads(limit)
    
    def _deduplicate(self) -> List[RawLead]:
        seen = {}
        for lead in self.all_leads:
            key = lead.company_name.lower().strip()
            key = re.sub(r'\s+(bhd|berhad|sdn|snd|ltd|inc|corp)\.?$', '', key)
            if key not in seen or len(lead.company_name) > len(seen[key].company_name):
                seen[key] = lead
        return list(seen.values())


async def save_leads_to_csv(leads: List[RawLead], filepath: Path):
    """Save leads to CSV for CRM import"""
    DATA_DIR.mkdir(exist_ok=True)
    
    fieldnames = [
        'company_name', 'website', 'phone', 'email', 'hr_email', 'linkedin',
        'address', 'city', 'state', 'industry', 'sub_industry',
        'source', 'source_url', 'employee_count', 'foreign_worker_count',
        'priority_score', 'notes', 'scraped_at'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow(asdict(lead))
    
    print(f"Saved {len(leads)} leads to {filepath}")


async def save_leads_to_db(leads: List[RawLead]):
    """Save leads to SQLite database"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            website TEXT,
            phone TEXT,
            email TEXT,
            hr_email TEXT,
            linkedin TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            industry TEXT,
            sub_industry TEXT,
            source TEXT,
            source_url TEXT,
            employee_count INTEGER DEFAULT 0,
            foreign_worker_count INTEGER DEFAULT 0,
            priority_score REAL DEFAULT 50.0,
            notes TEXT,
            scraped_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(company_name, source)
        )
    """)
    
    inserted = 0
    for lead in leads:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO raw_leads 
                (company_name, website, phone, email, hr_email, linkedin,
                 address, city, state, industry, sub_industry, source,
                 source_url, employee_count, foreign_worker_count,
                 priority_score, notes, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead.company_name, lead.website, lead.phone, lead.email,
                lead.hr_email, lead.linkedin, lead.address, lead.city,
                lead.state, lead.industry, lead.sub_industry, lead.source,
                lead.source_url, lead.employee_count, lead.foreign_worker_count,
                lead.priority_score, lead.notes, lead.scraped_at
            ))
            if cursor.rowcount > 0:
                inserted += 1
        except Exception as e:
            print(f"  DB error for {lead.company_name}: {e}")
    
    conn.commit()
    conn.close()
    print(f"Inserted {inserted} new leads to database")


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Multi-channel lead generation")
    parser.add_argument("--sources", nargs="+", default=["directories", "jobs", "news"],
                        choices=["directories", "jobs", "news", "all"])
    parser.add_argument("--limit", type=int, default=100, help="Limit per source")
    parser.add_argument("--keywords", nargs="+", default=[
        "manufacturing", "electronics", "construction", "plantation",
        "hospitality", "cleaning", "security", "logistics"
    ])
    parser.add_argument("--output", default="data/leads_raw.csv")
    parser.add_argument("--save-db", action="store_true", help="Also save to SQLite")
    args = parser.parse_args()
    
    print("=" * 60)
    print("MALAYSIA CORRIDOR OPS — MULTI-CHANNEL LEAD GENERATION")
    print("=" * 60)
    print(f"Sources: {args.sources}")
    print(f"Limit per source: {args.limit}")
    print(f"Keywords: {args.keywords}")
    print()
    
    all_leads = []
    
    if "directories" in args.sources or "all" in args.sources:
        print("\n[1/3] Government/Industry Directories...")
        agg = DirectoryAggregator()
        dir_leads = await agg.run_all(args.limit)
        all_leads.extend(dir_leads)
        print(f"  Total directory leads: {len(dir_leads)}")
    
    if "jobs" in args.sources or "all" in args.sources:
        print("\n[2/3] Job Portals (hiring signals)...")
        job_source = JobPortalSource("Job Portals", "https://www.jobstreet.com.my")
        job_leads = await job_source.get_leads(args.keywords, limit=args.limit)
        all_leads.extend(job_leads)
        print(f"  Total job leads: {len(job_leads)}")
    
    if "news" in args.sources or "all" in args.sources:
        print("\n[3/3] News Monitoring (expansion signals)...")
        news_source = NewsSource("News Monitor", "https://www.theedgemarkets.com")
        news_leads = await news_source.get_leads(args.limit)
        all_leads.extend(news_leads)
        print(f"  Total news leads: {len(news_leads)}")
    
    # Deduplicate across all sources
    print(f"\nTotal raw leads: {len(all_leads)}")
    
    seen = {}
    for lead in all_leads:
        key = lead.company_name.lower().strip()
        key = re.sub(r'\s+(bhd|berhad|sdn|snd|ltd|inc|corp)\.?$', '', key)
        if key not in seen or len(lead.company_name) > len(seen[key].company_name):
            seen[key] = lead
    
    unique_leads = list(seen.values())
    print(f"Unique leads after dedup: {len(unique_leads)}")
    
    # Save
    output_path = Path(args.output)
    await save_leads_to_csv(unique_leads, output_path)
    
    if args.save_db:
        await save_leads_to_db(unique_leads)
    
    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())