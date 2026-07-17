---
last_updated: 2026-02-25
status: active
name: resilience-patterns
description: Patterns for building systems that handle failures gracefully. Use for fault tolerance, recovery strategies, and chaos engineering decisions.
triggers:
  files: ["**/resilience/**", "**/fault-tolerance/**", "**/retry/**", "**/circuit-breaker/**"]
  keywords: ["resilience", "fault tolerance", "circuit breaker", "retry", "fallback", "bulkhead", "timeout", "graceful degradation", "chaos engineering", "disaster recovery", "failover"]
allowed-tools: Read, Write, Edit
---

# Resilience Patterns

## Overview

Resilience is the ability of a system to handle and recover from failures. In distributed systems, failures are not exceptional—they are inevitable. Networks partition, servers crash, disks fill up, and dependencies become unavailable.

Resilient systems are designed with the assumption that things will fail. They detect failures quickly, contain their impact, and recover gracefully. The goal is not to prevent all failures but to ensure the system continues providing value when failures occur.

This skill covers patterns for building resilient systems, including fault tolerance, graceful degradation, and recovery strategies.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Principles

### 1. Embrace Failure

Design with the expectation that components will fail.

**Mindset shift:**
- Not "if the database fails" but "when the database fails"
- Not "the network is reliable" but "the network will partition"
- Not "services are always available" but "services will be unavailable"

### 2. Fail Fast

Detect and report failures quickly rather than waiting.

```python
# BAD: Slow failure (default timeout might be 30+ seconds)
response = requests.get(url)

# GOOD: Fail fast with explicit timeout
response = requests.get(url, timeout=3)
```

### 3. Contain Failures

Prevent failures from cascading through the system.

```
┌─────────────────────────────────────────────────────┐
│                Without Isolation                     │
│    Service A fails → Service B fails → C fails      │
│                    Cascade failure                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 With Isolation                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │Service A│  │Service B│  │Service C│            │
│  │ (fails) │  │(isolated│  │(isolated│            │
│  └─────────┘  │  works) │  │  works) │            │
│               └─────────┘  └─────────┘            │
└─────────────────────────────────────────────────────┘
```

### 4. Design for Recovery

Systems should recover automatically when possible.

**Recovery hierarchy:**
1. Self-healing (automatic retry, failover)
2. Assisted recovery (human intervention with tools)
3. Manual recovery (last resort)

---

## Timeout Patterns

### Connection and Read Timeouts

```python
import httpx

client = httpx.Client(
    timeout=httpx.Timeout(
        connect=5.0,    # Time to establish connection
        read=10.0,      # Time to read response
        write=5.0,      # Time to send request
        pool=5.0,       # Time to acquire connection from pool
    )
)
```

### Timeout Guidelines

| Operation | Typical Timeout |
|-----------|----------------|
| Database query | 5-30 seconds |
| External API call | 5-15 seconds |
| Internal service call | 1-5 seconds |
| Cache lookup | 100-500 ms |

### Timeout Budget

Track remaining time across chained calls.

```python
from datetime import datetime, timedelta

class TimeoutBudget:
    def __init__(self, total_seconds: float):
        self.deadline = datetime.now() + timedelta(seconds=total_seconds)

    def remaining(self) -> float:
        remaining = (self.deadline - datetime.now()).total_seconds()
        if remaining <= 0:
            raise TimeoutError("Budget exhausted")
        return remaining

# Usage
budget = TimeoutBudget(10.0)  # 10 second total budget

# First call
user = user_service.get(user_id, timeout=budget.remaining())

# Second call uses remaining budget
orders = order_service.get_by_user(user_id, timeout=budget.remaining())
```

---

## Retry Patterns

### Simple Retry

```python
def retry_simple(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return func()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
```

### Exponential Backoff

Increase delay between retries to avoid overwhelming failing service.

