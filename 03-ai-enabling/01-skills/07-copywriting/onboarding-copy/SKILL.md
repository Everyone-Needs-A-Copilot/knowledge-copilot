---
last_updated: 2026-02-25
status: active
name: onboarding-copy
description: Write effective onboarding copy that guides new users from signup to first value. Use for welcome screens, setup wizards, feature tours, empty states, and first-run experiences.
triggers:
  files: ["**/onboarding/**", "**/welcome/**", "**/tour/**", "**/setup/**", "**/wizard/**"]
  keywords: ["onboarding", "welcome", "getting started", "first run", "setup wizard", "feature tour", "new user", "activation", "tutorial"]
allowed-tools: Read, Write, Edit
---

# Onboarding Copy Skill

Write onboarding copy that guides new users from signup to first success. Good onboarding copy reduces friction, builds confidence, and gets users to their "aha moment" quickly.

---

## Core Principles

### The Onboarding Mindset

| Principle | Description | Example |
|-----------|-------------|---------|
| Value-first | Show benefit before asking for effort | "See your dashboard in 30 seconds" |
| Progressive | Reveal complexity gradually | Setup essentials first, advanced later |
| Encouraging | Build confidence at each step | "Great start! One more step to go." |
| Skippable | Let power users jump ahead | "Skip tour" always available |
| Memorable | Reinforce key concepts | Consistent terminology throughout |

### User Mental States During Onboarding

| Stage | User Feeling | Copy Goal |
|-------|-------------|-----------|
| Just signed up | Curious, impatient | Get to value fast |
| Setup in progress | Invested, wants to finish | Show progress, encourage |
| First task | Uncertain, exploring | Guide without overwhelming |
| Feature discovery | Engaged, learning | Explain value, not just function |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Welcome Screens

### Welcome Message Formula

```
[Acknowledge their arrival] + [Promise of value] + [Clear first step]
```

### Welcome Copy Patterns

| Style | Example |
|-------|---------|
| Direct | "Welcome to [Product]. Let's set up your workspace." |
| Benefit-led | "Welcome! You're about to make [task] 10x faster." |
| Personal | "Hi [Name], welcome to [Product]. Here's how to get started." |
| Question-led | "What would you like to accomplish first?" |

### Welcome Screen Structure

```
Headline:    Welcome to [Product]
Subhead:     [Core value proposition in one sentence]
CTA:         [First action] → "Create your first project"
Skip option: "Explore on my own"
```

---

## Setup Wizards

### Setup Flow Principles

| Principle | Implementation |
|-----------|----------------|
| Minimal steps | Ask only what's essential to start |
| Progress visible | "Step 2 of 3" always visible |
| Undo available | "You can change this later" |
| Value each step | Explain why each input matters |

### Step-by-Step Copy

| Element | Pattern | Example |
|---------|---------|---------|
| Step header | "[Action verb] your [thing]" | "Name your workspace" |
| Helper text | "[Why this matters]" | "This helps your team find you" |
| Input label | Clear, specific | "Workspace name" |
| Placeholder | Example format | "e.g., Marketing Team" |
| Continue CTA | Progress-focused | "Next: Invite team" |

### Optional vs Required Steps

```
Required: "Name your workspace"
Optional: "Add a logo (optional)" or "Skip for now"
```

### Last Step Copy

Build anticipation for completion:

```
Header:  "Almost there!"
Body:    "One last thing before you start..."
CTA:     "Create workspace" or "Get started"
```

---

## Feature Tours and Tooltips

### Tour Introduction

```
Good: "Quick tour? See how to [do main thing] in 3 steps."
Bad:  "Would you like a product tour?"
```

Always offer skip: "Skip tour"

### Tooltip Sequence Pattern

| Step | Content Focus | Example |
|------|---------------|---------|
| 1 | Core action location | "Create new projects here" |
| 2 | Key feature | "Your dashboard shows all activity" |
| 3 | Quick win action | "Try adding your first task" |
| End | Clear completion | "You're all set! Explore on your own." |

### Tooltip Copy Rules

| Do | Don't |
|----|-------|
| Focus on user benefit | Describe technical features |
| Point to specific elements | Use vague directions |
| Keep under 15 words | Write paragraphs |
| Show keyboard shortcuts | Assume prior knowledge |

### Contextual Hint Pattern

```
[What you can do] + [How to do it]
"Add team members by clicking the + button"
```

---

## Empty States as Onboarding

### Empty State Formula

```
[What goes here] + [Why it's valuable] + [How to populate]
```

### Empty State Examples

| Context | Copy |
|---------|------|
| No projects | "No projects yet. Create one to start organizing your work." |
| No team members | "Just you for now. Invite teammates to collaborate." |
| No data | "Your analytics will appear here once you have traffic." |
| No notifications | "All caught up! Activity from your projects shows here." |

