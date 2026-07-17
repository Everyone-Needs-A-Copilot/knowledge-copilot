---
last_updated: 2026-02-25
status: active
name: design-token-architecture
description: Token taxonomy, naming conventions, tiered architecture, and cross-platform token systems. Use when structuring design system foundations.
triggers:
  files: ["**/tokens/**", "**/variables.*", "**/theme.*", "**/design-system/**"]
  keywords: ["design tokens", "token architecture", "semantic tokens", "primitive tokens", "token taxonomy", "css variables", "theming"]
allowed-tools: Read, Write, Edit
---

# Design Token Architecture: Deep Expertise Skill

Building scalable, maintainable design token systems with proper taxonomy, naming conventions, and multi-tier architecture.

## What Are Design Tokens

Design tokens are the atomic values that define a design system's visual properties. They create a single source of truth that bridges design and development.

### Token Benefits

| Benefit | Description |
|---------|-------------|
| **Consistency** | Single source of truth for values |
| **Maintainability** | Change once, update everywhere |
| **Scalability** | Supports theming and white-labeling |
| **Communication** | Shared vocabulary between teams |
| **Automation** | Enables design-to-code workflows |


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Token Taxonomy

### Three-Tier Token Architecture

```
┌─────────────────────────────────────────┐
│  COMPONENT TOKENS (Tier 3)              │
│  --button-bg, --card-padding            │
│  Most specific, component-scoped        │
├─────────────────────────────────────────┤
│  SEMANTIC TOKENS (Tier 2)               │
│  --color-primary, --space-md            │
│  Purpose-based, context-aware           │
├─────────────────────────────────────────┤
│  PRIMITIVE TOKENS (Tier 1)              │
│  --blue-500, --space-16                 │
│  Raw values, context-free               │
└─────────────────────────────────────────┘
```

### Tier Definitions

| Tier | Name | Purpose | Example |
|------|------|---------|---------|
| 1 | **Primitive** | Raw, context-free values | `--blue-500: #3b82f6` |
| 2 | **Semantic** | Purpose-based aliases | `--color-primary: var(--blue-500)` |
| 3 | **Component** | Component-specific | `--button-bg: var(--color-primary)` |

## Primitive Tokens

### Color Primitives

```css
:root {
  /* Gray scale */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --gray-950: #030712;

  /* Primary color scale (Blue) */
  --blue-50: #eff6ff;
  --blue-100: #dbeafe;
  --blue-200: #bfdbfe;
  --blue-300: #93c5fd;
  --blue-400: #60a5fa;
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --blue-700: #1d4ed8;
  --blue-800: #1e40af;
  --blue-900: #1e3a8a;
  --blue-950: #172554;

  /* Success (Green) */
  --green-50: #f0fdf4;
  --green-500: #22c55e;
  --green-600: #16a34a;
  --green-700: #15803d;

  /* Warning (Amber) */
  --amber-50: #fffbeb;
  --amber-500: #f59e0b;
  --amber-600: #d97706;
  --amber-700: #b45309;

  /* Error (Red) */
  --red-50: #fef2f2;
  --red-500: #ef4444;
  --red-600: #dc2626;
  --red-700: #b91c1c;
}
```

### Spacing Primitives

```css
:root {
  /* Base unit: 4px */
  --space-0: 0;
  --space-px: 1px;
  --space-0-5: 2px;
  --space-1: 4px;
  --space-1-5: 6px;
  --space-2: 8px;
  --space-2-5: 10px;
  --space-3: 12px;
  --space-3-5: 14px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 28px;
  --space-8: 32px;
  --space-9: 36px;
  --space-10: 40px;
  --space-11: 44px;
  --space-12: 48px;
  --space-14: 56px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  --space-28: 112px;
  --space-32: 128px;
}
```

### Typography Primitives

```css
:root {
  /* Font families */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-serif: 'Georgia', serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Font sizes */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  --text-5xl: 3rem;      /* 48px */
  --text-6xl: 3.75rem;   /* 60px */

  /* Font weights */
  --font-thin: 100;
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-extrabold: 800;

  /* Line heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;

  /* Letter spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
}
```

### Other Primitives

