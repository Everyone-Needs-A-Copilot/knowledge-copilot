---
last_updated: 2026-02-25
status: active
name: usability-test-design
description: Design effective usability tests - task scenarios, success criteria, participant criteria, test protocols. Use for validating UX decisions.
triggers:
  files: ["**/research/**", "**/usability/**", "**/test-plan/**"]
  keywords: ["usability test", "user testing", "task scenario", "test protocol", "participant recruitment", "usability study"]
allowed-tools: Read, Write, Edit
---

# Usability Test Design Skill

Master guide for designing effective usability tests that reveal real user behavior and generate actionable insights.

## Philosophy

**Watch, don't ask.** Observing users struggle reveals more than surveys ever will. Behavior beats opinions.

**Test early, test often.** A paper sketch tested with 5 users beats a polished prototype never tested.

**5 users find 85% of problems.** You don't need hundreds of participants for qualitative insights.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Test Design Framework

### 1. Define Research Questions

Start with what you need to learn:

**Good research questions**:
- "Can users complete the checkout process?"
- "Where do users get confused in onboarding?"
- "Do users understand the pricing options?"

**Bad research questions**:
- "Is the design good?" (too vague)
- "Do users like the color?" (opinion, not behavior)
- "Will this increase conversions?" (A/B testing, not usability)

### 2. Choose Test Type

| Type | When to Use | Participants |
|------|-------------|--------------|
| Moderated | Early design, complex tasks | 5-8 |
| Unmoderated | Validation, specific tasks | 10-20 |
| Remote | Geographic diversity | 5-15 |
| In-person | Complex products, hardware | 5-8 |
| Guerrilla | Quick feedback, low budget | 3-5 |

### 3. Define Success Criteria

**Task-level success**:
- Completion rate (% who complete)
- Time on task
- Error rate
- Path deviation
- Assistance requests

**Study-level success**:
- Overall usability score (SUS)
- Critical issues found
- Severity ratings

---

## Task Scenario Design

### Anatomy of a Good Scenario

```
Context: [Realistic situation]
Goal: [What user wants to accomplish]
Starting point: [Where they begin]

Example:
"You want to buy a pair of running shoes for under $100.
You prefer Nike or Adidas brands. Find shoes that match
these criteria and add a pair to your cart."
```

### Scenario Guidelines

**Do**:
- Provide realistic context
- State goal, not steps
- Use user's language
- Be specific enough to evaluate
- Allow natural exploration

**Don't**:
- Give step-by-step instructions
- Use UI terminology ("click the hamburger menu")
- Lead users to answers
- Make scenarios too long

### Scenario Templates

**Discovery task**:
```
"You're interested in [category]. Explore the site
to understand what's available and find something
that interests you."
```

**Specific task**:
```
"You need to [specific goal]. Use this website/app
to accomplish this."
```

**Comparison task**:
```
"You're deciding between [option A] and [option B].
Find the information you need to make a decision."
```

**Recovery task**:
```
"You completed [action] but now need to [undo/change].
Figure out how to do this."
```

### Task Complexity Levels

**Simple** (warmup):
- 1-3 steps
- Clear success criteria
- Builds confidence
- "Find the contact page"

**Medium** (core tasks):
- 4-7 steps
- Main user journeys
- Where issues typically surface
- "Complete a purchase with a discount code"

**Complex** (stress test):
- 8+ steps
- Edge cases
- Advanced features
- "Create a custom report and schedule delivery"

---

## Participant Criteria

### Defining Your Participants

**Primary criteria** (must match):
- Target user characteristics
- Experience level with product
- Technical proficiency needed

**Secondary criteria** (nice to have):
- Demographic diversity
- Geographic location
- Device preferences

### Screener Questions

```markdown
## Screener: [Product Name] Usability Study

1. How often do you [relevant behavior]?
   - Never (DISQUALIFY)
   - Rarely
   - Monthly
   - Weekly
   - Daily

2. In the past 6 months, have you [relevant action]?
   - Yes
   - No (DISQUALIFY)

3. Which best describes your role?
   - [Target role 1]
   - [Target role 2]
   - Other (DISQUALIFY)

4. Please rate your comfort with technology:
   1-5 scale (set minimum threshold)
```

### Sample Size Guidelines

| Study Type | Participants | Rationale |
|------------|--------------|-----------|
| Formative (find issues) | 5-8 | 85% of issues found |
| Comparative (A vs B) | 10-15 per variant | Statistical comparison |
| Benchmark | 20+ | Reliable metrics |
| Segment testing | 5-8 per segment | Cover each segment |

---

## Test Protocol

### Session Structure

```
1. Introduction (5 min)
   - Welcome, thank you
   - Explain session purpose
   - Get consent
   - Explain think-aloud

2. Background questions (5 min)
   - Relevant experience
   - Current behavior
   - Expectations

3. Tasks (30-45 min)
   - 3-5 task scenarios
   - Observation
   - Follow-up questions

4. Post-task questionnaire (5 min)
   - Task ease ratings
   - Overall impressions

5. Debrief (5 min)
   - Open feedback
   - Clarifying questions
   - Thank you
```

### Introduction Script

```
"Thank you for participating today. We're testing
[product/feature], not you. There are no wrong
answers or mistakes.

I'll ask you to think aloud as you work - share
what you're looking at, thinking, and expecting.
If you get stuck, I may not be able to help, as
I want to see how the product works on its own.

Do you have any questions before we start?"
```

### Think-Aloud Prompts

