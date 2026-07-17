---
last_updated: 2026-02-25
status: active
name: tax-planning
description: Quarterly and annual tax planning, estimated payment calculation, and proactive strategy. Use when calculating estimated payments, planning year-end tax moves, or structuring income and deductions.
triggers:
  files: ["**/finance/**", "**/tax/**"]
  keywords: ["tax planning", "quarterly", "annual", "estimated payments", "tax strategy", "withholding", "projections"]
allowed-tools: Read, Write, Edit
---

# Tax Planning

Tax planning is not tax preparation. Preparation looks backward at what happened. Planning looks forward at what you can still control. The window for most tax-saving strategies closes on December 31, and some quarterly decisions cannot be reversed. Proactive planning throughout the year -- not a scramble in April -- is what separates efficient tax management from leaving money on the table.

For self-employed individuals and solopreneurs, tax planning is especially critical because there is no employer withholding as a safety net. You are responsible for estimating, setting aside, and paying taxes quarterly. Underpayment triggers penalties. Overpayment means you gave the government an interest-free loan. The goal is accuracy: pay what you owe, when you owe it, and not a dollar more.

---

## Framework

### Quarterly Tax Planning Cycle

| Quarter | Key Dates | Planning Actions |
|---------|-----------|-----------------|
| Q1 (Jan-Mar) | Jan 15: Q4 estimated payment due | Review prior year final numbers, project current year income, set quarterly targets |
| Q2 (Apr-Jun) | Apr 15: Q1 estimated payment + prior year return due | File or extend prior year, compare Q1 actuals to projection, adjust |
| Q3 (Jul-Sep) | Jun 15: Q2 estimated payment due, Sep 15: Q3 payment due | Mid-year review, reassess annual projection, evaluate retirement contributions |
| Q4 (Oct-Dec) | Oct 15: Extension deadline, Jan 15: Q4 payment due | Year-end strategies, accelerate/defer income and deductions, finalize retirement contributions |

### Estimated Payment Calculation

**Step 1: Project Annual Taxable Income**

| Income Source | Annual Projection | Confidence |
|-------------|-------------------|-----------|
| W-2 wages (if any) | $X | High |
| Business net income (Schedule C or S-corp K-1) | $X | Medium |
| Investment income (dividends, interest, capital gains) | $X | Medium-Low |
| Other income (rental, royalties, etc.) | $X | Varies |
| **Total projected gross income** | **$X** | |

**Step 2: Estimate Deductions**

| Deduction | Amount |
|-----------|--------|
| Standard deduction OR itemized total | $X |
| Self-employment tax deduction (50% of SE tax) | $X |
| SEP-IRA / Solo 401(k) contribution | $X |
| HSA contribution | $X |
| Other above-the-line deductions | $X |
| **Total deductions** | **$X** |

**Step 3: Calculate Projected Tax**

| Tax Component | Calculation | Amount |
|--------------|-------------|--------|
| Taxable income | Gross - deductions | $X |
| Federal income tax | Apply tax brackets to taxable income | $X |
| Self-employment tax | Net SE income x 0.9235 x 15.3% (up to SS limit) + 2.9% above | $X |
| Net investment income tax | 3.8% on investment income above threshold | $X |
| State income tax | Apply state rates | $X |
| **Total projected tax liability** | | **$X** |

**Step 4: Determine Quarterly Payments**

| Method | Calculation | When to Use |
|--------|-------------|-------------|
| Current year 90% | (Projected total tax x 90%) / 4 | Income is stable and predictable |
| Prior year 100% safe harbor | Prior year total tax / 4 | Income varies significantly |
| Prior year 110% safe harbor | Prior year total tax x 110% / 4 | AGI > $150k and income varies |
| Annualized income installment | Actual income through period, annualized | Income is heavily seasonal |

### Safe Harbor Rules

| Situation | Safe Harbor Threshold | Penalty Avoidance |
|-----------|----------------------|-------------------|
| AGI <= $150K ($75K MFS) | Pay 100% of prior year tax OR 90% of current year | No underpayment penalty |
| AGI > $150K ($75K MFS) | Pay 110% of prior year tax OR 90% of current year | No underpayment penalty |
| W-2 employee | Withholding covers 90% of current or 100%/110% of prior | Withholding treated as paid evenly |

