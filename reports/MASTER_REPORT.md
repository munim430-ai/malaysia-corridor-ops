# Malaysia Corridor Ops — Master Report

**Date:** July 2026  
**Status:** Pre-Launch (Corridor Closed)  
**Corridor Status:** CLOSED since June 1, 2024 — 31+ months  
**Wait Mode:** Active preparation for reopening

---

## 1. Executive Summary

Malaysia Corridor Ops is a zero-cost, pre-launch intelligence and registration platform for the Malaysia-Bangladesh labour corridor. While the corridor remains closed (since June 2024), we have built the full infrastructure — employer database, compliance research, marketing plan, and bilingual website — so that when the MoU is signed, we can deploy immediately.

**Core thesis:** The post-reopening recruitment landscape will be fundamentally different — digital, employer-pays, tightly regulated. The old agent-based model (6-7 lakh BDT fees, middlemen, no documentation) is dying. Our model (direct, documented, RBA-aligned, digital-first) is built for the new era.

---

## 2. Current Inventory

| Asset | File | Status |
|-------|------|--------|
| Research database | `data/companies.db` | 203 companies, 13 sectors |
| CSV export | `data/companies.csv` | Generated |
| Scraper engine | `scrapers/scraper_runner.py` | 9 scraper classes |
| Contact enrichment | `scrapers/contact_enricher.py` | Built, not yet run |
| Top 100 targets | `reports/TOP_100_TARGETS.md` | Generated from 203 companies |
| Red team report | `reports/RED_TEAM_REPORT.md` | 13 assumptions attacked |
| Corridor watch | `reports/QUOTA_WATCH.md` | Full timeline + 3 scenarios |
| Bengali worker site | `site/index.html` | Live (GH Pages pre-deploy) |
| English employer site | `site/employers/index.html` | Live (GH Pages pre-deploy) |
| Corridor tracker | `site/corridor-tracker/index.html` | Live with 5 blog posts |
| Blog posts | 5 SEO articles | turap, fwcms, reopening, s60k, kesuma |
| Design system | `site/assets/styles.css` | Mobile-first, <3s 3G |
| Marketing playbook | `content/DISTRIBUTION.md` | Zero-cost, 6 channels |
| Assumptions doc | `ASSUMPTIONS.md` | 13 assumption inventory |
| Blockers log | `BLOCKERS.md` | Current constraints |

---

## 3. Database Composition (203 Companies)

| Sector | Count | Key Sub-Sectors |
|--------|-------|-----------------|
| E&E | 65 | Electronics manufacturing, semiconductors |
| Construction | 32 | Building, infrastructure, civil works |
| Plantation | 18 | Palm oil, rubber estates |
| Furniture | 17 | Wood, rattan, office furniture |
| General Manufacturing | 16 | Plastic, metal, packaging |
| Electrical & Electronics | 15 | Cables, components, switchgear |
| Retail | 12 | Hypermarkets, department stores |
| Rubber | 6 | Gloves, tyres, industrial rubber |
| Hospitality | 6 | Hotels, resorts |
| Agriculture | 5 | Livestock, aquaculture, crops |
| Services | 4 | Cleaning, facilities, logistics |
| Security | 4 | Guard services, surveillance |
| Property | 3 | Development, management |

**Target: 500 companies** — need ~300 more, especially in services, logistics, hospitality, and SME manufacturing.

---

## 4. Compliance Landscape

### Key Developments (2024-2026)

| Date | Event | Impact |
|------|-------|--------|
| Jun 2024 | Corridor closed | All recruitment frozen |
| Jan 2025 | EPF 2+2 for foreign workers | Higher employer costs |
| Apr 2025 | BD clears syndicate agents | Old system dismantled |
| Apr 2026 | Employer Pays Principle agreed | Zero-fee to workers |
| 22 Jun 2026 | PM Tarique visits KL | Cultural MoU signed, labour MoU pending |
| 6 Jul 2026 | KESUMA centralizes to FWCMS eQuota | 22,476 pending apps from 548 companies |

### Three Key Risks

1. **TURAP platform** — Bestinet's proposed $1,000/worker fee could reshape cost structure. NOT approved yet. HR Minister refuted adoption.
2. **10 conditions for agencies** — Only 5-7 BD agencies likely qualify (3K+ workers/5yr, training centre, 10K sq ft office).
3. **Timeline uncertainty** — Best case: late 2026. Base case: early 2027. Worst case: late 2027+.

---

## 5. Marketing & Distribution

### Channels (Zero-Cost)

| Channel | Target | Content |
|---------|--------|---------|
| Facebook Groups (BD workers) | 50+ groups | Bengali posts about corridor updates |
| TikTok | Young workers (18-30) | Short videos explaining the process |
| LinkedIn | Malaysian HR managers | Employer-pays compliance content |
| WhatsApp | Workers + employers | Direct registration via wa.me |
| Telegram | Channel members | Daily corridor reopening updates |
| Referral | Existing contacts | Word-of-mouth in villages |

