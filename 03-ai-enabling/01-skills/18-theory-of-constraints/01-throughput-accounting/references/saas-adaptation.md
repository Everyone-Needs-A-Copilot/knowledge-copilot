---
last_updated: 2026-04-02
status: active
---

# Adapting Throughput Accounting for SaaS

## Mapping T/I/OE to Subscription Businesses

Goldratt developed Throughput Accounting for manufacturing. In SaaS and subscription businesses, the concepts apply but the categories shift.

### Throughput (T) in SaaS

**T = Monthly Recurring Revenue - Truly Variable Costs**

Truly variable costs in SaaS (costs that scale per customer/transaction):
- AI inference costs per API call
- Payment processing fees (Stripe's 2.9%)
- Per-seat third-party API costs (enrichment services, etc.)
- Data transfer/bandwidth per customer
- Per-customer cloud compute (if isolated)

NOT variable costs (these are OE):
- Engineering salaries (paid regardless of customer count)
- Infrastructure base costs (servers run whether you have 10 or 1000 customers)
- Sales team compensation (unless purely commission-based)
- Office rent, tools, subscriptions

### Investment (I) in SaaS

Money tied up in the system:
- Product development cost (capitalized R&D)
- Server infrastructure (purchased, not rented)
- Security deposits on office/equipment leases
- Prepaid annual contracts (cloud, tools)
- Customer acquisition cost not yet recovered (CAC payback period = money tied up)

### Operating Expense (OE) in SaaS

Everything else — the fixed costs of running the business:
- All salaries and benefits
- Cloud infrastructure base costs
- SaaS tool subscriptions
- Marketing spend (unless directly tied to per-conversion cost)
- Office, insurance, legal, accounting

### The Constraint in SaaS

Common constraints in SaaS businesses:

| Constraint | Symptom | Exploit Strategy |
|-----------|---------|-----------------|
| Market/demand | Can build more than you can sell | Focus all marketing on highest-conversion channels |
| Sales bandwidth | More leads than sales can handle | Qualify harder, raise prices, automate low-touch |
| Engineering capacity | More features needed than can be built | Prioritize by throughput impact, not by volume of requests |
| Onboarding/support | Customers sign up but don't activate | Automate onboarding, focus support on highest-value accounts |
| Infrastructure | System can't handle more load | Optimize before scaling hardware |

### Throughput Per Constraint Unit in SaaS

The critical metric: which product/tier/feature generates the most throughput per unit of your constraint?

| If Constraint Is | Constraint Unit | Rank Products By |
|-----------------|----------------|-----------------|
| Engineering time | Dev hours per feature | T per dev hour |
| Server capacity | Compute units per customer | T per compute unit |
| Sales bandwidth | Sales hours per deal | T per sales hour |
| Support capacity | Support hours per customer | T per support hour |

This ranking determines what to prioritize — not margin, not revenue, not "strategic importance."
