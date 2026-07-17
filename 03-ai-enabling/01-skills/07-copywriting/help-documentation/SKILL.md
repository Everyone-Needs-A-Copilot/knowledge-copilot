---
last_updated: 2026-02-25
status: active
name: help-documentation
description: Write clear, user-friendly help content including tooltips, inline help, FAQs, and support articles. Use for help centers, knowledge bases, and in-app guidance.
triggers:
  files: ["**/help/**", "**/docs/**", "**/support/**", "**/faq/**", "**/knowledge-base/**"]
  keywords: ["help content", "documentation", "FAQ", "support article", "knowledge base", "help center", "how-to", "troubleshooting", "user guide"]
allowed-tools: Read, Write, Edit
---

# Help Documentation Skill

Write help content that empowers users to solve problems independently. Good help documentation is findable, scannable, and actionable - getting users unstuck quickly.

---

## Core Principles

### Help Content Mindset

| Principle | Description | Example |
|-----------|-------------|---------|
| Task-focused | Answer "How do I...?" | Organize by user goals, not features |
| Scannable | Users are in a hurry | Clear headings, steps, bullet points |
| Empathetic | User might be frustrated | Patient tone, no jargon |
| Complete | Cover the whole task | Include prerequisites, expected outcomes |
| Findable | Easy to locate | Clear titles, good search keywords |

### User State When Seeking Help

| State | What They Need |
|-------|---------------|
| Stuck | Immediate, specific answer |
| Confused | Clear explanation |
| Exploring | Overview, orientation |
| Troubleshooting | Diagnostic steps |
| Learning | Thorough walkthrough |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Help Article Structure

### Standard Article Format

```
Title: Task-focused, searchable
Brief description: One sentence overview
Prerequisites (if any): What user needs first
Steps: Numbered, action-oriented
Result: What success looks like
Related topics: Next logical steps
```

### Title Formulas

| Type | Formula | Example |
|------|---------|---------|
| How-to | "How to [task]" | "How to invite team members" |
| Concept | "[Noun]: [descriptor]" | "Workspaces: Overview" |
| Reference | "[Feature] [aspect]" | "Keyboard shortcuts" |
| Troubleshoot | "Fix [problem]" | "Fix sync issues" |

### Article Titles: Do vs Don't

| Don't | Do |
|-------|-----|
| "Invitations" | "Invite team members" |
| "The Dashboard Feature" | "Using your dashboard" |
| "About Settings" | "Manage your settings" |
| "Error 404" | "Page not found: What to do" |

---

## Writing How-To Articles

### Step-by-Step Format

Each step should:
- Start with an action verb
- Be one concrete action
- Include what the user will see

```
## How to create a new project

1. Click **New project** in the top right corner.
2. Enter a project name.
3. Select a template or choose **Blank project**.
4. Click **Create**.

Your new project opens with a blank canvas.
```

### Prerequisites Section

List what users need before starting:

```
**Before you begin:**
- Admin or Editor role required
- At least one team member added
- Billing information on file
```

### Expected Results

Tell users what success looks like:

```
**Result:** Your team members receive email invitations. Once they accept, they appear in your team list with their assigned role.
```

---

## Inline Help and Tooltips

### When to Use Inline Help

| Context | Type | Example |
|---------|------|---------|
| Complex field | Tooltip/hint | "Enter domain without www" |
| Optional field | Helper text | "Add tags to help organize" |
| Destructive action | Warning | "This cannot be undone" |
| New feature | Tooltip with link | "New! Learn more" |

### Inline Help Guidelines

| Do | Don't |
|----|-------|
| Keep under 2 sentences | Write paragraphs |
| Answer immediate question | Link away unnecessarily |
| Use specific examples | Be vague |
| Update with feature changes | Let it get stale |

### Tooltip Copy Patterns

| Type | Format | Example |
|------|--------|---------|
| Definition | "[Term] is [definition]" | "MFA is Multi-Factor Authentication" |
| Instruction | "[Action] to [result]" | "Click to copy link" |
| Clarification | "[Context for field]" | "Shown on your public profile" |

---

## FAQs

### FAQ Format

Each FAQ should be:
- Question in user's words
- Direct answer first
- Details/context after

```
**Q: Can I change my username?**

Yes, you can change your username anytime. Go to Settings > Profile > Edit username.

Note: This changes your profile URL, which may break existing links.
```

### Good FAQ Questions

| Type | Example |
|------|---------|
| Feature scope | "Can I share projects with people outside my team?" |
| Limitation | "Is there a limit to how many projects I can create?" |
| Process | "How do I cancel my subscription?" |
| Troubleshooting | "Why am I not receiving email notifications?" |

### FAQ Anti-Patterns

| Avoid | Better Approach |
|-------|-----------------|
| "What is [Product]?" | Put in overview/about page |
| Questions no one asks | Monitor actual user questions |
| Marketing speak | Honest, helpful answers |
| "How do I contact support?" | Show support options prominently |

---

## Troubleshooting Articles

### Troubleshooting Structure

