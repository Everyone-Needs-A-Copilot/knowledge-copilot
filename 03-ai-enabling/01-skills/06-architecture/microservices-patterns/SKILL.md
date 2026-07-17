---
last_updated: 2026-02-25
status: active
name: microservices-patterns
description: Patterns for designing, building, and operating microservices architectures. Use for service decomposition, inter-service communication, and operational patterns.
triggers:
  files: ["**/services/**", "**/microservices/**", "**/docker-compose.yml", "**/kubernetes/**"]
  keywords: ["microservices", "service mesh", "API gateway", "service discovery", "circuit breaker", "sidecar", "strangler fig", "saga pattern", "choreography", "orchestration", "decomposition", "bounded context"]
allowed-tools: Read, Write, Edit
---

# Microservices Patterns

## Overview

Microservices architecture structures an application as a collection of loosely coupled, independently deployable services. Each service is owned by a small team, implements a specific business capability, and communicates with other services through well-defined APIs.

This architecture style emerged from the need to scale development teams, deploy services independently, and use different technologies for different parts of a system. However, microservices introduce significant operational complexity that must be managed through proper patterns and practices.

This skill covers patterns for decomposing monoliths, designing service boundaries, managing inter-service communication, and operating microservices in production.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Principles

### 1. Single Responsibility per Service

Each service should do one thing well and have a clear reason to change.

**Indicators of good boundaries:**
- Service can be explained in one sentence
- Service has clear ownership (one team)
- Service can be deployed independently
- Changes to one service rarely require changes to others

**Example:**
```
# GOOD: Focused services
├── order-service       (manages order lifecycle)
├── inventory-service   (tracks stock levels)
├── payment-service     (processes payments)
└── notification-service (sends emails/SMS)

# BAD: Overlapping responsibilities
├── order-management-service (orders + inventory + payments)
└── customer-service (customers + notifications + preferences)
```

### 2. Decentralized Data Management

Each service owns its data and exposes it only through APIs.

**Database per service:**
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Order Svc   │   │ Inventory   │   │ Customer    │
│             │   │   Service   │   │  Service    │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       ▼                 ▼                 ▼
   ┌────────┐       ┌────────┐       ┌────────┐
   │ Orders │       │ Stock  │       │ Users  │
   │   DB   │       │   DB   │       │   DB   │
   └────────┘       └────────┘       └────────┘
```

**Benefits:**
- Services can choose appropriate database technology
- Schema changes don't affect other services
- Services can scale data independently

**Challenges:**
- No cross-service joins
- Data consistency across services requires patterns (sagas, events)

### 3. Design for Failure

Assume every network call can fail. Build resilience into every interaction.

**Failure patterns to handle:**
- Service unavailable
- Network timeout
- Partial failure (some calls succeed, others fail)
- Cascading failure

### 4. Automate Everything

Manual operations don't scale with microservices.

**Automation requirements:**
- CI/CD pipelines per service
- Infrastructure as code
- Automated testing (unit, integration, contract)
- Automated deployment (blue-green, canary)
- Monitoring and alerting

---

## Service Decomposition Patterns

### Decompose by Business Capability

Align services with business functions, not technical layers.

**Business capabilities map to services:**
```
E-commerce Business Capabilities:
├── Product Management
│   └── product-catalog-service
├── Order Management
│   ├── order-service
│   └── order-fulfillment-service
├── Customer Management
│   ├── customer-service
│   └── customer-preferences-service
├── Payment Processing
│   └── payment-service
└── Shipping & Delivery
    └── shipping-service
