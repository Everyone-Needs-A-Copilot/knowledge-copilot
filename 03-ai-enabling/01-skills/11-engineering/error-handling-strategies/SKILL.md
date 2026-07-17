---
last_updated: 2026-02-25
status: active
name: error-handling-strategies
description: Design robust error handling for reliable applications. Activate when implementing error recovery, exception handling, or fault tolerance.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["error handling", "exception", "try catch", "fault tolerance", "retry", "fallback", "graceful degradation", "error recovery"]
allowed-tools: Read, Write, Edit
---

# Error Handling Strategies

Design systems that fail gracefully, recover automatically, and provide clear feedback. This skill covers patterns for building reliable, fault-tolerant applications.

## Core Principles

| Principle | Practice |
|-----------|----------|
| **Fail fast** | Detect and report errors early |
| **Fail loudly** | Don't swallow errors silently |
| **Fail safely** | Minimize impact of failures |
| **Recover gracefully** | Automatic recovery when possible |

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Exception Best Practices

### Use Specific Exceptions

```python
# BAD: Generic exception
if not user:
    raise Exception("User not found")

# GOOD: Specific exception
class UserNotFoundError(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

if not user:
    raise UserNotFoundError(user_id)
```

### Exception Hierarchy

```python
# Base exception for your domain
class PaymentError(Exception):
    """Base class for payment errors."""
    pass

# Specific errors inherit from base
class PaymentDeclinedError(PaymentError):
    """Card was declined."""
    pass

class PaymentTimeoutError(PaymentError):
    """Payment gateway didn't respond in time."""
    pass

class InsufficientFundsError(PaymentError):
    """Not enough balance."""
    pass
```

### Catch Specific, Re-raise Generic

```python
def process_payment(payment):
    try:
        result = gateway.charge(payment)
    except ConnectionError as e:
        # Transform infrastructure error to domain error
        raise PaymentTimeoutError("Gateway unreachable") from e
    except GatewayDeclineError as e:
        raise PaymentDeclinedError(e.decline_reason) from e

    return result
```

---

## 2. Error Handling Patterns

### Guard Clauses

Validate early, fail fast.

```python
def transfer_funds(from_account, to_account, amount):
    # Guard clauses at the start
    if from_account is None:
        raise ValueError("Source account required")
    if to_account is None:
        raise ValueError("Destination account required")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if from_account.balance < amount:
        raise InsufficientFundsError(from_account.id, amount)

    # Happy path - all validations passed
    from_account.balance -= amount
    to_account.balance += amount
```

### Result Type Pattern

Return success/failure instead of throwing.

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Union

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    error: E

Result = Union[Ok[T], Err[E]]

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

# Usage
result = divide(10, 0)
match result:
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

### Null Object Pattern

Avoid null checks with default behavior.

```python
class NullUser:
    """Default user when none found."""
    id = None
    name = "Guest"
    permissions = frozenset()

    def can_access(self, resource):
        return False

def get_user(user_id) -> User:
    user = db.find_user(user_id)
    return user if user else NullUser()

# No null checks needed
user = get_user(user_id)
if user.can_access(resource):  # Works even if NullUser
    grant_access()
```

---

## 3. Recovery Patterns

### Retry with Backoff

```python
import time
import random

def retry_with_backoff(
    func,
    max_attempts=3,
    base_delay=1.0,
    max_delay=30.0,
    exponential_base=2,
    jitter=True
):
    """Retry function with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise

            delay = min(
                base_delay * (exponential_base ** attempt),
                max_delay
            )

            if jitter:
                delay *= (0.5 + random.random())

            time.sleep(delay)
```

### Circuit Breaker

Prevent cascading failures.

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=5,
        recovery_timeout=30,
        half_open_requests=3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_requests = half_open_requests
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_successes = 0

    def call(self, func):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_successes = 0
            else:
                raise CircuitOpenError("Circuit breaker is open")

        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_successes += 1
            if self.half_open_successes >= self.half_open_requests:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### Fallback

Provide degraded functionality.

