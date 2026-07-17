---
last_updated: 2026-04-02
status: active
name: current-reality-tree
description: Map undesirable effects to root causes using cause-effect logic. Use when diagnosing systemic problems, finding root causes behind multiple symptoms, or answering "what to change?" Triggers on root cause analysis, problem diagnosis, systemic issues, and why-analysis.
allowed-tools: Bash(python3:*) Read Write
---

# Current Reality Tree (CRT)

The Current Reality Tree is the first of Goldratt's Thinking Process tools. It answers the question **"What to change?"** by mapping observable symptoms (Undesirable Effects) back through chains of cause and effect until one or a few root causes emerge. Rather than treating each symptom independently, the CRT reveals the single leverage point whose elimination makes most symptoms disappear.

---

## Core Concepts

### Undesirable Effect (UDE)

A UDE is a symptom — something observable, real, and undesirable from the perspective of the system's goal. UDEs are **effects**, not causes. They describe what is wrong, not why it is wrong.

Good UDE: "Customers frequently complain about late deliveries."
Bad UDE (actually a cause): "We don't have enough inventory."

### Cause-Effect Connection

CRT logic uses "If ... then ..." statements to connect nodes:

> "If [A] exists, then [B] exists (because [rationale])."

Every arrow must pass the scrutiny test: is the cause sufficient to produce the effect, given the current context?

### AND-Connector

Sometimes two conditions must both be present for an effect to occur. These are marked with AND-connectors (an ellipse touching both incoming arrows). The effect only exists when both causes are true simultaneously.

### Root Cause

A node with no incoming connections is a root cause — something that exists independently. When the CRT is valid, most UDEs trace back to one or very few root causes. This is the core insight: the system's problems are not random; they share a common source.

### Convergence Ratio

`convergence_ratio = total_UDEs / total_root_causes`

A high ratio (e.g., 8 UDEs / 2 root causes = 4.0) indicates the tree has good explanatory power: a small number of causes explain many symptoms. A ratio below 2.0 suggests the tree may have too many disconnected branches or the root causes haven't been sufficiently surfaced.

---

## Building a CRT: Step-by-Step

### Step 1 — List UDEs

Collect every significant undesirable effect in the system. Aim for 5–10. Each must be:
- Observable (someone can point to evidence)
- Real (it actually occurs, not hypothetical)
- Undesirable from the system's goal perspective
- An **effect**, not a cause in disguise

Write each as a declarative statement in the present tense:
"Sales conversion rate is below target."
"Employee turnover in the support team is high."
"Product defect rate exceeds 5%."

### Step 2 — Identify First-Level Causes

For each UDE, ask: "What directly causes this?" Look for conditions in the current system — policies, behaviors, resource limitations, structural factors. Write them as new nodes.

### Step 3 — Connect with If-Then Logic

For each connection, write out the full logical statement before drawing the arrow:
> "If [cause] then [effect] because [rationale]."

Test each connection for sufficiency: given the cause, does the effect inevitably follow in your specific context? If not, the connection is invalid — find the missing intermediate step.

### Step 4 — Continue Surfacing Causes

For every new node that appears to be a cause, ask "what causes this?" Keep going until you reach nodes that have no plausible cause within the system's control — these are candidate root causes.

### Step 5 — Identify Convergence

Look for causes that feed into multiple branches. When a single node has multiple arrows pointing away from it (to different effects), this is a convergence point. When that node itself has no incoming arrows, it is a root cause.

### Step 6 — Validate the Tree

- Read each connection aloud as an "If-then" statement. Does it make logical sense?
- Check for circular reasoning: A causes B causes A is invalid.
- Verify all UDEs are reachable from at least one root cause.
- Check that AND-connectors are genuinely necessary (both conditions must be true).

### Step 7 — Identify the Core Problem

Usually one root cause (or cluster of tightly related root causes) explains the majority of UDEs. This is the "core problem" — the target for the Evaporating Cloud.

---

## Logical Validity Checks (CLR — Cause-Legitimacy Rules)

Each connection should pass these checks:

| Check | Question |
|-------|----------|
| Clarity | Is the cause and effect each stated precisely? |
| Completeness | Is a rationale provided explaining the mechanism? |
| Non-tautology | Is the cause actually different from the effect? |
| Sufficiency | Does the cause alone produce the effect, or are AND-conditions missing? |
| Entity existence | Does each node actually exist in the current reality? |

---

## Scripts

### `crt_builder.py`

Validates the tree structure, detects cycles, identifies root causes, and calculates convergence ratio.

Input format:
```json
{
  "udes": [
    { "id": "U1", "description": "..." }
  ],
  "connections": [
    {
      "from_id": "N1",
      "to_id": "U1",
      "type": "causes",
      "rationale": "..."
    }
  ]
}
```

Connection `type` values:
- `"causes"` — standard single-cause connection
- `"and_causes"` — this arrow is part of an AND-connector group

Output: root causes, convergence ratio, cycle detection, coverage warnings.

### `clr_validator.py`

Runs structural CLR checks on each connection. Input uses the same tree format. Output: per-connection pass/fail with quality score.

---

## Common Mistakes

**Mixing causes and effects.** If you write "We lack a clear process" as a UDE, you have described an absence, which is actually a cause. Reframe: "Orders are processed incorrectly" is the UDE; the absence of a process is a cause.

**Jumping levels.** "Management culture is poor" jumps too many levels. Trace intermediate steps: what specific management behavior, what policy, what decision causes the observable UDE?

**Circular trees.** If A causes B and B causes A, neither is a root cause. One of the connections is invalid — examine the rationale for each.

**Too few UDEs.** Fewer than 5 UDEs typically means the analysis is incomplete. Gather more symptoms before building.

**Stopping too early.** If every branch ends at "we don't have enough resources" without asking why resources are constrained, the root cause is still buried.

---

## Relationship to Other Thinking Process Tools

| Tool | Purpose | Follows CRT? |
|------|---------|--------------|
| Evaporating Cloud (EC) | Resolve the conflict underlying the core problem | Yes — takes the core problem as input |
| Future Reality Tree (FRT) | Validate that the proposed solution will work | Yes — takes EC injections as input |
| Prerequisite Tree (PRT) | Plan how to implement the solution | Yes — follows FRT |
| Transition Tree (TT) | Execute the implementation step-by-step | Yes — follows PRT |

The CRT is the diagnostic foundation. Do not skip it — without knowing the core problem, solutions are guesses.

---

## References

- `references/building-a-crt.md` — Full walkthrough with business example
- `references/ude-identification.md` — How to identify genuine UDEs
- `assets/crt-schema.json` — JSON schema for script input
