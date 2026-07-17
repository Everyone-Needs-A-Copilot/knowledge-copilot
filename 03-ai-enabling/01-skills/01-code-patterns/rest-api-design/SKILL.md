---
last_updated: 2026-02-25
status: active
name: rest-api-design
description: REST API design - resources, verbs, status codes, versioning. Use when designing or reviewing APIs.
triggers:
  files: ["**/api/**", "**/routes/**", "**/endpoints/**", "**/openapi.yaml", "**/swagger.*"]
  keywords: ["REST", "API design", "endpoint", "HTTP method", "status code", "resource", "versioning", "pagination"]
allowed-tools: Read, Write, Edit
---

# REST API Design: Deep Expertise Skill

Design APIs that developers love to use. This skill covers REST principles, resource modeling, HTTP semantics, and patterns for building intuitive, consistent APIs.

## Philosophy: APIs Are User Interfaces

APIs are products with developers as customers. Great API design means:

- **Predictable** - Developers can guess endpoints and behavior
- **Consistent** - Patterns repeat across the entire API
- **Forgiving** - Helpful errors guide developers to success
- **Evolvable** - Changes don't break existing integrations

**The test of good API design:** Can a developer use your API correctly without reading the docs?

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## 1. Resource Design

### Resources Are Nouns

REST APIs model resources (things), not actions. Use nouns, not verbs.

**Bad: Actions in URLs**
```
POST /createUser
GET /getUser?id=123
POST /updateUser
POST /deleteUser
GET /getAllPosts
POST /sendEmail
```

**Good: Resources with HTTP verbs**
```
POST   /users           # Create user
GET    /users/123       # Get user
PUT    /users/123       # Replace user
PATCH  /users/123       # Update user
DELETE /users/123       # Delete user
GET    /users           # List users
POST   /emails          # Send email (email is the resource)
```

### Plural Resource Names

Use plural nouns consistently, even for single items.

```
GET  /users         # List of users
GET  /users/123     # Single user
POST /orders        # Create order
GET  /orders/456    # Single order
```

**Why plural?** Consistency. `/users/123` reads as "user 123 from the users collection."

### Resource Hierarchy

Express relationships through URL structure:

```
# User's orders
GET /users/123/orders

# Order's items
GET /orders/456/items

# Specific item in order
GET /orders/456/items/789

# Organization structure
GET /organizations/acme/teams
GET /organizations/acme/teams/engineering/members
```

**Guidelines:**
- Maximum 2-3 levels of nesting
- If deeper, use query parameters or separate endpoints
- Nested resource should "belong to" parent

```
# Too deeply nested - avoid
GET /organizations/acme/teams/engineering/projects/website/tasks/123/comments

# Better - flatten or use query params
GET /tasks/123/comments
GET /comments?task_id=123
```

### Resource Naming Conventions

| Convention | Example | When to Use |
|------------|---------|-------------|
| Lowercase | `/users`, `/orders` | Always |
| Hyphens for multi-word | `/order-items`, `/user-profiles` | Compound nouns |
| No trailing slashes | `/users` not `/users/` | Always |
| No file extensions | `/users` not `/users.json` | Always |

---

## 2. HTTP Methods

### Method Semantics

| Method | Purpose | Idempotent | Safe | Body |
|--------|---------|------------|------|------|
| GET | Retrieve resource(s) | Yes | Yes | No |
| POST | Create resource | No | No | Yes |
| PUT | Replace resource | Yes | No | Yes |
| PATCH | Partial update | No | No | Yes |
| DELETE | Remove resource | Yes | No | Optional |
| HEAD | Get headers only | Yes | Yes | No |
| OPTIONS | Get capabilities | Yes | Yes | No |

**Idempotent:** Multiple identical requests have same effect as single request
**Safe:** No side effects, read-only

### GET - Retrieve Resources

