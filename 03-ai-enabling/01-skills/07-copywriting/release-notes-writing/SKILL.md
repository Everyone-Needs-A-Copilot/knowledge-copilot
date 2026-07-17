---
last_updated: 2026-02-25
status: active
name: release-notes-writing
description: Write clear, engaging release notes that communicate product updates. Use for changelogs, version updates, product announcements, and what's new sections.
triggers:
  files: ["**/changelog/**", "**/release-notes/**", "**/releases/**", "CHANGELOG.md", "RELEASE*.md"]
  keywords: ["release notes", "changelog", "what's new", "product update", "version release", "new features", "bug fixes", "improvements"]
allowed-tools: Read, Write, Edit
---

# Release Notes Writing Skill

Write release notes that inform users about changes and get them excited about improvements. Good release notes are scannable, benefit-focused, and help users understand what's new without overwhelming them.

---

## Core Principles

### Release Notes Mindset

| Principle | Description | Example |
|-----------|-------------|---------|
| Benefit-led | Focus on user value, not technical changes | "Find files faster" not "Improved search algorithm" |
| Scannable | Users skim, don't read | Clear headings, bullet points |
| Honest | Acknowledge breaking changes | Call out migrations, deprecations |
| Actionable | Help users take advantage | Include links to docs, settings |
| Consistent | Same format every release | Predictable structure |

### Audience Considerations

| Audience | What They Want |
|----------|---------------|
| End users | What's new for me? What do I do? |
| Developers | Breaking changes? Migration steps? |
| Admins | Security updates? New settings? |
| Stakeholders | Major features, timeline |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Release Notes Structure

### Standard Format

```
# [Product] [Version] Release Notes
[Date]

## Highlights
[Top 1-3 features/changes worth celebrating]

## New Features
[New capabilities]

## Improvements
[Enhancements to existing features]

## Bug Fixes
[Issues resolved]

## Breaking Changes
[What might affect existing workflows]

## Deprecations
[What's being phased out]
```

### Section Priority

| Priority | Section | Always Include? |
|----------|---------|-----------------|
| 1 | Highlights | Major releases |
| 2 | Breaking Changes | If any exist |
| 3 | New Features | If any exist |
| 4 | Improvements | If any exist |
| 5 | Bug Fixes | If any exist |
| 6 | Deprecations | If any exist |

---

## Writing Feature Announcements

### Feature Headline Formula

```
[User benefit] with [feature name]
```

| Technical | Benefit-Focused |
|-----------|-----------------|
| "Added search filters" | "Find exactly what you need with advanced filters" |
| "Implemented bulk actions" | "Save time with bulk editing" |
| "New dashboard widgets" | "See your metrics at a glance" |

### Feature Description Structure

```
**[Benefit headline]**

[1-2 sentences on what it does and why it matters]

[Screenshot or GIF if visual feature]

[Link to documentation or how to access]
```

### Example Feature Entry

```
**Export your data in one click**

Now you can export all your project data to CSV or JSON directly from Settings. Whether you're backing up data or moving to another tool, it takes seconds instead of hours.

Go to Settings > Data > Export to try it.
```

---

## Writing Improvements

### Improvement vs. New Feature

| It's an Improvement if... | It's a New Feature if... |
|---------------------------|--------------------------|
| Enhances existing capability | Adds capability that didn't exist |
| Faster, easier, better | New workflow possible |
| Users won't need to learn | Users need to discover/learn |

### Improvement Patterns

| Pattern | Example |
|---------|---------|
| Speed | "Dashboard loads 40% faster" |
| Usability | "Keyboard shortcuts now work everywhere" |
| Reliability | "Sync is more reliable on slow connections" |
| Polish | "Cleaner design for project cards" |

### Improvement Format

```
- **[Area improved]:** [What's better] [Quantify if possible]
```

Examples:
```
- **Search:** Results now appear as you type
- **Mobile:** Improved touch targets for buttons
- **Performance:** Page load times reduced by 30%
```

---

## Writing Bug Fixes

### Bug Fix Format

| Include | Omit |
|---------|------|
| What was broken | Technical cause |
| What works now | Internal ticket numbers |
| Affected scope | Blame for the bug |

### Bug Fix Patterns

| Vague | Clear |
|-------|-------|
| "Fixed a bug" | "Fixed: Notifications weren't sent for shared projects" |
| "Stability improvements" | "Fixed: App no longer crashes when uploading large files" |
| "Various bug fixes" | List the actual fixes |

### Bug Fix Examples

```
**Fixed**
- Images now save correctly when edited on mobile
- Email notifications appear for all team updates (not just the first)
- "Save" button is now clickable when form has only one field filled
```

---

## Breaking Changes and Migrations

### When to Include

| Include | Don't Include |
|---------|---------------|
| API changes | Internal refactoring |
| Removed features | Features most users never used |
| Required user action | Automatic migrations |
| Behavior changes | Identical behavior, different code |

### Breaking Change Format

```
**Breaking Change: [Clear description]**

**What's changing:** [Explain the change]

**Who's affected:** [Scope of impact]

**What to do:** [Migration steps]

**Deadline:** [If applicable]
```

