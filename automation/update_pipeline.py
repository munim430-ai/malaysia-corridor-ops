#!/usr/bin/env python3
"""
Malaysia Corridor Ops — Pipeline Tracker
==========================================
Lightweight CRM for the employer outreach queue. Tracks each company in
data/companies.db through: not_contacted -> contacted -> replied -> interested
-> converted / dead.

Usage:
    python automation/update_pipeline.py update "FGV Holdings Bhd" contacted --channel whatsapp
    python automation/update_pipeline.py summary
"""

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "companies.db"

STAGES = ["not_contacted", "contacted", "replied", "interested", "converted", "dead"]


def update_stage(company_name, stage, channel):
    if stage not in STAGES:
        raise SystemExit(f"Unknown stage '{stage}'. Valid stages: {', '.join(STAGES)}")

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM companies WHERE company_name = ?", (company_name,))
    match = cursor.fetchall()

    if not match:
        conn.close()
        raise SystemExit(f"No company found matching '{company_name}'. Check spelling against data/companies.csv.")
    if len(match) > 1:
        conn.close()
        raise SystemExit(f"'{company_name}' matches {len(match)} rows — use the exact name from data/companies.csv.")

    cursor.execute(
        "UPDATE companies SET pipeline_stage = ?, last_contacted = ?, outreach_channel = ? WHERE company_name = ?",
        (stage, datetime.now().strftime("%Y-%m-%d"), channel, company_name),
    )
    conn.commit()
    conn.close()
    print(f"Updated '{company_name}' -> {stage} ({channel or 'no channel specified'})")


def print_summary():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(companies)")
    if "pipeline_stage" not in {row[1] for row in cursor.fetchall()}:
        conn.close()
        raise SystemExit("No pipeline data yet — run automation/generate_outreach.py first.")

    cursor.execute("""
        SELECT COALESCE(pipeline_stage, 'not_contacted'), COUNT(*)
        FROM companies
        GROUP BY COALESCE(pipeline_stage, 'not_contacted')
    """)
    counts = dict(cursor.fetchall())
    conn.close()

    total = sum(counts.values())
    print(f"Pipeline summary — {total} companies\n")
    for stage in STAGES:
        n = counts.get(stage, 0)
        pct = (n / total * 100) if total else 0
        print(f"  {stage:<14} {n:>4}  ({pct:5.1f}%)")


def main():
    parser = argparse.ArgumentParser(description="Track employer outreach pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    upd = sub.add_parser("update", help="Update a company's pipeline stage")
    upd.add_argument("company_name")
    upd.add_argument("stage", choices=STAGES)
    upd.add_argument("--channel", default="", help="e.g. whatsapp, email, linkedin, phone")

    sub.add_parser("summary", help="Print pipeline funnel summary")

    args = parser.parse_args()
    if args.command == "update":
        update_stage(args.company_name, args.stage, args.channel)
    elif args.command == "summary":
        print_summary()


if __name__ == "__main__":
    main()
