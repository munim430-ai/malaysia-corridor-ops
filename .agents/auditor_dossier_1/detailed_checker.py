import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOSSIER_DIR = r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier"

def read_file(name):
    with open(os.path.join(DOSSIER_DIR, name), "r", encoding="utf-8") as f:
        return f.read()

r1 = read_file("R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md")
r2 = read_file("R2_MINISTERIAL_PRESENTATION_DECK.md")
r3 = read_file("R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md")
r4 = read_file("R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md")
idx = read_file("EXECUTIVE_DOSSIER_INDEX.md")
readme = read_file("README.md")

print("=" * 80)
print("DETAILED VERIFICATION OF ORIGINAL_REQUEST.MD REQUIREMENTS")
print("=" * 80)

# Check R1
print("\n--- AUDITING R1: BILINGUAL MINISTERIAL POLICY MEMO ---")
# 1. Bilingual check
has_english_memo = "PART 1: EXECUTIVE POLICY MEMORANDUM (ENGLISH)" in r1 or "PART 1:" in r1
has_bangla_memo = "PART 2: সচিবালয় নথি সারসংক্ষেপ ও সরকারি অনুশাসন" in r1 or "সচিবালয় নথি" in r1
print(f"R1 Bilingual Structure: English={has_english_memo}, Bangla={has_bangla_memo}")

# 2. Problem statement BDT 78,990 vs BDT 6.5 Lakh
has_cap = "78,990" in r1
has_extortion = "650,000" in r1 or "6.5 Lakh" in r1 or "৬.৫ লাখ" in r1
print(f"R1 Problem Statement: Cap 78,990={has_cap}, Extortion 6.5L={has_extortion}")

# 3. 5-Node Middlemen Extraction Chain
nodes_r1 = [
    "Village Dalal" in r1 or "স্থানীয় দালাল" in r1 or "Local Dalal" in r1,
    "District Sub-agent" in r1 or "জেলা সাব-এজেন্ট" in r1,
    "Dhaka Syndicate Agent" in r1 or "ঢাকা সিন্ডিকেট" in r1 or "102-Agency" in r1,
    "Malaysian Cartel Broker" in r1 or "মালয়েশিয়ান কার্টেল ব্রোকার" in r1,
    "Employer/HR Kickback" in r1 or "নিয়োগকর্তা/এইচআর কিকব্যাক" in r1 or "Employer Kickback" in r1
]
print(f"R1 5-Node Chain: {all(nodes_r1)} ({nodes_r1})")

# 4. Open Digital Clearinghouse Reform (Hybrid G2B)
has_odc_r1 = "Open Digital Clearinghouse" in r1 and ("Hybrid G2B" in r1 or "হাইব্রিড জিটুবি" in r1 or "G2B" in r1)
print(f"R1 ODC Reform (Hybrid G2B): {has_odc_r1}")

# 5. 3 Immediate Pre-MoU Executive Decrees
decrees_r1 = [
    "Decree 1" in r1 or "প্রজ্ঞাপন ১" in r1 or "অনুশাসন ১" in r1,
    "Decree 2" in r1 or "প্রজ্ঞাপন ২" in r1 or "অনুশাসন ২" in r1,
    "Decree 3" in r1 or "প্রজ্ঞাপন ৩" in r1 or "অনুশাসন ৩" in r1
]
print(f"R1 3 Executive Decrees: {all(decrees_r1)} ({decrees_r1})")

# Check R2
print("\n--- AUDITING R2: 10-SLIDE PRESENTATION DECK ---")
slide_matches = re.findall(r"##\s*SLIDE\s*(\d+):", r2)
print(f"R2 Slides Found: {slide_matches} (Count: {len(slide_matches)})")

# Check elements per slide
for i in range(1, 11):
    slide_pattern = rf"##\s*SLIDE\s*{i}:(.*?)(?=##\s*SLIDE\s*\d+:|$)"
    match = re.search(slide_pattern, r2, re.DOTALL)
    if match:
        content = match.group(1)
        has_headline = "Slide Headline" in content or "Headline" in content
        has_visual = "Visual Layout" in content or "Data Graphic" in content or "Visual Blueprint" in content
        has_talk = "Talk Track" in content or "Verbatim" in content
        has_transition = "Transition Line" in content or i == 10  # Slide 10 may have closing instead
        has_takeaway = "Takeaway" in content or "Core Data" in content
        print(f"  Slide {i:2d}: Headline={has_headline}, Visual={has_visual}, TalkTrack={has_talk}, Takeaway={has_takeaway}, Transition={has_transition}")
    else:
        print(f"  Slide {i:2d}: MISSING!")

