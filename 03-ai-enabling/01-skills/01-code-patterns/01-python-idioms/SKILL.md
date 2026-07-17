---
last_updated: 2026-02-25
status: active
name: python-idioms
description: Python best practices, FastAPI patterns, Pydantic models, SQLAlchemy ORM. Use when working with Python codebases.
triggers:
  files: ["**/*.py", "**/pyproject.toml", "**/requirements.txt"]
  keywords: ["list comprehension", "generator", "decorator", "context manager", "async/await", "type hint", "pydantic", "fastapi", "sqlalchemy"]
allowed-tools: Read, Write, Edit
---

# Python Idioms: Deep Expertise Skill

## Overview

This skill provides comprehensive guidance on writing idiomatic, production-grade Python code. Use this skill when working with Python codebases, particularly those using FastAPI, Pydantic, and SQLAlchemy.

**When to use this skill:**
- Writing or reviewing Python code
- Working with FastAPI applications
- Designing Pydantic models and validation
- Using SQLAlchemy ORM patterns
- Implementing async Python patterns
- Code reviews for Pythonic idioms

**Core Philosophy:** Python emphasizes readability and explicitness. Code should be obvious to read, even if it takes slightly more characters. "Explicit is better than implicit" from The Zen of Python guides all decisions.

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## Core Principles

### The Zen of Python (PEP 20)

```python
import this  # The Zen of Python

# Key principles:
# - Beautiful is better than ugly
# - Explicit is better than implicit
# - Simple is better than complex
# - Complex is better than complicated
# - Readability counts
# - Flat is better than nested
# - Sparse is better than dense
```

### EAFP vs LBYL

Python favors **EAFP** (Easier to Ask Forgiveness than Permission) over LBYL (Look Before You Leap):

```python
# ❌ BAD: LBYL (Look Before You Leap)
if key in dictionary:
    value = dictionary[key]
else:
    value = None

# ✅ GOOD: EAFP (Easier to Ask for Forgiveness than Permission)
try:
    value = dictionary[key]
except KeyError:
    value = None

# ✅ BETTER: Use dict.get()
value = dictionary.get(key)
```

---

## Core Python Idioms

### 1. List Comprehensions & Generator Expressions

**✅ Good: List comprehension**
```python
# Pythonic - clear, concise, fast
active_topics = [topic for topic in topics if topic.status == "active"]

# Transform data
topic_ids = [str(topic.id) for topic in topics]

# Nested comprehension (when readable)
evidence_dict = {
    str(topic.id): [e for e in topic.evidence if e.verified]
    for topic in topics
}
```

**❌ Bad: Manual loop accumulation**
```python
# Don't do this
active_topics = []
for topic in topics:
    if topic.status == "active":
        active_topics.append(topic)
```

**Generator expressions for memory efficiency:**
```python
# ✅ Good: Memory-efficient for large datasets
total_score = sum(item.score for item in evidence_items if item.verified)

# ❌ Bad: Creates intermediate list
total_score = sum([item.score for item in evidence_items if item.verified])

# ✅ Good: Lazy evaluation for large files
lines = (line.strip() for line in file)
```

### 2. Context Managers

Always use context managers for resource management.

**✅ Good: Database sessions**
```python
# FastAPI with SQLAlchemy async
async with get_session() as session:
    result = await session.execute(select(TLTopic))
    topics = result.scalars().all()
    # Session automatically closed and cleaned up

# File handling
with open('data.json', 'r') as f:
    data = json.load(f)
```

**❌ Bad: Manual cleanup**
```python
# Don't do this
session = SessionLocal()
try:
    topics = session.query(TLTopic).all()
finally:
    session.close()
```

**Custom context managers:**
```python
from contextlib import contextmanager
import structlog

@contextmanager
def log_operation(operation_name: str):
    """Context manager for operation logging"""
    logger = structlog.get_logger()
    logger.info(f"{operation_name}_started")
    try:
        yield
    except Exception as e:
        logger.error(f"{operation_name}_failed", error=str(e))
        raise
    else:
        logger.info(f"{operation_name}_completed")

# Usage
with log_operation("evidence_selection"):
    evidence = select_evidence(items)
```

### 3. Decorators

Decorators separate cross-cutting concerns from business logic.