```

**Benefits:**
- Stable boundaries (business capabilities change slowly)
- Clear ownership (maps to business teams)
- Independent evolution

### Decompose by Subdomain (DDD)

Use Domain-Driven Design to identify bounded contexts as service boundaries.

**Steps:**
1. Identify subdomains (core, supporting, generic)
2. Define bounded contexts
3. Map contexts to services

**Example:**
```
E-commerce Domain:
├── Core: Recommendation Engine → recommendation-service (custom)
├── Supporting: Order Processing → order-service (build)
├── Supporting: Inventory → inventory-service (build)
└── Generic: User Auth → auth-service (use library/SaaS)
```

### Strangler Fig Pattern

Incrementally migrate from monolith to microservices.

**Process:**
```
Phase 1: Monolith handles all traffic
┌──────────────────────────┐
│        Monolith          │
│  ┌──────────────────┐   │
│  │    All Features  │   │
│  └──────────────────┘   │
└──────────────────────────┘

Phase 2: Extract one service, route specific traffic
┌───────────────────────────────────────────┐
│                  Router                    │
└───────────────────┬───────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────────┐    ┌──────────────┐
│    Monolith      │    │  Order Svc   │
│  (remaining)     │    │  (extracted) │
└──────────────────┘    └──────────────┘

Phase 3: Continue extracting until monolith is gone
┌───────────────────────────────────────────┐
│                  Router                    │
└───────────────────┬───────────────────────┘
        ┌───────────┼───────────┬───────────┐
        ▼           ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│Order Svc │ │Inventory │ │Customer  │ │Payment   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

**Implementation tips:**
- Start with low-risk, well-understood features
- Use feature flags to route traffic
- Run old and new in parallel until confident
- Delete old code only after migration is complete

### Anti-Corruption Layer

Protect new services from legacy system models.

```
┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   Legacy     │───►│    ACL      │───►│   New        │
│   System     │    │ (Translator)│    │   Service    │
└──────────────┘    └─────────────┘    └──────────────┘
```

**Example:**
```python
# ACL translates legacy format to domain model
class LegacyOrderAdapter:
    def __init__(self, legacy_api):
        self.legacy = legacy_api

    def get_order(self, order_id: str) -> Order:
        legacy_data = self.legacy.fetch_order(order_id)
        return self._translate(legacy_data)

    def _translate(self, legacy: dict) -> Order:
        return Order(
            id=legacy['ORD_NUM'],
            customer_id=legacy['CUST_ID'],
            items=[self._translate_item(i) for i in legacy['ITEMS']],
            total=Money(legacy['TOTAL_AMT'], 'USD')
        )
```

---

## Communication Patterns

### Synchronous Communication

**REST/HTTP:**
```
┌──────────┐    HTTP GET /orders/123    ┌──────────┐
│ Service A├───────────────────────────►│ Service B│
│          │◄───────────────────────────┤          │
└──────────┘    { "id": 123, ... }      └──────────┘
```

**Pros:**
- Simple, well-understood
- Easy to debug
- Stateless

**Cons:**
- Temporal coupling (both services must be up)
- Latency adds up in call chains
- Tight coupling between services

**gRPC:**
```protobuf
service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc CreateOrder(CreateOrderRequest) returns (Order);
  rpc StreamOrderUpdates(OrderFilter) returns (stream OrderUpdate);
}
```

**Pros:**
- High performance (binary protocol, HTTP/2)
- Strongly typed contracts
- Bidirectional streaming

**Cons:**
- Less human-readable
- Requires code generation
- Browser support limited

### Asynchronous Communication

**Message Queues (point-to-point):**
```
┌──────────┐    ┌─────────────┐    ┌──────────┐
│ Producer ├───►│ Message     ├───►│ Consumer │
│          │    │ Queue       │    │          │
└──────────┘    └─────────────┘    └──────────┘
```

**Use cases:**
- Task distribution
- Load leveling
- Reliable delivery

**Pub/Sub (one-to-many):**
```
                    ┌──────────────┐
                    │  Consumer 1  │
                    └──────▲───────┘
┌──────────┐        ┌──────┴───────┐
│ Publisher├───────►│    Topic     │
└──────────┘        └──────┬───────┘
                    ┌──────▼───────┐
                    │  Consumer 2  │
                    └──────────────┘
```

