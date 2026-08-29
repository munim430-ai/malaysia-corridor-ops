# TECHNICAL BLUEPRINT: OPEN DIGITAL CLEARINGHOUSE (HYBRID G2B MODEL)
## BANGLADESH–MALAYSIA LABOR MIGRATION CORRIDOR
**Document ID:** ARCH-ODC-MY-BD-2026-V1  
**Target Authority:** Ministry of Expatriates' Welfare & Overseas Employment (MoEWOE), Government of the People's Republic of Bangladesh  
**Subject:** Open Digital Clearinghouse Architecture, Direct Sourcing, Blind Medical Allocation, Zero-Upfront-Cash Financing (PKB/MFI), and Malaysian Systems Interoperability (FWCMS/TURAP/JIM)  
**Security Classification:** Highly Confidential / Ministerial Policy Directive  
**Date:** August 2026  

---

## EXECUTIVE SUMMARY & ARCHITECTURAL OBJECTIVES

The Bangladesh–Malaysia labor migration corridor has historically suffered from systemic market failure, cartelization, and extortionate rent extraction. Between 2016 and 2024, successive closed syndicates (10 agencies in 2016; 25 and later 100 agencies in 2021–2024) monopolized Malaysian demand allocations, inflating the cost of migration from the government-stipulated fee of BDT 78,990 to between BDT 500,000 and BDT 650,000 per worker. This generated over USD 1.2 billion in illicit rent extraction, drove workers into debt bondage, and triggered international scrutiny (US TIP Report Tier 2/Watchlist, ILO Convention 29/181 violations, and US CBP Withhold Release Orders).

This **Open Digital Clearinghouse (ODC)** blueprint delivers a turnkey, zero-trust, API-first architecture designed to permanently dismantle syndicate monopolies, enforce the **Employer Pays Principle (EPP)**, and establish a **Zero-Upfront-Cash (0 BDT)** corridor for Bangladeshi workers. 

### Core Architectural Pillars
1. **Democratized Hybrid G2B Clearinghouse:** Replaces opaque agency quotas with an algorithmic matching engine open to all 1,500+ valid BMET-licensed Recruiting Agencies (RLs).
2. **Direct Digital Sourcing:** Bridges the national BMET database and Ami Probashi directly to Malaysian employer demand orders, preventing the physical hoarding and auctioning of demand letters.
3. **Cryptographic Blind Medical Allocation:** Implements a Verifiable Random Function (VRF) to distribute pre-departure medical screening across all DGHS-accredited medical facilities in Bangladesh, eliminating the 100-clinic cartel and injecting digital test results directly into FWCMS via signed PKI payloads.
4. **End-to-End Cashless Financing via Probashi Kallyan Bank (PKB) & MFIs:** Establishes a zero-cash escrow pipeline where statutory fees are settled directly between financial institutions and service providers, recovered via structured, regulated post-arrival digital salary deductions through Malaysian payroll systems (ePPAx, FWCMS e-Wages, SOCSO).
5. **Full Interoperability with Malaysian Digital Gateways:** Native bidirectional integration with FWCMS (Bestinet), TURAP (KESUMA), and the Malaysian Immigration Department (JIM MyIMMs/e-Visa).

---

