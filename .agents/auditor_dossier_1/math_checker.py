import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOSSIER_DIR = r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier"

files = {
    "R1": "R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md",
    "R2": "R2_MINISTERIAL_PRESENTATION_DECK.md",
    "R3": "R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md",
    "R4": "R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md",
    "INDEX": "EXECUTIVE_DOSSIER_INDEX.md",
    "README": "README.md"
}

contents = {}
for k, fname in files.items():
    with open(os.path.join(DOSSIER_DIR, fname), "r", encoding="utf-8") as f:
        contents[k] = f.read()

print("=" * 80)
print("DEEP MATHEMATICAL & NUMERICAL INTEGRITY VERIFICATION")
print("=" * 80)

# Check line-item table in R3
print("\n--- LINE-ITEM AUDIT IN R3 ---")
r3 = contents["R3"]
# Extract table lines
table_lines = [l for l in r3.splitlines() if l.startswith("| **A.") or l.startswith("| **B.") or l.startswith("| **C.")]
for tl in table_lines:
    print(tl)

# Check 5-node leakage breakdown in R3
print("\n--- 5-NODE LEAKAGE BREAKDOWN IN R3 ---")
for l in r3.splitlines():
    if "Node 1" in l or "Node 2" in l or "Node 3" in l or "Node 4" in l or "Node 5" in l:
        print(l)

# Check presence of key macro metrics in R1, R2, R3, R4, INDEX, README
print("\n--- MACRO METRIC PRESENCE MATRIX ---")
metrics = [
    ("Gazetted Cap BDT 78,990", r"78[,.]?990"),
    ("Statutory Floor BDT 130,532", r"130[,.]?532"),
    ("Statutory Floor RM 5,020", r"5[,.]?020"),
    ("Extortion Avg BDT 540,000", r"540[,.]?000"),
    ("Extortion High BDT 650,000", r"650[,.]?000"),
    ("Extortion BDT 6.5 Lakh", r"6\.5\s*Lakh|৬\.৫\s*লাখ"),
    ("Leakage BDT 409,468", r"409[,.]?468"),
    ("Exchange Rate 1 MYR = 26 BDT", r"26(?:\.00)?\s*BDT|BDT\s*26(?:\.00)?"),
    ("Aggregate Extortion BDT 216B / $1.83B", r"216\s*Billion|1\.83\s*Billion|২১৬\s*বিলিয়ন|১\.৮৩\s*বিলিয়ন"),
    ("Syndicate Rent BDT 184B", r"184\s*Billion|১৮৪\s*বিলিয়ন"),
    ("Hundi Drainage $600M-$850M", r"600M|850M|৬০০.*৮৫০\s*মিলিয়ন"),
    ("Clean Remittances $3.2B-$4.0B", r"3\.2\s*Billion|4\.0\s*Billion|3\.2B|4\.0B|৩\.২.*৪\.০\s*বিলিয়ন")
]

for label, pattern in metrics:
    print(f"\nMetric: {label}")
    for doc_name, text in contents.items():
        found = bool(re.search(pattern, text, re.IGNORECASE))
        print(f"  {doc_name:6s}: {'[OK]' if found else '[NOT PRESENT]'}")

print("\n" + "=" * 80)
