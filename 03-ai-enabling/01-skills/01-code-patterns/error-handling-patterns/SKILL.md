---
last_updated: 2026-02-25
status: active
name: error-handling-patterns
description: Comprehensive error handling strategies - exceptions, recovery, error boundaries. Use when designing robust error handling.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["error handling", "exception", "try catch", "error boundary", "recovery", "fault tolerance", "graceful degradation", "error propagation"]
allowed-tools: Read, Write, Edit
---

# Error Handling Patterns: Deep Expertise Skill

Build systems that fail gracefully and recover elegantly. This skill provides comprehensive patterns for handling errors at every level of your application.

## Philosophy: Errors Are Not Exceptional

Errors are a normal part of system operation. Network fails. Users provide bad input. Dependencies go down. Robust systems expect errors and handle them gracefully.

**Goals of good error handling:**
- **Fail fast** - Detect errors early, before they cascade
- **Fail safely** - Contain damage, protect data integrity
- **Fail informatively** - Provide actionable error messages
- **Recover gracefully** - Self-heal when possible, degrade when not

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## 1. Error Handling Fundamentals

### The Error Handling Hierarchy

Handle errors at the appropriate level:

```
┌─────────────────────────────────────────────────────┐
│ Global Level: Catch-all, logging, monitoring        │
├─────────────────────────────────────────────────────┤
│ Application Level: Business logic errors            │
├─────────────────────────────────────────────────────┤
│ Service Level: Integration errors, retries          │
├─────────────────────────────────────────────────────┤
│ Function Level: Validation, specific exceptions     │
└─────────────────────────────────────────────────────┘
```

**Rule:** Handle errors at the lowest level that has enough context to handle them properly.

### Exception vs Error Codes

**Use exceptions for:**
- Unexpected failures (file not found, network timeout)
- Programming errors (null pointer, index out of bounds)
- Errors that should interrupt normal flow

**Use return values for:**
- Expected failure cases (user not found, validation failed)
- High-performance code paths where exceptions are costly
- Functional-style code (Result types, Option types)

---

## 2. Designing Exception Hierarchies

### Create Domain-Specific Exceptions

**Bad: Generic exceptions**
```python
# No context, hard to catch specifically
raise Exception("Something went wrong")
raise ValueError("Invalid input")
```

**Good: Domain exceptions**
```python
class DomainError(Exception):
    """Base exception for all domain errors."""
    pass

class ValidationError(DomainError):
    """Invalid input data."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on {field}: {message}")

class NotFoundError(DomainError):
    """Requested resource does not exist."""
    def __init__(self, resource_type: str, resource_id: str):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} not found: {resource_id}")

class ConflictError(DomainError):
    """Operation conflicts with current state."""
    def __init__(self, message: str, conflicting_resource: str = None):
        self.conflicting_resource = conflicting_resource
        super().__init__(message)

class AuthorizationError(DomainError):
    """User lacks permission for operation."""
    def __init__(self, action: str, resource: str):
        self.action = action
        self.resource = resource
        super().__init__(f"Not authorized to {action} on {resource}")
```

### Exception Hierarchy Design

```python
class AppError(Exception):
    """Base for all application errors."""

    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> dict:
        """Convert to API response format."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }

# Client errors (4xx)
class ClientError(AppError):
    """Client-side errors (bad request, not found, etc.)."""
    pass

class ValidationError(ClientError):
    """Input validation failed."""
    pass

class NotFoundError(ClientError):
    """Resource not found."""
    pass

class AuthenticationError(ClientError):
    """Authentication required or failed."""
    pass

class AuthorizationError(ClientError):
    """Authenticated but not authorized."""
    pass

# Server errors (5xx)
class ServerError(AppError):
    """Server-side errors."""
    pass

class IntegrationError(ServerError):
    """External service integration failed."""
    pass

class DatabaseError(ServerError):
    """Database operation failed."""
    pass
```

### Map Exceptions to HTTP Status Codes

