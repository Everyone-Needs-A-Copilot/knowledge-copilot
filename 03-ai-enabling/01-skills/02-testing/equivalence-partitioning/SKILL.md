---
last_updated: 2026-02-25
status: active
name: equivalence-partitioning
description: Equivalence class testing - divide inputs into groups with same behavior, test one from each. Use when designing test cases efficiently.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*"]
  keywords: ["equivalence class", "equivalence partition", "test partition", "input class", "valid partition", "invalid partition", "test case reduction"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides equivalence partitioning, a test design technique that groups inputs into classes expected to behave the same way. Test one representative from each class to achieve thorough coverage efficiently.

The user provides testing requirements: a function with multiple input ranges, validation logic with categories, or an existing test suite to optimize. They may include context about input types, business rules, or coverage goals.

## Why Equivalence Partitioning

**The problem:** Testing every possible input is impossible.

```
Function: validate_age(age)
Possible inputs: -infinity to +infinity
Practical inputs: 0 to 150
All combinations: Still too many
```

**The solution:** Group inputs that should behave identically.

```
Age validation partitions:
  Invalid (negative): -100, -1    → Same behavior: rejected
  Invalid (too young): 0-17       → Same behavior: rejected
  Valid (adult): 18-65            → Same behavior: accepted
  Valid (senior): 66-120          → Same behavior: accepted
  Invalid (unrealistic): 121+     → Same behavior: rejected
```

**Test one from each class** instead of thousands.


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Core Technique

### Identifying Partitions

1. **Analyze the specification** - What inputs are valid/invalid?
2. **Identify ranges** - Where do behaviors change?
3. **Define classes** - Group inputs with identical behavior
4. **Select representatives** - Pick one value per class

### Partition Types

| Type | Description | Example |
|------|-------------|---------|
| Valid | Inputs system should accept | Age 18-65 |
| Invalid | Inputs system should reject | Age < 0 |
| Boundary | Edge of valid range | Age = 18 |
| Special | Unique handling | Age = 0 |

### Basic Example: Percentage Input

**Specification:** Accept percentage values 0-100.

**Partitions:**
```
Class 1: Negative numbers (-∞ to -1)   → Invalid
Class 2: Zero (0)                      → Valid (boundary)
Class 3: Valid range (1-99)            → Valid
Class 4: Maximum (100)                 → Valid (boundary)
Class 5: Over maximum (101+)           → Invalid
```

**Test cases:**
```python
def test_percentage_equivalence_classes():
    # Class 1: Negative (invalid)
    assert validate_percent(-50) == False

    # Class 2: Zero (valid boundary)
    assert validate_percent(0) == True

    # Class 3: Valid range
    assert validate_percent(50) == True

    # Class 4: Maximum (valid boundary)
    assert validate_percent(100) == True

    # Class 5: Over maximum (invalid)
    assert validate_percent(150) == False
```

## Multi-Variable Partitioning

### Two Variables: Discount Calculator

**Specification:**
- Quantity: 1-1000 items
- Customer type: Regular, Premium, VIP
- Output: Discount percentage

**Partitions:**

| Variable | Classes |
|----------|---------|
| Quantity | Invalid (0, <0), Small (1-10), Medium (11-100), Large (101-1000), Invalid (>1000) |
| Customer | Regular, Premium, VIP, Invalid |

**Combined test cases (one per class combination):**

```python
def test_discount_equivalence():
    # Regular customer, small quantity
    assert calculate_discount(qty=5, customer="regular") == 0

    # Regular customer, medium quantity
    assert calculate_discount(qty=50, customer="regular") == 5

    # Premium customer, large quantity
    assert calculate_discount(qty=500, customer="premium") == 15

    # VIP customer, medium quantity
    assert calculate_discount(qty=75, customer="vip") == 20

    # Invalid quantity
    with pytest.raises(ValueError):
        calculate_discount(qty=0, customer="regular")

    # Invalid customer type
    with pytest.raises(ValueError):
        calculate_discount(qty=10, customer="invalid")
```

### Three Variables: Shipping Calculator

**Specification:**
- Weight: 0-50 kg
- Distance: 0-1000 km
- Priority: Standard, Express, Overnight

**Partitions:**

| Variable | Classes |
|----------|---------|
| Weight | Invalid (≤0), Light (0.1-5), Medium (5.1-20), Heavy (20.1-50), Invalid (>50) |
| Distance | Invalid (≤0), Local (1-100), Regional (101-500), National (501-1000), Invalid (>1000) |
| Priority | Standard, Express, Overnight |

**Strategic test selection (not all combinations):**

```python
def test_shipping_key_combinations():
    # Light, local, standard (cheapest valid)
    assert shipping_cost(2, 50, "standard") == 5.00

    # Heavy, national, overnight (most expensive valid)
    assert shipping_cost(45, 900, "overnight") == 150.00

    # Medium, regional, express (middle case)
    assert shipping_cost(15, 300, "express") == 35.00

    # Invalid weight
    with pytest.raises(ValueError):
        shipping_cost(0, 100, "standard")

    # Invalid distance
    with pytest.raises(ValueError):
        shipping_cost(10, 1500, "standard")
```

## Weak vs Strong Equivalence Partitioning

### Weak Equivalence Testing

Test one value from each class for each variable independently.

**Minimum test cases:** max(classes per variable)

```
Weight classes: 5
Distance classes: 5
Priority classes: 3

Weak coverage: 5 test cases (covers all classes at least once)
```

**Example:**
```python
def test_weak_equivalence():
    # Each test covers multiple classes
    shipping_cost(2, 50, "standard")      # Light, Local, Standard
    shipping_cost(15, 300, "express")     # Medium, Regional, Express
    shipping_cost(45, 900, "overnight")   # Heavy, National, Overnight
    shipping_cost(0.5, 5, "standard")     # Light, Local, Standard
    shipping_cost(10, 150, "express")     # Medium, Regional, Express
```

### Strong Equivalence Testing

Test every combination of classes across variables.

**Test cases:** product(classes per variable)

```
Weight classes: 5
Distance classes: 5
Priority classes: 3

Strong coverage: 5 × 5 × 3 = 75 test cases
```

**When to use strong testing:**
- Variables interact (combinations have special behavior)
- High-risk functionality (payment, security)
- Complex business rules

## Identifying Equivalence Classes

### From Requirements

**Requirement:** "Users must be 18-65 years old, living in US, CA, or UK"

**Extract classes:**
```
Age:
  - Invalid: < 18
  - Valid: 18-65
  - Invalid: > 65

Country:
  - Valid: US
  - Valid: CA
  - Valid: UK
  - Invalid: Other countries
```

### From Data Types

| Data Type | Typical Classes |
|-----------|-----------------|
| Integer | Negative, zero, positive, max int |
| String | Empty, single char, typical, max length, special chars |
| Boolean | True, false |
| Array | Empty, single, few, many, max size |
| Date | Past, today, future, boundaries |
| Email | Valid format, missing @, missing domain |

### From Business Rules

**Rule:** "Orders over $100 get free shipping, premium members get 10% extra"

**Classes:**
```
Order Amount:
  - Below threshold: $0.01 - $99.99 (no free shipping)
  - At threshold: $100 (free shipping)
  - Above threshold: $100.01+ (free shipping)

Member Status:
  - Regular (standard pricing)
  - Premium (10% extra discount)
  - Non-member (no discount)
```

## Combining with Boundary Value Analysis

Equivalence partitioning and BVA work together:

1. **EP identifies classes** - What groups exist?
2. **BVA tests boundaries** - Where do classes meet?

**Example: Age validation (18-65)**

```python
def test_age_complete():
    # Equivalence class: Invalid (too young)
    assert is_valid(10) == False   # Representative

    # Boundary: Just below valid
    assert is_valid(17) == False

    # Boundary: Minimum valid
    assert is_valid(18) == True

    # Equivalence class: Valid
    assert is_valid(40) == True    # Representative

    # Boundary: Maximum valid
    assert is_valid(65) == True

    # Boundary: Just above valid
    assert is_valid(66) == False

    # Equivalence class: Invalid (too old)
    assert is_valid(80) == False   # Representative
```

## Output-Based Partitioning

### Partition by Expected Output

Instead of input classes, group by expected results:

**Function:** calculate_grade(score)

**Output classes:**
```
'A': score 90-100
'B': score 80-89
'C': score 70-79
'D': score 60-69
'F': score 0-59
'Invalid': score < 0 or > 100
```

**Tests:**
```python
def test_grade_calculation():
    # Each output class
    assert calculate_grade(95) == 'A'   # A range
    assert calculate_grade(85) == 'B'   # B range
    assert calculate_grade(75) == 'C'   # C range
    assert calculate_grade(65) == 'D'   # D range
    assert calculate_grade(45) == 'F'   # F range

    # Invalid outputs
    with pytest.raises(ValueError):
        calculate_grade(-5)
    with pytest.raises(ValueError):
        calculate_grade(105)
```

### Error Classes

Group by expected error types:

```python
def test_error_partitions():
    # Validation error class
    with pytest.raises(ValidationError):
        process(invalid_format_input)

    # Permission error class
    with pytest.raises(PermissionError):
        process(unauthorized_input)

    # Not found error class
    with pytest.raises(NotFoundError):
        process(nonexistent_resource)

    # Success class
    assert process(valid_input).success == True
```

## Practical Patterns

### String Input Classes

```python
def test_string_equivalence():
    validate = validate_username

    # Length classes
    assert validate("") == False           # Empty
    assert validate("a") == False          # Too short
    assert validate("abc") == True         # Min valid (3)
    assert validate("user123") == True     # Typical
    assert validate("a" * 20) == True      # Max valid (20)
    assert validate("a" * 21) == False     # Too long

    # Character classes
    assert validate("user_name") == True   # With underscore
    assert validate("user-name") == False  # Invalid char
    assert validate("user123") == True     # Alphanumeric
    assert validate("123user") == False    # Starts with number
```

### Numeric Input Classes

```python
def test_numeric_equivalence():
    process = process_payment

    # Value classes
    with pytest.raises(ValueError):
        process(0)                          # Zero (invalid)
    with pytest.raises(ValueError):
        process(-100)                       # Negative (invalid)
    assert process(0.01).success            # Minimum valid
    assert process(50).success              # Typical
    assert process(10000).success           # Large valid
    with pytest.raises(ValueError):
        process(10001)                      # Over limit

    # Precision classes
    assert process(99.99).amount == 99.99   # Two decimals
    assert process(99.999).amount == 100.00 # Rounded
```

### Date Input Classes

```python
def test_date_equivalence():
    validate = validate_reservation_date

    # Time classes
    assert validate(yesterday()) == False   # Past (invalid)
    assert validate(today()) == True        # Today (valid)
    assert validate(tomorrow()) == True     # Future (valid)
    assert validate(far_future()) == False  # Too far (invalid)

    # Special date classes
    assert validate(holiday()) == False     # Holidays blocked
    assert validate(weekend()) == True      # Weekends valid
    assert validate(weekday()) == True      # Weekdays valid
```

### Collection Input Classes

```python
def test_collection_equivalence():
    process = process_items

    # Size classes
    assert process([]) == []                 # Empty
    assert process([1]) == [1]               # Single
    assert process([1,2,3]) == [1,2,3]       # Multiple
    assert process([1]*100) == expected      # Large
    with pytest.raises(ValueError):
        process([1]*1001)                    # Over limit

    # Content classes
    assert process([1,2,3])                  # All valid items
    with pytest.raises(ValueError):
        process([1, None, 3])                # Contains null
    with pytest.raises(ValueError):
        process([1, -1, 3])                  # Contains invalid
```

## Test Case Reduction

### When Full Coverage is Too Large

**Problem:** 5 variables × 5 classes each = 3,125 combinations

**Solutions:**

1. **Pairwise testing:** Cover all pairs of class combinations
2. **Risk-based selection:** Focus on high-risk combinations
3. **Single-fault assumption:** Bugs usually involve one variable

### Pairwise Approach

```
Variables: Browser (Chrome, Firefox, Safari)
           OS (Windows, Mac, Linux)
           Device (Desktop, Mobile, Tablet)

Full combinations: 27
Pairwise combinations: 9 (covers all pairs)
```

```python
def test_pairwise_combinations():
    # Selected to cover all pairs at least once
    test_on(browser="chrome", os="windows", device="desktop")
    test_on(browser="chrome", os="mac", device="mobile")
    test_on(browser="chrome", os="linux", device="tablet")
    test_on(browser="firefox", os="windows", device="mobile")
    test_on(browser="firefox", os="mac", device="tablet")
    test_on(browser="firefox", os="linux", device="desktop")
    test_on(browser="safari", os="windows", device="tablet")
    test_on(browser="safari", os="mac", device="desktop")
    test_on(browser="safari", os="linux", device="mobile")
```

## Quick Reference

### Partition Identification Checklist

- [ ] What are the input parameters?
- [ ] What ranges are valid for each?
- [ ] What values are explicitly invalid?
- [ ] Are there special values (null, zero, empty)?
- [ ] Do parameters interact?
- [ ] What outputs/errors are possible?

### Class Selection Rules

| Situation | Approach |
|-----------|----------|
| Clear ranges | One from each range |
| Multiple valid types | One from each type |
| Invalid inputs | One per type of invalidity |
| Boundaries exist | Add BVA tests |
| Variables interact | Add combination tests |

### Coverage Formula

```
Weak EP:    max(n₁, n₂, ..., nₖ) tests
Strong EP:  n₁ × n₂ × ... × nₖ tests
Pairwise:   approximately max(n²) tests
```

Where n = number of classes per variable.

## Summary

Equivalence partitioning makes testing tractable:

1. **Identify input classes** - Group inputs with same expected behavior
2. **Select representatives** - Test one value from each class
3. **Combine with BVA** - Add boundary tests between classes
4. **Use weak or strong** - Based on risk and interaction
5. **Output partitions** - Group by expected results, not just inputs
6. **Reduce strategically** - Pairwise testing when combinations explode


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