### Example Breaking Change

```
**Breaking Change: Project URLs**

**What's changing:** Project URLs now use UUIDs instead of sequential IDs.

**Who's affected:** Anyone linking to projects externally.

**What to do:** Update any saved project links. Old links will redirect for 90 days.

**Deadline:** Old URLs stop working on March 1, 2024.
```

---

## Deprecation Notices

### Deprecation Format

```
**Deprecated: [Feature name]**

[What's being deprecated] will be removed in [timeline].

**Use instead:** [Alternative]

**Migration guide:** [Link]
```

### Example Deprecation

```
**Deprecated: Legacy API v1**

API v1 will be retired on June 1, 2024.

**Use instead:** API v2, which includes all v1 functionality plus new features.

**Migration guide:** [Link to docs]
```

---

## Versioning and Dates

### Version Number Display

| Context | Format |
|---------|--------|
| SaaS products | Date-based: "January 2024 Release" |
| Software versions | Semantic: "Version 2.4.0" |
| Continuous deploy | Week/sprint: "Week 48 Updates" |

### Date Formatting

| Format | When to Use |
|--------|-------------|
| "January 15, 2024" | Public-facing, formal |
| "2024-01-15" | Developer-focused, international |
| "Jan 15" | Informal, internal |

---

## Tone by Release Type

### Major Release

| Element | Approach |
|---------|----------|
| Headline | Celebratory, benefit-focused |
| Tone | Excited, confident |
| Visuals | Screenshots, demos |
| Length | Comprehensive |

### Minor Release

| Element | Approach |
|---------|----------|
| Headline | Clear, descriptive |
| Tone | Informative |
| Visuals | Optional |
| Length | Concise |

### Security/Hotfix

| Element | Approach |
|---------|----------|
| Headline | Direct, clear |
| Tone | Professional, reassuring |
| Visuals | Rarely needed |
| Length | Brief, to the point |

---

## Channel Adaptation

### Full Release Notes

For blog/documentation:
- Complete feature descriptions
- Screenshots and visuals
- Links to documentation
- Full context and reasoning

### In-App Announcement

For notification badges, modals:
```
**New: Bulk export**
Export all your data in one click. Try it in Settings > Export.
[Learn more]
```

### Email Announcement

```
Subject: [Product] January Update: Find files faster, export in one click

[Brief intro]

What's new:
• Advanced search filters
• One-click data export
• 40% faster dashboard

[CTA: See what's new]
```

### Social Media

```
Just shipped: Advanced search filters in [Product].
Find exactly what you need, way faster.
[Link to full release notes]
```

---

## Common Mistakes to Avoid

### Writing Pitfalls

| Avoid | Why | Instead |
|-------|-----|---------|
| "Various improvements" | Meaningless | List actual improvements |
| Technical jargon | Users don't care | User benefit language |
| "Minor bug fixes" | Dismissive | Name the fixes |
| Internal references | Confusing | User-facing descriptions |
| Massive walls of text | Won't be read | Scannable format |

### Structural Pitfalls

| Avoid | Why | Instead |
|-------|-----|---------|
| Inconsistent formatting | Hard to scan | Template for every release |
| Missing dates | Confusing timeline | Always include date |
| No version history | Can't find past notes | Maintain archive |
| Hidden breaking changes | Surprise users | Prominent placement |

---

## Release Notes Checklist

### Before Publishing

| Check | Question |
|-------|----------|
| Benefit-focused | Does each item explain the value to users? |
| Complete | Are all changes included? |
| Accurate | Does it match what actually shipped? |
| Scannable | Can someone skim in 30 seconds? |
| Actionable | Are there links to try new features? |
| Breaking changes | Prominently called out? |
| Migration info | Clear steps for any required changes? |
| Spell-check | No typos? |

### After Publishing

| Action | Why |
|--------|-----|
| Archive previous notes | Maintain history |
| Share across channels | Reach all users |
| Monitor feedback | Catch confusion/issues |
| Update documentation | Keep docs in sync |

---

## Templates

### Feature Release Entry

```markdown
## [Benefit headline]

[1-2 sentence description of what's new and why it matters]

![Screenshot/GIF description](image-url)

**How to try it:**
1. [Step 1]
2. [Step 2]

[Learn more →](link-to-docs)
```

### Quick Improvement/Fix Entry

```markdown
- **[Area]:** [What changed] ([impact/benefit if notable])
```

### Breaking Change Entry

```markdown
## ⚠️ Breaking Change: [Short description]

**What's changing:** [Clear explanation]

**Who's affected:** [Scope]

**What to do:**
1. [Step 1]
2. [Step 2]

**Timeline:** [Deadline if applicable]
```

### Monthly Release Email

```markdown
Subject: [Product] [Month] Update: [Top feature headline]

Hi [Name],

Here's what's new in [Product] this month:

**[Feature 1 headline]**
[1 sentence]

**[Feature 2 headline]**
[1 sentence]

**Also improved:**
• [Improvement 1]
• [Improvement 2]

[Button: See what's new]

Questions? [Reply to this email / Contact support]
```

---

This skill enables you to write release notes that effectively communicate product changes and help users take advantage of what's new.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