```python
from fastapi import HTTPException

EXCEPTION_STATUS_MAP = {
    ValidationError: 400,
    AuthenticationError: 401,
    AuthorizationError: 403,
    NotFoundError: 404,
    ConflictError: 409,
    IntegrationError: 502,
    DatabaseError: 500,
}

def exception_to_http(exc: AppError) -> HTTPException:
    """Convert domain exception to HTTP exception."""
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 500)
    return HTTPException(
        status_code=status_code,
        detail=exc.to_dict()
    )

# FastAPI exception handler
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 500)
    return JSONResponse(
        status_code=status_code,
        content=exc.to_dict()
    )
```

---

## 3. Try-Catch Best Practices

### Catch Specific Exceptions

**Bad: Catch-all**
```python
try:
    result = process_payment(order)
except Exception:
    # What went wrong? Network? Validation? Bug?
    return {"error": "Something went wrong"}
```

**Good: Specific handling**
```python
try:
    result = process_payment(order)
except PaymentDeclinedError as e:
    logger.info("payment_declined", order_id=order.id, reason=e.reason)
    return {"error": "Payment was declined", "reason": e.reason}
except PaymentGatewayError as e:
    logger.error("payment_gateway_error", order_id=order.id, error=str(e))
    raise  # Re-raise for retry handling
except ValidationError as e:
    logger.warning("payment_validation_failed", field=e.field)
    return {"error": f"Invalid {e.field}: {e.message}"}
```

### Don't Swallow Exceptions

**Bad: Silent failure**
```python
try:
    send_notification(user)
except Exception:
    pass  # Silently ignored - debugging nightmare
```

**Good: Log and handle appropriately**
```python
try:
    send_notification(user)
except NotificationError as e:
    logger.warning(
        "notification_failed",
        user_id=user.id,
        error=str(e),
        exc_info=True
    )
    # Continue - notification failure shouldn't block main flow
```

### Use Finally for Cleanup

```python
def process_file(path: str) -> ProcessResult:
    file = None
    try:
        file = open(path, 'r')
        return process_content(file.read())
    except FileNotFoundError:
        raise NotFoundError("file", path)
    except IOError as e:
        raise ServerError(f"Failed to read file: {e}")
    finally:
        # Always runs, even if exception raised
        if file:
            file.close()

# Better: Use context managers
def process_file(path: str) -> ProcessResult:
    try:
        with open(path, 'r') as file:
            return process_content(file.read())
    except FileNotFoundError:
        raise NotFoundError("file", path)
```

### Re-raise with Context

**Bad: Lose original context**
```python
try:
    result = external_api.call(data)
except Exception:
    raise IntegrationError("API call failed")  # Lost original error!
```

**Good: Chain exceptions**
```python
try:
    result = external_api.call(data)
except RequestException as e:
    raise IntegrationError(
        f"API call failed: {e}",
        details={"endpoint": external_api.url}
    ) from e  # Chains original exception

# Python's traceback will show both exceptions:
# IntegrationError: API call failed: Connection timeout
# During handling of the above exception, another exception occurred:
# RequestException: Connection timeout
```

---

## 4. Validation and Early Failure

### Fail Fast Principle

Detect errors as early as possible, before they cause damage.

**Bad: Validate late**
```python
def process_order(order_data: dict) -> Order:
    # Create order first
    order = Order(**order_data)
    db.save(order)  # Saved to DB

    # Then validate (too late!)
    if order.total < 0:
        db.delete(order)  # Cleanup required
        raise ValidationError("total", "must be positive")

    return order
```

**Good: Validate first**
```python
def process_order(order_data: dict) -> Order:
    # Validate before any state changes
    validated_data = validate_order_data(order_data)

    # Now safe to proceed
    order = Order(**validated_data)
    db.save(order)

    return order

def validate_order_data(data: dict) -> dict:
    """Validate all order data upfront."""
    errors = []

    if data.get("total", 0) < 0:
        errors.append(ValidationError("total", "must be positive"))

    if not data.get("items"):
        errors.append(ValidationError("items", "at least one item required"))

    if errors:
        raise ValidationErrors(errors)

    return data
```

### Guard Clauses

