---
last_updated: 2026-02-25
status: active
name: thematic-analysis
description: Systematically identify, analyze, and report patterns across qualitative data. Use when processing interview transcripts, survey responses, or observational notes to extract meaningful themes with supporting evidence.
triggers:
  keywords: ["thematic", "analysis", "systematically", "identify", "analyze", "report", "patterns", "across", "qualitative", "data"]
allowed-tools: Read, Write, Edit
---

# Thematic Analysis

## Overview

Transform raw qualitative data into structured themes through systematic coding. Produces defensible insights grounded in evidence, not impressions.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Familiarize with Data

Before coding, immerse in the data:

| Activity | Purpose |
|----------|---------|
| **Read through all data** | Get holistic understanding |
| **Note initial impressions** | Capture gut reactions before analysis |
| **Mark interesting passages** | Flag potential codes |
| **Count data sources** | Know your evidence base |

### Step 2: Generate Initial Codes

Create codes systematically:

| Coding Approach | When to Use |
|-----------------|-------------|
| **Descriptive** | What is literally being said |
| **In Vivo** | Participant's exact words |
| **Process** | Actions and sequences |
| **Emotion** | Feelings expressed |
| **Values** | Beliefs and priorities |

**Coding rules:**
- One segment can have multiple codes
- Codes should be granular (specific) not abstract
- Keep a codebook with definitions
- Code everything relevant — over-code initially

### Step 3: Search for Themes

Group codes into candidate themes:

| Step | Action |
|------|--------|
| **Cluster** | Group related codes together |
| **Name** | Give each cluster a descriptive label |
| **Define** | Write one sentence describing what theme captures |
| **Scope** | Clarify boundaries — what's in/out |

### Step 4: Review and Refine Themes

Validate themes against data:

| Check | Question |
|-------|----------|
| **Internal coherence** | Do all codes within theme fit together? |
| **External distinction** | Are themes clearly different from each other? |
| **Evidence sufficiency** | Does enough data support this theme? |
| **Data coverage** | Does theme set explain most of the data? |

### Step 5: Define and Name Final Themes

For each theme, document:

| Element | Description |
|---------|-------------|
| **Name** | Concise, descriptive label |
| **Definition** | What theme captures and means |
| **Codes included** | List of constituent codes |
| **Key quotes** | 2-3 exemplar quotes |
| **Prevalence** | How many sources mention this |

## Examples

**Output format:**
```markdown
## Thematic Analysis: [Dataset/Topic]

### Dataset Summary
- **Sources:** [Number and type]
- **Total segments coded:** [Count]
- **Codes generated:** [Count]

### Codebook Summary
| Code | Definition | Frequency |
|------|------------|-----------|

### Theme Structure
| Theme | Sub-themes | Sources | Key Finding |
|-------|------------|---------|-------------|

### Theme Details

#### Theme 1: [Name]
**Definition:** [One sentence]

**Supporting Codes:** [List]

**Prevalence:** [X of Y sources]

**Key Evidence:**
> "[Quote 1]" — Participant X
> "[Quote 2]" — Participant Y

**Interpretation:** [What this means]

### Theme Relationships
[How themes connect to each other]

### Limitations
[Gaps, alternative interpretations, caveats]
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

- Code inductively (from data) not deductively (from assumptions)
- Every theme needs multiple evidence points
- Distinguish between descriptive and interpretive themes
- Track negative cases that don't fit themes
- Document your analytic decisions

## Anti-Patterns

- Forcing data into predetermined themes
- Single-quote themes (need pattern, not instance)
- Vague theme names ("communication issues")
- Skipping the systematic coding phase
- Presenting themes without evidence

## References

- Braun & Clarke: Six-phase thematic analysis
- Guest, MacQueen & Namey: Applied Thematic Analysis
