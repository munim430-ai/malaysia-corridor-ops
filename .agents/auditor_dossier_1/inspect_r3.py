import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md", "r", encoding="utf-8") as f:
    r3 = f.read()

print("--- R3 WHITEPAPER METRICS & OUTLINE ---")
print(f"Total characters: {len(r3):,}")
print(f"Total lines: {len(r3.splitlines())}")

# Print major headings
for line in r3.splitlines():
    if line.startswith("# ") or line.startswith("## ") or line.startswith("### "):
        print(line)
