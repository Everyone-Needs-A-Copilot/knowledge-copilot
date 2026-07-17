---
last_updated: 2026-06-28
status: active
---

# Design Factory Governance

> The operating constitution for {{PRODUCT_NAME}}'s design-led, agentic software factory.

---

## 0. First Principles (Non-Negotiables)

These are not preferences. They are constraints. Any process, tool, or agent
that violates them is operating outside the factory.

### 1. Design-led creation
Start with the experience. Work backwards into implementation.

The question "how should this work technically?" is always preceded by
"what experience are we creating?" A technically elegant solution that
produces a bad experience is a failed solution.

### 2. CDO vs CTO decision doctrine
- **CTO owns implementation**: how an experience is realised through technology.
  Technology choices that do not affect user outcomes are CTO decisions.
- **CDO owns experience**: when a technology choice will constrain, alter, or
  determine user outcomes, the CDO has final say — with required CTO input.
  Neither role decides in isolation on experience-impacting technical choices.

### 3. MLP, not MVP
We ship **Minimum Lovable Product**. Not the minimum that functions — the minimum
that is genuinely good.

Practically: the approved prototype sets the quality bar. A feature that functions
but does not meet the approved design intent is not done.

### 4. Milestone-based reporting only
No time estimates. No deadlines in documentation or planning artefacts.

Progress is reported as:
- Gate status (Not Started / In Progress / Passed)
- Milestone completion (what is done vs what remains)
- Percentage complete where meaningful

If a stakeholder asks "when will it be done?", the answer is the next gate
criteria and what remains to meet them.

### 5. Safety boundaries
The factory operates within these hard limits:

| Boundary | Rule |
|----------|------|
| Money movement | Never autonomous. Always requires explicit human approval. |
| Contacting humans | Drafts only. No autonomous sending of external communications. |
| Merge and deploy | Requires human approval until explicitly and formally changed. |
| Deletion | Archive only. No permanent deletion of data or artefacts. |

---

## 1. Factory Intake Process

### 1.1 What the factory needs before it starts
The project owner provides a completed onboarding package. The minimum viable
package for Gate G1 includes:

- Vision, problem statement, and target users (`00-overview/00-vision.md`)
- Scope and non-goals (`00-overview/10-scope-and-non-goals.md`)
- Success metrics (`00-overview/20-success-metrics.md`)
- At least one completed research interview (`02-user-guides/10-research/10-interviews/`)
- Jobs to be done (`02-user-guides/20-service-design/30-jtbd.md`)
- Journey maps (`02-user-guides/20-service-design/20-journey-maps.md`)
- Moments that matter (`02-user-guides/20-service-design/40-moments-that-matter.md`)
- User stories (`03-developer-guides/30-requirements/10-user-stories.md`)

See `TODO-ONBOARDING-PACKAGE.md` for full gate-by-gate requirements.

### 1.2 CDO gap analysis (first factory action after intake)
Before any design work begins, the CDO:

1. Reviews the intake package for gaps and ambiguities in experience intent.
2. Produces the full view inventory — every distinct view/screen in the product.
3. Identifies candidate **critical views** (CVs): the views most load-bearing
   for the user's goals and emotional experience.

The critical view shortlist is not final until the project owner approves it.
This approval is required before the design concept competition begins.

---

## 2. Design Concept Competition

For each approved critical view, the factory works with the project owner to produce **five highly distinct** design concepts. These are not variations of one idea. They explore genuinely different directions.

This is collaborative, interactive work. The project owner is in the loop throughout — reviewing concepts as they emerge, providing direction, and making the selection that advances to Phase 2. The factory assists and produces; it does not make direction decisions autonomously.

**Purpose:** Surface the strongest possible direction through competition, not
consensus. Weak concepts reveal what does not work. Strong concepts become
the approved direction.

**Format:** All concepts are coded, interactive Next.js pages. The project owner clicks through a running prototype, not a static presentation.

**Basis:** The project's design system and established patterns. If a needed
component or pattern does not exist in the design system, the project owner
approves it before it is created.

**Gate:** The project owner selects or requests refinement of concepts before
the factory proceeds to prototype.

---

## 3. Gate Definitions

Gates are checkpoints. Work does not proceed past a gate until its criteria
are verified and approved. Gates are not time-based. They are criteria-based.

| Gate | Name | Key criteria |
|------|------|-------------|
| G1 | Ideation Package Complete | Vision, scope, metrics, research, journeys, JTBD, MTMs, user stories |
| G2 | Project Created | Repository exists, local setup documented, CI scaffolded |
| G4 | Design Challenge Approved | Design challenge brief approved, critical views agreed |
| G5 | CV Prototype Set Approved | Prototypes for all critical views approved by project owner |
| G6 | E2E Mapping Complete | All views mapped, journeys documented, prototype hub specced |
| G8 | Technical Plan Approved | Data model, architecture, test plan, security plan, work breakdown |
| G9 | Release Candidate Approved | All above gates passed, setup and deployment docs complete |

Full gate requirements: see `TODO-ONBOARDING-PACKAGE.md`.

---

## 4. Development Execution Model

After Design Approval (post-G5):

- The CTO leads implementation using the approved prototype as the quality bar.
- Testing, security testing, and audits are executed as defined in the test plan.
- Agents assist with implementation but do not autonomously merge or deploy.
- Human approval is required for every merge to main and every production deploy.

The Definition of Done (`DEFINITION-OF-DONE.md`) applies to every piece of work
without exception.

---

## 5. Verification Posture

Nothing is done until verified. Verified means:

- Browser console checked: no JavaScript errors
- Terminal/server logs checked: no runtime errors
- View inspected at target breakpoints: no layout integrity issues

Verbal claims of completion without verification are not accepted. The DoD
checklist must be worked through, not assumed.

**Research before asking.** Agents do not ask the project owner questions that
could be answered by reading the codebase, documentation, or prior decisions.
Questions are for genuine ambiguity, not avoidance of due diligence.
