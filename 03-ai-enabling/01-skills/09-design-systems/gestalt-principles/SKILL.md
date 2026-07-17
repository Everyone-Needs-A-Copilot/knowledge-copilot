---
last_updated: 2026-02-25
status: active
name: gestalt-principles
description: Perceptual organization laws - proximity, similarity, closure, continuity. Use when arranging UI elements.
triggers:
  files: ["**/layout.*", "**/components/**", "**/design-system/**"]
  keywords: ["gestalt", "proximity", "similarity", "closure", "continuity", "grouping", "visual perception", "figure-ground"]
allowed-tools: Read, Write, Edit
---

# Gestalt Principles: Deep Expertise Skill

Application of Gestalt psychology principles to create intuitive, visually coherent user interfaces.

## Introduction to Gestalt

Gestalt psychology explains how humans perceive visual information. "Gestalt" means "unified whole" in German. These principles describe how our brains automatically organize visual elements into meaningful patterns.

**Core Insight**: The whole is greater than the sum of its parts. Users perceive interfaces as organized patterns, not individual elements.


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## The Seven Gestalt Principles

### 1. Proximity

**Principle**: Elements placed close together are perceived as a group.

**Why It Works**: Our brains minimize cognitive effort by grouping nearby items, assuming spatial closeness implies relatedness.

**UI Applications:**

| Context | Application |
|---------|-------------|
| Form fields | Group label with input |
| Navigation | Cluster related links |
| Cards | Group related information |
| Toolbars | Group related actions |

**Implementation:**

```css
/* Bad - ambiguous grouping */
.form-field label {
  margin-bottom: 16px;
}
.form-field input {
  margin-bottom: 16px;
}

/* Good - clear association through proximity */
.form-field label {
  margin-bottom: 4px;  /* Close to its input */
}
.form-field input {
  margin-bottom: 24px; /* Separated from next field */
}
```

**Spacing Pattern:**
- **Within group**: Tight spacing (4-8px)
- **Between groups**: Larger spacing (16-32px)
- **Between sections**: Even larger (32-64px)

```css
:root {
  --space-within-group: 0.5rem;    /* 8px */
  --space-between-groups: 1.5rem;  /* 24px */
  --space-between-sections: 3rem;  /* 48px */
}
```

### 2. Similarity

**Principle**: Elements sharing visual characteristics are perceived as related.

**Similarity Attributes:**
- Color
- Shape
- Size
- Texture
- Orientation
- Typography

**UI Applications:**

| Context | Application |
|---------|-------------|
| Navigation | Same style for same-level items |
| Buttons | Consistent styling by action type |
| Status indicators | Color-coded states |
| Content types | Visual differentiation |

**Implementation:**

```css
/* Primary actions - similar appearance */
.btn-primary {
  background: var(--color-primary);
  color: white;
  font-weight: 600;
  border-radius: 8px;
}

/* Secondary actions - different but consistent */
.btn-secondary {
  background: transparent;
  color: var(--color-primary);
  font-weight: 600;
  border-radius: 8px;
  border: 2px solid var(--color-primary);
}

/* Destructive actions - clearly different */
.btn-danger {
  background: var(--color-danger);
  color: white;
  font-weight: 600;
  border-radius: 8px;
}
```

**Pattern: Visual Coding by Category**

```css
/* Content type indicators */
.badge-category {
  /* Articles */
  &.article { background: var(--color-blue-100); color: var(--color-blue-700); }
  /* Videos */
  &.video { background: var(--color-purple-100); color: var(--color-purple-700); }
  /* Podcasts */
  &.podcast { background: var(--color-green-100); color: var(--color-green-700); }
}
```

### 3. Closure

**Principle**: The mind completes incomplete shapes to form recognizable patterns.

**Why It Works**: Our brains prefer complete, familiar shapes and will "fill in" missing information.

**UI Applications:**

| Context | Application |
|---------|-------------|
| Icons | Simplified, suggestive shapes |
| Progress indicators | Partial circles, arcs |
| Loading states | Incomplete shapes |
| Logos | Negative space designs |

**Implementation:**

```css
/* Progress circle using closure */
.progress-ring {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: conic-gradient(
    var(--color-primary) calc(var(--progress) * 3.6deg),
    var(--color-gray-200) 0
  );
}

/* Card with implied boundary */
.card {
  /* No border needed - shadow implies closure */
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}
```