## FEATURES DISCOVERED & SPECIFIED

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Clearinghouse | Hybrid G2B Quota Allocation Engine | Distributes verified employer demand orders across all 1,500+ valid BMET RLs based on capacity rating and SLA score. | Verified Demand Order JSON, RL Registry, SLA performance vectors | Distributed Sub-Quota Allocation Tokens (SQAT) | Demand locked if RL license suspended or SLA < threshold. | BMET & KESUMA Quota Rules |
| 2 | Direct Sourcing | Ami Probashi / BMET Candidate Pool Sync | Real-time query and reservation of pre-verified candidates with NID, biometric registration, and skill certifications. | Candidate Skill Query, Geolocation filters, Passport status | Anonymized Candidate Match Set (ACMS) | Rejection on unverified NID, passport expiry < 6 mo, or active assignment lock. | BMET Emigration Database & Ami Probashi API |
| 3 | Anti-Hoarding | Demand Order Smart Escrow & Timeout | Enforces a strict 72-hour fulfillment window on allocated demand orders; unfulfilled quotas auto-revert to pool. | Demand Allocation ID, Timestamp, Sourcing status | Quota Reversion Event / Next-RL Allocation Trigger | Auto-cancellation and RL penalty mark on timeout breach. | Emigration Rules 2023 & Procurement Standards |
| 4 | Medical Allocation | VRF Cryptographic Blind Center Assigner | Cryptographically assigns candidates to approved DGHS diagnostic centers using NIST SP 800-90B entropy + candidate hash. | Candidate National ID hash, District code, Clinic daily capacity matrix | Cryptographically signed Medical Appointment Voucher | Allocation re-roll if target clinic capacity saturated; fallback to nearest tier-1 clinic. | GAMCA/Wafid Cartel Analysis & NIST VRF Spec |
| 5 | Medical Integrity | Automated LIMS-to-FWCMS Signed Upload | Direct machine-to-machine push of medical laboratory results (blood, X-ray, serology) signed with clinic private keys. | LIMS Raw Analyzer Output, Digital Signature, Candidate Biometric Token | Direct FWCMS/FOMEMA Medical Status Update, DGHS Sync | Immediate rejection on hash mismatch, expired timestamp, or unverified signing key. | FWCMS Bio-Medical Interface Spec |
| 6 | Financial Pipeline | PKB/MFI Zero-Upfront-Cash Escrow | Disburses statutory migration fees directly from PKB/MFI escrow to vendors (BMET, airlines, clinics), bypassing cash. | Approved Loan Token, Verified Cost Breakdown, Service Provider Invoices | Automated RTGS/BEFTN direct settlement vouchers | Transaction halted if invoice exceeds statutory ceiling; zero cash released to worker/agent. | PKB Migration Loan Mandate & Bangladesh Bank Guidelines |
| 7 | Payroll Recovery | Post-Arrival Digital Salary Deduction | Integrates with Malaysian digital payroll (ePPAx, e-Wages, SOCSO) to deduct monthly loan repayments directly from salary. | Worker Bank/e-Wallet Account, EPF/SOCSO ID, Loan Repayment Schedule | Monthly Remittance Credit to PKB, ISO 20022 camt.054 confirmation | Alerts generated on wage non-payment, unauthorized deduction, or employer default. | Malaysia Employment Act 1955 (Sec 60K/24) & FWCMS e-Wages |
| 8 | Interoperability | FWCMS Bidirectional Gateway | Synchronizes bio-enrollment, e-Quota, eVDR (Calling Visa) approval, and worker arrival telemetry via mTLS REST endpoints. | Calling Visa JSON, Bio-Token, Passport Number | BMET Emigration Clearance Smart Card Generation | Block clearance if eVDR hash doesn't match Malaysian Immigration Master Record. | FWCMS Bestinet API & JIM eVDR Standard |
| 9 | Interoperability | TURAP Compliance Gateway | Validates employer quota eligibility under KESUMA's Integrated Foreign Worker Management System. | Employer SSM ID, Sector Code, Section 60K clearance | Quota Eligibility Confirmation Token | Block allocation if employer has active JTKSM labor violations. | KESUMA TURAP Architecture Framework |
| 10 | Security | Immutable Corrupt-Attempt Audit Ledger | Append-only event store recording every candidate match, quota transfer, medical result, and fee transaction with SHA-256 chaining. | System Event Stream, Actor Digital Signature, Timestamp | Verifiable Cryptographic Audit Receipt (VCAR) | Ledger mutation triggers immediate system lockdown and Ministerial alert. | Government Enterprise Architecture (GEA) Standards |

---

## EDGE CASES & FAILURE MODES

