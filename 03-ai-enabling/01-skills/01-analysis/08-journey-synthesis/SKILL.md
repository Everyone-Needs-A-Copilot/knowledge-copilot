---
last_updated: 2026-02-25
status: active
name: journey-synthesis
description: Create evidence-based customer journey maps from research data. Map stages, touchpoints, emotions, and forces at each step. Use after interviews or behavioral analysis to visualize the complete customer experience.
triggers:
  keywords: ["journey", "synthesis", "create", "evidence-based", "customer", "maps", "research", "data", "stages", "touchpoints"]
allowed-tools: Read, Write, Edit
---

# Journey Synthesis

## Overview

Transform research findings into structured journey maps that show the complete customer experience. Maps stages, touchpoints, actions, emotions, and pain points with evidence from real user data. Produces actionable artifacts grounded in research, not assumptions.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Define Journey Scope

Clarify what journey you're mapping:

| Scope Element | Question to Answer |
|---------------|-------------------|
| **Journey type** | End-to-end experience or specific episode? |
| **Actor** | Whose journey is this? |
| **Starting point** | When does the journey begin? |
| **Ending point** | When is the journey "complete"? |
| **Data sources** | What evidence will inform the map? |

```markdown
## Journey Scope

**Journey:** [Name]
**Actor:** [Who — persona or segment]
**Trigger:** [What starts the journey]
**Goal:** [What they're trying to achieve]
**End state:** [How we know they're done]

**Data sources:**
- [Source 1]: [n= or description]
- [Source 2]: [n= or description]
```

### Step 2: Identify Journey Stages

Break journey into major phases:

| Stage Type | Characteristics |
|------------|-----------------|
| **Awareness** | Realizes need exists |
| **Consideration** | Evaluates options |
| **Decision** | Makes choice |
| **Onboarding** | Gets started |
| **Usage** | Uses product/service |
| **Growth** | Expands usage |
| **Renewal/Churn** | Continues or leaves |

```markdown
## Journey Stages

| Stage | Description | Key Question User Has |
|-------|-------------|----------------------|
| 1. [Stage name] | [What happens] | "[User question]" |
| 2. [Stage name] | [What happens] | "[User question]" |
| 3. [Stage name] | [What happens] | "[User question]" |
```

### Step 3: Map Touchpoints per Stage

Identify every interaction point:

| Touchpoint Category | Examples |
|---------------------|----------|
| **Digital** | Website, app, email, chat |
| **Human** | Sales, support, success |
| **Physical** | Office, event, mail |
| **Partner** | Reseller, integrations, reviews |

```markdown
## Touchpoints

### Stage: [Stage Name]
| Touchpoint | Channel | Owner | Evidence |
|------------|---------|-------|----------|
| [Touchpoint 1] | [Channel] | [Team] | P1, P3, P5 mention |
| [Touchpoint 2] | [Channel] | [Team] | Analytics shows 80% |
```

### Step 4: Document Actions and Goals

What is the user doing and trying to achieve at each stage?

```markdown
## User Actions

### Stage: [Stage Name]

**User goal:** [What they're trying to accomplish]

**Actions:**
1. [Action]: [Evidence]
2. [Action]: [Evidence]

**Jobs to be done:**
- Functional: [What task]
- Emotional: [How want to feel]
- Social: [How want to appear]
```

### Step 5: Map Emotional Journey

Track sentiment through the experience:

| Emotion Level | Indicators |
|---------------|------------|
| **High/Positive** | Delight, surprise, relief, confidence |
| **Neutral** | Functional, expected, unremarkable |
| **Low/Negative** | Frustration, confusion, anxiety, anger |

```markdown
## Emotional Arc

| Stage | Emotion | Level (-3 to +3) | Evidence |
|-------|---------|------------------|----------|
| [Stage 1] | [Emotion] | [Rating] | "[Quote]" — P3 |
| [Stage 2] | [Emotion] | [Rating] | "[Quote]" — P1 |
```

### Step 6: Identify Pain Points and Opportunities

Flag problems and improvement areas:

```markdown
## Pain Points

### Stage: [Stage Name]

| Pain Point | Severity | Frequency | Evidence |
|------------|----------|-----------|----------|
| [Pain point 1] | High/Med/Low | X/Y users | "[Quote]" |
| [Pain point 2] | High/Med/Low | X/Y users | "[Quote]" |

### Opportunities
| Opportunity | Stage | Potential Impact |
|-------------|-------|------------------|
| [Opportunity 1] | [Stage] | [What improves] |
```

### Step 7: Apply Forces Framework

Map forces at key decision points:

