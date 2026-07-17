---
last_updated: 2026-02-25
status: active
name: research-storytelling
description: Transform research findings into compelling narratives that drive action. Use when presenting to stakeholders, creating research reports, or needing findings to influence product decisions.
triggers:
  keywords: ["research", "storytelling", "transform", "findings", "compelling", "narratives", "drive", "action", "presenting", "stakeholders"]
allowed-tools: Read, Write, Edit
---

# Research Storytelling

## Overview

Convert research data into narratives that resonate with stakeholders and inspire action. Balances evidence rigor with emotional engagement to make findings memorable and actionable.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Identify Your Audience

Define who needs to act on findings:

| Stakeholder Type | What They Care About | Story Element to Emphasize |
|------------------|---------------------|---------------------------|
| **Executives** | Business impact, ROI | Numbers, trends, decisions needed |
| **Product managers** | Priorities, features | User needs, opportunities |
| **Engineers** | Feasibility, details | Specific behaviors, edge cases |
| **Designers** | User experience | Emotions, journeys, pain points |

### Step 2: Choose Your Story Structure

Select narrative arc based on goals:

| Structure | Best For | Format |
|-----------|----------|--------|
| **Problem → Evidence → Solution** | Advocating for change | "Users struggle with X, here's why, here's what to do" |
| **Journey narrative** | Experience redesign | Follow one user through their struggle |
| **Before/After** | Feature validation | How intervention changed experience |
| **Tension resolution** | Organizational alignment | Competing needs, resolution path |

### Step 3: Build Evidence Foundation

Every claim needs support:

| Claim Type | Evidence Needed |
|------------|-----------------|
| **Prevalence** | "X of Y participants mentioned..." |
| **Severity** | Quote + behavior description |
| **Impact** | Business metric or consequence |
| **Opportunity** | User need + unmet desire |

### Step 4: Craft Narrative Elements

Build compelling story components:

| Element | Purpose | Example |
|---------|---------|---------|
| **Hook** | Capture attention | "Every day, Sarah restarts her workflow 3 times" |
| **Character** | Create empathy | Composite user with real behaviors |
| **Tension** | Show stakes | Cost of current state |
| **Resolution** | Point toward action | What could be different |
| **Call to action** | Drive decision | Specific next step |

### Step 5: Select Evidence Highlights

Choose artifacts that make findings tangible:

| Artifact | When to Use |
|----------|-------------|
| **Direct quotes** | Convey emotion, authentic voice |
| **Video clips** | Show behavior, create empathy |
| **Journey maps** | Visualize pain points |
| **Data visualizations** | Show patterns, prevalence |
| **Before/after comparisons** | Demonstrate impact |

### Step 6: Structure the Presentation

Organize for your audience:

| Section | Content | Duration |
|---------|---------|----------|
| **Hook** | Compelling opening moment | 1-2 min |
| **Context** | Research goals, methods, scope | 2-3 min |
| **Key findings** | Top 3-5 insights with evidence | 10-15 min |
| **Implications** | What this means for product/business | 3-5 min |
| **Recommendations** | Specific actions to take | 3-5 min |
| **Discussion** | Q&A, debate, decisions | Remainder |

## Examples

**Output format:**
```markdown
## Research Story: [Title That Captures Core Insight]

### The Hook
[Opening moment — quote, scenario, or statistic that grabs attention]

### Research Context
- **Goal:** [What we set out to learn]
- **Method:** [How we learned it]
- **Participants:** [Who we learned from]

### The Story

#### Chapter 1: [Current State]
[Set up the problem with specific examples and quotes]

**Key Evidence:**
> "[Powerful quote]" — P3

#### Chapter 2: [Why It Matters]
[Show impact and stakes]

**Evidence:**
- [Statistic or pattern]
- [Consequence for users]
- [Consequence for business]

#### Chapter 3: [The Opportunity]
[Show what could be different]

### Key Insights
| # | Insight | Evidence | Implication |
|---|---------|----------|-------------|
| 1 | [Finding] | [Support] | [So what] |

### Recommendations
| Priority | Action | Expected Impact |
|----------|--------|-----------------|
| 1 | [Specific action] | [Outcome] |

### Next Steps
[Clear call to action for the audience]
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

- Lead with empathy, support with data
- One powerful quote beats five weak ones
- Every recommendation needs an evidence trail
- Make protagonists relatable (composite is fine)
- End with clear, achievable next step

## Anti-Patterns

- Data dumps without narrative thread
- All numbers, no human stories
- Vague recommendations ("improve onboarding")
- Missing evidence for key claims
- No clear call to action

## References

- Donna Lichaw: The User's Journey
- Chip & Dan Heath: Made to Stick
- Nancy Duarte: Resonate presentation framework
