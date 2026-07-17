---
last_updated: 2026-02-25
status: active
name: statistical-analysis
description: Apply statistical methods to quantitative research data. Calculate confidence intervals, run hypothesis tests, determine effect sizes. Use when analyzing survey results, A/B tests, or behavioral metrics requiring statistical rigor.
triggers:
  keywords: ["statistical", "analysis", "apply", "methods", "quantitative", "research", "data", "calculate", "confidence", "intervals"]
allowed-tools: Read, Write, Edit
---

# Statistical Analysis

## Overview

Apply appropriate statistical methods to research data to draw defensible conclusions. Covers hypothesis testing, confidence intervals, effect sizes, and common pitfalls. Focus on practical application for product and research decisions.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Understand Your Data Type

Choose analysis method based on data characteristics:

| Data Type | Description | Example | Common Tests |
|-----------|-------------|---------|--------------|
| **Continuous** | Measured on scale | Time on site, revenue | t-test, ANOVA |
| **Categorical** | Discrete categories | Plan type, device | Chi-square |
| **Binary** | Yes/No outcomes | Converted, churned | Proportion tests |
| **Count** | Number of events | Clicks, errors | Poisson |
| **Ordinal** | Ranked categories | NPS score, rating | Mann-Whitney |

### Step 2: State Hypotheses Clearly

Before analyzing, define what you're testing:

```markdown
## Hypothesis Statement

**Research question:** Does the new checkout flow improve conversion?

**Null hypothesis (H0):** No difference in conversion between flows
**Alternative hypothesis (H1):** New flow has higher conversion than control

**Test type:** Two-proportion z-test (one-tailed)
**Significance level:** α = 0.05
**Minimum detectable effect:** 5% relative improvement
```

### Step 3: Check Assumptions

Each test has requirements:

| Test | Key Assumptions | How to Check |
|------|-----------------|--------------|
| **t-test** | Normal distribution, equal variance | Q-Q plot, Levene's test |
| **Chi-square** | Expected counts > 5 | Check expected values |
| **ANOVA** | Normality, homogeneity | Residual plots |
| **Regression** | Linearity, independence, normality | Residual diagnostics |

```markdown
## Assumption Checks

### Normality
- Visual: [Q-Q plot assessment]
- Test: Shapiro-Wilk p = [value]
- Verdict: [Pass/Fail/Approximately normal]

### Equal Variance
- Visual: [Box plot assessment]
- Test: Levene's test p = [value]
- Verdict: [Pass/Fail]

### Sample Independence
- [How data was collected]
- [Confirm observations are independent]
```

### Step 4: Calculate Sample Size Requirements

Determine if you have enough data:

| Parameter | What It Means |
|-----------|---------------|
| **Effect size** | Minimum difference worth detecting |
| **Power (1-β)** | Probability of detecting true effect (typically 0.80) |
| **Significance (α)** | False positive rate (typically 0.05) |
| **Sample size (n)** | Number of observations needed |

```markdown
## Sample Size Calculation

**Parameters:**
- Baseline conversion: 10%
- Minimum detectable effect: 20% relative (10% → 12%)
- Power: 80%
- Significance: 5%

**Required sample size per group:** ~3,800
**Current sample size:** [n]
**Sufficient:** [Yes/No]
```

### Step 5: Run the Appropriate Test

Match test to question:

| Question Type | Recommended Test |
|---------------|------------------|
| Compare two means | Independent t-test |
| Compare two proportions | Two-proportion z-test |
| Compare >2 groups | ANOVA |
| Test association | Chi-square test |
| Predict continuous outcome | Linear regression |
| Predict binary outcome | Logistic regression |
| Before/after same group | Paired t-test |

### Step 6: Report Results Properly

Include all relevant statistics:

```markdown
## Results

### Descriptive Statistics
| Group | n | Mean | SD | 95% CI |
|-------|---|------|----|---------|
| Control | 5,000 | 10.2% | — | [9.4%, 11.0%] |
| Treatment | 5,200 | 12.1% | — | [11.2%, 13.0%] |

### Test Results
- Test: Two-proportion z-test
- z-statistic: 2.87
- p-value: 0.002 (one-tailed)
- Effect size: 1.9 percentage points (18.6% relative improvement)
- 95% CI for difference: [0.7%, 3.1%]

### Interpretation
The treatment group showed a statistically significant improvement in
conversion (12.1% vs 10.2%, p = 0.002). The effect size represents an
18.6% relative improvement, with 95% confidence the true difference is
between 0.7 and 3.1 percentage points.
```

### Step 7: Assess Practical Significance

Statistical significance ≠ practical importance:

| Question | Assessment |
|----------|------------|
| Is effect large enough to matter? | [Business threshold] |
| Is confidence interval actionable? | [Range acceptable?] |
| What's the ROI of acting on this? | [Cost vs benefit] |
| Could we be wrong? | [Type I/II risk] |

```markdown
## Practical Significance Assessment

### Business Impact
- Effect size: 1.9pp conversion improvement
- At 100,000 monthly visitors: ~1,900 additional conversions
- At $50 average value: ~$95,000/month revenue impact

### Decision Confidence
- Statistical confidence: 95%
- Lower bound of CI (0.7pp): Still worth $33,000/month
- Recommend: Ship the change

### Caveats
- Effect may diminish over time (novelty)
- Different segments may respond differently
- Monitor post-launch to confirm
```

## Examples

