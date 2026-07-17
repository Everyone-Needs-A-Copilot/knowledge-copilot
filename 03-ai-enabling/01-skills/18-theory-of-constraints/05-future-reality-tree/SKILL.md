---
last_updated: 2026-04-02
status: active
name: future-reality-tree
description: Validate proposed solutions before implementation by mapping expected effects and detecting negative branches. Use when testing whether a proposed change will actually solve the problem, or when checking for unintended consequences. Triggers on solution validation, impact analysis, change management planning, and risk assessment.
allowed-tools: Bash(python3:*) Read Write
---

# Future Reality Tree (FRT)

The Future Reality Tree answers the question **"Will the change actually work?"** It takes the injections produced by the Evaporating Cloud, maps the cause-effect chains they set in motion, and verifies that the original Undesirable Effects will actually be resolved. It also forces explicit detection of **negative branches** — unintended consequences that the injection might create.

Without an FRT, a proposed solution is a hypothesis. With an FRT, it is a validated causal argument.

---

## Core Concepts

### Injection

An injection is a specific change introduced into the system. It is the output of the Evaporating Cloud — a new policy, action, resource, or capability that invalidates a key assumption and resolves the conflict.

A good injection:
- Is specific and actionable (not "improve communication" — what exactly?)
- Is under the system's control to implement
- Directly addresses one or more assumptions from the cloud
- Does not itself depend on other changes that haven't been planned

### Desirable Effect

A Desirable Effect (DE) is an improvement we expect the injection to produce. DEs are the positive counterparts of UDEs — specific, observable conditions that will exist after the injection is in place.

Each DE should be:
- Stated in the present tense ("Customers achieve onboarding milestones within 30 days")
- Observable and verifiable
- A direct or traceable effect of one or more injections

### UDE Coverage

The primary test of the FRT: does this set of injections resolve the original UDEs from the CRT? Coverage is calculated as the percentage of original UDEs that are addressed by at least one chain of effects leading from the injections.

Unresolved UDEs signal that the injection set is incomplete — additional injections are needed, or the causal chains are broken.

### Negative Branch

A negative branch is an unintended consequence — a chain of effects from the injection that leads to a new Undesirable Effect. The FRT forces you to find these **before implementation**, not after.

A negative branch is not a reason to abandon the injection. It is a reason to design a **trimming injection** — an additional action that prevents the negative effect while preserving the positive one.

---

## Building the FRT

### Step 1 — State the Injections Clearly

List each injection from the EC as a specific, implementable change. If the EC produced a conceptual insight, convert it into a concrete action.

Vague: "Focus on customer value"
Specific: "Implement a 30-day structured onboarding program with role-specific workflows and milestone tracking"

### Step 2 — Map the Positive Effects

For each injection, ask: "If this injection exists, what changes?" Build cause-effect chains forward from the injection toward the original UDEs.

Use the same if-then logic as the CRT:
"If [injection] then [intermediate effect] because [rationale]."
"If [intermediate effect] then [desirable effect] because [rationale]."

Continue until you reach conditions that directly eliminate the original UDEs.

### Step 3 — Verify UDE Coverage

For each UDE from the CRT, trace whether the FRT's chains of effects lead to its elimination. A UDE is "covered" when a desirable effect exists that directly contradicts it.

If a UDE remains uncovered, the injection set must be expanded.

### Step 4 — Search for Negative Branches

For each injection, ask: "What else could this change cause?" Consider:
- **Stakeholders who are disadvantaged** by the change
- **Second-order effects** — what does the intermediate effect cause beyond the intended path?
- **Resource and capacity effects** — does the injection create demand that the system cannot handle?
- **Behavioral responses** — how might people in the system react in ways that undermine the injection?

### Step 5 — Design Trimming Injections

For each negative branch, design a trimming injection: a specific additional action that prevents the negative effect without eliminating the positive one.

This is an AND-connector in the tree: the original injection AND the trimming injection together produce the desirable effect without the negative branch.

### Step 6 — Iterate

Add trimming injections to the injection list. Repeat the negative branch search for them. A complete FRT has no untrimmed negative branches with high risk scores.

---

## Connection to the CRT and EC

The FRT closes the Thinking Process loop:

```
CRT ──► [What to change?] ──► EC ──► [What to change to?] ──► FRT ──► [Will the change work?]
```

| Input | Output |
|-------|--------|
| CRT's UDEs | UDE coverage check — are they resolved? |
| EC's injections | Starting nodes of the FRT |
| EC's cloud structure | Guidance on which assumptions are being invalidated |

A high-quality FRT demonstrates:
1. Every injection connects to at least one desirable effect
2. Every original UDE is covered by at least one desirable effect
3. All negative branches with high likelihood × severity scores have trimming injections

---

## Validating the FRT

Use the same CLR checks as the CRT:

| Check | Question |
|-------|----------|
| Clarity | Is each cause and effect precisely stated? |
| Completeness | Is a rationale provided for each connection? |
| Non-tautology | Is the cause different from the effect? |
| Sufficiency | Does the cause alone produce the effect? |

Additionally:
- Every injection must connect to at least one desirable effect
- Every desirable effect must trace back to at least one injection
- No "orphaned" nodes (nodes not connected to anything)

---

## Scripts

### `frt_builder.py`

Validates FRT structure and calculates UDE coverage.

Input:
```json
{
  "injections": [
    { "id": "I1", "description": "..." }
  ],
  "original_udes": [
    { "id": "U1", "description": "..." }
  ],
  "desirable_effects": [
    { "id": "DE1", "description": "...", "resolves_ude": "U1" }
  ],
  "connections": [
    {
      "from_id": "I1",
      "to_id": "DE1",
      "rationale": "..."
    }
  ]
}
```

Output: coverage percentage, resolved/unresolved UDEs, disconnected injections.

### `negative_branch.py`

Scores and ranks negative branches. Suggests trimming.

Input:
```json
{
  "injection": "...",
  "stakeholders": ["..."],
  "potential_effects": [
    {
      "description": "...",
      "likelihood": 3,
      "severity": 4,
      "stakeholder": "..."
    }
  ]
}
```

Output: ranked negative branches by risk score (likelihood × severity), grouped by stakeholder, trimming suggestions.

---

## Common Mistakes

**Injections are too vague.** An injection of "improve communication" cannot be placed in a cause-effect tree. What specifically changes? How? For whom?

**No negative branch search.** Skipping negative branches is the most dangerous FRT error. Even good solutions have unintended consequences. Finding them early is the entire point.

**Declaring a UDE "resolved" prematurely.** A UDE is not resolved because the injection sounds like it would help. It is resolved when a complete, unbroken logical chain connects the injection to the elimination of the UDE.

**Not looping back for additional injections.** If several UDEs remain uncovered, do not proceed to implementation planning. Return to the EC to design additional injections.

---

## References

- `references/injection-testing.md` — How to test injections rigorously
- `references/negative-branch-protocol.md` — Systematic negative branch detection