```css
:root {
  /* Border radius */
  --radius-none: 0;
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-2xl: 16px;
  --radius-3xl: 24px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
  --shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.25);

  /* Durations */
  --duration-75: 75ms;
  --duration-100: 100ms;
  --duration-150: 150ms;
  --duration-200: 200ms;
  --duration-300: 300ms;
  --duration-500: 500ms;
  --duration-700: 700ms;
  --duration-1000: 1000ms;

  /* Easings */
  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* Z-index scale */
  --z-0: 0;
  --z-10: 10;
  --z-20: 20;
  --z-30: 30;
  --z-40: 40;
  --z-50: 50;
}
```

## Semantic Tokens

### Color Semantics

```css
:root {
  /* Brand colors */
  --color-primary: var(--blue-600);
  --color-primary-hover: var(--blue-700);
  --color-primary-active: var(--blue-800);
  --color-primary-subtle: var(--blue-50);

  /* Neutral colors */
  --color-background: var(--gray-50);
  --color-surface: white;
  --color-surface-raised: white;
  --color-surface-overlay: white;

  /* Text colors */
  --color-text: var(--gray-900);
  --color-text-secondary: var(--gray-600);
  --color-text-tertiary: var(--gray-500);
  --color-text-disabled: var(--gray-400);
  --color-text-inverse: white;
  --color-text-link: var(--blue-600);

  /* Border colors */
  --color-border: var(--gray-200);
  --color-border-strong: var(--gray-300);
  --color-border-subtle: var(--gray-100);

  /* Feedback colors */
  --color-success: var(--green-600);
  --color-success-subtle: var(--green-50);
  --color-warning: var(--amber-500);
  --color-warning-subtle: var(--amber-50);
  --color-error: var(--red-600);
  --color-error-subtle: var(--red-50);
  --color-info: var(--blue-600);
  --color-info-subtle: var(--blue-50);

  /* Interactive states */
  --color-focus-ring: var(--blue-500);
  --color-selection: var(--blue-100);
}
```

### Spacing Semantics

```css
:root {
  /* Component internal spacing */
  --space-inset-xs: var(--space-1);
  --space-inset-sm: var(--space-2);
  --space-inset-md: var(--space-4);
  --space-inset-lg: var(--space-6);
  --space-inset-xl: var(--space-8);

  /* Stack spacing (vertical) */
  --space-stack-xs: var(--space-1);
  --space-stack-sm: var(--space-2);
  --space-stack-md: var(--space-4);
  --space-stack-lg: var(--space-6);
  --space-stack-xl: var(--space-8);
  --space-stack-2xl: var(--space-12);

  /* Inline spacing (horizontal) */
  --space-inline-xs: var(--space-1);
  --space-inline-sm: var(--space-2);
  --space-inline-md: var(--space-3);
  --space-inline-lg: var(--space-4);

  /* Section spacing */
  --space-section-sm: var(--space-12);
  --space-section-md: var(--space-16);
  --space-section-lg: var(--space-24);
}
```

### Typography Semantics

```css
:root {
  /* Headings */
  --font-heading: var(--font-sans);
  --font-body: var(--font-sans);
  --font-code: var(--font-mono);

  /* Heading sizes */
  --heading-xl-size: var(--text-4xl);
  --heading-xl-weight: var(--font-bold);
  --heading-xl-leading: var(--leading-tight);

  --heading-lg-size: var(--text-3xl);
  --heading-lg-weight: var(--font-bold);
  --heading-lg-leading: var(--leading-tight);

  --heading-md-size: var(--text-2xl);
  --heading-md-weight: var(--font-semibold);
  --heading-md-leading: var(--leading-snug);

  --heading-sm-size: var(--text-xl);
  --heading-sm-weight: var(--font-semibold);
  --heading-sm-leading: var(--leading-snug);

  --heading-xs-size: var(--text-lg);
  --heading-xs-weight: var(--font-semibold);
  --heading-xs-leading: var(--leading-normal);

  /* Body text */
  --body-lg-size: var(--text-lg);
  --body-md-size: var(--text-base);
  --body-sm-size: var(--text-sm);

  /* UI text */
  --ui-label-size: var(--text-sm);
  --ui-label-weight: var(--font-medium);
  --ui-helper-size: var(--text-xs);
  --ui-caption-size: var(--text-xs);
}
```

