---
last_updated: 2026-02-25
status: active
name: technology-selection
description: Systematically evaluate and select technologies (frameworks, databases, tools) based on requirements, constraints, and team capabilities. Use when choosing between competing technical options.
triggers:
  files: ["**/docs/tech-stack/**", "**/ADR/**", "**/architecture/**", "**/tech-selection*.md"]
  keywords: ["technology selection", "tech stack", "choose framework", "select database", "evaluate tools", "compare technologies", "which technology", "framework comparison"]
allowed-tools: Read, Write, Edit
---

# Technology Selection

## Overview

Technology selection impacts development velocity, operational cost, team morale, and system longevity. Poor choices create technical debt; good choices enable teams to move fast and maintain quality.

This skill provides a systematic framework for evaluating and selecting technologies. It emphasizes requirements over hype, team fit over perfection, and reversibility over commitment.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Instructions

### Step 1: Define Requirements

Before evaluating options, clarify what you need:

| Requirement Type | Questions |
|------------------|-----------|
| **Functional** | What must it do? |
| **Non-functional** | Performance, scalability, security needs? |
| **Integration** | What must it work with? |
| **Compliance** | Regulatory or policy constraints? |
| **Timeline** | When do we need it working? |
| **Budget** | Cost constraints? |

### Step 2: Identify Constraints

Constraints narrow the option space:

| Constraint | Impact |
|------------|--------|
| Team skills | Limits viable technologies |
| Existing infrastructure | Favors compatible tech |
| Vendor requirements | May mandate specific tools |
| Security policies | Eliminates some options |
| Support requirements | May require enterprise editions |
| Geographic | Data residency, latency |

### Step 3: Establish Evaluation Criteria

Define weighted criteria before evaluating:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Fit | High | Solves the actual problem |
| Team expertise | High | Team can use it effectively |
| Maturity | Medium | Production-proven, stable API |
| Community | Medium | Documentation, support, talent pool |
| Cost | Medium | License, infrastructure, training |
| Maintenance | Medium | Ongoing effort required |
| Exit cost | Low | Difficulty of switching later |

### Step 4: Evaluate Candidates

Score each option against criteria:

| Technology | Fit | Team | Maturity | Community | Cost | Total |
|------------|-----|------|----------|-----------|------|-------|
| Option A | 8 | 9 | 7 | 8 | 9 | 8.2 |
| Option B | 9 | 5 | 8 | 9 | 7 | 7.6 |
| Option C | 7 | 8 | 9 | 9 | 8 | 8.2 |

### Step 5: Prototype If Needed

For significant decisions, build a proof-of-concept:

| Test | Purpose |
|------|---------|
| Hello World | Development experience |
| Core use case | Functional fit |
| Edge case | Handles complexity |
| Integration | Works with existing systems |
| Performance | Meets non-functional requirements |

### Step 6: Document Decision

Use ADR format (see architecture-decision-records skill).

## Technology Evaluation Matrix

### Databases

| Type | Use When | Examples |
|------|----------|----------|
| **Relational** | Structured data, ACID, complex queries | PostgreSQL, MySQL |
| **Document** | Flexible schema, hierarchical data | MongoDB, CouchDB |
| **Key-Value** | Simple lookups, caching | Redis, DynamoDB |
| **Column** | Time-series, analytics, high write | Cassandra, ClickHouse |
| **Graph** | Relationships, traversals | Neo4j, ArangoDB |
| **Search** | Full-text search, facets | Elasticsearch, Algolia |

### Web Frameworks

| Criterion | Questions to Ask |
|-----------|------------------|
| Language fit | Does team know the language? |
| Performance | Request throughput needs? |
| Ecosystem | Available libraries, middleware? |
| Hiring | Can we find developers? |
| Longevity | Will it exist in 5 years? |

### Cloud vs Self-Hosted

| Factor | Cloud (Managed) | Self-Hosted |
|--------|-----------------|-------------|
| Ops effort | Low | High |
| Cost at scale | Higher | Lower |
| Customization | Limited | Full |
| Vendor lock-in | Yes | No |
| Time to start | Fast | Slow |

### Buy vs Build Decision

```
┌─────────────────────────────────────────────────────┐
│                    Is it core to                    │
│                    your business?                   │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │ Yes                     │ No
          ▼                         ▼
┌─────────────────┐      ┌─────────────────────────────┐
│     BUILD       │      │ Does a good solution exist? │
│                 │      └──────────────┬──────────────┘
│ Competitive     │                     │
│ advantage       │          ┌──────────┴──────────┐
│ requires        │          │ Yes                 │ No
│ ownership       │          ▼                     ▼
└─────────────────┘   ┌───────────┐         ┌───────────┐
                      │    BUY    │         │   BUILD   │
                      │           │         │ (simple)  │
                      │ Faster,   │         └───────────┘
                      │ proven    │
                      └───────────┘
```

## Technology Selection Template

