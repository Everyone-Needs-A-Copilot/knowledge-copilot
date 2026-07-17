---
last_updated: 2026-02-25
status: active
name: research-design
description: Design mixed-methods research studies that answer business questions with appropriate rigor. Select methods, sample sizes, and timelines. Use when planning research initiatives that require both qualitative depth and quantitative breadth.
triggers:
  keywords: ["research", "design", "mixed-methods", "studies", "answer", "business", "questions", "appropriate", "rigor", "select"]
allowed-tools: Read, Write, Edit
---

# Research Design

## Overview

Plan research studies that answer the right questions with the right methods. Match method to question, determine appropriate sample sizes, and create realistic timelines. Produces research plans that balance rigor with business constraints.


## Define Done

- [ ] Strategic situation assessed with evidence from multiple sources
- [ ] Key forces and dynamics identified and prioritized
- [ ] Recommendations account for constraints and trade-offs
- [ ] Action plan has clear owners and timelines

## Instructions

### Step 1: Define Research Objectives

Start with what you need to learn, not how you'll learn it:

| Objective Element | Question |
|-------------------|----------|
| **Core question** | What is the single most important thing to understand? |
| **Decision it informs** | What will change based on findings? |
| **Success criteria** | What would a useful answer look like? |
| **Assumptions to test** | What do we believe that might be wrong? |

```markdown
## Research Objectives

**Core question:** [Single sentence]

**Business decision:** [What this research informs]

**Success criteria:**
- [ ] We will know [specific thing]
- [ ] We can confidently decide [specific choice]

**Assumptions to validate:**
1. [Assumption 1]: [Current belief]
2. [Assumption 2]: [Current belief]
```

### Step 2: Choose Research Approach

Match approach to question type:

| Question Type | Best Approach | Methods |
|---------------|---------------|---------|
| **What?** (Descriptive) | Quantitative | Surveys, analytics |
| **How many?** | Quantitative | Surveys, analytics |
| **Why?** (Explanatory) | Qualitative | Interviews, observation |
| **How?** (Process) | Qualitative | Interviews, diary studies |
| **What + Why?** | Mixed methods | Quant → Qual or Qual → Quant |

```markdown
## Research Approach

**Primary question type:** [What/Why/How/Mixed]
**Approach:** [Quantitative/Qualitative/Mixed]

**Rationale:** [Why this approach fits]
```

### Step 3: Design Method Sequence

For mixed methods, plan the sequence:

| Sequence | When to Use | Example |
|----------|-------------|---------|
| **Qual → Quant** | Explore then validate | Interviews to find themes → Survey to measure prevalence |
| **Quant → Qual** | Identify then explain | Analytics to find pattern → Interviews to understand why |
| **Parallel** | When independent | Survey and interviews run simultaneously |
| **Embedded** | Depth within breadth | Survey with open-ended follow-up |

```markdown
## Method Sequence

### Phase 1: [Method]
- **Purpose:** [What this phase answers]
- **Inputs:** [What you need to start]
- **Outputs:** [What this produces for next phase]
- **Timeline:** [Duration]

### Phase 2: [Method]
- **Purpose:** [What this phase answers]
- **Inputs:** [From Phase 1]
- **Outputs:** [Final deliverables]
- **Timeline:** [Duration]
```

### Step 4: Determine Sample Requirements

Right-size your sample:

| Method | Sample Size Guidance |
|--------|---------------------|
| **Interviews (exploratory)** | 8-12 for initial themes |
| **Interviews (saturation)** | 15-30 until no new themes |
| **Usability testing** | 5-8 per distinct user group |
| **Surveys (descriptive)** | 100+ for stable percentages |
| **Surveys (comparative)** | 200-400 per group |
| **A/B tests** | Calculate based on effect size |

```markdown
## Sample Design

### Target Population
[Who the research is about]

### Sampling Strategy
| Criterion | Requirement | Rationale |
|-----------|-------------|-----------|
| [Criterion 1] | [Spec] | [Why] |
| [Criterion 2] | [Spec] | [Why] |

### Sample Size
| Method | Size | Rationale |
|--------|------|-----------|
| [Method 1] | n=X | [Why this number] |
| [Method 2] | n=X | [Why this number] |

### Recruitment Approach
[How you'll find participants]
```

### Step 5: Plan Data Collection

Specify what you'll collect and how:

```markdown
## Data Collection Plan

### Method 1: [e.g., Interviews]

**Instrument:** [Interview guide / Survey / etc.]
**Duration:** [Time per participant]
**Recording:** [How data is captured]
**Scheduling:** [How sessions are booked]

**Key topics/questions:**
1. [Topic 1]
2. [Topic 2]

### Method 2: [e.g., Survey]

**Platform:** [Tool used]
**Length:** [Number of questions, estimated time]
**Distribution:** [How sent to participants]
**Incentive:** [Compensation if any]

**Key measures:**
| Construct | Question Type | Scale |
|-----------|---------------|-------|
| [Construct 1] | [Type] | [Scale] |
```

