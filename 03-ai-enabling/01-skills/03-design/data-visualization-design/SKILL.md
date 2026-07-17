---
last_updated: 2026-02-25
status: active
name: data-visualization-design
description: Design effective charts, graphs, and dashboards that communicate data clearly. Use when creating or reviewing data visualizations.
triggers:
  files: ["**/charts/**", "**/dashboard/**", "**/analytics/**", "**/reports/**"]
  keywords: ["data visualization", "chart", "graph", "dashboard", "data display", "metrics", "KPI", "reporting"]
allowed-tools: Read, Write, Edit
---

# Data Visualization Design

Data visualization translates numbers into visual understanding. Effective visualizations reveal patterns, support decisions, and communicate insights at a glance.

## Core Principle

**Show the data, not the chart.** Visualization should illuminate data, not decorate it.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Chart Selection

### Choose by Data Relationship

| Relationship | Best Chart | Avoid |
|--------------|------------|-------|
| Comparison | Bar, Column | Pie (for many items) |
| Trend over time | Line, Area | Pie, Donut |
| Part-to-whole | Pie, Stacked bar, Treemap | Line |
| Distribution | Histogram, Box plot | Pie |
| Correlation | Scatter, Bubble | Line |
| Ranking | Horizontal bar | Vertical bar (if many items) |
| Geographic | Map, Choropleth | Bar |

### Chart Type Reference

| Chart | Best For | Limit To |
|-------|----------|----------|
| **Bar** | Comparison across categories | 5-15 items |
| **Line** | Change over time | 1-5 series |
| **Pie** | Parts of whole | 2-5 slices |
| **Scatter** | Correlation, distribution | 2-3 variables |
| **Area** | Volume over time | 1-3 series |
| **Table** | Precise values, lookup | Well-organized data |
| **Sparkline** | Compact trends | Context alongside text |

## Visual Encoding

### Data-Ink Ratio

**Maximize data-ink, minimize non-data-ink.**

| Remove | Keep |
|--------|------|
| Decorative gridlines | Subtle reference lines |
| 3D effects | 2D representations |
| Unnecessary borders | Data marks |
| Background images | Whitespace |
| Chart junk | Labels where needed |

### Color Usage

| Purpose | Approach |
|---------|----------|
| Categories | Distinct hues (max 5-7) |
| Sequential data | Light to dark single hue |
| Diverging data | Two hues from center |
| Highlighting | Gray base + accent color |

**Accessibility:**
- Don't rely on color alone
- Ensure 3:1 contrast minimum
- Test for color blindness (8% of men)

### Position & Length

**Most accurate encodings:**
1. Position (most accurate)
2. Length
3. Angle
4. Area
5. Color intensity (least accurate)

**Implication:** Bar charts (position/length) beat pie charts (angle/area) for accuracy.

## Dashboard Design

### Information Hierarchy

