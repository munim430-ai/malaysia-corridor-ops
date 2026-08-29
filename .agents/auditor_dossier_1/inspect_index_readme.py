import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\EXECUTIVE_DOSSIER_INDEX.md", "r", encoding="utf-8") as f:
    idx = f.read()

print("--- EXECUTIVE DOSSIER INDEX ---")
print(f"Total lines: {len(idx.splitlines())}")
for line in idx.splitlines():
    if line.startswith("#"):
        print(line)

with open(r"C:\Users\HP\.gemini\antigravity\scratch\malaysia-corridor-ops\dossier\README.md", "r", encoding="utf-8") as f:
    readme = f.read()

print("\n--- README ---")
print(f"Total lines: {len(readme.splitlines())}")
for line in readme.splitlines():
    if line.startswith("#"):
        print(line)
