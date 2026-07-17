---
last_updated: 2026-02-25
status: active
name: visual-rhythm
description: Repetition, pattern, and tempo in visual design for coherent interfaces. Use when establishing design consistency.
triggers:
  files: ["**/layout.*", "**/design-system/**", "**/spacing.*", "**/grid.*"]
  keywords: ["visual rhythm", "repetition", "pattern", "tempo", "cadence", "visual flow", "design consistency"]
allowed-tools: Read, Write, Edit
---

# Visual Rhythm: Deep Expertise Skill

Creating cohesive, scannable interfaces through deliberate repetition, pattern, and visual tempo.

## Understanding Visual Rhythm

Visual rhythm is the recurrence of visual elements that creates a sense of organized movement and predictability. Like musical rhythm, visual rhythm establishes patterns that guide users through an interface.

### Why Rhythm Matters

**Cognitive Benefits:**
- Reduces mental effort by creating expectations
- Enables faster scanning and comprehension
- Provides visual anchors for navigation
- Creates professional, polished appearance

**User Experience Benefits:**
- Predictable interaction patterns
- Easier content consumption
- Increased trust through consistency
- Reduced learning curve


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Types of Visual Rhythm

### 1. Regular Rhythm

**Definition**: Identical elements repeated at equal intervals.

**Characteristics:**
- Uniform spacing
- Consistent sizing
- Predictable pattern

**UI Applications:**

| Element | Example |
|---------|---------|
| Grids | Equal-width columns |
| Lists | Consistent item spacing |
| Navigation | Evenly spaced tabs |
| Cards | Uniform card sizes |

**Implementation:**

```css
/* Regular grid rhythm */
.grid-regular {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Regular list rhythm */
.list-regular {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.list-regular .item {
  padding: 16px;
  border-bottom: 1px solid var(--color-border);
}
```

### 2. Alternating Rhythm

**Definition**: Two or more elements alternating in sequence (ABABAB).

**Characteristics:**
- Predictable variation
- Visual interest
- Clear differentiation

**UI Applications:**

| Element | Example |
|---------|---------|
| Tables | Zebra striping |
| Layouts | Left-right alternation |
| Sections | Background color alternation |

**Implementation:**

```css
/* Alternating table rows */
.table-row:nth-child(even) {
  background: var(--color-gray-50);
}

/* Alternating content sections */
.section:nth-child(odd) {
  background: white;
}

.section:nth-child(even) {
  background: var(--color-gray-50);
}

/* Alternating feature layout */
.feature:nth-child(odd) {
  flex-direction: row;
}

.feature:nth-child(even) {
  flex-direction: row-reverse;
}
```

### 3. Progressive Rhythm

**Definition**: Elements that gradually change in a consistent direction.

**Characteristics:**
- Smooth transitions
- Builds momentum
- Creates hierarchy

**UI Applications:**

| Element | Example |
|---------|---------|
| Typography | Size hierarchy (H1→H6) |
| Spacing | Increasing margins |
| Animation | Staggered timing |
| Loading | Progressive reveals |

**Implementation:**

```css
/* Progressive typography */
.heading-xl { font-size: 3rem; }
.heading-lg { font-size: 2.25rem; }
.heading-md { font-size: 1.5rem; }
.heading-sm { font-size: 1.25rem; }
.heading-xs { font-size: 1rem; }

/* Progressive spacing */
.section-hero { padding: 6rem 0; }
.section-primary { padding: 4rem 0; }
.section-secondary { padding: 3rem 0; }
.section-tertiary { padding: 2rem 0; }

/* Progressive animation delay */
.stagger-item {
  opacity: 0;
  animation: fadeIn 0.3s ease-out forwards;
}

.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 75ms; }
.stagger-item:nth-child(3) { animation-delay: 150ms; }
.stagger-item:nth-child(4) { animation-delay: 225ms; }
```

### 4. Flowing Rhythm

**Definition**: Organic, varied patterns that maintain visual continuity.

**Characteristics:**
- Natural variation
- Avoids monotony
- Maintains coherence

**UI Applications:**

| Element | Example |
|---------|---------|
| Masonry layouts | Pinterest-style grids |
| Content feeds | Variable card heights |
| Organic designs | Nature-inspired layouts |

