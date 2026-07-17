---
last_updated: 2026-06-28
status: active
---

# Design Challenge Brief

<!--
FACILITATION GUIDE — CDO (Chief Design Officer)
=================================================
The design challenge brief defines what the CDO and design team
will prototype during the Critical Views (CV) phase. This is the
bridge between ideation and the factory.

PREREQUISITE: ALL Phase 1-4 documents must be completed before
this brief is written. The brief synthesizes everything into
actionable design direction.

This document is typically synthesized by the CDO from all prior
documents, NOT directly from a conversation. However, the product
owner must approve the brief before CV work begins (Gate G4).

CONVERSATION FLOW:
1. Understand where this brief sits in the factory intake process
2. Define the critical views that need to be prototyped
3. Define what a "Critical View" is (and what it is not)
4. Establish creative direction (drawing from UI Design doc)
5. Define the concept competition format (5 concepts per CV)
6. Define philosophy descriptor naming requirements
7. Set constraints and evaluation criteria
8. Establish the approval gate process

QUESTIONS TO ASK:

## Round 1: Process Position
- "Before we define the views, let's confirm where this brief sits
  in the factory intake process."
- Map the steps: vision docs → CDO gap analysis → view inventory →
  product owner approves critical view list → concept competition
  (this brief) → direction converges → full prototype → approval →
  development begins.
- "Which of these gates has the product owner already passed?
  Where are we now?"
- "What is the Stop-the-Line rule for the design-to-development
  transition?"

## Round 2: Critical Views
- "Based on everything we've designed, what are the critical
  views that need to be prototyped?"
- "Which views represent the core experience?"
- "Which views test the riskiest design decisions?"
- "For {{PRODUCT_NAME}}, candidates might include the primary dashboard,
  the core workflow view, any AI output surface, and any configuration view"

## Round 3: What Is a Critical View
- "A critical view is not just any screen — it is a screen that is:
    1. Directly tied to a Moment that Matters
    2. A primary product differentiator
    3. The view a user encounters at a decision point that determines
       whether the product earns trust or gets abandoned"
- "For each candidate view: Is it tied to a Moment that Matters?
  Is it a differentiator? Is it a trust decision point?"
- "Which candidate views fail this test and should be deprioritized?"

## Round 4: Creative Direction
- "What's the creative direction for these prototypes?"
- Pull from 60-ui-design.md (when available): visual direction,
  design tokens, anti-direction.
- "What is the anti-example — the thing this must never look like?"
- "Are there specific design risks to test in the prototypes?"
- "What does 'good design' mean for this product? What's the
  quality bar?"

## Round 5: Concept Competition Format
- "For each critical view, the design team will produce FIVE distinct
  visual concepts."
- "This is not five variations of the same idea. It is five genuinely
  different answers to the question 'what could this view be?'"
- "A concept is distinct if it differs in at least two dimensions:
    - Layout paradigm (card grid vs. single-column vs. split pane)
    - Information hierarchy (what is shown first, what is hidden)
    - Interaction model (tap-and-reveal vs. always-visible vs. progressive disclosure)
    - Typographic system (display-driven vs. data-table-driven vs. conversational)
    - Color expression (high-contrast dark vs. light and airy vs. warm and editorial)
    - Motion philosophy (instant vs. deliberate animation vs. ambient feedback)"
- "'We made the button a different color' is not a distinct concept.
  'We redesigned the information architecture' is a distinct concept."

## Round 6: Philosophy Descriptor Naming
- "Each concept must be named with a short descriptor that communicates
  its design philosophy."
- "Names like 'Minimal Presence,' 'Editorial Intelligence,' 'Dark Focus,'
  or 'Structured Clarity' help the product owner and CDO discuss concepts
  without pointing at screenshots."
- "The name should answer: 'What is this concept's relationship to the
  user and to information?'"
- "Name them before presenting. Never show concepts without names."

## Round 7: Constraints
- "What technical constraints must the prototypes respect?"
- "What interactions must work in the prototypes vs. what can use placeholder data? (Everything is coded — the question is depth of behavior, not whether to code it.)"
- "What data should the prototypes use? Representative fixture data is expected. Real API data is not required."
- "What devices must prototypes work on?"
- "What accessibility requirements apply from day one?"

## Round 8: Evaluation Criteria
- "How will you evaluate the prototypes?"
- "What does 'good' mean for each view?"
- "What would be an instant rejection?"
- "What matters most: visual quality, interaction quality, or
  information architecture?"
- "Before concepts reach the product owner, what does the CDO
  pre-screen against?"

