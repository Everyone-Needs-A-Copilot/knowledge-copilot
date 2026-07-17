---
last_updated: 2026-02-25
status: active
name: iconography-systems
description: Icon design principles, sizing systems, and consistent visual language. Use when creating or implementing icon libraries.
triggers:
  files: ["**/icons/**", "**/iconography.*", "**/icon-set.*", "**/sprites.*"]
  keywords: ["icons", "iconography", "icon set", "icon grid", "icon sizing", "icon consistency", "svg icons", "icon library"]
allowed-tools: Read, Write, Edit
---

# Iconography Systems: Deep Expertise Skill

Principles and systems for creating consistent, scalable, and meaningful icon libraries in digital products.

## Icon Design Fundamentals

### The Role of Icons

Icons serve as visual shortcuts that communicate meaning faster than text. They must be:

| Quality | Description |
|---------|-------------|
| **Recognizable** | Instantly identifiable meaning |
| **Consistent** | Unified visual language |
| **Scalable** | Clear at all sizes |
| **Accessible** | Meaningful with proper labels |
| **Purposeful** | Each icon serves a clear function |

### Icon Types

| Type | Purpose | Examples |
|------|---------|----------|
| **System** | UI actions and navigation | Menu, close, search, settings |
| **Status** | Communicate state | Success, error, warning, info |
| **Object** | Represent things | File, folder, document, image |
| **Action** | Indicate operations | Edit, delete, share, download |
| **Navigation** | Guide movement | Arrow, chevron, home, back |
| **Social** | Platform identification | Twitter, LinkedIn, GitHub |


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Icon Grid System

### The Base Grid

Icons are designed on a consistent grid for visual harmony:

```
Standard Grid Sizes:
├── 16×16 (micro) - Inline text, tight UI
├── 20×20 (small) - Form inputs, compact UI
├── 24×24 (medium) - Default UI size
├── 32×32 (large) - Feature icons, emphasis
├── 48×48 (xlarge) - Hero icons, onboarding
└── 64×64 (xxlarge) - Marketing, illustrations
```

### Grid Anatomy

```
┌─────────────────────────┐
│  ┌─────────────────┐   │  ← Live area (content)
│  │                 │   │
│  │     ████████    │   │
│  │     ████████    │   │
│  │     ████████    │   │
│  │                 │   │
│  └─────────────────┘   │
│                         │  ← Padding (optical balance)
└─────────────────────────┘
     ↑ Trim area
```

**Grid Specifications:**

| Grid Size | Live Area | Padding | Stroke Width |
|-----------|-----------|---------|--------------|
| 16×16 | 14×14 | 1px | 1.5px |
| 20×20 | 18×18 | 1px | 1.5px |
| 24×24 | 20×20 | 2px | 2px |
| 32×32 | 28×28 | 2px | 2px |
| 48×48 | 42×42 | 3px | 2.5px |

### Keylines

Keylines ensure consistent visual weight across different shapes:

```
Circle keyline:     Square keyline:     Portrait keyline:
┌───────────┐       ┌───────────┐       ┌───────────┐
│   ┌───┐   │       │ ┌───────┐ │       │  ┌─────┐  │
│  │     │  │       │ │       │ │       │  │     │  │
│  │     │  │       │ │       │ │       │  │     │  │
│   └───┘   │       │ └───────┘ │       │  │     │  │
└───────────┘       └───────────┘       │  └─────┘  │
                                        └───────────┘
```

## Icon Sizing System

### CSS Implementation

```css
:root {
  /* Base icon sizes */
  --icon-size-xs: 12px;
  --icon-size-sm: 16px;
  --icon-size-md: 20px;
  --icon-size-base: 24px;
  --icon-size-lg: 32px;
  --icon-size-xl: 48px;
  --icon-size-2xl: 64px;

  /* Contextual sizes */
  --icon-size-inline: var(--icon-size-sm);
  --icon-size-button: var(--icon-size-md);
  --icon-size-input: var(--icon-size-md);
  --icon-size-nav: var(--icon-size-base);
  --icon-size-card: var(--icon-size-lg);
  --icon-size-hero: var(--icon-size-xl);
}

/* Size classes */
.icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-xs { width: var(--icon-size-xs); height: var(--icon-size-xs); }
.icon-sm { width: var(--icon-size-sm); height: var(--icon-size-sm); }
.icon-md { width: var(--icon-size-md); height: var(--icon-size-md); }
.icon-base { width: var(--icon-size-base); height: var(--icon-size-base); }
.icon-lg { width: var(--icon-size-lg); height: var(--icon-size-lg); }
.icon-xl { width: var(--icon-size-xl); height: var(--icon-size-xl); }
```

### Size-Context Relationships

