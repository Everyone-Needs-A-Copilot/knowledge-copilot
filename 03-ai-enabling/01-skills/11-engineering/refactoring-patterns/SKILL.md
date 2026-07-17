---
last_updated: 2026-02-25
status: active
name: refactoring-patterns
description: Systematic code improvement techniques without changing behavior. Activate when restructuring, simplifying, or improving existing code.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["refactor", "restructure", "simplify", "extract", "inline", "rename", "move", "code smell", "technical debt"]
allowed-tools: Read, Write, Edit
---

# Refactoring Patterns

Improve code structure without changing external behavior. This skill provides systematic techniques for transforming messy code into clean, maintainable designs.

## Core Principle

**Refactoring ≠ Rewriting.** Change structure, preserve behavior. Always have tests before refactoring.

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Code Smells to Recognize

### Bloaters

| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Long Method | Can't fit on screen | Extract Method |
| Long Parameter List | 4+ parameters | Introduce Parameter Object |
| Large Class | Multiple responsibilities | Extract Class |
| Primitive Obsession | Strings/ints for domain concepts | Replace Primitive with Object |

### Couplers

| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Feature Envy | Method uses another class's data | Move Method |
| Inappropriate Intimacy | Classes know too much about each other | Move Method, Extract Class |
| Message Chains | `a.b().c().d()` | Hide Delegate |

### Dispensables

| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Duplicate Code | Copy-paste patterns | Extract Method |
| Dead Code | Unreachable code | Delete it |
| Speculative Generality | "Might need this someday" | Remove unused abstractions |

---

## 2. Extract Refactorings

### Extract Method

**When:** Block of code can be named meaningfully.

```python
# Before
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Empty")
    if not order.customer:
        raise ValueError("No customer")
    # ... more code

# After
def process_order(order):
    validate_order(order)
    # ... more code

def validate_order(order):
    if not order.items:
        raise ValueError("Empty")
    if not order.customer:
        raise ValueError("No customer")
```

### Extract Variable

**When:** Complex expression needs explanation.

```python
# Before
if user.subscription.plan.price > 100 and user.subscription.status == "active":
    pass

# After
is_premium_active = (
    user.subscription.plan.price > 100
    and user.subscription.status == "active"
)
if is_premium_active:
    pass
```

### Extract Class

**When:** Class has multiple responsibilities.

```python
# Before: User handles authentication AND profile
class User:
    def authenticate(self): ...
    def update_profile(self): ...
    def change_password(self): ...
    def upload_avatar(self): ...

# After: Separate concerns
class User:
    def __init__(self):
        self.auth = UserAuth(self)
        self.profile = UserProfile(self)

class UserAuth:
    def authenticate(self): ...
    def change_password(self): ...

class UserProfile:
    def update(self): ...
    def upload_avatar(self): ...
```

---

## 3. Move Refactorings

### Move Method

**When:** Method uses more of another class's data than its own.

```python
# Before: calculate_bonus uses employee data
class Department:
    def calculate_bonus(self, employee):
        return employee.salary * employee.performance_rating * 0.1

# After: Move to Employee
class Employee:
    def calculate_bonus(self):
        return self.salary * self.performance_rating * 0.1
```

### Move Field

**When:** Field is used more by another class.

---

## 4. Simplification Refactorings

### Replace Conditional with Polymorphism

**When:** Switch/if-else on type to determine behavior.

```python
# Before
def calculate_shipping(order):
    if order.type == "standard":
        return 5.99
    elif order.type == "express":
        return 15.99
    elif order.type == "overnight":
        return 29.99

# After
class ShippingMethod(Protocol):
    def calculate_cost(self) -> Decimal: ...

class StandardShipping:
    def calculate_cost(self) -> Decimal:
        return Decimal("5.99")

class ExpressShipping:
    def calculate_cost(self) -> Decimal:
        return Decimal("15.99")
```

### Introduce Parameter Object

**When:** Same parameters travel together.

```python
# Before
def create_report(start_date, end_date, department, format):
    pass

# After
@dataclass
class ReportRequest:
    start_date: date
    end_date: date
    department: str
    format: str

def create_report(request: ReportRequest):
    pass
```

### Replace Magic Number with Constant

```python
# Before
if attempts > 3:
    raise TooManyRetriesError()

# After
MAX_RETRIES = 3
if attempts > MAX_RETRIES:
    raise TooManyRetriesError()
```

---

## 5. Inline Refactorings

### Inline Method

**When:** Method body is as clear as its name.

```python
# Before
def is_more_than_five(value):
    return value > 5

if is_more_than_five(count):
    pass

# After
if count > 5:
    pass
```

### Inline Variable

**When:** Variable adds no clarity.

```python
# Before
base_price = order.base_price
return base_price > 1000

# After
return order.base_price > 1000
```

---

## 6. Safe Refactoring Process

### Steps

1. **Ensure tests pass** - Green baseline
2. **Make one small change** - Single refactoring
3. **Run tests** - Verify behavior unchanged
4. **Commit** - Save progress
5. **Repeat** - Next small change

### Golden Rules

| Rule | Why |
|------|-----|
| Never refactor and change behavior simultaneously | Impossible to debug failures |
| Small, incremental steps | Easy rollback |
| Run tests after each step | Catch breaks immediately |
| Commit frequently | Safety net |

---

## Quick Reference

| Smell | First Refactoring to Try |
|-------|--------------------------|
| Long method | Extract Method |
| Long parameter list | Introduce Parameter Object |
| Duplicate code | Extract Method |
| Feature envy | Move Method |
| Type-based conditionals | Replace Conditional with Polymorphism |
| Primitive obsession | Replace Primitive with Object |
| Large class | Extract Class |

Refactoring is continuous improvement. Do it in small, safe steps with test coverage.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

