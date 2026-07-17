---
last_updated: 2026-02-25
status: active
name: performance-css
description: CSS performance optimization - render blocking, layout thrashing, paint efficiency, will-change, containment. Use when optimizing UI performance.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/*.jsx", "**/styles/**"]
  keywords: ["performance", "render", "paint", "layout", "reflow", "will-change", "containment", "critical CSS", "lazy"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Performance CSS

Optimize CSS for fast rendering and smooth interactions.

## Rendering Pipeline

| Stage | Triggers | Cost |
|-------|----------|------|
| Style | CSS changes, class toggles | Low |
| Layout | Width, height, position changes | High |
| Paint | Color, shadow, background changes | Medium |
| Composite | Transform, opacity changes | Low |

### Property Cost Reference

| Low Cost (Composite) | Medium Cost (Paint) | High Cost (Layout) |
|---------------------|---------------------|-------------------|
| `transform` | `color` | `width`, `height` |
| `opacity` | `background` | `padding`, `margin` |
| `filter` | `box-shadow` | `border` |
| `clip-path` | `text-shadow` | `font-size` |
| | `border-radius` | `position` |
| | | `display` |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Animations and Transitions

### Prefer Composite Properties

```css
/* Bad: Triggers layout */
.animate-bad {
  transition: left 0.3s, top 0.3s;
}
.animate-bad:hover {
  left: 100px;
  top: 50px;
}

/* Good: Composite only */
.animate-good {
  transition: transform 0.3s;
}
.animate-good:hover {
  transform: translate(100px, 50px);
}

/* Scaling */
.scale-bad { transition: width 0.3s; }
.scale-bad:hover { width: 200px; }

.scale-good { transition: transform 0.3s; }
.scale-good:hover { transform: scale(1.5); }
```

### will-change Optimization

```css
/* Hint to browser for upcoming changes */
.will-animate {
  will-change: transform;
}

/* Apply only when needed */
.card { /* No will-change by default */ }
.card:hover {
  will-change: transform;
  transform: translateY(-5px);
}

/* Or apply via JavaScript before animation */
element.style.willChange = 'transform';
// After animation
element.style.willChange = 'auto';
```

**will-change Rules:**
- Don't apply to everything
- Remove after animation completes
- Avoid on too many elements
- Creates new stacking context

### GPU Acceleration

```css
/* Force GPU layer */
.gpu-accelerated {
  transform: translateZ(0);
  /* or */
  will-change: transform;
}

/* For fixed elements */
.fixed-header {
  position: fixed;
  transform: translateZ(0); /* Prevents repaint on scroll */
}
```

## Layout Performance

### Avoid Layout Thrashing

```tsx
// Bad: Forces multiple layouts
function bad() {
  const el = document.getElementById('box');
  el.style.width = el.offsetWidth + 10 + 'px'; // Read then write
  el.style.height = el.offsetHeight + 10 + 'px'; // Read then write
}

// Good: Batch reads and writes
function good() {
  const el = document.getElementById('box');
  const width = el.offsetWidth; // Read
  const height = el.offsetHeight; // Read
  el.style.width = width + 10 + 'px'; // Write
  el.style.height = height + 10 + 'px'; // Write
}

// Best: Use requestAnimationFrame
function best() {
  const el = document.getElementById('box');
  const width = el.offsetWidth;
  const height = el.offsetHeight;

  requestAnimationFrame(() => {
    el.style.width = width + 10 + 'px';
    el.style.height = height + 10 + 'px';
  });
}
```

### CSS Containment

```css
/* Isolate layout, paint, and style calculations */
.contained {
  contain: layout;        /* Isolate layout */
  contain: paint;         /* Isolate painting */
  contain: style;         /* Isolate counters/quotes */
  contain: size;          /* Fixed size, ignores children */
  contain: strict;        /* All containment */
  contain: content;       /* layout + paint + style */
}

/* Common use cases */
.card {
  contain: content; /* Good for repeated items */
}

.sidebar {
  contain: layout; /* Sidebar changes don't affect main */
}

.offscreen {
  contain: strict; /* Not visible, minimize work */
}
```

### content-visibility

```css
/* Skip rendering of off-screen content */
.article {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px; /* Estimated height for scrollbar */
}

/* Hidden but accessible */
.collapsed {
  content-visibility: hidden;
}
```

## Selector Performance

### Efficient Selectors

```css
/* Efficient: ID, class, element */
#header { }
.button { }
div { }

/* Less efficient: Attribute, pseudo-class */
[type="text"] { }
:nth-child(odd) { }

/* Avoid: Universal, complex combinators */
* { }
div > * > span { }

/* Right-to-left matching */
/* Browser reads: span → * → div */
div > * > span { } /* Scans all spans, then checks ancestors */

