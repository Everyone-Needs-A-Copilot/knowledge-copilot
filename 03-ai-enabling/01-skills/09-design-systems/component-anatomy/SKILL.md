---
last_updated: 2026-02-25
status: active
name: component-anatomy
description: Component structure, slots, variants, states, and composition patterns. Use when designing reusable UI components.
triggers:
  files: ["**/components/**", "**/ui/**", "**/atoms/**", "**/molecules/**"]
  keywords: ["component anatomy", "component structure", "slots", "variants", "component states", "composition", "atomic design"]
allowed-tools: Read, Write, Edit
---

# Component Anatomy: Deep Expertise Skill

Understanding the structural elements, composition patterns, and design considerations for building robust UI components.

## Component Structure

### Anatomy Overview

Every UI component consists of these structural layers:

```
┌─────────────────────────────────────────┐
│  Container (root element)               │
│  ┌───────────────────────────────────┐  │
│  │  Slots / Regions                   │  │
│  │  ┌─────────┐ ┌─────────────────┐  │  │
│  │  │ Leading │ │ Content         │  │  │
│  │  │ (icon)  │ │ (label/text)    │  │  │
│  │  └─────────┘ └─────────────────┘  │  │
│  │              ┌─────────────────┐  │  │
│  │              │ Trailing        │  │  │
│  │              │ (action/badge)  │  │  │
│  │              └─────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Core Structural Elements

| Element | Purpose | Examples |
|---------|---------|----------|
| **Container** | Root wrapper, defines boundaries | Button, Card, Input |
| **Slots** | Flexible content regions | Leading, Content, Trailing |
| **Content** | Primary information area | Label, Title, Body |
| **Affordances** | Interactive indicators | Icons, Chevrons, Handles |
| **Decorators** | Visual enhancements | Badges, Dots, Borders |


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Button Anatomy

### Structure

```
┌─────────────────────────────────────┐
│  ┌──────┐  ┌────────────┐  ┌────┐  │
│  │ Icon │  │   Label    │  │ →  │  │
│  │(opt) │  │ (required) │  │opt │  │
│  └──────┘  └────────────┘  └────┘  │
│                                     │
│  [padding]          [padding]       │
└─────────────────────────────────────┘
```

### CSS Implementation

```css
.button {
  /* Container */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--button-gap, 8px);

  /* Sizing */
  min-height: var(--button-height);
  padding: var(--button-padding-y) var(--button-padding-x);

  /* Typography */
  font-family: var(--font-family-ui);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  line-height: 1;

  /* Visual */
  background: var(--button-bg);
  color: var(--button-color);
  border: var(--button-border-width) solid var(--button-border-color);
  border-radius: var(--button-radius);

  /* Interaction */
  cursor: pointer;
  transition: var(--button-transition);
}

/* Slots */
.button-icon {
  flex-shrink: 0;
  width: var(--button-icon-size);
  height: var(--button-icon-size);
}

.button-label {
  /* Prevent text wrapping */
  white-space: nowrap;
}
```

### Size Variants

| Size | Height | Padding X | Font Size | Icon Size |
|------|--------|-----------|-----------|-----------|
| xs | 28px | 10px | 12px | 14px |
| sm | 32px | 12px | 13px | 16px |
| md | 40px | 16px | 14px | 18px |
| lg | 48px | 20px | 16px | 20px |
| xl | 56px | 24px | 18px | 24px |

## Input Field Anatomy

### Structure

```
┌──────────────────────────────────────────┐
│ Label (optional)                         │
├──────────────────────────────────────────┤
│ ┌──────────────────────────────────────┐ │
│ │ ┌────┐ ┌──────────────┐ ┌─────────┐ │ │
│ │ │Pfx │ │ Input        │ │ Suffix  │ │ │
│ │ │icon│ │              │ │ (clear) │ │ │
│ │ └────┘ └──────────────┘ └─────────┘ │ │
│ └──────────────────────────────────────┘ │
├──────────────────────────────────────────┤
│ Helper text / Error message              │
└──────────────────────────────────────────┘
```

### CSS Implementation

```css
.input-field {
  display: flex;
  flex-direction: column;
  gap: var(--input-label-gap, 4px);
}

.input-label {
  font-size: var(--input-label-size);
  font-weight: var(--input-label-weight);
  color: var(--input-label-color);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: var(--input-inner-gap, 8px);

  /* Container styling */
  min-height: var(--input-height);
  padding: var(--input-padding-y) var(--input-padding-x);
  background: var(--input-bg);
  border: var(--input-border-width) solid var(--input-border-color);
  border-radius: var(--input-radius);

  /* Focus container, not input */
  &:focus-within {
    border-color: var(--input-focus-border);
    box-shadow: var(--input-focus-shadow);
  }
}

