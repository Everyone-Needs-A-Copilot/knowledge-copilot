---
last_updated: 2026-02-25
status: active
name: color-theory-application
description: Color harmonies, psychological effects, and systematic color application in UI design. Use when making color decisions.
triggers:
  files: ["**/colors.*", "**/palette.*", "**/theme.*", "**/brand.*"]
  keywords: ["color harmony", "color psychology", "complementary colors", "triadic", "analogous", "color temperature", "hue"]
allowed-tools: Read, Write, Edit
---

# Color Theory Application: Deep Expertise Skill

Practical application of color theory principles to digital product design, focusing on harmonies, psychology, and systematic implementation.

## Color Theory Fundamentals

### Color Properties

**Hue**: The pure color (red, blue, green, etc.) - position on color wheel (0-360°)
**Saturation**: Color intensity (0% = gray, 100% = pure color)
**Lightness/Value**: Brightness level (0% = black, 100% = white)
**Temperature**: Perceived warmth or coolness

### The Color Wheel

The color wheel organizes colors by their relationship to each other.

**Primary Colors**: Red, Yellow, Blue (traditional) or Red, Green, Blue (additive/screen)
**Secondary Colors**: Created by mixing primaries (Orange, Green, Purple)
**Tertiary Colors**: Primary + adjacent secondary (Red-Orange, Blue-Green, etc.)


## Define Done

- [ ] Design tokens/components follow system conventions
- [ ] Visual consistency maintained across all instances
- [ ] Documentation updated to reflect any changes
- [ ] Accessibility requirements preserved in implementation

## Color Harmonies

### Monochromatic

**Definition**: Single hue with variations in saturation and lightness.

**Use Cases:**
- Minimalist interfaces
- Focus on content over decoration
- Subtle, sophisticated aesthetics

**Implementation:**
```css
:root {
  /* Blue monochromatic */
  --color-primary-50: hsl(210, 100%, 97%);
  --color-primary-100: hsl(210, 100%, 94%);
  --color-primary-200: hsl(210, 100%, 85%);
  --color-primary-300: hsl(210, 100%, 75%);
  --color-primary-400: hsl(210, 100%, 65%);
  --color-primary-500: hsl(210, 100%, 50%);
  --color-primary-600: hsl(210, 100%, 40%);
  --color-primary-700: hsl(210, 100%, 30%);
  --color-primary-800: hsl(210, 100%, 20%);
  --color-primary-900: hsl(210, 100%, 10%);
}
```

### Analogous

**Definition**: Adjacent colors on the wheel (within 30-60°).

**Use Cases:**
- Natural, harmonious designs
- Comfortable, unified interfaces
- Brand extensions

**Implementation:**
```css
:root {
  /* Blue-centered analogous (180° ± 30°) */
  --color-primary: hsl(210, 80%, 50%);    /* Blue */
  --color-secondary: hsl(180, 70%, 45%);  /* Cyan */
  --color-tertiary: hsl(240, 70%, 55%);   /* Indigo */
}
```

### Complementary

**Definition**: Opposite colors on the wheel (180° apart).

**Use Cases:**
- High contrast, attention-grabbing
- Call-to-action emphasis
- Sports, entertainment

**Implementation:**
```css
:root {
  /* Blue + Orange (complementary) */
  --color-primary: hsl(210, 100%, 50%);   /* Blue */
  --color-accent: hsl(30, 100%, 50%);     /* Orange */
}
```

### Split-Complementary

**Definition**: Base color + two colors adjacent to its complement.

**Use Cases:**
- High contrast with more flexibility
- Dynamic but balanced designs
- Marketing materials

**Implementation:**
```css
:root {
  /* Blue + Yellow-Orange + Red-Orange */
  --color-primary: hsl(210, 100%, 50%);   /* Blue */
  --color-accent-1: hsl(45, 100%, 55%);   /* Yellow-Orange */
  --color-accent-2: hsl(15, 100%, 55%);   /* Red-Orange */
}
```

### Triadic

**Definition**: Three colors equally spaced (120° apart).

