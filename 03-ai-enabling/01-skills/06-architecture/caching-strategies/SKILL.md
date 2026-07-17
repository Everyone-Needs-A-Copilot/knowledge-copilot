---
last_updated: 2026-02-25
status: active
name: caching-strategies
description: Patterns for implementing effective caching at various layers. Use for performance optimization, cache invalidation, and distributed caching decisions.
triggers:
  files: ["**/cache/**", "**/redis/**", "**/memcached/**", "**/cdn/**"]
  keywords: ["cache", "Redis", "Memcached", "CDN", "cache invalidation", "TTL", "cache-aside", "write-through", "cache warming", "distributed cache", "memoization"]
allowed-tools: Read, Write, Edit
---

# Caching Strategies

## Overview

Caching stores copies of frequently accessed data in faster storage to reduce latency and load on primary data sources. Effective caching can dramatically improve application performance, but it also introduces complexity around data consistency and invalidation.

The hardest problem in caching is invalidation—knowing when cached data is stale and should be refreshed. Understanding different caching strategies and their trade-offs helps you choose the right approach for each use case.

This skill covers caching patterns, invalidation strategies, and operational considerations for building effective caching layers.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Concepts

### Why Cache?

**Performance benefits:**
- Reduce latency (memory vs disk, local vs network)
- Decrease load on databases and upstream services
- Handle traffic spikes
- Enable offline functionality

**Trade-offs:**
- Stale data risk
- Memory/storage costs
- Complexity in invalidation
- Cold start problems

### Cache Hit Rate

```
Hit Rate = Cache Hits / (Cache Hits + Cache Misses)
```

**Typical targets:**
- >95% for frequently accessed data
- >80% for moderately accessed data
- Lower rates may indicate poor cache design

### Cache Layers

```
┌──────────────────────────────────────────────────────────────────┐
│                         Client                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Browser Cache (L1)                              │ │
│  │   - HTTP cache headers (Cache-Control, ETag)                │ │
│  │   - LocalStorage, IndexedDB                                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                          CDN (L2)                                  │
│   - Edge caching for static assets                                │
│   - Geographic distribution                                       │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                    Application Server                              │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │          In-Process Cache (L3)                               │  │
│  │   - Local memory cache                                       │  │
│  │   - Fastest access, limited size                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │          Distributed Cache (L4)                              │  │
│  │   - Redis, Memcached                                         │  │
│  │   - Shared across instances                                  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                        Database                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │          Query Cache (L5)                                    │  │
│  │   - Built-in database caching                                │  │
│  │   - Connection pooling                                       │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

---

## Caching Patterns

### Cache-Aside (Lazy Loading)

Application manages cache reads and writes explicitly.

```
┌────────────┐  1. Check cache  ┌────────────┐
│Application │─────────────────►│   Cache    │
│            │◄─────────────────┤            │
│            │  2. Cache miss   └────────────┘
│            │
│            │  3. Query DB     ┌────────────┐
│            │─────────────────►│  Database  │
│            │◄─────────────────┤            │
│            │  4. Return data  └────────────┘
│            │
│            │  5. Update cache ┌────────────┐
│            │─────────────────►│   Cache    │
└────────────┘                  └────────────┘
```

**Implementation:**
```python
def get_user(user_id: str) -> User:
    # 1. Check cache
    cache_key = f"user:{user_id}"
    cached = cache.get(cache_key)
    if cached:
        return deserialize(cached)

    # 2. Cache miss - fetch from DB
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)

    # 3. Update cache
    cache.set(cache_key, serialize(user), ttl=3600)

    return user