**Use cases:**
- Event broadcasting
- Decoupled services
- Event sourcing

**Event-Driven Architecture:**
```python
# Publisher (Order Service)
class OrderService:
    def place_order(self, order: Order) -> None:
        self.order_repository.save(order)
        self.event_bus.publish(OrderPlaced(
            order_id=order.id,
            customer_id=order.customer_id,
            items=order.items,
            occurred_at=datetime.now()
        ))

# Subscriber (Inventory Service)
class InventoryEventHandler:
    @subscribe(OrderPlaced)
    def handle_order_placed(self, event: OrderPlaced):
        for item in event.items:
            self.inventory.reserve(item.product_id, item.quantity)

# Subscriber (Notification Service)
class NotificationEventHandler:
    @subscribe(OrderPlaced)
    def handle_order_placed(self, event: OrderPlaced):
        self.email_service.send_order_confirmation(event.customer_id, event.order_id)
```

### Request-Response vs Event-Driven

| Aspect | Request-Response | Event-Driven |
|--------|------------------|--------------|
| Coupling | Temporal (both up) | Decoupled |
| Latency | Immediate response | Eventually consistent |
| Debugging | Direct call chain | Harder to trace |
| Scalability | Limited by slowest | Independent scaling |
| Failure handling | Synchronous retry | Built-in retry |

**Guideline:** Use request-response for queries, events for commands/updates.

---

## Data Management Patterns

### Database per Service

Each service owns its data and schema.

**Benefits:**
- Independent scaling
- Technology freedom (SQL, NoSQL, graph)
- No shared schema changes

**Challenges:**
- Cross-service queries require API calls
- Data consistency is eventual

### Saga Pattern

Manage distributed transactions across services without 2PC.

**Choreography (event-based):**
```
OrderService          InventoryService         PaymentService
     │                       │                       │
     │ OrderCreated          │                       │
     │─────────────────────►│                       │
     │                       │ InventoryReserved    │
     │                       │─────────────────────►│
     │                       │                       │ PaymentCompleted
     │◄──────────────────────│◄──────────────────────│
     │                       │                       │
     │ OrderConfirmed        │                       │
```

**Orchestration (coordinator-based):**
```
┌─────────────────────────────────────────┐
│           Saga Orchestrator             │
└─────────────────────┬───────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌────────┐       ┌────────┐       ┌────────┐
│ Order  │       │Inventory│       │Payment│
│Service │       │ Service │       │Service│
└────────┘       └────────┘       └────────┘

Orchestrator:
1. Create Order (pending)
2. Reserve Inventory
3. Process Payment
4. If success: Confirm Order
5. If failure: Compensate (release inventory, cancel order)
```

**Compensation logic:**
```python
class PlaceOrderSaga:
    def execute(self, order_data: dict) -> str:
        # Step 1: Create order
        order_id = self.order_service.create(order_data)
        try:
            # Step 2: Reserve inventory
            self.inventory_service.reserve(order_id, order_data['items'])
            try:
                # Step 3: Process payment
                self.payment_service.charge(order_id, order_data['total'])
                # Success
                self.order_service.confirm(order_id)
                return order_id
            except PaymentFailed:
                # Compensate inventory
                self.inventory_service.release(order_id)
                self.order_service.cancel(order_id)
                raise
        except InventoryUnavailable:
            # Compensate order
            self.order_service.cancel(order_id)
            raise
```

### CQRS (Command Query Responsibility Segregation)

Separate read and write models.

```
Commands (writes)              Queries (reads)
     │                              │
     ▼                              ▼
┌──────────┐    events       ┌──────────────┐
│  Write   │────────────────►│   Read       │
│  Model   │                 │   Model      │
└────┬─────┘                 └──────────────┘
     │                              │
     ▼                              ▼
┌──────────┐                 ┌──────────────┐
│ Event    │                 │ Denormalized │
│ Store    │                 │  Read DB     │
└──────────┘                 └──────────────┘
```

