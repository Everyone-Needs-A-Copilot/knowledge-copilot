---
last_updated: 2026-02-25
status: active
name: design-tokens
description: Design system foundations - tokens, CSS variables, theming, scales. Use when building design systems.
triggers:
  files: ["**/tokens/**", "**/design-system/**", "**/theme.*", "**/variables.css"]
  keywords: ["design token", "CSS variable", "theme", "design system", "spacing scale", "typography scale", "color token"]
allowed-tools: Read, Write, Edit
---

# Design Tokens Deep Expertise

## Overview

Design tokens are the atomic design decisions that form the foundation of a design system. They encode visual design attributes (colors, spacing, typography, etc.) as data that can be transformed for multiple platforms, enabling consistency, scalability, and maintainability across digital products.

**Core Principle**: Design tokens create a single source of truth for design decisions that can be consumed by designers (Figma), developers (CSS/JS), and platforms (iOS, Android, Web).


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Token Philosophy

### What Are Design Tokens?

Design tokens are named entities that store visual design attributes. Rather than hardcoding values like `#3B82F6` or `16px`, tokens provide semantic names like `color-primary-500` or `space-4`.

**Key Properties:**
- **Named**: Semantic identifiers that convey meaning
- **Typed**: Categorized by their purpose (color, spacing, etc.)
- **Hierarchical**: Organized in tiers from primitive to semantic to component-specific
- **Platform-agnostic**: Can be transformed for any target (CSS, iOS, Android, etc.)
- **Versioned**: Treated as product features with change management

### Why Design Tokens Matter

**For Design:**
- Consistency across touchpoints
- Faster design iterations
- Clear design language
- Scalable design systems

**For Engineering:**
- Single source of truth
- Type-safe design values
- Easy theme switching
- Reduced technical debt
- Platform portability

**For Product:**
- Brand consistency
- Accessibility compliance
- Faster feature development
- Easier rebranding

## Token Architecture

### Three-Tier Token System

The most maintainable token architecture uses three tiers:

#### 1. Primitive Tokens (Raw Values)

The foundation - absolute values without semantic meaning:

```css
/* primitives/colors.css */
:root {
  /* Base palette */
  --color-blue-50: #eff6ff;
  --color-blue-100: #dbeafe;
  --color-blue-200: #bfdbfe;
  --color-blue-300: #93c5fd;
  --color-blue-400: #60a5fa;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;
  --color-blue-800: #1e40af;
  --color-blue-900: #1e3a8a;
  --color-blue-950: #172554;

  /* Gray palette */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
  --color-gray-950: #030712;

  /* Spacing scale */
  --space-0: 0;
  --space-1: 0.25rem;    /* 4px */
  --space-2: 0.5rem;     /* 8px */
  --space-3: 0.75rem;    /* 12px */
  --space-4: 1rem;       /* 16px */
  --space-5: 1.25rem;    /* 20px */
  --space-6: 1.5rem;     /* 24px */
  --space-8: 2rem;       /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */
  --space-32: 8rem;      /* 128px */

  /* Font sizes */
  --font-size-xs: 0.75rem;      /* 12px */
  --font-size-sm: 0.875rem;     /* 14px */
  --font-size-base: 1rem;       /* 16px */
  --font-size-lg: 1.125rem;     /* 18px */
  --font-size-xl: 1.25rem;      /* 20px */
  --font-size-2xl: 1.5rem;      /* 24px */
  --font-size-3xl: 1.875rem;    /* 30px */
  --font-size-4xl: 2.25rem;     /* 36px */
  --font-size-5xl: 3rem;        /* 48px */
  --font-size-6xl: 3.75rem;     /* 60px */
}
```

**Rules for Primitives:**
- Never reference other tokens
- Use absolute values only
- Follow consistent scales (4px for spacing, Tailwind palette for colors)
- Document the scale system

#### 2. Semantic Tokens (Purpose-Driven)

Map primitives to intent and context:

```css
/* semantic/colors.css */
:root {
  /* Brand colors */
  --color-primary: var(--color-blue-600);
  --color-primary-hover: var(--color-blue-700);
  --color-primary-active: var(--color-blue-800);

  /* Status colors */
  --color-success: var(--color-green-600);
  --color-success-light: var(--color-green-50);
  --color-success-dark: var(--color-green-700);

  --color-warning: var(--color-yellow-500);
  --color-warning-light: var(--color-yellow-50);
  --color-warning-dark: var(--color-yellow-600);

  --color-danger: var(--color-red-600);
  --color-danger-light: var(--color-red-50);
  --color-danger-dark: var(--color-red-700);

  --color-info: var(--color-blue-500);
  --color-info-light: var(--color-blue-50);
  --color-info-dark: var(--color-blue-600);

  /* Surface colors */
  --color-background: white;
  --color-background-secondary: var(--color-gray-50);
  --color-background-tertiary: var(--color-gray-100);

  --color-surface: white;
  --color-surface-raised: white;
  --color-surface-overlay: white;

  /* Border colors */
  --color-border-default: var(--color-gray-200);
  --color-border-strong: var(--color-gray-300);
  --color-border-subtle: var(--color-gray-100);

  /* Text colors */
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-text-tertiary: var(--color-gray-500);
  --color-text-disabled: var(--color-gray-400);
  --color-text-inverse: white;

  /* Interactive colors */
  --color-interactive-default: var(--color-primary);
  --color-interactive-hover: var(--color-primary-hover);
  --color-interactive-active: var(--color-primary-active);
  --color-interactive-disabled: var(--color-gray-300);
}

/* semantic/spacing.css */
:root {
  /* Layout spacing */
  --space-layout-xs: var(--space-4);      /* 16px */
  --space-layout-sm: var(--space-6);      /* 24px */
  --space-layout-md: var(--space-8);      /* 32px */
  --space-layout-lg: var(--space-12);     /* 48px */
  --space-layout-xl: var(--space-16);     /* 64px */

  /* Component spacing */
  --space-component-xs: var(--space-1);   /* 4px */
  --space-component-sm: var(--space-2);   /* 8px */
  --space-component-md: var(--space-3);   /* 12px */
  --space-component-lg: var(--space-4);   /* 16px */
  --space-component-xl: var(--space-6);   /* 24px */

  /* Inline spacing (padding/gap within components) */
  --space-inline-xs: var(--space-1);
  --space-inline-sm: var(--space-2);
  --space-inline-md: var(--space-3);
  --space-inline-lg: var(--space-4);

  /* Stack spacing (vertical rhythm) */
  --space-stack-xs: var(--space-2);
  --space-stack-sm: var(--space-4);
  --space-stack-md: var(--space-6);
  --space-stack-lg: var(--space-8);
  --space-stack-xl: var(--space-12);
}

/* semantic/typography.css */
:root {
  /* Heading scale */
  --font-heading-xl: var(--font-size-4xl);
  --font-heading-lg: var(--font-size-3xl);
  --font-heading-md: var(--font-size-2xl);
  --font-heading-sm: var(--font-size-xl);
  --font-heading-xs: var(--font-size-lg);

  /* Body text */
  --font-body-lg: var(--font-size-lg);
  --font-body-md: var(--font-size-base);
  --font-body-sm: var(--font-size-sm);
  --font-body-xs: var(--font-size-xs);

  /* Line heights */
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* Font weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Font families */
  --font-family-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-family-serif: Georgia, Cambria, "Times New Roman", Times, serif;
  --font-family-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}
```