| # | Feature | Input / Edge Condition | Observed & Specified System Behavior |
|---|---------|------------------------|--------------------------------------|
| E1 | Quota Allocation | RL attempts to sub-contract or resell allocated quota to an unauthorized third-party broker (Dalal). | Cryptographic token binding: Quota allocation token is cryptographically bound to the RL's public key and specific worker BMET IDs. Sub-letting fails validation at BMET Smart Card issuance; RL license flagged for immediate suspension. |
| E2 | Candidate Sourcing | Candidate already registered under an active demand order attempts duplicate registration through another RL. | Global Deduplication Lock: Central registry detects active `UUID` and blocks duplicate binding. Emits warning to primary RL with a 24-hour resolution window. |
| E3 | Medical Allocation | Worker attempts to walk into a non-assigned or preferred medical center. | Biometric Check-in Failure: Clinic portal checks central VRF assignment ledger via mTLS. If Candidate ID != Allocated Clinic ID, check-in is rejected; system flags potential clinic poaching. |
| E4 | Medical Integrity | Diagnostic center attempts to upload a manually altered "FIT" result after automated analyzer flags TB/Hepatitis. | LIMS Data Tamper Detection: Central system cross-checks raw telemetry from calibrated automated analyzers against the uploaded summary report. Digital signature discrepancy triggers immediate DGHS audit freeze. |
| E5 | Financial Pipeline | Employer delays or defaults on depositing monthly wages into the worker's Malaysian digital account. | e-Wages Telemetry Alert: Clearinghouse detects missing ISO 20022 wage deposit event by day 7 of calendar month; automatically triggers diplomatic alert to Bangladesh High Commission in KL and formal complaint to JTKSM. |
| E6 | Interoperability | Malaysian Calling Visa (eVDR) issued with mismatched passport or misspelled candidate name. | Automated Rejection & Correction Pipeline: Clearinghouse validates eVDR payload against BMET/ICAO passport database. On mismatch, generates an automated eVDR Amendment Request to Malaysian Immigration (JIM) before ticketing. |
| E7 | Airfare & Logistics | Airline cancels flight or changes schedule after PKB direct escrow disbursement. | Automated Ticket Re-issuance Webhook: GDS integration automatically re-routes ticket; escrow ledger updates PNR reference without additional financial claim on worker. |
| E8 | Worker Rejection | Worker fails post-arrival FOMEMA medical screening in Malaysia despite passing pre-departure DGHS screening. | Insurance & Clinic Indemnity Trigger: Pre-departure clinic's mandatory indemnity bond is drawn down to cover repatriation costs; worker is protected from any debt liability; clinic placed on provisional audit. |

---

## 1. OPEN DIGITAL CLEARINGHOUSE (ODC) ARCHITECTURE

### 1.1 Architectural Vision: The Hybrid G2B Model
The Open Digital Clearinghouse operates as an intelligent, sovereign digital exchange sitting between the Malaysian employer demand ecosystem (FWCMS/TURAP) and the Bangladeshi supply ecosystem (BMET/Ami Probashi/RLs).

```
   MALAYSIAN EMPLOYERS (KESUMA / TURAP / FWCMS)
                       │
                       ▼
       ┌───────────────────────────────┐
       │   OPEN DIGITAL CLEARINGHOUSE  │
       │   (MoEWOE / BMET Sovereign)   │
       └───────┬───────────────┬───────┘
               │               │
      ┌────────┴──────┐ ┌──────┴──────────────┐
      ▼               │ │                     ▼
[TRACK A: DIRECT G2B] │ │ [TRACK B: PRIVATE RL PROCESSING]
Direct Employer-to-   │ │ 1,500+ Valid BMET Recruiting
Worker Digital Match  │ │ Licensees (Democratized Engine)
(BOESL / Platform)    │ │
      │               │ │                     │
      └────────┬──────┘ └──────┬──────────────┘
               │               │
               ▼               ▼
       ┌───────────────────────────────┐
       │   CENTRAL SERVICE PIPELINE    │
       │  • Blind Medical Allocation   │
       │  • PKB Zero-Cash Escrow       │
       │  • BMET Smart Card Clearance  │
       └───────────────────────────────┘
```

#### Dual-Track Fulfillment Architecture:
1. **Track A (Direct Digital Sourcing - G2B):** Employers requiring high-volume, standardized labor (e.g., major electronics multinationals, state-backed plantations) can directly search, interview, and issue digital job offers to pre-screened candidates on Ami Probashi / BMET, processed through the state agency (BOESL) or direct digital clearance, with zero recruitment intermediary fees.
2. **Track B (Democratized Private Processing - G2B2B):** Employers wishing to utilize private agencies must post their demand orders onto the Open Digital Clearinghouse. The clearinghouse algorithmically unbundles large demand quotas into manageable batches (e.g., 50–100 workers per batch) and distributes them across all 1,500+ valid BMET Recruiting Licensees (RLs) based on objective capacity, past compliance, and worker welfare ratings.

### 1.2 Quota Democratization & Anti-Syndicate Matching Algorithm
To eliminate the 25/100-agency syndicate model forever, the Clearinghouse enforces algorithmic quota distribution. No single agency or cartel can receive more than a capped percentage (e.g., max 2% of total corridor volume).

#### RL Allocation Scoring Function:
The allocation engine ranks and distributes demand batches using the **RL Integrity & Capacity Score ($S_{RL}$)**:

$$S_{RL} = w_1 \cdot C_{valid} + w_2 \cdot Q_{infra} + w_3 \cdot H_{welfare} - w_4 \cdot D_{penalty}$$

