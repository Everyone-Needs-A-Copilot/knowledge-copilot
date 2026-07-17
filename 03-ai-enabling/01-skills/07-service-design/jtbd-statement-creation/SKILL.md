---
last_updated: 2026-02-25
status: active
name: jtbd-statement-creation
description: Craft precise Jobs-to-be-Done statements capturing functional, emotional, and social dimensions of customer needs. Use when defining product strategy, identifying innovation opportunities, or reframing competitive landscape.
triggers:
  keywords: ["jtbd", "statement", "creation", "craft", "precise", "jobs-to-be-done", "statements", "capturing", "functional", "emotional"]
allowed-tools: Read, Write, Edit
---

# JTBD Statement Creation

## Overview

Create well-formed Jobs-to-be-Done statements that capture what customers are truly trying to accomplish, revealing stable customer needs independent of current solutions.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Identify the Core Job

Uncover the fundamental progress customers seek:

| Question | Purpose | Example Answer |
|----------|---------|----------------|
| What are they trying to accomplish? | Functional outcome | Get from A to B |
| Why does this matter to them? | Emotional driver | Feel in control of my time |
| How do they want to be perceived? | Social dimension | Seen as responsible |
| When does this need arise? | Triggering situation | Running late for meeting |

### Step 2: Apply the Job Statement Formula

Use the canonical structure:

```
When [situation/trigger],
I want to [motivation/action],
so I can [expected outcome].
```

| Component | Criteria | Good Example | Bad Example |
|-----------|----------|--------------|-------------|
| **Situation** | Specific, observable trigger | "When I have 10 minutes before a meeting" | "When I'm busy" |
| **Motivation** | Action-oriented, solution-free | "Review key discussion points" | "Use the app" |
| **Outcome** | Measurable progress | "Contribute meaningfully to discussion" | "Be prepared" |

### Step 3: Decompose into Job Dimensions

Break down the complete job:

| Dimension | Description | Example |
|-----------|-------------|---------|
| **Functional** | Practical task to complete | Arrive at destination on time |
| **Emotional** | How they want to feel | Confident, in control, relaxed |
| **Social** | How they want to appear | Responsible, professional, smart |
| **Related jobs** | Adjacent needs | Find parking, navigate unfamiliar area |

### Step 4: Map Job Hierarchy

Structure jobs at multiple levels:

| Level | Description | Example |
|-------|-------------|---------|
| **Aspirational job** | Big-picture life goal | Be a great parent |
| **Main job** | Core functional job | Get child to school safely |
| **Small jobs** | Steps within main job | Navigate route, park car |
| **Micro jobs** | Specific moments | Check traffic conditions |

### Step 5: Validate Job Statements

Test against quality criteria:

| Criterion | Test Question | Pass/Fail |
|-----------|---------------|-----------|
| **Solution-free** | Does it mention any specific solution? | Must be No |
| **Stable** | Would this job exist 50 years ago? | Should be Yes |
| **Measurable** | Can progress be objectively assessed? | Must be Yes |
| **Actionable** | Does it suggest design direction? | Must be Yes |
| **Segmentable** | Do different groups prioritize differently? | Should be Yes |

## Examples

**Good job statements:**
```
When preparing for an important client presentation,
I want to quickly understand their recent business changes,
so I can demonstrate that I understand their situation.

When onboarding a new team member,
I want to get them productive quickly,
so I can maintain team velocity and help them feel successful.
```

**Output format:**
```markdown
## Jobs-to-be-Done Analysis: [Context]

### Core Job Statement
When [situation],
I want to [motivation],
so I can [outcome].

### Job Dimensions
| Dimension | Statement |
|-----------|-----------|
| **Functional** | [What they need to accomplish] |
| **Emotional** | [How they want to feel] |
| **Social** | [How they want to appear] |

### Job Hierarchy
| Level | Job Statement |
|-------|---------------|
| **Aspirational** | [Big-picture goal] |
| **Main Job** | [Core job] |
| **Small Jobs** | [Step 1], [Step 2], [Step 3] |

### Related Jobs
| Job | Relationship | Priority |
|-----|--------------|----------|
| [Statement] | Before/After/During | High/Med/Low |

### Validation
| Criterion | Assessment |
|-----------|------------|
| Solution-free | ✓/✗ [Notes] |
| Stable | ✓/✗ [Notes] |
| Measurable | ✓/✗ [Notes] |
| Actionable | ✓/✗ [Notes] |

### Competing Solutions
| Solution | How it addresses job | Limitations |
|----------|---------------------|-------------|
| [Current solution] | [Approach] | [Gaps] |
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

- Never mention products, features, or solutions in job statements
- Include all three dimensions (functional, emotional, social)
- Create hierarchy with at least 3 levels
- Identify minimum 3 related jobs
- Validate against all 5 criteria

## References

- Forces of progress mapping: `07-service-design/forces-of-progress-mapping/SKILL.md`
- Moments Framework: `01-company/06-methodologies/20-moments-framework.md`
- Customer journey mapping: `07-service-design/customer-journey-mapping/SKILL.md`
