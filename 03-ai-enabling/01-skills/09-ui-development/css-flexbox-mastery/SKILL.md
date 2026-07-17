---
last_updated: 2026-02-25
status: active
name: css-flexbox-mastery
description: CSS Flexbox for one-dimensional layouts - alignment, distribution, responsive patterns. Use when building component layouts.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/*.jsx", "**/styles/**"]
  keywords: ["flexbox", "flex", "justify-content", "align-items", "flex-grow", "flex-shrink", "flex-basis", "gap"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# CSS Flexbox Mastery

Master Flexbox for flexible one-dimensional layouts.

## When to Use Flexbox vs Grid

| Use Flexbox For | Use Grid For |
|-----------------|--------------|
| One-dimensional layouts | Two-dimensional layouts |
| Component internals | Page structure |
| Navigation bars | Card grids |
| Centering content | Complex alignment |
| Unknown number of items | Fixed/known structure |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Flexbox Fundamentals

### Container Setup

```css
.container {
  display: flex;
  flex-direction: row;        /* Main axis direction */
  flex-wrap: wrap;            /* Allow wrapping */
  gap: 1rem;                  /* Space between items */
}

/* Shorthand */
.container {
  display: flex;
  flex-flow: row wrap;        /* direction + wrap */
}
```

### Axes

| Property | Row (default) | Column |
|----------|---------------|--------|
| Main axis | Horizontal → | Vertical ↓ |
| Cross axis | Vertical ↓ | Horizontal → |
| `justify-content` | Horizontal | Vertical |
| `align-items` | Vertical | Horizontal |

## Flex Direction

```css
.row         { flex-direction: row; }          /* → Left to right */
.row-reverse { flex-direction: row-reverse; }  /* ← Right to left */
.column      { flex-direction: column; }       /* ↓ Top to bottom */
.column-reverse { flex-direction: column-reverse; } /* ↑ Bottom to top */
```

```tsx
// Tailwind
<div className="flex flex-row">     // Default
<div className="flex flex-col">     // Column
<div className="flex flex-row-reverse">
<div className="flex flex-col-reverse">
```

## Justify Content (Main Axis)

```css
.container {
  display: flex;
  justify-content: flex-start;    /* Pack at start */
  justify-content: flex-end;      /* Pack at end */
  justify-content: center;        /* Pack at center */
  justify-content: space-between; /* First/last at edges, equal space between */
  justify-content: space-around;  /* Equal space around each item */
  justify-content: space-evenly;  /* Equal space everywhere */
}
```

Visual representation (row direction):
```
flex-start:      [A][B][C]          |
flex-end:                 |[A][B][C]
center:              |[A][B][C]|
space-between:   [A]    [B]    [C]
space-around:     [A]  [B]  [C]
space-evenly:    [A]   [B]   [C]
```

```tsx
// Tailwind
<div className="flex justify-start">
<div className="flex justify-end">
<div className="flex justify-center">
<div className="flex justify-between">
<div className="flex justify-around">
<div className="flex justify-evenly">
```

## Align Items (Cross Axis)

```css
.container {
  display: flex;
  align-items: stretch;    /* Fill container height (default) */
  align-items: flex-start; /* Align to top */
  align-items: flex-end;   /* Align to bottom */
  align-items: center;     /* Center vertically */
  align-items: baseline;   /* Align text baselines */
}
```

Visual representation (row direction):
```
stretch:     |[A====]|[B====]|[C====]|
flex-start:  |[A]    |[B]    |[C]    |
flex-end:    |    [A]|    [B]|    [C]|
center:      |  [A]  |  [B]  |  [C]  |
baseline:    |[A]____|[B]____|[C]____|
```

```tsx
// Tailwind
<div className="flex items-stretch">
<div className="flex items-start">
<div className="flex items-end">
<div className="flex items-center">
<div className="flex items-baseline">
```

## Align Content (Multi-line)

For wrapped flex containers with multiple rows:

```css
.container {
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;    /* Pack rows at start */
  align-content: flex-end;      /* Pack rows at end */
  align-content: center;        /* Pack rows at center */
  align-content: space-between; /* First/last rows at edges */
  align-content: space-around;  /* Equal space around rows */
  align-content: stretch;       /* Rows stretch to fill */
}
```

```tsx
// Tailwind
<div className="flex flex-wrap content-start">
<div className="flex flex-wrap content-center">
<div className="flex flex-wrap content-between">
```

## Gap

```css
.container {
  display: flex;
  gap: 1rem;                    /* All gaps */
  row-gap: 1rem;                /* Vertical gaps */
  column-gap: 2rem;             /* Horizontal gaps */
  gap: 1rem 2rem;               /* row-gap column-gap */
}
```

```tsx
// Tailwind
<div className="flex gap-4">
<div className="flex gap-x-4 gap-y-2">
```

## Flex Item Properties

### Flex Grow

```css
/* How much item should grow relative to siblings */
.item { flex-grow: 0; }  /* Don't grow (default) */
.item { flex-grow: 1; }  /* Grow to fill available space */
.item { flex-grow: 2; }  /* Grow twice as much as flex-grow: 1 */
```

Example:
```
Container: [===========================================]
           |  A (grow: 1)  |      B (grow: 2)        |
           |     1/3       |         2/3              |
