---
last_updated: 2026-02-25
status: active
name: data-visualization
description: Design effective visualizations that communicate research findings clearly. Choose appropriate chart types, apply visual hierarchy, and tell data stories. Use when presenting quantitative or qualitative findings to stakeholders.
triggers:
  keywords: ["data", "visualization", "design", "effective", "visualizations", "communicate", "research", "findings", "clearly", "choose"]
allowed-tools: Read, Write, Edit
---

# Data Visualization

## Overview

Create visualizations that communicate insights, not just display data. Choose the right chart for the message, design for clarity, and tell a story. The goal is understanding, not decoration.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Define the Message

Before choosing a chart, know what you're saying:

| Message Type | What You're Showing | Example |
|--------------|---------------------|---------|
| **Comparison** | How things differ | "Q3 sales by region" |
| **Trend** | How things change | "User growth over time" |
| **Distribution** | How data spreads | "Age distribution of users" |
| **Composition** | What makes up the whole | "Revenue by product line" |
| **Relationship** | How variables connect | "Price vs. sales volume" |

```markdown
## Visualization Brief

**Audience:** [Who will see this]
**Key message:** [One sentence takeaway]
**Message type:** [Comparison/Trend/Distribution/Composition/Relationship]
**Context:** [Where it will appear — slide, report, dashboard]
**Action desired:** [What should viewer do with this information]
```

### Step 2: Choose the Right Chart

Match chart to message:

| Message | Best Charts | Avoid |
|---------|-------------|-------|
| **Compare values** | Bar chart, Dot plot | Pie chart (hard to compare) |
| **Show trend** | Line chart, Area chart | Bar chart (implies discrete) |
| **Show distribution** | Histogram, Box plot | Pie chart (not for distribution) |
| **Show composition** | Stacked bar, Treemap | 3D pie (distorts) |
| **Show relationship** | Scatter plot, Heat map | Line chart (implies sequence) |
| **Show part-to-whole** | Stacked bar, Waffle | Pie (limit to 5 slices max) |

```markdown
## Chart Selection

**Primary chart:** [Chart type]
**Rationale:** [Why this chart fits the message]
**Alternative considered:** [Other option and why not chosen]
```

### Step 3: Design for Clarity

Apply visual hierarchy principles:

| Principle | Application |
|-----------|-------------|
| **Maximize data-ink ratio** | Remove non-essential elements |
| **Use pre-attentive attributes** | Color, size, position for emphasis |
| **Label directly** | Labels on data, not in legend when possible |
| **Order meaningfully** | Largest to smallest, or logical order |
| **Align to baseline** | Use consistent baselines for comparison |

```markdown
## Design Decisions

### Elements to Include
- [ ] Clear title (states the insight)
- [ ] Axis labels
- [ ] Data labels (where needed)
- [ ] Source attribution
- [ ] Legend (if multiple series)

### Elements to Remove
- [ ] Gridlines (or reduce to subtle)
- [ ] Redundant borders
- [ ] Decorative elements
- [ ] 3D effects
- [ ] Excessive tick marks
```

### Step 4: Choose Colors Purposefully

Color should have meaning:

| Color Use | Guideline |
|-----------|-----------|
| **Categorical** | Distinct hues, max 5-7 categories |
| **Sequential** | Single hue, light to dark |
| **Diverging** | Two hues from neutral center |
| **Highlighting** | One emphasis color, gray for context |
| **Accessibility** | Color-blind safe palettes |

```markdown
## Color Specification

**Palette type:** [Categorical/Sequential/Diverging]
**Colors:**
- Primary: [Hex code] — [What it represents]
- Secondary: [Hex code] — [What it represents]
- Highlight: [Hex code] — [What draws attention]
- Neutral: [Hex code] — [Background, supporting]

**Accessibility check:** [Pass/Fail colorblind simulation]
```

### Step 5: Write Effective Titles and Labels

Titles should state the insight:

| Element | Good Practice | Example |
|---------|---------------|---------|
| **Title** | States the finding | "Mobile users convert 2x better than desktop" |
| **Subtitle** | Provides context | "Q3 2024 trial-to-paid conversion by device" |
| **Axis labels** | Clear units | "Revenue ($M)" not just "Revenue" |
| **Data labels** | Only when needed | On bars when precise values matter |
| **Annotations** | Call out key points | Arrow to inflection point |

```markdown
## Text Elements

**Title:** [Insight-driven title]
**Subtitle:** [Context and scope]
**Annotations:**
- [Point A]: "[What to notice]"
- [Point B]: "[What to notice]"
**Source:** [Data source and date]
```

### Step 6: Validate Effectiveness

Check before sharing:

```markdown
## Visualization Checklist

### Clarity
- [ ] Key message apparent in <5 seconds
- [ ] No explanation needed for chart type
- [ ] Labels readable without zooming
- [ ] Colors distinguishable

### Accuracy
- [ ] Axes start at appropriate point (usually 0)
- [ ] Scale not truncated misleadingly
- [ ] Data accurately represented
- [ ] Totals add up (for compositions)

### Accessibility
- [ ] Works in black and white
- [ ] Color-blind friendly
- [ ] Adequate contrast
- [ ] Alt text available

### Context
- [ ] Source cited
- [ ] Time period clear
- [ ] Sample size noted (if relevant)
```

## Chart Type Reference

### Comparison Charts

**Bar Chart**
- Best for: Comparing categories
- Orientation: Horizontal for long labels, vertical for time
- Order: Largest to smallest (usually)
- Avoid: Too many categories (>12)

**Grouped Bar**
- Best for: Comparing sub-categories within categories
- Limit: 2-3 groups per cluster
- Alternative: Small multiples if too crowded

**Dot Plot**
- Best for: Precise comparisons, many categories
- Better than bar when: Space is tight, precision matters

### Trend Charts

**Line Chart**
- Best for: Continuous time series
- Multiple lines: Max 4-5 before confusion
- Labeling: Direct labels on lines, not legend

**Area Chart**
- Best for: Emphasizing magnitude over time
- Stacked: Shows part-to-whole over time
- Caution: Stacked areas hard to compare middle layers

### Distribution Charts

**Histogram**
- Best for: Single variable distribution
- Bins: Choose meaningful intervals
- Comparison: Overlapping histograms hard — use small multiples

**Box Plot**
- Best for: Comparing distributions across groups
- Shows: Median, quartiles, outliers
- Audience: Requires statistical literacy

### Composition Charts

**Stacked Bar**
- Best for: Part-to-whole over categories
- Total: Should be meaningful
- Limit: 5-7 segments max

**Treemap**
- Best for: Hierarchical part-to-whole
- Labeling: Small segments hard to label
- Alternative: Table if precision needed

### Relationship Charts

**Scatter Plot**
- Best for: Two continuous variables
- Enhancements: Size for third variable, color for category
- Trend line: Add only if relationship is the message

**Heat Map**
- Best for: Patterns in matrix data
- Color: Sequential or diverging from meaningful center
- Labeling: Values in cells when precision needed

## Examples

**Output: Visualization Specification**

```markdown
# Visualization: Conversion Funnel Analysis

## Brief
**Audience:** Product leadership
**Key message:** Mobile drop-off at checkout is costing us 40% of potential revenue
**Message type:** Comparison + Composition
**Context:** Quarterly business review slide
**Action desired:** Prioritize mobile checkout redesign

---

## Chart Design

### Primary Chart: Horizontal Funnel

```
                    Sessions   Conversion   Drop-off
Mobile
Visit              100,000      100%         —
Add to Cart         45,000       45%        55%
Checkout Start      22,000       22%        51%  ← Problem
Purchase             8,000        8%        64%  ← Biggest drop

