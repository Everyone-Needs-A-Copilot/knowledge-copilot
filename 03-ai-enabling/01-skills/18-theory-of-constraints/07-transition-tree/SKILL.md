---
last_updated: 2026-04-02
status: active
name: transition-tree
description: Create detailed action plans with cause-effect reasoning for each step. Use when converting a plan into executable steps where each action must be justified, or when implementing changes that require buy-in at each stage. Triggers on action planning, step-by-step implementation, change execution, and detailed project planning.
allowed-tools: Bash(python3:*) Read Write
---

# Transition Tree (TrT)

The Transition Tree converts a goal or Intermediate Objective into a detailed, logically connected action plan. Every step answers four questions: what is true now, what action do we take, what do we expect to become true as a result, and why do we believe the action will produce that effect.

The defining feature of a TrT is **chain continuity**: each step's `expected_effect` becomes the next step's `current_reality`. This means the plan is testable. If a step's expected effect doesn't materialize, the chain breaks — which is visible and diagnosable rather than invisible.

## When to Use TrT

| Situation | Why TrT Helps |
|-----------|--------------|
| Plan needs stakeholder buy-in at each stage | Rationale column makes the "why" explicit for every action |
| Previous implementations stalled or got stuck | Chain continuity reveals where the logic broke |
| Steps feel disconnected or arbitrary | Forcing each effect to become the next reality surfaces gaps |
| Team implements differently than planned | Rationale ensures shared understanding of the intent |
| "Why are we doing this?" questions arise | Every step documents its own justification |

## The Four-Column Structure

Each step in a TrT has exactly four fields:

| Column | Question | Rules |
|--------|----------|-------|
| `current_reality` | What is true right now, at the start of this step? | Must be a verifiable condition, not an activity. Should match the previous step's `expected_effect`. |
| `action` | What do we do? | Single, concrete action. Not a project — one step. |
| `expected_effect` | What will be true when this action is complete? | Must be verifiable. Becomes the next step's `current_reality`. |
| `rationale` | Why do we believe this action produces this effect? | Causal logic, evidence, or theory. The weakest column is the highest risk. |

## Building a TrT

### Step 1: Set the Starting Point

The first step's `current_reality` is the honest state of affairs today. Be precise. "We have no pricing page" is better than "our pricing is unclear" because it is verifiable.

### Step 2: Define Each Action

Each action must be:
- **Singular** — one thing, not a cluster of activities
- **Concrete** — specific enough that two different people would do the same thing
- **Bounded** — has a clear completion point

### Step 3: Predict the Expected Effect

Ask: "If I take this action and nothing else changes, what will be different?" Write that condition. It must be testable — you should be able to confirm or deny it after the action is complete.

### Step 4: Write the Rationale

The rationale is the most important column for risk management. It exposes your assumptions. When a step fails to produce its expected effect, the rationale tells you which assumption was wrong.

Weak rationale: "This will work because we've seen others do it."
Strong rationale: "Customers consistently cite pricing confusion as a purchase barrier (NPS comments, support tickets). A clear single-tier page removes the confusion and reduces the decision complexity."

### Step 5: Connect the Chain

Each step's `expected_effect` must plausibly describe the world that the next step's `action` will operate on. If the connection feels forced, there is a missing step between them.

## Anatomy of a TrT Step

```
Step N:
  current_reality:  [State of the world at the start of this step]
        action:     [The one thing we do]
  expected_effect:  [State of the world after this step]
       rationale:   [Why we believe the action produces the effect]
          ↓
Step N+1:
  current_reality:  [Same as step N's expected_effect — or close enough to be a valid continuation]
```

## Chain Continuity and Gap Detection

A chain is continuous when each `expected_effect` flows naturally into the next `current_reality`. Gaps appear when:

- The transition requires an unstated assumption ("and somehow X is also now true")
- The next step's reality describes something the previous effect didn't produce
- A step was skipped because it felt obvious

The `trt_builder.py` script flags gaps automatically using similarity scoring between `expected_effect` of step N and `current_reality` of step N+1. These flags are advisory — the human analyst must confirm whether a flagged gap is a real missing step or a benign phrasing difference.

## Scripts

### `scripts/trt_builder.py`

Validate a Transition Tree for chain continuity, rationale completeness, and logical structure.

```bash
python3 scripts/trt_builder.py --file input.json
python3 scripts/trt_builder.py '{"steps": [...]}'
```

Input: JSON with `steps[]` — each with `id`, `current_reality`, `action`, `expected_effect`, `rationale`.

Output:
- Validated chain with step-by-step analysis
- Gap analysis: which transitions have weak connections
- Completeness score (percentage of steps with strong rationale)
- Flagged steps needing attention
- Orphaned step detection (steps not connected to the chain)

See `references/four-column-structure.md` for detailed examples.

## Common Mistakes

**Making `current_reality` an activity.** "We are working on pricing" is not a verifiable condition. "We have no public pricing page" is.

**Making `expected_effect` describe an ongoing process.** "Customers will start to understand pricing better" is unmeasurable. "Conversion rate from pricing page to trial increases above baseline" is verifiable.

**Weak rationale for high-risk steps.** The steps where the rationale is thinnest are the steps most likely to fail. Treat thin rationale as a planning risk, not a writing problem.

**Skipping obvious steps.** Steps that "everyone knows" are the ones that cause surprise failures. If you can't write the expected_effect, the step isn't obvious — it's unexamined.

**Assuming effects compound automatically.** Each step's effect is contingent on the previous effect having been achieved. If step 3's effect didn't materialize, step 4's rationale may be invalid even if step 4 is executed correctly.

## Relationship to Other TOC Tools

The TrT is the most granular TOC planning tool. It is typically the last tool applied before execution begins.

| Tool | Granularity | Question |
|------|------------|----------|
| Future Reality Tree | Strategic | Will this change produce the desired effects? |
| Prerequisite Tree | Tactical | What obstacles must be overcome and in what order? |
| **Transition Tree** | **Operational** | **What exactly do we do, step by step, and why?** |

A common pattern: use the PRT to identify an Intermediate Objective and its phase, then use a TrT to plan the execution of that specific IO in detail.

## References

- [Four-Column Structure](references/four-column-structure.md) — Detailed explanation with business example (pricing change implementation)
