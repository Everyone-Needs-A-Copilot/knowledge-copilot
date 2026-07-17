---
last_updated: 2026-04-02
status: active
---

# Product Mix Decisions with Throughput Accounting

## The Greedy Algorithm

When you can't meet all demand (the constraint is limiting), Goldratt's product mix algorithm is:

1. Calculate Throughput per unit for each product: T = Price - Truly Variable Cost
2. Calculate constraint usage per unit for each product
3. Calculate T per constraint unit: T/CU = Throughput / Constraint Units
4. Rank all products by T/CU, highest first
5. Fill constraint capacity starting from the top
6. Products at the bottom may get partial or zero allocation

This is mathematically provable as the optimal mix for a single constraint. Cost accounting's "highest margin first" approach often gives the wrong answer.

## Why Cost Accounting Gets Product Mix Wrong

**Setup:** Two products, one constraint (machine hours).

| Product | Price | Variable Cost | Overhead Allocated | "Full Cost" | "Margin" |
|---------|-------|---------------|-------------------|-------------|----------|
| A | $100 | $30 | $40 | $70 | $30 (30%) |
| B | $80 | $20 | $50 | $70 | $10 (12.5%) |

Cost accounting says: prioritize Product A (30% margin vs 12.5%).

But add the constraint:

| Product | Throughput (T) | Constraint Hours/Unit | T per Hour |
|---------|---------------|----------------------|------------|
| A | $70 | 2 hours | $35/hr |
| B | $60 | 1 hour | $60/hr |

Throughput Accounting says: prioritize Product B ($60/hr vs $35/hr).

**If you have 100 constraint hours:**
- Cost accounting mix (prioritize A): 50 units of A = $3,500 throughput
- Throughput accounting mix (prioritize B): 100 units of B = $6,000 throughput

The "low margin" product generates **71% more throughput** because it uses less of the constraint.

## Multi-Product SaaS Example

| Tier | Monthly Price | Variable Cost/Seat | T/Seat | Support Hours/Seat/Mo | T per Support Hour |
|------|-------------|-------------------|--------|----------------------|-------------------|
| Base | $99 | $3.79 | $95.21 | 0.2 | $476.05 |
| CRM | $149 | $11.91 | $137.09 | 0.5 | $274.18 |
| Enterprise | $119/seat + platform | $14.17 | $104.83 | 1.5 | $69.89 |

If the constraint is support capacity:
1. Prioritize Base (highest T per support hour)
2. Then CRM
3. Enterprise last — unless its platform fee changes the math

This doesn't mean "don't sell Enterprise." It means when support is the bottleneck, invest in reducing Enterprise support load (better onboarding, self-serve tools) before adding more Enterprise customers.

## When the Constraint Shifts

The mix decision changes when the constraint moves. After exploiting and elevating the current constraint, a new resource becomes the bottleneck — and the T/CU ranking may change completely.

Always re-run the product mix analysis when:
- You've added capacity to the constraint
- A new product/tier is introduced
- Demand patterns shift significantly
- Variable costs change materially
