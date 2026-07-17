# ASSUMPTIONS LOG - Malaysia Corridor Launch Stack

**Created:** 2026-07-17
**Updated:** 2026-07-17

---

## Business Model Assumptions

| ID | Assumption | Status | Evidence Needed | Source |
|----|-----------|--------|-----------------|--------|
| A1 | TURAP toll is knowable and payable as fixed cost | UNVERIFIED | Official FWCMS/TURAP fee schedule | KESUMA/MOHR |
| A2 | 2-3 lakh BDT all-in leaves sustainable margin | UNVERIFIED | Complete cost breakdown (levy, VDR, FOMEMA, airfare, FWCMS, BMET, welfare, medical, training) | Multiple gov sources |
| A3 | Corridor reopens with room for new entrants (not just 102 incumbents) | UNVERIFIED | MoU text, Bangladesh MoEWOE circular, TURAP access policy | Bangladesh MoEWOE, KESUMA |
| A4 | Employers will name us as source partner on TURAP | UNVERIFIED | TURAP employer registration flow, source partner requirements | Bestinet/TURAP docs |
| A5 | TURAP won't eliminate Bangladesh-side agents entirely | UNVERIFIED | TURAP architecture docs, BMET role in TURAP | Bestinet, BMET |
| A6 | Workers can/will pay 2-3 lakh BDT (affordability + loan access) | UNVERIFIED | Microfinance/NGO loan products for migration, worker surveys | ILO, BRAC, NGOs |
| A7 | Zero-cost digital outreach reaches Malaysian HR decision-makers | UNVERIFIED | LinkedIn/email response rates for MY HR, WhatsApp adoption | Test campaigns |
| A8 | 102 incumbent agencies won't retaliate violently | UNVERIFIED | BAIRA history, recent incidents, protection strategies | News, police reports |
| A9 | Can operate legally without own RL (umbrella/consultancy/Malaysia entity) | UNVERIFIED | BMET RL regulations, consultancy license scope, Malaysia entity options | BMET, legal counsel |
| A10 | Employer-pays model shift is imminent (RBA/CBP enforcement) | UNVERIFIED | RBA code enforcement timeline, CBP WRO active cases | RBA, CBP |

---

## Technical Assumptions

| ID | Assumption | Status | Evidence Needed |
|----|-----------|--------|-----------------|
| T1 | Free tiers (Vercel, Railway, Supabase, GitHub Pages) suffice for launch | UNVERIFIED | Traffic projections, bandwidth limits |
| T2 | Public MYFutureJobs/FWCMS/SSM data is scrapeable without auth | UNVERIFIED | robots.txt, ToS, rate limits |
| T3 | Bengali content renders correctly on free static hosting | UNVERIFIED | Font loading, RTL support on Vercel/GitHub Pages |
| T4 | 12+ scrapers maintainable with GitHub Actions cron | UNVERIFIED | GH Actions minutes limit (2000/mo free) |
| T5 | GoatCounter/Umami analytics on free tier sufficient | UNVERIFIED | Pageview limits |

---

## Legal/Compliance Assumptions

| ID | Assumption | Status | Evidence Needed |
|----|-----------|--------|-----------------|
| L1 | "Information & registration service only" disclaimer provides legal cover | UNVERIFIED | Bangladesh Emigration Act, Malaysia Private Employment Agencies Act |
| L2 | No money collection = no recruiting license needed | UNVERIFIED | BMET circular on "service providers" vs "recruiting agencies" |
| L3 | Worker data collected via Google Forms = compliant with BD PDPA (draft) | UNVERIFIED | Bangladesh Data Protection Act 2023 status |
| L4 | Malaysian employer contact info from public sources = PDPA compliant | UNVERIFIED | Malaysia PDPA 2010, public directory exceptions |

---

## Timeline Assumptions

| ID | Assumption | Status | Evidence Needed |
|----|-----------|--------|-----------------|
| TM1 | Corridor reopens within 3 months (by Oct 2026) | UNVERIFIED | PM visit outcomes, MoU signing schedule |
| TM2 | 30-day build window realistic for MVP | UNVERIFIED | Team velocity, scraper complexity |
| TM3 | First worker deployment within 60 days of launch | UNVERIFIED | Employer pipeline conversion rates |