During tasks, use neutral prompts:
- "What are you looking at?"
- "What are you thinking?"
- "What did you expect to happen?"
- "Tell me more about that."
- "What would you do next?"

**Avoid**:
- "Why did you click that?" (can seem judgmental)
- "Did you see the button?" (leads them)
- "Most people find it here" (primes behavior)

### Post-Task Questions

After each task:
- "How easy or difficult was that?" (1-7 scale)
- "What, if anything, was confusing?"
- "How would you expect this to work?"
- "Is there anything you'd change?"

---

## Materials Preparation

### Test Script Document

```markdown
# Usability Test Script

## Study Info
- Product: [Name]
- Version: [Version/Date]
- Researcher: [Name]
- Date: [Date]

## Research Questions
1. [Question 1]
2. [Question 2]

## Participant Criteria
- [Criterion 1]
- [Criterion 2]

## Equipment Needed
- [ ] Device with prototype
- [ ] Recording software
- [ ] Consent form
- [ ] Note-taking template

## Introduction
[Script text]

## Background Questions
1. [Question]
2. [Question]

## Task Scenarios

### Task 1: [Name]
**Scenario:** [Full scenario text]
**Starting point:** [URL/Screen]
**Success criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
**Observe:** [What to watch for]
**Follow-up questions:**
- [Question]

### Task 2: [Name]
[Same structure]

## Post-Task Questionnaire
[Questions]

## Debrief
- What was your overall impression?
- What stood out as particularly good or bad?
- Any final thoughts?
```

### Consent Form

Include:
- Study purpose (general)
- What participation involves
- Recording consent
- Voluntary participation
- Data handling
- Contact information

### Note-Taking Template

```markdown
# Session Notes

**Participant:** P[#]
**Date:** [Date]
**Researcher:** [Name]

## Background
- [Relevant info from intro questions]

## Task 1: [Name]
**Result:** ☐ Success ☐ Partial ☐ Fail
**Time:** [mm:ss]
**Path:** [Key steps taken]
**Observations:**
- [Observation 1]
- [Observation 2]
**Quotes:**
- "[Exact quote]"
**Issues:**
- [Issue description] - Severity: High/Med/Low

## Task 2: [Name]
[Same structure]

## Post-Test
**SUS Score:** [#]
**Overall feedback:**
- [Summary]

## Key Takeaways
- [Insight 1]
- [Insight 2]
```

---

## Common Test Types

### Formative Testing

**Purpose**: Find problems early
**When**: During design/development
**Participants**: 5-8
**Output**: Issue list with severity

### Benchmark Testing

**Purpose**: Establish metrics baseline
**When**: Before major redesign
**Participants**: 20+
**Output**: Quantitative metrics

### Comparative Testing

**Purpose**: Compare designs/competitors
**When**: Design decision needed
**Participants**: 10-15 per variant
**Output**: Which performs better

### First-Click Testing

**Purpose**: Test navigation/findability
**When**: IA or navigation changes
**Participants**: 20-50
**Output**: % correct first clicks

---

## Metrics to Collect

### Task Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Completion rate | Successes / Attempts | > 80% |
| Time on task | End - Start | Depends on task |
| Error rate | Errors / Tasks | < 10% |
| Lostness | (N-S)/(N-S) | < 0.4 |

### System Usability Scale (SUS)

10 questions, 5-point scale:
1. I think I would like to use this frequently
2. I found it unnecessarily complex
3. I thought it was easy to use
4. I would need help to use this
5. I found functions well integrated
6. I thought there was too much inconsistency
7. Most people would learn quickly
8. I found it very awkward to use
9. I felt confident using it
10. I needed to learn a lot before I could use this

**Score interpretation**:
- 68: Average
- < 50: Poor
- > 80: Excellent

### Single Ease Question (SEQ)

"How easy or difficult was this task?"
1 (Very Difficult) to 7 (Very Easy)

Average > 5.5 indicates acceptable ease

---

## Pilot Testing

Before real sessions:

### Pilot Checklist

- [ ] Run through entire protocol
- [ ] Check recording works
- [ ] Time each section
- [ ] Test scenarios are clear
- [ ] Starting points work
- [ ] No broken features
- [ ] Questions flow naturally
- [ ] Task order makes sense

### What to Adjust

After pilot:
- Clarify confusing scenarios
- Adjust timing
- Fix technical issues
- Refine questions
- Add/remove tasks

---

## Quick Reference

### Test Design Checklist

- [ ] Research questions defined
- [ ] Test type selected
- [ ] Participant criteria set
- [ ] Screener created
- [ ] 3-5 task scenarios written
- [ ] Success criteria defined
- [ ] Protocol scripted
- [ ] Materials prepared
- [ ] Consent form ready
- [ ] Pilot test completed

### Scenario Quality Checklist

- [ ] Provides realistic context
- [ ] States goal, not steps
- [ ] Uses user language
- [ ] Doesn't lead user
- [ ] Has clear success criteria
- [ ] Takes appropriate time

### Facilitation Reminders

- Let silence happen
- Don't help (observe struggle)
- Use neutral prompts
- Note non-verbal cues
- Capture exact quotes
- Follow up on confusion

---

## Summary

**Good test design = Actionable insights**

1. Start with clear research questions
2. Write realistic task scenarios
3. Recruit representative participants
4. Prepare detailed protocol
5. Pilot before real sessions
6. Observe behavior, not opinions

*Testing with 5 users early beats testing with 50 users late.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

