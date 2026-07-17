---
last_updated: 2026-02-25
status: active
name: flexbox-patterns
description: CSS Flexbox for one-dimensional layouts - alignment, distribution, ordering. Use when building component layouts, navigation, or centering content.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/*.jsx", "**/styles/**", "**/components/**"]
  keywords: ["flexbox", "flex", "justify-content", "align-items", "flex-direction", "flex-wrap", "gap", "center", "space-between"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Flexbox Patterns

Master CSS Flexbox for one-dimensional layouts and component design.

## When to Use Flexbox vs Grid

| Use Flexbox For | Use Grid For |
|-----------------|--------------|
| One-dimensional layouts | Two-dimensional layouts |
| Component internals | Page structure |
| Navigation, toolbars | Complex card grids |
| Centering content | Overlapping elements |
| Unknown number of items | Fixed grid layouts |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Flexbox Fundamentals

### Container Properties

```css
.flex-container {
  display: flex;
  flex-direction: row;           /* row | row-reverse | column | column-reverse */
  flex-wrap: wrap;               /* nowrap | wrap | wrap-reverse */
  justify-content: flex-start;   /* Main axis alignment */
  align-items: stretch;          /* Cross axis alignment */
  align-content: flex-start;     /* Multi-line cross axis */
  gap: 1rem;                     /* Spacing between items */
}
```

### Item Properties

```css
.flex-item {
  flex-grow: 0;      /* Grow factor (default 0) */
  flex-shrink: 1;    /* Shrink factor (default 1) */
  flex-basis: auto;  /* Initial size */
  flex: 1;           /* Shorthand: grow shrink basis */
  align-self: auto;  /* Override container align-items */
  order: 0;          /* Visual order */
}
```

## Alignment

### Main Axis (justify-content)

```css
.container {
  justify-content: flex-start;    /* Items at start */
  justify-content: flex-end;      /* Items at end */
  justify-content: center;        /* Items centered */
  justify-content: space-between; /* First/last at edges */
  justify-content: space-around;  /* Equal space around items */
  justify-content: space-evenly;  /* Equal space everywhere */
}
```

### Cross Axis (align-items)

```css
.container {
  align-items: stretch;    /* Fill container height */
  align-items: flex-start; /* Top aligned */
  align-items: flex-end;   /* Bottom aligned */
  align-items: center;     /* Vertically centered */
  align-items: baseline;   /* Text baseline aligned */
}
```

### Individual Item (align-self)

```css
.item { align-self: flex-start | flex-end | center | stretch; }
```

## Common Patterns

### Perfect Centering

```css
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Shorthand */
.center { display: flex; place-items: center; }
```

```tsx
<div className="flex items-center justify-center h-screen">
  <div>Centered content</div>
</div>
```

### Navigation Bar

```tsx
function Navbar() {
  return (
    <nav className="flex items-center justify-between px-4 py-2">
      <a href="/" className="font-bold">Logo</a>
      <ul className="flex gap-4">
        <li><a href="/about">About</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
      <button>Sign In</button>
    </nav>
  );
}
```

```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 1rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
  list-style: none;
}
```

### Sticky Footer

```tsx
function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen">
      <header>Header</header>
      <main className="flex-1">{children}</main>
      <footer>Footer</footer>
    </div>
  );
}
```

```css
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main { flex: 1; } /* Grows to fill space */
```

### Card Layout

```tsx
function Card({ image, title, description, actions }) {
  return (
    <article className="flex flex-col h-full">
      <img src={image} alt="" className="w-full" />
      <div className="flex flex-col flex-1 p-4">
        <h3 className="font-bold">{title}</h3>
        <p className="flex-1">{description}</p>
        <div className="flex gap-2 mt-4">{actions}</div>
      </div>
    </article>
  );
}
```

```css
.card {
  display: flex;
  flex-direction: column;
}

.card-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-description { flex: 1; } /* Push actions to bottom */
.card-actions { margin-top: auto; }
```

### Media Object

```tsx
function MediaObject({ image, title, content }) {
  return (
    <div className="flex gap-4">
      <img src={image} alt="" className="w-16 h-16 rounded-full" />
      <div className="flex-1 min-w-0">
        <h4 className="font-bold truncate">{title}</h4>
        <p>{content}</p>
      </div>
    </div>
  );
}
```

```css
.media {
  display: flex;
  gap: 1rem;
}

.media-body {
  flex: 1;
  min-width: 0; /* Enable text truncation */
}
```

### Input Group

```tsx
function InputGroup({ prefix, suffix }) {
  return (
    <div className="flex">
      {prefix && <span className="px-3 py-2 bg-gray-100 border">{prefix}</span>}
      <input className="flex-1 px-3 py-2 border" />
      {suffix && <span className="px-3 py-2 bg-gray-100 border">{suffix}</span>}
    </div>
  );
}
```

```css
.input-group { display: flex; }
.input-group input { flex: 1; }
```

### Button Group

```tsx
function ButtonGroup({ children }) {
  return (
    <div className="inline-flex" role="group">
      {children}
    </div>
  );
}

