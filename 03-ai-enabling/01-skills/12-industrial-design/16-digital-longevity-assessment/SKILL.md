---
last_updated: 2026-02-25
status: active
name: digital-longevity-assessment
description: Assessment patterns for evaluating API stability and long-term maintainability. Use when designing versioning strategies, handling deprecation, or ensuring backwards compatibility.
category: industrial-design-digital
keywords:
  - api-stability
  - versioning
  - backwards-compatibility
  - deprecation
  - longevity
triggers:
  keywords:
    - API design
    - breaking changes
    - versioning
    - deprecation
    - backwards compatibility
  filePatterns:
    - "**/api/**/*.ts"
    - "**/routes/**/*.ts"
    - "openapi.yaml"
allowed-tools: Read, Write, Edit
---

# Digital Longevity Assessment

Design APIs, interfaces, and data structures that remain stable for 10+ years.

## Philosophy

Physical products designed by Rams remained relevant for decades. Digital products should be no different. An API designed in 2026 should work unchanged in 2036. Longevity comes from restraint—not predicting the future, but refusing to encode the present's fashion into the foundation.

**Rams Principle 7 (Long-lasting):** Avoid fashion. Design for decades.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Methodology

### Step 1: Identify Stability Layers

| Layer | Lifespan | Change Frequency | Strategy |
|-------|----------|------------------|----------|
| **Data schema** | 20+ years | Never break | Additive only |
| **Public APIs** | 10+ years | Semver major | Deprecation grace period |
| **Component interfaces** | 5+ years | Props addition only | Compose, don't configure |
| **Internal functions** | 1+ years | Refactor freely | Private contracts |

### Step 2: Timelessness Test

For each interface decision, ask:
1. **Will this be right in 2036?**
2. **Does this encode 2026 assumptions?**
3. **Can this grow without breaking?**

### Step 3: Additive Design

```typescript
// WRONG: Breaking change required for new feature
interface User {
  id: string;
  name: string;
  // Adding email breaks existing consumers
}

// RIGHT: Additive growth
interface User {
  id: string;
  name: string;
  email?: string;  // Optional addition
  profile?: UserProfile;  // Nested extension
}
```

### Step 4: Deprecation Protocol

When change is unavoidable:

1. **Announce:** 12 months advance notice
2. **Dual-run:** New + old coexist for 12 months
3. **Warn:** Runtime warnings in logs (not breaking)
4. **Remove:** Only after grace period

### Step 5: Version Strategy

```typescript
// Semantic versioning for public APIs
const API_VERSION = {
  major: 2,  // Breaking changes (rare)
  minor: 14, // New features (additive)
  patch: 3   // Bug fixes (transparent)
};

// URL versioning for external APIs
// /v2/users (long-lived)
// Not: /2026/users (dated)
```

## Tests

| Test | Pass Criteria | Fail Criteria |
|------|---------------|---------------|
| **10-Year Interface** | Design works unchanged in 2036 | Requires breaking changes |
| **Additive Growth** | New features add fields/endpoints | New features change existing |
| **No Fashion** | No 2026-specific patterns | "Modern" patterns that date |
| **Graceful Deprecation** | 12-month dual-run period | Immediate breaking removal |
| **Schema Stability** | Database columns only added | Database columns renamed/removed |

## Anti-Patterns

| Anti-Pattern | Why Wrong | Alternative |
|--------------|-----------|-------------|
| **Trendy API patterns** | "GraphQL is hot" → tight coupling | REST with additive growth |
| **Frequent breaking changes** | Disrespects consumers | Semver major = emergency only |
| **No versioning** | Can't evolve safely | URL versioning for public APIs |
| **Implicit contracts** | Breaking changes invisible | Explicit TypeScript interfaces |
| **Removing fields** | Breaks unknown consumers | Deprecate, warn, then remove |
| **Date-based versioning** | Encodes fashion | Semantic versioning |

## Examples

### Good Example

```typescript
// API designed for longevity (2026 → 2036)
// File: app/api/routes/v2/insights.py

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class InsightV2(BaseModel):
    """
    Stable schema. Additive only.
    v2.0.0 (2026-01-19): Initial
    v2.1.0 (2026-06-15): Added source_ids (optional)
    v2.2.0 (2026-09-10): Added confidence (optional)
    """
    id: str
    title: str
    content: str
    created_at: datetime

    # Additive additions (never breaking)
    source_ids: Optional[List[str]] = None
    confidence: Optional[float] = None

@router.get("/v2/insights/{id}")
async def get_insight_v2(id: str) -> InsightV2:
    """
    Stable endpoint. Will work unchanged in 2036.
    """
    return await insights_service.get_by_id(id)

# Deprecated v1 still runs alongside
@router.get("/v1/insights/{id}")
async def get_insight_v1(id: str) -> InsightV1:
    """
    DEPRECATED: Use /v2/insights/{id}
    Removal date: 2027-01-19 (12 months notice)
    """
    warnings.warn("v1 API deprecated", DeprecationWarning)
    return await insights_service.get_by_id_v1(id)
```

### Bad Example

```typescript
// Trendy, unstable, will break
// File: app/api/routes/insights.py (no versioning)

@router.get("/insights/{id}")  # No version
async def get_insight(id: str) -> dict:  # Untyped contract
    """Get insight by ID"""
    # Breaking change: renamed 'content' → 'body'
    return {
        "id": insight.id,
        "title": insight.title,
        "body": insight.content,  # BREAKING
        # Removed created_at (BREAKING)
    }

# No deprecation grace period
# No version history
# No TypeScript types
# Will break consumers immediately
```

## Implementation Checklist

- [ ] Public APIs use semantic versioning
- [ ] External APIs use URL versioning (/v2/)
- [ ] All interfaces have TypeScript types
- [ ] Database migrations are additive only
- [ ] Deprecation policy documented (12-month grace)
- [ ] Runtime warnings for deprecated endpoints
- [ ] Version history in docstrings
- [ ] No fashion-driven rewrites
- [ ] Consumer contracts tested
- [ ] Breaking changes require major version bump


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

