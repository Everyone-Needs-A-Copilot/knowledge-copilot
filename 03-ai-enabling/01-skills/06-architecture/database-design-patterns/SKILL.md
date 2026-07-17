---
last_updated: 2026-02-25
status: active
name: database-design-patterns
description: Patterns for database schema design, indexing, normalization, and data modeling. Use for relational and NoSQL database architecture decisions.
triggers:
  files: ["**/migrations/**", "**/models/**", "**/schema/**", "**/*.sql", "**/database/**"]
  keywords: ["database design", "schema", "normalization", "index", "foreign key", "primary key", "relational", "NoSQL", "partition", "sharding", "query optimization", "data model"]
allowed-tools: Read, Write, Edit
---

# Database Design Patterns

## Overview

Database design is the art of structuring data for efficient storage, retrieval, and manipulation. Good database design balances multiple concerns: data integrity, query performance, storage efficiency, and maintainability.

The design choices you make early significantly impact system performance and evolution. A poorly designed schema can be difficult to change once data is stored, while a well-designed schema makes common operations fast and uncommon operations possible.

This skill covers relational database design, NoSQL patterns, indexing strategies, and operational considerations.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Principles

### 1. Model the Domain

Database schema should reflect the business domain, not implementation details.

**Questions to ask:**
- What entities exist in the domain?
- What are the relationships between entities?
- What are the cardinalities? (one-to-one, one-to-many, many-to-many)
- What attributes define each entity?
- What uniquely identifies each entity?

### 2. Optimize for Access Patterns

Design for how data will be queried, not just how it's structured.

**Consider:**
- What queries will be most frequent?
- What queries need to be fast?
- What data is accessed together?
- Read-heavy or write-heavy workload?

### 3. Data Integrity First

Enforce correctness at the database level.

**Mechanisms:**
- Primary keys (uniqueness)
- Foreign keys (referential integrity)
- Constraints (CHECK, NOT NULL, UNIQUE)
- Transactions (ACID)

### 4. Plan for Evolution

Schemas change. Design for migration.

**Considerations:**
- How will you add new fields?
- How will you handle data migrations?
- How will you deploy schema changes?
- Can you make changes without downtime?

---

## Relational Database Design

### Normalization

Normalization reduces data redundancy and improves integrity.

**First Normal Form (1NF):**
- Eliminate repeating groups
- Each column contains atomic values
- Each row is unique

```sql
-- NOT 1NF: Repeating groups
CREATE TABLE orders (
    order_id INT,
    item1 VARCHAR(100),
    item2 VARCHAR(100),
    item3 VARCHAR(100)  -- What if 4 items?
);

-- 1NF: Separate table for items
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_name VARCHAR(100),
    quantity INT
);
```

**Second Normal Form (2NF):**
- Must be in 1NF
- All non-key columns depend on entire primary key

```sql
-- NOT 2NF: product_name depends only on product_id, not order_id
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- 2NF: Separate products table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT REFERENCES products(product_id),
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
```

**Third Normal Form (3NF):**
- Must be in 2NF
- No transitive dependencies (non-key depends on non-key)

```sql
-- NOT 3NF: city depends on zip_code, not customer_id
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    zip_code VARCHAR(10),
    city VARCHAR(100)  -- Depends on zip_code
);

-- 3NF: Separate zip_codes table
CREATE TABLE zip_codes (
    zip_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    zip_code VARCHAR(10) REFERENCES zip_codes(zip_code)
);
```

### Denormalization

Intentionally add redundancy for query performance.

**When to denormalize:**
- Frequent expensive joins
- Read-heavy workloads
- Caching computed values
- Reporting/analytics needs

**Example: Storing computed total**
```sql
-- Normalized: Calculate total with JOIN
SELECT o.order_id, SUM(oi.quantity * p.price) AS total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY o.order_id;

-- Denormalized: Store total directly
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10, 2),  -- Redundant but fast
    order_date DATE
);
```

**Trade-offs:**
| Aspect | Normalized | Denormalized |
|--------|------------|--------------|
| Read performance | Slower (joins) | Faster |
| Write performance | Faster | Slower (update multiple) |
| Storage | Efficient | Larger |
| Integrity | Guaranteed | Risk of inconsistency |
| Maintenance | Simpler | More complex |

### Entity-Relationship Modeling

**One-to-One:**
```sql
-- Option 1: Same table (if always accessed together)
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255),
    -- Profile fields
    bio TEXT,
    avatar_url VARCHAR(500)
);

-- Option 2: Separate tables (if often accessed separately)
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255)
);

CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    bio TEXT,
    avatar_url VARCHAR(500)
);
```

