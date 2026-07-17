---
last_updated: 2026-02-25
status: active
name: css-grid-mastery
description: CSS Grid for complex two-dimensional layouts - grid template, areas, auto-fit, responsive patterns. Use when building page layouts or complex grids.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/*.jsx", "**/styles/**"]
  keywords: ["grid", "grid-template", "grid-area", "auto-fit", "minmax", "fr", "layout", "two-dimensional"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# CSS Grid Mastery

Master CSS Grid for powerful two-dimensional layouts.

## When to Use Grid vs Flexbox

| Use Grid For | Use Flexbox For |
|--------------|-----------------|
| Two-dimensional layouts | One-dimensional layouts |
| Page structure | Component internals |
| Complex alignment | Simple row/column |
| Grid-like content (cards) | Navigation, toolbars |
| Overlapping elements | Centering content |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Grid Fundamentals

### Basic Grid Setup

```css
.container {
  display: grid;
  grid-template-columns: 200px 1fr 200px;  /* 3 columns */
  grid-template-rows: auto 1fr auto;        /* 3 rows */
  gap: 1rem;                                 /* Gutter */
}
```

```tsx
// React/Tailwind
<div className="grid grid-cols-[200px_1fr_200px] grid-rows-[auto_1fr_auto] gap-4">
  {/* Grid items */}
</div>
```

### Grid Units

| Unit | Description | Example |
|------|-------------|---------|
| `fr` | Fractional unit | `1fr 2fr` (1:2 ratio) |
| `px` | Fixed pixels | `200px` |
| `%` | Percentage | `50%` |
| `auto` | Content-based | `auto` |
| `minmax()` | Min/max range | `minmax(200px, 1fr)` |
| `min-content` | Smallest content size | `min-content` |
| `max-content` | Largest content size | `max-content` |
| `fit-content()` | Clamp to max | `fit-content(300px)` |

## Defining Grid Structure

### Explicit Grid

```css
/* Fixed columns */
.grid {
  display: grid;
  grid-template-columns: 100px 200px 100px;
  grid-template-rows: 50px 100px;
}

/* Using repeat() */
.grid {
  grid-template-columns: repeat(3, 1fr);        /* 3 equal columns */
  grid-template-columns: repeat(4, 100px);      /* 4 fixed columns */
  grid-template-columns: repeat(2, 1fr 2fr);    /* Pattern: 1fr 2fr 1fr 2fr */
}

/* Mixed sizes */
.grid {
  grid-template-columns: 200px 1fr 200px;       /* Fixed sidebar, fluid main */
  grid-template-columns: minmax(200px, 300px) 1fr; /* Flexible sidebar */
}
```

### Grid Template Areas

```css
.page {
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
.nav    { grid-area: nav; }
.main   { grid-area: main; }
.aside  { grid-area: aside; }
.footer { grid-area: footer; }
```

```tsx
// React component
function PageLayout({ children }) {
  return (
    <div className="grid min-h-screen" style={{
      gridTemplateAreas: `
        "header header header"
        "nav    main   aside"
        "footer footer footer"
      `,
      gridTemplateColumns: '200px 1fr 200px',
      gridTemplateRows: 'auto 1fr auto',
    }}>
      <header style={{ gridArea: 'header' }}>Header</header>
      <nav style={{ gridArea: 'nav' }}>Nav</nav>
      <main style={{ gridArea: 'main' }}>{children}</main>
      <aside style={{ gridArea: 'aside' }}>Sidebar</aside>
      <footer style={{ gridArea: 'footer' }}>Footer</footer>
    </div>
  );
}
```

### Implicit Grid

```css
/* Auto-generated rows */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: minmax(100px, auto);  /* All implicit rows */
}

/* Auto-generated columns */
.grid {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 200px;
}
```

## Placing Items

### Line-Based Placement

```css
/* Span by line numbers */
.item {
  grid-column: 1 / 3;      /* Start line 1, end line 3 (spans 2) */
  grid-row: 2 / 4;         /* Start line 2, end line 4 (spans 2) */
}

/* Shorthand: column-start / column-end */
.item {
  grid-column: 1 / -1;     /* Full width (first to last line) */
}

