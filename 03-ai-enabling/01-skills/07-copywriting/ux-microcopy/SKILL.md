---
last_updated: 2026-02-25
status: active
name: ux-microcopy
description: Write effective UX microcopy for digital interfaces - buttons, labels, tooltips, placeholders, and system messages. Use for any interface text that guides users through interactions.
triggers:
  files: ["**/components/**", "**/ui/**", "**/forms/**", "**/*.tsx", "**/*.jsx", "**/*.vue"]
  keywords: ["microcopy", "UI text", "button text", "label", "placeholder", "tooltip", "hint text", "form copy", "interface copy", "UX writing"]
allowed-tools: Read, Write, Edit
---

# UX Microcopy Skill

Write clear, helpful interface text that guides users through digital products. UX microcopy includes every word users read in an interface: buttons, labels, hints, tooltips, placeholders, notifications, and system messages.

---

## Core Principles

### The UX Microcopy Mindset

| Principle | Description | Example |
|-----------|-------------|---------|
| Clarity first | Users should understand instantly | "Save" not "Persist changes" |
| Context-aware | Copy fits the user's situation | Error state vs. success state |
| Action-oriented | Tell users what to do | "Create project" not "Project creation" |
| Scannable | Works at a glance | Short phrases over sentences |
| Consistent | Same action = same words | Always "Delete" not mix "Remove/Delete/Discard" |

### Voice Calibration Matrix

| Context | Tone | Length | Example |
|---------|------|--------|---------|
| Primary actions | Confident, direct | 1-3 words | "Save changes" |
| Secondary actions | Clear, informative | 2-4 words | "Save as draft" |
| Helper text | Helpful, supportive | 5-15 words | "We'll send a verification code to this number" |
| Error states | Honest, solution-focused | 10-25 words | "This email is already registered. Sign in or reset your password." |
| Success states | Confirming, brief | 2-5 words | "Project created" |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Buttons and Actions

### Primary Action Buttons

Use verbs that describe the outcome, not the interaction:

| Avoid | Use | Why |
|-------|-----|-----|
| Submit | Create account | Specific outcome |
| OK | Confirm booking | Names the action |
| Click here | Download PDF | States the result |
| Yes | Remove from list | Clarifies consequence |

### Button Copy Patterns

| Scenario | Pattern | Examples |
|----------|---------|----------|
| Create new | "[Verb] [noun]" | Create project, Add member |
| Save changes | "Save [context]" | Save changes, Save draft |
| Navigate forward | "Continue" or "Next: [step]" | Continue, Next: Payment |
| Cancel/abort | "[Specific action]" or "Cancel" | Discard changes, Cancel |
| Destructive | "[Verb] [noun]" | Delete account, Remove member |

### Destructive Action Guidelines

```
Primary button:   "Delete project"  (specific, irreversible)
Secondary button: "Cancel"          (escape route)
```

For irreversible actions:
- Name what's being destroyed
- Quantify impact when possible
- Offer confirmation with consequences

```
Good:  "Delete 'Q4 Analysis' and its 24 files"
Bad:   "Delete"
```

---

## Labels and Form Fields

### Label Best Practices

| Principle | Bad | Good |
|-----------|-----|------|
| Use nouns, not instructions | "Enter your email" | "Email" |
| Be specific when needed | "Name" | "Company name" |
| Avoid redundancy | "Email address" | "Email" |
| Match user vocabulary | "Unique identifier" | "Employee ID" |

### Placeholder Text Guidelines

Placeholders should demonstrate format or provide examples:

| Purpose | Example |
|---------|---------|
| Format hint | `YYYY-MM-DD` |
| Example content | `jane@company.com` |
| Clarification | `Search by name or ID` |

Never use placeholders as the only label - they disappear on focus.

### Helper Text Patterns

Position helper text below the field:

```
Email
[                              ]
We'll send a verification link to this address
```

| Purpose | Pattern | Example |
|---------|---------|---------|
| Format requirements | State the rule | "8+ characters with one number" |
| Explain consequences | What happens next | "You can change this later in settings" |
| Provide context | Why we need this | "Used for account recovery only" |

