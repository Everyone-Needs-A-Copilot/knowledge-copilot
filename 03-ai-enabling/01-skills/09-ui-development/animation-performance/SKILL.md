---
last_updated: 2026-02-25
status: active
name: animation-performance
description: High-performance CSS and JS animations - 60fps techniques, GPU acceleration, FLIP, reduced motion. Use when building smooth animations and transitions.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/*.jsx", "**/animations/**"]
  keywords: ["animation", "transition", "keyframes", "60fps", "performance", "transform", "opacity", "will-change", "FLIP", "reduced motion"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Animation Performance

Create smooth, 60fps animations that don't compromise user experience.

## Animation Fundamentals

### The 60fps Target

| Frame Budget | Impact |
|--------------|--------|
| 16.67ms | 60fps - smooth |
| 33.33ms | 30fps - noticeable jank |
| 100ms | 10fps - unusable |

### Composite-Only Properties

**Animating these properties is fast (GPU-accelerated):**

```css
/* Fast - Composite only */
transform: translate(), scale(), rotate(), skew();
opacity: 0-1;
filter: blur(), brightness(), contrast();

/* Slow - Triggers layout */
width, height, padding, margin, border;
top, left, right, bottom;
font-size, line-height;

/* Medium - Triggers paint */
color, background, box-shadow;
border-radius, outline;
```


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## CSS Transitions

### Basic Transitions

```css
.button {
  background: var(--color-primary);
  transform: translateY(0);
  transition:
    transform 0.2s ease-out,
    background 0.2s ease-out;
}

.button:hover {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
}
```

### Timing Functions

```css
/* Built-in */
transition-timing-function: linear;
transition-timing-function: ease;
transition-timing-function: ease-in;
transition-timing-function: ease-out;
transition-timing-function: ease-in-out;

/* Custom cubic-bezier */
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);      /* Material ease */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55); /* Overshoot */
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

/* Usage */
.element {
  transition: transform 0.3s var(--ease-smooth);
}
```

### Staggered Transitions

```css
.list-item {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.3s ease-out,
    transform 0.3s ease-out;
}

.list-item:nth-child(1) { transition-delay: 0ms; }
.list-item:nth-child(2) { transition-delay: 50ms; }
.list-item:nth-child(3) { transition-delay: 100ms; }
.list-item:nth-child(4) { transition-delay: 150ms; }

.list.is-visible .list-item {
  opacity: 1;
  transform: translateY(0);
}
```

## CSS Keyframe Animations

### Basic Keyframes

```css
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: slide-up 0.3s ease-out forwards;
}
```

### Complex Animations

```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

.button--error {
  animation: shake 0.3s ease-out;
}
```

### Animation Properties

```css
.element {
  animation-name: slide-up;
  animation-duration: 0.3s;
  animation-timing-function: ease-out;
  animation-delay: 0s;
  animation-iteration-count: 1; /* or infinite */
  animation-direction: normal; /* reverse, alternate */
  animation-fill-mode: forwards; /* none, backwards, both */
  animation-play-state: running; /* paused */

  /* Shorthand */
  animation: slide-up 0.3s ease-out 0s 1 normal forwards;
}
```

## FLIP Technique

### First, Last, Invert, Play

```tsx
function flipAnimation(element: HTMLElement, callback: () => void) {
  // First: Get initial position
  const first = element.getBoundingClientRect();

  // Last: Execute the change
  callback();

  // Get final position
  const last = element.getBoundingClientRect();

  // Invert: Calculate the difference
  const deltaX = first.left - last.left;
  const deltaY = first.top - last.top;
  const deltaW = first.width / last.width;
  const deltaH = first.height / last.height;

  // Play: Animate from inverted to final
  element.animate([
    {
      transform: `translate(${deltaX}px, ${deltaY}px) scale(${deltaW}, ${deltaH})`,
    },
    { transform: 'none' },
  ], {
    duration: 300,
    easing: 'ease-out',
  });
}

// Usage
flipAnimation(card, () => {
  // Move card to new position in DOM
  container.appendChild(card);
});
```

### React FLIP Hook

```tsx
function useFlip<T extends HTMLElement>(deps: any[]) {
  const ref = useRef<T>(null);
  const firstRect = useRef<DOMRect | null>(null);

  useLayoutEffect(() => {
    if (!ref.current) return;

    // Store first position before deps change
    firstRect.current = ref.current.getBoundingClientRect();
  });

  useLayoutEffect(() => {
    if (!ref.current || !firstRect.current) return;

    const last = ref.current.getBoundingClientRect();
    const deltaX = firstRect.current.left - last.left;
    const deltaY = firstRect.current.top - last.top;

    if (deltaX === 0 && deltaY === 0) return;

    ref.current.animate([
      { transform: `translate(${deltaX}px, ${deltaY}px)` },
      { transform: 'none' },
    ], { duration: 300, easing: 'ease-out' });
  }, deps);

  return ref;
}

// Usage
function Item({ index }) {
  const ref = useFlip<HTMLDivElement>([index]);
  return <div ref={ref}>Item</div>;
}
```

## GPU Acceleration

### Triggering Hardware Acceleration

```css
/* Create GPU layer */
.gpu-accelerated {
  transform: translateZ(0);
  /* or */
  will-change: transform;
  /* or */
  backface-visibility: hidden;
}

