---
last_updated: 2026-02-25
status: active
name: memory-management
description: Understand and optimize memory usage in applications. Activate when debugging leaks, reducing footprint, or managing resources.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go", "**/*.rs", "**/*.c", "**/*.cpp"]
  keywords: ["memory", "leak", "heap", "garbage collection", "allocation", "OOM", "out of memory", "memory usage", "gc"]
allowed-tools: Read, Write, Edit
---

# Memory Management

Understand memory allocation, prevent leaks, and optimize usage. This skill covers memory management patterns across garbage-collected and manual-memory languages.

## Core Concepts

### Memory Layout

| Region | Contents | Lifecycle |
|--------|----------|-----------|
| **Stack** | Local variables, function calls | Automatic (function scope) |
| **Heap** | Dynamically allocated objects | Manual or GC managed |
| **Static** | Global variables, constants | Program lifetime |

### Key Terms

| Term | Definition |
|------|------------|
| **Allocation** | Reserving memory for data |
| **Deallocation** | Releasing memory back |
| **Memory leak** | Allocated memory never freed |
| **Garbage collection** | Automatic deallocation of unreachable objects |
| **Reference counting** | Track references to decide when to free |

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Memory Leaks

### Common Leak Patterns

| Pattern | Cause | Solution |
|---------|-------|----------|
| **Forgotten references** | Object stored but never removed | Clear references when done |
| **Event listeners** | Listener keeps object alive | Remove listeners on cleanup |
| **Closures** | Closure captures outer scope | Minimize captured variables |
| **Caches without eviction** | Cache grows unbounded | Add size limits, TTL |
| **Circular references** | A → B → A | Weak references |

### JavaScript Leak Example

```javascript
// LEAK: Event listener keeps reference
class Component {
    constructor() {
        this.data = new Array(10000).fill('x');
        window.addEventListener('resize', this.handleResize);
    }

    handleResize = () => {
        // Uses this.data
    }

    // MISSING: Cleanup method never called
    destroy() {
        window.removeEventListener('resize', this.handleResize);
    }
}
```

### Python Leak Example

```python
# LEAK: Growing cache with no limit
_cache = {}

def get_data(key):
    if key not in _cache:
        _cache[key] = expensive_fetch(key)
    return _cache[key]

# FIX: Use bounded cache
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_data(key):
    return expensive_fetch(key)
```

---

## 2. Detecting Memory Issues

### Symptoms

| Symptom | Likely Cause |
|---------|--------------|
| Steady memory growth | Memory leak |
| Memory spikes | Large allocations, batch processing |
| OOM crashes | Leak or undersized limit |
| Frequent GC pauses | Too many allocations |
| Slow performance over time | Memory fragmentation |

### Profiling Tools

| Language | Tool |
|----------|------|
| Python | `tracemalloc`, `memory_profiler`, `objgraph` |
| JavaScript | Chrome DevTools Memory tab, `--inspect` |
| Java | VisualVM, JProfiler, `jmap` |
| Go | `pprof`, `runtime.MemStats` |

### Python Memory Profiling

```python
import tracemalloc

tracemalloc.start()

# Run code to profile
result = process_data()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)
```

### JavaScript Heap Snapshot

```javascript
// In Chrome DevTools:
// 1. Open Memory tab
// 2. Take heap snapshot
// 3. Compare snapshots to find leaks
// 4. Look for "Detached" DOM elements

// Or programmatically:
const v8 = require('v8');
const fs = require('fs');

const snapshot = v8.writeHeapSnapshot();
console.log(`Heap snapshot written to: ${snapshot}`);
```

---

## 3. Garbage Collection

### GC Strategies

| Strategy | How It Works | Tradeoff |
|----------|--------------|----------|
| **Reference counting** | Free when count = 0 | Can't handle cycles |
| **Mark and sweep** | Mark reachable, sweep rest | Stop-the-world pauses |
| **Generational** | Frequent young gen, rare old gen | Tuning complexity |
| **Concurrent** | GC runs with application | CPU overhead |

### GC-Friendly Code

```python
# BAD: Many small allocations
result = ""
for item in items:
    result += str(item)  # Creates new string each time

# GOOD: Batch allocation
result = "".join(str(item) for item in items)
```

```javascript
// BAD: Creating objects in hot loop
for (let i = 0; i < 1000000; i++) {
    const point = { x: i, y: i * 2 };  // Millions of allocations
    process(point);
}

// GOOD: Reuse objects
const point = { x: 0, y: 0 };
for (let i = 0; i < 1000000; i++) {
    point.x = i;
    point.y = i * 2;
    process(point);
}
```

### Monitoring GC

```python
# Python
import gc

gc.set_debug(gc.DEBUG_STATS)
gc.collect()  # Force collection and print stats
```

```javascript
// Node.js
node --trace-gc app.js
// Output: [12345:0x...] 42 ms: Scavenge 10.2 (20.0) -> 8.1 (20.0) MB
```

---

## 4. Memory Optimization Patterns

### Object Pooling

Reuse objects instead of allocating/deallocating.

```python
class ObjectPool:
    def __init__(self, factory, initial_size=10):
        self._factory = factory
        self._pool = [factory() for _ in range(initial_size)]

    def acquire(self):
        if self._pool:
            return self._pool.pop()
        return self._factory()

    def release(self, obj):
        self._pool.append(obj)

# Usage
pool = ObjectPool(lambda: {"data": None})
obj = pool.acquire()
obj["data"] = "work"
# ... use obj ...
obj["data"] = None  # Reset
pool.release(obj)
```

### Lazy Loading

Load data only when needed.

```python
class LazyLoader:
    def __init__(self, loader_func):
        self._loader = loader_func
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self._loader()
        return self._data

    def unload(self):
        self._data = None
```

### Streaming Large Data

Process data in chunks instead of loading all at once.

```python
# BAD: Load entire file into memory
data = open('large_file.csv').read()
process(data)

# GOOD: Stream line by line
with open('large_file.csv') as f:
    for line in f:
        process(line)
```

### Weak References

Allow objects to be collected even when referenced.

```python
import weakref

class Cache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get(self, key, loader):
        value = self._cache.get(key)
        if value is None:
            value = loader(key)
            self._cache[key] = value
        return value
```

---

## 5. Language-Specific Patterns

### Python

| Pattern | Use |
|---------|-----|
| `__slots__` | Reduce per-instance memory |
| Generators | Lazy iteration |
| `del` | Explicit reference removal |
| `gc.collect()` | Force garbage collection |

```python
class Point:
    __slots__ = ['x', 'y']  # No __dict__, saves memory

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### JavaScript

| Pattern | Use |
|---------|-----|
| `WeakMap` / `WeakSet` | Avoid retaining keys |
| `null` assignment | Clear references |
| Remove event listeners | Prevent DOM leaks |

```javascript
// WeakMap doesn't prevent GC of keys
const metadata = new WeakMap();

function attach(element, data) {
    metadata.set(element, data);
}
// When element is removed from DOM, metadata entry can be GC'd
```

---

## Quick Reference

### Memory Leak Checklist

- [ ] Event listeners removed on cleanup?
- [ ] Subscriptions unsubscribed?
- [ ] Timers/intervals cleared?
- [ ] Caches bounded with eviction?
- [ ] Closures not capturing unnecessarily?
- [ ] No circular references (or using weak refs)?

### Optimization Checklist

- [ ] Using streaming for large data?
- [ ] Object pooling for hot paths?
- [ ] Lazy loading for expensive resources?
- [ ] Appropriate data structures?
- [ ] Monitoring memory in production?

### Red Flags

| Flag | Investigate |
|------|-------------|
| Memory grows over time | Leak |
| OOM after specific operation | Large allocation |
| Frequent long GC pauses | Too many allocations |
| Memory not released after work | Retained references |

Manage memory consciously. Profile to find issues. Fix leaks at the source.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

