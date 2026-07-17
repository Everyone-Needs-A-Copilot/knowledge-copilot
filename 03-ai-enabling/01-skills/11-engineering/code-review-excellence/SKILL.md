---
last_updated: 2026-02-25
status: active
name: code-review-excellence
description: Conduct effective, constructive code reviews that improve code quality and team knowledge. Activate when reviewing or preparing PRs.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["code review", "PR review", "pull request", "review comments", "feedback", "approval", "merge request"]
allowed-tools: Read, Write, Edit
---

# Code Review Excellence

Conduct reviews that improve code quality, share knowledge, and build team trust. This skill covers both giving and receiving effective code reviews.

## Purpose of Code Review

| Primary Goals | Secondary Goals |
|---------------|-----------------|
| Catch bugs early | Share knowledge |
| Ensure code quality | Maintain consistency |
| Verify requirements | Mentorship |
| Security review | Team alignment |

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. As a Reviewer

### Review Mindset

- **Assume positive intent** - Author did their best
- **Be curious, not critical** - "I wonder why..." not "Why did you..."
- **Focus on the code** - Not the person
- **Offer alternatives** - Not just criticism
- **Pick your battles** - Major issues > style nits

### What to Look For

#### Priority 1: Critical Issues

| Area | Questions |
|------|-----------|
| **Correctness** | Does it work? Edge cases handled? |
| **Security** | Input validation? Auth checks? Injection risks? |
| **Data integrity** | Transactions? Race conditions? |
| **Breaking changes** | API compatibility? Migration needed? |

#### Priority 2: Code Quality

| Area | Questions |
|------|-----------|
| **Design** | Right abstraction level? Single responsibility? |
| **Clarity** | Self-documenting? Comments where needed? |
| **Tests** | Coverage adequate? Right test types? |
| **Error handling** | Failures handled gracefully? |

#### Priority 3: Style & Conventions

| Area | Questions |
|------|-----------|
| **Naming** | Clear, consistent? |
| **Formatting** | Matches team style? |
| **Documentation** | Public APIs documented? |

### Comment Guidelines

#### Use Comment Prefixes

| Prefix | Meaning |
|--------|---------|
| `nit:` | Minor style suggestion, optional |
| `suggestion:` | Idea to consider |
| `question:` | Seeking understanding |
| `issue:` | Must be addressed |
| `praise:` | Something done well |

#### Good vs. Bad Comments

**Bad: Vague criticism**
```
"This is confusing"
```

**Good: Specific, actionable**
```
"suggestion: This method does validation and processing.
Consider extracting `validate_input()` to make each
responsibility clear."
```

**Bad: Demanding**
```
"Change this to use map()"
```

**Good: Educational**
```
"nit: This could be `[x.name for x in users]` which
is more idiomatic Python. Happy to leave as-is if you
prefer the explicit loop."
```

### The Feedback Sandwich

For significant issues:
1. **Acknowledge** what's working
2. **Identify** the concern
3. **Suggest** improvement

```
"The overall approach of separating the API client looks
great. I'm concerned the retry logic might hit rate limits
under load. What do you think about exponential backoff?
We have a utility for this in `utils/retry.py`."
```

---

## 2. As an Author

### Before Requesting Review

| Checklist | |
|-----------|---|
| Tests pass locally | ✓ |
| Self-reviewed the diff | ✓ |
| PR description explains what/why | ✓ |
| Linked to ticket/issue | ✓ |
| Removed debug code | ✓ |
| No unrelated changes | ✓ |

### Writing Good PR Descriptions

```markdown
## What
Add exponential backoff to payment retries

## Why
Current immediate retries cause rate limiting under load (see ISSUE-123)

## How
- Added `RetryPolicy` class with configurable backoff
- Payment client uses policy for failed transactions
- Default: 3 retries, 1s base, 2x multiplier, 30s max

## Testing
- Unit tests for RetryPolicy
- Integration test for payment retry flow
- Manual tested with payment sandbox

## Notes
- Requires config change for MAX_RETRY_DELAY
- Consider follow-up to add circuit breaker
```

### Responding to Feedback

| Do | Don't |
|----|-------|
| Thank reviewers | Get defensive |
| Ask for clarification | Argue without understanding |
| Explain your reasoning | Dismiss feedback |
| Accept valid points | Take it personally |
| Push back respectfully | Ignore comments |

**Disagreeing constructively:**
```
"I see the concern about complexity. I chose this approach
because [reasoning]. Would it help if I added a comment
explaining the trade-off, or do you feel strongly about
the alternative?"
```

---

## 3. Review Process

### Efficient Review Flow

1. **Read PR description** - Understand context
2. **Check scope** - Is it focused?
3. **Review test changes first** - Understand expected behavior
4. **Review implementation** - Does it meet test expectations?
5. **Run locally if needed** - For complex changes

### Size Guidelines

| PR Size | Lines Changed | Review Time |
|---------|--------------|-------------|
| Small | < 200 | 15-30 min |
| Medium | 200-500 | 30-60 min |
| Large | 500+ | Break it up |

**Large PRs should be avoided.** If unavoidable, guide reviewers with a detailed description and suggest review order.

### Approval Criteria

| Must Have | Nice to Have |
|-----------|--------------|
| Correct functionality | Optimal performance |
| Adequate tests | Perfect naming |
| No security issues | Comprehensive docs |
| No breaking changes (or documented) | Elegant design |

---

## 4. Team Practices

### Review Etiquette

| Reviewer | Author |
|----------|--------|
| Review within 24h | Keep PRs small |
| Respond to follow-ups | Respond to feedback promptly |
| Approve when satisfied | Don't merge with open threads |

### Handling Disagreements

1. **Discuss in PR** - Keep context together
2. **Time-box discussion** - 2-3 rounds max
3. **Escalate if stuck** - Bring in third party
4. **Document decision** - ADR if significant

### Review Coverage

- **Every PR reviewed** - No exceptions
- **Two reviewers for critical paths** - Auth, payments, data
- **Domain expert for specialized areas** - Security, infra

---

## Quick Reference

### Reviewer Checklist

- [ ] Code works correctly
- [ ] Security considered
- [ ] Tests adequate
- [ ] Design reasonable
- [ ] Documentation sufficient
- [ ] Feedback specific and constructive

### Author Checklist

- [ ] Tests pass
- [ ] Self-reviewed
- [ ] Description complete
- [ ] Changes focused
- [ ] Feedback addressed

### Comment Prefixes

- `nit:` - Optional style
- `suggestion:` - Consider this
- `question:` - Help me understand
- `issue:` - Must fix
- `praise:` - Well done

Code review is collaboration, not gatekeeping. The goal is better code AND better engineers.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

