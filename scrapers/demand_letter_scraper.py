#!/usr/bin/env python3
"""
Malaysia Corridor Ops — Demand Letter & Quota Circular Scraper
================================================================
Async scraper for Malaysia-related foreign-worker circulars, notices, and
clearance data published by Bangladeshi government portals.

Corrected targets (verified 2026-07-20 — see module docstrings below for why):
  - bmet.gov.bd            : real target. Notices/circulars/office-orders/
                              publications, each linking to PDFs.
  - oep.gov.bd              : NOT a job-order board. It's a credential/
                              clearance system behind role-based logins.
                              The one public page (country clearance report)
                              is scraped for aggregate Malaysia stats only.
  - bmet.teletalk.com.bd    : DROPPED. This is BMET's generic Teletalk-
                              powered *internal staff recruitment* portal
                              (admit cards, payments) — unrelated to Malaysia
                              worker quotas. Scraping it would produce noise,
                              not signal.
  - "Public document repos" (Scribd, Docplayer, PDFCoffee, SlideShare,
                              Academia.edu): implemented as metadata-only
                              discovery via a real search API (Google
                              Custom Search JSON API). Never downloads
                              documents, never scrapes Google/Bing search
                              result pages directly (their ToS forbids it
                              and it's fragile), and never attempts to
                              bypass a paywall/viewer. This also avoids
                              sweeping up real personal data (names, passport
                              numbers) that may appear in filled-in employer
                              letters shared online, consistent with the
                              data-minimization commitments in
                              BULLETPROOF_BUSINESS_PLAN.md §10.
                              Query coverage: ~6 demand-letter/job-order
                              phrasings fanned out across all 5 repo sites
                              (30 generic queries), PLUS one targeted query
                              per real Malaysian employer already scored in
                              data/companies.db (top ~30 by priority_score,
                              capped to respect the 100/day free-tier quota)
                              — this is what actually searches for demand
                              letters "from Malaysian companies" specifically,
                              not just generic phrasing.

Known caveat: bmet.gov.bd serves a TLS certificate issued for a different
hostname (bicm.gov.bd) — a misconfiguration on their shared government
hosting, not evidence of a hostile intermediary. This scraper disables
certificate verification *only* for that specific host and logs a loud
warning every run so it's never a silent security compromise.

Usage:
    python scrapers/demand_letter_scraper.py                    # full run
    python scrapers/demand_letter_scraper.py --dry-run           # list only, no downloads
    python scrapers/demand_letter_scraper.py --skip-oep --skip-discovery
    python scrapers/demand_letter_scraper.py --max-pages 5 --concurrency 3

Discovery module requires GOOGLE_CSE_API_KEY and GOOGLE_CSE_CX environment
variables (free tier: 100 queries/day). See README section at the bottom
of this file for setup instructions. Without them, discovery is skipped
with an explanatory log line — not a silent no-op.
"""

import argparse
import asyncio
import hashlib
import json
import logging
import os
import re
import sqlite3
import ssl
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CIRCULARS_DIR = DATA_DIR / "circulars"
DB_PATH = DATA_DIR / "circulars.db"
DB_PATH_COMPANIES = DATA_DIR / "companies.db"  # the existing 505-company employer database

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("demand_letter_scraper")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
}

# Bureau of Manpower, Employment and Training — real, scrapable circular/notice categories.
BMET_BASE = "https://bmet.gov.bd"
BMET_CATEGORIES = [
    "notices",
    "notification-circulars",
    "office-orders",
    "publications",
    "monthly-reports",
    "annual-reports",
]
# bmet.gov.bd's cert is issued for the wrong hostname (bicm.gov.bd) — see module docstring.
BMET_INSECURE_HOSTS = {"bmet.gov.bd"}

# Overseas Employment Platform — credential/clearance system, not a job-order board.
OEP_CLEARANCE_URL = "https://www.oep.gov.bd/reports/country-clearance"
OEP_MALAYSIA_COUNTRY_ID = "106"  # confirmed via the country dropdown's <option value>