```

```tsx
// Tailwind
<div className="flex">
  <div className="flex-grow">Grows</div>
  <div>Fixed</div>
</div>

// Or
<div className="flex">
  <div className="grow">Grows</div>
  <div className="grow-0">Doesn't grow</div>
</div>
```

### Flex Shrink

```css
/* How much item should shrink when space is limited */
.item { flex-shrink: 1; }  /* Can shrink (default) */
.item { flex-shrink: 0; }  /* Don't shrink */
.item { flex-shrink: 2; }  /* Shrink twice as much */
```

```tsx
// Tailwind
<div className="flex">
  <div className="shrink">Can shrink</div>
  <div className="shrink-0">Won't shrink</div>
</div>
```

### Flex Basis

```css
/* Initial size before grow/shrink */
.item { flex-basis: auto; }    /* Use content size (default) */
.item { flex-basis: 0; }       /* Start at 0, grow from there */
.item { flex-basis: 200px; }   /* Fixed starting size */
.item { flex-basis: 25%; }     /* Percentage of container */
```

```tsx
// Tailwind
<div className="basis-auto">
<div className="basis-0">
<div className="basis-1/4">
<div className="basis-48">  // 12rem = 192px
```

### Flex Shorthand

```css
/* flex: grow shrink basis */
.item { flex: 0 1 auto; }      /* Default */
.item { flex: 1; }             /* flex: 1 1 0 - grow and shrink equally */
.item { flex: auto; }          /* flex: 1 1 auto - grow/shrink based on content */
.item { flex: none; }          /* flex: 0 0 auto - don't grow or shrink */
.item { flex: 0 0 200px; }     /* Fixed width, no grow/shrink */
```

Common patterns:
```css
.fill-space { flex: 1; }           /* Fill available space */
.fixed-size { flex: none; }         /* Keep natural size */
.at-least { flex: 1 0 200px; }     /* Min 200px, can grow */
.at-most { flex: 0 1 200px; }      /* Max 200px, can shrink */
```

```tsx
// Tailwind
<div className="flex-1">      // flex: 1 1 0%
<div className="flex-auto">   // flex: 1 1 auto
<div className="flex-initial"> // flex: 0 1 auto
<div className="flex-none">   // flex: none
```

### Align Self

```css
/* Override align-items for single item */
.item {
  align-self: auto;        /* Use container's align-items */
  align-self: flex-start;
  align-self: flex-end;
  align-self: center;
  align-self: stretch;
  align-self: baseline;
}
```

```tsx
// Tailwind
<div className="flex items-start">
  <div>Starts at top</div>
  <div className="self-end">This one at bottom</div>
  <div className="self-center">This one centered</div>
</div>
```

### Order

```css
/* Change visual order without changing DOM order */
.item { order: 0; }    /* Default */
.item { order: -1; }   /* Move earlier */
.item { order: 1; }    /* Move later */
```

```tsx
// Tailwind
<div className="flex">
  <div className="order-3">Third</div>
  <div className="order-1">First</div>
  <div className="order-2">Second</div>
</div>
```

## Common Patterns

### Centering

```css
/* Perfect centering */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Or shorthand with place-items (if only one child) */
.center {
  display: flex;
  place-items: center;
}
```

```tsx
// Tailwind
<div className="flex justify-center items-center h-screen">
  <div>Centered content</div>
