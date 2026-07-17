---
last_updated: 2026-04-02
status: active
---

# Common CLR Violations in Business Reasoning

These are the failure patterns seen most frequently in business plans, strategy documents, OKRs, retrospective analyses, and TOC thinking process trees. Each pattern has a name, the CLR it violates, an example, and the fix.

---

## Pattern 1: "We Did X, Therefore Y Happened"

**CLR violated:** CLR 3 (Causality Existence)

**What it looks like:**
> "We launched the redesign in Q2, and revenue grew 20% in Q3. The redesign drove the growth."

Two events happened in sequence. The writer assumes the first caused the second. No mechanism is stated. No confounds are considered.

**Why it happens:** Post-hoc rationalization is cognitively easy. Humans are pattern-matching machines and will find causation in coincidence, especially when one event was deliberate and the outcome was desirable.

**The fix:** State the mechanism. "The redesign caused revenue growth because [specific mechanism: better conversion on landing page, clearer pricing page, reduced churn from onboarding improvement]. We can verify this through [metric]."

If no mechanism can be articulated, the connection is correlation, not causation.

---

## Pattern 2: The Single Lever Fallacy

**CLR violated:** CLR 4 (Cause Insufficiency)

**What it looks like:**
> "If we hire two more engineers, our velocity will double."
> "If we improve our NPS, churn will drop."
> "If we raise prices, margins will improve."

Each of these may be a contributing cause — but each states a single lever as sufficient for a complex outcome.

**Why it happens:** Simplification is necessary for communication. But simplification in a strategic argument (where decisions will be made based on the logic) creates incorrect predictions and failed initiatives.

**The fix:** For each strategic claim, ask: "Is this cause alone sufficient? What else must also be true?" The answer reveals the AND-connector — the set of co-causes that must all be present.

Hiring two more engineers only doubles velocity IF: the current constraint is engineering capacity (not QA, not requirements, not deployment), the new engineers ramp quickly, and the work is structured to distribute across more people.

---

## Pattern 3: The Topic Entity

**CLR violated:** CLR 1 (Clarity)

**What it looks like:**
> Cause: "Culture"
> Effect: "Performance"

> Cause: "Technical debt"
> Effect: "Slow delivery"

> Cause: "Alignment"
> Effect: "Better outcomes"

**Why it happens:** Abstract nouns feel weighty and important. They also avoid the discomfort of specificity — once you state a specific cause, it can be challenged. "Culture" cannot be challenged; "managers reward individual heroics rather than team outcomes" can be.

**The fix:** Replace every noun entity with a complete declarative sentence describing a specific condition:
- "Culture" → "Managers publicly reward individual heroics rather than team-level outcomes"
- "Technical debt" → "Adding a new feature to the payments module requires touching 15 files with no tests"
- "Alignment" → "Product, Engineering, and Sales agree on which customer segment is the priority for Q3"

---

## Pattern 4: Symptom as Root Cause

**CLR violated:** CLR 6 (Cause-Effect Reversal) or CLR 3 (Causality Existence)

**What it looks like:**
> "Our team is burning out because they are working too many hours."
> "Churn is high because customers are not satisfied."
> "We are missing deadlines because we have poor estimation."

Each of these states a symptom as the cause of itself. Working too many hours is a symptom of burnout. Customer dissatisfaction is the definition of churn. Missing deadlines is (arguably) the definition of poor estimation.

**Why it happens:** The most visible signal becomes the explanation. The actual causal chain — what produces the symptom — is not explored.

**The fix:** Apply the "5 Whys" pattern. "Why are they working too many hours?" leads to the actual cause. The answer might be: "Managers approve more work than the team has capacity for" — a policy constraint that produces both the overwork and the burnout.

---

## Pattern 5: The Invisible AND-Connector

**CLR violated:** CLR 4 (Cause Insufficiency)

**What it looks like:**
A CRT or FRT diagram with a single arrow from one entity to a complex outcome, where multiple conditions are obviously required but only one is shown.

This is CLR 4 in visual form. The diagram implies sufficiency where multiple co-causes are needed.