SYNTHESIS:
This document becomes the assignment for the design team.
It must be specific enough that the CDO can hand it to the
UX/UI/UID agents and they can produce prototypes without
further clarification. It includes: process position diagram,
critical view definitions, creative direction, concept competition
rules, naming requirements, constraints, and evaluation criteria.

NOTE ON POST-BRIEF WORK:
Once this brief is approved (Gate G4), the work that follows is
interactive, not facilitated. The product owner works directly with
Claude Code or the agentic factory to build, review, and iterate on
coded prototypes. The AI assists — it does not drive. The product owner
is in the loop at every step: reviewing concepts, approving directions,
and deciding what advances.
-->

## 1. Brief Overview

### 1.1 Purpose

This document is the design team's mandate for Phase 1 of {{PRODUCT_NAME}}'s creation. Before any line of application code is written, the design team will produce multiple visual concept prototypes for each critical view. The product owner will react to these concepts, direction will converge, and the approved direction becomes the MLP bar.

This is not wireframing. It is a concept competition.

### 1.2 Primary Audience

| Role | Responsibility |
|------|----------------|
| CDO (Chief Design Officer) | Leads concept production; owns CDO-level design approvals |
| UI Designers | Produce the five distinct visual concepts per critical view |
| UX Designers | Validate that concepts respect the UX flows and JTBD |
| Product Owner | Reviews, reacts, approves; gates all design-to-development transitions |

### 1.3 Process Position

This brief sits at Step 5 of the factory intake process. The steps that precede and follow it are:

```
[Product owner provides vision docs]
      |
      v
[CDO gap analysis]
      |
      v
[CDO produces view inventory]
      |
      v
[Product owner approves critical view list] ✓
      |
      v
[Concept competition — this brief] <-- YOU ARE HERE
      |
      v
[Product owner reacts, direction converges]
      |
      v
[Full prototype — all views and scenarios]
      |
      v
[Product owner reviews prototype]
      |
      v
[Prototype approved]
      |
      v
[Demo branch + feature branch]
      |
      v
[Agentic development begins]
```

**Gate G4 — Design Challenge Approved** is the Stop-the-Line gate for design. No concepts are produced until this brief is fully approved by the product owner.

---

## 2. Critical Views

### 2.1 What Is a Critical View

A critical view is a screen or phase within {{PRODUCT_NAME}} that is:

- Directly tied to a Moment that Matters
- A primary product differentiator — something that makes {{PRODUCT_NAME}} distinct from anything else on the market
- The view a user will encounter at a decision point that determines whether the product earns love or gets abandoned

The design quality of critical views sets the MLP bar for the entire product.

### 2.2 Critical View Summary

<!-- Fill in once the product owner approves the critical view list -->
<!-- Format: CV number | View name | Type (Screen / Phase) | Phase -->

| CV | View | Type | Phase |
|----|------|------|-------|
| CV1 | | | |
| CV2 | | | |
| CV3 | | | |
| CV4 | | | |
| CV5 | | | |

### 2.3 Critical View Definitions

<!-- For each critical view, provide the full definition using this structure -->

---

**CV1 — [View Name]**

| Attribute | Detail |
|-----------|--------|
| Screens | |
| Phase | |
| Primary user | |
| Why critical | |
| Design imperative | |
| Constraint | |

---

**CV2 — [View Name]**

| Attribute | Detail |
|-----------|--------|
| Screens | |
| Phase | |
| Primary user | |
| Why critical | |
| Design imperative | |
| Constraint | |

---

**CV3 — [View Name]**

| Attribute | Detail |
|-----------|--------|
| Screens | |
| Phase | |
| Primary user | |
| Why critical | |
| Design imperative | |
| Constraint | |

---

**CV4 — [View Name]**

| Attribute | Detail |
|-----------|--------|
| Screens | |
| Phase | |
| Primary user | |
| Why critical | |
| Design imperative | |
| Constraint | |

---

**CV5 — [View Name]**

| Attribute | Detail |
|-----------|--------|
| Screens | |
| Phase | |
| Primary user | |
| Why critical | |
| Design imperative | |
| Constraint | |

---

## 3. Creative Direction

### 3.1 Philosophy
<!-- Summary from 60-ui-design.md (when available), plus governing creative principles -->
<!-- Example structure: name two reference points, explain how they apply -->

### 3.2 The Quality Bar
<!-- What does "good" mean for this product? What is the product owner's standard? -->
<!-- Be explicit. "Functionally complete" is not the bar. Name the actual bar. -->

### 3.3 Anti-Examples
<!-- What must this product NEVER look like? What is the clearest signal of what to avoid? -->

