---
last_updated: 2026-04-02
status: active
---

# The Five-Box Structure of the Evaporating Cloud

## Overview

The Evaporating Cloud (EC) is a five-element diagram connected by five arrows. Each element and each arrow has a precise meaning. Understanding the structure is required before attempting to build a cloud.

---

## The Five Elements

```
                     ┌──────────┐
              ┌─────►│  Need B  ├──────────────────────►┌──────────┐
              │      └──────────┘                        │  Want D  │
              │                                          └────┬─────┘
┌─────────────┤                                              │
│ Objective A │                                         CONFLICT
└─────────────┤                                              │
              │                                          ┌───┴──────┐
              │      ┌──────────┐                        │  Want D' │
              └─────►│  Need C  ├──────────────────────►└──────────┘
                     └──────────┘
```

| Box | Symbol | Role |
|-----|--------|------|
| Objective | A | The shared goal both parties want to achieve |
| Need 1 | B | A condition that must be satisfied to achieve A |
| Need 2 | C | A different condition that must also be satisfied to achieve A |
| Want 1 | D | The specific action or state that satisfies Need B |
| Want 2 | D' | The specific action or state that satisfies Need C |

**The conflict** exists between D and D' — having one appears to prevent having the other.

---

## The Five Arrows

Each arrow represents a logical "In order to ... we must ..." relationship:

```
A ──A-B──► B         In order to achieve A, we must satisfy B
A ──A-C──► C         In order to achieve A, we must also satisfy C
B ──B-D──► D         In order to satisfy B, we must have D
C ──C-D'─► D'        In order to satisfy C, we must have D'
D ◄─────── D'        D and D' conflict — we cannot have both (shown as double-headed)
```

Each arrow carries hidden assumptions. The conflict is maintained by those assumptions, not by physical law.

---

## Reading the Cloud Aloud

A well-formed cloud reads fluently in this sequence:

1. "In order to [A], we must [B]"
2. "In order to [B], we must have [D]"
3. "However, in order to [A], we must also [C]"
4. "In order to [C], we must have [D']"
5. "But [D] prevents [D'] — and [D'] prevents [D]"

If any sentence sounds forced, the element is mis-stated. Refine until the logic flows naturally.

---

## Notation Conventions

### Box Phrasing

Boxes should be phrased as **conditions** or **states**, not actions:

Good (state): "We maintain sufficient operating cash flow"
Bad (action): "We cut costs"

The want boxes (D and D') may be phrased as policies, positions, or required conditions. They should describe what each side insists must happen.

### Arrow Phrasing

Arrows should be read as: "In order to have [effect], we must have [cause]."

The causal direction runs from left to right:
- A causes the need for B and C
- B causes the need for D
- C causes the need for D'

### The Conflict Arrow

The D ↔ D' relationship is the **conflict**. It should be stated explicitly:

"We cannot simultaneously [D] and [D'] because [reason]."

The reason is itself an assumption — one of the most important ones to examine.

---

## The Assumption Layer

Every arrow is backed by one or more assumptions. Write assumptions per arrow:

### Arrow A → B
What do we believe makes B necessary for A?

Example:
- "A customer who hasn't achieved their goal will not renew" (belief)
- "Our company policy requires 90% customer retention to hit revenue targets" (policy)

### Arrow A → C
What do we believe makes C necessary for A?

Example:
- "Sustainable growth requires positive unit economics" (physics/logic)
- "Our investors require positive EBITDA by next quarter" (policy)

### Arrow B → D
What makes D the *only* way to satisfy B? This is often where the most vulnerable assumptions hide.

Example:
- "Price is the primary driver of purchase decisions in our market" (market/belief)
- "Our sales team only knows how to compete on price" (policy)

### Arrow C → D'
What makes D' the *only* way to satisfy C? Same scrutiny applies.

Example:
- "Our cost structure requires current pricing to cover fixed costs" (policy)
- "We cannot reduce variable costs without reducing quality" (belief)

### Arrow D ↔ D' (the conflict itself)
What makes these two things mutually exclusive?

Example:
- "Lowering prices reduces revenue per unit, which reduces cash flow" (physics/math)
- "Our current cash flow model does not allow for price reduction" (policy)

Note: sometimes the D ↔ D' conflict itself rests on an assumption that can be invalidated. If the conflict disappears under different conditions, it was never truly irreconcilable.

---

## Common Errors in Cloud Construction

### Putting a cause in the need box

The need boxes (B, C) should describe **conditions**, not specific solutions.

Wrong: "We need to run a price promotion"
Right: "We need to accelerate customer acquisition this quarter"

### Objective is too abstract

An objective of "be successful" or "grow the business" is too vague. It won't help test whether B and C are both genuinely required.

Better: "Achieve 40% revenue growth while maintaining positive operating margin"

### D and D' aren't really in conflict

Sometimes what looks like a conflict is actually a sequencing problem ("we can do D now and D' later") or a scoping problem ("D applies to enterprise, D' applies to SMB"). If D and D' don't actually conflict in all contexts, you don't have a dilemma — you have a planning problem.

Test the conflict: "Can we literally have both D and D' simultaneously right now, given our current constraints?" If yes, the cloud isn't needed.

### Conflating the want with the need

The want (D) must be a *specific* requirement of the need (B). If D is just a restatement of B in different words, the B→D arrow carries no assumptions and the analysis will be shallow.

---

## Verification Checklist

Before proceeding to assumption surfacing, verify:

- [ ] All five boxes contain specific, non-trivial statements
- [ ] The objective (A) is something both parties genuinely share
- [ ] Both needs (B, C) are genuinely necessary for A — neither is optional
- [ ] D and D' cannot coexist simultaneously in current conditions
- [ ] Each arrow reads fluently as an if-then statement
- [ ] Boxes contain states/conditions, not actions or solutions
- [ ] D' is not just the negation of D (that would make the conflict trivially true)

---

## Visual Template (Text-Based)

```
OBJECTIVE (A)
└── "In order to achieve: [A]"

    NEED B (first requirement)
    └── "We must satisfy: [B]"
        WANT D (satisfies B)
        └── "By having: [D]"

    NEED C (second requirement)
    └── "We must also satisfy: [C]"
        WANT D' (satisfies C)
        └── "By having: [D']"

CONFLICT: [D] and [D'] cannot coexist because [assumption]
```

---

## See Also

- `references/common-business-clouds.md` — Pre-structured business conflict templates
- `scripts/cloud_builder.py` — Automated validation and assumption ranking
- `scripts/assumption_analyzer.py` — In-depth assumption vulnerability scoring