// Usage
<ButtonGroup>
  <button className="rounded-l">Left</button>
  <button>Middle</button>
  <button className="rounded-r">Right</button>
</ButtonGroup>
```

### Equal Height Columns

```css
.columns {
  display: flex;
  gap: 1rem;
}

.column {
  flex: 1;           /* Equal width */
  /* Height automatically matches tallest */
}
```

### Responsive Flex

```tsx
<div className="flex flex-col md:flex-row gap-4">
  <aside className="md:w-64">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>
```

```css
.layout {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .layout { flex-direction: row; }
  .sidebar { width: 16rem; }
  .main { flex: 1; }
}
```

## Flex Shorthand Values

| Value | Meaning | Use Case |
|-------|---------|----------|
| `flex: 1` | `1 1 0%` | Equal distribution |
| `flex: auto` | `1 1 auto` | Size-aware distribution |
| `flex: none` | `0 0 auto` | Fixed size |
| `flex: initial` | `0 1 auto` | Default behavior |

```css
/* Equal width items */
.item { flex: 1; }

/* Item takes its content size, can shrink */
.item { flex: initial; } /* or flex: 0 1 auto */

/* Fixed size, no grow/shrink */
.item { flex: none; }
```

## Handling Overflow

```css
/* Prevent flex item from overflowing */
.flex-item {
  min-width: 0;    /* Allow shrinking below content size */
}

/* Text truncation in flex item */
.truncate {
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

```tsx
<div className="flex gap-4">
  <span className="flex-1 min-w-0 truncate">{longText}</span>
  <button className="flex-shrink-0">Action</button>
</div>
```

## Order and Visual Reordering

```css
/* Visual order (doesn't affect tab order or screen readers) */
.first { order: -1; }
.last { order: 1; }

/* Reverse all items */
.container { flex-direction: row-reverse; }
```

## Spacing Patterns

### Gap (Modern)

```css
.container {
  display: flex;
  gap: 1rem;         /* All gaps */
  column-gap: 1rem;  /* Horizontal */
  row-gap: 0.5rem;   /* Vertical (wrapping) */
}
```

### Auto Margins (Push to Edge)

```css
/* Push item to far right */
.item:last-child { margin-left: auto; }

/* Push item to far left */
.item:first-child { margin-right: auto; }

/* Center one item */
.item { margin: auto; }
```

```tsx
<nav className="flex items-center">
  <a href="/">Logo</a>
  <div className="flex gap-4">Links...</div>
  <button className="ml-auto">Sign In</button>
</nav>
```

## Wrapping

```css
.container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

/* Responsive card grid */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  flex: 1 1 300px; /* Grow, shrink, min 300px */
  max-width: 400px;
}
```

## React Component Patterns

```tsx
interface FlexProps {
  direction?: 'row' | 'column';
  justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
  align?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
  wrap?: boolean;
  gap?: string;
  children: React.ReactNode;
  className?: string;
}

function Flex({
  direction = 'row',
  justify = 'start',
  align = 'stretch',
  wrap = false,
  gap = '0',
  children,
  className,
}: FlexProps) {
  const justifyMap = { start: 'flex-start', end: 'flex-end', center: 'center', between: 'space-between', around: 'space-around', evenly: 'space-evenly' };
  const alignMap = { start: 'flex-start', end: 'flex-end', center: 'center', stretch: 'stretch', baseline: 'baseline' };

  return (
    <div
      className={className}
      style={{
        display: 'flex',
        flexDirection: direction,
        justifyContent: justifyMap[justify],
        alignItems: alignMap[align],
        flexWrap: wrap ? 'wrap' : 'nowrap',
        gap,
      }}
    >
      {children}
    </div>
  );
}

// Usage
<Flex justify="between" align="center" gap="1rem">
  <Logo />
  <NavLinks />
  <SignInButton />
</Flex>
```

## Best Practices

1. **Use `gap`** instead of margins between items
2. **Set `min-width: 0`** on items that might overflow
3. **Use `flex-shrink: 0`** for fixed-width items
4. **Avoid `order`** for content that must be accessible
5. **Prefer `flex: 1`** for equal distribution
6. **Combine with Grid** - Flexbox for 1D, Grid for 2D
7. **Use `margin-left: auto`** to push items to the edge

## Quick Reference

```css
/* Container */
display: flex;
flex-direction: row | column;
flex-wrap: wrap;
justify-content: center | space-between;
align-items: center | stretch;
gap: 1rem;

/* Items */
flex: 1;              /* Grow equally */
flex: none;           /* Fixed size */
flex-shrink: 0;       /* Don't shrink */
min-width: 0;         /* Allow shrink below content */
margin-left: auto;    /* Push to right */
align-self: center;   /* Override alignment */

/* Common Patterns */
.center { display: flex; place-items: center; }
.between { display: flex; justify-content: space-between; align-items: center; }
.stack { display: flex; flex-direction: column; gap: 1rem; }
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