**✅ Good: FastAPI dependency injection**
```python
from fastapi import Depends, HTTPException
from app.core.security import get_current_user

@router.get("/topics/{topic_id}")
async def get_topic(
    topic_id: UUID,
    current_user: User = Depends(get_current_user)  # Decorator-like dependency
) -> TopicResponse:
    """Get topic by ID with authentication"""
    # Business logic here
```

**Custom decorators:**
```python
from functools import wraps
import time

def timed(func):
    """Decorator to time function execution"""
    @wraps(func)  # Preserves original function metadata
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__}_duration", seconds=duration)
        return result
    return wrapper

# Usage
@timed
async def generate_concepts(topic_id: UUID):
    # Implementation
    pass
```

### 4. Type Hints

Use type hints everywhere for code clarity and IDE support.

**✅ Good: Comprehensive type hints**
```python
from typing import List, Dict, Any, Optional, Tuple, Union
from uuid import UUID
from decimal import Decimal

def calculate_score(
    item: TLEvidenceItem,
    preferences: Optional[FeedbackPreferences],
    topic_keywords: Optional[List[str]]
) -> Tuple[float, Dict[str, float]]:
    """
    Calculate final score for an evidence item.

    Args:
        item: Evidence item to score
        preferences: Optional user preferences
        topic_keywords: Optional topic keywords

    Returns:
        Tuple of (final_score, score_breakdown)
    """
    # Implementation
    pass
```

**Modern Python 3.10+ syntax:**
```python
# Union types with |
def process(value: str | int | None) -> dict[str, any]:
    pass

# Use dict/list instead of Dict/List (3.9+)
def get_evidence() -> list[dict[str, any]]:
    pass
```

### 5. Dataclasses & Pydantic Models

**Dataclasses for internal data:**
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ScoredEvidence:
    """Evidence item with calculated score"""
    evidence_item: dict
    final_score: float
    score_breakdown: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
```

**Pydantic for API schemas:**
```python
from pydantic import BaseModel, Field, validator
from uuid import UUID

class TopicCreate(BaseModel):
    """Schema for creating a new topic"""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    class Config:
        orm_mode = True  # Allow ORM model conversion
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
```

### 6. Error Handling

**✅ Good: Specific exceptions with context**
```python
class EvidenceNotFoundError(Exception):
    """Raised when evidence cannot be found"""
    pass

async def get_evidence(evidence_id: UUID) -> TLEvidence:
    """Get evidence by ID"""
    try:
        async with get_session() as session:
            result = await session.execute(
                select(TLEvidence).where(TLEvidence.id == evidence_id)
            )
            evidence = result.scalar_one_or_none()

            if not evidence:
                raise EvidenceNotFoundError(
                    f"Evidence {evidence_id} not found"
                )

            return evidence

    except SQLAlchemyError as e:
        logger.error("database_error", error=str(e))
        raise
    except Exception as e:
        logger.error("unexpected_error", error=str(e))
        raise
```

**❌ Bad: Catching everything**
```python
# Don't do this
try:
    result = do_something()
except:  # Bare except catches even SystemExit!
    pass
```

### 7. None Handling

**✅ Good: Explicit None checks**
```python
# Use 'is' for None comparison
if value is None:
    return default_value

if value is not None:
    process(value)

# Default with or operator (for falsy values)
result = user_input or "default"

# Default for None specifically
result = value if value is not None else "default"
```

**❌ Bad: Truthiness for None**
```python
# Don't do this - fails for 0, False, "", []
if not value:  # Intended to check for None, but catches other falsy values
    return default
```

### 8. Dictionary Operations

**✅ Good: Modern dict patterns**
```python
# Get with default
score = scores.get(item_id, 0.0)

# Merge dicts (Python 3.9+)
combined = base_config | user_config

# Dict comprehension
evidence_map = {
    str(item.id): item
    for item in evidence_items
    if item.verified
}

# Destructuring
metadata = {"source": "web", "confidence": 0.9, "extra": "data"}
needed_fields = {k: metadata[k] for k in ["source", "confidence"]}
```

### 9. String Formatting

**✅ Good: f-strings (Python 3.6+)**
```python
# Modern, readable, fast
logger.info(f"Processing topic {topic_id} with {len(items)} items")

# With expressions
message = f"Score: {score:.2f}%"

