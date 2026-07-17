---
last_updated: 2026-02-25
status: active
name: scalability-patterns
description: Patterns for scaling systems to handle increased load. Use for horizontal/vertical scaling, load balancing, and capacity planning decisions.
triggers:
  files: ["**/infrastructure/**", "**/scaling/**", "**/load-balancer/**", "**/kubernetes/**"]
  keywords: ["scalability", "horizontal scaling", "vertical scaling", "load balancing", "sharding", "partitioning", "capacity planning", "auto-scaling", "stateless", "throughput", "performance"]
allowed-tools: Read, Write, Edit
---

# Scalability Patterns

## Overview

Scalability is the ability of a system to handle increased load by adding resources. A scalable system can grow to accommodate more users, data, or transactions without fundamental redesign.

Scalability is not just about handling more load—it's about doing so economically and maintainably. The goal is to scale the parts of the system that need it, when they need it, without over-provisioning or creating operational complexity.

This skill covers patterns for scaling compute, data, and networks, along with strategies for identifying bottlenecks and planning capacity.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Concepts

### Scalability vs Performance

**Performance:** How fast a system responds to a single request
**Scalability:** How well a system handles increased load

A system can be performant but not scalable (fast but can't handle more users), or scalable but not performant (handles many users but slowly).

### Load Characteristics

**Throughput:** Requests per second, transactions per second
**Latency:** Time to process a single request
**Concurrency:** Number of simultaneous operations

### Amdahl's Law

The speedup from parallelization is limited by the sequential portion of the workload.

```
Speedup = 1 / (S + P/N)

S = Sequential fraction
P = Parallelizable fraction (P = 1 - S)
N = Number of processors
```

**Example:**
- If 20% of work is sequential (S = 0.2)
- Maximum speedup = 1/0.2 = 5x, regardless of how many processors

**Implication:** Identify and minimize sequential bottlenecks before scaling horizontally.

---

## Scaling Strategies

### Vertical Scaling (Scale Up)

Add more resources to existing machines.

```
Before:           After:
┌──────────┐     ┌──────────────┐
│ 4 CPU    │     │ 16 CPU       │
│ 16GB RAM │ ──► │ 64GB RAM     │
│ 500GB SSD│     │ 2TB NVMe     │
└──────────┘     └──────────────┘
```

**Advantages:**
- Simple (no code changes)
- No distributed system complexity
- Maintains ACID transactions easily

**Disadvantages:**
- Hardware limits (can't scale indefinitely)
- Single point of failure
- Expensive at high end
- Downtime during upgrade

**When to use:**
- Starting out (before complexity is needed)
- Database servers (easier than sharding)
- When cost < complexity

### Horizontal Scaling (Scale Out)

Add more machines to the pool.

```
Before:                After:
┌──────────┐          ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Server 1 │   ──►    │ Server 1 │ │ Server 2 │ │ Server 3 │
└──────────┘          └──────────┘ └──────────┘ └──────────┘
```

**Advantages:**
- Near-infinite scaling potential
- Redundancy and fault tolerance
- Cost-effective (commodity hardware)
- No downtime for scaling

**Disadvantages:**
- Distributed system complexity
- Data consistency challenges
- Network latency between nodes
- Operational overhead

**When to use:**
- Stateless application servers
- When vertical limits reached
- When fault tolerance required
- Commodity workloads

### Diagonal Scaling

Combine vertical and horizontal scaling.

```
Phase 1: Vertical (quick wins)
┌──────────┐     ┌──────────────┐
│ Small    │ ──► │ Medium       │
└──────────┘     └──────────────┘

Phase 2: Horizontal (when limits reached)
┌──────────────┐     ┌────────┐ ┌────────┐ ┌────────┐
│ Medium       │ ──► │ Medium │ │ Medium │ │ Medium │
└──────────────┘     └────────┘ └────────┘ └────────┘
```

**Strategy:**
1. Scale vertically until cost-prohibitive
2. Scale horizontally for additional capacity
3. Continue vertical scaling individual nodes as needed

---

## Stateless Architecture

Enable horizontal scaling by removing server-side state.

### The Problem with State

```
┌──────────────────────────────────────────────┐
│              Load Balancer                    │
└───────────────────┬──────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │Server 1│  │Server 2│  │Server 3│
   │Session │  │        │  │        │
   │ data!  │  │        │  │        │
   └────────┘  └────────┘  └────────┘

User's session is on Server 1.
If routed to Server 2, session is lost!
```

### Externalize State

Move state to shared storage.

```
┌──────────────────────────────────────────────┐
│              Load Balancer                    │
└───────────────────┬──────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │Server 1│  │Server 2│  │Server 3│
   │Stateless│  │Stateless│  │Stateless│
   └────┬───┘  └────┬───┘  └────┬───┘
        │           │           │
        └───────────┼───────────┘
                    │
             ┌──────▼──────┐
             │    Redis    │
             │ (Sessions)  │
             └─────────────┘
```

### Implementation

```python
# BAD: In-memory session storage
sessions = {}  # Lost on restart, not shared across instances

@app.post("/login")
def login(credentials):
    user = authenticate(credentials)
    session_id = generate_session_id()
    sessions[session_id] = user  # Local only!
    return {"session_id": session_id}

# GOOD: Externalized session storage
@app.post("/login")
def login(credentials):
    user = authenticate(credentials)
    session_id = generate_session_id()
    redis.setex(f"session:{session_id}", 3600, json.dumps(user))
    return {"session_id": session_id}

@app.get("/profile")
def get_profile(session_id: str):
    user_data = redis.get(f"session:{session_id}")
    if not user_data:
        raise HTTPException(401, "Session expired")
    return json.loads(user_data)
```

### JWT for Stateless Auth

Token contains all needed information.

```python
import jwt

def create_token(user):
    return jwt.encode({
        "user_id": user.id,
        "email": user.email,
        "roles": user.roles,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
```

---

## Load Balancing

Distribute traffic across multiple servers.

### Algorithms

**Round Robin:**
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A
...
```
- Simple, fair distribution
- Ignores server load

**Weighted Round Robin:**
```
Server A (weight=3): 3 requests per cycle
Server B (weight=2): 2 requests per cycle
Server C (weight=1): 1 request per cycle
```
- Accounts for different server capacities

**Least Connections:**
```
Route to server with fewest active connections
```
- Better for varying request durations
- Requires tracking connection state

**IP Hash:**
```
hash(client_ip) % num_servers → server
```
- Sticky sessions (same client → same server)
- Useful when some state is local

**Least Response Time:**
```
Route to server with fastest recent response
```
- Adapts to server performance
- More complex to implement

### Health Checks

Detect and avoid unhealthy servers.

```yaml
# NGINX example
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;

    # Health check
    health_check interval=5s fails=3 passes=2;
}
```

**Health check types:**
- **TCP:** Can connect to port
- **HTTP:** Returns 2xx status
- **Custom:** Application-specific endpoint

```python
@app.get("/health")
def health_check():
    # Check dependencies
    try:
        database.execute("SELECT 1")
        redis.ping()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503
```

### Layer 4 vs Layer 7

**Layer 4 (Transport):**
- Routes based on IP/port
- Fast, simple
- No application awareness
- Example: HAProxy in TCP mode

**Layer 7 (Application):**
- Routes based on HTTP content (path, headers)
- Can modify requests/responses
- SSL termination
- Example: NGINX, AWS ALB

```nginx
# Layer 7 routing by path
location /api/ {
    proxy_pass http://api_servers;
}

location /static/ {
    proxy_pass http://static_servers;
}
```

---

## Database Scaling

### Read Replicas

Distribute read load across copies.

```
                    ┌──────────────┐
       Writes ─────►│   Primary    │
                    │   (Write)    │
                    └──────┬───────┘
                           │ Replication
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │Replica │   │Replica │   │Replica │
         │  (Read)│   │  (Read)│   │  (Read)│
         └────────┘   └────────┘   └────────┘
```

**Implementation:**
```python
class DatabasePool:
    def __init__(self, primary_url, replica_urls):
        self.primary = create_connection(primary_url)
        self.replicas = [create_connection(url) for url in replica_urls]
        self.replica_index = 0

    def get_write_connection(self):
        return self.primary

    def get_read_connection(self):
        # Round-robin across replicas
        conn = self.replicas[self.replica_index]
        self.replica_index = (self.replica_index + 1) % len(self.replicas)
        return conn

# Usage
def get_user(user_id):
    with db.get_read_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", user_id)

def create_user(user):
    with db.get_write_connection() as conn:
        conn.execute("INSERT INTO users ...", user)
```

**Considerations:**
- Replication lag (reads may be stale)
- Read-after-write consistency

### Sharding (Horizontal Partitioning)

Distribute data across multiple databases.

```
                    ┌──────────────┐
                    │   Router     │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    ┌─────────┐       ┌─────────┐       ┌─────────┐
    │ Shard 0 │       │ Shard 1 │       │ Shard 2 │
    │Users 0-N│       │Users N-M│       │Users M+ │
    └─────────┘       └─────────┘       └─────────┘
```

**Sharding strategies:**

**Range-based:**
```python
def get_shard(user_id: int) -> str:
    if user_id < 1000000:
        return "shard_0"
    elif user_id < 2000000:
        return "shard_1"
    else:
        return "shard_2"
```
- Easy to understand
- Hotspots if data skewed

**Hash-based:**
```python
def get_shard(user_id: int, num_shards: int = 3) -> str:
    shard_num = hash(user_id) % num_shards
    return f"shard_{shard_num}"
```
- Even distribution
- Difficult to add shards (requires rehashing)

**Consistent hashing:**
```python
import hashlib
from bisect import bisect

class ConsistentHash:
    def __init__(self, nodes, replicas=100):
        self.ring = []
        self.nodes = {}
        for node in nodes:
            for i in range(replicas):
                key = self._hash(f"{node}:{i}")
                self.ring.append(key)
                self.nodes[key] = node
        self.ring.sort()

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_node(self, key):
        h = self._hash(str(key))
        idx = bisect(self.ring, h) % len(self.ring)
        return self.nodes[self.ring[idx]]
```
- Adding/removing nodes affects minimal data
- More complex to implement

**Shard key selection:**
- Must be in every query
- Should distribute evenly
- Common choices: user_id, tenant_id, region

### Connection Pooling

Reuse database connections.

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=10,        # Normal pool size
    max_overflow=20,     # Extra connections when needed
    pool_timeout=30,     # Wait time for connection
    pool_recycle=1800,   # Recycle connections after 30 min
)
```

**Benefits:**
- Avoid connection setup overhead
- Control maximum connections
- Prevent database overload

---

## Caching for Scale

### Caching Layers

```
┌──────────────────────────────────────────────────┐
│                    Request                        │
└───────────────────────┬──────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────┐
│                 CDN Cache                          │
│            (Static assets, API responses)          │
└───────────────────────┬───────────────────────────┘
                        │ Miss
                        ▼
┌───────────────────────────────────────────────────┐
│              Application Cache                     │
│             (Redis, Memcached)                     │
└───────────────────────┬───────────────────────────┘
                        │ Miss
                        ▼
┌───────────────────────────────────────────────────┐
│                Database                            │
└───────────────────────────────────────────────────┘
```

### Cache Effectiveness

```
Cache Hit Ratio = Hits / (Hits + Misses)

Without cache: 1000 req/s × 100ms/req = 100s of DB time/s
With 90% hit rate: 100 req/s × 100ms/req = 10s of DB time/s
10x reduction in database load!
```

### Hot Spot Caching

Cache the most accessed items more aggressively.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]

    def set(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove least recently used
```

---

## Asynchronous Processing

### Message Queues

Decouple request from processing.

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ Producer │────►│    Queue     │────►│   Workers    │
│ (Fast)   │     │              │     │  (Process)   │
└──────────┘     └──────────────┘     └──────────────┘

User request returns immediately.
Heavy processing happens asynchronously.
```

**Example: Image processing**
```python
# API endpoint - fast
@app.post("/images")
async def upload_image(file: UploadFile):
    image_id = str(uuid4())
    storage.save(file, f"uploads/{image_id}")

    # Queue processing
    queue.send(ProcessImageTask(image_id=image_id))

    return {"image_id": image_id, "status": "processing"}

# Worker - can scale independently
@worker.task
def process_image(task: ProcessImageTask):
    image = storage.load(f"uploads/{task.image_id}")
    thumbnail = create_thumbnail(image)
    storage.save(thumbnail, f"thumbnails/{task.image_id}")
    database.update_image_status(task.image_id, "ready")
```

### Event-Driven Scaling

Scale consumers based on queue depth.

```
Queue Depth: 1000 messages
Workers: 2 → Scale to 10 workers

Queue Depth: 10 messages
Workers: 10 → Scale to 2 workers
```

```yaml
# Kubernetes HPA based on queue depth
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: worker
  minReplicas: 2
  maxReplicas: 50
  metrics:
  - type: External
    external:
      metric:
        name: queue_depth
        selector:
          matchLabels:
            queue: image-processing
      target:
        type: AverageValue
        averageValue: "30"  # Target 30 messages per worker
```

---

## Auto-Scaling

### Metrics for Scaling

**CPU-based:**
```yaml
# Scale when average CPU > 70%
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 70
```

**Memory-based:**
```yaml
# Scale when memory > 80%
metrics:
- type: Resource
  resource:
    name: memory
    target:
      type: Utilization
      averageUtilization: 80
```

**Request-based:**
```yaml
# Scale to maintain 100 requests per pod
metrics:
- type: Pods
  pods:
    metric:
      name: http_requests_per_second
    target:
      type: AverageValue
      averageValue: "100"
```

**Custom metrics:**
```yaml
# Scale based on queue depth
metrics:
- type: External
  external:
    metric:
      name: queue_messages_ready
    target:
      type: Value
      value: "100"
```

### Scaling Policies

**Cool-down periods:**
```yaml
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60  # Max 10% scale down per minute
  scaleUp:
    stabilizationWindowSeconds: 0  # Scale up immediately
    policies:
    - type: Pods
      value: 4
      periodSeconds: 60  # Add up to 4 pods per minute
```

### Predictive Scaling

Scale before traffic arrives.

```python
# Schedule-based scaling for known patterns
SCHEDULE = {
    "weekday_morning": {"time": "09:00", "min_replicas": 20},
    "weekday_evening": {"time": "18:00", "min_replicas": 10},
    "weekend": {"time": "00:00", "min_replicas": 5},
}

# ML-based prediction
def predict_load(current_metrics, historical_data):
    # Use time series forecasting
    model = load_forecast_model()
    predicted_load = model.predict(current_metrics, horizon="1h")
    return predicted_load
```

---

## Content Delivery Networks (CDN)

### How CDNs Work

```
                    ┌────────────────────┐
                    │   Origin Server    │
                    │   (your server)    │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         ┌─────────┐    ┌─────────┐    ┌─────────┐
         │  Edge   │    │  Edge   │    │  Edge   │
         │  (NYC)  │    │  (LDN)  │    │  (TKY)  │
         └────┬────┘    └────┬────┘    └────┬────┘
              │              │              │
         ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
         │ Users   │    │ Users   │    │ Users   │
         │ (East)  │    │(Europe) │    │ (Asia)  │
         └─────────┘    └─────────┘    └─────────┘
```

### Caching Strategies

**Static content:**
```
# Long cache for versioned assets
/static/app.v123.js
Cache-Control: public, max-age=31536000, immutable

# Short cache for index.html
/
Cache-Control: public, max-age=60
```

**API responses:**
```
# Cache product listings at edge
GET /api/products
Cache-Control: public, s-maxage=300
Vary: Accept-Encoding
```

**Personalized content:**
```
# Don't cache at CDN
GET /api/user/profile
Cache-Control: private, no-store
```

### Edge Computing

Run code at CDN edge locations.

```javascript
// Cloudflare Worker example
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)

  // A/B testing at edge
  const variant = Math.random() < 0.5 ? 'A' : 'B'
  url.pathname = `/${variant}${url.pathname}`

  // Geolocation routing
  const country = request.cf.country
  if (country === 'CN') {
    return Response.redirect('https://china.example.com' + url.pathname)
  }

  return fetch(url)
}
```

---

## Capacity Planning

### Metrics to Track

**Resource utilization:**
- CPU usage (%)
- Memory usage (%)
- Disk I/O
- Network bandwidth

**Application metrics:**
- Requests per second
- Response time (p50, p95, p99)
- Error rate
- Queue depth

**Business metrics:**
- Active users
- Transactions per hour
- Data volume growth

### Load Testing

**Types:**
- **Smoke test:** Minimal load, verify system works
- **Load test:** Expected peak load
- **Stress test:** Beyond capacity, find breaking point
- **Soak test:** Sustained load over time

**Example with k6:**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay at peak
    { duration: '2m', target: 200 },  // Increase load
    { duration: '5m', target: 200 },  // Stay at higher peak
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // Less than 1% errors
  },
};

