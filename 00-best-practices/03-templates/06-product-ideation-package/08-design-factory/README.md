---
last_updated: 2026-06-28
status: active
---

# Design Factory

> The operating model for {{PRODUCT_NAME}}'s design-led, agentic software factory.

---

## What this directory contains

| Document | Purpose |
|----------|---------|
| `GOVERNANCE.md` | The operating constitution: first principles, intake process, gate definitions, decision doctrine |
| `DEFINITION-OF-DONE.md` | The checklist that must be fully verified before any work is considered complete |
| `RISK-CLASSIFICATION.md` | How work is assigned to risk tiers (Critical / High / Standard) and what each tier requires |
| `templates/` | Reusable templates for ADRs, security reviews, feature specs, and test plans |

---

## Templates

| Template | When to use |
|----------|------------|
| `templates/ADR.template.md` | Any significant architecture or technology decision |
| `templates/SECURITY.template.md` | Security review for Tier 1 and Tier 2 work |
| `templates/SPEC.template.md` | Feature specification before development begins |
| `templates/TESTPLAN.template.md` | Test planning for a feature or milestone |

---

## Quick reference: Gate sequence

G1 Ideation → G2 Project Created → G4 Design Challenge → G5 CV Prototypes Approved →
G6 E2E Mapping → G8 Technical Plan → G9 Release Candidate

Full gate requirements: `TODO-ONBOARDING-PACKAGE.md`

---

## The non-negotiables (short form)

1. Design-led — start with experience, work backwards into implementation
2. CDO owns experience, CTO owns implementation; experience-impacting tech decisions need both
3. MLP not MVP — the approved prototype is the quality bar
4. No time estimates — milestones and gates only
5. Safety boundaries: no autonomous money movement, no autonomous external comms, no autonomous merges

Full detail: `GOVERNANCE.md`
