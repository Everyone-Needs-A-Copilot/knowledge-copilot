---
last_updated: 2026-02-25
status: active
name: micro-interaction-design
description: Design small, contained product moments - triggers, rules, feedback, loops. Use for delightful, responsive interface details.
triggers:
  files: ["**/animation/**", "**/transition/**", "**/micro/**", "**/interaction/**"]
  keywords: ["micro-interaction", "animation", "transition", "hover", "feedback", "motion", "delight", "polish", "feel"]
allowed-tools: Read, Write, Edit
---

# Micro-Interaction Design Skill

Master guide for designing micro-interactions - the small, contained product moments that provide feedback, guide tasks, and add delight to interfaces.

## Philosophy

**Details make the experience.** Users may not consciously notice micro-interactions, but they feel them. Great micro-interactions make interfaces feel alive and responsive.

**Function before flair.** Every micro-interaction should serve a purpose. Decoration without function is clutter.

**Subtlety wins.** The best micro-interactions are felt, not seen. They guide without demanding attention.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Micro-Interaction Anatomy

### The Four Parts

Every micro-interaction has:

| Part | Purpose | Example |
|------|---------|---------|
| **Trigger** | Initiates the interaction | User clicks, system event |
| **Rules** | What happens | Toggle state, animate |
| **Feedback** | Shows result | Visual change, sound |
| **Loops/Modes** | Modifies over time | Repeat, evolve |

### Example: Like Button

```
Trigger: User taps heart icon
  │
  ▼
Rules: If not liked → like
       If liked → unlike
  │
  ▼
Feedback: Heart fills/empties
          Scale animation
          Particle burst
  │
  ▼
Loop: Count increments/decrements
```

---

## Common Micro-Interactions

### Button Feedback

**Basic states**:
```css
.button {
  background: var(--primary);
  transition: all 0.15s ease-out;
}

.button:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0) scale(0.98);
}

.button:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}
```

**Loading state**:
```css
.button.loading {
  pointer-events: none;
  position: relative;
}

.button.loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Toggle Switches

```css
.toggle {
  width: 48px;
  height: 24px;
  background: var(--gray-300);
  border-radius: 12px;
  transition: background 0.2s ease;
  cursor: pointer;
}

.toggle::after {
  content: '';
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  position: absolute;
  left: 2px;
  top: 2px;
  transition: transform 0.2s ease;
}

.toggle.on {
  background: var(--primary);
}

.toggle.on::after {
  transform: translateX(24px);
}
```

### Checkboxes

```css
.checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid var(--gray-400);
  border-radius: 4px;
  transition: all 0.15s ease;
}

.checkbox:checked {
  background: var(--primary);
  border-color: var(--primary);
}

.checkbox:checked::after {
  content: '';
  /* Checkmark drawing animation */
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  animation: draw 0.3s ease forwards;
}

@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```

### Form Field Focus

```css
.input {
  border: 1px solid var(--gray-300);
  border-radius: 4px;
  padding: 12px;
  transition: all 0.15s ease;
}

.input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.1);
}

/* Float label pattern */
.float-label {
  transform: translateY(12px);
  transition: transform 0.15s, font-size 0.15s;
}

.input:focus + .float-label,
.input:not(:placeholder-shown) + .float-label {
  transform: translateY(-8px);
  font-size: 0.75rem;
}
```

---

## Feedback Patterns

### Success Feedback

**Checkmark animation**:
```css
@keyframes checkmark {
  0% {
    stroke-dashoffset: 100;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

.success-check {
  stroke-dasharray: 100;
  animation: checkmark 0.4s ease forwards;
}
```

**Success pulse**:
```css
@keyframes success-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(34, 197, 94, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0);
  }
}

.success {
  animation: success-pulse 1s ease;
}
```

### Error Feedback

**Shake animation**:
```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-4px); }
  40%, 80% { transform: translateX(4px); }
}

