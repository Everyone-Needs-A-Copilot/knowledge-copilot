---
last_updated: 2026-02-25
status: active
name: typography-systems
description: Type scales, font hierarchies, responsive typography, and readability. Use when designing or implementing typography systems.
triggers:
  files: ["**/typography.*", "**/fonts.*", "**/type-scale.*", "**/text-styles.*"]
  keywords: ["typography", "font scale", "type hierarchy", "line height", "font pairing", "responsive type", "modular scale"]
allowed-tools: Read, Write, Edit
---

# Typography Systems: Deep Expertise Skill

Comprehensive guide to designing, implementing, and maintaining typography systems for digital products.

## Core Principles

### The Role of Typography

Typography is the foundation of visual communication. It establishes hierarchy, creates rhythm, and guides users through content. A well-designed typography system ensures consistency, readability, and brand expression across all touchpoints.

**Primary Functions:**
- **Hierarchy**: Distinguishes importance levels
- **Readability**: Ensures content is easily consumed
- **Rhythm**: Creates visual flow and pacing
- **Brand**: Expresses personality and tone
- **Accessibility**: Supports all users regardless of ability


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Type Scale Fundamentals

### Modular Scales

A modular scale creates harmonious relationships between type sizes using a mathematical ratio.

**Common Ratios:**

| Ratio | Name | Value | Use Case |
|-------|------|-------|----------|
| 1.067 | Minor Second | 16/15 | Subtle, dense interfaces |
| 1.125 | Major Second | 9/8 | Compact UI, mobile |
| 1.200 | Minor Third | 6/5 | General purpose |
| 1.250 | Major Third | 5/4 | Most UI applications |
| 1.333 | Perfect Fourth | 4/3 | Content-heavy, editorial |
| 1.414 | Augmented Fourth | √2 | Headlines, marketing |
| 1.500 | Perfect Fifth | 3/2 | Bold, impactful |
| 1.618 | Golden Ratio | φ | Classic, elegant |

### Building a Type Scale

```css
:root {
  /* Base size and ratio */
  --font-size-base: 1rem;      /* 16px */
  --type-ratio: 1.25;          /* Major Third */

  /* Scale: down */
  --font-size-xs: calc(var(--font-size-base) / var(--type-ratio) / var(--type-ratio));  /* ~10px */
  --font-size-sm: calc(var(--font-size-base) / var(--type-ratio));  /* ~13px */

  /* Scale: up */
  --font-size-md: var(--font-size-base);                            /* 16px */
  --font-size-lg: calc(var(--font-size-base) * var(--type-ratio));  /* 20px */
  --font-size-xl: calc(var(--font-size-base) * var(--type-ratio) * var(--type-ratio));  /* 25px */
  --font-size-2xl: calc(var(--font-size-base) * var(--type-ratio) * var(--type-ratio) * var(--type-ratio));  /* 31px */
  --font-size-3xl: calc(var(--font-size-base) * var(--type-ratio) * var(--type-ratio) * var(--type-ratio) * var(--type-ratio));  /* 39px */
}
```

### Practical Type Scale (Tailwind-Style)

```css
:root {
  /* Practical scale for UI */
  --font-size-xs: 0.75rem;     /* 12px - captions, labels */
  --font-size-sm: 0.875rem;    /* 14px - secondary text */
  --font-size-base: 1rem;      /* 16px - body text */
  --font-size-lg: 1.125rem;    /* 18px - lead text */
  --font-size-xl: 1.25rem;     /* 20px - h5 */
  --font-size-2xl: 1.5rem;     /* 24px - h4 */
  --font-size-3xl: 1.875rem;   /* 30px - h3 */
  --font-size-4xl: 2.25rem;    /* 36px - h2 */
  --font-size-5xl: 3rem;       /* 48px - h1 */
  --font-size-6xl: 3.75rem;    /* 60px - display */
  --font-size-7xl: 4.5rem;     /* 72px - hero */
  --font-size-8xl: 6rem;       /* 96px - jumbo */
}
```

## Line Height (Leading)

### Line Height Principles

Line height affects readability more than almost any other typographic property. Different contexts require different line heights.

**Guidelines by Context:**

