---
last_updated: 2026-02-25
status: active
name: logging-best-practices
description: Structured logging, appropriate levels, and observability patterns. Use when implementing logging strategies.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.go", "**/*.java", "**/logging.*", "**/logger.*"]
  keywords: ["logging", "logger", "log level", "structured logging", "observability", "tracing", "monitoring", "debug", "error log"]
allowed-tools: Read, Write, Edit
---

# Logging Best Practices: Deep Expertise Skill

Build observable systems through thoughtful logging. This skill covers structured logging, appropriate log levels, and patterns for debugging and monitoring production systems.

## Philosophy: Logs Tell the Story

Logs are your system's narrative. When something goes wrong at 3 AM, logs are often all you have. Good logs answer:

- **What happened?** - The event that occurred
- **When?** - Timestamp with timezone
- **Where?** - Service, file, function, line
- **Who?** - User, request, session
- **Why?** - Context that explains the event
- **How severe?** - Log level indicating importance

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## 1. Structured Logging Fundamentals

### Why Structured Logs?

**Unstructured (bad for parsing):**
```
2026-01-17 10:30:45 INFO User john@example.com logged in from 192.168.1.100 using Chrome
```

**Structured (machine-parseable):**
```json
{
  "timestamp": "2026-01-17T10:30:45.123Z",
  "level": "info",
  "message": "user_login",
  "user_email": "john@example.com",
  "ip_address": "192.168.1.100",
  "user_agent": "Chrome/120.0",
  "service": "auth-service",
  "request_id": "req_abc123"
}
```

### Setting Up Structured Logging

**Python with structlog:**
```python
import structlog
from datetime import datetime, timezone

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()  # JSON output
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage
logger.info(
    "order_created",
    order_id="ord_123",
    customer_id="cust_456",
    total=99.99,
    items_count=3
)
```

**TypeScript with Pino:**
```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  base: {
    service: 'my-service',
    environment: process.env.NODE_ENV,
  },
});

// Usage
logger.info({
  event: 'order_created',
  orderId: 'ord_123',
  customerId: 'cust_456',
  total: 99.99,
  itemsCount: 3,
});
```

### Contextual Logging

Bind context that applies to multiple log entries:

```python
# Create logger with bound context
logger = structlog.get_logger()

# Bind request context
request_logger = logger.bind(
    request_id=request.headers.get("X-Request-ID"),
    user_id=current_user.id if current_user else None,
    endpoint=request.path
)

# All logs include this context
request_logger.info("processing_started")
request_logger.info("validation_complete", valid=True)
request_logger.info("processing_complete", duration_ms=150)
```

---

## 2. Log Levels: When to Use What

### Level Hierarchy

| Level | Purpose | When to Use | Example |
|-------|---------|-------------|---------|
| **TRACE** | Ultra-detailed | Step-by-step debugging | Loop iterations, variable values |
| **DEBUG** | Development info | Debugging, not production | "Parsed config: {...}" |
| **INFO** | Normal operations | Events worth noting | "User logged in" |
| **WARNING** | Potential issues | Something unexpected but handled | "Retry attempt 2 of 3" |
| **ERROR** | Failures | Something failed | "Payment declined" |
| **CRITICAL** | System failures | System is unusable | "Database connection lost" |

### Level Guidelines

**TRACE (rarely used in production):**
```python
# Extremely detailed - usually disabled
logger.trace("loop_iteration", index=i, value=items[i])
logger.trace("cache_lookup", key=cache_key, hit=cache.has(key))
```

**DEBUG (development and troubleshooting):**
```python
# Helpful for debugging, too noisy for production
logger.debug("request_parsed", body=request.body, headers=dict(request.headers))
logger.debug("query_executed", sql=query.statement, params=query.params)
logger.debug("cache_operation", operation="set", key=key, ttl=ttl)
```

**INFO (normal operations):**
```python
# Business events and state changes
logger.info("user_registered", user_id=user.id, plan="free")
logger.info("order_placed", order_id=order.id, total=order.total)
logger.info("payment_processed", payment_id=payment.id, amount=payment.amount)
logger.info("job_completed", job_id=job.id, duration_ms=duration)
```

**WARNING (attention needed but not failure):**
```python
# Degraded state, potential issues
logger.warning("rate_limit_approaching", current=95, limit=100, user_id=user.id)
logger.warning("retry_attempt", attempt=2, max_attempts=3, error=str(e))
logger.warning("deprecated_api_used", endpoint="/v1/old", user_id=user.id)
logger.warning("slow_query", query=query_name, duration_ms=5000)
```

**ERROR (operation failed):**
```python
# Failures that need attention
logger.error("payment_failed", order_id=order.id, error=str(e), exc_info=True)
logger.error("api_error", service="stripe", status=500, response=response.text)
logger.error("validation_failed", field="email", value=masked_email)
```