```python
# Get single resource
@app.get("/users/{user_id}")
async def get_user(user_id: UUID) -> UserResponse:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return UserResponse.from_orm(user)

# List resources with filtering
@app.get("/users")
async def list_users(
    status: Optional[str] = None,
    role: Optional[str] = None,
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0)
) -> PaginatedResponse[UserResponse]:
    query = select(User)
    if status:
        query = query.where(User.status == status)
    if role:
        query = query.where(User.role == role)

    users = await db.execute(query.limit(limit).offset(offset))
    total = await db.count(query)

    return PaginatedResponse(
        data=[UserResponse.from_orm(u) for u in users],
        pagination=Pagination(limit=limit, offset=offset, total=total)
    )
```

### POST - Create Resources

```python
@app.post("/users", status_code=201)
async def create_user(
    request: CreateUserRequest,
    response: Response
) -> UserResponse:
    user = User(**request.dict())
    await db.add(user)

    # Include Location header pointing to new resource
    response.headers["Location"] = f"/users/{user.id}"

    return UserResponse.from_orm(user)
```

### PUT - Replace Resources

PUT replaces the entire resource. Missing fields become null/default.

```python
@app.put("/users/{user_id}")
async def replace_user(
    user_id: UUID,
    request: ReplaceUserRequest
) -> UserResponse:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Replace all fields
    for field, value in request.dict().items():
        setattr(user, field, value)

    await db.commit()
    return UserResponse.from_orm(user)
```

### PATCH - Partial Update

PATCH updates only provided fields.

```python
@app.patch("/users/{user_id}")
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest
) -> UserResponse:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Update only provided fields
    update_data = request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    return UserResponse.from_orm(user)
```

### DELETE - Remove Resources

```python
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: UUID):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    await db.delete(user)
    # 204 No Content - no response body
```

---

## 3. HTTP Status Codes

### Success Codes (2xx)

| Code | Name | When to Use |
|------|------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that creates resource |
| 202 | Accepted | Request accepted for async processing |
| 204 | No Content | Successful DELETE (no body) |

### Client Error Codes (4xx)

| Code | Name | When to Use |
|------|------|-------------|
| 400 | Bad Request | Invalid syntax, failed validation |
| 401 | Unauthorized | Authentication required/failed |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | Wrong HTTP method |
| 409 | Conflict | State conflict (duplicate, etc.) |
| 422 | Unprocessable Entity | Semantic validation error |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Error Codes (5xx)

| Code | Name | When to Use |
|------|------|-------------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service error |
| 503 | Service Unavailable | Temporarily unavailable |
| 504 | Gateway Timeout | Upstream timeout |

### Code Selection Guide

```
Is the request malformed?
├── Yes → 400 Bad Request
└── No → Is authentication required?
    ├── Missing/invalid credentials → 401 Unauthorized
    └── Authenticated → Is user authorized?
        ├── No → 403 Forbidden
        └── Yes → Does resource exist?
            ├── No → 404 Not Found
            └── Yes → Is there a conflict?
                ├── Yes → 409 Conflict
                └── No → Process request
                    ├── Success → 200/201/204
                    └── Server error → 500
```

---

## 4. Request/Response Design

### Consistent Response Structure

