---
last_updated: 2026-02-25
status: active
name: cash-flow-forecasting
description: Project cash flow 30/60/90 days forward, identifying potential shortfalls and surpluses. Use when planning upcoming expenses, evaluating purchase timing, or assessing runway.
triggers:
  files: ["**/finance/**", "**/cashflow/**"]
  keywords: ["cash flow", "forecast", "projection", "runway", "shortfall", "surplus", "liquidity", "30-60-90"]
allowed-tools: Read, Write, Edit
---

# Cash Flow Forecasting

Cash flow forecasting answers the most practical financial question: will I have enough money when I need it? Profitability and net worth are lagging indicators. Cash position is the leading indicator that determines whether you can meet obligations, seize opportunities, or need to take defensive action.

The key insight is that cash flow problems are timing problems. A business can be profitable and still run out of cash if receivables lag payables. An individual can have a healthy net worth and still miss a mortgage payment if assets are illiquid. Forecasting solves this by projecting when cash arrives and when it leaves, revealing gaps before they become crises.

---

## Framework

### Rolling Forecast Windows

| Window | Purpose | Update Frequency | Detail Level |
|--------|---------|-----------------|--------------|
| 30 days | Operational -- meet immediate obligations | Weekly | Transaction-level |
| 60 days | Tactical -- plan larger purchases, timing | Bi-weekly | Category-level |
| 90 days | Strategic -- assess runway, plan investments | Monthly | Aggregate-level |
| 6 months | Horizon -- seasonal planning, major decisions | Quarterly | Estimate-level |

### Income Projection Matrix

| Income Type | Confidence | Projection Method | Example |
|-------------|-----------|-------------------|---------|
| Fixed salary / W-2 | High (95%) | Flat projection from pay schedule | $X every 2 weeks |
| Recurring retainer | High (85%) | Known amount unless cancellation risk | $X/month per client |
| Project-based / milestone | Medium (60-80%) | Stage-weighted: signed > proposed > pipeline | $X at 80% confidence |
| Variable / commission | Medium (50-70%) | 3-month rolling average, seasonally adjusted | Average of last 3 months |
| One-time / sporadic | Low (20-50%) | Include only when confirmed | Tax refund, bonus |
| Passive / investment | Varies | Historical average, adjust for known changes | Dividend schedule |

**Confidence-Weighted Income Calculation:**

```
Projected Income = Sum of (Amount x Confidence %)

Example:
  Salary:    $8,000 x 95% = $7,600
  Retainer:  $3,000 x 85% = $2,550
  Project:   $5,000 x 60% = $3,000
  --------------------------------
  Weighted Total:            $13,150
  Nominal Total:             $16,000
```

Always plan from the weighted total, not the nominal total.

### Expense Projection Matrix

| Expense Type | Projection Method | Accuracy |
|-------------|-------------------|----------|
| Fixed obligations | Exact amount on known date | High |
| Semi-fixed (utilities) | 3-month average + 10% buffer | Medium-High |
| Variable recurring (groceries, fuel) | 3-month average | Medium |
| Quarterly / annual (insurance, taxes) | Known amount, amortized or lump | High (if tracked) |
| Discretionary | Budget target or rolling average | Medium-Low |
| One-time known (planned purchase) | Exact amount on target date | High |
| One-time unknown (emergencies) | Monthly buffer allocation | Low |

### The 30/60/90 Day Forecast Template

**For each period, calculate:**

| Line Item | 30-Day | 60-Day | 90-Day |
|-----------|--------|--------|--------|
| Starting cash balance | $X | Ending balance from 30-day | Ending balance from 60-day |
| (+) Projected income (weighted) | $X | $X | $X |
| (-) Fixed obligations | $X | $X | $X |
| (-) Variable expenses (estimated) | $X | $X | $X |
| (-) Quarterly/annual (if due) | $X | $X | $X |
| (-) Planned one-time expenses | $X | $X | $X |
| (-) Emergency buffer | $X | $X | $X |
| (=) Projected ending balance | $X | $X | $X |
| Minimum balance during period | $X | $X | $X |

**Critical: Track minimum balance, not just ending balance.** A period can end positive but dip negative mid-month if income arrives after expenses are due.

### Scenario Modeling

| Scenario | Income Modifier | Expense Modifier | Use Case |
|----------|----------------|-------------------|----------|
| Best case | 100% of nominal | 90% of projected | Upside planning, investment timing |
| Expected case | Confidence-weighted | 100% of projected | Primary planning baseline |
| Conservative case | 80% of weighted | 110% of projected | Safety planning |
| Worst case | Fixed income only | 110% of projected + emergency | Stress test, runway calculation |

### Cash Position Action Triggers

| Cash Position | Status | Action |
|--------------|--------|--------|
| > 6 months expenses | Strong surplus | Consider investing excess, accelerate goals |
| 3-6 months expenses | Healthy | Maintain current strategy |
| 2-3 months expenses | Adequate | Monitor closely, build buffer |
| 1-2 months expenses | Warning | Reduce discretionary, accelerate receivables |
| < 1 month expenses | Critical | Emergency measures: defer non-essential, liquidate if needed |
| Projected negative | Crisis | Immediate action: bridge financing, payment negotiation |

### Runway Calculation

For self-employed or variable income situations:

```
Runway (months) = Liquid Cash / Monthly Burn Rate

Monthly Burn Rate = Fixed Obligations + Average Variable Expenses

Conservative Runway = Liquid Cash / (Monthly Burn Rate x 1.15)
```