---

## Tooltips and Contextual Help

### When to Use Tooltips

- Explain icons or abbreviated text
- Provide additional context that doesn't fit in the UI
- Clarify advanced features
- Show keyboard shortcuts

### Tooltip Guidelines

| Do | Don't |
|----|-------|
| One sentence maximum | Multi-paragraph explanations |
| Action-oriented when possible | Obvious restatements |
| Context-specific details | Generic help text |

```
Good: "Sort by most recent first"
Bad:  "This button sorts the list"
```

---

## Notifications and Feedback

### Success Messages

Keep them brief and specific:

| Action | Message |
|--------|---------|
| Save | "Changes saved" |
| Delete | "Project deleted" |
| Send | "Message sent to 3 recipients" |
| Copy | "Link copied" |

### Toast Notification Patterns

| Type | Duration | Pattern |
|------|----------|---------|
| Success | 3-5 seconds | "[Action] complete" or "[Item] [action]ed" |
| Info | 5-7 seconds | "[Information]. [Optional action]" |
| Warning | Until dismissed | "[Issue]. [How to resolve]" |
| Error | Until dismissed | "[What happened]. [How to fix]" |

---

## Empty States

### Empty State Formula

```
[What this area shows] + [How to populate it]
```

| Context | Copy |
|---------|------|
| First use | "No projects yet. Create your first project." |
| No results | "No results for 'search term'. Try different keywords." |
| Cleared list | "All caught up! New items will appear here." |
| Access issue | "You don't have access. Request access from the owner." |

### Empty State Tone

- Encouraging, not apologetic
- Forward-looking with clear next step
- Never blame the user

---

## Loading and Progress States

### Loading Copy by Duration

| Duration | Approach | Example |
|----------|----------|---------|
| < 2 sec | Spinner only | [Loading...] |
| 2-10 sec | Describe action | "Loading your projects..." |
| > 10 sec | Show progress | "Processed 45 of 120 files" |
| Unknown | Reassure | "This may take a moment..." |

### Progress Indicators

```
Step 1 of 3: Uploading files
Step 2 of 3: Processing images
Step 3 of 3: Generating preview
```

---

## Common Anti-Patterns

### Words to Avoid

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Please | Unnecessary | Direct statement |
| Click here | Vague, inaccessible | Specific action |
| Invalid | Blaming | Specific requirement |
| Oops | Infantilizing | Direct acknowledgment |
| Submit | Generic | Specific verb |
| Error | Unhelpful | What went wrong |

### Patterns to Avoid

| Pattern | Problem | Fix |
|---------|---------|-----|
| "Are you sure?" | Lazy confirmation | State consequences |
| "Something went wrong" | No useful information | Specific error + solution |
| Technical jargon | Users don't speak code | Plain language |
| Exclamation marks! | Feels aggressive | Period or nothing |
| Double negatives | Confusing | Positive framing |

---

## Microcopy Checklist

Before shipping interface copy:

| Check | Question |
|-------|----------|
| Clarity | Would a first-time user understand this? |
| Action | Does the user know what to do or what happens? |
| Length | Is every word necessary? |
| Consistency | Does terminology match the rest of the product? |
| Accessibility | Is there enough context without visuals? |
| Edge cases | How does this read when text is very long or very short? |

---

## Examples by Component

### Search Input

```
Placeholder: "Search projects..."
No results:  "No matches for 'quarterly'. Try different keywords."
Loading:     "Searching..."
Results:     "12 projects match 'quarterly'"
```

### File Upload

```
Default:    "Drop files here or browse"
Dragging:   "Drop to upload"
Uploading:  "Uploading report.pdf (45%)..."
Success:    "report.pdf uploaded"
Error:      "File too large. Maximum size is 10 MB."
```

### Settings Toggle

```
Label:      "Email notifications"
Helper:     "Get notified when someone comments on your projects"
States:     "On" / "Off"
```

---

This skill enables you to write interface copy that guides users clearly and stays out of their way.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

