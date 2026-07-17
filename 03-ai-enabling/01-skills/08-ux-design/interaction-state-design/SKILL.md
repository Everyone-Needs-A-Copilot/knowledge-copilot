---
last_updated: 2026-02-25
status: active
name: interaction-state-design
description: Design all 8 interaction states - default, hover, focus, active, disabled, loading, error, empty. Use for complete state coverage.
triggers:
  files: ["**/components/**", "**/buttons/**", "**/forms/**", "**/states/**"]
  keywords: ["hover state", "focus state", "disabled", "loading state", "error state", "empty state", "active state", "interaction state"]
allowed-tools: Read, Write, Edit
---

# Interaction State Design Skill

Master guide for designing all 8 essential interaction states for UI components - ensuring complete, consistent, and accessible state coverage.

## Philosophy

**Every element has states.** A button isn't just a button—it's a button in default state, hover state, focus state, active state, disabled state, and possibly loading state. Incomplete state design creates inconsistent, confusing interfaces.

**States communicate.** Each state tells users something: "this is interactive," "you're here," "this is unavailable," "processing your request."

**Design all states upfront.** Retrofitting states leads to inconsistency. Consider all states from the beginning.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## The 8 Essential States

| State | Purpose | Trigger |
|-------|---------|---------|
| **Default** | Resting appearance | None (initial) |
| **Hover** | Interactive feedback | Mouse enters |
| **Focus** | Keyboard location | Tab/click |
| **Active** | Being pressed | Mouse down |
| **Disabled** | Not available | System/logic |
| **Loading** | Processing | Async operation |
| **Error** | Something wrong | Validation/failure |
| **Empty** | No content | No data |

---

## State-by-State Guide

### 1. Default State

The baseline, resting appearance.

**Guidelines**:
- Clear affordance (buttons look clickable)
- Consistent across similar components
- Sufficient contrast
- No ambiguity about interactivity

```css
.button {
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
}
```

### 2. Hover State

Feedback when mouse is over interactive element.

**Guidelines**:
- Subtle but noticeable change
- Don't rely on hover alone (touch devices)
- Consistent hover treatment across similar elements
- Fast transition (100-150ms)

```css
.button:hover {
  background: var(--color-primary-dark);
  /* Or: box-shadow, transform scale, etc. */
  transition: background 0.15s ease-out;
}
```

**Hover patterns**:
| Element | Hover Effect |
|---------|-------------|
| Button | Darken/lighten, subtle shadow |
| Link | Underline, color change |
| Card | Lift (shadow + translateY) |
| List item | Background highlight |
| Icon | Color change, scale |

### 3. Focus State

Shows keyboard navigation position. **Critical for accessibility.**

**Guidelines**:
- Must be visible (WCAG requirement)
- Different from hover (users need to distinguish)
- Never remove focus outline without replacement
- Logical tab order

```css
.button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  /* Or: box-shadow for more control */
}

/* Don't do this: */
.button:focus {
  outline: none; /* ❌ Accessibility violation */
}

/* Do this instead: */
.button:focus-visible {
  outline: 3px solid var(--color-focus);
}
```

**Focus-visible vs Focus**:
- `:focus` - Any focus (click or keyboard)
- `:focus-visible` - Keyboard focus only (better UX)

### 4. Active State

Element is being pressed/activated.

**Guidelines**:
- Immediate feedback (no delay)
- Usually "pressed" appearance
- Brief (only during press)
- Clear cause-effect relationship

```css
.button:active {
  transform: scale(0.98);
  background: var(--color-primary-darker);
}
```

**Active patterns**:
| Element | Active Effect |
|---------|--------------|
| Button | Scale down, darken |
| Link | Color change |
| Card | Slight depression |
| Toggle | Position change |

### 5. Disabled State

Element is not currently interactive.

**Guidelines**:
- Visually distinct from default
- Cursor shows not-allowed
- Explain why disabled (tooltip)
- Don't hide disabled elements (unless confusing)

```css
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none; /* Prevents interaction */
}

/* Or use color changes: */
.button:disabled {
  background: var(--color-gray-300);
  color: var(--color-gray-500);
}
```