**Rules for Semantic Tokens:**
- Always reference primitive tokens
- Name by purpose, not appearance
- Group by domain (color-text-*, color-border-*, etc.)
- Support multiple themes by mapping to different primitives

#### 3. Component Tokens (Context-Specific)

Tokens specific to component implementation:

```css
/* components/button.css */
:root {
  /* Button spacing */
  --button-padding-y-sm: var(--space-inline-sm);
  --button-padding-x-sm: var(--space-inline-md);
  --button-padding-y-md: var(--space-inline-md);
  --button-padding-x-md: var(--space-inline-lg);
  --button-padding-y-lg: var(--space-inline-lg);
  --button-padding-x-lg: var(--space-component-lg);

  /* Button colors - primary */
  --button-primary-bg: var(--color-interactive-default);
  --button-primary-bg-hover: var(--color-interactive-hover);
  --button-primary-bg-active: var(--color-interactive-active);
  --button-primary-text: var(--color-text-inverse);
  --button-primary-border: transparent;

  /* Button colors - secondary */
  --button-secondary-bg: transparent;
  --button-secondary-bg-hover: var(--color-background-secondary);
  --button-secondary-bg-active: var(--color-background-tertiary);
  --button-secondary-text: var(--color-text-primary);
  --button-secondary-border: var(--color-border-default);

  /* Button typography */
  --button-font-size-sm: var(--font-body-sm);
  --button-font-size-md: var(--font-body-md);
  --button-font-size-lg: var(--font-body-lg);
  --button-font-weight: var(--font-weight-medium);

  /* Button radius */
  --button-radius: var(--radius-md);

  /* Button transitions */
  --button-transition: all var(--duration-fast) var(--easing-standard);
}

/* components/input.css */
:root {
  /* Input spacing */
  --input-padding-y: var(--space-inline-sm);
  --input-padding-x: var(--space-inline-md);
  --input-gap: var(--space-inline-sm);

  /* Input colors */
  --input-bg: var(--color-background);
  --input-bg-disabled: var(--color-background-secondary);
  --input-border: var(--color-border-default);
  --input-border-hover: var(--color-border-strong);
  --input-border-focus: var(--color-interactive-default);
  --input-border-error: var(--color-danger);
  --input-text: var(--color-text-primary);
  --input-text-placeholder: var(--color-text-tertiary);

  /* Input sizing */
  --input-height-sm: 2rem;
  --input-height-md: 2.5rem;
  --input-height-lg: 3rem;

  /* Input typography */
  --input-font-size: var(--font-body-md);

  /* Input radius */
  --input-radius: var(--radius-md);
}
```

**Rules for Component Tokens:**
- Reference semantic tokens preferentially
- Only create when component needs unique values
- Scope naming to component (--button-*, --input-*)
- Document component variants

## Token Types

### Color Tokens

Colors are the most complex token category, requiring careful organization:

#### Color Palette Structure

```css
/* Palette: Base colors in 50-950 scale */
:root {
  /* Primary palette (brand) */
  --color-brand-50: #eff6ff;
  --color-brand-100: #dbeafe;
  --color-brand-200: #bfdbfe;
  --color-brand-300: #93c5fd;
  --color-brand-400: #60a5fa;
  --color-brand-500: #3b82f6;  /* Base brand color */
  --color-brand-600: #2563eb;
  --color-brand-700: #1d4ed8;
  --color-brand-800: #1e40af;
  --color-brand-900: #1e3a8a;
  --color-brand-950: #172554;

  /* Neutral palette (grays) */
  /* Use for text, borders, backgrounds */

  /* Accent palette (secondary brand) */
  /* Use for highlights, CTAs, special features */

  /* Semantic palettes */
  --color-success-50: /* ... */;
  --color-success-500: /* base */;
  --color-success-900: /* ... */;

  --color-error-50: /* ... */;
  --color-error-500: /* base */;
  --color-error-900: /* ... */;

  --color-warning-50: /* ... */;
  --color-warning-500: /* base */;
  --color-warning-900: /* ... */;

  --color-info-50: /* ... */;
  --color-info-500: /* base */;
  --color-info-900: /* ... */;
}
```