| Context | Recommended Size | Rationale |
|---------|------------------|-----------|
| Inline with text | 1em or 16px | Matches text height |
| Button icon | 20px | Touch-friendly, balanced |
| Input prefix/suffix | 20px | Fits input height |
| Navigation item | 24px | Scannable at distance |
| Card header | 32px | Visual anchor |
| Empty state | 48-64px | Draws attention |
| Feature showcase | 48-64px | Marketing emphasis |

## Visual Style Guidelines

### Stroke vs Fill

**Stroke Icons (Outlined):**
- Lighter visual weight
- Better for dense UI
- Consistent stroke width critical
- Works well at smaller sizes

**Fill Icons (Solid):**
- Heavier visual weight
- Better for emphasis
- More recognizable silhouettes
- Better for status indicators

```css
/* Stroke icon styling */
.icon-stroke {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Fill icon styling */
.icon-fill {
  fill: currentColor;
  stroke: none;
}
```

### Style Consistency Rules

| Property | Guideline |
|----------|-----------|
| **Stroke width** | Consistent within size tier |
| **Corner radius** | Unified across set (0, 2px, or fully round) |
| **Angles** | Use 45°, 90° angles; avoid arbitrary |
| **Curves** | Consistent bezier handles |
| **Optical alignment** | Center visually, not mathematically |
| **Detail level** | Appropriate for smallest intended size |

### Stroke Width by Size

```css
:root {
  /* Stroke width scales with icon size */
  --icon-stroke-xs: 1px;
  --icon-stroke-sm: 1.5px;
  --icon-stroke-md: 1.5px;
  --icon-stroke-base: 2px;
  --icon-stroke-lg: 2px;
  --icon-stroke-xl: 2.5px;
}
```

## Color System for Icons

### Semantic Icon Colors

```css
:root {
  /* Base colors */
  --icon-color-default: var(--color-gray-600);
  --icon-color-muted: var(--color-gray-400);
  --icon-color-emphasis: var(--color-gray-900);

  /* Interactive states */
  --icon-color-hover: var(--color-gray-900);
  --icon-color-active: var(--color-primary-600);
  --icon-color-disabled: var(--color-gray-300);

  /* Semantic colors */
  --icon-color-success: var(--color-green-600);
  --icon-color-warning: var(--color-amber-600);
  --icon-color-error: var(--color-red-600);
  --icon-color-info: var(--color-blue-600);

  /* On dark backgrounds */
  --icon-color-inverse: var(--color-white);
  --icon-color-inverse-muted: var(--color-gray-300);
}
```

### Color Application

```css
.icon {
  color: var(--icon-color-default);
  transition: color 0.15s ease;
}

/* Contextual coloring */
.icon-muted { color: var(--icon-color-muted); }
.icon-emphasis { color: var(--icon-color-emphasis); }

/* Status icons */
.icon-success { color: var(--icon-color-success); }
.icon-warning { color: var(--icon-color-warning); }
.icon-error { color: var(--icon-color-error); }
.icon-info { color: var(--icon-color-info); }

/* Interactive icons */
button .icon,
a .icon {
  color: inherit;
}

button:hover .icon,
a:hover .icon {
  color: var(--icon-color-hover);
}

button:disabled .icon {
  color: var(--icon-color-disabled);
}
```

## Icon Component Patterns

### React Component

```tsx
interface IconProps {
  name: string;
  size?: 'xs' | 'sm' | 'md' | 'base' | 'lg' | 'xl';
  color?: 'default' | 'muted' | 'emphasis' | 'success' | 'warning' | 'error' | 'info';
  label?: string;
  className?: string;
}

function Icon({
  name,
  size = 'base',
  color = 'default',
  label,
  className
}: IconProps) {
  const IconComponent = icons[name];

  return (
    <span
      className={`icon icon-${size} icon-${color} ${className}`}
      role={label ? 'img' : 'presentation'}
      aria-label={label}
      aria-hidden={!label}
    >
      <IconComponent />
    </span>
  );
}
```

### Icon + Text Alignment

```css
/* Icon with text alignment */
.icon-text {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
}

.icon-text .icon {
  /* Optical adjustment for common icons */
  margin-top: -0.0625em;
}

/* Icon-only buttons need explicit sizing */
.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
}

.btn-icon .icon {
  width: var(--icon-size-md);
  height: var(--icon-size-md);
}
```

## SVG Optimization

### SVG Structure Best Practices

```xml
<!-- Optimized SVG icon -->
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
>
  <!-- Paths go here -->
  <path d="M12 5v14M5 12h14"/>
</svg>
```

### Optimization Checklist

