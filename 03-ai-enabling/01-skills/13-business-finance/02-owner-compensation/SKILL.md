---
last_updated: 2026-02-25
status: active
name: owner-compensation
description: Optimize S-corp owner salary/distribution split, reasonable compensation, and tax efficiency. Use when setting or adjusting owner pay, evaluating S-corp salary, or planning distributions.
triggers:
  files: ["**/finance/**", "**/compensation/**", "**/s-corp/**"]
  keywords: ["owner compensation", "S-corp", "salary", "distribution", "reasonable compensation", "payroll", "self-employment tax"]
allowed-tools: Read, Write, Edit
---

# Owner Compensation

S-corp owner compensation is one of the most impactful tax optimization levers available to small business owners. The fundamental mechanism is straightforward: salary is subject to payroll taxes (FICA -- Social Security and Medicare), while distributions above salary are subject only to income tax. The tax savings from a well-structured salary/distribution split can be $10,000-$30,000+ annually for profitable businesses.

However, this lever comes with a critical constraint: the IRS requires S-corp owner-employees to pay themselves "reasonable compensation" before taking distributions. Setting salary too low invites audit and penalties. Setting salary too high wastes the tax advantage. The goal is to find the defensible sweet spot -- a salary that is reasonable by market standards and supported by documentation, with the remaining profit taken as distributions.

---

## Framework

### The S-Corp Compensation Structure

| Component | Subject To | Tax Rate (approximate) |
|-----------|-----------|----------------------|
| Salary (W-2) | Federal income tax + FICA (employer + employee) | Income tax rate + 15.3% FICA (up to SS wage base) + 2.9% Medicare above |
| Distributions (K-1) | Federal income tax only | Income tax rate only |
| **Savings from distributions** | **Avoids FICA on distributed amount** | **Up to 15.3% on amount up to SS wage base** |

**Example Tax Impact:**

| Scenario | Net Profit: $150K | Salary | Distribution | FICA on Salary | Tax Savings vs All-Salary |
|----------|-------------------|--------|-------------|----------------|---------------------------|
| All salary | $150,000 | $150,000 | $0 | ~$18,000 | Baseline |
| 60/40 split | $150,000 | $90,000 | $60,000 | ~$12,600 | ~$5,400 |
| 50/50 split | $150,000 | $75,000 | $75,000 | ~$10,200 | ~$7,800 |

Note: Actual savings depend on whether salary is above or below the Social Security wage base and current tax rates. These are illustrative.

### Reasonable Compensation Analysis

The IRS does not define a specific salary-to-distribution ratio. Instead, it requires "reasonable compensation for services actually rendered." Multiple factors determine what is reasonable.

**IRS Reasonable Compensation Factors:**

| Factor | Description | How to Evaluate |
|--------|-----------|----------------|
| Training and experience | Education, certifications, years in field | Compare to job listings for similar credentials |
| Duties and responsibilities | What the owner actually does | Document all roles performed |
| Time and effort devoted | Hours worked in the business | Track hours, compare to industry norms |
| Comparable salaries | What similar positions pay in the market | Research salary databases |
| Dividend history | Pattern of distributions vs salary | Ensure salary is not artificially suppressed |
| Company agreements | Employment contracts, shareholder agreements | Document compensation decisions |
| Use of corporate facilities | How much of the business value comes from the owner | Distinguish owner contribution from business systems |
| General economic conditions | Market rates in current economy | Adjust for local market |
| Revenue of the business | What the business earns overall | Salary should be proportional to business success |

### Industry Benchmark Methodology

**Step 1: Identify comparable roles**

The S-corp owner typically fills multiple roles. Identify all of them:

| Role | % of Time | Market Salary Range |
|------|-----------|-------------------|
| Primary service delivery (e.g., consultant, designer) | X% | $X - $X |
| Business development / sales | X% | $X - $X |
| General management / operations | X% | $X - $X |
| Administrative / bookkeeping | X% | $X - $X |

**Step 2: Calculate weighted reasonable compensation**

```
Reasonable Salary = Sum of (Market Salary for Role x % of Time in Role)

Example:
  Senior Consultant (60% of time):    $120K x 0.60 = $72,000
  Business Development (20% of time): $90K x 0.20 = $18,000
  Management (15% of time):           $80K x 0.15 = $12,000
  Admin (5% of time):                 $50K x 0.05 = $2,500
  -----------------------------------------------
  Weighted Reasonable Salary:                      = $104,500
```

**Step 3: Adjust for factors**

| Adjustment | Direction | When to Apply |
|-----------|-----------|---------------|
| Small market / low cost of living | Reduce 10-20% | Business is in a lower-cost market |
| High demand specialty | Increase 10-20% | Skills are scarce, premium in market |
| Part-time effort | Pro-rate | Owner works less than full time |
| Business revenue is modest | Reduce | Salary should not exceed what the business can sustain |
| Business is highly profitable | May increase | IRS expects higher salary when business is very profitable |