**Use cases:**
- Read and write patterns differ significantly
- Need optimized query models (dashboards, reports)
- Event sourcing systems

### API Composition

Query multiple services to compose a response.

```
┌──────────────────────────────────────────┐
│           API Composition Service        │
└───────────────────┬──────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌────────┐    ┌──────────┐    ┌────────┐
│Customer│    │  Order   │    │Product │
│Service │    │ Service  │    │Service │
└────────┘    └──────────┘    └────────┘
```

**Example:**
```python
class OrderDetailsComposer:
    def get_order_details(self, order_id: str) -> OrderDetails:
        # Parallel calls
        order_future = self.executor.submit(self.order_service.get, order_id)
        customer_future = None
        products_future = None

        order = order_future.result()

        customer_future = self.executor.submit(
            self.customer_service.get, order.customer_id
        )
        products_future = self.executor.submit(
            self.product_service.get_many, [i.product_id for i in order.items]
        )

        return OrderDetails(
            order=order,
            customer=customer_future.result(),
            products=products_future.result()
        )
```

---

## Infrastructure Patterns

### API Gateway

Single entry point for clients.

```
┌────────────────────────────────────────────┐
│                 Clients                     │
└───────────────────┬────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────┐
│              API Gateway                   │
│  ┌─────────────────────────────────────┐  │
│  │ - Authentication/Authorization      │  │
│  │ - Rate limiting                     │  │
│  │ - Request routing                   │  │
│  │ - Response aggregation              │  │
│  │ - Protocol translation              │  │
│  │ - SSL termination                   │  │
│  └─────────────────────────────────────┘  │
└───────────────────┬───────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌────────┐    ┌──────────┐    ┌────────┐
│Service │    │ Service  │    │Service │
│   A    │    │    B     │    │   C    │
└────────┘    └──────────┘    └────────┘
```

**Responsibilities:**
- Route requests to appropriate services
- Authenticate and authorize requests
- Rate limiting and throttling
- Request/response transformation
- Circuit breaking for downstream services
- Logging and monitoring

**Backend for Frontend (BFF):**
```
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Web    │    │ Mobile  │    │  IoT    │
│  App    │    │  App    │    │ Device  │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     ▼              ▼              ▼
┌────────┐    ┌──────────┐    ┌────────┐
│Web BFF │    │Mobile BFF│    │IoT BFF │
└────┬───┘    └────┬─────┘    └────┬───┘
     │              │              │
     └──────────────┼──────────────┘
                    │
                    ▼
        ┌───────────────────┐
        │  Backend Services │
        └───────────────────┘
```

### Service Discovery

Services need to find each other without hardcoded addresses.

**Client-side discovery:**
```
┌────────────┐  1. Query   ┌────────────────┐
│  Client    │────────────►│ Service        │
│  Service   │             │ Registry       │
└──────┬─────┘             └────────────────┘
       │                          ▲
       │ 2. Call directly         │ Register
       ▼                          │
┌──────────────┐           ┌──────┴─────┐
│  Instance 1  │           │ Instance 2 │
└──────────────┘           └────────────┘
```

**Server-side discovery:**
```
┌────────────┐  1. Request  ┌────────────────┐
│  Client    │─────────────►│ Load Balancer  │
│  Service   │              │ + Discovery    │
└────────────┘              └───────┬────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌──────────┐   ┌──────────┐   ┌──────────┐
              │Instance 1│   │Instance 2│   │Instance 3│
              └──────────┘   └──────────┘   └──────────┘
```

**Tools:**
- Consul
- Netflix Eureka
- Kubernetes DNS
- AWS Cloud Map

### Service Mesh

Infrastructure layer for service-to-service communication.