```

**Pros:**
- Only cache what's actually used
- Cache failure doesn't break reads (fallback to DB)
- Simple to implement

**Cons:**
- Cache miss penalty (three round trips)
- Stale data until TTL expires
- Cache stampede risk

### Read-Through

Cache handles reads automatically; application only talks to cache.

```
┌────────────┐  1. Request     ┌────────────┐  2. If miss    ┌────────────┐
│Application │────────────────►│   Cache    │───────────────►│  Database  │
│            │◄────────────────┤            │◄───────────────┤            │
│            │  4. Return data │            │  3. Load data  │            │
└────────────┘                 └────────────┘                └────────────┘
```

**Implementation:**
```python
class ReadThroughCache:
    def __init__(self, cache, database, ttl=3600):
        self.cache = cache
        self.database = database
        self.ttl = ttl

    def get(self, key: str, loader: Callable) -> Any:
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        # Cache handles the load
        value = loader()
        self.cache.set(key, value, ttl=self.ttl)
        return value


# Usage
cache = ReadThroughCache(redis, database)
user = cache.get(f"user:{user_id}", lambda: database.get_user(user_id))
```

**Pros:**
- Simpler application code
- Consistent cache logic

**Cons:**
- Tight coupling between cache and data source
- Less flexibility

### Write-Through

Writes go through cache to database synchronously.

```
┌────────────┐  1. Write       ┌────────────┐  2. Write      ┌────────────┐
│Application │────────────────►│   Cache    │───────────────►│  Database  │
│            │◄────────────────┤            │◄───────────────┤            │
│            │  4. Confirm     │            │  3. Confirm    │            │
└────────────┘                 └────────────┘                └────────────┘
```

**Implementation:**
```python
class WriteThroughCache:
    def write(self, key: str, value: Any) -> None:
        # Write to database first
        self.database.save(key, value)

        # Then update cache
        self.cache.set(key, value, ttl=self.ttl)
```

**Pros:**
- Cache always consistent with database
- Simple mental model

**Cons:**
- Write latency (two writes)
- Write failure handling complexity

### Write-Behind (Write-Back)

Writes go to cache immediately; database updated asynchronously.

```
┌────────────┐  1. Write       ┌────────────┐
│Application │────────────────►│   Cache    │
│            │◄────────────────┤            │
│            │  2. Immediate   │            │
│            │     confirm     │            │
└────────────┘                 └────────────┘
                                     │
                            3. Async │ (batched)
                                     ▼
                               ┌────────────┐
                               │  Database  │
                               └────────────┘
```

**Implementation:**
```python
class WriteBehindCache:
    def __init__(self, cache, database, batch_size=100, flush_interval=5):
        self.cache = cache
        self.database = database
        self.pending_writes = []
        self.batch_size = batch_size
        # Background thread flushes periodically

    def write(self, key: str, value: Any) -> None:
        # Update cache immediately
        self.cache.set(key, value)

        # Queue for async database write
        self.pending_writes.append((key, value))

        if len(self.pending_writes) >= self.batch_size:
            self._flush()

    def _flush(self):
        if not self.pending_writes:
            return
        # Batch write to database
        self.database.batch_save(self.pending_writes)
        self.pending_writes.clear()
```

**Pros:**
- Fast writes (no database wait)
- Batching improves database efficiency
- Handles write spikes

**Cons:**
- Data loss risk if cache fails before flush
- Complexity in failure handling
- Eventual consistency

### Refresh-Ahead

Proactively refresh cache before expiration.

```python
class RefreshAheadCache:
    def __init__(self, cache, ttl=3600, refresh_threshold=0.8):
        self.cache = cache
        self.ttl = ttl
        self.refresh_threshold = refresh_threshold  # Refresh at 80% of TTL

    def get(self, key: str, loader: Callable) -> Any:
        cached, ttl_remaining = self.cache.get_with_ttl(key)

        if cached is None:
            # Cache miss - load and cache
            value = loader()
            self.cache.set(key, value, ttl=self.ttl)
            return value

        # Check if should refresh
        if ttl_remaining < self.ttl * (1 - self.refresh_threshold):
            # Near expiration - refresh in background
            self._async_refresh(key, loader)

        return cached

    def _async_refresh(self, key: str, loader: Callable):
        # Run in background thread/task
        asyncio.create_task(self._do_refresh(key, loader))

    async def _do_refresh(self, key: str, loader: Callable):
        value = loader()
        self.cache.set(key, value, ttl=self.ttl)
