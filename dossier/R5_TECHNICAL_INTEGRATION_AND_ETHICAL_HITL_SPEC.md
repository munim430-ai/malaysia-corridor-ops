# Technical Integration & Ethical Human-in-the-Loop (HITL) Protocol
## FWCMS/TURAP Bridge, Unified Responsive Web/PWA Architecture, and Zero-Corruption Flight Allocation

**Target System:** Bangladesh–Malaysia Clean Labor Corridor Platform  
**Target Stakeholders:** Ministry of Expatriates' Welfare & Overseas Employment, BMET, Malaysian Ministry of Human Resources (KESUMA), and Probashi Kallyan Bank (PKB)  
**Classification:** Technical Architecture & Operational SOP Specification (Part R5)  
**Date:** August 2026  

---

## 1. Executive Problem Resolution

This specification directly resolves the three core operational dilemmas of the corridor:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 3 CORE RESOLUTIONS                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. FWCMS / TURAP Dilemma:   We do NOT break Malaysian law by bypassing official state  │
│                             systems. We BYPASS the private syndicate brokers by acting │
│                             as the verified digital API bridge directly into FWCMS.    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. Form Factor Dilemma:     A single Unified Responsive Web Application (Next.js) with │
│                             a Desktop Portal for Employers & BMET Officers, and a      │
│                             Mobile-First PWA for Union Digital Centers (UDCs) & workers│
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. The Illiteracy & HITL    Illiterate workers are never left alone with software. A   │
│    Dilemma:                 3-Stage Ethical Human-in-the-Loop (HITL) Protocol enforces │
│                             in-person verification, anti-extortion affidavits, and     │
│                             institutional bulk airline booking via PKB escrow.         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The FWCMS & TURAP Regulatory Strategy: "Compliant Bridge & Middleman Bypass"

### 2.1 The Legal Reality of Malaysian Migration Software
* **FWCMS (Foreign Workers Centralized Management System):** Operated by Bestinet Sdn Bhd for KESUMA (Ministry of Human Resources) and JIM (Immigration Department of Malaysia). It is the **mandatory statutory system** for issuing Calling Visas (VDR) and biometric health approvals. It is legally impossible and illegal to deploy foreign workers to Malaysia without FWCMS approval.
* **TURAP:** A proposed recruitment matching platform by Bestinet attempting to levy an additional US$ 1,000 toll per worker.

### 2.2 How We "Bypass" the Syndicate Without Bypassing the Law
In previous cycles, the **102-agency cartel in Dhaka** and **corrupt Malaysian labor brokers in KL** inserted themselves between the employer and FWCMS, demanding Tk 2.5 Lakh per quota slot just to enter data into the system.

**Our Architecture Eliminates the Middlemen via Direct Digital Ingestion:**

```
   [ Malaysian Employer ] ──(Submits Section 60K eQuota)──► [ KESUMA / FWCMS ]
            │                                                      ▲
            │ (Direct Job Order API)                               │ (Verified Candidate Dossier)
            ▼                                                      │
   [ Keystone Workforce Bridge ] ──► [ Central Clearinghouse ] ────┘
                                     (BMET / NID / PKB Escrow)
```

1. **Direct Employer Ingestion:** Malaysian employers connect their approved KESUMA eQuota directly to `Keystone Workforce Bridge`. No Malaysian labor sub-agent is paid.
2. **Verified Candidate Dossier Push:** When BMET clears a worker batch in Bangladesh, our Clearinghouse pushes the verified candidate biometric and passport data directly into FWCMS via standard agency/employer credentials.
3. **Neutralizing the TURAP $1,000 Toll:** By enforcing the bilateral **ILO Employer-Pays Principle** agreed in April 2026, statutory software fees are charged directly to Malaysian employers under local business operating expenses, ensuring **BDT 0 is charged to the worker**.

---

## 3. What We Are Building: Unified Responsive Web & Mobile PWA