# PRIMARY_KEYWORDS: Malaysia-specific terms. At least one MUST be present — BMET's entire
# publishing stream is about "workers"/"recruitment"/"clearance" in general (that's their
# whole domain), so those generic terms alone match almost everything and are useless as a
# filter on their own. An earlier version of this scraper used them as primary triggers and
# it matched internal staff passport NOCs and Qatar/Singapore/UAE guides as "Malaysia"
# circulars — verified false positives, not a hypothetical risk.
PRIMARY_KEYWORDS = [
    "malaysia", "মালয়েশিয়া", "মালয়েশিয়ায়", "মালয়েশিয়ার",
    "fwcms", "turap", "kesuma",
]
# SECONDARY_KEYWORDS: only meaningful once a primary keyword already matched — used for
# more specific categorization/tagging, never as a standalone trigger.
SECONDARY_KEYWORDS = [
    "quota", "কোটা",
    "demand letter", "চাহিদাপত্র", "চাহিদা পত্র",
    "job order",
    "departure clearance", "বহির্গমন", "ছাড়পত্র",
    "recruiting agency", "রিক্রুটিং এজেন্সি",
]

PDF_URL_PATTERN = re.compile(r'https?://[^\s"\'<>]+\.pdf', re.IGNORECASE)


def make_ssl_context(host: str):
    """Default verified context for most hosts; unverified only for known-broken hosts."""
    if host in BMET_INSECURE_HOSTS:
        log.warning(
            "TLS verification DISABLED for %s — its certificate is issued for the wrong "
            "hostname (bicm.gov.bd), a known misconfiguration on their shared government "
            "hosting, not evidence of interception. Re-check this if that ever changes.",
            host,
        )
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return ssl.create_default_context()


def init_db():
    CIRCULARS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS circulars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            category TEXT,
            title TEXT,
            detail_url TEXT UNIQUE,
            file_url TEXT,
            local_path TEXT,
            matched_keywords TEXT,
            sha256 TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS discovered_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            title TEXT,
            snippet TEXT,
            url TEXT,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reviewed INTEGER DEFAULT 0,
            UNIQUE(url)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS oep_clearance_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT,
            raw_json TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


class RateLimiter:
    """Caps concurrent requests and enforces a minimum delay between them, per host."""

    def __init__(self, concurrency: int, delay: float):
        self.semaphore = asyncio.Semaphore(concurrency)
        self.delay = delay

    async def get(self, session: aiohttp.ClientSession, url: str, **kwargs):
        host = aiohttp.helpers.URL(url).host
        async with self.semaphore:
            for attempt in range(3):
                try:
                    ssl_ctx = make_ssl_context(host) if url.startswith("https") else None
                    async with session.get(url, ssl=ssl_ctx, timeout=aiohttp.ClientTimeout(total=30), **kwargs) as resp:
                        text = await resp.text(errors="ignore")
                        await asyncio.sleep(self.delay)
                        return resp.status, text
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    wait = 2 ** attempt
                    log.warning("Fetch failed (%s), attempt %d/3, retrying in %ds: %s", url, attempt + 1, wait, e)
                    await asyncio.sleep(wait)
            log.error("Giving up on %s after 3 attempts", url)
            return None, None

    async def get_bytes(self, session: aiohttp.ClientSession, url: str):
        host = aiohttp.helpers.URL(url).host
        async with self.semaphore:
            try:
                ssl_ctx = make_ssl_context(host) if url.startswith("https") else None
                async with session.get(url, ssl=ssl_ctx, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    data = await resp.read()
                    await asyncio.sleep(self.delay)
                    return resp.status, data
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                log.warning("Binary fetch failed for %s: %s", url, e)
                return None, None


def extract_detail_links(html: str, base_url: str, category: str) -> list:
    soup = BeautifulSoup(html, "lxml")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if f"/pages/{category}/" in href and href.rstrip("/") != f"/pages/{category}":
            links.add(urljoin(base_url, href))
    return sorted(links)


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].split("|")[0].strip()
    if soup.title:
        return soup.title.text.split("|")[0].strip()
    return ""


def find_pdf_links(html: str) -> list:
    return sorted(set(PDF_URL_PATTERN.findall(html)))


