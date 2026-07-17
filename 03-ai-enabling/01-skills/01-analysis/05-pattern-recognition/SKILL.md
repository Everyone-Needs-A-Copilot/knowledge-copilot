---
last_updated: 2026-02-25
status: active
name: pattern-recognition
description: Identify patterns, trends, and anomalies across data sources through systematic triangulation. Distinguishes signal from noise, convergence from coincidence. Use when analyzing multiple data sources to find defensible insights.
triggers:
  keywords: ["pattern", "recognition", "identify", "patterns", "trends", "anomalies", "across", "data", "sources", "systematic"]
allowed-tools: Read, Write, Edit
---

# Pattern Recognition

## Overview

Systematically identify meaningful patterns across disparate data sources. Combines multiple evidence types (qualitative, quantitative, behavioral) to find convergent signals. Distinguishes true patterns from noise through triangulation.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Inventory Data Sources

Map what evidence you have available:

| Source Type | Examples | What It Shows |
|-------------|----------|---------------|
| **Qualitative** | Interviews, surveys, support tickets | What people say |
| **Quantitative** | Analytics, metrics, A/B tests | What people do |
| **Behavioral** | Session recordings, heatmaps | How people behave |
| **Contextual** | Market data, competitor info | External factors |

```markdown
## Data Inventory
| Source | Type | Sample Size | Time Period | Confidence |
|--------|------|-------------|-------------|------------|
| User interviews | Qualitative | n=12 | March 2024 | High |
| Product analytics | Quantitative | n=50,000 | Q1 2024 | High |
| Support tickets | Qualitative | n=847 | Q1 2024 | Medium |
| Competitor analysis | Contextual | n=5 | Current | Medium |
```

### Step 2: Define Pattern Types

Know what you're looking for:

| Pattern Type | Definition | Example |
|--------------|------------|---------|
| **Trend** | Directional change over time | Usage increasing 10% MoM |
| **Cluster** | Elements that co-occur | Feature A users also use Feature B |
| **Sequence** | Common order of events | Search → Compare → Purchase |
| **Correlation** | Variables that move together | Higher engagement = lower churn |
| **Anomaly** | Deviation from expected | Spike in errors on Mondays |
| **Segment** | Distinct subgroups | Power users vs casual users |

### Step 3: Scan Each Source

Analyze each data source independently first:

```markdown
## Source Analysis: [Source Name]

### Key Observations
1. [Observation]: [Evidence]
2. [Observation]: [Evidence]

### Potential Patterns
- [Pattern type]: [Description]

### Anomalies Noted
- [Anomaly]: [Why it stands out]

### Questions Raised
- [Question this source raises]
```

### Step 4: Triangulate Across Sources

Look for patterns that appear in multiple sources:

| Triangulation Type | What to Check |
|--------------------|---------------|
| **Method triangulation** | Same pattern in qual AND quant? |
| **Source triangulation** | Same pattern across user segments? |
| **Time triangulation** | Pattern consistent over time? |
| **Researcher triangulation** | Others see the same pattern? |

```markdown
## Triangulation Matrix
| Pattern | Source 1 | Source 2 | Source 3 | Confidence |
|---------|----------|----------|----------|------------|
| [Pattern A] | Present | Present | Absent | Medium |
| [Pattern B] | Present | Present | Present | High |
| [Pattern C] | Present | Absent | Absent | Low |
```

### Step 5: Distinguish Signal from Noise

Apply these tests to each pattern:

| Test | Question | Pass Criteria |
|------|----------|---------------|
| **Prevalence** | How common is it? | Appears in >30% of data |
| **Consistency** | Does it repeat? | Stable across time periods |
| **Triangulation** | Multiple sources? | 2+ sources confirm |
| **Magnitude** | How big is the effect? | Meaningful difference |
| **Mechanism** | Does it make sense? | Plausible explanation |
| **Actionability** | Can we do something? | Implies clear response |

```markdown
## Pattern Validation: [Pattern Name]

| Test | Result | Notes |
|------|--------|-------|
| Prevalence | Pass | 45% of users exhibit |
| Consistency | Pass | Stable Q1-Q3 |
| Triangulation | Pass | Interviews + analytics |
| Magnitude | Pass | 2x difference in conversion |
| Mechanism | Pass | Reduces friction at key step |
| Actionability | Pass | Can add feature to address |

**Confidence Level:** High
```

### Step 6: Document Pattern Relationships

Map how patterns connect:

```markdown
## Pattern Relationships

### Causal Chains
[Pattern A] → leads to → [Pattern B] → leads to → [Outcome]

### Moderating Factors
[Pattern X] is stronger when [Condition Y]

### Competing Patterns
[Pattern A] and [Pattern B] are mutually exclusive in [Segment]
```

### Step 7: Write Pattern Report

Document findings with full evidence chain:

```markdown
## Pattern: [Descriptive Name]

### Summary
[One sentence description]

### Evidence
| Source | Finding | Confidence |
|--------|---------|------------|
| [Source 1] | [What it shows] | High/Medium/Low |
| [Source 2] | [What it shows] | High/Medium/Low |

### Triangulation
[How sources confirm each other]

### Mechanism
[Why this pattern exists — the explanation]

### Implications
[What to do with this knowledge]

### Limitations
[What could make this wrong]
```

