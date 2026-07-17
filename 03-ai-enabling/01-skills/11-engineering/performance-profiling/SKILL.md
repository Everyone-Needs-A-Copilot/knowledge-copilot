---
last_updated: 2026-02-25
status: active
name: performance-profiling
description: Measure, analyze, and optimize application performance. Activate when investigating slowness or optimizing critical paths.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["performance", "profiling", "slow", "optimize", "latency", "throughput", "bottleneck", "benchmark", "profile"]
allowed-tools: Read, Write, Edit
---

# Performance Profiling

Measure first, optimize second. This skill covers systematic performance analysis and optimization techniques.

## Core Principles

| Principle | Practice |
|-----------|----------|
| **Measure, don't guess** | Profile before optimizing |
| **Optimize bottlenecks** | 80% of time in 20% of code |
| **Set targets** | Know "fast enough" |
| **Compare baselines** | Measure before and after |

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Performance Metrics

### Key Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **Latency** | Time to complete operation | p50, p95, p99 |
| **Throughput** | Operations per time unit | req/sec, tx/sec |
| **Resource usage** | CPU, memory, I/O | % utilization |
| **Error rate** | Failed operations | % of total |

### Percentiles Matter

| Percentile | Meaning |
|------------|---------|
| p50 (median) | Typical user experience |
| p95 | Worst 5% of users |
| p99 | Worst 1% of users |
| p99.9 | Tail latency issues |

**Example:** p50=50ms, p99=500ms means most users are fine, but 1% see 10x worse.

---

## 2. Profiling Approaches

### Types of Profilers

| Type | What It Measures | Use Case |
|------|-----------------|----------|
| **CPU profiler** | Time spent in functions | Slow computations |
| **Memory profiler** | Allocations, heap usage | Memory leaks, GC pressure |
| **I/O profiler** | File, network, DB operations | Waiting on external resources |
| **Flame graph** | Visual call stack breakdown | Finding hotspots |

### Sampling vs. Instrumentation

| Approach | Pros | Cons |
|----------|------|------|
| **Sampling** | Low overhead, production-safe | Less precise |
| **Instrumentation** | Precise, detailed | High overhead, dev only |

---

## 3. Profiling Workflow

### Step 1: Establish Baseline

```python
# Measure current state
import time

def benchmark(func, iterations=100):
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)

    return {
        "min": min(times) * 1000,
        "max": max(times) * 1000,
        "avg": (sum(times) / len(times)) * 1000,
        "p95": sorted(times)[int(0.95 * len(times))] * 1000
    }
```

### Step 2: Profile

**Python:**
```python
import cProfile
import pstats

# Profile a function
cProfile.run('my_function()', 'profile_output')

# Analyze results
stats = pstats.Stats('profile_output')
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

**JavaScript (Node.js):**
```javascript
// Start with --inspect flag
// Use Chrome DevTools Performance tab
// Or use clinic.js
npx clinic doctor -- node server.js
```

### Step 3: Identify Bottlenecks

Look for:
- Functions with high cumulative time
- Functions called many times
- Unexpected hot paths
- I/O waits

### Step 4: Optimize & Verify

1. Make targeted change
2. Re-measure
3. Compare to baseline
4. Document improvement

---

## 4. Common Performance Issues

### CPU-Bound Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Algorithm complexity | O(n²) with large n | Better algorithm |
| Unnecessary computation | Repeated calculations | Caching, memoization |
| Tight loops | High CPU, low I/O wait | Batch operations |

### Memory Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Memory leak | Steady growth | Find and fix references |
| Large allocations | Spiky memory | Streaming, pagination |
| GC pressure | Frequent pauses | Object pooling, reduce allocations |

### I/O Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| N+1 queries | Many small DB calls | Batch, eager loading |
| Unindexed queries | Slow DB operations | Add indexes |
| Sequential I/O | Low parallelism | Concurrent requests |
| Large payloads | Network latency | Compression, pagination |

---

## 5. Optimization Techniques

### Caching

| Level | Example | Tradeoff |
|-------|---------|----------|
| Function | `@lru_cache` | Memory vs. computation |
| Application | Redis, Memcached | Staleness, consistency |
| HTTP | CDN, browser cache | Cache invalidation |
| Database | Query cache | Memory, write overhead |

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_calculation(n):
    # Cached after first call with same n
    return compute(n)
```

### Batching

```python
# Bad: N+1 queries
for user_id in user_ids:
    user = db.get_user(user_id)  # N queries

# Good: Batch query
users = db.get_users(user_ids)  # 1 query
```

### Async I/O

```python
import asyncio

# Sequential: 5 seconds
for url in urls:
    await fetch(url)  # Each takes 1 second

# Concurrent: 1 second
await asyncio.gather(*[fetch(url) for url in urls])
```

### Lazy Loading

```python
# Eager: Load everything upfront
def get_user_with_posts(user_id):
    user = db.get_user(user_id)
    user.posts = db.get_posts(user_id)  # Even if not needed
    return user

# Lazy: Load on demand
class User:
    @property
    def posts(self):
        if self._posts is None:
            self._posts = db.get_posts(self.id)
        return self._posts
```

---

## 6. Benchmarking

### Micro-benchmarks

```python
import timeit

# Time a specific operation
result = timeit.timeit(
    'sorted(data)',
    setup='data = list(range(1000))',
    number=10000
)
print(f"Average: {result / 10000 * 1000:.3f}ms")
```

### Load Testing

Tools: k6, locust, wrk, Apache Bench

```javascript
// k6 example
import http from 'k6/http';

export const options = {
    vus: 100,           // Virtual users
    duration: '30s',    // Test duration
};

export default function() {
    http.get('http://localhost:3000/api/users');
}
```

---

## 7. Monitoring in Production

### Key Signals (USE Method)

| Resource | Utilization | Saturation | Errors |
|----------|-------------|------------|--------|
| CPU | % busy | Load average | Machine check errors |
| Memory | % used | Swapping | OOM events |
| Disk | % capacity | Wait queue | Read/write errors |
| Network | Bandwidth % | Dropped packets | Connection errors |

### Application Metrics

- Request latency (histogram)
- Request rate (counter)
- Error rate (counter)
- In-flight requests (gauge)

---

## Quick Reference

### Profiling Checklist

1. [ ] Set performance target
2. [ ] Establish baseline measurement
3. [ ] Profile to find bottleneck
4. [ ] Identify root cause
5. [ ] Apply targeted fix
6. [ ] Verify improvement
7. [ ] Check for regressions
8. [ ] Document findings

### Optimization Order

1. Algorithm/data structure (biggest impact)
2. I/O optimization (batching, caching)
3. Concurrency/parallelism
4. Memory optimization
5. Micro-optimizations (last resort)

### Red Flags

- Optimizing without measuring
- Premature optimization
- Optimizing rarely-executed code
- Sacrificing readability for marginal gains

Measure first. Optimize bottlenecks. Verify improvements. Repeat.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

