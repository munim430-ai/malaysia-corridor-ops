# Malaysia Corridor Ops — Outreach Playbook
## Complete B2B Outreach System for Malaysian Employer Acquisition

---

## 🎯 Executive Summary

**Goal:** Build a pipeline of 100+ qualified Malaysian employers ready to hire Bangladesh workers when the corridor reopens (est. Q1 2027).

**Current State:** 505 companies in DB → Target: 1,000+ with 60%+ contact coverage

**Strategy:** Multi-channel lead gen → CRM pipeline → Automated outreach → Manual closing

---

## 📊 Target Market Analysis

### Total Addressable Market (Malaysia)

| Segment | Companies | Foreign Workers | Priority |
|---------|-----------|-----------------|----------|
| **Plantation** (Palm oil) | 500-800 | 40,000-60,000 | 🔥 **HIGHEST** |
| **Manufacturing** (E&E, Gloves, Auto) | 2,000-3,000 | 100,000+ | 🔥 **HIGH** |
| **Construction** (CIDB G7) | 300-500 | 25,000-35,000 | 🔥 **HIGH** |
| **Services** (Cleaning, Security, Logistics) | 2,000-4,000 | 30,000-50,000 | 📈 **MEDIUM** |
| **Hospitality/Retail** | 1,500-2,500 | 15,000-25,000 | 📈 **MEDIUM** |

**Key Insight:** 650 companies drive 90% of hiring volume. Focus there.

---

## 🔍 Lead Generation Channels

### 1. Government/Industry Directories (Highest Quality)

| Source | URL | Target Companies | Frequency |
|--------|-----|------------------|-----------|
| **FMM** (Manufacturing) | fmm.org.my/members-directory | 13,200 members | Monthly |
| **MATRADE** (Exporters) | matrade.gov.my/en/directory | 5,000+ exporters | Monthly |
| **MPOB** (Plantations) | mpob.gov.my | 150+ large estates | Monthly |
| **CIDB** (Construction) | cidb.gov.my | 2,500+ G7 contractors | Monthly |
| **SME Corp** | smecorp.gov.my | 900k SMEs | Quarterly |

**Automation:** `outreach/lead_sources.py` → `DirectoryAggregator` runs monthly via GitHub Actions

### 2. Job Portals (Hiring Intent Signals)

| Portal | Keywords | Signal |
|--------|----------|--------|
| **JobStreet** | manufacturing, construction, plantation, hospitality | Active hiring = budget approved |
| **Indeed MY** | same + cleaning, security, logistics | High volume = expansion |
| **Maukerja** | blue-collar specific | Direct worker demand |

**Signal:** Companies posting 5+ blue-collar roles = high probability of foreign worker need

### 3. News Monitoring (Expansion Triggers)

| Source | Keywords | Action |
|--------|----------|--------|
| The Edge Markets | "new factory", "expansion", "groundbreaking", "investment" | Immediate outreach |
| The Star Business | "capacity expansion", "new plant", "hiring" | Same week |
| FMT Business | "Bangladesh workers", "foreign workers", "FWCMS" | Same day |
| Malay Mail | "manpower", "labor shortage" | Same week |

**Automation:** `NewsSource` in `lead_sources.py` runs weekly

---

## 📈 CRM Pipeline Stages

```
NEW → CONTACTED → QUALIFIED → PROPOSAL → NEGOTIATION → WON
                    ↓
              NURTURING (stalled)
```

### Stage Definitions & Requirements

| Stage | Probability | Requirements to Enter | Actions |
|-------|-------------|----------------------|---------|
| **NEW** | 5% | Lead created in CRM | Auto-enroll in cold sequence |
| **CONTACTED** | 10% | ≥1 activity (email/call) | Track opens/clicks |
| **QUALIFIED** | 25% | Contact identified + need confirmed + budget ≥RM10k/yr | Discovery call, send case study |
| **PROPOSAL** | 50% | Proposal sent + decision maker engaged | Follow up day 1, 3, 7, 14 |
| **NEGOTIATION** | 75% | Terms discussed + decision maker committed | Legal review, pilot agreement |
| **WON** | 100% | Contract signed + deposit received | Onboard, schedule first deployment |
| **LOST** | 0% | Reason recorded | Move to nurture (quarterly check-in) |
| **NURTURING** | 5% | Stalled >30 days | Quarterly value email |