def relevant_keywords(text: str) -> list:
    """Require a Malaysia-specific PRIMARY keyword before considering this relevant at all;
    SECONDARY keywords are only appended for categorization once that gate is passed."""
    text_lower = text.lower()
    primary_hits = [kw for kw in PRIMARY_KEYWORDS if kw.lower() in text_lower]
    if not primary_hits:
        return []
    secondary_hits = [kw for kw in SECONDARY_KEYWORDS if kw.lower() in text_lower]
    return primary_hits + secondary_hits


async def crawl_bmet_category(session, limiter: RateLimiter, category: str, max_pages: int) -> list:
    """Paginate a BMET listing category until a page yields no new detail links."""
    log.info("[BMET] Crawling category: %s", category)
    seen_links = set()
    for page_num in range(1, max_pages + 1):
        url = f"{BMET_BASE}/pages/{category}" if page_num == 1 else f"{BMET_BASE}/pages/{category}?page={page_num}"
        status, html = await limiter.get(session, url)
        if status != 200 or not html:
            log.info("[BMET] %s page %d: HTTP %s, stopping pagination", category, page_num, status)
            break
        links = extract_detail_links(html, BMET_BASE, category)
        new_links = [l for l in links if l not in seen_links]
        if not new_links:
            log.info("[BMET] %s page %d: no new links, stopping pagination", category, page_num)
            break
        seen_links.update(new_links)
        log.info("[BMET] %s page %d: %d new links (total %d)", category, page_num, len(new_links), len(seen_links))
    return sorted(seen_links)


async def process_bmet_detail(session, limiter: RateLimiter, conn, category: str, detail_url: str, dry_run: bool):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM circulars WHERE detail_url = ?", (detail_url,))
    if cursor.fetchone():
        return  # already processed

    status, html = await limiter.get(session, detail_url)
    if status != 200 or not html:
        log.warning("[BMET] Could not fetch detail page %s (HTTP %s)", detail_url, status)
        return

    title = extract_title(html)
    combined_text = title + " " + BeautifulSoup(html, "lxml").get_text(" ", strip=True)[:3000]
    matched = relevant_keywords(combined_text)
    if not matched:
        return  # not relevant to Malaysia/quota/demand-letter topics

    pdf_links = find_pdf_links(html)
    if not pdf_links:
        # Still record the notice itself even with no attached PDF — the notice text may matter.
        cursor.execute(
            "INSERT OR IGNORE INTO circulars (source, category, title, detail_url, file_url, local_path, matched_keywords) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("bmet.gov.bd", category, title, detail_url, None, None, ",".join(matched)),
        )
        conn.commit()
        log.info("[BMET] MATCH (no PDF attached): %s — %s", category, title)
        return

    for pdf_url in pdf_links:
        local_path = None
        if not dry_run:
            pdf_status, pdf_bytes = await limiter.get_bytes(session, pdf_url)
            if pdf_status == 200 and pdf_bytes:
                sha = hashlib.sha256(pdf_bytes).hexdigest()
                dest_dir = CIRCULARS_DIR / "bmet" / category
                dest_dir.mkdir(parents=True, exist_ok=True)
                local_path = str(dest_dir / f"{sha[:16]}.pdf")
                if not Path(local_path).exists():
                    Path(local_path).write_bytes(pdf_bytes)
        cursor.execute(
            "INSERT OR IGNORE INTO circulars (source, category, title, detail_url, file_url, local_path, matched_keywords, sha256) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("bmet.gov.bd", category, title, detail_url, pdf_url, local_path,
             ",".join(matched), hashlib.sha256(pdf_url.encode()).hexdigest() if dry_run else None),
        )
    conn.commit()
    log.info("[BMET] MATCH: %s — %s (%d file(s))", category, title, len(pdf_links))


async def run_bmet_scrape(conn, max_pages: int, concurrency: int, delay: float, categories: list, dry_run: bool):
    limiter = RateLimiter(concurrency, delay)
    async with aiohttp.ClientSession(headers=HEADERS, trust_env=True) as session:
        for category in categories:
            detail_links = await crawl_bmet_category(session, limiter, category, max_pages)
            tasks = [process_bmet_detail(session, limiter, conn, category, url, dry_run) for url in detail_links]
            for i in range(0, len(tasks), concurrency):
                await asyncio.gather(*tasks[i:i + concurrency])


