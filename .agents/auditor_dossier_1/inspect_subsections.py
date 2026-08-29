import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOSSIER_DIR = r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier"

with open(os.path.join(DOSSIER_DIR, "R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md"), "r", encoding="utf-8") as f:
    r1 = f.read()

print("--- R1 SECTION TITLES ---")
for line in r1.splitlines():
    if line.startswith("#"):
        print(line)

print("\n--- R1 5-NODE SEARCH ---")
for m in re.finditer(r"(?:Node\s*[1-5]|স্তর\s*[১-৫]|১\.|২\.|৩\.|৪\.|৫\.).*", r1):
    print(m.group(0)[:100])

with open(os.path.join(DOSSIER_DIR, "R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md"), "r", encoding="utf-8") as f:
    r3 = f.read()

print("\n--- R3 LINE ITEMS SEARCH ---")
for line in r3.splitlines():
    if any(k in line.lower() for k in ["fee", "charge", "service", "bmet", "levy", "airfare"]):
        if "|" in line or "BDT" in line or "RM" in line:
            print(line[:120])
