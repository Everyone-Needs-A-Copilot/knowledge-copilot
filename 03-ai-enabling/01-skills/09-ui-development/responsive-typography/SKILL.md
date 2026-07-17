---
last_updated: 2026-02-25
status: active
name: responsive-typography
description: Fluid typography systems using clamp(), viewport units, and modular scales. Use when building scalable type systems that adapt across screen sizes.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/styles/**", "**/typography/**", "**/theme/**"]
  keywords: ["typography", "font-size", "clamp", "fluid", "responsive", "viewport", "vw", "modular scale", "line-height"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Responsive Typography

Create fluid, accessible typography that scales beautifully across all screen sizes.

## Core Concepts

### Fluid Typography with clamp()

```css
/* clamp(minimum, preferred, maximum) */
.heading {
  font-size: clamp(1.5rem, 4vw, 3rem);
  /* Min: 1.5rem (24px) */
  /* Preferred: 4vw (scales with viewport) */
  /* Max: 3rem (48px) */
}

/* Formula for preferred value */
/* preferred = minSize + (maxSize - minSize) * viewportFactor */
```

### Why Not Just vw?

| Method | Issue |
|--------|-------|
| `font-size: 4vw` | Too small on mobile, too large on desktop |
| `font-size: 16px` | Doesn't scale |
| `font-size: clamp()` | Best of both worlds |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Type Scale System

### Modular Scale

```css
:root {
  /* Base values */
  --font-size-base: 1rem;        /* 16px */
  --scale-ratio: 1.25;           /* Major third */

  /* Calculated scale */
  --font-size-xs: calc(var(--font-size-base) / var(--scale-ratio));                    /* 0.8rem */
  --font-size-sm: calc(var(--font-size-base) / 1.125);                                  /* 0.889rem */
  --font-size-md: var(--font-size-base);                                                 /* 1rem */
  --font-size-lg: calc(var(--font-size-base) * var(--scale-ratio));                     /* 1.25rem */
  --font-size-xl: calc(var(--font-size-base) * var(--scale-ratio) * var(--scale-ratio)); /* 1.563rem */
  --font-size-2xl: calc(var(--font-size-xl) * var(--scale-ratio));                       /* 1.953rem */
  --font-size-3xl: calc(var(--font-size-2xl) * var(--scale-ratio));                      /* 2.441rem */
  --font-size-4xl: calc(var(--font-size-3xl) * var(--scale-ratio));                      /* 3.052rem */
}
```

### Fluid Type Scale

```css
:root {
  /* Fluid scale with clamp() */
  --step--2: clamp(0.69rem, 0.66rem + 0.18vw, 0.8rem);
  --step--1: clamp(0.83rem, 0.78rem + 0.29vw, 1rem);
  --step-0: clamp(1rem, 0.91rem + 0.43vw, 1.25rem);
  --step-1: clamp(1.2rem, 1.07rem + 0.63vw, 1.56rem);
  --step-2: clamp(1.44rem, 1.26rem + 0.89vw, 1.95rem);
  --step-3: clamp(1.73rem, 1.48rem + 1.24vw, 2.44rem);
  --step-4: clamp(2.07rem, 1.73rem + 1.7vw, 3.05rem);
  --step-5: clamp(2.49rem, 2.03rem + 2.31vw, 3.82rem);
}

/* Apply to elements */
body { font-size: var(--step-0); }
h1 { font-size: var(--step-5); }
h2 { font-size: var(--step-4); }
h3 { font-size: var(--step-3); }
h4 { font-size: var(--step-2); }
h5 { font-size: var(--step-1); }
h6 { font-size: var(--step-0); }
small { font-size: var(--step--1); }
```

### Calculate clamp() Values

```
/* Formula */
clamp(minSize, preferredSize, maxSize)

/* preferredSize calculation */
preferredSize = minSize + (maxSize - minSize) * ((100vw - minViewport) / (maxViewport - minViewport))

/* Simplified for 320px-1200px viewport range */
preferredSize = minSizeRem + (maxSizeRem - minSizeRem) * (100vw - 20rem) / (75rem - 20rem)
             = minSizeRem + (maxSizeRem - minSizeRem) * 1.818vw

/* Example: 1rem to 1.5rem */
clamp(1rem, 0.727rem + 0.909vw, 1.5rem)
```

## Line Height

### Fluid Line Height

```css
:root {
  --line-height-tight: 1.2;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;
}

/* Headings: tighter */
h1, h2, h3 { line-height: var(--line-height-tight); }

/* Body: comfortable */
body { line-height: var(--line-height-normal); }

/* Long-form: relaxed */
article p { line-height: var(--line-height-relaxed); }
```

### Line Length (Measure)

```css
/* Optimal: 45-75 characters per line */
.prose {
  max-width: 65ch; /* Character-based width */
}

/* Responsive measure */
.content {
  max-width: min(65ch, 100% - 2rem);
  margin-inline: auto;
}
```

## Spacing and Rhythm

### Vertical Rhythm

```css
:root {
  --rhythm: 1.5rem; /* Base line-height in rem */
}

