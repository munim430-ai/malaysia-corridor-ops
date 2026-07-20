# 🇧🇩→🇲🇾 Malaysia Corridor Ops — Zero-Cost Launch Stack

**Complete launch stack for a Bangladesh-to-Malaysia manpower venture.**

The labor corridor is reopening after its June 2024 closure. This repo builds the entire operational, legal, marketing, and intelligence foundation at **zero cost** before the first worker departs.

---

## What's Here

| Directory | Contents |
|-----------|----------|
| `BUSINESS_PLAN.md` | The actionable business plan — start here |
| `MASTER_PROMPT.md` | Reusable AI operations prompt — paste into any AI assistant to run outreach/content tasks with full context |
| `WORKER_INTAKE_SETUP.md` | 15-minute guide to wire the site's placeholder form/WhatsApp links to a live intake pipeline |
| `/reports/` | RED_TEAM_REPORT, TOP_100_TARGETS, QUOTA_WATCH, MASTER_REPORT |
| `/site/` | GitHub Pages marketing site (Bengali + English, 4 pages, 5 SEO posts) |
| `/data/` | companies.db (SQLite), companies.csv, scraper outputs |
| `/scrapers/` | Python scrapers for employer intelligence |
| `/automation/` | Outreach message generator + pipeline/CRM tracker for the 505-company database |
| `/outreach/` | Generated, ready-to-send outreach queue (email/WhatsApp/LinkedIn per company) |
| `/content/` | Marketing copy, email templates, social scripts, flyer assets |

## Live Site

**[→ Visit Malaysia Corridor Ops](https://[your-org].github.io/malaysia-corridor-ops/)**

| Page | Language | Purpose |
|------|----------|---------|
| `/` | Bengali | Worker registration & waitlist funnel |
| `/employers/` | English | Malaysian employer acquisition |
| `/corridor-tracker/` | English | SEO blog + reopening updates |

## Key Deliverables

1. **RED TEAM REPORT** — 13 assumptions attacked with evidence, verdicts, corrections
2. **TOP 100 TARGETS** — Ranked Malaysian employer list with approach playbook
3. **QUOTA WATCH** — Live corridor reopening tracker with dated sources
4. **DISTRIBUTION PLAYBOOK** — Zero-cost marketing channels (Facebook groups, TikTok, LinkedIn, WhatsApp)
5. **MASTER REPORT** — 30-day action plan merging all intelligence

## Legal Disclaimer

> Corridor closed since June 2024; reopening terms pending official MoU between Bangladesh and Malaysia. This is an **information & registration service only**. We do not guarantee visas, jobs, or recruitment outcomes. No payments are collected through this site.

## Tech Stack

| Layer | Tool | Cost |
|-------|------|------|
| Hosting | GitHub Pages | Free |
| Analytics | GoatCounter | Free |
| Forms | Google Forms | Free |
| Chat | wa.me (WhatsApp) | Free |
| Database | SQLite | Free |
| Scrapers | Python + requests/BS4 | Free |
| CI/CD | GitHub Actions | Free |

## Quick Start

```bash
git clone https://github.com/[your-org]/malaysia-corridor-ops
cd malaysia-corridor-ops
pip install -r requirements.txt
python scrapers/scraper_runner.py       # Run all scrapers
python automation/generate_outreach.py  # Generate outreach queue for all 505 companies
python automation/update_pipeline.py summary  # Check pipeline funnel
```

Read `BUSINESS_PLAN.md` first, then `WORKER_INTAKE_SETUP.md` to wire the live site.

## Repository Structure

```
malaysia-corridor-ops/
├── BUSINESS_PLAN.md         # The actionable business plan
├── MASTER_PROMPT.md         # Reusable AI operations prompt
├── WORKER_INTAKE_SETUP.md   # Wire the live intake pipeline (15 min)
├── ASSUMPTIONS.md          # All business/technical assumptions
├── BLOCKERS.md             # Active blockers & workarounds
├── progress.db             # SQLite checkpoint database
├── RESUME_STATE.md         # Session continuation state
├── automation/
│   ├── generate_outreach.py        # Drafts email/WhatsApp/LinkedIn per company
│   └── update_pipeline.py          # Lightweight CRM: track outreach status
├── outreach/
│   └── outreach_queue.csv          # Generated outreach drafts (505 companies)
├── data/
│   ├── corridor_intel.md           # Corridor reopening intelligence
│   ├── visa_requirements.md         # Malaysian visa specs
│   ├── bmet_process.md              # BMET worker deployment flow
│   └── agency_licensing.md          # RL requirements
├── reports/
│   ├── RED_TEAM_REPORT.md          # Full red team analysis (13 attacks)
│   ├── TOP_100_TARGETS.md          # Ranked employer targets
│   ├── QUOTA_WATCH.md              # Corridor reopening tracker
│   └── MASTER_REPORT.md            # 30-day action plan
├── site/                           # GitHub Pages website
│   ├── index.html                  # Bengali worker funnel
│   ├── employers/index.html        # English employer funnel
│   ├── corridor-tracker/           # SEO blog + calendar
│   └── assets/                     # CSS, JS, logos, flyers
├── scrapers/                       # Python scraping scripts
│   ├── scraper_runner.py           # Employer database orchestrator
│   └── demand_letter_scraper.py    # Async: BMET circulars/notices + OEP clearance data
│                                   #   for Malaysia-specific quota/demand-letter documents
│                                   #   (see file docstring for corrected target list + setup)
├── content/
│   └── DISTRIBUTION.md             # Zero-cost marketing playbook
└── requirements.txt                # Python dependencies
```