Where:
- $C_{valid} \in \{0, 1\}$: Active BMET license validation status.
- $Q_{infra} \in [0, 1]$: Physical & digital infrastructure score (verified training center, licensed counselors, biometric desks).
- $H_{welfare} \in [0, 1]$: Historical worker welfare compliance score (timely deployment rate, zero contract substitution complaints, zero illegal fee reports).
- $D_{penalty} \geq 0$: Accumulated penalty points for SLA breaches, delayed processing, or suspicious sub-agent associations.
- $w_1 = 0.40, w_2 = 0.25, w_3 = 0.25, w_4 = 0.50$ (Heavily weighted against malpractice).

```
+-------------------------------------------------------------------------------+
|                       DEMAND QUOTA DISTRIBUTION PIPELINE                      |
+-------------------------------------------------------------------------------+
| 1. Malaysian Demand Order Received: 5,000 Workers (Manufacturing Sector)      |
|    └─ Verified by Bangladesh High Commission (KL) via Digital Attestation     |
|                                                                               |
| 2. Clearinghouse Batch Decomposition:                                         |
|    └─ 5,000 Quotas split into 50 Batches of 100 Workers                       |
|                                                                               |
| 3. Dynamic Eligibility Filter:                                                |
|    └─ 1,500 RLs Evaluated -> 850 RLs meet Sector & Infrastructure Threshold   |
|                                                                               |
| 4. Algorithmic Quota Allocation:                                              |
|    └─ Top 50 Qualified RLs assigned 1 Batch (100 workers) each                |
|    └─ 72-Hour Acceptance & Sourcing SLA lock                                  |
|    └─ Unaccepted / Unfulfilled quotas auto-revert to pool after 72 hours      |
+-------------------------------------------------------------------------------+
```

---

## 2. DIRECT DIGITAL WORKER SOURCING & MATCHING ENGINE

### 2.1 Integration with National Registries
The Clearinghouse connects directly to Bangladesh's national identity and manpower infrastructure via real-time mTLS microservices:

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    NATIONAL REGISTRY INTEGRATION BUS                      │
├───────────────────┬───────────────────┬───────────────────────────────────┤
│ System            │ Integration Type  │ Data Exchanged                    │
├───────────────────┼───────────────────┼───────────────────────────────────┤
│ Election Comm.    │ gRPC / mTLS       │ NID 10/17-digit verification,     │
│ (NID Database)    │                   │ Biometric fingerprint match (1:1) │
├───────────────────┼───────────────────┼───────────────────────────────────┤
│ DIP (Passports)   │ RESTful JSON      │ Machine Readable Passport (MRP) / │
│                   │                   │ e-Passport validity, ICAO data    │
├───────────────────┼───────────────────┼───────────────────────────────────┤
│ BMET Master       │ Event-Driven Kafka│ Candidate registration status,    │
│ Database          │ Streams           │ PDO completion, Smart Card ledger │
├───────────────────┼───────────────────┼───────────────────────────────────┤
│ Ami Probashi      │ REST / Webhooks   │ Mobile candidate profiles, video  │
│ Ecosystem         │                   │ interviews, job offer acceptance  │
├───────────────────┼───────────────────┼───────────────────────────────────┤
│ National Skill    │ RESTful JSON      │ TVET / TTC skill certifications,  │
│ Registry (B-SEP)  │                   │ Welding/Construction/E&E ratings  │
└───────────────────┴───────────────────┴───────────────────────────────────┘
```

### 2.2 Sourcing & Anti-Hoarding Workflow
1. **Direct Digital Sourcing:** Aspiring migrant workers register via the **Ami Probashi App** or at Union Digital Centers (UDCs) / District Employment and Manpower Offices (DEMO). All candidates undergo mandatory biometric capture (10 fingerprints + facial recognition) and skill profile mapping.
2. **Algorithmic Vacancy Matching:** When a Malaysian demand order is ingested, the Clearinghouse matching engine scans the verified candidate database and generates an **Anonymized Candidate Match Set (ACMS)** based strictly on job qualifications, age criteria, and physical fitness metrics.
3. **Anti-Hoarding Tokenization:** 
   - Every matched candidate receives a unique **Migration Tracking UUID (MT-UUID)**.
   - Physical paper demand letters are rendered legally null and void.
   - Demand quotas are represented solely as non-transferable digital cryptographic tokens assigned to specific candidate IDs.
   - If an agency fails to advance an assigned candidate within 5 business days (e.g. scheduling medical or interview), the token expires and the candidate is automatically reassigned.

---

## 3. CENTRALIZED BLIND MEDICAL ALLOCATION SYSTEM

### 3.1 Eliminating the Medical Cartel
In previous recruitment cycles, a cartel of 100 private diagnostic clinics controlled medical testing for Malaysia, charging extortionate rates (BDT 8,000–12,000 vs real cost of BDT 3,500–4,500) and routinely issuing fraudulent fit/unfit certificates to extort bribes.

The **Centralized Blind Medical Allocation System (CBMAS)** eliminates this cartel through:
1. **Universal Accreditation:** Any DGHS-accredited diagnostic center with automated laboratory equipment (minimum 300+ centers across all 64 districts) is eligible to join the network.
2. **Cryptographic Random Assignment:** Candidates cannot choose their medical clinic, and clinics cannot select or solicit candidates.

### 3.2 Cryptographic Blind Allocation Engine (VRF Architecture)

```
Candidate NID Hash (H_c) ──┐
Current Timestamp (T)   ───┼──> [HMAC-SHA256 / NIST SP 800-90B] ──> Uniform Random Value (R)
Daily Master Seed (S_day) ─┘                                                   │
                                                                               ▼