Check preconditions at the start of functions.

**Bad: Nested conditionals**
```python
def process_refund(order: Order, user: User) -> Refund:
    if user:
        if user.is_active:
            if order:
                if order.status == "completed":
                    if order.user_id == user.id:
                        # Finally, the actual logic
                        return create_refund(order)
                    else:
                        raise AuthorizationError("Not your order")
                else:
                    raise ValidationError("status", "Order not completed")
            else:
                raise NotFoundError("order", "unknown")
        else:
            raise AuthenticationError("User inactive")
    else:
        raise AuthenticationError("User required")
```

**Good: Guard clauses**
```python
def process_refund(order: Order, user: User) -> Refund:
    # Guard clauses - fail fast
    if not user:
        raise AuthenticationError("User required")

    if not user.is_active:
        raise AuthenticationError("User inactive")

    if not order:
        raise NotFoundError("order", "unknown")

    if order.status != "completed":
        raise ValidationError("status", "Order must be completed for refund")

    if order.user_id != user.id:
        raise AuthorizationError("refund", f"order:{order.id}")

    # Main logic - clean and clear
    return create_refund(order)
```

### Input Validation Patterns

**Pydantic for API validation:**
```python
from pydantic import BaseModel, Field, validator

class CreateOrderRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    items: list[OrderItem] = Field(..., min_items=1)
    shipping_address: Address

    @validator('items')
    def validate_items(cls, items):
        if sum(item.quantity for item in items) > 100:
            raise ValueError("Maximum 100 items per order")
        return items

# FastAPI automatically validates and returns 422 on failure
@app.post("/orders")
async def create_order(request: CreateOrderRequest) -> Order:
    return order_service.create(request)
```

**Custom validation with detailed errors:**
```python
class ValidationErrors(AppError):
    """Multiple validation errors."""

    def __init__(self, errors: list[ValidationError]):
        self.errors = errors
        super().__init__(
            f"Validation failed: {len(errors)} errors",
            details={"errors": [e.to_dict() for e in errors]}
        )

def validate_user_registration(data: dict) -> dict:
    errors = []

    # Email validation
    if not data.get("email"):
        errors.append(ValidationError("email", "required"))
    elif not is_valid_email(data["email"]):
        errors.append(ValidationError("email", "invalid format"))
    elif user_exists(data["email"]):
        errors.append(ValidationError("email", "already registered"))

    # Password validation
    if not data.get("password"):
        errors.append(ValidationError("password", "required"))
    elif len(data["password"]) < 12:
        errors.append(ValidationError("password", "minimum 12 characters"))

    if errors:
        raise ValidationErrors(errors)

    return data
```

---

## 5. Error Recovery Strategies

### Retry with Backoff

For transient failures (network, rate limits):

```python
import asyncio
from typing import TypeVar, Callable
import random

T = TypeVar('T')

async def retry_with_backoff(
    operation: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    retryable_exceptions: tuple = (ConnectionError, TimeoutError)
) -> T:
    """
    Retry operation with exponential backoff and jitter.

    Args:
        operation: Async function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential calculation
        retryable_exceptions: Exceptions that trigger retry

    Returns:
        Result of successful operation

    Raises:
        Last exception if all retries fail
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return await operation()
        except retryable_exceptions as e:
            last_exception = e

            if attempt == max_retries:
                logger.error(
                    "retry_exhausted",
                    operation=operation.__name__,
                    attempts=attempt + 1,
                    error=str(e)
                )
                raise

            # Calculate delay with exponential backoff
            delay = min(
                base_delay * (exponential_base ** attempt),
                max_delay
            )

            # Add jitter (±25%) to prevent thundering herd
            jitter = delay * 0.25 * (2 * random.random() - 1)
            delay = delay + jitter

            logger.warning(
                "retry_attempt",
                operation=operation.__name__,
                attempt=attempt + 1,
                delay=delay,
                error=str(e)
            )

            await asyncio.sleep(delay)

    raise last_exception

# Usage
async def fetch_user_data(user_id: str) -> dict:
    return await retry_with_backoff(
        lambda: external_api.get_user(user_id),
        max_retries=3,
        retryable_exceptions=(ConnectionError, TimeoutError, RateLimitError)
    )
```