## Component Tokens

### Button Component Tokens

```css
:root {
  /* Button base */
  --button-font-family: var(--font-body);
  --button-font-weight: var(--font-medium);
  --button-border-width: 1px;
  --button-transition: all var(--duration-150) var(--ease-in-out);

  /* Button sizes */
  --button-sm-height: var(--space-8);
  --button-sm-padding-x: var(--space-3);
  --button-sm-font-size: var(--text-sm);
  --button-sm-radius: var(--radius-md);

  --button-md-height: var(--space-10);
  --button-md-padding-x: var(--space-4);
  --button-md-font-size: var(--text-sm);
  --button-md-radius: var(--radius-lg);

  --button-lg-height: var(--space-12);
  --button-lg-padding-x: var(--space-6);
  --button-lg-font-size: var(--text-base);
  --button-lg-radius: var(--radius-lg);

  /* Button primary variant */
  --button-primary-bg: var(--color-primary);
  --button-primary-bg-hover: var(--color-primary-hover);
  --button-primary-bg-active: var(--color-primary-active);
  --button-primary-text: var(--color-text-inverse);
  --button-primary-border: var(--color-primary);

  /* Button secondary variant */
  --button-secondary-bg: transparent;
  --button-secondary-bg-hover: var(--color-primary-subtle);
  --button-secondary-text: var(--color-primary);
  --button-secondary-border: var(--color-primary);
}
```

### Input Component Tokens

```css
:root {
  /* Input base */
  --input-font-family: var(--font-body);
  --input-font-size: var(--text-sm);
  --input-border-width: 1px;
  --input-transition: border-color var(--duration-150) var(--ease-in-out),
                      box-shadow var(--duration-150) var(--ease-in-out);

  /* Input sizes */
  --input-sm-height: var(--space-8);
  --input-sm-padding-x: var(--space-2);
  --input-sm-radius: var(--radius-md);

  --input-md-height: var(--space-10);
  --input-md-padding-x: var(--space-3);
  --input-md-radius: var(--radius-lg);

  --input-lg-height: var(--space-12);
  --input-lg-padding-x: var(--space-4);
  --input-lg-radius: var(--radius-lg);

  /* Input states */
  --input-bg: var(--color-surface);
  --input-border: var(--color-border);
  --input-border-hover: var(--color-border-strong);
  --input-border-focus: var(--color-primary);
  --input-border-error: var(--color-error);
  --input-text: var(--color-text);
  --input-placeholder: var(--color-text-tertiary);
  --input-focus-ring: 0 0 0 3px var(--color-primary-subtle);
}
```

### Card Component Tokens

```css
:root {
  /* Card base */
  --card-bg: var(--color-surface);
  --card-border: var(--color-border-subtle);
  --card-border-width: 1px;
  --card-radius: var(--radius-xl);
  --card-shadow: var(--shadow-sm);
  --card-shadow-hover: var(--shadow-md);

  /* Card spacing */
  --card-padding-sm: var(--space-4);
  --card-padding-md: var(--space-6);
  --card-padding-lg: var(--space-8);

  /* Card content */
  --card-title-size: var(--heading-sm-size);
  --card-title-weight: var(--heading-sm-weight);
  --card-body-size: var(--body-md-size);
  --card-divider: var(--color-border-subtle);
}
```

## Naming Conventions

### Token Naming Pattern

```
--{category}-{property}-{variant}-{state}

Examples:
--color-text-primary
--color-bg-surface-hover
--space-inset-md
--button-bg-primary-active
```

### Naming Guidelines

| Rule | Good | Bad |
|------|------|-----|
| **Lowercase** | `--color-primary` | `--Color-Primary` |
| **Hyphen-separated** | `--font-size-lg` | `--fontSizeLg` |
| **Category first** | `--color-text-primary` | `--primary-text-color` |
| **No abbreviations** | `--background` | `--bg` (except common: bg, sm, md, lg) |
| **Consistent order** | `--button-bg-primary-hover` | `--hover-primary-bg-button` |

### Category Prefixes