**Single resource:**
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-01-17T10:30:00Z"
}
```

**Collection:**
```json
{
  "data": [
    {"id": "user_123", "name": "John"},
    {"id": "user_456", "name": "Jane"}
  ],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

**Error:**
```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "request_id": "req_abc123"
  }
}
```

### Field Naming

Use consistent case (snake_case or camelCase) throughout:

```json
{
  "user_id": "123",
  "first_name": "John",
  "created_at": "2026-01-17T10:30:00Z",
  "is_active": true
}
```

### Date/Time Format

Always use ISO 8601 with timezone:

```json
{
  "created_at": "2026-01-17T10:30:00Z",
  "updated_at": "2026-01-17T15:45:30.123Z",
  "expires_at": "2026-02-17T10:30:00+00:00"
}
```

### Null vs Absent Fields

Be consistent. Either:
- Include null fields explicitly
- Omit null fields entirely

```json
// Option 1: Include nulls
{
  "name": "John",
  "nickname": null,
  "avatar_url": null
}

// Option 2: Omit nulls (smaller payload)
{
  "name": "John"
}
```

---

## 5. Pagination

### Offset-Based Pagination

Simple but has issues with changing data:

```
GET /users?limit=20&offset=40

Response:
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 543,
    "has_more": true
  }
}
```

**Pros:** Easy to implement, supports page jumping
**Cons:** Performance degrades at high offsets, inconsistent with data changes

### Cursor-Based Pagination

More robust for dynamic data:

```
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ

Response:
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTQzfQ",
    "prev_cursor": "eyJpZCI6MTAzfQ",
    "has_more": true
  }
}
```

**Implementation:**
```python
def encode_cursor(last_item) -> str:
    cursor_data = {"id": str(last_item.id), "created_at": last_item.created_at.isoformat()}
    return base64.urlsafe_b64encode(json.dumps(cursor_data).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())

@app.get("/users")
async def list_users(
    limit: int = Query(default=20, le=100),
    cursor: Optional[str] = None
) -> CursorPaginatedResponse:
    query = select(User).order_by(User.created_at.desc(), User.id.desc())

    if cursor:
        cursor_data = decode_cursor(cursor)
        query = query.where(
            or_(
                User.created_at < cursor_data["created_at"],
                and_(
                    User.created_at == cursor_data["created_at"],
                    User.id < cursor_data["id"]
                )
            )
        )

    users = await db.execute(query.limit(limit + 1))  # Fetch one extra

    has_more = len(users) > limit
    users = users[:limit]

    return CursorPaginatedResponse(
        data=users,
        pagination=CursorPagination(
            next_cursor=encode_cursor(users[-1]) if has_more else None,
            has_more=has_more
        )
    )
```

---

## 6. Filtering and Sorting

### Query Parameters for Filtering

```
# Simple equality
GET /users?status=active

# Multiple values (OR)
GET /users?status=active,pending

# Range filters
GET /orders?created_after=2026-01-01&created_before=2026-12-31
GET /products?price_min=10&price_max=100

# Boolean filters
GET /users?is_verified=true

# Text search
GET /products?q=laptop
```

### Sorting

```
# Single field
GET /users?sort=created_at        # Ascending
GET /users?sort=-created_at       # Descending (prefix with -)

# Multiple fields
GET /users?sort=-created_at,name  # Primary: created_at desc, Secondary: name asc
```

**Implementation:**
```python
@app.get("/users")
async def list_users(
    sort: str = Query(default="-created_at"),
    status: Optional[str] = None
) -> PaginatedResponse:
    query = select(User)

    # Apply filters
    if status:
        query = query.where(User.status == status)

    # Apply sorting
    for field in sort.split(","):
        descending = field.startswith("-")
        field_name = field.lstrip("-")

        if hasattr(User, field_name):
            column = getattr(User, field_name)
            query = query.order_by(column.desc() if descending else column.asc())

    return await execute_paginated(query)
```

### Field Selection

Let clients request only needed fields:

```
GET /users/123?fields=id,name,email
```

```python
@app.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    fields: Optional[str] = None
) -> dict:
    user = await db.get(User, user_id)

    if fields:
        requested_fields = fields.split(",")
        return {k: v for k, v in user.dict().items() if k in requested_fields}

    return user.dict()
```

---

## 7. Versioning

### When to Version

Version when making **breaking changes**:
- Removing fields or endpoints
- Renaming fields
- Changing field types
- Changing response structure

**Non-breaking changes** (no version needed):
- Adding new optional fields
- Adding new endpoints
- Adding new optional parameters

### URI Versioning (Recommended)

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

**Implementation:**
```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: UUID):
    return {"user_id": user_id, "full_name": "John Doe"}  # Old field name

@v2_router.get("/users/{user_id}")
async def get_user_v2(user_id: UUID):
    return {"user_id": user_id, "name": "John Doe"}  # New field name

app.include_router(v1_router)
app.include_router(v2_router)
```

### Deprecation

Communicate deprecation clearly:

```python
@app.get("/v1/users/{user_id}")
async def get_user_v1(user_id: UUID, response: Response):
    # Add deprecation headers
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Sat, 31 Dec 2026 23:59:59 GMT"
    response.headers["Link"] = '</v2/users>; rel="successor-version"'

    return user
```

---

## 8. Error Handling

### Error Response Format

```python
from pydantic import BaseModel
from typing import List, Optional

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    code: str

class ErrorResponse(BaseModel):
    code: str
    message: str
    details: List[ErrorDetail] = []
    request_id: str
    docs_url: Optional[str] = None

# Usage
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            code="validation_error",
            message="Request validation failed",
            details=[
                ErrorDetail(field=e["loc"][-1], message=e["msg"], code="invalid")
                for e in exc.errors()
            ],
            request_id=request.state.request_id,
            docs_url="https://api.example.com/docs/errors#validation_error"
        ).dict()
    )
```

### Consistent Error Codes

```python
ERROR_CODES = {
    # Authentication
    "auth_required": "Authentication required",
    "auth_invalid": "Invalid credentials",
    "auth_expired": "Token expired",

    # Authorization
    "forbidden": "Not authorized for this resource",

    # Validation
    "validation_error": "Request validation failed",
    "invalid_format": "Invalid field format",
    "required_field": "Required field missing",

    # Resources
    "not_found": "Resource not found",
    "already_exists": "Resource already exists",
    "conflict": "Resource conflict",

    # Rate limiting
    "rate_limited": "Rate limit exceeded",
}
```

---

## 9. Security Considerations

### Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = await db.get(User, payload["sub"])
        if not user:
            raise HTTPException(401, "User not found")
        return user
    except JWTError:
        raise HTTPException(401, "Invalid token")

@app.get("/users/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/users")
@limiter.limit("100/minute")
async def list_users(request: Request):
    return users

# Include rate limit headers in response
@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset_time)
    return response