/* All spacing based on rhythm */
h1 { margin-bottom: var(--rhythm); }
h2 { margin-top: calc(var(--rhythm) * 2); margin-bottom: var(--rhythm); }
p { margin-bottom: var(--rhythm); }

/* Or simpler flow spacing */
.flow > * + * {
  margin-top: var(--flow-space, 1.5em);
}

h2 { --flow-space: 2em; }
h3 { --flow-space: 1.5em; }
```

### Letter Spacing

```css
/* Headings: slightly tighter at large sizes */
h1 { letter-spacing: -0.02em; }
h2 { letter-spacing: -0.01em; }

/* Small text: slightly looser */
.caption { letter-spacing: 0.02em; }

/* All caps: always looser */
.uppercase {
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

## Complete Typography System

```css
:root {
  /* Font families */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-serif: Georgia, Cambria, 'Times New Roman', serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Font weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Fluid type scale */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --text-4xl: clamp(2.25rem, 1.75rem + 2.5vw, 3rem);
  --text-5xl: clamp(3rem, 2.25rem + 3.75vw, 4rem);

  /* Line heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
}

/* Base styles */
body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--color-text);
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  font-weight: var(--font-weight-bold);
  line-height: var(--leading-tight);
}

h1 { font-size: var(--text-5xl); }
h2 { font-size: var(--text-4xl); }
h3 { font-size: var(--text-3xl); }
h4 { font-size: var(--text-2xl); }
h5 { font-size: var(--text-xl); }
h6 { font-size: var(--text-lg); }

/* Prose content */
.prose {
  max-width: 65ch;
  font-size: var(--text-lg);
  line-height: var(--leading-relaxed);
}

.prose p { margin-bottom: 1.5em; }

.prose h2 {
  font-size: var(--text-3xl);
  margin-top: 2em;
  margin-bottom: 0.5em;
}
```

## React/Tailwind Integration

### Tailwind Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    fontSize: {
      xs: 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
      sm: 'clamp(0.875rem, 0.8rem + 0.375vw, 1rem)',
      base: 'clamp(1rem, 0.9rem + 0.5vw, 1.125rem)',
      lg: 'clamp(1.125rem, 1rem + 0.625vw, 1.25rem)',
      xl: 'clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)',
      '2xl': 'clamp(1.5rem, 1.25rem + 1.25vw, 2rem)',
      '3xl': 'clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem)',
      '4xl': 'clamp(2.25rem, 1.75rem + 2.5vw, 3rem)',
      '5xl': 'clamp(3rem, 2.25rem + 3.75vw, 4rem)',
    },
  },
};
```

### Typography Component

```tsx
interface TextProps {
  as?: 'p' | 'span' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
  size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl';
  weight?: 'normal' | 'medium' | 'semibold' | 'bold';
  children: React.ReactNode;
  className?: string;
}

function Text({
  as: Component = 'p',
  size = 'base',
  weight = 'normal',
  children,
  className,
}: TextProps) {
  const sizeClass = {
    xs: 'text-xs',
    sm: 'text-sm',
    base: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
    '2xl': 'text-2xl',
    '3xl': 'text-3xl',
    '4xl': 'text-4xl',
    '5xl': 'text-5xl',
  }[size];

  const weightClass = {
    normal: 'font-normal',
    medium: 'font-medium',
    semibold: 'font-semibold',
    bold: 'font-bold',
  }[weight];

  return (
    <Component className={`${sizeClass} ${weightClass} ${className || ''}`}>
      {children}
    </Component>
  );
}

// Usage
<Text as="h1" size="5xl" weight="bold">Page Title</Text>
<Text size="lg">Body text with larger size</Text>
```

## Accessibility

### Respect User Preferences

```css
/* Respect user font size preference */
html {
  font-size: 100%; /* Uses browser default (usually 16px) */
}

/* Never use px for font-size */
body {
  font-size: 1rem;     /* Good: relative */
  font-size: 16px;     /* Bad: fixed */
}

/* Allow zoom to 200% without breaking layout */
.container {
  max-width: min(65ch, 100%);
}
```

### Minimum Font Sizes

```css
/* Ensure readability */
body { font-size: max(1rem, 16px); }
small { font-size: max(0.875rem, 14px); }

/* Clamp with minimum */
.text {
  font-size: clamp(max(1rem, 16px), 2vw, 1.25rem);
}
```

## Best Practices

1. **Use relative units** (rem, em) for font sizes
2. **Set base font-size: 100%** on html element
3. **Use clamp()** for fluid typography
4. **Limit line length** to 45-75 characters
5. **Maintain vertical rhythm** with consistent spacing
6. **Test at 200% zoom** for accessibility
7. **Use system fonts** for performance
8. **Provide sufficient contrast** (4.5:1 minimum)

## Quick Reference

```css
/* Fluid typography */
font-size: clamp(1rem, 0.5rem + 2vw, 2rem);

/* Type scale (1.25 ratio) */
--step-0: 1rem;
--step-1: 1.25rem;
--step-2: 1.563rem;
--step-3: 1.953rem;

/* Line height by use case */
headings: 1.2
body: 1.5
long-form: 1.625

/* Measure */
max-width: 65ch;

/* Accessible base */
html { font-size: 100%; }
body { font-size: 1rem; }
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