**One-to-Many:**
```sql
-- One customer has many orders
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE
);
```

**Many-to-Many:**
```sql
-- Students and courses
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    title VARCHAR(200)
);

-- Junction table
CREATE TABLE enrollments (
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    enrolled_at TIMESTAMP DEFAULT NOW(),
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id)
);
```

### Primary Keys

**Natural key:** Business attribute that uniquely identifies (email, SSN)
```sql
CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,  -- Natural key
    name VARCHAR(100)
);
```

**Surrogate key:** System-generated identifier (auto-increment, UUID)
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- Surrogate key
    email VARCHAR(255) UNIQUE,
    name VARCHAR(100)
);

-- Or with UUID
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    name VARCHAR(100)
);
```

**Guidelines:**
| Consideration | Natural Key | Surrogate Key |
|---------------|-------------|---------------|
| Immutability | May change | Never changes |
| Size | Variable | Fixed |
| Foreign keys | Wider | Narrow |
| Business meaning | Yes | No |
| Uniqueness | Must verify | Guaranteed |

**Recommendation:** Use surrogate keys for most tables, natural keys for lookup tables.

### Foreign Keys

**Benefits:**
- Referential integrity (no orphan records)
- Cascade operations
- Query planner hints

**Options:**
```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id)
        ON DELETE CASCADE      -- Delete orders when customer deleted
        ON UPDATE CASCADE      -- Update if customer_id changes
);

-- Other options:
-- ON DELETE SET NULL: Set to NULL when parent deleted
-- ON DELETE RESTRICT: Prevent parent deletion if children exist
-- ON DELETE NO ACTION: Same as RESTRICT (default)
```

### Constraints

**NOT NULL:**
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,  -- Required
    bio TEXT  -- Optional (can be NULL)
);
```

**UNIQUE:**
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,           -- Single column
    UNIQUE (first_name, last_name)       -- Composite
);
```

**CHECK:**
```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    price DECIMAL(10, 2) CHECK (price > 0),
    status VARCHAR(20) CHECK (status IN ('draft', 'active', 'archived'))
);
```

**DEFAULT:**
```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Indexing Strategies

### How Indexes Work

**B-tree index (most common):**
```
                    [50]
                   /    \
            [25,30]      [75,90]
           /   |  \      /   |  \
        [10] [27] [35] [60] [80] [95]
```

- Sorted structure
- O(log n) lookups
- Good for: equality, range, prefix, ORDER BY
- Bad for: suffix matching (LIKE '%abc')

**Hash index:**
```
hash(value) → bucket → row
```

- O(1) lookups
- Good for: exact equality only
- Bad for: range queries, ORDER BY

### Index Types

**Single-column index:**
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Composite index:**
```sql
-- Order matters! Leftmost prefix is key
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- This index supports:
-- WHERE customer_id = 123
-- WHERE customer_id = 123 AND order_date > '2024-01-01'
-- ORDER BY customer_id, order_date

-- But NOT efficiently:
-- WHERE order_date > '2024-01-01' (no customer_id)
```

**Covering index (includes all columns):**
```sql
-- Query: SELECT name, email FROM users WHERE email = 'x'
CREATE INDEX idx_users_email_covering ON users(email) INCLUDE (name);
-- No need to access table, all data in index
```

**Partial index:**
```sql
-- Only index active orders
CREATE INDEX idx_orders_active ON orders(customer_id)
WHERE status = 'active';
```

**Expression index:**
```sql
-- Index on lowercase email
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Supports: WHERE LOWER(email) = 'john@example.com'
```

### When to Create Indexes

**Create indexes on:**
- Primary keys (automatic)
- Foreign keys
- Columns used in WHERE clauses
- Columns used in JOIN conditions
- Columns used in ORDER BY
- Columns used in GROUP BY

**Avoid indexes on:**
- Small tables (full scan may be faster)
- Columns with low cardinality (few unique values)
- Frequently updated columns (index maintenance cost)
- Columns rarely used in queries

### Index Maintenance

**Monitor index usage:**
```sql
-- PostgreSQL: Check unused indexes
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Rebuild bloated indexes:**
```sql
-- PostgreSQL
REINDEX INDEX idx_users_email;

-- Or concurrent rebuild
REINDEX INDEX CONCURRENTLY idx_users_email;
```

---

## Query Optimization

### EXPLAIN and EXPLAIN ANALYZE

```sql
-- Show query plan
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';

