---
last_updated: 2026-02-25
status: active
name: interview-synthesis
description: Transform interview transcripts into structured insights using thematic coding and force mapping. Produces evidence-backed findings with supporting quotes. Use after completing interviews to extract patterns and actionable insights.
triggers:
  keywords: ["interview", "synthesis", "transform", "transcripts", "structured", "insights", "using", "thematic", "coding", "force"]
allowed-tools: Read, Write, Edit
---

# Interview Synthesis

## Overview

Convert raw interview transcripts into structured findings through systematic coding and force analysis. Produces defensible insights grounded in participant evidence, organized by themes and forces of progress.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Prepare Transcripts

Before coding, ensure clean data:

| Preparation Task | Action |
|------------------|--------|
| **Clean transcript** | Fix typos, remove filler words if needed |
| **Add timestamps** | Enable quick reference to original |
| **Note speaker turns** | Clearly mark interviewer vs participant |
| **Remove PII** | Replace names with codes (P1, P2...) |

```markdown
## Interview Log
| Code | Role | Date | Duration | Key context |
|------|------|------|----------|-------------|
| P1 | Marketing Director | 2024-03-15 | 45 min | Recently switched tools |
| P2 | Small business owner | 2024-03-16 | 52 min | First-time buyer |
```

### Step 2: First Pass — Highlight Key Moments

Read each transcript marking significant segments:

| Segment Type | What to Mark |
|--------------|--------------|
| **Trigger events** | "That's when I decided to..." |
| **Frustrations** | Strong emotion about problems |
| **Desires** | What they wished for |
| **Workarounds** | How they hack current solutions |
| **Decisions** | Choice points and rationale |
| **Surprises** | Unexpected behaviors or beliefs |

### Step 3: Code Forces of Progress

For each participant, map the four forces:

```markdown
## Forces Map: [Participant Code]

### Push (Away from status quo)
- "I was spending 3 hours every week just on [task]" (P1, 12:34)
- "It kept breaking and I'd lose work" (P1, 18:22)

### Pull (Toward new solution)
- "I saw [competitor] using it and it looked so easy" (P1, 23:15)
- "They promised I could do [outcome] in half the time" (P1, 25:40)

### Anxiety (Fears about change)
- "What if I lose all my data?" (P1, 28:10)
- "I wasn't sure I could learn a new system" (P1, 30:05)

### Habit (Inertia with current state)
- "At least I knew where everything was" (P1, 32:22)
- "My whole team was trained on it already" (P1, 34:18)
```

### Step 4: Create Thematic Codes

Develop codes that capture patterns across interviews:

| Code Category | Example Codes |
|---------------|---------------|
| **Problems** | #time-waste, #data-loss, #complexity |
| **Goals** | #automation, #visibility, #growth |
| **Emotions** | #frustration, #relief, #anxiety |
| **Triggers** | #breaking-point, #recommendation, #mandate |
| **Barriers** | #learning-curve, #integration, #cost |

```markdown
## Codebook
| Code | Definition | Example |
|------|------------|---------|
| #time-waste | Excessive manual effort on routine tasks | "Hours entering the same data twice" |
| #breaking-point | Event that triggered active search | "The report was wrong for the third time" |
```

### Step 5: Identify Patterns

Look for patterns across participants:

| Pattern Type | What to Look For |
|--------------|------------------|
| **Convergence** | Same code appears in 3+ interviews |
| **Divergence** | Contradictory findings to investigate |
| **Sequences** | Common paths through experience |
| **Clusters** | Codes that co-occur |
| **Outliers** | Unique findings worth noting |

```markdown
## Pattern Summary
| Pattern | Frequency | Confidence | Example |
|---------|-----------|------------|---------|
| Time trigger | 5/6 participants | High | Breaking point is time-related |
| Fear of migration | 4/6 participants | Medium | Data loss primary concern |
```

### Step 6: Write Insight Statements

Transform patterns into actionable insights:

```markdown
## Insight: [Descriptive Title]

**Finding:** [One sentence stating what you learned]

**Evidence:**
> "[Quote 1]" — P1
> "[Quote 2]" — P3
> "[Quote 3]" — P5

**Prevalence:** [X of Y participants]

**So what:** [Why this matters for decisions]

**Questions raised:** [What you still don't know]
```

### Step 7: Create Forces Summary

Synthesize forces across all participants:

```markdown
## Forces Summary (n=6)

### Dominant Push Forces
1. **Time waste** (5/6) — Manual processes consuming hours weekly
2. **Reliability** (4/6) — Current solution failing at critical moments

### Dominant Pull Forces
1. **Automation promise** (6/6) — Set it and forget it appeal
2. **Modern interface** (4/6) — Desire for "clean" experience

### Primary Anxieties
1. **Data migration** (5/6) — Fear of losing history
2. **Learning curve** (4/6) — Time investment concerns

### Strongest Habits
1. **Workflow familiarity** (4/6) — "I know where everything is"
2. **Team training** (3/6) — Sunk cost in current knowledge
```

