---
last_updated: 2026-02-25
status: active
name: visual-hierarchy-design
description: Establish clear visual hierarchy using size, weight, color, position, and spacing. Use when designing layouts or reviewing visual communication clarity.
triggers:
  files: ["**/design/**", "**/layouts/**", "**/components/**"]
  keywords: ["visual hierarchy", "layout", "prominence", "visual weight", "eye flow", "focal point", "information hierarchy"]
allowed-tools: Read, Write, Edit
---

# Visual Hierarchy Design

Visual hierarchy directs user attention through deliberate use of visual properties. Effective hierarchy ensures users see the most important information first and understand content relationships at a glance.

## Core Principle

**Hierarchy = Importance made visible.** Every element should have a clear level of importance relative to others.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Hierarchy Tools

### 1. Size

Size is the strongest hierarchy signal. Larger elements command attention first.

| Level | Use Case | Relative Size |
|-------|----------|---------------|
| Primary | Page title, hero headline | 200-300% of body |
| Secondary | Section headings, key metrics | 150-175% of body |
| Tertiary | Subheadings, labels | 100-125% of body |
| Body | Main content | 100% (base) |
| Supporting | Captions, metadata | 75-85% of body |

### 2. Weight & Contrast

Bold and high-contrast elements appear more important.

**Weight Scale:**
- Primary: Bold (700) + high contrast
- Secondary: Semibold (600) + medium contrast
- Body: Regular (400) + standard contrast
- Supporting: Regular (400) + reduced contrast

### 3. Color

Color draws attention and conveys meaning.

| Purpose | Application |
|---------|-------------|
| Accent | CTAs, key actions, important status |
| Brand | Primary headings, logo, key UI |
| Semantic | Success/error/warning indicators |
| Neutral | Supporting text, borders, backgrounds |

**Rule:** Use accent color sparingly. Overuse dilutes its attention-grabbing power.

### 4. Position

Reading patterns determine visual priority by position.

**F-Pattern (Text-heavy):**
- Top-left: Most important
- Horizontal scan for headings
- Vertical scan down left edge

**Z-Pattern (Visual):**
- Top-left to top-right
- Diagonal to bottom-left
- Left to right across bottom

**Position Priority:**
1. Above the fold
2. Top-left quadrant
3. Center (for modals/dialogs)
4. Right side (for actions)

### 5. Spacing

Whitespace creates grouping and emphasis.

| Spacing Type | Effect |
|--------------|--------|
| Tight | Elements feel related, part of same group |
| Standard | Normal reading rhythm |
| Generous | Emphasis, premium feel, separation |
| Asymmetric | Draws attention to the isolated element |

## Hierarchy Patterns

### Card Hierarchy

```
[         CARD TITLE (Large, Bold)         ]
[ Supporting info (Small, Muted)           ]
[                                          ]
[ Body content at standard size and        ]
[ weight for comfortable reading.          ]
[                                          ]
[   [Secondary Action]  [PRIMARY ACTION]   ]
```

### Dashboard Hierarchy

1. **Page title** - Largest, top-left
2. **Key metrics** - Large numbers, prominent position
3. **Section headers** - Medium, divide content areas
4. **Data labels** - Small, reduced contrast
5. **Data values** - Medium, standard contrast

### Form Hierarchy

1. **Form title** - Clear purpose statement
2. **Section labels** - Group related fields
3. **Field labels** - Consistent, visible
4. **Input text** - High contrast for readability
5. **Helper text** - Small, muted
6. **Submit button** - Maximum prominence

## Evaluation Checklist

When reviewing hierarchy:

- [ ] Can users identify the primary action in <3 seconds?
- [ ] Is there one clear focal point per section?
- [ ] Do related elements share similar visual treatment?
- [ ] Is contrast sufficient for accessibility?
- [ ] Does eye flow follow intended reading order?
- [ ] Are there no more than 4-5 distinct hierarchy levels?

## Anti-Patterns

| Problem | Symptom | Fix |
|---------|---------|-----|
| Flat hierarchy | Everything looks equal | Increase contrast between levels |
| Too many levels | Visual confusion | Consolidate to 3-4 clear levels |
| Competing focal points | User can't decide where to look | Choose one primary element |
| Color overuse | Nothing stands out | Reserve accent for key actions |
| Cramped spacing | Content feels overwhelming | Add whitespace around priority elements |

## Implementation Tips

1. **Squint test**: Blur your vision - important elements should still be visible
2. **5-second test**: Show design briefly - ask what stood out
3. **Grayscale test**: Remove color - hierarchy should still work
4. **Mobile test**: Smallest screen forces clearest hierarchy

---

**Remember**: Good hierarchy feels invisible. Users should naturally flow through content without conscious effort.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