async def run_oep_clearance(conn):
    """Best-effort fetch of Malaysia's row from OEP's public country-clearance report.

    This is an aggregate stats page (a public credential-system report), not a
    demand-letter/job-order source — see module docstring for why oep.gov.bd's
    other sections aren't scraped at all (role-based logins).
    """
    log.info("[OEP] Fetching Malaysia clearance report")
    limiter = RateLimiter(concurrency=1, delay=1.0)
    async with aiohttp.ClientSession(headers=HEADERS, trust_env=True) as session:
        # Try the common query-param pattern first; this endpoint renders via a country
        # dropdown client-side, so this may need adjustment if OEP changes their form handling.
        for params in (f"?country_id={OEP_MALAYSIA_COUNTRY_ID}", ""):
            url = OEP_CLEARANCE_URL + params
            status, html = await limiter.get(session, url)
            if status != 200 or not html:
                continue
            soup = BeautifulSoup(html, "lxml")
            tables = soup.find_all("table")
            if tables:
                rows = []
                for table in tables:
                    for tr in table.find_all("tr"):
                        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                        if cells:
                            rows.append(cells)
                if rows:
                    conn.execute(
                        "INSERT INTO oep_clearance_snapshots (country, raw_json) VALUES (?, ?)",
                        ("Malaysia", json.dumps(rows, ensure_ascii=False)),
                    )
                    conn.commit()
                    log.info("[OEP] Stored %d table row(s) from %s", len(rows), url)
                    return
        log.warning(
            "[OEP] Could not extract tabular clearance data automatically — the report page "
            "renders after a client-side country selection that this scraper's simple GET "
            "request may not trigger. Manual inspection of %s is recommended; this is logged, "
            "not silently swallowed.", OEP_CLEARANCE_URL,
        )


async def run_discovery(conn, queries: list):
    """Metadata-only discovery via Google Custom Search JSON API.

    Never downloads documents, never scrapes search-engine result pages directly.
    Requires GOOGLE_CSE_API_KEY and GOOGLE_CSE_CX (free tier: 100 queries/day).
    Setup: https://developers.google.com/custom-search/v1/overview
    """
    api_key = os.environ.get("GOOGLE_CSE_API_KEY")
    cx = os.environ.get("GOOGLE_CSE_CX")
    if not api_key or not cx:
        log.info(
            "[Discovery] Skipped — GOOGLE_CSE_API_KEY / GOOGLE_CSE_CX not set. "
            "This is deliberate, not a bug: see the README section at the bottom of this "
            "file for how to get a free-tier key if you want document discovery enabled."
        )
        return

    limiter = RateLimiter(concurrency=1, delay=1.0)
    async with aiohttp.ClientSession(headers=HEADERS, trust_env=True) as session:
        for query in queries:
            api_url = "https://www.googleapis.com/customsearch/v1"
            params = {"key": api_key, "cx": cx, "q": query, "num": 10}
            async with session.get(api_url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    log.warning("[Discovery] Search API error %s for query: %s", resp.status, query)
                    continue
                data = await resp.json()
                for item in data.get("items", []):
                    conn.execute(
                        "INSERT OR IGNORE INTO discovered_documents (query, title, snippet, url) VALUES (?, ?, ?, ?)",
                        (query, item.get("title"), item.get("snippet"), item.get("link")),
                    )
                conn.commit()
                log.info("[Discovery] %d result(s) for: %s", len(data.get("items", [])), query)
            await asyncio.sleep(limiter.delay)


# Public document-repository domains most likely to host shared demand-letter/job-order
# PDFs. Kept as a separate list (not folded into query strings) so both the generic and
# per-company query builders below can reuse it consistently.
DOCUMENT_REPO_SITES = [
    "scribd.com",
    "docplayer.net",
    "pdfcoffee.com",
    "slideshare.net",
    "academia.edu",
]

# Generic phrasings covering the different names/formats a Malaysia worker demand letter or
# job order commonly appears under, each fanned out across the document-repo sites above.
DEMAND_LETTER_PHRASES = [
    "DEMAND LETTER FOR RECRUITMENT OF WORKERS Malaysia",
    "JOB ORDER Malaysia manpower Bangladesh",
    "MANPOWER REQUISITION Malaysia worker",
    "POWER OF ATTORNEY recruitment agency Malaysia worker",
    "BMET demand letter Malaysia quota approval",
    "foreign worker demand letter Malaysia Sdn Bhd",
]


def build_default_discovery_queries() -> list:
    """Generic queries covering the different names a demand letter appears under, fanned
    out across every known public document-repo site — not just Scribd."""
    queries = []
    for site in DOCUMENT_REPO_SITES:
        for phrase in DEMAND_LETTER_PHRASES:
            queries.append(f'site:{site} "{phrase}"')
    return queries


DEFAULT_DISCOVERY_QUERIES = build_default_discovery_queries()


def build_company_discovery_queries(min_priority: float = 85.0, limit: int = 30) -> list:
    """Per-company demand-letter queries, one per real Malaysian employer already scored in
    data/companies.db — this is what actually targets 'every type of demand letter from
    Malaysian companies' rather than only generic phrasing. Capped and priority-gated to stay
    within the Google CSE free tier (100 queries/day total, shared with the generic queries
    above), and deduplicated by company name (the DB has a few name/sector/state duplicates)."""
    if not DB_PATH_COMPANIES.exists():
        log.info("[Discovery] data/companies.db not found — skipping per-company queries")
        return []
    conn = sqlite3.connect(str(DB_PATH_COMPANIES))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT company_name FROM companies WHERE priority_score >= ? "
        "ORDER BY priority_score DESC LIMIT ?",
        (min_priority, limit),
    )
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    # A couple of rows in companies.db are placeholder aggregates from the original seed
    # data (e.g. "Palm oil sector - multiple companies"), not real single companies —
    # searching for those by name in quotes is useless, so filter them out.
    names = [n for n in names if "multiple companies" not in n.lower() and "(various)" not in n.lower()]
    queries = []
    for name in names:
        site_filter = " OR ".join(f"site:{s}" for s in DOCUMENT_REPO_SITES)
        queries.append(f'"{name}" "demand letter" Malaysia worker ({site_filter})')
    log.info("[Discovery] Built %d per-company queries from data/companies.db (priority >= %s)",
              len(queries), min_priority)
    return queries