/* Use sparingly - each layer uses memory */
```

### will-change Best Practices

```css
/* Bad: Always on */
.element {
  will-change: transform;
}

/* Good: Only when needed */
.element:hover {
  will-change: transform;
}

/* Better: Via JavaScript */
element.addEventListener('mouseenter', () => {
  element.style.willChange = 'transform';
});

element.addEventListener('transitionend', () => {
  element.style.willChange = 'auto';
});
```

## Web Animations API

```tsx
// Basic animation
element.animate([
  { transform: 'translateX(0)' },
  { transform: 'translateX(100px)' },
], {
  duration: 300,
  easing: 'ease-out',
  fill: 'forwards',
});

// With control
const animation = element.animate(keyframes, options);

animation.pause();
animation.play();
animation.reverse();
animation.cancel();
animation.finish();

// Events
animation.onfinish = () => console.log('done');
animation.oncancel = () => console.log('cancelled');

// Promise-based
await animation.finished;
```

### React Animation Hook

```tsx
function useAnimation() {
  const elementRef = useRef<HTMLElement>(null);
  const animationRef = useRef<Animation | null>(null);

  const animate = useCallback((
    keyframes: Keyframe[],
    options: KeyframeAnimationOptions
  ) => {
    if (!elementRef.current) return;

    animationRef.current = elementRef.current.animate(keyframes, options);
    return animationRef.current.finished;
  }, []);

  const cancel = useCallback(() => {
    animationRef.current?.cancel();
  }, []);

  return { ref: elementRef, animate, cancel };
}

// Usage
function Component() {
  const { ref, animate } = useAnimation();

  const handleClick = async () => {
    await animate([
      { transform: 'scale(1)' },
      { transform: 'scale(1.1)' },
      { transform: 'scale(1)' },
    ], { duration: 200 });
  };

  return <button ref={ref} onClick={handleClick}>Click</button>;
}
```

## Reduced Motion

### Respecting User Preferences

```css
/* Full animation by default */
.element {
  transition: transform 0.3s ease-out;
}

/* Reduce or remove for motion-sensitive users */
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: none;
    /* or shorter/simpler animation */
    transition: opacity 0.1s ease-out;
  }

  /* Remove decorative animations */
  .decorative-animation {
    animation: none;
  }
}
```

### React Hook

```tsx
function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(() => {
    const query = window.matchMedia('(prefers-reduced-motion: reduce)');
    return query.matches;
  });

  useEffect(() => {
    const query = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    query.addEventListener('change', handler);
    return () => query.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}

// Usage
function AnimatedComponent() {
  const prefersReducedMotion = usePrefersReducedMotion();

  return (
    <div
      className={prefersReducedMotion ? 'simple-fade' : 'complex-animation'}
    />
  );
}
```

## Common Animation Patterns

### Modal/Dialog

```css
/* Backdrop */
.modal-backdrop {
  opacity: 0;
  transition: opacity 0.2s ease-out;
}

.modal-backdrop.is-open {
  opacity: 1;
}

/* Modal content */
.modal-content {
  opacity: 0;
  transform: scale(0.95) translateY(-20px);
  transition:
    opacity 0.2s ease-out,
    transform 0.2s ease-out;
}

.modal-content.is-open {
  opacity: 1;
  transform: scale(1) translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .modal-content {
    transform: none;
    transition: opacity 0.1s ease-out;
  }
}
```

### Skeleton Loading

```css
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.skeleton {
  position: relative;
  overflow: hidden;
  background: #e0e0e0;
}

.skeleton::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.5),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@media (prefers-reduced-motion: reduce) {
  .skeleton::after {
    animation: none;
  }
}
```

### Page Transitions

```css
.page-enter {
  opacity: 0;
  transform: translateX(20px);
}

.page-enter-active {
  opacity: 1;
  transform: translateX(0);
  transition:
    opacity 0.3s ease-out,
    transform 0.3s ease-out;
}

.page-exit {
  opacity: 1;
  transform: translateX(0);
}

.page-exit-active {
  opacity: 0;
  transform: translateX(-20px);
  transition:
    opacity 0.3s ease-out,
    transform 0.3s ease-out;
}
```

## Performance Checklist

| Check | Action |
|-------|--------|
| Properties | Only animate transform/opacity |
| Duration | Keep under 300ms for interactions |
| will-change | Apply only when needed |
| Reduced motion | Test with preference enabled |
| Layout shifts | Avoid animating layout properties |
| Frame rate | Test on low-end devices |

## Quick Reference

```css
/* Performant properties */
transform: translate(), scale(), rotate();
opacity: 0-1;

/* Timing functions */
ease-out: decelerate (entering)
ease-in: accelerate (exiting)
ease-in-out: both (moving)

/* Recommended durations */
Micro-interactions: 100-200ms
Transitions: 200-300ms
Complex animations: 300-500ms

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```


## Quality Tests

### Visual Fidelity Test
- Implementation matches design within acceptable tolerance
- **PASS:** Spacing, colors, and typography match design tokens exactly
- **FAIL:** Visible deviations from design that aren't documented as intentional

### Accessibility Test
- Component is usable with keyboard-only and screen reader
- **PASS:** All interactive elements reachable by Tab, operable by Enter/Space
- **FAIL:** Mouse-only interactions or missing ARIA labels