**Output: A/B Test Analysis Report**

```markdown
# A/B Test Analysis: Simplified Checkout Flow

## Test Setup
| Parameter | Value |
|-----------|-------|
| Test duration | 14 days |
| Traffic split | 50/50 |
| Primary metric | Checkout completion rate |
| Significance level | 5% (two-tailed) |
| Power | 80% |
| MDE | 10% relative improvement |

## Sample Size
- Required per group: 3,800
- Actual Control: 4,127
- Actual Treatment: 4,089
- **Sufficient: Yes**

## Results Summary

### Primary Metric: Checkout Completion
| Variant | n | Conversions | Rate | 95% CI |
|---------|---|-------------|------|--------|
| Control | 4,127 | 412 | 9.98% | [9.07%, 10.90%] |
| Treatment | 4,089 | 489 | 11.96% | [10.96%, 12.96%] |
| **Difference** | — | +77 | +1.98pp | [0.61%, 3.35%] |

### Statistical Test
- Test type: Two-proportion z-test
- z-statistic: 2.84
- p-value: 0.0045
- **Result: Statistically significant at α = 0.05**

### Effect Size
- Absolute: +1.98 percentage points
- Relative: +19.8% improvement
- 95% CI: [6.1%, 33.6%] relative

## Secondary Metrics

### Revenue per Visitor
| Variant | Mean | Median | p-value |
|---------|------|--------|---------|
| Control | $4.52 | $0 | — |
| Treatment | $5.31 | $0 | 0.023 |

### Average Order Value (converters only)
| Variant | Mean | Median | p-value |
|---------|------|--------|---------|
| Control | $45.29 | $38.00 | — |
| Treatment | $44.41 | $37.50 | 0.412 |

**Note:** Conversion improvement drives revenue lift; AOV unchanged.

## Segment Analysis

| Segment | Control Rate | Treatment Rate | Significant? |
|---------|--------------|----------------|--------------|
| Mobile | 7.2% | 10.1% | Yes (p=0.008) |
| Desktop | 12.8% | 13.9% | No (p=0.32) |
| New users | 6.4% | 8.9% | Yes (p=0.011) |
| Returning | 14.2% | 15.8% | No (p=0.24) |

**Finding:** Effect driven primarily by mobile and new users.

## Assumption Checks
- Sample independence: ✓ Users randomly assigned
- Sample size: ✓ Exceeded requirement
- Test duration: ✓ Covered full week cycles

## Practical Significance

### Business Impact (monthly projection)
| Metric | Calculation | Value |
|--------|-------------|-------|
| Monthly visitors | 100,000 | — |
| Additional conversions | 100,000 × 1.98% | 1,980 |
| Revenue per conversion | $45 | — |
| **Monthly revenue lift** | 1,980 × $45 | **$89,100** |

### Lower-bound scenario (CI lower limit)
- Conservative conversion lift: 0.61pp
- Minimum monthly revenue impact: ~$27,500

## Recommendation

**Ship the treatment.** Results show:
1. Statistically significant improvement (p < 0.01)
2. Practically significant revenue impact ($89K/month)
3. No regression in secondary metrics
4. Strongest gains in key growth segments (mobile, new users)

**Post-launch monitoring:**
- Watch for effect decay over 4-6 weeks
- Segment-specific dashboards for mobile/desktop
- Alert if conversion drops below control baseline
```



## Quality Tests

### Evidence Test
- Every finding cites specific data, quotes, or observations
- **PASS:** Each insight traces back to a named source or data point
- **FAIL:** Findings use vague language like 'it seems' or 'generally' without evidence

### Completeness Test
- All relevant dimensions of the framework have been considered
- **PASS:** Analysis addresses each framework dimension, noting gaps where data is unavailable
- **FAIL:** Key dimensions skipped without acknowledgment

### Actionability Test
- Recommendations are specific enough to act on immediately
- **PASS:** Each recommendation names who should do what by when
- **FAIL:** Recommendations are vague ('improve communication') without concrete actions

## Guidelines

1. **Set hypotheses before looking at data** — Prevents p-hacking
2. **Report confidence intervals, not just p-values** — Shows effect magnitude
3. **Check and document assumptions** — Invalid tests = invalid conclusions
4. **Distinguish statistical from practical significance** — Small p ≠ big effect
5. **Use appropriate corrections** — Multiple comparisons need adjustment
6. **State limitations** — What could make your conclusion wrong

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| P-hacking | Testing until significant | Pre-register analysis plan |
| Peeking | Stopping test early when significant | Fixed sample size or sequential methods |
| Multiple comparisons | Inflated false positive rate | Bonferroni/Holm correction |
| Underpowered tests | Missing real effects | Calculate sample size upfront |
| Ignoring effect size | Tiny effects appear "significant" | Always report effect magnitude |
| No confidence intervals | Can't assess precision | Report CIs for all estimates |

## Common Test Reference

| Scenario | Test | Key Output |
|----------|------|------------|
| Two group means | t-test | t, df, p, Cohen's d |
| Two proportions | z-test | z, p, risk difference |
| >2 group means | ANOVA | F, df, p, η² |
| Categorical association | Chi-square | χ², df, p, Cramér's V |
| Correlation | Pearson/Spearman | r, p |
| Prediction | Regression | β, SE, p, R² |

## References

- pattern-recognition: Identifying patterns for hypothesis generation
- research-design: Study design considerations
- data-visualization: Presenting statistical results
