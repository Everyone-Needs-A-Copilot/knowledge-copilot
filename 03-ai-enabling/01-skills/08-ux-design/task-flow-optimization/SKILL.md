---
last_updated: 2026-02-25
status: active
name: task-flow-optimization
description: Design efficient task flows - minimizing steps, friction, and time to completion. Use for workflow design and conversion optimization.
triggers:
  files: ["**/flow/**", "**/workflow/**", "**/checkout/**", "**/onboarding/**"]
  keywords: ["task flow", "user flow", "workflow", "conversion", "funnel", "checkout", "onboarding", "steps", "friction", "optimization"]
allowed-tools: Read, Write, Edit
---

# Task Flow Optimization Skill

Master guide for designing task flows that get users to their goals efficiently - minimizing friction, reducing abandonment, and maximizing completion rates.

## Philosophy

**Every step is a potential exit.** Each additional screen, click, or decision increases the chance users will abandon. Ruthlessly eliminate unnecessary steps.

**Momentum matters.** Once users start a flow, keep them moving. Interruptions break concentration and invite abandonment.

**Match flow to intent.** Quick tasks need quick flows. Complex tasks benefit from guidance. Know the difference.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Task Flow Anatomy

### Basic Flow Structure

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Entry  │ →  │  Step 1 │ →  │  Step 2 │ →  │ Success │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Flow Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Entry** | Start the flow | "Sign up" button |
| **Steps** | Gather info/actions | Form fields |
| **Progress** | Show location | Step 2 of 4 |
| **Validation** | Confirm correctness | Field validation |
| **Confirmation** | Verify intent | "Confirm purchase?" |
| **Success** | Complete flow | "Order placed!" |
| **Recovery** | Handle errors | "Try again" |

---

## Flow Optimization Principles

### 1. Eliminate Steps

Every step removed improves completion:

```
❌ 7 Steps: 20% completion
✅ 4 Steps: 60% completion
```

**Audit each step**:
- Is this information essential?
- Can we get this elsewhere?
- Can steps be combined?
- Can this be deferred to later?

### 2. Reduce Fields

Fewer fields = higher completion:

| Fields | Completion Rate |
|--------|-----------------|
| 3 fields | 25% higher |
| 5 fields | Baseline |
| 7+ fields | 20% lower |

**Field reduction tactics**:
- Remove optional fields
- Use smart defaults
- Combine fields (full name vs first/last)
- Defer non-essential to later

### 3. Progress Visibility

Users complete more when they see progress:

```
Step 2 of 4: Payment Details
━━━━━━━━━●━━━━━━━━━━━━━━━━━
```

**Progress patterns**:
- Step indicators (Step X of Y)
- Progress bars (percentage)
- Breadcrumbs (for non-linear)
- Checklist (for multi-task)

### 4. Smart Defaults

Pre-fill whenever possible:

```
❌ Bad: Empty fields
Country: [Select ▼]
Currency: [Select ▼]

✅ Good: Intelligent defaults
Country: [United States ▼] ← IP-based
Currency: [USD ▼] ← Country-based
```

### 5. Clear Next Steps

Always show what's next:

```
✓ Email verified

Next: Complete your profile
[Continue →]
```

---

## Flow Patterns

### Linear Flow

Best for: Sequential tasks, checkout, wizards

```
[1] → [2] → [3] → [Done]
```

**Guidelines**:
- Clear progress indication
- Back button available
- Save state between steps
- Validation before proceeding

### Branching Flow

Best for: Conditional paths, configurators

```
[1] → [2A] or [2B] → [3] → [Done]
         ↘     ↙
```

**Guidelines**:
- Clear decision points
- Explain consequences of choices
- Allow path changes
- Merge back to common end

### Hub-and-Spoke Flow

Best for: Multiple independent tasks, settings

```
        [Task A]
            ↑
[Task B] ← [Hub] → [Task C]
            ↓
        [Task D]
```

**Guidelines**:
- Clear return to hub
- Show completion status
- Allow any order
- Save individual task progress

### Parallel Flow

Best for: Background processing, async tasks

```
[Start] → [Processing...] → [Complete]
              ↓ Continue using app
         [Other tasks]
```

**Guidelines**:
- Clear processing indicator
- Allow other activities
- Notify on completion
- Easy access to results

---

