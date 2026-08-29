# Master System Design & UX/UI Architecture
## The Desktop SaaS Portal ("Keystone Workforce Bridge") & The Mobile PWA ("Probashi Kormoshetu / Deshantari")

**Classification:** Full Product & Interface Design Specification (Part R7)  
**Target Systems:** Desktop Web SaaS (Next.js 16) & Mobile PWA (React 19 + PWA Service Worker)  
**Date:** August 2026  

---

## 1. System Naming & Architectural Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                SYSTEM NAMING TAXONOMY                                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. The Macro Platform:       ProbashiOS: The Clean Corridor Operating System           │
│ 2. The Bangladesh Brand:     প্রবাসী কর্মসেতু (Probashi Kormoshetu)                     │
│ 3. The Desktop Portal:       Keystone Workforce Bridge (Enterprise SaaS)               │
│ 4. The Mobile Application:   Deshantari PWA (Voice-Assisted Rural Worker & UDC App)    │
│ 5. The Architecture Pattern: The Tripartite Clean Corridor Architecture (TCCA)         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component A: The Desktop SaaS Web Portal (Keystone Workforce Bridge)

**Target Users:** Malaysian HR Directors, BMET Desk Officers, Bangladesh High Commission Labour Wing (KL), and Licensed Agencies (RLs).  
**Tech Stack:** Next.js 16 (App Router), Tailwind CSS, shadcn/ui, TypeScript, Supabase/PostgreSQL.

### 2.1 Information Architecture & Navigation Hierarchy

```
Keystone Desktop Portal
├── 1. Executive Mission Control (Corridor Metrics, Active Quotas, Deployment Speed)
├── 2. Job Demand Ingestion (KESUMA Section 60K Upload, Wage Formula, ESG Housing Audit)
├── 3. Algorithmic Candidate Matching (Trade Filter, Porichoy NID Verified Pool, Batch Review)
├── 4. US CBP / RBA Zero-Debt Compliance Vault (Immutable Audit Ledger, Zero-Fee Certs)
├── 5. FWCMS Calling Visa (VDR) & Flight Manifests (Automated Sync, Biman/AirAsia E-Tickets)
└── 6. Escrow & Banking Settlement (Probashi Kallyan Bank RTGS Disbursement Tracker)
```

### 2.2 Wireframe 1: Malaysian Employer Bulk Job Order Intake View

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│  KEYSTONE WORKFORCE BRIDGE | Malaysian Employer Portal                 [Inari Tech Bhd]  │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│  [ Dashboard ]  [ Post Job Quota ]*  [ Candidate Batches ]  [ Compliance Vault ] [ Flights ]│
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  NEW JOB ORDER INTAKE (KESUMA eQuota Section 60K)                                        │
│  ────────────────────────────────────────────────                                        │
│  1. KESUMA Approval Reference No: [ KSM/100/2026/008819        ] [ Upload PDF Slip (✓) ] │
│  2. Industry Sector:              [ Electronics & Semiconductor ▼ ]                      │
│  3. Job Designation:              [ SMT Machine Operator       ]                         │
│  4. Required Quota Count:         [ 250 Workers                ]                         │
│  5. Monthly Basic Wage (MYR):     [ RM 1,800.00                ] (Min. statutory RM 1.5k)│
│  6. Guaranteed Overtime / Day:    [ 2.0 Hours (1.5x OT)        ]                         │
│  7. Accommodation Standard:       [ Free Central Dormitory (JTK Certified - Act 446) (✓)] │
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ ILO / US CBP ZERO-RECRUITMENT-FEE COMMITMENT                                       │  │
│  │ [✓] Employer agrees to bear Malaysian Levy (RM 1,850), Visa, FWCMS, and Insurance. │  │
│  │ [✓] Zero recruitment fee is charged to the Bangladeshi worker.                     │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                          │
│                          [ SAVE DRAFT ]       [ SUBMIT TO BMET CLEARINGHOUSE ──► ]       │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component B: The Mobile-First PWA (Deshantari / Probashi Kormoshetu)

**Target Users:** 5,200+ Union Digital Center (UDC) Entrepreneurs, BMET Vocational Students, and Rural Bangladeshi Candidates.  
**Tech Stack:** React 19, Tailwind CSS, Vite PWA (Workbox Service Worker), Web Speech API / HTML5 Audio (Dialect Voice Guides).

### 3.1 PWA Key Design Constraints for Rural Bangladesh
* **Sub-50KB Core Bundle:** Instant load on 3G cellular connections in rural villages.
* **Offline-First Storage:** IndexedDB caches candidate drafts even when electricity/internet cuts out.
* **Dialect Audio Prompts:** Built-in Bangla voice narrator reads instructions aloud for illiterate candidates.

---

### 3.2 Wireframe 2: Worker Mobile PWA — 4 Core Screen Flows

