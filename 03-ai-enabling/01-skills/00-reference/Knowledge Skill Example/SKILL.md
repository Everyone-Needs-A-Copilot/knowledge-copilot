---
last_updated: 2026-02-25
status: active
name: forces-analysis
description: >-
  Analyze strategic forces acting on a person, company, or situation using the Forces Framework.
  Use when preparing for strategic conversations, qualifying opportunities, or diagnosing resistance.
triggers:
  keywords: ["forces", "analysis", "strategic", "push", "pull", "tension", "resistance",
             "motivation", "blocker", "driver", "friction", "momentum", "switch"]
allowed-tools: Read, Write, Edit
---

# Forces Analysis

## Overview

Apply the Forces Framework to understand what's driving or blocking a change, decision, or relationship. Forces are the invisible dynamics -- tensions, motivations, anxieties, and habits -- that shape every strategic situation. This skill teaches how to identify, categorize, and act on forces.

## Define Done

A forces analysis is complete when:

- [ ] All 4 force types identified (Push, Pull, Anxiety, Habit)
- [ ] Each force has evidence (not speculation)
- [ ] Forces are ranked by intensity (1-5 scale)
- [ ] Net force direction determined (favoring change or status quo)
- [ ] Recommended actions address the dominant forces

## Prerequisites

- Situation context: who, what change, what's at stake
- Data sources: conversation history, relationship data, market signals
- For copilot-enriched analysis: `copilot conv forces list --json`, `copilot insights forces list --json`

## Framework

The Forces Framework identifies 4 types of forces acting on any change:

| Force Type | Direction | Description | Example |
|-----------|-----------|-------------|---------|
| **Push** | Toward change | Pain with current situation | "Our current tool is costing us 40% more than competitors" |
| **Pull** | Toward change | Attraction of the new | "The new platform has AI features we need" |
| **Anxiety** | Against change | Fear of the new | "What if the migration fails and we lose data?" |
| **Habit** | Against change | Comfort with current | "Our team knows the current tool inside-out" |

### Force Intensity Scale

| Level | Intensity | Indicator |
|-------|-----------|-----------|
| 1 | Awareness | Person mentions it casually |
| 2 | Interest | Person asks questions about it |
| 3 | Concern | Person brings it up unprompted |
| 4 | Urgency | Person is actively seeking solutions |
| 5 | Crisis | Person must act now -- blocking everything else |

### Net Force Calculation

```
Net = (Sum of Push + Pull intensities) - (Sum of Anxiety + Habit intensities)

Net > 0  -> Change is likely -- focus on reducing remaining anxiety
Net = 0  -> Stalemate -- one force shift tips the balance
Net < 0  -> Status quo wins -- must increase push/pull or reduce anxiety/habit
```

## Instructions

### Step 1: Gather Force Evidence (REQUIRED)

Collect data from available sources:

**From Conversations Copilot:**
```bash
copilot conv forces list --json          # Existing identified forces
copilot conv people personality --id <id> --json   # Personality affects force sensitivity
copilot conv conversations list --json   # Recent conversation context
```

**From Insights Copilot:**
```bash
copilot insights forces list --json      # Market-level forces
copilot insights synthesis patterns --json  # Cross-force patterns
```

**From direct observation:** quotes, behaviors, decisions, hesitations.

### Step 2: Categorize Each Force (REQUIRED)

For each force identified, determine:
1. **Type:** Push, Pull, Anxiety, or Habit
2. **Evidence:** Specific quote, data point, or observed behavior
3. **Intensity:** 1-5 scale
4. **Validated:** Has this been confirmed by the person, or is it inferred?

### Step 3: Calculate Net Direction (REQUIRED)

Sum the pro-change forces (Push + Pull) and anti-change forces (Anxiety + Habit). Determine the net direction and magnitude.

### Step 4: Recommend Actions (REQUIRED)

Based on the net force direction:

| Net Direction | Strategy | Actions |
|---------------|----------|---------|
| Strong positive (>5) | Accelerate | Remove remaining friction, propose next step |
| Weak positive (1-5) | Nurture | Address top anxiety, reinforce strongest pull |
| Neutral (0) | Tip the balance | Find the one force that's easiest to shift |
| Weak negative (-1 to -5) | Reframe | Introduce new push force or reduce top habit |
| Strong negative (<-5) | Wait or pivot | Situation isn't ready -- monitor for change triggers |

### Step 5: Validate Forces (OPTIONAL)

Use the next conversation to test your analysis:

```bash
# After conversation, mark forces as validated
copilot conv forces validate --id <force_id> --json
```

## Examples

### Example: Technology Migration Decision

**Situation:** Client considering switching from legacy CRM to new platform.

**Forces identified:**

| # | Type | Force | Evidence | Intensity |
|---|------|-------|----------|-----------|
| 1 | Push | Data silos causing missed opportunities | "We lost a deal because sales didn't see support's notes" | 4 |
| 2 | Push | Rising costs of legacy maintenance | Maintenance contract up 30% this year | 3 |
| 3 | Pull | AI-powered insights in new platform | "The predictive scoring demo was impressive" | 3 |
| 4 | Anxiety | Migration risk to active deals | "We can't afford any downtime during Q4" | 4 |
| 5 | Anxiety | Team retraining time | "My team barely learned the current system" | 3 |
| 6 | Habit | Existing integrations work | "Everything is wired up and running" | 2 |

**Net calculation:**
- Pro-change: 4 + 3 + 3 = 10
- Anti-change: 4 + 3 + 2 = 9
- **Net: +1 (weak positive)**

**Strategy:** Nurture -- address the top anxiety (migration risk) by proposing a phased rollout that avoids Q4.

### Example: Relationship Stagnation

**Situation:** Long-term client engagement losing momentum.

| # | Type | Force | Evidence | Intensity |
|---|------|-------|----------|-----------|
| 1 | Habit | Comfortable with status quo | Declining meeting frequency, "things are fine" | 4 |
| 2 | Push | Competitor gaining ground | Client mentioned a competitor's new feature twice | 3 |
| 3 | Pull | Strategic planning season | "We need to figure out next year's priorities" | 2 |
| 4 | Anxiety | Budget uncertainty | "We're not sure about next year's budget yet" | 3 |

**Net: +5 - 7 = -2 (weak negative)**

**Strategy:** Reframe -- introduce a new push force by surfacing competitive intelligence the client hasn't seen.

## Quality Tests

### Force Completeness Test
- All 4 force types have been considered (not just push and pull)
- **PASS:** Analysis includes at least one force from each of the 4 types, or explicitly notes why a type has no forces
- **FAIL:** Only push and pull forces listed -- anxiety and habit ignored

### Evidence Test
- Every force has specific evidence, not vague assertions
- **PASS:** Each force cites a quote, data point, behavior, or observation
- **FAIL:** Force listed as "they seem resistant" without specific evidence

### Actionability Test
- Recommended actions directly address the dominant forces
- **PASS:** Top-intensity force has a specific recommended action
- **FAIL:** Generic advice ("build trust") that doesn't target a specific force

### Validation Test
- Analysis distinguishes between observed and inferred forces
- **PASS:** Each force marked as "validated" (confirmed by person) or "inferred" (analyst's assessment)
- **FAIL:** All forces presented with equal confidence regardless of evidence quality

## Guidelines

1. Always check all 4 force types -- anxiety and habit are easy to miss
2. Higher-intensity forces deserve more investigation, not just acknowledgment
3. Net force direction determines strategy -- don't fight strong negatives
4. Validate inferred forces in the next conversation before acting on them
5. Forces change over time -- re-analyze after significant events
6. Cross-reference Conv forces (relationship-level) with Insights forces (market-level) for full picture

## References

- Related skills: `conversation-prep`, `intelligence-brief`
- Forces data: `copilot conv forces list --json` (relationship forces)
- Market forces: `copilot insights forces list --json` (strategic forces)
- Force types reference: `reference/force-types.md`
- Output template: `reference/output-template.md`