**Use Cases:**
- Vibrant, balanced designs
- Playful interfaces
- Children's products

**Implementation:**
```css
:root {
  /* Primary triad */
  --color-primary: hsl(210, 85%, 50%);    /* Blue */
  --color-secondary: hsl(330, 85%, 50%);  /* Magenta */
  --color-tertiary: hsl(90, 85%, 45%);    /* Green */
}
```

### Tetradic (Rectangle)

**Definition**: Four colors in two complementary pairs.

**Use Cases:**
- Complex, rich designs
- Multiple content categories
- Media-heavy interfaces

**Implementation:**
```css
:root {
  --color-primary: hsl(210, 80%, 50%);    /* Blue */
  --color-secondary: hsl(30, 80%, 50%);   /* Orange */
  --color-tertiary: hsl(150, 70%, 45%);   /* Teal */
  --color-quaternary: hsl(330, 70%, 55%); /* Pink */
}
```

## Color Psychology

### Emotional Associations

| Color | Positive | Negative | UI Use |
|-------|----------|----------|--------|
| **Red** | Energy, passion, urgency | Danger, aggression | CTAs, errors, sales |
| **Orange** | Warmth, creativity, optimism | Caution, cheap | Warnings, highlights |
| **Yellow** | Happiness, optimism, attention | Anxiety, caution | Notifications, emphasis |
| **Green** | Growth, health, success | Envy, inexperience | Success states, eco |
| **Blue** | Trust, calm, professional | Cold, distant | Primary UI, corporate |
| **Purple** | Luxury, creativity, wisdom | Artificial, immature | Premium features |
| **Pink** | Playful, romantic, modern | Immature, weak | Fashion, lifestyle |
| **Brown** | Reliable, earthy, organic | Dull, old | Natural products |
| **Gray** | Neutral, professional | Boring, indecisive | Backgrounds, UI |
| **Black** | Elegant, powerful, modern | Death, evil | Luxury, contrast |
| **White** | Clean, pure, simple | Sterile, empty | Backgrounds, space |

### Industry Color Conventions

| Industry | Primary Colors | Rationale |
|----------|----------------|-----------|
| Finance | Blue, Navy | Trust, stability |
| Healthcare | Blue, Green, White | Clean, healing, trust |
| Technology | Blue, Cyan | Innovation, reliability |
| Food | Red, Orange, Yellow | Appetite, warmth |
| Eco/Organic | Green, Brown | Nature, earth |
| Luxury | Black, Gold, Purple | Elegance, wealth |
| Children | Primary colors | Energy, playfulness |
| Legal | Navy, Gray | Authority, stability |

## Color Temperature

### Warm Colors

**Hue Range**: 0° - 60° (Red → Yellow)
**Characteristics**: Advancing, energetic, attention-grabbing
**UI Applications**: CTAs, notifications, warnings

### Cool Colors

**Hue Range**: 180° - 270° (Cyan → Blue → Purple)
**Characteristics**: Receding, calm, professional
**UI Applications**: Backgrounds, primary UI, content areas

### Temperature in Practice

```css
:root {
  /* Warm accent for action */
  --color-action: hsl(15, 90%, 55%);      /* Warm orange */
  --color-action-hover: hsl(15, 90%, 45%);

  /* Cool primary for stability */
  --color-primary: hsl(210, 80%, 50%);    /* Cool blue */
  --color-primary-hover: hsl(210, 80%, 40%);

  /* Neutral temperature for balance */
  --color-neutral: hsl(220, 10%, 50%);    /* Cool gray */
}
```

## Systematic Color Application

### 60-30-10 Rule

**60%**: Dominant color (backgrounds, large areas)
**30%**: Secondary color (supporting elements)
**10%**: Accent color (highlights, CTAs)

```css
:root {
  /* 60% - Dominant */
  --color-bg-primary: hsl(220, 15%, 98%);
  --color-bg-secondary: hsl(220, 15%, 94%);

  /* 30% - Secondary */
  --color-surface: hsl(0, 0%, 100%);
  --color-text-primary: hsl(220, 25%, 15%);

  /* 10% - Accent */
  --color-accent: hsl(210, 100%, 50%);
  --color-accent-hover: hsl(210, 100%, 40%);
}
```

