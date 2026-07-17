---
last_updated: 2026-02-25
status: active
name: cognitive-load-management
description: Design for limited human attention and working memory - reducing mental effort required to use interfaces. Use for simplification and clarity.
triggers:
  files: ["**/ux/**", "**/simplify/**", "**/complexity/**"]
  keywords: ["cognitive load", "working memory", "mental effort", "complexity", "simplify", "chunking", "attention", "overwhelm", "cognitive overload"]
allowed-tools: Read, Write, Edit
---

# Cognitive Load Management Skill

Master guide for designing interfaces that respect human cognitive limitations - keeping mental effort low so users can focus on their goals, not on figuring out your interface.

## Philosophy

**Working memory is precious.** Humans can hold roughly 4 items in working memory at once. Every interface element competes for this limited resource.

**Effort spent on UI is effort stolen from tasks.** When users struggle to understand an interface, they have less capacity for their actual work.

**Simplicity is kindness.** Reducing cognitive load isn't dumbing down - it's respecting users' mental energy.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Types of Cognitive Load

### Intrinsic Load

Inherent complexity of the task itself.

| Cannot Reduce | Can Support |
|---------------|-------------|
| Learning accounting principles | Break into steps |
| Understanding medical terms | Provide definitions |
| Writing code logic | Offer autocomplete |

### Extraneous Load

Unnecessary complexity added by poor design.

| Problem | Solution |
|---------|----------|
| Confusing navigation | Clear information architecture |
| Cluttered interface | Visual hierarchy |
| Inconsistent patterns | Design system |
| Jargon in labels | Plain language |

### Germane Load

Useful mental effort that builds understanding.

| Support | Avoid |
|---------|-------|
| Meaningful practice | Busywork |
| Connecting concepts | Isolated facts |
| Progressive complexity | Everything at once |

---

## Cognitive Load Reducers

### 1. Chunking

Group related information into digestible units.

**Text chunking**:
```
❌ Bad: Wall of text
The system will process your request and send
a confirmation email to the address you provided
when you created your account which you can...

✅ Good: Chunked information
Your request is being processed.

We'll email confirmation to: john@example.com

Expected time: 2-3 business days
```

**Form chunking**:
```
❌ Bad: 20 fields at once

✅ Good: Chunked into sections
┌─ Personal Information ─────────┐
│ Name: [          ]             │
│ Email: [          ]            │
└────────────────────────────────┘
┌─ Shipping Address ─────────────┐
│ Street: [          ]           │
│ City: [          ]             │
└────────────────────────────────┘
```

**Number chunking**:
```
❌ Bad: 4155551234
✅ Good: (415) 555-1234

❌ Bad: 4532015678901234
✅ Good: 4532 0156 7890 1234
```

### 2. Progressive Disclosure

Show only what's needed now; reveal more on demand.

```
Initial view:
┌────────────────────────────────┐
│ [Search: __________] [Search] │
└────────────────────────────────┘

Expanded (on request):
┌────────────────────────────────┐
│ [Search: __________] [Search] │
│ ▼ Advanced options             │
│   Date: [Any ▼]                │
│   Type: [All ▼]                │
│   Sort: [Relevance ▼]          │
└────────────────────────────────┘
```

### 3. Recognition Over Recall

Help users recognize rather than remember.

```
❌ Bad: Empty field
Enter discount code: [___________]

✅ Good: Suggestions and history
Enter discount code: [___________]
Recent codes: SAVE20, FREESHIP
```

```
❌ Bad: Memorize navigation
Where was that setting...?

✅ Good: Search + breadcrumbs
Settings > Account > Privacy
[Search settings: ___]
```

### 4. Sensible Defaults

Pre-fill the most likely answer.

```
❌ Bad: Empty form
Country: [Select ▼]
Language: [Select ▼]
Currency: [Select ▼]

✅ Good: Smart defaults
Country: [United States ▼] ← Based on IP
Language: [English ▼] ← Based on browser
Currency: [USD ▼] ← Based on country
```

### 5. Visual Hierarchy

Use design to show importance without words.

