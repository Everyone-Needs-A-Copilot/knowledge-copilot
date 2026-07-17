---
last_updated: 2026-02-25
status: active
name: brand-visual-application
description: Apply brand identity consistently across digital interfaces - logo, color, typography, imagery. Use when implementing brand guidelines in UI design.
triggers:
  files: ["**/brand/**", "**/theme/**", "**/style-guide/**", "**/design-system/**"]
  keywords: ["brand identity", "brand guidelines", "visual identity", "brand consistency", "logo usage", "brand colors", "brand typography"]
allowed-tools: Read, Write, Edit
---

# Brand Visual Application

Brand visual application translates brand identity into consistent digital experiences. Proper application builds recognition, trust, and emotional connection with users.

## Core Principle

**Consistency breeds recognition.** Every visual element should reinforce brand identity without sacrificing usability.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Brand Elements

### Primary Elements

| Element | Purpose | Application |
|---------|---------|-------------|
| Logo | Recognition, trust | Header, favicon, loading states |
| Primary color | Identity, CTAs | Key actions, brand moments |
| Typography | Voice, readability | Headlines, body text |
| Imagery style | Personality, emotion | Photography, illustrations |

### Secondary Elements

| Element | Purpose | Application |
|---------|---------|-------------|
| Secondary colors | Variety, hierarchy | Supporting UI elements |
| Iconography | Functionality, style | Actions, navigation |
| Patterns/textures | Depth, interest | Backgrounds, accents |
| Motion style | Personality, feedback | Transitions, micro-interactions |

## Logo Application

### Placement Hierarchy

| Location | Usage | Requirements |
|----------|-------|--------------|
| Header (primary) | Constant brand presence | Full logo, prominent |
| Footer | Secondary presence | Can be simplified |
| Favicon | Browser tab | Simplified mark |
| Loading states | Brand moment | Logo or mark |
| App icon | Home screen | Simplified, recognizable |

### Clear Space Rules

```
┌─────────────────────────────────┐
│                                 │
│         X                       │  Minimum clear space
│    ┌─────────┐                  │  = height of "X" in logo
│  X │  LOGO   │ X                │  (or similar element)
│    └─────────┘                  │
│         X                       │
│                                 │
└─────────────────────────────────┘
```

### Logo Don'ts

| Violation | Problem | Rule |
|-----------|---------|------|
| Stretching | Distorts identity | Maintain proportions |
| Low contrast | Illegible | Meet contrast minimums |
| Crowded placement | Lost impact | Maintain clear space |
| Color alterations | Off-brand | Use approved colors only |
| Adding effects | Looks unprofessional | No shadows, glows, outlines |

## Color Application

### Color Hierarchy

| Level | Usage | Typical Colors |
|-------|-------|----------------|
| Primary | CTAs, key brand moments | 1-2 brand colors |
| Secondary | Supporting UI, variety | 2-3 complementary |
| Neutral | Text, backgrounds, borders | Grays, whites |
| Semantic | Status, feedback | Success/error/warning |

### Color Ratios (60-30-10 Rule)

```
┌─────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ 60% Neutral/Background
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ 30% Secondary
│████████████████████████████████████████│ 10% Primary/Accent
└─────────────────────────────────────────┘
```

### Color Mapping

| Brand Color | UI Application |
|-------------|----------------|
| Primary brand | Primary buttons, links, focus states |
| Secondary brand | Secondary buttons, highlights |
| Dark neutral | Primary text, headings |
| Medium neutral | Secondary text, icons |
| Light neutral | Borders, dividers, backgrounds |

## Typography Application

### Font Mapping

| Brand Font | UI Usage | Fallback |
|------------|----------|----------|
| Display font | H1, hero text | Sans-serif stack |
| Heading font | H2-H4, section titles | Sans-serif stack |
| Body font | Paragraphs, UI text | System sans-serif |
| Mono font | Code, technical | System monospace |

### Brand Voice in Type

