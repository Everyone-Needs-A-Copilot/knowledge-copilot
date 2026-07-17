---
last_updated: 2026-02-25
status: active
name: layout-grid-systems
description: Column grids, fluid layouts, responsive breakpoints, and spatial organization. Use when designing page layouts.
triggers:
  files: ["**/grid.*", "**/layout.*", "**/breakpoints.*", "**/container.*"]
  keywords: ["grid system", "column grid", "responsive layout", "breakpoints", "fluid grid", "12-column", "layout grid"]
allowed-tools: Read, Write, Edit
---

# Layout Grid Systems: Deep Expertise Skill

Comprehensive guide to designing and implementing grid systems for consistent, responsive layouts.

## Grid System Fundamentals

### What Grids Provide

| Benefit | Description |
|---------|-------------|
| **Consistency** | Predictable element placement |
| **Hierarchy** | Clear visual organization |
| **Efficiency** | Faster design decisions |
| **Responsiveness** | Adaptable across viewports |
| **Alignment** | Unified visual rhythm |

### Grid Anatomy

```
┌─────────────────────────────────────────────────────────────┐
│ Margin                                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Container                                            │    │
│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │    │
│  │  │Col │ │Col │ │Col │ │Col │ │Col │ │Col │  ...    │    │
│  │  │    │ │    │ │    │ │    │ │    │ │    │         │    │
│  │  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘         │    │
│  │     ↑ Gutter ↑                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Grid Components:**

| Component | Description | Typical Values |
|-----------|-------------|----------------|
| **Container** | Max-width wrapper | 1200px, 1440px |
| **Columns** | Vertical divisions | 12, 16 columns |
| **Gutters** | Space between columns | 16px, 24px, 32px |
| **Margins** | Outer page spacing | 16px–64px (responsive) |


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Column Grid Systems

### The 12-Column Grid

The 12-column grid is the industry standard due to its divisibility:

```
12 columns divisible by: 1, 2, 3, 4, 6, 12

Common layouts:
├── 12 (full width)
├── 6 + 6 (halves)
├── 4 + 4 + 4 (thirds)
├── 3 + 3 + 3 + 3 (quarters)
├── 8 + 4 (content + sidebar)
├── 3 + 6 + 3 (centered content)
└── 2 + 8 + 2 (narrow centered)
```

### CSS Grid Implementation

```css
:root {
  --grid-columns: 12;
  --grid-gutter: 24px;
  --container-max: 1200px;
  --container-padding: 24px;
}

.container {
  width: 100%;
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--container-padding);
}

.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), 1fr);
  gap: var(--grid-gutter);
}

/* Column span utilities */
.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-5 { grid-column: span 5; }
.col-6 { grid-column: span 6; }
.col-7 { grid-column: span 7; }
.col-8 { grid-column: span 8; }
.col-9 { grid-column: span 9; }
.col-10 { grid-column: span 10; }
.col-11 { grid-column: span 11; }
.col-12 { grid-column: span 12; }
```

### Flexbox Grid Alternative

```css
.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 calc(var(--grid-gutter) / -2);
}

.col {
  flex: 1 0 0%;
  padding: 0 calc(var(--grid-gutter) / 2);
}

/* Fixed column widths */
.col-1 { flex: 0 0 8.333%; max-width: 8.333%; }
.col-2 { flex: 0 0 16.666%; max-width: 16.666%; }
.col-3 { flex: 0 0 25%; max-width: 25%; }
.col-4 { flex: 0 0 33.333%; max-width: 33.333%; }
.col-6 { flex: 0 0 50%; max-width: 50%; }
.col-12 { flex: 0 0 100%; max-width: 100%; }
```

## Responsive Breakpoints

### Standard Breakpoint System

```css
:root {
  /* Breakpoint values */
  --bp-xs: 0;
  --bp-sm: 640px;
  --bp-md: 768px;
  --bp-lg: 1024px;
  --bp-xl: 1280px;
  --bp-2xl: 1536px;
}

/* Mobile-first media queries */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

### Responsive Grid Configuration

| Breakpoint | Columns | Gutter | Container | Margin |
|------------|---------|--------|-----------|--------|
| xs (0-639px) | 4 | 16px | 100% | 16px |
| sm (640-767px) | 8 | 16px | 100% | 24px |
| md (768-1023px) | 12 | 24px | 100% | 32px |
| lg (1024-1279px) | 12 | 24px | 960px | auto |
| xl (1280-1535px) | 12 | 32px | 1200px | auto |
| 2xl (1536px+) | 12 | 32px | 1400px | auto |