**Step 4: Validate against revenue-based guidelines**

| Business Net Profit | Suggested Salary Range | Distribution Range |
|--------------------|----------------------|-------------------|
| < $50K | 80-100% as salary | 0-20% as distribution |
| $50K - $100K | 60-80% as salary | 20-40% as distribution |
| $100K - $200K | 50-70% as salary | 30-50% as distribution |
| $200K - $400K | 40-60% as salary | 40-60% as distribution |
| > $400K | 35-50% as salary | 50-65% as distribution |

Note: These are guidelines, not rules. The actual determination depends on the reasonable compensation analysis, not a formula.

### Salary/Distribution Optimization Process

**Constraints:**

1. Salary must meet "reasonable compensation" standard
2. Salary cannot exceed business net income (cannot create a loss with salary alone)
3. Distributions cannot exceed accumulated earnings and profits
4. Owner must actually receive the salary through payroll (with withholding)
5. Retirement contributions (Solo 401k employer match) are based on W-2 salary

**Optimization Steps:**

1. Calculate reasonable compensation (benchmark methodology above)
2. Calculate FICA savings at different salary levels
3. Calculate retirement contribution impact at different salary levels
4. Factor in state-specific considerations (some states tax S-corp income differently)
5. Choose salary that balances tax savings with audit defensibility

**Retirement Contribution Trade-Off:**

| Higher Salary Means | Lower Salary Means |
|--------------------|--------------------|
| More FICA tax paid | Less FICA tax paid |
| Higher Solo 401(k) employer contribution limit | Lower Solo 401(k) employer contribution limit |
| More Social Security credits | Fewer Social Security credits |
| More defensible against IRS | Higher audit risk |

```
Solo 401(k) employer contribution = W-2 salary x 25%

At $80K salary: employer contribution up to $20,000
At $120K salary: employer contribution up to $30,000
Difference: $10,000 additional tax-deferred savings
```

Sometimes a higher salary is worth the extra FICA because the additional retirement contribution more than offsets it.

### Quarterly Salary Adjustment Framework

| Trigger | Assessment | Action |
|---------|-----------|--------|
| Revenue increased > 20% YoY | Higher revenue may warrant higher salary | Re-run reasonable compensation analysis |
| Revenue decreased > 20% YoY | Business may not support current salary | Reduce salary to match business reality |
| New significant client | Revenue composition changed | Evaluate if roles/time allocation shifted |
| Lost major client | Revenue dropped materially | May need to reduce salary to maintain solvency |
| Added employees | Owner's role may have changed | Re-assess which roles owner still fills |
| Industry salary survey update | Market rates may have changed | Compare current salary to updated benchmarks |

### Documentation Requirements

**Maintain a reasonable compensation file with:**

| Document | Purpose | Update Frequency |
|----------|---------|-----------------|
| Role description | Documents what the owner does | Annually or when roles change |
| Time allocation log | Proves how time is spent | Quarterly summary |
| Salary survey data | Market comparables | Annually |
| Compensation calculation worksheet | Shows how salary was determined | Annually |
| Board resolution or meeting minutes | Documents the decision formally | Annually or when salary changes |
| Industry benchmarks | Third-party validation | Annually |

---


## Define Done

- [ ] Financial data gathered and categorized accurately
- [ ] Analysis based on actual numbers, not estimates
- [ ] Recommendations account for tax implications and time horizon
- [ ] Action steps are specific and prioritized

## Application

### Annual Compensation Setting Template

**Business Information:**
- Business name: ___
- Tax year: ___
- Projected net profit before owner compensation: $___
- Number of employees (besides owner): ___

**Owner Role Analysis:**

| Role | % of Time | Market Rate (annual) | Weighted Value |
|------|-----------|---------------------|---------------|
| [Primary role] | __% | $____ | $____ |
| [Secondary role] | __% | $____ | $____ |
| [Additional role] | __% | $____ | $____ |
| **Total** | **100%** | | **$____** |

**Adjustments:**
- Market adjustment (geography, specialization): +/- ___%
- Part-time adjustment (if applicable): ___%
- Revenue-based reasonableness check: $____

**Final Salary Determination:**
- Calculated reasonable salary: $____
- Rounded salary (for payroll): $____
- Projected distributions: $____
- FICA savings vs all-salary: $____
- Retirement contribution at this salary: $____

**Documentation filed:**
- [ ] Written role description
- [ ] Salary survey printouts or screenshots
- [ ] Compensation calculation worksheet
- [ ] Board resolution documenting salary decision
- [ ] Prior year comparison

