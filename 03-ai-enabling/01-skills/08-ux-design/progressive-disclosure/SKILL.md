---
last_updated: 2026-02-25
status: active
name: progressive-disclosure
description: Reveal complexity progressively - show basic options first, advanced on demand. Use for reducing cognitive load.
triggers:
  files: ["**/wizard/**", "**/onboarding/**", "**/settings/**"]
  keywords: ["progressive disclosure", "show more", "advanced options", "expand", "accordion", "wizard", "step by step", "reveal"]
allowed-tools: Read, Write, Edit
---

# Progressive Disclosure Skill

Master guide for designing interfaces that reveal information and options progressively, reducing cognitive load while maintaining access to advanced features.

## Philosophy

**Simplicity first, complexity on demand.** Users shouldn't face every option at once. Show what most people need; let power users dig deeper.

**Respect cognitive load.** Working memory is limited (~4 items). Progressive disclosure keeps users focused on the current decision.

**Trust the 80/20 rule.** 80% of users use 20% of features. Surface the common cases; progressively reveal the rest.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Core Principles

### 1. Staged Complexity

| Stage | Content | Example |
|-------|---------|---------|
| Initial | Essential options only | Email, Password |
| On demand | Secondary options | "Show advanced" reveals more |
| Deep | Power user features | Developer settings, API keys |

### 2. Information Scent

Each disclosure trigger must hint at what's revealed:
```
❌ Bad:  [More] → ???
✅ Good: [Show formatting options] → Font, size, color
```

### 3. Reversibility

Users must be able to:
- Collapse what they expanded
- Return to simple view
- Reset to defaults

---

## Disclosure Patterns

### 1. Expand/Collapse

**Accordion**:
```
▼ Basic Settings (expanded)
  ├─ Option 1
  ├─ Option 2
  └─ Option 3

▶ Advanced Settings (collapsed)
▶ Expert Settings (collapsed)
```

**Best for**: Settings, FAQs, documentation sections

**Guidelines**:
- Allow multiple open (usually better for settings)
- Or force single open (better for FAQs)
- Clear expand/collapse affordance
- Remember state across sessions

### 2. Show More/Less

**Inline expansion**:
```
This is the beginning of a long description that
provides important context about the product...
[Read more]

↓ (after click)

This is the beginning of a long description that
provides important context about the product and
includes all the additional details that were
previously hidden from view to save space.
[Show less]
```

**Best for**: Long text, lists, search results

### 3. Stepped Wizard

**Multi-step form**:
```
Step 1/4: Basics
┌─────────────────────────────┐
│ Name: [_______________]     │
│ Email: [______________]     │
│                             │
│         [Continue →]        │
└─────────────────────────────┘

Step 2/4: Details (after step 1 complete)
...
```

**Best for**: Complex forms, onboarding, checkout

**Guidelines**:
- Show progress (step X of Y)
- Allow back navigation
- Save progress
- Group related fields

### 4. Layered Interface

**Basic → Advanced toggle**:
```
Mode: [Simple ● | Advanced]

Simple view:
┌─────────────────────────────┐
│ Search: [________________]  │
│ [Search]                    │
└─────────────────────────────┘

Advanced view (toggle):
┌─────────────────────────────┐
│ Search: [________________]  │
│ Filter: [All types ▼]       │
│ Date:   [Last 30 days ▼]    │
│ Sort:   [Relevance ▼]       │
│ [Search]                    │
└─────────────────────────────┘
```

**Best for**: Search, filters, form builders

### 5. Tooltip/Popover Layers

**Information layering**:
```
Field Label [?]  ← Hover/click for help

Tooltip (hover):
┌──────────────────────┐
│ Brief explanation    │
└──────────────────────┘

Popover (click):
┌────────────────────────────┐
│ Detailed explanation with  │
│ examples and links:        │
│ • [Learn more]             │
│ • [See documentation]      │
└────────────────────────────┘

Modal (if critical):
┌────────────────────────────┐
│ Complete help content      │
│ with images, videos, etc.  │
└────────────────────────────┘
```

### 6. Contextual Reveal

**Conditional fields**:
```
Shipping method:
( ) Standard
( ) Express
(●) Store pickup

[When Store pickup selected:]
┌─────────────────────────────┐
│ Select store:               │
│ ( ) Downtown - 0.5 mi       │
│ ( ) Mall - 2.3 mi           │
│ ( ) Airport - 5.1 mi        │
└─────────────────────────────┘
```

**Best for**: Forms with conditional logic

### 7. Drill-Down Navigation

**Hierarchical reveal**:
```
Level 1:              Level 2:
Settings          →   Account
                     └─ Profile
                     └─ Security
                     └─ Privacy
```

**Best for**: Settings, file browsers, categories

---

## Implementation Guidelines

### When to Use Progressive Disclosure

