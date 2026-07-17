---
last_updated: 2026-04-02
status: active
---

# Common Business Clouds

Pre-structured Evaporating Clouds for recurring business dilemmas. Each cloud is a starting point — refine the box statements to match your specific context before surfacing assumptions.

---

## Cloud 1: Growth vs. Cash Flow

**The dilemma:** Invest in growth initiatives (headcount, marketing, product) vs. conserve cash for stability.

```
A: Build a financially sustainable, growing business
B: Generate enough revenue to scale operations
C: Maintain positive cash flow and financial stability
D: Invest aggressively in growth (headcount, marketing, product)
D': Minimize spending and preserve cash reserves
```

**Key assumptions to surface on B→D:**
- Revenue growth requires proportional spending increases
- We cannot grow revenue without increasing headcount or marketing budget
- Our market window requires speed over efficiency

**Key assumptions to surface on C→D':**
- Cash reserves can only be protected by reducing spend (not by increasing revenue)
- Investors will not provide additional capital if needed
- Our burn rate puts us at existential risk within [X months]

**Common injection:** Find revenue sources (upsell, pricing, partnerships) that improve cash flow while enabling growth — so you don't have to choose between the two.

---

## Cloud 2: Speed vs. Quality

**The dilemma:** Ship features quickly to stay competitive vs. maintain quality standards to avoid defects and rework.

```
A: Deliver software that wins and retains customers
B: Stay ahead of market and competitor expectations
C: Maintain trust through reliable, defect-free software
D: Ship features on an aggressive timeline (compress testing, skip documentation)
D': Follow full QA process and quality gates before release
```

**Key assumptions to surface on B→D:**
- Speed of delivery is the primary factor customers use to evaluate our product
- Competitors release faster than us, causing us to lose deals
- We cannot be first-to-market while following full QA

**Key assumptions to surface on C→D':**
- A defect in production damages trust more than a late release
- Our current QA process is the minimum necessary to catch critical defects
- Quality and speed are inherently in tension in our current engineering setup

**Common injection:** Invest in automated testing and CI/CD infrastructure so quality gates run faster — making speed and quality complementary rather than competing.

---

## Cloud 3: Standardize vs. Customize

**The dilemma:** Standardize the product for operational efficiency vs. customize for individual customer needs.

```
A: Grow revenue with a profitable, scalable business model
B: Operate efficiently and control costs as we scale
C: Win and retain customers by meeting their specific requirements
D: Standardize product and processes; resist custom requests
D': Accommodate custom requirements for key accounts
```

**Key assumptions to surface on B→D:**
- Customization increases cost non-linearly (each custom is unique)
- There is no way to standardize a configurable product that meets diverse needs
- Operational efficiency requires identical processes for all customers

**Key assumptions to surface on C→D':**
- Our target customers have fundamentally different needs that cannot be met by one product
- Customers will not accept a standardized product if a competitor offers customization
- Winning large accounts requires bespoke development

**Common injection:** Build a platform with configuration layers — standardize the core, parameterize the variations. Customers get "their" product; operations stays scalable.

---

## Cloud 4: Short-Term Metrics vs. Long-Term Investment

**The dilemma:** Hit quarterly targets (cuts, deferrals) vs. invest in capabilities that pay off in 2-3 years.

```
A: Build a business that performs well now and is competitive in the future
B: Meet current financial commitments and investor expectations
C: Build the capabilities needed to compete in the future market
D: Cut costs, defer investment, optimize for near-term financial metrics
D': Fund R&D, people, and infrastructure for future competitiveness
```

**Key assumptions to surface on B→D:**
- The only way to hit quarterly targets is to cut investment
- Investors will react negatively if we miss a quarter to invest in growth
- Current financial metrics are the primary signal of business health

**Key assumptions to surface on C→D':**
- Future competitiveness requires current spending that reduces near-term profit
- There are no ways to build capability that are self-funding or that pay back within 12 months
- Capability investments cannot be prioritized without increasing total spend

**Common injection:** Identify investments with near-term revenue contribution (e.g., customer success that reduces churn, tooling that accelerates revenue-generating work), making them financially self-justifying in the current period.

---

## Cloud 5: Centralize vs. Decentralize

**The dilemma:** Centralize decision-making for consistency and control vs. decentralize for speed and local responsiveness.

```
A: Execute strategy consistently while responding quickly to local conditions
B: Ensure brand consistency, risk management, and strategic alignment
C: Enable teams to move quickly and respond to market conditions
D: Centralize all significant decisions through headquarters approval
D': Give local teams full autonomy to make decisions independently
```

**Key assumptions to surface on B→D:**
- Local teams cannot be trusted to make decisions aligned with strategy
- Consistency can only be achieved through central approval
- Decentralized decisions introduce unacceptable brand or legal risk

**Key assumptions to surface on C→D':**
- Speed requires autonomy — central approval always creates bottlenecks
- Local teams have context that headquarters lacks
- The market moves faster than our approval cycle

**Common injection:** Establish clear decision rights by type (strategic vs. operational vs. tactical), with rules-based autonomy for well-defined decisions and escalation for exceptions. Speed and consistency both improve.

---

## Cloud 6: Expert Opinion vs. Data-Driven Decision

**The dilemma:** Follow expert judgment vs. require data evidence before acting.

```
A: Make decisions that lead to good outcomes for the business
B: Leverage domain expertise and pattern recognition for nuanced situations
C: Ensure decisions are grounded in evidence, not bias
D: Defer to expert opinion, especially when data is ambiguous
D': Require statistically significant data before approving decisions
```

**Key assumptions to surface on B→D:**
- Experts in our domain have reliable intuition that outperforms naive data analysis
- The situation is too novel or complex for historical data to apply
- Waiting for data means missing the window to act

**Key assumptions to surface on C→D':**
- Expert opinions are subject to bias that data can correct
- We have enough data, or can get it quickly enough, to inform this decision
- Being wrong is worse than being slow

**Common injection:** Use expert judgment to form hypotheses, then design fast experiments to validate or invalidate them — so data and expertise are complementary inputs to the same decision.

---

## How to Use These Templates

1. Select the cloud that most closely matches your dilemma
2. Restate each box in the specific language of your situation
3. Verify: does each box reflect reality in your specific context? Adjust until it does
4. Run `cloud_builder.py` with the customized five-box structure
5. Surface assumptions per arrow (at least 2 per arrow)
6. Run `assumption_analyzer.py` to rank by vulnerability
7. Design injections targeting the most vulnerable assumptions
8. Test each injection against both needs: does it allow B and C to coexist?
