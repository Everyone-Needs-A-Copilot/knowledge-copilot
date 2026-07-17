---
last_updated: 2026-04-02
status: active
---

# The Eight Categories of Legitimate Reservation

The CLRs define the only valid ways to challenge a cause-effect connection. Every objection to causal logic falls into one of these eight categories, or it is not a logical objection.

---

## CLR 1: Clarity

**Definition:** Before assessing whether a connection is valid, both the cause and the effect must be stated as clear, specific, unambiguous declarative sentences.

**Test question:** "Do we agree on exactly what each statement means?"

**What "clear" requires:**
- Complete sentences stating a condition, not topics or nouns
- Specific enough that two people reading it independently would understand the same thing
- No vague qualifiers ("various," "some," "many")

**Correct example:**
> Cause: "The code review process requires approval from three engineers before merge."
> Effect: "Feature branches remain open for an average of 5 days before reaching main."

**Violation example:**
> Cause: "Process issues."
> Effect: "Delays."

These are topics, not entities. You cannot assess causation when neither side is defined.

**How to fix:** Restate each entity as a complete condition. Ask "What specifically is true? What condition exists?"

---

## CLR 2: Entity Existence

**Definition:** Both stated entities must actually exist. The cause must be a real current condition, and the effect must be real or a verifiable prediction.

**Test question:** "Is this condition actually real, or are we assuming it?"

**What existence requires:**
- In a Current Reality Tree: both cause and effect are present conditions that can be observed or verified
- In a Future Reality Tree: causes must exist; effects may be predicted but should be believable
- Not wishes, assumptions, or feared scenarios (unless the tree is specifically about hypotheticals)

**Correct example:**
> Cause: "We have one engineer who understands the payment module." [Verifiable]
> Effect: "Payment-related bugs take 3x longer to resolve than other areas." [Verifiable]

**Violation example:**
> Cause: "We might not have enough engineers in six months." [Assumed future]
> Effect: "Development velocity declines." [Double hypothetical]

**How to fix:** For each entity, ask "Can I verify this is true today?" If not, the connection belongs in a different analysis or needs qualification.

---

## CLR 3: Causality Existence

**Definition:** A causal mechanism must exist connecting the cause to the effect. Correlation and temporal sequence are not sufficient.

**Test question:** "If the cause exists, does the effect necessarily follow? What is the mechanism?"

**What causality requires:**
- An explainable mechanism — not just "A and B happened together" or "A happened before B"
- The mechanism must be stated in the rationale
- The connection must be logical, not just observed

**Correct example:**
> Cause: "Deployments take 4 hours."
> Effect: "Engineers batch their commits and push once per day."
> Rationale: "A 4-hour pipeline means feedback on a commit arrives hours later. Engineers adapt by accumulating changes to reduce the number of times they must wait for feedback."

**Violation — Correlation:**
> Cause: "We hired three engineers in Q3."
> Effect: "Delivery velocity improved in Q4."
> Rationale: "Both happened in the same year."
> [No mechanism — the engineers may have been irrelevant.]

**Violation — Temporal sequence:**
> Cause: "The CEO announced a new strategy."
> Effect: "Team morale improved."
> Rationale: "Morale improved after the announcement."
> [Sequence does not establish cause. Many other things changed simultaneously.]

**How to fix:** State the mechanism: "A causes B because [mechanism]. If A is true and nothing else changes, B will follow."

---

## CLR 4: Cause Insufficiency

**Definition:** The stated cause is real and related to the effect, but is not sufficient alone to produce it. Additional co-causes (connected by AND) are required.

**Test question:** "Is this cause, by itself, enough to produce this effect? Or must other conditions also be true?"

**What sufficiency requires:**
- If A alone is sufficient for B, use a single arrow: A → B
- If A AND C are both necessary for B, use an AND-connector (ellipse): A + C → B
- A single arrow without an AND-connector asserts sufficiency

**Correct example:**
> Cause: "Marketing budget increased by 50% AND conversion rate is above 3% AND sales team has capacity."
> Effect: "New customer acquisition doubles."
> [Multiple necessary conditions, all shown with AND-connector]

**Violation example:**
> Cause: "Marketing budget increased by 50%."
> Effect: "New customer acquisition doubles."
> [Asserts that budget alone doubles acquisition — ignores conversion, sales capacity, market size, competitive response]

**The AND-connector rule:** When drawing a thinking process tree, draw an ellipse touching all the arrows that feed a single effect. This means: ALL of these causes must be present for the effect to occur. Omitting the ellipse implies each cause alone is sufficient.

**Why this is the most common violation:** In business reasoning, we simplify by stating the most visible or most controllable cause. The other necessary conditions are assumed to be "already true" — until they are not.

**How to fix:** Ask "Would the effect occur if only this cause were present and everything else were normal?" If not, identify what else must be true.

---

## CLR 5: Additional Cause

