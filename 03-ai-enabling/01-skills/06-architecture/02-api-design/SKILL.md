---
last_updated: 2026-02-25
status: active
name: api-design
description: REST API design, GraphQL patterns, versioning, documentation. Use when designing or reviewing APIs.
triggers:
  files: ["**/api/**", "**/routes/**", "**/openapi.yaml", "**/schema.graphql", "**/swagger.*"]
  keywords: ["REST", "GraphQL", "endpoint", "API versioning", "OpenAPI", "HTTP method", "status code", "pagination", "API design"]
allowed-tools: Read, Write, Edit
---

# API Design Deep Expertise

Create APIs that developers love to use. This skill covers designing intuitive, consistent, and well-documented APIs that balance developer experience with technical excellence.

## Philosophy: Designing for Developers

APIs are products with developers as customers. Great API design means:

- **Intuitive**: Developers can predict behavior without reading docs
- **Consistent**: Patterns repeat predictably across endpoints
- **Forgiving**: Helpful errors guide developers to success
- **Evolvable**: Changes don't break existing integrations
- **Discoverable**: Self-documenting with clear relationships
- **Performant**: Fast responses with smart caching and pagination

The best APIs feel like an extension of the developer's own code.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Design Principles

### 1. Consistency Above All

Consistency reduces cognitive load. Establish patterns and follow them religiously:

- Resource naming conventions
- Error response format
- Authentication approach
- Pagination style
- Filtering syntax
- Date/time formats
- Case conventions (snake_case vs camelCase)

**Bad**: Mixing conventions
```
GET /users          → Returns array
GET /api/v1/posts   → Returns {data: [...]}
GET /comments       → Returns {results: [...], count: 10}
```

**Good**: Consistent structure
```
GET /v1/users       → {data: [...], pagination: {...}}
GET /v1/posts       → {data: [...], pagination: {...}}
GET /v1/comments    → {data: [...], pagination: {...}}
```

### 2. Design for Backwards Compatibility

Breaking changes destroy trust. Design with evolution in mind:

- Add new fields (don't remove or rename existing)
- Make new fields optional
- Use API versioning for breaking changes
- Deprecate gradually with warnings
- Maintain old versions for migration periods

### 3. Make Invalid States Impossible

Use HTTP semantics and validation to prevent errors:

- Required fields should return 400 Bad Request
- Missing authentication returns 401 Unauthorized
- Insufficient permissions return 403 Forbidden
- Missing resources return 404 Not Found
- Validation errors include field-level details

### 4. Optimize for Common Cases

Design for the 80% use case, but support the 20%:

- Default pagination for large collections
- Sensible defaults for optional parameters
- Common fields included by default
- Related resources accessible via expansion
- Bulk operations for batch scenarios

## REST API Design

### Resource Naming

Resources are **nouns**, not verbs. Use plural nouns consistently.

**Bad**: Verbs in URLs
```
POST /createUser
GET /getUser/123
POST /updateUser/123
GET /getAllPosts
```

**Good**: Nouns with HTTP methods
```
POST /users              # Create user
GET /users/123           # Get user
PUT /users/123           # Update user (full)
PATCH /users/123         # Update user (partial)
DELETE /users/123        # Delete user
GET /users               # List users
```

### Resource Hierarchy

Express relationships through URL structure:

```
GET /users/123/posts                    # User's posts
GET /posts/456/comments                 # Post's comments
GET /organizations/789/teams            # Org's teams
GET /organizations/789/teams/12/members # Team members

# Alternative for many-to-many
GET /posts?author_id=123                # Posts by author
GET /teams?member_id=456                # Teams with member
```

**Rule**: Nest only for 1-to-many relationships. Use query parameters for many-to-many.

### HTTP Method Semantics

Each method has specific meaning and guarantees:

| Method | Purpose | Idempotent | Safe | Request Body | Response Body |
|--------|---------|------------|------|--------------|---------------|
| GET | Retrieve resource | Yes | Yes | No | Yes |
| POST | Create resource | No | No | Yes | Yes |
| PUT | Replace resource | Yes | No | Yes | Yes |
| PATCH | Update resource | No | No | Yes | Yes |
| DELETE | Remove resource | Yes | No | Optional | Optional |
| HEAD | Get metadata | Yes | Yes | No | No |
| OPTIONS | Get capabilities | Yes | Yes | No | Yes |

**Idempotent**: Multiple identical requests have same effect as single request
**Safe**: No side effects, read-only operation

### HTTP Status Codes

Use the right status code to communicate clearly:

#### 2xx Success
- **200 OK**: Successful GET, PUT, PATCH, or DELETE
- **201 Created**: Successful POST that creates resource (include Location header)
- **202 Accepted**: Request accepted for async processing
- **204 No Content**: Successful DELETE or update with no response body

#### 3xx Redirection
- **301 Moved Permanently**: Resource has new permanent URL
- **302 Found**: Temporary redirect
- **304 Not Modified**: Resource unchanged (ETag match)

#### 4xx Client Errors
- **400 Bad Request**: Invalid syntax, failed validation
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **405 Method Not Allowed**: HTTP method not supported for endpoint
- **409 Conflict**: Request conflicts with current state (e.g., duplicate)
- **422 Unprocessable Entity**: Syntax valid but semantically incorrect
- **429 Too Many Requests**: Rate limit exceeded

#### 5xx Server Errors
- **500 Internal Server Error**: Generic server error
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Server temporarily unavailable
- **504 Gateway Timeout**: Upstream server timeout

### Pagination Patterns

Never return unbounded collections. Implement pagination from day one.

#### Offset-Based Pagination

Simple but has consistency issues with changing data:

```
GET /posts?limit=20&offset=40

Response:
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 1543,
    "has_more": true
  }
}
```

**Pros**: Easy to implement, supports jumping to pages
**Cons**: Performance degrades with high offsets, inconsistent with data changes

#### Cursor-Based Pagination

More robust for changing data:

```
GET /posts?limit=20&cursor=eyJpZCI6MTIzfQ==

Response:
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTQzfQ==",
    "prev_cursor": "eyJpZCI6MTAzfQ==",
    "has_more": true
  }
}
```

**Pros**: Consistent results, efficient for infinite scroll
**Cons**: Can't jump to arbitrary pages, opaque cursors

**Cursor encoding**: Base64-encode JSON with sorting/filtering state
```json
// Decoded cursor
{"id": 143, "created_at": "2025-01-14T10:30:00Z"}
```

#### Keyset Pagination

Transparent alternative to cursor pagination:

```
GET /posts?limit=20&after_id=123&after_created_at=2025-01-14T10:30:00Z

Response:
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "last_id": 143,
    "last_created_at": "2025-01-14T11:00:00Z",
    "has_more": true
  }
}
```

**Pros**: Efficient, transparent, supports complex sorting
**Cons**: More complex to implement correctly

### Filtering and Sorting

Provide flexible querying without building a query language:

```
# Simple equality filters
GET /posts?status=published&author_id=123

# Range filters
GET /posts?created_after=2025-01-01&created_before=2025-12-31

# Multiple values (OR)
GET /posts?status=published,draft

# Sorting
GET /posts?sort=created_at        # Ascending (default)
GET /posts?sort=-created_at       # Descending (minus prefix)
GET /posts?sort=author_id,-created_at  # Multiple fields

# Full-text search
GET /posts?q=api+design

# Combined
GET /posts?status=published&author_id=123&sort=-created_at&limit=20
```

**Complex filters**: Consider dedicated search endpoint with JSON body:
```
POST /posts/search
{
  "filters": {
    "status": ["published", "draft"],
    "created_at": {"gte": "2025-01-01", "lt": "2026-01-01"},
    "author": {"team_id": 5}
  },
  "sort": ["-created_at", "title"],
  "limit": 20
}
```

### Sparse Fieldsets (Partial Responses)

Let clients request only needed fields:

```
# Default: Return all fields
GET /users/123

# Sparse: Return specific fields
GET /users/123?fields=id,name,email

# Include related resources
GET /posts/456?include=author,comments
```

Implementation:
```python
# FastAPI example
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    fields: Optional[str] = None,
    include: Optional[str] = None
):
    user = await db.get_user(user_id)

    if fields:
        requested_fields = fields.split(',')
        user_dict = {k: v for k, v in user.dict().items()
                     if k in requested_fields}
    else:
        user_dict = user.dict()

    if include:
        for relation in include.split(','):
            user_dict[relation] = await db.get_related(user_id, relation)

    return user_dict
```

### Bulk Operations

Support batch requests to reduce round trips:

```
# Create multiple resources
POST /users/batch
{
  "items": [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
  ]
}

Response:
{
  "results": [
    {"index": 0, "status": 201, "id": 123, "name": "Alice"},
    {"index": 1, "status": 409, "error": "Email already exists"}
  ]
}

# Update multiple resources
PATCH /posts/batch
{
  "items": [
    {"id": 1, "status": "published"},
    {"id": 2, "status": "archived"}
  ]
}

# Delete multiple resources
DELETE /comments/batch
{
  "ids": [1, 2, 3, 4, 5]
}
```

**Key principle**: Partial success is OK. Return status per item.

### HATEOAS (Hypermedia)

Include links to related actions and resources:

```json
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "status": "active",
  "_links": {
    "self": {"href": "/users/123"},
    "posts": {"href": "/users/123/posts"},
    "edit": {"href": "/users/123", "method": "PATCH"},
    "deactivate": {"href": "/users/123/deactivate", "method": "POST"}
  }
}
```

Benefits:
- Self-documenting API
- Clients discover available actions
- Server controls state transitions
- Easier API evolution

## GraphQL Design

### Schema Design Principles

GraphQL schemas should model your domain clearly:

```graphql
# Good: Clear types with meaningful relationships
type User {
  id: ID!
  name: String!
  email: String!
  posts(
    first: Int = 20
    after: String
    status: PostStatus
  ): PostConnection!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments(first: Int = 10, after: String): CommentConnection!
  publishedAt: DateTime
  status: PostStatus!
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  cursor: String!
  node: Post!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

**Key practices**:
- Use clear, domain-specific types
- Non-null (`!`) for required fields
- Enums for fixed sets of values
- Connections for paginated lists
- DateTime scalar for timestamps
- ID type for identifiers

### Query Patterns

Design queries for common use cases:

```graphql
type Query {
  # Single resource
  user(id: ID!): User
  post(id: ID!): Post

  # Lists with filtering and pagination
  users(
    first: Int = 20
    after: String
    status: UserStatus
    search: String
  ): UserConnection!

  posts(
    first: Int = 20
    after: String
    authorId: ID
    status: PostStatus
    sortBy: PostSortField
    sortOrder: SortOrder
  ): PostConnection!

  # Search across multiple types
  search(
    query: String!
    types: [SearchableType!]
    first: Int = 20
  ): SearchResultConnection!

  # Current user context
  me: User
}

enum SortOrder {
  ASC
  DESC
}

enum PostSortField {
  CREATED_AT
  UPDATED_AT
  PUBLISHED_AT
  TITLE
}
```

### Mutation Patterns

Clear input/output types for mutations:

```graphql
type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): DeletePostPayload!
  publishPost(id: ID!): PublishPostPayload!
}

