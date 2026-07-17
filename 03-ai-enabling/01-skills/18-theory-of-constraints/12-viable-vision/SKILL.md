---
last_updated: 2026-04-02
status: active
name: viable-vision
description: Model business growth through sequential constraint removal using Goldratt's Viable Vision methodology. Use when developing growth strategy, evaluating market potential, designing offers that customers cannot refuse, or modeling revenue trajectories. Triggers on growth strategy, revenue modeling, market strategy, competitive positioning, and offer design.
allowed-tools: Bash(python3:*) Read Write
---

# Viable Vision

Viable Vision is Goldratt's answer to the question: "How fast can a company grow?" His claim — backed by case studies — is that any company can reach a revenue level equal to its current total profit within four years. Not by cutting costs, not by luck, but by systematically identifying and removing the constraints that are throttling growth.

The premise sounds audacious. If your company makes $10M profit today on $100M revenue, Goldratt says you can reach $10M revenue (i.e., operate as a 100% margin business at smaller scale, or more practically: dramatically increase throughput while holding operating expense near-constant). In practice it means: your constraints are causing you to leave enormous throughput on the table. Remove them in the right sequence and growth becomes inevitable.

## The Core Logic

Most companies chase growth by adding expense: hire more salespeople, spend more on marketing, build more products. Goldratt's observation is that this approach treats symptoms. The real problem is always a constraint — and a constraint, once identified, can be exploited, subordinated around, and eventually elevated at a fraction of the cost of adding resources.

The Viable Vision process:

1. **Identify the binding constraint** — what single thing limits total system throughput most?
2. **Design a Mafia Offer** — an offer so good that customers who have the problem the constraint causes cannot refuse it, yet is highly profitable for you
3. **Exploit the constraint** — get maximum output from it before spending a dollar to expand it
4. **Subordinate everything else** — every other part of the system must serve the constraint's needs
5. **Elevate** — if throughput is still limited after exploitation, invest to expand the constraint
6. **Repeat** — after elevation, the constraint moves. Find it and start over.

The four-year horizon is not arbitrary. It reflects how quickly a company that has properly identified its constraint can compound growth when subordination is working correctly.

## Why Most Growth Strategies Fail

Traditional strategy assumes the company can grow proportionally: 2x sales headcount → 2x revenue. This fails because:

- The constraint is still there. Adding salespeople doesn't help if fulfilment is the constraint.
- Operating expense rises with headcount. Margins compress even if revenue grows.
- The new resources create new bottlenecks. You've elevated one constraint and created three.

Viable Vision forces the question: "What is the ONE thing that, if removed, would unlock the most throughput?" Everything else is distraction until that one thing is resolved.

## The Mafia Offer

The Mafia Offer is the central mechanism for market-facing constraint removal. The name comes from The Godfather: "an offer you can't refuse."

A genuine Mafia Offer has three properties:

1. **Solves a significant problem** — not a nice-to-have. A problem that costs the customer real money, causes real pain, or creates real risk.
2. **Eliminates the customer's risk** — traditional offers ask the customer to bear uncertainty. A Mafia Offer transfers risk back to the supplier. "If it doesn't work, you don't pay" is the prototype.
3. **Is profitable for you** — the offer only works if your constraint removal makes it economically viable to deliver what you're promising.

The third property is where most companies stumble. They can design an attractive offer but can't deliver it profitably because their constraint is still in place. Viable Vision says: remove the constraint first, then the offer becomes economical. Or: design the offer, and let the offer force you to remove the constraint.

### Mafia Offer Examples

| Industry | Old Offer | Mafia Offer |
|----------|-----------|-------------|
| Software implementation | "We'll implement it. Timeline TBD." | "Live in 60 days or your money back." |
| Management consulting | "We'll write you a report." | "We only get paid when the improvement is measured." |
| Manufacturing supplier | "Next-day delivery 95% of the time." | "If we miss a delivery, the part is free." |
| SaaS product | "14-day free trial." | "Use it free until it pays for itself, then pay." |

In each case the offer is only credible if you've solved the internal constraint that used to make the promise dangerous. The Mafia Offer is both a market weapon and an internal forcing function.

## Scripts

### `scripts/revenue_model.py`

Model sequential constraint removal and project revenue trajectory.

```bash
python3 scripts/revenue_model.py --file input.json
```

Input: JSON with `current_annual_revenue`, `current_annual_profit`, `constraints[]` (each with `name`, `type`, `estimated_revenue_unlock`, `removal_difficulty` 1-5).

Output: Constraint removal sequence ranked by ROI (unlock/difficulty), cumulative revenue trajectory year by year, whether Goldratt's four-year target (revenue = current profit) is achievable, and feasibility assessment.

**Use when:** Building a growth roadmap, prioritizing strategic initiatives, modeling whether the Viable Vision target is realistic for your business.

### `scripts/mafia_offer.py`

Score an offer on "unrefusability" and competitive defensibility.

```bash
python3 scripts/mafia_offer.py --file input.json
```

Input: JSON with `offer_description`, `customer_pains[]` (each with `pain`, `severity` 1-10, `addressed_by_offer` bool), `competitor_offers[]` (each with `competitor`, `offer`, `weakness`).

Output: Unrefusable score 0-100 (based on % of top pains addressed and their severity), defensibility score 0-100 (based on competitor weaknesses exploited), gap analysis of unaddressed high-severity pains, and competitive positioning summary.

**Use when:** Testing whether a proposed offer is strong enough, identifying gaps in offer design before launch, or comparing offer strength against competitive alternatives.

## Sequencing Constraints for Maximum Impact

Not all constraints are equal, and not all are ready to be elevated simultaneously. The sequencing heuristic:

1. **Policy constraints first** — rules you invented to cope with an old limitation. Easiest to remove, highest leverage.
2. **Knowledge constraints second** — things you don't know how to do yet. Invest in learning.
3. **Capacity constraints third** — expand only after policy and knowledge are addressed.
4. **Market constraints last** — often a symptom of a bad offer, which is a policy/knowledge constraint.

A capacity constraint that looks fixed often dissolves when the policy constraint causing inefficient use of that capacity is removed.

## The Four-Year Math

If your current profit is P and current revenue is R, the target is: revenue grows until it equals P.

This requires revenue growth of: `(R - P) / R` reduction in "revenue needed to earn P" — or equivalently, a dramatic increase in margin through T/OE improvement.

In practice companies don't reach exactly P in revenue — they reach a state where throughput far exceeds operating expense, often with revenue significantly higher than today but margin profile transformed.

The practical test: is your constraint removal roadmap capable of delivering the throughput gains implied by the math? The `revenue_model.py` script makes this concrete.

## References

- `references/viable-vision-methodology.md` — Full framework: current state → identify constraints → design mafia offer → implement → measure → repeat
- `references/mafia-offer-design.md` — How to design an offer the market can't refuse; risk transfer mechanics; profitability requirements