### Step 6: Plan Analysis

Define how you'll make sense of data:

```markdown
## Analysis Plan

### Qualitative Analysis
- **Approach:** [Thematic analysis / Grounded theory / etc.]
- **Coding:** [How codes are developed]
- **Validation:** [Inter-rater reliability, member checking]

### Quantitative Analysis
- **Descriptive:** [Frequencies, means, distributions]
- **Comparative:** [Tests to use, e.g., t-test, chi-square]
- **Significance level:** [α = 0.05 typically]

### Integration
[How qual and quant findings combine]
```

### Step 7: Create Timeline and Budget

Make it actionable:

```markdown
## Project Timeline

| Phase | Activities | Duration | Dates |
|-------|------------|----------|-------|
| Design | Finalize plan, create instruments | 1 week | [Dates] |
| Recruitment | Screen, schedule participants | 2 weeks | [Dates] |
| Collection | Run interviews/launch survey | 3 weeks | [Dates] |
| Analysis | Code, analyze, synthesize | 2 weeks | [Dates] |
| Reporting | Create deliverables | 1 week | [Dates] |

**Total duration:** X weeks

## Budget

| Item | Cost | Notes |
|------|------|-------|
| Participant incentives | $X | $Y × Z participants |
| Tools/software | $X | [Platform costs] |
| Recruitment | $X | [If using panel] |
| **Total** | **$X** | |
```

## Examples

**Output: Complete Research Design**