---

## 📧 Email Sequences by Industry

### Manufacturing/E&E (5-touch + breakup)

| Touch | Day | Template | Goal |
|-------|-----|----------|------|
| 1 | 0 | `cold_manufacturing_1` | Problem awareness (quota backlog) |
| 2 | 3 | `cold_manufacturing_2` | Urgency (KESUMA centralization) |
| 3 | 7 | `cold_manufacturing_3` | Social proof (3 Penang, 2 Johor clients) |
| 4 | 14 | `cold_manufacturing_4` | Zero-risk offer (reserve now, pay on arrival) |
| 5 | 21 | `cold_manufacturing_breakup` | Close file, leave door open |

**Metrics Target:** 25% open, 5% reply, 2% meeting booked

### Construction (4-touch + breakup)

| Touch | Day | Template | Angle |
|-------|-----|----------|-------|
| 1 | 0 | `cold_construction_1` | Project delay cost (LDs = RM400K/mo) |
| 2 | 4 | `cold_construction_2` | Peer proof (Selangor G7 contractor) |
| 3 | 7 | `cold_construction_3` | Final push (Q1 2027 window) |
| 4 | 14 | `cold_construction_breakup` | Close file |

### Plantation (4-touch + breakup)

| Touch | Day | Template | Angle |
|-------|-----|----------|-------|
| 1 | 0 | `cold_plantation_1` | RM640 levy advantage + EUDR compliance |
| 2 | 4 | `cold_plantation_2` | FIFO queue (FGV/Sime/IOI already registered) |
| 3 | 10 | `cold_plantation_3` | Final window (Jan 2027 deployment) |
| 4 | 20 | `cold_plantation_breakup` | Close file |

---

## 🤖 Automation Architecture

### n8n Workflows (`outreach/n8n_workflows/`)

| Workflow | File | Trigger | Actions |
|----------|------|---------|---------|
| **Cold Manufacturing** | `cold_outreach_manufacturing.json` | New lead (industry=manufacturing) | 5-email sequence, CRM logging, reply detection |
| **Cold Construction/Plantation** | `cold_outreach_construction_plantation.json` | New lead (construction/plantation) | 4-email sequence, industry branching |
| **Warm Nurture** | (to create) | Lead status = nurturing | Quarterly value emails |
| **Proposal Follow-up** | (to create) | Deal stage = proposal | Day 1, 3, 7, 14 follow-ups |

### GitHub Actions Pipeline (`.github/workflows/scraper_enrichment.yml`)

| Schedule | Jobs |
|----------|------|
| **Sunday 02:00 UTC** | Scrape → Enrich → Reports → CRM Sync → Deploy |
| **Wednesday 14:00 UTC** | Enrich → Reports → Deploy |
| **Manual** | Any subset (scrape/enrich/reports/crm-sync) |

**Jobs:**
1. `scrape-companies` - Runs `scraper_runner.py`
2. `enrich-contacts` - Runs `company_enricher.py` (parallel, 30 workers)
3. `generate-reports` - Runs `report_generator.py --all`
4. `crm-sync` - Imports to CRM, scores leads, creates sequences
5. `deploy-site` - GitHub Pages with updated `stats.json`
6. `health-check` - Pipeline metrics, alerts if concerning

---

## 📊 Conversion Metrics & Targets

### Weekly Dashboard

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| **New Leads Added** | 50/week | < 20 |
| **Leads Contacted** | 100% within 24h | Any uncontacted >48h |
| **Email Open Rate** | 25% | < 15% |
| **Email Reply Rate** | 5% | < 2% |
| **Meetings Booked** | 10/week | < 5 |
| **Proposals Sent** | 5/week | < 2 |
| **Deals Won** | 2/month | 0 for 60 days |
| **Pipeline Value (Weighted)** | RM500K+ | < RM200K |
| **Win Rate** | 20%+ | < 10% |

### Monthly Cohort Analysis

Track: `Leads added in Month X → Meetings in Month X+1 → Proposals in X+2 → Wins in X+3`

---

## 🎯 Objection Handling Playbook

