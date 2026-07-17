---
last_updated: 2026-02-25
status: active
name: accessibility-copy
description: Write accessible copy that works for all users including those using assistive technologies. Use for alt text, ARIA labels, accessible link text, form labels, and inclusive language.
triggers:
  files: ["**/a11y/**", "**/accessibility/**", "**/components/**", "**/*.tsx", "**/*.jsx"]
  keywords: ["accessibility", "a11y", "screen reader", "alt text", "ARIA label", "accessible", "inclusive", "assistive technology", "WCAG"]
allowed-tools: Read, Write, Edit
---

# Accessibility Copy Skill

Write copy that works for everyone, including users of screen readers, voice control, and other assistive technologies. Accessible copy ensures all users can navigate, understand, and interact with your content.

---

## Core Principles

### Accessible Copy Mindset

| Principle | Description | Example |
|-----------|-------------|---------|
| Meaningful | Conveys purpose, not just presence | "Download report PDF" not "Click here" |
| Context-independent | Makes sense without visuals | Full meaning in text alone |
| Consistent | Same action = same terminology | Always "Delete" not mix "Remove/Trash" |
| Descriptive | Specific about what happens | "Opens in new tab" not just icon |
| Inclusive | Respects all abilities | "Select" not "Click" |

### Who Benefits

| User Group | Accessibility Need |
|------------|-------------------|
| Blind users | Screen reader compatibility |
| Low vision | Clear, large text; good contrast |
| Deaf users | Captions, text alternatives |
| Motor impaired | Keyboard navigation, large targets |
| Cognitive | Simple language, clear structure |
| Temporary | Injury, environment, situation |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Alternative Text

### Alt Text Formula

For informational images:
```
[What] + [Why it matters in context]
```

For functional images (buttons, links):
```
[What action this performs]
```

### Alt Text by Image Type

| Image Type | Alt Text Approach | Example |
|------------|-------------------|---------|
| Informational | Describe content and purpose | "Bar chart showing 40% increase in sales Q3 vs Q2" |
| Functional | Describe action | "Submit form" |
| Decorative | Empty alt or CSS | `alt=""` (not omitted) |
| Complex | Brief alt + long description | "Sales data chart. Full data in table below." |
| Logo | Company name | "Acme Corp logo" |

### Alt Text Guidelines

| Do | Don't |
|----|-------|
| Be specific and concise | Start with "Image of" or "Picture of" |
| Describe relevant content | Describe every visual detail |
| Include text in image | Rely on surrounding text |
| Consider context | Write generic descriptions |

### Alt Text Examples

| Context | Bad | Good |
|---------|-----|------|
| Product photo | "Shoe" | "Navy blue running shoe, side view" |
| Team photo | "Team meeting" | "Marketing team discussing Q4 campaign around conference table" |
| Button icon | "Arrow" | "Download PDF" |
| Infographic | "Statistics" | "Key findings: 80% prefer mobile. See full data below." |

---

## Link Text

### Accessible Link Principles

| Principle | Implementation |
|-----------|----------------|
| Descriptive | Link text explains destination |
| Context-free | Makes sense out of context |
| Unique | Different links have different text |
| Specific | Names the resource or action |

### Link Text Patterns

| Bad | Good | Why |
|-----|------|-----|
| "Click here" | "View pricing details" | Descriptive |
| "Learn more" | "Learn more about accessibility" | Specific |
| "Read more" | "Read the full case study" | Names content |
| "Here" | "Download the annual report" | Action + object |

### Links Opening New Windows

Always indicate:
```
"View documentation (opens in new tab)"
```

Or visually with icon + accessible text:
```
<a href="...">Documentation <span class="sr-only">(opens in new tab)</span></a>
```

---

## Form Labels and Instructions

### Label Requirements

| Element | Requirement | Example |
|---------|-------------|---------|
| Input fields | Visible, associated label | `<label for="email">Email</label>` |
| Required fields | Clear indication | "Email (required)" or `aria-required="true"` |
| Format requirements | Visible instructions | "Date format: MM/DD/YYYY" |
| Error states | Descriptive error + association | "Email is required" linked to field |

### Form Instructions

Place instructions before or within labels:

```
Email address
[                              ]
We'll send a confirmation link to this address
```

### Error Messages for Accessibility

| Requirement | Implementation |
|-------------|----------------|
| Programmatically associated | `aria-describedby` or `aria-errormessage` |
| Announced to screen readers | `role="alert"` or live region |
| Specific | Names the field and the fix |
| Persistent | Stays visible until fixed |

```
Bad:  "Invalid input"
Good: "Email address must include @ symbol"
```

---

## Button and Action Text

### Accessible Button Patterns

| Context | Button Text | Why |
|---------|-------------|-----|
| Single action | "Save changes" | Specific action |
| Repeated in list | "Delete 'Project Alpha'" | Unique, specific |
| Icon-only | Hidden text + icon | "Delete" (sr-only) + icon |
| Toggle | State-aware | "Mute notifications" / "Unmute notifications" |

### Icon Buttons

Always provide accessible text:

```html
<!-- Approach 1: Visually hidden text -->
<button>
  <span class="sr-only">Close dialog</span>
  <svg>...</svg>
</button>

<!-- Approach 2: aria-label -->
<button aria-label="Close dialog">
  <svg>...</svg>
</button>
```

