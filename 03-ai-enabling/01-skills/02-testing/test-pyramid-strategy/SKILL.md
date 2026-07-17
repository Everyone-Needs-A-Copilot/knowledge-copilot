---
last_updated: 2026-02-25
status: active
name: test-pyramid-strategy
description: Test pyramid design strategy - more unit tests, fewer integration tests, minimal E2E. Use when designing test architecture.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*", "**/pytest.ini", "**/jest.config.*"]
  keywords: ["test pyramid", "test strategy", "unit test ratio", "test distribution", "testing architecture", "test balance", "test planning"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides strategic test distribution across the testing pyramid. The goal is fast feedback loops through many unit tests, moderate integration coverage, and selective E2E tests for critical paths.

The user provides test planning requirements: a new feature needing test strategy, an existing codebase needing test rebalancing, or CI/CD pipeline optimization. They may include context about risk profile, time constraints, or team capabilities.

## The Test Pyramid Principle

The pyramid shape reflects optimal test distribution:

```
        /\
       /E2E\      5-10% - Critical user journeys only
      /------\
     /  INT   \   15-25% - Component boundaries
    /----------\
   /    UNIT    \ 70-80% - Business logic, utilities
  /--------------\
```

**Why this shape works:**
- Unit tests: milliseconds, isolated, many
- Integration tests: seconds, boundaries, moderate
- E2E tests: minutes, full stack, few

**The pyramid inverted (anti-pattern):**
- Slow CI pipelines (30+ minutes)
- Flaky tests (environment-dependent)
- Expensive maintenance
- Late feedback on failures


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Determining Test Distribution

### By Risk Profile

| Risk Level | Unit | Integration | E2E | Example |
|------------|------|-------------|-----|---------|
| Critical (payment, auth) | 85% | 10% | 5% | Payment processor |
| High (core features) | 75% | 20% | 5% | Order management |
| Medium (standard) | 70% | 20% | 10% | User profiles |
| Low (admin tools) | 60% | 30% | 10% | Internal dashboards |

### By Code Type

| Code Type | Primary Test | Secondary | Rationale |
|-----------|--------------|-----------|-----------|
| Pure functions | Unit (90%) | - | No dependencies |
| Domain logic | Unit (80%) | Integration (20%) | Core value |
| Service layer | Integration (60%) | Unit (40%) | Coordination |
| Controllers | Integration (70%) | E2E (30%) | Request/response |
| UI components | Integration (60%) | E2E (40%) | Visual, interactive |

## Unit Test Guidelines

### What to Unit Test

**Always unit test:**
- Calculations and transformations
- Business rules and validation
- State machines and transitions
- Parsing and serialization
- Edge cases and error handling

**Example ratio:**
```
src/
  utils/
    calculate-tax.ts        → 15 unit tests
    validate-email.ts       → 8 unit tests
    format-currency.ts      → 6 unit tests
  services/
    order-service.ts        → 10 unit tests + 3 integration
    payment-service.ts      → 12 unit tests + 5 integration
```

### Unit Test Characteristics

| Characteristic | Target | Why |
|---------------|--------|-----|
| Execution time | <10ms each | Run on every save |
| Dependencies | Zero external | Fast, reliable |
| Setup | <5 lines | Readable |
| Assertions | 1-3 per test | Clear failures |

### Unit Test Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Testing framework code | Waste of time | Trust the framework |
| Testing getters/setters | No logic to test | Skip trivial accessors |
| Extensive mocking | Brittle, slow | Use real objects |
| Testing implementation | Breaks on refactor | Test behavior |

## Integration Test Guidelines

### What to Integration Test

**Focus on:**
- API endpoints (request → response)
- Database operations (CRUD)
- External service interactions (mocked)
- Component boundaries
- Data transformation pipelines

**Skip:**
- Internal method calls
- Duplicate coverage of unit tests
- Configuration loading
- Framework-provided functionality

### Integration Test Characteristics

| Characteristic | Target | Why |
|---------------|--------|-----|
| Execution time | <500ms each | Tolerable in CI |
| Dependencies | Database, services | Real boundaries |
| Setup | Test fixtures | Realistic data |
| Scope | 2-3 components | Boundary testing |

### Integration Test Patterns

```
# Test API endpoint
test "POST /orders creates order and sends email":
  # Arrange - realistic fixture
  user = fixtures.authenticated_user()
  product = fixtures.available_product()

  # Act - through real API
  response = client.post("/orders", {
    product_id: product.id,
    quantity: 2
  })

  # Assert - multiple system effects
  assert response.status == 201
  assert database.orders.count() == 1
  assert email_service.sent_to(user.email)
```

## E2E Test Guidelines

### What to E2E Test

**Test only:**
- Critical user journeys (login, purchase, signup)
- Revenue-generating paths
- Compliance-required flows
- Smoke tests (app loads, key pages render)

**Never E2E test:**
- Edge cases (use unit tests)
- Error handling (use integration tests)
- All feature variations (combinatorial explosion)
- Internal admin flows (low risk)

### E2E Test Characteristics

| Characteristic | Target | Why |
|---------------|--------|-----|
| Execution time | <30s each | Tolerable nightly |
| Dependencies | Full stack | Production-like |
| Count | 5-20 tests | Critical paths only |
| Flakiness | <1% | Reliable signal |

### Critical Path Selection

| User Journey | Priority | E2E Coverage |
|--------------|----------|--------------|
| Authentication | P0 | Login, logout, password reset |
| Purchase | P0 | Cart, checkout, confirmation |
| Signup | P1 | Registration, verification |
| Search | P1 | Basic search, results display |
| Profile | P2 | None (low risk) |
| Settings | P2 | None (low risk) |

## Rebalancing an Existing Test Suite

### Assessment Checklist

| Metric | Healthy | Warning | Action |
|--------|---------|---------|--------|
| CI time | <10 min | >20 min | Reduce E2E |
| Flaky rate | <1% | >5% | Fix or remove |
| Unit ratio | >60% | <40% | Add unit tests |
| E2E ratio | <15% | >30% | Convert to integration |

### Conversion Strategies

**E2E → Integration:**
```
# Before: Full browser E2E
test "user can update profile":
  browser.login(user)
  browser.visit("/profile")
  browser.fill("name", "New Name")
  browser.click("Save")
  assert browser.has_text("Profile updated")

# After: API integration
test "profile update API":
  response = client.patch("/profile", {name: "New Name"}, auth: user)
  assert response.status == 200
  assert database.users.find(user.id).name == "New Name"
```

**Integration → Unit:**
```
# Before: Database integration
test "tax calculation":
  product = database.create_product(price: 100)
  order = database.create_order(product_id: product.id)
  assert order.tax == 7.5

# After: Pure unit
test "tax calculation":
  tax = calculate_tax(price: 100, rate: 0.075)
  assert tax == 7.5
```

## CI/CD Optimization

### Test Execution Strategy

| Stage | Tests | Trigger | Time Budget |
|-------|-------|---------|-------------|
| Pre-commit | Lint, unit | Every save | <30s |
| PR build | Unit + integration | Every push | <10 min |
| Main build | All tests | Merge | <20 min |
| Nightly | E2E + perf | Scheduled | <1 hour |

### Parallelization Strategy

```
# Optimal pipeline
parallel:
  - job: unit-tests        # 2 min
    shards: 4
  - job: integration-tests  # 5 min
    shards: 2

sequential:
  - job: e2e-tests          # 10 min (after unit/integration pass)
    critical-only: true
```

## Quick Reference

### Test Type Selection Matrix

| Question | Yes → | No → |
|----------|-------|------|
| Does it have business logic? | Unit test | Skip or integration |
| Does it cross boundaries? | Integration test | Unit test |
| Is it a critical user path? | E2E test | Integration test |
| Does it have external deps? | Mock + integration | Unit test |
| Is it UI-heavy? | Integration + E2E | Unit test |

### Healthy Test Suite Indicators

| Indicator | Target |
|-----------|--------|
| Unit test count | 100+ per service |
| Integration test count | 20-50 per service |
| E2E test count | 5-15 per application |
| CI pipeline time | <15 minutes |
| Flaky test rate | <1% |
| Coverage (critical paths) | >90% |
| Coverage (overall) | >70% |

## Summary

The test pyramid is about **fast feedback** and **risk management**:

1. **Many unit tests** - Fast, cheap, thorough coverage of logic
2. **Some integration tests** - Verify component boundaries work
3. **Few E2E tests** - Confirm critical user journeys
4. **Optimize for speed** - Tests that run get trusted
5. **Focus on risk** - More tests where failures hurt most


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

