---
last_updated: 2026-02-25
status: active
name: heuristic-evaluation
description: Expert review using Nielsen's 10 heuristics - systematic usability inspection without users. Use for identifying UX issues quickly.
triggers:
  files: ["**/ux/**", "**/audit/**", "**/review/**", "**/heuristics/**"]
  keywords: ["heuristic", "Nielsen", "usability review", "expert review", "ux audit", "inspection", "evaluation", "10 heuristics"]
allowed-tools: Read, Write, Edit
---

# Heuristic Evaluation Skill

Master guide for conducting expert usability reviews using Jakob Nielsen's 10 Usability Heuristics and other evaluation frameworks.

## Philosophy

**Heuristics are rules of thumb.** They're principles derived from decades of usability research. Violations correlate with user problems.

**Expert review complements user testing.** Find obvious issues fast through heuristics; validate with real users.

**Multiple evaluators find more.** One evaluator finds ~35% of issues. Three find ~60%. Five find ~75%.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Nielsen's 10 Usability Heuristics

### 1. Visibility of System Status

**Principle**: Keep users informed about what's happening through appropriate, timely feedback.

**Checklist**:
- [ ] System acknowledges user actions immediately
- [ ] Loading states show progress
- [ ] Current location/state is clear
- [ ] Changes are communicated
- [ ] System shows what's happening in background

**Violations**:
```
❌ Button click with no feedback
❌ Form submits with no loading indicator
❌ No confirmation after action
❌ User doesn't know if they're logged in
```

**Good examples**:
```
✅ Button shows loading spinner during submit
✅ Upload shows progress percentage
✅ Toast confirms "Item saved"
✅ Breadcrumbs show current location
```

### 2. Match Between System and Real World

**Principle**: Speak the user's language. Follow real-world conventions; make information appear in natural, logical order.

**Checklist**:
- [ ] Uses words users know (not jargon)
- [ ] Follows familiar conventions
- [ ] Information in logical order
- [ ] Metaphors match user expectations
- [ ] Icons are recognizable

**Violations**:
```
❌ Technical error codes ("ERR_0x45")
❌ Internal naming ("Go to HCM module")
❌ Illogical field order
❌ Obscure icons
```

**Good examples**:
```
✅ "Your session expired" vs "401 Unauthorized"
✅ "Contacts" not "CRM Entities"
✅ Name before email in forms
✅ Familiar shopping cart icon
```

### 3. User Control and Freedom

**Principle**: Support undo and redo. Provide clear emergency exits from unwanted states.

**Checklist**:
- [ ] Easy to cancel or go back
- [ ] Undo available for actions
- [ ] Can exit flows without completing
- [ ] No forced completion
- [ ] Clear "emergency exits"

**Violations**:
```
❌ No back button in wizard
❌ Can't undo delete
❌ Forced to complete signup
❌ Modal with no close option
```

**Good examples**:
```
✅ "Undo" option in toast notification
✅ Trash/archive before permanent delete
✅ "Skip" option in onboarding
✅ × to close any modal
```

### 4. Consistency and Standards

**Principle**: Users shouldn't have to wonder whether different words, situations, or actions mean the same thing.

**Checklist**:
- [ ] Same action = same label
- [ ] Same visual style for same elements
- [ ] Follows platform conventions
- [ ] Consistent terminology throughout
- [ ] Predictable behavior

**Violations**:
```
❌ "Delete" in one place, "Remove" in another
❌ Different button styles for same action
❌ Non-standard icon meanings
❌ Inconsistent date formats
```

**Good examples**:
```
✅ All primary buttons same style
✅ "Cancel" always on left
✅ Standard icons (⚙️ = settings)
✅ Consistent navigation pattern
```

### 5. Error Prevention

**Principle**: Better than good error messages is design that prevents problems in the first place.

**Checklist**:
- [ ] Constraints prevent invalid input
- [ ] Confirmation before destructive actions
- [ ] Clear requirements shown upfront
- [ ] Defaults are safe
- [ ] Edge cases handled

**Violations**:
```
❌ Any text allowed in phone field
❌ Delete without confirmation
❌ Hidden character requirements
❌ Date picker allows past dates for future events
```

**Good examples**:
```
✅ Input masks for formatted data
✅ "Are you sure?" for delete
✅ Inline validation as user types
✅ Date picker only shows valid dates
```