```markdown
## Forces at [Decision Stage]

### Push (away from status quo)
- [Force]: [Evidence]

### Pull (toward new solution)
- [Force]: [Evidence]

### Anxiety (about change)
- [Force]: [Evidence]

### Habit (staying put)
- [Force]: [Evidence]

**Net force direction:** [Toward change / Status quo / Balanced]
```

### Step 8: Create Journey Map Artifact

Synthesize into visual/tabular format:

```markdown
## Journey Map: [Journey Name]

| Layer | Stage 1: [Name] | Stage 2: [Name] | Stage 3: [Name] | Stage 4: [Name] |
|-------|-----------------|-----------------|-----------------|-----------------|
| **User Goal** | [Goal] | [Goal] | [Goal] | [Goal] |
| **Actions** | [Actions] | [Actions] | [Actions] | [Actions] |
| **Touchpoints** | [Touchpoints] | [Touchpoints] | [Touchpoints] | [Touchpoints] |
| **Emotions** | [Rating + emoji] | [Rating + emoji] | [Rating + emoji] | [Rating + emoji] |
| **Pain Points** | [Pain points] | [Pain points] | [Pain points] | [Pain points] |
| **Opportunities** | [Opportunities] | [Opportunities] | [Opportunities] | [Opportunities] |
```

## Examples

**Output: Complete Journey Map**