```python
import random
import time

def retry_with_backoff(
    func,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
):
    for attempt in range(max_attempts):
        try:
            return func()
        except TransientError as e:
            if attempt == max_attempts - 1:
                raise

            # Exponential delay: 1s, 2s, 4s, 8s, ...
            delay = min(base_delay * (2 ** attempt), max_delay)

            # Add jitter to prevent thundering herd
            if jitter:
                delay = delay * (0.5 + random.random())

            time.sleep(delay)
```

### Retry with Decorrelation

Spread out retry times to reduce contention.

```python
def retry_decorrelated_jitter(
    func,
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0
):
    delay = base_delay
    for attempt in range(max_attempts):
        try:
            return func()
        except TransientError:
            if attempt == max_attempts - 1:
                raise

            # Decorrelated jitter
            delay = min(max_delay, random.uniform(base_delay, delay * 3))
            time.sleep(delay)
```

### Retry Policies

```python
from dataclasses import dataclass
from typing import Tuple, Type

@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential: bool = True
    jitter: bool = True
    retryable_exceptions: Tuple[Type[Exception], ...] = (TransientError,)

    def should_retry(self, exception: Exception, attempt: int) -> bool:
        if attempt >= self.max_attempts:
            return False
        return isinstance(exception, self.retryable_exceptions)

    def get_delay(self, attempt: int) -> float:
        if self.exponential:
            delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        else:
            delay = self.base_delay

        if self.jitter:
            delay *= (0.5 + random.random())

        return delay


# Different policies for different operations
AGGRESSIVE_RETRY = RetryPolicy(max_attempts=5, base_delay=0.1)
CONSERVATIVE_RETRY = RetryPolicy(max_attempts=3, base_delay=2.0)
```

### When NOT to Retry