-- Show plan with actual execution
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';
```

**Key metrics to watch:**
- Seq Scan vs Index Scan
- Rows estimated vs actual
- Cost (startup and total)
- Execution time

### Common Optimizations

**Avoid SELECT *:**
```sql
-- BAD: Fetches all columns
SELECT * FROM orders WHERE customer_id = 123;

-- GOOD: Only fetch needed columns
SELECT order_id, status, total FROM orders WHERE customer_id = 123;
```

**Use appropriate data types:**
```sql
-- BAD: String for numeric ID
customer_id VARCHAR(50)

-- GOOD: Integer ID
customer_id INT
```

**Avoid functions on indexed columns:**
```sql
-- BAD: Can't use index on email
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';

-- GOOD: Store normalized, query directly
SELECT * FROM users WHERE email_lower = 'john@example.com';

-- Or create expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

**Use EXISTS instead of COUNT:**
```sql
-- BAD: Counts all rows
SELECT CASE WHEN COUNT(*) > 0 THEN true ELSE false END
FROM orders WHERE customer_id = 123;

-- GOOD: Stops at first match
SELECT EXISTS(SELECT 1 FROM orders WHERE customer_id = 123);
```

**Batch operations:**
```sql
-- BAD: N individual inserts
INSERT INTO items (name) VALUES ('a');
INSERT INTO items (name) VALUES ('b');
INSERT INTO items (name) VALUES ('c');

-- GOOD: Single batch insert
INSERT INTO items (name) VALUES ('a'), ('b'), ('c');
```

### N+1 Query Problem

**Problem:**
```python
# 1 query for orders
orders = db.query("SELECT * FROM orders LIMIT 10")

# N queries for customers (one per order)
for order in orders:
    customer = db.query(
        "SELECT * FROM customers WHERE customer_id = ?",
        order.customer_id
    )
```

**Solution: JOIN or batch**
```python
# JOIN: Single query
orders_with_customers = db.query("""
    SELECT o.*, c.name AS customer_name
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    LIMIT 10
""")

# Batch: Two queries
orders = db.query("SELECT * FROM orders LIMIT 10")
customer_ids = [o.customer_id for o in orders]
customers = db.query(
    "SELECT * FROM customers WHERE customer_id IN (?)",
    customer_ids
)
```

---

## NoSQL Patterns

### Document Databases (MongoDB, CouchDB)

**When to use:**
- Flexible, evolving schema
- Hierarchical data
- Document-centric access patterns

**Embedding vs Referencing:**

**Embed when:**
- Data accessed together
- Contained relationship
- One-to-few cardinality

```json
{
  "_id": "order123",
  "customer_name": "John",
  "items": [
    {"product": "Widget", "quantity": 2, "price": 10.00},
    {"product": "Gadget", "quantity": 1, "price": 25.00}
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "Springfield"
  }
}
```

**Reference when:**
- Data accessed independently
- Many-to-many relationships
- Data changes frequently

```json
// Order document
{
  "_id": "order123",
  "customer_id": "cust456",
  "item_ids": ["item1", "item2"]
}

// Customer document
{
  "_id": "cust456",
  "name": "John",
  "email": "john@example.com"
}
```

### Key-Value Stores (Redis, DynamoDB)

**When to use:**
- Simple lookup by key
- Caching
- Session storage
- High-throughput reads

**Access patterns:**
```python
# Simple key-value
redis.set("user:123", json.dumps(user_data))
user = json.loads(redis.get("user:123"))

# Hash (multiple fields)
redis.hset("user:123", mapping={
    "name": "John",
    "email": "john@example.com"
})
name = redis.hget("user:123", "name")
```

**DynamoDB single-table design:**
```
PK              SK                  Attributes
USER#123        PROFILE             {name, email, ...}
USER#123        ORDER#2024-001      {status, total, ...}
USER#123        ORDER#2024-002      {status, total, ...}
ORDER#2024-001  ITEM#1              {product, quantity, ...}
ORDER#2024-001  ITEM#2              {product, quantity, ...}
```

### Column-Family (Cassandra, HBase)

**When to use:**
- Time-series data
- Write-heavy workloads
- Horizontal scalability
- Known query patterns

**Schema design:**
```cql
-- Cassandra: Design around query patterns
CREATE TABLE sensor_readings (
    sensor_id UUID,
    reading_date DATE,
    reading_time TIMESTAMP,
    value DECIMAL,
    PRIMARY KEY ((sensor_id, reading_date), reading_time)
) WITH CLUSTERING ORDER BY (reading_time DESC);

-- Query: Latest readings for sensor on date
SELECT * FROM sensor_readings
WHERE sensor_id = ? AND reading_date = ?
LIMIT 10;
```

### Graph Databases (Neo4j)