/* Span keyword */
.item {
  grid-column: 1 / span 2; /* Start at 1, span 2 columns */
  grid-row: span 3;        /* Span 3 rows from current position */
}
```

### Named Lines

```css
.grid {
  display: grid;
  grid-template-columns:
    [full-start] 1fr
    [main-start] 2fr
    [main-end] 1fr
    [full-end];
}

.item {
  grid-column: main-start / main-end;
}

.full-width {
  grid-column: full-start / full-end;
}
```

### Area Placement

```css
.grid {
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* Empty cells use . */
.grid {
  grid-template-areas:
    "header header"
    ".      main"
    "footer footer";
}
```

## Alignment

### Container Alignment

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 100px);
  grid-template-rows: repeat(3, 100px);

  /* Align items within cells */
  justify-items: start | end | center | stretch;  /* Horizontal */
  align-items: start | end | center | stretch;    /* Vertical */
  place-items: center;  /* Shorthand: align-items justify-items */

  /* Align entire grid within container */
  justify-content: start | end | center | space-between | space-around | space-evenly;
  align-content: start | end | center | space-between | space-around | space-evenly;
  place-content: center;  /* Shorthand */
}
```

### Item Alignment

```css
.item {
  justify-self: start | end | center | stretch;  /* Horizontal */
  align-self: start | end | center | stretch;    /* Vertical */
  place-self: center;  /* Shorthand */
}
```

## Responsive Grid Patterns

### Auto-Fit and Auto-Fill

```css
/* Auto-fit: Columns expand to fill space */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

/* Auto-fill: Keeps empty tracks */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
```

| Pattern | Behavior |
|---------|----------|
| `auto-fit` | Collapses empty tracks, items expand |
| `auto-fill` | Keeps empty tracks, items don't expand |

### Responsive Card Grid

```css
/* Pure CSS responsive grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

/* With max columns */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
  gap: 1.5rem;
}
```

```tsx
// React/Tailwind
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6 p-4">
  {cards.map(card => (
    <Card key={card.id} {...card} />
  ))}
</div>
```

### Breakpoint-Based Layouts

```css
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

```tsx
// Tailwind
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => <Item key={item.id} {...item} />)}
</div>
```

### Responsive Layout Switch

```css
.page {
  display: grid;
  grid-template-areas:
    "header"
    "main"
    "sidebar"
    "footer";
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .page {
    grid-template-areas:
      "header header"
      "sidebar main"
      "footer footer";
    grid-template-columns: 250px 1fr;
  }
}

@media (min-width: 1024px) {
  .page {
    grid-template-areas:
      "header header header"
      "nav    main   aside"
      "footer footer footer";
    grid-template-columns: 200px 1fr 250px;
  }
}
```

## Common Layout Patterns

### Holy Grail Layout

```css
.holy-grail {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .holy-grail {
    grid-template-areas:
      "header"
      "nav"
      "main"
      "aside"
      "footer";
    grid-template-columns: 1fr;
    grid-template-rows: auto auto 1fr auto auto;
  }
}
```

### Card Grid with Featured Item

```css
.featured-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.featured-grid .featured {
  grid-column: span 2;
  grid-row: span 2;
}

/* Or using :first-child */
.featured-grid > :first-child {
  grid-column: 1 / 3;
  grid-row: 1 / 3;
}
```

### Masonry-Style (with known columns)

```css
.masonry {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 10px;  /* Small row height */
  gap: 1rem;
}

.masonry-item {
  /* Each item spans different rows */
}

.masonry-item.small { grid-row: span 20; }
.masonry-item.medium { grid-row: span 30; }
.masonry-item.large { grid-row: span 40; }
```

### Full-Bleed Layout

```css
.full-bleed-layout {
  display: grid;
  grid-template-columns:
    1fr
    min(65ch, 100% - 2rem)
    1fr;
}

.full-bleed-layout > * {
  grid-column: 2;  /* Center column */
}

.full-bleed-layout > .full-bleed {
  grid-column: 1 / -1;  /* Full width */
}
```

### Pancake Stack

```css
.pancake {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

/* Header and footer take needed space */
/* Main expands to fill remaining */
```

### RAM (Repeat, Auto, Minmax)

```css
/* The most useful responsive pattern */
.ram {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
  gap: 1rem;
}
```

## Overlapping Content

```css
.overlap-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-template-rows: repeat(4, 100px);
}

