---
last_updated: 2026-02-25
status: active
name: concurrency-patterns
description: Design and implement concurrent systems safely. Activate when working with threads, async operations, or parallel processing.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["concurrent", "parallel", "thread", "async", "await", "race condition", "deadlock", "mutex", "lock", "synchronization"]
allowed-tools: Read, Write, Edit
---

# Concurrency Patterns

Design safe, efficient concurrent systems. This skill covers patterns for managing shared state, coordinating tasks, and avoiding common pitfalls.

## Core Concepts

### Concurrency vs. Parallelism

| Concept | Definition | Example |
|---------|------------|---------|
| **Concurrency** | Managing multiple tasks | Single core switching between tasks |
| **Parallelism** | Executing multiple tasks simultaneously | Multiple cores running tasks |

### Key Terms

| Term | Definition |
|------|------------|
| **Race condition** | Outcome depends on timing |
| **Deadlock** | Tasks waiting for each other forever |
| **Starvation** | Task never gets resources |
| **Atomicity** | Operation completes entirely or not at all |

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Common Concurrency Hazards

### Race Conditions

```python
# UNSAFE: Race condition
counter = 0

def increment():
    global counter
    counter += 1  # Read-modify-write is not atomic

# Two threads calling increment() might:
# Thread 1: Read counter (0)
# Thread 2: Read counter (0)
# Thread 1: Write counter (1)
# Thread 2: Write counter (1)
# Expected: 2, Actual: 1
```

### Deadlocks

```python
# DEADLOCK: Each waits for the other
lock_a = Lock()
lock_b = Lock()

# Thread 1:
lock_a.acquire()
lock_b.acquire()  # Waits for Thread 2

# Thread 2:
lock_b.acquire()
lock_a.acquire()  # Waits for Thread 1
# Neither can proceed
```

### Data Races

```python
# DATA RACE: Unsynchronized access to shared data
shared_list = []

def add_item(item):
    shared_list.append(item)  # Not thread-safe

def read_items():
    return list(shared_list)  # Might see partial state
```

---

## 2. Synchronization Primitives

### Locks (Mutexes)

```python
from threading import Lock

lock = Lock()
counter = 0

def safe_increment():
    global counter
    with lock:  # Acquire on enter, release on exit
        counter += 1  # Now atomic
```

### Read-Write Locks

Allow multiple readers OR single writer.

```python
from threading import RLock
from contextlib import contextmanager

class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    @contextmanager
    def read_lock(self):
        with self._read_ready:
            self._readers += 1
        try:
            yield
        finally:
            with self._read_ready:
                self._readers -= 1
                if self._readers == 0:
                    self._read_ready.notify_all()

    @contextmanager
    def write_lock(self):
        with self._read_ready:
            while self._readers > 0:
                self._read_ready.wait()
            yield
```

### Semaphores

Limit concurrent access to a resource.

```python
from threading import Semaphore

# Allow max 5 concurrent connections
connection_pool = Semaphore(5)

def use_connection():
    with connection_pool:
        # At most 5 threads here simultaneously
        do_work()
```

### Condition Variables

Wait for specific conditions.

```python
from threading import Condition

condition = Condition()
queue = []

def producer():
    with condition:
        queue.append(item)
        condition.notify()  # Wake up consumer

def consumer():
    with condition:
        while not queue:
            condition.wait()  # Release lock and wait
        item = queue.pop(0)
```

---

## 3. Async/Await Patterns

### Basic Async Pattern

```python
import asyncio

async def fetch_data(url):
    response = await http_client.get(url)
    return response.json()

async def main():
    # Concurrent execution
    results = await asyncio.gather(
        fetch_data("http://api.example.com/a"),
        fetch_data("http://api.example.com/b"),
        fetch_data("http://api.example.com/c"),
    )
    return results
```

### JavaScript Async

```javascript
async function fetchAll(urls) {
    const promises = urls.map(url => fetch(url));
    const responses = await Promise.all(promises);
    return Promise.all(responses.map(r => r.json()));
}

// With error handling
async function fetchAllSafe(urls) {
    const results = await Promise.allSettled(
        urls.map(url => fetch(url))
    );

    const successful = results
        .filter(r => r.status === 'fulfilled')
        .map(r => r.value);

    return successful;
}
```