# Input types
input CreatePostInput {
  title: String!
  content: String!
  status: PostStatus = DRAFT
}

input UpdatePostInput {
  id: ID!
  title: String
  content: String
  status: PostStatus
}

# Payload types with errors
type CreatePostPayload {
  post: Post
  errors: [UserError!]!
  success: Boolean!
}

type UserError {
  message: String!
  field: String
  code: String!
}

type DeletePostPayload {
  deletedId: ID
  errors: [UserError!]!
  success: Boolean!
}
```

**Pattern**: Input types + Payload types with nullable result + errors array

### Resolver Best Practices

Efficient resolver implementation:

```python
# Bad: N+1 query problem
class PostResolver:
    def resolve_author(self, info):
        # This runs once PER POST
        return db.query(User).filter_by(id=self.author_id).first()

# Good: DataLoader batching
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        # This runs ONCE for all posts
        users = await db.query(User).filter(User.id.in_(user_ids)).all()
        user_map = {user.id: user for user in users}
        return [user_map.get(id) for id in user_ids]

class PostResolver:
    def resolve_author(self, info):
        loader = info.context.loaders.user_loader
        return loader.load(self.author_id)
```

**DataLoader pattern**: Batch + cache related resource fetches

### Subscription Patterns

Real-time updates with GraphQL subscriptions:

```graphql
type Subscription {
  # Subscribe to changes on specific resource
  postUpdated(id: ID!): Post!

  # Subscribe to new items in collection
  newPost(authorId: ID): Post!

  # Subscribe to stream of events
  notifications: Notification!
}