# Multi-line
query = f"""
    SELECT * FROM evidence
    WHERE topic_id = {topic_id}
    AND status = 'verified'
"""
```

**❌ Bad: Old-style formatting**
```python
# Don't use these
message = "Processing topic %s" % topic_id
message = "Processing topic {}".format(topic_id)
```

### 10. Iteration Patterns

**✅ Good: Modern iteration**
```python
# Enumerate for index + item
for idx, item in enumerate(evidence_items):
    print(f"{idx}: {item.content}")

# Zip for parallel iteration
for topic, score in zip(topics, scores):
    print(f"{topic.title}: {score}")

# Unpacking in loops
for name, value in metadata.items():
    process(name, value)

# Reversed iteration
for item in reversed(items):
    process(item)
```

---

## FastAPI Patterns

### 1. Dependency Injection

FastAPI's dependency injection is its superpower. Use it for authentication, database sessions, and shared logic.

**✅ Good: Reusable dependencies**
```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncSession:
    """Provide database session"""
    async with SessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    """Get authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

# Usage in route
@router.post("/topics")
async def create_topic(
    topic_data: TopicCreate,
    current_user: User = Depends(get_current_user),  # Auto-injected
    session: AsyncSession = Depends(get_session)     # Auto-injected
) -> TopicResponse:
    """Create new topic (authenticated)"""
    topic = TLTopic(**topic_data.dict(), user_id=current_user.id)
    session.add(topic)
    await session.commit()
    return TopicResponse.from_orm(topic)
```

### 2. Response Models

Always define explicit response models for type safety and auto-generated docs.

**✅ Good: Explicit response models**
```python
from pydantic import BaseModel
from datetime import datetime

class TopicResponse(BaseModel):
    """Topic API response"""
    id: UUID
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.get("/topics/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: UUID) -> TopicResponse:
    """Get topic by ID - response automatically validated"""
    # Return ORM model, FastAPI converts to Pydantic
    return topic_orm_instance
```

### 3. Background Tasks

Use BackgroundTasks for async operations that don't block the response.

**✅ Good: Background task pattern**
```python
from fastapi import BackgroundTasks

async def process_evidence_background(topic_id: UUID):
    """Background: Process evidence for topic"""
    logger.info("background_processing_started", topic_id=str(topic_id))
    try:
        # Long-running operation
        await generate_concepts(topic_id)
        logger.info("background_processing_complete", topic_id=str(topic_id))
    except Exception as e:
        logger.error("background_processing_failed",
                    topic_id=str(topic_id), error=str(e))

@router.post("/topics/{topic_id}/process")
async def trigger_processing(
    topic_id: UUID,
    background_tasks: BackgroundTasks
):
    """Trigger evidence processing (async)"""
    background_tasks.add_task(process_evidence_background, topic_id)
    return {"message": "Processing started", "topic_id": str(topic_id)}
```

### 4. Error Handling with HTTPException

**✅ Good: Specific HTTP exceptions**
```python
from fastapi import HTTPException, status

@router.get("/topics/{topic_id}")
async def get_topic(
    topic_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> TopicResponse:
    """Get topic by ID"""
    result = await session.execute(
        select(TLTopic).where(TLTopic.id == topic_id)
    )
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {topic_id} not found"
        )

    return TopicResponse.from_orm(topic)
```

### 5. Request Validation

**✅ Good: Pydantic validation in request body**
```python
from pydantic import BaseModel, Field, validator

class EvidenceFilter(BaseModel):
    """Filter parameters for evidence search"""
    category: Optional[str] = Field(None, description="Evidence category")
    min_confidence: float = Field(0.0, ge=0.0, le=1.0)
    max_items: int = Field(50, ge=1, le=100)
    keywords: List[str] = Field(default_factory=list)

    @validator('category')
    def validate_category(cls, v):
        valid_categories = ['insight', 'statistic', 'quote', 'framework']
        if v and v not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}")
        return v

@router.post("/evidence/search")
async def search_evidence(
    filters: EvidenceFilter,  # Auto-validated
    session: AsyncSession = Depends(get_session)
) -> List[EvidenceResponse]:
    """Search evidence with validated filters"""
    # filters guaranteed to be valid
    pass
```

---

## SQLAlchemy Patterns

### 1. Async Session Management

**✅ Good: Context manager for sessions**
```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    """Provide database session with automatic cleanup"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 2. Query Patterns

**✅ Good: SQLAlchemy 2.0 style (select)**
```python
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

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
```

