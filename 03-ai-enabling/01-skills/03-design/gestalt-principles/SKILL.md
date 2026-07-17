---
last_updated: 2026-02-25
status: active
name: gestalt-principles
description: Apply Gestalt psychology principles for visual organization - similarity, proximity, continuity, closure. Use when organizing content or designing layouts.
triggers:
  files: ["**/layout/**", "**/components/**", "**/design/**"]
  keywords: ["gestalt", "visual grouping", "proximity", "similarity", "closure", "continuity", "visual perception", "grouping"]
allowed-tools: Read, Write, Edit
---

# Gestalt Principles

Gestalt principles describe how humans perceive visual elements as organized patterns rather than individual parts. Applying these principles creates intuitive, scannable interfaces.

## Core Principle

**The whole is greater than the sum of its parts.** People perceive organized patterns and shapes before seeing individual elements.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## The Seven Gestalt Principles

### 1. Proximity

**Elements close together are perceived as related.**

| Application | UI Example |
|-------------|------------|
| Form fields | Group label, input, and helper text closely |
| Navigation | Space between nav groups signals hierarchy |
| Cards | Tight internal spacing, larger gaps between cards |
| Lists | Items within a section closer than section headers |

**Implementation:**
```
RELATED ITEMS          UNRELATED ITEMS
[Label]                [Group A]
[Input]
[Helper text]           [Spacer]

[Large gap]            [Group B]

[Label]
[Input]
```

**Common spacing ratios:**
- Within groups: 1x (8px)
- Between groups: 2-3x (16-24px)
- Between sections: 4-6x (32-48px)

### 2. Similarity

**Elements that look alike are perceived as related.**

| Shared Property | Perceived As |
|-----------------|--------------|
| Same color | Same category/type |
| Same shape | Same function |
| Same size | Same importance |
| Same style | Same meaning |

**Implementation:**
- All interactive links: same color
- All buttons: same border-radius
- All error states: same red treatment
- All metadata: same gray, smaller size

**Warning:** Breaking similarity intentionally draws attention. Use sparingly for emphasis.

### 3. Continuity

**Elements aligned along a line or curve are perceived as related.**

| Application | UI Example |
|-------------|------------|
| Lists | Left-aligned items flow as single group |
| Timelines | Vertical line connects related events |
| Progress | Horizontal path shows sequence |
| Grids | Aligned columns create visual order |

**Implementation:**
```
Left-aligned list (strong continuity):
• Item one
• Item two
• Item three

Centered items (weak continuity):
       • Item one
    • Item two
          • Item three
```

**Best practices:**
- Align labels above or to left of inputs
- Use consistent margins/gutters in grids
- Path lines connect sequential steps
- Tables: align columns consistently

### 4. Closure

**The mind completes incomplete shapes, seeing whole forms.**

| Application | UI Example |
|-------------|------------|
| Icons | Simple shapes suggest objects |
| Logos | Negative space forms images |
| Cards | Border on 3 sides still reads as container |
| Progress | Partial circle shows completion |

**Implementation:**
```
[  ─────────  ]  Progress bar (closure fills gap mentally)
       70%

┌──────────┐
│  Card    │     Implied container (closure adds bottom)
│  content │
```

**Uses:**
- Progress indicators with partial fills
- Icon design with implied shapes
- Containers with partial borders
- Loading states with incomplete circles

### 5. Figure-Ground

**People instinctively separate foreground from background.**

| Figure | Ground | UI Example |
|--------|--------|------------|
| Content | Background | Page content on white |
| Modal | Overlay | Dialog on dimmed background |
| Dropdown | Page | Menu floating above content |
| Focus | Context | Selected item highlighted |

**Implementation:**
- Modals: dark overlay separates from page
- Dropdowns: shadow lifts from surface
- Selected items: background color change
- Focus states: outline or highlight ring

**Best practices:**
- Ensure sufficient contrast
- Use shadow for elevation
- Dim/blur background for overlays
- One clear focal point at a time

### 6. Common Fate

**Elements moving in the same direction are perceived as grouped.**

| Application | UI Example |
|-------------|------------|
| Carousels | Items slide together |
| Expanding sections | Content animates in unison |
| Hover states | Related elements change together |
| Page transitions | Elements animate as group |

**Implementation:**
- Accordion content expands with arrow rotation
- Card hover: shadow + transform together
- Sidebar collapse: all items slide in unison
- Toast dismissal: icon + text fade together

### 7. Common Region

**Elements within a shared boundary are perceived as grouped.**

| Boundary Type | UI Example |
|---------------|------------|
| Border | Card with outline |
| Background | Different colored section |
| Shadow | Elevated panel |
| Line | Divider separating groups |

**Implementation:**
```
┌─────────────────────┐
│  Grouped content    │  Border creates region
│  within a card      │
└─────────────────────┘

[  Section A          ]  Background color change
[  (light gray bg)    ]  creates region
[                     ]

[  Section B          ]
[  (white bg)         ]
```

## Principles in Combination

Gestalt principles often work together:

| Combination | Example |
|-------------|---------|
| Proximity + Similarity | Form groups (close + same style) |
| Common Region + Similarity | Card grid (containers + consistent design) |
| Continuity + Common Fate | Carousel (aligned + move together) |
| Figure-Ground + Closure | Modals (foreground + implied container) |

## Application by Component

### Forms
- **Proximity**: Label close to input
- **Common Region**: Fieldset for groups
- **Similarity**: All inputs same style

### Navigation
- **Proximity**: Group related links
- **Similarity**: Consistent link styling
- **Continuity**: Vertical or horizontal alignment

### Cards
- **Common Region**: Border or background
- **Similarity**: Consistent card layout
- **Proximity**: Related content close within

### Data Tables
- **Continuity**: Aligned columns
- **Proximity**: Related rows grouped
- **Common Region**: Row striping or borders

## Evaluation Checklist

- [ ] Related elements are visually grouped (proximity)
- [ ] Similar functions have similar appearance (similarity)
- [ ] Elements follow clear alignment (continuity)
- [ ] Boundaries clearly separate groups (common region)
- [ ] Content is clearly foreground vs background
- [ ] Interactive states change elements together (common fate)

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Equal spacing | No visual grouping | Vary spacing by relationship |
| Inconsistent styling | Confuses relationships | Same function = same appearance |
| Random alignment | Breaks visual flow | Align to grid, consistent margins |
| Weak containers | Ambiguous grouping | Add borders, backgrounds, or spacing |
| Competing focal points | Unclear figure-ground | One primary element per view |

---

**Remember**: Gestalt principles explain how users *already* perceive - design with perception, not against it.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

