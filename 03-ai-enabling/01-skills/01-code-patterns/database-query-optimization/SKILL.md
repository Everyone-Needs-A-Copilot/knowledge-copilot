---
last_updated: 2026-02-25
status: active
name: database-query-optimization
description: Database query optimization - indexes, explain plans, N+1 prevention. Use when optimizing database performance.
triggers:
  files: ["**/*.sql", "**/models/**", "**/migrations/**", "**/queries/**", "**/repository/**"]
  keywords: ["query optimization", "slow query", "index", "explain", "N+1", "database performance", "ORM", "SQLAlchemy", "Prisma"]
allowed-tools: Read, Write, Edit
---

# Database Query Optimization: Deep Expertise Skill

Make your database queries fast and efficient. This skill covers indexing strategies, query analysis, ORM optimization, and patterns for high-performance data access.

## Philosophy: Measure Before Optimizing

Database optimization is not guesswork. Always:

1. **Measure** - Profile actual query performance
2. **Analyze** - Use EXPLAIN to understand query plans
3. **Optimize** - Apply targeted improvements
4. **Verify** - Confirm improvements with measurements

**The cardinal rule:** Premature optimization is the root of all evil, but ignoring obvious N+1 queries is just negligence.

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## 1. Understanding Query Execution

### EXPLAIN: Your Best Friend

Always analyze queries before optimizing:

**PostgreSQL:**
```sql
EXPLAIN ANALYZE
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active'
GROUP BY u.id;
```

**Output interpretation:**
```
HashAggregate  (cost=156.34..158.34 rows=200 width=48) (actual time=12.5..12.8 rows=150 loops=1)
  Group Key: u.id
  ->  Hash Left Join  (cost=45.00..148.34 rows=800 width=44) (actual time=3.2..10.5 rows=800 loops=1)
        Hash Cond: (o.user_id = u.id)
        ->  Seq Scan on users u  (cost=0.00..85.00 rows=200 width=40) (actual time=0.02..2.5 rows=200 loops=1)
              Filter: (status = 'active'::text)
              Rows Removed by Filter: 300
        ->  Hash  (cost=35.00..35.00 rows=800 width=8) (actual time=2.8..2.8 rows=800 loops=1)
              ->  Seq Scan on orders o  (cost=0.00..35.00 rows=800 width=8) (actual time=0.01..1.5 rows=800 loops=1)
Planning Time: 0.5 ms
Execution Time: 13.2 ms
```

**Key metrics:**
- **Seq Scan** = Full table scan (usually bad for large tables)
- **Index Scan** = Using an index (usually good)
- **Hash Join** = Building hash table for join
- **Nested Loop** = For each row in outer, scan inner (watch for N+1)
- **actual time** = Real execution time
- **rows** = Rows processed

### Identifying Slow Queries

**PostgreSQL slow query log:**
```sql
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
SELECT pg_reload_conf();

-- Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

**Python query logging:**
```python
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if total > 0.1:  # Log queries > 100ms
        logger.warning(f"Slow query ({total:.2f}s): {statement[:200]}")
```

---

## 2. Indexing Strategies

### Index Fundamentals

**When to create indexes:**
- Columns in WHERE clauses
- Columns in JOIN conditions
- Columns in ORDER BY
- Columns with high selectivity (many unique values)

**When NOT to index:**
- Small tables (< 1000 rows)
- Columns with low selectivity (e.g., boolean status)
- Columns rarely used in queries
- Tables with heavy INSERT/UPDATE (indexes slow writes)

### Index Types

**B-Tree (default):**
```sql
-- Good for: equality, range queries, sorting
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_created ON orders (created_at);

-- Supports: =, <, >, <=, >=, BETWEEN, IN, LIKE 'prefix%'
SELECT * FROM users WHERE email = 'user@example.com';
SELECT * FROM orders WHERE created_at > '2026-01-01';
```

**Hash Index:**
```sql
-- Good for: equality only (faster than B-tree for =)
CREATE INDEX idx_users_email_hash ON users USING HASH (email);

-- Only supports: =
SELECT * FROM users WHERE email = 'user@example.com';
```

**GIN (Generalized Inverted Index):**
```sql
-- Good for: arrays, JSONB, full-text search
CREATE INDEX idx_products_tags ON products USING GIN (tags);
CREATE INDEX idx_users_metadata ON users USING GIN (metadata jsonb_path_ops);

