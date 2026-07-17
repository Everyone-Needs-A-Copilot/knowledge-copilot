---
last_updated: 2026-02-25
status: active
name: expense-categorization
description: Categorize expenses into actionable frameworks -- needs/wants, fixed/variable, business/personal. Use when sorting transactions, building budgets, or analyzing spending composition.
triggers:
  files: ["**/finance/**", "**/expenses/**"]
  keywords: ["categorize", "expenses", "needs", "wants", "fixed", "variable", "business", "personal", "sorting", "classification"]
allowed-tools: Read, Write, Edit
---

# Expense Categorization

Categorization transforms raw transactions into decision-making tools. A list of transactions is noise. A categorized spending breakdown is signal. The way you categorize determines what questions you can answer: "Am I spending too much on food?" requires a food category. "Can I survive a 50% income drop?" requires a needs-vs-wants split. "What can I deduct?" requires a business-vs-personal split.

The critical principle is multi-dimensional categorization. A single expense can be simultaneously a need (dimension 1), variable (dimension 2), and business (dimension 3). Each dimension serves a different decision. Flattening expenses into a single taxonomy sacrifices the ability to answer important questions.

---

## Framework

### Three-Dimensional Categorization Model

Every expense should be tagged along three independent dimensions:

**Dimension 1: Necessity (for budgeting decisions)**

| Classification | Definition | Examples |
|---------------|-----------|----------|
| Need | Required for basic functioning -- cannot eliminate without material harm | Rent, groceries, health insurance, minimum debt payments |
| Important | Significantly improves quality of life or productivity -- painful to cut | Reliable car, good internet, gym membership, quality food |
| Want | Enhances life but could be eliminated without real hardship | Dining out, streaming, hobbies, premium subscriptions |
| Luxury | Premium version of something a cheaper alternative could satisfy | First class, designer items, top-tier plans |

**Dimension 2: Flexibility (for cash flow decisions)**

| Classification | Definition | Examples |
|---------------|-----------|----------|
| Fixed | Same amount, same schedule, contractually bound | Mortgage, car payment, insurance premiums |
| Semi-fixed | Predictable range, some control | Utilities, phone plan, groceries |
| Variable | Changes month to month, fully controllable | Dining, entertainment, shopping, travel |
| Discretionary one-time | Non-recurring, fully optional | New furniture, gadgets, gifts |

**Dimension 3: Tax Character (for tax decisions)**

| Classification | Definition | Examples |
|---------------|-----------|----------|
| Business -- fully deductible | 100% business purpose | Software tools, contractor payments, business insurance |
| Business -- partially deductible | Mixed use, requires allocation | Home office, phone, internet, vehicle |
| Personal -- tax-advantaged | Personal but has tax benefit | HSA contributions, charitable donations, mortgage interest |
| Personal -- no tax benefit | Purely personal consumption | Groceries, entertainment, clothing |

### The 50/30/20 Framework (Adapted for Solopreneurs)

**Standard 50/30/20:**

| Category | Target % of Net Income | Contains |
|----------|----------------------|----------|
| Needs | 50% | Housing, utilities, groceries, insurance, minimum debt payments, transportation |
| Wants | 30% | Dining, entertainment, subscriptions, hobbies, upgrades |
| Savings & Debt Paydown | 20% | Emergency fund, retirement, investments, extra debt payments |

**Solopreneur Adaptation (50/20/15/15):**

| Category | Target % of Gross Revenue | Contains |
|----------|--------------------------|----------|
| Business operations | 20% | Tools, contractors, marketing, business insurance, professional development |
| Taxes | 25-35% | Federal, state, self-employment (set aside, not discretionary) |
| Personal needs | 30% | Housing, utilities, food, personal insurance, transportation |
| Personal wants + savings | 15-25% | Discretionary + retirement + investments |

Note: Percentages are of gross revenue for solopreneurs because taxes must be explicitly planned.

### Expense Scoring System

For expenses that are hard to classify, use this scoring rubric:

**Necessity Score (1-5)**

| Score | Meaning | Test |
|-------|---------|------|
| 5 | Survival essential | Would I be homeless, hungry, or uninsured without this? |
| 4 | Functional essential | Would my ability to work or live be materially impaired? |
| 3 | Productivity enhancer | Does this save me significant time or improve output? |
| 2 | Quality-of-life enhancer | Does this bring meaningful enjoyment or comfort? |
| 1 | Pure discretionary | Could I eliminate this and barely notice after a week? |

**ROI Score (1-5, for business expenses)**

| Score | Meaning | Test |
|-------|---------|------|
| 5 | Direct revenue generator | Removing this would directly reduce revenue |
| 4 | Strong enabler | Significantly improves capacity or client experience |
| 3 | Moderate enabler | Helpful but alternatives exist |
| 2 | Marginal benefit | Nice to have, unclear impact |
| 1 | No measurable benefit | Cannot articulate what this accomplishes |

### Category Taxonomy

**Level 1: Primary Categories (10-15 max)**

| # | Category | Subcategories |
|---|----------|---------------|
| 1 | Housing | Rent/mortgage, property tax, insurance, maintenance, HOA |
| 2 | Utilities | Electric, gas, water, sewer, trash, internet, phone |
| 3 | Food | Groceries, dining out, delivery, coffee shops, alcohol |
| 4 | Transportation | Car payment, insurance, fuel, maintenance, parking, transit, rideshare |
| 5 | Healthcare | Premiums, copays, prescriptions, dental, vision, therapy, HSA |
| 6 | Insurance | Life, disability, umbrella (non-health, non-auto, non-home) |
| 7 | Debt Service | Student loans, credit cards, personal loans (minimum payments) |
| 8 | Subscriptions | Streaming, software, memberships, publications, SaaS |
| 9 | Personal | Clothing, grooming, gifts, hobbies, education, fitness |
| 10 | Business Ops | Tools, contractors, marketing, professional dev, business insurance |
| 11 | Taxes | Federal, state, local, self-employment, property |
| 12 | Savings | Emergency fund, retirement, brokerage, goal-specific |
| 13 | Giving | Charitable, religious, community |
| 14 | Miscellaneous | Uncategorized (target: < 3% of total) |

### Mixed-Use Expense Allocation Rules

| Expense | Allocation Method | Documentation |
|---------|-------------------|---------------|
| Home office | Square footage: office / total home | Measure and record once, update if changes |
| Internet | Time-based: business hours / total hours, or 50/50 | Log if audited, reasonable estimate acceptable |
| Phone | Usage-based or flat 50/50 split | Second line simplifies to 100% business |
| Vehicle | Mileage log: business miles / total miles | IRS requires contemporaneous log |
| Computer | Primary use test: > 50% business = business asset | Track usage pattern for first month |
| Professional development | Direct business relevance test | Must maintain or improve current business skills |
| Meals | Business purpose: with client or during business travel | Document who, what business was discussed |

---


## Define Done

- [ ] Financial data gathered and categorized accurately
- [ ] Analysis based on actual numbers, not estimates
- [ ] Recommendations account for tax implications and time horizon
- [ ] Action steps are specific and prioritized

## Application

### Transaction Categorization Workflow

**Step 1: Auto-categorize by vendor**

Build a vendor-to-category mapping. Most transactions recur with the same vendor:

| Vendor Pattern | Auto-Category | Dimension Tags |
|---------------|---------------|----------------|
| Whole Foods, Trader Joe's | Food > Groceries | Need, Variable, Personal |
| Shell, Chevron | Transport > Fuel | Need, Variable, Personal (or split) |
| Adobe, Figma | Business > Tools | Business, Fixed, Deductible |
| Netflix, Spotify | Subscriptions > Streaming | Want, Fixed, Personal |

**Step 2: Review and correct auto-categorizations**

Focus on: new vendors, amounts that differ from pattern, merchants that serve multiple categories (e.g., Amazon, Target, Costco).

