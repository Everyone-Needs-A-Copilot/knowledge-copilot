---
last_updated: 2026-02-25
status: active
name: motion-design-principles
description: Animation timing, easing curves, micro-interactions, and purposeful motion in UI. Use when designing interface animations.
triggers:
  files: ["**/animation.*", "**/motion.*", "**/transitions.*", "**/keyframes.*"]
  keywords: ["animation", "motion design", "easing", "micro-interactions", "transitions", "timing", "keyframes", "spring animation"]
allowed-tools: Read, Write, Edit
---

# Motion Design Principles: Deep Expertise Skill

Creating purposeful, performant animations that enhance user experience and communicate interface behavior.

## Why Motion Matters

### The Role of Animation

| Purpose | Description | Example |
|---------|-------------|---------|
| **Feedback** | Confirm user actions | Button press effect |
| **Guidance** | Direct attention | Focus transitions |
| **Continuity** | Show relationships | Page transitions |
| **Personality** | Express brand | Loading animations |
| **Orientation** | Establish spatial model | Sliding panels |

### Animation Principles

| Principle | Application |
|-----------|-------------|
| **Purposeful** | Every animation serves a function |
| **Quick** | 150-300ms for most UI transitions |
| **Natural** | Follow physical world expectations |
| **Consistent** | Same actions = same animations |
| **Accessible** | Respect motion preferences |


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Timing and Duration

### Duration Guidelines

```css
:root {
  /* Instant feedback (micro-interactions) */
  --duration-instant: 50ms;

  /* Fast transitions (hover, focus) */
  --duration-fast: 100ms;
  --duration-quick: 150ms;

  /* Standard transitions (most UI) */
  --duration-normal: 200ms;
  --duration-moderate: 300ms;

  /* Slow transitions (complex movements) */
  --duration-slow: 400ms;
  --duration-slower: 500ms;

  /* Extended (page transitions, modals) */
  --duration-extended: 700ms;
}
```

### Duration by Interaction Type

| Interaction | Duration | Rationale |
|-------------|----------|-----------|
| Hover states | 100-150ms | Instant feedback |
| Button press | 100-200ms | Responsive feel |
| Toggle/switch | 150-200ms | State change clarity |
| Dropdown open | 200-250ms | Content reveal |
| Modal appear | 200-300ms | Focus shift |
| Page transition | 300-500ms | Spatial orientation |
| Loading states | 500ms+ (loop) | Background activity |

### Duration by Distance

Larger movements need longer durations:

```css
/* Small movement (< 100px) */
.move-small {
  transition-duration: var(--duration-fast);
}

/* Medium movement (100-500px) */
.move-medium {
  transition-duration: var(--duration-normal);
}

/* Large movement (> 500px) */
.move-large {
  transition-duration: var(--duration-slow);
}
```

## Easing Functions

### Standard Easings

```css
:root {
  /* Linear - constant speed (avoid for UI) */
  --ease-linear: linear;

  /* Ease out - fast start, slow end (entering) */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);

  /* Ease in - slow start, fast end (exiting) */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);

  /* Ease in-out - slow start and end */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* Emphasized easings */
  --ease-out-emphasized: cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-in-emphasized: cubic-bezier(0.3, 0, 0.8, 0.15);
}
```

### When to Use Each Easing

| Easing | Use Case | Feel |
|--------|----------|------|
| **Ease-out** | Elements entering view | Decelerating arrival |
| **Ease-in** | Elements leaving view | Accelerating departure |
| **Ease-in-out** | On-screen movement | Smooth transitions |
| **Linear** | Looping animations | Continuous motion |
| **Emphasized** | Major transitions | Dramatic effect |

### Easing Visualization

```
ease-out: ████████▓▒░░  (fast → slow)
ease-in:  ░░▒▓████████  (slow → fast)
ease-in-out: ░▒▓████▓▒░ (slow → fast → slow)
linear:   ▓▓▓▓▓▓▓▓▓▓▓▓  (constant)
```

## CSS Transitions

### Basic Transition Pattern

```css
/* Define what transitions */
.element {
  transition-property: transform, opacity;
  transition-duration: var(--duration-normal);
  transition-timing-function: var(--ease-out);
}

/* Shorthand */
.element {
  transition: transform var(--duration-normal) var(--ease-out),
              opacity var(--duration-normal) var(--ease-out);
}
```

### Transition Utilities

