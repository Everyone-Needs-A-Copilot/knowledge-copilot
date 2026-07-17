---
last_updated: 2026-04-02
status: active
name: cause-effect-analysis
description: Validate cause-effect logic using Goldratt's Categories of Legitimate Reservation (CLR). Use when reviewing any causal argument, validating thinking process trees (CRT, FRT, EC), or checking the logic of business plans and strategic decisions. This is the meta-skill that validates all other TOC Thinking Process outputs.
allowed-tools: Bash(python3:*) Read Write
---

# Cause-Effect Analysis (Categories of Legitimate Reservation)

The Thinking Processes in TOC — Current Reality Tree, Future Reality Tree, Evaporating Cloud, Prerequisite Tree, Transition Tree — all depend on valid cause-effect logic. A tree built on faulty connections produces incorrect conclusions no matter how rigorous the rest of the analysis is.

Goldratt developed the Categories of Legitimate Reservation (CLR) as a formal grammar for challenging causal claims. The CLRs define the only legitimate ways to object to a cause-effect connection. Any other objection is either a misunderstanding or an emotional response, not a logical challenge.

The CLRs serve two purposes: they discipline the person presenting an argument (forcing them to make claims that can be checked), and they discipline the reviewer (preventing them from rejecting valid logic because they dislike the conclusion).

---

## The Eight Categories of Legitimate Reservation

### CLR 1: Clarity

**Definition:** The entities (cause or effect) are stated ambiguously. Before assessing whether a connection is valid, both sides must be clear, specific, and unambiguous.

**Test question:** "Do we agree on exactly what this statement means?"

**Correct use:** An entity is a declarative statement describing a condition or event. "Sales are growing" is an entity. "Sales" is not — it is a topic, not a condition.

**Common violation:** Using nouns or concepts as entities instead of complete statements. "Morale" is not an entity. "Team morale is declining" is.

**Why it matters first:** All other CLRs are meaningless if the terms are unclear. Clarity is always the first check.

---

### CLR 2: Entity Existence

**Definition:** One or both entities do not actually exist — they are assumed, inferred, or untrue.

**Test question:** "Does this condition actually exist, or are we assuming it?"

**Correct use:** Each entity in a cause-effect connection should be verifiable. If the cause does not actually exist, the connection is irrelevant regardless of its logical form.

**Common violation:** Building trees on entities that represent desired states or feared futures, not current or past reality. A Current Reality Tree must reflect current reality.

**Note:** Entity Existence applies to both the cause and the effect. An effect that has not yet occurred may legitimately be the output of a Future Reality Tree — but the cause must exist.

---

### CLR 3: Causality Existence

**Definition:** The stated cause does not actually produce the stated effect. There is no causal mechanism connecting them.

**Test question:** "If the cause exists, does the effect necessarily follow?"

**Correct use:** A causal connection requires a mechanism — not just correlation, not just sequence in time. "It rained and then the meeting was productive" is not a causal connection unless rain affected meeting productivity.

**Common violation:** Confusing correlation with causation. Two things that occur together are not necessarily linked by causation.

**Second common violation:** Confusing temporal sequence with causation. A causes B does not mean that A happening before B is causation.

---

### CLR 4: Cause Insufficiency

**Definition:** The stated cause exists and is related to the effect, but is not sufficient on its own to produce the effect. Additional causes (co-causes) are required.

**Test question:** "Is this cause, by itself, enough to produce this effect — or does something else also need to be true?"

**Correct use:** TOC uses AND-connectors to show when multiple causes are all necessary for an effect. CLR 4 challenges whether the AND-connector is needed.

**Example:** "Increased marketing spend → more customers." Is marketing spend alone sufficient? Or does it also require: a converting landing page, a sales team to close, a product that retains customers?

**Common violation:** Presenting a single cause for a complex effect when multiple contributing factors are necessary. This makes the logic appear simpler and more controllable than it is.

**Note:** This is the most important CLR in business reasoning. Most causal claims in strategy documents fail CLR 4. Use `scripts/sufficiency_check.py` for a dedicated deep-dive on this reservation.

---

### CLR 5: Additional Cause

**Definition:** An independent cause exists that can produce the same effect without the stated cause. The stated cause is not the only path to the effect.

**Test question:** "Could the effect occur even if the stated cause were absent?"

**Correct use:** This CLR challenges whether eliminating the stated cause would actually eliminate the effect. If an additional independent cause exists, the effect will persist even after addressing the stated cause.

**Common violation:** Treating a contributing factor as the root cause when another independent cause can produce the same result. Removing the stated cause would have no effect on the outcome.