```

**Pros:**
- No cache miss latency for hot data
- Smooth performance

**Cons:**
- Wasted refreshes for unused data
- Complexity

---

## Cache Invalidation Strategies

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

### Time-Based Expiration (TTL)

Set a time-to-live; data expires automatically.

```python
# Set with TTL
cache.set("user:123", user_data, ttl=3600)  # Expires in 1 hour

# Consider staleness tolerance
# High-frequency changing data: short TTL (seconds to minutes)
# Slowly changing data: longer TTL (hours to days)
# Static data: very long TTL or no expiration
```

**TTL guidelines:**
| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| Session data | 15-30 min | Security, memory |
| User profile | 5-15 min | Moderate change frequency |
| Product catalog | 1-24 hours | Relatively stable |
| Static content | Days/weeks | Rarely changes |
| Real-time data | Seconds | Must be fresh |

### Event-Based Invalidation

Invalidate cache when source data changes.

```python
# On user update
def update_user(user_id: str, updates: dict) -> None:
    # Update database
    database.update("users", user_id, updates)

    # Invalidate cache
    cache.delete(f"user:{user_id}")

    # Also invalidate derived caches
    cache.delete(f"user_orders:{user_id}")
    cache.delete(f"user_profile:{user_id}")
```

**Pattern: Publish invalidation events**
```python
# Publisher
def update_user(user_id: str, updates: dict):
    database.update("users", user_id, updates)
    event_bus.publish(UserUpdated(user_id=user_id))

# Subscriber (can be multiple services)
@subscribe(UserUpdated)
def invalidate_user_cache(event: UserUpdated):
    cache.delete(f"user:{event.user_id}")
```

### Version-Based Invalidation

Include version in cache key; new version = new key.

```python
# Get current version
version = database.get_version("products_catalog")  # e.g., "v42"

# Cache with version in key
cache_key = f"products:{version}"
products = cache.get(cache_key)

if not products:
    products = database.get_all_products()
    cache.set(cache_key, products, ttl=86400)

# When catalog changes, increment version
# Old cached data naturally becomes orphaned
```

### Tag-Based Invalidation

Associate cache entries with tags for bulk invalidation.

```python
class TaggedCache:
    def set(self, key: str, value: Any, tags: List[str], ttl: int = 3600):
        self.cache.set(key, value, ttl=ttl)
        for tag in tags:
            self.cache.sadd(f"tag:{tag}", key)

    def invalidate_tag(self, tag: str):
        keys = self.cache.smembers(f"tag:{tag}")
        for key in keys:
            self.cache.delete(key)
        self.cache.delete(f"tag:{tag}")


# Usage
cache.set("user:123", user_data, tags=["users", "active_users"])
cache.set("user:456", user_data, tags=["users", "premium_users"])

# Invalidate all users
cache.invalidate_tag("users")
```

---

## Distributed Caching

### Redis

**Common patterns:**

**Simple key-value:**
```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# String
r.set("user:123", json.dumps(user_data), ex=3600)
user = json.loads(r.get("user:123"))

# Hash (multiple fields)
r.hset("user:123", mapping={"name": "John", "email": "john@example.com"})
name = r.hget("user:123", "name")
all_fields = r.hgetall("user:123")

# Sorted set (leaderboard)
r.zadd("leaderboard", {"user:123": 1000, "user:456": 950})
top_10 = r.zrevrange("leaderboard", 0, 9, withscores=True)
```

**Atomic operations:**
```python
# Increment counter
r.incr("page_views:home")

# Set if not exists (for locking)
acquired = r.setnx("lock:process_order:123", "worker-1")
if acquired:
    r.expire("lock:process_order:123", 30)  # Lock timeout
    # Do work
    r.delete("lock:process_order:123")

