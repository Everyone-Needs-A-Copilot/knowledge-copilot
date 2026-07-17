---
last_updated: 2026-06-28
status: active
---

# {{PRODUCT_NAME}} — Documentation & Onboarding Package

This directory contains all the documents needed to bring this product to life
through the agentic factory. Each facilitated document has a **facilitation guide**
embedded in HTML comments that drives the conversation.

## How This Works

1. You and I have a conversation for each facilitated document (Phases 1-5)
2. I ask the questions from the facilitation guide
3. You answer in your own words
4. I synthesize your answers into the document
5. We move to the next document in sequence
6. Technical documents (Phase 6-7) are created by factory agents from the experience docs

## How to Resume

When starting a new conversation, run `/continue` or say:
> "I'm working on the {{PRODUCT_NAME}} onboarding package. Check TODO-ONBOARDING-PACKAGE.md for where I left off."

The **TODO-ONBOARDING-PACKAGE.md** is the operational status tracker with
per-file status and gate checklists. Use it as the primary resume point.

## Document Structure

```
├── 00-overview/                    # Vision, scope, metrics
├── 01-setup/                       # Local dev setup (stub until G2)
├── 02-user-guides/
│   ├── 01-research/01-interviews/  # Interview artifacts
│   └── 02-service-design/          # JTBD, journeys, UX, UI, copy
├── 03-developer-guides/
│   ├── 01-requirements/            # User stories, use cases, AC
│   ├── 02-design-challenge/        # CV brief + concept specs
│   ├── 03-prototypes/              # Standards + hub requirements
│   ├── 04-e2e-mapping/             # E2E journeys + view map
│   └── 05-technical-planning/      # Test, security, work breakdown
├── 04-architecture/                # Data model + system architecture
├── 05-api-reference/               # API docs (stub until dev)
├── 06-deployment/                  # Deploy docs (stub until G9)
├── 07-troubleshooting/             # Issue resolution (stub until launch)
├── 08-design-factory/              # Governance, DoD, risk, templates
├── 09-appendix/                    # Glossary + related docs
├── README.md                       # This file
└── TODO-ONBOARDING-PACKAGE.md      # Status tracker + gate checklists
```

## Conversation Order

The order follows the Human-Centered Development philosophy — Human Advocates
first, then Technical Implementers.

---

### Phase 1: Discovery (Service Designer) — Facilitated

| # | Document | What We Figure Out |
|---|----------|--------------------|
| 1 | [00-vision.md](00-overview/00-vision.md) | Problem, users, vision, forces, JTBD, AI philosophy, A+ capabilities, ecosystem context, guardrails |
| 2 | [01-scope-and-non-goals.md](00-overview/01-scope-and-non-goals.md) | Scope, non-goals, anti-features, design philosophy, integration boundaries, future considerations |
| 3 | [02-success-metrics.md](00-overview/02-success-metrics.md) | User/business outcomes, quantitative/qualitative metrics, operational efficiency, ecosystem health |

### Phase 2: Research & Service Design (Service Designer) — Facilitated

| # | Document | What We Figure Out |
|---|----------|--------------------|
| 4 | [01-interview-self.md](02-user-guides/01-research/01-interviews/01-interview-self.md) | At least 1 interview artifact (notes, quotes, takeaways) |
| 5 | [03-jtbd.md](02-user-guides/02-service-design/03-jtbd.md) | Jobs to be done grouped by persona, priority ranked |
| 6 | [02-journey-maps.md](02-user-guides/02-service-design/02-journey-maps.md) | Per-stage journeys with emotional state, pain, and solve |
| 7 | [04-moments-that-matter.md](02-user-guides/02-service-design/04-moments-that-matter.md) | Critical moments with B-/A+ analysis, pain-to-delight transformations |
| 8 | [01-service-blueprint.md](02-user-guides/02-service-design/01-service-blueprint.md) | Frontstage, backstage, support processes, failure points |

---

**GATE G1 — "Ideation Package Complete"**
- [ ] Vision + scope + success metrics (Phase 1)
- [ ] At least 1 completed interview artifact
- [ ] Journeys / JTBD / Moments That Matter
- [ ] User stories + scenarios / use cases

---

### Phase 3: Requirements (Service Designer + UX Designer) — Facilitated