**Disabled UX patterns**:
```
❌ Bad: [Disabled button with no explanation]

✅ Good:
[Submit] (disabled)
↳ Tooltip: "Complete required fields to submit"
```

### 6. Loading State

Element is processing or fetching.

**Guidelines**:
- Clear loading indicator
- Disable interaction during load
- Show progress if known
- Provide escape/cancel if long

```css
.button.loading {
  position: relative;
  color: transparent; /* Hide text */
  pointer-events: none;
}

.button.loading::after {
  content: "";
  position: absolute;
  /* Spinner styles */
  animation: spin 1s linear infinite;
}
```

**Loading patterns**:
| Duration | Treatment |
|----------|-----------|
| < 300ms | No indicator (feels instant) |
| 300ms-1s | Spinner |
| 1-10s | Progress bar |
| > 10s | Progress + time estimate |

**Button loading**:
```
[Submit] → [◌ Submitting...] → [✓ Done]
```

### 7. Error State

Something went wrong or validation failed.

**Guidelines**:
- Clear error indication (color + icon + text)
- Explain what's wrong
- Explain how to fix
- Don't lose user data

```css
.input.error {
  border-color: var(--color-error);
}

.error-message {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: 4px;
}
```

**Error patterns**:
```
Field Label *
[Input with error          ]
↳ ✗ This field is required

Field Label
[user@example              ]
↳ ✗ Please enter a valid email address
```

**Error components**:
| Component | Error Treatment |
|-----------|----------------|
| Input | Red border, error message below |
| Form | Error summary + field highlights |
| Page | Error banner or modal |
| Toast | Brief error notification |

### 8. Empty State

No content to display.

**Guidelines**:
- Clear explanation (not just blank)
- Helpful guidance on what to do
- Appropriate visual (icon/illustration)
- Call to action when relevant

**Empty state anatomy**:
```
┌─────────────────────────────────────┐
│         [Illustration/Icon]         │
│                                     │
│      No projects yet                │  ← Explanation
│                                     │
│   Create your first project to      │  ← Guidance
│   start tracking your work.         │
│                                     │
│      [+ Create Project]             │  ← CTA
│                                     │
│   [Watch tutorial] [See examples]   │  ← Secondary
└─────────────────────────────────────┘
```

**Empty state types**:
| Type | Example |
|------|---------|
| First-time | "No projects yet. Create one!" |
| No results | "No matches found. Try different search." |
| Cleared | "Inbox zero! You're all caught up." |
| Error-caused | "Couldn't load items. Retry?" |

---

## State Combinations

### Combined States

States can combine:

```css
/* Focused + Hover */
.button:focus:hover {
  /* Both focus ring AND hover treatment */
}

/* Disabled takes precedence */
.button:disabled:hover {
  /* No hover effect - disabled wins */
}
```

### State Priority

When states conflict, follow this priority:
1. Disabled (highest - prevents all interaction)
2. Loading (prevents interaction)
3. Error (shows problem)
4. Active (being pressed)
5. Focus (keyboard location)
6. Hover (mouse position)
7. Default (lowest)

---

## Component State Matrix

### Button States

| State | Background | Border | Text | Cursor | Other |
|-------|------------|--------|------|--------|-------|
| Default | Primary | None | White | Pointer | - |
| Hover | Primary-dark | None | White | Pointer | - |
| Focus | Primary | Focus ring | White | - | Outline |
| Active | Primary-darker | None | White | Pointer | Scale 0.98 |
| Disabled | Gray-300 | None | Gray-500 | Not-allowed | Opacity 0.5 |
| Loading | Primary | None | Hidden | Default | Spinner |

### Input States

| State | Border | Background | Label | Helper |
|-------|--------|------------|-------|--------|
| Default | Gray-300 | White | Gray-700 | Gray-500 |
| Hover | Gray-400 | White | Gray-700 | Gray-500 |
| Focus | Primary | White | Primary | Gray-500 |
| Filled | Gray-300 | White | Gray-700 | Gray-500 |
| Disabled | Gray-200 | Gray-100 | Gray-400 | Gray-400 |
| Error | Error | White | Error | Error message |
| Success | Success | White | Gray-700 | Success message |

