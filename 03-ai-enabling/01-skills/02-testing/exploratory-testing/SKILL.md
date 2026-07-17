---
last_updated: 2026-02-25
status: active
name: exploratory-testing
description: Exploratory testing - simultaneous learning, test design, and execution. Use when discovering bugs through creative investigation.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*"]
  keywords: ["exploratory test", "ad hoc test", "session-based testing", "charter", "test exploration", "bug hunting", "manual testing"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides exploratory testing, a human-driven approach that combines learning, test design, and test execution simultaneously. Discover bugs that scripted tests miss through creative investigation.

The user provides testing requirements: a feature to explore, an area with suspected bugs, or a system to learn through testing. They may include context about time constraints, risk areas, or testing focus.

## What is Exploratory Testing

**Not random clicking.** Exploratory testing is structured investigation:

| Scripted Testing | Exploratory Testing |
|------------------|---------------------|
| Pre-written test cases | Tests designed during execution |
| Follow exact steps | Adapt based on findings |
| Pass/fail binary | Rich observations |
| Verifies known behavior | Discovers unknown behavior |
| Automated or manual | Human-driven |

**When to use exploratory testing:**
- New feature without documentation
- Complex user interactions
- Suspected hidden bugs
- Learning how system actually works
- Supplement to automated tests


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Session-Based Test Management (SBTM)

### Test Charter

Define focus before exploring:

```
Charter: Explore [target] with [resources] to discover [information]

Example:
Charter: Explore the checkout flow with valid and invalid payment methods
         to discover payment processing edge cases and error handling.

Time: 60 minutes
Focus: Payment validation, error messages, state consistency
Tools: Dev tools, multiple browsers, test payment cards
```

### Charter Components

| Component | Description | Example |
|-----------|-------------|---------|
| Target | What to test | Checkout flow |
| Resources | Tools and data | Test cards, browsers |
| Information | What to discover | Edge cases, bugs |
| Time | Session duration | 60 minutes |
| Focus | Specific areas | Payment validation |

### Session Notes Template

```markdown
# Exploratory Testing Session

**Charter:** [Your charter]
**Tester:** [Name]
**Date:** [Date]
**Duration:** 60 minutes planned

## Setup
- Environment: Staging
- Browser: Chrome 120
- Account: test_user@example.com

## Timeline

### 00:00 - Initial exploration
- Started at checkout with empty cart
- Noticed: No message when trying to checkout empty cart
- Bug #1: Silent failure on empty cart checkout

### 00:15 - Payment validation
- Tested expired card: 4000 0000 0000 0069
- Error message displayed correctly
- Tested invalid CVV: Accepts 2 digits (should require 3)
- Bug #2: CVV validation accepts invalid length

### 00:30 - Edge cases
- Added item, removed item, added different item
- Cart total correct
- Shipping calculation correct after address change

### 00:45 - Error recovery
- Simulated network timeout mid-payment
- Bug #3: Order stuck in "processing" state, no retry option

## Summary

**Bugs Found:** 3
**Observations:** 5
**Questions:** 2
**Coverage:** Checkout happy path, payment validation, error states

## Bugs
1. [HIGH] Empty cart checkout fails silently
2. [MED] CVV accepts 2-digit values
3. [HIGH] No recovery from payment timeout

## Questions
1. What happens if payment succeeds but confirmation email fails?
2. Is there a timeout limit for the "processing" state?
```

## Exploration Heuristics

### SFDPOT: San Francisco Depot

A mnemonic for areas to explore:

| Letter | Area | Questions |
|--------|------|-----------|
| S | Structure | How is it built? Components? Dependencies? |
| F | Function | What does it do? All features? |
| D | Data | What data does it use? Edge values? |
| P | Platform | What environment? Browsers? Devices? |
| O | Operations | How is it used? Sequences? Workflows? |
| T | Time | What changes over time? Timeouts? Dates? |

### FEW HICCUPS: Testing Mnemonics

| Letter | Focus | Example Tests |
|--------|-------|---------------|
| F | Flow | Interrupt mid-flow, skip steps |
| E | Existence | Empty, null, missing |
| W | Web | Browser back, refresh, tabs |
| H | Help | Documentation accuracy |
| I | Interoperability | System interactions |
| C | Concurrency | Multiple users, race conditions |
| C | Claims | Does it do what docs say? |
| U | Usability | Intuitive? Accessible? |
| P | Performance | Speed under load |
| S | Security | Auth, injection, data exposure |

### CRUD + Variations

| Operation | Variations to Test |
|-----------|-------------------|
| Create | Empty, duplicate, max length, special chars |
| Read | Missing item, permissions, pagination |
| Update | Partial, concurrent, invalid values |
| Delete | In use, cascade, undo |

## Exploration Techniques

### Boundary Probing

```
Testing a username field:
1. Start with typical input: "john_doe"
2. Try empty: ""
3. Try minimum: "a"
4. Try maximum: "a" × 50 (if max is 50)
5. Try over max: "a" × 51
6. Try special chars: "@#$%"
7. Try unicode: "用户名"
8. Try injection: "<script>alert(1)</script>"
```

### State Exploration

```
Testing a shopping cart:
1. Empty cart → checkout (what happens?)
2. Add item → remove item → add same item
3. Add item → close browser → reopen
4. Add item → logout → login
5. Add item as guest → register
6. Add item → item goes out of stock
7. Add item → price changes
```

### Interrupt Testing

```
Testing form submission:
1. Submit → immediately press back
2. Submit → close tab mid-submission
3. Submit → lose network connection
4. Submit → double-click submit button
5. Submit → refresh during processing
```

### Time-Based Testing

```
Testing time-sensitive features:
1. Set clock to past date
2. Set clock to far future
3. Cross midnight boundary
4. Cross timezone boundary
5. Test during DST transition
6. Test expiration (session, token, content)
```

## Bug Investigation Patterns

### When You Find Something Odd

```
1. REPRODUCE
   - Can I make it happen again?
   - What are the exact steps?
   - What are minimum steps?

2. VARY
   - Does it happen in other browsers?
   - Does it happen with different data?
   - Does it happen as different user types?

3. ISOLATE
   - What's the smallest change that triggers it?
   - What's the smallest change that prevents it?

4. DOCUMENT
   - Screenshot/video
   - Steps to reproduce
   - Expected vs actual
   - Environment details
```

### Bug Severity Assessment

| Severity | Impact | Example |
|----------|--------|---------|
| Critical | System unusable | Payment processing broken |
| High | Major feature broken | Cannot add items to cart |
| Medium | Feature impaired | Sort order incorrect |
| Low | Minor issue | Typo in error message |
| Cosmetic | Visual only | Misaligned button |

## Exploration Templates

### Feature Exploration

```markdown
## Feature: [Name]

### What I Know
- [Documentation says...]
- [Similar to existing feature X...]

### Questions to Answer
1. How does it handle invalid input?
2. What happens at boundaries?
3. How does it interact with [related feature]?

### Test Ideas
- [ ] Happy path with typical data
- [ ] Happy path with edge case data
- [ ] Error paths (invalid input, missing data)
- [ ] Interruptions (back button, timeout)
- [ ] Concurrent usage

### Findings
| Time | Observation | Type | Severity |
|------|-------------|------|----------|
| 10:15 | X happens when Y | Bug | High |
```

### Bug Hunt Session

```markdown
## Bug Hunt: [Area]

### Hypothesis
- Bugs might exist in [area] because:
  - [Reason 1: Complex logic]
  - [Reason 2: Recent changes]
  - [Reason 3: User reports]

### Hunt Strategy
1. Try edge cases in [specific input]
2. Test race conditions in [workflow]
3. Check error handling in [feature]

### Environment
- Production-like staging
- Multiple browsers
- Test data: [describe]

### Results
| Bug | Severity | Reproducible | Notes |
|-----|----------|--------------|-------|
| #1  | High     | Always       | [details] |
```

### Smoke Test Exploration

```markdown
## Smoke Test: [Release/Build]

### Critical Paths
- [ ] User can register
- [ ] User can login
- [ ] User can [core action 1]
- [ ] User can [core action 2]
- [ ] User can [core action 3]

### Quick Checks
- [ ] Homepage loads
- [ ] Navigation works
- [ ] Search returns results
- [ ] Forms submit
- [ ] Payments process (test mode)

### Issues Found
| Path | Issue | Blocking? |
|------|-------|-----------|
```

## Combining with Automation

### What to Automate After Exploring

| Finding | Automate? | Why |
|---------|-----------|-----|
| Critical bug fix | Yes | Regression prevention |
| Edge case bug | Yes | Prevent recurrence |
| Happy path works | Yes | Smoke test |
| UI layout issue | Maybe | Visual regression tools |
| Usability problem | No | Needs human judgment |
| Complex sequence | Partial | Key steps only |

### Exploration → Test Case Pipeline

```
1. Explore feature manually
2. Document interesting scenarios
3. Identify automatable patterns
4. Write automated tests for:
   - Regression bugs found
   - Critical path scenarios
   - Boundary conditions found
5. Continue manual exploration for:
   - New features
   - Complex interactions
   - Subjective quality
```

## Reporting Exploration Results

### Session Summary

```markdown
## Session Summary

**Charter:** Explore checkout payment processing
**Duration:** 60 minutes (90% on testing)
**Coverage:** Payment validation, error handling, timeout behavior

### Key Findings
1. 🐛 [HIGH] CVV validation accepts 2 digits
2. 🐛 [HIGH] No recovery from payment timeout
3. 🐛 [MED] Empty cart checkout fails silently
4. ❓ Question: What happens to orphaned orders?
5. 💡 Idea: Add payment retry mechanism

### Metrics
- Bugs found: 3
- Questions raised: 2
- Test ideas generated: 5
- Areas need more exploration: Timeout handling

### Recommendations
1. Fix CVV validation before release
2. Add order recovery mechanism
3. Schedule session for timeout scenarios
```

### Defect Report from Exploration

```markdown
## Bug Report

**Title:** CVV validation accepts 2-digit values
**Severity:** Medium
**Found:** Exploratory session 2024-01-15
**Reporter:** [Name]

### Environment
- Staging server
- Chrome 120, Windows 11
- Test card: 4242 4242 4242 4242

### Steps to Reproduce
1. Go to checkout
2. Enter valid card number
3. Enter 2-digit CVV (e.g., "12")
4. Submit payment

### Expected
- Form validation error
- CVV field highlighted
- Message: "CVV must be 3 or 4 digits"

### Actual
- Form submits
- Payment fails with unclear error later

### Impact
- Poor user experience
- Unnecessary API calls
- Confusing error state

### Attachments
- Screenshot of form accepting "12"
- Video of full flow
```

## Quick Reference

### Session Checklist

Before session:
- [ ] Charter defined
- [ ] Time boxed
- [ ] Environment ready
- [ ] Tools prepared
- [ ] Note template open

During session:
- [ ] Stay focused on charter
- [ ] Take continuous notes
- [ ] Screenshot findings
- [ ] Note questions and ideas
- [ ] Watch the clock

After session:
- [ ] Summarize findings
- [ ] File bug reports
- [ ] Share with team
- [ ] Plan follow-up

### Exploration Time Allocation

| Activity | % of Time |
|----------|-----------|
| Actual testing | 80-90% |
| Note taking | 5-10% |
| Bug investigation | 5-10% |
| Session setup | < 5% |

## Summary

Exploratory testing finds bugs scripted tests miss:

1. **Use charters** - Focus exploration, don't wander
2. **Time box sessions** - 60-90 minutes max
3. **Take notes** - Document as you go
4. **Use heuristics** - SFDPOT, FEW HICCUPS
5. **Vary inputs** - Boundaries, interrupts, time
6. **Investigate thoroughly** - Reproduce, vary, isolate
7. **Report clearly** - Bugs, questions, ideas
8. **Feed automation** - Turn findings into tests


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