### Timeouts and Cancellation

```python
import asyncio

async def with_timeout(coro, timeout_sec):
    try:
        return await asyncio.wait_for(coro, timeout=timeout_sec)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {timeout_sec}s")
```

---

## 4. Message Passing

### Producer-Consumer Queue

```python
import queue
from threading import Thread

task_queue = queue.Queue(maxsize=100)

def producer():
    for item in generate_items():
        task_queue.put(item)  # Blocks if full
    task_queue.put(None)  # Signal completion

def consumer():
    while True:
        item = task_queue.get()  # Blocks if empty
        if item is None:
            break
        process(item)
        task_queue.task_done()
```

### Channel Pattern (Go-style)

```python
import asyncio

async def channel_example():
    channel = asyncio.Queue()

    async def producer():
        for i in range(10):
            await channel.put(i)
        await channel.put(None)

    async def consumer():
        while True:
            item = await channel.get()
            if item is None:
                break
            print(f"Received: {item}")

    await asyncio.gather(producer(), consumer())
```

---

## 5. Thread-Safe Data Structures

### Concurrent Collections

| Need | Thread-Safe Option |
|------|-------------------|
| List | `queue.Queue` |
| Dict | `threading.Lock` + dict, `concurrent.futures` |
| Counter | `threading.Lock` + int |
| Set | `threading.Lock` + set |

### Immutable State

Avoid sharing mutable state.

```python
from dataclasses import dataclass

@dataclass(frozen=True)  # Immutable
class Config:
    host: str
    port: int
    timeout: int

# Safe to share across threads
config = Config(host="localhost", port=8080, timeout=30)
```

### Copy-on-Write

```python
class CopyOnWriteList:
    def __init__(self):
        self._lock = Lock()
        self._data = []

    def append(self, item):
        with self._lock:
            self._data = self._data + [item]  # New list

    def snapshot(self):
        return self._data  # Safe to read without lock
```

---

## 6. Patterns for Avoiding Problems

### Lock Ordering

Prevent deadlocks by always acquiring locks in consistent order.

```python
def transfer(from_account, to_account, amount):
    # Always lock lower ID first
    first, second = sorted([from_account, to_account], key=lambda a: a.id)

    with first.lock:
        with second.lock:
            from_account.balance -= amount
            to_account.balance += amount
```

### Try-Lock Pattern

Avoid deadlock by not waiting forever.

```python
def try_transfer(from_account, to_account, amount, timeout=1.0):
    if from_account.lock.acquire(timeout=timeout):
        try:
            if to_account.lock.acquire(timeout=timeout):
                try:
                    from_account.balance -= amount
                    to_account.balance += amount
                    return True
                finally:
                    to_account.lock.release()
        finally:
            from_account.lock.release()
    return False  # Couldn't acquire locks
```

### Actor Model

Encapsulate state with message passing.

```python
import asyncio

class Actor:
    def __init__(self):
        self._mailbox = asyncio.Queue()
        self._state = {}

    async def send(self, message):
        await self._mailbox.put(message)

    async def run(self):
        while True:
            message = await self._mailbox.get()
            await self._handle(message)

    async def _handle(self, message):
        # Process message and update internal state
        # No external access to _state
        pass
```

---

## Quick Reference

### Choosing Concurrency Model

| Situation | Approach |
|-----------|----------|
| I/O-bound, many connections | Async/await |
| CPU-bound | Multiprocessing (not threads in Python) |
| Shared mutable state | Locks/synchronization |
| Independent tasks | Message passing |
| Event handling | Callbacks/async |

### Deadlock Prevention

1. Lock ordering (always same order)
2. Lock timeout (don't wait forever)
3. Avoid nested locks when possible
4. Use higher-level abstractions

### Checklist

- [ ] Identified all shared mutable state?
- [ ] All shared access synchronized?
- [ ] Lock ordering consistent?
- [ ] Resources released in finally/with?
- [ ] Tested under concurrent load?
- [ ] Considered async vs threads?

Prefer immutable data and message passing. When you must share state, synchronize carefully.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

