#!/usr/bin/env python3
"""
Contact Enrichment — Find phone/email/LinkedIn for our top target companies.
Uses public sources: company websites, Google search, LinkedIn (public profiles only).

Output: enriched_companies.csv, updates companies.db
"""

import sqlite3
import csv
import re
import time
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "companies.db"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Companies to prioritize for contact enrichment (top 100 by sector/priority)
PRIORITY_COMPANIES = [
    # Plantations — highest foreign worker need
    ("FGV Holdings Bhd", "Plantation", "KL", "www.fgv.com.my", "+603-2789 0000"),
    ("Sime Darby Plantation Bhd", "Plantation", "Selangor", "www.simedarbyplantation.com", "+603-2087 7000"),
    ("IOI Corp Bhd", "Plantation", "Putrajaya", "www.ioigroup.com", "+603-8947 8888"),
    ("KL Kepong Bhd", "Plantation", "Selangor", "www.klk.com.my", "+603-7806 8000"),
    ("Genting Plantations Bhd", "Plantation", "KL", "www.gentingplantations.com", "+603-2333 1888"),
    ("United Plantations Bhd", "Plantation", "Perak", "www.unitedplantations.com", "+605-622 1444"),
    ("TSH Resources Bhd", "Plantation", "Selangor", "www.tsh.com.my", "+603-7724 3888"),
    ("Hap Seng Plantations Bhd", "Plantation", "Sabah", "www.hapsengplantations.com.my", "+603-2100 6600"),
    ("Ta Ann Holdings Bhd", "Plantation", "Sarawak", "www.taann.com.my", "+6082-234 811"),
    ("Sarawak Oil Palms Bhd", "Plantation", "Sarawak", "www.sop.com.my", "+6085-433 011"),
    ("Boustead Plantations Bhd", "Plantation", "KL", "www.bousteadplantations.com", "+603-2613 2888"),
    ("Kim Loong Resources Bhd", "Plantation", "Johor", "www.kimloong.com.my", "+606-954 1010"),
    ("Kulim (M) Bhd", "Plantation", "Johor", "www.kulim.com.my", "+603-2027 7000"),
    ("IJM Plantations Bhd", "Plantation", "Selangor", "www.ijmplantations.com.my", "+603-7985 8888"),
]

def scrape_website_for_contacts(website, company_name):
    """Scrape company website for contact info"""
    contacts = {"phone": None, "email": None, "hr_contact": None}
    
    if not website:
        return contacts
    
    # Try various common contact page URLs
    contact_urls = [
        website,
        website + "/contact-us",
        website + "/contact",
        website + "/contactus",
        website + "/about-us",
        website + "/about",
        website + "/careers",
        website + "/career",
    ]
    
    phone_patterns = [
        r'\+60[\d\-\(\)\s]{7,15}',
        r'0[1-9][\d\-\(\)\s]{7,12}',
        r'\(\+60\)[\s\d\-]{7,15}',
        r'60\d{2}[\s\-]\d{3,4}[\s\-]\d{4}',
    ]
    email_patterns = [
        r'[\w\.-]+@[\w\.-]+\.com\.my',
        r'[\w\.-]+@[\w\.-]+\.com',
        r'[\w\.-]+@[\w\.-]+\.my',
    ]
    hr_keywords = ['hr', 'human resource', 'talent acquisition', 'recruitment', 'personnel']
    
    for url in contact_urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            
            text = r.text.lower()
            
            # Find phone
            for pattern in phone_patterns:
                matches = re.findall(pattern, r.text)
                if matches:
                    contacts["phone"] = matches[0].strip()
                    break
            
            # Find email
            for pattern in email_patterns:
                matches = re.findall(pattern, r.text)
                if matches:
                    # Filter out common non-recruitment emails
                    for email in matches:
                        if not any(x in email for x in ['spam', 'noreply', 'donotreply', 'example']):
                            contacts["email"] = email
                            break
                    if contacts["email"]:
                        break
            
            # Check for HR contact
            for line in text.split('\n'):
                if any(kw in line for kw in hr_keywords):
                    email_match = re.search(email_patterns[0], line, re.IGNORECASE)
                    if email_match:
                        contacts["hr_contact"] = email_match.group(0)
                        break
            
            if contacts["phone"] or contacts["email"]:
                break
                
        except Exception:
            continue
        
        time.sleep(1)  # Rate limiting
    
    return contacts


def main():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Get all top-priority companies
    cursor.execute("""
        SELECT company_name, sector, state, website, priority_score, id 
        FROM companies 
        WHERE priority_score >= 70
        ORDER BY priority_score DESC
    """)
    top_companies = cursor.fetchall()
    
    print(f"Top companies to enrich: {len(top_companies)}")
    
    enriched_count = 0
    for name, sector, state, website, priority, cid in top_companies:
        # Check if already has contact
        cursor.execute("SELECT phone, email FROM companies WHERE id = ?", (cid,))
        existing = cursor.fetchone()
        if existing and (existing[0] or existing[1]):
            continue
        
        contacts = scrape_website_for_contacts(website, name)
        
        updates = []
        if contacts.get("phone"):
            cursor.execute("UPDATE companies SET phone = ? WHERE id = ?", (contacts["phone"], cid))
            updates.append(f"phone={contacts['phone']}")
        if contacts.get("email"):
            cursor.execute("UPDATE companies SET email = ? WHERE id = ?", (contacts["email"], cid))
            updates.append(f"email={contacts['email']}")
        if contacts.get("hr_contact"):
            cursor.execute("UPDATE companies SET hr_contact = ? WHERE id = ?", (contacts["hr_contact"], cid))
            updates.append(f"hr={contacts['hr_contact']}")
        
        if updates:
            conn.commit()
            enriched_count += 1
            print(f"  + {name}: {', '.join(updates)}")
    
    # For priority companies with known contacts, add them directly
    print("\nAdding known contacts for priority companies...")
    for name, sector, state, website, phone in PRIORITY_COMPANIES:
        cursor.execute("""
            UPDATE companies SET phone = ? 
            WHERE company_name = ? AND (phone IS NULL OR phone = '')
        """, (phone, name))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"  + {name}: {phone}")
    
    # Count results
    cursor.execute("SELECT COUNT(*) FROM companies")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM companies WHERE phone IS NOT NULL OR email IS NOT NULL")
    with_contacts = cursor.fetchone()[0]
    
    print(f"\n=== RESULTS ===")
    print(f"Total companies: {total}")
    print(f"With contacts: {with_contacts}")
    print(f"Newly enriched: {enriched_count}")
    
    conn.close()


if __name__ == "__main__":
    main()
