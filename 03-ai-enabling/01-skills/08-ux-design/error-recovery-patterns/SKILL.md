---
last_updated: 2026-02-25
status: active
name: error-recovery-patterns
description: Design for graceful error handling and recovery - helping users recover from mistakes and system failures. Use for resilient interfaces.
triggers:
  files: ["**/error/**", "**/exception/**", "**/fallback/**"]
  keywords: ["error handling", "error recovery", "error message", "fallback", "retry", "undo", "graceful degradation", "fault tolerant"]
allowed-tools: Read, Write, Edit
---

# Error Recovery Patterns Skill

Master guide for designing interfaces that help users recover from errors gracefully - whether user mistakes, validation failures, or system errors.

## Philosophy

**Errors are inevitable.** Users make mistakes. Systems fail. Networks drop. Good design anticipates failure and makes recovery effortless.

**Blame the design, not the user.** If users make errors, the design failed to prevent them. Error messages should help, not lecture.

**Every error is a crossroads.** Users who can't recover abandon. Users who recover easily become more confident.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Error Prevention

### Proactive Patterns

Prevent errors before they happen:

| Pattern | Implementation | Example |
|---------|----------------|---------|
| **Constraints** | Limit invalid inputs | Date picker vs free text |
| **Defaults** | Pre-fill sensible values | Country based on IP |
| **Confirmation** | Verify destructive actions | "Delete 5 files?" |
| **Undo** | Reverse recent actions | Gmail's "Undo send" |
| **Auto-save** | Prevent data loss | Draft saved every 30s |
| **Suggestions** | Guide correct input | Autocomplete |

### Input Constraints

```
❌ Bad: Free text for date
[Enter date: __________]

✅ Good: Constrained picker
[📅 Jan 15, 2024 ▼]
```

```
❌ Bad: Any value accepted
Amount: [_________]

✅ Good: Constrained input
Amount: [$] [0.00] (min: $1.00, max: $10,000)
```

### Confirmation Patterns

**Destructive actions**:
```
┌────────────────────────────────────┐
│ Delete "Project Alpha"?            │
│                                    │
│ This will permanently delete the   │
│ project and all 47 files inside.   │
│                                    │
│ Type "Project Alpha" to confirm:   │
│ [____________________]             │
│                                    │
│     [Cancel]  [Delete Project]     │
└────────────────────────────────────┘
```

**High-impact changes**:
```
┌────────────────────────────────────┐
│ Change billing plan?               │
│                                    │
│ From: Pro ($29/mo)                 │
│ To: Basic ($9/mo)                  │
│                                    │
│ You'll lose:                       │
│ • Priority support                 │
│ • Advanced analytics               │
│ • 50GB → 5GB storage               │
│                                    │
│     [Keep Pro]  [Downgrade]        │
└────────────────────────────────────┘
```

---

## Error Message Design

### Anatomy of a Good Error

```
┌────────────────────────────────────┐
│ [Icon] Title (what happened)       │
│                                    │
│ Explanation (why + context)        │
│                                    │
│ [Primary Action] [Secondary]       │
└────────────────────────────────────┘
```

### Error Message Formula

1. **What happened** - Brief, clear description
2. **Why it happened** - Context (if helpful)
3. **What to do** - Specific action(s)

```
❌ Bad:
"Error 500: Internal Server Error"

✅ Good:
"We couldn't save your changes"
"Our servers are temporarily overloaded."
"[Try again] or [Save offline]"
```

### Tone Guidelines

| Don't | Do |
|-------|-----|
| "Invalid input" | "Please enter a valid email" |
| "Error occurred" | "We couldn't complete your request" |
| "You entered wrong" | "That password doesn't match" |
| "Failure" | "Something went wrong" |
| Technical jargon | Plain language |
| Passive voice | Active voice |
| Blame user | Offer solution |

### Error Specificity

**Too vague**:
```
❌ "Something went wrong"
```

**Too technical**:
```
❌ "ECONNREFUSED: Connection refused at 127.0.0.1:3000"
```

**Just right**:
```
✅ "We couldn't connect to the server. Check your internet
   connection and try again."
```

---

## Validation Patterns