## Critical Flow Types

### Sign-Up Flow

**Minimal sign-up**:
```
┌────────────────────────────────┐
│ Create your account            │
│                                │
│ Email: [_______________]       │
│                                │
│ [Continue with Google]         │
│ [Continue with Email]          │
│                                │
│ Already have an account? →     │
└────────────────────────────────┘
```

**Progressive profiling**:
```
Sign up: Email only
↓
First use: Ask name
↓
Day 7: Ask preferences
↓
First purchase: Ask address
```

### Checkout Flow

**Optimized checkout**:
```
┌────────────────────────────────┐
│ Checkout                       │
│                                │
│ ┌─ Contact ─────────────────┐  │
│ │ Email: [________________] │  │
│ └───────────────────────────┘  │
│                                │
│ ┌─ Shipping ────────────────┐  │
│ │ Address: [______________] │  │
│ │ (autocomplete)            │  │
│ └───────────────────────────┘  │
│                                │
│ ┌─ Payment ─────────────────┐  │
│ │ Card: [________________]  │  │
│ │ [Apple Pay] [Google Pay]  │  │
│ └───────────────────────────┘  │
│                                │
│ ┌─ Summary ─────────────────┐  │
│ │ Subtotal: $99             │  │
│ │ Shipping: $5              │  │
│ │ Total: $104               │  │
│ └───────────────────────────┘  │
│                                │
│      [Complete Purchase]       │
└────────────────────────────────┘
```

**Checkout principles**:
- Single-page when possible
- Guest checkout option
- Multiple payment methods
- Address autocomplete
- Clear pricing throughout
- Security indicators

### Onboarding Flow

**Activation-focused onboarding**:
```
Welcome, Sarah!

Let's get you started:

□ Create your first project (recommended)
□ Import existing data
□ Explore templates
□ Skip and explore

[Continue with: Create project →]
```

**Onboarding principles**:
- Get to value fast
- Celebrate first success
- Allow skipping
- Personalize when possible
- Don't front-load settings

---

## Friction Points

### Common Friction Types

| Friction | Solution |
|----------|----------|
| Too many steps | Reduce/combine steps |
| Unclear progress | Add progress indicator |
| Form errors | Inline validation |
| Required fields | Make optional or remove |
| Account required | Allow guest flow |
| Slow loading | Optimize performance |
| Confusing copy | Clear, concise language |
| Poor mobile UX | Responsive design |

### Friction Identification

**Analytics signals**:
- Drop-off rates by step
- Time-on-step (too long = confusion)
- Error rates by field
- Back button usage

**User research signals**:
- Verbal frustration
- Repeated attempts
- Questions about basics
- Abandonment points

### Strategic Friction

Sometimes friction is intentional:

| Use Case | Friction | Purpose |
|----------|----------|---------|
| Delete account | Confirmation + password | Prevent accidents |
| Large purchase | Review step | Build confidence |
| Legal requirement | Terms acceptance | Compliance |
| Data entry | Validation | Data quality |

---

## Validation Strategies

### Real-Time Validation

Validate as users type:

```
Email: [john@example.com] ✓
Password: [●●●●●●●●]
          ✓ 8+ characters
          ✓ Contains number
          ○ Contains special character
```

### Step-Level Validation

Validate before proceeding:

```
[Previous step completed]
↓
Check all fields valid
↓
If valid → Proceed
If invalid → Show errors, stay on step
```

### Positive Validation

Confirm correct input:

```
✓ Email available
✓ Password strong
✓ Dates valid
```

---

## Mobile Flow Optimization

### Touch Considerations

```
❌ Bad: Small tap targets
[tiny] [buttons] [here]

✅ Good: 44px minimum
[  Large  ] [  Buttons  ]
```

### Single-Column Layout

```
❌ Bad: Side-by-side on mobile
[First] [Last]

✅ Good: Stacked fields
[Full Name        ]
[Email            ]
```

### Mobile Input Optimization

```
<input type="email" inputmode="email">
<input type="tel" inputmode="tel">
<input type="number" inputmode="decimal">
```

### Sticky Elements

```
┌────────────────────────────┐
│ [Form content scrolls]     │
│ ...                        │
│ ...                        │
├────────────────────────────┤
│ [Continue] ← Sticky footer │
└────────────────────────────┘
```