### Salary vs Distribution Decision Worksheet

| Line | Item | Amount |
|------|------|--------|
| A | Projected annual net business income | $____ |
| B | Calculated reasonable compensation | $____ |
| C | Salary set at (B or adjusted) | $____ |
| D | FICA on salary (C x 15.3% up to SS base + 2.9% above) | $____ |
| E | Distribution (A - C) | $____ |
| F | FICA saved on distributions (vs if E were salary) | $____ |
| G | Solo 401(k) employer contribution (C x 25%) | $____ |
| H | Tax on retirement contribution deferred | $____ |
| I | Net tax benefit of S-corp structure (F + H) | $____ |

### When S-Corp Compensation Stops Making Sense

| Situation | Issue | Alternative |
|-----------|-------|-------------|
| Net profit < $40K | FICA savings do not justify payroll costs + complexity | Sole proprietorship may be simpler |
| Owner fills no operational role | Hard to justify salary for passive ownership | May need different entity structure |
| Multiple owners with different roles | Compensation disagreements, complex allocation | Clear operating agreement with defined comp methodology |
| Highly variable income | Setting fixed salary is difficult | Use quarterly adjustments, lower base + variable bonus |
| State taxes unfavorable | Some states tax S-corp income at entity level | Evaluate state-specific treatment |

---

## Quick Reference

### Reasonable Compensation Quick Test

Answer these questions to sanity-check your salary:

| Question | If Yes | If No |
|----------|--------|-------|
| Would you pay someone this salary to do what you do? | Salary may be reasonable | Salary is likely too low |
| Could you hire a replacement at this salary? | Salary is in range | Salary may be too low |
| Is your salary less than 40% of net profit on a $200K+ business? | Re-examine -- may be too aggressive | Likely in reasonable range |
| Have you documented how you arrived at this number? | Protected | Vulnerable in audit |
| Is your salary the same as 10 years ago despite revenue growth? | Red flag -- update | Reasonable if business has not grown |

### Annual Compensation Checklist

- [ ] Project annual net business income
- [ ] Identify all roles performed with time allocation
- [ ] Research current market rates for each role
- [ ] Calculate weighted reasonable compensation
- [ ] Apply market and circumstance adjustments
- [ ] Evaluate FICA savings at chosen salary level
- [ ] Evaluate retirement contribution impact
- [ ] Document decision with salary surveys and board resolution
- [ ] Set up or adjust payroll for new salary amount
- [ ] File documentation in reasonable compensation file

### Key Numbers to Know

| Item | Where to Find | Why It Matters |
|------|--------------|---------------|
| Social Security wage base (current year) | SSA.gov, updated annually | FICA rate changes above this threshold |
| Solo 401(k) employee contribution limit | IRS.gov, updated annually | Max tax-deferred savings from salary |
| Solo 401(k) total contribution limit | IRS.gov, updated annually | Employee + employer combined limit |
| Self-employment tax rate | 15.3% (12.4% SS + 2.9% Medicare) | The tax you are saving on distributions |
| Additional Medicare tax threshold | $200K single / $250K MFJ | Extra 0.9% Medicare above this |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Setting salary at minimum wage | Clearly unreasonable for a business owner providing skilled services | Use market-based reasonable compensation analysis |
| Taking 100% as distributions, 0% as salary | IRS explicitly targets this; guaranteed audit adjustment | Pay reasonable salary through payroll |
| Using the same salary for years regardless of business growth | Suggests salary is not based on actual business performance | Review and adjust annually |
| Not running payroll (just writing checks) | Salary must go through payroll with proper withholding | Use a payroll service, even for single-owner S-corps |
| Setting salary based solely on a percentage rule | IRS does not recognize percentage formulas; requires actual analysis | Conduct role-based market analysis |
| Ignoring retirement contribution trade-off | May lose more in retirement contribution limits than saved in FICA | Model the complete picture: FICA savings vs retirement opportunity |
| No documentation | Cannot defend salary level if audited | Maintain reasonable compensation file with annual documentation |
| Paying irregular salary amounts | Suggests distributions disguised as salary | Pay consistent salary on regular payroll schedule |
| Comparing to unrelated industries | IRS compares to similar roles in similar industries | Use industry-specific salary data |
| Forgetting Social Security benefit impact | Very low salary reduces future Social Security benefits | Factor in long-term Social Security impact for career planning |


## Quality Tests

### Accuracy Test
- All calculations are correct and assumptions are stated
- **PASS:** Numbers are verifiable and assumptions clearly documented
- **FAIL:** Rough estimates presented as precise figures

### Completeness Test
- Analysis considers tax implications and opportunity costs
- **PASS:** Tax impact calculated for each recommendation
- **FAIL:** Pre-tax returns presented without noting tax drag