export default function() {
  const res = http.get('https://api.example.com/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### Capacity Model

```
Current capacity:
- 10 servers
- 1000 req/s per server
- Total: 10,000 req/s

Traffic growth:
- Current: 5,000 req/s
- Growth rate: 20%/month
- In 6 months: 5,000 × 1.2^6 = 14,900 req/s

Required capacity:
- Need 15 servers in 6 months
- Add 50% buffer: 22 servers
- Plan scaling events quarterly
```

---

## Anti-Patterns

### Premature Optimization

```python
# ANTI-PATTERN: Sharding from day one
# "We might have millions of users!"
# (Currently have 100 users)

# BETTER: Scale when needed
# Start with simple PostgreSQL
# Add read replicas when reads are slow
# Shard only when vertical scaling exhausted
```

### Ignoring Database

```
# ANTI-PATTERN: Scale app servers but not database
┌──────────────────────────────────────────────┐
│              Load Balancer                    │
└───────────────────┬──────────────────────────┘
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │Server 1│  │Server 2│  │Server 3│
   └────┬───┘  └────┬───┘  └────┬───┘
        └───────────┼───────────┘
                    │
             ┌──────▼──────┐
             │  Database   │ ← Bottleneck!
             │  (Single)   │
             └─────────────┘
```

### Stateful Services

```python
# ANTI-PATTERN: Local state
class OrderService:
    def __init__(self):
        self.pending_orders = {}  # Can't scale horizontally!

    def process_order(self, order_id):
        self.pending_orders[order_id] = "processing"
        # ...

# BETTER: External state
class OrderService:
    def __init__(self, redis):
        self.redis = redis

    def process_order(self, order_id):
        self.redis.set(f"order:{order_id}:status", "processing")
        # ...
```

### Over-Engineering

```
# ANTI-PATTERN: Kubernetes for 3 services
# - Complex infrastructure
# - High operational overhead
# - Premature for small scale

# BETTER: Match complexity to needs
# - Heroku/Railway for startups
# - Docker Compose for small teams
# - Kubernetes when truly needed
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

### When to Scale

**Scale when:**
- Response times increasing
- Resource utilization consistently >70%
- Error rates increasing
- Approaching known capacity limits

**Don't scale prematurely:**
- Optimize first (queries, algorithms, caching)
- Profile to find actual bottlenecks
- Scale the bottleneck, not everything

### How to Apply

1. **Measure first**: Know your bottleneck
2. **Start simple**: Vertical before horizontal
3. **Design for statelessness**: Enable horizontal scaling
4. **Cache aggressively**: Reduce load on expensive operations
5. **Use async where possible**: Decouple and scale independently
6. **Automate scaling**: Use auto-scaling policies
7. **Plan for growth**: Capacity planning and load testing

### Red Flags

- Stateful application servers
- Single database without replication
- No caching layer
- Manual scaling processes
- No load testing
- Unknown capacity limits
- Scaling everything uniformly

---

## References

### Books
- *Designing Data-Intensive Applications* by Martin Kleppmann
- *The Art of Scalability* by Abbott & Fisher
- *High Performance Browser Networking* by Ilya Grigorik

### Tools
- Load testing: k6, Locust, JMeter
- Monitoring: Prometheus, Grafana, Datadog
- Auto-scaling: Kubernetes HPA, AWS Auto Scaling
- CDN: Cloudflare, Fastly, AWS CloudFront
