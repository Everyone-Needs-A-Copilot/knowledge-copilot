---
last_updated: 2026-02-25
status: active
name: regression-strategy
description: Regression testing strategy - prevent reintroduced bugs, prioritize test selection, optimize test suites. Use when maintaining test coverage over time.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*", "**/ci/**", "**/.github/workflows/**"]
  keywords: ["regression test", "regression suite", "test selection", "test prioritization", "smoke test", "sanity test", "test maintenance"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides regression testing strategy to prevent reintroduced bugs while maintaining test suite efficiency. Balance thoroughness with speed through smart test selection and prioritization.

The user provides testing requirements: a growing test suite to optimize, a CI pipeline running too slowly, or a strategy for regression test selection. They may include context about codebase size, team size, or release frequency.

## What is Regression Testing

**Regression = "going backward"**

Regression testing verifies that:
- Fixed bugs stay fixed
- Working features continue working
- New changes don't break existing functionality

**Without regression testing:**
```
Week 1: Fix login bug → Works!
Week 2: Add new feature → Login broken again
Week 3: Discover login bug in production → :(
```

**With regression testing:**
```
Week 1: Fix login bug → Add regression test
Week 2: Add new feature → Regression test fails → Fix immediately
Week 3: Deploy with confidence → :)
```


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Regression Test Types

### Test Suite Levels

| Level | Purpose | When to Run | Typical Duration |
|-------|---------|-------------|------------------|
| Smoke | App starts, critical paths work | Every commit | < 5 minutes |
| Sanity | Core features work | Every PR | 5-15 minutes |
| Full Regression | Everything works | Nightly/release | 30+ minutes |

### Smoke Tests

Minimal tests that verify the system is testable:

```python
class SmokeTests:
    def test_app_starts(self):
        response = client.get("/health")
        assert response.status == 200

    def test_database_connected(self):
        result = db.execute("SELECT 1")
        assert result is not None

    def test_login_page_loads(self):
        response = client.get("/login")
        assert response.status == 200
        assert "Login" in response.text

    def test_api_responds(self):
        response = client.get("/api/v1/status")
        assert response.status == 200
```

### Sanity Tests

Core functionality tests for confidence:

```python
class SanityTests:
    def test_user_can_login(self):
        response = login(valid_credentials)
        assert response.status == 200
        assert "session" in response.cookies

    def test_user_can_create_order(self):
        login(valid_credentials)
        response = create_order(valid_order)
        assert response.status == 201

    def test_user_can_view_orders(self):
        login(valid_credentials)
        response = get_orders()
        assert response.status == 200
        assert isinstance(response.json(), list)

    def test_payment_processing(self):
        order = create_test_order()
        response = process_payment(order, test_card)
        assert response.json()["status"] == "succeeded"
```

### Full Regression Suite

Comprehensive coverage:

```
tests/
  regression/
    test_authentication.py      # All auth scenarios
    test_user_management.py     # CRUD operations
    test_orders.py              # Order lifecycle
    test_payments.py            # Payment processing
    test_notifications.py       # Email/SMS
    test_reporting.py           # Reports generation
    test_admin.py               # Admin functions
    test_api_v1.py              # API endpoints
    test_integrations.py        # Third-party integrations
```

## Test Selection Strategies

### Risk-Based Selection

Prioritize tests based on risk:

| Risk Factor | Weight | Example |
|-------------|--------|---------|
| Changed code | High | Tests for modified files |
| Bug history | High | Areas with past bugs |
| User impact | High | Revenue-critical paths |
| Complexity | Medium | Complex business logic |
| Integration points | Medium | External service calls |
| UI changes | Lower | Visual regressions |

```python
def select_regression_tests(changed_files, bug_history, test_suite):
    selected = set()

    # Always run smoke tests
    selected.update(test_suite.smoke_tests)

    # Tests for changed code
    for file in changed_files:
        selected.update(test_suite.tests_for_file(file))

    # Tests for historically buggy areas
    for area in bug_history.recent_bug_areas():
        selected.update(test_suite.tests_for_area(area))

    # Core business path tests
    selected.update(test_suite.critical_path_tests)

    return selected
```

### Change-Based Selection

Run tests related to changed code:

```yaml
# CI configuration example
test-selection:
  rules:
    - paths: ["src/auth/**"]
      tests: ["tests/auth/**", "tests/integration/login.py"]

    - paths: ["src/payments/**"]
      tests: ["tests/payments/**", "tests/e2e/checkout.py"]

    - paths: ["src/api/**"]
      tests: ["tests/api/**"]

    - paths: ["**"]  # Any other change
      tests: ["tests/smoke/**"]
```

### Time-Based Selection

Different test suites for different triggers:

| Trigger | Test Suite | Rationale |
|---------|------------|-----------|
| Every commit | Smoke (< 2 min) | Fast feedback |
| Every PR | Sanity (< 15 min) | Catch issues before merge |
| Merge to main | Full related (< 30 min) | Comprehensive check |
| Nightly | Full regression (1+ hour) | Complete coverage |
| Pre-release | Full + E2E + perf | Release confidence |

## Test Prioritization

### Prioritization Factors

```python
def calculate_test_priority(test):
    score = 0

    # Recent failure history (most important)
    if test.failed_recently:
        score += 100

    # Covers frequently changed code
    score += test.change_frequency * 10

    # Covers critical functionality
    if test.covers_critical_path:
        score += 50

    # Execution time (prefer faster)
    score -= test.avg_duration_seconds

    # Bug detection history
    score += test.bugs_caught * 5

    return score

def prioritize_tests(tests):
    return sorted(tests, key=calculate_test_priority, reverse=True)
```

### Fail-Fast Ordering

Run tests most likely to fail first:

```python
class TestOrdering:
    def order_tests(self, tests):
        # Recently failed tests first
        recently_failed = [t for t in tests if t.failed_in_last_5_runs]

        # Tests for changed files second
        changed_file_tests = [t for t in tests if t.covers_changed_file]

        # Fast tests third
        fast_tests = [t for t in tests if t.duration < 1.0]

        # Everything else
        remaining = [t for t in tests if t not in
                     recently_failed + changed_file_tests + fast_tests]

        return recently_failed + changed_file_tests + fast_tests + remaining
```

## Regression Test Maintenance

### Test Suite Health Metrics

| Metric | Healthy | Warning | Action |
|--------|---------|---------|--------|
| Flaky rate | < 1% | > 3% | Fix or quarantine |
| Suite duration | < 15 min | > 30 min | Optimize or parallelize |
| Coverage | > 80% | < 60% | Add tests |
| Test/code ratio | 1:1 | < 0.5:1 | Review coverage |

### Dealing with Flaky Tests

```python
# Quarantine flaky tests
@pytest.mark.flaky
@pytest.mark.skip(reason="Flaky: investigating race condition")
def test_concurrent_updates():
    ...

# Track flaky history
class FlakyTestTracker:
    def record_result(self, test_name, passed, run_id):
        self.results.append({
            "test": test_name,
            "passed": passed,
            "run_id": run_id,
            "timestamp": datetime.now()
        })

    def get_flaky_tests(self, threshold=0.1):
        """Tests that fail more than threshold of runs."""
        return [
            test for test, results in self.aggregate_results().items()
            if results["fail_rate"] > threshold
        ]
```

### Test Retirement Criteria

| Condition | Action |
|-----------|--------|
| Tests code that no longer exists | Delete test |
| Duplicate of another test | Merge or delete |
| Never fails (zero bugs found) | Review value, possibly delete |
| Tests third-party code | Delete (not your responsibility) |
| Consistently flaky, can't fix | Quarantine or delete |

### Keeping Tests Current

```python
# Regular test audit
def audit_test_suite():
    report = {
        "total_tests": 0,
        "orphaned_tests": [],      # Test files without source
        "slow_tests": [],          # Tests > 5 seconds
        "flaky_tests": [],         # > 5% failure rate
        "low_value_tests": [],     # Never caught bugs
        "duplicate_tests": [],     # Testing same thing
    }

    for test in all_tests:
        report["total_tests"] += 1

        if not test.source_file_exists():
            report["orphaned_tests"].append(test)

        if test.avg_duration > 5:
            report["slow_tests"].append(test)

        if test.flaky_rate > 0.05:
            report["flaky_tests"].append(test)

    return report
```

## CI/CD Integration

### Pipeline Configuration

```yaml
# .github/workflows/test.yml
name: Test Pipeline

on:
  push:
    branches: [main]
  pull_request:

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Smoke Tests
        run: pytest tests/smoke -v --timeout=60

  sanity:
    needs: smoke
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Sanity Tests
        run: pytest tests/sanity -v --timeout=300

  regression:
    needs: sanity
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Full Regression
        run: pytest tests/regression -v --timeout=1800

  nightly:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - name: Full Suite + E2E
        run: |
          pytest tests/ -v
          pytest tests/e2e -v --timeout=3600
```

### Parallelization Strategy

```yaml
regression:
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
  steps:
    - name: Run Shard
      run: |
        pytest tests/regression \
          --shard-id=${{ matrix.shard }} \
          --num-shards=4
```

### Test Result Tracking

```python
# Track regression test results over time
class RegressionMetrics:
    def record_run(self, run_data):
        self.db.insert({
            "run_id": run_data["id"],
            "timestamp": datetime.now(),
            "total_tests": run_data["total"],
            "passed": run_data["passed"],
            "failed": run_data["failed"],
            "skipped": run_data["skipped"],
            "duration": run_data["duration"],
            "commit": run_data["commit"],
        })

    def get_trends(self, days=30):
        return {
            "pass_rate_trend": self.calculate_pass_rate_trend(days),
            "duration_trend": self.calculate_duration_trend(days),
            "flaky_tests": self.identify_flaky_tests(days),
            "slowest_tests": self.get_slowest_tests(days),
        }
```

## Regression Test Patterns

### Bug Fix Regression Test

```python
def test_issue_1234_login_with_special_characters():
    """
    Regression test for issue #1234.

    Bug: Users with '+' in email couldn't login.
    Fix: Properly URL-encode email in auth request.
    """
    # Arrange
    user = UserFactory.create(email="user+test@example.com")

    # Act
    response = login(email="user+test@example.com", password="valid")

    # Assert
    assert response.status == 200
    assert "session" in response.cookies
```

### Feature Regression Test

```python
class TestCheckoutRegression:
    """Regression tests for checkout flow."""

    def test_basic_checkout_flow(self):
        """Happy path checkout continues working."""
        # Add to cart
        add_to_cart(product_id=1, quantity=1)

        # Checkout
        response = checkout(payment=valid_card)

        assert response.status == 200
        assert response.json()["order_id"] is not None

    def test_checkout_with_discount(self):
        """Discount codes continue working."""
        add_to_cart(product_id=1, quantity=1)
        apply_discount("SAVE10")

        response = checkout(payment=valid_card)

        assert response.json()["discount_applied"] == True
        assert response.json()["total"] < original_price

    def test_checkout_with_multiple_items(self):
        """Multiple items checkout continues working."""
        add_to_cart(product_id=1, quantity=2)
        add_to_cart(product_id=2, quantity=1)

        response = checkout(payment=valid_card)

        assert response.json()["items_count"] == 3
```

## Quick Reference

### Regression Strategy Checklist

- [ ] Smoke tests run on every commit
- [ ] Sanity tests run on every PR
- [ ] Full regression runs nightly
- [ ] Tests prioritized by risk
- [ ] Flaky tests tracked and fixed
- [ ] Test results trending over time
- [ ] Orphaned tests identified and removed

### Test Selection Matrix

| Change Type | Smoke | Sanity | Related | Full |
|-------------|-------|--------|---------|------|
| Config only | ✓ | | | |
| Single file | ✓ | ✓ | ✓ | |
| Feature branch | ✓ | ✓ | ✓ | |
| Merge to main | ✓ | ✓ | ✓ | ✓ |
| Release | ✓ | ✓ | ✓ | ✓ |

### Regression Test Health

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Suite takes too long | Too many E2E tests | Shift to unit tests |
| Frequent failures | Flaky tests | Fix or quarantine |
| Bugs slip through | Gaps in coverage | Add targeted tests |
| Tests break often | Brittle tests | Improve isolation |

## Summary

Effective regression testing prevents bugs from returning:

1. **Layer your tests** - Smoke, sanity, full regression
2. **Prioritize by risk** - Changed code, bug history, critical paths
3. **Select smartly** - Not every test on every change
4. **Run fast tests first** - Fail fast, fix fast
5. **Track health** - Flaky rate, duration, coverage
6. **Maintain actively** - Remove obsolete, fix flaky
7. **Integrate with CI** - Automate the strategy
8. **Add tests for fixes** - Every bug fix gets a regression test


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