```markdown
## Technology Selection: [Category]

### Requirements

**Functional:**
- [Requirement 1]
- [Requirement 2]

**Non-functional:**
- [Performance requirement]
- [Scalability requirement]

### Constraints

- [Constraint 1]
- [Constraint 2]

### Evaluation Criteria

| Criterion | Weight (1-5) | Notes |
|-----------|--------------|-------|
| [Criterion 1] | 5 | Critical |
| [Criterion 2] | 3 | Important |

### Candidates

| Option | [Criterion 1] | [Criterion 2] | Weighted Score |
|--------|---------------|---------------|----------------|
| [Tech A] | 4 | 3 | |
| [Tech B] | 3 | 5 | |

### Recommendation

[Technology] because [reasons].

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Mitigation] |

### Proof of Concept Results

[If applicable]
```

## Examples

### Example 1: Database Selection

```markdown
## Technology Selection: Primary Database

### Requirements

**Functional:**
- Store users, orders, products
- Complex queries for reporting
- Transactional integrity for payments

**Non-functional:**
- 10k orders/day
- 100ms query latency p99
- 99.9% availability

### Constraints

- Team has SQL expertise
- AWS infrastructure
- 3-month timeline
- $500/month budget initially

### Evaluation Criteria

| Criterion | Weight | Notes |
|-----------|--------|-------|
| ACID support | 5 | Required for payments |
| Team expertise | 5 | Faster development |
| Query flexibility | 4 | Reporting needs |
| Managed option | 3 | Reduce ops burden |
| Cost | 3 | Budget constrained |

### Candidates

| Database | ACID | Team | Queries | Managed | Cost | Total |
|----------|------|------|---------|---------|------|-------|
| PostgreSQL | 5 | 5 | 5 | 4 | 4 | 4.7 |
| MySQL | 5 | 5 | 4 | 5 | 5 | 4.7 |
| MongoDB | 3 | 2 | 3 | 5 | 4 | 3.2 |
| DynamoDB | 2 | 2 | 2 | 5 | 3 | 2.6 |

### Recommendation

PostgreSQL (AWS RDS) because:
- Strong ACID support for payment transactions
- Team already proficient in PostgreSQL
- Rich query capabilities for reporting
- AWS RDS provides managed option with reasonable cost

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Scaling limits | Start with read replicas; evaluate sharding at 10x scale |
| RDS cost at scale | Reserved instances; consider Aurora if cost-effective |
```

### Example 2: Frontend Framework

```markdown
## Technology Selection: Frontend Framework

### Requirements

**Functional:**
- Single-page application
- Complex forms with validation
- Real-time updates
- Mobile-responsive

**Non-functional:**
- Initial load < 3s
- Support IE11 (legacy requirement)

### Constraints

- Team knows JavaScript (some React experience)
- Must integrate with existing REST API
- 2-month timeline

### Evaluation Criteria

| Criterion | Weight | Notes |
|-----------|--------|-------|
| Team experience | 5 | Fast ramp-up |
| Ecosystem | 4 | Available components |
| Performance | 4 | Initial load time |
| IE11 support | 3 | Legacy requirement |
| Hiring pool | 3 | Future team growth |

### Candidates

| Framework | Team | Ecosystem | Perf | IE11 | Hiring | Total |
|-----------|------|-----------|------|------|--------|-------|
| React | 4 | 5 | 4 | 4 | 5 | 4.4 |
| Vue | 2 | 4 | 5 | 4 | 3 | 3.5 |
| Angular | 2 | 4 | 3 | 5 | 4 | 3.4 |
| Svelte | 1 | 3 | 5 | 3 | 2 | 2.7 |

### Recommendation

React because:
- Team has existing React experience
- Largest ecosystem (component libraries, tooling)
- Strong hiring pool for team growth
- IE11 support via polyfills

### Proof of Concept Results

- Built login form in 4 hours (vs 2 days estimated for Vue)
- Integration with existing auth API straightforward
- Bundle size acceptable (150KB gzipped with tree-shaking)
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

### Red Flags in Technology Selection

| Red Flag | Problem |
|----------|---------|
| "It's what Google uses" | Your scale isn't Google's scale |
| "It's the newest thing" | Newer ≠ better; maturity matters |
| "Everyone is switching to X" | Hype cycles mislead |
| "We can learn it" | Underestimates learning curve |
| "It's free" | Total cost includes ops, training |
| "Vendor said so" | Vendors have sales targets |

### Questions to Ask

1. **Fit**: Does it actually solve our problem?
2. **Team**: Can our team use it effectively?
3. **Maturity**: Is it production-proven?
4. **Support**: What happens when things break?
5. **Exit**: How hard is it to switch later?
6. **Future**: Will it exist and be maintained in 5 years?

### When to Reconsider

- Requirements significantly change
- Team composition changes
- Technology is deprecated or abandoned
- Better alternatives emerge
- Scale exceeds original assumptions

### Avoiding Common Mistakes

| Mistake | Remedy |
|---------|--------|
| Resume-driven development | Focus on solving the problem, not learning new tech |
| Analysis paralysis | Set a deadline; "good enough" is often good enough |
| Ignoring team input | Those who use it should have a voice |
| Skipping proof-of-concept | Test critical assumptions before committing |
| Not documenting decision | Future team will ask "why?" |

## References

- Thoughtworks Technology Radar
- StackOverflow Developer Survey
- ThoughtWorks Technology Advisory Board
- CNCF Landscape (for cloud-native)