```
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                         │
│  (Configuration, certificates, policies)                │
└─────────────────────────────────────────────────────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│┌──────────────┐│  │┌──────────────┐│  │┌──────────────┐│
││   Service A  ││  ││   Service B  ││  ││   Service C  ││
│└──────────────┘│  │└──────────────┘│  │└──────────────┘│
│┌──────────────┐│  │┌──────────────┐│  │┌──────────────┐│
││ Sidecar      ││  ││ Sidecar      ││  ││ Sidecar      ││
││ Proxy        ││  ││ Proxy        ││  ││ Proxy        ││
│└──────────────┘│  │└──────────────┘│  │└──────────────┘│
└────────────────┘  └────────────────┘  └────────────────┘
```

**Features:**
- Traffic management (load balancing, routing)
- Security (mTLS, authorization)
- Observability (tracing, metrics)
- Resilience (retries, timeouts, circuit breakers)

**Tools:**
- Istio
- Linkerd
- Consul Connect

### Sidecar Pattern

Deploy helper components alongside service containers.

```
┌─────────────────────────────────────┐
│              Pod                     │
│  ┌─────────────────────────────┐   │
│  │      Main Container         │   │
│  │      (Application)          │   │
│  └─────────────────────────────┘   │
│  ┌──────────────┐ ┌────────────┐   │
│  │   Sidecar    │ │  Sidecar   │   │
│  │   (Proxy)    │ │  (Logger)  │   │
│  └──────────────┘ └────────────┘   │
└─────────────────────────────────────┘
```

**Use cases:**
- Envoy proxy (service mesh)
- Log collectors (Fluentd)
- Monitoring agents (Prometheus)
- Configuration management
- Secret management

---

## Resilience Patterns

### Circuit Breaker

Stop calling failing services to prevent cascade failures.

```
States:
┌────────┐  failures exceed threshold  ┌────────┐
│ CLOSED │───────────────────────────►│  OPEN  │
└────────┘                             └───┬────┘
     ▲                                     │
     │ success                  timeout expires
     │                                     │
     └─────────────────────────────────────┘
                                     │
                               ┌─────▼─────┐
                               │ HALF-OPEN │
                               └───────────┘
```

**Implementation:**
```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = timedelta(seconds=recovery_timeout)
        self.failures = 0
        self.state = 'CLOSED'
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if datetime.now() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitOpenError("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failures = 0
        self.state = 'CLOSED'

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = 'OPEN'
```

### Retry with Backoff

Retry transient failures with increasing delays.

```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
```

**Exponential backoff with jitter:**
| Attempt | Base Delay | Jitter Range | Total Range |
|---------|------------|--------------|-------------|
| 1 | 1s | 0-0.1s | 1-1.1s |
| 2 | 2s | 0-0.2s | 2-2.2s |
| 3 | 4s | 0-0.4s | 4-4.4s |

### Bulkhead

Isolate failures to prevent system-wide impact.

```
┌─────────────────────────────────────────────────┐
│                  Service                         │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │ Thread Pool │  │ Thread Pool │  │ Thread   │ │
│  │ (Orders)    │  │ (Payments)  │  │ Pool     │ │
│  │             │  │             │  │ (Other)  │ │
│  │ [5 threads] │  │ [3 threads] │  │ [10]     │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
└─────────────────────────────────────────────────┘
```

**Benefits:**
- Slow downstream service doesn't exhaust all threads
- Failures contained to specific pools
- Other functionality continues working

### Timeout

Set timeouts on all network calls.

```python
import httpx

async def call_service(url: str, timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url)
            return response.json()
        except httpx.TimeoutException:
            # Return cached/default value or raise
            raise ServiceUnavailableError(f"Timeout calling {url}")
```

**Guidelines:**
- Set timeouts on every external call
- Make timeouts configurable
- Consider cascade effects (total time budget)

### Fallback

Provide degraded functionality when service fails.

