---
last_updated: 2026-02-25
status: active
name: architecture-decision-records
description: Create and maintain Architecture Decision Records (ADRs). Document context, options considered, decision rationale, and consequences. Use when making significant technical decisions that need documentation.
triggers:
  files: ["**/ADR/**", "**/adr/**", "**/decisions/**", "**/architecture-decisions/**", "**/docs/adr*.md"]
  keywords: ["ADR", "architecture decision", "decision record", "technical decision", "document decision", "decision rationale", "alternatives considered"]
allowed-tools: Read, Write, Edit
---

# Architecture Decision Records

## Overview

Architecture Decision Records (ADRs) capture significant technical decisions along with their context, options considered, and consequences. They serve as a historical record explaining *why* decisions were made, not just *what* was decided.

Good ADRs prevent repeated debates, onboard new team members faster, and provide accountability for architectural choices. They acknowledge that decisions are made with incomplete information and may need revisiting.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Instructions

### Step 1: Identify Decision-Worthy Topics

Not every choice needs an ADR. Document decisions that are:

| Worth Documenting | Skip ADR |
|-------------------|----------|
| Affects multiple components/teams | Localized to one file |
| Hard to reverse later | Easily changed |
| Has multiple viable options | One obvious choice |
| Impacts non-functional requirements | Pure implementation detail |
| Team disagrees on approach | Everyone agrees immediately |

### Step 2: Gather Context

Before writing, understand:

1. **Problem statement**: What are we trying to solve?
2. **Constraints**: Budget, timeline, team skills, existing systems
3. **Stakeholders**: Who cares about this decision?
4. **Requirements**: Functional and non-functional needs

### Step 3: Evaluate Options

For each viable option:

| Evaluation Criteria | Questions |
|---------------------|-----------|
| **Fit** | Does it solve the problem? |
| **Cost** | Implementation effort, licensing, infrastructure |
| **Risk** | What could go wrong? |
| **Team** | Do we have the skills? |
| **Operations** | Can we run and maintain it? |
| **Reversibility** | How hard to change later? |

### Step 4: Write the ADR

Use the standard template (see Examples section). Key sections:

1. **Title**: Short, descriptive (ADR-NNN: Decision Title)
2. **Status**: Proposed → Accepted → Deprecated/Superseded
3. **Context**: Why we're making this decision
4. **Decision**: What we decided
5. **Consequences**: Good and bad outcomes
6. **Alternatives**: Options we didn't choose and why

### Step 5: Review and Publish

- Get stakeholder buy-in before finalizing
- Store ADRs with the codebase (version controlled)
- Link ADRs from relevant code via comments
- Set review dates for long-term decisions

## ADR Template

```markdown
# ADR-NNN: [Decision Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

**Date:** YYYY-MM-DD

**Deciders:** [Names/roles of people involved]

## Context

[Describe the situation that prompted this decision. Include:]
- What problem are we solving?
- What constraints exist?
- What requirements must we meet?
- Why is a decision needed now?

## Decision

[State the decision clearly in 1-2 sentences.]

We will [decision].

## Alternatives Considered

### Option 1: [Name]

[Brief description]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Why rejected:** [Reason]

### Option 2: [Name]

[Same structure as Option 1]

## Consequences

### Positive

- [Good outcome 1]
- [Good outcome 2]

### Negative

- [Bad outcome or trade-off 1]
- [Mitigation strategy if any]

### Risks

- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Review

**Review date:** [When to revisit this decision]

**Triggers for review:**
- [Condition that would prompt reconsideration]
```

## Examples

### Example 1: Database Selection ADR

