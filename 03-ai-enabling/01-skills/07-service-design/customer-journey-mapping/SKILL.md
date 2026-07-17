---
last_updated: 2026-02-25
status: active
name: customer-journey-mapping
description: Visualize complete customer experiences across touchpoints, channels, and time. Use when understanding customer pain points, designing new experiences, or aligning teams around customer perspective.
triggers:
  keywords: ["customer", "journey", "mapping", "visualize", "complete", "experiences", "across", "touchpoints", "channels", "time"]
allowed-tools: Read, Write, Edit
---

# Customer Journey Mapping

## Overview

Create visual narratives of customer experiences that capture actions, thoughts, emotions, and pain points across all touchpoints, revealing opportunities for experience improvement.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Define the Journey

Establish scope and perspective:

| Element | Question | Example |
|---------|----------|---------|
| **Persona** | Who is taking this journey? | First-time enterprise buyer |
| **Scenario** | What are they trying to accomplish? | Evaluate and purchase solution |
| **Scope** | Where does journey start/end? | Problem awareness → First renewal |
| **Lens** | Current state or future state? | Current state |

### Step 2: Map Journey Stages

Divide experience into meaningful phases:

| Stage Type | Description | Example Stages |
|------------|-------------|----------------|
| **Awareness** | Recognizing need exists | Trigger event, research |
| **Consideration** | Evaluating options | Compare, demo, trial |
| **Decision** | Making the choice | Negotiate, approve, purchase |
| **Onboarding** | Getting started | Setup, training, first use |
| **Usage** | Ongoing experience | Daily use, support, upgrade |
| **Advocacy** | Becoming promoter | Refer, review, renew |

### Step 3: Build Journey Layers

For each stage, document:

| Layer | Content | Capture Method |
|-------|---------|----------------|
| **Actions** | What customer does | Observation, analytics |
| **Touchpoints** | Where interaction happens | Channel audit |
| **Thoughts** | What customer thinks | Interviews, surveys |
| **Emotions** | How customer feels | Sentiment analysis |
| **Pain points** | Friction and frustration | Complaints, feedback |
| **Opportunities** | Improvement potential | Gap analysis |

### Step 4: Identify Moments of Truth

Find critical experience inflection points:

| Moment Type | Description | Impact |
|-------------|-------------|--------|
| **First impression** | Initial contact | Sets expectations |
| **Make or break** | Critical decision point | Determines continuation |
| **Peak positive** | Highest satisfaction | Drives loyalty |
| **Peak negative** | Lowest satisfaction | Drives churn |
| **Final impression** | Last touchpoint | Shapes memory |

### Step 5: Calculate Experience Metrics

Quantify the journey:

| Metric | Formula | Target |
|--------|---------|--------|
| **Effort Score** | Sum of friction points | Minimize |
| **Emotion Curve** | Plot sentiment over time | Positive trend |
| **Drop-off Rate** | Exits at each stage | <10% per stage |
| **Time to Value** | Start to first success | Minimize |

## Examples

**Output format:**
```markdown
## Customer Journey Map: [Persona] — [Scenario]

### Journey Overview
- **Persona:** [Name and key attributes]
- **Goal:** [What they're trying to achieve]
- **Scope:** [Start point] → [End point]
- **Journey type:** Current/Future state

### Journey Stages
| Stage | Duration | Key Actions | Primary Channel |
|-------|----------|-------------|-----------------|
| [Name] | [Time] | [Actions] | [Channel] |

### Detailed Journey
#### Stage: [Name]
| Layer | Content |
|-------|---------|
| **Actions** | [What they do] |
| **Touchpoints** | [Where] |
| **Thoughts** | [What they think] |
| **Emotions** | [How they feel] 😊/😐/😟 |
| **Pain points** | [Friction] |

### Emotion Curve
```
High  |    *
      |   * *      *
      |  *   *    *
      | *     *  *
Low   |*       **
      +-----------------
       Stage 1  2  3  4
```

### Moments of Truth
| Moment | Stage | Type | Current Experience | Impact |
|--------|-------|------|-------------------|--------|
| [Name] | [Stage] | Peak positive/negative | [Description] | High/Med/Low |

### Pain Points Summary
| Pain Point | Stage | Severity | Frequency | Root Cause |
|------------|-------|----------|-----------|------------|
| [Description] | [Stage] | High/Med/Low | [%] | [Why] |

### Opportunities
| Opportunity | Stage | Impact | Effort | Priority |
|-------------|-------|--------|--------|----------|
| [Description] | [Stage] | High/Med/Low | High/Med/Low | 1/2/3 |
```



## Quality Tests

### Customer Perspective Test
- Analysis reflects actual customer experience, not internal assumptions
- **PASS:** Insights are based on customer data, quotes, or observed behavior
- **FAIL:** Journey map reflects what we think customers experience, not reality

### Systemic Test
- Analysis considers the full service ecosystem, not just one touchpoint
- **PASS:** Cross-channel handoffs and backstage processes are included
- **FAIL:** Only the digital touchpoint analyzed, ignoring phone/in-person/email

## Guidelines

- Base journey on research, not assumptions
- Include at least 5 stages
- Document all layers for each stage
- Plot emotion curve with supporting evidence
- Identify minimum 3 moments of truth
- Prioritize opportunities by impact/effort

## References

- Service blueprints: `07-service-design/service-blueprint-design/SKILL.md`
- Touchpoint analysis: `07-service-design/touchpoint-analysis/SKILL.md`
- Moments Framework: `01-company/06-methodologies/20-moments-framework.md`