#### Color Usage Tokens

Map palette to UI purposes:

```css
:root {
  /* Text colors */
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-text-tertiary: var(--color-gray-500);
  --color-text-disabled: var(--color-gray-400);
  --color-text-inverse: white;
  --color-text-link: var(--color-brand-600);
  --color-text-link-hover: var(--color-brand-700);
  --color-text-success: var(--color-success-700);
  --color-text-error: var(--color-error-700);
  --color-text-warning: var(--color-warning-700);

  /* Background colors */
  --color-bg-primary: white;
  --color-bg-secondary: var(--color-gray-50);
  --color-bg-tertiary: var(--color-gray-100);
  --color-bg-inverse: var(--color-gray-900);
  --color-bg-brand: var(--color-brand-600);
  --color-bg-success: var(--color-success-50);
  --color-bg-error: var(--color-error-50);
  --color-bg-warning: var(--color-warning-50);
  --color-bg-info: var(--color-info-50);

  /* Border colors */
  --color-border-default: var(--color-gray-200);
  --color-border-strong: var(--color-gray-300);
  --color-border-subtle: var(--color-gray-100);
  --color-border-inverse: var(--color-gray-700);
  --color-border-brand: var(--color-brand-600);
  --color-border-success: var(--color-success-300);
  --color-border-error: var(--color-error-300);
  --color-border-warning: var(--color-warning-300);
  --color-border-focus: var(--color-brand-500);

  /* Interactive colors */
  --color-action-primary-default: var(--color-brand-600);
  --color-action-primary-hover: var(--color-brand-700);
  --color-action-primary-active: var(--color-brand-800);
  --color-action-primary-disabled: var(--color-gray-300);

  /* Surface colors (cards, modals, panels) */
  --color-surface-default: white;
  --color-surface-raised: white;
  --color-surface-overlay: white;
  --color-surface-sunken: var(--color-gray-50);
}
```

#### Color Accessibility

Ensure WCAG compliance:

```css
:root {
  /* Text on light backgrounds - minimum AA contrast */
  --color-text-aa-on-light: var(--color-gray-700);    /* 4.5:1 */
  --color-text-aaa-on-light: var(--color-gray-900);   /* 7:1 */

  /* Text on dark backgrounds */
  --color-text-aa-on-dark: var(--color-gray-200);
  --color-text-aaa-on-dark: white;

  /* Interactive minimum touch targets */
  --color-interactive-area-min: 44px; /* iOS guideline */
}
```

### Spacing Tokens

Spacing creates visual rhythm and hierarchy:

#### Spacing Scale

Use a consistent mathematical scale (commonly 4px base):

```css
:root {
  /* Base scale (4px increments) */
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
  --space-32: 8rem;     /* 128px */
  --space-40: 10rem;    /* 160px */
  --space-48: 12rem;    /* 192px */
  --space-56: 14rem;    /* 224px */
  --space-64: 16rem;    /* 256px */

  /* Negative space (for negative margins) */
  --space-n-1: calc(var(--space-1) * -1);
  --space-n-2: calc(var(--space-2) * -1);
  --space-n-3: calc(var(--space-3) * -1);
  --space-n-4: calc(var(--space-4) * -1);
  --space-n-6: calc(var(--space-6) * -1);
  --space-n-8: calc(var(--space-8) * -1);
}
```

#### Spacing Usage Patterns

Create semantic spacing for different contexts:

```css
:root {
  /* Inset spacing (padding inside elements) */
  --space-inset-xs: var(--space-1);
  --space-inset-sm: var(--space-2);
  --space-inset-md: var(--space-3);
  --space-inset-lg: var(--space-4);
  --space-inset-xl: var(--space-6);

  /* Squish inset (less vertical, more horizontal) */
  --space-inset-squish-sm: var(--space-1) var(--space-2);
  --space-inset-squish-md: var(--space-2) var(--space-3);
  --space-inset-squish-lg: var(--space-3) var(--space-4);

  /* Stretch inset (more vertical, less horizontal) */
  --space-inset-stretch-sm: var(--space-2) var(--space-1);
  --space-inset-stretch-md: var(--space-3) var(--space-2);
  --space-inset-stretch-lg: var(--space-4) var(--space-3);

  /* Stack spacing (vertical gaps between elements) */
  --space-stack-xs: var(--space-2);
  --space-stack-sm: var(--space-4);
  --space-stack-md: var(--space-6);
  --space-stack-lg: var(--space-8);
  --space-stack-xl: var(--space-12);
  --space-stack-2xl: var(--space-16);

  /* Inline spacing (horizontal gaps) */
  --space-inline-xs: var(--space-1);
  --space-inline-sm: var(--space-2);
  --space-inline-md: var(--space-3);
  --space-inline-lg: var(--space-4);
  --space-inline-xl: var(--space-6);

  /* Layout spacing (page sections, grids) */
  --space-layout-xs: var(--space-8);
  --space-layout-sm: var(--space-12);
  --space-layout-md: var(--space-16);
  --space-layout-lg: var(--space-24);
  --space-layout-xl: var(--space-32);
}
```

### Typography Tokens

Typography establishes visual hierarchy and readability:

#### Font Size Scale

