---
last_updated: 2026-04-02
status: active
---

# Injection Testing — How to Validate Injections Rigorously

An injection is the proposed change that resolves the conflict in the Evaporating Cloud. But a good idea in a cloud is not the same as a workable solution in the real world. This guide explains how to test an injection rigorously using the Future Reality Tree before committing to implementation.

---

## What "Testing" an Injection Means

Testing an injection is a logical exercise, not an empirical one (at this stage). You are asking:

1. **Will this injection actually produce the intended effects?** (Causal validity)
2. **Will it resolve the original UDEs?** (Coverage)
3. **Will it create new problems?** (Negative branches)
4. **Is it implementable in the current context?** (Feasibility check)

The FRT is the tool for questions 1-3. Question 4 is addressed by the Prerequisite Tree.

---

## Test 1: Causal Validity

For each injection, trace the logical chain from the injection to each claimed desirable effect.

### The if-then test

Write the full logical chain:

> "If [injection] then [intermediate effect 1] because [mechanism]."
> "If [intermediate effect 1] then [intermediate effect 2] because [mechanism]."
> "If [intermediate effect 2] then [desirable effect] because [mechanism]."

Read each link aloud. Ask: "Is this actually how things work in our specific system?" If any link requires a stretch of logic, or if you find yourself saying "well, hopefully..." — the chain is broken.

### Sufficiency test

Is the injection sufficient, by itself, to produce the effect? Or does the injection only work if combined with other conditions that are not yet in place?

If the injection requires AND-conditions (other things that must also be true), identify them explicitly. Are those conditions already present, or do they also need to be injected?

### Time delay test

Some cause-effect chains have significant time delays. An injection today may not produce the desirable effect for 6-12 months. If UDEs need to be resolved sooner, the injection may be valid but insufficient in isolation — a bridge solution may be needed.

---

## Test 2: UDE Coverage

For each original UDE from the CRT, trace whether a complete, unbroken logical chain connects the injection to the elimination of that UDE.

### Coverage map

Create a simple matrix:

| UDE | Injection | Chain valid? | DE that resolves it |
|-----|-----------|-------------|---------------------|
| U1 | I1 | Yes | DE3 |
| U2 | I1, I2 | Yes | DE5 |
| U3 | (none) | No | — |

Any UDE with no valid coverage chain means the injection set is incomplete. Before declaring the FRT done, every UDE must have a valid, traceable resolution.

### Partial resolution

Sometimes an injection reduces the severity of a UDE without fully eliminating it. This is acceptable as a transitional state, but it must be acknowledged explicitly — not treated as full resolution.

### Coverage threshold

A coverage rate below 80% typically means the injection set addresses only symptoms, not the root cause. Return to the EC and examine whether the assumptions underlying additional UDEs have been addressed.

---

## Test 3: Negative Branch Detection

For every injection, systematically ask:

**"What else could this cause?"**

Go through each stakeholder group and ask from their perspective:
- Does this injection reduce their resources, authority, or options?
- Does it create new work or responsibilities for them without corresponding support?
- Does it change their incentives in a way that creates perverse behavior?
- Does it require capabilities they currently lack?

### The four categories of negative branches

**Capacity negative branches:** The injection creates new demand that the system cannot handle. "We launch a 30-day onboarding program, but the customer success team is already at capacity — they cannot deliver it."

**Behavioral negative branches:** The injection changes incentives in an unintended way. "Measuring onboarding milestones creates pressure to mark milestones complete even when they aren't."

**Resource competition:** The injection competes with existing priorities for the same people, tools, or budget. "The engineering investment required for the injection delays existing product commitments, increasing technical debt."

**Market or customer reaction:** Customers or market actors respond to the injection in an unexpected way. "Introducing structured onboarding is perceived by customers as complexity, increasing time-to-value perception."

### Scoring negative branches

Use `negative_branch.py` to score each by `likelihood × severity` (max 25):

| Score | Risk Level | Action |
|-------|-----------|--------|
| 15–25 | High | Trimming injection required before implementation |
| 6–14 | Medium | Design a monitoring and contingency plan |
| 1–5 | Low | Note and monitor |

---

## Test 4: Trimming Injections

A trimming injection is a specific additional action that prevents a negative branch while preserving the positive effect.

### Properties of a good trimming injection

- **Specific:** Describes exactly what will be done, not just "monitor and respond"
- **Upstream:** Acts on the cause of the negative branch, not its symptom
- **Compatible:** Does not undermine the original injection's effectiveness
- **Proportionate:** The cost of the trimming injection is justified by the risk it prevents

### Example

**Original injection:** "Implement a structured 30-day onboarding program"

**Negative branch:** "Customer success team is overwhelmed, leading to reduced quality on existing accounts"

**Trimming injection:** "Before launching structured onboarding, automate three recurring support tasks (password resets, basic configuration, integration setup) to free 20% of CS team capacity. Hire one additional CSM ahead of launch."

The trimming injection removes the capacity constraint before it becomes a problem, without reducing the scope of the onboarding program.

---

## When an Injection Fails the Tests

### It fails the causal validity test

Restate the injection more concretely. Vague injections often fail this test. If the chain still doesn't hold, the injection may be addressing a symptom rather than the root cause — return to the EC and reconsider.

### It fails the coverage test

The injection set needs additional members. Run the EC again for the uncovered UDEs — is there an additional conflict that hasn't been surfaced?

### It has high-risk negative branches that cannot be trimmed

Sometimes the negative branches of an injection are too severe to mitigate practically. In this case, the injection needs to be redesigned, scoped down, or replaced with an alternative that achieves the same need without the same consequences.

Never proceed with an untrimmed high-risk negative branch. The FRT's purpose is to find these problems before they cost real resources.

---

## The Validated Injection

An injection is validated when:
- [ ] Complete causal chains connect it to all claimed desirable effects
- [ ] All original UDEs have a traceable resolution
- [ ] All high-risk negative branches have trimming injections
- [ ] AND-conditions are identified and either already in place or included in the injection set
- [ ] Time delays are acknowledged and a sequencing plan exists

A validated injection set is the input to the **Prerequisite Tree** — the tool for planning implementation.
