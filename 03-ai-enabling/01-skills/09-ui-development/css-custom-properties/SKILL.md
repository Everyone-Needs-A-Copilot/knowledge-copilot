---
last_updated: 2026-02-25
status: active
name: css-custom-properties
description: CSS Custom Properties (CSS Variables) for theming, dynamic values, and maintainable styles. Use when building design systems or implementing themes.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/*.jsx", "**/styles/**", "**/theme/**"]
  keywords: ["CSS variables", "custom properties", "--", "var()", "theme", "tokens", "dark mode", ":root"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# CSS Custom Properties

Master CSS Custom Properties for dynamic, maintainable styles and theming.

## Why Custom Properties

| Feature | CSS Variables | Preprocessor Variables |
|---------|---------------|------------------------|
| Runtime changes | Yes | No |
| Cascade/inheritance | Yes | No |
| JavaScript access | Yes | No |
| Media query updates | Yes | No |
| Component scoping | Yes | Limited |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Fundamentals

### Defining and Using Variables

```css
/* Define at :root for global scope */
:root {
  --color-primary: #0066cc;
  --color-secondary: #6c757d;
  --spacing-md: 1rem;
  --font-family-base: system-ui, sans-serif;
}

/* Use with var() */
.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  font-family: var(--font-family-base);
}

/* Fallback values */
.element {
  color: var(--color-text, #333);              /* Single fallback */
  padding: var(--spacing-lg, var(--spacing-md, 1rem)); /* Nested fallback */
}
```

### Scope and Inheritance

```css
/* Global scope */
:root {
  --color-primary: blue;
}

/* Component scope - overrides for descendants */
.card {
  --color-primary: green;
}

/* State-based overrides */
.card:hover {
  --color-primary: darkgreen;
}

/* Scoped to component */
.button {
  --button-bg: var(--color-primary);
  --button-padding: 0.75rem 1.5rem;

  background: var(--button-bg);
  padding: var(--button-padding);
}

.button--large {
  --button-padding: 1rem 2rem;
}
```

## Design Token System

### Token Categories

```css
:root {
  /* Primitive tokens (raw values) */
  --color-blue-500: #0066cc;
  --color-blue-600: #0052a3;
  --color-gray-100: #f8f9fa;
  --color-gray-900: #212529;

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;

  /* Semantic tokens (purpose-driven) */
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-text-inverse: var(--color-gray-100);

  --color-bg-primary: var(--color-gray-100);
  --color-bg-secondary: white;

  --color-border: var(--color-gray-300);
  --color-focus-ring: var(--color-blue-500);

  /* Component tokens */
  --button-bg: var(--color-blue-500);
  --button-bg-hover: var(--color-blue-600);
  --button-text: white;
  --button-padding: var(--space-2) var(--space-4);
  --button-radius: var(--radius-md);
}
```

### Systematic Naming

```css
:root {
  /* Pattern: --{category}-{property}-{variant} */
  --color-primary: #0066cc;
  --color-primary-light: #3399ff;
  --color-primary-dark: #004080;

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}
```

## Theming

### Light/Dark Theme

```css
/* Default (light) theme */
:root {
  --color-bg: white;
  --color-text: #1a1a1a;
  --color-border: #e5e5e5;
  --color-primary: #0066cc;
}

/* Dark theme via class */
[data-theme="dark"] {
  --color-bg: #1a1a1a;
  --color-text: #f5f5f5;
  --color-border: #333;
  --color-primary: #66b3ff;
}

/* Dark theme via media query */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg: #1a1a1a;
    --color-text: #f5f5f5;
    --color-border: #333;
    --color-primary: #66b3ff;
  }
}

/* Usage - no changes needed */
body {
  background: var(--color-bg);
  color: var(--color-text);
}
```

### React Theme Toggle

```tsx
function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') || 'system';
    }
    return 'system';
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'system') {
      root.removeAttribute('data-theme');
    } else {
      root.setAttribute('data-theme', theme);
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <select value={theme} onChange={(e) => setTheme(e.target.value)}>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
      <option value="system">System</option>
    </select>
  );
}
```

### Brand Theming

```css
/* Default brand */
:root {
  --brand-primary: #0066cc;
  --brand-secondary: #6c757d;
  --brand-accent: #ff6b35;
}

/* Brand overrides */
[data-brand="enterprise"] {
  --brand-primary: #1a365d;
  --brand-secondary: #4a5568;
  --brand-accent: #ed8936;
}

[data-brand="startup"] {
  --brand-primary: #6b46c1;
  --brand-secondary: #805ad5;
  --brand-accent: #f56565;
}
```

## Dynamic Values

### Calculated Values

```css
:root {
  --base-size: 1rem;
  --scale-ratio: 1.25;
}

