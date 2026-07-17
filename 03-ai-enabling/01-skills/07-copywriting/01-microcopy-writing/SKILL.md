---
last_updated: 2026-02-25
status: active
name: microcopy-writing
description: Write effective UI microcopy - buttons, labels, hints, tooltips, and form elements. Use for interface copy that guides user actions.
triggers:
  files: ["**/components/**", "**/ui/**", "**/forms/**", "**/*.tsx", "**/*.jsx"]
  keywords: ["button text", "label", "placeholder", "tooltip", "hint", "microcopy", "UI text", "form labels", "call to action", "CTA"]
allowed-tools: Read, Write, Edit
---

# Microcopy Writing Skill

Write clear, actionable interface copy that guides users without getting in their way. Microcopy is the small text that makes interfaces usable: buttons, labels, hints, tooltips, placeholders, and form elements.

---

## Core Principles

### Voice Calibration for UI

| Context | Tone | Example |
|---------|------|---------|
| Primary actions | Direct, confident | "Save changes" not "Click here to save" |
| Form labels | Clear, minimal | "Email" not "Please enter your email address" |
| Hints | Helpful, specific | "8+ characters, one number" not "Password must be secure" |
| Errors | Honest, actionable | "Email already registered. Sign in?" not "Invalid input" |
| Empty states | Encouraging, next-step | "No projects yet. Create your first." not "Nothing to display" |

### The Three Tests

Before shipping any microcopy:

1. **Scannable?** Can users understand it in <2 seconds?
2. **Actionable?** Does it tell them what to do or what happens?
3. **Human?** Would you say this to someone in conversation?

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Button Copy

### Primary Actions

Use verbs that describe what happens next:

| Avoid | Use | Why |
|-------|-----|-----|
| Submit | Save profile | Specific outcome |
| OK | Confirm delete | Names the action |
| Click here | Download report | States result |
| Yes | Remove member | Clarifies consequence |

### Button Patterns

| Scenario | Pattern | Example |
|----------|---------|---------|
| Create new | "Create [thing]" | Create project |
| Save existing | "Save [thing]" | Save changes |
| Continue flow | "Continue" or "Next: [step]" | Next: Payment |
| Cancel/close | "Cancel" or specific action | Discard draft |
| Destructive | "[Action] [thing]" | Delete account |

### Destructive Actions

Be explicit about what's being destroyed:

```
Bad:  "Delete" (delete what?)
Good: "Delete project"
Best: "Delete 'Q4 Analysis'" (when context allows)
```

For irreversible actions, use confirmation copy:
```
"This will permanently delete all 24 files. This cannot be undone."
```

---

## Form Labels and Hints

### Labels

| Principle | Bad | Good |
|-----------|-----|------|
| Noun, not sentence | "Enter your email" | "Email" |
| Specific when needed | "Name" | "Company name" |
| No redundancy | "Email address" | "Email" |
| Match user's words | "Identification number" | "Employee ID" |

### Placeholder Text

Placeholders are hints, not labels. Use them for:
- Format examples: `YYYY-MM-DD`
- Sample content: `jane@company.com`
- Clarification: `Search by name or ID`

Never use placeholders as the only label - they disappear on input.

### Helper Text

Place helper text below the field, not in placeholders:

```
Email
[________________]
We'll send a confirmation link
```

Helper text patterns:
- **Format requirements**: "8+ characters, one number"
- **What happens next**: "We'll send a confirmation link"
- **Why we need this**: "Used for account recovery"

---

## Error Messages

### Error Message Formula

```
[What happened] + [How to fix it]
```

| Bad | Good |
|-----|------|
| "Invalid email" | "Enter a valid email (e.g., name@company.com)" |
| "Error" | "Password must be at least 8 characters" |
| "Field required" | "Email is required to create your account" |
| "Request failed" | "Couldn't save. Check your connection and try again." |

### Error Tone

| Avoid | Use |
|-------|-----|
| Blaming | Neutral |
| Technical jargon | Plain language |
| Passive voice | Active voice |
| Vague instructions | Specific next steps |