.input-prefix,
.input-suffix {
  flex-shrink: 0;
  color: var(--input-addon-color);
}

.input-element {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  outline: none;
  font-size: var(--input-font-size);
  color: var(--input-text-color);

  &::placeholder {
    color: var(--input-placeholder-color);
  }
}

.input-helper {
  font-size: var(--input-helper-size);
  color: var(--input-helper-color);
}

.input-error {
  color: var(--color-error);
}
```

## Card Anatomy

### Structure

```
┌─────────────────────────────────────────┐
│ ┌─────────────────────────────────────┐ │
│ │         Media (optional)            │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ Header                              │ │
│ │ ┌───────┐ ┌─────────────┐ ┌──────┐ │ │
│ │ │Avatar │ │ Title       │ │Action│ │ │
│ │ │(opt)  │ │ Subtitle    │ │(opt) │ │ │
│ │ └───────┘ └─────────────┘ └──────┘ │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ Body                                │ │
│ │ Content goes here...                │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ Footer                              │ │
│ │ [Actions]              [Metadata]   │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### CSS Implementation

```css
.card {
  display: flex;
  flex-direction: column;
  background: var(--card-bg);
  border: var(--card-border-width) solid var(--card-border-color);
  border-radius: var(--card-radius);
  overflow: hidden;
  box-shadow: var(--card-shadow);
}

.card-media {
  aspect-ratio: var(--card-media-ratio, 16/9);
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: var(--card-header-gap, 12px);
  padding: var(--card-padding);

  /* Remove bottom padding if followed by body */
  &:not(:last-child) {
    padding-bottom: 0;
  }
}

.card-header-content {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: var(--card-title-size);
  font-weight: var(--card-title-weight);
  color: var(--card-title-color);
  margin: 0;
}

.card-subtitle {
  font-size: var(--card-subtitle-size);
  color: var(--card-subtitle-color);
  margin: var(--card-subtitle-gap, 4px) 0 0;
}

.card-body {
  padding: var(--card-padding);
  color: var(--card-body-color);
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--card-footer-gap);
  padding: var(--card-padding);
  border-top: 1px solid var(--card-divider-color);
}
```

## Component States

### State Definitions

| State | Trigger | Visual Treatment |
|-------|---------|------------------|
| **Default** | Initial state | Base styling |
| **Hover** | Mouse over | Subtle highlight |
| **Focus** | Keyboard focus | Visible ring |
| **Active** | Being pressed | Pressed appearance |
| **Disabled** | Cannot interact | Reduced opacity |
| **Loading** | Processing | Spinner, disabled |
| **Error** | Validation fail | Error colors |
| **Success** | Validation pass | Success colors |
| **Selected** | Chosen item | Highlight/check |

### State CSS Implementation

```css
.component {
  /* Default state */
  background: var(--bg-default);
  color: var(--text-default);
  border-color: var(--border-default);
  transition: all 0.15s ease;
}

/* Hover state */
.component:hover:not(:disabled) {
  background: var(--bg-hover);
  border-color: var(--border-hover);
}

/* Focus state - always visible for keyboard */
.component:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Active/pressed state */
.component:active:not(:disabled) {
  background: var(--bg-active);
  transform: scale(0.98);
}

/* Disabled state */
.component:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Loading state */
.component.is-loading {
  pointer-events: none;
  position: relative;
}

.component.is-loading::after {
  content: '';
  position: absolute;
  /* spinner styles */
}

/* Error state */
.component.is-error {
  border-color: var(--color-error);
  background: var(--color-error-bg);
}

/* Success state */
.component.is-success {
  border-color: var(--color-success);
  background: var(--color-success-bg);
}

/* Selected state */
.component.is-selected {
  background: var(--color-primary-bg);
  border-color: var(--color-primary);
}
```

## Variant Patterns

### Variant Types

| Variant Type | Purpose | Example |
|--------------|---------|---------|
| **Visual** | Appearance changes | primary, secondary, ghost |
| **Size** | Dimension changes | sm, md, lg |
| **Shape** | Form changes | rounded, pill, square |
| **Intent** | Semantic meaning | success, warning, error |

### Variant Implementation

