---
last_updated: 2026-02-25
status: active
name: logging-observability
description: Implement effective logging and observability for debugging and monitoring. Activate when adding logs, traces, or metrics to applications.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["logging", "observability", "monitoring", "tracing", "metrics", "debug", "telemetry", "structured logging"]
allowed-tools: Read, Write, Edit
---

# Logging & Observability

Build observable systems that are easy to debug, monitor, and maintain. This skill covers logging best practices, distributed tracing, and metrics.

## Three Pillars of Observability

| Pillar | Purpose | Example |
|--------|---------|---------|
| **Logs** | Discrete events | "User 123 logged in" |
| **Metrics** | Aggregated measurements | "99th percentile latency: 250ms" |
| **Traces** | Request flow across services | "Request took 500ms: API→DB→Cache→API" |

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Logging Best Practices

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed diagnostic info | Variable values, loop iterations |
| **INFO** | Normal operations | Request handled, job completed |
| **WARNING** | Unexpected but handled | Retry succeeded, deprecated API |
| **ERROR** | Operation failed | Request failed, exception caught |
| **CRITICAL** | System is broken | Database down, disk full |

### What to Log

| Do Log | Don't Log |
|--------|-----------|
| Request/response (sanitized) | Passwords, tokens, PII |
| Operation start/end | High-frequency loops |
| Decision points | Redundant information |
| Error context | Stack traces for handled errors |
| External calls | Internal function calls (usually) |

### Structured Logging

```python
import logging
import json

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def info(self, message, **context):
        self.logger.info(json.dumps({
            "message": message,
            **context
        }))

logger = StructuredLogger(__name__)

# Instead of:
logger.info(f"User {user_id} logged in from {ip}")

# Use:
logger.info("User logged in", user_id=user_id, ip=ip, method="oauth")
```

**Output:**
```json
{"message": "User logged in", "user_id": "123", "ip": "10.0.0.1", "method": "oauth"}
```

### Contextual Logging

Add request context to all logs.

```python
import contextvars
import uuid

request_id_var = contextvars.ContextVar('request_id', default=None)

class RequestContextFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get() or 'no-request'
        return True

# Middleware sets context
def middleware(request, next):
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request_id_var.set(request_id)
    return next(request)
```

---

## 2. Logging Patterns

### Request Logging

```python
import time

def log_request(handler):
    async def wrapper(request):
        start = time.perf_counter()

        logger.info("Request started",
            method=request.method,
            path=request.path,
            request_id=request.id
        )

        try:
            response = await handler(request)
            duration = time.perf_counter() - start

            logger.info("Request completed",
                method=request.method,
                path=request.path,
                status=response.status,
                duration_ms=round(duration * 1000, 2),
                request_id=request.id
            )

            return response
        except Exception as e:
            duration = time.perf_counter() - start

            logger.error("Request failed",
                method=request.method,
                path=request.path,
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=round(duration * 1000, 2),
                request_id=request.id,
                exc_info=True
            )
            raise

    return wrapper
```

### Operation Logging

```python
from contextlib import contextmanager

@contextmanager
def log_operation(operation_name, **context):
    """Log operation with timing and error handling."""
    start = time.perf_counter()

    logger.info(f"Starting {operation_name}", **context)

    try:
        yield
        duration = time.perf_counter() - start
        logger.info(f"Completed {operation_name}",
            duration_ms=round(duration * 1000, 2),
            **context
        )
    except Exception as e:
        duration = time.perf_counter() - start
        logger.error(f"Failed {operation_name}",
            error=str(e),
            error_type=type(e).__name__,
            duration_ms=round(duration * 1000, 2),
            **context,
            exc_info=True
        )
        raise

# Usage
with log_operation("payment_processing", order_id=order.id, amount=order.total):
    process_payment(order)
```

### Error Context

```python
def process_order(order):
    try:
        validate_order(order)
        charge_payment(order)
        fulfill_order(order)
    except Exception as e:
        # Add context before re-raising
        logger.error("Order processing failed",
            order_id=order.id,
            customer_id=order.customer_id,
            items_count=len(order.items),
            total=order.total,
            step="unknown",  # Could track current step
            exc_info=True
        )
        raise
```

---

## 3. Distributed Tracing

### Concepts

| Concept | Definition |
|---------|------------|
| **Trace** | Full journey of a request |
| **Span** | Single operation within a trace |
| **Context** | Trace ID, Span ID passed between services |

### Manual Tracing

