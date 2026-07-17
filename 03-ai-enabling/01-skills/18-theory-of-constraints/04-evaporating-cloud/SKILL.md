---
last_updated: 2026-04-02
status: active
name: evaporating-cloud
description: Resolve conflicts by surfacing and challenging hidden assumptions. Use when two positions seem irreconcilable, when there is a dilemma or trade-off, or when stakeholders disagree on direction. Triggers on conflict resolution, trade-off analysis, dilemma, and opposing requirements.
allowed-tools: Bash(python3:*) Read Write
---

# Evaporating Cloud (EC)

The Evaporating Cloud is Goldratt's tool for resolving conflicts that appear to be dilemmas. It answers the question **"What to change to?"** by exposing the hidden assumptions that make a conflict seem irresolvable, then invalidating one or more of those assumptions to find a win-win solution.

The name comes from Goldratt's observation that conflicts "evaporate" when the assumptions supporting them are surfaced and challenged — what appeared to be a fundamental dilemma turns out to be an artifact of beliefs that can be changed.

---

## The Five-Box Structure

A cloud has exactly five elements:

```
        Need A ──────────────────► Want D
       /                                  \
A ───►                                     ◄──── CONFLICT
       \                                  /
        Need B ──────────────────► Want D'
```

| Box | Label | Question to identify it |
|-----|-------|------------------------|
| A | Objective | What shared goal do both sides ultimately want? |
| B | Need 1 | What condition must be satisfied to achieve A? |
| C | Need 2 | What condition must also be satisfied to achieve A? |
| D | Want 1 | What specific action/state satisfies Need B? |
| D' | Want 2 | What specific action/state satisfies Need C? |

**The conflict:** D and D' appear mutually exclusive. You cannot have both simultaneously under current conditions.

---

## Reading the Cloud

The cloud contains five logical arrows, each representing an if-then relationship:

| Arrow | Statement |
|-------|-----------|
| A → B | "In order to achieve [A], we must satisfy [B]" |
| A → C | "In order to achieve [A], we must satisfy [C]" |
| B → D | "In order to satisfy [B], we must have [D]" |
| C → D' | "In order to satisfy [C], we must have [D']" |
| D ↔ D' | "We cannot have both [D] and [D'] simultaneously" (the conflict) |

Every arrow is backed by one or more assumptions. The conflict persists only because those assumptions are unexamined.

---

## Building the Cloud

### Step 1 — Identify the Conflict (D ↔ D')

Start with the visible conflict: the two things that seem impossible to have simultaneously.

Example: "We must reduce prices to win deals" vs. "We must maintain margins to stay profitable."

D = Reduce prices
D' = Maintain current margins

### Step 2 — Find the Needs (B and C)

Ask: "Why is D necessary? What need does it serve?"
B = "We need to remain competitive in the market"

Ask: "Why is D' necessary? What need does it serve?"
C = "We need sufficient cash flow to fund operations"

### Step 3 — Find the Shared Objective (A)

Ask: "Why do both B and C matter? What are we ultimately trying to achieve?"
A = "Build a financially sustainable, growing business"

Both B and C are genuine — abandoning either would undermine the objective. That is what makes this a real dilemma, not a false one.

### Step 4 — Verify the Cloud Reads Logically

Test each arrow by reading it as a full sentence:
- "In order to build a financially sustainable, growing business, we must remain competitive." ✓
- "In order to build a financially sustainable, growing business, we must have sufficient cash flow." ✓
- "In order to remain competitive, we must reduce prices." ← This is where assumptions hide.
- "In order to have sufficient cash flow, we must maintain current margins." ← More assumptions here.

If any arrow does not read logically, the box is mis-stated. Refine the wording.

---

## Surfacing Assumptions

Every arrow is supported by **hidden assumptions** — beliefs, policies, market conditions, or physical constraints that make the connection seem necessary. The conflict exists because nobody has questioned these assumptions.

### Categories of Assumptions

