---
last_updated: 2026-02-25
status: active
name: debugging-strategies
description: Systematic approaches to finding and fixing bugs efficiently. Activate when investigating issues, tracing errors, or diagnosing unexpected behavior.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["debug", "bug", "error", "issue", "trace", "diagnose", "investigate", "breakpoint", "stack trace", "root cause"]
allowed-tools: Read, Write, Edit
---

# Debugging Strategies

Systematic approaches to finding and fixing bugs efficiently. Debug like a scientist: hypothesize, test, conclude.

## Core Mindset

| Principle | Practice |
|-----------|----------|
| **Be systematic** | Don't guess randomly |
| **Question assumptions** | The bug is rarely where you first look |
| **Isolate variables** | Change one thing at a time |
| **Document findings** | Track what you've tried |

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. The Debugging Process

### Scientific Method for Bugs

1. **Reproduce** - Can you make it happen reliably?
2. **Observe** - What exactly happens? What should happen?
3. **Hypothesize** - What could cause this?
4. **Test** - Validate or invalidate hypothesis
5. **Fix** - Address root cause
6. **Verify** - Confirm fix, check for regressions

### Reproduction Is King

If you can't reproduce it, you can't fix it.

| Reproduction Level | Approach |
|-------------------|----------|
| **Consistent** | Great - proceed to diagnose |
| **Intermittent** | Find pattern: timing, load, data? |
| **Environment-specific** | Compare environments |
| **User-reported only** | Get logs, screenshots, steps |

---

## 2. Information Gathering

### Essential Questions

| Question | Why It Matters |
|----------|----------------|
| What changed recently? | Narrows time window |
| What's the expected behavior? | Defines the gap |
| What's the actual behavior? | Precise symptoms |
| When did it start? | Correlate with deploys/changes |
| Who is affected? | Scope the impact |
| How often? | Severity, patterns |

### Where to Look

| Source | What You'll Find |
|--------|------------------|
| Stack traces | Execution path, line numbers |
| Application logs | Events, errors, warnings |
| System metrics | CPU, memory, disk, network |
| Database queries | Slow queries, deadlocks |
| Network traffic | Request/response payloads |
| Git history | Recent changes |
| Monitoring dashboards | Timing, patterns |

### Reading Stack Traces

```python
Traceback (most recent call last):
  File "app.py", line 45, in handle_request    # Entry point
    result = process_data(data)
  File "processor.py", line 23, in process_data # Called from handle_request
    return validate(data)
  File "validator.py", line 12, in validate     # Root cause location
    raise ValueError("Invalid format")          # Actual error
ValueError: Invalid format
```

Read **bottom-up** for the error, **top-down** for context.

---

## 3. Debugging Techniques

### Binary Search

Narrow down the problem space:

1. Find a known-good state (works) and known-bad state (broken)
2. Test midpoint between them
3. Move boundary based on result
4. Repeat until isolated

```
Commits: A --- B --- C --- D --- E --- F (broken)
                     ↑
              Test here first
         If broken: bug is A-C
         If works: bug is D-F
```

### Rubber Duck Debugging

Explain the problem out loud, step by step:
- "First, the user clicks submit..."
- "Then the form data is sent to..."
- "The server receives... wait, does it actually receive all fields?"

The act of explaining often reveals assumptions.

### Simplify and Isolate

Create minimal reproduction:
1. Remove unrelated code
2. Hardcode dependencies
3. Reduce data to minimal failing case
4. Run in isolation

### Print Debugging (Strategic)

```python
# Mark entry points
print(f">>> Entering process_order: {order_id=}")

# Track state changes
print(f"Before validation: {order.status=}")
validate(order)
print(f"After validation: {order.status=}")

# Confirm execution paths
if condition:
    print(">>> Taking path A")
else:
    print(">>> Taking path B")
```

### Breakpoint Debugging

When to use debugger vs. prints:

| Use Debugger | Use Prints |
|--------------|------------|
| Complex state inspection | Quick checks |
| Step through logic | Production debugging |
| Examine call stack | Distributed systems |
| Interactive exploration | When debugger unavailable |

---

## 4. Common Bug Patterns

### Data Issues

| Pattern | Symptoms | Check |
|---------|----------|-------|
| Null/undefined | `NoneType has no attribute` | Input validation, default values |
| Type mismatch | `cannot concatenate str and int` | Type checking, conversions |
| Encoding | Garbled text, `UnicodeDecodeError` | Charset specification |
| Off-by-one | Wrong count, array bounds | Loop conditions, indices |

### State Issues

| Pattern | Symptoms | Check |
|---------|----------|-------|
| Race condition | Intermittent failures | Timing, shared state |
| Stale data | Old values returned | Cache, memoization |
| Mutation | Unexpected changes | Object references, copying |
| Initialization | Works after restart | Init order, lazy loading |

### Environment Issues

| Pattern | Symptoms | Check |
|---------|----------|-------|
| Config difference | Works locally, fails in prod | Environment variables |
| Dependency version | Different behavior | Package versions |
| Resource limits | OOM, timeout | Memory, connections |
| Permissions | Access denied | File/network permissions |

---

## 5. Advanced Techniques

### Logging for Production

Add strategic logging before issues occur:

```python
logger.info("Starting payment process", extra={
    "order_id": order_id,
    "amount": amount,
    "customer_id": customer_id
})

try:
    result = payment_gateway.charge(amount)
    logger.info("Payment successful", extra={
        "order_id": order_id,
        "transaction_id": result.id
    })
except PaymentError as e:
    logger.error("Payment failed", extra={
        "order_id": order_id,
        "error_code": e.code,
        "error_message": str(e)
    }, exc_info=True)
    raise
```

### Time Travel Debugging

For intermittent bugs:
1. Enable verbose logging temporarily
2. Wait for occurrence
3. Analyze logs around failure time
4. Correlate with system events

### Bisect for Regressions

Git bisect automates binary search:

```bash
git bisect start
git bisect bad HEAD          # Current is broken
git bisect good v1.2.0       # This version worked
# Git checks out middle commit
# Test and mark:
git bisect bad   # or
git bisect good
# Repeat until found
git bisect reset
```

---

## 6. After the Fix

### Verify Thoroughly

| Check | Why |
|-------|-----|
| Original issue fixed | Confirm the symptom is gone |
| Add regression test | Prevent recurrence |
| Check related areas | Fix didn't break something else |
| Test edge cases | Don't just fix the one case |

### Document and Learn

- Add comments explaining non-obvious fixes
- Update runbooks if operational
- Share learnings with team
- Consider architectural improvements

---

## Quick Reference

### Debugging Checklist

1. [ ] Can reproduce reliably?
2. [ ] Symptoms documented?
3. [ ] Recent changes reviewed?
4. [ ] Logs/errors examined?
5. [ ] Hypothesis formed?
6. [ ] Minimal reproduction created?
7. [ ] Root cause identified (not just symptom)?
8. [ ] Fix verified?
9. [ ] Regression test added?

### Quick Wins

- Check the obvious first (typos, config, recent changes)
- Read the actual error message
- Search codebase for error text
- Check if it works in different environment
- Ask: "What changed?"

Debug systematically. Document your journey. Fix root causes, not symptoms.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