### 6. Recognition Rather Than Recall

**Principle**: Minimize user memory load by making objects, actions, and options visible or easily retrievable.

**Checklist**:
- [ ] Options visible, not hidden
- [ ] Recently used items accessible
- [ ] Context provided where needed
- [ ] Don't require remembering between screens
- [ ] Preview before committing

**Violations**:
```
❌ Command-line-only interface
❌ Codes users must remember
❌ No recent items list
❌ Referring to info from previous screens
```

**Good examples**:
```
✅ Recently viewed items shown
✅ Search suggestions based on history
✅ Preview of changes before apply
✅ Autocomplete dropdowns
```

### 7. Flexibility and Efficiency of Use

**Principle**: Accelerators for experts that don't affect novices. Allow customization for frequent actions.

**Checklist**:
- [ ] Keyboard shortcuts available
- [ ] Power user features don't clutter UI
- [ ] Customization options
- [ ] Multiple ways to accomplish tasks
- [ ] Defaults work for most users

**Violations**:
```
❌ No keyboard navigation
❌ Can't customize frequently used actions
❌ Only one way to do things
❌ Power features hidden from all users
```

**Good examples**:
```
✅ Cmd+K command palette
✅ Customizable dashboard
✅ Drag-and-drop AND menu options
✅ Quick actions for common tasks
```

### 8. Aesthetic and Minimalist Design

**Principle**: Don't include irrelevant or rarely needed information. Every extra unit of information competes with relevant information.

**Checklist**:
- [ ] Only necessary information shown
- [ ] Clear visual hierarchy
- [ ] Adequate white space
- [ ] Secondary info accessible but not prominent
- [ ] No visual clutter

**Violations**:
```
❌ Walls of text
❌ Every possible action shown
❌ Dense, cramped layouts
❌ Distracting decorative elements
```

**Good examples**:
```
✅ Progressive disclosure
✅ Clear primary action
✅ Generous spacing
✅ Information hierarchy
```

### 9. Help Users Recognize, Diagnose, and Recover from Errors

**Principle**: Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.

**Checklist**:
- [ ] Error messages in plain language
- [ ] Specifically identify the problem
- [ ] Suggest how to fix
- [ ] Don't blame user
- [ ] Visible where error occurred

**Violations**:
```
❌ "Error 500"
❌ "Invalid input"
❌ "Please try again"
❌ Error message at top, field at bottom
```

**Good examples**:
```
✅ "Password must be at least 8 characters"
✅ "Email address must include @"
✅ "Couldn't save. Check your connection."
✅ Error shown next to problematic field
```

### 10. Help and Documentation

**Principle**: Even though it's better if the system works without documentation, it may be necessary to provide help. Help should be easy to search, focused on user's task, and not too large.

**Checklist**:
- [ ] Contextual help available
- [ ] Help is searchable
- [ ] Task-focused, not feature-focused
- [ ] Easy to access when needed
- [ ] Doesn't interfere when not needed

**Violations**:
```
❌ No help available
❌ Help only in PDF manual
❌ Features explained, not tasks
❌ Help requires leaving the app
```

**Good examples**:
```
✅ Tooltips on complex features
✅ Inline help icons
✅ Searchable help center
✅ Getting started guides
```

---

## Evaluation Process

### 1. Preparation

```markdown
## Evaluation Setup

**Product:** [Name and version]
**Evaluator:** [Your name]
**Date:** [Date]
**Scope:** [What's being evaluated]

**Method:**
- [ ] Independent evaluation
- [ ] Heuristics reference available
- [ ] Severity scale defined
- [ ] Recording method ready
```

### 2. First Pass: Exploration

- Walk through main flows
- Note first impressions
- Identify key screens
- Understand system structure

### 3. Second Pass: Systematic Review

For each screen/flow:
1. Check against all 10 heuristics
2. Document violations
3. Note severity
4. Capture screenshots

### 4. Third Pass: Edge Cases

- Error states
- Empty states
- Long content
- Many items
- No permissions
- First-time use

### 5. Consolidation

- Review all findings
- Remove duplicates
- Prioritize by severity
- Identify patterns

---

## Severity Rating Scale