| Brand Attribute | Typographic Expression |
|-----------------|------------------------|
| Professional | Clean sans-serif, regular weight |
| Friendly | Rounded fonts, looser tracking |
| Luxurious | Serif headlines, generous spacing |
| Technical | Monospace accents, tight tracking |
| Playful | Variable weights, expressive display |

## Imagery Guidelines

### Photography Style

| Brand Type | Photo Style |
|------------|-------------|
| Corporate | Professional, studio, diverse |
| Lifestyle | Natural, candid, aspirational |
| Technical | Clean, product-focused, minimal |
| Creative | Artistic, bold, unexpected |
| Healthcare | Warm, reassuring, authentic |

### Image Treatment

| Technique | Brand Fit | Application |
|-----------|-----------|-------------|
| Color overlay | Strong brand color | Heroes, cards |
| Duotone | Bold, modern brands | Feature images |
| Desaturated | Sophisticated, minimal | Backgrounds |
| High contrast | Energetic brands | Action shots |
| Soft/muted | Calm, wellness brands | Ambient imagery |

### Illustration Style

| Style | Brand Personality |
|-------|-------------------|
| Line art | Clean, minimal, technical |
| Flat | Modern, approachable, digital |
| Isometric | Technical, structured, SaaS |
| Hand-drawn | Friendly, casual, creative |
| 3D | Premium, innovative, bold |

## Component Brand Integration

### Button Branding

```css
/* Primary button: Brand color, brand radius, brand font */
.button-primary {
  background: var(--color-brand-primary);
  border-radius: var(--brand-radius);      /* Rounded for friendly, sharp for corporate */
  font-family: var(--font-brand-ui);
  font-weight: var(--brand-weight-button);
}
```

### Card Branding

| Brand Type | Card Style |
|------------|------------|
| Minimal | Subtle shadow, no border |
| Corporate | Light border, small radius |
| Playful | Larger radius, colorful accents |
| Premium | Generous padding, refined shadow |

### Navigation Branding

| Element | Brand Application |
|---------|-------------------|
| Logo placement | Consistent position |
| Link color | Brand or neutral |
| Active state | Brand color indicator |
| Hover effect | Brand-appropriate animation |

## Consistency Checklist

### Visual Identity
- [ ] Logo used correctly (size, spacing, color)
- [ ] Primary brand color applied to key actions
- [ ] Typography matches brand guidelines
- [ ] Imagery style is consistent

### UI Components
- [ ] Buttons use brand colors appropriately
- [ ] Form elements align with brand style
- [ ] Icons match brand illustration style
- [ ] Cards reflect brand personality

### Overall Experience
- [ ] Color ratios follow 60-30-10
- [ ] Brand moments at key touchpoints
- [ ] Consistent feel across pages
- [ ] Mobile experience matches desktop brand

## Brand Flexibility

### When to Adapt

| Context | Adaptation |
|---------|------------|
| Dark mode | Adjust color intensity |
| Mobile | Simplify complex elements |
| Accessibility | Ensure contrast compliance |
| Partner co-branding | Clear visual separation |
| Error states | Semantic colors take precedence |

### Brand Hierarchy

1. **Usability first** - Brand should enhance, not hinder
2. **Accessibility always** - Contrast trumps exact brand colors
3. **Context appropriate** - Error red over brand color for errors
4. **Recognition maintained** - Key brand elements always present

## Anti-Patterns

| Problem | Impact | Fix |
|---------|--------|-----|
| Brand color everywhere | Dilutes impact | Reserve for key moments |
| Logo too prominent | Distracts from content | Appropriate sizing |
| Typography mismatch | Feels off-brand | Use brand fonts consistently |
| Inconsistent imagery | Confuses identity | Follow style guide |
| Over-branding | Looks like ad | Balance brand with utility |

---

**Remember**: Brand application is not decoration - it's strategic communication. Every brand element should serve both identity and usability.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