Approved Clinic Capacity Matrix [C_1, C_2, ... C_n] ─────────────> Modulo Mapping Function
                                                                               │
                                                                               ▼
                                                                 Assigned Clinic ID & Nonce
```

#### Mathematical Allocation Formulation:
For a candidate $C_i$ with national identity hash $H(NID_i)$ on day $D_j$, the assigned clinic $K_{target}$ within candidate district $Dist_k$ is computed as:

$$R_i = \text{HMAC-SHA256}\left(S_{\text{daily\_seed}}, H(NID_i) \parallel T_{\text{request}} \parallel Nonce\right)$$

$$Index_{clinic} = R_i \pmod{N_{\text{available\_clinics}(Dist_k)}}$$

$$K_{target} = \text{ClinicList}[Index_{clinic}]$$

Where $S_{\text{daily\_seed}}$ is published on a public bulletin board at 06:00 AM UTC daily, generated from the hash of the latest Bangladesh Bank settlement block, ensuring **unpredictability and verifiable fairness**.

### 3.3 Automated LIMS Integration & Direct FWCMS Upload
To prevent the issuance of forged or doctored medical reports:
1. **Biometric Check-In:** The candidate checks into the assigned clinic using 1:1 fingerprint verification against the NID/BMET biometric token.
2. **Automated Laboratory Instrumentation (LIMS):** Automated analyzers (Hematology, Biochemistry, Digital X-Ray PACS) transmit test values directly to the clinic's local gateway via HL7/ASTM protocols without human operator intervention.
3. **Cryptographically Signed Direct Upload:**
   - The clinic's accredited physician signs the standardized electronic report using a hardware security token (PKI private key).
   - The report is transmitted via mTLS REST API directly to the **Clearinghouse Medical Ledger**, **DGHS Database**, and **Malaysian FWCMS (Bestinet Biomedical Gateway)** simultaneously.
   - Zero physical paper certificates are issued.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 DIRECT MACHINE-TO-MACHINE MEDICAL PIPELINE                  │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ Diagnostic Equipment │ Automated Interface  │ Action Taken                  │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ Digital Chest X-Ray  │ DICOM / PACS Server  │ Automated AI screening for TB │
│                      │                      │ + Radiologist digital sign    │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ Blood Analyzer       │ HL7 Protocol         │ Direct feed of HIV, VDRL,     │
│ (Serology/Biochem)   │                      │ Hepatitis B, Malaria assays   │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ Urine Analyzer       │ ASTM E1394-91        │ Pregnancy, Opiates, Cannabis  │
│                      │                      │ raw telemetry lock            │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ Clinic Gateway       │ mTLS / RSA-4096 Sign │ Packages ISO 27001 medical    │
│                      │                      │ payload -> FWCMS / DGHS / ODC │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

---

## 4. PROBASHI KALLYAN BANK (PKB) & MFI ZERO-UPFRONT-CASH FINANCIAL PIPELINE

### 4.1 The Zero-Upfront-Cash Mandate
Under the **Employer Pays Principle (EPP)** and the MoEWOE zero-extortion framework, the aspiring worker pays **0 BDT upfront cash** out of their pocket. 

All legitimate migration costs (capped at official statutory rates: ~BDT 120,000 to BDT 130,000, or covered directly by employers under RBA compliance) are financed through an **End-to-End Cashless Escrow Pipeline** operated by **Probashi Kallyan Bank (PKB)** in syndication with state-partnered Microfinance Institutions (PKSF, BRAC, Grameen).

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │             PROBASHI KALLYAN BANK (PKB) SMART ESCROW VAULT              │
   └───────┬─────────────────┬─────────────────┬─────────────────┬───────────┘
           │                 │                 │                 │
    (1) Flight Ticket  (2) BMET Fees    (3) Medical Fee   (4) RL Service Fee
           │                 │                 │                 │
           ▼                 ▼                 ▼                 ▼
   [Biman / Airlines]  [BMET Welfare/    [DGHS Accredited   [Recruiting Agency
    Direct Settlement   Smart Card]       Medical Clinic]    Capped Service Fee]
```