.error {
  animation: shake 0.4s ease;
  border-color: var(--error);
}
```

### Loading States

**Skeleton loading**:
```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--gray-200) 0%,
    var(--gray-100) 50%,
    var(--gray-200) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

**Progress indicator**:
```css
.progress {
  height: 4px;
  background: var(--gray-200);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--primary);
  width: 0%;
  transition: width 0.3s ease;
}
```

---

## Transition Patterns

### Page Transitions

**Fade transition**:
```css
.page-enter {
  opacity: 0;
}

.page-enter-active {
  opacity: 1;
  transition: opacity 0.2s ease;
}

.page-exit {
  opacity: 1;
}

.page-exit-active {
  opacity: 0;
  transition: opacity 0.2s ease;
}
```

**Slide transition**:
```css
.slide-enter {
  transform: translateX(100%);
}

.slide-enter-active {
  transform: translateX(0);
  transition: transform 0.3s ease;
}

.slide-exit {
  transform: translateX(0);
}

.slide-exit-active {
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}
```

### Modal Transitions

```css
.modal-overlay {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.modal-overlay.open {
  opacity: 1;
}

.modal-content {
  transform: scale(0.95) translateY(-10px);
  opacity: 0;
  transition: all 0.2s ease;
}

.modal-content.open {
  transform: scale(1) translateY(0);
  opacity: 1;
}
```

### List Item Transitions

**Add item**:
```css
.list-item-enter {
  opacity: 0;
  transform: translateY(-10px);
}

.list-item-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.2s ease;
}
```

**Remove item**:
```css
.list-item-exit {
  opacity: 1;
  max-height: 100px; /* Set to item height */
}

.list-item-exit-active {
  opacity: 0;
  max-height: 0;
  margin: 0;
  padding: 0;
  transition: all 0.2s ease;
}
```

---

## Hover Interactions

### Card Hover

```css
.card {
  transition: all 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
```

### Image Hover

```css
.image-container {
  overflow: hidden;
}

.image-container img {
  transition: transform 0.3s ease;
}

.image-container:hover img {
  transform: scale(1.05);
}
```

### Link Hover

```css
.link {
  position: relative;
}

.link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: currentColor;
  transition: width 0.2s ease;
}

.link:hover::after {
  width: 100%;
}
```

### Button Icon Hover

```css
.button-icon {
  transition: transform 0.2s ease;
}

.button:hover .button-icon {
  transform: translateX(4px);
}

/* Or rotation */
.button:hover .button-icon {
  transform: rotate(90deg);
}
```

---

## Scroll Interactions

### Scroll-Triggered Animations

```javascript
// Intersection Observer for scroll animations
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll('.animate-on-scroll')
  .forEach(el => observer.observe(el));
```

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
}

.animate-on-scroll.animate-in {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.5s ease;
}
```

### Sticky Header Transition

```css
.header {
  transition: all 0.2s ease;
}

.header.scrolled {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 1rem; /* Smaller */
}
```

### Pull to Refresh

```
[Pull indicator]
      ↓
[Content moves down]
      ↓
[Spinner appears]
      ↓
[Content refreshes]
```

---

## Gesture Interactions

### Swipe to Delete

```css
.swipe-item {
  transform: translateX(0);
  transition: transform 0.2s ease;
}

.swipe-item.swiping {
  transition: none; /* Direct control during gesture */
}

.swipe-item.dismissed {
  transform: translateX(-100%);
  opacity: 0;
  transition: all 0.3s ease;
}
```

### Drag and Drop

```css
.draggable {
  cursor: grab;
  transition: transform 0.2s, box-shadow 0.2s;
}