```

### Input Validation

```python
from pydantic import BaseModel, Field, validator

class CreateUserRequest(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=12)
    name: str = Field(..., min_length=1, max_length=100)

    @validator("email")
    def validate_email(cls, v):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
            raise ValueError("Invalid email format")
        return v.lower()

    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v
```

---

## 10. Documentation

### OpenAPI/Swagger

```python
from fastapi import FastAPI, Path, Query

app = FastAPI(
    title="My API",
    description="API for managing users and orders",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a single user by their unique identifier",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
async def get_user(
    user_id: UUID = Path(..., description="Unique user identifier"),
    include_orders: bool = Query(False, description="Include user's orders")
):
    """
    Get a user by ID.

    - **user_id**: The unique identifier for the user
    - **include_orders**: Whether to include the user's order history
    """
    pass
```

### Response Examples

```python
class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "user_123",
                "email": "john@example.com",
                "name": "John Doe",
                "created_at": "2026-01-17T10:30:00Z"
            }
        }
```

---

## Quick Reference: REST API Checklist

### Resource Design
- [ ] Resources are nouns (plural)
- [ ] No verbs in URLs
- [ ] Consistent naming conventions
- [ ] Maximum 2-3 levels of nesting

### HTTP Methods
- [ ] GET for retrieval (safe, idempotent)
- [ ] POST for creation
- [ ] PUT for full replacement (idempotent)
- [ ] PATCH for partial update
- [ ] DELETE for removal (idempotent)

### Status Codes
- [ ] 200 for successful GET/PUT/PATCH
- [ ] 201 for successful POST (with Location header)
- [ ] 204 for successful DELETE
- [ ] 400 for bad requests
- [ ] 401 for unauthenticated
- [ ] 403 for unauthorized
- [ ] 404 for not found
- [ ] 422 for validation errors
- [ ] 429 for rate limiting

### Response Design
- [ ] Consistent structure across endpoints
- [ ] Proper date/time formatting (ISO 8601)
- [ ] Consistent field naming
- [ ] Informative error responses

### Features
- [ ] Pagination implemented
- [ ] Filtering and sorting available
- [ ] Rate limiting in place
- [ ] API versioning strategy
- [ ] OpenAPI documentation

---

Great REST API design is about consistency and predictability. When developers can intuit how your API works, they're productive immediately. Make the common case easy, handle edge cases gracefully, and document everything.


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