```css
:root {
  /* Display sizes (marketing, heroes) */
  --font-size-display-2xl: 4.5rem;    /* 72px */
  --font-size-display-xl: 3.75rem;    /* 60px */
  --font-size-display-lg: 3rem;       /* 48px */
  --font-size-display-md: 2.25rem;    /* 36px */
  --font-size-display-sm: 1.875rem;   /* 30px */

  /* Heading sizes */
  --font-size-heading-xl: 2.25rem;    /* 36px - h1 */
  --font-size-heading-lg: 1.875rem;   /* 30px - h2 */
  --font-size-heading-md: 1.5rem;     /* 24px - h3 */
  --font-size-heading-sm: 1.25rem;    /* 20px - h4 */
  --font-size-heading-xs: 1.125rem;   /* 18px - h5 */

  /* Body sizes */
  --font-size-body-xl: 1.25rem;       /* 20px */
  --font-size-body-lg: 1.125rem;      /* 18px */
  --font-size-body-md: 1rem;          /* 16px */
  --font-size-body-sm: 0.875rem;      /* 14px */
  --font-size-body-xs: 0.75rem;       /* 12px */

  /* Utility sizes */
  --font-size-caption: 0.75rem;       /* 12px */
  --font-size-overline: 0.625rem;     /* 10px */
}
```

#### Font Weight Scale

```css
:root {
  --font-weight-thin: 100;
  --font-weight-extralight: 200;
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
  --font-weight-black: 900;

  /* Semantic weights */
  --font-weight-body: var(--font-weight-normal);
  --font-weight-heading: var(--font-weight-semibold);
  --font-weight-emphasis: var(--font-weight-medium);
  --font-weight-strong: var(--font-weight-bold);
}
```

#### Line Height Scale

```css
:root {
  /* Absolute line heights */
  --line-height-none: 1;
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* Usage-based line heights */
  --line-height-heading: var(--line-height-tight);
  --line-height-body: var(--line-height-normal);
  --line-height-caption: var(--line-height-snug);
}
```

#### Font Families

```css
:root {
  /* System font stacks */
  --font-family-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                      "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji",
                      "Segoe UI Emoji", "Segoe UI Symbol";

  --font-family-serif: Georgia, Cambria, "Times New Roman", Times, serif;

  --font-family-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
                      "Liberation Mono", "Courier New", monospace;

  /* Brand fonts (loaded via @font-face) */
  --font-family-brand-sans: "Inter", var(--font-family-sans);
  --font-family-brand-serif: "Merriweather", var(--font-family-serif);
  --font-family-brand-mono: "JetBrains Mono", var(--font-family-mono);

  /* Semantic usage */
  --font-family-heading: var(--font-family-brand-sans);
  --font-family-body: var(--font-family-sans);
  --font-family-code: var(--font-family-mono);
}
```

#### Typography Compositions

Combine multiple typography tokens:

```css
:root {
  /* Heading compositions */
  --typography-h1: var(--font-weight-heading) var(--font-size-heading-xl) / var(--line-height-heading) var(--font-family-heading);
  --typography-h2: var(--font-weight-heading) var(--font-size-heading-lg) / var(--line-height-heading) var(--font-family-heading);
  --typography-h3: var(--font-weight-heading) var(--font-size-heading-md) / var(--line-height-heading) var(--font-family-heading);
  --typography-h4: var(--font-weight-heading) var(--font-size-heading-sm) / var(--line-height-heading) var(--font-family-heading);

  /* Body compositions */
  --typography-body-lg: var(--font-weight-body) var(--font-size-body-lg) / var(--line-height-body) var(--font-family-body);
  --typography-body-md: var(--font-weight-body) var(--font-size-body-md) / var(--line-height-body) var(--font-family-body);
  --typography-body-sm: var(--font-weight-body) var(--font-size-body-sm) / var(--line-height-body) var(--font-family-body);

  /* Utility compositions */
  --typography-caption: var(--font-weight-body) var(--font-size-caption) / var(--line-height-caption) var(--font-family-body);
  --typography-overline: var(--font-weight-semibold) var(--font-size-overline) / var(--line-height-tight) var(--font-family-body);
  --typography-code: var(--font-weight-normal) var(--font-size-body-sm) / var(--line-height-normal) var(--font-family-code);
}
```

### Shadow Tokens

Shadows create depth and hierarchy:

```css
:root {
  /* Shadow elevations */
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
  --shadow-none: 0 0 #0000;

  /* Semantic shadows */
  --shadow-card: var(--shadow-sm);
  --shadow-card-hover: var(--shadow-md);
  --shadow-dropdown: var(--shadow-lg);
  --shadow-modal: var(--shadow-xl);
  --shadow-popover: var(--shadow-md);
  --shadow-tooltip: var(--shadow-sm);

  /* Focus shadow */
  --shadow-focus: 0 0 0 3px var(--color-brand-200);
  --shadow-focus-error: 0 0 0 3px var(--color-error-200);
}
```

### Border Radius Tokens

Radius defines the softness of UI elements:

```css
:root {
  /* Radius scale */
  --radius-none: 0;
  --radius-sm: 0.125rem;    /* 2px */
  --radius-md: 0.25rem;     /* 4px */
  --radius-lg: 0.375rem;    /* 6px */
  --radius-xl: 0.5rem;      /* 8px */
  --radius-2xl: 0.75rem;    /* 12px */
  --radius-3xl: 1rem;       /* 16px */
  --radius-4xl: 1.5rem;     /* 24px */
  --radius-full: 9999px;
  --radius-circle: 50%;

  /* Semantic radius */
  --radius-button: var(--radius-md);
  --radius-input: var(--radius-md);
  --radius-card: var(--radius-lg);
  --radius-modal: var(--radius-xl);
  --radius-avatar: var(--radius-full);
  --radius-badge: var(--radius-full);
  --radius-pill: var(--radius-full);
}
```

### Animation Tokens

Motion creates delight and feedback:

#### Duration Tokens

```css
:root {
  /* Duration scale */
  --duration-instant: 0ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 400ms;
  --duration-slowest: 500ms;

  /* Semantic durations */
  --duration-tooltip: var(--duration-fast);
  --duration-popover: var(--duration-normal);
  --duration-modal: var(--duration-slow);
  --duration-drawer: var(--duration-slower);
  --duration-page-transition: var(--duration-slowest);
}
```

#### Easing Tokens