```python
async def get_user_recommendations(user_id):
    try:
        # Try personalized recommendations
        return await recommendation_service.get_for_user(user_id)
    except ServiceUnavailableError:
        try:
            # Fallback to cached recommendations
            return await cache.get(f"recommendations:{user_id}")
        except CacheMissError:
            # Final fallback to popular items
            return await get_popular_items()
```

---

## 4. Error Communication

### User-Facing Errors

```python
@dataclass
class UserError:
    """Error message for end users."""
    code: str
    message: str
    details: dict = None

    def to_response(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }

# Map internal errors to user errors
ERROR_MESSAGES = {
    PaymentDeclinedError: UserError(
        code="PAYMENT_DECLINED",
        message="Your payment was declined. Please try another card."
    ),
    InsufficientFundsError: UserError(
        code="INSUFFICIENT_FUNDS",
        message="Insufficient funds in your account."
    ),
}

def handle_error(error):
    user_error = ERROR_MESSAGES.get(
        type(error),
        UserError(code="INTERNAL_ERROR", message="Something went wrong.")
    )
    return user_error.to_response()
```

### Logging Errors

```python
import logging

logger = logging.getLogger(__name__)

def process_order(order):
    try:
        result = execute_order(order)
        logger.info("Order processed", extra={
            "order_id": order.id,
            "total": order.total
        })
        return result
    except PaymentError as e:
        logger.error("Payment failed", extra={
            "order_id": order.id,
            "error_type": type(e).__name__,
            "error_message": str(e)
        }, exc_info=True)  # Include stack trace
        raise
```

---

## 5. Defensive Programming

### Input Validation

```python
def create_user(data: dict) -> User:
    """Create user with validated data."""
    # Validate required fields
    required = ["email", "name", "password"]
    missing = [f for f in required if f not in data]
    if missing:
        raise ValidationError(f"Missing required fields: {missing}")

    # Validate formats
    if not is_valid_email(data["email"]):
        raise ValidationError("Invalid email format")

    if len(data["password"]) < 8:
        raise ValidationError("Password must be at least 8 characters")

    # Now safe to use data
    return User.create(**data)
```

### Assertions for Invariants

```python
def process_batch(items):
    """Process items maintaining invariant: all items have IDs."""
    assert all(item.id is not None for item in items), "All items must have IDs"

    results = []
    for item in items:
        result = process(item)
        results.append(result)

    assert len(results) == len(items), "Must process all items"
    return results
```

---

## 6. Cleanup and Resources

### Context Managers

```python
from contextlib import contextmanager

@contextmanager
def transaction():
    """Ensure transaction is committed or rolled back."""
    tx = db.begin_transaction()
    try:
        yield tx
        tx.commit()
    except Exception:
        tx.rollback()
        raise

# Usage
with transaction() as tx:
    tx.execute("INSERT INTO users ...")
    tx.execute("INSERT INTO profiles ...")
    # Commits on success, rolls back on exception
```

### Finally for Cleanup

```python
def process_file(path):
    file = None
    try:
        file = open(path)
        return process(file.read())
    except FileNotFoundError:
        raise InputError(f"File not found: {path}")
    finally:
        if file:
            file.close()  # Always runs
```

---

## Quick Reference

### Exception Checklist

- [ ] Using specific exception types?
- [ ] Exceptions have meaningful messages?
- [ ] Original exception preserved (`from e`)?
- [ ] Resources cleaned up in finally/with?
- [ ] User-facing errors are helpful?
- [ ] Internal errors logged with context?

### Recovery Strategy Selection

| Failure Type | Strategy |
|--------------|----------|
| Transient (network, timeout) | Retry with backoff |
| Service degraded | Fallback |
| Repeated failures | Circuit breaker |
| Invalid input | Fail fast with clear error |
| Unknown | Log, alert, graceful degradation |

### Anti-Patterns

| Anti-Pattern | Problem |
|--------------|---------|
| Catching all exceptions | Hides bugs |
| Empty catch blocks | Silent failures |
| Returning null on error | Unclear failure |
| Generic error messages | Hard to debug |
| No cleanup on failure | Resource leaks |

Handle errors explicitly. Fail fast on invalid input. Recover gracefully from transient failures.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