**❌ Bad: Legacy query API**
```python
# Don't use this (SQLAlchemy 1.x style)
topics = session.query(TLTopic).filter_by(status="active").all()
```

### 3. Eager Loading (N+1 Prevention)

**✅ Good: Eager load relationships**
```python
from sqlalchemy.orm import selectinload, joinedload

# selectinload: Separate query (good for collections)
stmt = (
    select(TLTopic)
    .options(selectinload(TLTopic.concepts))
    .where(TLTopic.id == topic_id)
)

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
# Don't do this - causes N+1 queries
topics = await session.execute(select(TLTopic))
for topic in topics:
    print(topic.concepts)  # Each access = new query!
```

### 4. Model Definition

**✅ Good: Comprehensive model**
```python
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4

class TLTopic(Base):
    """Thought leadership topic model"""

    __tablename__ = "tl_topics"
    __table_args__ = (
        Index("idx_tl_topics_status", "status"),
        Index("idx_tl_topics_user", "user_id"),
        {"schema": "insights_copilot"}
    )

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Fields
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="idea", nullable=False)
    tags = Column(JSONB, default=list, nullable=False)

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("insights_copilot.users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Relationships (lazy loading by default)
    user = relationship("User", back_populates="topics")
    concepts = relationship("TLConcept", back_populates="topic")

    # Audit timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "tags": self.tags or [],
            "user_id": str(self.user_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
```

### 5. Transactions

**✅ Good: Explicit transaction management**
```python
async def create_topic_with_evidence(
    topic_data: TopicCreate,
    evidence_data: List[EvidenceCreate],
    session: AsyncSession
):
    """Create topic and evidence atomically"""
    # All within single transaction
    topic = TLTopic(**topic_data.dict())
    session.add(topic)
    await session.flush()  # Get topic.id without committing

    # Create evidence items
    evidence_items = [
        TLEvidence(**item.dict(), topic_id=topic.id)
        for item in evidence_data
    ]
    session.add_all(evidence_items)

    # Commit atomically (done by context manager)
    return topic
```

---

## Async/Await Patterns

### 1. Async Function Definition

**✅ Good: Clear async patterns**
```python
# Async function
async def fetch_evidence(topic_id: UUID) -> List[TLEvidence]:
    """Fetch evidence for topic"""
    async with get_session() as session:
        result = await session.execute(
            select(TLEvidence).where(TLEvidence.topic_id == topic_id)
        )
        return result.scalars().all()

# Regular function (when no async needed)
def calculate_score(item: TLEvidence) -> float:
    """Calculate evidence score (synchronous)"""
    return float(item.credibility_score or 0.5)
```

### 2. Concurrent Operations

**✅ Good: Run operations concurrently**
```python
import asyncio

# Gather: Wait for all
async def fetch_all_data(topic_id: UUID):
    """Fetch multiple data sources concurrently"""
    evidence_task = fetch_evidence(topic_id)
    concepts_task = fetch_concepts(topic_id)
    metadata_task = fetch_metadata(topic_id)

    # All run concurrently
    evidence, concepts, metadata = await asyncio.gather(
        evidence_task,
        concepts_task,
        metadata_task
    )

    return {"evidence": evidence, "concepts": concepts, "metadata": metadata}

# As completed: Process as they finish
async def process_topics(topic_ids: List[UUID]):
    """Process topics as they complete"""
    tasks = [process_topic(tid) for tid in topic_ids]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        handle_result(result)
```

### 3. Async Context Managers

**✅ Good: Async context manager**
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def timed_operation(operation_name: str):
    """Async context manager for timing operations"""
    start = time.time()
    logger.info(f"{operation_name}_started")
    try:
        yield
    finally:
        duration = time.time() - start
        logger.info(f"{operation_name}_completed", duration=duration)

# Usage
async with timed_operation("evidence_generation"):
    await generate_evidence(topic_id)
```

### 4. Async Generators

**✅ Good: Stream large results**
```python
async def stream_evidence(topic_id: UUID):
    """Stream evidence items one at a time"""
    async with get_session() as session:
        stmt = select(TLEvidence).where(TLEvidence.topic_id == topic_id)
        result = await session.stream(stmt)

        async for row in result:
            evidence = row[0]
            yield evidence

# Usage
async for evidence in stream_evidence(topic_id):
    await process_evidence(evidence)
