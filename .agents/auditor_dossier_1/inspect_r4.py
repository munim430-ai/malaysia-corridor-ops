import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md", "r", encoding="utf-8") as f:
    r4 = f.read()

print("--- R4 DEFENSE DOSSIER METRICS & OUTLINE ---")
print(f"Total characters: {len(r4):,}")
print(f"Total lines: {len(r4.splitlines())}")

# Print major headings
for line in r4.splitlines():
    if line.startswith("# ") or line.startswith("## ") or line.startswith("### "):
        print(line)
