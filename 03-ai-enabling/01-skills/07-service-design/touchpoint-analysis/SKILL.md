---
last_updated: 2026-02-25
status: active
name: touchpoint-analysis
description: Audit and evaluate customer touchpoints across channels for consistency, effectiveness, and experience quality. Use when optimizing omnichannel experiences, identifying gaps, or prioritizing experience investments.
triggers:
  keywords: ["touchpoint", "analysis", "audit", "evaluate", "customer", "touchpoints", "across", "channels", "consistency", "effectiveness"]
allowed-tools: Read, Write, Edit
---

# Touchpoint Analysis

## Overview

Systematically inventory, evaluate, and prioritize all points of interaction between customers and your service to identify inconsistencies, gaps, and improvement opportunities.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Inventory All Touchpoints

Catalog every interaction point:

| Channel Category | Touchpoint Types | Examples |
|------------------|------------------|----------|
| **Digital owned** | Website, app, email | Homepage, checkout, welcome email |
| **Digital earned** | Social, reviews, search | Twitter mentions, G2 reviews |
| **Physical owned** | Stores, offices, packaging | Retail location, product box |
| **Physical earned** | Events, PR, word of mouth | Conference booth, news article |
| **Human direct** | Sales, support, success | Demo call, support ticket |
| **Human indirect** | Partners, resellers | Channel partner interaction |

### Step 2: Map Touchpoints to Journey

Connect touchpoints to journey stages:

| Journey Stage | Touchpoints | Frequency | Criticality |
|---------------|-------------|-----------|-------------|
| **Awareness** | Ads, content, social | First encounter | Sets expectations |
| **Consideration** | Website, demos, reviews | Multiple | Builds confidence |
| **Purchase** | Checkout, contract, payment | One-time | Commits relationship |
| **Onboarding** | Welcome, setup, training | First weeks | Determines adoption |
| **Usage** | Product, support, billing | Ongoing | Drives satisfaction |
| **Advocacy** | Referral, review, community | Periodic | Generates growth |

### Step 3: Evaluate Each Touchpoint

Assess quality dimensions:

| Dimension | Assessment Question | Scale |
|-----------|-------------------|-------|
| **Availability** | Can customers access it when needed? | 1-5 |
| **Usability** | Is it easy to use effectively? | 1-5 |
| **Consistency** | Does it match brand and other touchpoints? | 1-5 |
| **Reliability** | Does it work correctly every time? | 1-5 |
| **Emotional impact** | How does it make customers feel? | -2 to +2 |

### Step 4: Identify Gaps and Issues

Analyze the touchpoint landscape:

| Issue Type | Indicator | Example |
|------------|-----------|---------|
| **Gaps** | Missing touchpoints | No mobile app for field users |
| **Inconsistencies** | Conflicting messages/experiences | Different pricing on web vs sales |
| **Redundancies** | Duplicate touchpoints | Two support email addresses |
| **Broken handoffs** | Lost context between touchpoints | Repeating info after transfer |
| **Channel conflicts** | Channels competing vs complementing | Store vs web pricing |

### Step 5: Prioritize Improvements

Rank opportunities by impact:

| Factor | Weight | Assessment |
|--------|--------|------------|
| **Customer frequency** | High | How often is touchpoint used? |
| **Journey criticality** | High | Is it at a make-or-break moment? |
| **Current performance** | Medium | How poor is current experience? |
| **Improvement feasibility** | Medium | Can we actually fix it? |
| **Cost of failure** | High | What happens if it fails? |

## Examples

**Output format:**
```markdown
## Touchpoint Analysis: [Service/Product]

### Touchpoint Inventory
| Touchpoint | Channel | Journey Stage | Owner | Status |
|------------|---------|---------------|-------|--------|
| [Name] | Digital/Physical/Human | [Stage] | [Team] | Active/Planned/Deprecated |

### Touchpoint by Journey Stage
```
Awareness    [●][●][○]
Consider     [●][●][●][●]
Purchase     [●][●]
Onboarding   [●][●][●]
Usage        [●][●][●][●][●]
Advocacy     [○][○]

● = Active touchpoint
○ = Gap/Missing
```

### Touchpoint Evaluation
| Touchpoint | Avail | Usable | Consistent | Reliable | Emotion | Score |
|------------|-------|--------|------------|----------|---------|-------|
| [Name] | 4/5 | 3/5 | 2/5 | 5/5 | +1 | 14/22 |

### Gap Analysis
| Gap Type | Location | Impact | Recommendation |
|----------|----------|--------|----------------|
| Missing | [Stage/Channel] | [Effect] | [Action] |
| Inconsistent | [Touchpoints] | [Effect] | [Action] |

### Handoff Quality
| From | To | Context Preserved | Friction Points |
|------|-----|-------------------|-----------------|
| [Touchpoint A] | [Touchpoint B] | High/Med/Low | [Issues] |

### Priority Improvements
| Rank | Touchpoint | Issue | Impact | Effort | ROI |
|------|------------|-------|--------|--------|-----|
| 1 | [Name] | [Problem] | High | Med | High |

### Recommendations
1. **Quick wins:** [Low effort, high impact fixes]
2. **Strategic investments:** [High effort, high impact projects]
3. **Monitoring:** [Touchpoints to track closely]
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

- Inventory at least 20 touchpoints across all channel types
- Evaluate all touchpoints in the purchase and onboarding stages
- Identify minimum 5 improvement opportunities
- Map handoffs between all high-frequency touchpoints
- Include both customer-facing and internal touchpoint owners

## References

- Customer journey mapping: `07-service-design/customer-journey-mapping/SKILL.md`
- Service blueprints: `07-service-design/service-blueprint-design/SKILL.md`
- Moments Framework: `01-company/06-methodologies/20-moments-framework.md`
