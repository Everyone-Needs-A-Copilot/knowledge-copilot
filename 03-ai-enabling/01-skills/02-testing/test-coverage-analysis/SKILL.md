---
last_updated: 2026-02-25
status: active
name: test-coverage-analysis
description: Test coverage strategy - behavior coverage over line coverage, meaningful metrics. Use when analyzing or improving test coverage.
triggers:
  files: ["**/coverage/**", "**/.nyc_output/**", "**/htmlcov/**", "**/*.lcov", "**/coverage.xml", "**/pytest.ini", "**/jest.config.*"]
  keywords: ["test coverage", "code coverage", "line coverage", "branch coverage", "coverage report", "coverage analysis", "coverage gaps", "mutation testing"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides meaningful test coverage analysis. The goal is confidence in code quality through behavior-focused coverage, not vanity metrics from line counting.

The user provides coverage analysis requirements: a coverage report to interpret, coverage gaps to address, or coverage strategy to design. They may include context about codebase risk, team policies, or CI requirements.

## Coverage Philosophy

**Coverage measures what code executes, not what code works.**

High coverage with poor assertions provides false confidence:
```python
# 100% line coverage, 0% confidence
def calculate_discount(price, percentage):
    return price * (1 - percentage / 100)

def test_calculate_discount():
    calculate_discount(100, 10)  # No assertion!
```

**Behavior coverage** matters more:
```python
# 100% behavior coverage
def test_discount_reduces_price():
    assert calculate_discount(100, 10) == 90

def test_zero_discount_returns_original():
    assert calculate_discount(100, 0) == 100

def test_hundred_percent_discount_returns_zero():
    assert calculate_discount(100, 100) == 0
```


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Coverage Types

### Line Coverage

What it measures: Lines of code executed by tests.

| Strength | Weakness |
|----------|----------|
| Easy to understand | Doesn't verify correctness |
| Universal tool support | Ignores assertions |
| Good baseline metric | Misses edge cases |

### Branch Coverage

What it measures: Decision branches (if/else, ternary, etc.) taken.

| Strength | Weakness |
|----------|----------|
| Catches untested paths | Complex to interpret |
| Better than line coverage | Still ignores assertions |
| Reveals hidden conditions | May miss compound conditions |

**Example:**
```python
def process_payment(amount, is_premium):
    if amount > 100 and is_premium:   # 4 branches
        return apply_discount(amount)
    return amount

# Branch coverage requires:
# 1. amount > 100 AND is_premium = true  → discount path
# 2. amount > 100 AND is_premium = false → no discount
# 3. amount <= 100 AND is_premium = true  → no discount
# 4. amount <= 100 AND is_premium = false → no discount
```

### Path Coverage

What it measures: All possible execution paths through code.

| Strength | Weakness |
|----------|----------|
| Most thorough | Combinatorially explosive |
| Finds complex bugs | Often impractical |
| Reveals state interactions | Tool support limited |

### Behavior Coverage (Recommended)

What it measures: Behaviors/scenarios tested per requirement.

| Strength | Weakness |
|----------|----------|
| Tied to requirements | Requires manual tracking |
| Meaningful confidence | No automatic tools |
| Catches missing tests | Subjective definition |

## Coverage Targets by Code Type

### Recommended Targets

| Code Category | Line | Branch | Behavior | Rationale |
|--------------|------|--------|----------|-----------|
| Payment/financial | 95% | 90% | 100% | Risk: monetary loss |
| Authentication | 90% | 85% | 100% | Risk: security breach |
| Core business logic | 85% | 80% | 95% | Risk: functional bugs |
| API endpoints | 80% | 75% | 90% | Risk: integration issues |
| Utilities/helpers | 80% | 70% | 85% | Risk: widespread impact |
| UI components | 60% | 50% | 70% | Risk: UX issues |
| Configuration | 50% | 40% | 60% | Risk: startup failures |
| Admin tools | 40% | 30% | 50% | Risk: low user impact |

### Coverage by Risk Matrix

| Risk | Probability | Target Coverage |
|------|-------------|-----------------|
| Critical | High | 95%+ with mutation testing |
| Critical | Low | 90%+ |
| High | High | 85%+ |
| High | Low | 80%+ |
| Medium | Any | 70%+ |
| Low | Any | 50%+ |

## Analyzing Coverage Reports

### Identifying Meaningful Gaps

**High-priority gaps:**
```
src/services/payment.ts
  Lines: 92% (uncovered: error handling)  ← FIX THIS
  Branches: 78% (uncovered: retry logic)  ← FIX THIS

src/utils/format.ts
  Lines: 85% (uncovered: edge cases)      ← REVIEW
```

**Low-priority gaps:**
```
src/config/constants.ts
  Lines: 45% (uncovered: unused exports)  ← IGNORE

src/types/index.ts
  Lines: 0% (type definitions only)       ← IGNORE
```

### Gap Analysis Checklist

| Gap Type | Priority | Action |
|----------|----------|--------|
| Error handling untested | High | Add error path tests |
| Boundary conditions missed | High | Add boundary tests |
| Race conditions untested | High | Add async tests |
| Logging statements | Low | Ignore or exclude |
| Configuration loading | Medium | Smoke test only |
| Third-party wrapper | Low | Integration test |

### Reading Coverage Reports Effectively

**HTML Report Analysis:**
```
File                    | Lines  | Branches | Functions |
------------------------|--------|----------|-----------|
payment-processor.ts    | 92.5%  | 87.3%    | 100%      | ← Good
order-calculator.ts     | 78.2%  | 65.4%    | 90%       | ← Needs work
email-service.ts        | 45.1%  | 32.8%    | 60%       | ← Investigate
```

**Priority investigation:**
1. Low branch coverage with high line coverage → missing edge cases
2. Low function coverage → untested entry points
3. High coverage but known bugs → assertions missing

## Improving Coverage Meaningfully

### Strategy: Behavior-First

1. **List behaviors** that should be tested
2. **Map to tests** that verify each behavior
3. **Identify gaps** in behavior coverage
4. **Write tests** for uncovered behaviors
5. **Verify coverage** improves as byproduct

### Finding Missing Behaviors

**Requirement:**
> Users can apply discount codes to orders

**Behaviors to test:**
- [ ] Valid code reduces order total
- [ ] Invalid code shows error
- [ ] Expired code rejected
- [ ] Code can only be used once
- [ ] Minimum order value enforced
- [ ] Maximum discount capped

**Coverage gap = missing behavior test**

### Writing Tests for Coverage Gaps

**Coverage report shows:**
```
Line 45-52 uncovered:
  if (order.total < minimumOrderValue) {
    throw new ValidationError("Order too small for discount")
  }
```

**Add meaningful test:**
```python
def test_discount_rejected_when_order_below_minimum():
    order = Order(total=10)
    discount = Discount(code="SAVE10", minimum=50)

    with pytest.raises(ValidationError) as exc:
        order.apply_discount(discount)

    assert "too small" in str(exc.value)
    assert order.total == 10  # Unchanged
```

## Mutation Testing

### What is Mutation Testing

Mutation testing verifies your tests catch bugs by:
1. Making small code changes (mutations)
2. Running tests against mutated code
3. Tests should fail (catch the mutation)
4. If tests pass, you have a gap

### Mutation Types

| Mutation | Original | Mutated | Tests Should |
|----------|----------|---------|--------------|
| Boundary | `x >= 10` | `x > 10` | Catch boundary bug |
| Operator | `a + b` | `a - b` | Catch wrong operator |
| Constant | `return 0` | `return 1` | Catch wrong value |
| Negation | `if (valid)` | `if (!valid)` | Catch inverted logic |
| Removal | `doSomething()` | `` | Catch missing effect |

### Running Mutation Tests

**Python (mutmut):**
```bash
mutmut run --paths-to-mutate=src/
mutmut results
mutmut show <id>
```

**JavaScript (Stryker):**
```bash
npx stryker run
# View report in reports/mutation/html
```

### Interpreting Mutation Score

| Score | Meaning | Action |
|-------|---------|--------|
| >90% | Excellent | Maintain |
| 80-90% | Good | Target improvements |
| 70-80% | Adequate | Review critical paths |
| <70% | Concerning | Prioritize coverage |

**Example report:**
```
File                    | Mutations | Killed | Survived | Score |
------------------------|-----------|--------|----------|-------|
payment-processor.ts    | 45        | 43     | 2        | 95.6% |
order-calculator.ts     | 32        | 24     | 8        | 75.0% | ← Focus
```

## Coverage Anti-Patterns

### Gaming Metrics

**Bad: Coverage without assertions**
```python
def test_process_order():
    process_order(order)  # 100% line coverage, 0% behavior coverage
```

**Good: Meaningful assertions**
```python
def test_process_order_creates_invoice():
    invoice = process_order(order)
    assert invoice.total == order.total
    assert invoice.status == "pending"
```

### Excluding Wrong Code

**Bad: Excluding to hit target**
```javascript
/* istanbul ignore next */
function complexBusinessLogic() {  // ← WRONG to exclude
  // Critical code hidden from coverage
}
```

**Good: Excluding appropriately**
```javascript
/* istanbul ignore next - debug helper */
function debugDump() {  // ← OK to exclude
  console.log(JSON.stringify(this, null, 2))
}
```

### Valid Exclusions

| Exclude | Reason |
|---------|--------|
| Debug helpers | Not production code |
| Type guards | Runtime type checks |
| Error formatting | Display logic only |
| Feature flags | Environment-specific |
| Abstract methods | Not directly callable |

### Invalid Exclusions

| Don't Exclude | Reason |
|---------------|--------|
| Error handling | Critical for reliability |
| Edge cases | Where bugs hide |
| Complex logic | High risk code |
| Business rules | Core functionality |

## Quick Reference

### Coverage Analysis Workflow

```
1. Run coverage: npm test -- --coverage
2. Review report: open coverage/lcov-report/index.html
3. Sort by lowest coverage
4. For each file:
   - Is it high-risk code?
   - What behaviors are untested?
   - Write behavior tests
5. Re-run coverage
6. Run mutation testing on critical files
```

### Coverage Tool Commands

**JavaScript (Jest):**
```bash
jest --coverage
jest --coverage --coverageReporters="text-summary"
jest --collectCoverageFrom="src/**/*.ts"
```

**Python (pytest-cov):**
```bash
pytest --cov=src --cov-report=html
pytest --cov=src --cov-report=term-missing
pytest --cov-fail-under=80
```

**Go:**
```bash
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Healthy Coverage Indicators

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Line coverage (critical) | >90% | 80-90% | <80% |
| Line coverage (overall) | >75% | 60-75% | <60% |
| Branch coverage | >70% | 55-70% | <55% |
| Mutation score | >80% | 65-80% | <65% |
| Coverage trend | Stable/up | Declining | Declining fast |

## Summary

Effective test coverage is about **confidence**, not metrics:

1. **Behavior coverage** over line coverage
2. **Risk-based targets** not universal minimums
3. **Meaningful gaps** are untested behaviors, not uncovered lines
4. **Mutation testing** validates test quality
5. **Trend over time** matters more than absolute number
6. **Quality assertions** make coverage meaningful


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

