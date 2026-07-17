---
last_updated: 2026-02-25
status: active
name: feedback-loop-design
description: Design effective system feedback - communicating state changes, action results, and system status. Use for responsive, communicative interfaces.
triggers:
  files: ["**/feedback/**", "**/notifications/**", "**/alerts/**", "**/toast/**"]
  keywords: ["feedback", "notification", "alert", "toast", "status", "loading", "success", "error", "confirmation", "response"]
allowed-tools: Read, Write, Edit
---

# Feedback Loop Design Skill

Master guide for designing feedback systems that communicate effectively with users - confirming actions, showing progress, and maintaining user confidence.

## Philosophy

**Silence is confusion.** Every user action deserves acknowledgment. Without feedback, users don't know if the system heard them, leading to repeated clicks, abandoned tasks, and frustration.

**Feedback builds trust.** Consistent, timely feedback creates confidence. Users learn to trust systems that communicate clearly.

**Match feedback to importance.** Not all feedback needs the same treatment. A successful button click needs subtle confirmation; a failed payment needs prominent attention.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Feedback Types

### By Purpose

| Type | When | Example |
|------|------|---------|
| **Acknowledgment** | Action received | Button press animation |
| **Progress** | Task in progress | Loading spinner, progress bar |
| **Completion** | Task finished | Success message, checkmark |
| **Error** | Something failed | Error message with recovery |
| **Warning** | Potential issue | Confirmation dialog |
| **Information** | Status update | Notification badge |

### By Urgency

| Level | Treatment | Duration | Example |
|-------|-----------|----------|---------|
| **Critical** | Modal, blocking | Until dismissed | Payment failed |
| **Important** | Toast, prominent | 5-10 seconds | Save successful |
| **Informational** | Subtle, non-blocking | 3-5 seconds | New message |
| **Background** | Minimal/none | Instant | Auto-save indicator |

---

## Feedback Timing

### Response Time Guidelines

| Delay | User Perception | Feedback Needed |
|-------|-----------------|-----------------|
| 0-100ms | Instant | Visual state change |
| 100-1000ms | Working | Spinner or animation |
| 1-10s | Waiting | Progress indicator |
| 10s+ | Long wait | Progress + time estimate |

### Timing Patterns

**Immediate feedback** (< 100ms):
```
User clicks → Button state changes instantly
User types → Characters appear immediately
User hovers → Hover state shows
```

**Brief delay** (100ms - 1s):
```
User submits form → Show spinner
User saves file → Show "Saving..." indicator
User uploads → Start progress animation
```

**Extended process** (> 1s):
```
User starts export → Show progress bar
User initiates search → Show skeleton UI
User processes payment → Show step-by-step status
```

---

## Visual Feedback Patterns

### Button States

```css
/* Complete button state progression */
.button {
  /* Default */
  background: var(--primary);
}

.button:hover {
  /* Hover - interactive hint */
  background: var(--primary-dark);
  cursor: pointer;
}

.button:focus {
  /* Focus - keyboard navigation */
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

.button:active {
  /* Active - being pressed */
  transform: scale(0.98);
  background: var(--primary-darker);
}

.button:disabled {
  /* Disabled - not interactive */
  opacity: 0.5;
  cursor: not-allowed;
}

.button.loading {
  /* Loading - processing */
  pointer-events: none;
  /* Show spinner inside */
}
```

### Loading Indicators

**Spinner** - Unknown duration:
```
┌────────────────────┐
│      ◠             │
│     Loading...     │
└────────────────────┘
```

**Progress bar** - Known duration:
```
┌────────────────────┐
│ ████████░░░░ 67%   │
│ Processing files...│
└────────────────────┘
```

**Skeleton** - Content loading:
```
┌────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓       │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │
│ ▓▓▓▓▓▓▓▓           │
└────────────────────┘
```

**Steps** - Multi-stage process:
```
┌────────────────────────────┐
│ ● Upload  ● Process  ○ Done│
│        Analyzing files...  │
└────────────────────────────┘
```

### Success Feedback

**Checkmark animation**:
```css
@keyframes checkmark {
  0% { stroke-dashoffset: 100; }
  100% { stroke-dashoffset: 0; }
}
```

**Toast notification**:
```
┌────────────────────────────┐
│ ✓ Changes saved            │
└────────────────────────────┘
```

**Inline confirmation**:
```
[Save] → [✓ Saved] → [Save] (after 2s)
```

### Error Feedback

**Inline error**:
```
Email *
[invalid-email]
⚠ Please enter a valid email address
```

**Toast error**:
```
┌────────────────────────────┐
│ ✕ Could not save changes   │
│   [Try again]              │
└────────────────────────────┘
```

**Error page**:
```
┌────────────────────────────┐
│        :(                  │
│  Something went wrong      │
│                            │
│  [Go back] [Try again]     │
└────────────────────────────┘
```

---

## Notification Systems

### Toast Notifications

**Placement**:
```
Top-right (common)    Bottom-center (mobile)
┌──────────────┐      ┌─────────────────────┐
│          [□] │      │                     │
│              │      │                     │
│              │      │    [Toast here]     │
└──────────────┘      └─────────────────────┘
```

**Anatomy**:
```
┌─────────────────────────────────────┐
│ [Icon] Message text        [Close] │
│        Secondary action             │
└─────────────────────────────────────┘
```

**Guidelines**:
- Auto-dismiss after 3-5 seconds
- Allow manual dismiss
- Stack multiple toasts
- Don't cover important content
- Persist errors until dismissed

### Status Indicators

**Badge counts**:
```
🔔 3    Messages (unread count)
●      Activity (dot indicator)
⬤ Live  Real-time status
```

**Connection status**:
```
● Online   ○ Offline   ◐ Connecting
```

