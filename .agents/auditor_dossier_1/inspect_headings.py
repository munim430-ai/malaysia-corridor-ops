import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOSSIER_DIR = r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier"

files = [
    "R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md",
    "R2_MINISTERIAL_PRESENTATION_DECK.md",
    "R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md",
    "R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md",
    "EXECUTIVE_DOSSIER_INDEX.md",
    "README.md"
]

for f in files:
    path = os.path.join(DOSSIER_DIR, f)
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    print("=" * 80)
    print(f"FILE: {f}")
    print("=" * 80)
    headings = [line for line in content.splitlines() if line.startswith("#")]
    for h in headings[:25]:
        print(f"  {h}")
    if len(headings) > 25:
        print(f"  ... and {len(headings)-25} more headings")
    print()