## Examples

**Output: Complete Interview Synthesis**

```markdown
# Interview Synthesis: Accounting Software Switch

## Study Overview
- **Research question:** Why do SMBs switch accounting software?
- **Participants:** 6 small business owners
- **Method:** 45-60 minute JTBD interviews
- **Dates:** March 15-22, 2024

## Participant Summary
| Code | Business Type | Switched From | Switched To |
|------|--------------|---------------|-------------|
| P1 | Marketing agency | Spreadsheets | QuickBooks |
| P2 | E-commerce | Wave | Xero |
| P3 | Consulting | QuickBooks Desktop | QuickBooks Online |
| P4 | Restaurant | Paper/manual | Toast |
| P5 | Freelancer | Spreadsheets | FreshBooks |
| P6 | Retail | QuickBooks | Xero |

## Key Insights

### Insight 1: Tax Season is the Breaking Point
**Finding:** The trigger for switching is rarely gradual — it's tax season chaos.

**Evidence:**
> "Every April I swore I'd switch, but then I'd forget until next April" — P1
> "My accountant yelled at me. That was it." — P3
> "I missed a quarterly payment because I couldn't find the number" — P5

**Prevalence:** 5/6 participants

**So what:** Marketing should peak in Q4/Q1, messaging around "never have that tax panic again"

### Insight 2: The Fear is About History, Not Learning
**Finding:** Migration anxiety centers on losing historical data, not learning new software.

**Evidence:**
> "I can figure out any software. I can't recreate 5 years of books." — P2
> "What if something goes wrong and I can't prove my expenses?" — P4

**Prevalence:** 5/6 participants

**So what:** Migration guarantees and data verification features matter more than tutorials

### Insight 3: Recommendations from Accountants are Decisive
**Finding:** When an accountant recommends a switch, it happens within weeks.

**Evidence:**
> "She said 'you need to get on QuickBooks Online' and I did it that day" — P3
> "I trust him. If he says it's better, it's better." — P6

**Prevalence:** 3/6 participants (but 100% conversion when present)

**So what:** Accountant partnership/referral program could be highest-leverage channel

## Forces Summary

### Push Forces (Ranked by prevalence)
| Force | Count | Representative Quote |
|-------|-------|---------------------|
| Tax prep chaos | 5/6 | "I spent 20 hours just gathering numbers" |
| Manual entry errors | 4/6 | "I was always finding mistakes" |
| Desktop limitations | 3/6 | "I couldn't check from my phone" |

### Pull Forces (Ranked by prevalence)
| Force | Count | Representative Quote |
|-------|-------|---------------------|
| Bank sync automation | 6/6 | "It just pulls everything in" |
| Anywhere access | 5/6 | "I can invoice from my couch" |
| Accountant collaboration | 4/6 | "She can just log in and see" |

### Anxieties (Ranked by blocking power)
| Anxiety | Count | Mitigation Observed |
|---------|-------|---------------------|
| Data loss risk | 5/6 | Migration service, trial import |
| Learning time | 4/6 | "Surprisingly easy" post-switch |
| Cost increase | 3/6 | Feature value justification |

### Habits (Ranked by stickiness)
| Habit | Count | What Broke It |
|-------|-------|---------------|
| Spreadsheet comfort | 4/6 | Scaling complexity |
| Known workarounds | 3/6 | Workaround failure |
| Team familiarity | 2/6 | Champion evangelism |

## Recommendations

1. **Position around tax season relief** — Primary marketing message
2. **Lead with migration guarantee** — Address dominant anxiety
3. **Build accountant referral program** — Highest-trust channel
4. **De-emphasize feature tutorials** — Learning curve not the real barrier

## Questions for Further Research
- How do we reach people before April panic?
- What role does the accountant play in post-switch success?
- How does team size affect decision dynamics?
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

1. **Preserve participant voice** — Use their words in quotes
2. **Count everything** — Prevalence gives weight to findings
3. **Name the outliers** — Single-participant insights can still matter
4. **Separate observation from interpretation** — What they said vs what it means
5. **Connect to decisions** — Every insight should imply an action
6. **Track uncertainty** — Note what you're confident about vs speculating

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Quoteless insights | Ungrounded assertions | Every finding needs evidence |
| Single-source themes | Pattern needs prevalence | 3+ sources for a theme |
| Leading interpretation | Fitting data to hypothesis | Let codes emerge from data |
| Ignoring contradictions | Oversimplified findings | Note and explain divergence |
| Opinion synthesis | Paraphrasing changes meaning | Use direct quotes |
| Missing forces | Incomplete analysis | Map all four forces per participant |

## References

- thematic-analysis: Systematic coding methodology
- forces-analysis: Forces framework details
- moments-mapping: Force identification techniques
- interview-guide-design: Source interview structure