**Pattern: Implied Containers**

```css
/* Visual grouping without explicit borders */
.feature-section {
  background: var(--color-gray-50);
  padding: 3rem;
  /* No border - background creates closure */
}

/* Tab indicator implying active state */
.tab.active {
  border-bottom: 3px solid var(--color-primary);
  /* Mind completes the "selected" box */
}
```

### 4. Continuity

**Principle**: Elements arranged on a line or curve are perceived as related and following a path.

**Why It Works**: Eyes naturally follow smooth paths, perceiving elements along that path as connected.

**UI Applications:**

| Context | Application |
|---------|-------------|
| Wizards | Step indicators on a line |
| Timelines | Events along a path |
| Navigation | Breadcrumbs |
| Data visualization | Trend lines |

**Implementation:**

```css
/* Stepper - continuity through connecting line */
.stepper {
  display: flex;
  align-items: center;
}

.step {
  display: flex;
  align-items: center;
}

.step-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-gray-200);
}

.step-line {
  width: 60px;
  height: 2px;
  background: var(--color-gray-200);
}

.step.completed .step-circle,
.step.completed .step-line {
  background: var(--color-primary);
}
```

**Pattern: Visual Flow**

```css
/* Timeline with continuity */
.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--color-gray-200);
}

.timeline-item {
  position: relative;
  padding-bottom: 2rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -1.5rem;
  top: 0.25rem;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-primary);
}
```

### 5. Figure-Ground

**Principle**: The mind separates elements into foreground (figure) and background (ground).

**Why It Works**: We instinctively distinguish objects of attention from their surroundings.

**UI Applications:**

| Context | Application |
|---------|-------------|
| Modals | Content over darkened background |
| Cards | Elevated surfaces |
| Focus states | Highlighted active elements |
| Overlays | Layered interfaces |

**Implementation:**

```css
/* Modal - clear figure-ground separation */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  /* Clearly the "figure" against blurred ground */
}

/* Card elevation */
.card {
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
  /* Increases figure prominence */
}
```

**Pattern: Z-Index Layering System**

```css
:root {
  --z-ground: 0;
  --z-elevated: 10;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal-backdrop: 300;
  --z-modal: 400;
  --z-tooltip: 500;
}
```

### 6. Common Region

**Principle**: Elements within a boundary are perceived as grouped.

**Why It Works**: Explicit visual boundaries create strong grouping even without proximity.

**UI Applications:**

| Context | Application |
|---------|-------------|
| Cards | Contained content groups |
| Sections | Background-defined areas |
| Panels | Sidebar groupings |
| Wells | Nested content areas |

**Implementation:**

```css
/* Card as common region */
.card {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  background: white;
}

/* Section with background */
.feature-section {
  background: var(--color-gray-50);
  padding: 4rem 2rem;
  margin: 2rem 0;
}

/* Well for nested content */
.well {
  background: var(--color-gray-100);
  border-radius: 8px;
  padding: 1rem;
}
```

**Pattern: Nested Regions**

```css
/* Outer region */
.panel {
  background: var(--color-gray-50);
  border-radius: 16px;
  padding: 2rem;
}

/* Inner region */
.panel .card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
```

### 7. Common Fate

**Principle**: Elements moving in the same direction or changing together are perceived as related.

**Why It Works**: Synchronized movement suggests shared purpose or connection.

**UI Applications:**

| Context | Application |
|---------|-------------|
| Accordions | Grouped content collapse |
| Carousels | Items moving together |
| Loading | Synchronized animations |
| Transitions | Related elements animating together |

**Implementation:**