```css
:root {
  /* Easing curves */
  --easing-linear: linear;
  --easing-ease: ease;
  --easing-ease-in: ease-in;
  --easing-ease-out: ease-out;
  --easing-ease-in-out: ease-in-out;

  /* Custom cubic bezier */
  --easing-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
  --easing-emphasized: cubic-bezier(0.4, 0.0, 0.6, 1);
  --easing-decelerated: cubic-bezier(0.0, 0.0, 0.2, 1);
  --easing-accelerated: cubic-bezier(0.4, 0.0, 1, 1);
  --easing-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --easing-smooth: cubic-bezier(0.25, 0.46, 0.45, 0.94);

  /* Semantic easing */
  --easing-default: var(--easing-standard);
  --easing-enter: var(--easing-decelerated);
  --easing-exit: var(--easing-accelerated);
}
```

#### Transition Tokens

```css
:root {
  /* Common transitions */
  --transition-colors: color var(--duration-normal) var(--easing-default),
                       background-color var(--duration-normal) var(--easing-default),
                       border-color var(--duration-normal) var(--easing-default);

  --transition-opacity: opacity var(--duration-normal) var(--easing-default);

  --transition-transform: transform var(--duration-normal) var(--easing-default);

  --transition-all: all var(--duration-normal) var(--easing-default);

  --transition-shadow: box-shadow var(--duration-normal) var(--easing-default);

  /* Component transitions */
  --transition-button: var(--transition-colors), var(--transition-shadow);
  --transition-link: color var(--duration-fast) var(--easing-default);
  --transition-card: transform var(--duration-normal) var(--easing-default),
                     box-shadow var(--duration-normal) var(--easing-default);
}
```

### Z-Index Tokens

Layering creates stacking context:

```css
:root {
  /* Z-index scale */
  --z-index-base: 0;
  --z-index-dropdown: 1000;
  --z-index-sticky: 1100;
  --z-index-fixed: 1200;
  --z-index-modal-backdrop: 1300;
  --z-index-modal: 1400;
  --z-index-popover: 1500;
  --z-index-tooltip: 1600;
  --z-index-notification: 1700;
  --z-index-max: 9999;

  /* Semantic z-index */
  --z-index-header: var(--z-index-sticky);
  --z-index-sidebar: var(--z-index-sticky);
  --z-index-overlay: var(--z-index-modal-backdrop);
  --z-index-dialog: var(--z-index-modal);
}
```

## Theming

### Dark Mode Implementation

Create theme-aware tokens using CSS custom properties:

```css
/* tokens/themes.css */

/* Light theme (default) */
:root {
  --color-bg-primary: white;
  --color-bg-secondary: var(--color-gray-50);
  --color-bg-tertiary: var(--color-gray-100);

  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-text-tertiary: var(--color-gray-500);

  --color-border-default: var(--color-gray-200);
  --color-border-strong: var(--color-gray-300);

  --shadow-card: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

/* Dark theme */
[data-theme="dark"] {
  --color-bg-primary: var(--color-gray-900);
  --color-bg-secondary: var(--color-gray-800);
  --color-bg-tertiary: var(--color-gray-700);

  --color-text-primary: var(--color-gray-50);
  --color-text-secondary: var(--color-gray-300);
  --color-text-tertiary: var(--color-gray-400);

  --color-border-default: var(--color-gray-700);
  --color-border-strong: var(--color-gray-600);

  --shadow-card: 0 1px 3px 0 rgb(0 0 0 / 0.5);
}

/* System preference detection */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    --color-bg-primary: var(--color-gray-900);
    --color-bg-secondary: var(--color-gray-800);
    /* ... other dark mode values ... */
  }
}
```

### Theme Switching

```typescript
// theme-manager.ts
export type Theme = 'light' | 'dark' | 'system';

export class ThemeManager {
  private static instance: ThemeManager;
  private currentTheme: Theme = 'system';

  static getInstance(): ThemeManager {
    if (!ThemeManager.instance) {
      ThemeManager.instance = new ThemeManager();
    }
    return ThemeManager.instance;
  }

  setTheme(theme: Theme): void {
    this.currentTheme = theme;

    if (theme === 'system') {
      document.documentElement.removeAttribute('data-theme');
      this.applySystemTheme();
    } else {
      document.documentElement.setAttribute('data-theme', theme);
    }

    localStorage.setItem('theme', theme);
  }

  private applySystemTheme(): void {
    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const theme = darkModeQuery.matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
  }

  getTheme(): Theme {
    return this.currentTheme;
  }

  init(): void {
    const savedTheme = localStorage.getItem('theme') as Theme || 'system';
    this.setTheme(savedTheme);

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', () => {
        if (this.currentTheme === 'system') {
          this.applySystemTheme();
        }
      });
  }
}
```

### Multi-Brand Theming

Support multiple brands with token overrides:

```css
/* tokens/brands/brand-a.css */
:root[data-brand="brand-a"] {
  --color-brand-50: #fef3c7;
  --color-brand-500: #f59e0b;  /* Amber */
  --color-brand-900: #78350f;

  --color-primary: var(--color-brand-500);
  --font-family-heading: "Montserrat", var(--font-family-sans);
  --radius-button: var(--radius-xl);  /* Rounder buttons */
}

/* tokens/brands/brand-b.css */
:root[data-brand="brand-b"] {
  --color-brand-50: #f0fdf4;
  --color-brand-500: #10b981;  /* Emerald */
  --color-brand-900: #064e3b;

  --color-primary: var(--color-brand-500);
  --font-family-heading: "Poppins", var(--font-family-sans);
  --radius-button: var(--radius-sm);  /* Sharper buttons */
}
```

## Token Naming Conventions

### Standard Naming Pattern

Follow this hierarchy:

```
{category}-{property}-{variant}-{state}
```

