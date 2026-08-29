import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOSSIER_DIR = r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier"

files = [
    "EXECUTIVE_DOSSIER_INDEX.md",
    "R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md",
    "R2_MINISTERIAL_PRESENTATION_DECK.md",
    "R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md",
    "R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md",
    "README.md"
]

print("=" * 80)
print("FORENSIC INTEGRITY AUDIT - AUTOMATED INSPECTION SUITE")
print("=" * 80)

# Check 1: File Existence & Basic Metrics
print("\n[CHECK 1] Deliverable File Metrics & Existence:")
total_bytes = 0
total_lines = 0
file_contents = {}

for f in files:
    path = os.path.join(DOSSIER_DIR, f)
    if not os.path.exists(path):
        print(f"FAIL: File missing: {f}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
        file_contents[f] = content
        lines = content.splitlines()
        words = len(content.split())
        bytes_len = len(content.encode("utf-8"))
        total_bytes += bytes_len
        total_lines += len(lines)
        print(f" - {f}: {len(lines)} lines | {words} words | {bytes_len:,} bytes")

print(f"\nTotal Aggregate Dossier Size: {total_lines} lines | {total_bytes:,} bytes (~{total_bytes/1024:.1f} KB)")

# Check 2: Prohibited Pattern & Placeholder Scan
print("\n[CHECK 2] Prohibited Pattern & Placeholder Scan:")
placeholder_patterns = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bXXX\b",
    r"\bYYY\b",
    r"\bTBD\b",
    r"\[insert\b",
    r"\[placeholder\b",
    r"lorem\s+ipsum",
    r"draft\s+only",
    r"to\s+be\s+determined",
    r"to\s+be\s+added"
]

violation_count = 0
for f, content in file_contents.items():
    for pattern in placeholder_patterns:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            for m in matches:
                line_no = content[:m.start()].count("\n") + 1
                snippet = content[max(0, m.start()-30):min(len(content), m.end()+30)].replace("\n", " ")
                print(f"FLAG in {f} line {line_no} matching '{pattern}': ...{snippet}...")
                violation_count += 1

if violation_count == 0:
    print("PASS: Zero placeholder, TODO, FIXME, or dummy patterns detected.")
else:
    print(f"FAIL: {violation_count} potential placeholder occurrences found.")

# Check 3: Administrative Bengali Terminology in R1
print("\n[CHECK 3] Administrative Bengali Terminology in R1:")
r1_content = file_contents.get("R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md", "")
bengali_terms = [
    ("নথি (Note-sheet)", "নথি"),
    ("সারসংক্ষেপ (Summary)", "সারসংক্ষেপ"),
    ("স্মারক (Memo Number)", "স্মারক"),
    ("অনুশাসন (Executive Orders/Decrees)", "অনুশাসন"),
    ("প্রবাসী কল্যাণ ও বৈদেশিক কর্মসংস্থান মন্ত্রণালয়", "প্রবাসী কল্যাণ ও বৈদেশিক কর্মসংস্থান মন্ত্রণালয়"),
    ("জনশক্তি কর্মসংস্থান ও প্রশিক্ষণ ব্যুরো (BMET)", "জনশক্তি কর্মসংস্থান ও প্রশিক্ষণ ব্যুরো"),
    ("বৈদেশিক কর্মসংস্থান ও অভিবাসী আইন, ২০১৩", "বৈদেশিক কর্মসংস্থান ও অভিবাসী আইন"),
    ("রিক্রুটিং এজেন্সি (Recruiting Agency)", "রিক্রুটিং এজেন্সি"),
    ("সিন্ডিকেট (Syndicate)", "সিন্ডিকেট"),
    ("দালাল (Middlemen)", "দালাল"),
    ("প্রবাসী কল্যাণ ব্যাংক (PKB)", "প্রবাসী কল্যাণ ব্যাংক"),
    ("ব্লাইন্ড মেডিকেল (Blind Medical)", "ব্লাইন্ড মেডিকেল")
]

for name, term in bengali_terms:
    count = r1_content.count(term)
    print(f"  - '{name}': {count} occurrences in R1")

# Check 4: Check Slide Structure in R2
print("\n[CHECK 4] R2 Slide Structure Verification:")
r2_content = file_contents.get("R2_MINISTERIAL_PRESENTATION_DECK.md", "")
slides = re.findall(r"(?:###?\s*Slide\s*(\d+)[:\s\-]|--- Slide (\d+) ---)", r2_content, re.IGNORECASE)
slide_nums = [int(s[0] or s[1]) for s in slides if (s[0] or s[1])]
slide_unique = sorted(list(set(slide_nums)))
print(f"  - Slides identified in R2: {slide_unique} (Total unique: {len(slide_unique)})")

slide_required_elements = ["Verbatim Talk Track", "Visual Blueprint", "Key Takeaway", "Transition Line"]
for elem in slide_required_elements:
    c = len(re.findall(re.escape(elem), r2_content, re.IGNORECASE))
    print(f"  - Element '{elem}': {c} occurrences in R2")

# Check 5: Check R3 Mathematical & Technical Sections
print("\n[CHECK 5] R3 Operational & Mathematical Sections Verification:")
r3_content = file_contents.get("R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md", "")
r3_sections = [
    "Mathematical Decomposition",
    "Cost Floor",
    "Extortion Leakage",
    "Centralized Blind Medical Allocation",
    "Probashi Kallyan Bank",
    "Open Digital Clearinghouse",
    "FWCMS",
    "TURAP",
    "OpenAPI"
]
for sec in r3_sections:
    c = len(re.findall(re.escape(sec), r3_content, re.IGNORECASE))
    print(f"  - Section/Concept '{sec}': {c} occurrences in R3")

# Check 6: Check R4 Counter-Arguments & Conditions
print("\n[CHECK 6] R4 Rebuttal & Counter-Argument Structure:")
r4_content = file_contents.get("R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md", "")
r4_sections = [
    "BAIRA",
    "102",
    "Condition 1",
    "Condition 2",
    "Condition 3",
    "Condition 4",
    "Condition 5",
    "Condition 6",
    "Condition 7",
    "Condition 8",
    "Condition 9",
    "Condition 10",
    "Bureaucracy",
    "IT Feasibility",
    "Pocket Battle Card"
]
for sec in r4_sections:
    c = len(re.findall(re.escape(sec), r4_content, re.IGNORECASE))
    print(f"  - Element '{sec}': {c} occurrences in R4")

print("\n" + "=" * 80)
print("AUDIT SCRIPT COMPLETED SUCCESSFULLY")
print("=" * 80)
