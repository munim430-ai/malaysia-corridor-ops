import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md", "r", encoding="utf-8") as f:
    r4 = f.read()

lines = r4.splitlines()

# Print Condition 1 and Condition 6
print("--- CONDITION 1 DETAILS ---")
p = False
for l in lines:
    if "### Condition 1:" in l:
        p = True
    elif "### Condition 2:" in l:
        p = False
    if p:
        print(l)

print("\n--- POCKET RAPID-FIRE CARD EXCERPT ---")
p = False
for l in lines:
    if "# 5. PART 4: POCKET RAPID-FIRE RESPONSE CARD" in l:
        p = True
    if p:
        print(l)