### Responsive Column Classes

```css
/* Base (mobile) */
.col-12 { grid-column: span 12; }

/* Small screens and up */
@media (min-width: 640px) {
  .sm\:col-6 { grid-column: span 6; }
  .sm\:col-4 { grid-column: span 4; }
}

/* Medium screens and up */
@media (min-width: 768px) {
  .md\:col-6 { grid-column: span 6; }
  .md\:col-4 { grid-column: span 4; }
  .md\:col-3 { grid-column: span 3; }
}

/* Large screens and up */
@media (min-width: 1024px) {
  .lg\:col-8 { grid-column: span 8; }
  .lg\:col-4 { grid-column: span 4; }
  .lg\:col-3 { grid-column: span 3; }
}
```

## Container Patterns

### Container Types

```css
/* Fixed-width container */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--container-padding);
}

/* Fluid container */
.container-fluid {
  width: 100%;
  padding: 0 var(--container-padding);
}

/* Narrow container (content) */
.container-narrow {
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  padding: 0 var(--container-padding);
}

/* Wide container (full-bleed sections) */
.container-wide {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--container-padding);
}
```

### Responsive Container

```css
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 16px;
}

@media (min-width: 640px) {
  .container { padding: 0 24px; }
}

@media (min-width: 768px) {
  .container { padding: 0 32px; }
}

@media (min-width: 1024px) {
  .container { max-width: 960px; }
}

@media (min-width: 1280px) {
  .container { max-width: 1200px; }
}

@media (min-width: 1536px) {
  .container { max-width: 1400px; }
}
```

## Layout Patterns

### Holy Grail Layout

```css
.layout-holy-grail {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

/* Responsive collapse */
@media (max-width: 768px) {
  .layout-holy-grail {
    grid-template-areas:
      "header"
      "nav"
      "main"
      "aside"
      "footer";
    grid-template-columns: 1fr;
  }
}
```

### Sidebar Layout

```css
.layout-sidebar {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--grid-gutter);
}

.layout-sidebar-right {
  grid-template-columns: 1fr 280px;
}

/* Collapsible sidebar */
@media (max-width: 1024px) {
  .layout-sidebar {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 280px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .sidebar.open {
    transform: translateX(0);
  }
}
```

### Card Grid Layout

```css
/* Auto-fit cards */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--grid-gutter);
}

/* Fixed column card grid */
.card-grid-fixed {
  display: grid;
  gap: var(--grid-gutter);
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .card-grid-fixed {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .card-grid-fixed {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .card-grid-fixed {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Masonry-Style Layout

```css
/* CSS Columns masonry */
.masonry {
  columns: 3;
  column-gap: var(--grid-gutter);
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: var(--grid-gutter);
}

/* Responsive columns */
@media (max-width: 1024px) {
  .masonry { columns: 2; }
}

@media (max-width: 640px) {
  .masonry { columns: 1; }
}
```

## Subgrid

### Using CSS Subgrid

```css
/* Parent grid */
.parent-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

/* Child inherits parent columns */
.child-subgrid {
  grid-column: span 8;
  display: grid;
  grid-template-columns: subgrid;
}

/* Grandchild aligns to main grid */
.grandchild {
  grid-column: span 4;
}
```

### Subgrid for Alignment

```css
/* Card grid with aligned content */
.card-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* header, body, footer */
}

.card-header { /* Aligns across cards */ }
.card-body { /* Aligns across cards */ }
.card-footer { /* Aligns across cards */ }
```

## Grid Utilities

### Alignment Utilities

```css
/* Justify items (horizontal) */
.justify-start { justify-items: start; }
.justify-center { justify-items: center; }
.justify-end { justify-items: end; }
.justify-stretch { justify-items: stretch; }

/* Align items (vertical) */
.items-start { align-items: start; }
.items-center { align-items: center; }
.items-end { align-items: end; }
.items-stretch { align-items: stretch; }

/* Justify content (row distribution) */
.justify-content-start { justify-content: start; }
.justify-content-center { justify-content: center; }
.justify-content-end { justify-content: end; }
.justify-content-between { justify-content: space-between; }
.justify-content-around { justify-content: space-around; }
.justify-content-evenly { justify-content: space-evenly; }