| Context | Line Height | Rationale |
|---------|-------------|-----------|
| Headings | 1.1 - 1.25 | Tight for impact |
| UI Labels | 1.25 - 1.4 | Compact, scannable |
| Body Text | 1.5 - 1.75 | Optimal readability |
| Long Form | 1.6 - 1.8 | Comfortable reading |
| Small Text | 1.5 - 1.6 | Prevents cramping |

### Line Height Scale

```css
:root {
  --line-height-none: 1;
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* Semantic line heights */
  --line-height-heading: var(--line-height-tight);
  --line-height-body: var(--line-height-normal);
  --line-height-reading: var(--line-height-relaxed);
}
```

### Calculating Optimal Line Height

```javascript
function calculateLineHeight(fontSize, lineWidth, complexity = 'normal') {
  // Base calculation: smaller text needs more line height
  const baseLineHeight = fontSize < 14 ? 1.6 : fontSize < 20 ? 1.5 : 1.3;

  // Adjust for line width (longer lines need more height)
  const widthFactor = lineWidth > 75 ? 0.1 : lineWidth < 45 ? -0.1 : 0;

  // Adjust for content complexity
  const complexityFactor = {
    simple: -0.05,
    normal: 0,
    complex: 0.1
  }[complexity];

  return baseLineHeight + widthFactor + complexityFactor;
}
```

## Font Weight System

### Weight Scale

```css
:root {
  /* Numeric weights */
  --font-weight-thin: 100;
  --font-weight-extralight: 200;
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
  --font-weight-black: 900;

  /* Semantic weights */
  --font-weight-body: var(--font-weight-regular);
  --font-weight-heading: var(--font-weight-semibold);
  --font-weight-emphasis: var(--font-weight-medium);
  --font-weight-strong: var(--font-weight-bold);
}
```

### Weight Usage Guidelines

| Weight | Use Case | Example |
|--------|----------|---------|
| 300 Light | Large display text | Hero headlines |
| 400 Regular | Body text | Paragraphs, descriptions |
| 500 Medium | Emphasis, UI labels | Buttons, nav items |
| 600 Semibold | Subheadings | Section titles |
| 700 Bold | Headlines | Page titles |
| 800+ | Impact | Marketing, callouts |

## Font Family System

### Font Stack Structure

```css
:root {
  /* System font stacks */
  --font-family-system: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                        "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji",
                        "Segoe UI Emoji", "Segoe UI Symbol";

  --font-family-serif: Georgia, Cambria, "Times New Roman", Times, serif;

  --font-family-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
                      "Liberation Mono", "Courier New", monospace;

  /* Brand fonts with fallbacks */
  --font-family-sans: "Inter", var(--font-family-system);
  --font-family-display: "Poppins", var(--font-family-system);
  --font-family-body: "Source Sans Pro", var(--font-family-system);

  /* Semantic usage */
  --font-family-heading: var(--font-family-display);
  --font-family-text: var(--font-family-body);
  --font-family-code: var(--font-family-mono);
}
```

### Font Pairing Principles

**Contrast-Based Pairing:**
- Combine serif headings with sans-serif body
- Mix geometric with humanist
- Pair display with neutral

**Harmony-Based Pairing:**
- Same superfamily (e.g., Roboto + Roboto Slab)
- Similar x-height and proportions
- Matching historical period

**Safe Pairings:**

| Heading | Body | Style |
|---------|------|-------|
| Playfair Display | Source Sans Pro | Classic editorial |
| Montserrat | Open Sans | Modern, clean |
| Lora | Inter | Professional |
| Poppins | Roboto | Contemporary |
| Merriweather | Lato | Readable, warm |

## Letter Spacing (Tracking)

### Tracking Guidelines

```css
:root {
  --letter-spacing-tighter: -0.05em;
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  --letter-spacing-wider: 0.05em;
  --letter-spacing-widest: 0.1em;
}
```

**When to Adjust Tracking:**

| Context | Adjustment | Reason |
|---------|------------|--------|
| Large headings | Tighter | Improves cohesion |
| All caps | Wider | Improves legibility |
| Small text | Slightly wider | Prevents cramping |
| Condensed fonts | Slightly wider | Compensates for density |
| Extended fonts | Slightly tighter | Maintains rhythm |

## Responsive Typography

### Fluid Typography with Clamp

