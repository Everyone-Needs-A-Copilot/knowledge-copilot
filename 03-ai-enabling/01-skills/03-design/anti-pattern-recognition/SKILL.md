---
last_updated: 2026-02-25
status: active
name: anti-pattern-recognition
description: Identify UI anti-patterns like mystery meat navigation, unclear affordances, and poor information architecture. Use when reviewing designs for usability issues.
triggers:
  files: ["**/design/**", "**/ui/**", "**/components/**"]
  keywords: ["anti-pattern", "usability issue", "UX problem", "mystery meat", "bad UX", "design review", "usability audit"]
allowed-tools: Read, Write, Edit
---

# UI Anti-Pattern Recognition

UI anti-patterns are common design mistakes that harm user experience. Recognizing these patterns helps prevent usability problems before they reach users.

## Core Principle

**Anti-patterns feel clever but frustrate users.** If users must think about how to use your UI, something is wrong.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Navigation Anti-Patterns

### Mystery Meat Navigation

**Problem:** Links/buttons with no clear indication of destination or action.

| Symptom | Example | Fix |
|---------|---------|-----|
| Icon-only buttons | Ambiguous icons without labels | Add text labels |
| Vague labels | "Click here", "Learn more" | Describe destination |
| Image-based nav | Unlabeled image buttons | Add visible text |
| Hidden menus | No indication of expandable sections | Show affordances |

**Test:** Can users predict where each link goes before clicking?

### Hamburger Menu Overuse

**Problem:** Hiding critical navigation behind hamburger menu on desktop.

| Symptom | Impact | Fix |
|---------|--------|-----|
| All nav in hamburger | Users miss key features | Expose primary nav |
| Important actions hidden | Reduced engagement | Surface top tasks |
| Desktop hamburger | Wastes available space | Use horizontal nav |

**Guideline:** Hamburger is acceptable on mobile; expose navigation on desktop.

### Infinite Pagination

**Problem:** Endless scroll without progress indication or way to return.

| Symptom | Impact | Fix |
|---------|--------|-----|
| No page indicators | Users feel lost | Show position/count |
| Can't bookmark position | Content unfindable later | Add URL state |
| Footer unreachable | Important links hidden | Sticky footer or pagination |

## Form Anti-Patterns

### Reset Button Adjacent to Submit

**Problem:** Easy to accidentally clear form instead of submitting.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Reset next to Submit | Data loss | Remove reset or separate |
| Same visual weight | Confusion | Style destructive differently |
| No confirmation | Instant loss | Add confirmation dialog |

### Disabled Submit Without Explanation

**Problem:** Submit button disabled with no indication why.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Grayed button, no text | User confusion | Explain what's missing |
| Validation not shown | Users guess | Inline validation |
| Required fields unclear | Frustration | Mark required fields |

### Field Label Disappearing on Focus

**Problem:** Placeholder text used as label vanishes when typing.

| Symptom | Impact | Fix |
|---------|--------|-----|
| No persistent label | User forgets field purpose | Label above input |
| Placeholder as hint | Hint lost during input | Separate label + hint |
| Light placeholder | Poor accessibility | Darker text, external label |

## Content Anti-Patterns

### Wall of Text

**Problem:** Dense paragraphs without visual breaks.

| Symptom | Impact | Fix |
|---------|--------|-----|
| No headings | Users can't scan | Add hierarchy |
| Long paragraphs | Low comprehension | Break into chunks |
| No whitespace | Visual fatigue | Add spacing |

### Carousel Syndrome

**Problem:** Important content hidden in rotating carousels.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Auto-rotating | Users miss content | Manual controls only |
| No position indicators | Users feel lost | Show progress dots |
| Critical info in slides | Key content missed | Static hero instead |

**Research:** Carousels have <1% click rate on secondary slides.

### Modal Overload

**Problem:** Excessive use of modal dialogs interrupting flow.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Modal on page load | Annoying, ignored | Wait for user action |
| Nested modals | Confusing layers | One modal at a time |
| Non-dismissable | Trapped feeling | Always allow close |
| Form in modal | Context lost | Inline or separate page |

## Interaction Anti-Patterns

### Click Target Mismatch

**Problem:** Clickable area smaller than visual element suggests.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Text link (no padding) | Hard to click | Min 44px touch target |
| Icon-only button (small) | Missed clicks | Increase hit area |
| Checkbox label not clickable | Reduced usability | Label triggers input |

### False Affordance

**Problem:** Non-interactive elements that look clickable.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Underlined text (not link) | User tries to click | Remove decoration |
| Blue text (not link) | Confusion | Use neutral color |
| Button-styled div | Dead click | Make interactive or restyle |

### Surprise Navigation

**Problem:** Links that unexpectedly leave context (new tab, external site, download).

| Symptom | Impact | Fix |
|---------|--------|-----|
| Silent external links | Users disoriented | External link icon |
| Auto-download | Unwanted files | Warn before download |
| Unannounced new tabs | Tab clutter | Indicate or avoid |

## Information Architecture Anti-Patterns

### Deep Nesting

**Problem:** Important content buried many levels deep.

| Symptom | Impact | Fix |
|---------|--------|-----|
| 4+ levels of nav | Users give up | Flatten hierarchy |
| Important items hidden | Low discovery | Surface key content |
| Breadcrumb overflow | Lost context | Reduce depth |

**Guideline:** Users should reach any content in 3 clicks or fewer.

### Inconsistent Location

**Problem:** Same action/info appears in different places across pages.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Moving navigation | Users relearn each page | Consistent placement |
| Different labels | Same action, different text | Standardize terminology |
| Scattered settings | Hard to find | Single settings location |

### Junk Drawer Category

**Problem:** Catch-all categories that don't help users find content.

| Symptom | Impact | Fix |
|---------|--------|-----|
| "Miscellaneous" | Users search randomly | Proper categorization |
| "Other" as primary | Vague, unhelpful | Specific categories |
| Large uncategorized list | Overwhelming | Group by task/topic |

## Feedback Anti-Patterns

### Silent Failure

**Problem:** Actions fail without notification.

| Symptom | Impact | Fix |
|---------|--------|-----|
| No error message | User retries blindly | Clear error states |
| Generic "error occurred" | No actionable info | Specific guidance |
| Success not confirmed | Uncertainty | Confirm successful actions |

### Crying Wolf Alerts

**Problem:** Overuse of alerts desensitizes users.

| Symptom | Impact | Fix |
|---------|--------|-----|
| Everything is "urgent" | Nothing is urgent | Reserve for real urgency |
| Constant notifications | Banner blindness | Reduce frequency |
| Same style for all | Can't prioritize | Vary severity styles |

## Anti-Pattern Audit Checklist

### Navigation
- [ ] All interactive elements have clear labels
- [ ] Primary navigation visible on desktop
- [ ] Users can tell where links go before clicking
- [ ] External links are indicated

### Forms
- [ ] Labels persist during input
- [ ] Required fields marked
- [ ] Disabled states explained
- [ ] Destructive actions separated/confirmed

### Content
- [ ] Text broken into scannable chunks
- [ ] Important content not in carousels
- [ ] Modals used sparingly

### Interaction
- [ ] Click targets are 44px+ on touch
- [ ] Only interactive elements look clickable
- [ ] Actions have clear feedback

### Information Architecture
- [ ] Key content reachable in 3 clicks
- [ ] Navigation consistent across pages
- [ ] Categories are specific and useful

---

**Remember**: Anti-patterns persist because they seem logical to designers. Always test with real users to catch what seems obvious but isn't.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