### 4.2 Cashless Escrow Disbursement Protocol
No cash is ever disbursed to the worker, local recruiting agent, or middleman (dalal). Disbursement occurs solely via automated inter-bank settlement (BEFTN / RTGS) directly to verified institutional vendor accounts upon cryptographic milestone verification:

| Milestone ID | Milestone Trigger | Receiving Entity | Allowable Fee (BDT) | Verification Method |
|--------------|-------------------|------------------|---------------------|---------------------|
| M-01 | Blind Medical Completed | Assigned DGHS Clinic | 4,000 | FWCMS "FIT" API receipt + Digital signature |
| M-02 | BMET Smart Card Issued | BMET Welfare Fund / WEDB | 4,200 | BMET Ledger smart card creation event |
| M-03 | Calling Visa Approved | Malaysian Immigration (JIM) | Direct (Employer paid) | FWCMS eVDR token validation |
| M-04 | Air Ticket Issued | Airline / GDS API | 35,000 – 45,000 | Confirmed PNR + e-Ticket issuance hash |
| M-05 | Pre-Departure Briefing | TTC / BMET Institute | 1,000 | Biometric PDO attendance verification |
| M-06 | Agency Processing Cap | Processing RL Account | 20,000 – 30,000 | Worker departure stamp via airport API |
| **TOTAL** | **Full Deployment Package** | **Direct Institutional Escrow** | **~BDT 65,000–85,000** | **100% Cashless Settlement** |

### 4.3 Post-Arrival Digital Salary Deduction & Cross-Border Servicing
Where statutory costs are structured as a collateral-free, low-interest migration loan (PKB Migration Loan at 4–7% simple interest per annum), repayment is executed seamlessly through Malaysian digital payroll rails:

```
[Malaysian Employer Digital Payroll]
              │
              ├─ (1) Gross Monthly Salary (Min RM 1,700)
              │
              ▼
[SOCSO / ePPAx / FWCMS e-Wages Integration]
              │
              ├─ Mandatory EPF / SOCSO Deductions
              ├─ PKB Loan Installment (e.g. RM 200 - RM 250 / month for 12 months)
              │
              ▼
[Bank Negara Malaysia (BNM) Licensed Foreign Worker Digital Account]
(e.g., Merchantrade Money, TNG eWallet Foreign Worker, Maybank)
              │
              ▼
[ISO 20022 Cross-Border Settlement Gateway]
              │
              ▼
[Probashi Kallyan Bank (PKB) Bangladesh Account]
(Worker loan balance reduced; automated SMS confirmation to worker & family)
```

#### Protection Safeguards:
- **Statutory Deduction Cap:** Under Section 24 of the Malaysian Employment Act 1955, total salary deductions cannot exceed 50% of monthly earnings. The PKB installment is strictly capped at **15% of net basic wage** (max RM 250/month).
- **Default Reserve & Currency Risk Fund:** A 1% corridor risk levy covers foreign exchange fluctuations (MYR/BDT) and provides credit insurance in cases of employer insolvency, injury, or premature repatriation.

---

## 5. INTEROPERABILITY WITH MALAYSIAN SYSTEMS (FWCMS / TURAP / JIM)

### 5.1 System Integration Landscape
The Open Digital Clearinghouse interfaces directly with Malaysia's tri-partite foreign worker architecture:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MALAYSIAN FOREIGN WORKER INFRASTRUCTURE                  │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Malaysian System               │ Functional Responsibility & Interface      │
├────────────────────────────────┼────────────────────────────────────────────┤
│ FWCMS (Bestinet / KDN / KESUMA)│ Master recruitment workflow, e-Quota,      │
│                                │ Bio-Medical, Calling Visa (eVDR), e-Wages  │
├────────────────────────────────┼────────────────────────────────────────────┤
│ TURAP (KESUMA / JTKSM)         │ Integrated Foreign Worker Management,      │
│                                │ Employer quota approval, Sec 60K compliance│
├────────────────────────────────┼────────────────────────────────────────────┤
│ JIM MyIMMs (Immigration Dept)  │ eVDR Calling Visa issuance, e-Visa         │
│                                │ generation, border entry biometric check   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ FOMEMA (Ministry of Health)    │ Post-arrival 30-day medical screening &    │
│                                │ annual work permit renewal validation      │
└────────────────────────────────┴────────────────────────────────────────────┘
```

### 5.2 API Architecture & Specification

#### 1. Ingest Demand Order Endpoint (Bilateral Gateway)
```http
POST /api/v1/bilateral/demand-order/ingest
Host: clearinghouse.bmet.gov.bd
Content-Type: application/json
Authorization: Bearer <mTLS_Signed_KESUMA_Token>
X-Corridor-Signature: <Ed25519_Signature>