# Check legacy & economic themes in R2
has_3b = "$3" in r2 or "3.2B" in r2 or "3.5B" in r2 or "3 Billion" in r2
has_tip = "TIP" in r2 and ("Tier 2" in r2 or "Tier-2" in r2)
has_1500_rls = "1,500" in r2
print(f"R2 Themes: $3B+ Remittances={has_3b}, US TIP Tier 2={has_tip}, 1500+ RLs={has_1500_rls}")

# Check R3
print("\n--- AUDITING R3: OPERATIONAL & MATHEMATICAL ARCHITECTURE WHITEPAPER ---")
# 1. Cost floor vs market extortion
has_cost_floor = "130,532" in r3 or "8,065" in r3 or "5,020" in r3
has_leakage = "409,468" in r3 or "500,000" in r3 or "5 Lakh" in r3 or "519,468" in r3
print(f"R3 Cost Floor ({has_cost_floor}) & Leakage ({has_leakage})")

# 2. Financial audit line items
items_r3 = ["Levy", "FWCMS", "Medical", "Visa", "Airfare", "BMET", "Insurance", "Agency Fee"]
items_found = {item: (item.lower() in r3.lower()) for item in items_r3}
print(f"R3 Financial Line Items: {all(items_found.values())} -> {items_found}")

# 3. Technical Blueprint components
has_direct_sourcing = "Direct Digital" in r3 or "Worker Sourcing" in r3
has_cbma = "Centralized Blind Medical" in r3 or "CBMA" in r3
has_pkb = "Probashi Kallyan Bank" in r3 and ("0-Cash" in r3 or "Zero-Upfront" in r3 or "Zero Upfront" in r3 or "Escrow" in r3)
has_fwcms_turap = "FWCMS" in r3 and "TURAP" in r3
print(f"R3 Tech Blueprint: Direct Sourcing={has_direct_sourcing}, CBMA={has_cbma}, PKB Escrow={has_pkb}, FWCMS/TURAP={has_fwcms_turap}")

# Check R4
print("\n--- AUDITING R4: MINISTERIAL DEFENSE & COUNTER-ARGUMENTS ---")
# 1. BAIRA syndicate lobbyist rebuttals
has_baira = "BAIRA" in r4 and ("102" in r4 or "Syndicate" in r4)
print(f"R4 BAIRA 102 Lobby Rebuttals: {has_baira}")

# 2. 10 Malaysian Restrictive Conditions
cond_matches = re.findall(r"Condition\s*(\d+)[:\s]", r4)
print(f"R4 10 Conditions Count: {len(set(cond_matches))} (Conditions found: {sorted(list(set(map(int, cond_matches))))})")

# 3. Bureaucracy IT feasibility
has_bureaucracy = "Bureaucracy" in r4 or "Civil Service" in r4 or "Operational IT Feasibility" in r4
print(f"R4 Bureaucracy IT Defense: {has_bureaucracy}")

# Check Cross-Document Consistency
print("\n--- CROSS-DOCUMENT FINANCIAL & FACTUAL CONSISTENCY ---")
docs = {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "INDEX": idx, "README": readme}
metrics = {
    "BDT 78,990 (Cap)": "78,990",
    "BDT 130,532 (Floor)": "130,532",
    "BDT 540,000 (Extortion Low)": "540,000",
    "BDT 650,000 (Extortion High)": "650,000",
    "BDT 409,468 (Leakage)": "409,468",
    "1 MYR = 26 BDT": ["26 BDT", "26.00 BDT", "26.0 BDT", "RM 1 = BDT 26", "1 MYR = 26", "1 MYR = BDT 26"],
    "400,000 Workers": "400,000",
    "BDT 184 Billion (Rent)": "184 Billion"
}

for label, pat in metrics.items():
    res = {}
    for dname, dtext in docs.items():
        if isinstance(pat, list):
            res[dname] = any(p in dtext for p in pat)
        else:
            res[dname] = pat in dtext
    print(f"  {label:30s}: " + ", ".join([f"{k}={'YES' if v else 'NO'}" for k, v in res.items()]))

print("\n" + "=" * 80)
print("AUDIT SCRIPT EXECUTION FINISHED")
print("=" * 80)