**Sync status**:
```
↻ Syncing   ✓ Synced   ✕ Sync failed
```

---

## Micro-interactions

### State Transitions

```css
/* Smooth state changes */
.element {
  transition: all 0.2s ease-out;
}

/* Different properties, different timing */
.card {
  transition:
    transform 0.15s ease-out,
    box-shadow 0.2s ease-out,
    background 0.1s ease-out;
}
```

### Interaction Feedback

**Hover lift**:
```css
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

**Press feedback**:
```css
.button:active {
  transform: scale(0.98);
}
```

**Success pulse**:
```css
@keyframes success-pulse {
  0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
}
```

---

## Optimistic UI

### Pattern

Show success immediately, roll back on failure:

```
1. User clicks "Like"
2. UI shows liked state immediately
3. API request sent in background
4. If fails: revert UI + show error
```

### Implementation

```javascript
// Optimistic update
function handleLike(postId) {
  // 1. Update UI immediately
  setLiked(true);
  setLikeCount(prev => prev + 1);

  // 2. Make API call
  try {
    await api.likePost(postId);
  } catch (error) {
    // 3. Revert on failure
    setLiked(false);
    setLikeCount(prev => prev - 1);
    showError("Couldn't like post. Try again.");
  }
}
```

### When to Use

**Good for**:
- Low-risk actions (likes, bookmarks)
- Common, fast operations
- Actions users expect to succeed

**Avoid for**:
- Critical operations (payments)
- Irreversible actions (delete)
- Actions requiring validation

---

## Progress Communication

### Determinate Progress

When you know the total:
```
┌────────────────────────────────────┐
│ Uploading 3 of 10 files...         │
│ ████████████░░░░░░░░░░░░░░░░ 30%  │
│ file-004.jpg                       │
└────────────────────────────────────┘
```

### Indeterminate Progress

When duration unknown:
```
┌────────────────────────────────────┐
│ Processing your request...         │
│ ▓▓▓▓░░░░▓▓▓▓░░░░▓▓▓▓ (animation) │
│ This may take a moment             │
└────────────────────────────────────┘
```

### Multi-Step Progress

```
┌────────────────────────────────────┐
│ Exporting data                     │
│                                    │
│ ✓ Gathering data                   │
│ ✓ Processing records               │
│ ◉ Generating file...               │
│ ○ Ready for download               │
└────────────────────────────────────┘
```

---

## Error Recovery

### Error Feedback Components

1. **What happened** - Clear description
2. **Why it happened** - Context (if helpful)
3. **What to do** - Recovery action

```
┌────────────────────────────────────┐
│ ✕ Upload failed                    │  What
│                                    │
│ The file exceeds the 10MB limit.   │  Why
│                                    │
│ [Choose smaller file] [Compress]   │  What to do
└────────────────────────────────────┘
```

### Error Levels

| Level | Display | User Action |
|-------|---------|-------------|
| Field | Inline below field | Fix and retry |
| Form | Summary above form | Review and retry |
| Page | Error banner | Navigate or retry |
| System | Error page | Wait or contact support |

---

## Accessibility

### Screen Reader Feedback

```html
<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true">
  Changes saved successfully
</div>

<!-- Assertive for errors -->
<div aria-live="assertive" role="alert">
  Error: Please enter a valid email
</div>
```

### Focus Management

```javascript
// After error, focus the first error field
function handleFormError() {
  const firstError = document.querySelector('[aria-invalid="true"]');
  firstError?.focus();
}

// After success, focus next logical element
function handleSuccess() {
  document.querySelector('[data-next-focus]')?.focus();
}
```

### Non-Visual Feedback

- Screen reader announcements for state changes
- Focus ring for keyboard navigation
- Haptic feedback on mobile (where supported)

---

## Anti-Patterns

### 1. Silent Failures

```
❌ Bad: Action fails with no indication
✅ Good: Clear error message with recovery option
```

### 2. Endless Loading

```
❌ Bad: Spinner forever with no timeout
✅ Good: Timeout after reasonable duration + retry option
```

### 3. Feedback Overload

```
❌ Bad: Toast for every minor action
✅ Good: Subtle feedback for minor, prominent for major
```

### 4. Generic Errors

```
❌ Bad: "An error occurred"
✅ Good: "Your session expired. Please sign in again."
```

### 5. Blocking Progress

```
❌ Bad: Success modal requiring dismiss
✅ Good: Auto-dismissing toast notification
```

### 6. Inconsistent Feedback

```
❌ Bad: Different feedback styles across app
✅ Good: Unified notification system
```

---

## Quick Reference

### Feedback Checklist

- [ ] Every action has visible feedback
- [ ] Loading states for operations > 100ms
- [ ] Progress indicators for operations > 1s
- [ ] Clear success confirmation
- [ ] Helpful error messages with recovery
- [ ] Consistent feedback patterns
- [ ] Accessible to screen readers
- [ ] Non-blocking where possible
- [ ] Auto-dismiss after appropriate duration

### Timing Quick Guide

| Duration | Show |
|----------|------|
| < 100ms | State change only |
| 100ms - 1s | Spinner |
| 1s - 10s | Progress indicator |
| > 10s | Progress + estimate |

### Feedback Hierarchy

```
Critical errors     → Modal (blocking)
Important messages  → Toast (prominent)
Minor confirmations → Inline (subtle)
Background activity → Indicator (minimal)
```

---

## Summary

**Good feedback = Trust + Confidence**

1. Acknowledge every action
2. Show progress for anything > 100ms
3. Confirm completions clearly
4. Make errors helpful, not hostile
5. Keep feedback proportional to importance
6. Make it accessible to all users

*Users should never wonder "Did that work?"*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