```css
/* Property-specific transitions */
.transition-opacity {
  transition: opacity var(--duration-normal) var(--ease-out);
}

.transition-transform {
  transition: transform var(--duration-normal) var(--ease-out);
}

.transition-colors {
  transition: color var(--duration-fast) var(--ease-out),
              background-color var(--duration-fast) var(--ease-out),
              border-color var(--duration-fast) var(--ease-out);
}

.transition-shadow {
  transition: box-shadow var(--duration-normal) var(--ease-out);
}

/* Combined utility */
.transition-all {
  transition: all var(--duration-normal) var(--ease-out);
}

/* No transition */
.transition-none {
  transition: none;
}
```

### Interactive State Transitions

```css
.button {
  background: var(--color-primary);
  transform: translateY(0);
  transition: background var(--duration-fast) var(--ease-out),
              transform var(--duration-fast) var(--ease-out);
}

.button:hover {
  background: var(--color-primary-hover);
}

.button:active {
  transform: translateY(1px);
  transition-duration: var(--duration-instant);
}
```

## CSS Animations

### Keyframe Animation Pattern

```css
/* Define keyframes */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Apply animation */
.element {
  animation: slideUp var(--duration-normal) var(--ease-out) forwards;
}
```

### Animation Utilities

```css
/* Entrance animations */
.animate-fade-in {
  animation: fadeIn var(--duration-normal) var(--ease-out) forwards;
}

.animate-slide-up {
  animation: slideUp var(--duration-normal) var(--ease-out) forwards;
}

.animate-slide-down {
  animation: slideDown var(--duration-normal) var(--ease-out) forwards;
}

.animate-scale-in {
  animation: scaleIn var(--duration-normal) var(--ease-out) forwards;
}

/* Looping animations */
.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-pulse {
  animation: pulse 2s var(--ease-in-out) infinite;
}

.animate-bounce {
  animation: bounce 1s var(--ease-out) infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
```

### Staggered Animations

```css
/* Stagger list items */
.stagger-item {
  opacity: 0;
  animation: slideUp var(--duration-normal) var(--ease-out) forwards;
}

.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 50ms; }
.stagger-item:nth-child(3) { animation-delay: 100ms; }
.stagger-item:nth-child(4) { animation-delay: 150ms; }
.stagger-item:nth-child(5) { animation-delay: 200ms; }

/* Dynamic stagger with CSS custom properties */
.stagger-item {
  animation-delay: calc(var(--index, 0) * 50ms);
}
```

## Micro-Interactions

### Button Press Effect

```css
.button {
  transform: scale(1);
  transition: transform var(--duration-fast) var(--ease-out);
}

.button:active {
  transform: scale(0.97);
  transition-duration: var(--duration-instant);
}
```

### Toggle Switch

```css
.toggle-track {
  background: var(--color-gray-300);
  transition: background var(--duration-fast) var(--ease-out);
}

.toggle-track.checked {
  background: var(--color-primary);
}

.toggle-thumb {
  transform: translateX(0);
  transition: transform var(--duration-normal) var(--ease-out);
}

.toggle-track.checked .toggle-thumb {
  transform: translateX(20px);
}
```

### Checkbox Animation

```css
.checkbox-icon {
  stroke-dasharray: 24;
  stroke-dashoffset: 24;
  transition: stroke-dashoffset var(--duration-normal) var(--ease-out);
}

.checkbox.checked .checkbox-icon {
  stroke-dashoffset: 0;
}
```

### Loading Spinner

```css
.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--color-gray-200);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

## Component Animations

### Modal/Dialog

```css
/* Backdrop */
.modal-backdrop {
  opacity: 0;
  transition: opacity var(--duration-normal) var(--ease-out);
}

.modal-backdrop.open {
  opacity: 1;
}

/* Content */
.modal-content {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
  transition: opacity var(--duration-normal) var(--ease-out),
              transform var(--duration-normal) var(--ease-out);
}

.modal-backdrop.open .modal-content {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Exit animation */
.modal-backdrop.closing .modal-content {
  opacity: 0;
  transform: scale(0.95);
  transition-timing-function: var(--ease-in);
}
```

### Dropdown Menu

```css
.dropdown-menu {
  opacity: 0;
  transform: translateY(-8px);
  transform-origin: top;
  transition: opacity var(--duration-fast) var(--ease-out),
              transform var(--duration-fast) var(--ease-out);
  pointer-events: none;
}

.dropdown.open .dropdown-menu {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
```

### Accordion

```css
.accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--duration-normal) var(--ease-out);
}

.accordion.open .accordion-content {
  grid-template-rows: 1fr;
}