### Dynamic State Changes

Announce state changes:
```
"Notification muted" (announced after toggle)
"3 items selected" (announced as selection changes)
```

---

## Screen Reader Announcements

### When to Announce

| Event | Announcement |
|-------|--------------|
| Form submitted | "Form submitted successfully" |
| Content loaded | "Search results loaded, 24 items" |
| Error occurred | "Error: [specific error message]" |
| Page navigation | New page title announced |
| Modal opened | Focus moves, title announced |

### Live Region Patterns

| Urgency | ARIA Attribute | Use Case |
|---------|----------------|----------|
| Polite | `aria-live="polite"` | Status updates, non-urgent |
| Assertive | `aria-live="assertive"` | Errors, critical alerts |
| Status | `role="status"` | Status messages |
| Alert | `role="alert"` | Immediate attention needed |

---

## Inclusive Language

### Ability-Neutral Language

| Avoid | Use | Why |
|-------|-----|-----|
| "See the results" | "View the results" | Doesn't assume sight |
| "Click the button" | "Select the button" | Works for keyboard/voice |
| "Watch the video" | "Play the video" | Doesn't assume hearing |
| "As you can see" | "As shown" or remove | Doesn't assume sight |

### Respectful References

| Avoid | Use |
|-------|-----|
| "Wheelchair-bound" | "Wheelchair user" |
| "Suffers from" | "Has" or "Lives with" |
| "Normal users" | "Users without disabilities" |
| "Handicapped" | "Disabled" or specific condition |

### Reading Level

| Guideline | Implementation |
|-----------|----------------|
| Aim for 8th grade | Short sentences, common words |
| Define jargon | Explain technical terms |
| One idea per sentence | Break complex ideas down |
| Use active voice | "We sent your email" not "Your email was sent" |

---

## Headings and Structure

### Heading Hierarchy

| Rule | Implementation |
|------|----------------|
| Logical order | h1 → h2 → h3, no skipping |
| Descriptive | Summarizes section content |
| Unique | Different headings for different sections |
| Not just visual | Use semantic elements, not just styling |

### Heading Text Guidelines

| Bad | Good |
|-----|------|
| "More information" | "Pricing and plans" |
| "Section 1" | "Getting started" |
| "Details" | "Shipping details" |

---

## Tables and Data

### Accessible Table Copy

| Element | Requirement |
|---------|-------------|
| Caption | Describes table purpose |
| Headers | Clear, specific column/row labels |
| Summary | Complex tables need explanation |

```html
<table>
  <caption>Q3 2024 Sales by Region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  ...
</table>
```

---

## ARIA Labels

### When to Use ARIA Labels

| Use Case | Example |
|----------|---------|
| Icon-only buttons | `aria-label="Close"` |
| Ambiguous links | `aria-label="Edit profile settings"` |
| Form regions | `aria-labelledby="section-heading"` |
| Dynamic content | `aria-describedby="error-message"` |

### ARIA Label Guidelines

| Do | Don't |
|----|-------|
| Be concise | Include "button" or "link" |
| Match visible text when possible | Duplicate information |
| Describe function | Describe appearance |
| Update with state | Leave stale labels |

---

## Testing Accessible Copy

### Manual Testing

| Test | Method |
|------|--------|
| Screen reader | Test with VoiceOver, NVDA, or JAWS |
| Keyboard only | Navigate without mouse |
| Link audit | Read all links out of context |
| Heading outline | Check logical structure |
| Alt text review | Verify all images have appropriate alt |

### Testing Questions

| Check | Question |
|-------|----------|
| Links | Do link texts make sense alone? |
| Buttons | Is every action clearly labeled? |
| Forms | Can users complete forms with screen reader? |
| Errors | Are errors announced and linked to fields? |
| Images | Do important images convey info in text? |
| Structure | Does heading outline make sense? |

### Automated + Manual

| Automated catches | Manual catches |
|-------------------|----------------|
| Missing alt attributes | Poor alt text quality |
| Missing form labels | Confusing label text |
| Empty buttons | Unclear button purpose |
| Heading hierarchy gaps | Non-descriptive headings |

---

## Accessibility Copy Checklist

Before shipping:

| Element | Check |
|---------|-------|
| Images | Appropriate alt text for all images |
| Links | Descriptive, unique link text |
| Buttons | Clear action text, visible or sr-only |
| Forms | Associated labels, clear instructions |
| Errors | Specific, linked to fields |
| Headings | Logical hierarchy, descriptive |
| Tables | Captions, header cells, scope |
| Language | Inclusive, ability-neutral |
| Reading level | Appropriate for audience |

---

## Templates

### Alt Text Template

```
Informational: [Subject] + [action/state] + [relevant context]
Functional: [Action performed when activated]
Decorative: alt="" (empty string, not omitted)
```

### Accessible Link Template

```
[Action verb] + [specific destination/content]
"Download the 2024 annual report (PDF, 2.4MB)"
```

### Form Label Template

```
[Field name]
[Input field]
[Helper text: Format requirements or additional context]
[Error message if applicable]
```

---

This skill enables you to write copy that works for all users, regardless of how they access your content.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