.heading-1 { font-size: calc(var(--base-size) * var(--scale-ratio) * var(--scale-ratio) * var(--scale-ratio)); }
.heading-2 { font-size: calc(var(--base-size) * var(--scale-ratio) * var(--scale-ratio)); }
.heading-3 { font-size: calc(var(--base-size) * var(--scale-ratio)); }
.body { font-size: var(--base-size); }
```

### Responsive Spacing

```css
:root {
  --space-unit: 0.25rem;
}

@media (min-width: 768px) {
  :root { --space-unit: 0.3rem; }
}

@media (min-width: 1024px) {
  :root { --space-unit: 0.35rem; }
}

/* Components use multipliers */
.card {
  padding: calc(var(--space-unit) * 4);
  gap: calc(var(--space-unit) * 2);
}
```

### JavaScript Integration

```tsx
// Read CSS variable
const primaryColor = getComputedStyle(document.documentElement)
  .getPropertyValue('--color-primary').trim();

// Set CSS variable
document.documentElement.style.setProperty('--color-primary', '#ff0000');

// React hook
function useCSSVariable(name: string) {
  const [value, setValue] = useState(() =>
    getComputedStyle(document.documentElement).getPropertyValue(name).trim()
  );

  const setVariable = useCallback((newValue: string) => {
    document.documentElement.style.setProperty(name, newValue);
    setValue(newValue);
  }, [name]);

  return [value, setVariable] as const;
}

// Usage
function ColorPicker() {
  const [primary, setPrimary] = useCSSVariable('--color-primary');
  return (
    <input type="color" value={primary} onChange={(e) => setPrimary(e.target.value)} />
  );
}
```

## Component Patterns

### Configurable Components

```css
.card {
  /* Component-scoped defaults */
  --card-padding: var(--space-4);
  --card-radius: var(--radius-md);
  --card-shadow: var(--shadow-md);
  --card-bg: var(--color-bg-secondary);

  padding: var(--card-padding);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  background: var(--card-bg);
}

/* Variants override internal variables */
.card--compact { --card-padding: var(--space-2); }
.card--flat { --card-shadow: none; }
.card--highlight { --card-bg: var(--color-primary-light); }
```

```tsx
<div className="card">Default card</div>
<div className="card card--compact">Compact card</div>
<div className="card" style={{ '--card-bg': '#f0f0f0' } as React.CSSProperties}>
  Custom background
</div>
```

### Animation Variables

```css
:root {
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
}

.button {
  transition: background var(--duration-fast) var(--ease-default),
              transform var(--duration-fast) var(--ease-default);
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --duration-slow: 0ms;
  }
}
```

### Grid System

```css
:root {
  --grid-columns: 12;
  --grid-gutter: 1rem;
  --container-max: 1200px;
}

.container {
  max-width: var(--container-max);
  padding-inline: var(--grid-gutter);
  margin-inline: auto;
}

.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), 1fr);
  gap: var(--grid-gutter);
}

/* Span utilities */
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-12 { grid-column: span 12; }
```

## Best Practices

### Naming Conventions

```css
/* Do: Semantic, hierarchical names */
:root {
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #6b7280;
  --button-bg-hover: var(--color-primary-dark);
}

/* Don't: Presentational names */
:root {
  --dark-gray: #1a1a1a;        /* What is it for? */
  --blue-button-bg: #0066cc;    /* Not reusable */
}
```

### Fallback Strategy

```css
/* Always provide fallbacks for critical values */
.element {
  color: var(--color-text, #333);
  font-size: var(--font-size-base, 1rem);
}

/* Use @supports for feature detection */
@supports (color: var(--test)) {
  /* CSS custom property styles */
}
```

### Organization

```css
/* 1. Primitives */
:root {
  /* Colors */
  --color-blue-500: #0066cc;
  /* Spacing */
  --space-4: 1rem;
  /* Typography */
  --font-size-base: 1rem;
}

/* 2. Semantic tokens */
:root {
  --color-primary: var(--color-blue-500);
  --color-text: var(--color-gray-900);
}

/* 3. Component tokens (in component files) */
.button {
  --button-bg: var(--color-primary);
}
```

## Tailwind CSS Integration

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
      },
      spacing: {
        unit: 'var(--space-unit)',
      },
    },
  },
};
```

```tsx
// Usage with Tailwind
<button className="bg-primary text-white p-[var(--button-padding)]">
  Button
</button>
```

## Quick Reference

```css
/* Definition */
:root { --name: value; }
.component { --scoped-name: value; }

/* Usage */
property: var(--name);
property: var(--name, fallback);
property: var(--name, var(--other, fallback));

/* Calculation */
property: calc(var(--base) * 2);

/* JavaScript */
getComputedStyle(el).getPropertyValue('--name');
el.style.setProperty('--name', 'value');

/* Media query override */
@media (min-width: 768px) { :root { --name: new-value; } }

/* Theme switching */
[data-theme="dark"] { --color-bg: #1a1a1a; }
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