.draggable.dragging {
  cursor: grabbing;
  transform: rotate(3deg);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.drop-target {
  transition: background 0.2s;
}

.drop-target.active {
  background: var(--primary-light);
  border: 2px dashed var(--primary);
}
```

### Long Press

```javascript
let timer;

element.addEventListener('touchstart', () => {
  timer = setTimeout(() => {
    // Long press action
    showContextMenu();
  }, 500);
});

element.addEventListener('touchend', () => {
  clearTimeout(timer);
});
```

---

## Timing and Easing

### Duration Guidelines

| Action | Duration | Use Case |
|--------|----------|----------|
| Instant | 0-100ms | Immediate feedback |
| Fast | 100-200ms | Small UI changes |
| Normal | 200-300ms | Standard transitions |
| Slow | 300-500ms | Emphasis, attention |
| Deliberate | 500ms+ | Complex animations |

### Easing Functions

```css
/* Standard easings */
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

/* Expressive easings */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-elastic: cubic-bezier(0.68, -0.6, 0.32, 1.6);
```

### When to Use Each

| Easing | Use When |
|--------|----------|
| `ease-out` | Elements entering (appearing) |
| `ease-in` | Elements exiting (disappearing) |
| `ease-in-out` | Elements moving/changing position |
| `linear` | Progress bars, continuous motion |
| `bounce/elastic` | Playful, attention-grabbing |

---

## Accessibility

### Reduced Motion

```css
/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Safe Animation Practices

- Keep animations under 500ms
- Avoid flashing (>3 per second)
- Provide pause/stop controls
- Don't block content with animation
- Ensure feedback is perceivable without motion

---

## Performance

### Hardware Acceleration

```css
/* GPU-accelerated properties */
.performant {
  transform: translateX(0); /* ✓ */
  opacity: 1; /* ✓ */
}

/* Avoid animating */
.slow {
  width: 100px; /* ✗ Triggers layout */
  margin: 10px; /* ✗ Triggers layout */
  box-shadow: ...; /* ✗ Can be slow */
}
```

### Will-Change Hint

```css
/* Use sparingly */
.will-animate {
  will-change: transform;
}

/* Remove after animation */
.will-animate.done {
  will-change: auto;
}
```

### Avoid Layout Thrashing

```javascript
// Bad: Causes reflow each iteration
elements.forEach(el => {
  el.style.height = el.offsetHeight + 10 + 'px';
});

// Good: Batch reads, then writes
const heights = elements.map(el => el.offsetHeight);
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px';
});
```

---

## Anti-Patterns

### 1. Animation for Animation's Sake

```
❌ Bad: Everything bounces and spins
✅ Good: Motion serves function
```

### 2. Blocking Interactions

```
❌ Bad: User must wait for animation
✅ Good: User can interact immediately
```

### 3. Inconsistent Timing

```
❌ Bad: Random durations everywhere
✅ Good: Consistent timing system
```

### 4. Jarring Transitions

```
❌ Bad: instant/none transitions
✅ Good: Smooth, natural motion
```

### 5. Ignoring Reduced Motion

```
❌ Bad: No reduced motion support
✅ Good: Respects user preferences
```

---

## Quick Reference

### Micro-Interaction Checklist

- [ ] Clear trigger (user or system)
- [ ] Appropriate duration (100-300ms typical)
- [ ] Meaningful feedback
- [ ] Consistent with brand/system
- [ ] Respects reduced motion
- [ ] GPU-accelerated (transform/opacity)
- [ ] Doesn't block interaction
- [ ] Adds value (function > decoration)

### Timing Quick Reference

| Animation Type | Duration |
|---------------|----------|
| Hover feedback | 150ms |
| Button press | 100ms |
| Toggle switch | 200ms |
| Modal open | 200-250ms |
| Page transition | 250-300ms |
| Loading skeleton | 1500ms loop |

### Property Quick Reference

| Animate | Avoid Animating |
|---------|----------------|
| `transform` | `width/height` |
| `opacity` | `margin/padding` |
| `clip-path` | `top/left/right/bottom` |
| `filter` | `font-size` |

---

## Summary

**Micro-interactions are the fingerprints of great design.**

1. Every interaction needs feedback
2. Function before flair
3. Keep it subtle (150-300ms)
4. Use GPU-accelerated properties
5. Respect reduced motion preferences
6. Be consistent across the system

*The best micro-interactions feel inevitable - users don't notice them, but they'd miss them if they were gone.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