# Lua script for atomic operations
RATE_LIMIT_SCRIPT = """
local current = redis.call('GET', KEYS[1])
if current and tonumber(current) >= tonumber(ARGV[1]) then
    return 0
end
redis.call('INCR', KEYS[1])
redis.call('EXPIRE', KEYS[1], ARGV[2])
return 1
"""
allowed = r.eval(RATE_LIMIT_SCRIPT, 1, "rate:user:123", 100, 60)
```

### Memcached

**Simple, fast, distributed:**
```python
import memcache

mc = memcache.Client(['127.0.0.1:11211'])

# Basic operations
mc.set("user:123", user_data, time=3600)
user = mc.get("user:123")

# Batch operations
users = mc.get_multi(["user:123", "user:456", "user:789"])

# CAS (Check-And-Set) for optimistic locking
while True:
    val, cas = mc.gets("counter")
    new_val = val + 1
    if mc.cas("counter", new_val, cas):
        break  # Success
    # Retry on collision
```

### Comparison

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data structures | Rich (strings, lists, sets, hashes, streams) | Strings only |
| Persistence | Optional (RDB, AOF) | No |
| Replication | Built-in | No |
| Pub/Sub | Yes | No |
| Lua scripting | Yes | No |
| Memory efficiency | Less efficient | More efficient |
| Clustering | Redis Cluster | Client-side sharding |

**Choose Redis when:**
- Need data structures beyond key-value
- Need persistence or replication
- Need pub/sub or scripting

**Choose Memcached when:**
- Simple key-value caching
- Maximum memory efficiency
- Simple horizontal scaling

---

## HTTP Caching

### Cache-Control Header

```
Cache-Control: public, max-age=3600, s-maxage=86400
```

**Directives:**
| Directive | Meaning |
|-----------|---------|
| `public` | Can be cached by browsers and CDNs |
| `private` | Only browser cache, not CDN |
| `no-cache` | Must revalidate with server |
| `no-store` | Don't cache at all |
| `max-age=N` | Fresh for N seconds |
| `s-maxage=N` | CDN-specific max-age |
| `stale-while-revalidate=N` | Serve stale while refreshing |

### ETag and Conditional Requests

```
# Server response
HTTP/1.1 200 OK
ETag: "abc123"
Content-Type: application/json

{"name": "John"}

# Client conditional request
GET /users/123
If-None-Match: "abc123"

# Server response if unchanged
HTTP/1.1 304 Not Modified
```

**Implementation:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: str, request: Request):
    user = database.get_user(user_id)
    etag = hashlib.md5(json.dumps(user).encode()).hexdigest()

    if request.headers.get("If-None-Match") == etag:
        return Response(status_code=304)

    return Response(
        content=json.dumps(user),
        headers={"ETag": etag, "Cache-Control": "max-age=300"}
    )
```

### CDN Caching

**Configure caching at the edge:**
```python
@app.get("/static/{path}")
def serve_static(path: str):
    content = read_static_file(path)
    return Response(
        content=content,
        headers={
            "Cache-Control": "public, max-age=31536000",  # 1 year
            "CDN-Cache-Control": "max-age=86400",  # CDN: 1 day
        }
    )

@app.get("/api/products")
def get_products():
    products = database.get_products()
    return Response(
        content=json.dumps(products),
        headers={
            "Cache-Control": "public, s-maxage=300",  # CDN: 5 min
            "Surrogate-Key": "products",  # For invalidation
        }
    )
```

**CDN invalidation:**
```python
# Invalidate by path
cdn.purge("/api/products")

# Invalidate by surrogate key (more efficient)
cdn.purge_key("products")
```

---

## Cache Warming

Pre-populate cache before traffic hits.

### Startup Warming