### Real-Time Validation

Validate as users type (with debounce):

```
Email:
[john@example.co] ✓ Valid

Password:
[weak]
⚠ Password too short (minimum 8 characters)
  □ 8+ characters
  ✓ Contains letter
  □ Contains number
```

### On-Blur Validation

Validate when field loses focus:

```
Before blur: [j]
After blur:  [j] ⚠ Please enter a valid email
```

### Submit Validation

Validate all fields on submit:

```
┌────────────────────────────────────┐
│ ⚠ Please fix 2 errors below        │
│ • Email is required                │
│ • Password must be 8+ characters   │
└────────────────────────────────────┘

Name:
[John Smith] ✓

Email *:
[______________] ← Focus here
⚠ Email is required

Password *:
[short]
⚠ Password must be 8+ characters
```

### Field Error Display

```css
/* Error state styling */
.field-error input {
  border-color: var(--color-error);
  background: var(--color-error-bg);
}

.field-error .error-message {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Icon for additional clarity */
.field-error::before {
  content: "⚠";
  color: var(--color-error);
}
```

---

## Recovery Patterns

### Undo

Allow users to reverse actions:

```
┌────────────────────────────────────┐
│ ✓ Email sent  [Undo - 5s]          │
└────────────────────────────────────┘
```

**Implementation considerations**:
- Time-limited (5-30 seconds typically)
- Clear countdown or timer
- Works for common destructive actions
- Stores state for reversal

### Retry

Enable users to attempt failed actions again:

```
┌────────────────────────────────────┐
│ ✕ Upload failed                    │
│                                    │
│ Connection interrupted             │
│                                    │
│ [Try again] [Cancel]               │
└────────────────────────────────────┘
```

**Retry with backoff**:
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000); // Exponential backoff
    }
  }
}
```

### Auto-Recovery

Automatically recover when possible:

```
┌────────────────────────────────────┐
│ ○ Connection lost                  │
│   Reconnecting...                  │
└────────────────────────────────────┘

↓ (after reconnection)

┌────────────────────────────────────┐
│ ● Connection restored              │
│   Your changes have been saved     │
└────────────────────────────────────┘
```

### Draft Preservation

Save work automatically:

```
┌────────────────────────────────────┐
│ ⚠ You have unsaved changes         │
│                                    │
│ Do you want to continue editing    │
│ your draft from 10 minutes ago?    │
│                                    │
│ [Discard] [Continue editing]       │
└────────────────────────────────────┘
```

---

## Graceful Degradation

### Fallback Hierarchy

```
Primary → Cached → Fallback → Error

Example: User profile image
1. Load from server
2. If fails → Show cached version
3. If no cache → Show initials avatar
4. If all fails → Show generic placeholder
```

### Feature Degradation

```
Full experience:
┌────────────────────────────────────┐
│ [Rich text editor with formatting] │
└────────────────────────────────────┘