</div>
```

### Navigation Bar

```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
}
```

```tsx
function Navbar() {
  return (
    <nav className="flex justify-between items-center p-4">
      <div className="logo">Logo</div>
      <ul className="flex gap-4">
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
      <button>Sign In</button>
    </nav>
  );
}
```

### Card Header

```css
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
```

```tsx
function CardHeader({ avatar, title, subtitle, actions }) {
  return (
    <div className="flex justify-between items-center">
      <div className="flex items-center gap-2">
        {avatar}
        <div>
          <h3>{title}</h3>
          <p className="text-sm text-gray-500">{subtitle}</p>
        </div>
      </div>
      <div className="flex gap-2">
        {actions}
      </div>
    </div>
  );
}
```

### Sticky Footer

```css
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main {
  flex: 1;  /* Fill available space */
}

.footer {
  flex-shrink: 0;  /* Don't shrink */
}
```

```tsx
function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen">
      <header>Header</header>
      <main className="flex-1">{children}</main>
      <footer className="shrink-0">Footer</footer>
    </div>
  );
}
```

### Input Group

```css
.input-group {
  display: flex;
}

.input-group input {
  flex: 1;
}

.input-group button {
  flex-shrink: 0;
}
```

```tsx
function SearchInput() {
  return (
    <div className="flex">
      <input className="flex-1" type="text" placeholder="Search..." />
      <button className="shrink-0 px-4">Search</button>
    </div>
  );
}
```

### Media Object

```css
.media {
  display: flex;
  gap: 1rem;
}

.media-image {
  flex-shrink: 0;
}

.media-body {
  flex: 1;
  min-width: 0;  /* Allow text truncation */
}
```

```tsx
function MediaObject({ image, title, description }) {
  return (
    <div className="flex gap-4">
      <img src={image} className="w-16 h-16 shrink-0" />
      <div className="flex-1 min-w-0">
        <h3 className="truncate">{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}
```

### Split Button Group

```css
.split-buttons {
  display: flex;
}

.split-buttons button:first-child {
  flex: 1;
}

.split-buttons button:last-child {
  flex-shrink: 0;
}
```

```tsx
function SplitButton({ label, options }) {
  return (
    <div className="flex">
      <button className="flex-1">{label}</button>
      <button className="shrink-0">▼</button>
    </div>
  );
}
```

### Responsive Stack

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .stack {
    flex-direction: row;
  }
}
```

```tsx
// Tailwind
<div className="flex flex-col md:flex-row gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Equal Height Columns

```css
.columns {
  display: flex;
}

.column {
  flex: 1;
}
```

```tsx
function EqualColumns({ children }) {
  return (
    <div className="flex">
      {React.Children.map(children, child => (
        <div className="flex-1">{child}</div>
      ))}
    </div>
  );
}
```

### Wrapping Tags

```css
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  flex-shrink: 0;
}
```

```tsx
function Tags({ items }) {
  return (
    <div className="flex flex-wrap gap-2">
      {items.map(item => (
        <span key={item} className="px-2 py-1 bg-gray-200 rounded shrink-0">
          {item}
        </span>
      ))}
    </div>
  );
}
```

## Responsive Patterns

### Wrap on Small Screens

```css
.responsive-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.responsive-row > * {
  flex: 1 1 300px;  /* Grow, shrink, minimum 300px */
}
```

```tsx
// Items wrap when they can't fit at 300px
<div className="flex flex-wrap gap-4">
  {items.map(item => (
    <div key={item.id} className="flex-1 basis-[300px]">
      <Card {...item} />
    </div>
  ))}
</div>
```

### Mobile-First Stack to Row

```tsx
// Stack on mobile, row on desktop
<div className="flex flex-col sm:flex-row gap-4">
  <div className="flex-1">Main content</div>
  <div className="w-full sm:w-64 shrink-0">Sidebar</div>
</div>
```

### Reverse on Mobile

```tsx
// Show sidebar first on mobile, after on desktop
<div className="flex flex-col-reverse md:flex-row gap-4">
  <main className="flex-1">Main content</main>
  <aside className="w-full md:w-64 shrink-0">Sidebar</aside>
</div>
```

## Flexbox in React Components

### Flex Component

```tsx
interface FlexProps extends React.HTMLAttributes<HTMLDivElement> {
  direction?: 'row' | 'column' | 'row-reverse' | 'column-reverse';
  justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
  align?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
  wrap?: boolean;
  gap?: string | number;
  children: React.ReactNode;
}

function Flex({
  direction = 'row',
  justify = 'start',
  align = 'stretch',
  wrap = false,
  gap,
  children,
  style,
  ...props
}: FlexProps) {
  const justifyMap = {
    start: 'flex-start',
    end: 'flex-end',
    center: 'center',
    between: 'space-between',
    around: 'space-around',
    evenly: 'space-evenly',
  };

  const alignMap = {
    start: 'flex-start',
    end: 'flex-end',
    center: 'center',
    stretch: 'stretch',
    baseline: 'baseline',
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: direction,
        justifyContent: justifyMap[justify],
        alignItems: alignMap[align],
        flexWrap: wrap ? 'wrap' : 'nowrap',
        gap: typeof gap === 'number' ? `${gap}px` : gap,
        ...style,
      }}
      {...props}
    >
      {children}
    </div>
  );
}