**Examples:**
- `color-text-primary` (category: color, property: text, variant: primary)
- `color-bg-error-hover` (category: color, property: bg, variant: error, state: hover)
- `space-layout-md` (category: space, property: layout, variant: md)
- `button-primary-bg-hover` (category: button, property: primary-bg, state: hover)

### Category Prefixes

```css
/* Color tokens */
--color-*

/* Spacing tokens */
--space-*

/* Typography tokens */
--font-*
--line-height-*

/* Shadow tokens */
--shadow-*

/* Border tokens */
--border-*
--radius-*

/* Animation tokens */
--duration-*
--easing-*
--transition-*

/* Z-index tokens */
--z-index-*

/* Component tokens */
--button-*
--input-*
--card-*
/* etc. */
```

### Naming Best Practices

**DO:**
- Use semantic names: `--color-text-primary` not `--color-dark-gray`
- Be consistent: `--space-layout-md` not `--layout-spacing-medium`
- Use kebab-case: `--font-size-body-md`
- Include variant: `--button-primary-bg-hover`
- Group related tokens: all `--color-text-*` together

**DON'T:**
- Use visual descriptions: `--color-blue-button` (use `--button-primary-bg`)
- Mix naming patterns: `--spaceMd` and `--space-lg`
- Use abbreviations inconsistently: `--bg-primary` vs `--background-secondary`
- Create overly specific tokens: `--homepage-hero-button-text-color`

## Tailwind Integration

### Extending Tailwind Config

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Map CSS variables to Tailwind colors
        primary: {
          50: 'var(--color-brand-50)',
          100: 'var(--color-brand-100)',
          200: 'var(--color-brand-200)',
          300: 'var(--color-brand-300)',
          400: 'var(--color-brand-400)',
          500: 'var(--color-brand-500)',
          600: 'var(--color-brand-600)',
          700: 'var(--color-brand-700)',
          800: 'var(--color-brand-800)',
          900: 'var(--color-brand-900)',
          950: 'var(--color-brand-950)',
        },
        // Semantic colors
        background: {
          DEFAULT: 'var(--color-bg-primary)',
          secondary: 'var(--color-bg-secondary)',
          tertiary: 'var(--color-bg-tertiary)',
        },
        foreground: {
          DEFAULT: 'var(--color-text-primary)',
          secondary: 'var(--color-text-secondary)',
          tertiary: 'var(--color-text-tertiary)',
        },
        border: {
          DEFAULT: 'var(--color-border-default)',
          strong: 'var(--color-border-strong)',
        },
      },
      spacing: {
        // Map spacing tokens
        'layout-xs': 'var(--space-layout-xs)',
        'layout-sm': 'var(--space-layout-sm)',
        'layout-md': 'var(--space-layout-md)',
        'layout-lg': 'var(--space-layout-lg)',
        'layout-xl': 'var(--space-layout-xl)',
      },
      fontSize: {
        'display-2xl': ['var(--font-size-display-2xl)', { lineHeight: 'var(--line-height-tight)' }],
        'display-xl': ['var(--font-size-display-xl)', { lineHeight: 'var(--line-height-tight)' }],
        'heading-xl': ['var(--font-size-heading-xl)', { lineHeight: 'var(--line-height-heading)' }],
        'heading-lg': ['var(--font-size-heading-lg)', { lineHeight: 'var(--line-height-heading)' }],
        'body-lg': ['var(--font-size-body-lg)', { lineHeight: 'var(--line-height-body)' }],
        'body-md': ['var(--font-size-body-md)', { lineHeight: 'var(--line-height-body)' }],
        'body-sm': ['var(--font-size-body-sm)', { lineHeight: 'var(--line-height-body)' }],
      },
      fontFamily: {
        sans: ['var(--font-family-sans)'],
        serif: ['var(--font-family-serif)'],
        mono: ['var(--font-family-mono)'],
        heading: ['var(--font-family-heading)'],
      },
      boxShadow: {
        'card': 'var(--shadow-card)',
        'card-hover': 'var(--shadow-card-hover)',
        'dropdown': 'var(--shadow-dropdown)',
        'modal': 'var(--shadow-modal)',
      },
      borderRadius: {
        'button': 'var(--radius-button)',
        'input': 'var(--radius-input)',
        'card': 'var(--radius-card)',
        'modal': 'var(--radius-modal)',
      },
      transitionDuration: {
        'fast': 'var(--duration-fast)',
        'normal': 'var(--duration-normal)',
        'slow': 'var(--duration-slow)',
      },
      transitionTimingFunction: {
        'standard': 'var(--easing-standard)',
        'emphasized': 'var(--easing-emphasized)',
        'enter': 'var(--easing-enter)',
        'exit': 'var(--easing-exit)',
      },
    },
  },
  plugins: [],
};