def print_summary(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) FROM circulars GROUP BY category")
    circular_counts = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM circulars WHERE local_path IS NOT NULL")
    downloaded = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM discovered_documents")
    discovered = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM oep_clearance_snapshots")
    oep_snapshots = cursor.fetchone()[0]

    print("\n" + "=" * 60)
    print("DEMAND LETTER SCRAPER — RUN SUMMARY")
    print("=" * 60)
    print(f"BMET matches by category: {dict(circular_counts) if circular_counts else '(none)'}")
    print(f"PDFs downloaded: {downloaded}")
    print(f"OEP Malaysia clearance snapshots stored: {oep_snapshots}")
    print(f"Documents discovered (metadata-only, unreviewed): {discovered}")
    print(f"Database: {DB_PATH}")
    print(f"Downloaded files: {CIRCULARS_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Scrape Malaysia-related BD labour quota circulars")
    parser.add_argument("--categories", nargs="+", default=BMET_CATEGORIES, help="BMET categories to crawl")
    parser.add_argument("--max-pages", type=int, default=10, help="Max pages to paginate per category")
    parser.add_argument("--concurrency", type=int, default=4, help="Max concurrent requests")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between requests per worker (seconds)")
    parser.add_argument("--dry-run", action="store_true", help="List matches without downloading files")
    parser.add_argument("--skip-oep", action="store_true", help="Skip the OEP clearance report fetch")
    parser.add_argument("--skip-discovery", action="store_true", help="Skip the search-API discovery module")
    parser.add_argument("--discovery-queries", nargs="+", default=None,
                         help="Override the full discovery query list (skips auto-building generic + per-company queries)")
    parser.add_argument("--skip-company-discovery", action="store_true",
                         help="Skip per-company demand-letter queries built from data/companies.db")
    parser.add_argument("--discovery-company-limit", type=int, default=30,
                         help="Max companies (by priority_score) to build discovery queries for")
    parser.add_argument("--discovery-min-priority", type=float, default=85.0,
                         help="Minimum companies.db priority_score to include in per-company discovery")
    parser.add_argument("--discovery-query-cap", type=int, default=95,
                         help="Hard cap on total discovery queries fired (Google CSE free tier is 100/day)")
    args = parser.parse_args()

    conn = init_db()
    log.info("Starting run — categories=%s max_pages=%d concurrency=%d dry_run=%s",
              args.categories, args.max_pages, args.concurrency, args.dry_run)

    asyncio.run(run_bmet_scrape(conn, args.max_pages, args.concurrency, args.delay, args.categories, args.dry_run))

    if not args.skip_oep:
        asyncio.run(run_oep_clearance(conn))
    else:
        log.info("[OEP] Skipped (--skip-oep)")

    if not args.skip_discovery:
        if args.discovery_queries is not None:
            queries = args.discovery_queries
        else:
            queries = list(DEFAULT_DISCOVERY_QUERIES)
            if not args.skip_company_discovery:
                queries += build_company_discovery_queries(args.discovery_min_priority, args.discovery_company_limit)
        if len(queries) > args.discovery_query_cap:
            log.warning("[Discovery] %d queries built, capping to %d to respect the free-tier daily quota",
                        len(queries), args.discovery_query_cap)
            queries = queries[:args.discovery_query_cap]
        asyncio.run(run_discovery(conn, queries))
    else:
        log.info("[Discovery] Skipped (--skip-discovery)")

    print_summary(conn)
    conn.close()