### Circuit Breaker Pattern

Prevent cascading failures by failing fast when a service is unhealthy:

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, TypeVar

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing fast
    HALF_OPEN = "half_open"  # Testing recovery

@dataclass
class CircuitBreaker:
    """Circuit breaker for external service calls."""

    failure_threshold: int = 5
    recovery_timeout: timedelta = timedelta(seconds=30)
    half_open_max_calls: int = 3

    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: datetime = None
    half_open_successes: int = 0

    def can_execute(self) -> bool:
        """Check if call should be allowed."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if datetime.now() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_successes = 0
                logger.info("circuit_half_open")
                return True
            return False

        # Half-open: allow limited calls to test recovery
        return True

    def record_success(self):
        """Record successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_successes += 1
            if self.half_open_successes >= self.half_open_max_calls:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                logger.info("circuit_closed")
        else:
            self.failure_count = 0

    def record_failure(self):
        """Record failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            logger.warning("circuit_reopened")
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning("circuit_opened", failures=self.failure_count)

class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass

# Usage
payment_circuit = CircuitBreaker(failure_threshold=3, recovery_timeout=timedelta(seconds=60))

async def process_payment(payment: Payment) -> PaymentResult:
    if not payment_circuit.can_execute():
        raise CircuitOpenError("Payment service temporarily unavailable")

    try:
        result = await payment_gateway.charge(payment)
        payment_circuit.record_success()
        return result
    except (ConnectionError, TimeoutError) as e:
        payment_circuit.record_failure()
        raise
```

### Graceful Degradation

Provide reduced functionality when services fail:

```python
class RecommendationService:
    """Service that degrades gracefully when ML service is unavailable."""

    def __init__(self, ml_client: MLClient, cache: Cache):
        self.ml_client = ml_client
        self.cache = cache
        self.circuit = CircuitBreaker()

    async def get_recommendations(
        self,
        user_id: str,
        count: int = 10
    ) -> list[Product]:
        """Get personalized recommendations with fallbacks."""

        # Try ML-powered recommendations
        try:
            if self.circuit.can_execute():
                recommendations = await self.ml_client.get_personalized(
                    user_id, count
                )
                self.circuit.record_success()

                # Cache for fallback
                await self.cache.set(
                    f"recommendations:{user_id}",
                    recommendations,
                    ttl=3600
                )

                return recommendations
        except (ConnectionError, TimeoutError, CircuitOpenError) as e:
            self.circuit.record_failure()
            logger.warning(
                "ml_recommendations_failed",
                user_id=user_id,
                error=str(e)
            )

        # Fallback 1: Return cached recommendations
        cached = await self.cache.get(f"recommendations:{user_id}")
        if cached:
            logger.info("using_cached_recommendations", user_id=user_id)
            return cached

        # Fallback 2: Return popular items
        logger.info("using_popular_items_fallback", user_id=user_id)
        return await self.get_popular_items(count)

    async def get_popular_items(self, count: int) -> list[Product]:
        """Static fallback: popular items."""
        return await self.cache.get("popular_items") or []
```

---

## 6. Error Boundaries and Isolation

### Application-Level Error Boundaries

**FastAPI global exception handler:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """Handle all domain errors."""
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 500)

    # Log server errors
    if status_code >= 500:
        logger.error(
            "server_error",
            path=request.url.path,
            error=exc.message,
            exc_info=True
        )

    return JSONResponse(
        status_code=status_code,
        content=exc.to_dict()
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected errors."""
    logger.critical(
        "unhandled_exception",
        path=request.url.path,
        error=str(exc),
        exc_info=True
    )

    # Don't expose internal details
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "An unexpected error occurred"
            }
        }
    )