export default config;
```

### Using Tailwind with Tokens

```tsx
// Button component with Tailwind + tokens
export function Button({ variant = 'primary', children }: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles using tokens via Tailwind
        'px-4 py-2 rounded-button font-medium',
        'transition-colors duration-fast',
        'focus:outline-none focus:ring-2 focus:ring-primary-500',

        // Variant styles
        variant === 'primary' && [
          'bg-primary-600 text-white',
          'hover:bg-primary-700',
          'active:bg-primary-800',
          'disabled:bg-gray-300',
        ],

        variant === 'secondary' && [
          'bg-transparent border border-border',
          'text-foreground',
          'hover:bg-background-secondary',
        ]
      )}
    >
      {children}
    </button>
  );
}
```

## Token Generation Tools

### Style Dictionary

Style Dictionary is the industry standard for token transformation:

```json
// config.json
{
  "source": ["tokens/**/*.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "dist/css/",
      "files": [{
        "destination": "variables.css",
        "format": "css/variables"
      }]
    },
    "js": {
      "transformGroup": "js",
      "buildPath": "dist/js/",
      "files": [{
        "destination": "tokens.js",
        "format": "javascript/es6"
      }]
    },
    "ios": {
      "transformGroup": "ios",
      "buildPath": "dist/ios/",
      "files": [{
        "destination": "Tokens.swift",
        "format": "ios-swift/class.swift"
      }]
    }
  }
}
```

```json
// tokens/color.json
{
  "color": {
    "brand": {
      "50": { "value": "#eff6ff" },
      "100": { "value": "#dbeafe" },
      "500": { "value": "#3b82f6" },
      "900": { "value": "#1e3a8a" }
    },
    "text": {
      "primary": { "value": "{color.gray.900}" },
      "secondary": { "value": "{color.gray.600}" }
    }
  }
}
```

Output CSS:

```css
:root {
  --color-brand-50: #eff6ff;
  --color-brand-100: #dbeafe;
  --color-brand-500: #3b82f6;
  --color-brand-900: #1e3a8a;
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
}
```

### Figma Tokens Plugin

Sync tokens between Figma and code:

1. Install Figma Tokens plugin
2. Define tokens in Figma
3. Export as JSON
4. Use Style Dictionary to transform
5. Import into codebase

**Workflow:**
```
Figma Design → Figma Tokens Plugin → JSON → Style Dictionary → CSS/JS/Platform
```

### Token Studio

Token Studio for Figma provides advanced token management:

- Token sets for themes
- Math operations (`{space.4} * 2`)
- Color modifications (`lighten({color.primary}, 20%)`)
- Token references (`{color.brand.500}`)

## Responsive Tokens

### Breakpoint-Based Tokens

```css
:root {
  /* Mobile first - default values */
  --space-layout-x: var(--space-4);
  --space-layout-y: var(--space-6);
  --font-size-hero: var(--font-size-3xl);
}

/* Tablet */
@media (min-width: 768px) {
  :root {
    --space-layout-x: var(--space-6);
    --space-layout-y: var(--space-8);
    --font-size-hero: var(--font-size-4xl);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  :root {
    --space-layout-x: var(--space-8);
    --space-layout-y: var(--space-12);
    --font-size-hero: var(--font-size-5xl);
  }
}

/* Large desktop */
@media (min-width: 1280px) {
  :root {
    --space-layout-x: var(--space-12);
    --space-layout-y: var(--space-16);
    --font-size-hero: var(--font-size-6xl);
  }
}
```

### Fluid Typography

Use CSS clamp for responsive type:

```css
:root {
  /* Fluid font sizes: min at 320px, max at 1280px */
  --font-size-fluid-sm: clamp(0.875rem, 0.8rem + 0.3vw, 1rem);
  --font-size-fluid-md: clamp(1rem, 0.9rem + 0.4vw, 1.25rem);
  --font-size-fluid-lg: clamp(1.25rem, 1.1rem + 0.6vw, 1.875rem);
  --font-size-fluid-xl: clamp(1.5rem, 1.2rem + 1vw, 2.5rem);
  --font-size-fluid-2xl: clamp(2rem, 1.5rem + 1.5vw, 3.5rem);

  /* Fluid spacing */
  --space-fluid-sm: clamp(1rem, 0.8rem + 0.5vw, 1.5rem);
  --space-fluid-md: clamp(2rem, 1.5rem + 1vw, 3rem);
  --space-fluid-lg: clamp(3rem, 2rem + 2vw, 5rem);
}
```

### Container Query Tokens

Tokens that respond to container size:

```css
.card {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    --card-padding: var(--space-6);
    --card-title-size: var(--font-size-xl);
  }
}

@container card (min-width: 600px) {
  .card {
    --card-padding: var(--space-8);
    --card-title-size: var(--font-size-2xl);
  }
}
```

## Token Documentation

### Documenting Token Purpose

```css
/**
 * COLOR TOKENS
 *
 * Color tokens are organized into three tiers:
 * 1. Primitives (--color-{hue}-{shade}): Raw palette values
 * 2. Semantic (--color-{purpose}-{variant}): Usage-based colors
 * 3. Component (--{component}-{property}-{state}): Component-specific
 *
 * Usage:
 * - Always prefer semantic tokens over primitives
 * - Use component tokens for component-specific styling
 * - Never hardcode color values
 *
 * @see https://design-system.example.com/tokens/colors
 */

/**
 * @token color-text-primary
 * @type color
 * @value {color.gray.900} (light) / {color.gray.50} (dark)
 * @description Primary text color for body content and headings
 * @wcag-aa Passes against --color-bg-primary
 */
--color-text-primary: var(--color-gray-900);

/**
 * @token space-layout-md
 * @type spacing
 * @value {space.8} (32px)
 * @description Medium layout spacing for section padding
 * @responsive Increases to {space.12} at tablet breakpoint
 */
--space-layout-md: var(--space-8);
```

### Token Showcase

Build a living style guide:

```tsx
// TokenShowcase.tsx
export function TokenShowcase() {
  return (
    <div className="space-y-12">
      {/* Colors */}
      <section>
        <h2>Color Tokens</h2>
        <div className="grid grid-cols-4 gap-4">
          <ColorSwatch
            token="--color-text-primary"
            value="var(--color-gray-900)"
            usage="Body text, headings"
          />
          <ColorSwatch
            token="--color-bg-primary"
            value="white"
            usage="Page background"
          />
        </div>
      </section>

      {/* Spacing */}
      <section>
        <h2>Spacing Tokens</h2>
        <div className="space-y-4">
          <SpacingDemo
            token="--space-layout-md"
            value="2rem (32px)"
            visual={<div style={{ width: 'var(--space-layout-md)' }} />}
          />
        </div>
      </section>

      {/* Typography */}
      <section>
        <h2>Typography Tokens</h2>
        <div className="space-y-4">
          <TypeDemo
            token="--typography-h1"
            sample="The quick brown fox"
          />
        </div>
      </section>
    </div>
  );
}
```

## Anti-Patterns

### DON'T: Hardcode Values

```css
/* ❌ BAD */
.button {
  padding: 12px 16px;
  background: #3b82f6;
  border-radius: 6px;
}