### SEO Strategy

5 blog posts targeting keywords:
- "TURAP Malaysia" — recruitment platform
- "FWCMS eQuota" — quota system
- "corridor reopening" — timeline
- "Section 60K Malaysia" — employer approval
- "KESUMA eQuota" — policy change

---

## 6. Website Architecture

```
site/
├── index.html                     # Bengali worker portal (funnel)
├── 404.html                       # Not found page
├── robots.txt                     # SEO
├── sitemap.xml                    # SEO
├── assets/
│   ├── styles.css                 # Design system
│   ├── script.js                  # FAQ accordion + GoatCounter
│   ├── logo.svg                   # Brand logo
│   ├── qr-flyer.svg               # QR code print flyer
│   ├── placeholder-turap.svg      # Blog card images
│   ├── placeholder-fwcms.svg      #
│   ├── placeholder-timeline.svg   #
│   ├── placeholder-section60k.svg #
│   └── placeholder-kesuma.svg     #
├── employers/
│   └── index.html                 # English employer portal
└── corridor-tracker/
    ├── index.html                 # Blog hub
    ├── turap-malaysia-guide.html  # SEO blog post
    ├── fwcms-equota-guide.html    # SEO blog post
    ├── corridor-reopening.html    # SEO blog post
    ├── section-60k.html           # SEO blog post
    └── kesuma-equota.html         # SEO blog post
```

### Design Stats
- **GoatCounter** analytics (free, privacy-first)
- **WhatsApp** floating button on all pages
- **Mobile-first** CSS, <3s on 3G
- **Bengali** (Noto Sans Bengali) + **English** (Inter) fonts
- Zero JavaScript dependencies — vanilla JS only

---

## 7. Financial Structure

### Cost Breakdown (per worker)

| Component | Market Rate | Our Target |
|-----------|------------|------------|
| Levy (mfg) | RM 1,850/yr | RM 1,850 |
| FWCMS processing | RM 215 | RM 215 |
| VDR visa fee | RM 250 | RM 250 |
| FOMEMA medical | RM 250 | RM 250 |
| Insurance | RM 500 | RM 500 |
| Airfare | RM 1,200 | RM 1,000 |
| Security bond | RM 500 | RM 500 |
| BD processing | BDT 80,000 | BDT 60,000 |
| **TOTAL** | **~RM 9,465 / ~6.5L BDT** | **~RM 8,065 / ~3.0L BDT** |

**Savings: ~54% (BDT 3.5 lakh per worker)**

### Revenue Model
- **Not yet defined** — corridor must reopen first
- Possible models: employer-side consulting fee, per-worker processing fee, or SaaS platform subscription
- Zero cost to workers (Employer Pays Principle mandate)

---

## 8. Immediate Next Steps (Priority Order)

| # | Task | Status | Owner |
|---|------|--------|-------|
| 1 | Commit & push to GitHub | 🔜 Ready | Sisyphus |
| 2 | Verify GH Pages deploy works | 🔜 Ready | Sisyphus |
| 3 | Run contact enricher (~100+ contacts) | ⏳ Pending | Scraper |
| 4 | Add 300+ more companies (target: 500) | ⏳ Pending | Scraper |
| 5 | Generate QR flyer for offline distribution | ✅ Done | — |
| 6 | Post in BD worker FB groups | ⏳ Post-launch | Manual |
| 7 | Set up Telegram channel automation | ⏳ Post-launch | Manual |
| 8 | Monitor FWCMS backlog weekly | ⏳ Ongoing | Manual |
| 9 | Update when labour MoU is signed | ⏳ Trigger | Manual |

---

## 9. Key Metrics Dashboard

| Metric | Current | Target |
|--------|---------|--------|
| Companies in database | 203 | 500 |
| Companies with phone/email | 0 | 200 |
| Top 100 targets documented | ✅ 100 | 100 |
| Red team findings resolved | 13/13 | 13 |
| Blog posts published | 5 | 5 |
| Website pages live | 8 | 8 |
| GoatCounter analytics | ✅ Setup | Active |
| GH Pages deployment | ⏳ Pending | ✅ Done |
| First commit | ⏳ Pending | ✅ Done |

---

## 10. Legal & Risk

**Disclaimer:** All content is informational. The corridor is closed. No visa, job, or recruitment guarantees are made. No payments are collected through this site. Verify all details with official government sources.

**Key risks:**
- Corridor reopening delay beyond 2027
- TURAP cost structure makes model uneconomical
- Competitor (established agencies) enter digital space first
- Regulatory changes in either country
- Limited capital for pre-launch operations

---

*Report generated July 2026. Next update: upon corridor reopening announcement or major policy change.*