### Color Roles in UI

| Role | Description | Example |
|------|-------------|---------|
| **Primary** | Main brand/action color | Buttons, links |
| **Secondary** | Supporting actions | Secondary buttons |
| **Accent** | Highlights, emphasis | Badges, indicators |
| **Neutral** | Backgrounds, text | Grays |
| **Success** | Positive feedback | Confirmations |
| **Warning** | Caution states | Alerts |
| **Error** | Negative feedback | Validation errors |
| **Info** | Informational | Tooltips, notices |

### Semantic Color System

```css
:root {
  /* Brand */
  --color-brand-primary: hsl(210, 100%, 50%);
  --color-brand-secondary: hsl(270, 70%, 55%);

  /* Feedback */
  --color-success: hsl(145, 65%, 42%);
  --color-success-bg: hsl(145, 65%, 95%);
  --color-warning: hsl(40, 95%, 50%);
  --color-warning-bg: hsl(40, 95%, 95%);
  --color-error: hsl(0, 75%, 55%);
  --color-error-bg: hsl(0, 75%, 97%);
  --color-info: hsl(210, 80%, 55%);
  --color-info-bg: hsl(210, 80%, 97%);

  /* Surfaces */
  --color-surface-primary: hsl(0, 0%, 100%);
  --color-surface-secondary: hsl(220, 15%, 97%);
  --color-surface-tertiary: hsl(220, 15%, 94%);

  /* Text */
  --color-text-primary: hsl(220, 25%, 10%);
  --color-text-secondary: hsl(220, 15%, 40%);
  --color-text-tertiary: hsl(220, 10%, 55%);
  --color-text-disabled: hsl(220, 10%, 70%);

  /* Borders */
  --color-border-primary: hsl(220, 15%, 85%);
  --color-border-secondary: hsl(220, 10%, 90%);
}
```

## Color for State Communication

### Interactive States

```css
.button-primary {
  /* Default */
  background: var(--color-brand-primary);

  /* Hover - darken 10% */
  &:hover {
    background: hsl(210, 100%, 45%);
  }

  /* Active - darken 15% */
  &:active {
    background: hsl(210, 100%, 40%);
  }

  /* Focus - add ring */
  &:focus-visible {
    outline: 2px solid var(--color-brand-primary);
    outline-offset: 2px;
  }

  /* Disabled - desaturate */
  &:disabled {
    background: hsl(210, 20%, 70%);
    cursor: not-allowed;
  }
}
```

### Status Indicators

```css
.status {
  /* Success */
  &.success {
    color: var(--color-success);
    background: var(--color-success-bg);
    border-left: 4px solid var(--color-success);
  }

  /* Warning */
  &.warning {
    color: hsl(25, 90%, 35%);
    background: var(--color-warning-bg);
    border-left: 4px solid var(--color-warning);
  }

  /* Error */
  &.error {
    color: var(--color-error);
    background: var(--color-error-bg);
    border-left: 4px solid var(--color-error);
  }
}
```

## Color Manipulation

### HSL Adjustments

```javascript
// Lighten a color
function lighten(hsl, amount) {
  const [h, s, l] = parseHSL(hsl);
  return `hsl(${h}, ${s}%, ${Math.min(100, l + amount)}%)`;
}

// Darken a color
function darken(hsl, amount) {
  const [h, s, l] = parseHSL(hsl);
  return `hsl(${h}, ${s}%, ${Math.max(0, l - amount)}%)`;
}

// Saturate a color
function saturate(hsl, amount) {
  const [h, s, l] = parseHSL(hsl);
  return `hsl(${h}, ${Math.min(100, s + amount)}%, ${l}%)`;
}

// Desaturate a color
function desaturate(hsl, amount) {
  const [h, s, l] = parseHSL(hsl);
  return `hsl(${h}, ${Math.max(0, s - amount)}%, ${l}%)`;
}

// Shift hue
function shiftHue(hsl, degrees) {
  const [h, s, l] = parseHSL(hsl);
  return `hsl(${(h + degrees + 360) % 360}, ${s}%, ${l}%)`;
}
```

