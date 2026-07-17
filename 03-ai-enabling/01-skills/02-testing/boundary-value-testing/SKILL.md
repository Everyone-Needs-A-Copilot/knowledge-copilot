---
last_updated: 2026-02-25
status: active
name: boundary-value-testing
description: Boundary value analysis - test min, max, just-inside, just-outside values. Use when testing numeric limits, ranges, and edge cases.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*"]
  keywords: ["boundary test", "edge case", "min max", "off-by-one", "range test", "limit test", "boundary value", "equivalence partition"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides boundary value testing, a technique that finds bugs at the edges of valid input ranges. Most bugs cluster at boundaries - test them systematically.

The user provides testing requirements: a function with numeric parameters, a validation rule with limits, or an existing test suite to strengthen. They may include context about input ranges, business rules, or known edge cases.

## Why Boundaries Matter

**Bugs cluster at edges:**
- Off-by-one errors (`<` vs `<=`)
- Integer overflow at limits
- Empty collection handling
- First/last element edge cases
- Timezone boundaries

**Example: Common off-by-one bug**
```python
# Bug: Should be >= 18, written as > 18
def can_vote(age):
    return age > 18  # Bug: 18-year-olds can't vote

# Without boundary test: passes
test_can_vote(25)  # Returns True ✓

# With boundary test: catches bug
test_can_vote(18)  # Returns False ✗ (should be True)
```


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Boundary Value Analysis (BVA)

### Core Technique

For any boundary B, test these values:

| Test Point | Value | Purpose |
|------------|-------|---------|
| Below boundary | B - 1 | Just outside valid range |
| At boundary | B | Boundary itself |
| Above boundary | B + 1 | Just inside valid range |

### For a Range [Min, Max]

Test these 6 points minimum:

```
Invalid ← | → Valid ← | → Invalid
          Min       Max
    ↓     ↓         ↓     ↓
  Min-1  Min       Max   Max+1
```

| Test Point | Value | Expected |
|------------|-------|----------|
| Below minimum | Min - 1 | Invalid |
| At minimum | Min | Valid |
| Above minimum | Min + 1 | Valid |
| Below maximum | Max - 1 | Valid |
| At maximum | Max | Valid |
| Above maximum | Max + 1 | Invalid |

### Example: Age Validation (18-65)

```python
def test_age_boundaries():
    # Below minimum
    assert is_valid_age(17) == False   # Just outside

    # At minimum
    assert is_valid_age(18) == True    # Boundary

    # Above minimum
    assert is_valid_age(19) == True    # Just inside

    # Below maximum
    assert is_valid_age(64) == True    # Just inside

    # At maximum
    assert is_valid_age(65) == True    # Boundary

    # Above maximum
    assert is_valid_age(66) == False   # Just outside
```

## Equivalence Partitioning

### Combined with BVA

Group inputs into equivalence classes, then test boundaries of each:

```
Quantity discount rules:
  0-9:   No discount
  10-49: 10% discount
  50+:   20% discount
```

**Equivalence classes:**
1. Invalid (negative)
2. No discount (0-9)
3. Small discount (10-49)
4. Large discount (50+)

**Boundary tests:**
```python
def test_discount_boundaries():
    # Class boundary: invalid → no discount
    assert discount(-1) == "invalid"
    assert discount(0) == 0

    # Class boundary: no discount → small discount
    assert discount(9) == 0      # Just inside no-discount
    assert discount(10) == 10    # Boundary
    assert discount(11) == 10    # Just inside small

    # Class boundary: small discount → large discount
    assert discount(49) == 10    # Just inside small
    assert discount(50) == 20    # Boundary
    assert discount(51) == 20    # Just inside large
```

## Common Boundary Scenarios

### Numeric Boundaries

| Scenario | Test Values |
|----------|-------------|
| Positive only | -1, 0, 1 |
| Non-negative | -1, 0, 1 |
| Percentage (0-100) | -1, 0, 1, 99, 100, 101 |
| Integer range | MIN_INT, MIN_INT+1, MAX_INT-1, MAX_INT |
| Floating point | 0.0, smallest positive, epsilon differences |

**Example: Percentage validation**
```python
def test_percentage_boundaries():
    # Below range
    assert validate_percent(-0.01) == False

    # At minimum
    assert validate_percent(0) == True

    # Just above minimum
    assert validate_percent(0.01) == True

    # Just below maximum
    assert validate_percent(99.99) == True

    # At maximum
    assert validate_percent(100) == True

    # Above range
    assert validate_percent(100.01) == False
```

### Collection Boundaries

| Scenario | Test Cases |
|----------|------------|
| Array/List | Empty [], single [x], two [x,y] |
| Required items | 0, 1, minimum, minimum-1 |
| Maximum items | max-1, max, max+1 |
| Index access | -1, 0, 1, length-1, length |

**Example: Array processing**
```python
def test_array_boundaries():
    # Empty array
    assert process([]) == []

    # Single element
    assert process([1]) == [1]

    # Two elements (minimum for comparison)
    assert process([2, 1]) == [1, 2]

    # First element access
    assert get_first([1, 2, 3]) == 1

    # Last element access
    assert get_last([1, 2, 3]) == 3

    # Index boundaries
    assert get_at([1, 2, 3], 0) == 1    # First
    assert get_at([1, 2, 3], 2) == 3    # Last
    with pytest.raises(IndexError):
        get_at([1, 2, 3], 3)            # Out of bounds
```

### String Boundaries

| Scenario | Test Cases |
|----------|------------|
| Length limits | empty, 1 char, min length, max length, max+1 |
| Character classes | first valid, last valid, invalid adjacent |
| Trimming | leading space, trailing space, only spaces |

**Example: Username validation (3-20 chars)**
```python
def test_username_boundaries():
    # Below minimum length
    assert is_valid_username("ab") == False

    # At minimum length
    assert is_valid_username("abc") == True

    # Just above minimum
    assert is_valid_username("abcd") == True

    # Just below maximum
    assert is_valid_username("a" * 19) == True

    # At maximum length
    assert is_valid_username("a" * 20) == True

    # Above maximum length
    assert is_valid_username("a" * 21) == False

    # Empty string
    assert is_valid_username("") == False
```

### Date/Time Boundaries

| Scenario | Test Cases |
|----------|------------|
| Day of month | 0, 1, 28, 29, 30, 31, 32 |
| Month transitions | last day → first day |
| Year boundaries | Dec 31, Jan 1 |
| Leap years | Feb 28/29 in leap/non-leap years |
| Timezone changes | DST transitions, midnight UTC |

**Example: Date validation**
```python
def test_date_boundaries():
    # Month boundaries
    assert is_valid_date(2024, 1, 0) == False   # Day too low
    assert is_valid_date(2024, 1, 1) == True    # First day
    assert is_valid_date(2024, 1, 31) == True   # Last day (Jan)
    assert is_valid_date(2024, 1, 32) == False  # Day too high

    # February (non-leap year)
    assert is_valid_date(2023, 2, 28) == True
    assert is_valid_date(2023, 2, 29) == False

    # February (leap year)
    assert is_valid_date(2024, 2, 28) == True
    assert is_valid_date(2024, 2, 29) == True
    assert is_valid_date(2024, 2, 30) == False

    # Month boundaries
    assert is_valid_date(2024, 0, 15) == False   # Month too low
    assert is_valid_date(2024, 13, 15) == False  # Month too high
```

### State Boundaries

| Scenario | Test Cases |
|----------|------------|
| State transitions | valid from, valid to, invalid from, invalid to |
| Counters | 0, 1, max-1, max, overflow attempt |
| Queues | empty, single, full, overflow |

**Example: Counter with max**
```python
def test_counter_boundaries():
    counter = Counter(max=10)

    # At zero
    assert counter.value == 0
    assert counter.decrement() == False  # Can't go below 0

    # Increment to 1
    assert counter.increment() == True
    assert counter.value == 1

    # At maximum - 1
    counter.set(9)
    assert counter.increment() == True
    assert counter.value == 10

    # At maximum
    assert counter.increment() == False  # Can't exceed max
    assert counter.value == 10
```

## Advanced Boundary Techniques

### Multi-Variable Boundaries

When multiple parameters have boundaries, test combinations:

```python
# Function: calculate_shipping(weight, distance)
# Weight: 0-50 kg, Distance: 0-1000 km

def test_shipping_boundary_combinations():
    # Both at minimum
    assert calculate_shipping(0, 0) == expected_min

    # Weight min, distance max
    assert calculate_shipping(0, 1000) == expected

    # Weight max, distance min
    assert calculate_shipping(50, 0) == expected

    # Both at maximum
    assert calculate_shipping(50, 1000) == expected_max

    # One just outside, other valid
    with pytest.raises(ValueError):
        calculate_shipping(51, 500)  # Weight over
    with pytest.raises(ValueError):
        calculate_shipping(25, 1001)  # Distance over
```

### Floating Point Boundaries

Handle floating point precision carefully:

```python
import math

def test_floating_point_boundaries():
    # Use approximate equality
    assert math.isclose(calculate(0.1 + 0.2), 0.3, rel_tol=1e-9)

    # Test smallest differences
    epsilon = 1e-10
    assert is_positive(epsilon) == True
    assert is_positive(-epsilon) == False

    # Test very small values
    assert is_zero(1e-15) == True  # Treat as zero
    assert is_zero(1e-5) == False  # Not zero
```

### Robustness Testing

Extend BVA to test beyond boundaries:

| Type | Test Values |
|------|-------------|
| Normal BVA | min-1, min, min+1, max-1, max, max+1 |
| Robust BVA | min-2, min-1, min, ..., max, max+1, max+2 |
| Extreme | MIN_INT, MAX_INT, NaN, Infinity |

```python
def test_robust_boundaries():
    # Standard BVA
    assert process(0) == valid
    assert process(100) == valid

    # Extreme values
    assert process(float('inf')) == error
    assert process(float('-inf')) == error
    assert process(float('nan')) == error

    # System limits
    assert process(sys.maxsize) == error
    assert process(-sys.maxsize) == error
```

## Boundary Testing Checklist

### For Any Parameter

- [ ] What is the minimum valid value?
- [ ] What is the maximum valid value?
- [ ] What happens at min - 1?
- [ ] What happens at max + 1?
- [ ] Are there internal boundaries (thresholds)?
- [ ] What are the type limits (int overflow, string length)?

### For Collections

- [ ] Empty collection
- [ ] Single element
- [ ] Two elements (for comparisons)
- [ ] Maximum elements
- [ ] Maximum + 1 elements
- [ ] First element access
- [ ] Last element access
- [ ] Out of bounds access

### For Dates/Times

- [ ] Day boundaries (1, 28/29/30/31)
- [ ] Month boundaries (1, 12)
- [ ] Year boundaries (leap year)
- [ ] Time boundaries (0:00, 23:59)
- [ ] Timezone boundaries
- [ ] DST transitions

## Quick Reference

### BVA Test Point Selection

```
For range [A, B]:

Minimum test set (4 points):
  A-1, A, B, B+1

Standard test set (6 points):
  A-1, A, A+1, B-1, B, B+1

Robust test set (8 points):
  A-2, A-1, A, A+1, B-1, B, B+1, B+2
```

### Common Boundary Patterns

| Input Type | Typical Boundaries |
|------------|-------------------|
| Age | 0, 1, 17, 18, 64, 65, 120 |
| Percentage | 0, 1, 99, 100 |
| Quantity | 0, 1, max-1, max |
| Price | 0, 0.01, max price |
| Date | month start/end, year start/end |
| Array index | -1, 0, length-1, length |

### Boundary Test Template

```python
def test_function_boundaries():
    # Below minimum (invalid)
    assert function(MIN - 1) == expected_invalid

    # At minimum (valid)
    assert function(MIN) == expected_min

    # Just above minimum (valid)
    assert function(MIN + 1) == expected_valid

    # Typical value (valid)
    assert function(TYPICAL) == expected_typical

    # Just below maximum (valid)
    assert function(MAX - 1) == expected_valid

    # At maximum (valid)
    assert function(MAX) == expected_max

    # Above maximum (invalid)
    assert function(MAX + 1) == expected_invalid
```

## Summary

Boundary value testing finds bugs where they hide most:

1. **Always test boundaries** - min, max, and adjacent values
2. **Combine with equivalence partitioning** - test class boundaries
3. **Consider all types** - numeric, string, collection, date, state
4. **Test combinations** - multi-variable boundary interactions
5. **Handle precision** - floating point requires special care
6. **Go beyond boundaries** - robust testing catches more bugs


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