# Example client usage
subscription {
  postUpdated(id: "123") {
    id
    title
    content
    status
    updatedAt
  }
}
```

Implementation considerations:
- Use WebSockets for transport
- Implement authentication on subscription connect
- Consider scaling with Redis Pub/Sub
- Rate limit subscription events
- Clean up subscriptions on disconnect

### N+1 Query Problem

The classic GraphQL performance issue:

```graphql
# Client query
query {
  posts(first: 10) {
    edges {
      node {
        id
        title
        author {    # N+1 problem here
          name
          email
        }
        comments(first: 5) {  # Another N+1 here
          edges {
            node {
              content
              author {  # And another here
                name
              }
            }
          }
        }
      }
    }
  }
}
```

**Solutions**:

1. **DataLoader** (recommended): Batches and caches
2. **Query optimization**: Look-ahead resolver
3. **GraphQL-specific ORM**: Automatic joins
4. **Persisted queries**: Pre-optimize known queries

## API Versioning

### When to Version

Version when making **breaking changes**:

- Removing fields or endpoints
- Renaming fields
- Changing field types
- Changing response structure
- Changing authentication scheme
- Changing error format

**Non-breaking changes** (no version bump needed):
- Adding new fields (optional)
- Adding new endpoints
- Adding new optional parameters
- Adding new enum values (append only)
- Making required fields optional

### Versioning Strategies

#### 1. URI Versioning (Most Common)

Include version in URL path:

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

**Pros**: Explicit, easy to test different versions, clear routing
**Cons**: URL changes, clutters namespace

#### 2. Header Versioning

Specify version in header:

```
GET /users
Accept: application/vnd.example.v1+json

GET /users
Accept: application/vnd.example.v2+json
```

**Pros**: Clean URLs, semantic HTTP
**Cons**: Less discoverable, harder to test in browser

#### 3. Query Parameter Versioning

Pass version as parameter:

```
GET /users?version=1
GET /users?version=2
```

**Pros**: Simple, flexible
**Cons**: Caching issues, non-standard

**Recommendation**: Use URI versioning (`/v1/`, `/v2/`) for simplicity and clarity.

### Version Management

```python
# FastAPI example with versioned routers
from fastapi import APIRouter, FastAPI

app = FastAPI()

# Version 1
v1_router = APIRouter(prefix="/v1")

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: int):
    return {
        "id": user_id,
        "full_name": "Alice Smith"  # Old field name
    }

# Version 2
v2_router = APIRouter(prefix="/v2")

@v2_router.get("/users/{user_id}")
async def get_user_v2(user_id: int):
    return {
        "id": user_id,
        "name": "Alice Smith",  # Renamed field
        "email": "alice@example.com"  # New field
    }

app.include_router(v1_router)
app.include_router(v2_router)
```

### Deprecation Strategy

Communicate deprecation clearly:

1. **Announce**: Document deprecation in changelog
2. **Warn**: Add deprecation headers
   ```
   Deprecation: true
   Sunset: Sat, 31 Dec 2025 23:59:59 GMT
   Link: <https://api.example.com/docs/v2>; rel="successor-version"
   ```
3. **Support**: Maintain old version for migration period (6-12 months)
4. **Remove**: After sunset date, return 410 Gone

## Request/Response Design

### Consistent Error Format

Standardize error responses across all endpoints:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Email address is invalid",
        "code": "invalid_format"
      },
      {
        "field": "age",
        "message": "Age must be between 0 and 120",
        "code": "out_of_range"
      }
    ],
    "request_id": "req_abc123xyz",
    "docs_url": "https://api.example.com/docs/errors/validation_error"
  }
}
```

**Error response fields**:
- `code`: Machine-readable error code (string constant)
- `message`: Human-readable description
- `details`: Array of field-level errors
- `request_id`: For support/debugging
- `docs_url`: Link to error documentation

