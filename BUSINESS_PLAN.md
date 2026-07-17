# BUSINESS PLAN — Malaysia Corridor Ops
**Bangladesh → Malaysia Labour Corridor: Compliance & Processing Venture**

**Version:** 1.0 | **Date:** 2026-07-17 | **Status:** Pre-launch, corridor closed, actively preparing
**Owner:** mu8210112@gmail.com

> This plan consolidates `RED_TEAM_REPORT.md`, `QUOTA_WATCH.md`, `MASTER_REPORT.md`, `TOP_100_TARGETS.md`, `content/DISTRIBUTION.md`, `ASSUMPTIONS.md`, and `BLOCKERS.md` into one execution document. Every number below traces back to one of those files — see them for sourcing and citations. This is the version you act on starting today.

---

## 1. Executive Summary

The Malaysia–Bangladesh labour corridor has been closed to new recruitment since June 1, 2024. It is reopening — Bangladesh's PM visited Kuala Lumpur on June 22, 2026 to request it, both governments agreed in April 2026 to an **Employer Pays Principle**, and Malaysia centralized all quota processing into a single digital system (FWCMS eQuota) on July 6, 2026. No labour MoU is signed yet. Best-case reopening is Q4 2026; base case is Q1 2027.

**The old model — worker pays 6-7 lakh BDT (~RM25,000-40,000) to a chain of village agents and BAIRA-licensed recruiters — is ending.** Regulatory pressure (CBP Withhold Release Orders, RBA zero-fee codes, the bilateral Employer Pays agreement) is forcing the industry toward a documented, digital, low-fee model. That shift is the opportunity.

**This venture's position:** a Bangladesh-side compliance and processing partner — not a middleman, not a matchmaker — that plugs into whatever the new system turns out to be (FWCMS, possibly TURAP), handles the eight functions no Malaysian platform can do from Kuala Lumpur (BMET registration, medical, PDOT training, village sourcing, document collection, financing coordination, arrival handling, bank guarantees), and sells on **transparency and documentation**, not just price.

**Revenue is dual-track:**
- **Worker-pays** (construction, plantation, SMEs where employer-pays is slow to arrive): launch at **3.0–3.5 lakh BDT** per worker, still ~50% below market, with sustainable margin (see §6).
- **Employer-pays** (electronics, gloves — sectors already under CBP/RBA pressure): a per-worker processing/compliance fee charged to the Malaysian employer, zero cost to the worker.

**What's already built, at zero cost:** a bilingual marketing site (Bengali worker funnel + English employer portal) live-deployable on GitHub Pages, a 505-company Malaysian employer database with sector/compliance scoring, 5 SEO blog posts, and a 6-channel zero-cost distribution playbook. What's new in this plan: the automation to actually run outreach against that database (§8), a reusable AI operations prompt (`MASTER_PROMPT.md`) to keep executing without re-deriving context every session, and the concrete first-30-days checklist below.

**The corridor being closed is not a blocker to starting.** Everything in this plan except actually deploying workers can — and should — start today.

---

## 2. Market Situation (as of 2026-07-17)

