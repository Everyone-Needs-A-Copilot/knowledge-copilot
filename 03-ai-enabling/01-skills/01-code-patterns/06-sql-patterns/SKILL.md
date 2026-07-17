---
last_updated: 2026-02-25
status: active
name: sql-patterns
description: SQL optimization - query performance, indexing, migrations, transactions. Use when working with databases.
triggers:
  files: ["**/*.sql", "**/migrations/**", "**/alembic/**", "**/models.py"]
  keywords: ["SQL", "query", "index", "join", "transaction", "migration", "database", "PostgreSQL", "normalize"]
allowed-tools: Read, Write, Edit
---

# SQL Patterns - Deep Expertise Skill

Advanced SQL patterns, optimization techniques, and database design principles for production systems. Focus on PostgreSQL but applicable to most RDBMS.

## Table of Contents

1. [Query Optimization Fundamentals](#query-optimization-fundamentals)
2. [Indexing Strategies](#indexing-strategies)
3. [EXPLAIN ANALYZE](#explain-analyze)
4. [Join Optimization](#join-optimization)
5. [N+1 Query Prevention](#n1-query-prevention)
6. [Transactions and Isolation](#transactions-and-isolation)
7. [Migrations Best Practices](#migrations-best-practices)
8. [Schema Design](#schema-design)
9. [PostgreSQL-Specific Features](#postgresql-specific-features)
10. [Connection Pooling](#connection-pooling)
11. [Anti-Patterns](#anti-patterns)

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## Query Optimization Fundamentals

### Performance Analysis Workflow

```sql
-- 1. Enable timing
\timing on

-- 2. Run EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM large_table WHERE status = 'active';

-- 3. Check query statistics
SELECT schemaname, tablename,
       seq_scan, seq_tup_read,
       idx_scan, idx_tup_fetch
FROM pg_stat_user_tables
WHERE tablename = 'large_table';

-- 4. Identify slow queries
SELECT query, calls, total_time, mean_time, max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;
```

### Query Rewriting for Performance

**BAD: Fetching unnecessary columns**
```sql
-- Fetches all columns, slow on wide tables
SELECT * FROM users
WHERE created_at > NOW() - INTERVAL '30 days';
```

**GOOD: Select only needed columns**
```sql
-- Faster, uses covering index potential
SELECT id, email, created_at FROM users
WHERE created_at > NOW() - INTERVAL '30 days';
```

**BAD: Function on indexed column**
```sql
-- Cannot use index on created_at
SELECT * FROM orders
WHERE DATE(created_at) = '2024-01-01';
```

**GOOD: Range query to use index**
```sql
-- Uses index on created_at
SELECT * FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-01-02';
```

**BAD: OR conditions on different columns**
```sql
-- Requires multiple index scans or full table scan
SELECT * FROM products
WHERE category = 'electronics' OR status = 'featured';
```

**GOOD: UNION ALL for OR conditions**
```sql
-- Each query uses its own index
SELECT * FROM products WHERE category = 'electronics'
UNION ALL
SELECT * FROM products WHERE status = 'featured' AND category != 'electronics';
```

### Subquery vs JOIN Performance

**BAD: Correlated subquery (runs for each row)**
```sql
SELECT u.id, u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;
```

**GOOD: JOIN with aggregation**
```sql
SELECT u.id, u.name, COALESCE(o.order_count, 0) as order_count
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;
```

### LIMIT with Ordering

**BAD: Ordering without index**
```sql
-- Requires full table sort
SELECT * FROM logs
ORDER BY created_at DESC
LIMIT 100;
```

**GOOD: Index on ordering column**
```sql
-- Create index first
CREATE INDEX idx_logs_created_at_desc ON logs (created_at DESC);

-- Now query is fast
SELECT * FROM logs
ORDER BY created_at DESC
LIMIT 100;
```

---

## Indexing Strategies

### B-Tree Indexes (Default)

**When to use**: Equality, range queries, sorting

```sql
-- Single column
CREATE INDEX idx_users_email ON users (email);

-- Multi-column (order matters!)
CREATE INDEX idx_orders_user_status ON orders (user_id, status);
-- Good for: WHERE user_id = X AND status = Y
-- Good for: WHERE user_id = X
-- BAD for:  WHERE status = Y (user_id not in WHERE)

-- Include columns for covering index
CREATE INDEX idx_users_email_covering
ON users (email) INCLUDE (name, created_at);
-- Returns name, created_at without table lookup
```

### Column Order in Composite Indexes

**Rule**: Most selective column first, OR most common query pattern first

```sql
-- If you query by user_id (high cardinality) more than status
CREATE INDEX idx_orders_user_status ON orders (user_id, status);

-- If you query by status alone AND user_id+status together
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_orders_user_status ON orders (user_id, status);
```

### Partial Indexes

**When to use**: Query filters on specific value frequently

```sql
-- Only index active users (reduces index size)
CREATE INDEX idx_active_users
ON users (email)
WHERE status = 'active';

-- Query must match WHERE clause
SELECT * FROM users
WHERE status = 'active' AND email = 'user@example.com';

-- Real-world: Index only recent data
CREATE INDEX idx_recent_orders
ON orders (user_id, created_at)
WHERE created_at > NOW() - INTERVAL '90 days';
```

### Expression Indexes

**When to use**: Query uses function on column

```sql
-- Case-insensitive email lookup
CREATE INDEX idx_users_email_lower
ON users (LOWER(email));

-- Query
SELECT * FROM users WHERE LOWER(email) = LOWER('User@Example.com');

-- JSON field indexing
CREATE INDEX idx_metadata_type
ON events ((metadata->>'type'));

-- Query
SELECT * FROM events WHERE metadata->>'type' = 'click';
```

### GIN Indexes (Generalized Inverted Index)

**When to use**: Full-text search, JSONB, arrays

```sql
-- Full-text search
CREATE INDEX idx_articles_search
ON articles USING GIN (to_tsvector('english', title || ' ' || body));

-- Query
SELECT * FROM articles
WHERE to_tsvector('english', title || ' ' || body) @@ to_tsquery('postgres & performance');

-- JSONB queries
CREATE INDEX idx_users_metadata
ON users USING GIN (metadata);

-- Supports various JSONB operators
SELECT * FROM users WHERE metadata @> '{"role": "admin"}';
SELECT * FROM users WHERE metadata ? 'premium_until';

-- JSONB specific path
CREATE INDEX idx_users_metadata_role
ON users USING GIN ((metadata -> 'role'));

-- Array contains
CREATE INDEX idx_posts_tags
ON posts USING GIN (tags);

SELECT * FROM posts WHERE tags @> ARRAY['postgresql', 'performance'];
```

### GiST Indexes (Generalized Search Tree)

**When to use**: Geometric data, range types, full-text (alternative)

```sql
-- Range queries (reservation conflicts)
CREATE INDEX idx_bookings_time_range
ON bookings USING GIST (time_range);

-- Find overlapping bookings
SELECT * FROM bookings
WHERE time_range && tsrange('2024-01-01 10:00', '2024-01-01 12:00');

-- Geometric data
CREATE INDEX idx_locations_point
ON locations USING GIST (coordinates);

-- Find nearby points
SELECT * FROM locations
WHERE ST_DWithin(coordinates, ST_MakePoint(-73.9857, 40.7484), 1000);
```

### BRIN Indexes (Block Range Index)

**When to use**: Very large tables with natural ordering (time-series)

```sql
-- Extremely small index for time-series data
CREATE INDEX idx_logs_created_at_brin
ON logs USING BRIN (created_at);

-- Works well for range queries
SELECT * FROM logs
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-02-01';

-- Size comparison
-- B-tree on 100M rows: ~2.2 GB
-- BRIN on 100M rows:   ~100 KB
```

### Index Maintenance

```sql
-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Remove unused indexes
DROP INDEX idx_never_used;

-- Rebuild bloated index
REINDEX INDEX idx_bloated;

-- Rebuild all indexes on table
REINDEX TABLE users;

-- Check index size
SELECT indexname, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## EXPLAIN ANALYZE

### Understanding EXPLAIN Output

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 10;
```

**Key metrics to analyze:**

1. **Execution Time**: `Planning Time` + `Execution Time`
2. **Node Types**: Seq Scan vs Index Scan vs Bitmap Scan
3. **Rows**: `rows=X` (estimate) vs `actual rows=Y`
4. **Loops**: Operations repeated multiple times
5. **Buffers**: `shared hit` (cache) vs `read` (disk)

### Node Types

**Sequential Scan (Seq Scan)**
```
Seq Scan on users  (cost=0.00..1234.56 rows=100 width=32)
```
- Reads entire table
- Good for: Small tables, selecting >15% of rows
- Bad for: Large tables with selective queries
- **Fix**: Add appropriate index

**Index Scan**
```
Index Scan using idx_users_email on users  (cost=0.29..8.31 rows=1 width=32)
  Index Cond: (email = 'user@example.com')
```
- Follows index to find rows
- Good for: Selective queries, sorted output
- Cost: Random I/O for each row
- **When bad**: Fetching many rows (use Bitmap or Seq Scan)

**Bitmap Index Scan + Bitmap Heap Scan**
```
Bitmap Heap Scan on orders  (cost=12.34..567.89 rows=500 width=32)
  Recheck Cond: (status = 'pending')
  -> Bitmap Index Scan on idx_orders_status  (cost=0.00..12.21 rows=500)
        Index Cond: (status = 'pending')
```
- Builds bitmap of matching rows, then fetches in disk order
- Good for: Moderate selectivity (5-15% of table)
- Better than Index Scan for multiple rows

**Hash Join**
```
Hash Join  (cost=123.45..6789.01 rows=1000 width=64)
  Hash Cond: (o.user_id = u.id)
  -> Seq Scan on orders o
  -> Hash (cost=100.00..100.00 rows=500 width=32)
        -> Seq Scan on users u
```
- Builds hash table of one side, probes with other
- Good for: Medium-sized tables, equality joins
- Memory intensive (watch `work_mem`)

**Nested Loop**
```
Nested Loop  (cost=0.29..234.56 rows=10 width=64)
  -> Index Scan using idx_users_id on users u
  -> Index Scan using idx_orders_user_id on orders o
        Index Cond: (user_id = u.id)
```
- For each row in outer table, scan inner table
- Good for: Small outer table, indexed inner table
- Bad for: Large outer table (becomes O(n²))

**Merge Join**
```
Merge Join  (cost=123.45..678.90 rows=1000 width=64)
  Merge Cond: (u.id = o.user_id)
  -> Index Scan using users_pkey on users u
  -> Index Scan using idx_orders_user_id on orders o
```
- Both sides sorted, then merged
- Good for: Pre-sorted data, large tables
- Requires sort or index on join key

### Analyzing Problem Queries

**Problem: Inaccurate row estimates**
```
Seq Scan on orders  (cost=0.00..123.45 rows=10 width=32) (actual rows=10000)
```
**Fix**: Update statistics
```sql
ANALYZE orders;
-- Or for specific columns
ANALYZE orders (status, created_at);

-- Increase statistics target for better estimates
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;
ANALYZE orders;
```

**Problem: Nested loop with large outer table**
```
Nested Loop  (cost=0.29..999999.99 rows=100000 width=64)
```
**Fix**: Add index on inner table join key, or force hash join
```sql
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Or increase work_mem to enable hash join
SET work_mem = '256MB';
```

**Problem: High buffer reads**
```
Buffers: shared hit=1000 read=50000
```
**Fix**: Add index, increase shared_buffers, or optimize query

---

## Join Optimization

### Join Strategy Selection

**PostgreSQL chooses based on**:
1. Table size
2. Indexes available
3. Row estimates
4. `work_mem` setting
5. `random_page_cost` vs `seq_page_cost`

### Optimizing Nested Loop Joins

**Pattern: Small outer, indexed inner**
```sql
-- Good: 10 users, orders indexed on user_id
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'vip';  -- Reduces outer table

-- Ensure index exists
CREATE INDEX idx_orders_user_id ON orders (user_id);
```

### Optimizing Hash Joins

**Pattern: Medium tables, equality join**
```sql
-- Increase work_mem to avoid disk spills
SET work_mem = '256MB';

SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id;

-- Check if hash spilled to disk
EXPLAIN (ANALYZE, BUFFERS)
-- Look for "Batches: X" where X > 1 means disk spill
```

### Optimizing Merge Joins

**Pattern: Large sorted tables**
```sql
-- Both sides indexed on join key
CREATE INDEX idx_users_id ON users (id);
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- PostgreSQL uses merge join automatically
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id;
```

### Join Order Matters

**BAD: Joins in wrong order**
```sql
-- Joins large table first, then filters
SELECT p.name, o.total, u.email
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
JOIN users u ON o.user_id = u.id
WHERE u.status = 'vip' AND o.created_at > NOW() - INTERVAL '7 days';
```

**GOOD: Filter early, join small to large**
```sql
-- Filter first, then join
WITH recent_vip_orders AS (
    SELECT o.id, o.total, u.email
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE u.status = 'vip'
      AND o.created_at > NOW() - INTERVAL '7 days'
)
SELECT p.name, rvo.total, rvo.email
FROM recent_vip_orders rvo
JOIN order_items oi ON rvo.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### LEFT JOIN vs INNER JOIN

```sql
-- If you filter on right table, LEFT JOIN becomes INNER JOIN
-- BAD: Misleading LEFT JOIN
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';  -- Filters out users without orders

-- GOOD: Use INNER JOIN explicitly
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';

-- GOOD: Keep LEFT JOIN, move filter to ON clause
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'completed';
```

---

## N+1 Query Prevention

### The Problem

**BAD: N+1 queries in application code**
```python
# Fetches users (1 query)
users = db.query(User).all()

# Fetches orders for each user (N queries)
for user in users:
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    print(f"{user.name}: {len(orders)} orders")
```

### Solution 1: JOIN

```python
# Single query with join
results = db.query(User, func.count(Order.id))\
    .join(Order, isouter=True)\
    .group_by(User.id)\
    .all()
```

### Solution 2: Eager Loading (SQLAlchemy)

```python
from sqlalchemy.orm import joinedload, selectinload

# joinedload: Uses LEFT JOIN (single query)
users = db.query(User).options(joinedload(User.orders)).all()

# selectinload: Uses IN clause (2 queries total)
users = db.query(User).options(selectinload(User.orders)).all()
# Generates:
# SELECT * FROM users;
# SELECT * FROM orders WHERE user_id IN (1,2,3,...);
```

### Solution 3: Subquery with JSON aggregation

```sql
-- Returns users with orders as JSON array
SELECT
    u.id,
    u.name,
    COALESCE(
        json_agg(
            json_build_object(
                'id', o.id,
                'total', o.total,
                'created_at', o.created_at
            )
        ) FILTER (WHERE o.id IS NOT NULL),
        '[]'
    ) as orders
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

### Solution 4: Lateral Join for Complex Cases

```sql
-- Get each user with their 3 most recent orders
SELECT
    u.id,
    u.name,
    recent_orders.orders
FROM users u
LEFT JOIN LATERAL (
    SELECT json_agg(
        json_build_object('id', o.id, 'total', o.total)
        ORDER BY o.created_at DESC
    ) as orders
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY o.created_at DESC
    LIMIT 3
) recent_orders ON true;
```

### Detecting N+1 in SQLAlchemy

```python
# Enable query logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Or use query counter
from sqlalchemy import event
from sqlalchemy.engine import Engine

query_count = 0

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    global query_count
    query_count += 1
    print(f"Query #{query_count}: {statement[:100]}")
```

---

## Transactions and Isolation

### Transaction Basics

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Check intermediate state
SELECT * FROM accounts WHERE id IN (1, 2);

COMMIT;  -- Or ROLLBACK to undo
```

### Isolation Levels

**PostgreSQL supports**:
1. `READ UNCOMMITTED` (treated as READ COMMITTED)
2. `READ COMMITTED` (default)
3. `REPEATABLE READ`
4. `SERIALIZABLE`

#### READ COMMITTED
```sql
-- Transaction 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Returns 1000

-- Transaction 2 (concurrent)
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;

-- Transaction 1 (continued)
SELECT balance FROM accounts WHERE id = 1;  -- Returns 900 (sees committed change)
COMMIT;
```
**Use for**: Most web applications, short transactions

#### REPEATABLE READ
```sql
-- Transaction 1
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;  -- Returns 1000

-- Transaction 2 (concurrent)
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;

-- Transaction 1 (continued)
SELECT balance FROM accounts WHERE id = 1;  -- Still returns 1000 (snapshot)
UPDATE accounts SET balance = 800 WHERE id = 1;  -- ERROR: could not serialize
COMMIT;
```
**Use for**: Reports, analytics queries that need consistent view

#### SERIALIZABLE
```sql
-- Most strict, prevents phantom reads and anomalies
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Returns 10

-- Transaction 2 (concurrent)
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
INSERT INTO orders (status) VALUES ('pending');
COMMIT;

-- Transaction 1 (continued)
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Still returns 10
INSERT INTO summary (pending_count) VALUES (10);
COMMIT;  -- May fail with serialization error
```
**Use for**: Financial transactions, critical business logic

### Locking Strategies

#### Row-Level Locks

```sql
-- FOR UPDATE: Exclusive lock (blocks reads with FOR SHARE)
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- FOR SHARE: Shared lock (blocks writes, allows reads)
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR SHARE;
-- Other transactions can read, but not modify
COMMIT;

-- FOR UPDATE SKIP LOCKED: Skip locked rows (useful for job queues)
BEGIN;
SELECT * FROM jobs
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
-- Multiple workers can process different jobs without blocking
UPDATE jobs SET status = 'processing' WHERE id = X;
COMMIT;

-- FOR UPDATE NOWAIT: Error immediately if locked
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;
-- Raises error if row is locked, instead of waiting
COMMIT;
```

#### Advisory Locks

```sql
-- Application-level locks using arbitrary keys
SELECT pg_advisory_lock(12345);
-- Do work
SELECT pg_advisory_unlock(12345);

-- Try lock (non-blocking)
SELECT pg_try_advisory_lock(12345);  -- Returns true if acquired

-- Session-level vs transaction-level
SELECT pg_advisory_lock(12345);  -- Held until explicit unlock
SELECT pg_advisory_xact_lock(12345);  -- Held until transaction end
```

**Use case: Ensure only one process runs a job**
```python
def process_unique_job(job_id):
    with db.begin():
        lock_acquired = db.execute(
            "SELECT pg_try_advisory_xact_lock(:lock_id)",
            {"lock_id": job_id}
        ).scalar()

        if not lock_acquired:
            return "Already processing"

        # Process job
        # Lock released on transaction end
```

### Deadlock Prevention

**Deadlock example**:
```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- Waiting for transaction 2...

-- Transaction 2
BEGIN;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Blocked by T1

-- Transaction 1 (continued)
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- DEADLOCK!
-- ERROR: deadlock detected
```

**Prevention**:
1. **Always lock in same order**
```sql
-- Both transactions lock id=1 first, then id=2
UPDATE accounts SET balance = balance - 100 WHERE id = LEAST(1, 2);
UPDATE accounts SET balance = balance + 100 WHERE id = GREATEST(1, 2);
```

2. **Use lock timeout**
```sql
SET lock_timeout = '2s';
```

3. **Keep transactions short**

---

## Migrations Best Practices

### Alembic Structure

```python
# migrations/versions/001_add_user_email_index.py
"""add user email index

Revision ID: 001
Revises:
Create Date: 2024-01-14
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_index(
        'idx_users_email',
        'users',
        ['email'],
        unique=False
    )

def downgrade():
    op.drop_index('idx_users_email', table_name='users')
```

### Safe Column Addition

**BAD: Adding NOT NULL column without default**
```python
def upgrade():
    # This locks table and fails if rows exist
    op.add_column('users', sa.Column('status', sa.String(20), nullable=False))
```

**GOOD: Multi-step migration**
```python
# Step 1: Add nullable column with default
def upgrade():
    op.add_column('users', sa.Column('status', sa.String(20),
                                     nullable=True,
                                     server_default='active'))

# Step 2: Backfill data (separate migration)
def upgrade():
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")

# Step 3: Make NOT NULL (separate migration)
def upgrade():
    op.alter_column('users', 'status', nullable=False)
    op.alter_column('users', 'status', server_default=None)  # Remove default
```

### Safe Index Creation

**BAD: Blocking index creation**
```python
def upgrade():
    # Locks table for entire index build
    op.create_index('idx_users_email', 'users', ['email'])
```

**GOOD: Concurrent index creation**
```python
def upgrade():
    # Does not lock table (PostgreSQL 11+)
    op.create_index(
        'idx_users_email',
        'users',
        ['email'],
        postgresql_concurrently=True
    )

def downgrade():
    op.drop_index(
        'idx_users_email',
        table_name='users',
        postgresql_concurrently=True
    )
```

**Note**: Must run outside transaction
```python
def upgrade():
    # Disable transaction for this migration
    connection = op.get_bind()
    connection.execution_options(isolation_level="AUTOCOMMIT")

    op.create_index(
        'idx_users_email',
        'users',
        ['email'],
        postgresql_concurrently=True
    )
```

### Safe Column Type Changes

**BAD: Direct type change**
```python
def upgrade():
    # Requires full table rewrite
    op.alter_column('users', 'age', type_=sa.BigInteger())
```

**GOOD: Multi-step with new column**
```python
# Step 1: Add new column
def upgrade():
    op.add_column('users', sa.Column('age_new', sa.BigInteger(), nullable=True))

# Step 2: Copy data
def upgrade():
    op.execute("UPDATE users SET age_new = age")

# Step 3: Swap columns (in transaction)
def upgrade():
    op.drop_column('users', 'age')
    op.alter_column('users', 'age_new', new_column_name='age')
```

### Safe Table Drops

```python
def upgrade():
    # Check no foreign keys reference this table
    # Drop foreign keys first if needed
    op.drop_constraint('fk_orders_user_id', 'orders', type_='foreignkey')

    # Then drop table
    op.drop_table('old_table')

def downgrade():
    # Recreate table structure
    op.create_table(
        'old_table',
        sa.Column('id', sa.Integer(), primary_key=True),
        # ... all columns
    )
    op.create_foreign_key(
        'fk_orders_user_id',
        'orders', 'old_table',
        ['user_id'], ['id']
    )
```

### Data Migrations

```python
def upgrade():
    # Use batch operations for large tables
    connection = op.get_bind()

    # Process in chunks to avoid long locks
    batch_size = 1000
    offset = 0

    while True:
        result = connection.execute(
            f"""
            UPDATE users
            SET normalized_email = LOWER(email)
            WHERE id IN (
                SELECT id FROM users
                WHERE normalized_email IS NULL
                ORDER BY id
                LIMIT {batch_size}
            )
            """
        )

        if result.rowcount == 0:
            break

        offset += batch_size
```

### Migration Testing

```python
def test_migration_up_down():
    # Test upgrade
    alembic.command.upgrade(config, '+1')

    # Verify schema changes
    inspector = sa.inspect(engine)
    assert 'status' in [c['name'] for c in inspector.get_columns('users')]

    # Test downgrade
    alembic.command.downgrade(config, '-1')

    # Verify rollback
    inspector = sa.inspect(engine)
    assert 'status' not in [c['name'] for c in inspector.get_columns('users')]
```

---

## Schema Design

### Normalization Levels

**First Normal Form (1NF)**: Atomic values, no repeating groups
```sql
-- BAD: Repeating groups
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product1 VARCHAR(100),
    product2 VARCHAR(100),
    product3 VARCHAR(100)
);

-- GOOD: Separate table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_name VARCHAR(100)
);
```

**Second Normal Form (2NF)**: 1NF + no partial dependencies
```sql
-- BAD: Product name depends on product_id, not full key (order_id, product_id)
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    product_name VARCHAR(100),
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);

-- GOOD: Separate product table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

**Third Normal Form (3NF)**: 2NF + no transitive dependencies
```sql
-- BAD: City depends on zip_code (transitive)
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    street VARCHAR(200),
    zip_code VARCHAR(10),
    city VARCHAR(100)
);

-- GOOD: Separate zip code table
CREATE TABLE zip_codes (
    code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100)
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    street VARCHAR(200),
    zip_code VARCHAR(10) REFERENCES zip_codes(code)
);
```

### When to Denormalize

**Use case: Frequently joined data**
```sql
-- Normalized (2 queries or expensive join)
SELECT u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Denormalized (1 fast query)
ALTER TABLE users ADD COLUMN order_count INTEGER DEFAULT 0;

-- Update with trigger
CREATE FUNCTION update_user_order_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET order_count = order_count + 1
    WHERE id = NEW.user_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_order_count
AFTER INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION update_user_order_count();
```

**Use case: Aggregated reports**
```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW daily_sales AS
SELECT
    DATE(created_at) as sale_date,
    SUM(total) as total_sales,
    COUNT(*) as order_count
FROM orders
GROUP BY DATE(created_at);

CREATE INDEX idx_daily_sales_date ON daily_sales (sale_date);

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales;
```

### Foreign Key Constraints

```sql
-- Basic foreign key
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id)
);

-- Named constraint with actions
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Composite foreign key
CREATE TABLE order_items (
    order_id INTEGER,
    line_number INTEGER,
    product_id INTEGER,
    CONSTRAINT fk_order_lines
        FOREIGN KEY (order_id, line_number)
        REFERENCES order_lines(order_id, line_number)
);
```

**ON DELETE actions**:
- `CASCADE`: Delete referencing rows
- `SET NULL`: Set foreign key to NULL
- `SET DEFAULT`: Set foreign key to default value
- `RESTRICT`: Prevent deletion (default)
- `NO ACTION`: Similar to RESTRICT but can defer check

### Check Constraints

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    discount_price DECIMAL(10, 2),

    CONSTRAINT chk_price_positive CHECK (price > 0),
    CONSTRAINT chk_discount_valid CHECK (
        discount_price IS NULL OR discount_price < price
    )
);

-- Add constraint to existing table
ALTER TABLE users
ADD CONSTRAINT chk_email_format
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
```

### Partitioning

**Range partitioning (time-series)**
```sql
-- Parent table
CREATE TABLE logs (
    id BIGSERIAL,
    created_at TIMESTAMP NOT NULL,
    message TEXT
) PARTITION BY RANGE (created_at);

-- Partitions
CREATE TABLE logs_2024_01 PARTITION OF logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE logs_2024_02 PARTITION OF logs
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Default partition for unmatched data
CREATE TABLE logs_default PARTITION OF logs DEFAULT;

-- Indexes on each partition
CREATE INDEX idx_logs_2024_01_created ON logs_2024_01 (created_at);
CREATE INDEX idx_logs_2024_02_created ON logs_2024_02 (created_at);
```

**List partitioning (categorical)**
```sql
CREATE TABLE orders (
    id BIGSERIAL,
    status VARCHAR(20) NOT NULL,
    total DECIMAL(10, 2)
) PARTITION BY LIST (status);

CREATE TABLE orders_pending PARTITION OF orders
    FOR VALUES IN ('pending', 'processing');

CREATE TABLE orders_completed PARTITION OF orders
    FOR VALUES IN ('completed', 'shipped');
```

---

## PostgreSQL-Specific Features

### Common Table Expressions (CTEs)

**Basic CTE**
```sql
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
)
SELECT au.name, COUNT(o.id) as order_count
FROM active_users au
LEFT JOIN orders o ON au.id = o.user_id
GROUP BY au.id, au.name;
```

**Recursive CTE (hierarchical data)**
```sql
-- Organization hierarchy
WITH RECURSIVE org_tree AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees reporting to current level
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree
ORDER BY level, name;
```

**Writable CTE**
```sql
-- Move money between accounts atomically
WITH debit AS (
    UPDATE accounts
    SET balance = balance - 100
    WHERE id = 1
    RETURNING id, balance
),
credit AS (
    UPDATE accounts
    SET balance = balance + 100
    WHERE id = 2
    RETURNING id, balance
)
SELECT * FROM debit
UNION ALL
SELECT * FROM credit;
```

### Window Functions

**Ranking**
```sql
SELECT
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as overall_rank,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as row_num
FROM employees;
```

**Running totals**
```sql
SELECT
    date,
    revenue,
    SUM(revenue) OVER (ORDER BY date) as cumulative_revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day
FROM daily_sales;
```

**LAG/LEAD for comparisons**
```sql
SELECT
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) as prev_day_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) as day_over_day_change,
    LEAD(revenue, 1) OVER (ORDER BY date) as next_day_revenue
FROM daily_sales;
```

**FIRST_VALUE/LAST_VALUE**
```sql
SELECT
    employee_id,
    salary,
    hire_date,
    FIRST_VALUE(salary) OVER (ORDER BY hire_date) as starting_salary,
    LAST_VALUE(salary) OVER (
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as current_salary
FROM salary_history;
```

### JSONB Operations

**Creation and indexing**
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    metadata JSONB
);

CREATE INDEX idx_events_metadata ON events USING GIN (metadata);
CREATE INDEX idx_events_type ON events ((metadata->>'type'));
```

**Querying**
```sql
-- Contains
SELECT * FROM events WHERE metadata @> '{"user_id": 123}';

-- Key exists
SELECT * FROM events WHERE metadata ? 'error_code';

-- Any key exists
SELECT * FROM events WHERE metadata ?| ARRAY['error', 'warning'];

-- All keys exist
SELECT * FROM events WHERE metadata ?& ARRAY['user_id', 'session_id'];

-- Path query
SELECT * FROM events WHERE metadata @> '{"user": {"role": "admin"}}';

-- Extract value
SELECT
    id,
    metadata->>'type' as event_type,
    metadata->'user'->>'name' as user_name
FROM events;

-- Array operations
SELECT * FROM events WHERE metadata->'tags' @> '["important"]';
```

**Updating**
```sql
-- Add/update key
UPDATE events
SET metadata = metadata || '{"processed": true}'
WHERE id = 1;

-- Remove key
UPDATE events
SET metadata = metadata - 'temp_data'
WHERE id = 1;

-- Update nested value
UPDATE events
SET metadata = jsonb_set(metadata, '{user, status}', '"active"')
WHERE id = 1;

-- Append to array
UPDATE events
SET metadata = jsonb_set(
    metadata,
    '{tags}',
    (metadata->'tags') || '["new_tag"]'
)
WHERE id = 1;
```

### Array Operations

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title TEXT,
    tags TEXT[]
);

-- Insert
INSERT INTO posts (title, tags)
VALUES ('PostgreSQL Tips', ARRAY['database', 'sql', 'performance']);

-- Query
SELECT * FROM posts WHERE tags @> ARRAY['database'];  -- Contains
SELECT * FROM posts WHERE tags && ARRAY['sql', 'nosql'];  -- Overlaps
SELECT * FROM posts WHERE 'performance' = ANY(tags);  -- Any match

-- Update
UPDATE posts SET tags = array_append(tags, 'new_tag') WHERE id = 1;
UPDATE posts SET tags = array_remove(tags, 'old_tag') WHERE id = 1;

-- Aggregation
SELECT unnest(tags) as tag, COUNT(*) as count
FROM posts
GROUP BY tag
ORDER BY count DESC;
```

### Full-Text Search

```sql
-- Add tsvector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Populate with trigger
CREATE FUNCTION articles_search_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.body, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvector_update
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW EXECUTE FUNCTION articles_search_trigger();

-- Create GIN index
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Search with ranking
SELECT
    id,
    title,
    ts_rank(search_vector, query) as rank
FROM articles,
     to_tsquery('english', 'postgresql & (performance | optimization)') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Highlight results
SELECT
    id,
    title,
    ts_headline('english', body, query) as excerpt
FROM articles,
     to_tsquery('english', 'postgresql & performance') query
WHERE search_vector @@ query;
```

---

## Connection Pooling

### Why Connection Pooling

**Problem**: Creating connections is expensive
- TCP handshake
- PostgreSQL authentication
- Session initialization

**Solution**: Reuse connections via pool

### PgBouncer Configuration

```ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 127.0.0.1
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Pool modes
pool_mode = transaction  # or session, or statement

# Pool sizes
default_pool_size = 25
max_client_conn = 100
reserve_pool_size = 5

# Timeouts
server_idle_timeout = 600
server_lifetime = 3600
```

**Pool modes**:
- `session`: Connection held for entire client session (safest)
- `transaction`: Connection released after transaction (recommended)
- `statement`: Connection released after each statement (aggressive)

### Application-Level Pooling (SQLAlchemy)

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/mydb',
    poolclass=QueuePool,
    pool_size=10,          # Persistent connections
    max_overflow=20,        # Additional connections if pool exhausted
    pool_timeout=30,        # Wait for connection (seconds)
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Verify connections before use
)

# Monitor pool
from sqlalchemy import event

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    print(f"New connection: {id(dbapi_conn)}")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    print(f"Checkout: {id(dbapi_conn)}, Pool size: {engine.pool.size()}")
```

### Monitoring Connections

```sql
-- Active connections
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query,
    state_change
FROM pg_stat_activity
WHERE datname = 'mydb';

-- Connection counts by state
SELECT state, COUNT(*)
FROM pg_stat_activity
GROUP BY state;

-- Long-running queries
SELECT
    pid,
    now() - query_start as duration,
    query
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '5 minutes'
ORDER BY duration DESC;

-- Kill connection
SELECT pg_terminate_backend(pid);
```

---

## Anti-Patterns

### 1. SELECT * in Production

**Problem**: Fetches unnecessary data, breaks when schema changes

```sql
-- BAD
SELECT * FROM users WHERE id = 1;

-- GOOD
SELECT id, name, email FROM users WHERE id = 1;
```

### 2. NOT IN with NULLs

**Problem**: Returns no rows if subquery contains NULL

```sql
-- BAD (returns no rows if any user has NULL manager_id)
SELECT * FROM users WHERE id NOT IN (SELECT manager_id FROM users);

-- GOOD
SELECT * FROM users
WHERE id NOT IN (SELECT manager_id FROM users WHERE manager_id IS NOT NULL);

-- BETTER
SELECT u.* FROM users u
LEFT JOIN users m ON u.id = m.manager_id
WHERE m.id IS NULL;
```

### 3. Correlated Subqueries in SELECT

**Problem**: Runs for every row

```sql
-- BAD (N queries)
SELECT
    u.id,
    u.name,
    (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count
FROM users u;

-- GOOD (1 query)
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

### 4. Implicit Type Conversions

**Problem**: Prevents index usage

```sql
-- BAD (user_id is INTEGER, but comparing to VARCHAR)
SELECT * FROM orders WHERE user_id = '123';

-- GOOD
SELECT * FROM orders WHERE user_id = 123;

-- BAD (created_at is TIMESTAMP, comparing to TEXT)
SELECT * FROM orders WHERE created_at::TEXT = '2024-01-01';

-- GOOD
SELECT * FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-01-02';
```

### 5. Cartesian Products

**Problem**: Joins without conditions

```sql
-- BAD (returns N × M rows)
SELECT * FROM users, orders;

-- GOOD
SELECT * FROM users u
JOIN orders o ON u.id = o.user_id;
```

### 6. OFFSET for Pagination

**Problem**: Slow for large offsets (still scans all rows)

```sql
-- BAD (scans 10,000 rows to skip them)
SELECT * FROM orders ORDER BY created_at LIMIT 100 OFFSET 10000;

-- GOOD (keyset pagination)
SELECT * FROM orders
WHERE created_at < :last_seen_timestamp
ORDER BY created_at DESC
LIMIT 100;

-- Or with composite key
SELECT * FROM orders
WHERE (created_at, id) < (:last_timestamp, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT 100;
```

### 7. DISTINCT Instead of JOIN Fix

**Problem**: Hides incorrect joins

```sql
-- BAD (using DISTINCT to hide duplicate rows)
SELECT DISTINCT u.name
FROM users u
JOIN orders o ON u.id = o.user_id;

-- GOOD (fix the join)
SELECT u.name
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- Or use aggregation
SELECT u.name
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

### 8. Storing JSON as TEXT

**Problem**: Can't query efficiently, loses validation

```sql
-- BAD
CREATE TABLE events (metadata TEXT);
INSERT INTO events VALUES ('{"user_id": 123}');
SELECT * FROM events WHERE metadata LIKE '%user_id%';

-- GOOD
CREATE TABLE events (metadata JSONB);
CREATE INDEX ON events USING GIN (metadata);
INSERT INTO events VALUES ('{"user_id": 123}');
SELECT * FROM events WHERE metadata @> '{"user_id": 123}';
```

### 9. Boolean Trap in WHERE

**Problem**: Verbose and slow

```sql
-- BAD
SELECT * FROM users WHERE is_active = true;
SELECT * FROM users WHERE is_deleted = false;

-- GOOD
SELECT * FROM users WHERE is_active;
SELECT * FROM users WHERE NOT is_deleted;
```

### 10. Missing Transaction for Multi-Statement Operations

**Problem**: Data inconsistency on partial failure

```python
# BAD
db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")

# GOOD
with db.begin():
    db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
```

---

## Quick Reference

### Query Optimization Checklist

- [ ] SELECT only needed columns
- [ ] Use indexes on WHERE/JOIN columns
- [ ] Avoid functions on indexed columns
- [ ] Use EXPLAIN ANALYZE to verify plan
- [ ] Check row estimate accuracy
- [ ] Prevent N+1 queries (use JOINs or eager loading)
- [ ] Use appropriate join type (INNER vs LEFT)
- [ ] Filter early (WHERE before JOIN when possible)
- [ ] Use CTEs for readability (but watch optimization fence)

### Index Creation Checklist

- [ ] Index columns in WHERE clauses
- [ ] Index foreign key columns
- [ ] Index ORDER BY columns
- [ ] Consider composite indexes for multiple columns
- [ ] Use partial indexes for frequent filters
- [ ] Use expression indexes for functions
- [ ] Create indexes CONCURRENTLY in production
- [ ] Monitor index usage (pg_stat_user_indexes)
- [ ] Remove unused indexes

### Transaction Checklist

- [ ] Keep transactions short
- [ ] Choose appropriate isolation level
- [ ] Use locking to prevent race conditions
- [ ] Handle deadlocks with retry logic
- [ ] Set lock timeout
- [ ] Use advisory locks for distributed coordination

### Schema Design Checklist

- [ ] Normalize to 3NF (usually)
- [ ] Add foreign key constraints
- [ ] Add check constraints for business rules
- [ ] Use appropriate data types
- [ ] Consider partitioning for large tables (>1M rows)
- [ ] Add indexes for common queries
- [ ] Document schema design decisions

### Migration Checklist

- [ ] Test upgrade and downgrade
- [ ] Add columns as nullable first
- [ ] Create indexes CONCURRENTLY
- [ ] Use multi-step migrations for type changes
- [ ] Batch large data migrations
- [ ] Set lock timeout
- [ ] Have rollback plan

---

## Performance Monitoring Queries

```sql
-- Cache hit ratio (should be >99%)
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;

-- Table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Missing indexes (high seq scan)
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan AS avg_seq_tup,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;

-- Bloat estimation
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Lock monitoring
SELECT
    locktype,
    database,
    relation::regclass,
    page,
    tuple,
    virtualxid,
    transactionid,
    mode,
    granted
FROM pg_locks
WHERE NOT granted;
```

This skill provides production-ready SQL patterns and PostgreSQL optimization techniques. Apply based on specific query performance issues and scale requirements.


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

