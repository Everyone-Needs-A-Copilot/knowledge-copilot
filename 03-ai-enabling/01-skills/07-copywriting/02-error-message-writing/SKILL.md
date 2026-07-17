---
last_updated: 2026-02-25
status: active
name: error-message-writing
description: Write clear, helpful error messages that explain what happened and how to fix it. Use for system errors, form validation, API responses.
triggers:
  files: ["**/errors/**", "**/exceptions/**", "**/validation/**", "**/messages/**"]
  keywords: ["error message", "error copy", "validation message", "error handling", "user feedback", "error state", "failure message"]
allowed-tools: Read, Write, Edit
---

# Error Message Writing Skill

Write error messages that respect users' time and intelligence. Every error is an opportunity to guide users back to success - not to frustrate them with vague, blaming, or unhelpful copy.

---

## The Error Message Formula

Every error message should answer two questions:

```
[What happened] + [How to fix it]
```

| Bad | Good |
|-----|------|
| "Error" | "Couldn't save. Check your connection and try again." |
| "Invalid input" | "Email format not recognized. Try name@company.com" |
| "Request failed" | "Payment declined. Try a different card or contact your bank." |
| "Something went wrong" | "The file couldn't upload. It may be too large (max 10 MB)." |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Error Message Anatomy

### Structure

```
[Title/Headline - What went wrong]
[Body - Why it happened + What to do]
[Action - Button or link to resolve]
```

### Example

```
Title:  "Payment couldn't be processed"
Body:   "Your card was declined. This sometimes happens with new cards.
         Try a different payment method or contact your bank."
Actions: [Try different card] [Contact support]
```

---

## Error Types and Patterns

### Form Validation Errors

Show errors inline, near the problem field. Be specific.

| Field | Bad Error | Good Error |
|-------|-----------|------------|
| Email | "Invalid email" | "Enter a valid email (e.g., name@company.com)" |
| Password | "Invalid password" | "Password needs 8+ characters and one number" |
| Phone | "Invalid format" | "Enter a 10-digit phone number" |
| Date | "Invalid date" | "Enter a date after today (MM/DD/YYYY)" |
| Required | "Field required" | "First name is required" |

### Real-Time vs. On-Submit

| Timing | Use For | Example |
|--------|---------|---------|
| As you type | Format validation | "Passwords must match" |
| On blur | Field completion | "Email already registered" |
| On submit | Cross-field validation | "Start date must be before end date" |

### Connection and Network Errors

```
Temporary:
"Couldn't connect. Check your internet and try again."
[Try again]

Server issue:
"Our servers are temporarily unavailable. We're working on it."
[Check status page]

Timeout:
"Request timed out. This sometimes happens with large files."
[Try again] [Use smaller file]
```

### Authentication Errors

Balance security with helpfulness:

| Scenario | Message |
|----------|---------|
| Wrong credentials | "Email or password incorrect. Try again or reset password." |
| Account locked | "Account temporarily locked after 5 attempts. Try again in 15 minutes." |
| Session expired | "Your session expired. Sign in again to continue." |
| No account | "No account found with this email. Create one?" |

### Permission Errors

```
"You don't have access to this project.
Request access from the project owner, or contact your admin."
[Request access]
```

### File and Upload Errors

| Error | Message |
|-------|---------|
| Too large | "File exceeds 10 MB limit. Compress it or use a smaller file." |
| Wrong type | "Only PDF, DOC, and TXT files are supported." |
| Corrupted | "File couldn't be read. It may be corrupted. Try a different file." |
| Upload failed | "Upload interrupted. Check your connection and try again." |

### Payment Errors

| Error | Message |
|-------|---------|
| Card declined | "Card declined. Try a different card or contact your bank." |
| Expired card | "Card has expired. Update your payment method." |
| Insufficient funds | "Payment declined. Try a different payment method." |
| Processing error | "Payment couldn't be processed. Your card wasn't charged. Try again." |

---

## Tone Guidelines

### Do

| Principle | Example |
|-----------|---------|
| Be specific | "Password needs one number" not "Invalid password" |
| Be helpful | "Try again in 5 minutes" not "Rate limited" |
| Be honest | "We couldn't process this" not "An error occurred" |
| Be human | "That email's already registered" not "Duplicate entry" |

### Don't

| Avoid | Why | Instead |
|-------|-----|---------|
| Blame the user | Feels accusatory | Neutral, solution-focused |
| Use jargon | Users don't speak code | Plain language |
| Be vague | Doesn't help fix it | Specific error + action |
| Over-apologize | Feels performative | Just explain and help |
| Use ALL CAPS | Feels aggressive | Normal sentence case |

### Tone Spectrum

| Too Cold | Right | Too Casual |
|----------|-------|------------|
| "Error 403: Forbidden" | "You don't have access to this page" | "Whoops! Looks like you're not allowed here!" |
| "Invalid credentials" | "Email or password incorrect" | "Oops! Wrong password?" |
| "Operation failed" | "Changes couldn't be saved" | "Uh oh! Something went wrong!" |

---

## Error Message Patterns

### The "Try This" Pattern

```
"[What happened]. Try [specific action]."

Examples:
- "Couldn't save. Try again in a moment."
- "File too large. Try compressing it first."
- "Connection lost. Try reconnecting to WiFi."
```

### The "Because" Pattern