```

**React error boundary:**
```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error reporting service
    console.error('Error caught by boundary:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary
      fallback={<ErrorPage />}
      onError={(error) => errorReportingService.capture(error)}
    >
      <MainContent />
    </ErrorBoundary>
  );
}
```

### Transaction Boundaries

Ensure atomicity - all or nothing:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def transaction():
    """Database transaction context manager."""
    async with db.begin() as conn:
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise

async def transfer_funds(
    from_account: str,
    to_account: str,
    amount: Decimal
) -> Transfer:
    """Transfer funds atomically."""
    async with transaction() as conn:
        # Debit source account
        source = await get_account(conn, from_account)
        if source.balance < amount:
            raise ValidationError("balance", "Insufficient funds")
        source.balance -= amount
        await save_account(conn, source)

        # Credit destination account
        dest = await get_account(conn, to_account)
        dest.balance += amount
        await save_account(conn, dest)

        # Create transfer record
        transfer = Transfer(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )
        await save_transfer(conn, transfer)

        return transfer
        # If any step fails, entire transaction rolls back
```

### Bulkhead Pattern

Isolate failures to prevent system-wide impact:

```python
from asyncio import Semaphore

class BulkheadManager:
    """Limit concurrent calls to isolate failures."""

    def __init__(self):
        # Separate limits for different services
        self.payment_semaphore = Semaphore(10)
        self.notification_semaphore = Semaphore(50)
        self.analytics_semaphore = Semaphore(100)

    @asynccontextmanager
    async def payment_bulkhead(self):
        """Limit concurrent payment calls."""
        async with self.payment_semaphore:
            yield

    @asynccontextmanager
    async def notification_bulkhead(self):
        """Limit concurrent notification calls."""
        async with self.notification_semaphore:
            yield

bulkheads = BulkheadManager()

async def process_order(order: Order):
    # Payment limited to 10 concurrent calls
    async with bulkheads.payment_bulkhead():
        payment = await charge_payment(order)

    # Notification limited to 50 concurrent calls
    async with bulkheads.notification_bulkhead():
        await send_confirmation(order)
```

---

## 7. Logging and Observability

### Structured Error Logging

```python
import structlog

logger = structlog.get_logger()

def log_error(
    error: Exception,
    context: dict = None,
    level: str = "error"
) -> None:
    """Log error with structured context."""
    log_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "error_code": getattr(error, 'code', None),
    }

    if context:
        log_data.update(context)

    if isinstance(error, AppError):
        log_data["error_details"] = error.details

    getattr(logger, level)(
        "error_occurred",
        **log_data,
        exc_info=True if level in ("error", "critical") else False
    )

# Usage
try:
    process_order(order)
except ValidationError as e:
    log_error(e, {"order_id": order.id}, level="warning")
    raise
except IntegrationError as e:
    log_error(e, {"order_id": order.id, "service": "payment"}, level="error")
    raise
```

### Error Context Propagation

Add context as errors bubble up:

```python
class ErrorContext:
    """Add context to exceptions as they propagate."""

    def __init__(self, **context):
        self.context = context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val and isinstance(exc_val, AppError):
            exc_val.details.update(self.context)
        return False

# Usage
async def process_order(order: Order) -> Order:
    with ErrorContext(order_id=str(order.id)):
        with ErrorContext(step="validation"):
            validate_order(order)

        with ErrorContext(step="payment"):
            await charge_payment(order)

        with ErrorContext(step="fulfillment"):
            await fulfill_order(order)

    return order

# Errors will include: {"order_id": "...", "step": "payment"}
```

---

## 8. User-Facing Error Messages

### Separate Internal and External Errors

**Internal (for developers):**
```python
logger.error(
    "payment_failed",
    error="STRIPE_CARD_DECLINED",
    decline_code="insufficient_funds",
    card_last_four="4242",
    customer_id="cus_123",
    amount=5000
)
```

**External (for users):**
```json
{
  "error": {
    "code": "payment_declined",
    "message": "Your payment was declined. Please try a different payment method.",
    "action": "Try using a different card or contact your bank."
  }
}
```

### Error Message Guidelines

