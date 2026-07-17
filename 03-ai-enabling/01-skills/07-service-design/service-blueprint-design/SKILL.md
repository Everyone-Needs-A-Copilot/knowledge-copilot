---
last_updated: 2026-02-25
status: active
name: service-blueprint-design
description: Create comprehensive service blueprints mapping customer actions, frontstage/backstage processes, and support systems. Use when designing new services, diagnosing service failures, or aligning teams on service delivery.
triggers:
  keywords: ["service", "blueprint", "design", "create", "comprehensive", "blueprints", "mapping", "customer", "actions", "frontstage"]
allowed-tools: Read, Write, Edit
---

# Service Blueprint Design

## Overview

Create visual representations of service delivery showing the relationship between customer touchpoints, employee actions, and supporting systems across the entire service journey.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Define Blueprint Scope

Establish boundaries for the blueprint:

| Element | Question |
|---------|----------|
| **Service** | What specific service or service component? |
| **Customer segment** | Who is the primary user? |
| **Scenario** | What use case or journey path? |
| **Start/End points** | Where does this experience begin and end? |

### Step 2: Map the Five Swimlanes

Build the blueprint layer by layer:

| Swimlane | Description | Examples |
|----------|-------------|----------|
| **Physical Evidence** | Tangible artifacts customers encounter | Website, app, receipt, email |
| **Customer Actions** | Steps customers take | Search, click, call, wait |
| **Frontstage Actions** | Visible employee/system actions | Greet, explain, process |
| **Backstage Actions** | Invisible employee/system actions | Verify, route, update |
| **Support Processes** | Systems and processes enabling delivery | CRM, inventory, billing |

### Step 3: Identify Key Elements

Mark critical blueprint components:

| Element | Symbol | Purpose |
|---------|--------|---------|
| **Line of Interaction** | ─── | Separates customer from frontstage |
| **Line of Visibility** | - - - | Separates frontstage from backstage |
| **Line of Internal Interaction** | ··· | Separates backstage from support |
| **Fail Points** | F | Where failures commonly occur |
| **Wait Points** | W | Where customers experience delays |
| **Decision Points** | ◇ | Where branching logic exists |

### Step 4: Add Time and Metrics

Annotate with operational data:

- **Duration** — Time for each step
- **Cost** — Resources required
- **Frequency** — How often this path occurs
- **Satisfaction** — Customer sentiment at each stage

### Step 5: Analyze and Prioritize

Identify improvement opportunities:

1. **Pain points** — Where do failures and waits cluster?
2. **Disconnects** — Where is handoff friction highest?
3. **Redundancy** — Where are steps duplicated?
4. **Gaps** — What's missing that customers expect?

## Examples

**Output format:**
```markdown
## Service Blueprint: [Service Name]

### Scope
- **Service:** [Name]
- **Customer:** [Segment]
- **Scenario:** [Use case]
- **Journey:** [Start] → [End]

### Blueprint
| Physical Evidence | [artifacts at each stage] |
| Customer Actions | [steps customers take] |
| ─── Line of Interaction ─── |
| Frontstage Actions | [visible actions] |
| - - - Line of Visibility - - - |
| Backstage Actions | [invisible actions] |
| ··· Line of Internal Interaction ··· |
| Support Processes | [systems/processes] |

### Time & Metrics
| Stage | Duration | Cost | Satisfaction |
|-------|----------|------|--------------|

### Critical Points
| Type | Location | Impact | Priority |
|------|----------|--------|----------|
| Fail Point | [stage] | [description] | High/Med/Low |
| Wait Point | [stage] | [description] | High/Med/Low |

### Recommendations
1. [Priority improvement with rationale]
2. [Second improvement]
3. [Third improvement]
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

- Always include all five swimlanes
- Mark fail points and wait points explicitly
- Include time estimates for each customer action
- Connect backstage actions to specific support processes
- Identify at least 3 improvement opportunities

## References

- Moments Framework: `01-company/06-methodologies/20-moments-framework.md`
- Touchpoint patterns: `01-company/05-patterns/`
- Customer journey mapping: `07-service-design/customer-journey-mapping/SKILL.md`
