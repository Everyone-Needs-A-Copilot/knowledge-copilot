---
last_updated: 2026-04-02
status: active
name: throughput-accounting
description: Evaluate business decisions using Goldratt's Throughput Accounting (T, I, OE) instead of cost accounting. Use when analyzing pricing decisions, product mix, hiring, investments, or any decision where "should we spend money on X" needs a rigorous answer. Triggers on pricing, margin analysis, investment evaluation, hiring decisions, product mix, and cost-vs-value trade-offs.
allowed-tools: Bash(python3:*) Read Write
---

# Throughput Accounting

Throughput Accounting replaces cost accounting for decision-making. Cost accounting allocates overhead to products and asks "what does this cost?" Throughput Accounting asks three different questions: "Does this increase Throughput? Does this reduce Investment? Does this reduce Operating Expense?" — in that priority order.

The core insight: most companies optimize by cutting costs (OE). But OE has a floor (zero) and cutting it often damages throughput. Throughput has no ceiling. The leverage is in T, not OE.

## The Three Measurements

| Measure | Definition | Examples |
|---------|-----------|----------|
| **Throughput (T)** | Rate the system generates money through sales. Revenue minus truly variable costs only. | Revenue - materials - sales commissions - per-unit API costs |
| **Investment (I)** | Money tied up in the system | Equipment, inventory, deposits, prepaid contracts, IP development |
| **Operating Expense (OE)** | Money spent to turn I into T. All fixed costs. | Salaries, rent, subscriptions, insurance — everything that isn't truly variable |

**Critical distinction:** Labor is OE, not a variable cost. You pay salaries whether or not you make a sale. Only costs that change per unit of sale are truly variable.

## Decision Priority

For ANY business decision, evaluate impact in this order:

1. **Does it increase T?** (highest leverage — no ceiling)
2. **Does it reduce I?** (frees capital)
3. **Does it reduce OE?** (lowest leverage — has a floor of zero)

A decision that increases T by $1 is worth more than one that reduces OE by $1, because T compounds and OE reduction has diminishing returns.

## Scripts

### `scripts/throughput_analysis.py`

Analyze revenue streams by throughput contribution.

```bash
python3 scripts/throughput_analysis.py --file input.json
```

Input: JSON with `revenue_streams[]` (each having `name`, `revenue`, `variable_costs`, `constraint_units`), `operating_expenses`, `investment`.

Output: T, I, OE, Net Profit, ROI for each stream. Streams ranked by throughput per constraint unit.

**Use when:** Evaluating which products/services/tiers to prioritize, which to sunset, or where to focus sales effort.

### `scripts/product_mix.py`

Determine optimal product/service mix given a constraint.

```bash
python3 scripts/product_mix.py --file input.json
```

Input: JSON with `products[]` (each having `name`, `throughput_per_unit`, `constraint_units_per_unit`, `demand`), `constraint_capacity`.

Output: Optimal production/sales order using Goldratt's greedy algorithm (rank by T per constraint unit, fill from top). Shows total throughput, which products get full demand, which get partial, which get rejected.

**Use when:** You have limited capacity (engineering time, sales bandwidth, server capacity) and need to decide what to build/sell/serve first.

### `scripts/investment_decision.py`

Compare investment options through the throughput lens.

```bash
python3 scripts/investment_decision.py --file input.json
```

Input: JSON with `options[]` (each having `name`, `cost`, `delta_throughput`, `delta_investment`, `delta_operating_expense`).

Output: Each option scored by delta_T (primary), delta_ROI, payback months. Ranked by throughput impact first, not cost savings.

**Use when:** Evaluating whether to hire, buy equipment, invest in a feature, expand infrastructure, or any capital allocation decision.

### `scripts/hiring_model.py`

Model the throughput impact of adding headcount.

```bash
python3 scripts/hiring_model.py --file input.json
```

Input: JSON with `role`, `annual_salary`, `benefits_pct`, `overhead_pct`, `expected_monthly_throughput_increase`, `ramp_months`.

Output: Fully loaded monthly cost, breakeven month, year-1 ROI, cumulative throughput gain over 12 months. Recommends hire/defer/restructure.

**Use when:** Deciding whether and when to hire, what salary range is justified by throughput, or comparing hiring vs. tooling vs. outsourcing.

## Key Principles

- **Never allocate overhead to products.** Cost-per-unit thinking leads to wrong decisions. A product with low "margin" in cost accounting may have the highest throughput per constraint unit.
- **The constraint determines the mix.** Without identifying the constraint, throughput analysis is incomplete. Use the constraint-identification skill first if the constraint is unknown.
- **T is always revenue minus truly variable costs.** If you'd pay it even with zero sales, it's OE, not variable.

## References

- [Cost Accounting vs Throughput Accounting](references/cost-vs-throughput.md) — Why cost accounting systematically leads to wrong decisions
- [Adapting TA for SaaS](references/saas-adaptation.md) — How to apply T/I/OE to subscription businesses
- [Product Mix Decisions](references/product-mix-decisions.md) — Detailed walkthrough of the greedy algorithm with examples

## When NOT to Use

- For tax reporting or GAAP compliance (use standard accounting)
- For external financial statements (investors expect traditional metrics)
- When there is no identifiable constraint (everything is underutilized)

Throughput Accounting is a decision-making framework, not a reporting framework. Use it alongside traditional accounting, not instead of it.
