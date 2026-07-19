# ROUND 2 — INVESTOR REVIEW

**Persona:** World-class investor
**Target:** `rounds/r1_hardened_plan.md`
**Method:** Fresh web-grounded adversarial review (not derived from the Qwen PDF)

---

## Objection 8 — The proposed MVP is built on a platform with no confirmed third-party API, and that platform is itself being replaced

**Probability of Rejection if Unresolved: 80%**

Round 1 (§8) proposes an MVP: a dashboard that tracks an employer's FWCMS eQuota status and lets them submit documents. Two problems, both freshly sourced:

1. **No evidence of an official FWCMS third-party integration/API program exists.** A dashboard that "tracks status" either requires FWCMS to expose data to third parties (unconfirmed) or requires employers to hand over their own FWCMS login credentials to this venture — which is itself a security and PDPA liability (see Objection 9).
2. **FWCMS itself is being phased out.** Malaysia's National Integrated Immigration System (NIISe) is rolling out in three phases from March 2026 to full nationwide implementation by October 2028, explicitly designed to replace and consolidate FWCMS and ePPAx. As of the Home Ministry's own June 2026 progress report, NIISe was **29.9% complete**, already slightly behind its own schedule. This venture's likely earliest launch window (post-MoU, best case Q4 2026-Q1 2027) lands squarely inside NIISe's active rollout period — meaning any MVP tightly coupled to today's FWCMS interface risks rework or obsolescence before it's even validated.

The MVP concept from Round 1 needs either (a) explicit confirmation that FWCMS/NIISe supports third-party integration on terms this venture can access, obtained as part of the §2.3 ministry engagement, or (b) a redesign so the MVP's core value doesn't depend on system integration at all (e.g., a document-readiness checklist and compliance-guidance tool that's useful regardless of which government system is live).

## Objection 9 — Handling employer/worker data now carries direct, independent legal liability under Malaysia's 2024 PDPA amendments

**Probability of Rejection if Unresolved: 65%**

The 2024 amendments to Malaysia's Personal Data Protection Act extended the Security Principle directly to **data processors**, not just data controllers — meaning this venture, the moment it processes an employer's FWCMS application data or a worker's passport/document data (as the Round 1 MVP and the existing outreach CRM both do), takes on **independent penalty exposure** if that data is lost, misused, or improperly accessed. The plan currently has no data protection program: no named responsible person, no security review, no breach protocol, no data processing agreements with employer clients. This has to exist before the MVP goes live, not after an incident.

## Objection 10 — The plan still has no revenue number an investor can underwrite, even an illustrative one

**Probability of Rejection if Unresolved: 55%**

Round 1 (§6.4) correctly declines to assert a fixed processing fee given regulatory uncertainty — but "we'll figure out pricing once regulations clarify" is not fundable on its own. An investor needs at least a scenario-bound illustrative model: for each of the Base/Moderate/Severe cost scenarios already in §6.3, pair an illustrative fee and volume assumption so the opportunity size is at least bounded, even while flagged as provisional.

## Objection 11 — Two Day-1 priorities may not actually be parallel tracks — regulatory access may itself depend on the RL partnership

**Probability of Rejection if Unresolved: 50%**

Round 1 presents ministry engagement (§2.3) and umbrella RL negotiation (§3.3) as parallel, independently-running priorities. But the plan's own risk register documents an entrenched incumbent network and a 10-condition regime designed to favor existing licensed agencies. It is entirely plausible that KESUMA/BMET simply won't grant a meaningful meeting to an unlicensed, pre-revenue outside party — and that credible regulatory access requires walking in alongside (or through) an established RL holder. If that's true, §3.3 isn't a parallel task, it's a **prerequisite** to §2.3 actually working. The plan should state this dependency risk explicitly and sequence accordingly, rather than assuming both tracks proceed independently.

## Objection 12 — No team/capacity model for what is now four simultaneous demanding workstreams

**Probability of Rejection if Unresolved: 45%**

Round 1 now asks for: (1) two-country ministry relationship-building, (2) umbrella RL negotiation, (3) an MVP build, and (4) a pilot program — all described as near-term priorities. Nothing in the plan says who does which. An investor will read this as a solo-founder plan with four full-time-equivalent workstreams and ask directly: is that realistic, and what's the hiring/partnership plan to cover the gap?

---

## Summary Table

| # | Objection | Probability of Rejection |
|---|---|---|
| 8 | MVP depends on unconfirmed FWCMS API access + FWCMS is being replaced by NIISe (29.9% done, full rollout by Oct 2028) | 80% |
| 9 | No PDPA 2024 data-processor compliance program despite handling regulated personal data | 65% |
| 10 | No illustrative/scenario-bound revenue number for investor underwriting | 55% |
| 11 | Regulatory access may depend on RL partnership, not run in parallel to it | 50% |
| 12 | No team/capacity model for four simultaneous demanding workstreams | 45% |