**CRITICAL (system in danger):**
```python
# System-wide issues
logger.critical("database_unavailable", error=str(e), exc_info=True)
logger.critical("out_of_memory", available_mb=10)
logger.critical("certificate_expired", domain="api.example.com")
```

### Common Level Mistakes

**Too verbose (everything is INFO):**
```python
# Bad - INFO for debugging details
logger.info("entering_function", func="process_order")
logger.info("checking_inventory", product_id=product.id)
logger.info("inventory_result", available=True)
logger.info("calculating_total", subtotal=99.99)
```

**Too quiet (missing important events):**
```python
# Bad - only logging errors
def create_order(data):
    try:
        order = Order.create(data)
        return order  # No log of successful creation!
    except Exception as e:
        logger.error("order_failed", error=str(e))
        raise
```

**Right balance:**
```python
def create_order(data):
    logger.debug("create_order_started", customer_id=data["customer_id"])

    try:
        order = Order.create(data)
        logger.info("order_created", order_id=order.id, total=order.total)
        return order
    except ValidationError as e:
        logger.warning("order_validation_failed", errors=e.errors)
        raise
    except Exception as e:
        logger.error("order_creation_failed", error=str(e), exc_info=True)
        raise
```

---

## 3. What to Log (and What Not To)

### Essential Context

**Always include:**
```python
# Request context
logger.info(
    "api_request",
    request_id=request.id,          # Unique request identifier
    method=request.method,          # HTTP method
    path=request.path,              # Endpoint
    user_id=current_user.id,        # Who made the request
    duration_ms=duration,           # How long it took
    status_code=response.status     # Result
)

# Error context
logger.error(
    "operation_failed",
    operation="create_order",       # What was being attempted
    error_type=type(e).__name__,    # Exception type
    error_message=str(e),           # Error message
    order_id=order_id,              # Relevant entity
    exc_info=True                   # Stack trace
)
```

### Log Events, Not Sentences

**Bad: Prose-style logs**
```python
logger.info(f"The user {user.email} has successfully logged in from IP {ip}")
logger.info(f"Order {order.id} created for customer {customer.id} with total ${total}")
```

**Good: Event-style logs**
```python
logger.info("user_login", email=user.email, ip=ip, method="password")
logger.info("order_created", order_id=order.id, customer_id=customer.id, total=total)
```

### Never Log Sensitive Data

**Sensitive data to exclude:**
- Passwords (even hashed)
- API keys and tokens
- Credit card numbers
- Social Security Numbers
- Personal health information
- Full email addresses (use masking)

**Data masking utilities:**
```python
def mask_email(email: str) -> str:
    """Mask email: john.doe@example.com -> j***e@e***.com"""
    if not email or '@' not in email:
        return '***'
    local, domain = email.split('@')
    return f"{local[0]}***{local[-1]}@{domain[0]}***.{domain.split('.')[-1]}"

def mask_card(number: str) -> str:
    """Mask card: 4242424242424242 -> ****4242"""
    return f"****{number[-4:]}" if len(number) >= 4 else "****"

def mask_token(token: str) -> str:
    """Mask token: abc123xyz789 -> abc...789"""
    if len(token) <= 6:
        return "***"
    return f"{token[:3]}...{token[-3:]}"

# Usage
logger.info(
    "payment_processed",
    card=mask_card(card_number),        # ****4242
    email=mask_email(user.email),       # j***n@e***.com
    amount=amount
)
```

### Appropriate Detail Levels

**Too much detail:**
```python
# Bad - logs entire objects
logger.info("user_data", user=user.__dict__)  # Might include password!
logger.debug("request_body", body=request.json())  # Could be huge
```

**Right amount:**
```python
# Good - relevant fields only
logger.info("user_created", user_id=user.id, email=mask_email(user.email))
logger.debug("request_received", path=request.path, content_length=len(request.body))
```

---

## 4. Request Tracing

### Correlation IDs

Track requests across services:

```python
import uuid
from contextvars import ContextVar

# Context variable for request ID
request_id_var: ContextVar[str] = ContextVar('request_id', default=None)

class RequestContextMiddleware:
    """Middleware to set up request context."""

    async def __call__(self, request, call_next):
        # Get or generate request ID
        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        request_id_var.set(request_id)

        # Bind to logger
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response = await call_next(request)

        # Include in response
        response.headers['X-Request-ID'] = request_id

        return response

# All logs automatically include request_id
logger.info("processing_order")  # {"request_id": "abc-123", "message": "processing_order"}
```

### Distributed Tracing

For microservices, propagate trace context:

```python
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

propagator = TraceContextTextMapPropagator()
tracer = trace.get_tracer(__name__)

async def call_external_service(url: str, data: dict) -> dict:
    """Call external service with trace propagation."""
    with tracer.start_as_current_span("external_call") as span:
        span.set_attribute("http.url", url)

        # Inject trace context into headers
        headers = {}
        propagator.inject(headers)

        # Log with trace context
        logger.info(
            "external_call_started",
            url=url,
            trace_id=span.get_span_context().trace_id
        )

        response = await http_client.post(url, json=data, headers=headers)

        logger.info(
            "external_call_completed",
            url=url,
            status_code=response.status_code,
            duration_ms=response.elapsed.total_seconds() * 1000
        )

        return response.json()
```

---

## 5. Performance Considerations

### Lazy Evaluation

Avoid expensive operations when log level is disabled:

**Bad: Always evaluated**
```python
# expensive_operation() runs even if DEBUG is disabled
logger.debug(f"Data: {expensive_operation()}")
```

**Good: Lazy evaluation**
```python
# Only evaluates if DEBUG is enabled
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("data", result=expensive_operation())

# Or use lazy formatting
logger.debug("data", result=lambda: expensive_operation())
```

### Async Logging

For high-throughput systems, use async logging:

```python
import asyncio
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler

async def setup_async_logger():
    logger = Logger.with_default_handlers(name='async-app')
    handler = AsyncFileHandler(filename='app.log')
    logger.add_handler(handler)
    return logger

# Logs don't block the event loop
await logger.info("high_throughput_event", count=1000000)
```

### Log Sampling

For very high-volume events:

```python
import random

class SampledLogger:
    """Logger that samples high-frequency events."""

    def __init__(self, logger, sample_rate: float = 0.1):
        self.logger = logger
        self.sample_rate = sample_rate

    def sampled_info(self, message: str, **kwargs):
        """Log with sampling - only logs sample_rate % of calls."""
        if random.random() < self.sample_rate:
            kwargs['_sampled'] = True
            kwargs['_sample_rate'] = self.sample_rate
            self.logger.info(message, **kwargs)

sampled_logger = SampledLogger(logger, sample_rate=0.01)  # 1% sampling

# High-frequency event - only logs ~1% of calls
sampled_logger.sampled_info("page_view", page="/home", user_id=user.id)
```

---

## 6. Log Aggregation Patterns

### Structured Log Format

Output format for log aggregators (ELK, Datadog, etc.):

```python
import json
from datetime import datetime, timezone

def json_log_formatter(record):
    """Format log record as JSON for aggregation."""
    return json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": record.levelname.lower(),
        "logger": record.name,
        "message": record.getMessage(),
        "service": "my-service",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": os.getenv("APP_VERSION", "unknown"),
        # Include any extra fields
        **getattr(record, 'extra', {})
    })
```

### Log Enrichment

Add context automatically:

```python
import platform
import os

class LogEnricher:
    """Enrich logs with environment context."""

    @staticmethod
    def get_base_context() -> dict:
        return {
            "service": os.getenv("SERVICE_NAME", "unknown"),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "version": os.getenv("APP_VERSION", "unknown"),
            "host": platform.node(),
            "pid": os.getpid(),
        }

# Configure structlog with enrichment
structlog.configure(
    processors=[
        # Add base context to all logs
        structlog.processors.add_log_level,
        lambda _, __, event_dict: {**LogEnricher.get_base_context(), **event_dict},
        structlog.processors.JSONRenderer(),
    ]
)
```

---

## 7. Application Lifecycle Logging

### Startup Logging

```python
logger.info(
    "application_starting",
    version=APP_VERSION,
    environment=ENVIRONMENT,
    config={
        "database_host": mask_host(DB_HOST),
        "cache_enabled": CACHE_ENABLED,
        "feature_flags": FEATURE_FLAGS,
    }
)

# After initialization
logger.info(
    "application_ready",
    startup_time_ms=startup_duration,
    database_connected=True,
    cache_connected=True,
)
```

### Shutdown Logging

```python
import signal
import asyncio

async def graceful_shutdown(sig: signal.Signals):
    logger.info("shutdown_initiated", signal=sig.name)

    # Log active connections/tasks
    logger.info(
        "shutdown_status",
        active_requests=len(active_requests),
        pending_tasks=len(pending_tasks),
    )

    # Wait for graceful completion
    await asyncio.gather(*pending_tasks, return_exceptions=True)

    logger.info("shutdown_complete", graceful=True)

# Register signal handlers
for sig in (signal.SIGTERM, signal.SIGINT):
    signal.signal(sig, lambda s, f: asyncio.create_task(graceful_shutdown(s)))
```

### Health Check Logging

```python
@app.get("/health")
async def health_check():
    health_status = {
        "database": await check_database(),
        "cache": await check_cache(),
        "external_api": await check_external_api(),
    }

    all_healthy = all(health_status.values())

    # Only log if unhealthy (avoid log noise)
    if not all_healthy:
        logger.warning("health_check_degraded", status=health_status)

    return {"status": "healthy" if all_healthy else "degraded", "checks": health_status}
```

