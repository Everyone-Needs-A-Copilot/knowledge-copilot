---
last_updated: 2026-04-02
status: active
---

# Identifying Undesirable Effects (UDEs)

The quality of a Current Reality Tree depends entirely on the quality of its UDEs. Vague, mis-stated, or incomplete UDEs produce trees that diagnose the wrong problems. This guide explains how to identify genuine UDEs.

---

## What Makes a Valid UDE

A UDE must satisfy four criteria:

### 1. Observable

A UDE describes something that **actually exists** in the current system and that someone can point to with evidence.

Good: "Sales win rate has fallen from 35% to 18% over the past two quarters."
Bad: "We might lose customers if we don't improve."

Observable means: if you asked two different people to verify it independently, they would reach the same conclusion.

### 2. Real (Not Hypothetical)

A UDE is something happening **now** in the present reality, not a future risk or a past event.

Good: "Engineering releases miss their committed sprint deliverables in 7 of the last 10 sprints."
Bad: "We could miss deadlines if we don't hire more engineers."

If the statement requires the word "could," "might," or "if we don't," it is not a UDE — it is a risk or a hypothesis.

### 3. Undesirable From the System's Perspective

"Undesirable" means it works against the system's goal. Define the goal first. In a business context, the goal is typically: generate profit now and in the future while satisfying market needs.

A UDE is undesirable from that perspective — not just annoying to one person, but genuinely harmful to the system's purpose.

Good: "Customer acquisition cost increased 60% year-over-year while conversion rate declined."
Questionable: "The engineering team is unhappy with the sprint planning process." (Is this undesirable at the system level, or just a preference?)

If something is uncomfortable but not actually harming the system's goal, it is not a UDE — it is a personal preference or a stylistic issue.

### 4. An Effect, Not a Cause

This is the most common mistake. A UDE must describe **what is wrong**, not **why it is wrong**.

Wrong framing (this is a cause): "We don't have a clear product roadmap."
Right framing (this is the UDE): "Engineering teams frequently work on initiatives that are later canceled or deprioritized."

Absence statements ("we don't have X," "there is no Y") are almost always causes or policy gaps, not UDEs. Ask: "What bad thing happens because of this absence?" That is the UDE.

---

## Common Traps

### The Absence Trap

"We lack documentation" is not a UDE. Ask: what is the observable undesirable effect of lacking documentation?

Answer: "New employees take 60+ days to become independently productive." That is the UDE.

### The Solution-in-Disguise Trap

"We need to hire more salespeople" is not a UDE — it is a proposed solution framed as a problem. Unwrap it: why do we think we need more salespeople?

Answer: "Sales pipeline has more qualified opportunities than the current team can handle." That is the UDE.

### The Feeling Trap

"The team is demoralized" is borderline. It may be observable (survey data, attrition rates), but it often describes an intermediate state. Ask: what is the system-level UDE that results from low morale?

Answer: "Voluntary turnover in the product team reached 35% in the past year." Now it is observable, real, and system-undesirable.

### The Vagueness Trap

"Our process is inefficient" is not a UDE. It describes a quality (inefficiency) without specifying what is actually happening. Specificity is required.

Good: "Order processing requires 4 manual handoffs, causing a 3-day lead time for standard orders."
Bad: "Our order process is slow."

---

## Collecting UDEs in Practice

### Interviews

Ask stakeholders: "What is the one thing in this system that, if fixed, would make your work significantly better?" Then: "What does that problem cause? What do you observe?"

Use the 5 Whys in reverse — start with the symptom the person describes, verify it is observable and real, then note it.

### Metrics Review

Look at leading and lagging indicators that are currently off-target. Each metric that is trending in the wrong direction is a candidate UDE — state it as a fact, not a trend: "Churn rate is 8.3% per quarter" not "churn rate is rising."

### Complaint Clustering

If the same complaint surfaces from multiple unrelated sources (different departments, different customers, different levels), it is likely a genuine UDE rather than a personal grievance.

### Operations Review

Walk through the process from beginning to end with someone who does the work. Ask at each step: "What goes wrong here? What slows you down? What creates rework?" These are candidate UDEs.

---

## UDE Quality Checklist

Before including a UDE in your CRT, verify:

- [ ] I can state this in a single, declarative present-tense sentence
- [ ] Someone independent could confirm this exists with data or direct observation
- [ ] This harms the system's goal (not just a preference or inconvenience)
- [ ] This is an effect — not a cause, not an absence, not a solution
- [ ] This is happening now — not a risk, not a historical event
- [ ] I am not hiding a solution or cause in the wording

---

## Minimum UDE Count

A robust CRT typically requires **5 to 10 UDEs**. Fewer than 5 usually means the analysis is incomplete — the team has either described the problem too narrowly or has conflated causes with effects. More than 15 UDEs suggests the scope is too broad or that some "UDEs" are actually intermediate causes.

If you have fewer than 5, go back to stakeholders and ask: "What else is going wrong? What else would you fix if you could?"

---

## From UDEs to Tree Structure

Once you have a validated UDE list, start the tree by grouping UDEs that feel intuitively related. This grouping is a hypothesis — the tree will either confirm or disconfirm it as you trace causes upward.

The goal is to find that most UDEs trace back to one or two root causes. If after completing the tree every UDE has its own independent root cause, the UDEs are either from different systems (out of scope for a single CRT), or the causal analysis stopped too early.

See `building-a-crt.md` for the full construction walkthrough.