if __name__ == "__main__":
    main()

# =============================================================================
# README — setup notes for this scraper
# =============================================================================
#
# Corrected target list (see top-of-file docstring for the full reasoning):
#   - bmet.gov.bd: scraped for real. TLS cert is misconfigured (issued for
#     bicm.gov.bd) — verification is disabled ONLY for this host, and every
#     run logs a loud warning so that's never invisible.
#   - oep.gov.bd: only the public country-clearance report is touched.
#     Everything else on that portal sits behind role-based logins
#     (admin/employer/agency/employee) and is intentionally not attempted.
#   - bmet.teletalk.com.bd: dropped. It's BMET's internal staff-recruitment
#     application system (Teletalk-hosted, used government-wide for
#     unrelated hiring rounds), not a Malaysia quota circular source.
#
# Discovery module (Scribd-style public documents):
#   1. Get a Google Custom Search API key: https://developers.google.com/custom-search/v1/introduction
#   2. Create a Programmable Search Engine (set it to search the entire web):
#      https://programmablesearchengine.google.com/
#   3. Set environment variables before running:
#        export GOOGLE_CSE_API_KEY="your-key"
#        export GOOGLE_CSE_CX="your-search-engine-id"
#   4. Free tier: 100 queries/day. By default this scraper builds ~30 generic
#      queries (demand-letter phrasings x 5 document-repo sites) PLUS one
#      targeted query per real Malaysian employer in data/companies.db
#      (top ~30 by priority_score) — ~60 total, capped at --discovery-query-cap
#      (default 95) to leave headroom under the daily quota. Tune with
#      --discovery-company-limit / --discovery-min-priority / --skip-company-discovery,
#      or replace everything with your own list via --discovery-queries.
#   Without GOOGLE_CSE_API_KEY/GOOGLE_CSE_CX set, discovery is skipped —
#   this is intentional, not a silent failure (see the log line in run_discovery()).
#
#   This module NEVER downloads the documents it finds — only title, snippet,
#   and URL land in discovered_documents, for a human to review and decide
#   whether/how to follow up manually. This is a deliberate choice: real
#   employer demand letters shared online may contain actual personal data
#   (names, passport numbers) that this project's own data-protection
#   commitments (BULLETPROOF_BUSINESS_PLAN.md §10) say to minimize, not
#   vacuum up automatically.
#
# Output:
#   - data/circulars.db: `circulars` (BMET matches + downloaded file paths),
#     `oep_clearance_snapshots` (raw table data as JSON), `discovered_documents`
#     (search-API metadata, unreviewed by default).
#   - data/circulars/bmet/<category>/<sha256-prefix>.pdf: downloaded PDFs,
#     deduplicated by content hash.