**Implementation:**

```css
/* Masonry rhythm */
.masonry {
  columns: 3;
  column-gap: 24px;
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: 24px;
}

/* Variable card heights with consistent width */
.cards-flowing {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.card {
  /* Height varies with content */
  min-height: 200px;
}
```

## Creating Rhythm with Spacing

### The Spacing Scale

A mathematical spacing scale creates consistent rhythm:

```css
:root {
  /* Base unit: 4px */
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
}
```

### Vertical Rhythm

Consistent vertical spacing creates readable, scannable content:

```css
/* Establish baseline rhythm */
:root {
  --baseline: 1.5rem; /* 24px baseline grid */
}

/* All elements align to baseline */
.prose {
  line-height: var(--baseline);
}

.prose p {
  margin-bottom: var(--baseline);
}

.prose h2 {
  margin-top: calc(var(--baseline) * 2);
  margin-bottom: var(--baseline);
  line-height: calc(var(--baseline) * 1.5);
}

.prose h3 {
  margin-top: calc(var(--baseline) * 1.5);
  margin-bottom: calc(var(--baseline) * 0.5);
  line-height: var(--baseline);
}
```

### Horizontal Rhythm

Grid systems establish horizontal rhythm:

```css
/* 12-column grid with consistent gutters */
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-6); /* Consistent gutter */
  padding: 0 var(--space-6);
}

/* Content aligns to grid */
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-8 { grid-column: span 8; }
.col-12 { grid-column: span 12; }
```

## Creating Rhythm with Repetition

### Component Repetition

Consistent component patterns establish interface rhythm:

```css
/* Repeated card pattern */
.card {
  background: white;
  border-radius: 12px;
  padding: var(--space-6);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: var(--space-2);
}

.card-content {
  color: var(--color-text-secondary);
  line-height: 1.6;
}

/* Every card follows the same rhythm */
```

### Visual Element Repetition

Recurring visual elements create pattern recognition:

```css
/* Consistent icon treatment */
.icon {
  width: 24px;
  height: 24px;
  color: var(--color-gray-600);
}

.icon-sm { width: 16px; height: 16px; }
.icon-lg { width: 32px; height: 32px; }

/* Consistent badge treatment */
.badge {
  display: inline-flex;
  padding: var(--space-1) var(--space-2);
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
}

/* Consistent button treatment */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
}
```

## Rhythm in Content Layout

### Section Rhythm

Consistent section structure creates predictable page flow:

```css
/* Section rhythm pattern */
.section {
  padding: var(--space-16) 0;
}

.section-header {
  text-align: center;
  max-width: 600px;
  margin: 0 auto var(--space-12);
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: var(--space-4);
}

.section-subtitle {
  font-size: 1.25rem;
  color: var(--color-text-secondary);
}

.section-content {
  /* Content follows header with consistent spacing */
}
```

### List Rhythm

Consistent list patterns aid scanning:

```css
/* Standard list rhythm */
.list {
  display: flex;
  flex-direction: column;
}

.list-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  border-bottom: 1px solid var(--color-border);
}

.list-item:last-child {
  border-bottom: none;
}

/* Consistent internal structure */
.list-item-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
}

.list-item-content {
  flex: 1;
  min-width: 0;
}

.list-item-action {
  flex-shrink: 0;
}
```

## Rhythm and Hierarchy

### Visual Weight Distribution

Rhythm helps establish and reinforce hierarchy:

```css
/* Primary elements - heavy, prominent */
.primary {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

/* Secondary elements - medium weight */
.secondary {
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

/* Tertiary elements - light weight */
.tertiary {
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--color-text-tertiary);
  margin-bottom: var(--space-2);
}
```

### Emphasis Through Rhythm Break

Breaking rhythm creates emphasis:

```css
/* Regular item rhythm */
.item {
  padding: var(--space-4);
  background: white;
}

/* Featured item breaks rhythm */
.item.featured {
  padding: var(--space-6);
  background: var(--color-primary-50);
  border: 2px solid var(--color-primary-200);
  border-radius: 12px;
}
```

## Temporal Rhythm (Animation)