| Prefix | Category | Examples |
|--------|----------|----------|
| `color-` | Colors | `--color-primary`, `--color-text` |
| `space-` | Spacing | `--space-4`, `--space-inset-md` |
| `font-` | Typography | `--font-sans`, `--font-medium` |
| `text-` | Text sizes | `--text-sm`, `--text-base` |
| `leading-` | Line height | `--leading-normal` |
| `tracking-` | Letter spacing | `--tracking-wide` |
| `radius-` | Border radius | `--radius-lg` |
| `shadow-` | Shadows | `--shadow-md` |
| `duration-` | Animation | `--duration-200` |
| `ease-` | Easing | `--ease-out` |
| `z-` | Z-index | `--z-modal` |

## Theming with Tokens

### Theme Switching

```css
/* Light theme (default) */
:root {
  --color-background: var(--gray-50);
  --color-surface: white;
  --color-text: var(--gray-900);
  --color-text-secondary: var(--gray-600);
  --color-border: var(--gray-200);
}

/* Dark theme */
[data-theme="dark"] {
  --color-background: var(--gray-950);
  --color-surface: var(--gray-900);
  --color-text: var(--gray-50);
  --color-text-secondary: var(--gray-400);
  --color-border: var(--gray-700);
}

/* High contrast theme */
[data-theme="high-contrast"] {
  --color-background: black;
  --color-surface: black;
  --color-text: white;
  --color-border: white;
}
```

### Brand Theming

```css
/* Default brand */
:root {
  --color-primary: var(--blue-600);
  --color-primary-hover: var(--blue-700);
  --color-primary-subtle: var(--blue-50);
}

/* Alternative brand */
[data-brand="alt"] {
  --color-primary: var(--purple-600);
  --color-primary-hover: var(--purple-700);
  --color-primary-subtle: var(--purple-50);
}
```

## Token Formats

### CSS Custom Properties

```css
:root {
  --color-primary: #3b82f6;
  --space-4: 16px;
  --font-sans: 'Inter', sans-serif;
}
```

### JSON Format (for tooling)

```json
{
  "color": {
    "primary": {
      "value": "#3b82f6",
      "type": "color"
    }
  },
  "space": {
    "4": {
      "value": "16px",
      "type": "dimension"
    }
  }
}
```

### Design Token Format (W3C Draft)

```json
{
  "$name": "Design System Tokens",
  "$description": "Core design tokens",
  "color": {
    "primary": {
      "$value": "#3b82f6",
      "$type": "color"
    }
  }
}
```

## Anti-Patterns

### Common Token Mistakes

**Skipping semantic layer:**
```css
/* Bad - primitives in components */
.button { background: var(--blue-600); }

/* Good - semantic tokens */
.button { background: var(--color-primary); }
```

**Inconsistent naming:**
```css
/* Bad - mixed conventions */
--primaryColor: blue;
--secondary_color: gray;
--text-Color: black;

/* Good - consistent naming */
--color-primary: blue;
--color-secondary: gray;
--color-text: black;
```

**Magic numbers:**
```css
/* Bad - arbitrary values */
.card { padding: 23px; border-radius: 7px; }

/* Good - tokens */
.card { padding: var(--space-6); border-radius: var(--radius-lg); }
```

**Over-tokenization:**
```css
/* Bad - too specific */
--card-header-title-font-size-on-mobile-landscape: 14px;

/* Good - reusable */
--heading-sm-size: 14px;
```

## Summary

Well-architected design tokens provide system-wide consistency:

| Principle | Implementation |
|-----------|----------------|
| **Three-tier system** | Primitive → Semantic → Component |
| **Clear naming** | category-property-variant-state |
| **Consistent scale** | Mathematical progressions |
| **Theme-ready** | Semantic tokens enable theming |
| **Single source** | One definition, multiple outputs |
| **Documentation** | Each token purpose documented |

**Key Guidelines:**
1. Never use raw values in components
2. Semantic tokens reference primitives
3. Component tokens reference semantics
4. Consistent naming conventions throughout
5. Design for theme switching
6. Document token purpose and usage

---

**When to use this skill:**
- Establishing design system foundations
- Creating token taxonomies
- Implementing theming systems
- Building design-to-code workflows
- Auditing token architecture


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

