---
last_updated: 2026-02-25
status: active
name: systems-thinking
description: Analyze complex problems through feedback loops, emergence, and interconnections. Use when facing wicked problems, unintended consequences, or situations where linear thinking fails.
triggers:
  keywords: ["systems", "thinking", "analyze", "complex", "problems", "feedback", "loops", "emergence", "interconnections", "facing"]
allowed-tools: Read, Write, Edit
---

# Systems Thinking

## Overview

Apply holistic analysis to understand how components interact within complex systems, revealing leverage points, feedback loops, and emergent behaviors that linear analysis misses.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Define the System

Establish boundaries and purpose:

| Element | Question | Example |
|---------|----------|---------|
| **Boundary** | What's inside vs outside the system? | Organization vs market |
| **Purpose** | What is the system trying to achieve? | Deliver customer value |
| **Components** | What are the key parts? | Teams, processes, tools |
| **Connections** | How do parts relate? | Information, resources, authority |

### Step 2: Identify Feedback Loops

Map reinforcing and balancing loops:

| Loop Type | Behavior | Symbol | Example |
|-----------|----------|--------|---------|
| **Reinforcing (R)** | Amplifies change | + → + | Growth breeds growth |
| **Balancing (B)** | Resists change | + → - | Demand drives up price, reducing demand |

Document each loop:
1. Name the loop
2. Identify all variables
3. Mark polarity of each connection (+/-)
4. Determine if R or B loop
5. Assess strength and speed

### Step 3: Find Delays

Identify where time lags exist:

| Delay Type | Description | Impact |
|------------|-------------|--------|
| **Information delay** | Time to perceive change | Overshoot/undershoot |
| **Decision delay** | Time to choose response | Missed opportunities |
| **Implementation delay** | Time to execute | Oscillation |
| **Impact delay** | Time for effects to appear | Wrong attribution |

### Step 4: Identify System Archetypes

Look for common patterns:

| Archetype | Pattern | Symptom | Leverage Point |
|-----------|---------|---------|----------------|
| **Fixes that Fail** | Quick fix creates side effects | Problem returns worse | Address root cause |
| **Shifting the Burden** | Symptomatic vs fundamental solutions | Dependency, atrophy | Strengthen fundamental |
| **Limits to Growth** | Success hits constraint | Plateau, decline | Remove limiting factor |
| **Tragedy of Commons** | Individual gain depletes shared resource | Resource exhaustion | Regulation or privatization |
| **Escalation** | Competitive response cycles | Arms race | Negotiate shared limit |
| **Success to Successful** | Winner takes more | Inequality | Level playing field |

### Step 5: Find Leverage Points

Identify where intervention has most impact:

| Leverage Level | Type | Example | Impact |
|----------------|------|---------|--------|
| 12 (lowest) | Parameters | Adjust quotas | Weak |
| 9-11 | Delays, feedback | Shorten cycle time | Moderate |
| 6-8 | Information flows | Add transparency | Strong |
| 4-5 | Rules, self-organization | Change incentives | Powerful |
| 1-3 (highest) | Goals, paradigm | Shift mental models | Transformative |

## Examples

**Output format:**
```markdown
## Systems Analysis: [System Name]

### System Definition
- **Boundary:** [What's in/out]
- **Purpose:** [System goal]
- **Key components:** [List]

### Feedback Loops
| Loop Name | Type | Variables | Speed | Strength |
|-----------|------|-----------|-------|----------|
| [Name] | R/B | A → B → C → A | Fast/Slow | Strong/Weak |

### Loop Diagram
```
    [Variable A]
        ↓ +
    [Variable B]
        ↓ +
    [Variable C]
        ↓ -
    [Variable A] (B)
```

### Delays
| Delay | Type | Duration | Impact |
|-------|------|----------|--------|
| [Name] | Information/Decision/etc | [Time] | [Effect] |

### System Archetypes Present
| Archetype | Evidence | Current State |
|-----------|----------|---------------|
| [Name] | [Symptoms observed] | [Where in pattern] |

### Leverage Points
| Point | Type | Intervention | Expected Impact |
|-------|------|--------------|-----------------|
| [Location] | [Level] | [Action] | [Outcome] |

### Recommendations
1. [Highest leverage intervention]
2. [Second intervention]
3. [Third intervention]
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

- Always define system boundary explicitly
- Identify at least 3 feedback loops (mix of R and B)
- Look for at least 2 system archetypes
- Find leverage points at multiple levels
- Consider delays in all recommendations

## References

- Forces Framework: `01-company/06-methodologies/10-forces-framework.md`
- Mental models: `06-strategy/02-mental-models/SKILL.md`
- Ecosystem mapping: `07-service-design/ecosystem-mapping/SKILL.md`