---

## 8. Common Patterns

### Request/Response Logging

```python
class RequestLoggingMiddleware:
    """Log all requests and responses."""

    async def __call__(self, request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Log request
        logger.info(
            "request_started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            user_agent=request.headers.get("user-agent"),
            client_ip=request.client.host,
        )

        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000

            # Log response
            logger.info(
                "request_completed",
                request_id=request_id,
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

            return response

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            logger.error(
                "request_failed",
                request_id=request_id,
                error_type=type(e).__name__,
                error_message=str(e),
                duration_ms=round(duration_ms, 2),
                exc_info=True,
            )
            raise
```

### Database Query Logging

```python
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - conn.info['query_start_time'].pop()

    # Log slow queries
    if total_time > 1.0:  # > 1 second
        logger.warning(
            "slow_query",
            query=statement[:500],  # Truncate long queries
            duration_ms=round(total_time * 1000, 2),
            parameters=str(parameters)[:200],  # Truncate params
        )
```

### External API Logging

```python
class LoggedHttpClient:
    """HTTP client with automatic logging."""

    def __init__(self, base_url: str, service_name: str):
        self.base_url = base_url
        self.service_name = service_name
        self.client = httpx.AsyncClient()

    async def request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> httpx.Response:
        url = f"{self.base_url}{path}"
        start_time = time.time()

        logger.debug(
            "external_request_started",
            service=self.service_name,
            method=method,
            path=path,
        )

        try:
            response = await self.client.request(method, url, **kwargs)
            duration_ms = (time.time() - start_time) * 1000

            log_level = "info" if response.is_success else "warning"
            getattr(logger, log_level)(
                "external_request_completed",
                service=self.service_name,
                method=method,
                path=path,
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

            return response

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            logger.error(
                "external_request_failed",
                service=self.service_name,
                method=method,
                path=path,
                error_type=type(e).__name__,
                error_message=str(e),
                duration_ms=round(duration_ms, 2),
            )
            raise
```

---

## 9. Testing Logging

### Capture Logs in Tests

```python
import pytest
import structlog
from structlog.testing import capture_logs

def test_order_creation_logs_event():
    """Verify order creation produces correct log."""
    with capture_logs() as cap_logs:
        order = create_order(customer_id="cust_123", items=[...])

    # Verify log was produced
    assert len(cap_logs) == 1
    assert cap_logs[0]["event"] == "order_created"
    assert cap_logs[0]["order_id"] == order.id
    assert cap_logs[0]["customer_id"] == "cust_123"
    assert cap_logs[0]["log_level"] == "info"

def test_no_sensitive_data_in_logs():
    """Verify sensitive data is not logged."""
    with capture_logs() as cap_logs:
        process_payment(
            card_number="4242424242424242",
            email="user@example.com"
        )

    log_output = str(cap_logs)

    # Verify sensitive data is masked
    assert "4242424242424242" not in log_output
    assert "user@example.com" not in log_output
    assert "****4242" in log_output  # Masked card
```

### Log Level Assertions

```python
def test_error_on_failure():
    """Verify errors produce ERROR level log."""
    with capture_logs() as cap_logs:
        with pytest.raises(PaymentError):
            process_payment(invalid_data)

    error_logs = [l for l in cap_logs if l["log_level"] == "error"]
    assert len(error_logs) == 1
    assert error_logs[0]["event"] == "payment_failed"
```

---

## Quick Reference: Logging Checklist

### Setup
- [ ] Structured logging configured (JSON output)
- [ ] Log levels set appropriately per environment
- [ ] Request ID propagation enabled
- [ ] Base context (service, version, environment) included

### What to Log
- [ ] All state changes (create, update, delete)
- [ ] External service calls (start, complete, fail)
- [ ] Authentication events
- [ ] Errors with context and stack traces
- [ ] Performance metrics (duration, counts)

### What NOT to Log
- [ ] Passwords or secrets
- [ ] Full credit card numbers
- [ ] Personal identifiable information (PII)
- [ ] Session tokens or API keys
- [ ] Large payloads (log size only)

### Log Levels
- [ ] DEBUG: Development details
- [ ] INFO: Business events
- [ ] WARNING: Recoverable issues
- [ ] ERROR: Failures
- [ ] CRITICAL: System-wide issues

### Performance
- [ ] Lazy evaluation for expensive operations
- [ ] Async logging for high throughput
- [ ] Sampling for very high frequency events
- [ ] Log rotation configured

---

Good logging is the difference between "something went wrong" and "user X's payment failed at step Y because of Z at timestamp T". Invest in logging infrastructure early, and debugging production issues becomes forensics rather than guesswork.


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