```css
:root {
  /* Fluid type scale: min @ 320px, max @ 1200px */
  --font-size-fluid-xs: clamp(0.625rem, 0.5rem + 0.4vw, 0.75rem);
  --font-size-fluid-sm: clamp(0.75rem, 0.6rem + 0.5vw, 0.875rem);
  --font-size-fluid-base: clamp(0.875rem, 0.75rem + 0.5vw, 1rem);
  --font-size-fluid-lg: clamp(1rem, 0.8rem + 0.8vw, 1.25rem);
  --font-size-fluid-xl: clamp(1.25rem, 0.9rem + 1.2vw, 1.75rem);
  --font-size-fluid-2xl: clamp(1.5rem, 1rem + 1.5vw, 2.25rem);
  --font-size-fluid-3xl: clamp(2rem, 1.2rem + 2.5vw, 3.5rem);
  --font-size-fluid-4xl: clamp(2.5rem, 1.5rem + 3.5vw, 5rem);
}
```

### Breakpoint-Based Scaling

```css
:root {
  --font-size-h1: 2rem;
  --font-size-h2: 1.5rem;
  --font-size-body: 1rem;
}

@media (min-width: 768px) {
  :root {
    --font-size-h1: 2.5rem;
    --font-size-h2: 1.875rem;
    --font-size-body: 1rem;
  }
}

@media (min-width: 1024px) {
  :root {
    --font-size-h1: 3rem;
    --font-size-h2: 2.25rem;
    --font-size-body: 1.125rem;
  }
}
```

## Measure (Line Length)

### Optimal Line Length

Research shows optimal reading occurs at 45-75 characters per line, with 66 characters being ideal.

```css
:root {
  --measure-narrow: 45ch;   /* Tight, focused reading */
  --measure-optimal: 65ch;  /* Ideal for body text */
  --measure-wide: 80ch;     /* Code, technical content */
}

.prose {
  max-width: var(--measure-optimal);
}

.narrow-column {
  max-width: var(--measure-narrow);
}

.code-block {
  max-width: var(--measure-wide);
}
```

## Typography Tokens

### Complete Token System

```css
:root {
  /* === FONT FAMILIES === */
  --font-family-sans: "Inter", -apple-system, sans-serif;
  --font-family-serif: "Merriweather", Georgia, serif;
  --font-family-mono: "JetBrains Mono", monospace;

  --font-family-heading: var(--font-family-sans);
  --font-family-body: var(--font-family-sans);
  --font-family-code: var(--font-family-mono);

  /* === FONT SIZES === */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;
  --font-size-5xl: 3rem;

  /* === FONT WEIGHTS === */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* === LINE HEIGHTS === */
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;

  /* === LETTER SPACING === */
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;

  /* === SEMANTIC COMPOSITIONS === */
  /* Display */
  --typography-display-xl: var(--font-weight-bold) var(--font-size-5xl)/var(--line-height-tight) var(--font-family-heading);
  --typography-display-lg: var(--font-weight-bold) var(--font-size-4xl)/var(--line-height-tight) var(--font-family-heading);

  /* Headings */
  --typography-h1: var(--font-weight-semibold) var(--font-size-3xl)/var(--line-height-tight) var(--font-family-heading);
  --typography-h2: var(--font-weight-semibold) var(--font-size-2xl)/var(--line-height-tight) var(--font-family-heading);
  --typography-h3: var(--font-weight-semibold) var(--font-size-xl)/var(--line-height-snug) var(--font-family-heading);
  --typography-h4: var(--font-weight-semibold) var(--font-size-lg)/var(--line-height-snug) var(--font-family-heading);

  /* Body */
  --typography-body-lg: var(--font-weight-normal) var(--font-size-lg)/var(--line-height-relaxed) var(--font-family-body);
  --typography-body: var(--font-weight-normal) var(--font-size-base)/var(--line-height-normal) var(--font-family-body);
  --typography-body-sm: var(--font-weight-normal) var(--font-size-sm)/var(--line-height-normal) var(--font-family-body);

  /* Utility */
  --typography-caption: var(--font-weight-normal) var(--font-size-xs)/var(--line-height-normal) var(--font-family-body);
  --typography-overline: var(--font-weight-semibold) var(--font-size-xs)/var(--line-height-tight) var(--font-family-body);
  --typography-code: var(--font-weight-normal) var(--font-size-sm)/var(--line-height-normal) var(--font-family-code);
}
```