| Runway | Risk Level | Response |
|--------|-----------|----------|
| > 12 months | Low | Invest in growth |
| 6-12 months | Moderate | Comfortable, maintain discipline |
| 3-6 months | Elevated | Prioritize revenue, reduce optional expenses |
| 1-3 months | High | Aggressive cash preservation |
| < 1 month | Critical | Emergency mode |

---


## Define Done

- [ ] Financial data gathered and categorized accurately
- [ ] Analysis based on actual numbers, not estimates
- [ ] Recommendations account for tax implications and time horizon
- [ ] Action steps are specific and prioritized

## Application

### Weekly Cash Flow Check (30-Day Window)

1. Record current liquid cash balance (checking + savings accessible within 2 days)
2. List all known inflows for next 30 days with dates and confidence
3. List all known outflows for next 30 days with dates
4. Plot daily running balance: starting balance + cumulative inflows - cumulative outflows
5. Identify the minimum daily balance in the period
6. If minimum balance < 1 week of expenses, flag for action

### Monthly Forecast Update (60/90-Day Window)

1. Update actual results for completed month
2. Calculate forecast accuracy: (Actual / Forecast) x 100
3. Adjust projection methodology if accuracy < 85%
4. Roll forecast forward one month
5. Update income confidence levels based on new information
6. Add any newly known one-time expenses
7. Recalculate runway

### Forecast Accuracy Tracking

| Month | Projected Income | Actual Income | Accuracy | Projected Expenses | Actual Expenses | Accuracy |
|-------|-----------------|---------------|----------|--------------------|-----------------|----------|
| Jan | $X | $X | X% | $X | $X | X% |
| Feb | $X | $X | X% | $X | $X | X% |
| Mar | $X | $X | X% | $X | $X | X% |

Track accuracy over time to calibrate your projection methodology. If consistently over- or under-estimating, adjust confidence weights.

### Surplus Deployment Decision Tree

When forecast shows surplus:

1. Is emergency fund fully funded (3-6 months)? If no, fund it.
2. Are there high-interest debts (> 6%)? If yes, pay down.
3. Are tax-advantaged accounts maxed? If no, contribute.
4. Is there a known large expense in next 6 months? If yes, set aside.
5. Remaining surplus: invest according to portfolio strategy.

### Shortfall Response Playbook

When forecast shows shortfall:

| Timeframe to Shortfall | Primary Response | Secondary Response |
|-----------------------|------------------|-------------------|
| > 60 days | Adjust spending plan, pursue additional income | Defer non-essential planned purchases |
| 30-60 days | Accelerate receivables, reduce discretionary to minimum | Liquidate non-retirement investments if needed |
| < 30 days | Contact creditors for payment arrangements | Access credit line (last resort, plan repayment) |
| Imminent | Prioritize: housing, utilities, food, insurance, minimum debts | Seek bridge financing |

---

## Quick Reference

### Weekly Forecast Checklist

- [ ] Record current liquid cash balance
- [ ] List expected inflows for next 7-30 days
- [ ] List expected outflows for next 7-30 days
- [ ] Calculate minimum projected balance
- [ ] Flag if minimum < 1 week expenses
- [ ] Note any changes to income confidence

### Monthly Forecast Checklist

- [ ] Compare prior month forecast to actuals
- [ ] Calculate forecast accuracy (income and expense)
- [ ] Update rolling averages for variable categories
- [ ] Adjust confidence weights if needed
- [ ] Roll 30/60/90 day windows forward
- [ ] Update runway calculation
- [ ] Check for upcoming quarterly/annual expenses
- [ ] Review cash position against action triggers

### Key Formulas

| Formula | Calculation |
|---------|-------------|
| Weighted income | Sum of (Amount x Confidence %) |
| Monthly burn rate | Fixed obligations + average variable expenses |
| Runway | Liquid cash / monthly burn rate |
| Conservative runway | Liquid cash / (burn rate x 1.15) |
| Forecast accuracy | (Actual / Forecast) x 100 |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Forecasting only end-of-month balance | Misses mid-month cash dips | Track minimum daily balance through the period |
| Using nominal income instead of weighted | Overestimates available cash, creates false comfort | Always apply confidence weights to variable income |
| Ignoring quarterly/annual lumpy expenses | Creates predictable "surprises" every quarter | Amortize or earmark monthly for known lumpy expenses |
| Not updating forecasts after actuals | Forecast drifts from reality, loses usefulness | Update weekly (30-day) and monthly (60/90-day) |
| Planning surplus before emergency fund is full | One unexpected expense eliminates the surplus | Emergency fund first, then deploy surplus |
| Treating credit availability as cash | Credit is debt, not cash; distorts true position | Forecast from actual cash only; credit is a last-resort response |
| Single-scenario planning | Ignores variability, creates brittle plans | Model at least expected and conservative scenarios |
| Forecasting too far out with high precision | False precision; 6-month forecasts are estimates | Match detail level to confidence: precise at 30 days, approximate at 90+ |


## Quality Tests

### Accuracy Test
- All calculations are correct and assumptions are stated
- **PASS:** Numbers are verifiable and assumptions clearly documented
- **FAIL:** Rough estimates presented as precise figures

### Completeness Test
- Analysis considers tax implications and opportunity costs
- **PASS:** Tax impact calculated for each recommendation
- **FAIL:** Pre-tax returns presented without noting tax drag