**Why it happens:** Drawing one arrow is simpler than drawing three with an AND-connector. Builders of TOC trees often know the co-causes exist but do not make them explicit — leaving a gap in the logic.

**The fix:** Anytime an effect is complex or high-stakes, ask explicitly: "Could this effect fail to occur even if this cause were present?" If yes, add the missing co-causes and draw the AND-connector ellipse.

The AND-connector ellipse is not optional decoration — it is a factual claim about necessity. Omitting it claims sufficiency. Including it claims necessity.

---

## Pattern 6: The Predicted Effect That Isn't There

**CLR violated:** CLR 7 (Predicted Effect Existence)

**What it looks like:**
> "Our planning process is causing delivery delays."

If this connection is valid, we should observe:
- Items spend significant time in planning before development begins
- Planning meetings are frequent and long relative to delivery time
- Developers frequently wait for planning outputs before starting

If none of these secondary effects are observable, the "planning process" explanation needs re-examination.

**Why it happens:** Causal claims are often made without testability in mind. The focus is on naming a cause, not on verifying the theory.

**The fix:** For every causal claim in a strategy document or retrospective, list two secondary effects that should be observable if the connection is valid. If the secondary effects are not present, the connection is suspect.

---

## Pattern 7: The Circular Business Case

**CLR violated:** CLR 8 (Tautology)

**What it looks like:**
> "We should invest in marketing because we need more customers."
> "We should improve quality because we have too many defects."
> "We should hire because we do not have enough capacity."

The "because" clause restates the problem — it does not explain the causal mechanism or establish that the proposed action will produce the desired effect.

**Why it happens:** Business proposals often establish the problem (not enough customers, too many defects, not enough capacity) and then propose the obvious solution without articulating the mechanism that links the investment to the outcome.

**The fix:** Replace "we should do X because we have problem Y" with "we should do X because X causes mechanism Z, which reduces Y, and we can verify this by measuring W."

---

## Pattern 8: The Reinforcing Loop Stated as One-Directional

**CLR violated:** CLR 6 (Cause-Effect Reversal) — incomplete version

**What it looks like:**
> "Low team morale causes low productivity."

This is often stated as a one-directional cause, when the actual system is a reinforcing loop:
- Low morale → low productivity → missed commitments → blame → lower morale

**Why it matters:** A one-directional framing suggests a single intervention ("fix morale"). A reinforcing loop requires a different strategy — breaking the loop at the most accessible point, or addressing the external trigger that started the loop.

**The fix:** When a cause-effect connection seems one-directional, ask: "Does the effect feed back into the cause?" If yes, draw the loop explicitly. A CRT with a reinforcing loop is not wrong — it is more accurate than one without.

---

## Pattern 9: The Assumption Stated as Fact

**CLR violated:** CLR 2 (Entity Existence)

**What it looks like:**
> "Our customers are price-sensitive."
> "The market is moving toward enterprise."
> "Our competitors will respond by cutting prices."

These may be plausible assumptions, but they are stated as facts in CRTs and FRTs without verification.

**Why it happens:** Teams build trees based on their mental models of the market. Those models may be untested or outdated.

**The fix:** Distinguish between verified entities and assumed entities. Mark assumptions explicitly. A CRT with a verified cause produces reliable insights. A CRT built on assumed causes produces an elaborate logic structure on a weak foundation.

---

## Pattern 10: "Everyone Knows" Causation

**CLR violated:** CLR 3 (Causality Existence)

**What it looks like:**
> "Obviously, technical debt slows us down."
> "Everyone knows that distributed teams communicate less effectively."
> "It's well-established that estimation is unreliable."

The mechanism is omitted because it is assumed to be common knowledge. This prevents the connection from being challenged even when it should be.

**Why it happens:** Common-knowledge claims bypass the discomfort of stating and defending a mechanism. They also bypass the discipline of verifying that the "obvious" connection actually holds in this specific system.

**The fix:** State the mechanism even for "obvious" connections. "Technical debt slows us down because adding a feature to the payments module requires touching 15 files, each requiring coordination and increasing the chance of regressions." This version can be challenged, tested, and verified — or refuted.
