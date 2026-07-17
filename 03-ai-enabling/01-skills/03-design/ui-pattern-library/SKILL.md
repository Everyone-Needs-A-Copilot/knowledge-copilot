---
last_updated: 2026-02-25
status: active
name: ui-pattern-library
description: Build and maintain component pattern libraries with documentation, variants, and usage guidelines. Use when creating or organizing design system components.
triggers:
  files: ["**/components/**", "**/design-system/**", "**/patterns/**", "**/ui/**"]
  keywords: ["pattern library", "component library", "design system", "UI components", "reusable patterns", "component documentation"]
allowed-tools: Read, Write, Edit
---

# UI Pattern Library

A pattern library documents reusable UI components with their variants, states, and usage guidelines. Well-organized libraries accelerate development and ensure consistency.

## Core Principle

**Document once, use everywhere.** A pattern library is the single source of truth for how components look and behave.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Library Structure

### Recommended Organization

```
pattern-library/
├── foundations/
│   ├── colors/
│   ├── typography/
│   ├── spacing/
│   ├── icons/
│   └── motion/
├── components/
│   ├── buttons/
│   ├── inputs/
│   ├── cards/
│   ├── navigation/
│   └── feedback/
├── patterns/
│   ├── forms/
│   ├── search/
│   ├── authentication/
│   └── data-display/
└── templates/
    ├── dashboard/
    ├── settings/
    └── marketing/
```

### Component Categories

| Category | Contents | Examples |
|----------|----------|----------|
| Foundations | Design tokens, raw values | Colors, type scale, spacing |
| Components | Reusable UI elements | Buttons, inputs, cards |
| Patterns | Component combinations | Search, auth flow, forms |
| Templates | Full page layouts | Dashboard, settings, landing |

## Component Documentation

### Essential Documentation Elements

Every component needs:

| Element | Description |
|---------|-------------|
| **Name** | Clear, descriptive identifier |
| **Description** | What it is and when to use it |
| **Anatomy** | Visual breakdown of parts |
| **Variants** | Different versions (primary, secondary) |
| **States** | Interactive states (hover, active, disabled) |
| **Sizing** | Size options (sm, md, lg) |
| **Properties** | Configurable options |
| **Do's/Don'ts** | Usage guidelines |
| **Code** | Implementation example |

### Documentation Template

```markdown
## Button

### Description
Primary interactive element for triggering actions. Use for form submissions,
CTAs, and user-initiated operations.

### Anatomy
┌─────────────────────────────────┐
│ [Icon]  Label Text  [Icon]     │
└─────────────────────────────────┘
   ↑         ↑           ↑
Leading   Label      Trailing
 icon               icon (optional)

### Variants
| Variant | Use Case | Visual |
|---------|----------|--------|
| Primary | Main CTA, form submit | Filled, brand color |
| Secondary | Secondary actions | Outlined |
| Tertiary | Low-emphasis actions | Text only |
| Destructive | Delete, remove | Red filled |

### States
- Default, Hover, Active, Focus, Disabled, Loading

### Sizes
- Small (32px), Medium (40px), Large (48px)

### Properties
- label: string (required)
- variant: 'primary' | 'secondary' | 'tertiary' | 'destructive'
- size: 'sm' | 'md' | 'lg'
- disabled: boolean
- loading: boolean
- icon: IconName (optional)

### Do's
✓ Use sentence case for labels
✓ Keep labels concise (1-3 words)
✓ Use primary for one main CTA per view
✓ Provide loading state for async actions

### Don'ts
✗ Don't use multiple primary buttons
✗ Don't use vague labels ("Click here")
✗ Don't disable without explanation
✗ Don't change label during loading
```

## Component Anatomy

Document the structural parts of each component:

### Card Anatomy Example

```
┌────────────────────────────────────┐
│ ┌──────────────────────────────┐   │
│ │         Media/Image          │   │ ← Media (optional)
│ └──────────────────────────────┘   │
│                                    │
│  Overline Text                     │ ← Overline (optional)
│  Card Title                        │ ← Title (required)
│  Supporting text that provides     │ ← Description (optional)
│  additional context about card.    │
│                                    │
│  [Secondary]  [Primary Action]     │ ← Actions (optional)
└────────────────────────────────────┘
     ↑ Padding (--space-4)
```

