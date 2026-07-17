# RESUME_STATE — Malaysia Corridor Ops

**Last session:** July 17, 2026
**Branch:** claude/business-plan-prompt-ofvzxk (open draft PR #1, not yet merged to master)
**Remote:** https://github.com/munim430-ai/malaysia-corridor-ops

## Completed

### Website (Full Stack)
- `site/index.html` — Bengali worker funnel (FAQ, cost table, CTA)
- `site/employers/index.html` — English employer portal (compliance, process, costs)
- `site/corridor-tracker/index.html` — SEO blog hub with 5 posts
- 5 blog posts: TURAP, FWCMS eQuota, Corridor Reopening, Section 60K, KESUMA eQuota
- `site/assets/` — styles.css, script.js, logo.svg, qr-flyer.svg, 5 placeholder SVGs
- `site/404.html`, `site/robots.txt`, `site/sitemap.xml`

### Database
- `data/companies.db` — **505 companies** across 13 sectors
  - Manufacturing: 109 | E&E: 74 | Services: 60 | Construction: 58
  - Plantation: 42 | Property: 30 | Hospitality: 27 | Retail: 24 | +5 more sectors
- **75 companies with phone, 37 with email** (full contact_enricher.py run, 2026-07-17 — up from 46/27)
- `data/companies.csv` — exported CSV
- Live pipeline CRM (Google Sheet): https://docs.google.com/spreadsheets/d/1EDFGwoo15CYUp7MrfcnxO2ISdP4c6fRd4dbXpSUA1oo/edit

### Reports
- `reports/RED_TEAM_REPORT.md` — 13 assumptions attacked
- `reports/QUOTA_WATCH.md` — full timeline + 3 scenarios
- `reports/TOP_100_TARGETS.md` — ranked employer list (generated from initial 203)
- `reports/MASTER_REPORT.md` — full stack inventory
- `content/DISTRIBUTION.md` — 6-channel zero-cost marketing playbook

### Infrastructure
- `.github/workflows/deploy.yml` — GH Pages deploy + weekly scraper + weekly outreach queue regen
- GitHub Pages: **confirmed live** at https://munim430-ai.github.io/malaysia-corridor-ops/ (verified 2026-07-17 — Bengali worker funnel renders correctly)
- GoatCounter analytics configured in `script.js`
- WhatsApp floating button on all pages

### Business Plan & Automation (this session)
- `BUSINESS_PLAN.md` — actionable, start-today plan synthesizing all reports
- `MASTER_PROMPT.md` — pasteable AI operations prompt with full business context
- `WORKER_INTAKE_SETUP.md` — 15-min guide to wire the site's placeholder form/WhatsApp links live (**not yet done** — still placeholders as of this session)
- `automation/generate_outreach.py` + `automation/update_pipeline.py` — outreach drafting + lightweight CRM
- **15 real Gmail drafts created** (not sent) for the top 15 highest-priority companies with a known email — sitting in the operator's Gmail Drafts folder, ready to review and send
- **Live Google Sheet CRM** mirroring `companies.db`'s pipeline: https://docs.google.com/spreadsheets/d/1EDFGwoo15CYUp7MrfcnxO2ISdP4c6fRd4dbXpSUA1oo/edit
- PR #1 open (draft): https://github.com/munim430-ai/malaysia-corridor-ops/pull/1

## Remaining / Deferred

| Task | Priority | Notes |
|------|----------|-------|
| Review and send the 15 Gmail drafts | High | Sitting in Drafts, un-sent by design — human judgment call on final send |
| Merge PR #1 | High | Business plan + automation, currently a draft PR |
| Wire real Google Form + WhatsApp number | High | Site links are still placeholders — see `WORKER_INTAKE_SETUP.md` |
| Secure umbrella BMET RL agreement | Critical | The one task automation can't do — needs real relationships in Dhaka |
| Keep expanding phone/email coverage | Medium | 75/505 phone, 37/505 email so far — re-run `contact_enricher.py` periodically |
| Post in BD worker FB groups | Low | Site is live — can start now |
| Set up Telegram channel | Low | `t.me/malaysia_corridor_ops` |
| Monitor corridor reopening | Ongoing | Track FWCMS eQuota backlog, MoU progress via `reports/QUOTA_WATCH.md` |

## Key Commands
```bash
# Run scrapers
python scrapers/scraper_runner.py

# Run contact enricher (generous timeout)
python scrapers/contact_enricher.py

# Verify deployment
# Visit: https://munim430-ai.github.io/malaysia-corridor-ops/

# Update CSV export
# (run inline: select * from companies; export to csv)
```

## Legal
Corridor closed since June 2024. Reopening terms pending official MoU. This is an information & registration service only. No visa/job/placement guarantees.