**Use when**:
- Information is secondary or optional
- Users have varying expertise levels
- Screen space is limited
- Choices are complex or numerous
- Full display would overwhelm

**Don't use when**:
- Information is critical for current decision
- Users need to compare all options simultaneously
- Hiding creates more friction than value
- Users expect all info upfront (e.g., pricing)

### Smart Defaults

Reduce disclosure needs with good defaults:

```
❌ Bad: Show 20 empty fields
✅ Good: Pre-fill sensible defaults

Country: [United States ▼]  ← Auto-detected
Time Zone: [EST ▼]          ← Based on country
```

### Progressive Disclosure Levels

| Level | Trigger | Example |
|-------|---------|---------|
| 1 | Always visible | Core functionality |
| 2 | One click | "Show advanced" section |
| 3 | Two clicks | Settings → Advanced → Developer |
| 4 | Search/discover | Hidden easter eggs, CLI flags |

### Mobile Considerations

More aggressive disclosure on mobile:
- Smaller screens = less visible at once
- Accordions over tabs
- Bottom sheets for secondary options
- Full-screen modals for complex tasks

---

## Design Patterns

### Disclosure Triggers

**Visual affordances**:
```
▶ Collapsed (chevron right)
▼ Expanded (chevron down)
+ Add more
− Remove/collapse
[Show 5 more items]
[Advanced options ▼]
```

**Trigger placement**:
- End of content being expanded
- Or beginning of hidden content
- Never hidden itself

### Animation

```css
/* Smooth expand/collapse */
.accordion-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.accordion-content.open {
  max-height: 500px; /* or calculated height */
}
```

### State Persistence

Remember user preferences:
```javascript
// Remember expanded sections
localStorage.setItem('settings_expanded', JSON.stringify({
  basic: true,
  advanced: false,
  expert: false
}));
```

---

## Accessibility

### Keyboard Support

```
Enter/Space: Toggle expanded state
Arrow Down: Move to next item
Arrow Up: Move to previous item
Home: Move to first item
End: Move to last item
```

### ARIA Attributes

```html
<button
  aria-expanded="false"
  aria-controls="panel1"
>
  Show more
</button>
<div
  id="panel1"
  role="region"
  aria-hidden="true"
>
  Hidden content
</div>
```

### Screen Reader Announcements

- Announce expanded/collapsed state
- Announce content when revealed
- Provide context for what's hidden

---

## Anti-Patterns

### 1. Mystery Meat

```
❌ Bad:
[More] → ??? (User has no idea what's revealed)

✅ Good:
[Show shipping options ▼] → Clear expectation
```

### 2. Over-Nesting

```
❌ Bad:
Click → Click → Click → Click → Content (4 levels deep)

✅ Good:
Click → Content (max 2 levels for most content)
```

### 3. Hidden Critical Info

```
❌ Bad:
Price: $99 [click for details]
  → Hidden: $99 + $50 shipping + $20 tax = $169

✅ Good:
Subtotal: $99
Shipping: $50
Tax: $20
────────────
Total: $169 (all visible)
```

### 4. Mandatory Expansion

```
❌ Bad:
User MUST expand every section to proceed

✅ Good:
Sensible defaults, expand only if customizing
```

### 5. Lost Context

```
❌ Bad:
Expand → New page (loses context of where they were)

✅ Good:
Expand → Inline reveal (maintains context)
```

### 6. No Collapse Option

```
❌ Bad:
[Show more] → No way to collapse

✅ Good:
[Show more] ↔ [Show less] (bidirectional)
```

---

## Quick Reference

### Disclosure Decision Tree

```
Is info essential for current task?
├─ Yes → Show immediately
└─ No → Is it frequently needed?
        ├─ Yes → One click away
        └─ No → Two+ clicks / search
```

### Disclosure Checklist

- [ ] Clear trigger affordance (chevron, "more", etc.)
- [ ] Trigger text hints at content
- [ ] Smooth animation (200-300ms)
- [ ] Keyboard accessible
- [ ] ARIA attributes present
- [ ] State persisted appropriately
- [ ] Reversible (can collapse)
- [ ] Max 2 levels for common content
- [ ] Critical info not hidden

### Component Summary

| Pattern | Use Case | Trigger |
|---------|----------|---------|
| Accordion | Settings, FAQs | Header click |
| Show more | Long text, lists | Link at end |
| Wizard | Complex forms | Next button |
| Toggle view | Simple/advanced | Mode switch |
| Tooltip | Help text | Hover/focus |
| Contextual | Conditional fields | Selection change |
| Drill-down | Navigation | List item click |

---

## Summary

**Progressive disclosure = Right info at the right time**

1. Start with essential only
2. Provide clear paths to more
3. Never hide critical information
4. Maintain context during revelation
5. Allow reversibility

*The best interfaces show less, not more.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