```
┌─────────────────────────────────────────────────┐
│ DASHBOARD TITLE                    [Filters]    │
├─────────────────────────────────────────────────┤
│ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐        │
│ │ KPI 1 │ │ KPI 2 │ │ KPI 3 │ │ KPI 4 │        │ ← Summary KPIs (top)
│ └───────┘ └───────┘ └───────┘ └───────┘        │
├─────────────────────────────────────────────────┤
│ ┌────────────────────┐ ┌────────────────────┐  │
│ │                    │ │                    │  │
│ │   Primary Chart    │ │  Secondary Chart   │  │ ← Main visualizations
│ │                    │ │                    │  │
│ └────────────────────┘ └────────────────────┘  │
├─────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────┐│
│ │            Supporting Detail Table          ││ ← Detail (bottom)
│ └─────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

### Dashboard Principles

| Principle | Application |
|-----------|-------------|
| One page | Avoid scrolling for key metrics |
| 5-second rule | Key insight visible immediately |
| Consistent time | Same date range across charts |
| Clear filters | Active filters always visible |
| Mobile consideration | Responsive or separate mobile view |

### KPI Card Design

```
┌──────────────────────────┐
│  Revenue        ⓘ       │ ← Label + info tooltip
│  $1.2M                   │ ← Primary value (large)
│  ↑ 12% vs last month    │ ← Comparison (small, colored)
│  ▁▂▃▅▇ sparkline        │ ← Optional trend
└──────────────────────────┘
```

## Axis & Labels

### Axis Best Practices

| Element | Guideline |
|---------|-----------|
| Start at zero | For bar charts (unless justified) |
| Consistent scale | Same scale for comparisons |
| Axis labels | Clear, concise, with units |
| Tick marks | 4-6 major ticks typical |
| Gridlines | Light, horizontal only usually |

### Label Guidelines

| Type | Placement | When to Use |
|------|-----------|-------------|
| Data labels | On/near data points | Few data points, precise values needed |
| Axis labels | Outside axis | Always |
| Legend | Top or right | Multiple series |
| Annotations | Near relevant data | Call out insights |

### Number Formatting

| Value Type | Format | Example |
|------------|--------|---------|
| Large numbers | Abbreviate | 1.2M, 450K |
| Currency | Symbol + abbreviation | $1.2M |
| Percentages | One decimal max | 12.5% |
| Dates | Contextual | Jan, Q1, 2024 |

## Common Chart Patterns

### Bar Chart

```
Horizontal (for labels):    Vertical (for time):

Product A  ████████ 80      100 │      ▓▓
Product B  █████ 50          75 │   ▓▓ ▓▓ ▓▓
Product C  ███ 30            50 │▓▓ ▓▓ ▓▓ ▓▓
Product D  ██ 20             25 │▓▓ ▓▓ ▓▓ ▓▓
                              0 └─────────────
                                  Q1 Q2 Q3 Q4
```

### Line Chart

```
Revenue Trend
100 │         ╭─────╮
 75 │    ╭────╯     ╰────
 50 │╭───╯
 25 │╯
  0 └─────────────────────
    Jan  Feb  Mar  Apr  May
```

### Pie/Donut

Use sparingly. Limit to 2-5 slices.

```
     ╭───────╮
   ╭─╯       ╰─╮
  │   45%      │    Market Share
  │            │    ─────────────
  │    ╭──╮    │    Category A: 45%
   ╰───│  │───╯     Category B: 30%
       │  │         Category C: 25%
       ╰──╯
```

## Anti-Patterns

### Chart Crimes

| Crime | Problem | Fix |
|-------|---------|-----|
| Truncated axis | Exaggerates differences | Start at zero |
| 3D charts | Distorts perception | Use 2D |
| Too many colors | Cognitive overload | Max 5-7 colors |
| Pie with many slices | Can't compare | Use bar chart |
| Double Y-axis | Confusing comparisons | Separate charts |
| Decorative elements | Distracts from data | Remove chart junk |

### Misleading Practices

| Practice | Misleading Because | Ethical Alternative |
|----------|-------------------|---------------------|
| Cherry-picked range | Hides context | Show full range |
| Cumulative vs rate | Obscures trends | Match to question |
| Inconsistent scales | False comparisons | Same scale |
| Missing context | Inflates importance | Include benchmarks |

## Evaluation Checklist

### Clarity
- [ ] Chart type matches data relationship
- [ ] Key insight visible in 5 seconds
- [ ] Labels are clear and complete
- [ ] Units and scales are explicit

### Accuracy
- [ ] Axes start at appropriate values
- [ ] Scales are consistent
- [ ] No visual distortions (3D, truncation)
- [ ] Data is complete and current

### Accessibility
- [ ] Works without color alone
- [ ] Sufficient contrast
- [ ] Screen reader compatible
- [ ] Alternative text or data table available

### Design
- [ ] High data-ink ratio
- [ ] Consistent visual style
- [ ] Appropriate use of whitespace
- [ ] Mobile responsive

---

**Remember**: The goal is insight, not art. Every visual element should help users understand the data.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

