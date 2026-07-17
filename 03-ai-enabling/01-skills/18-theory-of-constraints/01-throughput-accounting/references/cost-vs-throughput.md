---
last_updated: 2026-04-02
status: active
---

# Cost Accounting vs Throughput Accounting

## Why Cost Accounting Leads to Wrong Decisions

Cost accounting was designed for financial reporting, not decision-making. It allocates fixed overhead to individual products/services based on arbitrary allocation bases (labor hours, machine hours, revenue proportion). This creates "fully loaded costs" that don't reflect how costs actually behave.

### The Core Problem

| What Cost Accounting Does | What Actually Happens |
|--------------------------|----------------------|
| Allocates rent to each product | Rent stays the same whether you sell 1 product or 100 |
| Allocates salaries to each service | Engineers get paid whether they work on Feature A or Feature B |
| Reports "cost per unit" including overhead | Killing a "high cost" product doesn't actually reduce overhead |
| Suggests cutting "unprofitable" products | The overhead gets reallocated to remaining products, making THEM look unprofitable |

### The Death Spiral

This is the most dangerous outcome of cost accounting:

1. Product A appears unprofitable after overhead allocation
2. Management discontinues Product A
3. Overhead doesn't decrease (it's fixed)
4. Overhead gets reallocated across fewer products
5. Product B now appears unprofitable
6. Repeat until the company has one product carrying all overhead

### Example: SaaS Tiers

**Cost Accounting View:**
| Tier | Revenue | "Allocated Cost" | "Profit" |
|------|---------|-------------------|----------|
| Base ($99) | $99,000 | $85,000 | $14,000 |
| CRM ($149) | $29,800 | $35,000 | -$5,200 |

Conclusion: "CRM tier is losing money. Discontinue it."

**Throughput Accounting View:**
| Tier | Revenue | Truly Variable Costs | Throughput |
|------|---------|---------------------|------------|
| Base ($99) | $99,000 | $3,790 | $95,210 |
| CRM ($149) | $29,800 | $2,382 | $27,418 |

Conclusion: "CRM tier generates $27,418 in throughput. Discontinuing it would reduce total throughput by $27,418 while OE stays the same. Net profit drops by $27,418."

### When to Use Each

| Use Cost Accounting For | Use Throughput Accounting For |
|------------------------|------------------------------|
| Tax reporting | Product/service mix decisions |
| GAAP financial statements | Pricing decisions |
| Investor reporting | Hiring decisions |
| Regulatory compliance | Investment evaluation |
| Historical analysis | "Should we do X?" questions |