```python
import uuid
from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class Span:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation: str
    start_time: float
    end_time: Optional[float] = None
    tags: dict = None

class Tracer:
    def __init__(self):
        self.spans = []

    def start_span(self, operation, parent=None):
        trace_id = parent.trace_id if parent else str(uuid.uuid4())
        span = Span(
            trace_id=trace_id,
            span_id=str(uuid.uuid4()),
            parent_span_id=parent.span_id if parent else None,
            operation=operation,
            start_time=time.time()
        )
        return span

    def end_span(self, span):
        span.end_time = time.time()
        self.spans.append(span)
        return span

# Usage
tracer = Tracer()
root_span = tracer.start_span("handle_request")

db_span = tracer.start_span("database_query", parent=root_span)
result = db.query(...)
tracer.end_span(db_span)

tracer.end_span(root_span)
```

### Context Propagation

```python
# HTTP headers for trace context
TRACE_HEADERS = {
    "X-Trace-ID": trace_id,
    "X-Span-ID": span_id,
    "X-Parent-Span-ID": parent_span_id
}

# Extract in receiving service
def extract_trace_context(request):
    return TraceContext(
        trace_id=request.headers.get("X-Trace-ID"),
        parent_span_id=request.headers.get("X-Span-ID")
    )
```

---

## 4. Metrics

### Types of Metrics

| Type | Use Case | Example |
|------|----------|---------|
| **Counter** | Cumulative count | Requests, errors |
| **Gauge** | Current value | Queue size, connections |
| **Histogram** | Distribution | Request latency |

### Key Metrics (RED Method)

| Metric | Definition |
|--------|------------|
| **Rate** | Requests per second |
| **Errors** | Failed requests per second |
| **Duration** | Latency distribution |

### Implementation

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

# Use in middleware
def metrics_middleware(handler):
    async def wrapper(request):
        ACTIVE_CONNECTIONS.inc()
        start = time.perf_counter()

        try:
            response = await handler(request)
            status = response.status
            return response
        except Exception:
            status = 500
            raise
        finally:
            duration = time.perf_counter() - start
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path,
                status=status
            ).inc()
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.path
            ).observe(duration)
            ACTIVE_CONNECTIONS.dec()

    return wrapper
```

---

## 5. Log Management

### Log Aggregation

```yaml
# Typical setup
Application → Fluentd/Logstash → Elasticsearch → Kibana

# Or cloud-native
Application → CloudWatch Logs / Stackdriver / Datadog
```

### Log Retention

| Environment | Retention | Reason |
|-------------|-----------|--------|
| Development | 7 days | Short-term debugging |
| Staging | 30 days | Release validation |
| Production | 90+ days | Compliance, analysis |

### Sampling High-Volume Logs

```python
import random

class SampledLogger:
    def __init__(self, logger, sample_rate=0.1):
        self.logger = logger
        self.sample_rate = sample_rate

    def debug(self, message, **kwargs):
        if random.random() < self.sample_rate:
            kwargs['sampled'] = True
            self.logger.debug(message, **kwargs)
```

---

## 6. Debugging with Logs

### Finding Issues

```bash
# Find errors in time window
grep "ERROR" app.log | grep "2024-01-15T14"

# Find all logs for a request
grep "request_id=abc123" app.log

# Find slow requests
jq 'select(.duration_ms > 1000)' app.log
```

### Correlation

```python
# Log with correlation IDs
logger.info("Order created",
    order_id=order.id,
    customer_id=customer.id,
    session_id=session.id,
    request_id=request.id
)

# Now can trace:
# - All actions for this order
# - All actions for this customer
# - All actions in this session
# - All actions in this request
```

---

## Quick Reference

### Logging Checklist

- [ ] Using appropriate log levels?
- [ ] Structured logging with JSON?
- [ ] Request IDs in all logs?
- [ ] Sensitive data excluded?
- [ ] Start/end of operations logged?
- [ ] Errors include context?
- [ ] Logs searchable/aggregated?

### What to Include in Logs

| Always | When Relevant | Never |
|--------|---------------|-------|
| Timestamp | User ID | Passwords |
| Log level | Request ID | Auth tokens |
| Message | Duration | Credit cards |
| Service name | Error details | PII |

### Log Format Template

```
{
  "timestamp": "ISO8601",
  "level": "INFO|ERROR|etc",
  "message": "Human-readable description",
  "service": "service-name",
  "request_id": "uuid",
  "user_id": "if relevant",
  "duration_ms": "if operation",
  "error": "if error",
  "...context": "additional fields"
}
```

Log for humans to read and machines to parse. Add context generously. Correlate across services.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