```css
/* Visual variants */
.button--primary {
  --button-bg: var(--color-primary);
  --button-color: white;
  --button-border-color: var(--color-primary);
}

.button--secondary {
  --button-bg: transparent;
  --button-color: var(--color-primary);
  --button-border-color: var(--color-primary);
}

.button--ghost {
  --button-bg: transparent;
  --button-color: var(--color-text);
  --button-border-color: transparent;
}

/* Size variants */
.button--sm {
  --button-height: 32px;
  --button-padding-x: 12px;
  --button-font-size: 13px;
}

.button--lg {
  --button-height: 48px;
  --button-padding-x: 20px;
  --button-font-size: 16px;
}

/* Shape variants */
.button--pill {
  --button-radius: 9999px;
}

.button--square {
  --button-radius: 0;
}

/* Intent variants */
.button--danger {
  --button-bg: var(--color-error);
  --button-color: white;
}
```

## Slots and Composition

### Slot Pattern

```tsx
interface ComponentSlots {
  leading?: React.ReactNode;
  children: React.ReactNode;
  trailing?: React.ReactNode;
}

function ListItem({ leading, children, trailing }: ComponentSlots) {
  return (
    <div className="list-item">
      {leading && <div className="list-item-leading">{leading}</div>}
      <div className="list-item-content">{children}</div>
      {trailing && <div className="list-item-trailing">{trailing}</div>}
    </div>
  );
}

// Usage
<ListItem
  leading={<Avatar src={user.avatar} />}
  trailing={<Badge count={3} />}
>
  <Title>{user.name}</Title>
  <Subtitle>{user.email}</Subtitle>
</ListItem>
```

### Compound Components

```tsx
// Compound component pattern
function Card({ children }: { children: React.ReactNode }) {
  return <div className="card">{children}</div>;
}

Card.Media = function CardMedia({ src, alt }: { src: string; alt: string }) {
  return (
    <div className="card-media">
      <img src={src} alt={alt} />
    </div>
  );
};

Card.Header = function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>;
};

Card.Body = function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>;
};

Card.Footer = function CardFooter({ children }: { children: React.ReactNode }) {
  return <div className="card-footer">{children}</div>;
};

// Usage
<Card>
  <Card.Media src="/image.jpg" alt="Description" />
  <Card.Header>
    <h3>Title</h3>
  </Card.Header>
  <Card.Body>
    <p>Content here...</p>
  </Card.Body>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>
```

## Responsive Component Anatomy

### Adaptive Layouts

```css
/* List item responsive anatomy */
.list-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
}

.list-item-leading {
  flex-shrink: 0;
}

.list-item-content {
  flex: 1;
  min-width: 0;
}

.list-item-trailing {
  flex-shrink: 0;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .list-item {
    flex-wrap: wrap;
  }

  .list-item-content {
    width: 100%;
    order: 2;
    margin-top: var(--space-2);
  }

  .list-item-trailing {
    margin-left: auto;
  }
}
```

## Anti-Patterns

### Common Anatomy Mistakes

**Rigid slot structure:**
```tsx
/* Bad - forces all slots */
<Button icon={<Icon />} label="Text" badge={<Badge />} />

/* Good - flexible slots */
<Button>
  <Icon />
  Text
  <Badge />
</Button>
```

**Mixed concerns:**
```css
/* Bad - layout and visual mixed */
.card {
  display: flex;
  background: blue;
  gap: 10px;
  color: white;
}

/* Good - separated concerns */
.card {
  /* Structure */
  display: flex;
  flex-direction: column;
  gap: var(--card-gap);

  /* Visual (via tokens) */
  background: var(--card-bg);
  color: var(--card-color);
}
```

**Hardcoded dimensions:**
```css
/* Bad - fixed sizes */
.input { height: 40px; padding: 8px 12px; }

/* Good - token-based */
.input {
  min-height: var(--input-height);
  padding: var(--input-padding-y) var(--input-padding-x);
}
```

## Summary

Well-structured components enable scalability and consistency:

| Principle | Implementation |
|-----------|----------------|
| **Clear structure** | Define container, slots, content |
| **Flexible slots** | Allow optional regions |
| **Consistent states** | Implement all interactive states |
| **Systematic variants** | Size, visual, shape, intent |
| **Token-based** | Use design tokens for all values |
| **Composition** | Support compound patterns |

**Key Guidelines:**
1. Define clear anatomical regions
2. Make slots optional and flexible
3. Implement complete state coverage
4. Use CSS custom properties for variants
5. Support composition over configuration
6. Test responsive anatomy changes

---

**When to use this skill:**
- Designing new component specifications
- Implementing component libraries
- Auditing existing components
- Creating component documentation
- Building design system foundations


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

