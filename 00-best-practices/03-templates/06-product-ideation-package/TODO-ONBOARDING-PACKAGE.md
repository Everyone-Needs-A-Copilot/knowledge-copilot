---
last_updated: 2026-06-29
status: active
---

# Onboarding Package Completion Guide

> **Purpose:** Pick this up in a new conversation to finish the docs package
> **How to use:** `/continue` or tell Claude "Check TODO-ONBOARDING-PACKAGE.md for where I left off"
> **Standard:** Option A (Complex Projects) per knowledge-copilot 00-onboarding-package.md

---

## Status Summary

| Status | Count |
|--------|-------|
| NOT STARTED | 21 |
| IN PROGRESS | 0 |
| DONE | 0 |
| STUB | 5 |

---

## Section 1: 00-overview/ (vision + boundaries)

### Gate G1 requirement: Vision + scope + success metrics exist

| # | File | Status | Notes |
|---|------|--------|-------|
| 1 | `00-overview/00-vision.md` | NOT STARTED | Facilitation guide ready. Covers: problem, users, vision, forces, JTBD, AI philosophy, capabilities, ecosystem context, warning signs |
| 2 | `00-overview/10-scope-and-non-goals.md` | NOT STARTED | Facilitation guide ready. Covers: scope, non-goals, anti-features, constraints, integration boundaries |
| 3 | `00-overview/20-success-metrics.md` | NOT STARTED | Facilitation guide ready. Covers: user outcomes, business outcomes, leading/failure indicators, ecosystem health |

---

## Section 2: 10-research/ (evidence that anchors reality)

### Gate G1 requirement: At least 1 completed interview artifact exists

| # | File | Status | Notes |
|---|------|--------|-------|
| 4 | `02-user-guides/10-research/10-interviews/00-interview-template.md` | DONE | Generic interview template — copy and rename for each interview |
| 5 | `02-user-guides/10-research/10-interviews/01-interview-self.md` | NOT STARTED | Self-interview (product owner interviews themselves as primary user) |

---

## Section 3: 20-service-design/ (service blueprint + journeys)

### Gate G1 requirement: Journeys/JTBD/MTMs exist

| # | File | Status | Notes |
|---|------|--------|-------|
| 6 | `02-user-guides/20-service-design/30-jtbd.md` | NOT STARTED | Jobs to be done across all personas |
| 7 | `02-user-guides/20-service-design/20-journey-maps.md` | NOT STARTED | Personas, journey narrative, struggling moments, emotional arc |
| 8 | `02-user-guides/20-service-design/40-moments-that-matter.md` | NOT STARTED | Critical moments with success/failure criteria |
| 9 | `02-user-guides/20-service-design/10-service-blueprint.md` | NOT STARTED | Frontstage, backstage, support processes |

---

## Section 4: 30-requirements/ (what we will build + verify)

### Gate G1 requirement: User stories + scenarios/use cases exist

| # | File | Status | Notes |
|---|------|--------|-------|
| 10 | `03-developer-guides/30-requirements/10-user-stories.md` | NOT STARTED | User stories grouped by persona, prioritized |
| 11 | `03-developer-guides/30-requirements/20-use-cases-and-scenarios.md` | NOT STARTED | E2E scenarios, edge cases, CV scenarios |
| 12 | `03-developer-guides/30-requirements/30-acceptance-criteria.md` | NOT STARTED | Given/When/Then, performance, quality criteria |

---

## Section 5: 40-design-challenge/ (what to prototype)

### Gate G4 requirement: Design challenge brief exists and is approved

| # | File | Status | Notes |
|---|------|--------|-------|
| 13 | `03-developer-guides/40-design-challenge/00-brief.md` | NOT STARTED | Critical views, creative direction, concepts per view, evaluation criteria |

---

## Section 6: Experience Design

| # | File | Status | Notes |
|---|------|--------|-------|
| 14 | `02-user-guides/20-service-design/50-ux-design.md` | NOT STARTED | IA, task flows, interaction patterns, responsive, accessibility |
| 15 | `02-user-guides/20-service-design/60-ui-design.md` | NOT STARTED | Visual direction, design tokens, component patterns |
| 16 | `02-user-guides/20-service-design/70-copy-voice.md` | NOT STARTED | Voice character, speech patterns, key UI copy, banned language |

---

