#!/usr/bin/env python3
"""Generate TOP_100_TARGETS.md from companies database"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "companies.db"
OUTPUT = BASE_DIR / "reports" / "TOP_100_TARGETS.md"

SECTOR_DESCRIPTIONS = {
    "Plantation": "Plantation companies have the largest foreign worker workforce in Malaysia. RM640/yr levy tier. CBP forced labor scrutiny on palm oil creates compliance pressure — our RBA-aligned model is a direct selling point.",
    "Rubber (Gloves)": "Glove manufacturers employ thousands of foreign workers. Top Glove's CBP WRO history means the entire sector is sensitive to worker-paid fees. RM1,850/yr levy.",
    "Electrical & Electronics": "Malaysia's largest export sector. MNCs (Intel, Micron, Bosch) have strict RBA compliance. Foreign workers in manufacturing roles. RM1,850/yr levy.",
    "Construction": "Government infrastructure projects rely on foreign labor. G7 contractors with CIDB registration. RM1,850/yr levy.",
    "Retail / Services": "Large retail chains (MR DIY, 99 Speed Mart, AEON) and hospitality (Genting) need workers for front-line and back-end roles. RM1,850/yr levy.",
    "Furniture": "Labour-intensive manufacturing, largely in Johor (Muar). RM1,850/yr levy.",
    "Agriculture": "Poultry, aquaculture, food processing. RM640/1,850 levy tier depending on subsector.",
}

HOW_TO_APPROACH_TEMPLATES = {
    "Plantation": "Call their HR department directly. Pitch: RBA-aligned recruitment, no forced labor risk. Reference: 'I see your plantation sector faces CBP scrutiny on worker fees. We offer a documented, zero-fee channel from Bangladesh.'",
    "Rubber (Gloves)": "Email HR Director. Subject: 'CBP-compliant Bangladesh worker sourcing'. Reference their WRO history and offer a clean alternative.",
    "Electrical & Electronics": "LinkedIn outreach to HR/Talent Acquisition. Pitch: 'We pre-screen and document Bangladeshi workers per RBA standards. No middleman fees, fully auditable chain.'",
    "Construction": "Call procurement or HR. Pitch: 'We can supply documented workers for your infrastructure projects. JTKSM-compliant, FWCMS-ready.'",
    "Retail / Services": "Contact HR via company website form. Pitch: 'Direct-source front-line workers from Bangladesh. Lower cost, fully documented, no agent markups.'",
    "Furniture": "Call factory directly. Ask for HR Manager. Pitch: 'We supply documented Bangladeshi workers for furniture manufacturing. Direct from source — no dalal markups.'",
    "Agriculture": "Contact operations manager. Pitch: 'Reliable Bangladeshi workers for plantation/agriculture. RBA-aligned, lower cost than current agency channel.'",
}

def get_priority_description(score):
    if score >= 90: return "CRITICAL — Large foreign workforce, high compliance pressure"
    if score >= 80: return "HIGH — Significant employer, active demand likely"
    if score >= 70: return "MEDIUM-HIGH — Good target with moderate foreign worker need"
    if score >= 60: return "MEDIUM — Potential target, needs more research"
    return "LOW — Secondary target"

def main():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Get all companies ordered by priority
    cursor.execute("""
        SELECT company_name, sector, subsector, state, city, website, phone, email,
               employees_est, compliance_pressure, levy_tier, priority_score, notes
        FROM companies
        ORDER BY priority_score DESC
    """)
    companies = cursor.fetchall()
    conn.close()
    
    # Group by tier
    tier1 = [c for c in companies if c[11] and c[11] >= 80]
    tier2 = [c for c in companies if c[11] and 65 <= c[11] < 80]
    tier3 = [c for c in companies if c[11] and 50 <= c[11] < 65]
    tier4 = [c for c in companies if not c[11] or c[11] < 50]
    
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("# TOP 100 TARGET EMPLOYERS — Malaysia Corridor\n")
        f.write("**Generated:** 2026-07-17 | **Source:** companies.db (203 companies)\n\n")
        f.write("> **Priority Formula:** Sector fit (0-25) + Active demand (0-25) + Compliance pressure (0-20) + Scale (0-15) + Contactability (0-15)\n\n")
        
        # Tier 1
        f.write("---\n\n")
        f.write("## Tier 1: Critical Targets (Score 80-100)\n\n")
        f.write(f"*{len(tier1)} companies — Large foreign workforce, high compliance pressure, active demand*\n\n")
        
        for i, c in enumerate(tier1[:30], 1):
            name, sector, subsector, state, city, website, phone, email, employees, compliance, levy, score, notes = c
            f.write(f"### {i}. {name}\n\n")
            f.write("| Field | Value |\n|-------|-------|\n")
            f.write(f"| Sector | {sector} |\n")
            f.write(f"| Location | {city}, {state} |\n")
            f.write(f"| Website | {website or 'N/A'} |\n")
            f.write(f"| Phone | {phone or 'N/A'} |\n")
            f.write(f"| Email | {email or 'N/A'} |\n")
            if employees:
                f.write(f"| Est. Employees | ~{employees:,} |\n")
            f.write(f"| Priority Score | {score}/100 |\n")
            f.write(f"| Compliance | {compliance or 'None identified'} |\n")
            f.write(f"| Levy Tier | {levy or 'RM1,850/yr'} |\n\n")
            
            # Why they're a target
            sector_desc = SECTOR_DESCRIPTIONS.get(sector, f"{sector} sector employer.")
            f.write(f"**Why they're a target:** {sector_desc}\n\n")
            
            # How to approach
            approach = HOW_TO_APPROACH_TEMPLATES.get(sector, f"Find HR contact via LinkedIn or company website. Cold outreach with value proposition.")
            f.write(f"**How to approach:** {approach}\n\n")
            f.write("---\n\n")
        
        # Tier 2
        if tier2:
            f.write("## Tier 2: High Potential (Score 65-79)\n\n")
            f.write(f"*{len(tier2)} companies — Solid targets with moderate foreign worker need*\n\n")
            for i, c in enumerate(tier2[:35], 31):
                name, sector, subsector, state, city, website, phone, email, employees, compliance, levy, score, notes = c
                f.write(f"### {i}. {name}\n")
                f.write(f"- **Sector:** {sector} | **Location:** {city}, {state} | **Score:** {score}/100\n")
                f.write(f"- **Why:** {sector} employer {('(~' + str(employees) + ' employees)') if employees else ''}\n")
                f.write(f"- **Approach:** {HOW_TO_APPROACH_TEMPLATES.get(sector, 'Cold outreach via LinkedIn/phone')}\n\n")
                f.write("---\n\n")
        
        # Tier 3 (remaining to fill to 100)
        remaining_slots = 100 - len(tier1[:30]) - len(tier2[:35])
        remaining = tier3 + tier4
        if remaining_slots > 0 and remaining:
            f.write(f"## Tier 3: Targets to Develop (Score <65)\n\n")
            f.write(f"*{min(remaining_slots, len(remaining))} companies — Need more research but worth tracking*\n\n")
            for i, c in enumerate(remaining[:remaining_slots], 31 + min(35, len(tier2))):
                name, sector, subsector, state, city, website, phone, email, employees, compliance, levy, score, notes = c
                f.write(f"### {i}. {name}\n")
                f.write(f"- **Sector:** {sector} | **Location:** {city}, {state} | **Score:** {score}/100\n")
                f.write(f"- **Notes:** {notes or 'Potential target'}\n\n")
                f.write("---\n\n")
        
        # Appendix
        f.write("\n## Appendix: Sector Summary\n\n")
        f.write("| Sector | Companies in DB | Levy Tier | Key Compliance Pressure |\n")
        f.write("|--------|----------------|-----------|------------------------|\n")
        
        cursor = conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sector, COUNT(*), 
                   COUNT(CASE WHEN compliance_pressure IS NOT NULL AND compliance_pressure != '' THEN 1 END)
            FROM companies 
            GROUP BY sector 
            ORDER BY COUNT(*) DESC
        """)
        for sector, count, compliance_count in cursor.fetchall():
            levy = "RM640/yr" if sector in ("Plantation", "Agriculture") else "RM1,850/yr"
            f.write(f"| {sector} | {count} | {levy} | {compliance_count} companies with flags |\n")
        conn.close()
    
    print(f"Generated {OUTPUT} with data from {len(companies)} companies")


if __name__ == "__main__":
    main()