We are building a **single, unified Next.js 16 + React 19 architecture** designed for two distinct screen contexts:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                UNIFIED SOFTWARE ARCHITECTURE                            │
├────────────────────────────────────────────┬────────────────────────────────────────────┤
│ 1. DESKTOP SAAS PORTAL                     │ 2. MOBILE-FIRST PWA INTERFACE              │
│ (For Malaysian Employers, BMET & Agencies) │ (For UDC Field Operators & Rural Workers)  │
├────────────────────────────────────────────┼────────────────────────────────────────────┤
│ • Bulk Quota Demand Order Management       │ • Ultra-lightweight (<3s load on rural 3G) │
│ • US CBP / RBA Zero-Debt Compliance Engine │ • Step-by-Step Bangla Assisted Enrollment  │
│ • Digital Escrow & Milestone Authorization │ • Biometric Photo & Passport Camera Scan   │
│ • Calling Visa (VDR) & Flight Manifests    │ • Digital Migration Wallet (PKB Loan Card) │
└────────────────────────────────────────────┴────────────────────────────────────────────┘
```

### 3.1 Why a Progressive Web App (PWA) over a Native Mobile App?
* **Zero App Store Friction:** Rural workers and UDC operators do not need 50MB downloads from Google Play, Apple IDs, or phone storage cleanup.
* **Universal Dialect Accessibility:** Runs on any mobile browser (Chrome, Safari, Opera Mini) and features native voice-guided prompts in regional dialects (Sylheti, Chittagonian, Rangpuri).

---

## 4. The 3-Stage Ethical Human-in-the-Loop (HITL) Protocol

To guarantee that illiterate workers are protected and that flight tickets are never scalped by black-market cartels, the platform enforces three mandatory physical human checkpoints:

```
                                  ETHICAL HITL PIPELINE
                                  
   ┌───────────────────────────────────────────────────────────────────────────────────┐
   │ STAGE 1: PHYSICAL IN-PERSON VERIFICATION & ANTI-EXTORTION AFFIDAVIT (BMET / TTC)  │
   │ • 1-on-1 Mother-Tongue Contract Reading by BMET Welfare Officer                   │
   │ • Live Biometric Fingerprint Check against NID Registry                           │
   │ • Recorded Video Affidavit: "Did anyone ask you for cash? Your cost is Tk 0."     │
   └─────────────────────────────────────────┬─────────────────────────────────────────┘
                                             │ (Officer Signs Digital Approval)
                                             ▼
   ┌───────────────────────────────────────────────────────────────────────────────────┐
   │ STAGE 2: DIRECT INSTITUTIONAL AIRLINE BOOKING (PKB ESCROW SETTLEMENT)             │
   │ • Direct GDS Block Allocation with Biman Bangladesh / Malaysia Airlines / AirAsia │
   │ • Non-transferable E-Ticket issued directly in worker's name at bulk govt rate    │
   │ • PKB Escrow disburses Tk 35,000 ticket cost directly to Airline (No cash touts)  │
   └─────────────────────────────────────────┬─────────────────────────────────────────┘
                                             │ (Flight Manifest Dispatched)
                                             ▼
   ┌───────────────────────────────────────────────────────────────────────────────────┐
   │ STAGE 3: AIRPORT WELFARE ESCORT (DHAKA DAC ➔ KUALA LUMPUR KLIA)                  │
   │ • Dhaka Airport: BMET Welfare Desk provides physical badge & immigration escort   │
   │ • In-Flight Safety Card provided in Bangla                                        │
   │ • KLIA Airport: Certified Employer Reception Desk receives worker at arrival gate│
   └───────────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.1 Stage 1 Detailed SOP: In-Person Verification at BMET District Office (DEMO / TTC)
Before any visa stamping or flight allocation, the shortlisted candidate must physically report to his local BMET District Employment & Manpower Office (DEMO) or Technical Training Center (TTC).

#### The Standard Operating Procedure (SOP):
1. **Biometric Match:** The worker places his thumb on the biometric scanner; the system verifies his identity against the Bangladesh Election Commission NID database.
2. **Mother-Tongue Contract Disclosure:** The BMET Welfare Officer reads the mandatory employment terms aloud in Bangla:
   * *Company Name & Location in Malaysia.*
   * *Base Salary (Minimum RM 1,500 + Guaranteed Overtime).*
   * *Free Accommodation and Medical Insurance (SOCSO).*
   * *Probashi Kallyan Bank Loan Repayment: RM 250/month for 6 months.*
3. **The Anti-Extortion Video Affidavit (15-Second Recording):**
   * The officer records a brief video on the platform where the worker states:
     > *"আমি [নাম], আমার জাতীয় পরিচয়পত্র নম্বর [NID]। আমি স্বেচ্ছায় মালয়েশিয়া যাচ্ছি। এই চাকরির জন্য আমি কাউকে কোনো নগদ টাকা দেইনি। আমার সকল খরচ প্রবাসী কল্যাণ ব্যাংকের ঋণে সম্পন্ন হয়েছে।"*
     > *(“I am [Name], NID [Number]. I am voluntarily going to Malaysia. I have not paid cash to any middleman or dalal. My processing is fully covered by the Probashi Kallyan Bank loan.”)*
