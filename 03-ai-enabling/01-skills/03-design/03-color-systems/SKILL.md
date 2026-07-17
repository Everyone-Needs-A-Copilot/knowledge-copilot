---
last_updated: 2026-02-25
status: active
name: color-systems
description: Color theory and accessibility - palettes, contrast, color blindness, semantic colors. Use for color design.
triggers:
  files: ["**/colors.*", "**/palette.*", "**/theme.*"]
  keywords: ["color palette", "contrast ratio", "color theory", "accessibility", "color blindness", "WCAG", "semantic color", "HSL"]
allowed-tools: Read, Write, Edit
---

# Color Systems: Deep Expertise Skill

Comprehensive guide to designing, implementing, and maintaining accessible color systems for digital products.

## Table of Contents

1. [Color Theory Fundamentals](#color-theory-fundamentals)
2. [Color Models & Formats](#color-models--formats)
3. [Building Color Scales](#building-color-scales)
4. [Accessibility & Contrast](#accessibility--contrast)
5. [Color Blindness Considerations](#color-blindness-considerations)
6. [Semantic Color Naming](#semantic-color-naming)
7. [Dark Mode Color Systems](#dark-mode-color-systems)
8. [Color in Data Visualization](#color-in-data-visualization)
9. [Brand Color Adaptation](#brand-color-adaptation)
10. [Color Tools & Resources](#color-tools--resources)
11. [Tailwind Color Configuration](#tailwind-color-configuration)
12. [Anti-Patterns & Common Mistakes](#anti-patterns--common-mistakes)

---


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Color Theory Fundamentals

### Primary Color Concepts

**Hue**: The pure color without tint or shade (0-360° on color wheel)
**Saturation**: Color intensity (0% = grayscale, 100% = pure color)
**Lightness**: Amount of light (0% = black, 50% = pure color, 100% = white)
**Value**: Perceived brightness of a color

### Color Harmonies

**Monochromatic**: Single hue with variations in lightness/saturation
- Use: Minimalist designs, focus on content
- Example: Blue-50 to Blue-900

**Analogous**: Adjacent colors on color wheel (30° apart)
- Use: Natural, harmonious interfaces
- Example: Blue, Cyan, Teal

**Complementary**: Opposite colors on wheel (180° apart)
- Use: High contrast, call-to-action emphasis
- Example: Blue + Orange

**Triadic**: Three colors equally spaced (120° apart)
- Use: Vibrant, balanced designs
- Example: Red, Yellow, Blue

**Split-Complementary**: Base + two adjacent to complement
- Use: High contrast with more nuance
- Example: Blue + Red-Orange + Yellow-Orange

**Tetradic**: Two complementary pairs
- Use: Rich, complex designs
- Example: Blue + Orange + Green + Red

### Color Psychology

| Color | Associations | Use Cases |
|-------|--------------|-----------|
| **Red** | Urgency, danger, passion | Errors, alerts, CTAs |
| **Orange** | Energy, warning, creativity | Warnings, notifications |
| **Yellow** | Optimism, caution | Highlights, warnings |
| **Green** | Success, growth, safety | Success states, confirmations |
| **Blue** | Trust, calm, professional | Primary actions, corporate |
| **Purple** | Luxury, creativity | Premium features, branding |
| **Pink** | Playful, modern | Consumer apps, lifestyle |
| **Gray** | Neutral, professional | Backgrounds, disabled states |

**Cultural Considerations**:
- Red: Luck in China, danger in West
- White: Purity in West, mourning in East
- Yellow: Caution in West, sacred in India
- Green: Nature universally, but varies in intensity

---

## Color Models & Formats

### RGB (Red, Green, Blue)

**Use**: Screen displays, additive color mixing
**Format**: `rgb(255, 99, 71)` or `rgba(255, 99, 71, 0.8)`
**Range**: 0-255 per channel

```css
.element {
  color: rgb(59, 130, 246);
  background: rgba(59, 130, 246, 0.1);
}
```

**Pros**:
- Native to displays
- Direct hardware mapping
- Efficient rendering

**Cons**:
- Not intuitive for humans
- Hard to adjust lightness
- Poor for color manipulation

### HEX (Hexadecimal)

**Use**: Web, compact notation
**Format**: `#FF6347` or `#FF634780` (with alpha)
**Range**: 00-FF per channel

```css
.element {
  color: #3B82F6;
  background: #3B82F61A; /* 10% opacity */
}
```

**Pros**:
- Compact
- Universal web support
- Copy-paste friendly

**Cons**:
- Not human-readable
- Hard to manipulate
- No intuitive adjustments

### HSL (Hue, Saturation, Lightness)

**Use**: Human-readable, easy manipulation
**Format**: `hsl(211, 92%, 60%)` or `hsla(211, 92%, 60%, 0.8)`
**Range**: H: 0-360°, S: 0-100%, L: 0-100%

```css
.element {
  /* Base color */
  color: hsl(211, 92%, 60%);

  /* Easy variations */
  color: hsl(211, 92%, 70%); /* Lighter */
  color: hsl(211, 92%, 50%); /* Darker */
  color: hsl(211, 50%, 60%); /* Less saturated */
}
```

**Pros**:
- Intuitive adjustments
- Easy to create scales
- Human-readable
- Perfect for theming

**Cons**:
- Perceptual non-uniformity
- Not as precise as LAB
- Browser rendering variations

### HSB/HSV (Hue, Saturation, Brightness/Value)

**Use**: Design tools (Figma, Sketch)
**Format**: Similar to HSL but different lightness model
**Range**: H: 0-360°, S: 0-100%, B: 0-100%

**Key Difference from HSL**:
- HSL: 50% lightness = pure color
- HSB: 100% brightness + 100% saturation = pure color

### LAB/LCH (Perceptually Uniform)

**Use**: Accurate color manipulation, gradients
**Format**: `lab(60% 40 -20)` or `lch(60% 50 270)`
**Range**: L: 0-100, a/b: -128 to 127, C: 0-150, H: 0-360°

```css
.element {
  /* More perceptually accurate than HSL */
  color: lch(60% 50 270);

  /* Smooth gradients */
  background: linear-gradient(
    in lch,
    lch(60% 50 270),
    lch(80% 50 90)
  );
}
```

**Pros**:
- Perceptually uniform
- Accurate color distance
- Better gradients
- Professional color work

**Cons**:
- Limited browser support (CSS Color Level 4)
- Less familiar
- Requires polyfills for older browsers

### When to Use Each

| Task | Recommended Format |
|------|-------------------|
| **Static colors** | HEX (compact) |
| **Dynamic manipulation** | HSL (intuitive) |
| **Opacity variations** | RGBA or HSLA |
| **Color scales** | HSL or LCH |
| **Accurate gradients** | LCH |
| **Design tools** | HSB |
| **Print** | CMYK |
| **Professional color work** | LAB |

---

## Building Color Scales

### The Challenge

Creating a color scale isn't just about adjusting lightness:
- Perceptual uniformity (equal visual steps)
- Contrast requirements (WCAG compliance)
- Saturation curve (pure colors in middle)
- Hue shifting (more natural transitions)

### Method 1: Linear HSL (Simple)

```javascript
// Basic scale generation
function generateScale(baseHue, baseSat, steps = 10) {
  const scale = {};
  for (let i = 0; i < steps; i++) {
    const lightness = 95 - (i * 9); // 95% to 5%
    scale[(i + 1) * 100] = `hsl(${baseHue}, ${baseSat}%, ${lightness}%)`;
  }
  return scale;
}

// Usage
const blueScale = generateScale(211, 92, 10);
// Result:
// 100: hsl(211, 92%, 95%)
// 200: hsl(211, 92%, 86%)
// ...
// 900: hsl(211, 92%, 14%)
```

**Issues**:
- Middle colors too bright or dull
- Not perceptually uniform
- Poor contrast progression

### Method 2: Easing Curve (Better)

```javascript
// Easing function for non-linear distribution
function easeInOutCubic(t) {
  return t < 0.5
    ? 4 * t * t * t
    : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function generateScaleWithEasing(baseHue, baseSat, steps = 10) {
  const scale = {};
  for (let i = 0; i < steps; i++) {
    const t = i / (steps - 1);
    const eased = easeInOutCubic(t);
    const lightness = 95 - (eased * 85); // 95% to 10%
    scale[(i + 1) * 100] = `hsl(${baseHue}, ${baseSat}%, ${lightness}%)`;
  }
  return scale;
}
```

**Improvements**:
- More steps in mid-range
- Better visual distribution
- Smoother transitions

### Method 3: Saturation Curve (Professional)

```javascript
function generateProfessionalScale(baseHue, steps = 10) {
  const scale = {};
  const lightnessSteps = [95, 90, 80, 70, 60, 50, 40, 30, 20, 10];
  const saturationSteps = [20, 30, 50, 70, 85, 92, 85, 75, 65, 50];

  for (let i = 0; i < steps; i++) {
    const lightness = lightnessSteps[i];
    const saturation = saturationSteps[i];
    scale[(i + 1) * 100] = `hsl(${baseHue}, ${saturation}%, ${lightness}%)`;
  }
  return scale;
}
```

**Why this works**:
- Lower saturation at extremes (more neutral)
- Higher saturation in middle (vibrant)
- Natural appearance
- Better for UI backgrounds

### Method 4: Hue Shifting (Advanced)

```javascript
function generateScaleWithHueShift(baseHue, steps = 10) {
  const scale = {};
  const lightnessSteps = [95, 90, 80, 70, 60, 50, 40, 30, 20, 10];
  const saturationSteps = [20, 30, 50, 70, 85, 92, 85, 75, 65, 50];

  for (let i = 0; i < steps; i++) {
    // Shift hue slightly: lighter = cooler, darker = warmer
    const hueShift = (i - 4.5) * -2; // -9° to +9°
    const hue = (baseHue + hueShift + 360) % 360;
    const lightness = lightnessSteps[i];
    const saturation = saturationSteps[i];
    scale[(i + 1) * 100] = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  }
  return scale;
}
```

**Advanced features**:
- Blues get warmer when dark (like night sky)
- Yellows get cooler when dark
- More natural, less synthetic
- Mimics real-world color behavior

### Tailwind-Style Scale Structure

```javascript
// Complete color scale with recommended use cases
const colorScale = {
  50:  { color: 'hsl(211, 20%, 95%)', use: 'Subtle backgrounds' },
  100: { color: 'hsl(211, 30%, 90%)', use: 'Hover backgrounds' },
  200: { color: 'hsl(211, 50%, 80%)', use: 'Disabled states' },
  300: { color: 'hsl(211, 70%, 70%)', use: 'Borders' },
  400: { color: 'hsl(211, 85%, 60%)', use: 'Secondary text' },
  500: { color: 'hsl(211, 92%, 50%)', use: 'Primary color' },
  600: { color: 'hsl(211, 85%, 40%)', use: 'Hover states' },
  700: { color: 'hsl(211, 75%, 30%)', use: 'Active states' },
  800: { color: 'hsl(211, 65%, 20%)', use: 'Primary text' },
  900: { color: 'hsl(211, 50%, 10%)', use: 'Headings' },
};
```

### Testing Your Scale

```javascript
// Check contrast ratios across scale
function testScaleContrast(scale) {
  const results = [];
  const shades = Object.keys(scale);

  for (let i = 0; i < shades.length - 1; i++) {
    const light = scale[shades[i]];
    const dark = scale[shades[i + 1]];
    const ratio = calculateContrastRatio(light, dark);
    results.push({
      pair: `${shades[i]}-${shades[i + 1]}`,
      ratio: ratio.toFixed(2),
      passAA: ratio >= 4.5,
      passAAA: ratio >= 7
    });
  }

  return results;
}
```

### Industry Examples

**Tailwind CSS**:
- 10 shades (50-900)
- Saturation peaks at 500-600
- Slightly desaturated at extremes

**Material Design**:
- 14 shades (50-900 + A100-A700)
- Accent colors for emphasis
- Specific contrast requirements

**Ant Design**:
- 10 shades based on HSV
- Generated from single brand color
- Algorithmic consistency

---

## Accessibility & Contrast

### WCAG Contrast Requirements

**WCAG 2.1 Standards**:

| Level | Normal Text | Large Text | UI Components |
|-------|-------------|------------|---------------|
| **AA** | 4.5:1 | 3:1 | 3:1 |
| **AAA** | 7:1 | 4.5:1 | 4.5:1 |

**Large Text Definition**:
- 18pt+ (24px+) regular weight
- 14pt+ (18.5px+) bold weight

### Calculating Contrast Ratio

```javascript
// Calculate relative luminance
function getLuminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928
      ? c / 12.92
      : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

// Calculate contrast ratio
function getContrastRatio(color1, color2) {
  const lum1 = getLuminance(...color1); // [r, g, b]
  const lum2 = getLuminance(...color2);
  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Check WCAG compliance
function checkWCAG(foreground, background, fontSize, fontWeight) {
  const ratio = getContrastRatio(foreground, background);
  const isLargeText = fontSize >= 24 || (fontSize >= 18.5 && fontWeight >= 700);

  const aaThreshold = isLargeText ? 3 : 4.5;
  const aaaThreshold = isLargeText ? 4.5 : 7;

  return {
    ratio: ratio.toFixed(2),
    passAA: ratio >= aaThreshold,
    passAAA: ratio >= aaaThreshold,
    level: ratio >= aaaThreshold ? 'AAA' : ratio >= aaThreshold ? 'AA' : 'Fail'
  };
}
```

### Common Contrast Mistakes

**❌ Low Contrast Gray Text**:
```css
/* FAIL: 2.8:1 ratio */
.subtle-text {
  color: #999999;
  background: #FFFFFF;
}
```

**✅ Accessible Gray Text**:
```css
/* PASS AA: 4.6:1 ratio */
.accessible-text {
  color: #757575;
  background: #FFFFFF;
}

/* PASS AAA: 7.1:1 ratio */
.high-contrast-text {
  color: #595959;
  background: #FFFFFF;
}
```

**❌ Colored Text on White**:
```css
/* FAIL: Beautiful but inaccessible */
.error-text {
  color: #FF6B6B; /* 3.2:1 - fails AA */
  background: #FFFFFF;
}
```

**✅ Accessible Colored Text**:
```css
/* PASS AA: Darkened red */
.error-text {
  color: #D32F2F; /* 4.5:1 */
  background: #FFFFFF;
}

/* PASS AAA: Even darker */
.error-text-aaa {
  color: #A52A2A; /* 7.4:1 */
  background: #FFFFFF;
}
```

### Building Accessible Palettes

```javascript
// Ensure minimum contrast in color scale
function ensureAccessibleScale(baseHue, background = '#FFFFFF') {
  const scale = {};
  const targetContrasts = {
    100: 1.2,  // Barely visible (backgrounds only)
    200: 1.5,
    300: 3.0,  // AA for large text & UI

    400: 4.5,  // AA for normal text
    500: 4.5,
    600: 7.0,  // AAA for normal text
    700: 10.0,
    800: 12.0,
    900: 15.0
  };

  for (const [shade, targetRatio] of Object.entries(targetContrasts)) {
    let lightness = 50;
    let iterations = 0;

    // Binary search for correct lightness
    let min = 0, max = 100;
    while (iterations < 20) {
      const color = hslToRgb(baseHue, 92, lightness);
      const ratio = getContrastRatio(color, hexToRgb(background));

      if (Math.abs(ratio - targetRatio) < 0.1) break;

      if (ratio < targetRatio) {
        max = lightness;
        lightness = (min + lightness) / 2;
      } else {
        min = lightness;
        lightness = (lightness + max) / 2;
      }

      iterations++;
    }

    scale[shade] = `hsl(${baseHue}, 92%, ${lightness}%)`;
  }

  return scale;
}
```

### Contrast in Different Contexts

**1. Text on Colored Backgrounds**:
```css
/* Light background needs dark text */
.card-light {
  background: hsl(211, 92%, 95%);
  color: hsl(211, 92%, 20%); /* 12:1 ratio */
}

/* Dark background needs light text */
.card-dark {
  background: hsl(211, 92%, 20%);
  color: hsl(211, 92%, 95%); /* 12:1 ratio */
}
```

**2. Buttons & Interactive Elements**:
```css
/* Primary button */
.btn-primary {
  background: hsl(211, 92%, 50%);
  color: #FFFFFF; /* 4.6:1 - PASS AA */
  border: 2px solid hsl(211, 92%, 40%); /* 3:1 against bg */
}

/* Button states must maintain contrast */
.btn-primary:hover {
  background: hsl(211, 92%, 45%); /* Still passes */
}

.btn-primary:disabled {
  background: hsl(211, 30%, 75%);
  color: hsl(211, 30%, 40%); /* 3.2:1 - PASS for UI */
}
```

**3. Links**:
```css
/* Link must contrast with both text AND background */
.content {
  background: #FFFFFF;
  color: #333333; /* Body text */
}

.content a {
  /* Must contrast 4.5:1 with white AND 3:1 with #333 */
  color: #0066CC; /* 7.7:1 with white, 3.2:1 with text */
  text-decoration: underline; /* Visual indicator besides color */
}
```

### Non-Text Contrast (UI Components)

**WCAG 2.1 Success Criterion 1.4.11**:
- UI components: 3:1 minimum
- Graphical objects: 3:1 minimum

```css
/* Form inputs */
.input {
  border: 2px solid #757575; /* 3.5:1 with white */
  background: #FFFFFF;
}

.input:focus {
  border-color: #0066CC; /* 7.7:1 - highly visible */
  outline: 3px solid rgba(0, 102, 204, 0.2);
}

/* Icons */
.icon {
  color: #595959; /* 7.1:1 - clearly visible */
}

/* Dividers */
.divider {
  border-top: 1px solid #C7C7C7; /* 3.1:1 - meets minimum */
}
```

### Programmatic Contrast Checking

```javascript
// Auto-select text color based on background
function getAccessibleTextColor(backgroundColor, level = 'AA') {
  const bgColor = hexToRgb(backgroundColor);
  const whiteRatio = getContrastRatio([255, 255, 255], bgColor);
  const blackRatio = getContrastRatio([0, 0, 0], bgColor);

  const threshold = level === 'AAA' ? 7 : 4.5;

  if (whiteRatio >= threshold) return '#FFFFFF';
  if (blackRatio >= threshold) return '#000000';

  // Neither works - adjust background
  throw new Error(`Background ${backgroundColor} cannot meet ${level} with pure black or white`);
}

// Generate accessible color pairs
function getAccessiblePairs(baseColor) {
  const pairs = [];
  const shades = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900];

  shades.forEach(bg => {
    shades.forEach(fg => {
      if (bg === fg) return;

      const bgColor = baseColor[bg];
      const fgColor = baseColor[fg];
      const ratio = getContrastRatio(
        hexToRgb(bgColor),
        hexToRgb(fgColor)
      );

      if (ratio >= 4.5) {
        pairs.push({
          background: bg,
          foreground: fg,
          ratio: ratio.toFixed(2),
          level: ratio >= 7 ? 'AAA' : 'AA'
        });
      }
    });
  });

  return pairs;
}
```

---

## Color Blindness Considerations

### Types of Color Blindness

**Protanopia** (Red-Blind, ~1% males):
- Cannot distinguish red from green
- Reds appear darker
- Confuse: Red/Green, Red/Brown, Purple/Blue

**Deuteranopia** (Green-Blind, ~1% males):
- Most common type
- Cannot distinguish red from green
- Confuse: Green/Brown, Green/Orange, Red/Brown

**Tritanopia** (Blue-Blind, ~0.001%):
- Rare
- Cannot distinguish blue from yellow
- Confuse: Blue/Green, Purple/Red, Yellow/Pink

**Achromatopsia** (Complete Color Blindness, ~0.003%):
- See only grayscale
- Rely entirely on brightness/contrast

### Design Strategies

**1. Never Use Color Alone**:

**❌ Bad - Color only**:
```jsx
<div className="status-indicator">
  <span className="text-green-600">Active</span>
  <span className="text-red-600">Inactive</span>
</div>
```

**✅ Good - Color + Icon**:
```jsx
<div className="status-indicator">
  <span className="text-green-600">
    <CheckIcon /> Active
  </span>
  <span className="text-red-600">
    <XIcon /> Inactive
  </span>
</div>
```

**✅ Good - Color + Shape**:
```jsx
<div className="status-indicator">
  <span className="rounded-full bg-green-600">●</span> Active
  <span className="rotate-45 bg-red-600">+</span> Inactive
</div>
```

**2. Use Patterns & Textures**:

```css
/* Charts with patterns */
.chart-bar-1 { fill: #0066CC; } /* Solid */
.chart-bar-2 { fill: url(#stripes); } /* Striped */
.chart-bar-3 { fill: url(#dots); } /* Dotted */

/* Define patterns */
<pattern id="stripes" patternUnits="userSpaceOnUse" width="4" height="4">
  <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" stroke="#000" />
</pattern>
```

**3. High Contrast Differences**:

```javascript
// Ensure colors are distinguishable by brightness alone
function colorBlindSafePalette() {
  return {
    primary: {
      color: '#0066CC',
      luminance: 0.25, // Dark
      alternative: 'Solid fill'
    },
    success: {
      color: '#00AA00',
      luminance: 0.45, // Medium
      alternative: 'Checkmark icon'
    },
    warning: {
      color: '#FFCC00',
      luminance: 0.75, // Light
      alternative: 'Alert icon'
    },
    danger: {
      color: '#CC0000',
      luminance: 0.20, // Very dark
      alternative: 'X icon'
    }
  };
}
```

**4. Safe Color Combinations**:

**For Red-Green Color Blindness (Most Common)**:
```javascript
const safeColors = {
  // These pairs are distinguishable
  good: [
    ['#0066CC', '#FFB300'], // Blue + Orange
    ['#663399', '#FFCC00'], // Purple + Yellow
    ['#0088CC', '#CC3333'], // Cyan + Red (if enough contrast)
    ['#000000', '#FFAA00'], // Black + Orange
  ],

  // AVOID these pairs
  bad: [
    ['#CC3333', '#33AA33'], // Red + Green
    ['#CC6600', '#999900'], // Orange + Olive
    ['#993333', '#666600'], // Brown + Dark Yellow
  ]
};
```

**For Blue-Yellow Color Blindness (Rare)**:
```javascript
const tritanopiaSafe = {
  good: [
    ['#CC3333', '#33AA33'], // Red + Green
    ['#CC0066', '#006633'], // Magenta + Teal
  ],
  bad: [
    ['#0066CC', '#FFCC00'], // Blue + Yellow
    ['#663399', '#CCAA00'], // Purple + Gold
  ]
};
```

### Testing Tools

**Simulation Libraries**:
```javascript
import { simulateColorBlindness } from 'color-blind-simulator';

// Test your palette
const colors = ['#CC3333', '#33AA33', '#0066CC'];

const protanopia = colors.map(c =>
  simulateColorBlindness(c, 'protanopia')
);

const deuteranopia = colors.map(c =>
  simulateColorBlindness(c, 'deuteranopia')
);

// Check if simulated colors are still distinguishable
function areDistinguishable(color1, color2, threshold = 30) {
  const [r1, g1, b1] = hexToRgb(color1);
  const [r2, g2, b2] = hexToRgb(color2);

  const distance = Math.sqrt(
    Math.pow(r2 - r1, 2) +
    Math.pow(g2 - g1, 2) +
    Math.pow(b2 - b1, 2)
  );

  return distance > threshold;
}
```

**Manual Testing Checklist**:
- [ ] Convert UI to grayscale - still usable?
- [ ] Every status has icon or text label
- [ ] Charts use patterns or shapes
- [ ] Error states have text descriptions
- [ ] Links are underlined or have icon
- [ ] Form validation shows messages, not just red borders
- [ ] Data visualization uses more than color

### Accessible Color Palettes

**Okabe-Ito Palette** (Scientifically designed):
```javascript
const okabeIto = {
  black: '#000000',
  orange: '#E69F00',
  skyBlue: '#56B4E9',
  bluishGreen: '#009E73',
  yellow: '#F0E442',
  blue: '#0072B2',
  vermillion: '#D55E00',
  reddishPurple: '#CC79A7'
};
```

**IBM Design Color Blind Safe Palette**:
```javascript
const ibmSafe = {
  blue: '#648FFF',
  purple: '#785EF0',
  magenta: '#DC267F',
  orange: '#FE6100',
  yellow: '#FFB000'
};
```

---

## Semantic Color Naming

### Why Semantic Names Matter

**❌ Bad - Literal Names**:
```javascript
// Breaks when you change brand colors
const colors = {
  blue500: '#0066CC',
  blue600: '#0052A3',
  green500: '#00AA00',
  red500: '#CC3333'
};

// Usage is unclear
<Button className="bg-blue500" />
<Text className="text-red500" />
```

**✅ Good - Semantic Names**:
```javascript
const colors = {
  primary: '#0066CC',
  primaryHover: '#0052A3',
  success: '#00AA00',
  danger: '#CC3333'
};

// Usage is clear and rebrandable
<Button className="bg-primary" />
<Text className="text-danger" />
```

### Multi-Layer Naming System

**Layer 1: Foundation (Literal)**
```javascript
const foundation = {
  blue: {
    50: '#EFF6FF',
    100: '#DBEAFE',
    // ... through 900
  },
  green: { /* ... */ },
  red: { /* ... */ }
};
```

**Layer 2: Semantic (Purpose)**
```javascript
const semantic = {
  primary: {
    DEFAULT: foundation.blue[500],
    hover: foundation.blue[600],
    active: foundation.blue[700],
    disabled: foundation.blue[300],
    subtle: foundation.blue[100],
    emphasis: foundation.blue[700]
  },
  success: {
    DEFAULT: foundation.green[500],
    hover: foundation.green[600],
    subtle: foundation.green[100],
    border: foundation.green[300]
  },
  danger: {
    DEFAULT: foundation.red[500],
    hover: foundation.red[600],
    subtle: foundation.red[100],
    border: foundation.red[300]
  },
  warning: {
    DEFAULT: foundation.orange[500],
    hover: foundation.orange[600],
    subtle: foundation.orange[100],
    border: foundation.orange[300]
  }
};
```

**Layer 3: Component (Context)**
```javascript
const components = {
  button: {
    primary: {
      bg: semantic.primary.DEFAULT,
      bgHover: semantic.primary.hover,
      text: foundation.white,
      border: semantic.primary.DEFAULT
    },
    secondary: {
      bg: semantic.primary.subtle,
      bgHover: semantic.primary.DEFAULT,
      text: semantic.primary.DEFAULT,
      border: semantic.primary.DEFAULT
    },
    danger: {
      bg: semantic.danger.DEFAULT,
      bgHover: semantic.danger.hover,
      text: foundation.white,
      border: semantic.danger.DEFAULT
    }
  },
  input: {
    bg: foundation.white,
    border: foundation.gray[300],
    borderFocus: semantic.primary.DEFAULT,
    borderError: semantic.danger.DEFAULT,
    text: foundation.gray[900],
    placeholder: foundation.gray[400]
  }
};
```

### Naming Conventions

**State-Based Names**:
```javascript
const stateBased = {
  // Interactive states
  'primary': base,
  'primary-hover': onHover,
  'primary-active': onPress,
  'primary-disabled': notInteractive,

  // Emphasis levels
  'primary-subtle': lowEmphasis,
  'primary-emphasis': highEmphasis,

  // Surface variations
  'primary-on-surface': colorOnBackground,
  'primary-surface': backgroundWithColor
};
```

**Content-Based Names**:
```javascript
const contentBased = {
  // Text hierarchy
  'text-primary': mainContent,
  'text-secondary': supportingContent,
  'text-tertiary': subtleContent,
  'text-disabled': nonInteractive,
  'text-inverse': lightOnDark,

  // Backgrounds
  'bg-primary': mainSurface,
  'bg-secondary': subtleSurface,
  'bg-tertiary': ultraSubtle,

  // Borders
  'border-primary': strongDivider,
  'border-secondary': subtleDivider,
  'border-tertiary': barelyVisible
};
```

**Feedback-Based Names**:
```javascript
const feedbackBased = {
  success: { /* ... */ },
  error: { /* ... */ },
  warning: { /* ... */ },
  info: { /* ... */ },

  // Extended feedback
  'success-subtle': lowEmphasisPositive,
  'error-surface': errorBackground,
  'warning-border': warningOutline
};
```

### Complete Semantic System

```typescript
type ColorToken = {
  description: string;
  value: string;
  wcagWith: {
    light: 'AA' | 'AAA' | 'Fail';
    dark: 'AA' | 'AAA' | 'Fail';
  };
};

const semanticSystem: Record<string, ColorToken> = {
  // Brand
  'brand-primary': {
    description: 'Main brand color for primary actions',
    value: '#0066CC',
    wcagWith: { light: 'AA', dark: 'AAA' }
  },
  'brand-secondary': {
    description: 'Secondary brand color for accents',
    value: '#663399',
    wcagWith: { light: 'AA', dark: 'AA' }
  },

  // Text
  'text-primary': {
    description: 'Primary text color for main content',
    value: '#111827',
    wcagWith: { light: 'AAA', dark: 'Fail' }
  },
  'text-secondary': {
    description: 'Secondary text for supporting content',
    value: '#6B7280',
    wcagWith: { light: 'AA', dark: 'Fail' }
  },
  'text-tertiary': {
    description: 'Tertiary text for subtle content',
    value: '#9CA3AF',
    wcagWith: { light: 'AA', dark: 'Fail' }
  },
  'text-inverse': {
    description: 'Text on dark backgrounds',
    value: '#FFFFFF',
    wcagWith: { light: 'Fail', dark: 'AAA' }
  },

  // Backgrounds
  'bg-primary': {
    description: 'Primary background color',
    value: '#FFFFFF',
    wcagWith: { light: 'N/A', dark: 'N/A' }
  },
  'bg-secondary': {
    description: 'Secondary background for subtle contrast',
    value: '#F9FAFB',
    wcagWith: { light: 'N/A', dark: 'N/A' }
  },
  'bg-tertiary': {
    description: 'Tertiary background for layered surfaces',
    value: '#F3F4F6',
    wcagWith: { light: 'N/A', dark: 'N/A' }
  },

  // Interactive
  'interactive-primary': {
    description: 'Primary interactive elements',
    value: '#0066CC',
    wcagWith: { light: 'AA', dark: 'AAA' }
  },
  'interactive-primary-hover': {
    description: 'Hover state for primary interactive',
    value: '#0052A3',
    wcagWith: { light: 'AA', dark: 'AAA' }
  },
  'interactive-primary-active': {
    description: 'Active/pressed state',
    value: '#004182',
    wcagWith: { light: 'AAA', dark: 'AAA' }
  },
  'interactive-disabled': {
    description: 'Disabled interactive elements',
    value: '#D1D5DB',
    wcagWith: { light: 'Fail', dark: 'Fail' }
  },

  // Feedback
  'feedback-success': {
    description: 'Success states and positive feedback',
    value: '#059669',
    wcagWith: { light: 'AA', dark: 'AAA' }
  },
  'feedback-success-subtle': {
    description: 'Subtle success background',
    value: '#D1FAE5',
    wcagWith: { light: 'Fail', dark: 'Fail' }
  },
  'feedback-error': {
    description: 'Error states and negative feedback',
    value: '#DC2626',
    wcagWith: { light: 'AA', dark: 'AAA' }
  },
  'feedback-error-subtle': {
    description: 'Subtle error background',
    value: '#FEE2E2',
    wcagWith: { light: 'Fail', dark: 'Fail' }
  },
  'feedback-warning': {
    description: 'Warning states and caution',
    value: '#D97706',
    wcagWith: { light: 'AA', dark: 'AA' }
  },
  'feedback-warning-subtle': {
    description: 'Subtle warning background',
    value: '#FEF3C7',
    wcagWith: { light: 'Fail', dark: 'Fail' }
  },
  'feedback-info': {
    description: 'Informational states',
    value: '#2563EB',
    wcagWith: { light: 'AA', dark: 'AAA' }
  },
  'feedback-info-subtle': {
    description: 'Subtle info background',
    value: '#DBEAFE',
    wcagWith: { light: 'Fail', dark: 'Fail' }
  },

  // Borders
  'border-primary': {
    description: 'Primary borders and dividers',
    value: '#E5E7EB',
    wcagWith: { light: 'AA', dark: 'Fail' }
  },
  'border-secondary': {
    description: 'Secondary borders, more subtle',
    value: '#F3F4F6',
    wcagWith: { light: 'Fail', dark: 'Fail' }
  },
  'border-focus': {
    description: 'Focus rings for accessibility',
    value: '#0066CC',
    wcagWith: { light: 'AA', dark: 'AAA' }
  }
};
```

### Usage Patterns

```tsx
// Component with semantic colors
function Button({
  variant = 'primary',
  children
}: ButtonProps) {
  const variants = {
    primary: {
      bg: 'bg-interactive-primary',
      bgHover: 'bg-interactive-primary-hover',
      bgActive: 'bg-interactive-primary-active',
      text: 'text-inverse',
      border: 'border-interactive-primary'
    },
    secondary: {
      bg: 'bg-transparent',
      bgHover: 'bg-bg-secondary',
      bgActive: 'bg-bg-tertiary',
      text: 'text-interactive-primary',
      border: 'border-border-primary'
    },
    danger: {
      bg: 'bg-feedback-error',
      bgHover: 'bg-feedback-error-hover',
      bgActive: 'bg-feedback-error-active',
      text: 'text-inverse',
      border: 'border-feedback-error'
    }
  };

  const styles = variants[variant];

  return (
    <button className={`
      ${styles.bg} hover:${styles.bgHover} active:${styles.bgActive}
      ${styles.text} border-2 ${styles.border}
      px-4 py-2 rounded-lg transition-colors
    `}>
      {children}
    </button>
  );
}
```

---

## Dark Mode Color Systems

### Core Principles

**1. Not Just Inverted**:
- Don't simply invert lightness values
- Adjust saturation (less saturated in dark mode)
- Consider different contrast needs
- Maintain brand identity

**2. Surface Elevation**:
- Lighter surfaces = higher elevation
- Use subtle overlays, not just grays
- Maintain hierarchy through lightness

**3. Accessibility in Dark Mode**:
- Lower contrast than light mode is acceptable
- But still minimum 4.5:1 for text
- Reduce eyestrain with softer colors

### Building a Dark Mode Palette

**Light Mode Base**:
```javascript
const lightMode = {
  // Backgrounds
  'bg-primary': '#FFFFFF',
  'bg-secondary': '#F9FAFB',
  'bg-tertiary': '#F3F4F6',

  // Text
  'text-primary': '#111827',
  'text-secondary': '#6B7280',
  'text-tertiary': '#9CA3AF',

  // Borders
  'border-primary': '#E5E7EB',
  'border-secondary': '#F3F4F6',

  // Brand
  'brand-primary': 'hsl(211, 92%, 50%)',
  'brand-secondary': 'hsl(271, 46%, 50%)'
};
```

**Dark Mode Translation**:
```javascript
const darkMode = {
  // Backgrounds (NOT pure black)
  'bg-primary': '#0F172A',      // Slate-900
  'bg-secondary': '#1E293B',    // Slate-800 (elevated)
  'bg-tertiary': '#334155',     // Slate-700 (more elevated)

  // Text (NOT pure white)
  'text-primary': '#F1F5F9',    // Slate-100
  'text-secondary': '#94A3B8',  // Slate-400
  'text-tertiary': '#64748B',   // Slate-500

  // Borders (more subtle)
  'border-primary': '#334155',  // Slate-700
  'border-secondary': '#1E293B', // Slate-800

  // Brand (less saturated, lighter)
  'brand-primary': 'hsl(211, 70%, 60%)',    // Less sat, lighter
  'brand-secondary': 'hsl(271, 35%, 60%)'   // Less sat, lighter
};
```

### Surface Elevation System

**Material Design Approach**:
```javascript
// White overlay on dark surface = elevation
function getElevatedSurface(baseColor, elevation) {
  const overlayOpacity = {
    0: 0,      // Base surface
    1: 0.05,   // 1dp
    2: 0.07,   // 2dp
    3: 0.08,   // 3dp
    4: 0.09,   // 4dp
    6: 0.11,   // 6dp (nav drawer)
    8: 0.12,   // 8dp (app bar)
    12: 0.14,  // 12dp (FAB)
    16: 0.15,  // 16dp (nav rail)
    24: 0.16   // 24dp (dialog)
  };

  const opacity = overlayOpacity[elevation] || 0;

  return `
    background: ${baseColor};
    background-image: linear-gradient(
      rgba(255, 255, 255, ${opacity}),
      rgba(255, 255, 255, ${opacity})
    );
  `;
}

// Usage
const surfaces = {
  base: getElevatedSurface('#0F172A', 0),
  card: getElevatedSurface('#0F172A', 1),
  modal: getElevatedSurface('#0F172A', 8),
  dropdown: getElevatedSurface('#0F172A', 24)
};
```

**Custom Elevation Scale**:
```javascript
const darkModeElevation = {
  0: '#0F172A',  // Base
  1: '#1A2236',  // Slightly lighter
  2: '#252F42',  // Cards
  3: '#30394E',  // Hover states
  4: '#3B435A',  // Active elevated elements
  5: '#464D66',  // Modals/dialogs
};
```

### Color Transformation Strategies

**Strategy 1: Lightness Flip**:
```javascript
function transformForDarkMode(hsl) {
  const [h, s, l] = parseHsl(hsl);

  // Flip lightness around 50%
  const newL = 100 - l;

  // Reduce saturation slightly
  const newS = s * 0.8;

  return `hsl(${h}, ${newS}%, ${newL}%)`;
}
```

**Strategy 2: Perceptual Adjustment**:
```javascript
function transformForDarkModePerceptual(hsl) {
  const [h, s, l] = parseHsl(hsl);

  // More complex transformation
  let newL, newS;

  if (l < 20) {
    // Very dark becomes light
    newL = 75 + (20 - l);
  } else if (l > 80) {
    // Very light becomes dark
    newL = 25 - (l - 80);
  } else {
    // Middle range inverts
    newL = 100 - l;
  }

  // Reduce saturation more for lighter colors
  newS = l > 50 ? s * 0.7 : s * 0.85;

  return `hsl(${h}, ${newS}%, ${newL}%)`;
}
```

**Strategy 3: Manual Mapping (Recommended)**:
```javascript
const colorMapping = {
  // Light -> Dark transformations
  light: {
    'gray-50': '#F9FAFB',
    'gray-100': '#F3F4F6',
    'gray-200': '#E5E7EB',
    'gray-800': '#1F2937',
    'gray-900': '#111827',
  },
  dark: {
    'gray-50': '#1F2937',   // Map to dark
    'gray-100': '#374151',  // Map to dark
    'gray-200': '#4B5563',  // Map to dark
    'gray-800': '#E5E7EB',  // Map to light
    'gray-900': '#F3F4F6',  // Map to light
  }
};
```

### Implementation Patterns

**CSS Variables (Recommended)**:
```css
:root {
  /* Light mode (default) */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F9FAFB;
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;
  --color-brand-primary: hsl(211, 92%, 50%);
}

[data-theme="dark"] {
  /* Dark mode overrides */
  --color-bg-primary: #0F172A;
  --color-bg-secondary: #1E293B;
  --color-text-primary: #F1F5F9;
  --color-text-secondary: #94A3B8;
  --color-brand-primary: hsl(211, 70%, 60%);
}

/* Usage in components */
.card {
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
}
```

**Tailwind Dark Mode**:
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media'
  theme: {
    extend: {
      colors: {
        // Semantic colors that adapt
        'bg-primary': {
          light: '#FFFFFF',
          dark: '#0F172A'
        },
        'text-primary': {
          light: '#111827',
          dark: '#F1F5F9'
        }
      }
    }
  }
};
```

```tsx
// Usage in components
<div className="
  bg-white dark:bg-slate-900
  text-gray-900 dark:text-slate-100
">
  Content adapts to theme
</div>
```

**Styled Components**:
```typescript
// Theme definition
const theme = {
  light: {
    bgPrimary: '#FFFFFF',
    bgSecondary: '#F9FAFB',
    textPrimary: '#111827',
    brandPrimary: 'hsl(211, 92%, 50%)'
  },
  dark: {
    bgPrimary: '#0F172A',
    bgSecondary: '#1E293B',
    textPrimary: '#F1F5F9',
    brandPrimary: 'hsl(211, 70%, 60%)'
  }
};

// Component
const Card = styled.div`
  background: ${props => props.theme.bgPrimary};
  color: ${props => props.theme.textPrimary};
`;

// App
function App() {
  const [mode, setMode] = useState('light');

  return (
    <ThemeProvider theme={theme[mode]}>
      <Card>Content</Card>
    </ThemeProvider>
  );
}
```

### Dark Mode Best Practices

**1. Test Contrast in Both Modes**:
```javascript
function validateDarkMode(lightColor, darkColor) {
  const lightBg = '#FFFFFF';
  const darkBg = '#0F172A';

  const lightRatio = getContrastRatio(
    hexToRgb(lightColor),
    hexToRgb(lightBg)
  );

  const darkRatio = getContrastRatio(
    hexToRgb(darkColor),
    hexToRgb(darkBg)
  );

  return {
    light: {
      ratio: lightRatio,
      passes: lightRatio >= 4.5
    },
    dark: {
      ratio: darkRatio,
      passes: darkRatio >= 4.5
    }
  };
}
```

**2. Avoid Pure Black**:
```css
/* ❌ Don't use pure black */
[data-theme="dark"] {
  background: #000000; /* Too harsh */
}

/* ✅ Use very dark gray/blue */
[data-theme="dark"] {
  background: #0F172A; /* Easier on eyes */
  background: #1A1A1A; /* Or dark gray */
}
```

**3. Reduce Saturation**:
```css
/* Light mode */
.button-primary {
  background: hsl(211, 92%, 50%); /* Vibrant */
}

/* Dark mode */
[data-theme="dark"] .button-primary {
  background: hsl(211, 70%, 60%); /* Less saturated, lighter */
}
```

**4. Shadows in Dark Mode**:
```css
/* Light mode */
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Dark mode - lighter shadows or borders */
[data-theme="dark"] .card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5); /* Darker shadow */
  /* OR */
  border: 1px solid rgba(255, 255, 255, 0.1); /* Light border */
}
```

---

## Color in Data Visualization

### Choosing Visualization Colors

**Sequential Palettes** (For ordered data):
```javascript
// Single hue, varying lightness
const sequential = {
  light: ['#EFF6FF', '#DBEAFE', '#BFDBFE', '#93C5FD', '#60A5FA'],
  medium: ['#3B82F6', '#2563EB', '#1D4ED8', '#1E40AF', '#1E3A8A'],

  // Usage: population density, temperature, progress
};
```

**Diverging Palettes** (For data with meaningful midpoint):
```javascript
// Two hues diverging from neutral center
const diverging = {
  redBlue: [
    '#B91C1C', '#DC2626', '#EF4444', // Red (negative)
    '#F3F4F6',                        // Neutral
    '#3B82F6', '#2563EB', '#1D4ED8'  // Blue (positive)
  ],

  // Usage: profit/loss, temperature anomaly, sentiment
};
```

**Categorical Palettes** (For distinct categories):
```javascript
// Distinct hues, similar lightness
const categorical = {
  primary: [
    '#3B82F6', // Blue
    '#10B981', // Green
    '#F59E0B', // Orange
    '#EF4444', // Red
    '#8B5CF6', // Purple
    '#EC4899', // Pink
    '#14B8A6', // Teal
    '#F97316'  // Amber
  ],

  // Requirements:
  // - Distinguishable by color-blind users
  // - Similar perceived brightness
  // - Maximum visual separation
};
```

### Color-Blind Safe Visualization

**Paul Tol's Qualitative Schemes**:
```javascript
const paulTol = {
  // 3 colors
  bright: ['#4477AA', '#CCBB44', '#EE6677'],

  // 6 colors
  vibrant: [
    '#0077BB', '#33BBEE', '#009988',
    '#EE7733', '#CC3311', '#EE3377'
  ],

  // 9 colors (maximum for distinct perception)
  muted: [
    '#332288', '#88CCEE', '#44AA99', '#117733',
    '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499'
  ]
};
```

**IBM Carbon Dataviz Palette**:
```javascript
const ibmCarbon = [
  '#6929c4', // Purple
  '#1192e8', // Blue
  '#005d5d', // Teal
  '#9f1853', // Magenta
  '#fa4d56', // Red
  '#570408', // Dark red
  '#198038', // Green
  '#002d9c', // Dark blue
  '#ee538b', // Pink
  '#b28600', // Gold
  '#009d9a', // Cyan
  '#012749', // Navy
];
```

### Heat Maps & Gradients

**Perceptually Uniform Scales**:
```javascript
// Viridis (scientifically designed)
const viridis = [
  '#440154', '#414487', '#2A788E',
  '#22A884', '#7AD151', '#FDE725'
];

// Avoid rainbow gradients (perceptually non-uniform)
// ❌ Don't use: Red -> Orange -> Yellow -> Green -> Blue
// ✅ Use: Perceptually uniform scales
```

**Creating Custom Heat Map Scale**:
```javascript
function createHeatMapScale(startColor, endColor, steps = 10) {
  const start = hexToLch(startColor);
  const end = hexToLch(endColor);

  const scale = [];
  for (let i = 0; i < steps; i++) {
    const t = i / (steps - 1);

    // Interpolate in LCH for perceptual uniformity
    const l = start.l + (end.l - start.l) * t;
    const c = start.c + (end.c - start.c) * t;
    const h = start.h + (end.h - start.h) * t;

    scale.push(lchToHex({ l, c, h }));
  }

  return scale;
}

// Usage
const blueToRed = createHeatMapScale('#3B82F6', '#EF4444', 10);
```

### Chart-Specific Guidelines

**Bar Charts**:
```javascript
const barChartColors = {
  // Single series - use brand color
  single: '#3B82F6',

  // Multiple series - distinct colors
  multiple: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444'],

  // Highlighting - desaturate non-highlighted
  highlight: {
    focus: '#3B82F6',
    others: 'rgba(59, 130, 246, 0.3)'
  }
};
```

**Line Charts**:
```javascript
const lineChartColors = {
  // High contrast for overlapping lines
  lines: [
    { color: '#2563EB', width: 2 },
    { color: '#DC2626', width: 2 },
    { color: '#059669', width: 2 },
    { color: '#D97706', width: 2 }
  ],

  // Use dashed patterns for color-blind accessibility
  patterns: [
    { dash: 'solid', color: '#2563EB' },
    { dash: '5,5', color: '#DC2626' },
    { dash: '10,5', color: '#059669' },
    { dash: '2,2', color: '#D97706' }
  ]
};
```

**Pie Charts**:
```javascript
const pieChartColors = {
  // Adjacent slices should be distinct
  ordered: [
    '#3B82F6', // Blue
    '#FBBF24', // Yellow (high contrast with blue)
    '#10B981', // Green
    '#F87171', // Red (high contrast with green)
    '#8B5CF6', // Purple
  ],

  // Consider pattern fills for accessibility
  accessible: slices.map((slice, i) => ({
    fill: colors[i],
    pattern: patterns[i % patterns.length]
  }))
};
```

### Data Visualization Anti-Patterns

**❌ Rainbow Gradients**:
```javascript
// Perceptually non-uniform, color-blind unfriendly
const rainbow = ['red', 'orange', 'yellow', 'green', 'blue', 'purple'];
```

**✅ Perceptually Uniform**:
```javascript
const proper = viridis; // or other scientific palette
```

**❌ Red-Green Scale**:
```javascript
// 8% of males can't distinguish
const badScale = ['#DC2626', '#FBBF24', '#10B981'];
```

**✅ Blue-Orange Scale**:
```javascript
const goodScale = ['#2563EB', '#F3F4F6', '#F97316'];
```

**❌ Too Many Categories**:
```javascript
// Human perception limit: ~7-9 distinct colors
const tooMany = generateColors(15); // Impossible to distinguish
```

**✅ Group Categories**:
```javascript
const grouped = {
  main: generateColors(5),
  other: '#9CA3AF' // Group remaining as "Other"
};
```

---

## Brand Color Adaptation

### Extracting Brand Colors

**From Logo**:
```javascript
// Get dominant colors from logo image
async function extractBrandColors(logoUrl) {
  const palette = await ColorThief.getPalette(logoUrl, 5);

  // Convert to HSL for easier manipulation
  const hslPalette = palette.map(rgb => rgbToHsl(rgb));

  // Select primary (most saturated, mid-lightness)
  const primary = hslPalette.reduce((prev, curr) =>
    curr.s > prev.s && Math.abs(curr.l - 50) < Math.abs(prev.l - 50)
      ? curr : prev
  );

  return {
    primary,
    palette: hslPalette
  };
}
```

**Brand Color Analysis**:
```javascript
function analyzeBrandColor(color) {
  const [h, s, l] = parseHsl(color);

  return {
    hue: h,
    saturation: s,
    lightness: l,

    // Color characteristics
    warmth: h < 60 || h > 300 ? 'warm' : 'cool',
    vibrance: s > 70 ? 'vibrant' : s > 40 ? 'moderate' : 'muted',
    tone: l > 70 ? 'light' : l > 30 ? 'medium' : 'dark',

    // Recommendations
    needsDarkening: l > 60, // For text on white
    needsLightening: l < 40, // For text on dark
    needsDesaturation: s > 85 // For large areas
  };
}
```

### Building Full Palette from Brand Color

```javascript
function createBrandSystem(brandColor) {
  const [h, s, l] = parseHsl(brandColor);

  // Primary scale (brand color variations)
  const primary = {
    50:  `hsl(${h}, ${s * 0.3}%, 95%)`,
    100: `hsl(${h}, ${s * 0.4}%, 90%)`,
    200: `hsl(${h}, ${s * 0.5}%, 80%)`,
    300: `hsl(${h}, ${s * 0.7}%, 70%)`,
    400: `hsl(${h}, ${s * 0.85}%, 60%)`,
    500: brandColor, // Original
    600: `hsl(${h}, ${s * 0.9}%, 45%)`,
    700: `hsl(${h}, ${s * 0.85}%, 35%)`,
    800: `hsl(${h}, ${s * 0.7}%, 25%)`,
    900: `hsl(${h}, ${s * 0.5}%, 15%)`,
  };

  // Secondary (complementary or analogous)
  const secondaryHue = (h + 180) % 360; // Complementary
  const secondary = {
    500: `hsl(${secondaryHue}, ${s * 0.8}%, 50%)`,
    // ... full scale
  };

  // Neutrals (based on primary hue for cohesion)
  const neutrals = {
    50:  `hsl(${h}, 10%, 98%)`,
    100: `hsl(${h}, 10%, 95%)`,
    200: `hsl(${h}, 10%, 90%)`,
    300: `hsl(${h}, 8%, 80%)`,
    400: `hsl(${h}, 7%, 65%)`,
    500: `hsl(${h}, 5%, 50%)`,
    600: `hsl(${h}, 5%, 40%)`,
    700: `hsl(${h}, 5%, 30%)`,
    800: `hsl(${h}, 7%, 20%)`,
    900: `hsl(${h}, 10%, 10%)`,
  };

  // Semantic colors (harmonious with brand)
  const success = {
    500: `hsl(${(h + 120) % 360}, 60%, 45%)` // Triadic
  };

  const warning = {
    500: `hsl(${(h + 60) % 360}, 90%, 55%)` // Analogous
  };

  const error = {
    500: `hsl(${(h + 180) % 360}, 70%, 50%)` // Complementary
  };

  return {
    primary,
    secondary,
    neutrals,
    success,
    warning,
    error
  };
}
```

### Adapting Brand Colors for UI

**Problem: Brand color not suitable for UI**:
```javascript
// Example: Very dark or very light brand color
const brandColor = 'hsl(211, 92%, 15%)'; // Too dark for primary button

// Solution: Create UI-optimized variant
function optimizeForUI(brandColor, context) {
  const [h, s, l] = parseHsl(brandColor);

  const optimizations = {
    primaryButton: {
      // Needs good contrast with white text
      targetLightness: 45,
      targetSaturation: Math.max(s, 70),
      requirement: 'Must have 4.5:1 contrast with white'
    },

    link: {
      // Needs contrast with both text and background
      targetLightness: 40,
      targetSaturation: 85,
      requirement: 'Must have 4.5:1 with white, 3:1 with body text'
    },

    background: {
      // Needs to be subtle
      targetLightness: 95,
      targetSaturation: Math.min(s * 0.3, 20),
      requirement: 'Subtle, not distracting'
    }
  };

  const opt = optimizations[context];
  return `hsl(${h}, ${opt.targetSaturation}%, ${opt.targetLightness}%)`;
}
```

### Multi-Brand Systems

```javascript
// Managing multiple brands in one system
const brandManager = {
  brands: {
    acme: {
      primary: '#FF6B35',
      secondary: '#004E89',
      neutralHue: 210
    },
    techcorp: {
      primary: '#6C63FF',
      secondary: '#FF6584',
      neutralHue: 260
    }
  },

  // Generate full theme for brand
  getTheme(brandId) {
    const brand = this.brands[brandId];
    return createBrandSystem(brand.primary);
  },

  // CSS variables approach
  toCSSVariables(brandId) {
    const theme = this.getTheme(brandId);
    return `
      :root[data-brand="${brandId}"] {
        --color-primary: ${theme.primary[500]};
        --color-secondary: ${theme.secondary[500]};
        /* ... */
      }
    `;
  }
};
```

---

## Color Tools & Resources

### Essential Tools

**Design Tools**:
- **Figma Color Styleguide Plugin**: Generate scales from single color
- **Coolors.co**: Generate palette, check contrast, export to code
- **Adobe Color**: Color wheel, harmonies, accessibility
- **Paletton**: Advanced color scheme designer
- **ColorBox by Lyft Design**: Create accessible color systems

**Contrast Checkers**:
- **WebAIM Contrast Checker**: Simple, reliable WCAG checking
- **Contrast Ratio by Lea Verou**: Real-time contrast calculation
- **Stark Plugin**: Figma/Sketch plugin for accessibility
- **Who Can Use**: Shows how colors appear to different vision types

**Color Blindness Simulators**:
- **Coblis**: Upload image, see different color blind views
- **Color Oracle**: Desktop app, real-time simulation
- **Chromatic Vision Simulator**: Browser extension

**Palette Generators**:
- **Tailwind Color Generator**: Generate Tailwind-style scales
- **Eva Design System**: Generate semantic color system
- **Material Design Color Tool**: Material palette generator
- **Colorable**: Find accessible color combinations

### Programmatic Tools

**JavaScript Libraries**:
```javascript
// Chroma.js - color manipulation
import chroma from 'chroma-js';

const scale = chroma.scale(['#fafa6e', '#2A4858'])
  .mode('lch')
  .colors(10);

// TinyColor - color utilities
import tinycolor from 'tinycolor2';

const color = tinycolor('#0066CC');
console.log(color.getLuminance()); // 0.25
console.log(color.darken(10).toString()); // #004C99

// Color-blind simulator
import { simulate } from 'color-blind';

const protanopia = simulate('#CC3333', 'protanopia');
```

**CSS Tools**:
```css
/* CSS Color Module Level 4 */
.element {
  /* Relative colors */
  --base: #0066CC;
  --lighter: color-mix(in srgb, var(--base) 80%, white);
  --darker: color-mix(in srgb, var(--base) 80%, black);

  /* LCH colors */
  color: lch(60% 50 270);

  /* Color contrast function (future) */
  color: color-contrast(var(--bg) vs white, black);
}
```

### Validation Scripts

```javascript
// Validate entire color system
function validateColorSystem(colors) {
  const issues = [];

  // Check all text/background combinations
  const textColors = Object.keys(colors).filter(k => k.startsWith('text-'));
  const bgColors = Object.keys(colors).filter(k => k.startsWith('bg-'));

  textColors.forEach(textKey => {
    bgColors.forEach(bgKey => {
      const ratio = getContrastRatio(
        hexToRgb(colors[textKey]),
        hexToRgb(colors[bgKey])
      );

      if (ratio < 4.5) {
        issues.push({
          type: 'contrast',
          text: textKey,
          background: bgKey,
          ratio: ratio.toFixed(2),
          severity: 'error'
        });
      }
    });
  });

  // Check for color-blind safety
  const categoricalColors = colors.charts?.categorical || [];
  if (categoricalColors.length > 0) {
    const protanopia = categoricalColors.map(c =>
      simulateColorBlindness(c, 'protanopia')
    );

    // Check if any colors are too similar after simulation
    for (let i = 0; i < protanopia.length; i++) {
      for (let j = i + 1; j < protanopia.length; j++) {
        if (!areDistinguishable(protanopia[i], protanopia[j])) {
          issues.push({
            type: 'color-blind',
            colors: [categoricalColors[i], categoricalColors[j]],
            condition: 'protanopia',
            severity: 'warning'
          });
        }
      }
    }
  }

  return {
    valid: issues.filter(i => i.severity === 'error').length === 0,
    issues
  };
}
```

---

## Tailwind Color Configuration

### Custom Color Palette

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Brand colors
        brand: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6', // Primary brand color
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
        },

        // Semantic colors
        success: {
          DEFAULT: '#10B981',
          light: '#D1FAE5',
          dark: '#065F46',
        },
        error: {
          DEFAULT: '#EF4444',
          light: '#FEE2E2',
          dark: '#991B1B',
        },
        warning: {
          DEFAULT: '#F59E0B',
          light: '#FEF3C7',
          dark: '#92400E',
        },

        // Custom neutrals with brand hue
        gray: {
          50: 'hsl(211, 10%, 98%)',
          100: 'hsl(211, 10%, 95%)',
          200: 'hsl(211, 10%, 90%)',
          300: 'hsl(211, 8%, 80%)',
          400: 'hsl(211, 7%, 65%)',
          500: 'hsl(211, 5%, 50%)',
          600: 'hsl(211, 5%, 40%)',
          700: 'hsl(211, 5%, 30%)',
          800: 'hsl(211, 7%, 20%)',
          900: 'hsl(211, 10%, 10%)',
        },
      },
    },
  },
};
```

### Semantic Color Utilities

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Semantic naming
        'text-primary': 'rgb(17 24 39)', // gray-900
        'text-secondary': 'rgb(107 114 128)', // gray-600
        'text-tertiary': 'rgb(156 163 175)', // gray-400

        'bg-primary': 'rgb(255 255 255)',
        'bg-secondary': 'rgb(249 250 251)', // gray-50
        'bg-tertiary': 'rgb(243 244 246)', // gray-100

        'border-primary': 'rgb(229 231 235)', // gray-200
        'border-secondary': 'rgb(243 244 246)', // gray-100

        // Interactive states
        'interactive': {
          DEFAULT: 'rgb(59 130 246)', // blue-500
          hover: 'rgb(37 99 235)', // blue-600
          active: 'rgb(29 78 216)', // blue-700
          disabled: 'rgb(209 213 219)', // gray-300
        },
      },
    },
  },
};
```

### Dark Mode Configuration

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Colors that change in dark mode
        surface: {
          DEFAULT: '#FFFFFF',
          dark: '#0F172A',
        },
        'surface-raised': {
          DEFAULT: '#F9FAFB',
          dark: '#1E293B',
        },
      },

      // Or use CSS variables
      backgroundColor: {
        'primary': 'var(--color-bg-primary)',
        'secondary': 'var(--color-bg-secondary)',
      },
      textColor: {
        'primary': 'var(--color-text-primary)',
        'secondary': 'var(--color-text-secondary)',
      },
    },
  },
};
```

### Custom Color Utilities

```javascript
// tailwind.config.js
const plugin = require('tailwindcss/plugin');

module.exports = {
  plugins: [
    plugin(function({ addUtilities, theme }) {
      // Add custom utilities
      const colorUtilities = {
        '.text-on-primary': {
          color: theme('colors.white'),
        },
        '.text-on-secondary': {
          color: theme('colors.gray.900'),
        },
        '.surface-elevated': {
          backgroundColor: theme('colors.white'),
          boxShadow: theme('boxShadow.md'),
        },
      };

      addUtilities(colorUtilities);
    }),
  ],
};
```

### Using Colors in Components

```tsx
// Component with Tailwind semantic colors
function Button({ variant = 'primary', children }) {
  const variants = {
    primary: 'bg-interactive text-white hover:bg-interactive-hover',
    secondary: 'bg-bg-secondary text-text-primary hover:bg-bg-tertiary',
    danger: 'bg-error text-white hover:bg-error-dark',
  };

  return (
    <button className={`
      px-4 py-2 rounded-lg font-medium
      transition-colors duration-200
      ${variants[variant]}
    `}>
      {children}
    </button>
  );
}
```

---

## Anti-Patterns & Common Mistakes

### Color Selection Mistakes

**❌ Using Pure Colors Everywhere**:
```css
/* Too vibrant, causes eye strain */
.element {
  background: #FF0000; /* Pure red */
  color: #0000FF; /* Pure blue */
}
```

**✅ Use Toned Colors**:
```css
/* More sophisticated, easier on eyes */
.element {
  background: #DC2626; /* Toned red */
  color: #2563EB; /* Toned blue */
}
```

**❌ Too Many Colors**:
```javascript
// Visual chaos
const palette = {
  red: '#EF4444',
  orange: '#F97316',
  yellow: '#EAB308',
  green: '#10B981',
  blue: '#3B82F6',
  purple: '#8B5CF6',
  pink: '#EC4899',
  // ... 10 more colors
};
```

**✅ Focused Palette**:
```javascript
// Clear hierarchy
const palette = {
  primary: '#3B82F6',
  secondary: '#8B5CF6',
  success: '#10B981',
  error: '#EF4444',
  warning: '#F97316',
  neutral: { /* gray scale */ }
};
```

### Accessibility Mistakes

**❌ Insufficient Contrast**:
```css
/* Beautiful but inaccessible */
.subtle-text {
  color: #CCCCCC;
  background: #FFFFFF;
  /* Only 1.6:1 contrast - FAIL */
}
```

**✅ Meet WCAG Standards**:
```css
/* Accessible */
.readable-text {
  color: #666666;
  background: #FFFFFF;
  /* 5.74:1 contrast - PASS AA */
}
```

**❌ Color as Only Indicator**:
```html
<!-- Inaccessible -->
<span class="text-green-600">Available</span>
<span class="text-red-600">Unavailable</span>
```

**✅ Multiple Indicators**:
```html
<!-- Accessible -->
<span class="text-green-600">
  <CheckIcon /> Available
</span>
<span class="text-red-600">
  <XIcon /> Unavailable
</span>
```

### Implementation Mistakes

**❌ Hard-Coded Colors**:
```jsx
// Impossible to maintain or rebrand
function Button() {
  return (
    <button style={{
      background: '#3B82F6',
      color: '#FFFFFF'
    }}>
      Click me
    </button>
  );
}
```

**✅ Use Design Tokens**:
```jsx
// Easy to maintain and rebrand
function Button() {
  return (
    <button className="bg-primary text-white">
      Click me
    </button>
  );
}
```

**❌ Inconsistent Color Values**:
```css
/* Same blue, different values */
.button { background: #3B82F6; }
.link { color: rgb(59, 130, 246); }
.border { border-color: hsl(217, 91%, 60%); }
```

**✅ Single Source of Truth**:
```css
:root {
  --color-primary: #3B82F6;
}

.button { background: var(--color-primary); }
.link { color: var(--color-primary); }
.border { border-color: var(--color-primary); }
```

### Dark Mode Mistakes

**❌ Simply Inverting Colors**:
```css
/* Light mode */
.card { background: #FFFFFF; color: #000000; }

/* Dark mode - WRONG */
[data-theme="dark"] .card {
  background: #000000; /* Too harsh */
  color: #FFFFFF; /* Too bright */
}
```

**✅ Proper Dark Mode Colors**:
```css
/* Light mode */
.card { background: #FFFFFF; color: #111827; }

/* Dark mode - CORRECT */
[data-theme="dark"] .card {
  background: #1F2937; /* Softer dark */
  color: #F3F4F6; /* Softer light */
}
```

**❌ Same Saturation in Dark Mode**:
```css
[data-theme="dark"] {
  --color-primary: hsl(211, 92%, 50%); /* Too vibrant */
}
```

**✅ Reduce Saturation**:
```css
[data-theme="dark"] {
  --color-primary: hsl(211, 70%, 60%); /* Easier on eyes */
}
```

### Gradient Mistakes

**❌ Harsh Color Transitions**:
```css
/* Colors fight each other */
.gradient {
  background: linear-gradient(to right, #FF0000, #00FF00);
}
```

**✅ Harmonious Gradients**:
```css
/* Smooth, perceptually uniform */
.gradient {
  background: linear-gradient(
    in oklch,
    oklch(60% 0.15 30),
    oklch(80% 0.15 90)
  );
}
```

### Naming Mistakes

**❌ Visual Names in Code**:
```javascript
// Locks you into specific colors
const colors = {
  lightBlue: '#3B82F6',
  darkBlue: '#1E40AF'
};
```

**✅ Semantic Names**:
```javascript
// Flexible for rebranding
const colors = {
  primary: '#3B82F6',
  primaryDark: '#1E40AF'
};
```

---

## Summary & Quick Reference

### Color Model Decision Tree

```
Need to manipulate colors dynamically? → HSL
Need compact notation? → HEX
Need maximum color accuracy? → LCH/LAB
Need design tool compatibility? → HSB
Working with displays/hardware? → RGB
```

### WCAG Compliance Quick Check

```
Normal text: 4.5:1 (AA), 7:1 (AAA)
Large text (18pt+/14pt+ bold): 3:1 (AA), 4.5:1 (AAA)
UI components: 3:1
```

### Color Scale Essentials

```
50:  Subtle backgrounds
500: Primary/brand color
600: Hover states
800: Primary text
900: Headings
```

### Semantic Color Categories

```
Brand: Primary, Secondary
Feedback: Success, Error, Warning, Info
Content: Text (primary/secondary/tertiary)
Surface: Backgrounds (primary/secondary/tertiary)
Interactive: Default, Hover, Active, Disabled
Border: Primary, Secondary
```

### Dark Mode Checklist

- [ ] Use dark gray (#0F172A), not pure black
- [ ] Use off-white (#F3F4F6), not pure white
- [ ] Reduce saturation 15-30%
- [ ] Increase lightness of brand colors
- [ ] Test contrast in both modes
- [ ] Use surface elevation for hierarchy

### Accessibility Checklist

- [ ] All text meets WCAG AA (4.5:1)
- [ ] Heading text meets WCAG AAA (7:1)
- [ ] UI components have 3:1 contrast
- [ ] Links distinguishable without color
- [ ] Status indicators use icons + color
- [ ] Forms show text errors, not just red borders
- [ ] Charts use patterns or shapes
- [ ] Test with color-blind simulator

### Color-Blind Safe Practices

- [ ] Never use color alone
- [ ] Provide text labels or icons
- [ ] Use patterns in data viz
- [ ] Avoid red/green only combinations
- [ ] Ensure sufficient brightness differences
- [ ] Test with simulation tools

---

## When to Use This Skill

**Automatically load when**:
- Files match: `**/colors.*`, `**/palette.*`, `**/theme.*`
- Keywords: "color palette", "contrast ratio", "accessibility", "dark mode"

**Manually invoke for**:
- Building new design system
- Ensuring WCAG compliance
- Creating data visualizations
- Implementing dark mode
- Rebranding projects
- Color-blind accessibility improvements

**Key Principles**:
1. Accessibility is non-negotiable (WCAG AA minimum)
2. Use semantic naming for flexibility
3. Test in both light and dark modes
4. Consider color-blind users from start
5. Use perceptually uniform scales
6. Validate programmatically

---

## Additional Resources

**Books**:
- "Refactoring UI" by Adam Wathan & Steve Schoger
- "The Elements of Color" by Johannes Itten
- "Interaction of Color" by Josef Albers

**Standards**:
- WCAG 2.1 Color Contrast Guidelines
- Material Design Color System
- Human Interface Guidelines (Apple)

**Tools**:
- Coolors.co - Palette generation
- Contrast Ratio - WCAG checking
- Color Oracle - Color blindness simulation
- Chroma.js - Color manipulation library

**Scientific Palettes**:
- ColorBrewer - Cartography palettes
- Viridis - Perceptually uniform
- Paul Tol's Schemes - Color-blind safe
- IBM Carbon - Enterprise design

---

This skill provides comprehensive guidance for all aspects of color systems in digital product design, from theory to implementation, with a strong focus on accessibility and maintainability.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

