---
last_updated: 2026-02-25
status: active
name: interface-hierarchy
description: Visual and information hierarchy design - organizing interface elements by importance, guiding user attention. Use for layout prioritization.
triggers:
  files: ["**/layouts/**", "**/hierarchy/**", "**/components/**"]
  keywords: ["visual hierarchy", "information hierarchy", "layout", "priority", "emphasis", "focal point", "scanning", "F-pattern", "Z-pattern"]
allowed-tools: Read, Write, Edit
---

# Interface Hierarchy Skill

Master guide for designing visual and information hierarchy in user interfaces - controlling what users see first and how they scan content.

## Philosophy

**Hierarchy is communication.** Every design decision signals what matters. Size, color, position, and contrast tell users where to look and in what order. Poor hierarchy means users work harder; good hierarchy feels effortless.

**Importance drives design, not aesthetics.** Start with content priority, then apply visual treatment. Beautiful designs with bad hierarchy fail; clear hierarchy with simple visuals succeeds.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Hierarchy Principles

### 1. Visual Weight

Elements "weigh" more based on:

| Factor | High Weight | Low Weight |
|--------|-------------|------------|
| Size | Large | Small |
| Color | Bold/saturated | Muted/desaturated |
| Contrast | High contrast | Low contrast |
| Position | Top/center | Bottom/sides |
| Density | Dense/detailed | Sparse/simple |
| White space | Surrounded by space | Crowded |

### 2. Scanning Patterns

**F-Pattern** (text-heavy pages):
```
████████████████
██████████
████████████████████
██████████
████████
```
- Users scan horizontally, then down left side
- Best for: Articles, search results, feeds

**Z-Pattern** (landing pages):
```
1 ─────────────→ 2
        ↙
3 ─────────────→ 4
```
- Users scan corner to corner
- Best for: Marketing pages, simple layouts

**Layer Cake** (structured content):
```
═══════════════════
  Body text here
═══════════════════
  Body text here
═══════════════════
```
- Users scan headings, dive into relevant sections
- Best for: Documentation, FAQs

### 3. Hierarchy Levels

**Level 1 - Primary**: What users must see
- Largest, boldest, most prominent
- One per screen (hero, main CTA)

**Level 2 - Secondary**: Supporting information
- Clearly subordinate to Level 1
- Section headings, key features

**Level 3 - Tertiary**: Additional details
- Smaller, less prominent
- Metadata, secondary actions

**Level 4 - Quaternary**: Optional/reference
- Smallest, lowest contrast
- Footnotes, timestamps, captions

---

## Typography Hierarchy

### Scale System

```css
/* Recommended type scale (1.25 ratio) */
--text-xs:   0.75rem;   /* 12px - captions */
--text-sm:   0.875rem;  /* 14px - metadata */
--text-base: 1rem;      /* 16px - body */
--text-lg:   1.25rem;   /* 20px - lead text */
--text-xl:   1.563rem;  /* 25px - h4 */
--text-2xl:  1.953rem;  /* 31px - h3 */
--text-3xl:  2.441rem;  /* 39px - h2 */
--text-4xl:  3.052rem;  /* 49px - h1 */
```

### Weight Hierarchy

| Purpose | Weight | Example |
|---------|--------|---------|
| Display/Hero | 700-900 | Page titles, hero text |
| Headings | 600-700 | Section headings |
| Subheadings | 500-600 | Subsections |
| Body | 400 | Paragraph text |
| Captions | 400 | Metadata, labels |

### Spacing Hierarchy

```css
/* Heading spacing (more space above than below) */
h1 { margin-top: 0; margin-bottom: 1.5rem; }
h2 { margin-top: 3rem; margin-bottom: 1rem; }
h3 { margin-top: 2rem; margin-bottom: 0.75rem; }
h4 { margin-top: 1.5rem; margin-bottom: 0.5rem; }
```

---

## Color Hierarchy

### Foreground Colors

```css
/* Text color hierarchy */
--text-primary:   hsl(0 0% 10%);    /* Main content */
--text-secondary: hsl(0 0% 40%);    /* Supporting text */
--text-tertiary:  hsl(0 0% 55%);    /* Metadata, hints */
--text-disabled:  hsl(0 0% 70%);    /* Disabled states */

/* Dark mode */
--text-primary:   hsl(0 0% 95%);
--text-secondary: hsl(0 0% 70%);
--text-tertiary:  hsl(0 0% 55%);
--text-disabled:  hsl(0 0% 40%);
```

### Accent for Emphasis

```css
/* Use accent sparingly for emphasis */
.highlight { color: var(--color-primary); }
.alert     { color: var(--color-danger); }
.success   { color: var(--color-success); }
```

### Background Hierarchy

```css
/* Surface elevation */
--surface-0: hsl(0 0% 100%);  /* Base */
--surface-1: hsl(0 0% 98%);   /* Raised */
--surface-2: hsl(0 0% 95%);   /* Higher */
--surface-3: hsl(0 0% 92%);   /* Highest */
```

---

## Layout Hierarchy

### Grid-Based Priority

