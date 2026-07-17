---
last_updated: 2026-02-25
status: active
name: css-architecture
description: CSS architecture methodologies - BEM, utility-first, component patterns, file organization. Use when structuring large-scale CSS codebases.
triggers:
  files: ["**/*.css", "**/*.scss", "**/styles/**", "**/tailwind.config.*"]
  keywords: ["BEM", "CSS architecture", "utility classes", "component CSS", "CSS modules", "methodology", "naming convention", "organization"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# CSS Architecture

Build maintainable, scalable CSS systems for large applications.

## Architecture Goals

| Goal | Description |
|------|-------------|
| **Predictable** | CSS behaves as expected |
| **Reusable** | Components work anywhere |
| **Maintainable** | Easy to update without side effects |
| **Scalable** | Grows without complexity explosion |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Methodologies

### BEM (Block Element Modifier)

```css
/* Block: Standalone component */
.card { }

/* Element: Part of block (double underscore) */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier: Variation (double hyphen) */
.card--featured { }
.card--compact { }
.card__header--highlighted { }
```

```tsx
function Card({ featured, compact, children }) {
  const classes = [
    'card',
    featured && 'card--featured',
    compact && 'card--compact',
  ].filter(Boolean).join(' ');

  return (
    <article className={classes}>
      <header className="card__header">{title}</header>
      <div className="card__body">{children}</div>
    </article>
  );
}
```

### Utility-First (Tailwind)

```tsx
// Compose utilities for components
function Card({ children }) {
  return (
    <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <header className="font-bold text-xl mb-4">{title}</header>
      <div className="text-gray-600">{children}</div>
    </article>
  );
}

// Extract repeated patterns
// tailwind.config.js
module.exports = {
  theme: {
    extend: {},
  },
  plugins: [
    function({ addComponents }) {
      addComponents({
        '.card': {
          '@apply bg-white rounded-lg shadow-md p-6': {},
        },
      });
    },
  ],
};
```

### CSS Modules

```css
/* Card.module.css */
.card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.header {
  font-weight: bold;
  margin-bottom: 1rem;
}

.featured {
  composes: card;
  border: 2px solid var(--color-primary);
}
```

```tsx
import styles from './Card.module.css';

function Card({ featured, children }) {
  return (
    <article className={featured ? styles.featured : styles.card}>
      <header className={styles.header}>{title}</header>
      {children}
    </article>
  );
}
```

### Atomic CSS

```css
/* Single-purpose classes */
.d-flex { display: flex; }
.d-grid { display: grid; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.m-auto { margin: auto; }
.text-center { text-align: center; }
.fw-bold { font-weight: bold; }
```

## Naming Conventions

### Component Namespacing

```css
/* Prefix by type */
.c-card { }      /* Component */
.l-grid { }      /* Layout */
.u-hidden { }    /* Utility */
.is-active { }   /* State */
.has-icon { }    /* Feature */
.js-toggle { }   /* JavaScript hook (no styles) */
```

### ITCSS (Inverted Triangle)

```
1. Settings    - Variables, config
2. Tools       - Mixins, functions
3. Generic     - Reset, normalize
4. Elements    - Base HTML elements
5. Objects     - Layout patterns
6. Components  - UI components
7. Utilities   - Helpers, overrides
```

```scss
// main.scss
@import 'settings/variables';
@import 'settings/breakpoints';

@import 'tools/mixins';

@import 'generic/reset';
@import 'generic/box-sizing';

@import 'elements/headings';
@import 'elements/links';

@import 'objects/container';
@import 'objects/grid';

@import 'components/button';
@import 'components/card';

@import 'utilities/spacing';
@import 'utilities/display';
```

## File Organization

### Component-Based Structure

```
styles/
├── base/
│   ├── _reset.css
│   ├── _typography.css
│   └── _variables.css
├── components/
│   ├── _button.css
│   ├── _card.css
│   ├── _form.css
│   └── _modal.css
├── layouts/
│   ├── _container.css
│   ├── _grid.css
│   └── _sidebar.css
├── utilities/
│   ├── _spacing.css
│   ├── _display.css
│   └── _text.css
└── main.css
```

### Co-located Styles

```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.module.css
│   └── Button.test.tsx
├── Card/
│   ├── Card.tsx
│   ├── Card.module.css
│   └── index.ts
```

## Specificity Management

### Specificity Layers

```css
/* Low specificity base */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
}

/* Modifier increases specificity minimally */
.btn--primary {
  background: var(--color-primary);
  color: white;
}

/* State classes */
.btn.is-loading {
  opacity: 0.7;
  pointer-events: none;
}

/* Never use !important except utilities */
.u-hidden { display: none !important; }
```

### CSS Cascade Layers

```css
/* Define layer order */
@layer reset, base, components, utilities;

/* Assign styles to layers */
@layer reset {
  * { box-sizing: border-box; }
}

@layer base {
  body { font-family: system-ui; }
}

@layer components {
  .card { background: white; }
}

@layer utilities {
  .hidden { display: none; }
}

/* Later layers override earlier */
/* utilities > components > base > reset */
```

## Design Token Integration

### Token System

```css
/* tokens.css */
:root {
  /* Primitive tokens */
  --color-blue-500: #0066cc;
  --color-gray-100: #f5f5f5;

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;

  /* Semantic tokens */
  --color-primary: var(--color-blue-500);
  --color-bg-page: var(--color-gray-100);

  --space-component-padding: var(--space-4);
  --space-component-gap: var(--space-2);
}

/* components.css */
.card {
  padding: var(--space-component-padding);
  gap: var(--space-component-gap);
  background: var(--color-bg-page);
}
```

### Component API

```css
/* Expose customization points */
.card {
  --card-padding: var(--space-4);
  --card-radius: var(--radius-md);
  --card-bg: white;

  padding: var(--card-padding);
  border-radius: var(--card-radius);
  background: var(--card-bg);
}

/* Override via inline styles or custom classes */
.card--compact {
  --card-padding: var(--space-2);
}
```

## State Management

### State Classes

```css
/* Boolean states */
.is-active { }
.is-disabled { }
.is-loading { }
.is-hidden { }
.is-expanded { }

/* Feature states */
.has-icon { }
.has-error { }
.has-children { }

/* Usage */
.nav-item {
  color: var(--color-text);
}

.nav-item.is-active {
  color: var(--color-primary);
  font-weight: bold;
}

.form-field.has-error .form-input {
  border-color: var(--color-error);
}
```

### Data Attributes

```css
/* State via data attributes */
.button[data-loading="true"] {
  opacity: 0.7;
}

.tabs[data-orientation="vertical"] {
  flex-direction: column;
}

.alert[data-type="error"] {
  background: var(--color-error-bg);
}
```

```tsx
<button data-loading={isLoading}>Submit</button>
<div className="tabs" data-orientation="vertical">
```

## Responsive Patterns

### Mobile-First

```css
/* Base (mobile) */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Container Queries

```css
/* Component adapts to container, not viewport */
.card {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card__content {
    display: flex;
    gap: 1rem;
  }
}
```

## Reusable Patterns

### Object Classes

```css
/* Layout objects (no cosmetics) */
.o-container {
  max-width: var(--container-max);
  margin-inline: auto;
  padding-inline: var(--gutter);
}

.o-stack > * + * {
  margin-top: var(--stack-space, 1rem);
}

.o-cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-space, 1rem);
}