Desktop
Visit               80,000      100%         —
Add to Cart         40,000       50%        50%
Checkout Start      28,000       35%        30%
Purchase            19,000       24%        32%
```

### Visual Specifications

**Layout:** Horizontal bar funnel, mobile above desktop
**Highlight:** Mobile checkout and purchase bars in red
**Annotation:** Arrow pointing to mobile drop-off with "64% abandon at checkout"

### Colors
- Mobile bars: #1E88E5 (blue), checkout/purchase: #E53935 (red highlight)
- Desktop bars: #757575 (gray for context)
- Background: White
- Text: #212121 (near black)

### Text
**Title:** "Mobile checkout abandonment is our biggest conversion leak"
**Subtitle:** "Q3 2024 funnel by device type, n=180,000 sessions"
**Annotation:** "64% of mobile users abandon at checkout — 3x desktop rate"
**Source:** "Google Analytics, July-Sept 2024"

---

## Supporting Chart: Revenue Impact

```
Revenue Lost to Mobile Abandonment

             Desktop    Mobile
Completed    $1.9M      $0.8M
Lost         $0.8M      $1.2M  ← 40% of potential
```

**Chart type:** Stacked horizontal bar
**Message:** Mobile lost revenue ($1.2M) exceeds mobile actual revenue ($0.8M)

---

## Validation

### Clarity
- [x] Message clear: mobile checkout is broken
- [x] No chart explanation needed
- [x] Labels readable
- [x] Red highlight draws eye to problem

### Accuracy
- [x] Bars start at 0
- [x] Scale consistent
- [x] Numbers verified
- [x] Revenue calculated correctly

### Accessibility
- [x] Works in grayscale (red is darker)
- [x] Color-blind checked (red/blue safe)
- [x] Adequate contrast
- [x] Alt text: "Funnel chart showing 64% mobile checkout abandonment vs 32% desktop"
```



## Quality Tests

### Evidence Test
- Every finding cites specific data, quotes, or observations
- **PASS:** Each insight traces back to a named source or data point
- **FAIL:** Findings use vague language like 'it seems' or 'generally' without evidence

### Completeness Test
- All relevant dimensions of the framework have been considered
- **PASS:** Analysis addresses each framework dimension, noting gaps where data is unavailable
- **FAIL:** Key dimensions skipped without acknowledgment

### Actionability Test
- Recommendations are specific enough to act on immediately
- **PASS:** Each recommendation names who should do what by when
- **FAIL:** Recommendations are vague ('improve communication') without concrete actions

## Guidelines

1. **One chart, one message** — Don't overload with multiple points
2. **Title is the takeaway** — Viewer should understand without reading chart
3. **Less is more** — Remove everything that doesn't serve the message
4. **Test on audience** — Show to someone unfamiliar, check understanding
5. **Default to simple** — Bar and line charts work; exotic charts confuse
6. **Consider the medium** — Slide, report, and dashboard have different needs

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Pie charts for comparison | Hard to compare angles | Bar chart |
| 3D effects | Distorts perception | Flat 2D |
| Dual y-axes | Misleading correlations | Separate charts |
| Rainbow colors | No meaning, hard to read | Purposeful palette |
| Truncated axes | Exaggerates differences | Start at 0 (or annotate) |
| Too many data points | Can't see signal | Aggregate or filter |
| Decorative elements | Distract from data | Remove chartjunk |
| Legend instead of labels | Requires eye movement | Direct labels |

## Tool Recommendations

| Use Case | Recommended Tools |
|----------|-------------------|
| Quick charts | Google Sheets, Excel |
| Polished slides | Figma, Canva, Google Slides |
| Interactive dashboards | Looker, Metabase, Tableau |
| Custom visualizations | D3.js, Observable |
| Research reports | RAWGraphs, Flourish |

## References

- statistical-analysis: Data preparation for visualization
- pattern-recognition: Finding patterns to visualize
- research-design: Context for research visualizations
- Tufte: The Visual Display of Quantitative Information