```
Bad:  "The system encountered an error processing your request"
Good: "We couldn't process your payment. Your card wasn't charged."
```

---

## Tooltips and Hints

### When to Use Tooltips

- Additional context that doesn't fit in the UI
- Explaining icons or abbreviated text
- Advanced features that need clarification

### Tooltip Guidelines

| Principle | Example |
|-----------|---------|
| One sentence max | "Export as CSV file" |
| Action-oriented | "Click to copy link" |
| Context-specific | "Last updated 2 hours ago" |
| No obvious info | Don't tooltip "Save" with "Saves your work" |

### Progressive Disclosure

Reveal complexity only when needed:

```
Basic:     [Search] (simple input)
Expanded:  [Search] [Filter ▾] [Date range ▾] (advanced options)
```

---

## Empty States

### Empty State Formula

```
[What this area shows] + [How to populate it]
```

| Context | Copy |
|---------|------|
| No results | "No projects match your search. Try different keywords." |
| First use | "No projects yet. Create your first project to get started." |
| Cleared data | "All caught up. New items will appear here." |
| Access issue | "You don't have access to this project. Request access from the owner." |

### Empty State Tone

- **Encouraging**, not apologetic
- **Forward-looking**, not dwelling on absence
- **Actionable**, with clear next step

---

## Loading and Progress States

### Loading Copy

| Duration | Pattern | Example |
|----------|---------|---------|
| < 3 seconds | Spinner only | [Loading...] |
| 3-10 seconds | Action description | "Generating report..." |
| > 10 seconds | Progress indicator | "Processing 24 of 100 files" |
| Unknown duration | Reassurance | "This may take a moment" |

### Progress Messaging

```
Step 1 of 3: Uploading files
Step 2 of 3: Processing data
Step 3 of 3: Generating report
```

---

## Notifications and Confirmations

### Success Messages

Keep them brief and confirm the action:

| Action | Confirmation |
|--------|--------------|
| Save | "Changes saved" |
| Delete | "Project deleted" |
| Send | "Message sent" |
| Copy | "Copied to clipboard" |

### Confirmation Dialogs

For destructive or significant actions:

```
Title: Delete "Q4 Analysis"?

Body: This will permanently delete the project and all 24 files.
      This cannot be undone.

Actions: [Cancel] [Delete project]
```

---

## Microcopy Anti-Patterns

### Words to Avoid

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Please | Unnecessary politeness | Direct statement |
| Click here | Vague, accessibility issue | Specific action |
| Invalid | Blaming | Specific requirement |
| Oops | Infantilizing | Direct acknowledgment |
| Submit | Generic | Specific action verb |
| Error | Unhelpful | What went wrong |

### Patterns to Avoid

| Pattern | Problem | Fix |
|---------|---------|-----|
| "Are you sure?" | Lazy confirmation | Describe consequence |
| "Something went wrong" | Unhelpful | Specific error + fix |
| Double negatives | Confusing | Positive framing |
| Jargon in UI | User doesn't speak developer | Plain language |
| Exclamation marks | Feels pushy | Period or nothing |

---

## Microcopy Checklist

Before shipping, verify:

| Test | Check |
|------|-------|
| Clarity | Can a new user understand this instantly? |
| Action | Does the user know what to do? |
| Length | Is every word necessary? |
| Consistency | Does terminology match rest of product? |
| Accessibility | Is there enough context without visuals? |
| Edge cases | What happens when text is long/short? |

---

## Examples by Component

### Search

```
Placeholder: "Search projects..."
No results:  "No projects match 'quarterly'. Try a different search."
Loading:     "Searching..."
```

### Settings Toggle

```
Label:  "Email notifications"
Hint:   "Get notified when someone comments on your projects"
States: "On" / "Off"
```

### File Upload

```
Default:  "Drop files here or browse"
Dragging: "Drop to upload"
Uploading: "Uploading report.pdf..."
Success:  "report.pdf uploaded"
Error:    "File too large. Maximum size is 10 MB."
```

---

This skill enables you to write interface copy that guides users clearly and gets out of their way.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

