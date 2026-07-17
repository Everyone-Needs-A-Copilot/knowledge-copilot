---
last_updated: 2026-02-25
status: active
name: typography-systems
description: Design type scales, font pairings, and line-height systems for readable, harmonious interfaces. Use when establishing typography foundations or reviewing text legibility.
triggers:
  files: ["**/typography/**", "**/fonts/**", "**/type.*", "**/text.**"]
  keywords: ["typography", "type scale", "font pairing", "line height", "font family", "type system", "readability"]
allowed-tools: Read, Write, Edit
---

# Typography Systems

Typography systems establish consistent, readable text across an interface. A well-designed type system creates visual rhythm, supports hierarchy, and ensures legibility across devices.

## Core Principle

**Typography is 95% of web design.** Text carries meaning - make it easy to read and pleasant to look at.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Type Scale

A type scale creates harmonious size relationships using mathematical ratios.

### Common Ratios

| Ratio | Name | Scale Example (16px base) |
|-------|------|---------------------------|
| 1.067 | Minor Second | 15, 16, 17, 18 |
| 1.125 | Major Second | 14, 16, 18, 20, 23 |
| 1.200 | Minor Third | 13, 16, 19, 23, 28 |
| 1.250 | Major Third | 13, 16, 20, 25, 31 |
| 1.333 | Perfect Fourth | 12, 16, 21, 28, 37 |
| 1.414 | Augmented Fourth | 11, 16, 23, 32, 45 |
| 1.500 | Perfect Fifth | 11, 16, 24, 36, 54 |
| 1.618 | Golden Ratio | 10, 16, 26, 42, 68 |

### Recommended Scale

For most UI work, use **Major Third (1.250)** or **Perfect Fourth (1.333)**:

```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;      /* 48px */
```

## Font Pairing

Pair fonts with complementary characteristics. The classic approach: one serif and one sans-serif.

### Pairing Strategies

| Strategy | Example | Best For |
|----------|---------|----------|
| Contrast | Serif heading + sans body | Editorial, premium |
| Similar x-height | Fonts with matching proportions | Cohesive feel |
| Same family | Weight variations only | Simplicity, consistency |
| Historical match | Fonts from same era | Period-specific design |

### Safe Pairings

| Heading | Body | Character |
|---------|------|-----------|
| Playfair Display | Source Sans Pro | Elegant, editorial |
| Roboto Slab | Roboto | Clean, modern |
| Montserrat | Open Sans | Friendly, approachable |
| Merriweather | Lato | Readable, warm |
| Work Sans | Work Sans | Minimal, versatile |

### Pairing Rules

1. **Maximum 2-3 fonts** per project
2. **Contrasting weights** between heading/body
3. **Similar x-height** for visual harmony
4. **Test at multiple sizes** before committing

## Line Height

Line height (leading) affects readability significantly. Too tight strains eyes; too loose breaks reading flow.

### Line Height Guidelines

| Content Type | Line Height | Rationale |
|--------------|-------------|-----------|
| Body text | 1.5-1.6 | Optimal readability |
| Headings | 1.1-1.3 | Tighter for visual unity |
| Small text (<14px) | 1.6-1.8 | More space aids legibility |
| Long-form | 1.6-1.8 | Reduces fatigue |
| UI labels | 1.2-1.4 | Compact, efficient |

### Responsive Line Height

```css
/* Tighter on mobile (narrower columns) */
body {
  line-height: 1.5;
}

/* Slightly looser on desktop (wider columns) */
@media (min-width: 768px) {
  body {
    line-height: 1.6;
  }
}
```

## Measure (Line Length)

Optimal characters per line for comfortable reading.

| Content Type | Characters | Rationale |
|--------------|------------|-----------|
| Body text | 45-75 | Classic readability range |
| Ideal | 66 | Research-backed optimum |
| Wide columns | 75-90 | Acceptable with larger line-height |
| Narrow columns | 30-45 | Good for mobile, sidebars |

```css
/* Constrain measure */
.prose {
  max-width: 65ch; /* Character-based width */
}
```

## Typography Scale Implementation

### CSS Custom Properties

```css
:root {
  /* Font families */
  --font-family-heading: 'Inter', sans-serif;
  --font-family-body: 'Inter', sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;

  /* Font weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Letter spacing */
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  --letter-spacing-wider: 0.05em;
}
```

### Semantic Type Styles

```css
/* Headings */
h1 { font: var(--font-weight-bold) var(--font-size-4xl)/var(--line-height-tight) var(--font-family-heading); }
h2 { font: var(--font-weight-semibold) var(--font-size-3xl)/var(--line-height-tight) var(--font-family-heading); }
h3 { font: var(--font-weight-semibold) var(--font-size-2xl)/var(--line-height-tight) var(--font-family-heading); }
h4 { font: var(--font-weight-semibold) var(--font-size-xl)/var(--line-height-tight) var(--font-family-heading); }

/* Body */
body { font: var(--font-weight-normal) var(--font-size-base)/var(--line-height-normal) var(--font-family-body); }

/* Supporting */
.caption { font-size: var(--font-size-sm); line-height: var(--line-height-relaxed); }
.overline { font-size: var(--font-size-xs); letter-spacing: var(--letter-spacing-wider); text-transform: uppercase; }
```

## Evaluation Checklist

- [ ] Body text is 16px or larger
- [ ] Line height is 1.4-1.6 for body text
- [ ] Measure is 45-75 characters
- [ ] Font pairing has clear contrast or cohesion
- [ ] Weights span from regular (400) to bold (700)
- [ ] Headings use tighter line height than body
- [ ] Type scale follows a mathematical ratio

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Too many fonts | Visual chaos | Max 2-3 font families |
| Inconsistent scale | Random sizes | Use mathematical ratio |
| Tight line height | Hard to read | 1.5+ for body text |
| Wide measure | Eyes lose place | Max 75 characters |
| No weight variation | Weak hierarchy | Use 3-4 weights minimum |
| Centered body text | Harder to read | Left-align long text |

---

**Remember**: Good typography is invisible - readers focus on content, not the letters themselves.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