-- Supports: @>, ?, ?|, ?&, containment queries
SELECT * FROM products WHERE tags @> ARRAY['electronics'];
SELECT * FROM users WHERE metadata @> '{"verified": true}';
```

**GiST (Generalized Search Tree):**
```sql
-- Good for: geometric data, range types, full-text
CREATE INDEX idx_locations_coords ON locations USING GIST (coordinates);

-- Supports: geometric operators, range containment
SELECT * FROM locations WHERE coordinates <-> point(40.7, -74.0) < 10;
```

### Composite Indexes

Order matters! Put most selective columns first, or columns used in equality comparisons.

```sql
-- Good: status (equality) before created_at (range)
CREATE INDEX idx_orders_status_created ON orders (status, created_at);

-- Query uses the index efficiently
SELECT * FROM orders
WHERE status = 'pending'
AND created_at > '2026-01-01';

-- This query CANNOT use the index (missing leading column)
SELECT * FROM orders WHERE created_at > '2026-01-01';
```

**Composite index rules:**
1. Equality columns first
2. Range columns last
3. ORDER BY columns can extend the index

```sql
-- Covers: WHERE status = ? AND created_at > ? ORDER BY created_at
CREATE INDEX idx_orders_status_created ON orders (status, created_at);
```

### Partial Indexes

Index only rows that matter:

```sql
-- Only index active users (much smaller index)
CREATE INDEX idx_active_users_email ON users (email)
WHERE status = 'active';

-- Only index recent orders
CREATE INDEX idx_recent_orders ON orders (created_at)
WHERE created_at > CURRENT_DATE - INTERVAL '30 days';

-- Index for NULL queries
CREATE INDEX idx_unprocessed_orders ON orders (id)
WHERE processed_at IS NULL;
```

### Covering Indexes (Index-Only Scans)

Include all needed columns to avoid table lookups:

```sql
-- Covering index for common query
CREATE INDEX idx_users_email_name ON users (email) INCLUDE (name, status);

-- Query satisfied entirely from index (no table access)
SELECT name, status FROM users WHERE email = 'user@example.com';
```

---

## 3. Query Optimization Patterns

### Avoid SELECT *

```sql
-- Bad: Fetches all columns
SELECT * FROM users WHERE id = 123;

-- Good: Fetch only needed columns
SELECT id, name, email FROM users WHERE id = 123;
```

### Use WHERE Instead of HAVING

```sql
-- Bad: Filters after grouping
SELECT user_id, COUNT(*)
FROM orders
GROUP BY user_id
HAVING user_id IN (SELECT id FROM users WHERE status = 'active');

-- Good: Filters before grouping
SELECT user_id, COUNT(*)
FROM orders
WHERE user_id IN (SELECT id FROM users WHERE status = 'active')
GROUP BY user_id;
```

### Optimize JOINs

```sql
-- Ensure join columns are indexed
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Prefer explicit JOINs over subqueries
-- Bad: Correlated subquery
SELECT *,
  (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count
FROM users u;

-- Good: JOIN with aggregation
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id;
```

### Use EXISTS Instead of COUNT

```sql
-- Bad: Counts all matching rows
SELECT * FROM users
WHERE (SELECT COUNT(*) FROM orders WHERE user_id = users.id) > 0;

-- Good: Stops at first match
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = u.id);
```

### Pagination Optimization

```sql
-- Bad: OFFSET is slow for large offsets
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 10000;

-- Good: Keyset pagination (cursor-based)
SELECT * FROM orders
WHERE created_at < '2026-01-15T10:00:00Z'
ORDER BY created_at DESC
LIMIT 20;