.image {
  grid-column: 1 / 5;
  grid-row: 1 / 4;
}

.text {
  grid-column: 3 / 7;
  grid-row: 2 / 5;
  z-index: 1;
  background: white;
  padding: 2rem;
}
```

```tsx
// React component
function OverlapCard({ image, content }) {
  return (
    <div className="grid grid-cols-6 grid-rows-4">
      <div className="col-start-1 col-end-5 row-start-1 row-end-4">
        <img src={image} alt="" className="w-full h-full object-cover" />
      </div>
      <div className="col-start-3 col-end-7 row-start-2 row-end-5 z-10 bg-white p-8">
        {content}
      </div>
    </div>
  );
}
```

## Subgrid

```css
/* Parent grid */
.parent {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* Child inherits parent's grid */
.child {
  display: grid;
  grid-column: span 3;
  grid-template-columns: subgrid;  /* Inherits parent columns */
}

/* Useful for consistent alignment */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;  /* Header, content, footer */
}

.card-header { /* Aligns across all cards */ }
.card-content { /* Aligns across all cards */ }
.card-footer { /* Aligns across all cards */ }
```

## CSS Grid in React/Tailwind

### Tailwind Utilities

```tsx
// Basic grid
<div className="grid grid-cols-3 gap-4">

// Responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// Auto-fit
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]">

// Named areas (inline style needed)
<div
  className="grid"
  style={{
    gridTemplateAreas: `"header header" "sidebar main" "footer footer"`,
    gridTemplateColumns: '200px 1fr',
  }}
>
```

### Grid Component

```tsx
interface GridProps {
  children: React.ReactNode;
  columns?: number | 'auto-fit' | 'auto-fill';
  minColumnWidth?: string;
  gap?: string;
  className?: string;
}

function Grid({
  children,
  columns = 'auto-fit',
  minColumnWidth = '250px',
  gap = '1rem',
  className,
}: GridProps) {
  const gridColumns = typeof columns === 'number'
    ? `repeat(${columns}, 1fr)`
    : `repeat(${columns}, minmax(min(${minColumnWidth}, 100%), 1fr))`;

  return (
    <div
      className={className}
      style={{
        display: 'grid',
        gridTemplateColumns: gridColumns,
        gap,
      }}
    >
      {children}
    </div>
  );
}

// Usage
<Grid columns={3} gap="1.5rem">
  {items.map(item => <Card key={item.id} {...item} />)}
</Grid>

<Grid columns="auto-fit" minColumnWidth="300px">
  {items.map(item => <Card key={item.id} {...item} />)}
</Grid>
```

## Debugging Grid

```css
/* Visual grid lines (dev only) */
.grid {
  outline: 2px dashed red;
}

.grid > * {
  outline: 1px solid blue;
}

/* Firefox Grid Inspector is best */
/* Chrome DevTools > Elements > Layout panel */
```

## Best Practices

1. **Use `fr` units** for fluid proportions
2. **Prefer `minmax()`** over fixed widths
3. **Use `auto-fit`** for responsive grids
4. **Name areas** for complex layouts
5. **Combine with Flexbox** - Grid for layout, Flexbox for components
6. **Test responsiveness** - Use browser DevTools
7. **Avoid negative margins** - Grid handles gaps
8. **Use `min()` function** - Prevents overflow: `minmax(min(250px, 100%), 1fr)`

## Quick Reference

```css
/* Essential properties */
display: grid;
grid-template-columns: repeat(3, 1fr);
grid-template-rows: auto 1fr auto;
grid-template-areas: "header" "main" "footer";
gap: 1rem;

/* Item placement */
grid-column: 1 / 3;
grid-row: 1 / span 2;
grid-area: header;

/* Alignment */
justify-items: center;  /* Horizontal in cell */
align-items: center;    /* Vertical in cell */
justify-content: center; /* Grid in container */
align-content: center;   /* Grid in container */

/* Auto behavior */
grid-auto-rows: minmax(100px, auto);
grid-auto-flow: row | column | dense;

/* Responsive pattern */
grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
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

