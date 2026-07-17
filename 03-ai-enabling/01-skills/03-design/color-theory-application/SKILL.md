---
last_updated: 2026-02-25
status: active
name: color-theory-application
description: Apply color theory for harmonious palettes, effective contrast, and psychological impact. Use when designing color systems or reviewing color choices.
triggers:
  files: ["**/colors/**", "**/palette/**", "**/theme/**"]
  keywords: ["color theory", "color harmony", "color palette", "contrast", "color psychology", "color scheme", "color system"]
allowed-tools: Read, Write, Edit
---

# Color Theory Application

Color theory provides frameworks for creating harmonious, effective color palettes. Understanding color relationships and psychological effects enables intentional design decisions.

## Core Principle

**Color communicates before words.** Every color choice carries meaning, evokes emotion, and influences perception.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Color Relationships

### The Color Wheel

Primary relationships on the 12-hue color wheel:

| Relationship | Definition | Example (Base: Blue) |
|--------------|------------|----------------------|
| Complementary | Opposite on wheel | Orange |
| Analogous | Adjacent (2-3 colors) | Blue-violet, Blue-green |
| Triadic | Equal thirds (120°) | Blue, Yellow, Red |
| Split-complementary | Base + 2 adjacent to complement | Blue, Yellow-orange, Red-orange |
| Tetradic | Rectangle (4 colors) | Blue, Orange, Red, Green |
| Square | Equal quarters (90°) | Blue, Yellow-green, Orange, Red-violet |

### Harmony Formulas

| Harmony | Best For | Character |
|---------|----------|-----------|
| Monochromatic | Elegant, focused | Single hue, varied lightness/saturation |
| Analogous | Natural, serene | 2-3 adjacent hues |
| Complementary | Dynamic, high contrast | Opposite hues |
| Triadic | Balanced, vibrant | Three evenly spaced hues |
| Split-complementary | Nuanced contrast | Less tension than complementary |

## Color Properties

### HSL Model

| Property | Range | Effect |
|----------|-------|--------|
| Hue | 0-360° | The "color" - position on wheel |
| Saturation | 0-100% | Intensity - gray to vivid |
| Lightness | 0-100% | Brightness - black to white |

### Creating Variations

From a base color, create a scale:

```css
/* Base: hsl(220, 80%, 50%) - Blue */
--color-50:  hsl(220, 80%, 97%);  /* Near white */
--color-100: hsl(220, 80%, 94%);
--color-200: hsl(220, 80%, 86%);
--color-300: hsl(220, 80%, 74%);
--color-400: hsl(220, 80%, 62%);
--color-500: hsl(220, 80%, 50%);  /* Base */
--color-600: hsl(220, 80%, 42%);
--color-700: hsl(220, 80%, 34%);
--color-800: hsl(220, 80%, 26%);
--color-900: hsl(220, 80%, 18%);
--color-950: hsl(220, 80%, 10%);  /* Near black */
```

## Color Psychology

| Color | Associations | Use Cases |
|-------|--------------|-----------|
| Red | Energy, urgency, danger, passion | Errors, CTAs, sales |
| Orange | Warmth, enthusiasm, creativity | CTAs, playful brands |
| Yellow | Optimism, caution, attention | Warnings, highlights |
| Green | Growth, success, nature, money | Success states, eco brands |
| Blue | Trust, calm, professionalism | Finance, tech, healthcare |
| Purple | Luxury, creativity, mystery | Premium, creative brands |
| Pink | Care, romance, youth | Feminine brands, wellness |
| Brown | Earth, reliability, warmth | Organic, outdoors |
| Black | Sophistication, power, luxury | Premium, fashion |
| White | Purity, simplicity, space | Minimal, healthcare |
| Gray | Neutral, professional, balance | UI elements, backgrounds |

### Cultural Considerations

| Color | Western | Eastern | Middle Eastern |
|-------|---------|---------|----------------|
| White | Purity | Mourning | Purity |
| Red | Danger, love | Luck, prosperity | Danger |
| Yellow | Happiness | Imperial, sacred | Happiness |
| Green | Nature, money | Eternal life | Islam, paradise |
| Blue | Trust, sadness | Immortality | Protection |

## Contrast & Accessibility

### WCAG Contrast Requirements

| Use Case | Minimum Ratio | Preferred |
|----------|---------------|-----------|
| Body text | 4.5:1 (AA) | 7:1 (AAA) |
| Large text (18px+) | 3:1 (AA) | 4.5:1 (AAA) |
| UI components | 3:1 (AA) | 4.5:1 |
| Non-essential decorative | No requirement | - |

### Practical Contrast

| Background | Minimum Text Color |
|------------|-------------------|
| White (#FFF) | #595959 (4.5:1) |
| Light gray (#F5F5F5) | #525252 (4.5:1) |
| Dark (#1A1A1A) | #A8A8A8 (4.5:1) |
| Brand blue (#2563EB) | #FFFFFF (4.5:1) |

## Palette Construction

### UI Palette Components

A complete UI palette needs:

| Category | Purpose | Typical Colors |
|----------|---------|----------------|
| Primary | Brand, key actions | 1 color + variations |
| Secondary | Supporting actions | 1 color + variations |
| Neutral | Text, backgrounds, borders | Gray scale (10+ shades) |
| Success | Positive feedback | Green |
| Warning | Caution states | Yellow/amber |
| Error | Errors, destructive | Red |
| Info | Informational | Blue |

### Building a Palette

1. **Start with primary** - Brand or key action color
2. **Create neutral scale** - 10+ grays from near-white to near-black
3. **Add semantic colors** - Success, warning, error, info
4. **Test contrast** - Verify all text combinations
5. **Document usage** - Define when each color applies

## Dark Mode Considerations

| Light Mode | Dark Mode Approach |
|------------|-------------------|
| White background | Dark gray (#121212), not pure black |
| Dark text | Light gray (#E0E0E0), not pure white |
| Saturated colors | Desaturate slightly for comfort |
| Strong shadows | Reduce or eliminate shadows |
| Brand colors | May need brightness adjustment |

## Evaluation Checklist

- [ ] Primary/secondary colors have clear purpose
- [ ] Neutral scale has 10+ shades
- [ ] All text passes WCAG AA contrast (4.5:1)
- [ ] Color meanings are consistent (red = error everywhere)
- [ ] Palette works in dark mode
- [ ] Colors are distinguishable for color-blind users
- [ ] No more than 5-6 distinct hues in palette

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Too many colors | Visual chaos | Limit to 5-6 hues max |
| Low contrast | Inaccessible | Test all combinations |
| Inconsistent meaning | Confusing UX | Red = error everywhere |
| Pure black/white | Harsh, fatiguing | Use near-black/near-white |
| Ignoring color blindness | Excludes 8% of men | Don't rely on color alone |
| Over-saturation | Eye strain | Balance vivid with muted |

---

**Remember**: Color should support meaning, not replace it. Never communicate information through color alone.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

