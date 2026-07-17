---
last_updated: 2026-02-25
status: active
name: value-stream-mapping
description: Visualize end-to-end flow of value delivery identifying waste, bottlenecks, and improvement opportunities. Use when optimizing processes, reducing lead times, or identifying operational inefficiencies.
triggers:
  keywords: ["value", "stream", "mapping", "visualize", "end-to-end", "flow", "delivery", "identifying", "waste", "bottlenecks"]
allowed-tools: Read, Write, Edit
---

# Value Stream Mapping

## Overview

Create visual representations of the steps, information flows, and time metrics required to deliver value from request to fulfillment, revealing waste and improvement opportunities.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Define the Value Stream

Establish scope and boundaries:

| Element | Definition | Example |
|---------|------------|---------|
| **Product/Service** | What value is being delivered? | Customer onboarding |
| **Trigger** | What initiates the stream? | Contract signed |
| **End point** | What signals completion? | First successful use |
| **Customer** | Who receives the value? | New enterprise client |

### Step 2: Map Current State

Document each step in the process:

| Step Element | What to Capture |
|--------------|-----------------|
| **Process box** | Activity name, responsible party |
| **Data box** | Cycle time, lead time, quality rate |
| **Inventory** | Queue size, WIP limits |
| **Information flow** | Manual (arrow) vs electronic (lightning) |
| **Push/Pull** | How work moves between steps |

### Step 3: Capture Time Metrics

For each step, measure:

| Metric | Definition | Goal |
|--------|------------|------|
| **Cycle Time (CT)** | Time to complete one unit | Minimize |
| **Lead Time (LT)** | Total time from start to finish | Minimize |
| **Wait Time** | Time spent in queue | Eliminate |
| **Value-Add Time** | Time actually creating value | Maximize ratio |
| **Process Time** | CT × volume | Right-size |

### Step 4: Identify the Seven Wastes

Look for Lean wastes in the stream:

| Waste | Definition | Examples |
|-------|------------|----------|
| **Transport** | Unnecessary movement of materials | Email forwarding, file transfers |
| **Inventory** | Excess WIP or finished goods | Backlog, pending queues |
| **Motion** | Unnecessary movement of people | Context switching, meetings |
| **Waiting** | Idle time between steps | Approvals, handoffs |
| **Overproduction** | Making more than needed | Batch processing, premature work |
| **Overprocessing** | Doing more than required | Gold-plating, unnecessary reviews |
| **Defects** | Errors requiring rework | Bugs, mistakes, rejections |

### Step 5: Design Future State

Create improved value stream:

1. **Calculate takt time** — Available time / Customer demand
2. **Create continuous flow** — Eliminate queues where possible
3. **Implement pull** — Only produce when downstream needs it
4. **Level the workload** — Balance capacity across steps
5. **Build in quality** — Catch defects at source

## Examples

**Output format:**
```markdown
## Value Stream Map: [Product/Service]

### Scope
- **Value stream:** [Name]
- **Trigger:** [Start event]
- **End point:** [Completion event]
- **Customer:** [Who receives value]

### Current State Metrics
| Metric | Value |
|--------|-------|
| Total Lead Time | [X days/hours] |
| Total Cycle Time | [X days/hours] |
| Value-Add Ratio | [X%] |
| First Pass Yield | [X%] |

### Process Steps
| Step | Owner | CT | LT | Queue | Quality |
|------|-------|-----|-----|-------|---------|
| [Name] | [Role] | [Time] | [Time] | [Count] | [%] |

### Waste Identification
| Waste Type | Location | Impact | Root Cause |
|------------|----------|--------|------------|
| [Type] | [Step] | [Time/Cost] | [Why] |

### Future State Targets
| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Lead Time | [X] | [Y] | [Z%] |

### Improvement Actions
| Action | Step | Expected Impact | Owner |
|--------|------|-----------------|-------|
| [Description] | [Location] | [Benefit] | [Who] |
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

- Always map current state before designing future state
- Include all seven waste types in analysis
- Calculate value-add ratio (must be documented)
- Identify at least 5 improvement opportunities
- Set measurable targets for future state

## References

- Service blueprints: `07-service-design/service-blueprint-design/SKILL.md`
- Systems thinking: `07-service-design/systems-thinking/SKILL.md`
- Forces Framework: `01-company/06-methodologies/10-forces-framework.md`
