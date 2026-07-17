# RESUME_STATE — Malaysia Corridor Ops

**Last session:** July 17, 2026
**Branch:** master (2 commits)
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
- 46 companies with phone, 27 with email (quick enrichment)
- `data/companies.csv` — exported CSV

### Reports
- `reports/RED_TEAM_REPORT.md` — 13 assumptions attacked
- `reports/QUOTA_WATCH.md` — full timeline + 3 scenarios
- `reports/TOP_100_TARGETS.md` — ranked employer list (generated from initial 203)
- `reports/MASTER_REPORT.md` — full stack inventory
- `content/DISTRIBUTION.md` — 6-channel zero-cost marketing playbook

### Infrastructure
- `.github/workflows/deploy.yml` — GH Pages deploy + weekly scraper
- GitHub Pages: auto-deploys on push to master (action configures `site/` as root)
- GoatCounter analytics configured in `script.js`
- WhatsApp floating button on all pages

## Remaining / Deferred

| Task | Priority | Notes |
|------|----------|-------|
| Run full contact enricher | Medium | Needs 10+ min timeout, scrapes 100+ websites |
| Verify GH Pages live URL | Medium | Check `munim430-ai.github.io/malaysia-corridor-ops/` after deploy action completes |
| Update TOP_100_TARGETS.md | Low | Generated from initial 203 companies; now 505 |
| Post in BD worker FB groups | Low | Wait until site is verified live |
| Set up Telegram channel | Low | `t.me/malaysia_corridor_ops` |
| Monitor corridor reopening | Ongoing | Track FWCMS eQuota backlog, MoU progress |

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