```python
class ProductService:
    def get_recommendations(self, user_id: str) -> List[Product]:
        try:
            return self.recommendation_api.get(user_id, timeout=2.0)
        except (TimeoutError, ServiceUnavailableError):
            # Fallback to cached popular products
            return self.cache.get('popular_products', [])
```

---

## Observability Patterns

### Distributed Tracing

Track requests across service boundaries.

```
Request: GET /order/123

Trace ID: abc-123
├── Span: API Gateway (10ms)
│   └── Span: Order Service (50ms)
│       ├── Span: Customer Service (15ms)
│       │   └── Span: Database (5ms)
│       └── Span: Inventory Service (20ms)
│           └── Span: Cache (2ms)
```

**Implementation:**
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def get_order(order_id: str):
    with tracer.start_as_current_span("get_order") as span:
        span.set_attribute("order.id", order_id)

        order = await order_repo.get(order_id)

        with tracer.start_as_current_span("get_customer"):
            customer = await customer_service.get(order.customer_id)

        with tracer.start_as_current_span("get_products"):
            products = await product_service.get_many(order.product_ids)

        return OrderDetails(order, customer, products)
```

### Centralized Logging

Aggregate logs from all services.

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│Service A │  │Service B │  │Service C │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   ▼
         ┌─────────────────┐
         │  Log Aggregator │
         │  (ELK/Loki)     │
         └─────────────────┘
```

**Structured logging format:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "order-service",
  "trace_id": "abc-123",
  "span_id": "def-456",
  "message": "Order created",
  "order_id": "order-789",
  "customer_id": "cust-123",
  "total": 150.00
}
```

### Health Checks

Expose service health for orchestrators.

```python
@app.get("/health/live")
def liveness():
    """Is the process running?"""
    return {"status": "ok"}

@app.get("/health/ready")
def readiness():
    """Can the service handle traffic?"""
    try:
        # Check dependencies
        db.execute("SELECT 1")
        cache.ping()
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}, 503
```

### Metrics

Collect and expose service metrics.

**Key metrics:**
```
# Request rate
http_requests_total{service="order", method="POST", status="200"}

# Request latency
http_request_duration_seconds{service="order", quantile="0.99"}

# Error rate
http_requests_total{service="order", status="500"}

# Saturation
thread_pool_active_threads{service="order", pool="orders"}
```

---

## Security Patterns

### Service-to-Service Authentication

Verify service identity.

**Mutual TLS (mTLS):**
```
┌──────────────┐    certificate    ┌──────────────┐
│  Service A   │◄─────────────────►│  Service B   │
│ (cert + key) │    verify both    │ (cert + key) │
└──────────────┘                   └──────────────┘
```

**JWT token passing:**
```
User Request               Service A              Service B
    │                          │                      │
    │ JWT (user token)         │                      │
    │─────────────────────────►│                      │
    │                          │ JWT (service token)  │
    │                          │─────────────────────►│
    │                          │                      │
```

### API Security

Protect service APIs.

**Patterns:**
- API key authentication
- OAuth 2.0 / OpenID Connect
- Rate limiting per client
- Input validation
- Output encoding

### Secret Management

Manage sensitive configuration.

```
┌──────────────┐         ┌─────────────────┐
│   Service    │◄───────►│  Vault / AWS    │
│              │         │  Secrets Mgr    │
└──────────────┘         └─────────────────┘
```

**Best practices:**
- Never store secrets in code or config files
- Rotate secrets automatically
- Audit secret access
- Use short-lived credentials

---

## Testing Patterns

### Contract Testing

Verify service interfaces match expectations.

```
Consumer                                Provider
   │                                       │
   │  Define expected contract             │
   │─────────────────────────────────────►│
   │                                       │
   │  Provider verifies contract           │
   │                                       │