### Card States

| State | Shadow | Border | Transform |
|-------|--------|--------|-----------|
| Default | sm | None | None |
| Hover | md | None | translateY(-2px) |
| Focus | sm | Focus ring | None |
| Active | xs | None | translateY(0) |
| Selected | md | Primary | None |
| Disabled | none | Gray | None (opacity 0.6) |

---

## Implementation Patterns

### CSS State Management

```css
/* Base component */
.component {
  /* Default state */
}

/* Interactive states (in order) */
.component:hover { }
.component:focus-visible { }
.component:active { }

/* Controlled states (via class/attribute) */
.component:disabled,
.component[aria-disabled="true"] { }

.component.is-loading { }
.component.is-error { }
.component.is-empty { }
```

### React State Pattern

```tsx
interface ButtonProps {
  disabled?: boolean;
  loading?: boolean;
  error?: boolean;
}

function Button({ disabled, loading, error }: ButtonProps) {
  return (
    <button
      disabled={disabled || loading}
      className={cn(
        'button',
        loading && 'is-loading',
        error && 'is-error'
      )}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
}
```

### State Transitions

```css
/* Smooth state transitions */
.button {
  transition:
    background-color 0.15s ease-out,
    transform 0.1s ease-out,
    box-shadow 0.15s ease-out;
}
```

---

## Accessibility

### Focus Requirements

- Focus must be visible (WCAG 2.4.7)
- Focus indicator must have 3:1 contrast (WCAG 2.4.11)
- Focus order must be logical (WCAG 2.4.3)

### Disabled State Accessibility

```html
<!-- Button -->
<button disabled>Submit</button>

<!-- Other elements need aria-disabled -->
<div role="button" aria-disabled="true">Custom button</div>
```

### Error State Accessibility

```html
<label for="email">Email</label>
<input
  id="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">
  Please enter a valid email
</span>
```

### Loading State Accessibility

```html
<button aria-busy="true" aria-label="Submitting...">
  <span class="sr-only">Submitting</span>
  <Spinner aria-hidden="true" />
</button>
```

---

## Testing States

### State Checklist

For each interactive component, verify:

- [ ] **Default**: Clear affordance
- [ ] **Hover**: Visible feedback
- [ ] **Focus**: Visible, high-contrast ring
- [ ] **Active**: Immediate press feedback
- [ ] **Disabled**: Visually distinct, cursor correct
- [ ] **Loading**: Clear indicator, interaction blocked
- [ ] **Error**: Visible, explains problem
- [ ] **Empty**: Helpful, guides user

### Testing Methods

**Visual inspection**:
- Tab through interface
- Test all mouse interactions
- Check disabled elements
- Trigger all error cases
- View empty states

**Automated**:
- Contrast checking
- Focus order verification
- ARIA attribute validation

**User testing**:
- Can users identify interactive elements?
- Do users understand disabled states?
- Are errors clear and actionable?

---

## Quick Reference

### State Design Checklist

Before shipping any component:
- [ ] All 8 states designed
- [ ] States visually distinct
- [ ] Transitions smooth (100-200ms)
- [ ] Focus visible and accessible
- [ ] Disabled clearly indicated
- [ ] Loading blocks interaction
- [ ] Errors explain and guide
- [ ] Empty states helpful

### CSS Properties by State

| State | Common Properties |
|-------|-------------------|
| Hover | background, box-shadow, transform |
| Focus | outline, box-shadow |
| Active | transform, background |
| Disabled | opacity, cursor, background |
| Loading | animation, position |
| Error | border-color, color |

### Timing Guidelines

| Transition | Duration |
|------------|----------|
| Hover in | 100-150ms |
| Hover out | 150-200ms |
| Focus | Instant |
| Active | Instant |
| Loading spinner | 800-1200ms rotation |
| Error shake | 300-400ms |

---

## Summary

**Complete state coverage = Professional interface**

1. Design all 8 states for every interactive element
2. Make states visually distinct
3. Prioritize focus state (accessibility)
4. Use consistent treatment across similar components
5. Test all states before shipping

*States aren't extra work—they're the work. An interface without proper states is incomplete.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

