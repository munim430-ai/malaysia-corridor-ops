# Bangladesh Government Official Endpoints Integration Specification
## Connecting the Clean Corridor Platform to Porichoy (NID), BMET, and Probashi Kallyan Bank (PKB)

**Prepared for:** Technical Taskforce & System Architects  
**Authoritative Reference:** ICT Division, Bangladesh Election Commission, BMET, and PKB  
**Classification:** Technical API Integration Specification  
**Date:** August 2026  

---

## 1. Executive Integration Overview

The Open Digital Clearinghouse does not store unverified citizen identity data. It integrates directly with **three existing, official Bangladesh Government REST API gateways**:

```
                              ┌────────────────────────────────────────────────────────┐
                              │            OPEN DIGITAL CLEARINGHOUSE BACKEND          │
                              └───────┬──────────────────┬──────────────────┬──────────┘
                                      │                  │                  │
               ┌──────────────────────┴───────┐   ┌──────┴──────────────┐   │
               │ 1. PORICHOY (porichoy.gov.bd)│   │ 2. BMET MANPOWER DB │   │
               │ • National NID KYC Gateway   │   │ • Trade Skill Pool  │   │
               │ • Biometric Face & Thumb KYC │   │ • Smart Card Exit   │   │
               └──────────────────────────────┘   └─────────────────────┘   │
                                                                            ▼
                                                 ┌─────────────────────────────────────┐
                                                 │ 3. PROBASHI KALLYAN BANK (PKB) CBS  │
                                                 │ • Direct Vendor Escrow Payouts      │
                                                 │ • Automated Salary Deduction Recovery│
                                                 └─────────────────────────────────────┘
```

---

## 2. Gateway 1: Porichoy National ID Verification API (`porichoy.gov.bd`)

### 2.1 Overview & Legal Standing
* **Operator:** ICT Division, Government of Bangladesh & Bangladesh Election Commission (EC).
* **Service:** Porichoy is the official national KYC gateway used by commercial banks, telecom operators (Grameenphone, Robi), and mobile financial services (bKash, Nagad) to verify citizen identities in real time.
* **Why it eliminates fake profiles:** When an illiterate worker registers at a Union Digital Center (UDC), the operator scans the worker's NID and captures a live photo. Porichoy returns a cryptographically signed match with the Election Commission database within 800ms.

### 2.2 REST API Specification: NID Verification Endpoint

#### Request Endpoint:
`POST https://api.porichoy.gov.bd/api/v1/verification/nid`

#### HTTP Headers:
```http
Content-Type: application/json
x-api-key: {{PORICHOY_API_KEY}}
Authorization: Bearer {{PORICHOY_JWT_TOKEN}}
```

#### Request Payload (JSON):
```json
{
  "national_id": "19942691234567890",
  "dob": "1994-06-15",
  "full_name": "MD RAHIM MIA",
  "match_level": "strict",
  "check_fingerprint": true,
  "fingerprint_template": "base64_encoded_iso_template_data...",
  "live_face_image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

#### Response Payload (JSON):
```json
{
  "status": "success",
  "status_code": 200,
  "transaction_id": "PRC-20260829-88192",
  "data": {
    "is_valid": true,
    "nid_matched": true,
    "dob_matched": true,
    "name_similarity_score": 0.98,
    "biometric_verified": true,
    "citizen_details": {
      "name_en": "MD RAHIM MIA",
      "name_bn": "মো: রহিম মিয়া",
      "father_name": "MD ABDUL KARIM",
      "mother_name": "RAHIMA BEGUM",
      "gender": "male",
      "permanent_address": {
        "division": "Dhaka",
        "district": "Tangail",
        "upazila": "Gopalpur",
        "union": "Hadira",
        "village": "Bhabanipur"
      }
    }
  },
  "signature": "SHA256withRSA_signature_from_election_commission..."
}
```

---

## 3. Gateway 2: BMET & Ami Probashi Central Manpower Gateway

### 3.1 Overview
* **Operator:** Bureau of Manpower, Employment and Training (BMET).
* **Function:** Validates pre-departure trade certification from Technical Training Centers (TTC), manages statutory Pre-Departure Orientation (PDOT), and issues the **Emigration Clearance Smart Card**.

### 3.2 Key REST Endpoints:

#### A. Trade Skill & TTC Validation
`GET https://api.bmet.gov.bd/v2/candidates/{national_id}/trade-qualification`
* Returns candidate's certified vocational trade (e.g., *Welder 3G, Electrical Assembler, Machine Operator, Construction Mason*) and TTC certificate number.

#### B. Emigration Clearance Smart Card Trigger
`POST https://api.bmet.gov.bd/v2/emigration/smart-card-issue`
* **Trigger condition:** Calling Visa (VDR) verified + PKB Escrow confirmed + Anti-Extortion Video Affidavit uploaded.
* Returns: **BMET Smart Card QR Code** and Emigration Barcode for airport clearance.

---

## 4. Gateway 3: Probashi Kallyan Bank (PKB) Core Banking Solution (CBS) API

### 4.1 Cashless Escrow Settlement Pipeline

```
[ Worker Cleared Stage 1 HITL ] ──► [ PKB CBS API: POST /api/v1/escrow/disburse ]
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               │                            │                            │
               ▼                            ▼                            ▼
   [ Biman Airline Account ]    [ DGHS Clinic Account ]    [ BMET Smart Card Acc ]
         (BDT 35,000)                  (BDT 8,000)                (BDT 15,990)
```

### 4.2 Automated Remittance Recovery Endpoint
* **How it works:** When the worker's Malaysian salary is deposited into partner banks (Maybank / CIMB / Bank Islam), an automated standing instruction deducts **RM 250/month (~BDT 6,500)** and transfers it via formal SWIFT/NPSB rails to Probashi Kallyan Bank in Dhaka.
* **Webhook Notification:**
  `POST https://api.clearinghouse.gov.bd/v1/pkb/remittance-installment-ack`
  * Logs installment payment and updates worker's credit score.

---

## 5. Security Architecture & Data Privacy

1. **mTLS (Mutual TLS 1.3):** All traffic between the Open Digital Clearinghouse, Porichoy, BMET, and PKB is encrypted using hardware-backed X.509 client certificates.
2. **Zero Plaintext Storage:** Biometric templates and NID numbers are tokenized using SHA-256 with salted hashes; only verified status flags are stored in the application database.
3. **Audit Compliance:** In accordance with the **Digital Security Act / Cyber Security Act** and the **Personal Data Protection Act (PDPA)**, all API calls produce immutable, cryptographically timestamped audit logs.