| Optimization | Description |
|--------------|-------------|
| **Remove metadata** | Strip editor comments, IDs |
| **Simplify paths** | Reduce point count |
| **Use currentColor** | Inherit color from parent |
| **Set viewBox** | Enable scaling |
| **Remove dimensions** | Let CSS control size |
| **Combine paths** | Where logical |
| **Use relative commands** | Smaller file size |

### SVG Sprite System

```html
<!-- Icon sprite (hidden) -->
<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
  <symbol id="icon-search" viewBox="0 0 24 24">
    <circle cx="11" cy="11" r="8"/>
    <path d="m21 21-4.35-4.35"/>
  </symbol>
  <symbol id="icon-menu" viewBox="0 0 24 24">
    <path d="M3 12h18M3 6h18M3 18h18"/>
  </symbol>
</svg>

<!-- Usage -->
<svg class="icon icon-base">
  <use href="#icon-search"/>
</svg>
```

## Accessibility

### Icon Accessibility Guidelines

| Scenario | Implementation |
|----------|----------------|
| **Decorative icon** | `aria-hidden="true"` |
| **Meaningful icon** | `aria-label="Description"` |
| **Icon + visible text** | `aria-hidden="true"` on icon |
| **Icon button** | `aria-label` on button |
| **Status icon** | Include sr-only text |

### Implementation Examples

```html
<!-- Decorative icon (has visible label) -->
<button>
  <svg aria-hidden="true">...</svg>
  Save
</button>

<!-- Meaningful icon-only button -->
<button aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Status icon with context -->
<span class="status status-success">
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">Success:</span>
  File uploaded
</span>
```

### Screen Reader Classes

```css
/* Visually hidden but accessible */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Icon Library Organization

### File Structure

```
icons/
├── system/
│   ├── close.svg
│   ├── menu.svg
│   ├── search.svg
│   └── settings.svg
├── navigation/
│   ├── arrow-left.svg
│   ├── arrow-right.svg
│   ├── chevron-down.svg
│   └── home.svg
├── actions/
│   ├── edit.svg
│   ├── delete.svg
│   ├── share.svg
│   └── download.svg
├── status/
│   ├── check-circle.svg
│   ├── alert-triangle.svg
│   ├── x-circle.svg
│   └── info.svg
└── objects/
    ├── file.svg
    ├── folder.svg
    ├── image.svg
    └── document.svg
```

### Naming Conventions

| Convention | Example |
|------------|---------|
| **Lowercase** | `arrow-left.svg` |
| **Hyphen-separated** | `check-circle.svg` |
| **Descriptive** | `chevron-down.svg` not `v.svg` |
| **State suffix** | `eye.svg`, `eye-off.svg` |
| **Direction suffix** | `arrow-up.svg`, `arrow-down.svg` |

## Anti-Patterns

### Common Icon Mistakes

**Inconsistent stroke widths:**
```css
/* Bad - varying strokes */
.icon-a { stroke-width: 1.5px; }
.icon-b { stroke-width: 2px; }
.icon-c { stroke-width: 2.5px; }

/* Good - consistent stroke */
.icon { stroke-width: 2px; }
```

**Mixing styles:**
```css
/* Bad - stroke and fill mixed randomly */
.icon-settings { fill: none; stroke: currentColor; }
.icon-home { fill: currentColor; stroke: none; }

/* Good - consistent style per icon set */
.icon-outline { fill: none; stroke: currentColor; }
.icon-solid { fill: currentColor; stroke: none; }
```

**Poor scaling:**
```css
/* Bad - fixed pixel sizes */
.icon { width: 24px; height: 24px; }

/* Good - flexible sizing */
.icon {
  width: 1em;
  height: 1em;
}
```

**Missing accessibility:**
```html
<!-- Bad - no context -->
<button>
  <svg>...</svg>
</button>

<!-- Good - accessible -->
<button aria-label="Delete item">
  <svg aria-hidden="true">...</svg>
</button>
```

## Summary

Effective iconography systems require:

| Principle | Implementation |
|-----------|----------------|
| **Consistency** | Unified grid, stroke width, style |
| **Scalability** | Vector format, responsive sizing |
| **Clarity** | Simple forms, clear meaning |
| **Accessibility** | Proper labels, contrast |
| **Organization** | Logical categorization, naming |
| **Optimization** | Clean SVG, sprite systems |

**Key Guidelines:**
1. Design on a consistent grid (24×24 as base)
2. Maintain uniform stroke width within size tiers
3. Use currentColor for flexible theming
4. Provide semantic sizing tokens
5. Always consider accessibility
6. Optimize SVGs for performance

---

**When to use this skill:**
- Creating or extending icon libraries
- Implementing icon components
- Establishing icon design guidelines
- Auditing icon consistency
- Optimizing icon performance


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