### 3.4 Tone and Texture

| Quality | What It Means in Practice |
|---------|--------------------------|
| | |

---

## 4. Design System Basis

### 4.1 Foundation
<!-- What design system is the basis? What reference product should designers study? -->

### 4.2 Component Rules

```
[Design need arises]
      |
      v
[Component exists in design system?]
  YES: Use existing component — CDO approves usage
  NO:  Design new component — product owner approves first
              |
              v
       [Component added to design system]
              |
              v
       [CDO can approve future uses without product owner]
```

---

## 5. Concept Competition Rules

### 5.1 Deliverable

For each approved critical view, the design team will produce **five distinct visual concepts**.

This is not five variations of the same idea. It is five genuinely different answers to the question "what could this view be?"

| Type | CVs | Concepts per CV | Total |
|------|-----|-----------------|-------|
| Screen-level | CV1–CV[X] | 5 | [X × 5] |
| **Total** | **[X]** | — | **[X × 5]** |

Five concepts per view. No exceptions. The purpose is to give the product owner real range — so that direction can emerge from reaction, not from a single guess.

### 5.2 What "Distinct" Means

A concept is distinct from another concept if it differs in at least two of the following:

| Dimension | Example Contrast |
|-----------|-----------------|
| Layout paradigm | Card grid vs. single-column sequential vs. split pane vs. full-bleed |
| Information hierarchy | What is shown first, what is hidden, what is never shown |
| Interaction model | Tap-and-reveal vs. always-visible vs. progressive disclosure |
| Typographic system | Display-driven vs. data-table-driven vs. conversational |
| Color expression | High-contrast dark vs. light and airy vs. warm and editorial |
| Motion philosophy | Instant transitions vs. deliberate animation vs. ambient feedback |

"We made the button a different color" is not a distinct concept. "We redesigned the information architecture so the primary action is discovery-led" is a distinct concept.

### 5.3 Philosophy Descriptor Naming

Each concept must be named with a short descriptor that communicates its design philosophy before it is presented.

**Requirements:**
- The name communicates the concept's relationship to the user and to information
- The name enables verbal discussion without pointing at screenshots
- The name reflects a coherent design position, not a mood board word

**Examples of valid names:** "Minimal Presence," "Editorial Intelligence," "Dark Focus," "Structured Clarity," "Ambient Confidence"

**Examples of invalid names:** "Concept A," "Blue Version," "Modern," "Clean"

Name concepts before presenting them. Never show a concept without a philosophy descriptor.

### 5.4 Prototype Fidelity

Concepts must be coded, interactive Next.js pages served by the dev server. No Figma frames, no static exports, no PDFs.

Each concept is a running page at `localhost:3000/prototypes/cv-XX/concept-X`.

Concepts must be:

- **Visually complete** — the aesthetic expression must be legible. Colors, type, spacing, and visual weight must be defined, not placeholder.
- **Interaction-representative** — the primary interaction pattern must be functional and clickable. Not every micro-state needs to be built, but the core interaction works.
- **Runnable** — `pnpm dev` starts the server and the concept is immediately navigable in a browser.

Concept-phase prototypes are scoped in complexity — fewer states, simpler data, a single primary flow — but they are still interactive, clickable code. The product owner reacts to a real experience, not a picture of one.

### 5.5 What Is NOT Required at This Stage

- Complete component coverage of every state
- Production-grade accessibility implementation (though WCAG thinking should inform the design)
- Real API calls or live data (representative fixture data is required)
- Full responsive breakpoint coverage

What IS required: a running Next.js page that renders the view with representative data and responds to user interaction for the primary action.

---

## 6. Constraints and Guardrails

### 6.1 Vision Alignment

Every concept must be consistent with the product vision (`00-vision.md`). The AI philosophy section of the vision is the design guardrail, not just the engineering guardrail.

| Vision Principle | Design Implication |
|------------------|--------------------|
| [From 00-vision.md AI philosophy] | [How this constrains the design] |
| [From 00-vision.md AI philosophy] | [How this constrains the design] |

### 6.2 Accessibility

WCAG 2.1 AA is required throughout.

| Requirement | Applies To |
|-------------|------------|
| 4.5:1 minimum contrast ratio | All text on all backgrounds, all CVs |
| 44x44 point minimum touch targets | Mobile views |
| Keyboard navigability | All desktop views |
| Focus indicators on all interactive elements | All views |
| Status indicators must not rely on color alone | All data display views |

### 6.3 Technology Constraints