.accordion-inner {
  overflow: hidden;
}
```

### Toast Notification

```css
.toast {
  transform: translateX(100%);
  opacity: 0;
  transition: transform var(--duration-normal) var(--ease-out),
              opacity var(--duration-normal) var(--ease-out);
}

.toast.visible {
  transform: translateX(0);
  opacity: 1;
}

.toast.exiting {
  transform: translateX(100%);
  opacity: 0;
  transition-timing-function: var(--ease-in);
}
```

## Performance Optimization

### Performant Properties

Only animate properties that don't trigger layout:

| Property | Performance | Notes |
|----------|-------------|-------|
| `transform` | Best | GPU accelerated |
| `opacity` | Best | GPU accelerated |
| `filter` | Good | GPU accelerated |
| `background-color` | OK | Paint only |
| `box-shadow` | Avoid | Paint intensive |
| `width`, `height` | Avoid | Triggers layout |
| `top`, `left` | Avoid | Triggers layout |

### Performance Techniques

```css
/* Promote to GPU layer */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
}

/* Use transform instead of position */
/* Bad */
.slide-bad {
  left: 0;
  transition: left 300ms;
}
.slide-bad.active { left: 100px; }

/* Good */
.slide-good {
  transform: translateX(0);
  transition: transform 300ms;
}
.slide-good.active { transform: translateX(100px); }

/* Clean up will-change after animation */
.element {
  transition: transform 300ms;
}

.element:hover {
  will-change: transform;
}
```

## Accessibility

### Respecting Motion Preferences

```css
/* Reduced motion media query */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Alternative: provide instant feedback */
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: none;
  }

  .element:hover {
    /* Immediate state change, no motion */
  }
}
```

### Animation Tokens with Reduced Motion

```css
:root {
  --motion-duration: 200ms;
  --motion-easing: var(--ease-out);
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-duration: 0ms;
    --motion-easing: linear;
  }
}

.element {
  transition: transform var(--motion-duration) var(--motion-easing);
}
```

## Motion Design System

### Motion Tokens

```css
:root {
  /* Duration scale */
  --motion-duration-instant: 50ms;
  --motion-duration-fast: 100ms;
  --motion-duration-normal: 200ms;
  --motion-duration-slow: 400ms;

  /* Easing */
  --motion-ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --motion-ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --motion-ease-exit: cubic-bezier(0.4, 0, 1, 1);

  /* Composite tokens */
  --motion-enter: var(--motion-duration-normal) var(--motion-ease-enter);
  --motion-exit: var(--motion-duration-fast) var(--motion-ease-exit);
  --motion-standard: var(--motion-duration-normal) var(--motion-ease-default);
}

/* Usage */
.element {
  transition: transform var(--motion-enter);
}
```

## Anti-Patterns

### Common Motion Mistakes

**Too slow:**
```css
/* Bad - sluggish */
.button { transition-duration: 800ms; }

/* Good - snappy */
.button { transition-duration: 150ms; }
```

**Wrong easing:**
```css
/* Bad - element bounces in weirdly */
.modal { transition: transform 300ms ease-in; }

/* Good - natural deceleration */
.modal { transition: transform 300ms ease-out; }
```

**Animating layout properties:**
```css
/* Bad - triggers layout */
.expand { transition: width 300ms; }

/* Good - GPU accelerated */
.expand { transition: transform 300ms; }
```

**Linear motion:**
```css
/* Bad - robotic */
.slide { transition: transform 200ms linear; }

/* Good - natural */
.slide { transition: transform 200ms ease-out; }
```

**Ignoring reduced motion:**
```css
/* Bad - no accommodation */
.spinner { animation: spin 1s infinite; }

/* Good - respects preferences */
@media (prefers-reduced-motion: reduce) {
  .spinner { animation: none; }
}
```

## Summary

Purposeful motion enhances user experience:

| Principle | Implementation |
|-----------|----------------|
| **Duration** | 100-300ms for most UI |
| **Easing** | Ease-out for enter, ease-in for exit |
| **Performance** | Only animate transform/opacity |
| **Accessibility** | Respect prefers-reduced-motion |
| **Consistency** | Use motion tokens system-wide |
| **Purpose** | Every animation serves a function |

**Key Guidelines:**
1. Keep durations under 400ms for UI
2. Use ease-out for elements entering view
3. Only animate GPU-accelerated properties
4. Always provide reduced-motion alternatives
5. Define motion tokens in design system
6. Test animations on low-powered devices

---

**When to use this skill:**
- Creating micro-interactions
- Designing component transitions
- Building animation systems
- Optimizing animation performance
- Ensuring animation accessibility


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

