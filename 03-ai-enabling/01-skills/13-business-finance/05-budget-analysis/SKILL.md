---
last_updated: 2026-02-25
status: active
name: budget-analysis
description: Analyze spending patterns, identify trends, and surface anomalies in personal and business budgets. Use when reviewing monthly expenses, comparing budget vs actual, or investigating spending changes.
triggers:
  files: ["**/finance/**", "**/budget/**"]
  keywords: ["budget", "spending", "patterns", "trends", "anomalies", "expenses", "monthly review", "spending analysis"]
allowed-tools: Read, Write, Edit
---

# Budget Analysis

Budget analysis is not about restriction -- it is about visibility. Most financial problems stem from delayed awareness: a subscription that doubled, a category that crept up 15% over three months, a one-time charge that became recurring. The purpose of budget analysis is to surface these signals early, before they compound into structural problems.

Effective budget analysis operates on three levels: snapshot (what happened this month), trend (how does this compare to the last 3-6 months), and structural (are my spending ratios aligned with my goals). Each level reveals different insights and demands different responses.

---

## Framework

### Three-Level Analysis Model

| Level | Timeframe | Question Answered | Action Triggered |
|-------|-----------|-------------------|------------------|
| Snapshot | Current month | What happened? | Flag outliers |
| Trend | 3-6 months | What is changing? | Adjust budget targets |
| Structural | 6-12 months | Are ratios aligned? | Redesign budget categories |

### Spending Pattern Analysis Process

**Step 1: Gather and Normalize Data**

| Data Point | Source | Normalization |
|------------|--------|---------------|
| Bank transactions | Bank export / CSV | Standardize category names |
| Credit card transactions | Card export / CSV | Remove pending duplicates |
| Cash transactions | Manual log | Estimate if incomplete |
| Recurring subscriptions | Subscription tracker | Annualize, then divide by 12 |
| Irregular expenses | Calendar review | Amortize over 12 months |

**Step 2: Categorize and Aggregate**

Primary categories with suggested subcategories:

| Category | Subcategories | Benchmark % of Income |
|----------|---------------|-----------------------|
| Housing | Rent/mortgage, insurance, maintenance, property tax | 25-35% |
| Transportation | Car payment, insurance, fuel, maintenance, transit | 10-15% |
| Food | Groceries, dining out, delivery, coffee | 10-15% |
| Healthcare | Insurance premiums, copays, prescriptions, dental | 5-10% |
| Utilities | Electric, water, gas, internet, phone | 5-8% |
| Subscriptions | Software, streaming, memberships, SaaS | 2-5% |
| Personal | Clothing, grooming, gifts, hobbies | 5-10% |
| Savings/Investment | Retirement, brokerage, emergency fund | 15-25% |
| Business (if applicable) | Tools, contractors, education, marketing | Varies |

**Step 3: Compare Against Targets**

| Variance | Classification | Response |
|----------|---------------|----------|
| Within 5% | On track | No action needed |
| 5-15% over | Yellow flag | Investigate cause, note for next month |
| 15-30% over | Orange flag | Identify specific drivers, create correction plan |
| 30%+ over | Red flag | Immediate review, likely anomaly or structural issue |
| Under budget | Green flag | Verify not deferred spending, consider reallocation |

### Trend Identification Framework

**Month-Over-Month (MoM) Analysis**

| Signal | What It Means | Investigation |
|--------|---------------|---------------|
| Category up 3 consecutive months | Lifestyle inflation or new commitment | Check for new subscriptions, habit changes |
| Sudden spike (50%+ over average) | One-time event or anomaly | Verify: emergency, annual bill, or error |
| Gradual increase (5-10% MoM) | Creep -- most dangerous pattern | Price increases, frequency increases, or scope expansion |
| Sudden drop | Cancelled service or deferred expense | Confirm intentional, check if expense shifted categories |
| Seasonal pattern | Predictable variation | Build into forecast, do not flag as anomaly |

**Rolling Average Method**

Calculate 3-month rolling average for each category. Compare current month to rolling average rather than single prior month. This smooths seasonal variation and provides a more stable baseline.

```
Rolling Average = (Month N + Month N-1 + Month N-2) / 3
Variance = (Current Month - Rolling Average) / Rolling Average * 100
```

### Anomaly Detection Checklist