| Type | Description | Vulnerability |
|------|-------------|---------------|
| Policy | A rule or procedure we follow | High — can be changed |
| Belief | A mental model or conviction | Medium-high — can be challenged with evidence |
| Market | An external market condition | Medium — can shift or be influenced |
| Physics | A physical/logical constraint | Low — genuinely hard to change |

Policies and beliefs are the most vulnerable because they are internally controlled. When you find a policy assumption, ask: "Who made this policy? Why? Is the original reason still valid?"

### How to Surface Assumptions per Arrow

For each arrow A→B, B→D, etc., ask:
1. "What would have to be true for this connection to hold?"
2. "What are we assuming about the world that makes this necessary?"
3. "Under what conditions would this arrow NOT hold?"

Write every assumption as a complete sentence. A good assumption statement is falsifiable: you can imagine evidence that would disprove it.

**Weak (unfalsifiable):** "It's just how things work."
**Strong (falsifiable):** "Our customers choose suppliers based primarily on list price."

---

## Finding the Injection

An **injection** is a new idea, action, or condition that invalidates a key assumption — making the conflict disappear.

The injection does not "compromise" between D and D'. It changes the underlying reality so that both D and D' can coexist, or reveals that the conflict was never real.

### The Injection Process

1. Rank assumptions by vulnerability (policy > belief > market > physics)
2. For the most vulnerable assumption: "If this assumption were false, what would be possible?"
3. Design an injection: a specific, actionable change that makes the assumption false
4. Verify: does the injection allow both needs (B and C) to be satisfied simultaneously?

### Example Injection

Arrow: B → D ("In order to remain competitive, we must reduce prices")

Assumption: "Our customers choose suppliers primarily based on list price."

Challenge: "What if customers choose based on total cost of ownership, not list price? What if the problem is that customers don't see the value that justifies our price?"

Injection: "Develop a value quantification tool that helps prospects calculate ROI, so they are evaluating total economic impact rather than upfront cost."

This injection makes D ("reduce prices") unnecessary — the need B ("remain competitive") is now satisfied through differentiated value demonstration instead.

---

## Validating the Cloud

A well-formed cloud satisfies these criteria:

1. **Objective is shared** — both sides genuinely want A; if they don't, there is no common ground and a different approach is needed
2. **Needs are genuine** — B and C are real prerequisites for A; if either is optional, the conflict is false
3. **Conflict is real** — D and D' genuinely cannot coexist under current conditions
4. **Arrows are logical** — each if-then reads without strain
5. **Assumptions are specific** — each assumption is stated as a falsifiable claim

---

## Scripts

### `cloud_builder.py`

Validates the five-box structure, checks completeness of assumptions per arrow, ranks assumptions by vulnerability, and identifies injection points.

Input:
```json
{
  "objective": "...",
  "need_a": "...",
  "need_b": "...",
  "want_a": "...",
  "want_b": "...",
  "assumptions": [
    {
      "arrow": "A-B",
      "statement": "...",
      "type": "policy"
    }
  ]
}
```

Arrow labels: `"A-B"`, `"A-C"`, `"B-D"`, `"C-D'"`, `"D-D'"`

### `assumption_analyzer.py`

Takes assumptions with evidence and examines them in depth. Ranks by vulnerability for invalidation. Identifies top injection candidates.

---

## Common Business Clouds

See `references/common-business-clouds.md` for pre-structured clouds on recurring business dilemmas.

---

## Relationship to Other TP Tools

The EC is the creative center of the Thinking Process:

| Direction | Tool | Purpose |
|-----------|------|---------|
| Input | CRT | The core problem identified in the CRT becomes the conflict to resolve |
| Output | FRT | The injection(s) from the EC become the starting points of the Future Reality Tree |

The EC answers "what to change to" — but it does not yet prove the change will work. That is the Future Reality Tree's job.

---

## References

- `references/five-box-structure.md` — Detailed notation and diagram conventions
- `references/common-business-clouds.md` — Pre-structured business conflict templates
- `assets/cloud-schema.json` — JSON schema for script input