**Non-retryable errors:**
- 400 Bad Request (client error, won't succeed on retry)
- 401/403 Authentication/Authorization errors
- 404 Not Found
- Business logic failures

**Idempotency requirement:**
```python
def create_order(order: Order) -> str:
    # BAD: Retry might create duplicate orders
    return api.post("/orders", order)

# GOOD: Use idempotency key
def create_order(order: Order, idempotency_key: str) -> str:
    return api.post(
        "/orders",
        order,
        headers={"Idempotency-Key": idempotency_key}
    )
```

---

## Circuit Breaker Pattern

Prevent repeated failures by temporarily stopping calls to failing service.

### States

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   ┌──────────┐  failures >= threshold   ┌──────────┐               │
│   │  CLOSED  │─────────────────────────►│   OPEN   │               │
│   │(normal)  │                          │(failing) │               │
│   └──────────┘                          └────┬─────┘               │
│        ▲                                     │                      │
│        │                            timeout expires                │
│        │ success                             │                      │
│        │                                     ▼                      │
│   ┌────┴─────┐                        ┌───────────┐                │
│   │          │◄───────────────────────┤ HALF-OPEN │                │
│   │          │      trial success     │ (testing) │                │
│   └──────────┘                        └───────────┘                │
│                                              │                      │
│                         trial failure        │                      │
│                         └────────────────────┼──────►OPEN          │
└────────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
from datetime import datetime
from enum import Enum
from threading import Lock

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._half_open_calls = 0
        self._lock = Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_calls = 0
            return self._state

    def _should_attempt_reset(self) -> bool:
        return (
            self._last_failure_time and
            (datetime.now() - self._last_failure_time).total_seconds()
            >= self.recovery_timeout
        )

    def call(self, func, *args, **kwargs):
        state = self.state

        if state == CircuitState.OPEN:
            raise CircuitOpenError("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        with self._lock:
            self._failure_count = 0
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1
                if self._half_open_calls >= self.half_open_max_calls:
                    self._state = CircuitState.CLOSED

    def _on_failure(self):
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = datetime.now()

            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
            elif self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN


# Usage
payment_circuit = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

def process_payment(payment):
    return payment_circuit.call(payment_gateway.charge, payment)
```

### Circuit Breaker with Fallback

```python
def get_product_recommendations(user_id: str) -> List[Product]:
    try:
        return recommendation_circuit.call(
            recommendation_service.get,
            user_id
        )
    except CircuitOpenError:
        # Fallback to cached/generic recommendations
        return get_popular_products()
```

---

## Bulkhead Pattern

Isolate components to contain failures.

### Thread Pool Isolation

```python
from concurrent.futures import ThreadPoolExecutor

class BulkheadedService:
    def __init__(self):
        # Separate thread pools for different operations
        self.critical_pool = ThreadPoolExecutor(
            max_workers=20,
            thread_name_prefix="critical"
        )
        self.non_critical_pool = ThreadPoolExecutor(
            max_workers=5,
            thread_name_prefix="non_critical"
        )

    def critical_operation(self, func, *args):
        """Important operations get dedicated resources."""
        future = self.critical_pool.submit(func, *args)
        return future.result(timeout=10)

    def non_critical_operation(self, func, *args):
        """Less important operations isolated from critical path."""
        future = self.non_critical_pool.submit(func, *args)
        return future.result(timeout=30)
```

### Semaphore Isolation

```python
import asyncio

class SemaphoreBulkhead:
    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(self, coro):
        acquired = await asyncio.wait_for(
            self.semaphore.acquire(),
            timeout=5.0  # Wait at most 5s for slot
        )
        try:
            return await coro
        finally:
            self.semaphore.release()


# Usage
payment_bulkhead = SemaphoreBulkhead(max_concurrent=10)
inventory_bulkhead = SemaphoreBulkhead(max_concurrent=20)

async def process_order(order):
    # Each service has its own concurrency limit
    payment = await payment_bulkhead.execute(
        process_payment(order.payment)
    )
    inventory = await inventory_bulkhead.execute(
        reserve_inventory(order.items)
    )
```

### Service Isolation

```
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   ┌─────────┐         ┌─────────┐         ┌─────────┐
   │Critical │         │ Normal  │         │  Batch  │
   │ Traffic │         │ Traffic │         │  Jobs   │
   │   Pod   │         │   Pod   │         │   Pod   │
   │ (10 CPU)│         │ (4 CPU) │         │ (2 CPU) │
   └─────────┘         └─────────┘         └─────────┘

   Kubernetes resource limits enforce isolation.
   Batch jobs can't starve critical traffic.
```

---

## Fallback Patterns

### Static Fallback

Return cached or default data.

```python
FALLBACK_PRODUCTS = [
    Product(id="default-1", name="Popular Item 1"),
    Product(id="default-2", name="Popular Item 2"),
]

def get_recommendations(user_id: str) -> List[Product]:
    try:
        return recommendation_service.get(user_id)
    except ServiceUnavailableError:
        return FALLBACK_PRODUCTS
```

### Cached Fallback

Return stale cached data when fresh data unavailable.

```python
def get_product(product_id: str) -> Product:
    cache_key = f"product:{product_id}"

    # Try fresh data
    try:
        product = product_service.get(product_id)
        cache.set(cache_key, product, ttl=300)
        return product
    except ServiceUnavailableError:
        # Fall back to cached (potentially stale) data
        cached = cache.get(cache_key)
        if cached:
            return cached
        raise  # No fallback available
```

### Graceful Degradation

Provide reduced functionality instead of total failure.

```python
def render_product_page(product_id: str) -> Page:
    product = product_service.get(product_id)  # Required

    # Optional: Reviews (fail gracefully)
    try:
        reviews = review_service.get(product_id, timeout=2)
    except Exception:
        reviews = []  # Show page without reviews

    # Optional: Recommendations (fail gracefully)
    try:
        recommendations = recommendation_service.get(product_id, timeout=2)
    except Exception:
        recommendations = []  # Show page without recommendations

    return Page(
        product=product,
        reviews=reviews,
        recommendations=recommendations
    )
```

### Feature Flags for Degradation

```python
class FeatureFlags:
    def __init__(self):
        self.flags = {
            "recommendations_enabled": True,
            "real_time_inventory": True,
            "video_streaming": True,
        }

    def is_enabled(self, feature: str) -> bool:
        return self.flags.get(feature, False)

    def disable(self, feature: str):
        """Emergency kill switch."""
        self.flags[feature] = False

# During incident
flags.disable("recommendations_enabled")  # Reduce load
flags.disable("video_streaming")  # Reduce bandwidth
```

---

## Health Checks

### Liveness vs Readiness

**Liveness:** Is the process alive?
- If false: Restart the container
- Should be fast and simple
- Avoid checking dependencies

```python
@app.get("/health/live")
def liveness():
    return {"status": "alive"}
```

**Readiness:** Can the service handle traffic?
- If false: Remove from load balancer
- Check critical dependencies
- Should recover when dependencies recover

```python
@app.get("/health/ready")
def readiness():
    try:
        # Check critical dependencies
        database.execute("SELECT 1")
        redis.ping()
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}, 503
```

### Deep Health Checks

```python
@app.get("/health/deep")
def deep_health():
    """Comprehensive health check for monitoring."""
    checks = {}

    # Database
    try:
        start = time.time()
        database.execute("SELECT 1")
        checks["database"] = {
            "status": "healthy",
            "latency_ms": (time.time() - start) * 1000
        }
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}

    # Cache
    try:
        start = time.time()
        redis.ping()
        checks["cache"] = {
            "status": "healthy",
            "latency_ms": (time.time() - start) * 1000
        }
    except Exception as e:
        checks["cache"] = {"status": "unhealthy", "error": str(e)}

    # External service
    try:
        start = time.time()
        payment_service.health_check()
        checks["payment_service"] = {
            "status": "healthy",
            "latency_ms": (time.time() - start) * 1000
        }
    except Exception as e:
        checks["payment_service"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    overall_healthy = all(
        c["status"] == "healthy" for c in checks.values()
    )

    return {
        "status": "healthy" if overall_healthy else "degraded",
        "checks": checks
    }, 200 if overall_healthy else 503
```

---

## Rate Limiting

Protect services from being overwhelmed.

### Token Bucket

```python
import time
from threading import Lock

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # Tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = Lock()

    def acquire(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.time()
            # Add tokens based on time elapsed
            elapsed = now - self.last_update
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


# Usage
rate_limiter = TokenBucket(rate=100, capacity=200)  # 100/s, burst of 200

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    if not rate_limiter.acquire():
        return Response(status_code=429, content="Rate limit exceeded")
    return await call_next(request)
```

### Sliding Window

```python
import redis
import time

class SlidingWindowRateLimiter:
    def __init__(self, redis_client, limit: int, window_seconds: int):
        self.redis = redis_client
        self.limit = limit
        self.window = window_seconds

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window

        pipe = self.redis.pipeline()
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)
        # Add current request
        pipe.zadd(key, {str(now): now})
        # Count requests in window
        pipe.zcard(key)
        # Set expiry
        pipe.expire(key, self.window)

        results = pipe.execute()
        count = results[2]

        return count <= self.limit


# Usage
limiter = SlidingWindowRateLimiter(redis, limit=100, window_seconds=60)

@app.get("/api/resource")
def get_resource(user_id: str):
    if not limiter.is_allowed(f"rate_limit:{user_id}"):
        raise HTTPException(429, "Rate limit exceeded")
    return {"data": "..."}
```

### Rate Limit Headers

```python
@app.middleware("http")
async def rate_limit_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-RateLimit-Limit"] = str(rate_limiter.limit)
    response.headers["X-RateLimit-Remaining"] = str(rate_limiter.remaining)
    response.headers["X-RateLimit-Reset"] = str(rate_limiter.reset_time)

    return response
```

---

## Disaster Recovery

### Recovery Point Objective (RPO)

Maximum acceptable data loss in time.

```
RPO = 1 hour
└── Can lose up to 1 hour of data

Strategies:
- RPO = 0: Synchronous replication
- RPO = minutes: Asynchronous replication
- RPO = hours: Periodic backups
```

### Recovery Time Objective (RTO)

Maximum acceptable downtime.

```
RTO = 4 hours
└── Must recover within 4 hours

Strategies:
- RTO = minutes: Hot standby, auto-failover
- RTO = hours: Warm standby, manual failover
- RTO = days: Cold standby, restore from backup
```

### Backup Strategies

```
┌─────────────────────────────────────────────────────────────────┐
│                       Backup Strategy                            │
├─────────────────────────────────────────────────────────────────┤
│  Full Backup (weekly)                                           │
│  ├── Differential (daily) - changes since last full            │
│  │   ├── Incremental (hourly) - changes since last backup     │
│  │   ├── Incremental                                           │
│  │   └── Incremental                                           │
│  ├── Differential                                               │
│  │   ├── Incremental                                           │
│  │   └── Incremental                                           │
└─────────────────────────────────────────────────────────────────┘
```

### Multi-Region Deployment

```
┌─────────────────────┐         ┌─────────────────────┐
│    Region A (Primary)│         │  Region B (Standby) │
│   ┌───────────────┐ │  sync   │ ┌───────────────┐   │
│   │   App Servers │ │ ◄──────►│ │   App Servers │   │
│   └───────────────┘ │         │ └───────────────┘   │
│   ┌───────────────┐ │  async  │ ┌───────────────┐   │
│   │   Database    │ │ ───────►│ │   Database    │   │
│   │   (Primary)   │ │ replicate│ │   (Replica)   │   │
│   └───────────────┘ │         │ └───────────────┘   │
└─────────────────────┘         └─────────────────────┘
            │
            │ failover
            ▼
┌─────────────────────────────────────────────────────┐
│               Global Load Balancer                   │
│   Routes traffic to healthy region                  │
└─────────────────────────────────────────────────────┘
```

---

## Chaos Engineering

Proactively test system resilience by injecting failures.

### Principles

1. **Start with a hypothesis**: "The system should survive if Service X fails"
2. **Introduce controlled failures**: Kill instances, inject latency
3. **Observe behavior**: Does the system degrade gracefully?
4. **Learn and improve**: Fix weaknesses discovered

### Common Experiments

```python
# Experiment 1: Kill random instances
def chaos_kill_instance():
    instances = get_running_instances()
    victim = random.choice(instances)
    terminate_instance(victim)
    # Verify system still works

# Experiment 2: Inject network latency
def chaos_network_delay(service: str, delay_ms: int):
    inject_latency(service, delay_ms)
    # Verify timeouts work correctly

# Experiment 3: Fail external dependency
def chaos_dependency_failure(service: str):
    block_traffic(service)
    # Verify fallbacks activate

# Experiment 4: Resource exhaustion
def chaos_cpu_stress(percentage: int):
    stress_cpu(percentage)
    # Verify system degrades gracefully
```

### Chaos Monkey (Netflix)

```yaml
# Simian Army configuration
chaos_monkey:
  enabled: true
  probability: 0.1  # 10% chance per instance per day
  schedule:
    start: "09:00"
    end: "17:00"  # Only during business hours
  excluded_groups:
    - critical-infrastructure
    - databases
```

### Game Days

Scheduled chaos exercises with the team.

```
Game Day Runbook:
1. Pre-game: Brief team, ensure rollback procedures ready
2. Inject failure: [specific failure scenario]
3. Observe: Monitor dashboards, alerts
4. Recover: Fix or rollback
5. Post-mortem: Document learnings
```

---

## Observability for Resilience

### Key Metrics

```python
# Error rate
http_requests_total{status=~"5.."}

# Latency
http_request_duration_seconds{quantile="0.99"}

# Saturation
process_open_fds / process_max_fds

# Circuit breaker state
circuit_breaker_state{service="payment"} == 1  # 1 = open

# Retry rate
retry_attempts_total / requests_total
```

### Alerting on Resilience

```yaml
# Alert when circuit opens
- alert: CircuitBreakerOpen
  expr: circuit_breaker_state == 1
  for: 1m
  annotations:
    summary: "Circuit breaker open for {{ $labels.service }}"

# Alert on high retry rate
- alert: HighRetryRate
  expr: rate(retry_attempts_total[5m]) / rate(requests_total[5m]) > 0.1
  for: 5m
  annotations:
    summary: "High retry rate indicates upstream issues"

# Alert on degraded mode
- alert: SystemDegraded
  expr: feature_flag_enabled{name="degraded_mode"} == 1
  for: 1m
  annotations:
    summary: "System running in degraded mode"
```

---

## Anti-Patterns

### Retry Storm

Retries amplify load during failures.

```
Normal: 1000 req/s
With failure + 3 retries: 4000 req/s
└── Makes recovery harder!

Mitigation:
- Exponential backoff
- Jitter
- Circuit breaker to stop retries
- Retry budgets
```

### Cascading Timeout

Timeouts that don't account for chained calls.

```
Service A (timeout=30s) → Service B (timeout=30s) → Service C (timeout=30s)
└── Total possible wait: 90 seconds!

Solution: Timeout budget
Service A (budget=30s) → B (remaining=25s) → C (remaining=20s)
```

### Missing Fallbacks

```python
# ANTI-PATTERN: No fallback
def get_recommendations(user_id):
    return recommendation_service.get(user_id)  # If fails, error propagates

# BETTER: Graceful fallback
def get_recommendations(user_id):
    try:
        return recommendation_service.get(user_id)
    except ServiceUnavailableError:
        return get_default_recommendations()
```

### Ignoring Partial Failures

```python
# ANTI-PATTERN: All or nothing
def get_dashboard_data():
    users = user_service.get_stats()      # If fails...
    orders = order_service.get_stats()    # ...never reached
    revenue = finance_service.get_stats() # ...never reached
    return Dashboard(users, orders, revenue)

# BETTER: Independent failures
def get_dashboard_data():
    return Dashboard(
        users=safe_call(user_service.get_stats, default={}),
        orders=safe_call(order_service.get_stats, default={}),
        revenue=safe_call(finance_service.get_stats, default={}),
    )
```

---



## Quality Tests

### Trade-Off Test
- Alternatives were considered before choosing this architecture
- **PASS:** At least 2 alternative approaches evaluated with pros/cons
- **FAIL:** Architecture chosen without considering alternatives

### Scalability Test
- Architecture handles 10x current load without redesign
- **PASS:** Bottlenecks identified with specific scaling strategies
- **FAIL:** No analysis of how the system behaves under increased load

## Guidelines

### When to Apply Resilience Patterns

**Always:**
- Timeout on all external calls
- Health checks for all services
- Monitoring and alerting

**For critical paths:**
- Circuit breakers
- Retries with backoff
- Fallbacks

**For complex systems:**
- Bulkheads
- Chaos engineering
- Multi-region deployment

### How to Apply

1. **Identify failure modes**: What can go wrong?
2. **Assess impact**: What happens when it fails?
3. **Choose patterns**: Match patterns to failure modes
4. **Implement incrementally**: Start with timeouts and retries
5. **Test failures**: Chaos engineering, game days
6. **Monitor and iterate**: Learn from production incidents

### Red Flags

- No timeouts on external calls
- No health checks
- Retries without backoff
- No circuit breakers for unstable dependencies
- No fallbacks for optional features
- Never tested failure scenarios

---

## References

### Books
- *Release It!* by Michael Nygard
- *Site Reliability Engineering* by Google
- *Chaos Engineering* by Casey Rosenthal

### Libraries
- Resilience4j (Java)
- Polly (.NET)
- Tenacity (Python)
- Hystrix (Java, deprecated but influential)

### Tools
- Chaos Monkey (Netflix)
- Gremlin (commercial chaos platform)
- LitmusChaos (Kubernetes)