| Rating | Description | Impact |
|--------|-------------|--------|
| **0** | Not a usability problem | N/A |
| **1** | Cosmetic | Low priority, fix if time |
| **2** | Minor | Some users affected, fix soon |
| **3** | Major | Many users affected, high priority |
| **4** | Catastrophic | Must fix before release |

### Severity Factors

Consider:
- **Frequency**: How often encountered?
- **Impact**: How serious when it occurs?
- **Persistence**: Can users overcome it?

---

## Reporting Template

```markdown
# Heuristic Evaluation Report

## Executive Summary
- Evaluated: [Product/Feature]
- Date: [Date]
- Evaluators: [Names]
- Total issues: [#]
  - Severity 4: [#]
  - Severity 3: [#]
  - Severity 2: [#]
  - Severity 1: [#]

## Methodology
[Description of evaluation process]

## Findings by Heuristic

### H1: Visibility of System Status
**Issues found:** [#]

#### Issue 1.1: [Brief title]
**Location:** [Where in UI]
**Severity:** [1-4]
**Description:** [What's wrong]
**Heuristic violated:** System doesn't show [what]
**Recommendation:** [How to fix]
**Screenshot:** [Image]

[Repeat for each issue]

### H2: Match Between System and Real World
[Same structure]

[Continue for all heuristics]

## Summary Table

| ID | Issue | Location | Severity | Heuristic |
|----|-------|----------|----------|-----------|
| 1.1 | No loading state | Checkout | 3 | H1 |
| 2.1 | Technical jargon | Errors | 2 | H2 |
[...]

## Recommendations

### Critical (Fix Immediately)
1. [Issue] - [Brief solution]

### High Priority
1. [Issue] - [Brief solution]

### Medium Priority
1. [Issue] - [Brief solution]

### Low Priority
1. [Issue] - [Brief solution]
```

---

## Other Evaluation Frameworks

### Cognitive Walkthrough

Task-focused evaluation:

For each step in a task:
1. Will user know what to do?
2. Is the correct action visible?
3. Will user recognize it as correct?
4. Will user understand feedback?

### Accessibility Audit

WCAG 2.1 focused:
- Perceivable (alt text, contrast, captions)
- Operable (keyboard, timing, navigation)
- Understandable (readable, predictable, input assist)
- Robust (compatible with assistive tech)

### Content Audit

- Is language clear?
- Is terminology consistent?
- Is content current?
- Is content necessary?

---

## Common Issue Patterns

### Navigation Issues
- Unclear current location
- Inconsistent navigation
- Too many levels deep
- No breadcrumbs

### Form Issues
- Poor validation timing
- Unclear requirements
- Loss of data on error
- No autosave

### Feedback Issues
- No loading indicators
- Silent failures
- Unclear success states
- Delayed confirmation

### Consistency Issues
- Mixed terminology
- Inconsistent icons
- Variable button placement
- Different patterns for same action

---

## Quick Reference

### Heuristic Evaluation Checklist

Before evaluation:
- [ ] Define scope
- [ ] Gather heuristics reference
- [ ] Set up note-taking system
- [ ] Plan evaluation passes

During evaluation:
- [ ] Check all 10 heuristics per screen
- [ ] Rate severity consistently
- [ ] Capture screenshots
- [ ] Note location precisely

After evaluation:
- [ ] Consolidate findings
- [ ] Remove duplicates
- [ ] Prioritize by severity
- [ ] Write recommendations

### 10 Heuristics Quick Reference

| # | Heuristic | Key Question |
|---|-----------|--------------|
| 1 | Visibility of status | Do users know what's happening? |
| 2 | Match real world | Does it speak users' language? |
| 3 | User control | Can users undo/exit? |
| 4 | Consistency | Is it predictable? |
| 5 | Error prevention | Does it prevent mistakes? |
| 6 | Recognition | Can users see options? |
| 7 | Flexibility | Can experts work fast? |
| 8 | Minimalist design | Is it focused? |
| 9 | Error recovery | Are errors helpful? |
| 10 | Help | Is guidance available? |

---

## Summary

**Heuristic evaluation = Fast, expert-driven issue finding**

1. Learn the 10 heuristics
2. Evaluate systematically
3. Rate severity consistently
4. Document with screenshots
5. Prioritize recommendations

*Heuristics catch many issues quickly, but always validate critical findings with real users.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

