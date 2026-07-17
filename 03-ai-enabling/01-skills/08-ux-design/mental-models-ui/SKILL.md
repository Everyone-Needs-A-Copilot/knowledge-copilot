---
last_updated: 2026-02-25
status: active
name: mental-models-ui
description: Design interfaces matching users' mental models - how they expect things to work based on prior experience. Use for intuitive design.
triggers:
  files: ["**/ux/**", "**/user-research/**", "**/persona/**"]
  keywords: ["mental model", "user expectation", "intuitive", "familiar", "convention", "affordance", "conceptual model", "user understanding"]
allowed-tools: Read, Write, Edit
---

# Mental Models UI Skill

Master guide for designing interfaces that align with how users think, expect, and understand systems based on their prior experiences.

## Philosophy

**Users bring expectations.** Every user arrives with mental models built from previous experiences—other apps, real-world objects, cultural norms. Align with these or expect confusion.

**Match the model, not the system.** The UI should reflect how users think about tasks, not how the backend is architected.

**When in doubt, follow conventions.** Novel designs require learning. Convention-following is effortless.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Understanding Mental Models

### What is a Mental Model?

A user's internal understanding of how something works:
- What it does
- How to interact with it
- What to expect after actions
- How it relates to other things

### Model Types

| Type | Description | Example |
|------|-------------|---------|
| **Structural** | How things are organized | File system as folders/files |
| **Functional** | How things work | Shopping cart holds items until checkout |
| **Causal** | Cause and effect | Click "Delete" → Item removed |
| **Social** | How others interact | Comments appear below posts |

### Mental Model Mismatch

**System Model**: How the system actually works
**Mental Model**: How users think it works
**Design Goal**: Minimize the gap

```
System Reality:          User Expectation:
┌─────────────────┐      ┌─────────────────┐
│ Complex backend │  ≠   │ Simple folder   │
│ with metadata   │      │ structure       │
│ and relations   │      │                 │
└─────────────────┘      └─────────────────┘

Design Solution:
Present complex system through familiar folder metaphor
```

---

## Common Mental Models

### File Management

Users expect:
- Hierarchical folders
- Drag to move
- Copy/paste works
- Undo is available
- Trash before permanent delete

Design implications:
```
✅ Use folder icons for organization
✅ Support drag and drop
✅ Provide undo for destructive actions
✅ "Trash" before permanent deletion
```

### Shopping/E-commerce

Users expect:
- Cart holds items
- Can add/remove items
- See total before checkout
- Checkout is linear process
- Confirmation before payment

Design implications:
```
✅ Cart icon with item count
✅ Clear "Add to cart" buttons
✅ Running total always visible
✅ Step-by-step checkout
✅ Order review before final submit
```

### Social Media

Users expect:
- Feed shows recent content
- Scroll for more
- Like/react is easy
- Comments thread below content
- Profile has their content

### Forms

Users expect:
- Tab moves to next field
- Enter submits
- Required fields marked
- Errors shown near fields
- Data saved on submit

### Navigation

Users expect:
- Logo goes home
- Back button works
- Breadcrumbs show location
- Search finds things
- Menu items describe destinations

---

## Mapping Models to UI

### Process

1. **Research user mental models**
   - Interviews: "How would you describe this?"
   - Card sorting: How do users group things?
   - Task analysis: What steps do users expect?

2. **Identify mismatches**
   - Where does system differ from expectations?
   - What's confusing in current design?
   - Where do users make errors?

3. **Bridge the gap**
   - Adapt UI to match mental model
   - Or educate users on system model
   - Use familiar metaphors

### Metaphor Selection

Choose metaphors users already understand:

| Task | Metaphor | UI Elements |
|------|----------|-------------|
| Organize content | Folders | Folder icons, tree structure |
| Save progress | Document | "Save" button, auto-save indicator |
| Communication | Mail | Inbox, sent, compose |
| Purchases | Shopping | Cart, checkout, receipt |
| Settings | Control panel | Toggles, sliders, buttons |

### Metaphor Guidelines

**Do**:
- Use familiar metaphors
- Be consistent with metaphor
- Extend metaphor logically

**Don't**:
- Mix incompatible metaphors
- Force system architecture into UI
- Use metaphors users don't know

---

## Designing for Mental Models

### Affordances

Make interactions obvious based on real-world expectations:

```
Button → Clickable (raised, colored)
Input → Type here (outlined box)
Link → Navigate (underlined, colored)
Slider → Drag (handle on track)
Toggle → On/off (switch shape)
```

### Signifiers

Show how to interact:

```
Hover states → "This is interactive"
Cursor change → "Click here"
Focus ring → "You're here"
Placeholder → "Type this kind of thing"
Arrow/chevron → "More content this way"
```

### Feedback

Confirm expectations were correct:

```
Click button → Visual feedback (press state)
Submit form → Confirmation message
Delete item → Item disappears
Error → Clear error message
Loading → Progress indicator
```

### Consistency

Match established patterns:

| Convention | User Expectation |
|------------|------------------|
| Logo top-left | Clicking goes home |
| Primary button right | Main action on right |
| Red color | Error or danger |
| Green color | Success or go |
| × icon | Close or dismiss |
| ☰ icon | Menu |

---

## Testing Mental Models

### Card Sorting

Test how users categorize:

```
Open sort:
- Give users cards (features, content)
- Users create and name groups
- Reveals natural categories

Closed sort:
- Give users predefined categories
- Users place cards
- Tests proposed structure
```

### Think-Aloud Testing

Reveal mental models during tasks:

```
Task: "Find your recent orders"

User thinks aloud:
"I'd expect this in my account..."
"Looking for 'Orders' or 'History'..."
"This icon looks like it might be orders..."
```

### First Click Testing

Test initial expectations:

```
Show: Homepage mockup
Ask: "Where would you click to find X?"
Measure: % who click correct area
```

### Expectation Mapping

Before showing UI, ask:
- "What do you expect to see on this page?"
- "What would you expect this button to do?"
- "Where would you expect to find X?"

---

## Bridging Model Gaps

### When Models Don't Match

**Option 1: Change the UI**
Adapt to user's mental model

**Option 2: Educate the user**
Help user learn system model

**Option 3: Both**
Familiar surface, teach advanced features

### Education Techniques

**Onboarding**:
```
"Unlike traditional folders, our Smart
Collections automatically organize files
based on content. Here's how they work..."
```

**Inline hints**:
```
[New Feature] Files are now auto-organized
Learn how Smart Collections work →
```

**Progressive disclosure**:
```
Basic view: Looks like folders
Advanced view: Shows smart collections logic
```

### When to Challenge Models

Sometimes better experiences require new models:
- Old model is inefficient
- New model provides significant value
- Users can be guided through transition

Examples:
- Gmail's labels vs folders
- Spotify's playlists vs albums
- Figma's multiplayer vs local files

---

## Domain-Specific Models

### Technical Users

Expect:
- Keyboard shortcuts
- Precise control
- Terminal/CLI options
- Configuration files
- Version control

### Non-Technical Users

Expect:
- Visual interfaces
- Guided workflows
- Undo/safety nets
- Plain language
- Minimal configuration

### Mobile Users

Expect:
- Touch gestures
- Swipe to navigate
- Pull to refresh
- Bottom navigation
- One-handed use

### Enterprise Users

Expect:
- Permissions/roles
- Approval workflows
- Audit trails
- Bulk operations
- Integrations

---

## Anti-Patterns

### 1. Exposing System Architecture

```
❌ Bad:
"Error: FK_constraint_violation on user_id"

✅ Good:
"This user couldn't be deleted because they
have active projects. Archive projects first."
```

### 2. Novel Navigation

```
❌ Bad:
Inventing new navigation patterns

✅ Good:
Standard nav (tabs, sidebar, breadcrumbs)
```

### 3. Inconsistent Metaphors

```
❌ Bad:
"Folders" that have "Channels" containing "Boards"

✅ Good:
Pick one metaphor, use consistently
```

### 4. Ignoring Platform Conventions

```
❌ Bad:
iOS app with Android-style navigation

✅ Good:
Follow platform HIG (Human Interface Guidelines)
```

### 5. Jargon in UI

```
❌ Bad:
"Instantiate a new document instance"

✅ Good:
"Create new document"
```

---

## Research Methods

### User Interviews

Questions to reveal mental models:
- "How would you describe what this does?"
- "What did you expect to happen?"
- "What does this remind you of?"
- "How would you explain this to someone else?"

### Concept Testing

Test mental model before building:
1. Describe concept verbally
2. Ask users to sketch expected UI
3. Compare to planned design
4. Identify gaps

### A/B Testing

Test which model resonates:
- Version A: Folder metaphor
- Version B: Tag metaphor
- Measure: Task completion, satisfaction

---

## Quick Reference

### Mental Model Checklist

- [ ] Researched how users think about this task
- [ ] Identified existing mental models
- [ ] UI matches expected mental model
- [ ] Familiar metaphors used appropriately
- [ ] Conventions followed (or consciously broken)
- [ ] Affordances match interactions
- [ ] Feedback confirms expectations
- [ ] Error messages in user's language
- [ ] Tested with representative users

### Common Mappings

| System Concept | User-Friendly Term |
|----------------|-------------------|
| Record | Item, Entry |
| Instance | Copy |
| Parent-child | Folder-file |
| Association | Connection, Link |
| Attribute | Property, Detail |
| Validation error | "Please fix..." |
| Authentication | Sign in |
| Authorization | Permission |

### Model Alignment Questions

Before designing, ask:
1. What do users already know about this?
2. What similar things have they used?
3. What words do they use?
4. What do they expect to happen?
5. Where might they get confused?

---

## Summary

**Design for how users think, not how systems work.**

1. Research user mental models
2. Map UI to user expectations
3. Use familiar metaphors
4. Follow conventions
5. Test for alignment
6. Bridge gaps through education when needed

*The best interfaces feel obvious because they match what users already expect.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