---

## Conversion Optimization

### A/B Testing Flows

Test variations:
- Number of steps (3 vs 5)
- Field order
- CTA copy ("Continue" vs "Next Step")
- Progress indicator style
- Default selections

### Micro-Conversions

Track intermediate steps:

```
Start → Step 1 → Step 2 → Step 3 → Complete
100%     80%      60%      50%       40%
```

Identify and fix biggest drops.

### Exit Intent

Capture before abandonment:

```
┌────────────────────────────────┐
│ Leaving so soon?               │
│                                │
│ We'll save your progress.      │
│ Enter your email to continue   │
│ later:                         │
│                                │
│ [________________] [Save]      │
│                                │
│ [No thanks, leave]             │
└────────────────────────────────┘
```

---

## Success States

### Confirmation Design

```
┌────────────────────────────────┐
│           ✓                    │
│                                │
│    Order Confirmed!            │
│    Order #12345                │
│                                │
│    Confirmation sent to        │
│    john@example.com            │
│                                │
│    What's next:                │
│    • Ships in 2-3 days         │
│    • Tracking email incoming   │
│                                │
│    [Track Order] [Continue]    │
└────────────────────────────────┘
```

### Success Principles

1. **Celebrate** - Acknowledge completion
2. **Confirm** - Show what happened
3. **Inform** - Next steps
4. **Offer** - Related actions
5. **Provide** - Reference info (order #, receipt)

---

## Flow Documentation

### Flow Diagrams

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────┐     ┌─────────┐
│ Step 1  │────►│ Error?  │
└────┬────┘     └────┬────┘
     │               │ Yes
     │ No            ▼
     │         ┌─────────┐
     │         │  Error  │
     │         │  State  │
     │         └────┬────┘
     │               │
     │◄──────────────┘
     ▼
┌─────────┐
│ Success │
└─────────┘
```

### Flow Specifications

| Step | Screen | Purpose | Fields | Validation | Exit |
|------|--------|---------|--------|------------|------|
| 1 | Contact | Get email | Email | Format check | → Step 2 |
| 2 | Payment | Collect card | Card, CVC, Exp | Card validation | → Confirm |
| 3 | Confirm | Review order | None | None | → Success |

---

## Anti-Patterns

### 1. Unnecessary Account Creation

```
❌ Bad: Must create account
"Create account to continue"

✅ Good: Guest option
[Checkout as guest] [Create account]
```

### 2. Hidden Requirements

```
❌ Bad: Surprise requirements
Step 5 of 5: "Also upload ID"

✅ Good: Upfront requirements
"You'll need: Email, ID, Payment method"
```

### 3. Broken Back Button

```
❌ Bad: Back = lose data
← Back → Data lost!

✅ Good: Back preserves state
← Back → Data preserved
```

### 4. Unclear Progress

```
❌ Bad: No indication
[Form] [Form] [Form] ???

✅ Good: Clear progress
Step 2 of 4: Shipping Details
```

### 5. Confirmation Overload

```
❌ Bad: Confirm everything
"Are you sure?" × 5

✅ Good: Confirm only destructive/expensive
"Are you sure?" × 1 (final step only)
```

---

## Quick Reference

### Flow Optimization Checklist

- [ ] Minimum possible steps
- [ ] Minimum required fields
- [ ] Clear progress indicator
- [ ] Smart defaults pre-filled
- [ ] Inline validation
- [ ] Back button preserves data
- [ ] Guest option (if applicable)
- [ ] Mobile-optimized
- [ ] Clear success state
- [ ] Recovery from errors

### Metrics to Track

| Metric | Target |
|--------|--------|
| Completion rate | Maximize |
| Time to complete | Minimize |
| Error rate | < 5% |
| Drop-off per step | < 20% |
| Support tickets | Minimize |

### Step Reduction Questions

For each step, ask:
1. Can we eliminate this step?
2. Can we combine with another step?
3. Can we defer to later?
4. Can we get this data elsewhere?
5. Is this truly required?

---

## Summary

**Shorter flows = Higher completion**

1. Ruthlessly eliminate unnecessary steps
2. Show clear progress throughout
3. Pre-fill everything possible
4. Validate inline, not at the end
5. Always preserve user data
6. Celebrate successful completion

*The best flow is the one users barely notice.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