**Implementation**:
```python
from fastapi import HTTPException
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    field: str
    message: str
    code: str

class ErrorResponse(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = []
    request_id: str
    docs_url: str

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    details = [
        ErrorDetail(
            field=err['loc'][-1],
            message=err['msg'],
            code='invalid_format'
        )
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "error": ErrorResponse(
                code="validation_error",
                message="Invalid request parameters",
                details=details,
                request_id=request.state.request_id,
                docs_url=f"{BASE_URL}/docs/errors/validation_error"
            ).dict()
        }
    )
```

### Error Code Taxonomy

Establish consistent error codes:

```
# Authentication/Authorization
- auth_required
- auth_invalid
- auth_expired
- permission_denied

# Validation
- validation_error
- missing_field
- invalid_format
- out_of_range
- too_long
- too_short

# Resources
- not_found
- already_exists
- conflict
- gone

# Rate Limiting
- rate_limit_exceeded
- quota_exceeded

# Server
- internal_error
- service_unavailable
- timeout
```

### Envelope Pattern

**Avoid envelopes for simple success**:

```json
// Bad: Unnecessary wrapper
{
  "status": "success",
  "data": {
    "id": 123,
    "name": "Alice"
  }
}

// Good: Direct resource
{
  "id": 123,
  "name": "Alice"
}
```

**Use envelopes when you need metadata**:

```json
// Good: Pagination metadata needed
{
  "data": [...],
  "pagination": {
    "total": 1543,
    "limit": 20,
    "offset": 40
  }
}

// Good: Mixed success/failure in batch
{
  "results": [
    {"index": 0, "status": 201, "data": {...}},
    {"index": 1, "status": 409, "error": {...}}
  ]
}
```

### Idempotency Keys

Support safe retries for write operations:

```
POST /payments
Idempotency-Key: key_abc123xyz
{
  "amount": 5000,
  "currency": "usd",
  "customer_id": "cus_123"
}

# If client retries with same key, return original result
POST /payments
Idempotency-Key: key_abc123xyz
{...}
→ Returns same payment, doesn't charge twice
```

**Implementation**:
```python
from fastapi import Header, HTTPException

@app.post("/payments")
async def create_payment(
    payment: PaymentRequest,
    idempotency_key: str = Header(None, alias="Idempotency-Key")
):
    if not idempotency_key:
        raise HTTPException(400, "Idempotency-Key header required")

    # Check if already processed
    existing = await db.get_by_idempotency_key(idempotency_key)
    if existing:
        return existing  # Return cached result

    # Process new request
    result = await process_payment(payment)

    # Store with idempotency key
    await db.store_with_key(idempotency_key, result)

    return result
```

**Idempotency key guidelines**:
- Client-generated UUID
- Store for 24 hours minimum
- Required for non-idempotent operations (POST, PATCH)
- Not needed for idempotent operations (GET, PUT, DELETE)

## Authentication & Authorization

### Authentication Schemes

#### API Keys

Simple but limited:

```
GET /users
Authorization: Bearer api_key_abc123xyz
```

**Pros**: Simple, good for server-to-server
**Cons**: No expiration, no scopes, hard to rotate

**Use for**: Internal services, webhooks, simple integrations

#### JWT (JSON Web Tokens)

Stateless tokens with claims:

```
GET /users
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

JWT payload:
```json
{
  "sub": "user_123",
  "email": "alice@example.com",
  "scopes": ["read:users", "write:posts"],
  "exp": 1737728400,
  "iat": 1737724800
}
```

**Pros**: Stateless, contains claims, supports expiration
**Cons**: Can't revoke before expiration (use short TTL + refresh tokens)

**Use for**: Web apps, mobile apps, distributed systems

#### OAuth 2.0

Delegation with scopes:

```
# Authorization Code Flow
1. Client redirects to: /oauth/authorize?client_id=...&scope=read:users
2. User approves
3. Redirect back with code: /callback?code=abc123
4. Exchange code for token: POST /oauth/token
5. Use token: GET /users (Authorization: Bearer ...)
```

**Pros**: Industry standard, supports delegation, fine-grained scopes
**Cons**: Complex to implement correctly

**Use for**: Third-party integrations, public APIs

### Scopes and Permissions

Define granular permissions:

```
# Resource:action pattern
read:users
write:users
delete:users
read:posts
write:posts
admin:all