.o-sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sidebar-gap, 1rem);
}

.o-sidebar > :first-child {
  flex-basis: var(--sidebar-width, 20rem);
  flex-grow: 1;
}

.o-sidebar > :last-child {
  flex-basis: 0;
  flex-grow: 999;
  min-width: var(--sidebar-content-min, 50%);
}
```

### Composition

```tsx
// Combine utilities and components
<div className="o-container">
  <div className="o-stack">
    <header className="c-page-header">
      <h1 className="u-text-4xl">Title</h1>
    </header>
    <main className="o-sidebar">
      <aside className="c-sidebar">Nav</aside>
      <article className="c-content">Content</article>
    </main>
  </div>
</div>
```

## Best Practices

| Practice | Rationale |
|----------|-----------|
| Single responsibility | One class, one job |
| Low specificity | Easier to override |
| Immutable utilities | Utilities never change |
| Component encapsulation | Styles don't leak |
| Semantic naming | Names describe purpose |
| Token-based values | Consistent design |

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| `!important` everywhere | Fix specificity issues |
| Deep nesting `.a .b .c .d` | Flat, specific classes |
| ID selectors `#header` | Class selectors |
| Styling by element `.card div` | Named classes |
| Magic numbers `margin: 17px` | Design tokens |
| Inline styles for reusable patterns | CSS classes |

## Quick Reference

```css
/* BEM */
.block { }
.block__element { }
.block--modifier { }

/* State */
.is-active { }
.has-icon { }

/* Layers */
@layer base, components, utilities;

/* Component API */
.component {
  --component-prop: default;
  property: var(--component-prop);
}

/* File structure */
base/ → tokens, reset
components/ → UI components
layouts/ → page structure
utilities/ → helpers
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

