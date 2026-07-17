---
last_updated: 2026-04-02
status: active
---

# Buffer Sizing in CCPM

## The Core Problem with Individual Estimates

Every task estimate contains embedded safety. The developer who says "5 days" really means "I can almost certainly finish in 5 days." Their true aggressive estimate might be 2.5 days. That 2.5-day safety margin is invisible, gets consumed by Student Syndrome and Parkinson's Law, and provides no protection to the project because it can't be redistributed.

CCPM makes the safety explicit, removes it from tasks, and aggregates it into a project buffer where it can actually be managed.

---

## The 50% Rule

**Buffer size = 50% of the total safety removed from the chain.**

For each task on the critical chain:
```
safety_removed = safe_duration - aggressive_duration
```

Project buffer:
```
PB = 0.5 × Σ(safety_removed) for all critical chain tasks
```

Feeding buffer for a feeding chain:
```
FB = 0.5 × Σ(safety_removed) for all tasks in that feeding chain
```

### Why 50%?

The 50% factor comes from the statistical aggregation principle. If individual task uncertainties are independent (which they roughly are), the variance of the total path is the sum of individual variances — but the standard deviation (the square root of variance) is less than the sum of individual standard deviations.

For a chain of N tasks each with safety S, the aggregate safety needed is approximately:
```
S × √N  (not S × N)
```

In practice, this works out to roughly 50% of the sum of individual safety margins, which is why the 50% rule is a good approximation.

### The Alternative: Statistical Method (Root Sum of Squares)

A more precise buffer sizing uses:
```
Buffer = √(Σ(safety_removed²)) for critical chain tasks
```

This is more mathematically rigorous but gives similar results in practice. The 50% rule is simpler to explain and defend to stakeholders.

---

## When to Adjust the 50% Factor

The 50% rule is a starting point. Adjust based on context:

### Increase Buffer (toward 60-65% of safety)

| Situation | Reason |
|-----------|--------|
| High novelty — team hasn't done this type of work before | Variance is higher than typical |
| Many external dependencies (vendors, approvals, integrations) | Uncertainty outside your control |
| Aggressive estimates are genuinely uncertain, not just "padded" | Safety estimates are conservative too |
| Regulatory or compliance milestones | Hard stops that can't be compressed |
| Long project (>6 months) | More accumulated uncertainty |

### Decrease Buffer (toward 35-40% of safety)

| Situation | Reason |
|-----------|--------|
| Highly repeating work the team knows well | Variance is low |
| Small team, few handoffs | Less coordination risk |
| Well-defined requirements | Lower scope uncertainty |
| Previous similar projects as reference | Estimates are calibrated |

---

## Sizing Aggressive Estimates

Getting the aggressive estimate right is critical. The buffer only works if the aggressive estimate represents "what you'd expect with focused work and no interruptions" — not "best case" and not "safe case."

**Test:** "If you worked on this task focused, with no interruptions, and everything went as expected, how long would it take?" That's your aggressive estimate.

A useful calibration: for knowledge work, aggressive estimates are typically 40-60% of safe estimates. If your aggressive estimate is 90% of your safe estimate, you haven't actually removed much safety.

### Common Estimate Inflation Patterns

| Pattern | Safe Estimate | True Aggressive |
|---------|--------------|-----------------|
| "I'll need meetings and reviews" | 10 days | 5 days (focused work) |
| "There might be bugs" | 8 days | 4 days (assuming normal discovery) |
| "I haven't done this exact thing before" | 12 days | 7 days (with some learning expected) |
| "Other tasks might interrupt" | 6 days | 3 days (single-focus) |

---

## Buffer Consumption Targets

A healthy project buffer at delivery should show:
- **Under-consumed (<50%):** Project finished with buffer to spare — estimates were calibrated well.
- **Consumed 50-80%:** Normal — the buffer did its job absorbing variability.
- **Consumed >80%:** Close call — review what caused the consumption for future planning.
- **Consumed >100% (project late):** Buffer was undersized or estimates were not truly aggressive.

Tracking buffer consumption at delivery across multiple projects calibrates your 50% factor over time.

---

## Feeding Buffer vs. Project Buffer Priority

When the project buffer is being consumed, investigate whether feeding chains are the cause. A feeding chain with an inadequately sized feeding buffer will start eroding the project buffer at the merge point.

**Rule of thumb:** If a feeding chain has more than 3 tasks and feeds into the middle of the critical chain, give it a dedicated feeding buffer. Don't rely on the project buffer to absorb all feeding chain variation.