#### Screen 1: Assisted NID Registration (Porichoy API)
```
┌────────────────────────────────────────┐
│  প্রবাসী কর্মসেতু (Probashi Kormoshetu)  │
│  [🔊 শুনুন / Audio Guide]      [বাংলা ▼]│
├────────────────────────────────────────┤
│                                        │
│  ধাপ ১: পরিচয় যাচাই (NID Verification) │
│  ───────────────────────────────       │
│                                        │
│  [   জাতীয় পরিচয়পত্র স্ক্যান করুন    ] │
│  [      (Scan NID Card)              ] │
│                                        │
│  জাতীয় পরিচয়পত্র নম্বর:                │
│  [ 19942691234567890                 ] │
│                                        │
│  জন্ম তারিখ:                           │
│  [ ১৫ জুন ১৯৯৪                       ] │
│                                        │
│  [✓] পরিচয় যাচাই সম্পন্ন (Porichoy API)│
│  নাম: মো: রহিম মিয়া                     │
│  জেলা: টাঙ্গাইল | ইউনিয়ন: হাদিরা         │
│                                        │
│  কাজের দক্ষতা নির্বাচন করুন:             │
│  (●) ফ্যাক্টরি অপারেটর  ( ) ওয়েল্ডার   │
│  ( ) কনস্ট্রাকশন        ( ) ক্লিনার     │
│                                        │
│  [ পরবর্তী ধাপ (Next Step) ──► ]       │
└────────────────────────────────────────┘
```

#### Screen 2: Transparent Matched Job Card
```
┌────────────────────────────────────────┐
│  প্রবাসী কর্মসেতু — চাকরির প্রস্তাব     │
├────────────────────────────────────────┤
│                                        │
│  🎉 অভিনন্দন রহিম! একটি চাকরি পাওয়া গেছে│
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ 🇲🇾 ইনসারি টেকনোলজি (পেনাং)       │  │
│  │ পদবি: ফ্যাক্টরি মেশিন অপারেটর     │  │
│  │                                  │  │
│  │ 💰 মাসিক বেতন: RM ১,৮০০ + ওভারটাইম│  │
│  │    (প্রায় ৳৪৮,৫০০ টাকা প্রতি মাসে)│  │
│  │                                  │  │
│  │ 🏠 থাকা-খাওয়া: সম্পূর্ণ ফ্রি      │  │
│  │ ✈️ বিমান টিকিট: ব্যাংক ঋণ (০ নগদ) │  │
│  │                                  │  │
│  │ 🟢 আপনার নগদ খরচ: ০ টাকা        │  │
│  │    (কোনো দালালকে টাকা দেবেন না!) │  │
│  └──────────────────────────────────┘  │
│                                        │
│  [🔊 চাকরির বিবরণ শুনুন (Listen)]      │
│                                        │
│  [  চাকরিতে সম্মতি প্রদান করুন (Accept) ]│
└────────────────────────────────────────┘
```

#### Screen 3: Zero-Cash Migration Loan Wallet (Probashi Kallyan Bank)
```
┌────────────────────────────────────────┐
│  প্রবাসী কল্যাণ ব্যাংক — ০ নগদ ঋণ ওয়ালেট│
├────────────────────────────────────────┤
│                                        │
│  মোট অনুমোদিত অভিবাসন খরচ: ৳৭৮,৯৯০ টাকা │
│  (আপনার পকেট থেকে কোনো টাকা দিতে হবে না)│
│                                        │
│  ব্যাংক সরাসরি পরিশোধ করেছে:            │
│  • বিমান টিকিট (বিমান বাংলাদেশ): ৳৩৫,০০০│
│  • মেডিকেল টেস্ট (ডিজিএইচএস):    ৳৮,০০০ │
│  • বিএমইটি স্মার্ট কার্ড ও বীমা: ৳১৫,৯৯০ │
│  • রিক্রুটিং এজেন্সি সার্ভিস ফি: ৳২০,০০০ │
│                                        │
│  মালয়েশিয়ায় কিস্তি পরিশোধ প্ল্যান:     │
│  • প্রতি মাসে কর্তন: RM ২৫০ (৳৬,৫০০)   │
│  • মোট সময়: মাত্র ৬ মাস                │
│  • ৭ম মাস থেকে ১০০% আয় নিজের!         │
│                                        │
│  [ ডিজিটাল স্মার্ট পাস ডাউনলোড করুন (QR) ]│
└────────────────────────────────────────┘
```

#### Screen 4: 15-Second Anti-Extortion Video Affidavit
```
┌────────────────────────────────────────┐
│  ভিডিও হলফনামা (Video KYC Affidavit)   │
├────────────────────────────────────────┤
│                                        │
│  বিএমইটি অফিসারের সামনে ক্যামেরা খুলুন │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │                                  │  │
│  │          [ LIVE CAMERA ]         │  │
│  │                                  │  │
│  │   "আমি মো: রহিম মিয়া।            │  │
│  │    আমি স্বেচ্ছায় মালয়েশিয়া যাচ্ছি। │  │
│  │    আমি কোনো দালালকে নগদ          │  │
│  │    টাকা দেইনি।"                  │  │
│  │                                  │  │
│  └──────────────────────────────────┘  │
│                                        │
│  [ 🔴 ১৫ সেকেন্ডের ভিডিও রেকর্ড করুন ]  │
│                                        │
│  [ বিএমইটি অফিসার স্বাক্ষর ও ছাড়পত্র ]  │
└────────────────────────────────────────┘
```

---

## 4. Summary for Technical & Product Teams

* **Desktop SaaS Portal (`Keystone Workforce Bridge`):** Gives Malaysian employers the exact corporate tool they need to post quotas, automate FWCMS candidate submissions, and get US CBP zero-debt compliance certificates.
* **Mobile-First PWA (`Probashi Kormoshetu`):** Gives rural, semi-literate Bangladeshi workers an easy, voice-guided, zero-dalal mobile experience backed by Porichoy NID verification and Probashi Kallyan Bank cashless escrow.