**Definition:** An independent cause exists that can produce the same effect through a different path. The stated cause is not the only way to reach the effect.

**Test question:** "Could the effect occur even if the stated cause were absent?"

**What this requires:**
- The additional cause must be genuinely independent — not a co-cause for the same path
- If additional causes exist for an Undesirable Effect in a CRT, addressing only the stated cause will not eliminate the UDE

**Correct example:**
> Cause: "QA queue averages 14 items (CLR identifies this as causing delayed delivery)"
> Additional cause identified: "Unclear acceptance criteria cause items to be rejected and re-queued"
> [Even if QA capacity is increased, the rework loop will continue causing delays]

**Violation — Treating a contributing factor as the only cause:**
> Assuming that increasing QA headcount (addressing the physical constraint) will eliminate delivery delays when a separate rework loop is also causing them.

**Why it matters:** In a CRT, multiple root causes can independently produce the same UDE. Finding and fixing one root cause leaves the system producing the same problems through the other path.

**How to fix:** Draw multiple arrows into the effect if multiple independent causes can produce it. This is normal in a well-built CRT.

---

## CLR 6: Cause-Effect Reversal

**Definition:** The causal direction is backwards. What is stated as the cause is actually downstream of the effect.

**Test question:** "Does A cause B, or does B cause A?"

**What to look for:**
- Situations where the relationship runs in both directions (feedback loops)
- Cases where the more obvious or measurable phenomenon is stated as the cause when it is actually the effect
- Reinforcing loops where both statements are true — but the primary driver may be the less visible one

**Correct example:**
> Original claim: "Low morale → low productivity"
> Reversal check: Is it also true that "low productivity → low morale"?
> Finding: Both are true. There is a reinforcing feedback loop. The original claim is not wrong, but it is incomplete without acknowledging the loop.

**Violation example:**
> Claim: "High bug count causes slow development."
> Reversal: "Slow development causes high bug count" — because time pressure leads to skipping tests and reviews.
> [The actual driver may be development speed, not the other direction.]

**How to fix:** Draw feedback loops explicitly when both directions are true. Then ask: "Which direction is the primary driver?" That is the more important cause to address.

---

## CLR 7: Predicted Effect Existence

**Definition:** If the causal connection is valid, it should produce verifiable secondary effects. If those predicted effects are not observable, the connection is suspect.

**Test question:** "If this cause-effect connection is real, what else should we observe? Do we observe it?"

**What this requires:**
- A valid causal theory makes predictions beyond the single stated effect
- Those predictions should be testable against reality
- If key predicted effects are absent, the causal theory needs revision

**Correct example:**
> Connection: "Insufficient QA capacity → delayed feature delivery"
> Predicted secondary effects: "QA team works overtime / high QA queue / developers idle waiting for sign-off"
> Validation: All three are observable → the connection is likely valid.

**Violation — No predicted effects:**
> Connection: "Management style is causing low engagement."
> Predicted effects: None stated.
> [A connection that makes no testable predictions cannot be validated — and cannot be used to make decisions.]

**Violation — Predicted effects are absent:**
> Connection: "Understaffing causes delivery delays."
> Predicted effect: "Team members work excessive overtime."
> Finding: Team is working normal hours but delivery is still delayed.
> [The predicted effect is absent — the connection needs re-examination. The constraint may be elsewhere.]

**How to fix:** For each claimed cause-effect connection in a CRT or FRT, list two or three secondary effects that should be observable if the connection is valid. Verify at least one of them.

---

## CLR 8: Tautology

**Definition:** The cause and effect are the same condition restated. The effect is used as evidence for the cause, creating a circular argument.

**Test question:** "Is the evidence for the cause the effect itself? Are these two distinct conditions, or one condition stated twice?"

**What non-tautological reasoning requires:**
- Cause and effect must be distinct states
- The evidence for the causal connection must be external to the connection itself
- The mechanism must explain why A produces B, not just assert that they are the same thing

**Correct example:**
> Cause: "The support ticket resolution process requires three team members to sign off before closing."
> Effect: "Average ticket resolution time is 5 days."
> [These are distinct conditions. The policy causes the duration — different states, observable separately.]

**Violation — Direct restatement:**
> Cause: "Our throughput is low."
> Effect: "We are delivering slowly."
> [Low throughput and slow delivery are definitionally equivalent — this is a tautology.]

**Violation — Circular evidence:**
> Cause: "The team is disengaged."
> Evidence: "The team is producing low-quality work."
> Effect: "Low-quality work is being delivered."
> [If "disengaged" is inferred FROM "low-quality work," then the evidence for the cause IS the effect. Circular.]

**The diagnostic tell:** Can you explain why A causes B without using A's definition or B's definition as evidence? If not, it is likely a tautology.

**How to fix:** Define the cause and effect as independent, observable conditions. Find evidence for the cause that is distinct from the effect.