**Step 3: Tag multi-dimensional attributes**

For each transaction, confirm all three dimensions are assigned (necessity, flexibility, tax character).

**Step 4: Handle edge cases**

| Edge Case | Resolution |
|-----------|-----------|
| Amazon purchase (could be anything) | Categorize by item, not vendor |
| Costco (groceries + household + business) | Split transaction by receipt line items |
| Venmo/PayPal (peer transfers) | Categorize by purpose, not platform |
| ATM withdrawal | Categorize as "Cash" and estimate allocation |
| Credit card payment | Do not categorize (avoid double-counting); categorize the charges |
| Transfer between own accounts | Exclude from spending analysis |

### Emergency Budget Triage

When income drops, use categorization to identify cuts quickly:

| Priority to Cut | Category Criteria | Expected Savings |
|----------------|-------------------|------------------|
| Cut first | Luxury + Variable + Personal | Immediate, no consequence |
| Cut second | Want + Variable + Personal | Noticeable but manageable |
| Cut third | Want + Fixed + Personal | May have cancellation fees, plan timing |
| Reduce fourth | Need + Semi-fixed (downgrade) | Switch plans, shop for lower rates |
| Protect last | Need + Fixed + contractual | Housing, insurance, minimum debt payments |

---

## Quick Reference

### Categorization Decision Tree

1. Is this a transfer between my own accounts? **Exclude.**
2. Is this a credit card payment for charges already categorized? **Exclude.**
3. Can I identify the specific purpose? **Categorize by purpose.**
4. Is this a mixed-use purchase? **Split by line item or apply allocation rule.**
5. Is this vendor in my mapping table? **Auto-assign, review if amount unusual.**
6. New vendor? **Assign all three dimension tags manually.**

### Category Health Metrics

| Metric | Healthy Target |
|--------|---------------|
| Miscellaneous / Total Spending | < 3% |
| Needs / Net Income | < 55% |
| Fixed / Total Spending | < 65% |
| Subscriptions / Discretionary | < 25% |
| Business Expenses / Gross Revenue | 15-30% (varies by industry) |

### Monthly Categorization Checklist

- [ ] Export all transactions from all accounts
- [ ] Run auto-categorization against vendor mapping
- [ ] Review and correct auto-categorized transactions
- [ ] Manually categorize new vendors
- [ ] Split mixed-use purchases
- [ ] Apply allocation rules to shared expenses
- [ ] Verify all three dimension tags are assigned
- [ ] Check miscellaneous category is < 3%
- [ ] Update vendor mapping with new recurring vendors

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Too many categories (30+) | Analysis paralysis, inconsistent sorting | Keep to 10-15 primary categories with subcategories |
| Too few categories (3-5) | Cannot answer specific questions | Use at least the 10-category taxonomy above |
| Single-dimension only | Cannot answer "what can I cut?" or "what can I deduct?" | Always tag all three dimensions |
| Categorizing by vendor instead of purpose | Amazon, Target, Costco serve multiple categories | Categorize by what was purchased, not where |
| Ignoring credit card payments vs charges | Double-counts spending | Categorize charges, exclude payments |
| Letting miscellaneous grow | Hides actual spending patterns | Recategorize monthly, keep misc < 3% |
| Rigid categories that never evolve | Life changes, spending patterns change | Review and adjust taxonomy annually |
| Not splitting mixed-use expenses | Understates business expenses, overstates personal | Apply documented allocation rules consistently |
| Categorizing aspirationally | Calling wants "needs" distorts analysis | Use the necessity test honestly: would I be materially harmed without this? |


## Quality Tests

### Accuracy Test
- All calculations are correct and assumptions are stated
- **PASS:** Numbers are verifiable and assumptions clearly documented
- **FAIL:** Rough estimates presented as precise figures

### Completeness Test
- Analysis considers tax implications and opportunity costs
- **PASS:** Tax impact calculated for each recommendation
- **FAIL:** Pre-tax returns presented without noting tax drag