### Consistent Timing

Animation timing creates temporal rhythm:

```css
:root {
  /* Duration scale */
  --duration-instant: 50ms;
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;

  /* Consistent easing */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
}

/* Apply consistent timing */
.transition-colors {
  transition: color var(--duration-fast) var(--ease-default),
              background-color var(--duration-fast) var(--ease-default);
}

.transition-transform {
  transition: transform var(--duration-normal) var(--ease-out);
}
```

### Staggered Animations

Staggered timing creates progressive rhythm:

```css
/* Stagger entrance animations */
.stagger-container .item {
  opacity: 0;
  transform: translateY(20px);
  animation: slideUp var(--duration-normal) var(--ease-out) forwards;
}

.stagger-container .item:nth-child(1) { animation-delay: 0ms; }
.stagger-container .item:nth-child(2) { animation-delay: 100ms; }
.stagger-container .item:nth-child(3) { animation-delay: 200ms; }
.stagger-container .item:nth-child(4) { animation-delay: 300ms; }

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## Implementing Rhythm Systems

### Design Token Approach

```css
:root {
  /* Spacing rhythm */
  --rhythm-xs: var(--space-2);
  --rhythm-sm: var(--space-4);
  --rhythm-md: var(--space-6);
  --rhythm-lg: var(--space-8);
  --rhythm-xl: var(--space-12);
  --rhythm-2xl: var(--space-16);

  /* Component rhythm */
  --card-padding: var(--rhythm-md);
  --section-padding: var(--rhythm-2xl);
  --list-gap: var(--rhythm-sm);
  --form-gap: var(--rhythm-md);
}
```

### Component Library Pattern

```tsx
// Consistent spacing props
interface RhythmProps {
  spacing?: 'tight' | 'normal' | 'loose';
}

const spacingMap = {
  tight: 'gap-2',
  normal: 'gap-4',
  loose: 'gap-8'
};

function Stack({ spacing = 'normal', children }: RhythmProps) {
  return (
    <div className={`flex flex-col ${spacingMap[spacing]}`}>
      {children}
    </div>
  );
}

function Grid({ spacing = 'normal', children }: RhythmProps) {
  return (
    <div className={`grid grid-cols-3 ${spacingMap[spacing]}`}>
      {children}
    </div>
  );
}
```

## Anti-Patterns

### Inconsistent Spacing

```css
/* Bad - random spacing */
.section-1 { padding: 20px; }
.section-2 { padding: 35px; }
.section-3 { padding: 48px; }

/* Good - rhythmic spacing */
.section-sm { padding: var(--space-8); }
.section-md { padding: var(--space-12); }
.section-lg { padding: var(--space-16); }
```

### Breaking Pattern Without Purpose

```css
/* Bad - arbitrary style change */
.card { border-radius: 12px; }
.card-special { border-radius: 4px; } /* Why different? */

/* Good - purposeful variation */
.card { border-radius: 12px; }
.card-compact { border-radius: 8px; } /* Smaller = tighter radius */
```

### Monotonous Rhythm

```css
/* Bad - no variation, boring */
.item { padding: 16px; margin: 16px; gap: 16px; }

/* Good - varied but consistent */
.item {
  padding: var(--space-4);     /* Internal */
  margin-bottom: var(--space-6); /* Between items */
  gap: var(--space-3);         /* Within item */
}
```

## Summary

Visual rhythm creates coherent, professional interfaces:

| Rhythm Type | Characteristic | Best For |
|-------------|----------------|----------|
| **Regular** | Equal intervals | Grids, lists, navigation |
| **Alternating** | ABAB pattern | Tables, content sections |
| **Progressive** | Gradual change | Hierarchy, animations |
| **Flowing** | Organic variation | Masonry, creative layouts |

**Key Principles:**
1. Use a mathematical spacing scale
2. Maintain vertical rhythm with baseline grid
3. Repeat visual patterns consistently
4. Break rhythm intentionally for emphasis
5. Apply consistent animation timing
6. Document rhythm tokens in design system

---

**When to use this skill:**
- Establishing design system foundations
- Auditing interface consistency
- Creating layout patterns
- Designing animation systems
- Building component libraries


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