{
  "demand_order_id": "DO-MY-2026-88912",
  "kesuma_approval_ref": "KSM/TURAP/2026/0912",
  "fwcms_quota_id": "FWC-Q-55102",
  "employer": {
    "company_ssm_no": "201901034567",
    "company_name": "Apex Semiconductor Manufacturing Sdn Bhd",
    "sector": "MANUFACTURING",
    "sub_sector": "ELECTRONICS",
    "factory_address": "Bayan Lepas Free Industrial Zone, Penang"
  },
  "quota_details": {
    "total_positions": 500,
    "job_title": "Assembly Line Operator",
    "basic_monthly_wage_myr": 1700.00,
    "overtime_rate_multiplier": 1.5,
    "contract_duration_months": 36,
    "accommodation_provided": true,
    "employer_pays_airfare": true,
    "employer_pays_levy": true
  },
  "required_skills": ["GENERAL_ASSEMBLY", "BASIC_ENGLISH_OR_MALAY"],
  "timestamp_utc": "2026-08-27T10:15:30Z"
}
```

#### 2. Push Medical Status to FWCMS Endpoint
```http
POST /api/v1/fwcms/biomedical/cert-upload
Host: api.fwcms.com.my
Content-Type: application/json
Authorization: Bearer <BD_Clearinghouse_Auth_Token>
X-DGHS-PKI-Signature: <RSA4096_Signature>

{
  "transaction_id": "MED-BD-2026-009812",
  "candidate_passport": "A09182341",
  "candidate_nid": "19942691234567890",
  "bmet_tracking_id": "MT-2026-99120",
  "clinic": {
    "dghs_reg_no": "DGHS-CL-0412",
    "clinic_name": "Padma Diagnostic & Medical Center, Dhaka",
    "certifying_physician_bmdc": "BMDC-DOC-34190"
  },
  "examination_results": {
    "fit_status": "FIT",
    "screening_date": "2026-08-27",
    "valid_until": "2026-11-27",
    "chest_xray_ref": "DICOM-XR-99120",
    "serology_panel_ref": "LAB-SER-88129",
    "biometric_verification_match": true
  },
  "raw_payload_sha256": "8f4a1...9b2c3"
}
```

#### 3. Calling Visa (eVDR) Sync & BMET Smart Card Clearance
```http
POST /api/v1/bilateral/calling-visa/sync
Host: clearinghouse.bmet.gov.bd
Content-Type: application/json
Authorization: Bearer <JIM_Gateway_Token>

