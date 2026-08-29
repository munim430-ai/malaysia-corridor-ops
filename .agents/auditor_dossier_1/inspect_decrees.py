import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md", "r", encoding="utf-8") as f:
    r1 = f.read()

lines = r1.splitlines()

print("--- R1 ENGLISH DECREES ---")
start_en = False
for l in lines:
    if "THREE (3) IMMEDIATE BINDING MINISTERIAL EXECUTIVE DECREES" in l:
        start_en = True
    if "MINISTERIAL ACTION & APPROVAL REQUEST" in l:
        start_en = False
    if start_en:
        print(l)

print("\n--- R1 BANGLA DECREES ---")
start_bn = False
for l in lines:
    if "৩টি বাধ্যতামূলক প্রজ্ঞাপন ও প্রশাসনিক অনুশাসন" in l:
        start_bn = True
    if "অনুমোদন ও সিদ্ধান্ত প্রস্তাবনা" in l:
        start_bn = False
    if start_bn:
        print(l)