| Objection | Response | Proof Point |
|-----------|----------|-------------|
| **"Corridor closed / no timeline"** | "KESUMA centralized quota July 6. 22,476 applications pending. MoU negotiations active. We position you *before* opening." | Show KESUMA July 6 announcement |
| **"We use local agencies"** | "Local agencies use same FWCMS quota. We source *direct* from Bangladesh villages — lower cost, pre-screened, faster deployment." | Show village coordinator network |
| **"Too risky / workers run away"** | "Pre-departure FOMEMA + family consent + village guarantor = <3% absconding vs industry 15%." | Show absconding rate data |
| **"No budget / freeze"** | "Zero cost to reserve. Standard agency fee (RM5-8k) only on *successful arrival*. Reserve now = priority when quota opens." | Show reservation agreement |
| **"We'll wait for corridor to open"** | "FIFO processing: 22,476 applications queued. Early registrants deploy Jan 2027. Late registrants deploy Apr+." | Show FWCMS queue data |
| **"Need board approval"** | "We provide board-ready deck: cost comparison, risk mitigation, compliance checklist. 1-pager for decision makers." | Send board deck template |

---

## 📞 Call Script Framework

### Discovery Call (15 min)

**Opening (2 min):**
> "Thanks for taking the call. I'm [Name] from Malaysia Corridor Ops. We help Malaysian employers in [industry] secure Bangladesh workforce *before* the corridor reopens. Not selling today — just understanding your manpower plan for 2027."

**Discovery (8 min):**
1. "What's your current foreign worker count?"
2. "Any roles you struggle to fill locally?"
3. "What's your experience with Bangladesh workers?"
3. "When do you expect to need next batch?"
4. "Who handles recruitment decisions?"

**Qualification (3 min):**
- Need confirmed? → Budget ≥RM10k/yr? → Decision maker identified?
- If YES → "I'll send a 1-pager with worker profiles matching your roles. Can we review Thursday?"
- If NO → "Fair enough. I'll add you to our quarterly corridor update. Only 4 emails/year."

**Close (2 min):**
> "Based on what you shared, I think we can help with [specific roles]. I'll send the profile sheet and a 15-min calendar invite for Thursday. Sound good?"

---

## 📋 Lead Scoring Model

| Factor | Weight | Scoring |
|--------|--------|---------|
| **Industry** | 25% | Plantation=25, Manufacturing=20, Construction=18, Services=8 |
| **Company Size** | 15% | 1000+=20, 500-999=18, 200-499=15, 50-199=10, <50=5 |
| **Foreign Worker Track Record** | 20% | 500+=25, 100-499=20, 20-99=10, 0=5 |
| **Contact Quality** | 15% | HR email=15, phone=10, general email=5, none=0 |
| **Scraper Priority** | 10% | priority_score/10 |
| **Engagement** | 15% | Reply=30, Meeting=25, Click=10, Open=5 |

**Score → Action:**
- **80-100:** Hot → Immediate call + proposal prep
- **60-79:** Warm → Sequence + call within 1 week
- **40-59:** Cool → Nurture sequence + monthly check
- **<40:** Cold → Quarterly newsletter only

---

## 🛠️ Tool Stack

| Function | Tool | Cost |
|----------|------|------|
| **CRM/Database** | SQLite (local) + GitHub sync | Free |
| **Email Sending** | SMTP (Gmail/Outlook) or SendGrid | Free tier / $15/mo |
| **Automation** | n8n (self-hosted) | Free |
| **Scraping** | Python (aiohttp, BeautifulSoup) | Free |
| **Enrichment** | Company website scraping | Free |
| **Analytics** | GitHub Actions + custom Python | Free |
| **Hosting** | GitHub Pages (site) + GitHub Actions (compute) | Free |

**Total Monthly Cost: $0-15** (SendGrid if >100 emails/day)

---

## 🚀 30-Day Launch Plan

### Week 1: Foundation
- [ ] Deploy CRM (`python crm/models.py --init`)
- [ ] Import existing 505 companies (`python crm/models.py --import-csv data/companies.csv`)
- [ ] Score all leads (`python crm/pipeline.py --score-all`)
- [ ] Create default sequences (`python crm/pipeline.py --create-sequences`)
- [ ] Deploy n8n workflows (import JSON files)

