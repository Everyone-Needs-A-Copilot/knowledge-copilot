---
last_updated: 2026-04-02
status: active
name: technology-constraint
description: Evaluate technology investments using Goldratt's "Necessary But Not Sufficient" framework. Use when assessing whether technology purchases will deliver value, auditing past technology investments, or deciding whether to build vs buy. Triggers on technology evaluation, build vs buy, ROI on technology, digital transformation, and tool adoption.
allowed-tools: Bash(python3:*) Read Write
---

# Technology Constraint

Goldratt's "Necessary But Not Sufficient" is a deceptively simple observation: technology is a necessary condition for the value it promises, but it is almost never sufficient on its own to deliver that value. The missing ingredient is almost always a change in the rules — the policies, processes, and assumptions that were put in place to cope with the limitation the technology is supposed to remove.

This explains why so many technology investments underperform. The technology works. The problem is that the organization continues operating by rules designed for a world where the old limitation still exists.

## The Four Questions

Goldratt's framework for evaluating any technology investment:

### Question 1: What is the power of the technology?

What can this technology do that was previously impossible or impractical?

A good answer is specific and constraint-aware. "It's faster" is not a power statement. "It enables real-time inventory visibility across all warehouses" is a power statement, because it names a previously impossible capability.

Vague power statements are the first warning sign. If you can't articulate the specific new capability in one sentence, the purchase rationale is probably based on vendor marketing, not strategic analysis.

### Question 2: What limitation does it diminish?

What specific constraint in your current system does this technology reduce or eliminate?

Note the word "diminish," not "eliminate." Technology rarely eliminates a constraint completely — it reduces its severity. The question is: what were you previously unable to do (or do well) that this technology makes easier?

The answer must connect to a real constraint you've identified in your system. If the limitation in Question 2 is not currently causing you measurable throughput loss, the technology is addressing a non-constraint — which, by definition, cannot improve system throughput even if it works perfectly.

### Question 3: What rules helped us accommodate the limitation?

Every limitation generates compensating rules. When we couldn't have real-time inventory data, we created rules: "Order in batches of 100 to reduce the risk of stockouts." "Always hold 4 weeks of safety stock." "Confirm availability with warehouse before committing to customer."

These rules were rational when the limitation existed. They are often invisible because they've become standard operating procedure — nobody questions them.

This question requires active archaeology: looking at your current processes and asking "why do we do this?" until you find the rule that exists because of the old limitation.

### Question 4: What rules should we use now?

With the limitation diminished, the old rules are not just unnecessary — they're counterproductive. Safety stock rules designed for a world without real-time visibility actively destroy value in a world with it. They create excess inventory, slow response time, and consume cash.

The new rules must be designed from scratch, starting from the new capability the technology provides. What can you now do that you couldn't do before? What rules would you design if you were starting with this capability from day one?

The answer to this question is where the value of the technology actually lives.

## Why Technology Fails to Deliver

The classic failure pattern:

1. Company buys technology to solve a problem
2. Technology is implemented technically correctly
3. Company continues operating by old rules
4. Results disappoint
5. Conclusion: "The technology didn't deliver"

The technology delivered everything it could. The company failed to change the rules that were blocking value realization.

### The CRM Example

A company buys a CRM to improve sales performance. The CRM has the power to give sales managers real-time visibility into pipeline health, deal velocity, and rep activity.

The limitation it diminishes: previously, pipeline visibility required weekly manual roll-ups from sales reps, which were slow, incomplete, and often wishful.

The old rules that accommodated the limitation:
- Weekly pipeline review meetings (everyone stops to compile status)
- "Don't bother the rep during the deal — they'll update the forecast on Friday"
- Forecasting based on rep judgment, not deal data
- Managers wait for a deal to slip before intervening

After the CRM implementation, these rules remain intact. The weekly meetings still happen. Reps still only update on Friday. Managers still wait for Friday reports.

The CRM is technically live. Usage metrics are good. But sales performance hasn't improved, because the rules that made the CRM necessary — the weekly roll-up culture, the hands-off management style, the Friday forecasting rhythm — are still in place.

The new rules that should replace them:
- Managers review pipeline daily, not weekly (now possible — data is always current)
- Deal health criteria trigger automatic flags (no manual roll-up required)
- Intervention happens when a deal goes quiet, not after it slips (now detectable)
- Forecasting is generated from deal data, not rep estimates (CRM contains this data)

None of these rules require additional technology. They require changing how work is done.

## The Build vs. Buy Question

The four-question framework applies equally to build vs. buy decisions:

| Question | Build Consideration | Buy Consideration |
|----------|--------------------|--------------------|
| Power | What capability does building give you that buying doesn't? | What capability does the vendor provide that you'd take years to build? |
| Limitation | Does building actually remove your constraint, or just give you control? | Does buying remove the constraint, or does it just move the problem? |
| Old rules | Which of your current rules exist because you're constrained by bought tools? | Which of your current rules exist because you lacked the vendor's capability? |
| New rules | What process would you redesign if you owned the platform? | What process would you redesign if the vendor's capability existed from day one? |

The common mistake in build decisions: building because you're frustrated with bought tools, when the real constraint is a rule you've never challenged. Building the tool doesn't change the rule.

## Scripts

### `scripts/tech_assessment.py`

Evaluate a single technology investment using the four-question framework.

```bash
python3 scripts/tech_assessment.py --file input.json
```

Input: JSON with `technology`, `power`, `limitation_diminished`, `old_rules[]` (each with `rule`, `still_active` bool, `replacement_rule` string or null), `investment_cost`.

Output: power clarity score (0-100), rule-change completeness (what % of old rules have replacement rules), old rules audit (rules still active without replacement), unrealized value assessment, recommendations.

**Use when:** Evaluating whether a technology investment will deliver, or diagnosing why an existing investment is underperforming.

### `scripts/rule_change_audit.py`

Audit a portfolio of technology investments for rule-change completeness and value realization.

```bash
python3 scripts/rule_change_audit.py --file input.json
```

Input: JSON with `investments[]` (each with `technology`, `cost`, `old_rules_count`, `rules_changed`, `value_expected`, `value_realized`).

Output: per-investment analysis, portfolio summary, correlation between rule-change ratio and value realization, recommendations for underperforming investments.

**Use when:** Running a post-implementation review, identifying which technology investments have unrealized value, or making the case for process change to accompany technology.

## References

- `references/four-questions-framework.md` — Walkthrough of the four questions with worked examples
- `references/necessary-not-sufficient.md` — The full framework from Goldratt's perspective, adapted for modern technology purchasing decisions