### Empty State CTA Patterns

| Purpose | CTA Text |
|---------|----------|
| Create first item | "Create your first [thing]" |
| Import existing | "Import from [source]" |
| Learn more | "See how it works" |
| Skip for now | "I'll do this later" |

---

## Progress and Completion

### Progress Indicators

| Format | Example |
|--------|---------|
| Steps | "Step 2 of 4" |
| Percentage | "Profile 75% complete" |
| Checklist | "3 of 5 tasks done" |
| Time estimate | "About 2 minutes left" |

### Milestone Celebrations

Keep them brief and genuine:

```
Good: "Nice work! Your workspace is ready."
Bad:  "Congratulations!!! You did it! 🎉🎉🎉"
```

### Completion Copy

| Element | Pattern |
|---------|---------|
| Headline | "You're all set!" or "Setup complete" |
| Summary | Brief recap of what was created/configured |
| Next step | Clear CTA to main product experience |

```
"Your workspace is ready. Start by creating your first project."
[Create project]
```

---

## Activation Prompts

### Nudging Toward Key Actions

| Timing | Copy Style | Example |
|--------|------------|---------|
| Immediate | Direct, helpful | "Add your first task to get started" |
| After delay | Gentle reminder | "Ready to create something?" |
| Near feature | Contextual tip | "Pro tip: Drag tasks to reorder" |

### Re-engagement Copy

For users who signed up but haven't completed setup:

```
Email: "Your workspace is waiting. Finish setup in 2 minutes."
In-app: "Continue where you left off?"
```

---

## Onboarding Checklist Copy

### Checklist Structure

```
Header: "Get started with [Product]"
Items:  [Clear, actionable tasks with completion states]
Progress: "3 of 5 complete"
```

### Checklist Item Patterns

| Type | Format | Example |
|------|--------|---------|
| Setup task | "[Verb] your [thing]" | "Complete your profile" |
| Feature try | "Try [feature]" | "Create your first project" |
| Integration | "Connect [tool]" | "Connect your calendar" |
| Learning | "Learn how to [action]" | "Learn how to invite teammates" |

### Completed Item Copy

```
Before: "Create your first project"
After:  "✓ Created first project"
```

---

## Personalization During Onboarding

### Asking for Preferences

| Question Type | Copy Pattern |
|---------------|--------------|
| Role | "What best describes your role?" |
| Goal | "What are you hoping to accomplish?" |
| Experience | "Have you used similar tools before?" |
| Team size | "How many people will use this?" |

### Using Personalization

```
General:     "Welcome! Let's set up your workspace."
Personalized: "Welcome, Sarah! Let's set up [Company] workspace."
```

---

## Anti-Patterns to Avoid

### Common Mistakes

| Avoid | Why | Instead |
|-------|-----|---------|
| Walls of text | Users don't read | Short, scannable points |
| Feature dumps | Overwhelming | Progressive disclosure |
| Forced tours | Frustrating | Optional, skippable |
| No escape | Trapped feeling | "Skip" always available |
| Generic greetings | Impersonal | Contextual, relevant |
| Tech jargon | Confusing | Plain language |

### Tone Mistakes

| Avoid | Better |
|-------|--------|
| "You need to..." | "You can..." |
| "You must complete..." | "To get started..." |
| Excessive exclamation!!! | Calm, confident tone |
| Condescending explanations | Respect user intelligence |

---

## Testing Onboarding Copy

### Metrics to Track

| Metric | What It Measures |
|--------|------------------|
| Completion rate | Are users finishing setup? |
| Time to complete | Is it quick enough? |
| Drop-off points | Where do users quit? |
| First action rate | Do users take key actions? |
| Skip rate | Is tour actually helpful? |

### Checklist Before Launch

| Check | Question |
|-------|----------|
| Clarity | Does each step make sense on its own? |
| Value | Is the benefit of completing clear? |
| Length | Is this the minimum necessary? |
| Progress | Can users see how far along they are? |
| Escape | Can users skip or exit at any point? |
| Mobile | Does the copy work on small screens? |

---

## Templates

### Welcome Screen

```
[Product logo]

Welcome to [Product]

[One sentence value prop]

[Primary CTA: Get started →]
[Secondary: Skip tour]
```

### Setup Step

```
Step [X] of [Y]

[Action verb] your [thing]

[Helper text: Why this matters]

[Input field]

[Continue button: Next: [upcoming step]]
[Skip option if applicable]
```

### Completion

```
[Celebration icon or animation]

You're all set!

[Summary of what's ready: "Your workspace is configured..."]

[Primary CTA: Start using [Product]]
```

---

This skill enables you to write onboarding experiences that guide users from signup to success with clarity and confidence.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