| Fact | Status |
|---|---|
| Corridor closed for new BD recruitment | Since 2024-06-01 (31+ months) |
| Cultural MoU signed (Tarique KL visit) | 2026-06-22 |
| Labour MoU | **Not signed.** No confirmed date. |
| Employer Pays Principle | Bilaterally agreed, 2026-04-09 |
| FWCMS eQuota centralization | 2026-07-06 — 22,476 pending applications / 548 companies |
| FWCMS fee | RM215/worker (confirmed, current) |
| TURAP (Bestinet's proposed platform) | **Not approved.** Proposed at $1,000/worker + 1 month salary, 12-year contract. HR Minister has publicly denied Cabinet has seen it. |
| Malaysia's "10 conditions" for agencies | Proposed: 3,000+ workers/5yr track record, own training centre, 10,000 sq ft office — would qualify only 5–7 of the 102 incumbent BAIRA agencies |

**Reopening scenarios** (from `RED_TEAM_REPORT.md`, Attack 3):

| Scenario | Probability | What it means for us |
|---|---|---|
| A — Confined to 5–7 qualifying agencies | 45% | Cannot enter directly. Umbrella agreement with a qualifying RL holder, 30–50% revenue share. |
| B — Bangladesh negotiates relaxed conditions, open pool | 35% | Get our own BMET Recruiting Licence (RL), compete directly. |
| C — BOESL-led government-to-government channel | 20% | Become BOESL's outsourcing/service partner. |

**Base-case timeline:** labour MoU Q3–Q4 2026, 10-conditions relaxation negotiation Q3 2026, first new worker batch departs Q1 2027 (base case). **This plan is built to survive a 12-month delay without revenue**, because that is the single highest-probability failure mode identified in the red team exercise (Attack 11, risk 9/10).

---

## 3. Business Model

### 3.1 What we are
A **Bangladesh-side compliance and processing partner**, positioned to Malaysian employers as "the TURAP/FWCMS-compatible fulfilment arm" and to Bangladeshi workers as "the transparent, direct, no-dalal channel." We do not claim to be a matchmaker if the eventual platform (TURAP or otherwise) handles matching — we own everything that platform cannot do from Malaysia.

### 3.2 The eight functions only a BD-side partner can perform
1. BMET registration & smart card
2. Pre-departure medical (BMET-approved centres)
3. PDOT (Pre-Departure Orientation Training)
4. Village-level worker sourcing
5. Document collection (passport, police clearance, certificates)
6. Worker financing / microfinance coordination (BRAC, ASA, Grameen)
7. Arrival handling (KLIA pickup, transit, transport)
8. Bank guarantee processing

### 3.3 Legal structure — start without a licence, grow into one
Per `RED_TEAM_REPORT.md` Attack 9, four structures, in order of how soon they're usable:

1. **Now, zero licence needed:** Information & registration service only — no recruiting, no money collection. This is what the current site already is. Legal today.
2. **Soon:** Umbrella agreement with an existing BMET Recruiting Licence (RL) holder — 30–50% revenue share, standard industry practice. This is the fastest path to actually processing workers once the corridor opens, and it's also the answer to Scenario A above.
3. **Medium-term:** Malaysia entity (SSM company + KDN agency registration) + Bangladesh sourcing arm operating as "overseas principal" rather than "recruiting agency."
4. **At scale:** Apply for our own BMET RL (~BDT 5–8 lakh + bank guarantee, ~6 months). Only worth it once volume justifies it — this is the Scenario B answer.

**Action this quarter:** start conversations with 2–3 respected, mid-sized BMET RL holders (not one of the giant BAIRA incumbents — a smaller, reputation-conscious one) about an umbrella deal. This is the single highest-leverage non-technical task in this plan and cannot be automated — it needs a real relationship.

### 3.4 Pricing
Per `RED_TEAM_REPORT.md` Attack 2 — full cost breakdown in §6 below.

| Segment | Price to worker | Employer fee | Notes |
|---|---|---|---|
| Worker-pays (construction, plantation, SME) | 3.0–3.5 lakh BDT launch, target 2.5 lakh at scale (500+/yr) | — | Still ~50% below the market's 6–7 lakh |
| Employer-pays (E&E, gloves, RBA/CBP-exposed) | 0 (by design — that's the selling point) | Per-worker compliance/processing fee, negotiated | Sell to compliance-pressured HR/procurement, not price-shop |

### 3.5 Differentiation — not price, documentation
Incumbents can and will drop prices temporarily to kill new entrants (Attack 12, confirmed, risk 7/10) — they have 300-400% margin at market rates to play with. **Do not compete on price alone.** Compete on:
- Full BMET/FOMEMA/FWCMS documentation chain, auditable
- RBA-alignment as a sellable compliance feature, not a cost
- Zero worker-paid fees on the employer-pays track (directly solves the CBP/RBA problem incumbents can't)
- Transparent, published cost breakdown (already on the site) — incumbents' opacity is their weakness

---

## 4. Target Market

### 4.1 Employers — 505 companies scored and in `data/companies.db`

| Sector | Count | Levy tier | Compliance flags |
|---|---|---|---|
| Manufacturing | 109 | RM1,850/yr | 2 |
| E&E | 74 | RM1,850/yr | 60 |
| Services | 66 | RM1,850/yr | 0 |
| Construction | 58 | RM1,850/yr | 16 |
| Plantation | 42 | RM640/yr | 5 |
| Property | 33 | RM1,850/yr | 0 |
| Hospitality | 27 | RM1,850/yr | 0 |
| Retail | 24 | RM1,850/yr | 0 |
| Agriculture | 19 | RM640/yr | 0 |
| Furniture | 17 | RM1,850/yr | 0 |
| Electrical & Electronics | 15 | RM1,850/yr | 0 |
| Security | 14 | RM1,850/yr | 0 |
| Rubber | 7 | RM1,850/yr | 0 |

Full ranked list with approach scripts: `reports/TOP_100_TARGETS.md`. Priority formula: sector fit + active demand + compliance pressure + scale + contactability.

### 4.2 Who to approach first (Attack 13 — don't fight for the big fish)
1. **SMEs (100–500 workers)** ignored by the big BAIRA agencies
2. **New factories / 2025-2026 expansions** with no existing agency relationship (Infineon, Intel expansions and similar)
3. **CBP/RBA-exposed companies** (glove sector post-Top Glove WRO, E&E exporters) — they need a clean channel *now*, and switching partners is less costly for them than the compliance risk
4. Large incumbents-locked employers (Top Glove, FGV, Sime Darby) — **only after** 6+ months of documented SME deployments to point to as case studies

### 4.3 Workers
Bangladeshi workers currently paying 6–7 lakh BDT through village agents, primarily reached through Facebook groups, TikTok, WhatsApp, and referral networks (full channel breakdown in `content/DISTRIBUTION.md`). At 2.5–3.5 lakh BDT, a worker on a typical RM2,000/month Malaysian salary can repay their migration cost in 6-9 months via BRAC/ASA/Grameen migration loans, versus 18-24 months at market rate.

---

## 5. Go-to-Market (zero cost, already designed)

Full playbook: `content/DISTRIBUTION.md`. Summary:

| Channel | Audience | 30-day target | Cost |
|---|---|---|---|
| Facebook groups (10 identified, ~2.4M combined members) | Workers | 500 signups | $0 |
| TikTok/Shorts (5 scripts written, Bengali + English) | Workers 18-30 | 50K views | $0 |
| LinkedIn (50/week outreach, templates written) | Malaysian HR | 50 employer contacts | $0 |
| WhatsApp broadcast (scripts written, BD + MY) | Both | 200 signups | $0 |
| Telegram channel | Workers | 1,000 members | $0 |
| Referral program (tiered: 5 refs = free PDOT, 10 = free FOMEMA) | Returning workers | 100 signups | $0 |
| SEO blog (5 posts live) | Both, organic search | 500 visitors | $0 |
| QR flyer, printed | Offline, BMET office | 50 signups | ~$5 |

**Target: 1,400 worker signups + 50 employer contacts in 30 days for under $5 total spend.**

---

## 6. Financial Model

### 6.1 Cost floor per worker (from Attack 2, full sourcing there)

| Side | Component | Cost |
|---|---|---|
| Malaysia | Levy (mfg/construction/services) | RM1,850/yr (RM640/yr plantation/agri) |
| Malaysia | FWCMS processing | RM215 |
| Malaysia | VDR visa fee | ~RM250 |
| Malaysia | FOMEMA medical | ~RM180-250 |
| Malaysia | Insurance (FWCS+SKHPPA) | ~RM500/yr |
| Malaysia | Airfare (KL-Dhaka-KL) | ~RM1,000-1,200 |
| Malaysia | Security bond (refundable) | ~RM500 |
| **Malaysia subtotal** | | **~RM4,200-4,750 (BDT 71,000-81,000)** |
| Bangladesh | BMET clearance/smart card | BDT 10,000-15,000 |
| Bangladesh | Medical (approved centre) | BDT 8,000-12,000 |
| Bangladesh | PDOT training | BDT 5,000-8,000 |
| Bangladesh | Passport | BDT 5,000 |
| Bangladesh | Police clearance | BDT 1,000 |
| Bangladesh | Welfare Board fee | BDT 5,000-7,000 |
| Bangladesh | Village sourcing/agent commission | BDT 20,000-30,000 |
| Bangladesh | Bank guarantee/insurance | BDT 5,000 |
| **Bangladesh subtotal** | | **BDT 59,000-83,000** |
| **Total cost floor** | | **BDT 130,000-164,000 (RM7,600-9,600)** |

### 6.2 Margin by price point

| Launch price | Gross margin/worker | Margin % | Verdict |
|---|---|---|---|
| 2.5 lakh BDT | BDT 86,000-120,000 | 51-73% | Too thin as a launch price — risk from unforeseen costs |
| **3.0 lakh BDT (recommended launch)** | **BDT 136,000-170,000** | **83-104%** | Sustainable, still 54% below market |
| 6.5 lakh BDT (current market rate) | BDT 486,000-520,000 | 296-400% | Incumbent exploit pricing — what we're displacing |

**TURAP risk:** if Bestinet's proposed $1,000/worker + 1-month-salary fee is adopted, it roughly doubles the Malaysia-side cost floor. Treat as a separate line-item risk to monitor (Cabinet has not approved it as of this writing), not a baseline assumption.

### 6.3 Revenue projection (illustrative, base case, corridor opens Q1 2027)

| Milestone | Workers/month | Monthly gross margin (at 3.0 lakh BDT, BDT→RM ≈ 17.4) |
|---|---|---|
| Month 1-3 post-launch | 10 | RM 50,000-59,000 |
| Month 4-6 | 30 | RM 150,000-177,000 |
| Month 7-12 | 75 | RM 375,000-442,000 |

These are directional, not audited — treat as a planning floor, revisit against actual conversion once the corridor reopens and real BD-side processing costs are confirmed (several line items above are still market estimates, not contracted rates — see `ASSUMPTIONS.md` A1-A2).

### 6.4 Burn rate: keep it at $0
Every tool in the stack (GitHub Pages, GoatCounter, Google Forms, SQLite, WhatsApp click-to-chat, Telegram) is free-tier. There is no reason to spend money before the corridor reopens. The only recurring cost target during pre-launch is $0; the only planned spend is ~$5 for printed QR flyers.

---

## 7. Risk Register

From `RED_TEAM_REPORT.md` and `BLOCKERS.md`, ranked by severity:

| Risk | Severity | Mitigation |
|---|---|---|
| Corridor delayed 12+ months, no revenue window | CRITICAL (9/10) | Zero burn rate; use the wait to build SEO authority, waitlist, employer relationships, and secure an umbrella RL deal — so we're ready to move same-day the MoU signs |
| Incumbents price-match to kill new entrants | HIGH (7/10) | Compete on documentation/transparency, not price; target SMEs and compliance-pressured sectors incumbents serve poorly |
| Large employers already locked with incumbent agencies | HIGH (7/10) | Don't chase them first; build case studies from SME deployments, then approach |
| BAIRA incumbent retaliation (documented history of internal violence, May 2025) | HIGH | Quiet entry via umbrella RL partner; no public criticism of incumbents; consider Malaysia-based entity to reduce physical exposure in Bangladesh |
| TURAP mandatory + high fee ($1,000/worker) adopted | MEDIUM | Reposition immediately as "TURAP-compatible fulfilment partner"; the 8 BD-side functions remain necessary regardless of platform |
| Malaysia's 10 conditions restrict entry to 5-7 agencies | MEDIUM (45% probability, Scenario A) | Umbrella deal is the primary path, not a fallback — pursue it now |
| Legal exposure: unlicensed recruitment | MEDIUM | Stay strictly in "information & registration service" mode (no money collection, no job guarantees) until an umbrella RL or own RL is in place |
| Bangladesh PDPA / Malaysia PDPA compliance on collected data | LOW-MEDIUM | Google Forms data disclosed to users; no sale/sharing of personal data; revisit once BD Data Protection Act 2023 finalizes |

**Legal disclaimer, unchanged and mandatory on every public-facing asset:** *"Corridor closed since June 2024; reopening terms pending official MoU between Bangladesh and Malaysia. This is an information & registration service only. We do not guarantee visas, jobs, or recruitment outcomes. No payments are collected through this site."*

---

## 8. Operations & Automation Stack

What's live/buildable at zero cost, and what this plan adds:

| Layer | Tool | Status |
|---|---|---|
| Employer database | `data/companies.db` (SQLite, 505 companies) | Live |
| Employer discovery | `scrapers/scraper_runner.py` (9 sources: FMM, CBP, Bursa, MATRADE, plantation, construction, services, industrial zones, SME) | Live, runs weekly via GH Actions |
| Contact enrichment | `scrapers/contact_enricher.py` | Live, partial coverage (46 phones, 27 emails of 505) |
| **Employer outreach generation** | `automation/generate_outreach.py` | **New — see §9** |
| **Pipeline / lightweight CRM** | `automation/update_pipeline.py` + `pipeline_status` columns in companies.db | **New — see §9** |
| Worker funnel | `site/index.html` (Bengali) → Google Form | Live; wiring instructions in `WORKER_INTAKE_SETUP.md` (**new**) |
| Employer funnel | `site/employers/index.html` (English) | Live |
| SEO content | 5 blog posts, `site/corridor-tracker/` | Live |
| Hosting/CI | GitHub Pages + GitHub Actions, weekly cron | Live |
| **AI operations copilot** | `MASTER_PROMPT.md` | **New — see §10** |

---

## 9. What's New: Automation to Actually Run Outreach

Having a scored database of 505 employers is not the same as contacting them. This plan adds:

1. **`automation/generate_outreach.py`** — walks every company in `companies.db`, picks the sector-specific pitch already defined in `TOP_100_TARGETS.md`'s approach templates, and generates a ready-to-send email + WhatsApp message + LinkedIn DM per company. Output: `outreach/outreach_queue.csv`, sorted by priority score, ready for manual sending or mail-merge (e.g. Gmail mail merge add-on, still $0).
2. **Pipeline columns added to `companies.db`** (`pipeline_stage`, `last_contacted`, `outreach_channel`) so every company has a status: `not_contacted → contacted → replied → interested → converted / dead`.
3. **`automation/update_pipeline.py`** — one-line CLI to update a company's stage after you actually send a message or get a reply, and to print a pipeline funnel summary (how many at each stage, weekly).
4. GitHub Actions runs the outreach generator right after the weekly scraper, so the queue always reflects newly discovered companies.

**This is intentionally semi-automated, not fully automated.** Mass automated cold-emailing/WhatsApp-blasting Malaysian HR contacts at scale risks account bans (LinkedIn, WhatsApp Business) and, more importantly, undermines the "transparent, not spammy" positioning this plan is built on. The generator produces the messages; a human sends them at the safe daily volumes `content/DISTRIBUTION.md` already specifies (15 LinkedIn/day, etc.).

---

## 10. What's New: The Operations Prompt

`MASTER_PROMPT.md` is a single, self-contained prompt block encoding this entire business — market status, pricing, target segments, compliance rules, tone — so that any session with an AI assistant (Claude, ChatGPT, etc.) can immediately draft outreach, answer FAQs, generate content, or qualify a lead without re-reading this whole repo. Paste it in as a system/first message and go. Update it whenever a material fact in this plan changes (MoU signs, TURAP decision, price change).

---

## 11. 30-60-90 Day Plan ("Start Today")

### This week
- [ ] Push this repo live on GitHub Pages if not already confirmed (`RESUME_STATE.md` flags this as unverified)
- [ ] Run `python scrapers/contact_enricher.py` (needs a generous timeout) to raise the 46/505 phone coverage
- [ ] Run `python automation/generate_outreach.py` to produce the first outreach queue
- [ ] Start Week 1 of the Facebook-groups authority-building plan (`content/DISTRIBUTION.md` §1) — no links, just answering questions
- [ ] Identify and message 2-3 candidate BMET RL holders for an umbrella conversation (§3.3) — the one task on this list that most determines whether this business can operate at all once the corridor opens

### Days 1-30
- [ ] Send the first 100 outreach messages from the generated queue (15 LinkedIn/day, WhatsApp/email as available) — track replies in `pipeline_stage`
- [ ] Publish the referral program and start collecting worker waitlist signups
- [ ] Set up the Telegram channel and cross-promote from all other channels
- [ ] Hit the 30-day targets in §5: 1,400 worker signups, 50 employer contacts
- [ ] Weekly: check `QUOTA_WATCH.md`-tracked sources for MoU/TURAP news; update it

### Days 31-60
- [ ] Convert warm employer leads (`pipeline_stage = interested`) into signed intent-to-hire conversations
- [ ] Finalize umbrella RL agreement or confirm progress toward Malaysia entity structure
- [ ] Expand `companies.db` past 505 toward the 1,000+ mark, focused on underrepresented sectors (services, logistics)
- [ ] Build 3-5 case-study-ready employer relationships in compliance-pressured sectors (E&E, gloves)

### Days 61-90
- [ ] Reassess against the 3-scenario plan (§2) based on actual MoU/TURAP developments
- [ ] If corridor shows signs of opening: finalize legal structure, prep first worker batch documentation pipeline
- [ ] If still delayed: shift emphasis fully to SEO authority + waitlist growth, hold burn at $0, revisit Mauritius as a parallel corridor (per Attack 11 mitigation)

---

## 12. KPI Dashboard

| Metric | Baseline (today) | 30-day target | 90-day target |
|---|---|---|---|
| Companies in database | 505 | 700+ | 1,000+ |
| Companies with phone/email | 46 / 27 | 150+ | 300+ |
| Companies contacted | 0 | 100 | 400 |
| Employer replies | 0 | 15+ | 60+ |
| Worker waitlist signups | 0 | 1,400 | 3,000+ |
| Telegram members | 0 | 1,000 | 3,000 |
| Umbrella RL agreement | Not started | In negotiation | Signed (target) |
| Monthly burn | $0 | $0-5 | $0-20 |

---

## 13. What This Plan Does Not Solve

Being direct about the limits of what a repo of code and content can do:
- It cannot get you a BMET Recruiting Licence or an umbrella agreement — that requires real relationships and, likely, travel/meetings in Dhaka.
- It cannot confirm whether TURAP gets Cabinet approval, or when the labour MoU signs — that's tracked in `QUOTA_WATCH.md` and needs a human checking sources weekly.
- It cannot deploy a single worker until the corridor legally reopens — everything here is pre-launch positioning, and that positioning is the entire point: be ready to move the day the MoU is signed, while competitors are still starting from zero.