```

**Tools:**
- Pact
- Spring Cloud Contract

### Consumer-Driven Contracts

Consumers define their expectations, providers verify.

```python
# Consumer side (Order Service expects this from Customer Service)
@pact_consumer("OrderService")
def test_get_customer(pact):
    pact.given("customer 123 exists")
    pact.upon_receiving("a request for customer 123")
    pact.with_request("GET", "/customers/123")
    pact.will_respond_with(200, body={
        "id": "123",
        "name": Like("John Doe"),
        "email": Like("john@example.com")
    })

    # Test code using mock
    customer = customer_client.get("123")
    assert customer.id == "123"
```

### Integration Testing

Test service interactions in isolation.

```python
@pytest.fixture
def order_service():
    """Spin up order service with test dependencies."""
    with docker_compose_up("order-service", "postgres", "redis"):
        yield OrderServiceClient("http://localhost:8080")

def test_create_order(order_service):
    order = order_service.create(customer_id="123", items=[...])
    assert order.status == "pending"
```

### End-to-End Testing

Test complete user journeys.

```python
def test_checkout_flow():
    # 1. Add items to cart
    cart = api.add_to_cart(user_id="123", product_id="abc", quantity=2)

    # 2. Create order
    order = api.checkout(cart_id=cart.id, payment_method="card")
    assert order.status == "pending"

    # 3. Verify inventory reserved
    inventory = api.get_inventory(product_id="abc")
    assert inventory.reserved == 2

    # 4. Simulate payment
    api.complete_payment(order_id=order.id)

    # 5. Verify order confirmed
    order = api.get_order(order.id)
    assert order.status == "confirmed"
```

---

## Anti-Patterns

### Distributed Monolith

Microservices with monolithic coupling.

**Symptoms:**
- Services share database
- Services must deploy together
- Synchronous call chains everywhere
- Shared libraries with business logic

**Fix:**
- True data ownership per service
- Event-driven communication
- API versioning
- Bounded contexts

### Chatty Services

Too many round-trips between services.

```
# BAD: Multiple calls
order = order_service.get(order_id)
customer = customer_service.get(order.customer_id)
for item in order.items:
    product = product_service.get(item.product_id)  # N+1 problem

# GOOD: Batch or aggregate
order_details = order_aggregator.get_full_order(order_id)
```

### Shared Database

Multiple services accessing same database.

**Problems:**
- Schema changes affect all services
- No clear data ownership
- Tight coupling

**Fix:**
- Database per service
- API for data access
- Event-driven data synchronization

### No API Versioning

Breaking changes without versioning.

**Fix:**
```
# URL versioning
GET /v1/orders/123
GET /v2/orders/123

# Header versioning
Accept: application/vnd.company.v2+json
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

### When to Use Microservices

**Good fit:**
- Large teams (>15 engineers)
- Need independent deployment
- Different scaling requirements per component
- Polyglot requirements (different tech stacks)
- Clear bounded contexts

**Not a good fit:**
- Small team (<10 engineers)
- Unknown domain (still learning)
- Performance-critical tight coupling needed
- Simple CRUD application

### How to Apply

1. **Start with a monolith**: Extract services later
2. **Identify bounded contexts**: DDD helps
3. **Design APIs first**: Contract-driven development
4. **Automate everything**: CI/CD, infrastructure
5. **Build observability in**: Logging, tracing, metrics
6. **Plan for failure**: Resilience patterns

### Red Flags

- No CI/CD pipeline per service
- Shared database across services
- Synchronous chains >3 hops
- No monitoring or tracing
- Manual deployments
- No API versioning strategy

---

## References

### Books
- *Building Microservices* by Sam Newman
- *Microservices Patterns* by Chris Richardson
- *Release It!* by Michael Nygard

### Online Resources
- microservices.io (patterns catalog)
- Martin Fowler's microservices articles
- Netflix tech blog

### Tools
- API Gateways: Kong, AWS API Gateway, Nginx
- Service Mesh: Istio, Linkerd
- Observability: Jaeger, Prometheus, Grafana
- Messaging: Kafka, RabbitMQ, NATS