Degraded (JS fails):
┌────────────────────────────────────┐
│ [Basic textarea]                   │
└────────────────────────────────────┘
```

### Offline Patterns

```
┌────────────────────────────────────┐
│ ⚡ You're offline                   │
│                                    │
│ You can still:                     │
│ • View cached content              │
│ • Edit drafts (syncs when online)  │
│ • Browse previously loaded pages   │
│                                    │
│ Not available:                     │
│ • Search                           │
│ • Send messages                    │
└────────────────────────────────────┘
```

---

## Error Page Design

### 404 Not Found

```
┌────────────────────────────────────┐
│              🔍                    │
│                                    │
│    Page not found                  │
│                                    │
│    This page doesn't exist or      │
│    may have been moved.            │
│                                    │
│    [Go to homepage]                │
│    [Search site]                   │
│                                    │
│    Popular pages:                  │
│    • Products                      │
│    • Support                       │
│    • Contact                       │
└────────────────────────────────────┘
```

### 500 Server Error

```
┌────────────────────────────────────┐
│              ⚠️                    │
│                                    │
│    Something went wrong            │
│                                    │
│    We're working on fixing this.   │
│    Please try again in a few       │
│    minutes.                        │
│                                    │
│    [Refresh page]                  │
│    [Report issue]                  │
│                                    │
│    Error ID: ABC-123-XYZ           │
└────────────────────────────────────┘
```

### Maintenance Page

```
┌────────────────────────────────────┐
│              🔧                    │
│                                    │
│    We'll be back soon              │
│                                    │
│    Scheduled maintenance           │
│    Expected duration: ~30 minutes  │
│    Started: 2:00 PM UTC            │
│                                    │
│    [Status page] [@statusTwitter]  │
└────────────────────────────────────┘
```

---

## Error States by Component

### Empty States (No Data)

```
┌────────────────────────────────────┐
│          📭                        │
│                                    │
│    No messages yet                 │
│                                    │
│    Start a conversation to see     │
│    your messages here.             │
│                                    │
│    [New message]                   │
└────────────────────────────────────┘
```

### Load Failures

```
┌────────────────────────────────────┐
│          ⚠️                        │
│                                    │
│    Couldn't load messages          │
│                                    │
│    Check your connection and       │
│    try again.                      │
│                                    │
│    [Retry]                         │
└────────────────────────────────────┘
```

### Partial Failures

```
┌────────────────────────────────────┐
│ ✓ 8 of 10 files uploaded           │
│                                    │
│ Failed:                            │
│ ✕ large-video.mp4 (exceeds 50MB)   │
│ ✕ corrupted.pdf (file unreadable)  │
│                                    │
│ [Retry failed] [Skip and continue] │
└────────────────────────────────────┘
```

---

## Accessibility

### Screen Reader Announcements

```html
<!-- Announce errors to screen readers -->
<div role="alert" aria-live="assertive">
  Error: Please enter a valid email address
</div>

<!-- Focus management after error -->
<script>
  document.querySelector('[aria-invalid="true"]')?.focus();
</script>
```

### Error Identification

```html
<!-- Associate error with field -->
<label for="email">Email</label>
<input
  id="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">
  Please enter a valid email
</span>
```

### Color Independence

```
❌ Bad: Red border only
✅ Good: Red border + icon + text message
```

---

## Anti-Patterns

### 1. Dead Ends

```
❌ Bad:
"Error occurred" [OK]
→ User stuck, no way forward

✅ Good:
"Error occurred" [Retry] [Go back] [Get help]
→ Clear paths forward
```

### 2. Data Loss

```
❌ Bad:
Error on submit → Form cleared
→ User loses all input

✅ Good:
Error on submit → Form preserved with errors highlighted
→ User fixes only what's wrong
```

### 3. Generic Messages

```
❌ Bad:
"Invalid input"
→ Which input? What's wrong?

✅ Good:
"Password must be at least 8 characters"
→ Specific, actionable
```

### 4. Buried Errors

```
❌ Bad:
Errors only in console.log
→ Users don't see developer tools

✅ Good:
Visible error in UI with recovery options
```

### 5. Blame Language

```
❌ Bad:
"You entered an invalid date"

✅ Good:
"Please enter a date in MM/DD/YYYY format"
```

---

## Quick Reference

### Error Recovery Checklist

- [ ] Errors clearly explain what happened
- [ ] Errors explain what to do next
- [ ] Recovery actions are visible and accessible
- [ ] Form data preserved after errors
- [ ] Undo available for destructive actions
- [ ] Retry available for transient failures
- [ ] Offline state handled gracefully
- [ ] Errors announced to screen readers
- [ ] Error states don't rely on color alone

### Error Message Template

```
[What]: We couldn't [action]
[Why]: [Reason if helpful]
[Do]: [Primary action] or [Alternative]
```

### Recovery Priority

| Error Type | Recovery Pattern |
|------------|------------------|
| User input | Inline validation + preserve data |
| Network | Retry + offline fallback |
| Server | Retry + error ID for support |
| Permission | Explain + request access |
| Not found | Search + popular links |

---

## Summary

**Design for recovery, not just success.**

1. Prevent errors through constraints and confirmation
2. Write helpful, specific error messages
3. Always provide a path forward
4. Preserve user data across errors
5. Enable undo for destructive actions
6. Degrade gracefully when systems fail

*The best error handling makes users feel competent, not frustrated.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