```
**Problem:** [Clear description of the issue]

**Possible causes:**
- [Cause 1]
- [Cause 2]
- [Cause 3]

**Solutions:**

### Try this first
[Most common/likely fix]

### If that doesn't work
[Next solution]

### Still having issues?
[Contact support with specific info to gather]
```

### Diagnostic Language

| Vague | Specific |
|-------|----------|
| "Check your settings" | "Go to Settings > Notifications > Email" |
| "Make sure you're connected" | "Check the connection icon shows green" |
| "Try again later" | "Wait 5 minutes, then refresh the page" |

### Error Message to Article Mapping

Create articles that match common errors:

| Error User Sees | Article Title |
|-----------------|---------------|
| "Session expired" | "Fix 'Session expired' errors" |
| "File too large" | "File size limits and how to reduce files" |
| "Permission denied" | "Understanding permissions and access" |

---

## Knowledge Base Organization

### Structure Patterns

| Pattern | Best For | Example |
|---------|----------|---------|
| By task | Most help centers | "Getting started", "Managing team", "Billing" |
| By user role | Different user types | "For admins", "For members" |
| By feature | Technical products | "Dashboard", "Integrations", "API" |
| By journey | Onboarding-focused | "First week", "Power user" |

### Category Naming

| Don't | Do |
|-------|-----|
| "Miscellaneous" | Specific topic names |
| Product codenames | User-facing feature names |
| "Advanced features" | Feature-specific categories |

### Cross-Linking

| Link Type | When to Use |
|-----------|-------------|
| Prerequisites | Article requires prior knowledge |
| Related tasks | Logical next steps |
| Deeper dives | User might want more detail |
| Alternatives | Different ways to accomplish same goal |

---

## Writing Style for Help

### Voice and Tone

| Do | Don't |
|----|-------|
| "Select your timezone" | "Please be sure to select your timezone" |
| "This can't be undone" | "WARNING: This action is irreversible!" |
| "This might take a moment" | "Please wait while the system processes" |

### Formatting for Scannability

| Element | Use For |
|---------|---------|
| **Bold** | UI elements, key terms |
| `Code` | Commands, inputs |
| Numbered lists | Steps in sequence |
| Bullet lists | Items in no particular order |
| > Callouts | Important notes, warnings |

### Standard Phrases

| Phrase | Use |
|--------|-----|
| "Note:" | Additional relevant information |
| "Tip:" | Helpful but optional advice |
| "Important:" | Critical information |
| "Warning:" | Could cause data loss/issues |

---

## Video and Visual Help

### When to Use Screenshots

| Use Screenshots When | Skip Screenshots When |
|---------------------|----------------------|
| UI is complex | Steps are straightforward |
| Location isn't obvious | Text description is clear |
| Multiple elements involved | Single button/field |
| UI has changed | Instructions are durable |

### Screenshot Annotation Guidelines

| Element | Guideline |
|---------|-----------|
| Callouts | Number steps, circle targets |
| Cropping | Show context but not full screen |
| Highlighting | Blur sensitive data |
| Alt text | Describe what screenshot shows |

### Video Guidelines

| Consideration | Recommendation |
|---------------|----------------|
| Length | 1-3 minutes max per topic |
| Captions | Always include |
| Transcript | Provide for accessibility |
| Chapters | For longer videos |

---

## Maintaining Help Content

### Update Triggers

| Event | Action Needed |
|-------|---------------|
| Feature change | Update affected articles |
| New feature | Create new article |
| Common support ticket | Write article to deflect |
| UI rename | Search and replace |

### Quality Checklist

| Check | Question |
|-------|----------|
| Accurate | Does this match current product? |
| Complete | Are all steps included? |
| Clear | Would a new user understand? |
| Findable | Are search terms in title/body? |
| Current | When was this last reviewed? |

### Metrics to Track

| Metric | What It Tells You |
|--------|-------------------|
| Search terms with no results | Content gaps |
| Article feedback (helpful Y/N) | Quality issues |
| Top articles | What users struggle with |
| Support ticket deflection | Self-service success |

---

## Help Content Templates

### How-To Article Template

```markdown
# How to [task]

[One sentence overview of what user will accomplish]

## Before you begin

- [Prerequisite 1]
- [Prerequisite 2]

## Steps

1. [Action verb] [specific instruction].
2. [Action verb] [specific instruction].
3. [Action verb] [specific instruction].

## Result

[What success looks like]

## Related topics

- [Related article 1]
- [Related article 2]
```

### Troubleshooting Template

```markdown
# Fix [problem]

[Brief description of the issue]

## Quick fixes

Try these solutions first:

1. **[Solution 1]**: [Brief instruction]
2. **[Solution 2]**: [Brief instruction]

## Detailed troubleshooting

### Check [common cause 1]

[Detailed steps]

### Check [common cause 2]

[Detailed steps]

## Still need help?

Contact support with this information:
- [Info needed 1]
- [Info needed 2]
```

### FAQ Entry Template

```markdown
## [Question in user's voice]?

[Direct answer in first sentence.]

[Additional context or steps if needed.]

**Related:** [Link to full article if available]
```

---

This skill enables you to write help content that empowers users to solve problems independently and efficiently.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

