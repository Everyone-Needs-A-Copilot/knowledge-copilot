---
last_updated: 2026-02-25
status: active
name: system-design
description: Architecture patterns, scalability, distributed systems, trade-off analysis. Use for system architecture decisions.
triggers:
  files: ["**/docs/architecture/**", "**/ADR/**", "**/design/**", "**/architecture.md"]
  keywords: ["architecture", "scalability", "distributed system", "microservices", "monolith", "CAP theorem", "circuit breaker", "load balancer", "caching", "trade-off", "system design", "availability", "consistency", "partitioning"]
allowed-tools: Read, Write, Edit
---

# System Design

## Overview

System design is the art and science of architecting scalable, maintainable, and resilient software systems. It requires balancing competing concerns: performance vs. cost, consistency vs. availability, simplicity vs. functionality, and immediate needs vs. future growth.

Good system design is invisible. Users experience fast, reliable systems. Developers work with clear boundaries and understandable patterns. Operations teams can diagnose and fix issues quickly.

This skill guides architectural decision-making through patterns, trade-offs, and real-world considerations. Use it when designing new systems, evaluating existing architectures, or making critical technical decisions that affect scalability, reliability, or maintainability.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Principles

### 1. Simplicity First

> "Complexity is the enemy of reliability." — Ben Treynor Sloss, Google SRE

- Start with the simplest solution that could work
- Add complexity only when measurements prove it necessary
- Every abstraction layer adds latency and failure modes
- Optimize for readability and debuggability

**Example**: Begin with a monolith and proven database before adopting microservices and distributed data stores.

### 2. Modularity and Loose Coupling

- Components should be replaceable without system-wide changes
- Define clear interfaces and contracts
- Minimize dependencies between modules
- Use abstraction layers (ports & adapters) for external systems

**Pattern**: Dependency inversion — depend on interfaces, not implementations.

### 3. Fault Tolerance by Design

Systems fail. Design for graceful degradation, not perfection.

- Assume every network call will fail
- Build timeout and retry mechanisms into every integration
- Implement circuit breakers for external dependencies
- Design for partial failures (if one service fails, others continue)

### 4. Evolvability over Optimization

- Optimize for change, not just current performance
- Make it easy to measure, experiment, and iterate
- Build observability into the system from day one
- Accept technical debt that enables learning, reject debt that blocks change

### 5. Data is Harder than Code

- Schema changes are deployment events
- Data migrations can take days or weeks
- Lost data is usually unrecoverable
- Design data models with future queries in mind

**Guideline**: Code can be rewritten; data must be migrated.

---

## Architecture Patterns

### Monolith

**When to use:**
- Starting a new product with unknown scale
- Team < 10 engineers
- Domain is not yet well-understood
- Need to iterate quickly on features

**Advantages:**
- Simple deployment (one artifact)
- Easy to reason about end-to-end flows
- No network latency between modules
- Straightforward testing and debugging
- Single database = ACID transactions

