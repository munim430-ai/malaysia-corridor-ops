#!/usr/bin/env python3
"""
Malaysia Corridor Ops — Employer Outreach Generator
=====================================================
Reads data/companies.db and generates a ready-to-send outreach message
(email + WhatsApp + LinkedIn DM) for every company, using the sector-specific
pitch angles defined in MASTER_PROMPT.md.

Output: outreach/outreach_queue.csv, sorted by priority score, with a
pipeline_stage column so sent messages can be tracked (see update_pipeline.py).

This does NOT send anything. It only drafts messages for a human to send at
safe daily volumes (see content/DISTRIBUTION.md) — mass automated sending
would risk account bans and undermines the transparency positioning this
business is built on.
"""

import csv
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "companies.db"
OUTREACH_DIR = BASE_DIR / "outreach"
OUTPUT_PATH = OUTREACH_DIR / "outreach_queue.csv"

SECTOR_ANGLES = {
    "Plantation": "I see your plantation sector faces CBP scrutiny on worker fees. We offer a documented, zero-fee channel from Bangladesh.",
    "Rubber": "Given the sector's CBP Withhold Release Order history, we offer a fully documented, zero-worker-fee Bangladesh channel — built to hold up under audit.",
    "E&E": "We pre-screen and document Bangladeshi workers per RBA standards. No middleman fees, fully auditable chain.",
    "Electrical & Electronics": "We pre-screen and document Bangladeshi workers per RBA standards. No middleman fees, fully auditable chain.",
    "Manufacturing": "We pre-screen and document Bangladeshi workers per RBA standards. No middleman fees, fully auditable chain.",
    "Construction": "We can supply documented workers for your infrastructure projects. JTKSM-compliant, FWCMS-ready.",
    "Furniture": "We supply documented Bangladeshi workers for furniture manufacturing. Direct from source — no dalal markups.",
    "Retail": "Direct-source front-line workers from Bangladesh. Lower cost, fully documented, no agent markups.",
    "Services": "Direct-source front-line workers from Bangladesh. Lower cost, fully documented, no agent markups.",
    "Hospitality": "Direct-source front-line workers from Bangladesh. Lower cost, fully documented, no agent markups.",
    "Security": "Direct-source front-line workers from Bangladesh. Lower cost, fully documented, no agent markups.",
    "Property": "Direct-source front-line workers from Bangladesh. Lower cost, fully documented, no agent markups.",
    "Agriculture": "Reliable Bangladeshi workers for plantation/agriculture. RBA-aligned, lower cost than current agency channel.",
}
DEFAULT_ANGLE = "We're building a documented, RBA-aligned Bangladeshi worker channel with no middleman fees."

SIGNOFF = "Malaysia Corridor Ops | wa.me/880XXXXXXXXXX"

DISCLAIMER = (
    "This is an information & registration service; the corridor is currently closed pending "
    "the labour MoU. No fees are collected through this outreach."
)


def ensure_pipeline_columns(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(companies)")
    existing = {row[1] for row in cursor.fetchall()}
    if "pipeline_stage" not in existing:
        cursor.execute("ALTER TABLE companies ADD COLUMN pipeline_stage TEXT DEFAULT 'not_contacted'")
    if "last_contacted" not in existing:
        cursor.execute("ALTER TABLE companies ADD COLUMN last_contacted TEXT")
    if "outreach_channel" not in existing:
        cursor.execute("ALTER TABLE companies ADD COLUMN outreach_channel TEXT")
    conn.execute("UPDATE companies SET pipeline_stage = 'not_contacted' WHERE pipeline_stage IS NULL")
    conn.commit()


def build_messages(name, sector, city, state, employees, phone, email):
    angle = SECTOR_ANGLES.get(sector, DEFAULT_ANGLE)
    location = ", ".join(p for p in (city, state) if p and p != "None") or "Malaysia"
    scale = f" (~{employees:,} employees)" if employees else ""

    email_subject = f"Documented Bangladesh worker channel for {name}"
    email_body = (
        f"Hello,\n\n"
        f"I'm reaching out because the Malaysia-Bangladesh labour corridor is reopening, and we're "
        f"building a direct-source channel for documented, pre-screened Bangladeshi workers.\n\n"
        f"{angle}\n\n"
        f"Our model:\n"
        f"- RBA-aligned: zero worker-paid recruitment fees available on the employer-pays track\n"
        f"- FWCMS-compatible processing, TURAP-ready if/when adopted\n"
        f"- Complete documentation: BMET clearance, FOMEMA medical, PDOT trained\n\n"
        f"If {name} is planning 2026-2027 hiring{scale} and wants a compliance-safe alternative to "
        f"the current agency channel, I'd welcome a brief call.\n\n"
        f"{SIGNOFF}\n\n{DISCLAIMER}"
    )

    whatsapp_message = (
        f"Hello, I'm reaching out on behalf of Malaysia Corridor Ops. {angle} "
        f"We're preparing documented Bangladeshi worker channels for {sector.lower()} employers ahead of "
        f"the corridor reopening — happy to share details if useful for {name}'s 2026-2027 hiring plans. "
        f"{SIGNOFF}"
    )

    linkedin_dm = (
        f"Hi, I'm building a direct-source channel for Bangladeshi {sector.lower()} workers — RBA-aligned, "
        f"fully documented, no middlemen fees. Given the corridor reopening, would you be open to a 5-min "
        f"chat about {name}'s current hiring needs?"
    )

    return email_subject, email_body, whatsapp_message, linkedin_dm


def main():
    conn = sqlite3.connect(str(DB_PATH))
    ensure_pipeline_columns(conn)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT company_name, sector, state, city, website, phone, email,
               employees_est, priority_score, pipeline_stage
        FROM companies
        ORDER BY priority_score DESC, company_name ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    OUTREACH_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "company_name", "sector", "location", "priority_score", "pipeline_stage",
            "phone", "email", "website",
            "email_subject", "email_body", "whatsapp_message", "linkedin_dm",
        ])
        for name, sector, state, city, website, phone, email, employees, priority, stage in rows:
            location = ", ".join(p for p in (city, state) if p and p != "None") or "Malaysia"
            subject, body, wa, dm = build_messages(name, sector, city, state, employees, phone, email)
            writer.writerow([
                name, sector, location, priority, stage,
                phone or "", email or "", website or "",
                subject, body, wa, dm,
            ])

    print(f"Generated {len(rows)} outreach drafts -> {OUTPUT_PATH}")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Next: send at safe daily volumes (see content/DISTRIBUTION.md), "
          "then track replies with automation/update_pipeline.py")


if __name__ == "__main__":
    main()