```
Most important → Largest, boldest, top
Less important → Smaller, lighter, lower
Least important → Smallest, subtle, bottom
```

### 6. Consistency

Same patterns everywhere reduce learning.

| Inconsistent | Consistent |
|--------------|------------|
| "Submit" / "Send" / "Go" | "Submit" everywhere |
| Blue links / green links | Blue links only |
| Modal here / page there | Modal for quick actions |

---

## Working Memory Constraints

### The 4±1 Rule

Miller's law updated: users can hold ~4 chunks in working memory.

**Navigation design**:
```
❌ Bad: 12 top-level items
Home Products Services Solutions Resources...

✅ Good: 4-5 top-level items
Home  Products  Resources  About  Contact
```

**Form design**:
```
❌ Bad: Show 20 fields
User sees wall of inputs

✅ Good: Show 3-5 fields per section
Section 1: Personal Info (4 fields)
Section 2: Contact Info (3 fields)
Section 3: Preferences (3 fields)
```

### Decision Fatigue

Each decision depletes mental resources.

**Reduce decisions**:
```
❌ Bad: 50 font options
Choose font: [50 options...]

✅ Good: Curated choices
Choose style:
( ) Professional (Helvetica)
( ) Friendly (Open Sans)
( ) Classic (Georgia)
[More fonts →]
```

**Decision order**:
```
❌ Bad: Hard decision first
"Commit to 3-year plan?"

✅ Good: Easy decisions first
"What's your name?"
"What's your email?"
...build momentum...
"Choose your plan"
```

---

## Attention Management

### Focus Direction

Guide users to what matters:

```css
/* Visual weight hierarchy */
.primary-action {
  background: var(--primary);
  font-size: 1rem;
  font-weight: 600;
}

.secondary-action {
  background: transparent;
  border: 1px solid var(--border);
  font-weight: 400;
}
```

### Distraction Reduction

Remove visual noise:

```
❌ Bad: Everything competes
[AD] [PROMO] CONTENT [SIDEBAR] [POPUP]

✅ Good: Content first
          CONTENT
[subtle navigation below]
```

### Attention Preservation

Avoid unnecessary interruptions:

| Interruptive | Non-Interruptive |
|--------------|------------------|
| Pop-up modal | Inline notification |
| Auto-play video | Click-to-play |
| Alert sounds | Badge indicator |
| Forced redirect | Suggested link |

---

## Information Architecture

### Flat vs Deep Hierarchy

```
❌ Bad: Too deep (many clicks)
Home > Products > Electronics > Phones > Android > Samsung

✅ Good: Flatter (fewer clicks)
Home > Phones > Samsung Galaxy
```

### Grouping Strategies

**By task**:
```
What do you want to do?
├── Create
├── Edit
├── Share
└── Export
```

**By type**:
```
Browse by category:
├── Documents
├── Images
├── Videos
└── Audio
```

**By user**:
```
For your role:
├── Developer tools
├── Admin settings
└── Team management
```

---

## Content Simplification

### Writing for Low Load

| High Load | Low Load |
|-----------|----------|
| "Please proceed to enter the information pertaining to your account" | "Enter your account details" |
| "Utilize the following functionality" | "Use this feature" |
| "In order to" | "To" |
| "At this point in time" | "Now" |

### Scannability

```
❌ Bad: Dense paragraph
The new feature allows users to create, edit, share,
and export documents in multiple formats including PDF,
DOCX, and plain text. Users can also collaborate in
real-time with team members and track changes...

✅ Good: Scannable format
**What you can do:**
• Create and edit documents
• Share with team members
• Export to PDF, DOCX, or TXT
• Collaborate in real-time
• Track changes
```

### Labels and Microcopy

```
❌ Bad: Technical
"Authenticate credentials"

✅ Good: Human
"Sign in"
```

```
❌ Bad: Vague
"Submit"

✅ Good: Specific
"Create account"
```

---

## Form Optimization

### Field Reduction

Every field is cognitive cost:

```
❌ Bad: 15 fields
First Name, Last Name, Middle Name, Title, Suffix,
Address Line 1, Address Line 2, City, State, ZIP...

✅ Good: Essential only
Full Name: [_____________]
Address: [_____________] (autocomplete)
```

### Smart Inputs

Reduce effort with intelligent fields:

```
Address: [123 Main]
         ↓ Autocomplete suggestion
         123 Main St, San Francisco, CA 94102
```

### Inline Help

Provide context without navigation:

```
Password: [______________]
          8+ characters, include number

NOT:
Password: [______________] [?]
(Requires extra click to understand)
```

---

## Task Flow Optimization

### Steps Visible

Show progress and reduce uncertainty:

```
Step 2 of 4: Shipping
━━━━━━━━●━━━━━━━━━━━━
```

### Save Progress

Don't force completion in one session:

```
┌────────────────────────────────┐
│ Continue where you left off?   │
│ Step 3 of 5: Payment Details   │
│ [Continue] [Start Over]        │
└────────────────────────────────┘
```

### Clear Next Steps

Always show what happens next:

```
✓ Order placed

What's next:
1. Confirmation email sent
2. Order ships within 2 days
3. Tracking number emailed

[Track your order]
```

---

## Measuring Cognitive Load

### Observational Signals

| High Load | Low Load |
|-----------|----------|
| Users pause frequently | Smooth progression |
| Many errors | Few errors |
| Questions about basics | Questions about advanced |
| Abandonment | Completion |
| Use of help/support | Self-service success |

### Testing Methods

**Think-aloud testing**:
Listen for phrases like:
- "Wait, what does this mean?"
- "Where do I find...?"
- "I'm confused about..."

**Time-on-task**:
Compare completion times across designs.

**Error rates**:
Track mistakes per flow.

---

## Anti-Patterns

### 1. Feature Explosion

```
❌ Bad: Every feature visible
[50 toolbar buttons visible]

✅ Good: Progressive features
[5 common buttons] [More ▼]
```

### 2. Information Dump

```
❌ Bad: Everything upfront
[10 paragraphs before the form]

✅ Good: Just-in-time information
Field-specific help when needed
```

### 3. Inconsistent Patterns

```
❌ Bad: Different for each page
Page 1: Save button top-right
Page 2: Save button bottom-left
Page 3: Auto-save only

✅ Good: Same everywhere
All pages: Auto-save + Save button top-right
```

### 4. Memory Requirements

```
❌ Bad: "Remember your confirmation code: XYZ123"
→ User must memorize

✅ Good: "Confirmation code: XYZ123 [Copy]"
→ Code emailed automatically
```

### 5. Context Switching

```
❌ Bad: Modal opens new tab
→ User loses context

✅ Good: Modal stays in context
→ User keeps place
```

---

## Quick Reference

### Cognitive Load Checklist

- [ ] 4-5 items max in any group
- [ ] Progressive disclosure for complexity
- [ ] Recognition over recall (show don't ask)
- [ ] Sensible defaults pre-filled
- [ ] Consistent patterns throughout
- [ ] Clear visual hierarchy
- [ ] Plain language (no jargon)
- [ ] Chunked information
- [ ] Progress indicators for flows
- [ ] Minimal required fields

### Load Reduction Techniques

| Technique | Implementation |
|-----------|----------------|
| Chunking | Group related items (max 4-5) |
| Defaults | Pre-fill likely values |
| Recognition | Show options, history, suggestions |
| Hierarchy | Visual weight = importance |
| Consistency | Same patterns everywhere |
| Disclosure | Show basics, reveal advanced |
| Simplification | Fewer words, clearer labels |

### Questions to Ask

Before adding any element:
1. Does the user need this right now?
2. Can we show fewer options?
3. Can we pre-fill this?
4. Is the label clear without thinking?
5. Is this consistent with other screens?

---

## Summary

**Every pixel costs mental energy.**

1. Respect working memory limits (4±1 items)
2. Chunk information into digestible groups
3. Show don't ask (recognition > recall)
4. Pre-fill sensible defaults
5. Maintain ruthless consistency
6. Remove everything non-essential

*The best interface is one users don't have to think about.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

