---
last_updated: 2026-02-25
status: active
name: clean-code-principles
description: Write self-documenting, maintainable code through naming, functions, and abstractions. Activate when writing, reviewing, or refactoring code for clarity.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["refactor", "clean code", "naming", "readability", "self-documenting", "code smell", "maintainability", "simplify"]
allowed-tools: Read, Write, Edit
---

# Clean Code Principles

Write code that communicates intent clearly. This skill guides you in creating self-documenting, maintainable code through thoughtful naming, function design, and appropriate abstractions.

## Core Philosophy

Code is read 10x more often than written. Every line communicates to future developers. Clean code:

| Principle | Meaning |
|-----------|---------|
| Reveals intent | The "what" and "why" are obvious |
| Minimizes cognitive load | Readers hold minimal context |
| Prevents misunderstanding | No ambiguity or surprises |
| Adapts to change | Easy to modify without breaking |

**Test:** Can a new team member understand this without asking questions?

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Naming

### Names Reveal Intent

| Type | Convention | Example |
|------|------------|---------|
| Variables | Nouns describing data | `user_count`, `active_orders` |
| Booleans | Questions/predicates | `is_valid`, `has_permission` |
| Functions | Verbs describing action | `calculate_total()`, `send_notification()` |
| Classes | Nouns describing entity | `UserService`, `OrderProcessor` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |

### Name Length Guidelines

- **Short scope** = short name OK (`u` in list comprehension)
- **Long scope** = descriptive name required (`authenticated_premium_users`)

### Avoid Meaningless Names

Never use: `data`, `info`, `temp`, `result`, `stuff`, `obj`, number suffixes (`user1`, `user2`)

---

## 2. Functions

### Single Responsibility

Each function does **one thing** well.

**Signs of too much:**
- Name contains "and" or "or"
- Multiple levels of abstraction
- Hard to describe in one sentence

### Function Guidelines

| Metric | Target |
|--------|--------|
| Lines | 5-15 (max 30) |
| Parameters | 0-3 |
| Return values | Single, clear type |

### Command-Query Separation

- **Command:** Change state, return nothing
- **Query:** Return data, no side effects

---

## 3. Abstractions

### One Level Per Function

Don't mix high-level and low-level operations in the same function.

### Rule of Three

Wait until you have 3 similar cases before abstracting. Premature abstraction creates unnecessary complexity.

### Extract Till You Drop

If you can name a block of code meaningfully, extract it as a function.

---

## 4. Comments

### When Comments Are Valuable

| Good Use | Example |
|----------|---------|
| Explain WHY | `# Retry with backoff to avoid API rate limits` |
| Warn about consequences | `# WARNING: Expensive query, cache for non-admins` |
| Document public APIs | Full docstrings with params, returns, raises |

### Comments to Avoid

- Redundant (says what code already says)
- Commented-out code (use git)
- Journal entries (use git)
- Noise (`# Constructor`)

---

## 5. Code Organization

### The Newspaper Metaphor

1. **Headline** - class/function name (most important)
2. **Lead** - public methods (high-level overview)
3. **Details** - private methods (supporting details)

### Vertical Density

Related code stays close together. Group by concept, not by type.

---

## 6. Error Handling

| Pattern | Recommendation |
|---------|----------------|
| Return codes | Avoid - use exceptions |
| Generic exceptions | Avoid - create specific types |
| Returning null | Avoid - raise or return Optional with clear naming |

---

## Quick Checklist

- [ ] Names reveal intent
- [ ] Functions do one thing (5-15 lines)
- [ ] 0-3 parameters
- [ ] One abstraction level per function
- [ ] Comments explain why, not what
- [ ] No redundant comments
- [ ] Specific exceptions
- [ ] Related code grouped

Clean code optimizes for readability over cleverness. When in doubt, make the next developer's job easier.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

