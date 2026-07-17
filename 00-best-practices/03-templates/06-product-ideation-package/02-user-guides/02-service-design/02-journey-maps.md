---
last_updated: 2026-06-28
status: active
---

# User Journeys

<!--
FACILITATION GUIDE — Service Designer
======================================
This document maps the end-to-end experience. We're designing for
humans, not screens. The Service Designer has VETO POWER over any
decision that harms user experience.

PREREQUISITE: 00-vision.md, JTBD, and at least one interview must
be completed.

CONVERSATION FLOW:
1. Identify who the users are (personas)
2. Map each persona's journey with emotional state, pain, and solve per stage
3. Find the struggling moments (where friction lives)
4. Map the emotional arc (how they feel at each stage)
5. Define touchpoints (every point of interaction)
6. Map intelligence handoffs (what flows between systems/stages)
7. Capture critical design requirements

QUESTIONS TO ASK:

## Round 1: Personas
- "Who are the different types of people who would use this?"
- "For each type: What's their context? What do they already know?
  What are they feeling when they arrive?"
- "Which persona is the PRIMARY user we design for first?"
- "Consider: the primary operator, the reviewer/approver, the admin/configurator,
  and any secondary beneficiaries"

## Round 2: Primary Persona Journey
For the primary persona, walk through the full journey with this
structure for each stage:

- What happens at this stage?
- Emotional state: How are they feeling? (one word + "I am..." quote)
- Pain (today): What goes wrong without this product?
- Solve: What does {{PRODUCT_NAME}} do at this stage?

Ask:
- "How do they first discover or encounter this product?"
- "What's their first interaction? What do they see, do, feel?"
- "Walk me through a typical session — from opening the product
  to finishing their work."
- "When do they have their 'aha' moment?"
- "What brings them back? What does ongoing use look like?"

## Round 3: Secondary Persona Journeys
For each additional persona:
- "Walk me through [persona]'s journey — from first contact with
  the product to getting their job done."
- Keep secondary journeys high-level (stage names + what they need
  at each stage), not full narrative.
- "What do they share with the primary persona's journey?
  Where do their needs diverge?"

## Round 4: Struggling Moments
- "Where in this journey would someone get confused?"
- "Where would they feel frustrated or stuck?"
- "Where might they give up and leave?"
- "What's the hardest thing they have to do?"
- "What information do they need that they don't have at each step?"
- "Where could the AI get in the way instead of helping?"

## Round 5: Emotional Arc
For each stage of the journey, ask:
- "How is the user feeling here? Overwhelmed? Hopeful? Skeptical?"
- "What would make them feel confident at this moment?"
- "What could go wrong emotionally?"

## Round 6: Touchpoints
- "What are ALL the ways a user interacts with this product?"
- "Are there touchpoints outside the product? (Email notifications,
  calendar reminders, team collaboration)"
- "Which touchpoint has the most impact on their overall experience?"

## Round 7: Intelligence Handoffs
- "What data flows in from outside this product?"
- "What does this product hand off to other tools when a stage completes?"
- "What would break if the handoff failed?"

## Round 8: Critical Design Requirements
- "Looking across all personas and all stages, what are the must-have
  design requirements — the ones that, if missed, the product fails?"
- "For each requirement: Why is it required? What's the success metric?"

SYNTHESIS:
Build the journey for the primary persona as a stage-by-stage narrative
with emotional state, pain, and solve per stage.
Secondary personas can be abbreviated. End with a requirements table
derived from the journeys.
-->

## Personas
<!-- From Round 1 -->

## 1. [Primary Persona] Journey
<!-- From Round 2: Full stage-by-stage journey with emotional state,
     pain (today), and solve per stage -->

```
[Stage 1] → [Stage 2] → [Stage 3] → [Stage 4] → [Stage 5] → [Stage 6]
```

**Stage 1: [Name]**
- [What happens at this stage]
- Emotional state: **[Word]** — "[I am... quote]"
- Pain (today): [What goes wrong without this product]
- Solve: [What {{PRODUCT_NAME}} does at this stage]

**Stage 2: [Name]**
- [What happens at this stage]
- Emotional state: **[Word]** — "[I am... quote]"
- Pain (today): [What goes wrong without this product]
- Solve: [What {{PRODUCT_NAME}} does at this stage]

**Stage 3: [Name]**
- [What happens at this stage]
- Emotional state: **[Word]** — "[I am... quote]"
- Pain (today): [What goes wrong without this product]
- Solve: [What {{PRODUCT_NAME}} does at this stage]

**Stage 4: [Name]**
- [What happens at this stage]
- Emotional state: **[Word]** — "[I am... quote]"
- Pain (today): [What goes wrong without this product]
- Solve: [What {{PRODUCT_NAME}} does at this stage]

**Stage 5: [Name]**
- [What happens at this stage]
- Emotional state: **[Word]** — "[I am... quote]"
- Pain (today): [What goes wrong without this product]
- Solve: [What {{PRODUCT_NAME}} does at this stage]

---

## 2. [Secondary Persona] Journey
<!-- From Round 3: Abbreviated journey — stage names + what they need -->

```
[Stage 1] → [Stage 2] → [Stage 3] → [Stage 4]
```

- **[Stage 1]:** [What they need here]
- **[Stage 2]:** [What they need here]
- **[Stage 3]:** [What they need here]
- **[Stage 4]:** [What they need here]

---

## 3. [Secondary Persona] Journey

```
[Stage 1] → [Stage 2] → [Stage 3]
```

- **[Stage 1]:** [What they need here]
- **[Stage 2]:** [What they need here]
- **[Stage 3]:** [What they need here]

---

## Struggling Moments
<!-- From Round 4: Where friction, confusion, or abandonment lives -->
<!-- These are the PRIORITY design targets -->

| Moment | What Goes Wrong | What They Need | Severity |
|--------|----------------|----------------|----------|
| | | | |

## Emotional Arc
<!-- From Round 5: How the user feels at each journey stage -->

| Stage | Feeling | What Builds Confidence | What Could Go Wrong |
|-------|---------|----------------------|---------------------|
| | | | |

## Touchpoints
<!-- From Round 6: Every interaction point, ranked by impact -->

## Intelligence Handoffs (Ecosystem)
<!-- From Round 7: What flows in, what flows out, what breaks if the handoff fails -->

| Handoff | From → To | What Flows |
|---------|-----------|-----------|
| | | |

## Critical Design Requirements (Summary)
<!-- From Round 8: Must-have requirements derived from the journey -->

| Requirement | Why | Success Metric |
|-------------|-----|----------------|
| | | |

## Service Blueprint Layers
<!-- Filled in after journey is mapped -->

| Layer | Description |
|-------|-------------|
| **Customer Actions** | |
| **Frontstage** | |
| **Backstage** | |
| **Support Processes** | |

---

**Related:** [JTBD](03-jtbd.md) | [Moments That Matter](04-moments-that-matter.md)
