---
last_updated: 2026-02-25
status: active
name: interaction-feedback-design
description: Design patterns for tactile interaction feedback and micro-interactions. Use when designing button states, loading indicators, form submissions, or any UI state change feedback.
category: industrial-design-digital
keywords:
  - feedback
  - state
  - interaction
  - micro-interactions
  - tactile
triggers:
  keywords:
    - button click
    - loading state
    - form submission
    - interaction feedback
    - state change
  filePatterns:
    - "**/*.tsx"
    - "**/*.ts"
    - "**/components/**"
allowed-tools: Read, Write, Edit
---

# Interaction Feedback Design

Design state changes and micro-interactions as digital tactile feedback.

## Philosophy

A physical button clicks. You feel it compress, hear it engage, see it move. Digital buttons require the same honesty—the user must know the system heard them. Not decoration. Not delight. Just truth: "Your action registered. Here's what's happening."

**Rams Principle 4 (Understandable):** The object teaches you—no manual needed.
**Rams Principle 6 (Honest):** No tricks.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Methodology

### Step 1: Map Physical Feedback to Digital

| Physical Feedback | Digital Equivalent | Implementation |
|-------------------|-------------------|----------------|
| **Tactile click** | Visual state change | Button active state, 100ms |
| **Resistance** | Disabled state | Reduced opacity, no hover |
| **Movement** | Position shift | 2px press, spring easing |
| **Sound** | System feedback | Haptic on mobile, focus sound |
| **Completion** | Success state | Checkmark, green border |
| **Error** | Rejection feedback | Shake animation, red border |

### Step 2: State Visibility Hierarchy

Every interaction has 5 states. All must be visible:

```typescript
enum InteractionState {
  IDLE = "idle",           // Ready to act
  HOVER = "hover",         // System acknowledges pointer
  ACTIVE = "active",       // User is pressing
  LOADING = "loading",     // System is working
  COMPLETE = "complete"    // Action finished
}
```

### Step 3: Timing Constraints

Feedback must match human perception:

| Event | Timing | Reason |
|-------|--------|--------|
| **Visual acknowledgment** | <100ms | Below perception threshold |
| **Progress indication** | >200ms | Don't show spinner for fast ops |
| **Completion feedback** | 300-500ms | Long enough to perceive success |
| **Error persistence** | Until dismissed | User must acknowledge |

### Step 4: Feedback Necessity Test

For each micro-interaction, ask:
1. **Does user need to know this happened?** → Yes = feedback required
2. **Is this state change or decoration?** → State = keep, decoration = remove
3. **Would physical object provide this feedback?** → Yes = digital should too

### Step 5: Honest Progress

```typescript
// HONEST: Real progress
<Button disabled={loading}>
  {loading ? `Saving... ${progress}%` : 'Save'}
</Button>

// DISHONEST: Fake progress
<Button disabled={loading}>
  {loading ? <Spinner /> : 'Save'}  // No info about duration/progress
</Button>
```

## Tests

| Test | Pass Criteria | Fail Criteria |
|------|---------------|---------------|
| **Acknowledgment** | Every action gets <100ms feedback | Silent actions |
| **State Visibility** | All 5 states visually distinct | States look identical |
| **Honest Duration** | Loading states show real progress | Fake spinners |
| **No Decoration** | Feedback communicates state only | Animations for delight |
| **Physical Analog** | Behavior matches physical expectation | Violates physics |

## Anti-Patterns

| Anti-Pattern | Why Wrong | Alternative |
|--------------|-----------|-------------|
| **Silent buttons** | User doesn't know if click registered | Visual active state <100ms |
| **Indeterminate spinners** | Dishonest about duration | Progress bar with % or time |
| **Hover animations** | Decoration, not feedback | Hover = color change only |
| **Success theater** | Fake "saving..." delays | Show real save duration |
| **Loading without context** | "Loading what?" | "Loading insights (2/47)" |
| **No error recovery** | Error state is dead end | Error + retry action |

## Examples

### Good Example

```typescript
// Honest interaction feedback
import { useState } from 'react';

function SaveButton({ onSave }: { onSave: () => Promise<void> }) {
  const [state, setState] = useState<InteractionState>('idle');
  const [progress, setProgress] = useState(0);

  const handleClick = async () => {
    setState('active');
    await new Promise(r => setTimeout(r, 100)); // Visual acknowledgment

    setState('loading');
    try {
      await onSave(setProgress); // Real progress updates
      setState('complete');
      setTimeout(() => setState('idle'), 500); // Show success briefly
    } catch (error) {
      setState('error');
      // Error persists until user dismisses
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={state === 'loading'}
      className={cn(
        'px-4 py-2 rounded transition-all duration-100',
        state === 'idle' && 'bg-blue-500 hover:bg-blue-600',
        state === 'active' && 'bg-blue-700 translate-y-[2px]', // Physical press
        state === 'loading' && 'bg-gray-400 cursor-wait',
        state === 'complete' && 'bg-green-500',
        state === 'error' && 'bg-red-500 animate-shake'
      )}
    >
      {state === 'idle' && 'Save'}
      {state === 'active' && 'Save'}
      {state === 'loading' && `Saving... ${progress}%`}
      {state === 'complete' && '✓ Saved'}
      {state === 'error' && 'Error - Retry?'}
    </button>
  );
}
```

### Bad Example

```typescript
// Dishonest interaction feedback
function SaveButton({ onSave }: { onSave: () => Promise<void> }) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    await new Promise(r => setTimeout(r, 1000)); // FAKE DELAY
    await onSave();
    setLoading(false);
    // No completion feedback
    // No error handling
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className="px-4 py-2 bg-blue-500 hover:scale-110 transition-transform duration-300"
      // ↑ Decoration, not feedback. Violates physics.
    >
      {loading ? <Spinner /> : 'Save'}
      {/* No progress info */}
      {/* No completion state */}
      {/* No error state */}
    </button>
  );
}
```

## Implementation Checklist

- [ ] All interactive elements have 5 states (idle, hover, active, loading, complete)
- [ ] Visual feedback <100ms for all actions
- [ ] Loading states show real progress (%, time, or item count)
- [ ] Success states visible for 300-500ms
- [ ] Error states persist until dismissed
- [ ] No animations longer than 200ms
- [ ] Disabled states visually distinct (opacity 0.5)
- [ ] Focus states meet WCAG 2.1 (3:1 contrast ratio)
- [ ] No hover effects on touch devices
- [ ] All feedback serves function, not decoration


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