### Creating Color Variations

```css
:root {
  --color-primary: hsl(210, 100%, 50%);

  /* Auto-generate variations */
  --color-primary-light: hsl(210, 100%, 65%);
  --color-primary-lighter: hsl(210, 100%, 80%);
  --color-primary-lightest: hsl(210, 100%, 95%);
  --color-primary-dark: hsl(210, 100%, 40%);
  --color-primary-darker: hsl(210, 100%, 30%);
  --color-primary-darkest: hsl(210, 100%, 15%);

  /* Muted version */
  --color-primary-muted: hsl(210, 40%, 55%);
}
```

## Practical Application Patterns

### Creating a Harmonious Palette

```javascript
function createPalette(baseHue, harmony = 'analogous') {
  const harmonies = {
    monochromatic: [0],
    analogous: [-30, 0, 30],
    complementary: [0, 180],
    splitComplementary: [0, 150, 210],
    triadic: [0, 120, 240],
    tetradic: [0, 90, 180, 270]
  };

  return harmonies[harmony].map(offset => ({
    hue: (baseHue + offset + 360) % 360,
    color: `hsl(${(baseHue + offset + 360) % 360}, 70%, 50%)`
  }));
}

// Usage
const palette = createPalette(210, 'splitComplementary');
// Results in blue (210°), yellow-green (0°), red-orange (60°)
```

### Balancing Visual Weight

Saturated colors appear heavier and more prominent. Balance by:
- Using saturated colors for smaller elements
- Using desaturated colors for larger areas
- Adjusting lightness to compensate

```css
/* Heavy element - smaller, saturated */
.badge {
  background: hsl(210, 100%, 50%);
  padding: 0.25rem 0.5rem;
}

/* Light element - larger, desaturated */
.card {
  background: hsl(210, 20%, 97%);
  padding: 2rem;
}
```

## Anti-Patterns

### Common Color Mistakes

**Using too many colors:**
```css
/* Bad - visual chaos */
.ui {
  --color-1: red;
  --color-2: blue;
  --color-3: green;
  --color-4: purple;
  --color-5: orange;
  --color-6: pink;
}

/* Good - focused palette */
.ui {
  --color-primary: hsl(210, 100%, 50%);
  --color-secondary: hsl(210, 30%, 30%);
  --color-accent: hsl(30, 100%, 50%);
}
```

**Clashing colors without purpose:**
```css
/* Bad - visual tension */
.alert {
  background: lime;
  color: magenta;
}

/* Good - purposeful contrast */
.alert {
  background: hsl(145, 65%, 95%);
  color: hsl(145, 65%, 25%);
}
```

**Ignoring color roles:**
```css
/* Bad - success color for errors */
.error {
  color: green; /* Confusing! */
}

/* Good - appropriate semantic color */
.error {
  color: var(--color-error);
}
```

## Summary

Effective color theory application requires:

1. **Choose appropriate harmonies** based on design goals
2. **Apply the 60-30-10 rule** for balance
3. **Use color psychology** aligned with brand and audience
4. **Create semantic color systems** for maintainability
5. **Consider temperature** for emotional impact
6. **Maintain consistency** through systematic application
7. **Test for accessibility** across all color choices

---

**When to use this skill:**
- Selecting brand color palettes
- Creating color systems for design systems
- Balancing colors in UI layouts
- Communicating through color (states, feedback)
- Ensuring color harmony across interfaces


## Quality Tests

### Consistency Test
- New work uses existing tokens and patterns, not custom values
- **PASS:** All colors, spacing, and type sizes reference design tokens
- **FAIL:** Hard-coded values or one-off styles introduced

### Scalability Test
- Patterns work across all supported contexts and screen sizes
- **PASS:** Component tested in smallest and largest supported viewport
- **FAIL:** Pattern only works at one breakpoint or in one context