**Why it matters:** If you identify additional causes for an Undesirable Effect (UDE) in a CRT, you may need to address multiple root causes, not just the most visible one.

---

### CLR 6: Cause-Effect Reversal

**Definition:** The direction of causality is backwards. What is stated as the cause is actually the effect, and vice versa.

**Test question:** "Does A cause B, or does B cause A?"

**Correct use:** Cause-effect reversal catches logic that is inverted. This is particularly common in systems with feedback loops, where A and B both influence each other.

**Example:** "Low morale → low productivity" vs. "low productivity → low morale." Both may be true, which means there is a reinforcing loop — but the original claim that morale is the cause of productivity problems may be a reversal of the more primary dynamic.

**Common violation:** Assuming that the more observable phenomenon is the cause when it is actually downstream of a less visible driver.

---

### CLR 7: Predicted Effect Existence

**Definition:** If the causal connection is valid, there should be a predictable secondary effect that can be observed. If that secondary effect does not exist, the connection is likely invalid.

**Test question:** "If this cause-effect connection is real, what else should we observe? Do we observe it?"

**Correct use:** This CLR provides a testability check. Valid causal theories make predictions. If the predicted secondary effects are not present, the original connection is suspect.

**Example:** If "understaffing causes delayed delivery," we should also observe "understaffing causes team members working excessive hours." If the team is not working excessive hours, the understaffing-to-delay connection deserves re-examination.

**Common violation:** Asserting causal connections that are not testable. A connection that makes no predictions cannot be validated or refuted — which makes it useless for decision-making.

---

### CLR 8: Tautology

**Definition:** The cause and effect are the same statement rephrased. The effect is used to justify the cause in a circular argument.

**Test question:** "Is the evidence for the cause the effect itself?"

**Correct use:** A tautology contains no information. "We are delivering slowly because our throughput is low" is a tautology — slow delivery and low throughput are the same condition stated differently.

**Common violation:** Restating a symptom as a cause. "Customer satisfaction is low because customers are not happy" is a tautology. "Customer satisfaction is low because support tickets take 5 days to resolve" is a testable causal claim.

**The tell:** If you cannot explain the mechanism without using the same words or a direct synonym, it is likely a tautology.

---

## Scripts

### `scripts/clr_full_audit.py`

Run all structural CLR checks across a set of cause-effect connections.

```bash
python3 scripts/clr_full_audit.py --file input.json
```

Input: JSON with `connections[]` where each has:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., "C01") |
| `cause` | string | The cause entity (complete declarative statement) |
| `effect` | string | The effect entity (complete declarative statement) |
| `rationale` | string | Explanation of why cause produces effect |

Output: Quality score 0-100, per-connection CLR results, failures grouped by CLR type, most common failure type, and overall assessment.

**Use when:** Reviewing a complete thinking process tree (CRT, FRT, etc.) or validating a strategic argument with multiple linked claims.

### `scripts/sufficiency_check.py`

Deep-dive analysis on CLR 4 (Cause Insufficiency) for a single cause-effect pair.

```bash
python3 scripts/sufficiency_check.py --file input.json
```

Input: JSON with:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cause` | string | Yes | The stated cause |
| `effect` | string | Yes | The stated effect |
| `supporting_causes` | string[] | No | Additional causes the analyst believes contribute |

Output: Sufficiency verdict (sufficient/insufficient), list of potential missing co-causes if identifiable, AND-connector recommendation, and next steps.

**Use when:** A specific connection in a tree feels logically weak, or when a strategic claim rests on a single cause that seems oversimplified.

## References

- [Eight CLR Rules](references/eight-clr-rules.md) — Each CLR with definition, test question, and examples
- [Common Violations](references/common-violations.md) — Most frequent CLR violations in business reasoning
- [Connection Schema](assets/connection-schema.json) — JSON schema for script input format

## Key Principles

- **CLRs are the only legitimate objections.** Any objection to a causal claim falls into one of the eight categories or is not a logical objection.
- **Clarity first, always.** Never assess causality before ensuring both entities are unambiguously stated.
- **CLR 4 is the most important.** Cause insufficiency is the most common failure in business reasoning. Most strategic claims rest on a single cause that requires several co-causes to actually produce the effect.
- **CLRs discipline both parties.** The presenter must make checkable claims. The reviewer must check logic, not reject conclusions they dislike.
- **A tautology is not evidence.** If you are using the effect to prove the cause, you have proven nothing.

## When NOT to Use

- For empirical disputes (whether something is true, not whether the logic is valid) — CLRs check logic, not data quality
- As a substitute for data gathering — a logically valid connection built on false premises is still wrong
- In the middle of a brainstorm — CLRs are for validating conclusions, not suppressing hypotheses