4. **Digital Signature & Gate Pass:** The officer signs the verification on the portal. If the worker reports that anyone demanded cash, the system triggers an immediate investigation and flags the recruiting agency.

---

### 4.2 Stage 2 Detailed SOP: Direct Institutional Airline Booking Engine

#### How Syndicates Previously Extorted Workers on Flights:
In the 2022–2024 syndicate, cartel agencies bought up blocks of Dhaka–Kuala Lumpur flights, creating artificial ticket shortages and charging workers **Tk 85,000 to Tk 1,10,000** for a flight that normally costs **Tk 35,000**.

#### The Clean Booking Mechanism:
1. **Direct GDS / API Block Agreements:** The Ministry of Expatriates' Welfare establishes institutional block-seat agreements with **Biman Bangladesh Airlines, Malaysia Airlines, US-Bangla, and AirAsia** at a fixed government migrant fare (**BDT 35,000–38,000**).
2. **Automated Non-Transferable Ticket Issuance:** When Stage 1 verification is completed, the Central Clearinghouse API automatically issues a non-transferable electronic ticket linked directly to the worker's passport number.
3. **Direct Bank-to-Airline Settlement:** Probashi Kallyan Bank (PKB) disburses the ticket payment directly to the airline's institutional bank account via electronic fund transfer (EFT/RTGS). **No cash touches agency hands; zero ticket scalping is possible.**

---

### 4.3 Stage 3 Detailed SOP: Pre-Departure & Arrival Welfare Escort (DAC ➔ KLIA)

1. **Dhaka Airport (Hazrat Shahjalal International - DAC):**
   * Workers arrive at the dedicated **Expatriate Welfare Lounge (প্রবাসী লাউঞ্জ)**.
   * BMET Welfare Desk inspects the digital QR Gate Pass, provides luggage tags, and escorts the cohort through immigration and security clearance, eliminating harassment or off-loading threats.
2. **Kuala Lumpur Airport (KLIA Terminal 1 / Terminal 2):**
   * Under Malaysian Immigration (JIM) regulations, foreign workers cannot exit KLIA without being received by their employer.
   * The Malaysian Employer’s certified HR representative (tracked via `Keystone Workforce Bridge`) scans the worker's QR badge at the immigration arrival gate.
   * Confirmation of safe arrival is instantly transmitted back to BMET in Dhaka and to the worker’s family via automated SMS.

---

## 5. Technical Data Flow & OpenAPI REST Endpoints

### 5.1 Architecture Data Flow Diagram

```
[ Employer: Keystone Portal ]
       │
       │ (1) POST /api/v1/jobs/demand (KESUMA Quota, Roles, Salary)
       ▼
[ Central Clearinghouse API Engine ]
       │
       │ (2) GET /api/v1/workers/matched (Query BMET/UDC Talent Pool)
       │ (3) POST /api/v1/medical/blind-assign (NIST VRF Random Clinic Allocation)
       ▼
[ BMET District Office / TTC ]
       │
       │ (4) POST /api/v1/verification/hitl-complete (Biometric + Video Affidavit)
       ▼
[ Probashi Kallyan Bank Escrow ]
       │
       │ (5) POST /api/v1/escrow/disburse (Pay Airline Tk 35k, Clinic Tk 8k, BMET Tk 15.9k)
       ▼
[ Direct Airline GDS Engine ]
       │
       │ (6) POST /api/v1/flights/issue-ticket (Non-transferable E-Ticket)
       ▼
[ FWCMS / JIM Immigration ]
       │
       │ (7) POST /api/v1/fwcms/vdr-sync (Candidate Biodata & Departure Notice)
       ▼
[ KLIA Reception & SOCSO Onboarding ]
```

---

## 6. Implementation Summary for the Minister

When presenting this to the Minister, you provide complete operational certainty:

1. **No Legal Conflict with Malaysia:** We work directly with FWCMS and KESUMA eQuota, feeding clean data and eliminating the corrupt third-party brokers.
2. **No Technical Exclusion for Illiterate Workers:** Union Digital Centers (UDCs) and BMET TTCs handle assisted digital enrollment; workers use simple voice-guided mobile tools.
3. **No Risk of Coercion or Ticket Hoarding:** The 3-Stage Ethical Human-in-the-Loop protocol guarantees that every worker is interviewed on video, pays **0 Taka cash**, and receives a direct institutional airline ticket settled through Probashi Kallyan Bank.