```markdown
# Customer Journey Map: SaaS Evaluation to Conversion

## Journey Scope
**Journey:** First-time buyer evaluation and purchase
**Actor:** IT Manager at mid-market company (100-500 employees)
**Trigger:** Current tool causing problems or contract coming up for renewal
**Goal:** Find and implement better solution
**End state:** Successfully deployed, team trained, measuring ROI

**Data sources:**
- Customer interviews: n=15 recent buyers
- Lost deal interviews: n=8 non-buyers
- Product analytics: 5,000 trial users
- Sales call recordings: 25 calls

---

## Stage 1: Problem Recognition

**User goal:** Confirm the current situation is unacceptable

**Actions:**
- Notices recurring issues with current tool
- Documents complaints from team
- Calculates time/money lost to problems
- Brings concerns to leadership

**Touchpoints:**
| Touchpoint | Channel | Evidence |
|------------|---------|----------|
| Team complaints | Internal | 12/15 buyers cite team frustration |
| Error logs | Current system | 9/15 mention specific failures |
| Competitor mentions | Word of mouth | 8/15 heard about alternatives |

**Emotions:**
- Dominant: Frustration, hesitation
- Level: -2
- Quote: "I knew something had to change but dreaded the migration project" — P7

**Forces at play:**
- **Push:** Tool failures costing real money, team threatening to quit
- **Habit:** "At least I know how this one breaks" — P4

**Pain points:**
| Pain Point | Severity | Frequency |
|------------|----------|-----------|
| Can't quantify cost of status quo | High | 11/15 |
| Unclear if leadership will approve | Medium | 8/15 |

---

## Stage 2: Solution Research

**User goal:** Understand what options exist

**Actions:**
- Google searches for alternatives
- Reads G2/Capterra reviews
- Asks network for recommendations
- Visits 3-5 vendor websites

**Touchpoints:**
| Touchpoint | Channel | Evidence |
|------------|---------|----------|
| G2/Capterra | Third-party | 14/15 used review sites |
| Google search | Web | 15/15 searched |
| LinkedIn asks | Social | 6/15 posted or messaged |
| Vendor websites | Web | 15/15 visited 3+ sites |

**Emotions:**
- Dominant: Overwhelmed, curious
- Level: 0 (neutral)
- Quote: "There are so many options that all sound the same" — P2

**Pain points:**
| Pain Point | Severity | Frequency |
|------------|----------|-----------|
| Vendors sound identical | High | 12/15 |
| Hard to know what features matter | Medium | 9/15 |
| Reviews seem fake/outdated | Medium | 7/15 |

**Opportunities:**
- Differentiated positioning that doesn't rely on feature lists
- Updated social proof with verifiable case studies

---

## Stage 3: Evaluation

**User goal:** Narrow to 2-3 real options and test them

**Actions:**
- Signs up for trials/demos
- Builds evaluation criteria spreadsheet
- Involves additional stakeholders
- Tests with real workflows

**Touchpoints:**
| Touchpoint | Channel | Evidence |
|------------|---------|----------|
| Free trial | Product | 12/15 started trial |
| Sales demo | Human | 11/15 attended demo |
| Technical deep-dive | Human | 8/15 had technical call |
| Stakeholder meetings | Internal | 15/15 involved others |

**Emotions:**
- Dominant: Anxiety, cautious optimism
- Level: -1 to +1 (varies)
- Quote: "I could see it working for us, but I kept thinking about what could go wrong" — P9

**Forces at play:**
- **Pull:** "The demo looked so clean compared to our current mess" — P11
- **Anxiety:** "What if my data doesn't migrate correctly?" — P3 (10/15 share concern)
- **Habit:** "My team has muscle memory for the old system" — P6

**Pain points:**
| Pain Point | Severity | Frequency |
|------------|----------|-----------|
| Trial too short to properly test | High | 9/15 |
| Can't test with real data | High | 11/15 |
| Getting stakeholder time | Medium | 8/15 |

**Opportunities:**
- Extended trial with migration preview
- Pre-built evaluation criteria template

---

## Stage 4: Decision

**User goal:** Get approval and make final choice

**Actions:**
- Presents recommendation to leadership
- Negotiates pricing/contract
- Addresses final concerns
- Signs agreement

**Touchpoints:**
| Touchpoint | Channel | Evidence |
|------------|---------|----------|
| Proposal/quote | Email/Doc | 15/15 received quote |
| Executive sponsor call | Human | 7/15 requested |
| Legal/security review | Internal | 12/15 required |
| Contract signing | Digital | 15/15 |

**Emotions:**
- Dominant: Relief, nervousness
- Level: +1
- Quote: "I was relieved to finally decide, but nervous about whether I made the right call" — P14

**Pain points:**
| Pain Point | Severity | Frequency |
|------------|----------|-----------|
| Pricing not transparent | High | 10/15 |
| Security review delays | Medium | 8/15 |
| Long contract negotiation | Medium | 6/15 |

**Lost deal insights (n=8):**
| Reason | Frequency | Quote |
|--------|-----------|-------|
| Couldn't justify ROI | 4/8 | "Leadership wanted harder numbers" |
| Security concerns | 2/8 | "Failed our security review" |
| Champion left | 2/8 | "New person had different preference" |

---

## Stage 5: Implementation

**User goal:** Get up and running without disrupting team

**Actions:**
- Completes onboarding checklist
- Migrates data
- Configures for team workflows
- Trains team members

**Touchpoints:**
| Touchpoint | Channel | Evidence |
|------------|---------|----------|
| Onboarding email sequence | Email | 15/15 received |
| Implementation specialist | Human | 10/15 assigned |
| Documentation/help center | Web | 15/15 used |
| Training sessions | Virtual | 8/15 attended |

**Emotions:**
- Dominant: Stressed, determined
- Level: -1
- Quote: "The next two weeks were rough. I was basically doing two jobs." — P5

**Pain points:**
| Pain Point | Severity | Frequency |
|------------|----------|-----------|
| Migration issues | High | 9/15 experienced |
| Team resistance | High | 7/15 faced |
| Missing documentation | Medium | 8/15 mentioned |

**Opportunities:**
- White-glove migration service (even if paid)
- Change management toolkit for team buy-in

---

## Summary Journey Map

| Layer | Recognition | Research | Evaluation | Decision | Implementation |
|-------|-------------|----------|------------|----------|----------------|
| **Goal** | Confirm need | Know options | Test fit | Get approval | Get running |
| **Emotions** | Frustrated (-2) | Overwhelmed (0) | Anxious (-1) | Relieved (+1) | Stressed (-1) |
| **Top Pain** | Can't quantify | All sound same | Can't test real | Pricing unclear | Migration issues |
| **Opportunity** | ROI calculator | Differentiation | Extended trial | Transparent pricing | Migration service |

---

## Strategic Recommendations

1. **Biggest drop-off:** Evaluation → Decision (lost deals cite ROI justification)
   - Action: Create ROI calculator and business case template

2. **Highest anxiety:** Migration concerns (10/15 mention)
   - Action: Offer data migration preview in trial

3. **Biggest pain:** Implementation difficulty (9/15 issues)
   - Action: Productize implementation support, don't leave to chance

4. **Differentiation opportunity:** Research stage ("all sound same")
   - Action: Lead with outcomes, not features
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

1. **Evidence over assumption** — Every element needs supporting data
2. **Quote the user** — Real words are more powerful than summaries
3. **Show prevalence** — Note how common each finding is
4. **Map emotions honestly** — Not every stage is delightful
5. **Connect to action** — Every pain point should suggest improvement
6. **Involve stakeholders** — Journey maps are communication tools

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Happy path only | Misses real friction | Include pain points and failures |
| Assumption-based | Not grounded in research | Cite evidence for every element |
| Too many stages | Overwhelming, not actionable | 4-7 stages typically |
| Missing emotions | Dry, not compelling | Always include emotional layer |
| No prioritization | Everything seems equal | Flag severity and frequency |
| Static artifact | Gets outdated | Build update cadence |

## References

- interview-synthesis: Extracting journey data from interviews
- touchpoint-analysis: Deep-dive on specific touchpoints
- pattern-recognition: Finding patterns across journeys