```markdown
# ADR-001: Use PostgreSQL for Primary Database

**Status:** Accepted

**Date:** 2024-01-15

**Deciders:** Tech Lead, Backend Team, DBA

## Context

We need a primary database for our e-commerce platform. Requirements:
- Store users, orders, products, inventory
- ACID transactions for inventory management
- Complex queries for reporting
- Expected scale: 100k users, 10k orders/day

Constraints:
- Team familiar with SQL
- AWS infrastructure
- 3-month deadline

## Decision

We will use PostgreSQL as our primary database.

## Alternatives Considered

### Option 1: MongoDB

Flexible document store with horizontal scaling.

**Pros:**
- Schema flexibility for rapid iteration
- Built-in horizontal scaling
- Good for hierarchical data

**Cons:**
- Weaker consistency guarantees
- Team has no MongoDB experience
- Complex joins require application logic

**Why rejected:** ACID transactions required for inventory; team lacks expertise.

### Option 2: DynamoDB

Fully managed NoSQL database.

**Pros:**
- Zero operational overhead
- Auto-scaling built-in
- AWS integration

**Cons:**
- Complex queries are expensive
- Vendor lock-in
- Requires denormalized schema design

**Why rejected:** Relational queries needed for reporting; cost unpredictable.

## Consequences

### Positive

- Strong consistency for financial transactions
- Rich query capabilities for analytics
- Team can start immediately (existing expertise)
- Mature tooling (backups, monitoring, ORMs)

### Negative

- Vertical scaling initially (single primary)
- Schema migrations require coordination
- May need sharding at 10x scale

### Risks

- **Scaling ceiling**: Mitigate with read replicas, then evaluate sharding at 1M users
- **Migration complexity**: Use tools like Flyway; test migrations in staging

## Review

**Review date:** 2024-07-15 (6 months)

**Triggers for review:**
- Query latency exceeds 100ms p99
- Database CPU consistently above 70%
- Team size exceeds 15 engineers
```

### Example 2: Authentication ADR

```markdown
# ADR-002: JWT-based Authentication with Redis Session Store

**Status:** Accepted

**Date:** 2024-02-01

**Deciders:** Security Lead, Backend Team

## Context

Need authentication system for multi-service architecture. Requirements:
- Support web and mobile clients
- Enable service-to-service auth
- Handle 10k concurrent users
- Support token revocation

## Decision

We will use JWT tokens for authentication with Redis for session/revocation management.

## Alternatives Considered

### Option 1: Session-based auth (cookies)

**Pros:** Simple, built-in CSRF protection, easy revocation
**Cons:** Doesn't work for mobile apps, sticky sessions required
**Why rejected:** Multi-client requirement.

### Option 2: JWT only (no Redis)

**Pros:** Stateless, scalable, simple
**Cons:** No revocation until expiry
**Why rejected:** Security requirement for immediate revocation.

## Consequences

### Positive

- Works across web/mobile/service-to-service
- Stateless verification (no DB hit for every request)
- Token payload carries user context

### Negative

- Redis adds operational complexity
- JWT size larger than session IDs
- Must handle token refresh flow

### Risks

- **Redis failure**: Mitigate with Redis Sentinel/Cluster
- **Token theft**: Short expiry (15min) + refresh tokens

## Review

**Review date:** 2024-08-01

**Triggers for review:**
- Security audit findings
- Redis operational issues
- New authentication standards emerge
```



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

### Naming Convention

```
docs/adr/
├── 0001-use-postgresql-for-database.md
├── 0002-jwt-authentication.md
├── 0003-kubernetes-for-orchestration.md
└── template.md
```

### Status Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
```

- **Proposed**: Under discussion
- **Accepted**: Decision made, being implemented
- **Deprecated**: No longer applies (context changed)
- **Superseded**: Replaced by newer ADR (link to it)

### When to Update vs. Create New

| Scenario | Action |
|----------|--------|
| Minor clarification | Edit existing ADR |
| New information emerges | Add note to existing ADR |
| Decision reversed | Create new ADR, mark old as superseded |
| Context significantly changed | Create new ADR |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too much detail | Focus on *why*, not implementation |
| Missing alternatives | Always document at least 2 options |
| No consequences | List both positive and negative outcomes |
| Stale ADRs | Set review dates, update when context changes |
| ADR for everything | Only document significant, hard-to-reverse decisions |

### Linking ADRs to Code

```python
# Authentication uses JWT with Redis session store
# See: docs/adr/0002-jwt-authentication.md
class JWTAuthenticator:
    pass
```

```yaml
# Database: PostgreSQL (ADR-0001)
database:
  type: postgresql
  host: ${DB_HOST}
```

## References

- Michael Nygard's original ADR proposal
- adr-tools: Command-line ADR management
- log4brains: ADR management with decision log
- Documenting Architecture Decisions (Thoughtworks)