// Usage
<Flex justify="between" align="center" gap={16}>
  <Logo />
  <Nav />
  <Button>Sign In</Button>
</Flex>
```

### Stack Component

```tsx
interface StackProps {
  direction?: 'horizontal' | 'vertical';
  gap?: string | number;
  align?: 'start' | 'end' | 'center' | 'stretch';
  children: React.ReactNode;
}

function Stack({
  direction = 'vertical',
  gap = '1rem',
  align = 'stretch',
  children,
}: StackProps) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: direction === 'vertical' ? 'column' : 'row',
        gap: typeof gap === 'number' ? `${gap}px` : gap,
        alignItems: align,
      }}
    >
      {children}
    </div>
  );
}

// Usage
<Stack gap="1rem">
  <Input label="Name" />
  <Input label="Email" />
  <Button>Submit</Button>
</Stack>
```

## Common Gotchas

### Min-Width and Text Overflow

```css
/* Problem: Text doesn't truncate */
.flex-item {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  /* Doesn't work! */
}

/* Solution: Add min-width: 0 */
.flex-item {
  flex: 1;
  min-width: 0;  /* Override default min-width: auto */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### Image Sizing

```css
/* Problem: Images don't shrink */
.flex-container img {
  /* Image overflows container */
}

/* Solution */
.flex-container img {
  max-width: 100%;
  height: auto;
}

/* Or for flex item images */
.image-container {
  flex-shrink: 0;  /* Don't shrink */
  width: 100px;    /* Fixed size */
}
```

### Margin Auto Trick

```css
/* Push item to end */
.flex-container {
  display: flex;
}

.push-right {
  margin-left: auto;
}

/* Center one item, push others */
.center-item {
  margin-left: auto;
  margin-right: auto;
}
```

```tsx
// Tailwind: Push last item to end
<div className="flex">
  <div>Left</div>
  <div>Middle</div>
  <div className="ml-auto">Right (pushed)</div>
</div>
```

## Best Practices

1. **Use `gap` instead of margins** - cleaner, doesn't affect first/last items
2. **Remember `min-width: 0`** - for text truncation in flex items
3. **Use `flex-shrink: 0`** - for fixed-size items like icons
4. **Prefer `flex: 1`** - over `width: 100%` for filling space
5. **Use `flex-wrap`** - for responsive layouts
6. **Combine with Grid** - Flexbox for 1D, Grid for 2D
7. **Test responsiveness** - flex layouts can behave unexpectedly

## Quick Reference

```css
/* Container */
display: flex;
flex-direction: row | column | row-reverse | column-reverse;
flex-wrap: nowrap | wrap | wrap-reverse;
justify-content: flex-start | flex-end | center | space-between | space-around | space-evenly;
align-items: stretch | flex-start | flex-end | center | baseline;
align-content: stretch | flex-start | flex-end | center | space-between | space-around;
gap: 1rem;

/* Items */
flex: grow shrink basis;
flex-grow: 0 | 1 | 2...;
flex-shrink: 0 | 1 | 2...;
flex-basis: auto | 0 | 200px | 25%;
align-self: auto | flex-start | flex-end | center | stretch | baseline;
order: 0 | 1 | -1...;

/* Common shortcuts */
flex: 1;           /* Grow to fill */
flex: none;        /* Don't grow or shrink */
flex: 0 0 200px;   /* Fixed size */
min-width: 0;      /* Allow shrinking past content */
margin-left: auto; /* Push to right */
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

