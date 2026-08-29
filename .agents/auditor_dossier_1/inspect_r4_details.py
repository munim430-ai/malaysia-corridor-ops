import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md", "r", encoding="utf-8") as f:
    r4 = f.read()

lines = r4.splitlines()

print("--- R4 10 MALAYSIAN CONDITIONS SUMMARY ---")
start = False
for l in lines:
    if "### Condition " in l:
        print(l)
    elif "### 3.2 The 5 Strategic Diplomatic Leverage Points" in l:
        print(l)
    elif "## 4.2 Phased 5-Stage Transition Plan" in l:
        print(l)
    elif "# 5. PART 4: POCKET RAPID-FIRE RESPONSE CARD" in l:
        print(l)
