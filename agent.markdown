# AGENT INSTRUCTION & CONTINUITY MANUAL (`agent.markdown`)
## Project: Bangladesh–Malaysia Clean Labor Corridor Platform (Open Digital Clearinghouse)

**Branch:** `feat/legal-verification-and-visual-architecture`  
**Purpose:** Comprehensive onboarding and technical reference for any AI agent or software engineer continuing work on this repository.  
**Last Updated:** August 2026  

---

## 1. Project Mission & High-Level Architecture

This repository contains the operational, legal, architectural, and ministerial intelligence stack for dismantling the **BDT 5.4 to 6.5 Lakh per worker extortion syndicate** in the Bangladesh–Malaysia labor migration corridor, restoring the migration cost to the government-mandated **BDT 78,990 ceiling (or $0 worker-cost under the ILO Employer-Pays Principle)**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE 3-SIDED ARCHITECTURE                              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Malaysian Employer Portal (Next.js SaaS): Ingests Section 60K quotas, generates US │
│    CBP / RBA Zero-Debt Compliance certificates, and tracks calling visas (VDR).        │
│ 2. Central Clearinghouse Engine (Python / REST): Algorithmic matching, Centralized    │
│    Blind Medical Allocation (CBMA), and Probashi Kallyan Bank (PKB) 0-cash escrow.     │
│ 3. Worker Mobile PWA & UDC Assisted Onboarding: NID verification via Porichoy API,     │
│    in-person contract disclosure, and 3-stage Ethical Human-in-the-Loop (HITL) gate.   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Directory Layout & Critical File Map

```
malaysia-corridor-ops/
├── agent.markdown                                      # THIS FILE — Master AI continuity manual
├── PROJECT.md                                          # Institutional project roadmap & milestone status
├── data/
│   ├── companies.db                                    # SQLite database of 203+ verified Malaysian employers
│   └── companies.csv                                   # CSV export of employer target list
├── dossier/                                            # Master Institutional Briefing Suite
│   ├── README.md                                       # Dossier table of contents & reading guides
│   ├── EXECUTIVE_DOSSIER_INDEX.md                      # Master synthesis binder & KPI matrix
│   ├── R1_MINISTERIAL_POLICY_MEMO_BILINGUAL.md          # 1-Page Bilingual Memo (Bangla Nothi + English)
│   ├── R2_MINISTERIAL_PRESENTATION_DECK.md              # 10-Slide Pitch Deck Script & Talk Tracks
│   ├── R3_OPERATIONAL_MATHEMATICAL_ARCHITECTURE_WHITEPAPER.md # Forensic Math & Architecture Whitepaper
│   ├── R4_MINISTERIAL_DEFENSE_COUNTER_ARGUMENTS.md      # Rebuttals against BAIRA cartel & JWG pushback
│   ├── R5_TECHNICAL_INTEGRATION_AND_ETHICAL_HITL_SPEC.md # FWCMS Bridge & 3-Stage HITL Protocol Spec
│   ├── LEGAL_VERIFICATION_MALAYSIA_BANGLADESH.md       # Comparative Statutory Analysis (Act 265, Act 2013)
│   ├── BANGLADESH_GOVERNMENT_APIS_INTEGRATION_SPEC.md   # Porichoy NID, BMET, & PKB CBS API Specs
│   └── VISUAL_EXPLANATION_FOR_MINISTERS.md             # High-impact visual metaphors & diagram guide
├── scrapers/                                           # Python scrapers & company enrichers
│   └── scraper_runner.py                               # Master scraping orchestrator
└── site/                                               # GitHub Pages bilingual marketing frontend
```

---

## 3. Statutory Legal Truths & Invariants (DO NOT VIOLATE)

When generating code, proposals, or communications, any AI operating on this codebase must adhere to the following verified legal facts:

1. **FWCMS & Bestinet Standing:** FWCMS is an outsourced administrative IT concession operated by Bestinet Sdn Bhd, NOT a sovereign law. We do NOT negotiate with Bestinet (whose founder has an arrest warrant in Bangladesh). We interface with FWCMS by automating the **Malaysian Employer's authorized corporate login (SSM)** via headless browser agents (Skyvern / Playwright).
2. **Direct Sourcing Legality:** Under Malaysian Employment Act 1955 (Section 60K), employers have direct statutory standing to employ foreign workers. Under Bangladesh Overseas Employment and Migrants Act 2013 (Section 14 & 19), recruitment is fulfilled via an **Attested Demand Letter + Power of Attorney (POA) from the Bangladesh High Commission in KL**, processed through an **Open Pool of all 1,500+ licensed BAIRA RL holders** at a fixed statutory service fee of **BDT 20,000**.
3. **No Direct Worker Fees:** The platform strictly enforces the **Zero-Upfront Cash** model. All statutory fees (BDT 78,990) are settled directly to vendors by Probashi Kallyan Bank (PKB) micro-loans or paid by the Malaysian employer under ILO/RBA Employer-Pays rules.

---

## 4. Key API Endpoints & Government Gateway Summary

| Gateway | Host Endpoint | Function & Payload |
|---|---|---|
| **Porichoy (NID KYC)** | `POST https://api.porichoy.gov.bd/api/v1/verification/nid` | Validates NID, DOB, and live biometric photo against the Election Commission database within 800ms. |
| **BMET Manpower DB** | `GET https://api.bmet.gov.bd/v2/candidates/{nid}/trade-qualification` | Returns certified vocational training status from government Technical Training Centers (TTCs). |
| **BMET Smart Card** | `POST https://api.bmet.gov.bd/v2/emigration/smart-card-issue` | Triggers final QR-coded Emigration Clearance Smart Card once PKB escrow and Video Affidavit are verified. |
| **PKB CBS Escrow** | `POST https://api.pkb.gov.bd/v1/escrow/disburse` | Cashless milestone disbursement directly to Biman Airlines (Tk 35k), Clinic (Tk 8k), and BMET (Tk 15.9k). |

---

## 5. Guidelines for Future AI Tasks

* **Tone:** Professional, technocratic, legally rigorous, and grounded in authentic administrative language (Secretariat Bangla `নথি` and international boardroom English).
* **Mathematical Precision:** Always use the authoritative baseline:
  - Gazetted Cap: `BDT 78,990`
  - Real Statutory Cost Floor: `BDT 130,532 (RM 5,020)`
  - Historical Syndicate Extortion: `BDT 540,000 – BDT 650,000`
  - Net Syndicate Illicit Leakage: `BDT 409,468 per worker`
* **Human-in-the-Loop Safeguards:** Never propose removing physical human verification. The 3-Stage Ethical HITL Protocol (In-person video affidavit, direct airline escrow, and airport welfare escort) is a non-negotiable architectural invariant.