Note: Safe harbor protects from underpayment penalties only. You still owe the full tax amount by the filing deadline.

### Income Timing Strategies

| Strategy | How It Works | When to Use |
|----------|-------------|-------------|
| Defer income | Delay invoicing or contract signing to January | Current year income is high, next year expected lower |
| Accelerate income | Invoice early, collect before Dec 31 | Current year income is low, next year expected higher |
| Roth conversion | Convert Traditional IRA to Roth in low-income year | Current year tax bracket is unusually low |
| Capital gain harvesting | Sell appreciated assets in low-income year at 0% rate | Taxable income below LTCG 0% threshold |
| Capital loss harvesting | Sell losing investments to offset gains | Have realized gains to offset |

**Income Timing Decision Matrix:**

| This Year's Income vs Normal | Next Year's Expected Income | Action |
|-----------------------------|----------------------------|--------|
| Higher | Lower or similar | Defer income if possible, accelerate deductions |
| Lower | Higher | Accelerate income, consider Roth conversion, defer deductions |
| Similar | Similar | Optimize within current year, no timing games |
| Uncertain | Uncertain | Default to safe harbor, maintain flexibility |

### Deduction Timing Strategies

| Strategy | How It Works | When to Use |
|----------|-------------|-------------|
| Accelerate deductions | Prepay deductible expenses in December | High income year, want to reduce taxable income |
| Bunch deductions | Concentrate 2 years of deductions into 1 year | Alternate between standard and itemized |
| Defer deductions | Delay deductible expenses to January | Low income year, deductions more valuable later |
| Maximize retirement contributions | Max out SEP-IRA, Solo 401(k), or defined benefit plan | Reduce taxable income significantly |

### S-Corp Tax Considerations

| Factor | Impact | Planning Consideration |
|--------|--------|----------------------|
| Reasonable salary | Subject to FICA (15.3% up to SS limit + 2.9% above) | Set at defensible market rate |
| Distributions above salary | No FICA, only income tax | Maximize within reasonable compensation rules |
| Salary/distribution ratio | Audit target if salary is too low | Document comparable salary research |
| Payroll timing | W-2 withholding treated as paid evenly across year | Can adjust Q4 withholding to cover annual shortfall |
| Retirement plan contributions | Based on W-2 salary amount | Higher salary = higher retirement contribution limit |

### Retirement Contribution Strategy

| Account Type | Contribution Limit (check annually) | Tax Benefit | Deadline |
|-------------|-------------------------------------|------------|----------|
| Traditional 401(k) / Solo 401(k) employee | Check current year limit | Reduces current year taxable income | Dec 31 |
| Solo 401(k) employer | Up to 25% of net SE income | Reduces current year taxable income | Tax filing deadline (with extensions) |
| SEP-IRA | Up to 25% of net SE income | Reduces current year taxable income | Tax filing deadline (with extensions) |
| Traditional IRA | Check current year limit | Deductible if income below threshold | Apr 15 (no extension) |
| Roth IRA | Check current year limit | No current deduction; tax-free growth | Apr 15 (no extension) |
| HSA | Check current year limit | Triple tax advantage | Apr 15 (no extension) |

**Priority order for contributions (self-employed):**

1. HSA (if eligible) -- triple tax advantage is unmatched
2. Solo 401(k) or SEP-IRA employee portion -- largest immediate tax reduction
3. Solo 401(k) employer portion -- additional tax-deferred space
4. Roth IRA (if eligible) or backdoor Roth -- tax-free growth
5. Taxable brokerage -- no contribution limits, flexible

---


## Define Done

- [ ] Financial data gathered and categorized accurately
- [ ] Analysis based on actual numbers, not estimates
- [ ] Recommendations account for tax implications and time horizon
- [ ] Action steps are specific and prioritized

## Application

### Quarterly Tax Review Template

**Quarter: Q___ | Year: ____**

**Income Review:**
- Year-to-date actual income: $___
- Annualized projection: $___
- Change from last quarter's projection: ___%
- Confidence in annual projection: High / Medium / Low

**Estimated Payments:**
- Payments made YTD: $___
- Remaining payments due: $___
- Safe harbor target (annual): $___
- On track for safe harbor? Yes / No
- Adjustment needed for next payment: $___

