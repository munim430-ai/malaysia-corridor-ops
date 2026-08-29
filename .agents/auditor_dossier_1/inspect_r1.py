import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"R1 Total lines: {len(lines)}")
print("First 40 lines:")
for l in lines[:40]:
    print(l, end="")

print("\n--- Searching for Part headers ---")
for i, l in enumerate(lines):
    if l.startswith("#"):
        print(f"Line {i+1}: {l.strip()}")