| Anomaly Type | Detection Method | Common Causes |
|-------------|-----------------|---------------|
| Subscription creep | Compare subscription total to 3 months ago | Free trials converting, price increases, forgotten services |
| Category migration | Transaction moved between categories | Reclassified merchant, new vendor for same need |
| Phantom recurring | Same amount appears monthly, not in subscription list | Auto-renewals, membership dues, installment plans |
| Round-number charges | Exact round amounts on variable expenses | Manual charges, estimated bills, potential fraud |
| Duplicate charges | Same vendor, same amount, close dates | Processing errors, double-billing |
| Price inflation | Same vendor, gradually increasing amounts | Annual price increases, tier upgrades |

---


## Define Done

- [ ] Financial data gathered and categorized accurately
- [ ] Analysis based on actual numbers, not estimates
- [ ] Recommendations account for tax implications and time horizon
- [ ] Action steps are specific and prioritized

## Application

### Monthly Budget Review Template

**Header:** Month, total income, total spending, savings rate

**Section 1: Top-Line Summary**
- Total income vs prior month and 3-month average
- Total spending vs prior month and 3-month average
- Savings rate vs target
- Net cash flow (income - spending)

**Section 2: Category Breakdown**

For each category, report:
- Amount spent
- Budget target
- Variance ($ and %)
- vs 3-month rolling average
- Flag status (green/yellow/orange/red)

**Section 3: Anomalies and Flags**
- List all orange and red flags with investigation notes
- List any new recurring charges detected
- List any subscription price changes

**Section 4: Action Items**
- Specific corrections for overspending categories
- Budget adjustments warranted by trend data
- Subscriptions to cancel or downgrade
- Categories to monitor next month

### Budget vs Actual Comparison Table

| Category | Budget | Actual | Variance $ | Variance % | 3mo Avg | Trend | Flag |
|----------|--------|--------|------------|------------|---------|-------|------|
| Housing | $X | $X | $X | X% | $X | Flat | -- |
| Food | $X | $X | $X | X% | $X | Up | YY |
| Transport | $X | $X | $X | X% | $X | Down | -- |

### Spending Ratio Health Check

| Ratio | Healthy Range | Your Value | Status |
|-------|--------------|------------|--------|
| Fixed / Total Spending | 50-65% | -- | -- |
| Discretionary / Total Spending | 20-35% | -- | -- |
| Savings / Gross Income | 15-25% | -- | -- |
| Debt Payments / Gross Income | < 20% | -- | -- |
| Subscriptions / Discretionary | < 25% | -- | -- |

---

## Quick Reference

### Monthly Review Checklist

- [ ] Export and normalize all transaction data
- [ ] Categorize uncategorized transactions
- [ ] Calculate category totals and compare to budget
- [ ] Calculate 3-month rolling averages
- [ ] Flag categories with >15% variance
- [ ] Check for new recurring charges
- [ ] Check for subscription price changes
- [ ] Compare savings rate to target
- [ ] Identify top 3 action items
- [ ] Update budget targets if structural changes warrant

### Anomaly Quick Scan

- [ ] Any single transaction > 2x average for that vendor?
- [ ] Any category > 30% above rolling average?
- [ ] Any new recurring charges not previously budgeted?
- [ ] Any subscription total increase month-over-month?
- [ ] Any round-number charges on variable expense categories?

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Reviewing only total spending | Hides category shifts (up in one, down in another) | Always review at category level |
| Comparing only to prior month | Misses seasonal patterns, amplifies one-time spikes | Use 3-month rolling average as baseline |
| Setting rigid budgets for variable categories | Creates false failures, discourages tracking | Use ranges (floor-ceiling) for variable categories |
| Ignoring small overages | $20/month x 5 categories = $1,200/year | Aggregate small overages to see cumulative impact |
| Annual subscriptions hidden as "one-time" | Distorts monthly budget, forgotten at renewal | Amortize annual charges monthly, track separately |
| Categorizing everything as "miscellaneous" | No actionable insight | Create specific categories; misc should be < 5% of total |
| Only tracking when "things feel tight" | Misses gradual creep during good months | Review monthly regardless of perceived financial health |
| Budgeting gross income instead of net | Creates phantom surplus, underfunds obligations | Always budget from net (post-tax, post-deduction) income |


## Quality Tests

### Accuracy Test
- All calculations are correct and assumptions are stated
- **PASS:** Numbers are verifiable and assumptions clearly documented
- **FAIL:** Rough estimates presented as precise figures

### Completeness Test
- Analysis considers tax implications and opportunity costs
- **PASS:** Tax impact calculated for each recommendation
- **FAIL:** Pre-tax returns presented without noting tax drag

