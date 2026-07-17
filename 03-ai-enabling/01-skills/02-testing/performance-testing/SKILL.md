---
last_updated: 2026-02-25
status: active
name: performance-testing
description: Performance testing fundamentals - load testing, stress testing, benchmarking, profiling. Use when validating system performance.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*", "**/benchmark/**", "**/perf/**", "**/load/**"]
  keywords: ["performance test", "load test", "stress test", "benchmark", "latency", "throughput", "response time", "concurrent users"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides performance testing to ensure systems handle expected load with acceptable response times. Test before users experience slowness, not after.

The user provides testing requirements: an API to load test, a system to benchmark, or performance issues to investigate. They may include context about expected load, SLAs, or current performance problems.

## Performance Testing Types

### Overview

| Type | Question Answered | Typical Duration |
|------|-------------------|------------------|
| Load | Can it handle expected load? | Hours |
| Stress | Where does it break? | Hours |
| Spike | How does it handle sudden traffic? | Minutes |
| Soak/Endurance | Is it stable over time? | Days |
| Benchmark | How fast is this operation? | Minutes |

### Load Testing

Verify system handles expected concurrent users:

```
Expected: 1000 concurrent users
Test: Ramp to 1000 users over 10 minutes, hold for 30 minutes

Metrics to track:
- Response time (avg, p95, p99)
- Throughput (requests/second)
- Error rate
- Resource utilization
```

### Stress Testing

Find the breaking point:

```
Start: 100 concurrent users
Ramp: Add 100 users every 5 minutes
Monitor: When do errors spike? When does response time degrade?
Stop: When error rate > 5% or response time > 5s

Result: System breaks at ~800 users (CPU saturates)
```

### Spike Testing

Test sudden traffic bursts:

```
Baseline: 100 users for 5 minutes
Spike: Jump to 1000 users for 2 minutes
Recovery: Return to 100 users

Monitor:
- How fast does it recover?
- Are there errors during spike?
- Does autoscaling kick in?
```

### Soak Testing

Test stability over extended periods:

```
Duration: 24-72 hours
Load: 70% of peak capacity

Watch for:
- Memory leaks
- Connection pool exhaustion
- Log file growth
- Database performance degradation
```


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Key Metrics

### Response Time Metrics

| Metric | Description | Typical Target |
|--------|-------------|----------------|
| Average | Mean response time | < 200ms |
| Median (p50) | 50% of requests faster | < 150ms |
| p90 | 90% of requests faster | < 500ms |
| p95 | 95% of requests faster | < 1s |
| p99 | 99% of requests faster | < 2s |
| Max | Slowest request | < 5s |

**Why percentiles matter:**
```
Average: 200ms
p99: 5000ms

Means 1 in 100 users waits 5+ seconds!
At 1M requests/day = 10,000 frustrated users
```

### Throughput Metrics

| Metric | Description | Example |
|--------|-------------|---------|
| Requests/second | API throughput | 1000 rps |
| Transactions/second | Business transactions | 50 tps |
| Concurrent users | Simultaneous users | 500 users |
| Bandwidth | Data transferred | 100 Mbps |

### Error Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Error rate | < 0.1% | > 1% | > 5% |
| Timeout rate | < 0.01% | > 0.1% | > 1% |
| 5xx errors | 0 | Any | Sustained |

### Resource Metrics

| Resource | Healthy | Warning | Critical |
|----------|---------|---------|----------|
| CPU | < 70% | > 80% | > 95% |
| Memory | < 70% | > 85% | > 95% |
| Disk I/O | < 70% | > 80% | > 90% |
| Network | < 50% | > 70% | > 85% |
| DB connections | < 70% | > 80% | > 90% |

## Load Testing Tools

### k6 (JavaScript)

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Hold
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

Run: `k6 run load-test.js`

### Locust (Python)

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_products(self):
        self.client.get("/api/products")

    @task(2)
    def view_product_detail(self):
        self.client.get("/api/products/1")

    @task(1)
    def create_order(self):
        self.client.post("/api/orders", json={
            "product_id": 1,
            "quantity": 1
        })

    def on_start(self):
        # Login at start of session
        self.client.post("/api/login", json={
            "username": "testuser",
            "password": "testpass"
        })
```

Run: `locust -f locustfile.py --host=https://api.example.com`

### Apache JMeter (GUI/XML)

```xml
<!-- test-plan.jmx -->
<TestPlan>
  <ThreadGroup>
    <numThreads>100</numThreads>
    <rampUp>60</rampUp>
    <duration>300</duration>

    <HTTPSampler>
      <domain>api.example.com</domain>
      <path>/api/users</path>
      <method>GET</method>
    </HTTPSampler>

    <ResponseAssertion>
      <responseCode>200</responseCode>
    </ResponseAssertion>
  </ThreadGroup>
</TestPlan>
```

### wrk (Command Line)

```bash
# Simple load test
wrk -t4 -c100 -d30s http://api.example.com/users

# With Lua script for POST requests
wrk -t4 -c100 -d30s -s post.lua http://api.example.com/orders
```

```lua
-- post.lua
wrk.method = "POST"
wrk.body   = '{"product_id": 1, "quantity": 1}'
wrk.headers["Content-Type"] = "application/json"
```

## Benchmarking Code

### Python Benchmarking

```python
import timeit
import statistics

def benchmark_function(func, iterations=1000):
    times = []
    for _ in range(iterations):
        start = timeit.default_timer()
        func()
        end = timeit.default_timer()
        times.append((end - start) * 1000)  # ms

    return {
        "min": min(times),
        "max": max(times),
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times),
    }

# Usage
result = benchmark_function(lambda: my_function(data))
print(f"Mean: {result['mean']:.2f}ms, p50: {result['median']:.2f}ms")
```

### Python pytest-benchmark

```python
# test_performance.py
import pytest

def test_sorting_performance(benchmark):
    data = list(range(10000, 0, -1))

    result = benchmark(sorted, data)

    assert result == list(range(1, 10001))

def test_database_query_performance(benchmark, db_session):
    def query():
        return db_session.query(User).filter(User.active == True).all()

    users = benchmark(query)

    assert len(users) > 0
```

Run: `pytest test_performance.py --benchmark-only`

### JavaScript Benchmarking

```javascript
// benchmark.js
const Benchmark = require('benchmark');

const suite = new Benchmark.Suite();

suite
  .add('Array.forEach', function() {
    const arr = [1, 2, 3, 4, 5];
    arr.forEach(x => x * 2);
  })
  .add('Array.map', function() {
    const arr = [1, 2, 3, 4, 5];
    arr.map(x => x * 2);
  })
  .add('for loop', function() {
    const arr = [1, 2, 3, 4, 5];
    for (let i = 0; i < arr.length; i++) {
      arr[i] * 2;
    }
  })
  .on('complete', function() {
    console.log('Fastest is ' + this.filter('fastest').map('name'));
  })
  .run();
```

## Test Scenarios

### API Load Test Scenario

```javascript
// k6 - API load test
import http from 'k6/http';
import { check, group } from 'k6';

export const options = {
  scenarios: {
    browse: {
      executor: 'constant-vus',
      vus: 50,
      duration: '10m',
      exec: 'browse',
    },
    purchase: {
      executor: 'constant-vus',
      vus: 10,
      duration: '10m',
      exec: 'purchase',
    },
  },
};

export function browse() {
  group('Browse products', function () {
    const products = http.get(`${BASE_URL}/api/products`);
    check(products, { 'products loaded': (r) => r.status === 200 });

    const detail = http.get(`${BASE_URL}/api/products/1`);
    check(detail, { 'detail loaded': (r) => r.status === 200 });
  });
}

export function purchase() {
  group('Purchase flow', function () {
    // Login
    const login = http.post(`${BASE_URL}/api/login`, {
      username: 'user',
      password: 'pass',
    });

    // Add to cart
    const cart = http.post(`${BASE_URL}/api/cart`, {
      product_id: 1,
      quantity: 1,
    });

    // Checkout
    const order = http.post(`${BASE_URL}/api/checkout`, {
      payment_method: 'card',
    });

    check(order, { 'order created': (r) => r.status === 201 });
  });
}
```

### Database Performance Test

```python
import time
import statistics

class DatabasePerformanceTest:
    def __init__(self, session):
        self.session = session

    def test_bulk_insert(self, count=10000):
        users = [User(name=f"User {i}") for i in range(count)]

        start = time.time()
        self.session.bulk_save_objects(users)
        self.session.commit()
        duration = time.time() - start

        return {
            "operation": "bulk_insert",
            "count": count,
            "duration_seconds": duration,
            "records_per_second": count / duration
        }

    def test_query_with_index(self, iterations=100):
        times = []
        for _ in range(iterations):
            start = time.time()
            self.session.query(User).filter(User.id == 1000).first()
            times.append(time.time() - start)

        return {
            "operation": "indexed_query",
            "iterations": iterations,
            "mean_ms": statistics.mean(times) * 1000,
            "p99_ms": sorted(times)[int(iterations * 0.99)] * 1000
        }

    def test_complex_query(self, iterations=100):
        times = []
        for _ in range(iterations):
            start = time.time()
            self.session.query(User)\
                .join(Order)\
                .filter(Order.total > 100)\
                .group_by(User.id)\
                .having(func.count(Order.id) > 5)\
                .all()
            times.append(time.time() - start)

        return {
            "operation": "complex_join_query",
            "mean_ms": statistics.mean(times) * 1000,
            "p99_ms": sorted(times)[int(iterations * 0.99)] * 1000
        }
```

## Performance Test Reporting

### Test Report Template

```markdown
# Performance Test Report

**Test Date:** 2024-01-15
**Environment:** Staging (4 CPU, 16GB RAM)
**Duration:** 2 hours

## Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p95 Response Time | < 500ms | 320ms | ✅ |
| Error Rate | < 1% | 0.02% | ✅ |
| Throughput | > 500 rps | 750 rps | ✅ |
| Max Concurrent Users | 500 | 500 | ✅ |

## Test Scenarios

### Scenario 1: Normal Load (300 users)
- Duration: 30 minutes
- Response Time: avg 180ms, p95 280ms
- Throughput: 450 rps
- Error Rate: 0%
- CPU: 45%, Memory: 60%

### Scenario 2: Peak Load (500 users)
- Duration: 30 minutes
- Response Time: avg 320ms, p95 480ms
- Throughput: 750 rps
- Error Rate: 0.02%
- CPU: 78%, Memory: 72%

### Scenario 3: Stress Test (800 users)
- Duration: 15 minutes
- Response Time: avg 1200ms, p95 3500ms
- Error Rate: 8%
- Breaking point reached at 750 users

## Bottlenecks Identified

1. **Database connection pool** - Exhausted at 700 users
   - Recommendation: Increase pool size from 20 to 50

2. **API endpoint /api/search** - Slow under load
   - p95 jumps from 200ms to 2000ms at 500 users
   - Recommendation: Add caching layer

## Recommendations

1. Increase DB connection pool before production
2. Add Redis cache for search endpoint
3. Consider horizontal scaling above 500 users
```

## CI/CD Integration

### Performance Test Pipeline

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  schedule:
    - cron: '0 2 * * *'  # Nightly at 2 AM
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install k6
        run: |
          sudo apt-get update
          sudo apt-get install -y k6

      - name: Run Load Test
        run: k6 run tests/load/api-test.js --out json=results.json

      - name: Check Thresholds
        run: |
          # Fail if p95 > 500ms
          p95=$(jq '.metrics.http_req_duration.values["p(95)"]' results.json)
          if (( $(echo "$p95 > 500" | bc -l) )); then
            echo "Performance regression: p95 = ${p95}ms"
            exit 1
          fi

      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: performance-results
          path: results.json
```

## Quick Reference

### Performance Testing Checklist

Before testing:
- [ ] Define performance requirements (SLAs)
- [ ] Identify critical scenarios
- [ ] Prepare test environment (production-like)
- [ ] Set up monitoring

During testing:
- [ ] Monitor response times and errors
- [ ] Watch resource utilization
- [ ] Record all metrics

After testing:
- [ ] Analyze results against requirements
- [ ] Identify bottlenecks
- [ ] Document findings
- [ ] Create action items

### Common Performance Issues

| Symptom | Possible Cause | Investigation |
|---------|----------------|---------------|
| High CPU | Inefficient code | Profile code |
| High memory | Memory leak | Heap dump |
| Slow queries | Missing indexes | Explain plans |
| Connection errors | Pool exhaustion | Connection metrics |
| Timeouts | External service | Trace requests |

### Performance Budget Example

| Metric | Budget | Notes |
|--------|--------|-------|
| Time to First Byte | < 200ms | Server response |
| API Response (p95) | < 500ms | Most endpoints |
| Search Response (p95) | < 1s | Complex queries OK |
| Error Rate | < 0.1% | At peak load |
| Concurrent Users | 1000 | Peak capacity |

## Summary

Performance testing ensures your system handles real-world load:

1. **Define requirements** - Response time, throughput, error rate
2. **Choose test types** - Load, stress, spike, soak
3. **Use right tools** - k6, Locust, JMeter
4. **Monitor everything** - Response time, errors, resources
5. **Test realistic scenarios** - Mix of user behaviors
6. **Benchmark continuously** - Catch regressions early
7. **Report clearly** - Metrics, bottlenecks, recommendations
8. **Integrate with CI** - Automated performance gates


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