/* Align content (column distribution) */
.content-start { align-content: start; }
.content-center { align-content: center; }
.content-end { align-content: end; }
.content-between { align-content: space-between; }
```

### Gap Utilities

```css
:root {
  --gap-0: 0;
  --gap-1: 4px;
  --gap-2: 8px;
  --gap-3: 12px;
  --gap-4: 16px;
  --gap-5: 20px;
  --gap-6: 24px;
  --gap-8: 32px;
  --gap-10: 40px;
  --gap-12: 48px;
}

.gap-0 { gap: var(--gap-0); }
.gap-1 { gap: var(--gap-1); }
.gap-2 { gap: var(--gap-2); }
.gap-4 { gap: var(--gap-4); }
.gap-6 { gap: var(--gap-6); }
.gap-8 { gap: var(--gap-8); }

/* Directional gaps */
.gap-x-4 { column-gap: var(--gap-4); }
.gap-y-4 { row-gap: var(--gap-4); }
```

### Column Start/End

```css
/* Starting positions */
.col-start-1 { grid-column-start: 1; }
.col-start-2 { grid-column-start: 2; }
.col-start-3 { grid-column-start: 3; }
/* ... */

/* Ending positions */
.col-end-12 { grid-column-end: 12; }
.col-end-13 { grid-column-end: 13; }

/* Full width regardless of start */
.col-full { grid-column: 1 / -1; }
```

## Design System Integration

### Grid Tokens

```css
:root {
  /* Grid structure */
  --grid-columns-mobile: 4;
  --grid-columns-tablet: 8;
  --grid-columns-desktop: 12;

  /* Gutters */
  --grid-gutter-mobile: 16px;
  --grid-gutter-tablet: 24px;
  --grid-gutter-desktop: 32px;

  /* Containers */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;

  /* Margins */
  --margin-mobile: 16px;
  --margin-tablet: 24px;
  --margin-desktop: 32px;
}
```

### Responsive Grid Component

```tsx
interface GridProps {
  columns?: number | { sm?: number; md?: number; lg?: number; xl?: number };
  gap?: 'none' | 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

function Grid({ columns = 12, gap = 'md', children }: GridProps) {
  const gapMap = {
    none: 'gap-0',
    sm: 'gap-4',
    md: 'gap-6',
    lg: 'gap-8'
  };

  return (
    <div className={`grid grid-cols-${columns} ${gapMap[gap]}`}>
      {children}
    </div>
  );
}
```

## Anti-Patterns

### Common Grid Mistakes

**Fixed pixel widths:**
```css
/* Bad - doesn't adapt */
.column { width: 300px; }

/* Good - flexible */
.column { grid-column: span 4; }
```

**Inconsistent gutters:**
```css
/* Bad - random spacing */
.section-1 { gap: 20px; }
.section-2 { gap: 32px; }
.section-3 { gap: 18px; }

/* Good - systematic */
.section { gap: var(--grid-gutter); }
```

**Breaking the grid:**
```css
/* Bad - arbitrary positioning */
.element { margin-left: 47px; }

/* Good - grid-aligned */
.element { grid-column: 2 / span 4; }
```

**Nested containers:**
```css
/* Bad - nested containers add unwanted padding */
.container .container { /* Double padding! */ }

/* Good - container only at top level */
.section { padding: 0 var(--container-padding); }
```

## Summary

Effective grid systems provide structure and flexibility:

| Principle | Implementation |
|-----------|----------------|
| **Consistency** | Use design tokens for all values |
| **Responsiveness** | Mobile-first breakpoints |
| **Flexibility** | Column spans, not fixed widths |
| **Simplicity** | 12-column covers most needs |
| **Alignment** | Subgrid for nested alignment |
| **Semantics** | Named areas for clarity |

**Key Guidelines:**
1. Start with a 12-column grid as default
2. Use consistent gutters from spacing scale
3. Define clear breakpoints with purpose
4. Container max-widths prevent too-wide content
5. Use CSS Grid for 2D, Flexbox for 1D layouts
6. Test at all breakpoints

---

**When to use this skill:**
- Establishing page layout systems
- Creating responsive component layouts
- Building design system grid foundations
- Implementing card grids and galleries
- Designing dashboard layouts


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

