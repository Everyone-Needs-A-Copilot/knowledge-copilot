---
last_updated: 2026-02-25
status: active
name: design-critique
description: Evaluate designs objectively against principles, providing constructive feedback. Use when reviewing designs, conducting design reviews, or providing feedback.
triggers:
  files: ["**/design/**", "**/mockup/**", "**/prototype/**", "**/ui/**"]
  keywords: ["design review", "critique", "feedback", "design evaluation", "design assessment", "design quality"]
allowed-tools: Read, Write, Edit
---

# Design Critique

Design critique evaluates work against established principles to identify improvements. Effective critique is specific, actionable, and grounded in objective criteria rather than personal preference.

## Core Principle

**Critique the work, not the designer.** Focus on how well the design achieves its goals, not on taste or style.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Critique Framework

### The Four Lenses

Evaluate every design through these four perspectives:

| Lens | Question | Focus |
|------|----------|-------|
| **Function** | Does it work? | Usability, task completion, error prevention |
| **Form** | Does it communicate? | Hierarchy, clarity, visual language |
| **Fit** | Does it belong? | Brand alignment, consistency, context |
| **Feel** | Does it resonate? | Emotion, delight, personality |

### Structured Critique Process

1. **Understand context** - Goals, constraints, audience
2. **Observe first** - Note initial impressions without judgment
3. **Analyze systematically** - Apply each lens
4. **Prioritize feedback** - Critical issues before polish
5. **Suggest alternatives** - Don't just identify problems

## Evaluation Criteria

### Usability Assessment

| Criterion | Questions |
|-----------|-----------|
| Learnability | Can new users accomplish basic tasks? |
| Efficiency | Can experienced users complete tasks quickly? |
| Memorability | Can returning users remember how to use it? |
| Error tolerance | Does it prevent errors? Help recovery? |
| Satisfaction | Is it pleasant to use? |

### Visual Design Assessment

| Criterion | Questions |
|-----------|-----------|
| Hierarchy | Is importance clear? One focal point per section? |
| Alignment | Are elements properly aligned? Consistent grid? |
| Repetition | Are patterns consistent? Visual language coherent? |
| Contrast | Is there clear distinction between elements? |
| Proximity | Are related items grouped? Unrelated items separated? |
| Balance | Does the composition feel stable? |
| White space | Is there breathing room? Not cramped? |

### Interaction Design Assessment

| Criterion | Questions |
|-----------|-----------|
| Affordance | Is it clear what's clickable/interactive? |
| Feedback | Do actions have visible results? |
| Mapping | Do controls relate logically to their effects? |
| Consistency | Do similar elements behave similarly? |
| Constraint | Are impossible/dangerous actions prevented? |

## Critique Language

### Constructive Phrasing

| Instead of | Say |
|------------|-----|
| "I don't like this" | "This doesn't achieve [specific goal] because..." |
| "It's confusing" | "Users might struggle to find X because..." |
| "Make it pop" | "The hierarchy could be stronger if..." |
| "It feels off" | "The alignment creates tension here because..." |
| "That's wrong" | "This pattern typically causes [problem] - consider..." |

### Feedback Structure

For each issue, provide:

```
[OBSERVATION] What you see
[IMPACT] Why it matters / What problem it causes
[SUGGESTION] How to improve it
```

**Example:**
```
[OBSERVATION] The primary CTA and secondary button have similar visual weight.
[IMPACT] Users may hesitate about which action to take, reducing conversion.
[SUGGESTION] Increase contrast - filled button for primary, outline for secondary.
```

## Priority Framework

Rank issues by severity:

| Priority | Impact | Examples |
|----------|--------|----------|
| P0 - Critical | Blocks task completion | Broken flow, missing elements |
| P1 - Major | Significantly harms UX | Confusing navigation, poor contrast |
| P2 - Minor | Causes friction | Inconsistent spacing, alignment issues |
| P3 - Polish | Nice to have | Micro-interactions, animation refinement |

## Design Principles Checklist

### Layout & Composition
- [ ] Clear visual hierarchy
- [ ] Consistent grid/spacing system
- [ ] Appropriate white space
- [ ] Balanced composition
- [ ] Clear content grouping

### Typography
- [ ] Readable body text (16px+ on web)
- [ ] Clear heading hierarchy
- [ ] Appropriate line height (1.4-1.6)
- [ ] Manageable line length (45-75 chars)
- [ ] Maximum 2-3 font families

### Color
- [ ] Accessible contrast ratios (4.5:1 AA)
- [ ] Consistent color usage
- [ ] Color supports meaning (not sole indicator)
- [ ] Works in dark/light modes
- [ ] Color-blind friendly

### Interaction
- [ ] Clear interactive affordances
- [ ] Visible feedback for actions
- [ ] Touch targets 44px+ on mobile
- [ ] Focus states visible
- [ ] Error states helpful

### Consistency
- [ ] Matches design system
- [ ] Consistent patterns throughout
- [ ] Follows platform conventions
- [ ] Aligns with brand guidelines

## Giving Feedback

### The Praise-Question-Suggestion Model

1. **Praise** - Start with what's working
2. **Question** - Ask about intent to understand decisions
3. **Suggestion** - Offer specific improvements

### Do's and Don'ts

| Do | Don't |
|----|-------|
| Be specific and objective | Be vague or personal |
| Explain the "why" | Just say "change this" |
| Offer alternatives | Only point out problems |
| Prioritize feedback | Overwhelm with every issue |
| Focus on user impact | Focus on personal preference |
| Ask clarifying questions | Assume you know intent |

## Receiving Critique

### Best Practices

1. **Listen first** - Don't defend immediately
2. **Ask questions** - Seek to understand the feedback
3. **Take notes** - Capture feedback for later review
4. **Thank reviewers** - Feedback is a gift
5. **Separate self from work** - Critique is of the design, not you
6. **Evaluate objectively** - Not all feedback needs action

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Subjective feedback | "I don't like green" | Ground in principles |
| Solution jumping | Skipping problem definition | Ask "what problem does this solve?" |
| Context blindness | Ignoring constraints | Understand goals and limitations |
| Recency bias | Latest feedback = most important | Prioritize by user impact |
| Groupthink | Team agrees without scrutiny | Assign devil's advocate |
| Personal attachment | Designer defensiveness | Focus on goals, not ego |

---

**Remember**: Great critique makes designs better, not designers feel worse. Be kind, be specific, be constructive.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

