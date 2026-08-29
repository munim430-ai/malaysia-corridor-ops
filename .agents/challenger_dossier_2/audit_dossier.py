import re
import os
import glob
import sys

# Ensure UTF-8 output on Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

def audit_dossier():
    files = {
        'R1': 'dossier/R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md',
        'R2': 'dossier/R2_MINISTERIAL_PRESENTATION_DECK.md',
        'R3': 'dossier/R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md',
        'R4': 'dossier/R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md',
        'INDEX': 'dossier/EXECUTIVE_DOSSIER_INDEX.md',
        'README': 'dossier/README.md'
    }

    results = {}
    
    # 1. Check file presence and sizes
    print("=== 1. FILE INTEGRITY AUDIT ===")
    for key, path in files.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            lines = len(open(path, 'r', encoding='utf-8').readlines())
            print(f"[{key}] {path}: {lines} lines, {size} bytes - OK")
        else:
            print(f"[{key}] {path}: MISSING - FAIL")
            
    # 2. Check baseline figures consistency
    print("\n=== 2. NUMERICAL & BASELINE CONSISTENCY AUDIT ===")
    patterns = {
        'Exchange Rate 26.00': r'26\.00',
        'Govt Cap 78,990': r'78,?990',
        'Statutory Cost Floor 130,532': r'130,?532',
        'Market Extortion 540,000': r'540,?000',
        'Illicit Rent 184 Billion': r'184\s*Billion|১৮৪\s*বিলিয়ন',
        'Total Drain 216 Billion': r'216\s*Billion|২১৬\s*বিলিয়ন',
        'Hundi Flight 600M-850M': r'600M|৮৫০',
        'Clean Remittance 3.2B-4.0B': r'3\.2\s*Billion|৪\.০\s*বিলিয়ন|3\.2B'
    }
    
    for pat_name, pat in patterns.items():
        print(f"\nPattern: {pat_name}")
        for key, path in files.items():
            if not os.path.exists(path): continue
            content = open(path, 'r', encoding='utf-8').read()
            matches = len(re.findall(pat, content, re.IGNORECASE))
            print(f"  - {key}: {matches} occurrences")

    # 3. Check R4 structural elements
    print("\n=== 3. R4 MINISTERIAL DEFENSE STRUCTURAL AUDIT ===")
    r4_content = open(files['R4'], 'r', encoding='utf-8').read()
    
    # Check BAIRA narratives
    baira_narratives = [
        "Narrative 1", "Narrative 2", "Narrative 3", "Narrative 4", "Narrative 5", "Narrative 6"
    ]
    for n in baira_narratives:
        found = n in r4_content
        print(f"  - {n} present: {found}")
        
    # Check 10 Conditions
    print("\nCheck 10 Malaysian Conditions in R4:")
    for i in range(1, 11):
        cond = f"Condition {i}"
        found = cond in r4_content
        print(f"  - {cond} present: {found}")
        
    # Check 5 Diplomatic Levers
    print("\nCheck 5 Diplomatic Levers in R4:")
    levers = ["US State Department TIP", "US CBP", "EU Corporate Sustainability", "ILO Forced Labor", "Critical Labor Supply Monopoly"]
    for l in levers:
        found = any(l.lower() in line.lower() for line in r4_content.splitlines())
        print(f"  - Leverage '{l}' present: {found}")
        
    # Check 5 Phases
    print("\nCheck 5 IT Phases in R4:")
    for i in range(1, 6):
        phase = f"Phase {i}"
        found = phase in r4_content
        print(f"  - {phase} present: {found}")

    # Check Decrees in R1
    print("\n=== 4. R1 EXECUTIVE DECREES AUDIT ===")
    r1_content = open(files['R1'], 'r', encoding='utf-8').read()
    memos = ["৭৯০", "৭৯১", "৭৯২", "790", "791", "792"]
    for m in memos:
        print(f"  - Memo/Decree {m} present: {m in r1_content}")
        
if __name__ == '__main__':
    audit_dossier()