-- With composite key for uniqueness
SELECT * FROM orders
WHERE (created_at, id) < ('2026-01-15T10:00:00Z', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

### Batch Operations

```sql
-- Bad: Individual inserts
INSERT INTO orders (user_id, total) VALUES (1, 100);
INSERT INTO orders (user_id, total) VALUES (2, 200);
INSERT INTO orders (user_id, total) VALUES (3, 300);

-- Good: Batch insert
INSERT INTO orders (user_id, total)
VALUES (1, 100), (2, 200), (3, 300);

-- Bad: Individual updates
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
UPDATE inventory SET quantity = quantity - 2 WHERE product_id = 2;

-- Good: Batch update with CASE
UPDATE inventory SET quantity = quantity - CASE product_id
  WHEN 1 THEN 1
  WHEN 2 THEN 2
END
WHERE product_id IN (1, 2);
```

---

## 4. N+1 Query Problem

### Identifying N+1

The N+1 problem: 1 query to get N records, then N queries to get related data.

**Symptom:** Query count scales with data size.

```python
# BAD: N+1 queries
users = session.query(User).all()  # 1 query
for user in users:
    print(user.orders)  # N queries (one per user!)
```

**Detection:**
```python
# Log query count
query_count = 0

@event.listens_for(Engine, "before_cursor_execute")
def count_queries(*args):
    global query_count
    query_count += 1

# Check in tests
def test_no_n_plus_1():
    global query_count
    query_count = 0

    users = get_users_with_orders()

    # Should be 2 queries max (users + orders), not N+1
    assert query_count <= 2, f"N+1 detected: {query_count} queries"
```

### Solutions: Eager Loading

**SQLAlchemy - selectinload (recommended for collections):**
```python
from sqlalchemy.orm import selectinload

# 2 queries: SELECT users, SELECT orders WHERE user_id IN (...)
users = session.query(User).options(
    selectinload(User.orders)
).all()

for user in users:
    print(user.orders)  # No additional queries!
```

**SQLAlchemy - joinedload (for single relationships):**
```python
from sqlalchemy.orm import joinedload

# 1 query with LEFT JOIN
user = session.query(User).options(
    joinedload(User.profile)
).filter(User.id == user_id).first()
```

**SQLAlchemy - subqueryload:**
```python
from sqlalchemy.orm import subqueryload

# Uses subquery for loading
users = session.query(User).options(
    subqueryload(User.orders)
).all()
```

**When to use which:**

| Pattern | Use Case | Queries |
|---------|----------|---------|
| selectinload | Collections (1-to-many) | 2 |
| joinedload | Single relations (1-to-1, many-to-1) | 1 |
| subqueryload | Complex filters on related | 2 |

### Nested Eager Loading

```python
# Load orders and their items
users = session.query(User).options(
    selectinload(User.orders).selectinload(Order.items)
).all()

# Load multiple relations
users = session.query(User).options(
    selectinload(User.orders),
    selectinload(User.profile),
    selectinload(User.addresses)
).all()
```

### DataLoader Pattern (GraphQL)

For GraphQL or similar batch-loading scenarios:

```python
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        # Single query for all user IDs
        users = await session.execute(
            select(User).where(User.id.in_(user_ids))
        )
        user_map = {user.id: user for user in users.scalars()}
        return [user_map.get(uid) for uid in user_ids]

# Usage
loader = UserLoader()
user1 = await loader.load(1)  # Batched with other loads
user2 = await loader.load(2)
```

---

## 5. ORM Optimization

### Query Building Best Practices

**SQLAlchemy 2.0 style:**
```python
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

# Modern select() syntax
stmt = (
    select(User)
    .where(User.status == 'active')
    .order_by(User.created_at.desc())
    .limit(20)
)
result = await session.execute(stmt)
users = result.scalars().all()

# Aggregation
stmt = (
    select(
        User.status,
        func.count(User.id).label('count')
    )
    .group_by(User.status)
)

# Complex conditions
stmt = select(Order).where(
    and_(
        Order.status.in_(['pending', 'processing']),
        or_(
            Order.priority == 'high',
            Order.total > 1000
        )
    )
)
```

### Bulk Operations

```python
# Bulk insert
users = [User(name=f"User {i}") for i in range(1000)]
session.add_all(users)
await session.commit()

# Bulk update (without loading objects)
await session.execute(
    update(User)
    .where(User.status == 'inactive')
    .where(User.last_login < datetime.now() - timedelta(days=365))
    .values(status='archived')
)

# Bulk delete
await session.execute(
    delete(Order)
    .where(Order.status == 'cancelled')
    .where(Order.created_at < datetime.now() - timedelta(days=30))
)
```

### Raw SQL When Needed

Sometimes raw SQL is clearer or faster:

```python
from sqlalchemy import text

# Complex query with raw SQL
result = await session.execute(text("""
    WITH monthly_totals AS (
        SELECT
            user_id,
            DATE_TRUNC('month', created_at) as month,
            SUM(total) as monthly_total
        FROM orders
        WHERE created_at > :start_date
        GROUP BY user_id, DATE_TRUNC('month', created_at)
    )
    SELECT
        u.id,
        u.name,
        AVG(mt.monthly_total) as avg_monthly_spend
    FROM users u
    JOIN monthly_totals mt ON mt.user_id = u.id
    GROUP BY u.id, u.name
    HAVING AVG(mt.monthly_total) > :min_spend
    ORDER BY avg_monthly_spend DESC
"""), {"start_date": start_date, "min_spend": 100})
```

---

## 6. Connection Pooling

### Pool Configuration

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Connections to maintain
    max_overflow=10,       # Extra connections allowed
    pool_timeout=30,       # Seconds to wait for connection
    pool_recycle=1800,     # Recycle connections after 30 min
    pool_pre_ping=True,    # Verify connections before use
)
```

### Connection Management

```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def get_session() -> AsyncSession:
    """Provide transactional scope around operations."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Usage
async with get_session() as session:
    user = await session.get(User, user_id)
    user.name = "New Name"
    # Commits automatically on exit
```

---

## 7. Caching Strategies

### Query Result Caching

```python
import hashlib
import json
from functools import wraps

def cache_query(ttl: int = 300):
    """Cache query results in Redis."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_data = f"{func.__name__}:{args}:{sorted(kwargs.items())}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()

            # Try cache first
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute query
            result = await func(*args, **kwargs)

            # Cache result
            await redis.setex(cache_key, ttl, json.dumps(result))

            return result
        return wrapper
    return decorator

