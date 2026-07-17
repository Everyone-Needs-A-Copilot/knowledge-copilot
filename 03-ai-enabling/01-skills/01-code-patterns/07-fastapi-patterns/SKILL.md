---
last_updated: 2026-02-25
status: active
name: fastapi-patterns
description: FastAPI patterns - dependency injection, Pydantic models, async endpoints, middleware. Use when building FastAPI APIs.
triggers:
  files: ["**/routes/**/*.py", "**/api/**/*.py", "**/main.py", "**/dependencies.py"]
  keywords: ["fastapi", "pydantic", "dependency injection", "Depends", "APIRouter", "HTTPException", "BackgroundTasks", "middleware"]
allowed-tools: Read, Write, Edit
---

# FastAPI Patterns: Deep Expertise Skill

## Overview

This skill provides comprehensive guidance on building production-grade FastAPI applications with modern Python async patterns, dependency injection, Pydantic validation, and SQLAlchemy async ORM integration.

**When to use this skill:**
- Building FastAPI REST APIs
- Designing API routes and endpoints
- Implementing dependency injection patterns
- Creating Pydantic schemas for request/response validation
- Integrating async database access with SQLAlchemy
- Setting up middleware and authentication
- Managing background tasks
- Testing FastAPI applications

**Core Philosophy:** FastAPI emphasizes type safety, automatic documentation, dependency injection, and async-first design. All patterns should leverage Python's type hints for automatic validation and OpenAPI schema generation.

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## Table of Contents