**Disadvantages:**
- Harder to scale teams (everyone touches the same codebase)
- All-or-nothing deployments (high risk)
- Technology lock-in (can't mix languages/frameworks easily)
- Eventual performance bottlenecks

**Example structure:**
```
monolith/
├── app/
│   ├── api/          # HTTP handlers
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   └── db/           # Database connections
├── tests/
└── main.py           # Single entry point
```

### Microservices

**When to use:**
- Clear bounded contexts identified
- Teams > 15 engineers needing autonomy
- Different services have different scaling needs
- Need independent deployment cycles

**Advantages:**
- Independent scaling of components
- Team autonomy (own, deploy, monitor services)
- Technology flexibility (polyglot architecture)
- Isolated failures (one service crash doesn't take down the system)

**Disadvantages:**
- Operational complexity (service discovery, orchestration)
- Network latency and failures
- Distributed debugging is hard
- Eventual consistency challenges
- Transaction management complexity

**Anti-pattern:** **Distributed monolith** — microservices with tight coupling. All the complexity, none of the benefits.

**Checklist before adopting microservices:**
- [ ] Have clear bounded contexts?
- [ ] Can each service be deployed independently?
- [ ] Have monitoring/tracing infrastructure?
- [ ] Team capable of managing distributed systems?
- [ ] Have strategies for data consistency?

### Layered Architecture

Organize code into horizontal layers with clear responsibilities.

```
┌─────────────────────────┐
│   Presentation Layer    │  (API controllers, UI)
├─────────────────────────┤
│   Application Layer     │  (Use cases, orchestration)
├─────────────────────────┤
│   Domain Layer          │  (Business logic, entities)
├─────────────────────────┤
│   Infrastructure Layer  │  (Database, external APIs)
└─────────────────────────┘
```

**Rules:**
- Upper layers depend on lower layers (never reverse)
- Domain layer has no dependencies (pure business logic)
- Infrastructure details isolated at the bottom

**Benefits:**
- Clear separation of concerns
- Easy to test (mock lower layers)
- Business logic isolated from frameworks

### Hexagonal Architecture (Ports & Adapters)

Domain logic at the center, external systems connected via adapters.

```
         ┌──────────────┐
         │  HTTP REST   │ (Adapter)
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │    Port      │ (Interface)
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │  Domain Core │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │    Port      │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │  PostgreSQL  │ (Adapter)
         └──────────────┘
```

**Ports**: Interfaces defining what the domain needs (e.g., `UserRepository`)
**Adapters**: Concrete implementations (e.g., `PostgresUserRepository`, `MockUserRepository`)

**Benefits:**
- Swap implementations without changing domain logic
- Test domain logic with in-memory adapters
- Delay infrastructure decisions

**Example:**
```python
# Port (domain defines interface)
class UserRepository(Protocol):
    def get_by_id(self, user_id: str) -> User: ...
    def save(self, user: User) -> None: ...

# Adapter (infrastructure implements)
class PostgresUserRepository:
    def get_by_id(self, user_id: str) -> User:
        # SQL implementation
        pass
```

### Event-Driven Architecture

Services communicate via events rather than direct calls.

```
┌──────────┐    event    ┌──────────┐
│ Service A├────────────►│ Event Bus│
└──────────┘             └────┬─────┘
                              │ event
                         ┌────▼─────┐
                         │ Service B│
                         └──────────┘
```

**When to use:**
- Need to decouple services
- Multiple consumers need to react to state changes
- Audit log of all system changes required

**Advantages:**
- Loose coupling (publishers don't know about subscribers)
- Scalability (consumers process at their own pace)
- Extensibility (add new consumers without changing producers)

**Challenges:**
- Eventual consistency
- Debugging event flows
- Event schema evolution
- Ordering guarantees

**Event design principles:**
1. Events are facts about the past ("OrderPlaced", not "PlaceOrder")
2. Events are immutable
3. Include enough data to avoid subsequent queries
4. Version your events

### CQRS (Command Query Responsibility Segregation)

Separate read and write models.

```
┌─────────┐                    ┌─────────────┐
│ Command ├──────────────────► │ Write Model │
└─────────┘                    └──────┬──────┘
                                      │ events
                               ┌──────▼──────┐
┌───────┐                      │  Event Bus  │
│ Query ├─────────┐            └──────┬──────┘
└───────┘         │                   │
                  │            ┌──────▼──────┐
           ┌──────▼─────┐      │ Read Model  │
           │ Read Store │◄─────┤  Projector  │
           └────────────┘      └─────────────┘
```

**When to use:**
- Read and write patterns are very different
- Need to optimize reads independently (denormalization, caching)
- Complex business logic on writes, simple lookups on reads

**Benefits:**
- Independently scalable read and write sides
- Optimized data models for each use case
- Clear separation of business logic from queries

**Example:**
- **Write**: Validate order, check inventory, update order status
- **Read**: Pre-computed dashboard showing order summary (no joins)

### Event Sourcing

Store state changes as a sequence of events rather than current state.

```
Events:
1. AccountCreated(id=123, balance=0)
2. MoneyDeposited(id=123, amount=100)
3. MoneyWithdrawn(id=123, amount=30)

Current State (derived):
Account(id=123, balance=70)
```

**When to use:**
- Need complete audit trail
- Temporal queries ("what was the state at 3pm yesterday?")
- Multiple read models from same events
- Regulatory compliance requiring event history

**Benefits:**
- Full audit trail (how did we get to this state?)
- Time travel debugging
- Replay events to build new projections

**Challenges:**
- Storage grows unbounded (mitigation: snapshots)
- Schema evolution of old events
- Eventually consistent read models

### Service-Oriented Architecture (SOA)

Coarse-grained services with shared infrastructure (ESB).

**Difference from microservices:**
- Larger, business-function-sized services
- Often shares database
- Centralized governance (ESB, schema registry)

**When to use:**
- Enterprise environments with centralized IT
- Strong consistency requirements
- Reuse of business logic across applications

---

## Scalability

### Vertical vs. Horizontal Scaling

**Vertical (scale up):** Bigger machine (more CPU, RAM, disk)
- **Pros**: Simple, no code changes, maintains ACID transactions
- **Cons**: Hardware limits, expensive at high end, single point of failure

**Horizontal (scale out):** More machines
- **Pros**: Linear cost scaling, fault tolerance, no upper limit
- **Cons**: Requires code changes, eventual consistency, coordination overhead

**Guideline:** Exhaust vertical scaling first (simpler), then move to horizontal.

### Load Balancing Strategies

Distribute requests across multiple instances.

**Algorithms:**

1. **Round Robin**: Rotate through servers sequentially
   - Simple, fair distribution
   - Ignores server load

2. **Least Connections**: Route to server with fewest active connections
   - Better for long-lived connections
   - Requires connection state tracking

3. **IP Hash**: Route based on client IP
   - Sticky sessions (same client → same server)
   - Uneven distribution if clients behind NAT

4. **Weighted**: Route based on server capacity
   - Handles heterogeneous servers
   - Requires capacity awareness

**Health checks:** Load balancer must detect and avoid failed instances.

```
┌────────┐
│ Client ├─────┐
└────────┘     │
               ▼
        ┌──────────────┐
        │Load Balancer │
        └──────┬───────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│Server 1│ │Server 2│ │Server 3│
└────────┘ └────────┘ └────────┘
```

### Caching Layers

**Where to cache:**

1. **CDN**: Static assets (images, CSS, JS)
   - Geographic distribution
   - Offload origin server

2. **Application cache**: Computed results, session data
   - Redis, Memcached
   - Shared across instances

3. **Database query cache**: Repeated query results
   - Built into most databases
   - Invalidated on writes

4. **HTTP cache**: Browser and proxy caching
   - Cache-Control headers
   - ETags for validation

**Cache invalidation strategies:**

- **TTL (Time to Live)**: Expire after fixed duration
- **Write-through**: Update cache on write
- **Write-behind**: Async cache update
- **Invalidation on change**: Explicit cache clear

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

**Cache patterns:**

**Cache-Aside (Lazy Loading):**
```python
def get_user(user_id):
    # Try cache first
    user = cache.get(f"user:{user_id}")
    if user:
        return user

    # Cache miss — fetch from DB
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)

    # Update cache
    cache.set(f"user:{user_id}", user, ttl=300)
    return user
```

**Write-Through:**
```python
def update_user(user):
    # Write to database
    db.execute("UPDATE users SET ... WHERE id = ?", user.id)

    # Update cache immediately
    cache.set(f"user:{user.id}", user, ttl=300)
```

### Database Scaling

**Read replicas:**
```
┌────────────────┐
│ Primary (Write)│
└───────┬────────┘
        │ Replication
    ┌───┴───┬────────┐
    ▼       ▼        ▼
┌────────┐ ┌──────┐ ┌──────┐
│Replica1│ │Repli2│ │Repli3│ (Read-only)
└────────┘ └──────┘ └──────┘
```

- All writes go to primary
- Reads distributed across replicas
- Replication lag = eventual consistency

**Sharding (horizontal partitioning):**

Distribute data across databases by key.

```
Shard Key: user_id % 3

Shard 0: users 0, 3, 6, 9...
Shard 1: users 1, 4, 7, 10...
Shard 2: users 2, 5, 8, 11...
```

**Considerations:**
- **Shard key choice**: Must be in every query, evenly distributed
- **Cross-shard queries**: Expensive (scatter-gather)
- **Resharding**: Painful when adding shards

**Partitioning strategies:**
- **Range**: user_id 1-1000 → Shard 1, 1001-2000 → Shard 2 (hotspots possible)
- **Hash**: hash(user_id) % N (even distribution, no range queries)
- **Geographic**: users by region (data locality, compliance)

### Stateless Design

**Stateless:** Each request contains all information needed to process it.

**Benefits:**
- Any server can handle any request (simple load balancing)
- Easy to scale (just add servers)
- No lost state on server failure

**Implementation:**
- Store session state in database or cache (Redis)
- Use JWT tokens for authentication (self-contained)
- Pass context in request headers/parameters

**Stateful anti-pattern:**
```python
# BAD: In-memory state
user_sessions = {}  # Lost on restart, can't load balance

# GOOD: External state
def get_session(session_id):
    return redis.get(f"session:{session_id}")
```

---

## Reliability

### Redundancy and Failover

**Redundancy**: Multiple instances of components.

- **Active-Active**: All instances handle traffic (load balancing)
- **Active-Passive**: Primary handles traffic, standby waits (failover)

**Failover strategies:**
- **Automatic**: Health check detects failure → switch to standby
- **Manual**: Human decides to failover (slower, more control)

**Replication:**
- **Synchronous**: Write confirms only after replicas acknowledge (slow, consistent)
- **Asynchronous**: Write confirms immediately, replicas catch up (fast, eventual consistency)

### Circuit Breaker Pattern

Prevent cascading failures by stopping calls to failing services.

```
States:
┌────────┐
│ Closed │──[failures exceed threshold]──┐
└────────┘                                │
     ▲                                    ▼
     │                             ┌──────────┐
     │                             │   Open   │
     │                             └──────────┘
     │                                    │
     │                         [timeout expires]
     │                                    │
     │                                    ▼
     │                             ┌──────────────┐
     └────[success]────────────────┤ Half-Open    │
                                   └──────────────┘
```

**States:**
1. **Closed**: Normal operation, calls pass through
2. **Open**: Threshold exceeded, calls fail immediately (fast fail)
3. **Half-Open**: After timeout, allow test requests

**Implementation:**
```python
class CircuitBreaker:
    def __init__(self, threshold=5, timeout=60):
        self.failures = 0
        self.threshold = threshold
        self.timeout = timeout
        self.state = "CLOSED"
        self.last_failure = None

    def call(self, func):
        if self.state == "OPEN":
            if time.now() - self.last_failure > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError("Circuit breaker is open")

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def on_failure(self):
        self.failures += 1
        self.last_failure = time.now()
        if self.failures >= self.threshold:
            self.state = "OPEN"
```

### Retry with Exponential Backoff

Transient failures (network glitches) can be retried, but not immediately.

**Exponential backoff:** Increase delay between retries.

```python
def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)  # 1s, 2s, 4s
            time.sleep(delay + random.uniform(0, 1))  # Add jitter
```

**Jitter**: Add randomness to avoid thundering herd (all clients retry at the same time).

**When NOT to retry:**
- Client errors (400s) — will always fail
- Idempotency not guaranteed — could cause duplicates

### Graceful Degradation

Provide reduced functionality rather than total failure.

**Examples:**
- **Search down?** Show cached/popular results instead of error
- **Recommendations unavailable?** Show generic content
- **Payment gateway slow?** Queue for later processing, show "pending" status

**Implementation:**
```python
def get_recommendations(user_id):
    try:
        return recommendation_service.get(user_id, timeout=1.0)
    except (TimeoutError, ServiceUnavailableError):
        # Degrade to generic popular items
        return get_popular_items()
```

### Health Checks and Liveness Probes

**Liveness probe:** Is the service alive?
- Returns 200 if process is running
- Used by orchestrators (Kubernetes) to restart dead containers

**Readiness probe:** Is the service ready to handle traffic?
- Returns 200 only if dependencies are available (database connected, etc.)
- Used by load balancers to route traffic

```python
@app.get("/health/live")
def liveness():
    return {"status": "ok"}

@app.get("/health/ready")
def readiness():
    try:
        db.execute("SELECT 1")  # Check database
        cache.ping()            # Check cache
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}, 503
```

### Chaos Engineering Principles

Proactively test system resilience by injecting failures.

**Practices:**
- Kill random instances (Chaos Monkey)
- Inject network latency/failures
- Consume resources (CPU, memory, disk)
- Test degradation under load

**Goal:** Discover weaknesses before customers do.

---

## Data Design

### Database Selection: SQL vs. NoSQL

**SQL (Relational):**
- **Use when**: Data is structured, relationships matter, need ACID transactions
- **Examples**: PostgreSQL, MySQL
- **Strengths**: Strong consistency, complex queries, mature tooling
- **Weaknesses**: Harder to scale horizontally, rigid schema

**NoSQL:**

**Document (MongoDB, CouchDB):**
- **Use when**: Flexible schema, hierarchical data, rapid iteration
- **Strengths**: Schema flexibility, horizontal scaling
- **Weaknesses**: Weaker consistency, no joins

**Key-Value (Redis, DynamoDB):**
- **Use when**: Simple lookups by key, caching, session storage
- **Strengths**: Very fast, simple model
- **Weaknesses**: No complex queries

**Column-Family (Cassandra, HBase):**
- **Use when**: Time-series data, write-heavy workloads, huge scale
- **Strengths**: Linear scalability, high write throughput
- **Weaknesses**: Limited query flexibility

**Graph (Neo4j, ArangoDB):**
- **Use when**: Complex relationships, traversals, social networks
- **Strengths**: Relationship queries, path finding
- **Weaknesses**: Harder to scale, specialized use case

**Decision matrix:**
| Requirement | Choose |
|-------------|--------|
| ACID transactions | SQL |
| Complex joins/aggregations | SQL |
| Flexible schema | Document NoSQL |
| Massive scale (millions of writes/sec) | Column-family NoSQL |
| Relationship traversals | Graph NoSQL |
| Simple key lookups | Key-value NoSQL |

### Schema Design for Scalability

**Normalization vs. Denormalization:**

**Normalized:** Minimize redundancy via separate tables + joins.
```sql
-- Normalized
users: id, name
orders: id, user_id, total
order_items: id, order_id, product_id, quantity
```

**Denormalized:** Duplicate data to avoid joins.
```sql
-- Denormalized
orders: id, user_id, user_name, total, items_json
```

**Trade-off:**
- Normalized: Data consistency, smaller storage, harder to scale reads
- Denormalized: Faster reads, easier to scale, data duplication, consistency challenges

**Guideline:** Start normalized, denormalize based on query patterns.

**Indexing strategies:**
- Index columns used in WHERE, JOIN, ORDER BY
- Avoid over-indexing (slows writes)
- Use covering indexes (include all SELECT columns)
- Monitor slow queries and add indexes

### Data Consistency

**ACID (SQL default):**
- **Atomicity**: All or nothing
- **Consistency**: Data satisfies constraints
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data survives crashes

**BASE (NoSQL common):**
- **Basically Available**: System available even during failures
- **Soft state**: State may change without input (eventual consistency)
- **Eventual consistency**: Eventually all nodes see same data

**Consistency models:**

1. **Strong consistency**: Read sees latest write (ACID)
2. **Eventual consistency**: Read may see stale data, converges over time
3. **Causal consistency**: Reads see writes in causal order
4. **Read-your-writes**: Your own writes are visible to you immediately

**Choosing consistency level:**
- **Strong**: Financial transactions, inventory management
- **Eventual**: Social media feeds, analytics, recommendations

### CAP Theorem

In a distributed system, you can have at most 2 of 3:

- **Consistency**: All nodes see the same data at the same time
- **Availability**: Every request gets a response (success or failure)
- **Partition tolerance**: System continues despite network splits

```
        Consistency
            /\
           /  \
          /    \
         /  CA  \
        /        \
       /          \
      /    ACID    \
     /   databases  \
    /________________\
   AP              CP

 NoSQL          Paxos/Raft
(eventual)      (strong)
```

**Reality:** Partition tolerance is required (networks fail), so choose between:
- **CP**: Sacrifice availability for consistency (reject writes during partition)
- **AP**: Sacrifice consistency for availability (accept stale reads)

**Example:**
- **Banking (CP)**: Can't show wrong balance, reject requests during partition
- **Social feed (AP)**: Can show stale posts, keep system available

### Event-Driven Data Synchronization

Propagate data changes via events instead of polling or batch jobs.

**Change Data Capture (CDC):**
- Database emits events on INSERT/UPDATE/DELETE
- Consumers react to changes in real-time

**Tools:** Debezium (Kafka Connect), AWS DMS

**Example flow:**
```
1. User updates profile in users table
2. Database emits UserUpdated event
3. Event consumed by:
   - Search index updater (refresh Elasticsearch)
   - Cache invalidator (clear Redis)
   - Analytics pipeline (record event)
```

**Benefits:**
- Decoupled consumers
- Real-time data propagation
- Audit trail

---

## Communication Patterns

### Synchronous Communication

**REST (HTTP/JSON):**
- **Use when**: Public APIs, CRUD operations, browser clients
- **Pros**: Universal, human-readable, stateless, cacheable
- **Cons**: Verbose, slower than binary protocols

**Design principles:**
- Use HTTP methods correctly (GET, POST, PUT, DELETE)
- Versioning (/v1/users)
- Idempotent operations (retries safe)
- Consistent error responses

**gRPC (HTTP/2 + Protocol Buffers):**
- **Use when**: Service-to-service, performance-critical, strict schemas
- **Pros**: Fast, strongly typed, bidirectional streaming
- **Cons**: Not human-readable, requires code generation

**Example:**
```protobuf
service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc StreamUpdates(Empty) returns (stream UserUpdate);
}
```

### Asynchronous Communication

**Message Queues (RabbitMQ, SQS):**
- Point-to-point: One producer → one consumer
- **Use when**: Task queues, background jobs, load leveling

**Pub/Sub (Kafka, Google Pub/Sub):**
- One producer → many consumers
- **Use when**: Event broadcasting, real-time analytics, microservices coordination

**Example flow:**
```
User places order
  ↓
Order service publishes OrderPlaced event
  ↓
├─ Inventory service (decrease stock)
├─ Email service (send confirmation)
├─ Analytics service (record event)
└─ Shipping service (create shipment)
```

**Guarantees:**
- **At-most-once**: Message may be lost (fire and forget)
- **At-least-once**: Message may be delivered multiple times (requires idempotency)
- **Exactly-once**: Message delivered exactly once (hard, expensive)

### API Gateway

Single entry point for clients, routes to backend services.

```
        ┌───────┐
        │Client │
        └───┬───┘
            │
       ┌────▼────────┐
       │ API Gateway │
       └────┬────────┘
            │
    ┌───────┼────────┐
    ▼       ▼        ▼
┌────────┐ ┌─────┐ ┌──────┐
│User Svc│ │Order│ │Invent│
└────────┘ └─────┘ └──────┘
```

**Responsibilities:**
- Authentication/authorization
- Rate limiting
- Request routing
- Response aggregation
- Protocol translation (REST → gRPC)

**Benefits:**
- Clients talk to one endpoint
- Cross-cutting concerns centralized
- Backend services can change without client changes

### Service Mesh

Infrastructure layer for service-to-service communication.

**Examples:** Istio, Linkerd

**Features:**
- Automatic load balancing
- Service discovery
- Mutual TLS (mTLS)
- Distributed tracing
- Circuit breakers
- Retries and timeouts

**Architecture:**
```
Service A ──► Sidecar Proxy ──► Sidecar Proxy ──► Service B
```

Each service has a sidecar proxy handling communication logic.

### Saga Pattern (Distributed Transactions)

Coordinate transactions across multiple services without 2PC.

**Choreography:** Services react to events.
```
Order Service: CreateOrder → OrderCreated event
  ↓
Inventory Service: Reserve inventory → InventoryReserved event
  ↓
Payment Service: Charge card → PaymentCompleted event
  ↓
Shipping Service: Ship order
```

**Orchestration:** Central coordinator manages saga.
```
Saga Orchestrator:
1. Call Order Service
2. Call Inventory Service
3. Call Payment Service
4. Call Shipping Service
```

**Failure handling:** Compensating transactions (rollback).
```
Payment fails
  ↓
Saga orchestrator:
- Call Inventory Service: ReleaseInventory
- Call Order Service: CancelOrder
```

**Trade-off:**
- **Choreography**: Decoupled, harder to understand flow
- **Orchestration**: Central point of control, orchestrator is single point of failure

---

## Observability

### Logging Strategies

**Structured logging:** Machine-parseable format (JSON).

```python
# BAD: Unstructured
logger.info(f"User {user_id} created order {order_id}")

# GOOD: Structured
logger.info("order_created", extra={
    "user_id": user_id,
    "order_id": order_id,
    "total": order.total,
    "timestamp": datetime.now().isoformat()
})
```

**Log levels:**
- **DEBUG**: Detailed diagnostic info (disabled in production)
- **INFO**: General informational messages
- **WARNING**: Something unexpected, but system continues
- **ERROR**: Error occurred, operation failed
- **CRITICAL**: System failure, immediate attention required

**What to log:**
- Request/response (including trace IDs)
- Errors with stack traces
- Significant state changes
- Performance metrics (latency)

**What NOT to log:**
- Passwords, secrets, tokens
- PII without redaction
- Too much (log data is expensive)

### Metrics and Monitoring

**RED method (request-driven services):**
- **Rate**: Requests per second
- **Errors**: Failed requests per second
- **Duration**: Latency (p50, p95, p99)

**USE method (resource-driven services):**
- **Utilization**: % time resource is busy
- **Saturation**: Queue length, backlog
- **Errors**: Error count

**Key metrics by layer:**

**Application:**
- Request rate
- Error rate
- Response time (percentiles)
- Throughput (transactions/sec)

**Infrastructure:**
- CPU utilization
- Memory usage
- Disk I/O
- Network throughput

**Database:**
- Query latency
- Connection pool usage
- Slow queries
- Replication lag

**Implementation:**
```python
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency')

@request_latency.time()
def handle_request(request):
    # Process request
    request_count.labels(method=request.method, endpoint=request.path, status=200).inc()
```

### Distributed Tracing

Track requests across service boundaries.

**Trace:** End-to-end request flow
**Span:** Single operation within a trace

```
Trace ID: abc123
├─ Span: API Gateway (50ms)
│  ├─ Span: User Service (20ms)
│  │  └─ Span: Database query (15ms)
│  └─ Span: Order Service (30ms)
│     ├─ Span: Database query (10ms)
│     └─ Span: Payment API call (20ms)
```

**Implementation:** Propagate trace context via headers.
```
X-Trace-Id: abc123
X-Span-Id: span456
X-Parent-Span-Id: span123
```

**Tools:** Jaeger, Zipkin, AWS X-Ray

**Benefits:**
- Identify bottlenecks (which service is slow?)
- Debug distributed failures
- Understand service dependencies

### Alerting Best Practices

**Alert on symptoms, not causes:**
- **Bad**: "CPU > 80%" (so what?)
- **Good**: "API latency p95 > 500ms" (users affected)

**Actionable alerts only:**
- Every alert should require human action
- If you can't act on it, don't alert

**Alert fatigue prevention:**
- Use appropriate thresholds (not too sensitive)
- Aggregate related alerts
- Route alerts by severity (page for critical, email for warning)

**SLO-based alerting:**
- Define Service Level Objectives (99.9% uptime)
- Alert when error budget is being consumed

**Example alert:**
```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
for: 2m
annotations:
  summary: "Error rate above 5% for 2 minutes"
  description: "Current error rate: {{ $value }}"
```

---

## Trade-Off Analysis

Every architectural decision involves trade-offs. Make them explicit.

### Consistency vs. Availability

**Scenario:** Distributed database partition.

**Option 1: Favor Consistency (CP)**
- Reject writes to minority partition
- **Gain:** No split-brain, data always correct
- **Lose:** Availability during partition

**Option 2: Favor Availability (AP)**
- Accept writes to both partitions
- **Gain:** Always available
- **Lose:** Conflicting data, manual reconciliation

**Decision framework:**
- Can the business tolerate stale data? → AP
- Are conflicting writes acceptable? → AP
- Must data always be correct? → CP

### Latency vs. Throughput

**Latency:** Time to process one request
**Throughput:** Requests processed per second

**Trade-off:** Batching increases throughput but adds latency.

**Example: Database writes**
- **Low latency:** Write immediately (high overhead per write)
- **High throughput:** Batch 100 writes together (each write waits for batch)

**Decision framework:**
- Real-time requirement? → Optimize for latency
- Bulk processing? → Optimize for throughput

### Cost vs. Performance

**Options:**
1. **Scale vertically:** 16-core instance ($$$)
2. **Scale horizontally:** 4x 4-core instances ($$)
3. **Optimize code:** Reduce resource usage ($, high effort)

**Decision framework:**
- Is performance critical? → Scale first, optimize later
- Is cost constrained? → Optimize first
- Can you wait? → Measure, then decide

### Complexity vs. Maintainability

**Scenario:** Choosing between monolith and microservices.

**Microservices:**
- **Gain:** Independent scaling, team autonomy
- **Lose:** Operational complexity, debugging difficulty

**Monolith:**
- **Gain:** Simple deployment, easy debugging
- **Lose:** Scaling limitations, team coordination

**Decision framework:**
- Team < 10 engineers? → Monolith (simplicity wins)
- Clear bounded contexts? → Microservices (modularity wins)
- Unknown domain? → Monolith (defer decision)

### Build vs. Buy

**Build custom solution:**
- **Gain:** Exact fit, control, no licensing costs
- **Lose:** Development time, maintenance burden

**Buy/use existing:**
- **Gain:** Fast time-to-market, maintained by others
- **Lose:** Lock-in, may not fit perfectly, licensing costs

**Decision framework:**
- Is this core to your business? → Build
- Commodity functionality? → Buy
- Need to ship fast? → Buy

---

## Anti-Patterns

### Distributed Monolith

Microservices architecture with monolithic coupling.

**Symptoms:**
- Services share database
- Services call each other synchronously in chains
- Deploying one service requires deploying others
- No clear ownership boundaries

**Fix:**
- Define bounded contexts
- Use events for cross-service communication
- Each service owns its data

### Premature Optimization

Optimizing before measuring.

**Example:**
- "We'll need to scale to millions of users, so let's use Kubernetes + microservices + Kafka..."
- (Company has 100 users)

**Fix:**
- Build the simplest thing that works
- Measure actual bottlenecks
- Optimize based on data

> "Premature optimization is the root of all evil." — Donald Knuth

### Over-Engineering

Building for hypothetical future requirements.

**Example:**
- Abstract factory pattern for thing with one implementation
- Microservices for 2-person team
- Complex event sourcing for simple CRUD app

**Fix:**
- YAGNI (You Aren't Gonna Need It)
- Build for today's requirements
- Design for change, not for every possible future

### Ignoring CAP Theorem

Assuming you can have strong consistency AND high availability in a distributed system.

**Symptom:**
- Distributed system with synchronous replication across regions
- Expectation of zero latency writes with perfect consistency

**Fix:**
- Accept trade-offs
- Choose AP or CP based on requirements
- Use eventual consistency where acceptable

### Resume-Driven Development

Choosing technologies because they're trendy, not because they fit.

**Example:**
- "Let's use Kubernetes" (running 2 containers)
- "Let's use blockchain" (don't need decentralization)
- "Let's use GraphQL" (REST works fine)

**Fix:**
- Choose based on requirements
- Consider team expertise
- Evaluate operational overhead

### Big Ball of Mud

System with no discernible architecture.

**Symptoms:**
- Spaghetti code (everything depends on everything)
- No clear module boundaries
- Impossible to understand flow
- "Just add it anywhere"

**Fix:**
- Introduce layered architecture
- Define clear module boundaries
- Refactor incrementally

### God Object

Single object/service that knows and does everything.

**Example:**
- `OrderManager` that handles orders, payments, inventory, shipping, notifications...

**Fix:**
- Split into focused services/objects
- Single Responsibility Principle
- Define clear interfaces

### Chatty API

Multiple round-trips to get necessary data.

**Example:**
```
GET /user/123        → User data
GET /user/123/orders → Order IDs
For each order:
  GET /order/{id}    → Order details
```

**Fix:**
- Aggregate data on backend
- Provide `/user/123?include=orders` endpoint
- Use GraphQL for flexible querying

---

## Examples

### Example 1: E-Commerce System Architecture

**Requirements:**
- 10k orders/day
- 100k users
- Search products, place orders, track shipments
- High availability (99.9%)

**Architecture:**

```
                    ┌──────────┐
                    │   CDN    │ (Static assets)
                    └────┬─────┘
                         │
                    ┌────▼─────┐
Internet ──────────►│   LB     │
                    └────┬─────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     ┌────▼────┐    ┌────▼────┐   ┌────▼────┐
     │ Web App │    │ Web App │   │ Web App │
     └────┬────┘    └────┬────┘   └────┬────┘
          │              │              │
          └──────────────┼──────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     ┌────▼─────┐   ┌────▼──────┐  ┌───▼────┐
     │PostgreSQL│   │   Redis   │  │ Elastic│
     │(Primary) │   │  (Cache)  │  │ Search │
     └────┬─────┘   └───────────┘  └────────┘
          │
     ┌────▼─────┐
     │PostgreSQL│
     │(Replica) │
     └──────────┘
```

**Decisions:**
- **Monolith** (team < 10, domain understood)
- **PostgreSQL** (relational data, ACID needed)
- **Redis** (session storage, caching)
- **Elasticsearch** (product search)
- **Read replicas** (offload reports/analytics)

**Scaling plan:**
1. Vertical scale database (current needs)
2. Add read replicas (read-heavy workload)
3. Cache product catalog (Redis)
4. CDN for images (geographic distribution)
5. Revisit microservices if team grows > 15

### Example 2: Real-Time Analytics Platform

**Requirements:**
- Ingest 100k events/second
- Real-time dashboards (< 1s latency)
- Historical queries (batch)
- High write throughput

**Architecture:**

```
Event Sources
     │
     ▼
┌──────────┐
│  Kafka   │ (Event bus)
└────┬─────┘
     │
     ├─────────────────────┐
     │                     │
     ▼                     ▼
┌──────────┐      ┌─────────────┐
│  Flink   │      │  Spark      │
│(Real-time│      │ (Batch)     │
└────┬─────┘      └──────┬──────┘
     │                   │
     ▼                   ▼
┌──────────┐      ┌─────────────┐
│   Redis  │      │ Data Lake   │
│(Hot data)│      │   (S3)      │
└────┬─────┘      └─────────────┘
     │
     ▼
┌──────────┐
│Dashboard │
└──────────┘
```

**Decisions:**
- **Kafka** (high-throughput event streaming)
- **Flink** (real-time processing)
- **Spark** (batch processing)
- **Redis** (low-latency dashboard queries)
- **S3** (cheap storage for historical data)

**Trade-offs:**
- Eventual consistency (AP over CP)
- Denormalized data (query performance over storage)
- Lambda architecture (complexity for low latency)

### Example 3: Architecture Decision Record (ADR)

**Title:** ADR-001: Use PostgreSQL for Primary Database

**Status:** Accepted

**Context:**
- Need to store user, order, and product data
- Relationships between entities (users → orders → products)
- ACID transactions required (inventory management)
- Team familiar with SQL
- Expected scale: 10k orders/day, 100k users

**Decision:**
Use PostgreSQL as primary database.

**Alternatives Considered:**

1. **MongoDB**
   - Pros: Flexible schema, horizontal scaling
   - Cons: Weaker consistency, team unfamiliar
   - Rejected: ACID requirement, team expertise

2. **DynamoDB**
   - Pros: Fully managed, scalable
   - Cons: Complex queries expensive, vendor lock-in
   - Rejected: Relational queries needed

**Consequences:**

**Positive:**
- Strong consistency (critical for inventory)
- Rich query capabilities (reports, analytics)
- Team expertise (fast development)
- Mature tooling (backups, monitoring)

**Negative:**
- Vertical scaling initially (acceptable for scale)
- Schema migrations required (manageable)

**Risks:**
- May need sharding if scale exceeds single instance
- Mitigation: Monitor growth, plan for read replicas

**Review Date:** 6 months (re-evaluate if scale increases 10x)

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

### When to Use This Skill

- Designing new systems or major features
- Evaluating architecture proposals
- Making technology choices (database, messaging, etc.)
- Troubleshooting scalability or reliability issues
- Reviewing architecture documentation
- Writing Architecture Decision Records (ADRs)

### How to Apply

1. **Understand requirements**
   - Scale (users, throughput, data volume)
   - Consistency needs (strong vs eventual)
   - Availability requirements (uptime %)
   - Latency constraints (response time)
   - Team size and expertise

2. **Identify constraints**
   - Budget
   - Timeline
   - Existing infrastructure
   - Compliance/regulatory requirements

3. **Consider patterns**
   - Start simple (monolith, SQL)
   - Add complexity only when needed
   - Choose based on requirements, not trends

4. **Analyze trade-offs**
   - Make trade-offs explicit
   - Document decision rationale (ADRs)
   - Identify risks and mitigations

5. **Plan for evolution**
   - Design for change
   - Build observability from start
   - Set review dates for decisions

### Red Flags

- No monitoring or logging strategy
- "We'll figure out scaling later"
- Choosing tech because it's trendy
- No clear data consistency model
- Single points of failure (no redundancy)
- No disaster recovery plan
- Premature optimization
- Over-engineering for scale that doesn't exist

---

## References

### Books
- *Designing Data-Intensive Applications* by Martin Kleppmann
- *Building Microservices* by Sam Newman
- *Site Reliability Engineering* by Google
- *The Phoenix Project* by Gene Kim
- *Domain-Driven Design* by Eric Evans

### Patterns
- Martin Fowler's patterns: martinfowler.com/architecture
- Microservices.io patterns catalog
- AWS architecture patterns
- Google Cloud architecture framework

### Tools
- Architecture diagramming: Mermaid, PlantUML, draw.io
- ADR tools: adr-tools, log4brains
- Chaos engineering: Chaos Monkey, Gremlin
- Observability: Prometheus, Grafana, Jaeger

---

This skill provides a foundation for architectural decision-making. Remember: good architecture is not about using the latest technology—it's about choosing the right tool for the job, making trade-offs explicit, and designing systems that can evolve with changing requirements.

Start simple. Measure. Evolve based on data, not assumptions.
