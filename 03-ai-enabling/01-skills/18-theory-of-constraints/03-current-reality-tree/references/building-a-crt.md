---
last_updated: 2026-04-02
status: active
---

# Building a Current Reality Tree — Step-by-Step Guide

This guide walks through the complete process of constructing a CRT, using a B2B SaaS company as the running example. The company sells project management software and is struggling with growth stagnation.

---

## Phase 1: Gather Undesirable Effects

Before drawing anything, spend time in observation mode. Talk to stakeholders. Review metrics. Look for pain points that people complain about consistently.

**Ground rules for UDEs:**
- State in present tense ("X is happening" not "X might happen")
- Observable — someone can point to data or direct experience
- Undesirable from the system's goal (growing a profitable, sustainable business)
- An **effect**, not a cause or an absence

### Example UDE List

| ID | UDE |
|----|-----|
| U1 | Customer churn rate exceeds 8% per quarter |
| U2 | Sales cycle length has increased from 30 to 75 days |
| U3 | Support ticket volume grows faster than headcount |
| U4 | New feature adoption rate is below 20% |
| U5 | Engineering velocity has declined for three consecutive quarters |
| U6 | Prospects frequently request demo extensions before deciding |
| U7 | Customer satisfaction scores decline after the first 90 days |

**Tip:** Write UDEs on sticky notes or index cards so they can be physically rearranged as the tree develops.

---

## Phase 2: Find First-Level Causes

For each UDE, ask: "What in our current system directly causes this?" Do not jump to root causes yet — stay one level up from each UDE.

### Working with U1: Customer churn rate exceeds 8% per quarter

"What causes customers to churn?"

Possible direct causes:
- Customers are not achieving their desired outcomes with the product (C1)
- Customers find the product difficult to use (C2)
- Customers receive slow responses when they need help (C3)

Write each as a new node. Now ask: "If C1 exists, does U1 follow?" The answer should be clearly yes in our current context. If not, identify what's missing.

### Working with U2: Sales cycle length has increased

"What causes longer sales cycles?"

- Prospects cannot quickly understand the product's value (C4)
- Decision-makers require more internal approvals than before (C5)
- Sales reps spend excessive time on unqualified leads (C6)

---

## Phase 3: Build the If-Then Connections

For each connection, write the full logical statement before committing to an arrow:

**Connection: C1 → U1**
"If customers are not achieving their desired outcomes with the product, then customer churn rate will exceed 8% per quarter — because customers renew when they see value and cancel when they don't."

Read it aloud. Is it logical? Does it describe how things actually work in this company? If yes, draw the arrow.

**Connection: C3 → U1**
"If customers receive slow responses when they need help, then customer churn rate will exceed 8% per quarter — because unresolved problems frustrate customers to the point of cancellation."

This is also valid.

---

## Phase 4: Dig Deeper — Ask "What Causes This?"

Now apply the same question to each intermediate cause node.

### Digging into C1: Customers not achieving desired outcomes

"What causes customers to fail to achieve outcomes?"

- Onboarding does not teach customers how to apply the product to their specific workflow (C7)
- The product's configuration options are too complex for non-technical users (C8)

### Digging into C7: Onboarding doesn't teach workflow application

"What causes this?"

- Onboarding content is generic and not personalized by customer type (C9)
- Customer success team lacks capacity to deliver personalized onboarding (C10)

### Digging into C10: CS team lacks capacity

"What causes this?"

- CS headcount has not grown proportionally with customer base (C11)
- CS team spends 40% of time on reactive support rather than proactive success (C12)

### Digging into C12: CS time consumed by reactive support

"What causes this?"

- Product has recurring usability issues that generate repetitive support tickets (C13)

### Digging into C13: Recurring usability issues

"What causes this?"

- Product roadmap is driven by new feature requests, not by fixing existing friction points (C14)

### Digging into C14: Roadmap driven by new features over fixes

"What causes this?"

- Leadership believes new features are necessary to close new sales (C15)
- There is no systematic process for prioritizing customer-reported friction (C16)

At this point, C15 and C16 are beginning to look like root causes — they reflect **policies and beliefs** rather than downstream effects.

---

## Phase 5: Identify Convergence

Now look at which intermediate nodes appear in multiple causal chains.

**C11 (CS team under-resourced)** is reached from:
- U3 (support ticket volume grows faster than headcount) → C11
- U7 (satisfaction declines after 90 days) → C10 → C11

**C14 (roadmap driven by new features)** feeds:
- C13 → C12 → C10 → C1 → U1
- C5 (sales cycle: approval delays) → via C4 → U2
- U4 (low feature adoption) — because new features are added without usage design
- U5 (engineering velocity decline) — because technical debt from rushed features accumulates

**C15 (belief that new features close sales)** is a root cause feeding C14.

---

## Phase 6: Map the AND-Connectors

Some effects require two simultaneous conditions.

**U2 (sales cycle lengthened)** requires BOTH:
- C4 (prospects can't understand value) AND
- C5 (more internal approvals required)

Neither alone fully explains the increase. Draw an AND-connector: both arrows touch an ellipse before reaching U2.

---

## Phase 7: Identify Root Causes

Nodes with no incoming arrows and which have a wide reach across branches are root causes.

In our example:
- **C15**: "Leadership believes new features are necessary to close new sales" — a belief/policy with no upstream cause in the system
- **C16**: "No systematic process for prioritizing customer friction" — a structural absence

These two root causes, directly or indirectly, explain U1, U2, U3, U4, U5, U6, and U7.

**Convergence ratio: 7 UDEs / 2 root causes = 3.5** — strong explanatory power.

---

## Phase 8: Name the Core Problem

The core problem is the statement that unifies the root causes. In this case:

> "The company optimizes for acquiring new customers through new features rather than ensuring existing customers succeed, creating a growth ceiling driven by churn."

This becomes the input to the **Evaporating Cloud**: what conflict in our thinking keeps this policy in place?

---

## Phase 9: Validate the Complete Tree

Read every connection aloud as an if-then statement. Check for:

1. **Circular logic**: Does any path loop back to its own starting node?
2. **Unsupported leaps**: Is there a step where the cause is too remote from the effect?
3. **Missing AND-conditions**: Are there effects that only occur when multiple conditions are true?
4. **Completeness**: Does every UDE trace back to a root cause?

Use `crt_builder.py` to run automated structural checks.
Use `clr_validator.py` to validate each connection's logical soundness.

---

## Deliverable: Completed CRT

A completed CRT is a directed acyclic graph (when valid) where:
- All leaves (top nodes with no incoming arrows) are root causes
- All UDEs are reachable from at least one root cause
- Every connection is supported by a written rationale
- AND-connectors are explicitly marked
- The convergence ratio is 2.0 or higher

The completed CRT hands off cleanly to the **Evaporating Cloud** (Skill 04), which addresses the conflict keeping the core problem in place.