### Week 2: Outreach Engine
- [ ] Configure SMTP credentials in n8n
- [ ] Test all 4 email sequences (manufacturing, construction, plantation, nurture)
- [ ] Set up reply tracking webhook
- [ ] Run first enrichment batch (`python scrapers/company_enricher.py --priority-only`)

### Week 3: First Campaign
- [ ] Segment top 100 leads by industry
- [ ] Launch manufacturing sequence (30 leads)
- [ ] Launch construction sequence (20 leads)
- [ ] Launch plantation sequence (15 leads)
- [ ] Daily: Monitor replies, book meetings

### Week 4: Optimize & Scale
- [ ] Review Week 3 metrics
- [ ] A/B test subject lines
- [ ] Refine sequences based on replies
- [ ] Run full directory scrape (FMM, MATRADE, MPOB, CIDB)
- [ ] Enroll 200+ new leads in sequences

---

## 📈 90-Day Targets

| Month | Leads in Pipeline | Meetings | Proposals | Wins | Revenue (Weighted) |
|-------|-------------------|----------|-----------|------|-------------------|
| **Month 1** | 300 | 20 | 5 | 0 | RM100K |
| **Month 2** | 600 | 50 | 15 | 2 | RM500K |
| **Month 3** | 1,000 | 100 | 30 | 5 | RM1.5M |

**Revenue per Win:** RM50K-200K/year (agency margin on 10-50 workers)

---

## ⚠️ Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Corridor stays closed >2027 | Medium | High | Build revenue from consulting/visa services |
| Email deliverability drops | Medium | High | Warm up domains, rotate IPs, SPF/DKIM/DMARC |
| Competitor enters with lower price | High | Medium | Differentiate on compliance + village network |
| Key team member leaves | Low | High | Document all processes, cross-train |
| Regulatory change (MoU terms) | Medium | High | Monitor KESUMA/MOHR weekly via news automation |

---

## 📞 Contact & Escalation

| Role | Responsibility | Contact |
|------|----------------|---------|
| **Outreach Lead** | Campaign strategy, sequence optimization | [You] |
| **CRM Admin** | Data quality, pipeline hygiene, scoring | [You/Assistant] |
| **Technical** | Scrapers, n8n, GitHub Actions, email infra | [You/Dev] |
| **Legal/Compliance** | BMET/FOMEMA/FWCMS process, contracts | External counsel |

---

## 📎 Appendix: File Inventory

```
malaysia-corridor-ops/
├── scrapers/
│   ├── scraper_runner.py          # Main scraper (10 sources, 505 companies)
│   ├── company_enricher.py        # Async contact extraction (30 parallel)
│   ├── report_generator.py        # Auto-reports (DB_SNAPSHOT, SECTOR, CONTACTS)
│   └── db_tools.py                # Dedup, rescore, validate, export
├── crm/
│   ├── models.py                  # Company, Contact, Lead, Activity, Deal
│   └── pipeline.py                # Scoring, stages, forecasting, sequences
├── outreach/
│   ├── lead_sources.py            # Multi-channel (dirs, jobs, news)
│   ├── n8n_workflows/
│   │   ├── cold_outreach_manufacturing.json
│   │   └── cold_outreach_construction_plantation.json
│   └── email_templates/
│       ├── cold_manufacturing_1-5.txt
│       ├── cold_construction_1-4.txt
│       └── cold_plantation_1-4.txt
├── .github/workflows/
│   ├── scraper_enrichment.yml     # Weekly automation
│   └── augmented.yml              # Full pipeline
├── data/
│   ├── companies.db               # Main SQLite (505 companies)
│   ├── companies.csv              # Export
│   ├── companies_enriched.csv     # Latest contacts
│   ├── crm.db                     # CRM pipeline
│   └── stats.json                 # Live site embedding
├── reports/
│   ├── DB_SNAPSHOT.md
│   ├── SECTOR_ANALYSIS.md
│   ├── CONTACT_ENRICHMENT.md
│   └── MASTER_REPORT.md
└── README_OUTREACH.md             # This file
```

---

*Last Updated: July 2026 | Version 1.0 | Malaysia Corridor Ops*