```css
/* Accordion - items share fate */
.accordion-content {
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.accordion.closed .accordion-content {
  max-height: 0;
}

.accordion.open .accordion-content {
  max-height: 500px;
}

/* List items with staggered but unified animation */
.list-item {
  opacity: 0;
  transform: translateY(10px);
  animation: fadeInUp 0.3s ease-out forwards;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
/* Items move together but with slight cascade */

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## Combining Principles

### Multi-Principle Layouts

Effective UI design uses multiple Gestalt principles together:

```css
/* Navigation combining proximity, similarity, and common region */
.nav {
  /* Common region - contains all nav items */
  background: white;
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-group {
  /* Proximity - group related items */
  display: flex;
  gap: 0.25rem;
}

.nav-group + .nav-group {
  /* Proximity - separate groups */
  margin-left: 1rem;
  padding-left: 1rem;
  border-left: 1px solid var(--color-gray-200);
}

.nav-item {
  /* Similarity - consistent styling */
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  color: var(--color-gray-700);
  transition: all 0.2s;
}

.nav-item:hover {
  /* Figure-ground - highlight on interaction */
  background: var(--color-gray-100);
}

.nav-item.active {
  /* Similarity break - indicate selection */
  background: var(--color-primary);
  color: white;
}
```

### Form Design with Gestalt

```css
.form {
  /* Common region */
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-section {
  /* Proximity between sections */
  margin-bottom: 2rem;
}

.form-section-title {
  /* Similarity for all section titles */
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

.form-row {
  /* Proximity - fields in a row are related */
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-field {
  /* Proximity - label close to input */
  margin-bottom: 1.5rem;
}

.form-field label {
  display: block;
  margin-bottom: 0.25rem;
  /* Similarity - all labels look the same */
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-gray-700);
}

.form-field input {
  width: 100%;
  padding: 0.75rem 1rem;
  /* Similarity - all inputs look the same */
  border: 1px solid var(--color-gray-300);
  border-radius: 8px;
  font-size: 1rem;
}

.form-field input:focus {
  /* Figure-ground - focused field stands out */
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-100);
  outline: none;
}
```

## Applying Gestalt to Components

### Data Tables

```css
.table {
  /* Common region */
  border: 1px solid var(--color-gray-200);
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  /* Similarity - header cells share style */
  background: var(--color-gray-50);
  font-weight: 600;
}

.table-row {
  /* Continuity - horizontal alignment */
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  border-bottom: 1px solid var(--color-gray-100);
}

.table-row:hover {
  /* Figure-ground on hover */
  background: var(--color-gray-50);
}

.table-cell {
  /* Proximity - padding creates cell breathing room */
  padding: 1rem;
}
```

### Navigation Menus

```css
.sidebar-nav {
  /* Common region */
  padding: 1rem;
}

.nav-section {
  /* Proximity - group related items */
  margin-bottom: 1.5rem;
}

.nav-section-title {
  /* Similarity break - distinguishes from items */
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-gray-500);
  margin-bottom: 0.5rem;
}

.nav-item {
  /* Similarity - all items share base style */
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  color: var(--color-gray-700);
}

.nav-item.active {
  /* Figure-ground - active state prominence */
  background: var(--color-primary-50);
  color: var(--color-primary-700);
}
```

## Anti-Patterns

### Common Gestalt Violations

**Breaking proximity expectations:**
```css
/* Bad - label far from input */
.field label {
  margin-bottom: 24px; /* Too much space */
}

/* Good - label associated with input */
.field label {
  margin-bottom: 4px;
}
```

**Inconsistent similarity:**
```css
/* Bad - inconsistent button styles */
.btn-save { background: blue; border-radius: 8px; }
.btn-cancel { background: gray; border-radius: 4px; }
.btn-delete { background: red; border-radius: 16px; }

/* Good - consistent base, meaningful variation */
.btn { border-radius: 8px; font-weight: 600; }
.btn-primary { background: var(--color-primary); }
.btn-secondary { background: var(--color-gray-200); }
.btn-danger { background: var(--color-danger); }
```

**Unclear figure-ground:**
```css
/* Bad - modal blends with background */
.modal {
  background: rgba(255, 255, 255, 0.9);
  /* Hard to distinguish from page */
}

/* Good - clear separation */
.modal {
  background: white;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}
```

## Summary

Gestalt principles provide a psychological foundation for visual design:

| Principle | Application | Key Technique |
|-----------|-------------|---------------|
| **Proximity** | Group related elements | Spacing hierarchy |
| **Similarity** | Show relationships | Consistent styling |
| **Closure** | Simplify shapes | Implied boundaries |
| **Continuity** | Guide the eye | Alignment, lines |
| **Figure-Ground** | Create focus | Elevation, contrast |
| **Common Region** | Define groups | Containers, backgrounds |
| **Common Fate** | Show connection | Synchronized motion |

---

**When to use this skill:**
- Designing layouts and component arrangements
- Establishing visual hierarchy
- Grouping related UI elements
- Creating navigation systems
- Reviewing designs for perceptual clarity


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