## States Documentation

### Interactive State Matrix

| State | Trigger | Visual Treatment |
|-------|---------|------------------|
| Default | Initial render | Base styling |
| Hover | Mouse over | Slight color change, cursor |
| Focus | Tab navigation | Focus ring |
| Active | Mouse down | Pressed effect |
| Disabled | disabled=true | Reduced opacity, no cursor |
| Loading | Async operation | Spinner, disabled |
| Error | Validation fail | Error color, icon |
| Success | Positive result | Success color, icon |

### State Specification Example

```css
/* Button states */
.button {
  /* Default */
  background: var(--color-primary);

  /* Hover */
  &:hover:not(:disabled) {
    background: var(--color-primary-dark);
  }

  /* Active */
  &:active:not(:disabled) {
    transform: translateY(1px);
  }

  /* Focus */
  &:focus-visible {
    outline: 2px solid var(--color-focus-ring);
    outline-offset: 2px;
  }

  /* Disabled */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
```

## Pattern Composition

### Form Pattern Example

```markdown
## Form Pattern

### Components Used
- Form Container
- Form Group (label + input + helper)
- Text Input
- Select
- Checkbox
- Button (submit)

### Layout Rules
1. Single column for mobile
2. Two columns for related fields (first/last name)
3. Full width for textarea
4. Right-aligned submit button

### Spacing
- Between form groups: var(--space-6)
- Label to input: var(--space-2)
- Input to helper: var(--space-1)
- Before submit: var(--space-8)

### Validation
- Inline validation on blur
- Summary at top for submission errors
- Success state on valid fields
```

## Naming Conventions

### Component Names

| Pattern | Example | Use For |
|---------|---------|---------|
| PascalCase | `ButtonPrimary` | React components |
| kebab-case | `button-primary` | CSS classes, files |
| SCREAMING_SNAKE | `BUTTON_VARIANTS` | Constants |

### Token Names

```
--{category}-{property}-{variant}-{state}

Examples:
--color-text-primary
--color-background-secondary
--button-padding-md
--input-border-error
```

### File Structure

```
button/
├── Button.tsx           # Component
├── Button.test.tsx      # Tests
├── Button.stories.tsx   # Storybook stories
├── Button.module.css    # Styles
├── index.ts             # Public exports
└── README.md            # Documentation
```

## Version Management

### Semantic Versioning

| Change Type | Version Bump | Examples |
|-------------|--------------|----------|
| Breaking | Major (1.0 → 2.0) | Removing prop, changing API |
| Feature | Minor (1.0 → 1.1) | New variant, new component |
| Fix | Patch (1.0.0 → 1.0.1) | Bug fix, typo, alignment |

### Deprecation Strategy

1. Mark deprecated in docs
2. Add console warning
3. Provide migration guide
4. Remove in next major version

```tsx
/** @deprecated Use `Button` with variant="outline" instead */
export const OutlineButton = deprecated(Button);
```

## Quality Checklist

### Component Readiness

- [ ] Documentation complete (description, variants, states)
- [ ] All variants implemented
- [ ] All states styled
- [ ] Accessible (ARIA, keyboard, screen reader)
- [ ] Responsive behavior defined
- [ ] Unit tests written
- [ ] Visual regression tests
- [ ] Storybook stories for all variants

### Library Maintenance

- [ ] Consistent naming conventions
- [ ] Up-to-date documentation
- [ ] Changelog maintained
- [ ] Breaking changes documented
- [ ] Migration guides provided
- [ ] Regular audits for unused patterns

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Undocumented variants | Inconsistent usage | Document all options |
| Missing states | Incomplete UX | Define all interactive states |
| No usage guidelines | Misuse of components | Add do's and don'ts |
| Stale documentation | Drift from implementation | Automate doc generation |
| Single-use patterns | Library bloat | Refactor or remove |

---

**Remember**: A pattern library is only valuable if it's used. Make it easy to find, easy to understand, and easy to implement.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