| Do | Don't |
|----|-------|
| "Email address is already registered" | "Duplicate key violation" |
| "Session expired. Please sign in again" | "JWT token expired" |
| "Unable to connect. Please try again" | "ECONNREFUSED 10.0.0.1:5432" |
| "File must be smaller than 10MB" | "Request entity too large" |

### Actionable Error Messages

Every error should tell the user what to do:

```python
ERROR_MESSAGES = {
    "email_taken": {
        "message": "This email is already registered.",
        "action": "Try signing in or use a different email."
    },
    "password_weak": {
        "message": "Password doesn't meet requirements.",
        "action": "Use at least 12 characters with uppercase, lowercase, numbers, and symbols."
    },
    "rate_limited": {
        "message": "Too many requests.",
        "action": "Please wait a moment and try again."
    },
    "payment_declined": {
        "message": "Payment was declined.",
        "action": "Check your card details or try a different payment method."
    }
}

def get_user_error(code: str) -> dict:
    return ERROR_MESSAGES.get(code, {
        "message": "Something went wrong.",
        "action": "Please try again. If the problem persists, contact support."
    })
```

---

## 9. Testing Error Handling

### Test Expected Errors

```python
import pytest

class TestOrderService:

    def test_rejects_empty_order(self, order_service):
        """Validation error for empty order."""
        with pytest.raises(ValidationError) as exc_info:
            order_service.create_order(items=[])

        assert exc_info.value.field == "items"
        assert "at least one item" in exc_info.value.message

    def test_rejects_negative_quantity(self, order_service):
        """Validation error for negative quantity."""
        with pytest.raises(ValidationError) as exc_info:
            order_service.create_order(items=[
                {"product_id": "123", "quantity": -1}
            ])

        assert exc_info.value.field == "quantity"

    def test_handles_payment_failure(self, order_service, mock_payment):
        """Order creation fails gracefully when payment fails."""
        mock_payment.charge.side_effect = PaymentDeclinedError("insufficient_funds")

        with pytest.raises(PaymentDeclinedError) as exc_info:
            order_service.create_order(items=[{"product_id": "123", "quantity": 1}])

        # Verify order was not saved
        assert order_service.repository.count() == 0
```

### Test Error Recovery

```python
class TestRetryBehavior:

    async def test_retries_on_transient_failure(self):
        """Retries transient failures with backoff."""
        call_count = 0

        async def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Network error")
            return "success"

        result = await retry_with_backoff(flaky_operation, max_retries=5)

        assert result == "success"
        assert call_count == 3

    async def test_gives_up_after_max_retries(self):
        """Raises after exhausting retries."""
        async def always_fails():
            raise ConnectionError("Network error")

        with pytest.raises(ConnectionError):
            await retry_with_backoff(always_fails, max_retries=3)

class TestCircuitBreaker:

    def test_opens_after_threshold(self):
        """Circuit opens after failure threshold."""
        circuit = CircuitBreaker(failure_threshold=3)

        for _ in range(3):
            circuit.record_failure()

        assert circuit.state == CircuitState.OPEN
        assert not circuit.can_execute()
```

---

## Quick Reference: Error Handling Checklist

### Design
- [ ] Domain-specific exception hierarchy
- [ ] Exceptions map to HTTP status codes
- [ ] Internal vs external error messages
- [ ] All errors have actionable messages

### Implementation
- [ ] Catch specific exceptions
- [ ] Never swallow exceptions silently
- [ ] Use guard clauses for validation
- [ ] Validate early, fail fast
- [ ] Use context managers for cleanup

### Recovery
- [ ] Retry with exponential backoff
- [ ] Circuit breakers for external services
- [ ] Graceful degradation fallbacks
- [ ] Bulkheads to isolate failures

### Observability
- [ ] Structured error logging
- [ ] Error context propagation
- [ ] Request IDs for tracing
- [ ] Alerting on error thresholds

### Testing
- [ ] Test expected error cases
- [ ] Test error recovery paths
- [ ] Test circuit breaker behavior
- [ ] Test validation edge cases

---

Good error handling is invisible when things work and invaluable when they don't. Design for failure from day one, and your system will be resilient, debuggable, and trustworthy.


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