```

---

## Logging with Structlog

**✅ Good: Structured logging**
```python
import structlog

logger = structlog.get_logger(__name__)

# Bind context to logger
logger = logger.bind(service="evidence_selector", version="2.0")

# Log with structured data
logger.info(
    "evidence_selected",
    topic_id=str(topic_id),
    selected_count=len(selected),
    top_score=selected[0].score if selected else 0.0
)

# Error logging with exception
try:
    result = await process_evidence(topic_id)
except Exception as e:
    logger.error(
        "evidence_processing_failed",
        topic_id=str(topic_id),
        error=str(e),
        exc_info=True  # Include traceback
    )
    raise
```

**❌ Bad: String interpolation in logs**
```python
# Don't do this - loses structured data
logger.info(f"Processing topic {topic_id} with {count} items")
```

---

## Anti-Patterns

### 1. Mutable Default Arguments

**❌ BAD: Mutable default**
```python
def add_item(item: str, items: List[str] = []):  # WRONG!
    items.append(item)
    return items

# Problem: default list is shared across calls
add_item("a")  # ["a"]
add_item("b")  # ["a", "b"] - unexpected!
```

**✅ GOOD: None as default**
```python
def add_item(item: str, items: Optional[List[str]] = None) -> List[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### 2. Catching Exception Too Broadly

**❌ BAD: Catch everything**
```python
try:
    result = process_data()
except Exception:  # Catches too much
    return None
```

**✅ GOOD: Specific exceptions**
```python
try:
    result = process_data()
except (ValueError, KeyError) as e:
    logger.error("data_processing_failed", error=str(e))
    raise DataProcessingError(f"Failed to process: {e}")
except Exception as e:
    logger.error("unexpected_error", error=str(e))
    raise
```

### 3. String Concatenation in Loops

**❌ BAD: String concatenation**
```python
result = ""
for item in items:
    result += item + ", "  # Creates new string each iteration
```

**✅ GOOD: Join**
```python
result = ", ".join(items)
```

### 4. Using * Imports

**❌ BAD: Star imports**
```python
from models import *  # What did we import?
from utils import *
```

**✅ GOOD: Explicit imports**
```python
from models import TLTopic, TLEvidence, TLConcept
from utils import calculate_score, format_date
```

### 5. Not Using Pathlib

**❌ BAD: String manipulation**
```python
import os
path = os.path.join("data", "evidence", filename)
if os.path.exists(path):
    with open(path, "r") as f:
        data = f.read()
```

**✅ GOOD: Pathlib**
```python
from pathlib import Path

path = Path("data") / "evidence" / filename
if path.exists():
    data = path.read_text()
```

### 6. Manual Type Checking

**❌ BAD: isinstance checks**
```python
def process(value):
    if isinstance(value, str):
        return value.upper()
    elif isinstance(value, int):
        return value * 2
    elif isinstance(value, list):
        return len(value)
```

**✅ GOOD: Polymorphism or Protocol**
```python
from typing import Protocol

class Processable(Protocol):
    def process(self) -> Any:
        ...

def process(value: Processable) -> Any:
    return value.process()
```

### 7. Not Using Comprehensions

**❌ BAD: Manual filtering**
```python
result = []
for item in items:
    if item.status == "active":
        transformed = transform(item)
        result.append(transformed)
```

**✅ GOOD: Comprehension**
```python
result = [transform(item) for item in items if item.status == "active"]
```

### 8. Manual JSON Serialization

**❌ BAD: Manual dict building**
```python
def to_json(topic: TLTopic) -> str:
    data = {
        "id": str(topic.id),
        "title": topic.title,
        # ... many more fields
    }
    return json.dumps(data)
```

**✅ GOOD: Pydantic or dataclass**
```python
class TopicResponse(BaseModel):
    id: UUID
    title: str

    class Config:
        orm_mode = True

# Automatic serialization
return TopicResponse.from_orm(topic).json()
```

---

## Code Examples: Good vs Bad

### Example 1: Evidence Selection Service

**❌ BAD: Imperative, unclear**
```python
def select_evidence(items, preferences, max_items):
    result = []
    for item in items:
        if preferences:
            if preferences.excluded_types:
                skip = False
                for excluded in preferences.excluded_types:
                    if item.type == excluded:
                        skip = True
                        break
                if skip:
                    continue

        score = item.confidence
        if preferences and preferences.type_weights:
            if item.type in preferences.type_weights:
                score = score * preferences.type_weights[item.type]

        result.append((item, score))

    result.sort(key=lambda x: x[1], reverse=True)
    return [item for item, score in result[:max_items]]
```

**✅ GOOD: Declarative, readable**
```python
def select_evidence(
    items: List[TLEvidenceItem],
    preferences: Optional[FeedbackPreferences] = None,
    max_items: int = 50
) -> List[ScoredEvidence]:
    """
    Select and score evidence items based on preferences.

    Returns top N items by score, excluding filtered types.
    """
    # Filter exclusions
    if preferences and preferences.excluded_types:
        items = [
            item for item in items
            if item.evidence_type not in preferences.excluded_types
        ]

    # Calculate scores
    scored_items = [
        ScoredEvidence(
            evidence_item=item.to_dict(),
            final_score=self._calculate_score(item, preferences),
            score_breakdown=self._get_breakdown(item, preferences)
        )
        for item in items
    ]

    # Sort and limit
    scored_items.sort(key=lambda x: x.final_score, reverse=True)
    return scored_items[:max_items]
```

### Example 2: Database Query

**❌ BAD: Manual query building**
```python
def get_topics_for_user(user_id, status=None, limit=100):
    query = f"SELECT * FROM tl_topics WHERE user_id = '{user_id}'"
    if status:
        query += f" AND status = '{status}'"
    query += f" LIMIT {limit}"

    # SQL injection risk!
    results = db.execute(query)
    return results
```

**✅ GOOD: SQLAlchemy with type safety**
```python
async def get_topics_for_user(
    user_id: UUID,
    status: Optional[str] = None,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
) -> List[TLTopic]:
    """
    Get topics for user with optional status filter.

    Args:
        user_id: User ID to filter by
        status: Optional status filter
        limit: Maximum results to return
        session: Database session

    Returns:
        List of topic models
    """
    stmt = (
        select(TLTopic)
        .where(TLTopic.user_id == user_id)
        .limit(limit)
    )

    if status:
        stmt = stmt.where(TLTopic.status == status)

    result = await session.execute(stmt)
    return result.scalars().all()
```

### Example 3: Error Handling

**❌ BAD: Silent failures**
```python
def process_topic(topic_id):
    try:
        topic = get_topic(topic_id)
        evidence = generate_evidence(topic)
        concepts = generate_concepts(evidence)
        return concepts
    except:
        return None  # What went wrong?
```

**✅ GOOD: Explicit error handling**
```python
async def process_topic(topic_id: UUID) -> ProcessingResult:
    """
    Process topic through full pipeline.

    Raises:
        TopicNotFoundError: If topic doesn't exist
        EvidenceGenerationError: If evidence generation fails
        ConceptGenerationError: If concept generation fails
    """
    logger.info("processing_started", topic_id=str(topic_id))

    try:
        # Get topic
        topic = await get_topic(topic_id)
        if not topic:
            raise TopicNotFoundError(f"Topic {topic_id} not found")

        # Generate evidence
        try:
            evidence = await generate_evidence(topic)
        except Exception as e:
            logger.error("evidence_generation_failed",
                        topic_id=str(topic_id), error=str(e))
            raise EvidenceGenerationError(
                f"Failed to generate evidence: {e}"
            ) from e

        # Generate concepts
        try:
            concepts = await generate_concepts(evidence)
        except Exception as e:
            logger.error("concept_generation_failed",
                        topic_id=str(topic_id), error=str(e))
            raise ConceptGenerationError(
                f"Failed to generate concepts: {e}"
            ) from e

        logger.info("processing_complete",
                   topic_id=str(topic_id),
                   concepts_count=len(concepts))

        return ProcessingResult(
            topic_id=topic_id,
            concepts=concepts,
            evidence_count=len(evidence)
        )

    except (TopicNotFoundError, EvidenceGenerationError, ConceptGenerationError):
        # Re-raise known errors
        raise
    except Exception as e:
        # Catch unexpected errors
        logger.error("unexpected_processing_error",
                    topic_id=str(topic_id), error=str(e))
        raise ProcessingError(
            f"Unexpected error processing topic: {e}"
        ) from e
```

---

## Performance Tips

### 1. Use Generators for Large Data

```python
# ✅ Memory efficient
def process_large_file(filepath: Path):
    """Process file line by line"""
    with filepath.open() as f:
        for line in f:  # Generator - one line at a time
            yield process_line(line)

# ❌ Memory intensive
def process_large_file_bad(filepath: Path):
    """Loads entire file into memory"""
    with filepath.open() as f:
        lines = f.readlines()  # All lines in memory
        return [process_line(line) for line in lines]
```

### 2. Batch Database Operations

```python
# ✅ Batch insert
async def create_evidence_items(
    items: List[EvidenceCreate],
    session: AsyncSession
):
    """Create multiple evidence items in one transaction"""
    evidence_objects = [TLEvidence(**item.dict()) for item in items]
    session.add_all(evidence_objects)  # Batch insert
    await session.commit()

# ❌ Individual inserts
async def create_evidence_items_bad(items, session):
    """One query per item - slow!"""
    for item in items:
        evidence = TLEvidence(**item.dict())
        session.add(evidence)
        await session.commit()  # Commit each - very slow!
```

### 3. Use `__slots__` for Memory Optimization

```python
# ✅ Reduced memory footprint
class Evidence:
    __slots__ = ['content', 'score', 'category', 'source']

    def __init__(self, content: str, score: float, category: str, source: str):
        self.content = content
        self.score = score
        self.category = category
        self.source = source
```

### 4. Cache Expensive Operations

```python
from functools import lru_cache

# ✅ Cache pure function results
@lru_cache(maxsize=128)
def calculate_expensive_metric(value: int) -> float:
    """Expensive calculation - cached for repeated calls"""
    return complex_calculation(value)

# For async functions
from aiocache import cached

@cached(ttl=300)  # Cache for 5 minutes
async def fetch_remote_data(url: str) -> dict:
    """Cache API responses"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

---

## Testing Patterns

### 1. Pytest Fixtures

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def session() -> AsyncSession:
    """Provide test database session"""
    # Setup
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()  # Cleanup

@pytest.fixture
async def sample_topic(session: AsyncSession) -> TLTopic:
    """Provide sample topic for testing"""
    topic = TLTopic(
        title="Test Topic",
        description="Test description",
        user_id=uuid4()
    )
    session.add(topic)
    await session.commit()
    await session.refresh(topic)
    return topic
```

### 2. Test Structure

```python
@pytest.mark.asyncio
async def test_select_evidence_with_preferences(session):
    """Test evidence selection with user preferences"""
    # Arrange
    preferences = FeedbackPreferences(
        evidence_type_weights={"statistic": 2.0, "example": 0.5}
    )
    items = [
        TLEvidenceItem(
            content="Stat content",
            evidence_type="statistic",
            confidence_score=0.8
        ),
        TLEvidenceItem(
            content="Example content",
            evidence_type="example",
            confidence_score=0.8
        )
    ]

    # Act
    service = EvidenceSelectorService()
    selected = service.select_evidence(items, preferences, max_items=10)

    # Assert
    assert len(selected) == 2
    assert selected[0].evidence_item["evidence_type"] == "statistic"
    assert selected[0].final_score > selected[1].final_score
```

### 3. Mocking

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_process_topic_with_api_failure():
    """Test handling of API failures"""
    # Mock external API
    with patch('app.services.openai_service.generate_concepts') as mock_gen:
        mock_gen.side_effect = Exception("API Error")

        # Test error handling
        with pytest.raises(ConceptGenerationError):
            await process_topic(topic_id)
```

---

## Conclusion

This skill covers the essential Python idioms, FastAPI patterns, Pydantic validation, SQLAlchemy ORM usage, and async patterns for production-grade Python development.

**Key Takeaways:**
1. **Readability matters**: Write explicit, clear code
2. **Use type hints**: Enable IDE support and catch errors early
3. **Leverage standard library**: List comprehensions, context managers, etc.
4. **Handle errors explicitly**: Specific exceptions with context
5. **Async properly**: Use `async`/`await` consistently
6. **FastAPI dependencies**: Leverage dependency injection
7. **SQLAlchemy 2.0 style**: Use `select()` pattern
8. **Pydantic everywhere**: For validation and serialization
9. **Structured logging**: Use structlog for observability
10. **Test thoroughly**: Pytest with fixtures and mocks

When in doubt, follow The Zen of Python: "Explicit is better than implicit" and "Readability counts".


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