```python
class CacheWarmer:
    def warm(self):
        # Load frequently accessed data
        popular_products = database.get_popular_products(limit=1000)
        for product in popular_products:
            cache.set(f"product:{product.id}", product)

        # Load configuration
        config = database.get_config()
        cache.set("app_config", config)

        # Load user sessions (if persistent)
        active_sessions = database.get_active_sessions()
        for session in active_sessions:
            cache.set(f"session:{session.id}", session)

# Run on application startup
@app.on_event("startup")
async def startup():
    CacheWarmer().warm()
```

### Scheduled Warming

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', minutes=5)
def warm_trending_cache():
    trending = analytics.get_trending_products()
    for product_id in trending:
        product = database.get_product(product_id)
        cache.set(f"product:{product_id}", product, ttl=600)

@scheduler.scheduled_job('cron', hour=0, minute=0)  # Daily at midnight
def warm_daily_cache():
    # Pre-compute daily aggregates
    daily_stats = analytics.compute_daily_stats()
    cache.set("daily_stats", daily_stats, ttl=86400)
```

---

## Cache Stampede Prevention

Multiple clients simultaneously miss cache and hammer the database.

### Locking

Only one client fetches; others wait.

```python
def get_with_lock(key: str, loader: Callable, ttl: int = 3600) -> Any:
    # Try cache first
    cached = cache.get(key)
    if cached is not None:
        return cached

    # Acquire lock
    lock_key = f"lock:{key}"
    if cache.setnx(lock_key, "1"):
        cache.expire(lock_key, 30)  # Lock timeout
        try:
            # Load data
            value = loader()
            cache.set(key, value, ttl=ttl)
            return value
        finally:
            cache.delete(lock_key)
    else:
        # Wait for lock holder
        for _ in range(50):  # Max 5 seconds
            time.sleep(0.1)
            cached = cache.get(key)
            if cached is not None:
                return cached
        # Timeout - load anyway
        return loader()
```

### Probabilistic Early Expiration

Randomly refresh before actual expiration.

```python
def get_with_early_expiration(
    key: str,
    loader: Callable,
    ttl: int = 3600,
    beta: float = 1.0  # Higher = more aggressive refresh
) -> Any:
    cached, ttl_remaining = cache.get_with_ttl(key)

    if cached is None:
        value = loader()
        cache.set(key, value, ttl=ttl)
        return value

    # Probabilistic early refresh
    # As TTL approaches 0, probability of refresh increases
    delta = ttl - ttl_remaining
    if delta > 0:
        xfetch = delta * beta * math.log(random.random())
        if ttl_remaining + xfetch <= 0:
            # Refresh in background
            asyncio.create_task(async_refresh(key, loader, ttl))

    return cached
```

### Request Coalescing

Batch identical concurrent requests.

```python
from asyncio import Lock
from collections import defaultdict

class CoalescingCache:
    def __init__(self, cache):
        self.cache = cache
        self.pending = defaultdict(Lock)
        self.results = {}

    async def get(self, key: str, loader: Callable) -> Any:
        # Try cache
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        # Coalesce concurrent requests
        async with self.pending[key]:
            # Check again (another request might have loaded)
            cached = self.cache.get(key)
            if cached is not None:
                return cached

            # Load and cache
            value = await loader()
            self.cache.set(key, value)
            return value
```

---

## Monitoring and Metrics

### Key Metrics

```python
# Cache hit rate
cache_hits = Counter('cache_hits_total', 'Total cache hits', ['cache_name'])
cache_misses = Counter('cache_misses_total', 'Total cache misses', ['cache_name'])

# Hit rate = hits / (hits + misses)

# Latency
cache_latency = Histogram('cache_operation_seconds', 'Cache operation latency',
                          ['operation', 'cache_name'])

# Memory usage
cache_memory = Gauge('cache_memory_bytes', 'Cache memory usage', ['cache_name'])

# Evictions
cache_evictions = Counter('cache_evictions_total', 'Cache evictions', ['cache_name'])
```

### Alerting

```yaml
# Alert on low hit rate
- alert: LowCacheHitRate
  expr: |
    sum(rate(cache_hits_total[5m])) /
    (sum(rate(cache_hits_total[5m])) + sum(rate(cache_misses_total[5m]))) < 0.8
  for: 10m
  annotations:
    summary: "Cache hit rate below 80%"