**When to use:**
- Complex relationships
- Traversals (shortest path, recommendations)
- Social networks
- Knowledge graphs

**Cypher example:**
```cypher
// Create nodes and relationships
CREATE (john:Person {name: 'John'})
CREATE (jane:Person {name: 'Jane'})
CREATE (acme:Company {name: 'Acme Corp'})
CREATE (john)-[:WORKS_AT]->(acme)
CREATE (jane)-[:WORKS_AT]->(acme)
CREATE (john)-[:KNOWS]->(jane)

// Find colleagues
MATCH (p:Person {name: 'John'})-[:WORKS_AT]->(c:Company)<-[:WORKS_AT]-(colleague)
RETURN colleague.name
```

---

## Partitioning and Sharding

### Horizontal Partitioning (Sharding)

Distribute data across multiple databases by key.

**Range partitioning:**
```
Shard 1: customer_id 1-10000
Shard 2: customer_id 10001-20000
Shard 3: customer_id 20001-30000
```
- **Pro:** Range queries efficient
- **Con:** Hotspots if data skewed

**Hash partitioning:**
```
Shard = hash(customer_id) % num_shards
```
- **Pro:** Even distribution
- **Con:** Range queries require scatter-gather

**Directory-based:**
```
Lookup table: customer_id -> shard_id
```
- **Pro:** Flexible placement
- **Con:** Lookup overhead

### Vertical Partitioning

Split table by columns.

```sql
-- Original: Wide table
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    bio TEXT,              -- Large, rarely accessed
    avatar BYTEA           -- Very large, rarely accessed
);

-- Partitioned: Separate hot and cold data
CREATE TABLE users_core (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255)
);

CREATE TABLE users_profile (
    user_id INT PRIMARY KEY REFERENCES users_core(user_id),
    bio TEXT,
    avatar BYTEA
);
```

### PostgreSQL Table Partitioning

```sql
-- Range partitioning by date
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total DECIMAL(10, 2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Query only touches relevant partition
SELECT * FROM orders WHERE order_date = '2024-02-15';
```

---

## Data Integrity Patterns

### Soft Deletes

Mark records as deleted instead of physically removing.

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255),
    deleted_at TIMESTAMP NULL
);

-- "Delete" user
UPDATE users SET deleted_at = NOW() WHERE user_id = 123;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;

-- View with soft delete filter
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;
```

**Benefits:**
- Audit trail
- Easy recovery
- Referential integrity preserved

**Considerations:**
- Unique constraints need care: `UNIQUE(email) WHERE deleted_at IS NULL`
- Query complexity
- Storage growth

### Audit Trails

Track all changes to data.

**Audit table pattern:**
```sql
CREATE TABLE user_audit (
    audit_id SERIAL PRIMARY KEY,
    user_id INT,
    action VARCHAR(10),  -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by INT,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger to log changes
CREATE OR REPLACE FUNCTION audit_user_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO user_audit (user_id, action, new_values, changed_by)
        VALUES (NEW.user_id, 'INSERT', to_jsonb(NEW), current_user_id());
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO user_audit (user_id, action, old_values, new_values, changed_by)
        VALUES (NEW.user_id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), current_user_id());
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO user_audit (user_id, action, old_values, changed_by)
        VALUES (OLD.user_id, 'DELETE', to_jsonb(OLD), current_user_id());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_user_changes();
```

### Optimistic Locking

Prevent lost updates without blocking.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    status VARCHAR(20),
    version INT DEFAULT 1
);

-- Update only if version matches
UPDATE orders
SET status = 'shipped', version = version + 1
WHERE order_id = 123 AND version = 5;

-- If 0 rows affected, someone else updated first
```

**Application code:**
```python
def update_order_status(order_id: int, new_status: str, expected_version: int):
    result = db.execute("""
        UPDATE orders
        SET status = ?, version = version + 1
        WHERE order_id = ? AND version = ?
    """, (new_status, order_id, expected_version))

    if result.rowcount == 0:
        raise OptimisticLockError("Order was modified by another process")
```

---

## Migrations

### Schema Migration Patterns

**Add column (non-breaking):**
```sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
```

**Rename column (breaking):**
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);

-- Step 2: Migrate data
UPDATE users SET full_name = name;

-- Step 3: Application uses both columns

-- Step 4: Remove old column (after deployment)
ALTER TABLE users DROP COLUMN name;
```

**Change column type:**
```sql
-- Step 1: Add new column
ALTER TABLE orders ADD COLUMN total_cents BIGINT;

-- Step 2: Migrate data
UPDATE orders SET total_cents = (total * 100)::BIGINT;