| # | Document | What We Figure Out |
|---|----------|--------------------|
| 9 | [01-user-stories.md](03-developer-guides/01-requirements/01-user-stories.md) | User stories with inline acceptance criteria, grouped by persona |
| 10 | [02-use-cases-and-scenarios.md](03-developer-guides/01-requirements/02-use-cases-and-scenarios.md) | E2E scenarios, edge cases, CV-specific scenarios |
| 11 | [03-acceptance-criteria.md](03-developer-guides/01-requirements/03-acceptance-criteria.md) | Given/When/Then criteria, performance targets, quality thresholds |

### Phase 4: Experience Design (UX + UI + Copywriter) — Facilitated

| # | Document | What We Figure Out |
|---|----------|--------------------|
| 12 | [05-ux-design.md](02-user-guides/02-service-design/05-ux-design.md) | Information architecture, task flows, interaction patterns |
| 13 | [06-ui-design.md](02-user-guides/02-service-design/06-ui-design.md) | Visual direction, design tokens, component patterns |
| 14 | [07-copy-voice.md](02-user-guides/02-service-design/07-copy-voice.md) | Voice character, speech patterns, key UI copy, banned language |

### Phase 5: Design Challenge (CDO) — Facilitated

| # | Document | What We Figure Out |
|---|----------|--------------------|
| 15 | [00-brief.md](03-developer-guides/02-design-challenge/00-brief.md) | Critical views, concept competition, philosophy descriptors, evaluation criteria |

---

**GATE G4 — "Design Challenge Approved"**
- [ ] Design challenge brief exists and is approved
- [ ] Critical views list approved

---

### Facilitation Boundary

**The facilitated process ends here.**

Phases 1–5 are conversational — you answer questions and I synthesize your answers into documents. The design challenge brief (Phase 5) is the last facilitated output.

After G4 approval, prototyping is interactive, hands-on work. You work directly with Claude Code or your agentic factory to build, review, and iterate on real, running code. The AI assists but you are in the loop — reviewing concepts, approving directions, and deciding what advances to Phase 2. This is not a process the AI drives autonomously.

Technical documents (Phase 6) are generated by factory agents from the experience documents, but again with you in the loop — not as a set-and-forget automation.

---

### Phase 6: Technical Documents (Factory Agents — Not Facilitated)

These are created by CTO, QA, SEC, and design agents from the experience docs.

| Document | Agent | Gate |
|----------|-------|------|
| [01-data-model.md](04-architecture/01-data-model.md) | CTO / TA | G8 |
| [02-architecture.md](04-architecture/02-architecture.md) | CTO / TA | G8 |
| [00-prototype-standards.md](03-developer-guides/03-prototypes/00-prototype-standards.md) | CDO + CTO | G5 |
| [01-prototype-hub-requirements.md](03-developer-guides/03-prototypes/01-prototype-hub-requirements.md) | CDO + CTO | G5 |
| [00-e2e-journeys.md](03-developer-guides/04-e2e-mapping/00-e2e-journeys.md) | SD + UXD | G6 |
| [01-view-map.md](03-developer-guides/04-e2e-mapping/01-view-map.md) | UXD | G6 |
| [01-test-plan.md](03-developer-guides/05-technical-planning/01-test-plan.md) | QA | G8 |
| [02-security.md](03-developer-guides/05-technical-planning/02-security.md) | SEC | G8 |
| [03-work-breakdown.md](03-developer-guides/05-technical-planning/03-work-breakdown.md) | CTO / TA | G8 |

### Phase 7: Factory Governance (Pre-populated)

| Document | Purpose |
|----------|---------|
| [GOVERNANCE.md](08-design-factory/GOVERNANCE.md) | Operating constitution, first principles, gate definitions |
| [DEFINITION-OF-DONE.md](08-design-factory/DEFINITION-OF-DONE.md) | Checklist: experience, engineering, security, operations |
| [RISK-CLASSIFICATION.md](08-design-factory/RISK-CLASSIFICATION.md) | Three-tier risk classification with gate requirements |
| [templates/](08-design-factory/templates/) | ADR, Security Review, Feature Spec, Test Plan templates |

---

## Rules

- Human Advocate documents (Phase 1-5) are completed BEFORE technical docs
- Every technical decision must trace back to a user need
- Human Advocates can veto any decision that harms user experience
- No time estimates — use phases, priorities, complexity, and dependencies
- Gate checks are hard stops — no phase begins without approval
- MLP, not MVP — the approved prototype is the quality bar
- Prototypes are real, coded, interactive Next.js views — not wireframes, Figma exports, or PDFs. Every concept must be runnable with `pnpm dev` and clickable in a browser

---

**Detailed status tracking:** [TODO-ONBOARDING-PACKAGE.md](TODO-ONBOARDING-PACKAGE.md)