/* Better: Specific class */
.nested-span { }
```

### Selector Guidelines

| Good | Avoid |
|------|-------|
| `.btn` | `div.container .btn` |
| `.card-title` | `.card > div > h2` |
| `[data-state]` | `*[data-state]` |

## Critical CSS

### Extract Above-the-Fold Styles

```html
<head>
  <!-- Inline critical CSS -->
  <style>
    .header { /* Critical styles */ }
    .hero { /* Above fold */ }
  </style>

  <!-- Defer non-critical CSS -->
  <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

### CSS Loading Strategies

```html
<!-- Critical: Inline -->
<style>/* Critical CSS */</style>

<!-- High priority -->
<link rel="stylesheet" href="critical.css">

<!-- Lazy load below-fold -->
<link rel="stylesheet" href="components.css" media="print" onload="this.media='all'">

<!-- Preload fonts -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
```

## Reduce CSS Size

### Efficient CSS

```css
/* Use shorthand */
.bad { margin-top: 10px; margin-right: 20px; margin-bottom: 10px; margin-left: 20px; }
.good { margin: 10px 20px; }

/* Combine selectors */
.bad-a { color: blue; }
.bad-b { color: blue; }
.good-a, .good-b { color: blue; }

/* Use CSS variables */
.bad-1 { background: #0066cc; }
.bad-2 { border-color: #0066cc; }
:root { --primary: #0066cc; }
.good-1 { background: var(--primary); }
.good-2 { border-color: var(--primary); }
```

### Remove Unused CSS

```js
// PurgeCSS config
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  css: ['./src/**/*.css'],
  safelist: ['dynamic-class', /^modal-/],
};
```

## Paint Performance

### Reduce Paint Complexity

```css
/* Expensive paint operations */
.expensive {
  box-shadow: 0 10px 20px rgba(0,0,0,0.3);
  border-radius: 20px;
  filter: blur(5px);
}

/* Optimize with pseudo-element on separate layer */
.optimized {
  position: relative;
}

.optimized::after {
  content: '';
  position: absolute;
  inset: 0;
  box-shadow: 0 10px 20px rgba(0,0,0,0.3);
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.3s;
  will-change: opacity; /* Separate layer */
}

.optimized:hover::after {
  opacity: 1;
}
```

### Avoid Paint on Scroll

```css
/* Fixed elements need GPU layer */
.fixed-header {
  position: fixed;
  top: 0;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Use transform for scroll-triggered animations */
.parallax {
  will-change: transform;
}
```

## Font Performance

```css
/* Font display strategy */
@font-face {
  font-family: 'Custom';
  src: url('font.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately, swap when loaded */
}

/* Subsetting (load only needed characters) */
@font-face {
  font-family: 'Icons';
  src: url('icons.woff2') format('woff2');
  unicode-range: U+E000-E100; /* Only icon characters */
}

/* Variable fonts (one file, multiple weights) */
@font-face {
  font-family: 'Variable';
  src: url('variable.woff2') format('woff2-variations');
  font-weight: 100 900;
}
```

## Measuring Performance

### DevTools

```js
// Performance marks
performance.mark('css-start');
// Load CSS
performance.mark('css-end');
performance.measure('CSS Load', 'css-start', 'css-end');

// Layout shift
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log('Layout Shift:', entry.value);
  }
}).observe({ type: 'layout-shift', buffered: true });
```

### Lighthouse Metrics

| Metric | CSS Impact |
|--------|------------|
| FCP (First Contentful Paint) | Critical CSS, font loading |
| LCP (Largest Contentful Paint) | Image/text visibility |
| CLS (Cumulative Layout Shift) | Font fallback, image sizing |
| TBT (Total Blocking Time) | Large CSS files, complex styles |

## React Performance Patterns

```tsx
// Memoize expensive style calculations
const styles = useMemo(() => ({
  transform: `translateX(${offset}px)`,
  transition: isAnimating ? 'transform 0.3s' : 'none',
}), [offset, isAnimating]);

// Avoid inline styles for static values
// Bad
<div style={{ display: 'flex', gap: '1rem' }}>

// Good - use classes
<div className="flex gap-4">

// CSS-in-JS: Extract static styles
const StaticButton = styled.button`
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
`;
```

## Best Practices Summary

| Category | Best Practice |
|----------|---------------|
| Animations | Use `transform` and `opacity` only |
| Layout | Use `contain` for isolated components |
| Selectors | Prefer classes, avoid deep nesting |
| Loading | Inline critical CSS, defer rest |
| Paints | Minimize shadow/blur animations |
| Fonts | Use `font-display: swap` |
| Measurement | Monitor CLS, LCP in production |

## Quick Reference

```css
/* Performant animations */
transform: translate() | scale() | rotate();
opacity: 0-1;
filter: blur() | brightness();

/* GPU acceleration */
transform: translateZ(0);
will-change: transform;

/* Layout containment */
contain: content;
content-visibility: auto;

/* Font loading */
font-display: swap;

/* Efficient selectors */
.specific-class { }
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