@cache_query(ttl=60)
async def get_popular_products(category: str, limit: int = 10):
    """Get popular products - cached for 60 seconds."""
    return await session.execute(
        select(Product)
        .where(Product.category == category)
        .order_by(Product.sales_count.desc())
        .limit(limit)
    )
```

### Materialized Views

For expensive aggregations that don't need real-time data:

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW user_stats AS
SELECT
    u.id as user_id,
    u.name,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.total), 0) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;

-- Create index on materialized view
CREATE INDEX idx_user_stats_total ON user_stats (total_spent DESC);

-- Refresh periodically (can be scheduled)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
```

---

## 8. Common Anti-Patterns

### Fetching All When You Need One

```python
# Bad: Fetches all, uses first
users = session.query(User).filter(User.email == email).all()
user = users[0] if users else None

# Good: Fetch one
user = session.query(User).filter(User.email == email).first()
```

### Not Using Limits

```python
# Bad: Fetches potentially millions
users = session.query(User).filter(User.status == 'active').all()

# Good: Always limit
users = session.query(User).filter(User.status == 'active').limit(100).all()
```

### Inefficient Counting

```python
# Bad: Loads all objects just to count
count = len(session.query(User).all())

# Good: Database count
count = session.query(func.count(User.id)).scalar()
```

### Loading Objects for Updates

```python
# Bad: Load, modify, save
user = session.query(User).get(user_id)
user.login_count += 1
session.commit()

# Good: Direct update
session.query(User).filter(User.id == user_id).update(
    {User.login_count: User.login_count + 1}
)
session.commit()
```

### String Concatenation in Queries

```python
# BAD: SQL injection risk!
session.execute(f"SELECT * FROM users WHERE email = '{email}'")

# Good: Parameterized query
session.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)
```

---

## Quick Reference: Optimization Checklist

### Before Optimizing
- [ ] Profile actual query performance
- [ ] Use EXPLAIN ANALYZE to understand plans
- [ ] Identify slowest queries with pg_stat_statements
- [ ] Measure baseline performance

### Indexing
- [ ] Index columns in WHERE clauses
- [ ] Index JOIN columns
- [ ] Use composite indexes correctly (equality first)
- [ ] Consider partial indexes for filtered queries
- [ ] Don't over-index (slows writes)

### Query Design
- [ ] Avoid SELECT * (fetch needed columns)
- [ ] Use LIMIT on all queries
- [ ] Prefer EXISTS over COUNT for existence checks
- [ ] Use keyset pagination instead of OFFSET

### ORM Usage
- [ ] Eager load related data (prevent N+1)
- [ ] Use bulk operations for batch updates
- [ ] Use direct updates instead of load-modify-save
- [ ] Drop to raw SQL when ORM is limiting

### Connection Management
- [ ] Configure connection pool appropriately
- [ ] Use connection pooling (PgBouncer for heavy loads)
- [ ] Set appropriate timeouts
- [ ] Recycle connections periodically

### Caching
- [ ] Cache expensive, infrequently changing queries
- [ ] Use materialized views for heavy aggregations
- [ ] Invalidate cache on relevant data changes

---

Database optimization is an iterative process. Measure, analyze, optimize, verify. Focus on the queries that matter most - those that run frequently or take the longest. Sometimes the best optimization is not running the query at all (caching, denormalization, or rethinking the data model).


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

