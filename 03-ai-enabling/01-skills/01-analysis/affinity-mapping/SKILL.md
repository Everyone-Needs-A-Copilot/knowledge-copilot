---
last_updated: 2026-02-25
status: active
name: affinity-mapping
description: Synthesize qualitative data by grouping related insights into hierarchical themes. Use when processing research notes, brainstorming outputs, or scattered observations to find patterns and build shared understanding.
triggers:
  keywords: ["affinity", "mapping", "synthesize", "qualitative", "data", "grouping", "related", "insights", "hierarchical", "themes"]
allowed-tools: Read, Write, Edit
---

# Affinity Mapping

## Overview

Organize large volumes of qualitative data into meaningful groups through bottom-up clustering. Creates shared understanding across teams while preserving individual data points as evidence.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Prepare Data Points

Transform raw data into individual units:

| Source | Data Point Format |
|--------|-------------------|
| **Interview notes** | One observation/quote per sticky |
| **Survey responses** | One response per sticky |
| **Brainstorm ideas** | One idea per sticky |
| **Observation notes** | One observation per sticky |

**Data point rules:**
- Each point is one discrete idea
- Write in user voice when possible ("I struggle to...")
- Include source reference (P3, Survey#45)
- Keep brief but specific

### Step 2: Initial Clustering

Group data points organically:

| Action | Guidance |
|--------|----------|
| **Read each point** | Understand before placing |
| **Find related points** | Move similar items together |
| **Create new groups** | When points don't fit existing groups |
| **Allow singletons** | Not everything needs a group |

**Clustering tips:**
- Don't pre-define categories — let them emerge
- Move silently during team sessions
- Duplicate points that fit multiple groups
- Keep groups between 3-8 items

### Step 3: Name the Groups

Label each cluster:

| Level | What to Capture |
|-------|-----------------|
| **Descriptive** | What items have in common |
| **Interpretive** | What it means for users |
| **Actionable** | Design implication |

**Good group names:**
- "Users fear losing work" (not "Fear")
- "First-time setup is confusing" (not "Onboarding issues")
- Specific enough to guide action

### Step 4: Build Hierarchy

Create parent categories:

| Level | Description | Example |
|-------|-------------|---------|
| **L3 (top)** | Strategic theme | "Trust & Confidence" |
| **L2 (middle)** | Sub-theme | "Data Security Concerns" |
| **L1 (bottom)** | Individual insights | "I worry about losing my files" |

### Step 5: Extract Insights

Transform structure into findings:

| For Each Group | Document |
|----------------|----------|
| **Prevalence** | How many data points |
| **Sources** | Which participants/sources |
| **Key quotes** | Most representative evidence |
| **Design implication** | So what? |

## Examples

**Output format:**
```markdown
## Affinity Map: [Research/Project Name]

### Data Summary
- **Total data points:** [Count]
- **L1 groups:** [Count]
- **L2 themes:** [Count]
- **L3 strategic areas:** [Count]

### Affinity Structure

#### L3: [Strategic Theme Name]
**Sub-themes:** [Count] | **Data points:** [Count]

##### L2: [Sub-theme Name]
**Evidence strength:** [Count] data points from [Count] sources

L1 Groups:
- **[Group name]** ([Count] points)
  - "[Example quote]" — P3
  - "[Example quote]" — P7

##### L2: [Sub-theme Name]
...

### Top Insights
| Rank | Theme | Evidence | Design Implication |
|------|-------|----------|-------------------|
| 1 | [Theme] | [X points, Y sources] | [Action] |
| 2 | [Theme] | [X points, Y sources] | [Action] |

### Outliers & Edge Cases
[Data points that didn't fit — may indicate emerging needs]

### Team Alignment Notes
[Key discussions, disagreements, decisions during mapping]
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

- Build bottom-up — let structure emerge from data
- Every insight needs multiple evidence points
- Preserve original wording in data points
- Name groups with user language, not jargon
- Document the process, not just the output

## Anti-Patterns

- Starting with predefined categories (top-down)
- Groups with only 1-2 items (may be outliers)
- Abstract group names ("Communication")
- Losing source attribution during clustering
- Forcing all points into groups

## References

- Karen Holtzblatt: Contextual Design affinity diagrams
- Nielsen Norman Group: Affinity Diagramming guide