1. [Application Setup](#application-setup)
2. [Router Organization](#router-organization)
3. [Dependency Injection](#dependency-injection)
4. [Request & Response Models](#request--response-models)
5. [Authentication & Authorization](#authentication--authorization)
6. [Database Integration](#database-integration)
7. [Background Tasks](#background-tasks)
8. [Middleware](#middleware)
9. [Error Handling](#error-handling)
10. [OpenAPI Customization](#openapi-customization)
11. [Testing FastAPI Apps](#testing-fastapi-apps)
12. [Performance Patterns](#performance-patterns)
13. [Security Best Practices](#security-best-practices)

---

## Application Setup

### Main Application Structure

**✅ Good: Lifespan events with structured setup**
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import structlog

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events for startup/shutdown.

    Use for:
    - Database connection pooling
    - Cache initialization
    - External service connections
    - Cleanup on shutdown
    """
    # Startup
    logger.info("application_starting", environment=settings.node_env)

    # Initialize database
    try:
        from app.db.database import init_db
        await init_db()
        logger.info("database_initialized")
    except Exception as e:
        logger.error("database_init_failed", error=str(e))
        # Don't crash - may already exist or use migrations

    yield  # Application runs here

    # Shutdown
    logger.info("application_shutdown")

    # Close connections
    try:
        from app.db.database import close_db
        await close_db()
        logger.info("database_closed")
    except Exception as e:
        logger.error("database_close_failed", error=str(e))


# Create application with comprehensive metadata
app = FastAPI(
    title="My API",
    description="API for awesome things",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=openapi_tags,  # Organize endpoints in docs
    lifespan=lifespan
)
```

**❌ Bad: No lifecycle management**
```python
# Don't do this - no cleanup, no initialization
app = FastAPI()

# Database connection created at module level (BAD)
engine = create_engine(DATABASE_URL)
```

### OpenAPI Tags for Documentation

**✅ Good: Organized API documentation**
```python
openapi_tags = [
    {
        "name": "Authentication",
        "description": "User authentication and token management",
    },
    {
        "name": "Topics",
        "description": "Topic CRUD operations with evidence management",
    },
    {
        "name": "Background Jobs",
        "description": "Long-running async operations",
    },
]

app = FastAPI(openapi_tags=openapi_tags)

# In routes
@router.get("/topics", tags=["Topics"])
async def list_topics():
    """List all topics (appears under Topics in docs)"""
    pass
```

---

## Router Organization

### APIRouter for Modular Routes

**✅ Good: Organized router structure**
```python
# app/api/routes/topics.py
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
import structlog

logger = structlog.get_logger(__name__)

# Define router with prefix and tags
router = APIRouter(
    prefix="/api/topics",
    tags=["Topics"],
    responses={404: {"description": "Not found"}},  # Common responses
)


# Route handlers with clear patterns
@router.get("/", response_model=List[TopicResponse])
async def list_topics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> List[TopicResponse]:
    """
    List all topics for authenticated user.

    Query Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum records to return

    Returns:
        List of topic objects
    """
    stmt = (
        select(TLTopic)
        .where(TLTopic.user_id == user.id)
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    topics = result.scalars().all()

    logger.info("topics_listed", user_id=str(user.id), count=len(topics))
    return [TopicResponse.from_orm(t) for t in topics]


@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_data: TopicCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TopicResponse:
    """
    Create a new topic.

    Requires authentication. Topic is created for the authenticated user.
    """
    topic = TLTopic(
        **topic_data.dict(),
        user_id=user.id
    )

    session.add(topic)
    await session.commit()
    await session.refresh(topic)

    logger.info("topic_created", topic_id=str(topic.id), user_id=str(user.id))
    return TopicResponse.from_orm(topic)


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TopicResponse:
    """Get topic by ID"""
    stmt = select(TLTopic).where(
        TLTopic.id == topic_id,
        TLTopic.user_id == user.id  # Security: only user's topics
    )
    result = await session.execute(stmt)
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {topic_id} not found"
        )

    return TopicResponse.from_orm(topic)


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(
    topic_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete topic by ID"""
    stmt = select(TLTopic).where(
        TLTopic.id == topic_id,
        TLTopic.user_id == user.id
    )
    result = await session.execute(stmt)
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {topic_id} not found"
        )

    await session.delete(topic)
    await session.commit()

    logger.info("topic_deleted", topic_id=str(topic_id), user_id=str(user.id))
    return None  # 204 No Content
```

**❌ Bad: Flat structure without organization**
```python
# Don't do this - all routes in main.py
@app.get("/topics")
def list_topics():
    pass

@app.get("/users")
def list_users():
    pass

@app.get("/reports")
def list_reports():
    pass
```

### Including Routers in Main App

**✅ Good: Clean router registration**
```python
# app/main.py
from app.api.routes import topics, users, reports

# Include routers
app.include_router(topics.router)
app.include_router(users.router)
app.include_router(reports.router)

# Or with additional prefix/tags
app.include_router(
    topics.router,
    prefix="/admin",  # Routes now under /admin/api/topics
    tags=["Admin Operations"]
)
```

---

## Dependency Injection

Dependency injection is FastAPI's superpower. Use it for:
- Database sessions
- Authentication
- Configuration
- Shared business logic
- Rate limiting
- Caching

### Database Session Dependency

**✅ Good: Async session with context manager**
```python
# app/db/database.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.

    Usage:
        async with get_session() as session:
            result = await session.execute(query)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Usage in routes
@router.get("/topics")
async def list_topics(
    session: AsyncSession = Depends(get_session)  # Auto-injected
):
    """Session automatically managed - commit/rollback/close"""
    result = await session.execute(select(TLTopic))
    return result.scalars().all()
```

### Authentication Dependencies

**✅ Good: Layered authentication dependencies**
```python
# app/core/auth.py
from fastapi import Depends, Header, HTTPException, status
from jose import jwt, JWTError
import structlog

logger = structlog.get_logger(__name__)


async def get_current_user(
    authorization: str = Header(None, alias="Authorization")
) -> User:
    """
    Validate token and return authenticated user.

    Raises:
        HTTPException 401: Missing or invalid token
        HTTPException 403: Domain not authorized
    """
    if not authorization:
        logger.warning("auth_failed", reason="missing_header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        logger.warning("auth_failed", reason="invalid_format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header"
        )

    # Verify token (JWT, OAuth, etc.)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Get user from database
    async with get_session() as session:
        user = await user_service.get_user_by_id(UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        logger.info("user_authenticated", user_id=str(user.id))
        return user


async def require_admin(user: User = Depends(get_current_user)) -> User:
    """
    Dependency that requires admin role.

    Raises:
        HTTPException 403: User is not admin
    """
    if not user.is_admin():
        logger.warning(
            "admin_access_denied",
            user_id=str(user.id),
            role=user.role
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user


class RequireRole:
    """
    Configurable role-based access control dependency.

    Example:
        require_staff = RequireRole(roles=["admin", "staff"])

        @router.get("/reports")
        async def get_reports(user: User = Depends(require_staff)):
            ...
    """

    def __init__(self, roles: list[str]):
        if not roles:
            raise ValueError("At least one role must be specified")
        self.roles = roles

    async def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.role not in self.roles:
            logger.warning(
                "role_access_denied",
                user_id=str(user.id),
                user_role=user.role,
                required_roles=self.roles
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of: {', '.join(self.roles)}"
            )
        return user


# Usage in routes
@router.get("/topics")
async def list_topics(
    user: User = Depends(get_current_user)  # Any authenticated user
):
    """List user's topics"""
    pass


@router.delete("/topics/{topic_id}")
async def delete_topic(
    topic_id: UUID,
    user: User = Depends(require_admin)  # Admin only
):
    """Delete any topic (admin only)"""
    pass


require_moderator = RequireRole(roles=["admin", "moderator"])

@router.put("/topics/{topic_id}/approve")
async def approve_topic(
    topic_id: UUID,
    user: User = Depends(require_moderator)  # Admin or moderator
):
    """Approve topic for publication"""
    pass
```

### Service Dependencies

**✅ Good: Inject service instances**
```python
# app/services/topic_service.py
class TopicService:
    """Service for topic operations"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = structlog.get_logger(__name__)

    async def list_topics(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[TLTopic]:
        """List topics for user"""
        stmt = (
            select(TLTopic)
            .where(TLTopic.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


def get_topic_service(
    session: AsyncSession = Depends(get_session)
) -> TopicService:
    """Dependency provider for TopicService"""
    return TopicService(session=session)


# Usage in routes
@router.get("/topics")
async def list_topics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user: User = Depends(get_current_user),
    topic_service: TopicService = Depends(get_topic_service)
) -> List[TopicResponse]:
    """List topics using injected service"""
    topics = await topic_service.list_topics(
        user_id=user.id,
        skip=skip,
        limit=limit
    )
    return [TopicResponse.from_orm(t) for t in topics]
```

### Dependency Chains

**✅ Good: Dependencies can depend on other dependencies**
```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)  # Nested dependency
) -> User:
    """Get authenticated user (depends on session)"""
    # Validate token...
    user = await session.get(User, user_id)
    return user


async def get_topic_with_auth(
    topic_id: UUID,
    user: User = Depends(get_current_user),  # Depends on user
    session: AsyncSession = Depends(get_session)
) -> TLTopic:
    """Get topic and verify user owns it"""
    stmt = select(TLTopic).where(
        TLTopic.id == topic_id,
        TLTopic.user_id == user.id
    )
    result = await session.execute(stmt)
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    return topic


# Usage - both dependencies resolved automatically
@router.put("/topics/{topic_id}")
async def update_topic(
    topic_data: TopicUpdate,
    topic: TLTopic = Depends(get_topic_with_auth)  # Auto-validates ownership
):
    """Update topic (ownership verified by dependency)"""
    for field, value in topic_data.dict(exclude_unset=True).items():
        setattr(topic, field, value)

    await session.commit()
    return TopicResponse.from_orm(topic)
```

---

## Request & Response Models

### Pydantic Models for Validation

**✅ Good: Comprehensive Pydantic schemas**
```python
from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class TopicBase(BaseModel):
    """Base topic fields (shared between Create/Update)"""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    tags: List[str] = Field(default_factory=list, max_items=20)

    @validator('title')
    def title_not_empty(cls, v):
        """Ensure title is not just whitespace"""
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('tags')
    def tags_lowercase(cls, v):
        """Normalize tags to lowercase"""
        return [tag.lower().strip() for tag in v if tag.strip()]


class TopicCreate(TopicBase):
    """Schema for creating a topic"""
    source: str = Field("manual", regex="^(manual|ai_generated|imported)$")


class TopicUpdate(TopicBase):
    """Schema for updating a topic (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)

    model_config = ConfigDict(
        # Allow partial updates
        extra='forbid'  # Reject unknown fields
    )


class TopicResponse(TopicBase):
    """Schema for topic API responses"""
    id: UUID
    source: str
    status: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    # Include related data
    concepts_count: int = 0
    evidence_count: int = 0

    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode (was orm_mode in v1)
        json_encoders={
            UUID: str,
            datetime: lambda v: v.isoformat()
        },
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "AI in Healthcare",
                "description": "Strategic insights on AI adoption in healthcare",
                "tags": ["ai", "healthcare", "strategy"],
                "source": "manual",
                "status": "active",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "concepts_count": 5,
                "evidence_count": 23
            }
        }
    )


class TopicListResponse(BaseModel):
    """Paginated list response"""
    items: List[TopicResponse]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(from_attributes=True)


# Usage in routes
@router.post("/topics", response_model=TopicResponse)
async def create_topic(
    topic_data: TopicCreate,  # Auto-validated
    user: User = Depends(get_current_user)
):
    """
    Create topic - validation automatic:
    - title: required, 1-500 chars
    - tags: max 20, normalized to lowercase
    - source: must be one of allowed values
    """
    # topic_data is guaranteed valid here
    pass
```

### Request Body with Examples

**✅ Good: Request body with OpenAPI examples**
```python
from pydantic import BaseModel, Field


class ConceptCreate(BaseModel):
    """Schema for creating a concept"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Concept title",
        examples=["The Rise of AI-Powered Decision Making"]
    )
    content: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Detailed concept explanation",
        examples=["Organizations are increasingly leveraging AI..."]
    )
    confidence_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="AI confidence score",
        examples=[0.85]
    )


@router.post("/concepts")
async def create_concept(
    concept: ConceptCreate = Body(
        ...,
        openapi_examples={
            "normal": {
                "summary": "A typical concept",
                "description": "Standard concept with moderate confidence",
                "value": {
                    "title": "AI in Healthcare",
                    "content": "Healthcare organizations are adopting AI for diagnostics...",
                    "confidence_score": 0.75
                }
            },
            "high_confidence": {
                "summary": "High confidence concept",
                "description": "Concept with strong evidence backing",
                "value": {
                    "title": "Cloud Migration Trends",
                    "content": "95% of enterprises have adopted cloud infrastructure...",
                    "confidence_score": 0.95
                }
            }
        }
    )
):
    """Create concept with documented examples"""
    pass
```

### Response Models with Status Codes

**✅ Good: Multiple response models per endpoint**
```python
from fastapi import Response


@router.post(
    "/topics",
    response_model=TopicResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Topic created successfully",
            "model": TopicResponse
        },
        400: {
            "description": "Invalid input",
            "model": ErrorResponse
        },
        401: {
            "description": "Not authenticated",
            "model": ErrorResponse
        },
        409: {
            "description": "Topic already exists",
            "model": ErrorResponse
        }
    }
)
async def create_topic(
    topic_data: TopicCreate,
    user: User = Depends(get_current_user)
) -> TopicResponse:
    """
    Create new topic.

    Returns 201 with created topic.
    """
    # Check for duplicates
    existing = await check_duplicate(topic_data.title, user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Topic with this title already exists"
        )

    topic = await create_topic_in_db(topic_data, user.id)
    return TopicResponse.from_orm(topic)
```

### File Upload

**✅ Good: File upload with validation**
```python
from fastapi import File, UploadFile


@router.post("/topics/{topic_id}/upload-evidence")
async def upload_evidence(
    topic_id: UUID,
    file: UploadFile = File(
        ...,
        description="Evidence file (PDF, DOCX, TXT)",
        max_length=10_000_000  # 10MB
    ),
    user: User = Depends(get_current_user)
):
    """
    Upload evidence file for topic.

    Accepts: PDF, DOCX, TXT
    Max size: 10MB
    """
    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: PDF, DOCX, TXT"
        )

    # Read file
    contents = await file.read()

    # Validate size
    if len(contents) > 10_000_000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Max size: 10MB"
        )

    # Process file...
    logger.info(
        "evidence_uploaded",
        topic_id=str(topic_id),
        filename=file.filename,
        size=len(contents),
        content_type=file.content_type
    )

    return {"filename": file.filename, "size": len(contents)}
```

---

## Authentication & Authorization

### Token-Based Authentication

**✅ Good: OAuth2 with Bearer tokens**
```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "topics:read": "Read topics",
        "topics:write": "Create and update topics",
        "admin": "Admin access"
    }
)


@router.post("/auth/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token endpoint.

    Returns access token on successful authentication.
    """
    # Validate credentials
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create token
    access_token = create_access_token(
        data={"sub": str(user.id), "scopes": form_data.scopes}
    )

    logger.info("user_logged_in", user_id=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    """Extract and validate user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(UUID(user_id))
    if user is None:
        raise credentials_exception

    return user
```

### Google OAuth Integration

**✅ Good: Google ID token verification**
```python
from jose import jwt, jwk
from jose.utils import base64url_decode
import httpx

GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"


class GoogleTokenVerifier:
    """Verify Google ID tokens locally"""

    def __init__(self, audience: str, jwks_url: str = GOOGLE_JWKS_URL):
        if not audience:
            raise ValueError("Google OAuth client ID required")
        self._audience = audience
        self._jwks_url = jwks_url
        self._jwks: Dict[str, Dict[str, Any]] = {}
        self._expires_at = 0.0
        self._lock = asyncio.Lock()

    async def _refresh_keys(self) -> None:
        """Fetch and cache Google's public keys"""
        async with self._lock:
            now = time.time()
            if self._jwks and now < self._expires_at:
                return

            async with httpx.AsyncClient() as client:
                response = await client.get(self._jwks_url, timeout=5.0)
                response.raise_for_status()
                payload = response.json()
                keys = payload.get("keys", [])
                self._jwks = {k["kid"]: k for k in keys if "kid" in k}

                # Parse cache TTL from Cache-Control header
                cache_control = response.headers.get("cache-control", "")
                ttl = 300  # Default 5 minutes
                if "max-age" in cache_control:
                    try:
                        ttl = int(cache_control.split("max-age=")[1].split(",")[0])
                    except (ValueError, IndexError):
                        ttl = 300

                self._expires_at = now + ttl
                logger.info("google_jwks_refreshed", keys=len(self._jwks), ttl=ttl)

    async def verify(self, token: str) -> Dict[str, Any]:
        """Verify Google ID token"""
        # Get token header
        try:
            header = jwt.get_unverified_header(token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token header"
            )

        # Get public key
        await self._refresh_keys()
        key_dict = self._jwks.get(header.get("kid"))
        if not key_dict:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unknown signing key"
            )

        # Verify signature
        algorithm = header.get("alg", "RS256")
        public_key = jwk.construct(key_dict, algorithm=algorithm)
        message, encoded_signature = token.rsplit(".", 1)
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))

        if not public_key.verify(message.encode("utf-8"), decoded_signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid signature"
            )

        # Verify claims
        claims = jwt.get_unverified_claims(token)
        now = time.time()

        # Check expiration
        exp = claims.get("exp")
        if exp and now > float(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        # Check audience
        aud = claims.get("aud")
        audiences = [aud] if isinstance(aud, str) else (aud or [])
        if self._audience not in audiences:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid audience"
            )

        # Check issuer
        issuer = claims.get("iss")
        if issuer not in {"https://accounts.google.com", "accounts.google.com"}:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid issuer"
            )

        return claims


# Usage
verifier = GoogleTokenVerifier(audience=settings.google_oauth_client_id)


async def get_current_user_google(
    authorization: str = Header(None, alias="Authorization")
) -> User:
    """Authenticate user via Google ID token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header"
        )

    # Verify Google token
    claims = await verifier.verify(token)

    email = claims.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email claim missing"
        )

    # Get or create user
    async with get_session() as session:
        user = await get_or_create_user(
            session=session,
            email=email,
            name=claims.get("name"),
            picture=claims.get("picture")
        )
        return user
```

### User Impersonation (Admin Feature)

**✅ Good: Secure impersonation for admin debugging**
```python
async def get_effective_user(
    request: Request,
    user: User = Depends(get_current_user),
    x_impersonate_user_id: Optional[str] = Header(None, alias="X-Impersonate-User-Id")
) -> User:
    """
    Get effective user (current or impersonated).

    Allows admins to impersonate users for debugging.
    All impersonation events logged for audit trail.
    """
    # No impersonation - return current user
    if not x_impersonate_user_id:
        return user

    # Validate admin privileges
    if not user.is_admin():
        logger.warning(
            "impersonation_denied_not_admin",
            admin_user_id=str(user.id),
            target_user_id=x_impersonate_user_id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can impersonate users"
        )

    # Validate UUID format
    try:
        target_user_id = UUID(x_impersonate_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {x_impersonate_user_id}"
        )

    # Prevent self-impersonation
    if target_user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot impersonate yourself"
        )

    # Fetch target user
    async with get_session() as session:
        target_user = await get_user_by_id(session, target_user_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found: {target_user_id}"
            )

    # Log impersonation event (AUDIT TRAIL)
    logger.info(
        "impersonation_active",
        admin_id=str(user.id),
        admin_email=user.email,
        target_user_id=str(target_user.id),
        target_email=target_user.email,
        path=request.url.path,
        method=request.method,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

    return target_user


# Usage
@router.get("/topics")
async def list_topics(
    user: User = Depends(get_effective_user)  # May be impersonated
):
    """
    List topics for user.

    Admins can impersonate by sending:
    X-Impersonate-User-Id: <user_id>
    """
    # user is either authenticated user or impersonated user
    topics = await get_topics_for_user(user.id)
    return topics
```

---

## Database Integration

### Async SQLAlchemy Session

**✅ Good: Async session management**
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload, joinedload

# Create engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Query Patterns (SQLAlchemy 2.0)

**✅ Good: Modern SQLAlchemy 2.0 select syntax**
```python
# Simple query
stmt = select(TLTopic).where(TLTopic.status == "active")
result = await session.execute(stmt)
topics = result.scalars().all()

# Complex filtering
stmt = (
    select(TLEvidence)
    .where(
        and_(
            TLEvidence.topic_id == topic_id,
            TLEvidence.verification_status.in_(["verified", "pending"]),
            TLEvidence.credibility_score >= 0.7
        )
    )
    .order_by(TLEvidence.created_at.desc())
    .limit(50)
)

# Aggregation
stmt = (
    select(
        TLTopic.status,
        func.count(TLTopic.id).label("count")
    )
    .group_by(TLTopic.status)
)
result = await session.execute(stmt)
counts = {row.status: row.count for row in result}

# Join with relationships
stmt = (
    select(TLTopic)
    .join(TLConcept)
    .where(TLConcept.status == "approved")
    .distinct()
)
```

**❌ Bad: Legacy query API (SQLAlchemy 1.x)**
```python
# Don't use this
topics = session.query(TLTopic).filter_by(status="active").all()
```

### Eager Loading (Prevent N+1)

**✅ Good: Eager load relationships**
```python
from sqlalchemy.orm import selectinload, joinedload

# selectinload: Separate query (good for collections)
stmt = (
    select(TLTopic)
    .options(selectinload(TLTopic.concepts))
    .where(TLTopic.id == topic_id)
)
result = await session.execute(stmt)
topic = result.scalar_one_or_none()

# Access concepts without additional query
for concept in topic.concepts:
    print(concept.title)

# joinedload: Single query with JOIN (good for single relationships)
stmt = (
    select(TLConcept)
    .options(joinedload(TLConcept.topic))
    .where(TLConcept.id == concept_id)
)

# Multiple relationships
stmt = (
    select(TLTopic)
    .options(
        selectinload(TLTopic.concepts),
        selectinload(TLTopic.evidence_items)
    )
)
```

**❌ Bad: Lazy loading in loop (N+1 problem)**
```python
# Don't do this
topics = await session.execute(select(TLTopic))
for topic in topics.scalars():
    # Each access triggers a new query!
    print(topic.concepts)  # Query 1, 2, 3, ...
```

### Transactions

**✅ Good: Explicit transaction management**
```python
async def create_topic_with_concepts(
    topic_data: TopicCreate,
    concepts_data: List[ConceptCreate],
    session: AsyncSession
) -> TLTopic:
    """Create topic and concepts atomically"""
    # All within single transaction
    topic = TLTopic(**topic_data.dict())
    session.add(topic)
    await session.flush()  # Get topic.id without committing

    # Create concepts
    concepts = [
        TLConcept(**c.dict(), topic_id=topic.id)
        for c in concepts_data
    ]
    session.add_all(concepts)

    # Commit atomically (done by context manager)
    await session.commit()
    await session.refresh(topic)

    return topic


# Usage in route
@router.post("/topics/with-concepts")
async def create_topic_with_concepts_endpoint(
    topic_data: TopicCreate,
    concepts_data: List[ConceptCreate] = Body(...),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create topic and concepts in single transaction"""
    try:
        topic = await create_topic_with_concepts(
            topic_data, concepts_data, session
        )
        return TopicResponse.from_orm(topic)
    except Exception as e:
        # Session automatically rolled back by context manager
        logger.error("topic_creation_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create topic"
        )
```

---

## Background Tasks

### FastAPI BackgroundTasks

**✅ Good: Lightweight background tasks**
```python
from fastapi import BackgroundTasks


async def send_email_notification(
    user_email: str,
    topic_id: UUID,
    action: str
):
    """Send email notification (background task)"""
    logger.info(
        "sending_email",
        email=user_email,
        topic_id=str(topic_id),
        action=action
    )

    try:
        # Send email via external service
        await email_service.send(
            to=user_email,
            subject=f"Topic {action}",
            body=f"Your topic {topic_id} has been {action}"
        )
        logger.info("email_sent", email=user_email)
    except Exception as e:
        logger.error("email_failed", email=user_email, error=str(e))


@router.post("/topics", response_model=TopicResponse)
async def create_topic(
    topic_data: TopicCreate,
    background_tasks: BackgroundTasks,  # Inject background tasks
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TopicResponse:
    """Create topic and send notification in background"""
    topic = TLTopic(**topic_data.dict(), user_id=user.id)
    session.add(topic)
    await session.commit()
    await session.refresh(topic)

    # Add background task (runs after response sent)
    background_tasks.add_task(
        send_email_notification,
        user_email=user.email,
        topic_id=topic.id,
        action="created"
    )

    return TopicResponse.from_orm(topic)
```

### Long-Running Processing

**✅ Good: Background task for long operations**
```python
async def process_evidence_background(topic_id: UUID):
    """Background: Process evidence for topic (long-running)"""
    logger.info("evidence_processing_started", topic_id=str(topic_id))

    try:
        async with get_session() as session:
            # Update status
            stmt = select(TLTopic).where(TLTopic.id == topic_id)
            result = await session.execute(stmt)
            topic = result.scalar_one_or_none()

            if not topic:
                logger.error("topic_not_found", topic_id=str(topic_id))
                return

            topic.status = "processing"
            await session.commit()

            # Long-running operation
            evidence_items = await fetch_evidence_from_sources(topic)
            concepts = await generate_concepts(evidence_items)

            # Save results
            for concept in concepts:
                session.add(concept)

            topic.status = "completed"
            await session.commit()

            logger.info(
                "evidence_processing_complete",
                topic_id=str(topic_id),
                concepts_count=len(concepts)
            )

    except Exception as e:
        logger.error(
            "evidence_processing_failed",
            topic_id=str(topic_id),
            error=str(e),
            exc_info=True
        )

        # Update status to failed
        async with get_session() as session:
            stmt = select(TLTopic).where(TLTopic.id == topic_id)
            result = await session.execute(stmt)
            topic = result.scalar_one_or_none()
            if topic:
                topic.status = "failed"
                await session.commit()


@router.post("/topics/{topic_id}/process")
async def trigger_processing(
    topic_id: UUID,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
):
    """Trigger evidence processing (async)"""
    background_tasks.add_task(process_evidence_background, topic_id)

    return {
        "message": "Processing started",
        "topic_id": str(topic_id),
        "status_url": f"/topics/{topic_id}/status"
    }


@router.get("/topics/{topic_id}/status")
async def get_processing_status(
    topic_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Check processing status"""
    stmt = select(TLTopic).where(
        TLTopic.id == topic_id,
        TLTopic.user_id == user.id
    )
    result = await session.execute(stmt)
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    return {
        "topic_id": str(topic_id),
        "status": topic.status,
        "updated_at": topic.updated_at.isoformat()
    }
```

---

## Middleware

### Custom Middleware

**✅ Good: Correlation ID middleware**
```python
import uuid
from fastapi import Request
import structlog

logger = structlog.get_logger(__name__)


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    """
    Add correlation ID to all requests for tracing.

    Uses X-Correlation-ID header if present, generates new UUID otherwise.
    """
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

    # Bind to logger context (available to all logs in this request)
    structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

    logger.info(
        "request_received",
        method=request.method,
        path=request.url.path,
        correlation_id=correlation_id
    )

    # Process request
    response = await call_next(request)

    # Add correlation ID to response headers
    response.headers["X-Correlation-ID"] = correlation_id

    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        correlation_id=correlation_id
    )

    # Clear context variables
    structlog.contextvars.clear_contextvars()

    return response
```

### Timing Middleware

**✅ Good: Request timing middleware**
```python
import time


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header with request duration"""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    logger.info(
        "request_timing",
        path=request.url.path,
        method=request.method,
        duration=process_time
    )

    return response
```

### CORS Middleware

**✅ Good: CORS with multiple origins**
```python
from fastapi.middleware.cors import CORSMiddleware

allowed_origins = [
    "https://app.example.com",
    "https://admin.example.com",
]

# In development, also allow localhost
if settings.node_env == "development":
    allowed_origins.extend([
        "http://localhost:3000",
        "http://localhost:8000",
    ])

# Deduplicate
allowed_origins = list(set(origin for origin in allowed_origins if origin))

logger.info("cors_configured", origins=allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Correlation-ID", "X-Process-Time"],
    max_age=600 if settings.node_env == "production" else 0,
)
```

---

## Error Handling

### Custom Exception Handlers

**✅ Good: Global exception handling**
```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime, timezone


class ErrorResponse(BaseModel):
    """Standard error response"""
    code: str
    message: str
    details: Dict[str, Any] = {}
    timestamp: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "TOPIC_NOT_FOUND",
                "message": "Topic not found",
                "details": {"topic_id": "550e8400-e29b-41d4-a716-446655440000"},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions (401, 403, 404, etc.)"""
    logger.warning(
        "http_exception",
        status_code=exc.status_code,
        detail=str(exc.detail),
        path=request.url.path,
        method=request.method
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=f"HTTP_{exc.status_code}",
            message=str(exc.detail) if exc.detail else "Request failed",
            details={"path": request.url.path},
            timestamp=datetime.now(timezone.utc)
        ).model_dump(mode="json")
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(
        "unhandled_exception",
        error=str(exc),
        error_type=type(exc).__name__,
        path=request.url.path,
        method=request.method,
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            code="INTERNAL_ERROR",
            message="An internal error occurred. Please try again later.",
            details={
                "error_type": type(exc).__name__,
                "path": request.url.path
            },
            timestamp=datetime.now(timezone.utc)
        ).model_dump(mode="json")
    )


# Custom exceptions
class TopicNotFoundError(Exception):
    """Raised when topic not found"""
    pass


class EvidenceGenerationError(Exception):
    """Raised when evidence generation fails"""
    pass


@app.exception_handler(TopicNotFoundError)
async def topic_not_found_handler(request: Request, exc: TopicNotFoundError):
    """Handle topic not found errors"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            code="TOPIC_NOT_FOUND",
            message=str(exc),
            details={},
            timestamp=datetime.now(timezone.utc)
        ).model_dump(mode="json")
    )
```

### Validation Error Customization

**✅ Good: Custom validation error handler**
```python
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Format validation errors consistently"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(
        "validation_error",
        path=request.url.path,
        errors=errors
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": errors},
            timestamp=datetime.now(timezone.utc)
        ).model_dump(mode="json")
    )
```

---

## OpenAPI Customization

### Custom OpenAPI Schema

**✅ Good: Add custom fields to OpenAPI**
```python
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    """Customize OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API with custom OpenAPI schema",
        routes=app.routes,
    )

    # Add custom fields
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
        "GoogleOAuth": {
            "type": "oauth2",
            "flows": {
                "implicit": {
                    "authorizationUrl": "https://accounts.google.com/o/oauth2/auth",
                    "scopes": {
                        "openid": "OpenID",
                        "email": "Email",
                        "profile": "Profile"
                    }
                }
            }
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
```

### Documentation Examples

**✅ Good: Rich examples in documentation**
```python
@router.post(
    "/topics",
    response_model=TopicResponse,
    summary="Create a new topic",
    description="""
    Create a new topic for thought leadership content.

    The topic will be associated with the authenticated user.

    **Workflow:**
    1. Create topic (this endpoint)
    2. Add evidence via `/topics/{topic_id}/evidence`
    3. Generate concepts via `/topics/{topic_id}/generate-concepts`
    4. Review and publish
    """,
    response_description="The created topic with generated ID",
    responses={
        201: {
            "description": "Topic created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "AI in Healthcare",
                        "description": "Strategic insights on AI adoption",
                        "source": "manual",
                        "status": "active",
                        "user_id": "123e4567-e89b-12d3-a456-426614174000",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
    }
)
async def create_topic(
    topic_data: TopicCreate,
    user: User = Depends(get_current_user)
):
    """Create topic with rich documentation"""
    pass
```

---

## Testing FastAPI Apps

### Pytest with TestClient

**✅ Good: Comprehensive FastAPI testing**
```python
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Provide test client"""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Provide async test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_list_topics_unauthorized(async_client):
    """Test topics endpoint without auth"""
    response = await async_client.get("/api/topics")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_topic_success(async_client, auth_token, db_session):
    """Test creating a topic"""
    topic_data = {
        "title": "Test Topic",
        "description": "Test description",
        "source": "manual"
    }

    response = await async_client.post(
        "/api/topics",
        json=topic_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == topic_data["title"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_topic_validation_error(async_client, auth_token):
    """Test validation error on create"""
    topic_data = {
        "title": "",  # Invalid - too short
        "description": "Test"
    }

    response = await async_client.post(
        "/api/topics",
        json=topic_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 422
    errors = response.json()["details"]["errors"]
    assert any("title" in e["field"] for e in errors)
```

### Mocking Dependencies

**✅ Good: Override dependencies in tests**
```python
from app.core.auth import get_current_user
from app.models.user import User
from uuid import uuid4


@pytest.fixture
def test_user():
    """Provide test user"""
    return User(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        role="user",
        is_active=True
    )


@pytest.fixture
def client_with_auth(test_user):
    """Provide client with mocked authentication"""
    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    yield client

    # Cleanup
    app.dependency_overrides.clear()


def test_list_topics_authenticated(client_with_auth):
    """Test topics endpoint with auth"""
    response = client_with_auth.get("/api/topics")
    assert response.status_code == 200
```

### Database Testing with Fixtures

**✅ Good: Isolated database tests**
```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models import Base


@pytest.fixture(scope="function")
async def db_session():
    """Provide test database session"""
    # Create test engine
    engine = create_async_engine(
        "postgresql+asyncpg://test:test@localhost/test_db",
        echo=False
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_topic_in_db(db_session):
    """Test topic creation in database"""
    topic = TLTopic(
        title="Test Topic",
        description="Test description",
        user_id=uuid4()
    )

    db_session.add(topic)
    await db_session.commit()
    await db_session.refresh(topic)

    assert topic.id is not None
    assert topic.title == "Test Topic"
```

---

## Performance Patterns

### Response Compression

**✅ Good: Enable gzip compression**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses > 1KB
```

### Response Caching

**✅ Good: Cache expensive endpoints**
```python
from functools import lru_cache
from fastapi import Depends


@lru_cache(maxsize=128)
def get_settings():
    """Cache settings (expensive to load)"""
    return Settings()


@router.get("/config")
async def get_config(
    settings: Settings = Depends(get_settings)  # Cached
):
    """Get configuration (cached)"""
    return settings.dict()


# For async caching
from aiocache import cached

@cached(ttl=300)  # Cache for 5 minutes
async def get_popular_topics() -> List[TLTopic]:
    """Get popular topics (cached)"""
    async with get_session() as session:
        stmt = (
            select(TLTopic)
            .order_by(TLTopic.view_count.desc())
            .limit(10)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


@router.get("/topics/popular")
async def list_popular_topics():
    """Get popular topics (cached for 5 minutes)"""
    topics = await get_popular_topics()
    return [TopicResponse.from_orm(t) for t in topics]
```

### Streaming Responses

**✅ Good: Stream large responses**
```python
from fastapi.responses import StreamingResponse
import asyncio


async def generate_large_dataset():
    """Generate large dataset incrementally"""
    for i in range(10000):
        yield f'{{"id": {i}, "data": "value_{i}"}}\n'
        await asyncio.sleep(0.001)  # Simulate processing


@router.get("/data/export")
async def export_data():
    """Export large dataset as streaming response"""
    return StreamingResponse(
        generate_large_dataset(),
        media_type="application/x-ndjson",
        headers={
            "Content-Disposition": "attachment; filename=export.ndjson"
        }
    )
```

### Pagination

**✅ Good: Efficient pagination**
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ):
        """Create paginated response"""
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=(total + page_size - 1) // page_size
        )


@router.get("/topics", response_model=PaginatedResponse[TopicResponse])
async def list_topics_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """List topics with pagination"""
    # Get total count
    count_stmt = select(func.count()).select_from(TLTopic).where(
        TLTopic.user_id == user.id
    )
    total = await session.scalar(count_stmt)

    # Get page of results
    offset = (page - 1) * page_size
    stmt = (
        select(TLTopic)
        .where(TLTopic.user_id == user.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    topics = result.scalars().all()

    return PaginatedResponse.create(
        items=[TopicResponse.from_orm(t) for t in topics],
        total=total,
        page=page,
        page_size=page_size
    )
```

---

## Security Best Practices

### Rate Limiting

**✅ Good: Rate limit endpoints**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@router.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(
    request: Request,
    credentials: LoginCredentials
):
    """Login with rate limiting"""
    pass
```

### SQL Injection Prevention

**✅ Good: Use SQLAlchemy parameters (safe)**
```python
# Safe - parameterized query
stmt = select(TLTopic).where(TLTopic.id == topic_id)

# Safe - parameters bound by SQLAlchemy
stmt = select(TLTopic).where(TLTopic.title.like(f"%{search_term}%"))
```

**❌ Bad: String concatenation (SQL injection risk)**
```python
# NEVER do this - SQL injection vulnerability
query = f"SELECT * FROM tl_topics WHERE title = '{search_term}'"
```

### HTTPS Enforcement

**✅ Good: Enforce HTTPS in production**
```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if settings.node_env == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### Security Headers

**✅ Good: Add security headers**
```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response
```

---

## Anti-Patterns

### 1. Sync Endpoints in Async App

**❌ Bad: Blocking sync operations**
```python
@router.get("/topics")
def list_topics():  # Should be async
    topics = db.query(TLTopic).all()  # Blocks event loop
    return topics
```

**✅ Good: Async all the way**
```python
@router.get("/topics")
async def list_topics(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(TLTopic))
    return result.scalars().all()
```

### 2. Missing Response Models

**❌ Bad: No response validation**
```python
@router.get("/topics")
async def list_topics():
    topics = await get_topics()
    return topics  # No validation or documentation
```

**✅ Good: Explicit response model**
```python
@router.get("/topics", response_model=List[TopicResponse])
async def list_topics() -> List[TopicResponse]:
    topics = await get_topics()
    return [TopicResponse.from_orm(t) for t in topics]
```

### 3. Database Sessions in Global Scope

**❌ Bad: Session at module level**
```python
session = SessionLocal()  # BAD - shared across requests

@router.get("/topics")
async def list_topics():
    topics = await session.execute(select(TLTopic))
    return topics.scalars().all()
```

**✅ Good: Dependency injection**
```python
@router.get("/topics")
async def list_topics(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(TLTopic))
    return result.scalars().all()
```

### 4. Not Using Status Codes

**❌ Bad: Always returns 200**
```python
@router.post("/topics")
async def create_topic(topic_data: TopicCreate):
    topic = await create_topic_in_db(topic_data)
    return topic  # Returns 200, should be 201
```

**✅ Good: Explicit status codes**
```python
@router.post("/topics", status_code=status.HTTP_201_CREATED)
async def create_topic(topic_data: TopicCreate):
    topic = await create_topic_in_db(topic_data)
    return topic  # Returns 201
```

### 5. Catching All Exceptions

**❌ Bad: Silent failures**
```python
@router.get("/topics/{topic_id}")
async def get_topic(topic_id: UUID):
    try:
        topic = await fetch_topic(topic_id)
        return topic
    except:  # Catches everything - BAD
        return {"error": "Something went wrong"}
```

**✅ Good: Specific exception handling**
```python
@router.get("/topics/{topic_id}")
async def get_topic(topic_id: UUID):
    try:
        topic = await fetch_topic(topic_id)
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic {topic_id} not found"
            )
        return topic
    except HTTPException:
        raise
    except Exception as e:
        logger.error("topic_fetch_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch topic"
        )
```

---

## Conclusion

This skill covers essential FastAPI patterns for building production-grade APIs with type safety, dependency injection, async database access, and comprehensive testing.

**Key Takeaways:**

1. **Lifespan Events**: Use `@asynccontextmanager` for startup/shutdown
2. **Router Organization**: Modular routers with prefixes and tags
3. **Dependency Injection**: Leverage `Depends()` for sessions, auth, services
4. **Pydantic Models**: Comprehensive validation with clear schemas
5. **Authentication**: Token-based auth with role-based access control
6. **Async Database**: SQLAlchemy 2.0 style with async sessions
7. **Background Tasks**: Use `BackgroundTasks` for non-blocking operations
8. **Middleware**: Correlation IDs, timing, CORS, security headers
9. **Error Handling**: Global exception handlers with structured responses
10. **Testing**: TestClient with dependency overrides and database fixtures
11. **Performance**: Caching, compression, streaming, pagination
12. **Security**: Rate limiting, HTTPS, SQL injection prevention

**Golden Rules:**

- Always use async/await consistently
- Define explicit response models
- Inject dependencies, don't import at module level
- Use specific status codes
- Log structured data with structlog
- Test with dependency overrides
- Handle errors explicitly
- Document endpoints with examples
- Validate all inputs with Pydantic
- Prevent N+1 queries with eager loading

When in doubt, follow FastAPI's philosophy: "FastAPI is modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints."


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