# Check in endpoint
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    token: dict = Depends(verify_token)
):
    if "read:users" not in token["scopes"]:
        raise HTTPException(403, "Insufficient permissions")

    return await db.get_user(user_id)
```

**Scope design principles**:
- Use `resource:action` format
- Prefer fine-grained over coarse-grained
- Document scope requirements in API docs
- Return 403 Forbidden for insufficient scopes
- Consider hierarchical scopes (e.g., `admin:*` implies all)

### Rate Limiting

Protect API from abuse:

```
GET /users
→ 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1737724800

# After 1000 requests
→ 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1737724800
Retry-After: 3600

{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 1 hour."
  }
}
```

**Rate limit strategies**:

1. **Fixed window**: 1000 requests per hour (simple but has burst issue)
2. **Sliding window**: 1000 requests per rolling 60 minutes (better, more complex)
3. **Token bucket**: Refills at steady rate (smoothest, most complex)

**Implementation**:
```python
from fastapi import Request, HTTPException
import redis
from datetime import datetime

redis_client = redis.Redis()

async def rate_limit(request: Request):
    user_id = request.state.user_id
    window = datetime.now().strftime("%Y-%m-%d-%H")  # Hourly window
    key = f"rate_limit:{user_id}:{window}"

    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, 3600)  # 1 hour TTL

    limit = 1000
    remaining = max(0, limit - count)

    # Add headers
    request.state.rate_limit_headers = {
        "X-RateLimit-Limit": str(limit),
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(int(datetime.now().timestamp()) + 3600)
    }

    if count > limit:
        raise HTTPException(429, "Rate limit exceeded")

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    response = await call_next(request)
    if hasattr(request.state, "rate_limit_headers"):
        for key, value in request.state.rate_limit_headers.items():
            response.headers[key] = value
    return response
```

**Rate limit tiers**:
- Free tier: 1,000 requests/hour
- Basic tier: 10,000 requests/hour
- Pro tier: 100,000 requests/hour
- Enterprise: Custom limits

## Documentation

### OpenAPI/Swagger Specification

Generate documentation from code:

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="Example API",
    description="API for managing users and posts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class User(BaseModel):
    """User model"""
    id: int = Field(..., description="Unique user identifier")
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., description="User's email address")

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "name": "Alice Smith",
                "email": "alice@example.com"
            }
        }

@app.get(
    "/users/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Retrieve a single user by their unique identifier",
    responses={
        200: {
            "description": "User found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "name": "Alice Smith",
                        "email": "alice@example.com"
                    }
                }
            }
        },
        404: {"description": "User not found"}
    }
)
async def get_user(
    user_id: int = Path(..., description="ID of user to retrieve"),
    include_posts: bool = Query(False, description="Include user's posts")
):
    """
    Get a user by ID.

    - **user_id**: Unique identifier
    - **include_posts**: Whether to include user's posts in response
    """
    pass
```

**Documentation checklist**:
- [ ] Summary and description for each endpoint
- [ ] Request/response examples
- [ ] Parameter descriptions
- [ ] Error response examples
- [ ] Authentication requirements
- [ ] Rate limit information

### API Changelog

Maintain changelog for API changes:

```markdown
# API Changelog

## v2.0.0 - 2026-01-14

### Breaking Changes
- Renamed `full_name` to `name` in User model
- Removed deprecated `/users/search` endpoint (use `/users?search=` instead)

### Added
- Added `email` field to User model
- New endpoint: `POST /users/batch` for bulk user creation
- Support for cursor-based pagination in all list endpoints

### Fixed
- Fixed race condition in `POST /posts` when creating with duplicate titles
- Improved error messages for validation errors

## v1.5.0 - 2025-12-01

### Added
- Added `?include` parameter to expand related resources
- New endpoint: `GET /posts/{id}/comments`

### Deprecated
- `/users/search` endpoint (use `/users?search=` instead)
```

**Changelog guidelines**:
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Categorize: Breaking Changes, Added, Changed, Deprecated, Fixed
- Include migration guides for breaking changes
- Link to detailed docs for complex changes

## Performance

### Caching

Use HTTP caching for static and semi-static resources:

#### ETag (Entity Tag)

Content-based cache validation:

```
# Initial request
GET /users/123
→ 200 OK
ETag: "33a64df551425fcc55e4d42a148795d9"
{...}

# Subsequent request
GET /users/123
If-None-Match: "33a64df551425fcc55e4d42a148795d9"
→ 304 Not Modified
(no body, saves bandwidth)
```

**Implementation**:
```python
import hashlib
from fastapi import Request, Response

def generate_etag(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()

@app.get("/users/{user_id}")
async def get_user(user_id: int, request: Request, response: Response):
    user = await db.get_user(user_id)
    content = user.json()

    # Generate ETag
    etag = generate_etag(content)
    response.headers["ETag"] = f'"{etag}"'

    # Check If-None-Match
    if request.headers.get("if-none-match") == f'"{etag}"':
        return Response(status_code=304)

    return user
```

#### Cache-Control

Control caching behavior:

```
# Private, cache for 1 hour
Cache-Control: private, max-age=3600

# Public, cache for 1 day, revalidate
Cache-Control: public, max-age=86400, must-revalidate

# Never cache
Cache-Control: no-store, no-cache, must-revalidate
```

**Caching strategies**:
- **Static assets**: `public, max-age=31536000, immutable`
- **User-specific data**: `private, max-age=300`
- **Frequently changing data**: `no-cache` (always revalidate)
- **Sensitive data**: `no-store` (don't cache at all)

#### Last-Modified

Time-based cache validation:

```
# Initial request
GET /posts/456
→ 200 OK
Last-Modified: Wed, 10 Jan 2026 10:00:00 GMT
{...}

# Subsequent request
GET /posts/456
If-Modified-Since: Wed, 10 Jan 2026 10:00:00 GMT
→ 304 Not Modified (if not modified)
→ 200 OK (if modified)
```

### Compression

Enable compression for text responses:

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**Compression headers**:
```
# Client requests compression
Accept-Encoding: gzip, deflate, br

# Server responds with compressed content
Content-Encoding: gzip
Content-Length: 1234  # Compressed size
```

**Compression formats**:
- **gzip**: Universal support, good compression
- **brotli**: Better compression than gzip, modern browsers
- **deflate**: Older, less common

### Async Operations

Use async patterns for long-running operations:

#### Webhooks

Push updates to client:

```
# Client creates resource with webhook
POST /jobs
{
  "type": "export",
  "webhook_url": "https://client.example.com/webhooks/job-complete"
}

→ 202 Accepted
{
  "job_id": "job_abc123",
  "status": "pending",
  "status_url": "/jobs/job_abc123"
}

# When complete, server POSTs to webhook
POST https://client.example.com/webhooks/job-complete
{
  "job_id": "job_abc123",
  "status": "completed",
  "result_url": "/jobs/job_abc123/result"
}
```

#### Polling

Client checks status periodically:

```
# Create job
POST /exports
→ 202 Accepted
{
  "export_id": "exp_abc123",
  "status": "processing",
  "status_url": "/exports/exp_abc123"
}

# Poll status (client waits, then retries)
GET /exports/exp_abc123
→ 200 OK
{
  "export_id": "exp_abc123",
  "status": "processing",
  "progress": 45
}

# Eventually completes
GET /exports/exp_abc123
→ 200 OK
{
  "export_id": "exp_abc123",
  "status": "completed",
  "download_url": "/exports/exp_abc123/download"
}
```

**Polling guidelines**:
- Return `Retry-After` header with recommended wait time
- Exponential backoff (1s, 2s, 4s, 8s, max 30s)
- Include progress indicator when possible
- Set expiration for completed jobs

## Anti-Patterns

Avoid these common mistakes:

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| **Verbs in URLs** | `/getUser`, `/createPost` | Use HTTP methods: `GET /users`, `POST /posts` |
| **Inconsistent naming** | `/users`, `/api/posts`, `/v1/comment` | Consistent structure: `/v1/users`, `/v1/posts`, `/v1/comments` |
| **Generic errors** | `{"error": "Something went wrong"}` | Specific code + message + field details |
| **No pagination** | Return entire collection | Always paginate collections |
| **Ignoring HTTP status** | Return 200 with `{"status": "error"}` | Use proper HTTP status codes |
| **N+1 queries** | Fetching related resources one by one | Use DataLoader, eager loading, or includes |
| **Breaking changes without versioning** | Rename field in existing version | Use API versioning for breaking changes |
| **No rate limiting** | Allow unlimited requests | Implement rate limits with proper headers |
| **Cryptic errors** | `{"error": "Invalid input"}` | Specify which field and why: `{"field": "email", "error": "Invalid format"}` |
| **Required fields in PATCH** | Require all fields for partial update | PATCH should accept partial objects |
| **Deeply nested URLs** | `/orgs/1/teams/2/users/3/posts/4/comments/5` | Max 2-3 levels, use query params for filters |
| **Exposing internal IDs** | Sequential numeric IDs reveal volume | Use UUIDs or hashids for public IDs |
| **No idempotency** | Duplicate POSTs create duplicates | Support idempotency keys |
| **Synchronous long operations** | Client waits 60s for export | Use async with webhooks or polling |

## Real-World Examples

### Stripe API

Excellent API design with strong conventions:

```bash
# List customers with pagination
GET /v1/customers?limit=10&starting_after=cus_123

# Expandable related resources
GET /v1/charges/ch_123?expand[]=customer&expand[]=invoice

# Idempotency for safe retries
POST /v1/charges
Idempotency-Key: key_abc123
{
  "amount": 2000,
  "currency": "usd",
  "source": "tok_visa"
}

# Consistent error format
{
  "error": {
    "type": "card_error",
    "code": "card_declined",
    "message": "Your card was declined",
    "param": "source"
  }
}
```

### GitHub API

Great use of REST conventions:

```bash
# Resource hierarchy
GET /repos/owner/repo/issues
GET /repos/owner/repo/issues/123/comments

# Rich filtering
GET /repos/owner/repo/issues?state=open&labels=bug,urgent&sort=created&direction=desc

# HATEOAS links
{
  "url": "https://api.github.com/repos/owner/repo",
  "issues_url": "https://api.github.com/repos/owner/repo/issues{/number}",
  "pulls_url": "https://api.github.com/repos/owner/repo/pulls{/number}"
}

# Rate limit headers
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1737728400
```

### Shopify GraphQL API

Well-designed GraphQL schema:

```graphql
query {
  products(first: 10, query: "status:active") {
    edges {
      cursor
      node {
        id
        title
        variants(first: 5) {
          edges {
            node {
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

mutation {
  productCreate(input: {
    title: "New Product"
    productType: "Shoes"
  }) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

## Quick Reference

### REST Checklist

- [ ] Resources are nouns, plural
- [ ] HTTP methods used correctly
- [ ] Proper status codes returned
- [ ] Pagination implemented
- [ ] Filtering and sorting available
- [ ] Consistent error format
- [ ] API versioned in URL
- [ ] Rate limiting with headers
- [ ] Authentication required
- [ ] OpenAPI documentation generated
- [ ] Caching headers set appropriately

### GraphQL Checklist

- [ ] Clear type names and relationships
- [ ] Non-null (`!`) for required fields
- [ ] Connection types for pagination
- [ ] Input types for mutations
- [ ] Payload types with errors array
- [ ] DataLoader for N+1 prevention
- [ ] Query complexity limits
- [ ] Depth limits
- [ ] Schema documentation
- [ ] Introspection enabled (dev only)

### API Design Principles

1. **Be consistent** - Patterns should repeat
2. **Be predictable** - Developers should guess correctly
3. **Be forgiving** - Help developers succeed
4. **Be explicit** - Clear over clever
5. **Be versioned** - Never break existing clients
6. **Be documented** - Examples for everything
7. **Be fast** - Cache, paginate, optimize
8. **Be secure** - Auth, rate limit, validate
9. **Be observable** - Log, trace, monitor
10. **Be kind** - Developers are your customers

---

Great API design is about empathy for developers. Make the simple things simple and the complex things possible. Optimize for the common case, document the edge cases, and never break backwards compatibility without a clear migration path.


## Quality Tests

### Trade-Off Test
- Alternatives were considered before choosing this architecture
- **PASS:** At least 2 alternative approaches evaluated with pros/cons
- **FAIL:** Architecture chosen without considering alternatives

### Scalability Test
- Architecture handles 10x current load without redesign
- **PASS:** Bottlenecks identified with specific scaling strategies
- **FAIL:** No analysis of how the system behaves under increased load