{
  "evdr_reference_no": "VDR-2026-KL-00981",
  "fwcms_ref_no": "FWC-AP-991203",
  "candidate_passport": "A09182341",
  "employer_ssm": "201901034567",
  "visa_type": "EMPLOYMENT_PASS_VPTE",
  "validity_expiry_date": "2026-12-31",
  "immigration_status": "APPROVED",
  "jim_digital_seal": "MIIB...JIM_SEAL_HEX"
}
```

---

## 6. SECURITY, DATA SOVEREIGNTY & AUDIT LEDGER

### 6.1 Cryptographic Audit Trail (Event Sourcing)
Every transaction across the corridor—from initial candidate registration to loan clearance—is recorded in an **Append-Only Immutable Event Store**. 
- Each block of events is chained using SHA-256 hashes.
- Daily root hashes are co-anchored into the National Data Center (BCC) and Bangladesh Bank sovereign time-stamping authorities.
- Any attempt by administrative insiders, agency operators, or external actors to backdate, modify, or insert phantom candidates results in an immediate cryptographic fault and system halt.

```
[Event N-1 Hash] ──┐
Event Payload    ──┼──> [SHA-256 Chaining] ──> [Event N Hash] ──> [Anchored Root Ledger]
Actor Signature  ──┘
```

### 6.2 Anti-Dalal Telemetry & Anomaly Detection
The Clearinghouse integrates automated machine learning anomaly detection to uncover illicit intermediary activities:
1. **IP / Device Geofencing:** Flags any agency or IP address attempting to execute high-volume registration requests from centralized cyber-cafes or unrecognized locations.
2. **Payment Pattern Telemetry:** Real-time integration with Bangladesh Bank (NPSB / bKash / Nagad / PKB) flags suspicious bulk cash deposits or secondary mobile money transfers into accounts belonging to recruiting agency personnel or known dalals.
3. **Whistleblower Portal:** An encrypted reporting channel within Ami Probashi allows candidates to report illicit cash demands directly to the MoEWOE Anti-Corruption Taskforce with location-tagged evidence.

---

## 7. IMPLEMENTATION ROADMAP, SLA BENCHMARKS & GOVERNANCE

### 7.1 Four-Phase Implementation Roadmap

```
2026 Q3               2026 Q4               2027 Q1               2027 Q2
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ PHASE 1: CORE    │  │ PHASE 2: BILATERAL│ │ PHASE 3: PILOT   │  │ PHASE 4: FULL    │
│ ODC ENGINE BUILD │  │ INTEGRATION      │  │ DEPLOYMENT (5K)  │  │ CORRIDOR OPEN    │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│• BMET/Ami Sync   │  │• FWCMS API Gate  │  │• 5,000 Worker    │  │• All 1,500 RLs   │
│• VRF Medical     │  │• TURAP Connector │  │  Controlled Pilot│  │  Active          │
│• PKB Escrow Core │  │• JIM eVDR Link   │  │• E2E 0-Cash Audit│  │• Full Scale G2B  │
│• RL Registry Ref │  │• PKB/MY Payroll  │  │• Joint Bilateral │  │• 300K+ Annual    │
│  Architecture    │  │  Cross-Border    │  │  SLA Verification│  │  Clean Workers   │
└──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
```

### 7.2 Service Level Agreement (SLA) & Metric Benchmarks

| Metric | Historical Cartel System (2022–2024) | Open Digital Clearinghouse Target | Verification Authority |
|--------|--------------------------------------|-----------------------------------|------------------------|
| **Worker Out-of-Pocket Cost** | **BDT 500,000 – 650,000** | **BDT 0 (Zero Upfront Cash)** | PKB / Bangladesh Bank Audit |
| **Total Migration Cost Floor** | BDT 650,000 (Extortion markup) | BDT 78,990 – 125,000 (Statutory) | MoEWOE Official Gazetted Rates |
| **Quota Allocation Access** | 25 to 100 Syndicate Members | 1,500+ Valid BMET Licensed RLs | BMET Public License Ledger |
| **Medical Center Access** | 100 Syndicate-Controlled Clinics | 300+ Accredited DGHS Centers | DGHS / MoHFW Verification |
| **End-to-End Processing Time** | 90 to 180 Days (Artificially stalled)| 14 to 21 Business Days | Clearinghouse Telemetry Metrics |
| **Calling Visa Transparency** | Physical paper sales / Extortion | Cryptographic Real-Time Sync | Malaysian Immigration (JIM) |
| **Wage Tracking & Protection** | None (Widespread wage theft) | Automated e-Wages & PKB Remittance| JTKSM / Bangladesh High Comm |

---

## ARCHITECTURAL RECOMMENDATIONS FOR THE MINISTERIAL DECREE

To give immediate legal and regulatory teeth to this technical blueprint prior to bilateral MoU finalization, the Minister of Expatriates' Welfare & Overseas Employment should issue **Three Binding Executive Orders**:

1. **Executive Decree No. 1 — Mandatory ODC Routing:**  
   *Declare that no recruitment order, demand letter, or visa allocation for Malaysia shall have legal validity or receive BMET Emigration Clearance unless it is ingested, processed, and tracked exclusively through the sovereign Open Digital Clearinghouse.*
2. **Executive Decree No. 2 — Demolition of Medical Cartelization via VRF:**  
   *Stipulate that all pre-departure medical screenings for Malaysia must be allocated via the Centralized Blind Medical Allocation System (CBMAS) across all DGHS-accredited facilities, prohibiting any pre-selected or restricted clinic lists.*
3. **Executive Decree No. 3 — 100% Cashless Statutory Escrow via PKB:**  
   *Prohibit the direct collection of any cash payments from workers by recruiting agencies, intermediaries, or travel agents, mandating that all legitimate costs be routed through PKB/MFI cashless escrow accounts with automated payroll deductions in Malaysia.*

---
*Report certified and compiled by Survey Spec Miner 2 (Technical Architect & Clearinghouse Specialist).*