**Strategy Review:**
- Are there income timing opportunities? (defer/accelerate)
- Are there deduction timing opportunities?
- Retirement contribution status vs annual target
- Any capital gain/loss harvesting opportunities?

**Action Items:**
1. [Specific action with deadline]
2. [Specific action with deadline]
3. [Specific action with deadline]

### Year-End Tax Checklist (October - December)

**Income Management:**
- [ ] Project final annual income within +/- 10%
- [ ] Evaluate income deferral opportunities (delay invoicing?)
- [ ] Evaluate income acceleration opportunities (collect early?)
- [ ] Review S-corp salary vs distribution ratio if applicable

**Deduction Optimization:**
- [ ] Review itemized vs standard deduction (bunch if beneficial)
- [ ] Prepay any deductible expenses if accelerating
- [ ] Make charitable contributions (cash or appreciated stock)
- [ ] Review business expenses for anything deductible before year-end

**Retirement Contributions:**
- [ ] Maximize Solo 401(k) employee contributions by Dec 31
- [ ] Calculate employer contribution amount
- [ ] Fund HSA to annual maximum
- [ ] Evaluate Roth conversion opportunity

**Investment Tax Management:**
- [ ] Harvest tax losses to offset realized gains
- [ ] Review capital gains distributions from mutual funds
- [ ] Evaluate holding period (short-term vs long-term) before selling
- [ ] Consider charitable donation of appreciated stock

**Final Payment:**
- [ ] Calculate Q4 estimated payment (due Jan 15)
- [ ] Adjust S-corp payroll withholding if needed to cover shortfall
- [ ] Verify safe harbor is met for the year

---

## Quick Reference

### Federal Estimated Payment Due Dates

| Payment | Period Covered | Due Date |
|---------|---------------|----------|
| Q1 | Jan 1 - Mar 31 | Apr 15 |
| Q2 | Apr 1 - May 31 | Jun 15 |
| Q3 | Jun 1 - Aug 31 | Sep 15 |
| Q4 | Sep 1 - Dec 31 | Jan 15 (following year) |

### Safe Harbor Quick Test

1. Calculate prior year total tax (line from prior return)
2. If AGI > $150K: multiply by 110%. Otherwise: use 100%.
3. Divide by 4.
4. Pay at least that amount each quarter.
5. You are protected from underpayment penalties.

### Self-Employment Tax Quick Estimate

```
Net SE income x 0.9235 = SE tax base
First $X (SS wage base - check annually) x 15.3% = SS + Medicare
Amount above SS wage base x 2.9% = Medicare only
Additional 0.9% Medicare on earnings above $200K ($250K MFJ)
Total SE tax = sum of above
Deduction = 50% of total SE tax (above-the-line)
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Ignoring taxes until April | Most strategies expire Dec 31, penalties accrue | Plan quarterly, review monthly in Q4 |
| Paying "whatever last year was" without projecting | Overpays in lower-income years, underpays in higher | Project current year income quarterly, adjust payments |
| Minimizing S-corp salary to avoid FICA | IRS audit risk, penalties for unreasonable compensation | Set salary at defensible market rate, document rationale |
| Not tracking estimated payments across accounts | Confusion, potential underpayment | Maintain a single tracking sheet for all tax payments |
| Waiting until Dec to make retirement contributions | Cash flow crunch, may miss deadlines | Contribute throughout the year, quarterly at minimum |
| Deferring income without considering next year | May push into higher bracket next year | Model both years before deciding to defer |
| Ignoring state estimated payment requirements | Many states have separate estimated payment rules | Track federal and state payments separately |
| Conflating tax refund with good planning | Large refund = interest-free loan to government | Target refund of $0-500; accuracy is the goal |
| Making investment decisions solely for tax reasons | Tax tail wagging the investment dog | Tax efficiency is a factor, not the primary driver |


## Quality Tests

### Accuracy Test
- All calculations are correct and assumptions are stated
- **PASS:** Numbers are verifiable and assumptions clearly documented
- **FAIL:** Rough estimates presented as precise figures

### Completeness Test
- Analysis considers tax implications and opportunity costs
- **PASS:** Tax impact calculated for each recommendation
- **FAIL:** Pre-tax returns presented without noting tax drag

