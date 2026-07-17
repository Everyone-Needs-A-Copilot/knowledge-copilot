---
last_updated: 2026-02-25
status: active
name: responsive-patterns
description: Mobile-first responsive design - breakpoints, fluid layouts, container queries. Use for responsive UI.
triggers:
  files: ["**/styles/**", "**/*.css", "**/*.scss", "**/tailwind.config.*"]
  keywords: ["responsive", "breakpoint", "mobile-first", "media query", "fluid", "container query", "viewport", "grid", "flexbox"]
allowed-tools: Read, Write, Edit
---

# Responsive Patterns

Comprehensive guide to mobile-first responsive design patterns, breakpoint strategies, and modern CSS techniques for creating adaptive user interfaces.

## Table of Contents

1. [Mobile-First Philosophy](#mobile-first-philosophy)
2. [Breakpoint Strategies](#breakpoint-strategies)
3. [Fluid Typography](#fluid-typography)
4. [CSS Grid Responsive Patterns](#css-grid-responsive-patterns)
5. [Flexbox Responsive Patterns](#flexbox-responsive-patterns)
6. [Container Queries](#container-queries)
7. [Aspect Ratios](#aspect-ratios)
8. [Responsive Images](#responsive-images)
9. [Touch Targets](#touch-targets)
10. [Responsive Tables](#responsive-tables)
11. [Hiding and Showing Content](#hiding-and-showing-content)
12. [Tailwind Responsive Utilities](#tailwind-responsive-utilities)
13. [Testing Responsiveness](#testing-responsiveness)
14. [Anti-Patterns](#anti-patterns)

---


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Mobile-First Philosophy

### Core Principles

**Start with constraints, enhance progressively:**

```css
/* ❌ Desktop-first (legacy approach) */
.container {
  width: 1200px;
  padding: 40px;
}

@media (max-width: 768px) {
  .container {
    width: 100%;
    padding: 20px;
  }
}

/* ✅ Mobile-first (progressive enhancement) */
.container {
  width: 100%;
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    max-width: 1200px;
    padding: 2.5rem;
  }
}
```

### Why Mobile-First?

1. **Performance**: Smaller CSS bundles for mobile devices
2. **Forced constraints**: Design for essential content first
3. **Progressive enhancement**: Add complexity as screen space increases
4. **Future-proof**: Easier to add features than remove them
5. **Accessibility**: Constraints often improve usability

### Mobile-First Thinking

```css
/* Base styles: Mobile (320px+) */
.card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}

/* Tablet (640px+) */
@media (min-width: 640px) {
  .card {
    flex-direction: row;
    padding: 1.5rem;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .card {
    gap: 2rem;
    padding: 2rem;
  }
}

/* Large Desktop (1536px+) */
@media (min-width: 1536px) {
  .card {
    max-width: 1400px;
    margin-inline: auto;
  }
}
```

---

## Breakpoint Strategies

### Standard Breakpoint Systems

**Tailwind CSS Default Breakpoints:**

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'sm': '640px',   // Mobile landscape / Small tablet
      'md': '768px',   // Tablet portrait
      'lg': '1024px',  // Desktop / Tablet landscape
      'xl': '1280px',  // Large desktop
      '2xl': '1536px', // Extra large desktop
    },
  },
}
```

**Bootstrap-Style Breakpoints:**

```css
/* Extra small devices (portrait phones) */
/* Default: No media query */

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) { }

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) { }

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) { }

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) { }

/* Extra extra large devices (1400px and up) */
@media (min-width: 1400px) { }
```

### Content-Based Breakpoints

**Let content dictate breakpoints, not devices:**

```css
/* Navigation that breaks when items wrap */
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

/* Add hamburger menu when space gets tight */
@media (max-width: 45em) { /* ~720px - content-based */
  .nav {
    flex-direction: column;
  }

  .nav-toggle {
    display: block;
  }
}
```

### Named Breakpoint Variables

```css
/* CSS Custom Properties for Breakpoints */
:root {
  --bp-mobile: 320px;
  --bp-mobile-lg: 480px;
  --bp-tablet: 768px;
  --bp-desktop: 1024px;
  --bp-desktop-lg: 1280px;
  --bp-desktop-xl: 1536px;
}

/* Usage with @custom-media (PostCSS) */
@custom-media --mobile (min-width: 320px);
@custom-media --tablet (min-width: 768px);
@custom-media --desktop (min-width: 1024px);
```

### Breakpoint Mixins (SCSS)

```scss
// _breakpoints.scss
$breakpoints: (
  'mobile': 320px,
  'mobile-lg': 480px,
  'tablet': 768px,
  'desktop': 1024px,
  'desktop-lg': 1280px,
  'desktop-xl': 1536px,
);

@mixin respond-to($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (min-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  } @else {
    @warn "Breakpoint '#{$breakpoint}' not found in $breakpoints map.";
  }
}

// Usage
.component {
  padding: 1rem;

  @include respond-to('tablet') {
    padding: 2rem;
  }

  @include respond-to('desktop') {
    padding: 3rem;
  }
}
```

### Range-Based Media Queries

```css
/* Between two breakpoints */
@media (min-width: 640px) and (max-width: 1023px) {
  .tablet-only {
    display: block;
  }
}

/* Up to a breakpoint (max-width) - use sparingly */
@media (max-width: 767px) {
  .mobile-only {
    display: block;
  }
}

/* Modern range syntax (Level 4) */
@media (640px <= width < 1024px) {
  .tablet-range {
    display: block;
  }
}
```

---

## Fluid Typography

### CSS Clamp() Function

**Modern fluid scaling between min and max:**

```css
/* Syntax: clamp(MIN, PREFERRED, MAX) */

h1 {
  /* Scales between 1.5rem (mobile) and 3rem (desktop) */
  font-size: clamp(1.5rem, 5vw, 3rem);
}

h2 {
  font-size: clamp(1.25rem, 4vw, 2.5rem);
}

p {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
}
```

### Calculating Fluid Values

**Formula: `clamp(MIN, MIN + (MAX - MIN) * ((100vw - MIN_VP) / (MAX_VP - MIN_VP)), MAX)`**

```css
/* Fluid spacing between 1rem (375px) and 2rem (1440px) */
.section {
  padding-block: clamp(
    1rem,
    1rem + 1 * ((100vw - 23.4375rem) / 66.5625),
    2rem
  );
}

/* Simplified with calc() */
.section {
  padding-block: clamp(1rem, 0.6479rem + 1.5023vw, 2rem);
}
```

### Fluid Type Scale Generator

```css
/* Modular scale that adjusts with viewport */
:root {
  --fluid-min-width: 320;
  --fluid-max-width: 1440;

  --fluid-min-size: 16;
  --fluid-max-size: 20;

  --fluid-min-ratio: 1.2;
  --fluid-max-ratio: 1.333;
}

/* Base font size */
body {
  font-size: clamp(
    1rem,
    0.8rem + 0.4vw,
    1.25rem
  );
}

/* Scale multipliers */
.text-xs { font-size: clamp(0.75rem, 0.6rem + 0.3vw, 0.9375rem); }
.text-sm { font-size: clamp(0.875rem, 0.7rem + 0.35vw, 1.09375rem); }
.text-base { font-size: clamp(1rem, 0.8rem + 0.4vw, 1.25rem); }
.text-lg { font-size: clamp(1.125rem, 0.9rem + 0.45vw, 1.40625rem); }
.text-xl { font-size: clamp(1.266rem, 1.013rem + 0.507vw, 1.758rem); }
.text-2xl { font-size: clamp(1.424rem, 1.139rem + 0.571vw, 1.977rem); }
.text-3xl { font-size: clamp(1.602rem, 1.282rem + 0.641vw, 2.222rem); }
.text-4xl { font-size: clamp(1.802rem, 1.442rem + 0.722vw, 2.5rem); }
```

### Fluid Line Height

```css
/* Adjust line-height with viewport */
p {
  font-size: clamp(1rem, 0.8rem + 0.4vw, 1.25rem);
  line-height: clamp(1.5, 1.4 + 0.2vw, 1.7);
}

/* Optical sizing for better readability */
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.1; /* Tighter for large text */
}

.body-text {
  font-size: clamp(1rem, 2vw, 1.125rem);
  line-height: 1.6; /* More open for body copy */
}
```

### Fluid Spacing System

```css
/* Consistent fluid spacing scale */
:root {
  --space-3xs: clamp(0.25rem, 0.2rem + 0.1vw, 0.3125rem);
  --space-2xs: clamp(0.5rem, 0.4rem + 0.2vw, 0.625rem);
  --space-xs: clamp(0.75rem, 0.6rem + 0.3vw, 0.9375rem);
  --space-sm: clamp(1rem, 0.8rem + 0.4vw, 1.25rem);
  --space-md: clamp(1.5rem, 1.2rem + 0.6vw, 1.875rem);
  --space-lg: clamp(2rem, 1.6rem + 0.8vw, 2.5rem);
  --space-xl: clamp(3rem, 2.4rem + 1.2vw, 3.75rem);
  --space-2xl: clamp(4rem, 3.2rem + 1.6vw, 5rem);
  --space-3xl: clamp(6rem, 4.8rem + 2.4vw, 7.5rem);
}

/* Usage */
.section {
  padding-block: var(--space-xl);
}

.card {
  padding: var(--space-md);
  gap: var(--space-sm);
}
```

---

## CSS Grid Responsive Patterns

### Auto-Fit Grid (Intrinsic Layout)

```css
/* Grid that automatically adjusts columns */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* Variant: auto-fill (creates empty columns) */
.grid-fill {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
```

### Responsive Grid Areas

```css
/* Mobile: Single column */
.layout {
  display: grid;
  grid-template-areas:
    "header"
    "main"
    "sidebar"
    "footer";
  gap: 1rem;
}

/* Desktop: Classic layout */
@media (min-width: 1024px) {
  .layout {
    grid-template-columns: 250px 1fr;
    grid-template-areas:
      "header header"
      "sidebar main"
      "footer footer";
    gap: 2rem;
  }
}

.header { grid-area: header; }
.main { grid-area: main; }
.sidebar { grid-area: sidebar; }
.footer { grid-area: footer; }
```

### RAM Pattern (Repeat, Auto, Minmax)

```css
/* Responsive cards without media queries */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: clamp(1rem, 3vw, 2rem);
}

/* Explanation:
   - repeat(): Creates columns
   - auto-fit: Adjusts column count to available space
   - minmax(): Sets min/max column width
   - min(100%, 300px): Never wider than container
   - 1fr: Fills available space
*/
```

### Responsive Grid with Breakpoints

```css
/* Mobile: Stack */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet: 2 columns */
@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* Desktop: 3 columns */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

/* Large Desktop: 4 columns */
@media (min-width: 1536px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Asymmetric Grid Patterns

```css
/* Feature + List Pattern */
.feature-grid {
  display: grid;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .feature-grid {
    grid-template-columns: 2fr 1fr;
  }

  .feature-item:first-child {
    grid-column: 1 / -1; /* Full width */
  }
}

/* Masonry-Style (with subgrid) */
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-auto-rows: 50px;
  gap: 1rem;
}

.masonry-item {
  display: grid;
  grid-row: span var(--row-span, 4);
}
```

### Holy Grail Layout

```css
.holy-grail {
  display: grid;
  min-height: 100vh;
  grid-template-rows: auto 1fr auto;
}

@media (min-width: 768px) {
  .holy-grail {
    grid-template-columns: 200px 1fr 200px;
    grid-template-rows: auto 1fr auto;
  }

  .header {
    grid-column: 1 / -1;
  }

  .footer {
    grid-column: 1 / -1;
  }
}
```

---

## Flexbox Responsive Patterns

### Flex Wrap Pattern

```css
/* Automatically wraps items */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-wrap > * {
  flex: 1 1 300px; /* Grow, shrink, basis */
}
```

### Flex Direction Switch

```css
/* Mobile: Stack */
.flex-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Desktop: Row */
@media (min-width: 768px) {
  .flex-container {
    flex-direction: row;
    align-items: center;
  }
}
```

### Equal-Width Columns

```css
.flex-equal {
  display: flex;
  gap: 1.5rem;
}

.flex-equal > * {
  flex: 1; /* Equal width distribution */
}

/* With minimum width */
.flex-equal-min {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-equal-min > * {
  flex: 1 1 250px;
}
```

### Sidebar Layout (Flexbox)

```css
/* Mobile: Stack */
.flex-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Desktop: Sidebar + Main */
@media (min-width: 1024px) {
  .flex-sidebar {
    flex-direction: row;
  }

  .sidebar {
    flex: 0 0 250px; /* Fixed width */
  }

  .main {
    flex: 1; /* Fill remaining space */
  }
}
```

### Media Object Pattern

```css
/* Responsive media object (image + content) */
.media {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.media-image {
  width: 100%;
  max-width: 200px;
}

@media (min-width: 640px) {
  .media {
    flex-direction: row;
    align-items: flex-start;
  }

  .media-image {
    flex-shrink: 0;
    width: 150px;
  }

  .media-content {
    flex: 1;
  }
}
```

### Sticky Footer (Flexbox)

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1; /* Pushes footer to bottom */
}

footer {
  flex-shrink: 0;
}
```

### Navigation Patterns

```css
/* Mobile: Stack */
.nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Desktop: Horizontal */
@media (min-width: 768px) {
  .nav {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

/* Alternative: Wrap navigation */
.nav-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

@media (min-width: 768px) {
  .nav-wrap {
    justify-content: flex-start;
  }
}
```

---

## Container Queries

### Basic Container Query

```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query container size (not viewport) */
.card {
  display: flex;
  flex-direction: column;
}

@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}

@container card (min-width: 600px) {
  .card {
    gap: 2rem;
    padding: 2rem;
  }
}
```

### Container Query Units

```css
.container {
  container-type: inline-size;
}

.child {
  /* Container query units */
  font-size: clamp(1rem, 3cqi, 2rem); /* cqi = container inline query */
  padding: 2cqw; /* cqw = container query width */
  margin-block: 1cqh; /* cqh = container query height */

  /* Available units:
     - cqw: 1% of container width
     - cqh: 1% of container height
     - cqi: 1% of container inline size
     - cqb: 1% of container block size
     - cqmin: smaller of cqi or cqb
     - cqmax: larger of cqi or cqb
  */
}
```

### Responsive Component (Container-Based)

```css
/* Card that adapts to its container, not viewport */
.card-wrapper {
  container-type: inline-size;
  container-name: card-wrapper;
}

.card {
  padding: 1rem;
  display: grid;
  gap: 1rem;
}

/* Small container (sidebar) */
@container card-wrapper (min-width: 300px) {
  .card {
    grid-template-columns: 1fr;
  }

  .card-image {
    aspect-ratio: 16 / 9;
  }
}

/* Medium container (main content) */
@container card-wrapper (min-width: 500px) {
  .card {
    grid-template-columns: 200px 1fr;
    gap: 1.5rem;
  }

  .card-image {
    aspect-ratio: 1;
  }
}

/* Large container (full width) */
@container card-wrapper (min-width: 800px) {
  .card {
    grid-template-columns: 300px 1fr 200px;
    gap: 2rem;
    padding: 2rem;
  }
}
```

### Named Containers

```css
/* Multiple named containers */
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}

.main {
  container-type: inline-size;
  container-name: main;
}

/* Query specific containers */
@container sidebar (min-width: 250px) {
  .widget {
    display: block;
  }
}

@container main (min-width: 600px) {
  .article {
    columns: 2;
  }
}
```

### Container Query with Style Queries (Future)

```css
/* Style-based container queries (experimental) */
@container style(--theme: dark) {
  .card {
    background: #1a1a1a;
    color: #ffffff;
  }
}

@container style(--layout: compact) {
  .card {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
}
```

---

## Aspect Ratios

### Modern aspect-ratio Property

```css
/* Maintain aspect ratio without padding hack */
.video-wrapper {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.square {
  aspect-ratio: 1;
}

.portrait {
  aspect-ratio: 3 / 4;
}

/* Responsive aspect ratios */
.responsive-media {
  aspect-ratio: 16 / 9;
}

@media (min-width: 768px) {
  .responsive-media {
    aspect-ratio: 21 / 9; /* Wider on desktop */
  }
}
```

### Responsive Images with Aspect Ratio

```css
.image-container {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.image-container img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Different ratios for different breakpoints */
.hero-image {
  aspect-ratio: 4 / 3; /* Mobile: More vertical */
}

@media (min-width: 768px) {
  .hero-image {
    aspect-ratio: 16 / 9; /* Desktop: Wider */
  }
}
```

### Legacy Padding-Bottom Technique

```css
/* Fallback for older browsers */
.aspect-ratio-legacy {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 = 9/16 * 100 */
}

.aspect-ratio-legacy > * {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

/* With modern support detection */
.aspect-box {
  aspect-ratio: 16 / 9;
}

@supports not (aspect-ratio: 1) {
  .aspect-box {
    padding-bottom: 56.25%;
  }
}
```

---

## Responsive Images

### Srcset and Sizes

```html
<!-- Responsive image with multiple sources -->
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w,
    image-1600.jpg 1600w
  "
  sizes="
    (min-width: 1024px) 800px,
    (min-width: 768px) 600px,
    100vw
  "
  alt="Responsive image"
  loading="lazy"
/>
```

**Explanation:**
- `srcset`: Available image variants with widths
- `sizes`: Display size at different breakpoints
- Browser selects optimal image based on viewport and DPR

### Picture Element (Art Direction)

```html
<!-- Different crops for different viewports -->
<picture>
  <!-- Desktop: Landscape -->
  <source
    media="(min-width: 1024px)"
    srcset="hero-desktop-wide.jpg"
  />

  <!-- Tablet: Standard -->
  <source
    media="(min-width: 768px)"
    srcset="hero-tablet.jpg"
  />

  <!-- Mobile: Portrait crop -->
  <img
    src="hero-mobile.jpg"
    alt="Hero image"
    loading="lazy"
  />
</picture>
```

### Modern Image Formats

```html
<picture>
  <!-- WebP for modern browsers -->
  <source
    type="image/webp"
    srcset="
      image-400.webp 400w,
      image-800.webp 800w,
      image-1200.webp 1200w
    "
    sizes="(min-width: 768px) 50vw, 100vw"
  />

  <!-- AVIF for cutting-edge browsers -->
  <source
    type="image/avif"
    srcset="
      image-400.avif 400w,
      image-800.avif 800w,
      image-1200.avif 1200w
    "
    sizes="(min-width: 768px) 50vw, 100vw"
  />

  <!-- Fallback to JPEG -->
  <img
    src="image-800.jpg"
    srcset="
      image-400.jpg 400w,
      image-800.jpg 800w,
      image-1200.jpg 1200w
    "
    sizes="(min-width: 768px) 50vw, 100vw"
    alt="Responsive image with modern formats"
    loading="lazy"
  />
</picture>
```

### CSS Responsive Background Images

```css
/* Mobile-first background images */
.hero {
  background-image: url('hero-mobile.jpg');
  background-size: cover;
  background-position: center;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('hero-tablet.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-desktop.jpg');
  }
}

/* With resolution switching */
@media (min-width: 1024px) and (-webkit-min-device-pixel-ratio: 2),
       (min-width: 1024px) and (min-resolution: 192dpi) {
  .hero {
    background-image: url('hero-desktop@2x.jpg');
  }
}
```

### Lazy Loading

```html
<!-- Native lazy loading -->
<img
  src="image.jpg"
  loading="lazy"
  alt="Lazy loaded image"
/>

<!-- With Intersection Observer (JavaScript) -->
<img
  data-src="image-large.jpg"
  src="placeholder-tiny.jpg"
  class="lazy-load"
  alt="Progressive image loading"
/>
```

```css
/* Blur-up placeholder */
.lazy-load {
  filter: blur(10px);
  transition: filter 0.3s;
}

.lazy-load.loaded {
  filter: blur(0);
}
```

---

## Touch Targets

### Minimum Touch Target Size

```css
/* WCAG 2.1 Level AAA: 44x44px minimum */
.button,
.link,
.interactive {
  min-height: 44px;
  min-width: 44px;

  /* For smaller visual elements, increase padding */
  padding: 0.75rem 1.25rem;
}

/* Icon buttons */
.icon-button {
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Increase touch target without increasing visual size */
.small-target {
  position: relative;
}

.small-target::before {
  content: '';
  position: absolute;
  inset: -12px; /* Expands clickable area */
  cursor: pointer;
}
```

### Touch-Friendly Spacing

```css
/* Mobile: Larger gaps between interactive elements */
.nav-mobile {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* Minimum 8px between targets */
}

.nav-mobile a {
  padding: 1rem;
  min-height: 48px;
}

/* Desktop: Can be tighter */
@media (min-width: 768px) {
  .nav-desktop {
    gap: 0.25rem;
  }

  .nav-desktop a {
    padding: 0.5rem 1rem;
    min-height: auto;
  }
}
```

### Hover vs Touch States

```css
/* Touch-friendly interactions */
.button {
  padding: 0.875rem 1.5rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;

  /* Visible focus for keyboard navigation */
  outline: 2px solid transparent;
  outline-offset: 2px;
  transition: background 0.2s, outline 0.2s;
}

/* Hover only on devices that support it */
@media (hover: hover) {
  .button:hover {
    background: #0056b3;
  }
}

/* Active state for touch */
.button:active {
  transform: scale(0.98);
}

/* Focus for keyboard */
.button:focus-visible {
  outline-color: #007bff;
}
```

---

## Responsive Tables

### Horizontal Scroll Pattern

```css
/* Mobile: Horizontal scroll */
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
}

table {
  min-width: 600px;
  width: 100%;
}

/* Desktop: Full width */
@media (min-width: 768px) {
  table {
    min-width: 100%;
  }
}
```

### Card-Stack Pattern (Reflowed Table)

```css
/* Mobile: Stack cells */
table {
  border: 0;
}

thead {
  display: none; /* Hide headers */
}

tbody tr {
  display: block;
  margin-bottom: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
}

tbody td {
  display: block;
  text-align: right;
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
}

tbody td::before {
  content: attr(data-label);
  float: left;
  font-weight: 600;
}

tbody td:last-child {
  border-bottom: 0;
}

/* Desktop: Normal table */
@media (min-width: 768px) {
  thead {
    display: table-header-group;
  }

  tbody tr {
    display: table-row;
    margin: 0;
    border: 0;
  }

  tbody td {
    display: table-cell;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }

  tbody td::before {
    display: none;
  }
}
```

```html
<!-- HTML structure -->
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Name">John Doe</td>
      <td data-label="Email">john@example.com</td>
      <td data-label="Role">Admin</td>
    </tr>
  </tbody>
</table>
```

### Hide Columns Pattern

```css
/* Mobile: Hide less critical columns */
.table-responsive th:nth-child(3),
.table-responsive td:nth-child(3),
.table-responsive th:nth-child(4),
.table-responsive td:nth-child(4) {
  display: none;
}

/* Tablet: Show more columns */
@media (min-width: 640px) {
  .table-responsive th:nth-child(3),
  .table-responsive td:nth-child(3) {
    display: table-cell;
  }
}

/* Desktop: Show all columns */
@media (min-width: 1024px) {
  .table-responsive th:nth-child(4),
  .table-responsive td:nth-child(4) {
    display: table-cell;
  }
}
```

### Grid-Based Table

```css
/* Modern CSS Grid approach */
.data-table {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 640px) {
  .data-table {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .data-table {
    grid-template-columns: 2fr 3fr 1fr 1fr;
    gap: 0;
  }

  .data-table > * {
    padding: 1rem;
    border-bottom: 1px solid #ddd;
  }
}
```

---

## Hiding and Showing Content

### Display Utilities

```css
/* Hide on mobile, show on desktop */
.hidden-mobile {
  display: none;
}

@media (min-width: 768px) {
  .hidden-mobile {
    display: block;
  }
}

/* Show on mobile, hide on desktop */
.visible-mobile {
  display: block;
}

@media (min-width: 768px) {
  .visible-mobile {
    display: none;
  }
}
```

### Accessible Hiding (Screen Readers)

```css
/* Hide visually but keep for screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Show on focus (skip links) */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Content Reordering

```css
/* Mobile: Visual order different from DOM order */
.flex-order {
  display: flex;
  flex-direction: column;
}

.flex-order .header { order: 1; }
.flex-order .sidebar { order: 3; }
.flex-order .main { order: 2; }

/* Desktop: Restore natural order */
@media (min-width: 1024px) {
  .flex-order {
    flex-direction: row;
  }

  .flex-order .header { order: 0; }
  .flex-order .sidebar { order: 0; }
  .flex-order .main { order: 0; }
}
```

**Warning:** Only reorder visually. Keep semantic HTML order for accessibility.

### Progressive Disclosure

```css
/* Show more content on larger screens */
.truncated {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (min-width: 768px) {
  .truncated {
    -webkit-line-clamp: 5;
  }
}

@media (min-width: 1024px) {
  .truncated {
    display: block;
    -webkit-line-clamp: unset;
  }
}
```

---

## Tailwind Responsive Utilities

### Breakpoint Prefixes

```html
<!-- Mobile-first responsive classes -->
<div class="
  w-full           <!-- 100% on mobile -->
  md:w-1/2         <!-- 50% on tablet -->
  lg:w-1/3         <!-- 33% on desktop -->
  xl:w-1/4         <!-- 25% on large desktop -->

  p-4              <!-- padding 1rem on mobile -->
  md:p-6           <!-- padding 1.5rem on tablet -->
  lg:p-8           <!-- padding 2rem on desktop -->

  text-sm          <!-- small text on mobile -->
  lg:text-base     <!-- base text on desktop -->
">
  Responsive element
</div>
```

### Responsive Grid

```html
<div class="
  grid
  grid-cols-1       <!-- 1 column on mobile -->
  sm:grid-cols-2    <!-- 2 columns on small screens -->
  md:grid-cols-3    <!-- 3 columns on medium screens -->
  lg:grid-cols-4    <!-- 4 columns on large screens -->
  gap-4
  md:gap-6
  lg:gap-8
">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>
```

### Responsive Flexbox

```html
<div class="
  flex
  flex-col          <!-- Column on mobile -->
  md:flex-row       <!-- Row on tablet+ -->
  items-start
  md:items-center
  gap-4
  md:gap-6
">
  <div class="flex-1">Main content</div>
  <aside class="w-full md:w-64">Sidebar</aside>
</div>
```

### Show/Hide Utilities

```html
<!-- Hide on mobile, show on desktop -->
<div class="hidden lg:block">
  Desktop-only content
</div>

<!-- Show on mobile, hide on desktop -->
<div class="block lg:hidden">
  Mobile-only content
</div>

<!-- Show only on specific breakpoint range -->
<div class="hidden md:block lg:hidden">
  Tablet-only content
</div>
```

### Responsive Typography

```html
<h1 class="
  text-2xl          <!-- 1.5rem on mobile -->
  sm:text-3xl       <!-- 1.875rem on small -->
  md:text-4xl       <!-- 2.25rem on medium -->
  lg:text-5xl       <!-- 3rem on large -->
  xl:text-6xl       <!-- 3.75rem on xl -->

  leading-tight
  md:leading-snug

  tracking-tight
  md:tracking-normal
">
  Responsive Heading
</h1>
```

### Responsive Spacing

```html
<section class="
  px-4              <!-- horizontal padding mobile -->
  md:px-6
  lg:px-8
  xl:px-12

  py-8              <!-- vertical padding mobile -->
  md:py-12
  lg:py-16
  xl:py-24

  space-y-4         <!-- vertical spacing between children -->
  md:space-y-6
  lg:space-y-8
">
  <div>Section content</div>
</section>
```

### Custom Breakpoints (Tailwind Config)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      '3xl': '1920px',

      // Custom breakpoints
      'tablet': '640px',
      'laptop': '1024px',
      'desktop': '1280px',

      // Max-width breakpoints (use sparingly)
      'max-md': { 'max': '767px' },

      // Range breakpoints
      'tablet-only': { 'min': '640px', 'max': '1023px' },
    },
  },
}
```

### Container Queries (Tailwind)

```html
<!-- Tailwind v3.4+ supports container queries -->
<div class="@container">
  <div class="
    @sm:flex           <!-- flex when container > 384px -->
    @md:grid           <!-- grid when container > 448px -->
    @lg:grid-cols-2    <!-- 2 cols when container > 512px -->
  ">
    Content
  </div>
</div>
```

---

## Testing Responsiveness

### Browser DevTools

**Chrome DevTools:**
1. Open DevTools (F12 / Cmd+Option+I)
2. Toggle device toolbar (Cmd+Shift+M)
3. Select device preset or custom dimensions
4. Test at different DPR (Device Pixel Ratio)
5. Use "Responsive" mode and drag to resize

**Firefox Responsive Design Mode:**
1. Open Developer Tools (F12)
2. Toggle Responsive Design Mode (Cmd+Option+M)
3. Rotate device, change touch simulation
4. Screenshot full page at various sizes

### Testing Checklist

```markdown
## Responsive Testing Checklist

### Breakpoints
- [ ] 320px - Small mobile (iPhone SE)
- [ ] 375px - Standard mobile (iPhone 12/13)
- [ ] 414px - Large mobile (iPhone 12 Pro Max)
- [ ] 768px - Tablet portrait (iPad)
- [ ] 1024px - Tablet landscape / Small laptop
- [ ] 1280px - Desktop
- [ ] 1920px - Large desktop

### Common Devices
- [ ] iPhone SE (375x667)
- [ ] iPhone 12/13 (390x844)
- [ ] iPhone 12/13 Pro Max (428x926)
- [ ] iPad (810x1080)
- [ ] iPad Pro (1024x1366)
- [ ] Desktop (1920x1080)

### Orientation
- [ ] Portrait mode
- [ ] Landscape mode

### Content Tests
- [ ] Long text content (line length, readability)
- [ ] No horizontal scroll (except intentional)
- [ ] Images scale appropriately
- [ ] Forms are usable
- [ ] Navigation is accessible
- [ ] Touch targets are 44x44px minimum

### Visual Tests
- [ ] No overlapping elements
- [ ] Adequate spacing at all sizes
- [ ] Typography scales readably
- [ ] No cut-off content
- [ ] Aspect ratios maintained

### Performance
- [ ] Appropriate image sizes loaded
- [ ] No layout shifts (CLS)
- [ ] Fast interaction (FID)
```

### Automated Testing Tools

**Playwright Responsive Tests:**

```javascript
// playwright.config.js
module.exports = {
  projects: [
    {
      name: 'Mobile Chrome',
      use: {
        ...devices['iPhone 12'],
      },
    },
    {
      name: 'Mobile Safari',
      use: {
        ...devices['iPhone 12'],
      },
    },
    {
      name: 'Tablet',
      use: {
        ...devices['iPad Pro'],
      },
    },
    {
      name: 'Desktop',
      use: {
        viewport: { width: 1920, height: 1080 },
      },
    },
  ],
};

// Test file
test('responsive layout', async ({ page }) => {
  await page.goto('/');

  // Mobile viewport
  await page.setViewportSize({ width: 375, height: 667 });
  await expect(page.locator('.mobile-menu')).toBeVisible();
  await expect(page.locator('.desktop-menu')).toBeHidden();

  // Desktop viewport
  await page.setViewportSize({ width: 1920, height: 1080 });
  await expect(page.locator('.mobile-menu')).toBeHidden();
  await expect(page.locator('.desktop-menu')).toBeVisible();
});
```

**Cypress Viewport Testing:**

```javascript
// cypress/e2e/responsive.cy.js
describe('Responsive Design', () => {
  const sizes = [
    ['iphone-6', 375, 667],
    ['ipad-2', 768, 1024],
    ['macbook-15', 1440, 900],
  ];

  sizes.forEach(([name, width, height]) => {
    it(`should work on ${name}`, () => {
      cy.viewport(width, height);
      cy.visit('/');

      // Test responsive behavior
      cy.get('[data-testid="header"]').should('be.visible');
    });
  });
});
```

### Visual Regression Testing

**Percy (visual diff testing):**

```javascript
// Take snapshots at different widths
cy.visit('/');
cy.percySnapshot('Homepage', {
  widths: [375, 768, 1280, 1920],
});
```

**Backstop.js Configuration:**

```json
{
  "viewports": [
    {
      "label": "phone",
      "width": 375,
      "height": 667
    },
    {
      "label": "tablet",
      "width": 768,
      "height": 1024
    },
    {
      "label": "desktop",
      "width": 1920,
      "height": 1080
    }
  ],
  "scenarios": [
    {
      "label": "Homepage",
      "url": "http://localhost:3000"
    }
  ]
}
```

---

## Anti-Patterns

### 1. Fixed Widths Without Max-Width

```css
/* ❌ BAD: Fixed width breaks on small screens */
.container {
  width: 1200px;
}

/* ✅ GOOD: Responsive width with constraints */
.container {
  width: 100%;
  max-width: 1200px;
  padding-inline: 1rem;
}
```

### 2. Desktop-First Media Queries

```css
/* ❌ BAD: Desktop-first with max-width */
.element {
  font-size: 24px;
}

@media (max-width: 768px) {
  .element {
    font-size: 16px;
  }
}

/* ✅ GOOD: Mobile-first with min-width */
.element {
  font-size: 16px;
}

@media (min-width: 768px) {
  .element {
    font-size: 24px;
  }
}
```

### 3. Using Viewport Units for Everything

```css
/* ❌ BAD: Text becomes unreadable on small screens */
h1 {
  font-size: 10vw;
}

/* ✅ GOOD: Constrained fluid sizing */
h1 {
  font-size: clamp(1.5rem, 5vw, 3rem);
}
```

### 4. Hiding Content with display: none

```css
/* ❌ BAD: Hidden content still loaded */
@media (max-width: 768px) {
  .desktop-hero-image {
    display: none; /* Image still downloads */
  }
}

/* ✅ GOOD: Conditional loading with <picture> */
```

```html
<picture>
  <source media="(min-width: 768px)" srcset="large.jpg" />
  <img src="small.jpg" alt="Hero" />
</picture>
```

### 5. Too Many Breakpoints

```css
/* ❌ BAD: Overly specific breakpoints */
@media (min-width: 320px) { }
@media (min-width: 375px) { }
@media (min-width: 425px) { }
@media (min-width: 768px) { }
@media (min-width: 1024px) { }
@media (min-width: 1440px) { }
@media (min-width: 2560px) { }

/* ✅ GOOD: Fluid design with minimal breakpoints */
.element {
  font-size: clamp(1rem, 2vw + 0.5rem, 2rem);
  padding: clamp(1rem, 3vw, 3rem);
}

@media (min-width: 768px) {
  /* Only major layout changes */
}
```

### 6. Pixel-Perfect Design at All Sizes

```css
/* ❌ BAD: Trying to match exact design at every size */
@media (min-width: 768px) and (max-width: 769px) {
  .element {
    width: 384.5px;
  }
}

/* ✅ GOOD: Flexible, proportional design */
.element {
  width: 50%;
  max-width: 400px;
}
```

### 7. Not Testing on Real Devices

```markdown
❌ BAD: Only testing in Chrome DevTools
✅ GOOD: Test on actual mobile devices
✅ GOOD: Use BrowserStack/Sauce Labs for real device testing
✅ GOOD: Test with slow network conditions
```

### 8. Ignoring Touch Interactions

```css
/* ❌ BAD: Hover-only interactions */
.menu-item:hover .submenu {
  display: block;
}

/* ✅ GOOD: Touch-friendly interactions */
.menu-item.is-active .submenu {
  display: block;
}

@media (hover: hover) {
  .menu-item:hover .submenu {
    display: block;
  }
}
```

### 9. Not Using Relative Units

```css
/* ❌ BAD: Fixed pixel values */
.text {
  font-size: 16px;
  line-height: 24px;
  margin-bottom: 16px;
}

/* ✅ GOOD: Relative units */
.text {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 1em;
}
```

### 10. Horizontal Scrolling

```css
/* ❌ BAD: Content wider than viewport */
.wide-content {
  width: 1200px;
}

/* ✅ GOOD: Contained width */
.wide-content {
  max-width: 100%;
  overflow-x: auto; /* If horizontal scroll needed */
}
```

### 11. Forgetting About Landscape Mode

```css
/* ❌ BAD: Only considering portrait */
@media (max-width: 768px) {
  .hero {
    height: 100vh; /* Too tall in landscape */
  }
}

/* ✅ GOOD: Consider orientation */
@media (max-width: 768px) and (orientation: landscape) {
  .hero {
    height: auto;
    min-height: 400px;
  }
}
```

### 12. Not Planning for Content Growth

```css
/* ❌ BAD: Fixed heights that break with long content */
.card {
  height: 300px;
  overflow: hidden;
}

/* ✅ GOOD: Flexible heights */
.card {
  min-height: 300px;
  height: auto;
}
```

---

## Best Practices Summary

### Core Principles

1. **Mobile-first**: Start small, enhance progressively
2. **Fluid by default**: Use percentages, viewport units, and clamp()
3. **Breakpoints are major shifts**: Layout changes, not pixel-perfect adjustments
4. **Content informs design**: Let content dictate breakpoints
5. **Touch-friendly**: 44x44px minimum touch targets
6. **Performance matters**: Load appropriate assets for viewport
7. **Test on real devices**: Simulators don't catch everything
8. **Accessibility first**: Screen readers, keyboard navigation, focus states

### Quick Reference

```css
/* Fluid Container */
.container {
  width: min(100% - 2rem, 1200px);
  margin-inline: auto;
}

/* Fluid Typography */
h1 { font-size: clamp(1.5rem, 5vw, 3rem); }

/* Responsive Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: clamp(1rem, 3vw, 2rem);
}

/* Responsive Flexbox */
.flex {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex > * {
  flex: 1 1 300px;
}

/* Container Query */
.container {
  container-type: inline-size;
}

@container (min-width: 500px) {
  .card { grid-template-columns: 200px 1fr; }
}

/* Responsive Image */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Aspect Ratio */
.media {
  aspect-ratio: 16 / 9;
}

/* Touch Target */
.button {
  min-height: 44px;
  min-width: 44px;
}
```

---

## Resources

### Documentation
- [MDN: Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [CSS-Tricks: A Complete Guide to CSS Media Queries](https://css-tricks.com/a-complete-guide-to-css-media-queries/)
- [Web.dev: Responsive Images](https://web.dev/responsive-images/)
- [CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)

### Tools
- [Responsively App](https://responsively.app/) - Browser for responsive testing
- [BrowserStack](https://www.browserstack.com/) - Real device testing
- [Am I Responsive?](https://ui.dev/amiresponsive) - Quick preview tool
- [Polypane](https://polypane.app/) - Browser for developers

### Testing
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Performance audits
- [Percy](https://percy.io/) - Visual testing
- [Playwright](https://playwright.dev/) - E2E testing with multiple viewports

### Libraries
- [Tailwind CSS](https://tailwindcss.com/docs/responsive-design) - Utility-first responsive
- [Container Query Polyfill](https://github.com/GoogleChromeLabs/container-query-polyfill)

---

**End of Responsive Patterns Skill**

*Use this skill for mobile-first responsive design implementation, breakpoint strategies, fluid layouts, and modern CSS responsive techniques.*


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

