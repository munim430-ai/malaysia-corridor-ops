import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\R2_MINISTERIAL_PRESENTATION_DECK.md", "r", encoding="utf-8") as f:
    r2 = f.read()

print("--- R2 PRESENTATION DECK METRICS & OUTLINE ---")
print(f"Total characters: {len(r2):,}")
print(f"Total lines: {len(r2.splitlines())}")

# Print all slide titles
for line in r2.splitlines():
    if line.startswith("## SLIDE") or line.startswith("# "):
        print(line)
