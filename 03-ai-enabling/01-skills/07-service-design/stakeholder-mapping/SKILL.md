---
last_updated: 2026-02-25
status: active
name: stakeholder-mapping
description: Identify, analyze, and prioritize stakeholders by power, interest, and influence. Use when launching initiatives, managing change, or navigating complex organizational dynamics.
triggers:
  keywords: ["stakeholder", "mapping", "identify", "analyze", "prioritize", "stakeholders", "power", "interest", "influence", "launching"]
allowed-tools: Read, Write, Edit
---

# Stakeholder Mapping

## Overview

Systematically identify all parties affected by or affecting a service/initiative, then prioritize engagement strategies based on their power, interest, and influence.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Identify Stakeholders

Cast a wide net across categories:

| Category | Examples | Discovery Question |
|----------|----------|-------------------|
| **Decision makers** | Executives, board, budget owners | Who can approve or kill this? |
| **Influencers** | Advisors, thought leaders, unions | Who shapes opinions? |
| **Users** | End customers, internal users | Who uses the service directly? |
| **Providers** | Staff, vendors, partners | Who delivers value? |
| **Affected parties** | Communities, regulators, competitors | Who is impacted indirectly? |

### Step 2: Assess Each Stakeholder

Rate on key dimensions:

| Dimension | Scale | Assessment Question |
|-----------|-------|-------------------|
| **Power** | High/Medium/Low | Can they make or break success? |
| **Interest** | High/Medium/Low | How much do they care? |
| **Influence** | High/Medium/Low | Can they sway others? |
| **Attitude** | Supporter/Neutral/Opponent | Are they for or against? |
| **Impact** | High/Medium/Low | How much are they affected? |

### Step 3: Plot on Power-Interest Grid

Position stakeholders in quadrants:

| Quadrant | Power | Interest | Strategy |
|----------|-------|----------|----------|
| **Manage Closely** | High | High | Regular engagement, involve in decisions |
| **Keep Satisfied** | High | Low | Address concerns, don't overwhelm |
| **Keep Informed** | Low | High | Regular updates, leverage as advocates |
| **Monitor** | Low | Low | Minimal effort, watch for changes |

### Step 4: Develop Engagement Plan

For priority stakeholders, define:

| Element | Description |
|---------|-------------|
| **Key concerns** | What matters most to them? |
| **Value proposition** | What's in it for them? |
| **Communication channel** | How do they prefer to engage? |
| **Frequency** | How often to connect? |
| **Owner** | Who manages this relationship? |

### Step 5: Identify Dynamics

Map relationships between stakeholders:

- **Alliances** — Who works together?
- **Conflicts** — Who opposes each other?
- **Dependencies** — Who relies on whom?
- **Influence paths** — Who can sway whom?

## Examples

**Output format:**
```markdown
## Stakeholder Map: [Initiative/Service]

### Stakeholder Register
| Stakeholder | Category | Power | Interest | Attitude | Priority |
|-------------|----------|-------|----------|----------|----------|
| [Name/Role] | Decision maker | High | High | Supporter | Manage closely |

### Power-Interest Grid
```
         High Interest
              |
   Keep       |    Manage
   Informed   |    Closely
              |
Low Power ----+---- High Power
              |
   Monitor    |    Keep
              |    Satisfied
              |
         Low Interest
```

### Priority Stakeholders
| Stakeholder | Key Concern | Value Prop | Channel | Frequency |
|-------------|-------------|------------|---------|-----------|
| [Name] | [Concern] | [WIIFM] | [Method] | [Cadence] |

### Stakeholder Dynamics
| Relationship | Stakeholders | Type | Implication |
|--------------|--------------|------|-------------|
| [Description] | A ↔ B | Alliance/Conflict | [Strategic meaning] |

### Engagement Risks
1. [Risk with mitigation strategy]
2. [Second risk]
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

- Include at least 15 stakeholders across all categories
- Assess all five dimensions for priority stakeholders
- Identify at least 3 stakeholder dynamics
- Create engagement plans for all "Manage Closely" stakeholders
- Review and update quarterly

## References

- Ecosystem mapping: `07-service-design/ecosystem-mapping/SKILL.md`
- Forces Framework: `01-company/06-methodologies/10-forces-framework.md`
- Change management: `01-company/03-services/`