-- Step 3: Swap columns
ALTER TABLE orders
    DROP COLUMN total,
    RENAME COLUMN total_cents TO total;
```

### Zero-Downtime Migrations

**Expand-Contract pattern:**

1. **Expand:** Add new structure (backward compatible)
2. **Migrate:** Move data to new structure
3. **Contract:** Remove old structure

**Example: Splitting a table**
```sql
-- Phase 1: Add new table, application writes to both
CREATE TABLE user_preferences (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    theme VARCHAR(20),
    notifications_enabled BOOLEAN
);

-- Phase 2: Migrate existing data
INSERT INTO user_preferences (user_id, theme, notifications_enabled)
SELECT user_id, theme, notifications_enabled FROM users;

-- Phase 3: Application reads from new table

-- Phase 4: Remove old columns
ALTER TABLE users
    DROP COLUMN theme,
    DROP COLUMN notifications_enabled;
```

---

## Anti-Patterns

### Entity-Attribute-Value (EAV)

Storing attributes as rows instead of columns.

```sql
-- ANTI-PATTERN: EAV
CREATE TABLE user_attributes (
    user_id INT,
    attribute_name VARCHAR(100),
    attribute_value TEXT,
    PRIMARY KEY (user_id, attribute_name)
);

-- Query for user's email
SELECT attribute_value FROM user_attributes
WHERE user_id = 123 AND attribute_name = 'email';

-- Querying multiple attributes requires multiple joins
```

**Problems:**
- No data type enforcement
- Complex queries
- Poor performance
- No integrity constraints

**When EAV might be acceptable:**
- True dynamic attributes
- Configuration storage
- Very sparse data

### God Table

Single table storing everything.

```sql
-- ANTI-PATTERN: Everything in one table
CREATE TABLE everything (
    id INT PRIMARY KEY,
    type VARCHAR(50),  -- 'user', 'order', 'product', etc.
    data JSONB
);
```

### Ignoring Indexes

No indexes on frequently queried columns.

**Symptoms:**
- Slow queries on large tables
- Sequential scans in EXPLAIN
- High CPU on database

### Over-Indexing

Too many indexes.

**Problems:**
- Slow writes (every INSERT/UPDATE touches indexes)
- Storage overhead
- Complex query planner decisions

**Rule of thumb:** Start minimal, add indexes based on slow query analysis.

### Storing Calculated Values Without Strategy

```sql
-- PROBLEM: Total might become stale
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    total DECIMAL(10, 2)  -- How is this updated?
);
```

**Solutions:**
- Trigger to maintain consistency
- Application responsibility with clear ownership
- Compute on read (materialized view)

---

## Database Selection Guide

### When to Use Relational (PostgreSQL, MySQL)

- Complex queries with joins
- ACID transaction requirements
- Relational data model
- Strong consistency needed
- SQL expertise available

### When to Use Document (MongoDB)

- Flexible, evolving schema
- Document-centric access
- Hierarchical data
- Horizontal scalability needed
- Developer productivity priority

### When to Use Key-Value (Redis)

- Simple key-based access
- Caching layer
- Session storage
- High throughput, low latency
- Ephemeral data

### When to Use Column-Family (Cassandra)

- Write-heavy workloads
- Time-series data
- Known query patterns
- Linear horizontal scaling
- Eventual consistency acceptable

### When to Use Graph (Neo4j)

- Complex relationships
- Traversal queries
- Social networks
- Recommendation engines
- Knowledge graphs

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

- Designing new database schemas
- Optimizing slow queries
- Planning data migrations
- Choosing database technology
- Reviewing data models

### How to Apply

1. **Understand the domain**: Entities, relationships, attributes
2. **Identify access patterns**: What queries matter most?
3. **Start normalized**: Denormalize based on needs
4. **Plan for scale**: Partitioning, indexing strategy
5. **Design for evolution**: Migration patterns
6. **Monitor and optimize**: Query analysis, index tuning

### Red Flags

- No primary keys
- No foreign key constraints
- Missing indexes on JOIN columns
- SELECT * everywhere
- EAV tables for structured data
- No migration strategy
- Ignoring query performance
- One-size-fits-all database choice

---

## References

### Books
- *Designing Data-Intensive Applications* by Martin Kleppmann
- *Database Internals* by Alex Petrov
- *SQL Performance Explained* by Markus Winand

### Online Resources
- Use The Index, Luke (indexing guide)
- PostgreSQL documentation
- MongoDB University

### Tools
- pgAdmin, DBeaver (SQL clients)
- EXPLAIN ANALYZE (query analysis)
- pg_stat_statements (query statistics)