/* ✅ GOOD */
.button {
  padding: var(--button-padding-y-md) var(--button-padding-x-md);
  background: var(--button-primary-bg);
  border-radius: var(--radius-button);
}
```

### DON'T: Use Primitive Tokens Directly in Components

```css
/* ❌ BAD - component using primitive token */
.card {
  background: var(--color-gray-50);
  border: 1px solid var(--color-gray-200);
}

/* ✅ GOOD - component using semantic token */
.card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-default);
}
```

### DON'T: Create Overly Specific Tokens

```css
/* ❌ BAD - too specific */
--homepage-hero-cta-button-hover-background-color: #1d4ed8;

/* ✅ GOOD - appropriately scoped */
--button-primary-bg-hover: var(--color-primary-hover);
```

### DON'T: Mix Token Naming Conventions

```css
/* ❌ BAD - inconsistent naming */
--colorTextPrimary: #111;
--color-bg-primary: white;
--Color_Border_Default: #ccc;

/* ✅ GOOD - consistent kebab-case */
--color-text-primary: #111;
--color-bg-primary: white;
--color-border-default: #ccc;
```

### DON'T: Bypass Tokens with Inline Styles

```tsx
/* ❌ BAD */
<div style={{ padding: '16px', color: '#3b82f6' }}>
  Content
</div>

/* ✅ GOOD - use utility classes or CSS */
<div className="p-4 text-primary-600">
  Content
</div>
```

### DON'T: Create Single-Use Tokens

```css
/* ❌ BAD - token only used once */
--modal-backdrop-blur: 8px;

.modal-backdrop {
  backdrop-filter: blur(var(--modal-backdrop-blur));
}

/* ✅ GOOD - use semantic or reusable token */
--blur-md: 8px;  /* Can be used across components */

.modal-backdrop {
  backdrop-filter: blur(var(--blur-md));
}
```

### DON'T: Ignore Token Hierarchy

```css
/* ❌ BAD - semantic token referencing component token */
--color-primary: var(--button-bg);

/* ✅ GOOD - proper hierarchy */
--color-primary: var(--color-brand-600);  /* semantic → primitive */
--button-bg: var(--color-primary);         /* component → semantic */
```

## Token Maintenance

### Versioning Tokens

Treat tokens as a versioned API:

```json
// package.json
{
  "name": "@company/design-tokens",
  "version": "2.1.0",
  "description": "Design tokens for Company design system"
}
```

Use semantic versioning:
- **Major**: Breaking changes (removing tokens, changing token architecture)
- **Minor**: New tokens added
- **Patch**: Bug fixes, value adjustments

### Deprecating Tokens

Mark deprecated tokens clearly:

```css
/**
 * @deprecated Use --color-text-primary instead
 * @removed-in v3.0.0
 */
--text-color-main: var(--color-text-primary);
```

### Token Auditing

Regularly audit token usage:

```bash
# Find unused tokens
npx style-dictionary-utils audit --source tokens/ --target src/

# Find hardcoded values
npx hardcoded-values src/ --type color
npx hardcoded-values src/ --type spacing
```

### Migration Strategy

When updating tokens:

1. **Add new tokens** alongside old ones
2. **Mark old tokens deprecated** with migration path
3. **Update documentation** with migration guide
4. **Provide codemods** for automated migration
5. **Remove deprecated tokens** in next major version

```typescript
// codemod.ts - Automated token migration
export function migrateTokens(source: string): string {
  return source
    .replace(/--text-color-main/g, '--color-text-primary')
    .replace(/--bg-color-primary/g, '--color-bg-primary')
    .replace(/--spacing-md/g, '--space-layout-md');
}
```

## Best Practices Summary

1. **Three-tier architecture**: Primitives → Semantic → Component
2. **Semantic naming**: Name by purpose, not appearance
3. **Consistent conventions**: Use kebab-case, follow naming patterns
4. **Theme support**: Build for light/dark mode from day one
5. **Documentation**: Document token purpose and usage
6. **Tooling**: Use Style Dictionary for transformation
7. **Version control**: Treat tokens as a versioned API
8. **Accessibility**: Ensure WCAG compliance in color tokens
9. **Responsive**: Support fluid and breakpoint-based values
10. **Maintenance**: Regular audits and deprecation strategy

## Implementation Checklist

Starting a new design token system:

- [ ] Choose token architecture (three-tier recommended)
- [ ] Define naming conventions
- [ ] Create primitive tokens (colors, spacing, typography)
- [ ] Create semantic tokens
- [ ] Set up Style Dictionary or similar tool
- [ ] Integrate with CSS/Tailwind
- [ ] Build theme support (light/dark)
- [ ] Create token documentation
- [ ] Build living style guide
- [ ] Set up versioning strategy
- [ ] Create migration path for updates
- [ ] Add token auditing to CI/CD

## Resources

**Tools:**
- Style Dictionary: Token transformation platform
- Figma Tokens: Sync Figma and code
- Token Studio: Advanced Figma token management
- Theo (Salesforce): Token transformer

**Standards:**
- W3C Design Tokens Community Group
- Design Tokens Format Module (DTFM)

**Examples:**
- Material Design: material.io/design/color
- Apple HIG: developer.apple.com/design/human-interface-guidelines
- Carbon Design System: carbondesignsystem.com
- Tailwind CSS: tailwindcss.com/docs/customizing-colors

---

**Remember**: Design tokens are the foundation of a design system. Invest time in getting the architecture right, and the rest of the system will be more maintainable and scalable.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