## Accessibility

### WCAG Typography Requirements

**Minimum Requirements:**
- Text resizable up to 200% without loss of content
- Line height at least 1.5× font size for body text
- Paragraph spacing at least 2× font size
- Letter spacing at least 0.12× font size
- Word spacing at least 0.16× font size

### Accessible Typography Implementation

```css
/* Ensure text remains readable when scaled */
html {
  font-size: 100%; /* Respect user preferences */
}

/* Use relative units throughout */
body {
  font-size: 1rem;
  line-height: 1.5;
}

/* Support user spacing preferences */
p {
  margin-block: 1.5em;
  letter-spacing: 0.12em;
  word-spacing: 0.16em;
}

/* Maintain readability at scale */
@media (prefers-reduced-motion: no-preference) {
  html {
    scroll-behavior: smooth;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  body {
    font-weight: 500; /* Slightly bolder for contrast */
  }
}
```

## Implementation Patterns

### React Typography Component

```tsx
interface TypographyProps {
  variant: 'display' | 'h1' | 'h2' | 'h3' | 'body' | 'caption';
  as?: keyof JSX.IntrinsicElements;
  children: React.ReactNode;
  className?: string;
}

const variantStyles = {
  display: 'text-5xl font-bold leading-tight tracking-tight',
  h1: 'text-3xl font-semibold leading-tight',
  h2: 'text-2xl font-semibold leading-tight',
  h3: 'text-xl font-semibold leading-snug',
  body: 'text-base font-normal leading-normal',
  caption: 'text-xs font-normal leading-normal text-gray-600'
};

const variantElements = {
  display: 'h1',
  h1: 'h1',
  h2: 'h2',
  h3: 'h3',
  body: 'p',
  caption: 'span'
};

export function Typography({ variant, as, children, className }: TypographyProps) {
  const Component = as || variantElements[variant];

  return (
    <Component className={`${variantStyles[variant]} ${className || ''}`}>
      {children}
    </Component>
  );
}
```

### Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    fontFamily: {
      sans: ['Inter', ...defaultTheme.fontFamily.sans],
      serif: ['Merriweather', ...defaultTheme.fontFamily.serif],
      mono: ['JetBrains Mono', ...defaultTheme.fontFamily.mono],
    },
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],
      sm: ['0.875rem', { lineHeight: '1.25rem' }],
      base: ['1rem', { lineHeight: '1.5rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '1.75rem' }],
      '2xl': ['1.5rem', { lineHeight: '2rem' }],
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      '5xl': ['3rem', { lineHeight: '1.15' }],
    },
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            lineHeight: '1.6',
          },
        },
      },
    },
  },
};
```

## Anti-Patterns

### Common Typography Mistakes

**Using px for font sizes:**
```css
/* Bad - doesn't scale with user preferences */
body { font-size: 16px; }

/* Good - respects user settings */
body { font-size: 1rem; }
```

**Insufficient line height:**
```css
/* Bad - cramped, hard to read */
p { line-height: 1.2; }

/* Good - comfortable reading */
p { line-height: 1.5; }
```

**Too many font families:**
```css
/* Bad - visual chaos */
h1 { font-family: "Playfair Display"; }
h2 { font-family: "Montserrat"; }
p { font-family: "Open Sans"; }
.caption { font-family: "Roboto"; }

/* Good - focused system */
h1, h2 { font-family: var(--font-family-heading); }
p, .caption { font-family: var(--font-family-body); }
```

**Ignoring measure:**
```css
/* Bad - lines too long */
.content { width: 100%; }

/* Good - optimal reading width */
.content { max-width: 65ch; }
```

## Summary

Typography systems require careful attention to scale, hierarchy, and consistency. Key principles:

1. **Use modular scales** for harmonious relationships
2. **Optimize line height** for the content context
3. **Limit font families** to 2-3 maximum
4. **Use semantic tokens** for maintainability
5. **Implement fluid typography** for responsiveness
6. **Control measure** for readability
7. **Ensure accessibility** through proper sizing and spacing

---

**When to use this skill:**
- Designing a new type system
- Implementing responsive typography
- Auditing typography for accessibility
- Creating design tokens for type
- Establishing brand typography guidelines


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