```
┌─────────────────────────────────────┐
│ ████████████ LEVEL 1 ████████████   │ Hero/Primary
├─────────────────────────────────────┤
│ ████ L2 ████   ████ L2 ████         │ Secondary
├─────────────────────────────────────┤
│ L3    │ L3    │ L3    │ L3          │ Tertiary
├─────────────────────────────────────┤
│ L4 L4 L4 L4 L4 L4 L4 L4 L4          │ Quaternary
└─────────────────────────────────────┘
```

### Position Priority

**Top > Bottom**: Eyes start at top
**Left > Right**: LTR reading order
**Center > Edges**: Focal point
**Above fold > Below**: Visible without scroll

### White Space as Hierarchy

```
┌──────────────────────────────────────┐
│                                      │
│                                      │
│         IMPORTANT HEADLINE           │  Lots of space =
│                                      │  high importance
│                                      │
├──────────────────────────────────────┤
│ Dense content packed together with   │  Little space =
│ minimal spacing indicates this is    │  lower importance
│ secondary or tertiary information.   │
└──────────────────────────────────────┘
```

---

## Component Hierarchy

### Cards

```
┌─────────────────────────────────────┐
│ [Image/Hero]                        │  L1: Visual
├─────────────────────────────────────┤
│ Card Title                          │  L2: Title
│                                     │
│ Description text that provides      │  L3: Description
│ supporting information...           │
│                                     │
│ ○ Meta  ○ Meta  ○ Meta              │  L4: Metadata
└─────────────────────────────────────┘
```

### Lists

```
┌─────────────────────────────────────┐
│ ● Primary Item Name                 │  L1: Main identifier
│   Supporting description text       │  L2: Description
│   tag • metadata • timestamp        │  L3: Metadata
├─────────────────────────────────────┤
│ ● Primary Item Name                 │
│   Supporting description text       │
│   tag • metadata • timestamp        │
└─────────────────────────────────────┘
```

### Forms

```
┌─────────────────────────────────────┐
│ Form Section Title                  │  L1: Section
│                                     │
│ Field Label *                       │  L2: Label
│ [Input field]                       │  L2: Input
│ Helper text here                    │  L3: Helper
│                                     │
│ Field Label                         │
│ [Input field]                       │
│                                     │
│          [Secondary] [Primary]      │  Actions: R > L
└─────────────────────────────────────┘
```

---

## Establishing Hierarchy

### Process

1. **List all elements** on the page
2. **Rank by importance** (1 = most important)
3. **Assign visual treatment**:
   - Rank 1: Largest, boldest, most space
   - Rank 2-3: Clear subordination
   - Rank 4+: Progressively smaller/lighter
4. **Test by squinting**: Can you still tell what's most important?

### Squint Test

If you squint at your design:
- Can you identify the main element?
- Is there a clear reading path?
- Do elements group logically?

If not, increase contrast between hierarchy levels.

### 3-Second Test

Show design for 3 seconds, then ask:
- What was the main message?
- What action were you supposed to take?

---

## Anti-Patterns

### 1. Everything is Important

```
❌ Bad: All elements same size/weight
TITLE   TITLE   TITLE
TITLE   TITLE   TITLE

✅ Good: Clear primary element
═══════ MAIN TITLE ═══════
  secondary   secondary
```

### 2. Competing Focal Points

```
❌ Bad: Multiple elements demand attention
██████    ██████    ██████
[BIG]     [BIG]     [BIG]

✅ Good: Single primary focal point
     ████████████
        [BIG]
  small    small    small
```

### 3. Inconsistent Levels

```
❌ Bad: Random sizing
HUGE    medium    HUGE
small   ENORMOUS  tiny

✅ Good: Consistent level treatment
Large heading
  Medium subheading
    Small body text
```

### 4. Buried CTAs

```
❌ Bad: Primary action hidden
lots of text lots of text lots
of text lots of text lots of
[button] more text more text

✅ Good: CTA clearly prominent
Clear headline

Supporting text...

  [ PRIMARY ACTION ]
```

---

## Accessibility Considerations

### Color Alone

Never rely on color alone for hierarchy:
```
❌ Bad: Red text for emphasis (colorblind users miss it)
✅ Good: Red text + bold + icon for emphasis
```

### Screen Readers

Use semantic HTML for structural hierarchy:
```html
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

### Focus Order

Tab order should follow visual hierarchy:
1. Primary CTA
2. Secondary actions
3. Navigation
4. Footer

---

## Quick Reference

### Hierarchy Checklist

- [ ] One clear primary element per screen
- [ ] 3-4 distinct hierarchy levels
- [ ] Consistent sizing within levels
- [ ] Adequate contrast between levels
- [ ] White space reinforces importance
- [ ] Passes squint test
- [ ] Passes 3-second test
- [ ] Semantic HTML matches visual hierarchy

### Size Ratios

| Relationship | Minimum Ratio |
|--------------|---------------|
| H1 to body | 2:1 or greater |
| H2 to body | 1.5:1 |
| H3 to body | 1.25:1 |
| Level to level | 1.25:1 |

---

## Summary

**Hierarchy = Priority + Visual treatment**

1. Decide what matters most
2. Make important things look important
3. Create clear separation between levels
4. Test that users perceive the intended order
5. Maintain consistency across the interface

*Good hierarchy disappears. Users just know where to look.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