```markdown
# Research Design: Understanding Enterprise Buying Process

## Research Objectives

**Core question:** What drives enterprise IT purchasing decisions for collaboration tools?

**Business decision:** Whether to invest in enterprise sales motion and which capabilities to prioritize

**Success criteria:**
- [ ] Understand typical buying journey stages and timeline
- [ ] Identify key stakeholders and their criteria
- [ ] Know top 5 decision factors ranked by importance
- [ ] Understand why deals are won vs lost

**Assumptions to validate:**
1. Price is secondary to functionality for enterprise
2. IT has veto power over end-user preferences
3. Security/compliance is table stakes, not differentiator

---

## Research Approach

**Primary question type:** Why + How much (Mixed)
**Approach:** Mixed methods (Qual → Quant)

**Rationale:** Need qualitative depth to understand decision process (why), then quantitative validation to confirm prevalence (how many).

---

## Method Sequence

### Phase 1: Qualitative Discovery
**Method:** In-depth interviews
**Purpose:** Map buying journey, identify decision factors, understand stakeholder dynamics
**Sample:** 15 enterprise buyers (mix of won/lost deals)
**Outputs:**
- Draft buying journey map
- Preliminary decision factor list
- Stakeholder role definitions

### Phase 2: Quantitative Validation
**Method:** Survey
**Purpose:** Validate journey stages, quantify factor importance, segment by company size
**Sample:** 200 enterprise IT decision-makers
**Outputs:**
- Decision factor ranking with confidence intervals
- Journey stage prevalence
- Segment differences

---

## Sample Design

### Phase 1: Interviews

**Target population:** IT leaders who evaluated collaboration tools in past 12 months

**Sampling criteria:**
| Criterion | Requirement | Rationale |
|-----------|-------------|-----------|
| Company size | 500-5,000 employees | Enterprise segment |
| Role | Director+ in IT | Decision authority |
| Recency | Evaluated in past 12 months | Memory accuracy |
| Outcome | Mix of 8 buyers, 7 non-buyers | Understand both |

**Sample size:** n=15
- Targeting saturation at ~12, buffer for no-shows
- Mix: 8 who purchased (any vendor), 7 who didn't purchase

**Recruitment:**
- Partner with sales team for recent deal contacts
- Supplement with LinkedIn outreach
- $150 Amazon gift card incentive

### Phase 2: Survey

**Target population:** Same as Phase 1

**Sample size:** n=200
- Allows ±7% margin of error at 95% confidence
- Sufficient for 2-3 segment comparisons

**Recruitment:**
- B2B panel provider (Respondent.io or similar)
- Screener to verify role and recency
- $25 incentive

---

## Data Collection Plan

### Phase 1: Interview Protocol

**Duration:** 45-60 minutes
**Format:** Video call, recorded with permission
**Instrument:** Semi-structured interview guide

**Key topics:**
1. Buying journey: Trigger, research, evaluation, decision
2. Stakeholders: Who involved, who has veto, who influences
3. Decision factors: What mattered most, deal breakers
4. Competitive: What alternatives considered, why chosen/rejected
5. Process: Timeline, procurement requirements, security review

**Documentation:**
- Audio recording → professional transcription
- Observer notes during interview

### Phase 2: Survey Design

**Platform:** Typeform
**Length:** 25 questions, ~10 minutes
**Structure:**

| Section | Questions | Type |
|---------|-----------|------|
| Screener | 4 | Multiple choice |
| Journey stages | 6 | Likert + multiple choice |
| Decision factors | 8 | Max-diff + ranking |
| Stakeholders | 4 | Multiple choice + matrix |
| Demographics | 3 | Multiple choice |

**Key measures:**
| Construct | Method | Scale |
|-----------|--------|-------|
| Factor importance | Max-diff | 10 factors, 5 per set |
| Journey duration | Categorical | Time ranges |
| Stakeholder influence | Matrix | Roles × Influence level |

---

## Analysis Plan

### Phase 1: Qualitative

**Approach:** Thematic analysis (Braun & Clarke)
**Process:**
1. Transcribe all interviews
2. First-pass familiarization read
3. Initial coding (2 researchers independently)
4. Discuss and consolidate codes
5. Develop themes from codes
6. Review themes against data
7. Create journey map artifact

**Validation:**
- Inter-rater reliability on 3 transcripts
- Member check with 3 participants

### Phase 2: Quantitative

**Descriptive:**
- Factor importance scores (from max-diff)
- Journey stage frequencies
- Stakeholder involvement patterns

**Comparative:**
- Buyers vs non-buyers: Chi-square for categorical, t-test for continuous
- Company size segments: ANOVA for factor importance

**Significance level:** α = 0.05

### Integration

Qual findings guide survey design (factors identified become survey items). Survey validates qual prevalence. Final synthesis presents journey map with quantified confidence.

---

## Timeline

| Phase | Activities | Duration | Dates |
|-------|------------|----------|-------|
| Design | Finalize interview guide, pilot | 1 week | Week 1 |
| Interview recruitment | Recruit 15 participants | 2 weeks | Weeks 2-3 |
| Interviews | Conduct 15 interviews | 3 weeks | Weeks 3-5 |
| Qual analysis | Transcribe, code, theme | 2 weeks | Weeks 6-7 |
| Survey design | Build survey from qual findings | 1 week | Week 8 |
| Survey fielding | Launch, monitor, close | 2 weeks | Weeks 9-10 |
| Quant analysis | Analyze survey data | 1 week | Week 11 |
| Synthesis | Integrate findings, create deliverables | 1 week | Week 12 |

**Total duration:** 12 weeks

---

## Budget

| Item | Cost | Notes |
|------|------|-------|
| Interview incentives | $2,250 | $150 × 15 |
| Transcription | $900 | ~$60/interview |
| Survey panel | $3,000 | ~$15/complete × 200 |
| Survey incentives | $5,000 | $25 × 200 |
| Tools (Typeform, Dovetail) | $300 | Monthly subscriptions |
| **Total** | **$11,450** | |

---

## Deliverables

1. **Research report:** Full findings document
2. **Buying journey map:** Visual artifact with stages, touchpoints, emotions
3. **Decision factor ranking:** Quantified priorities with confidence intervals
4. **Segment profiles:** Key differences by company size
5. **Recommendations:** Strategic implications for enterprise GTM

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Recruitment difficulty | Medium | High | Start early, use multiple channels |
| Low survey response | Medium | Medium | Longer field time, higher incentive |
| Qual-quant mismatch | Low | Medium | Pilot survey with qual participants |
```



## Quality Tests

### Evidence Test
- Strategy is grounded in data and observations, not assumptions
- **PASS:** Each strategic recommendation traces to specific evidence
- **FAIL:** Strategy based on intuition without supporting data

### Completeness Test
- All relevant forces and stakeholders have been considered
- **PASS:** Analysis covers internal, external, and competitive dynamics
- **FAIL:** Only internal factors considered, external forces ignored

## Guidelines

1. **Start with the decision** — Research without decision is just curiosity
2. **Match method to question** — Why needs qual, how many needs quant
3. **Plan analysis upfront** — Know how you'll analyze before collecting
4. **Build in flexibility** — Research often reveals unexpected questions
5. **Document everything** — Methods section enables replication
6. **Consider constraints** — Time and budget are real

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Solution-first | "We need a survey" before knowing question | Start with research question |
| Undersized samples | Qualitative too small, quantitative underpowered | Follow sample guidance |
| Method misalignment | Survey for "why" questions | Match method to question type |
| Analysis afterthought | Figuring out analysis after data collected | Pre-plan analysis |
| Scope creep | Adding questions mid-study | Lock scope, save new questions |
| Single-method | Only qual OR only quant | Mixed methods when appropriate |

## References

- interview-guide-design: Qualitative instrument design
- statistical-analysis: Quantitative analysis methods
- research-ethics: Ethical considerations
- pattern-recognition: Cross-method triangulation