- Stack: {{STACK}}.
- No concept should assume capabilities outside the documented scope (`10-scope-and-non-goals.md`).
- The design system is evolving. New components must be approved before use.

---

## 7. Evaluation Criteria

### 7.1 The Primary Standard

<!-- State the product owner's evaluation standard explicitly. Be equally clear. -->

### 7.2 Evaluation Dimensions

The product owner will evaluate concepts against the following dimensions:

| Dimension | What It Means |
|-----------|--------------|
| Aesthetic Delight | Does it produce a physical reaction? Would someone want to use this? |
| Vision Alignment | Does it reflect the product's AI philosophy and scope boundaries? |
| MLP Standard | Is this worthy of shipping? Does it meet the minimum lovable bar? |
| Practical Viability | Is the interaction model realistic for the use context? |
| Design System Spirit | Does it feel like it belongs in the product family? |

### 7.3 CDO Pre-Screening Criteria

Before presenting concepts to the product owner, the CDO screens against:

| Criterion | Pass | Fail |
|-----------|------|------|
| Anti-example check | Would never appear in a generic SaaS tool | Looks like a standard enterprise dashboard |
| Vision compliance | AI outputs are offers, not conclusions | Auto-filled content presented as finished work |
| Distinctness | Genuinely different from the other four concepts | Variation of the same layout idea |
| WCAG 2.1 AA | Achievable with this visual direction | Requires contrast or interaction compromises |
| Design system basis | Built from established foundation | Entirely new design language with no shared roots |

### 7.4 Decision Outcomes

| Outcome | What It Means | Next Step |
|---------|--------------|-----------|
| Direction approved | One or more concepts provide a clear design direction | CDO proceeds to full prototype (Gate G5) |
| Direction narrowed | Product owner identifies what works and what does not | Design team refines and produces a second round |
| Re-brief required | The concepts miss the brief in a fundamental way | CDO and product owner align; new round begins |

---

## 8. Process and Approval Gates

### 8.1 Gate Map

```
[Gate G1: Ideation Package Complete]
      |
      v
[Gate G4: Design Challenge Approved]  <-- this document
      |
      v
[Gate G5: CV Prototype Set Approved]
      |
      v
[Gate G6: E2E Mapping Complete]
      |
      v
[Gate G8: Technical Plan Approved]
      |
      v
[Gate G9: Release Candidate Approved]
```

### 8.2 Gate G4 — Design Challenge Approved

G4 approval checklist:

- [ ] Product owner has reviewed and confirmed the critical view list
- [ ] Product owner has confirmed the creative direction is accurate
- [ ] Product owner has confirmed the evaluation criteria are understood
- [ ] Any adjustments are incorporated into this brief

**Gate G4 is the Stop-the-Line gate for design.** No concepts are produced until this brief is fully approved.

### 8.3 Milestone Sequence (No Time Estimates)

| Milestone | Deliverable | Owner | Approval Required |
|-----------|-------------|-------|-------------------|
| M1 | Design Challenge Brief approved | Product Owner | Product Owner |
| M2 | Critical view list confirmed | CDO | Product Owner |
| M3 | Concept production: 5 concepts per CV | Design team | CDO pre-screen |
| M4 | Concept competition review | Product Owner | Product Owner |
| M5 | Design direction converged | CDO documents direction | Product Owner |
| M6 | Full prototype: all views and scenarios | Design team | CDO |
| M7 | Prototype review and refinement | Product Owner | Product Owner |
| M8 | Prototype approved — MLP bar set | — | Product Owner |
| M9 | Demo branch created | CTO | — |
| M10 | Feature branch created, development begins | CTO | Product Owner (Stop-the-Line) |

### 8.4 Stop-the-Line Triggers

1. **Design to development transition** — no feature branch is created without Design Approval
2. **New components not in the design system** — product owner approves before CDO can proceed
3. **Scope change to critical views** — any addition or removal requires re-approval of the brief

---

## 9. Reference Documents

| Document | Purpose |
|----------|---------|
| `docs/00-overview/00-vision.md` | Product vision, AI philosophy, acceptance criteria |
| `docs/00-overview/10-scope-and-non-goals.md` | Scope boundaries; design guardrails |
| `docs/02-user-guides/20-service-design/40-moments-that-matter.md` | Moments That Matter; anchors for which views are critical |
| `docs/02-user-guides/20-service-design/30-jtbd.md` | Jobs-to-be-done across all user types |
| `docs/02-user-guides/20-service-design/20-journey-maps.md` | User journeys; emotional arc and pain points |
| `docs/03-developer-guides/30-requirements/10-user-stories.md` | User stories with inline acceptance criteria |