## Examples

**Output: Pattern Recognition Report**

```markdown
# Pattern Recognition Report: Onboarding Drop-off

## Data Sources
| Source | Type | Size | Period | Confidence |
|--------|------|------|--------|------------|
| Onboarding funnel analytics | Quantitative | 10,000 users | Q1 | High |
| User interviews | Qualitative | n=15 | March | High |
| Support tickets | Qualitative | n=234 | Q1 | Medium |
| Heatmaps | Behavioral | 500 sessions | March | Medium |

## Patterns Identified

### Pattern 1: "The Step 3 Wall"

**Summary:** Users drop off at 3x the rate at step 3 (integration setup) vs other steps.

**Evidence:**
| Source | Finding | Confidence |
|--------|---------|------------|
| Funnel analytics | 34% drop at step 3 vs 11% average | High |
| Interviews | 12/15 mentioned "getting stuck" at integrations | High |
| Support tickets | 47% of onboarding tickets about integrations | Medium |
| Heatmaps | Excessive scrolling, rage clicks on step 3 | Medium |

**Triangulation:** All four sources independently point to step 3 as friction point. High confidence.

**Mechanism:** Step 3 requires technical credentials (API keys) that users often don't have ready. They leave to get them and never return.

**Implications:**
- Add "skip for now" option at step 3
- Send email reminder if they leave at step 3
- Consider credential-free alternative integrations

**Limitations:**
- Interview sample skewed toward users who eventually succeeded
- Haven't tested whether skipping step 3 impacts activation

---

### Pattern 2: "First-Day Magic Window"

**Summary:** Users who complete a core action within first session are 4x more likely to convert.

**Evidence:**
| Source | Finding | Confidence |
|--------|---------|------------|
| Cohort analysis | Day-1 core action → 48% conversion. No action → 12% | High |
| Interviews | "I could see it working" theme in successful users | Medium |
| Session recordings | First session > 5 min correlates with success | Medium |

**Triangulation:** Quantitative pattern confirmed by qualitative explanation. Medium-high confidence.

**Mechanism:** First session is highest motivation point. Early "aha moment" locks in commitment. Users who don't see value immediately lose momentum.

**Implications:**
- Redesign onboarding to force core action earlier
- Consider pre-populated demo data for immediate value
- Reduce time-to-value metric as North Star

**Limitations:**
- Correlation ≠ causation — motivated users might both complete action AND convert
- Need A/B test to confirm causal mechanism

---

### Pattern 3: "Weekend Leakage"

**Summary:** Users who sign up on weekends have 40% lower completion rate.

**Evidence:**
| Source | Finding | Confidence |
|--------|---------|------------|
| Signup analytics | Weekend signups: 23% completion. Weekday: 38% | High |
| (No qual data) | — | N/A |

**Triangulation:** Single source only. Low confidence until validated.

**Mechanism (hypothesized):**
- Weekend signups are casual browsers vs weekday intent-driven
- Or: no support available on weekends if stuck

**Implications:**
- Investigate further before acting
- Consider different onboarding flow for weekend signups
- Test weekend support coverage

**Limitations:**
- No qualitative data to explain why
- Could be confounded by user segment (B2B vs B2C)

---

## Pattern Summary

| Pattern | Confidence | Triangulated | Action Priority |
|---------|------------|--------------|-----------------|
| Step 3 Wall | High | Yes (4 sources) | High — clear fix available |
| First-Day Magic | Medium-High | Yes (3 sources) | High — strategic insight |
| Weekend Leakage | Low | No (1 source) | Low — needs more research |

## Recommended Actions
1. **Immediate:** Add "skip for now" to step 3 with email reminder
2. **Near-term:** Redesign flow to get core action in session 1
3. **Investigate:** Qualitative research on weekend signups
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

1. **Independence first** — Analyze each source before comparing
2. **Count triangulation** — A pattern in 3 sources beats pattern in 1
3. **Distinguish correlation from causation** — Mark when you can't prove causality
4. **Name your confidence** — High/Medium/Low on every claim
5. **Document disconfirming evidence** — Note what doesn't fit
6. **Prioritize by actionability** — Best pattern is one you can act on

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Cherry-picking | Selecting data that confirms belief | Report all patterns, including contradictions |
| Single-source conclusions | No triangulation | Require 2+ sources for high confidence |
| Confusing correlation/causation | Wrong action taken | Mark causal claims as hypotheses |
| Ignoring base rates | Misinterpreting significance | Always compare to baseline |
| Over-fitting | Finding patterns in noise | Apply prevalence and consistency tests |
| Undocumented confidence | Others can't evaluate | State confidence level for every pattern |

## References

- thematic-analysis: Qualitative pattern coding
- statistical-analysis: Quantitative significance testing
- interview-synthesis: Qualitative data patterns
- research-design: Mixed methods triangulation