```
"[What happened] because [why]. [What to do]."

Examples:
- "Payment declined because the card expired. Update your card."
- "Upload failed because the file is too large. Use a file under 10 MB."
- "Can't delete because you have active subscriptions. Cancel them first."
```

### The "Check" Pattern

```
"[What happened]. Check [specific thing] and try again."

Examples:
- "Couldn't connect. Check your internet connection."
- "Sign-in failed. Check that caps lock is off."
- "Import failed. Check that the file format is CSV."
```

### The "Or" Pattern (Offer alternatives)

```
"[What happened]. [Option A] or [Option B]."

Examples:
- "Card declined. Try a different card or contact your bank."
- "Email already registered. Sign in or use a different email."
- "File too large. Compress it or split into multiple files."
```

---

## Context-Specific Errors

### Modal/Dialog Errors

```
Title: Clear, specific statement of error
Body:  1-2 sentences explaining why + what to do
Actions: Primary action to resolve | Secondary escape

Example:
Title:   "Unsaved changes will be lost"
Body:    "You have unsaved changes in this document. Save before leaving?"
Actions: [Save and leave] [Leave without saving] [Cancel]
```

### Inline Form Errors

- Show error immediately below the field
- Use red color and error icon for visibility
- Keep message to one line when possible

```
Email
[john@company____________]
⚠ This email is already registered. Sign in instead?
```

### Toast/Banner Errors

For non-blocking errors, brief and dismissible:

```
⚠ Couldn't auto-save. Check your connection.     [Retry] [✕]
```

### Empty State Errors

When search or filter returns nothing:

```
"No results for 'quarterly report'"
Try different keywords or remove filters.
[Clear filters]
```

---

## Technical Error Translation

### Server Errors to Human Language

| Code | Technical | Human Message |
|------|-----------|---------------|
| 400 | Bad Request | "Something's wrong with that request. Try again." |
| 401 | Unauthorized | "Sign in to continue." |
| 403 | Forbidden | "You don't have access to this." |
| 404 | Not Found | "We couldn't find that page." |
| 408 | Timeout | "Request took too long. Try again." |
| 429 | Too Many Requests | "Too many requests. Wait a moment and try again." |
| 500 | Internal Server Error | "Something went wrong on our end. We're looking into it." |
| 502 | Bad Gateway | "Our servers are temporarily unavailable." |
| 503 | Service Unavailable | "We're doing maintenance. Back soon." |

### Database Errors

| Technical | Human Message |
|-----------|---------------|
| Duplicate key | "That [thing] already exists. Try a different name." |
| Foreign key constraint | "Can't delete. This [thing] is still being used." |
| Connection failed | "Couldn't connect to our servers. Try again." |
| Query timeout | "Request took too long. Try with fewer items." |

---

## Error Prevention

### Before Errors Happen

| Technique | Example |
|-----------|---------|
| Input hints | "8+ characters, one number" below password field |
| Format examples | Placeholder: "MM/DD/YYYY" |
| Real-time validation | Green check when email format is valid |
| Confirmation dialogs | "Delete this project? This can't be undone." |
| Autosave | "All changes saved" indicator |

### Recovery Paths

Always provide a way forward:

| Error State | Recovery Path |
|-------------|---------------|
| Form validation | Fix highlighted fields |
| Authentication | Reset password link |
| Permission denied | Request access button |
| Network error | Retry button + offline mode |
| Not found | Search or navigation |

---

## Error Message Checklist

Before shipping, verify:

| Check | Question |
|-------|----------|
| Specific | Does it say exactly what went wrong? |
| Actionable | Does the user know what to do? |
| Human | Would you say this to someone in conversation? |
| Helpful | Does it help them succeed, not just report failure? |
| Blame-free | Is tone neutral, not accusatory? |
| Jargon-free | Would a non-technical user understand? |
| Concise | Is every word necessary? |
| Consistent | Does terminology match rest of product? |

---

## Anti-Patterns

### Messages to Never Use

| Pattern | Problem | Fix |
|---------|---------|-----|
| "An error occurred" | Meaningless | Specific error description |
| "Invalid [field]" | Blaming, vague | What's needed instead |
| "Something went wrong" | Unhelpful | What happened + what to do |
| "Oops!" | Infantilizing | Direct, professional |
| "Please try again later" | No clear action | When to try + alternative |
| "Contact support" (alone) | Lazy handoff | Explain error + offer support as option |

### Technical Leakage

Never expose:
- Stack traces
- Database errors
- Internal IDs
- Server paths
- Raw exception messages

```
Bad:  "NullPointerException at UserService.java:42"
Good: "Something went wrong. We've logged the issue."
```

---

## Examples by Industry

### E-commerce

```
Out of stock:
"This item just sold out. Want us to notify you when it's back?"
[Notify me] [Continue shopping]

Payment failed:
"Payment couldn't be processed. Your card wasn't charged.
Try a different card or payment method."
[Try different card] [Use PayPal]
```

### SaaS

```
Plan limit:
"You've reached your plan's 5 project limit.
Upgrade to create more projects."
[View plans] [Delete a project]

Feature unavailable:
"This feature is available on Pro and Enterprise plans."
[Compare plans] [Start free trial]
```

### Healthcare/Finance

```
Session expired (sensitive data):
"For your security, this session has expired.
Sign in again to continue."
[Sign in]

Compliance error:
"This action requires additional verification.
Check your email for a verification link."
[Resend email] [Contact support]
```

---

This skill enables you to write error messages that turn frustration into guidance.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