## Section 7: 50-prototypes/ (prototype standards + hub spec)

### Gate G5 requirement: CV prototype set approved

| # | File | Status | Notes |
|---|------|--------|-------|
| 17 | `03-developer-guides/50-prototypes/00-prototype-standards.md` | NOT STARTED | Created by factory (CDO+CTO) |
| 18 | `03-developer-guides/50-prototypes/10-prototype-hub-requirements.md` | NOT STARTED | Created by factory (CDO+CTO) |

---

## Section 8: 60-e2e-mapping/ (CVs to E2E)

### Gate G6 requirement: E2E journeys doc + view map exist

| # | File | Status | Notes |
|---|------|--------|-------|
| 19 | `03-developer-guides/60-e2e-mapping/00-e2e-journeys.md` | NOT STARTED | Created by factory (SD+UXD) |
| 20 | `03-developer-guides/60-e2e-mapping/10-view-map.md` | NOT STARTED | Created by factory (UXD) |

---

## Section 9: 70-technical-planning/ + 04-architecture/

### Gate G8 requirement: Data model + architecture + test plan + security + work breakdown

| # | File | Status | Notes |
|---|------|--------|-------|
| 21 | `04-architecture/10-data-model.md` | NOT STARTED | Created by factory (CTO/TA) |
| 22 | `04-architecture/20-architecture.md` | NOT STARTED | Created by factory (CTO/TA) |
| 23 | `03-developer-guides/70-technical-planning/30-test-plan.md` | NOT STARTED | Created by factory (QA) |
| 24 | `03-developer-guides/70-technical-planning/40-security.md` | NOT STARTED | Created by factory (SEC) |
| 25 | `03-developer-guides/70-technical-planning/50-work-breakdown.md` | NOT STARTED | Created by factory (CTO/TA) |

---

## Section 10: Infrastructure stubs

| # | File | Status | Notes |
|---|------|--------|-------|
| 26 | `01-setup/README.md` | STUB | Before Gate G2 |
| 27 | `05-api-reference/README.md` | STUB | During development |
| 28 | `06-deployment/README.md` | STUB | Before Gate G9 |
| 29 | `07-troubleshooting/README.md` | STUB | Post-launch |
| 30 | `09-appendix/README.md` | STUB | Glossary + related docs |

---

## Section 11: Factory governance

| # | File | Status | Notes |
|---|------|--------|-------|
| 31 | `08-design-factory/README.md` | DONE | Overview |
| 32 | `08-design-factory/GOVERNANCE.md` | DONE | Operating constitution |
| 33 | `08-design-factory/DEFINITION-OF-DONE.md` | DONE | DoD checklist |
| 34 | `08-design-factory/RISK-CLASSIFICATION.md` | DONE | Risk tiers |
| 35 | `08-design-factory/templates/ADR.template.md` | DONE | ADR template |
| 36 | `08-design-factory/templates/SECURITY.template.md` | DONE | Security review template |
| 37 | `08-design-factory/templates/SPEC.template.md` | DONE | Feature spec template |
| 38 | `08-design-factory/templates/TESTPLAN.template.md` | DONE | Test plan template |

---

## Completion Checklist by Gate

### Gate G1 — Ideation Package Complete
- [ ] Vision + scope + success metrics (#1-3)
- [ ] At least 1 completed interview (#5)
- [ ] Journeys/JTBD/MTMs (#6-9)
- [ ] User stories + scenarios/use cases (#10-12)
- **Status: NOT STARTED**

### Gate G4 — Design Challenge Approved
- [ ] Design challenge brief (#13)
- [ ] Critical views list approved
- **Status: NOT STARTED**

### Gate G5 — CV Prototype Set Approved
- [ ] Prototype standards (#17)
- [ ] Prototype hub requirements (#18)
- **Status: NOT STARTED**

### Gate G6 — E2E Mapping Complete
- [ ] E2E journeys doc (#19)
- [ ] View map (#20)
- **Status: NOT STARTED**

### Gate G8 — Technical Plan Approved
- [ ] Data model + architecture (#21-22)
- [ ] Test plan (#23)
- [ ] Security plan (#24)
- [ ] Work breakdown (#25)
- **Status: NOT STARTED**

### Gate G9 — Release Candidate Approved
- [ ] All above gates passed
- [ ] Setup/deployment docs filled in
- **Status: NOT STARTED**