# Alert on high latency
- alert: HighCacheLatency
  expr: histogram_quantile(0.99, cache_operation_seconds) > 0.1
  for: 5m
  annotations:
    summary: "Cache p99 latency > 100ms"

# Alert on memory pressure
- alert: CacheMemoryHigh
  expr: cache_memory_bytes / cache_memory_limit_bytes > 0.9
  for: 5m
  annotations:
    summary: "Cache memory usage > 90%"
```

---

## Anti-Patterns

### Caching Too Much

```python
# ANTI-PATTERN: Cache everything
def get_user(user_id):
    cache_key = f"user:{user_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    user = database.get_user(user_id)
    cache.set(cache_key, user)  # Even rarely accessed users

    return user

# BETTER: Cache based on access patterns
def get_user(user_id):
    # Only cache hot users
    if is_hot_user(user_id):
        cache_key = f"user:{user_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        user = database.get_user(user_id)
        cache.set(cache_key, user, ttl=3600)
        return user
    return database.get_user(user_id)
```

### Ignoring Cache Failures

```python
# ANTI-PATTERN: No fallback
def get_user(user_id):
    return cache.get(f"user:{user_id}")  # Returns None if cache down!

# BETTER: Fallback to source
def get_user(user_id):
    try:
        cached = cache.get(f"user:{user_id}")
        if cached:
            return cached
    except CacheError:
        pass  # Cache unavailable, continue to DB

    return database.get_user(user_id)
```

### Caching Null Results

```python
# ANTI-PATTERN: Don't cache misses
def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return cached

    user = database.get_user(user_id)
    if user:  # Only cache if found
        cache.set(f"user:{user_id}", user)
    return user
    # Problem: Repeated DB queries for non-existent users

# BETTER: Cache negative results with short TTL
def get_user(user_id):
    cache_key = f"user:{user_id}"
    cached = cache.get(cache_key)
    if cached == "NOT_FOUND":
        return None
    if cached:
        return cached

    user = database.get_user(user_id)
    if user:
        cache.set(cache_key, user, ttl=3600)
    else:
        cache.set(cache_key, "NOT_FOUND", ttl=60)  # Short TTL for negatives
    return user
```

### No Invalidation Strategy

```python
# ANTI-PATTERN: Cache forever, hope for the best
cache.set("user:123", user_data)  # No TTL, no invalidation

# BETTER: Explicit strategy
# Option 1: TTL
cache.set("user:123", user_data, ttl=3600)

# Option 2: Event-based invalidation
@event_handler(UserUpdated)
def on_user_updated(event):
    cache.delete(f"user:{event.user_id}")
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

### When to Cache

**Good candidates:**
- Frequently read, rarely changed data
- Expensive computations
- Data tolerant of staleness
- Predictable access patterns

**Poor candidates:**
- Frequently changing data
- Security-sensitive data
- One-time access data
- Data requiring strong consistency

### How to Apply

1. **Identify bottlenecks**: Profile before caching
2. **Choose appropriate layer**: Browser, CDN, application, database
3. **Select caching pattern**: Cache-aside, write-through, etc.
4. **Define invalidation strategy**: TTL, events, versions
5. **Handle cache failures**: Fallback to source
6. **Monitor and tune**: Hit rate, latency, memory

### Red Flags

- No TTL on cached data
- No cache failure handling
- Caching user-specific data in shared cache without proper keys
- No monitoring of hit rates
- Cache stampede risk on popular keys
- Inconsistent data due to stale cache

---

## References

### Tools
- Redis (distributed cache)
- Memcached (simple distributed cache)
- Varnish (HTTP accelerator)
- CDNs: Cloudflare, Fastly, AWS CloudFront

### Resources
- *Designing Data-Intensive Applications* by Martin Kleppmann
- Redis documentation
- Cloudflare caching guides
