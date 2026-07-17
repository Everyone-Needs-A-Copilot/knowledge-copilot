---
last_updated: 2026-02-25
status: active
name: contextual-inquiry
description: Observe users in their natural environment to understand real behaviors, workflows, and pain points. Use when assumptions about user behavior need validation, workflow mapping is required, or when traditional interviews miss tacit knowledge.
triggers:
  keywords: ["contextual", "inquiry", "observe", "users", "their", "natural", "environment", "understand", "real", "behaviors"]
allowed-tools: Read, Write, Edit
---

# Contextual Inquiry

## Overview

Conduct field research by observing users in their natural work environment while they perform real tasks. Captures tacit knowledge, workarounds, and environmental factors that users can't articulate in interviews.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Define Research Focus

Establish the inquiry scope:

| Element | Question to Answer |
|---------|-------------------|
| **Context** | What environment/situation are we studying? |
| **Tasks** | What specific activities should we observe? |
| **Users** | Who represents our target participants? |
| **Hypotheses** | What assumptions are we testing? |

### Step 2: Prepare for the Session

Create observation materials:
- **Discussion guide** — Key topics to explore (not a rigid script)
- **Observation form** — Structure for capturing notes
- **Recording consent** — Permission for notes/photos/video
- **Environment checklist** — Physical setup, tools, artifacts to note

### Step 3: Conduct the Inquiry

Follow the four principles of contextual inquiry:

| Principle | Description | In Practice |
|-----------|-------------|-------------|
| **Context** | Observe in the real environment | Go to their workspace, not a meeting room |
| **Partnership** | Collaborate as master-apprentice | "Teach me how you do this" |
| **Interpretation** | Share your understanding | "So it sounds like you're saying..." |
| **Focus** | Stay on research objectives | Redirect tangents back to key tasks |

### Step 4: Document Observations

Capture using the AEIOU framework:

| Category | What to Capture |
|----------|-----------------|
| **Activities** | Goal-directed actions and steps taken |
| **Environments** | Physical and digital workspace characteristics |
| **Interactions** | With people, tools, and systems |
| **Objects** | Artifacts, tools, documents used |
| **Users** | Roles, attitudes, values, needs |

### Step 5: Synthesize Findings

Transform raw observations into insights:
1. Identify patterns across sessions
2. Map workflow sequences
3. Note workarounds and pain points
4. Capture environmental influences
5. Document artifacts and tools

## Examples

**Output format:**
```markdown
## Contextual Inquiry: [Context/Task]

### Research Focus
- **Context:** [Environment studied]
- **Participants:** [Number and roles]
- **Sessions:** [Duration and dates]

### Key Observations

#### Workflow Map
[Sequential steps observed across participants]

#### Environmental Factors
| Factor | Impact on Work |
|--------|---------------|

#### Pain Points & Workarounds
| Pain Point | Workaround Used | Frequency |
|------------|-----------------|-----------|

### Artifacts Documented
[Photos, screenshots, documents collected]

### Key Insights
1. [Insight with supporting evidence]
2. [Insight with supporting evidence]
3. [Insight with supporting evidence]

### Design Implications
[How findings should influence design decisions]
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

- Always observe in the user's actual environment
- Follow the master-apprentice model — let users lead, you learn
- Interrupt to clarify, not to direct
- Document verbatim quotes for evidence
- Capture artifacts (photos, screenshots with permission)
- Note what users do, not just what they say

## Anti-Patterns

- Conducting sessions in conference rooms (loses context)
- Following a rigid interview script (misses emergent insights)
- Observing silently without interpretation sharing
- Focusing on opinions instead of behaviors
- Skipping artifact documentation

## References

- Beyer & Holtzblatt: Contextual Design methodology
- Nielsen Norman Group: Field Studies guidelines
