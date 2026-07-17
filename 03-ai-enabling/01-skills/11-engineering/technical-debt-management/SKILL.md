---
last_updated: 2026-02-25
status: active
name: technical-debt-management
description: Identify, categorize, and strategically pay down technical debt. Activate when assessing codebase health or planning debt reduction.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go", "**/*.md"]
  keywords: ["technical debt", "tech debt", "legacy code", "code quality", "maintenance", "refactor priority", "codebase health", "cruft"]
allowed-tools: Read, Write, Edit
---

# Technical Debt Management

Strategic approach to identifying, tracking, and paying down technical debt. Balance short-term delivery with long-term sustainability.

## Understanding Technical Debt

Technical debt is the implied cost of additional rework caused by choosing an easy solution now instead of a better approach that takes longer.

### Debt Quadrant

| | Deliberate | Inadvertent |
|---|------------|-------------|
| **Prudent** | "We must ship now and deal with consequences" | "Now we know how we should have done it" |
| **Reckless** | "We don't have time for design" | "What's layering?" |

**Prudent deliberate debt** is acceptable. **Reckless debt** is a red flag.

---


## Define Done

- [ ] Solution addresses the root cause, not just symptoms
- [ ] Code is readable, testable, and follows project conventions
- [ ] Performance implications understood and acceptable
- [ ] Error handling covers likely failure modes

## 1. Identifying Technical Debt

### Code-Level Indicators

| Indicator | What It Reveals |
|-----------|-----------------|
| TODO/FIXME/HACK comments | Known shortcuts |
| Suppressed warnings | Ignored problems |
| Copy-paste code | Missing abstraction |
| Long methods/classes | Poor modularization |
| Low test coverage | Risk zone |
| Complex conditionals | Logic sprawl |

### System-Level Indicators

| Indicator | What It Reveals |
|-----------|-----------------|
| Long build times | Architecture problems |
| Flaky tests | Coupling or timing issues |
| Deployment frequency | Risk aversion |
| Bug rate in specific areas | Code hotspots |
| Onboarding time | Complexity |

### Metrics to Track

```
Code churn     = lines changed / total lines
Hotspot        = files with high churn + high complexity
Coupling       = files that change together
Test coverage  = tested lines / total lines
Cyclomatic complexity = independent paths through code
```

---

## 2. Categorizing Debt

### By Impact

| Category | Description | Priority |
|----------|-------------|----------|
| **Blocking** | Prevents feature work | Immediate |
| **Slowing** | Makes development harder | High |
| **Annoying** | Minor friction | Medium |
| **Cosmetic** | Style/formatting | Low |

### By Type

| Type | Examples | Resolution |
|------|----------|------------|
| **Design debt** | Wrong patterns, missing layers | Refactor architecture |
| **Code debt** | Smells, duplication | Refactor code |
| **Test debt** | Low coverage, flaky tests | Add/fix tests |
| **Documentation debt** | Missing/outdated docs | Update docs |
| **Dependency debt** | Outdated libraries | Upgrade dependencies |
| **Infrastructure debt** | Manual processes | Automate |

---

## 3. Prioritizing Paydown

### Interest Rate Framework

Prioritize debt with highest "interest" - code that:

1. **Blocks planned work** - Must fix to proceed
2. **Changes frequently** - High-churn hotspots
3. **Causes bugs** - Quality issues
4. **Slows development** - Friction multiplier

### Prioritization Matrix

```
                     HIGH IMPACT
                          │
         Quick Wins       │    Strategic
         (Do now)         │    (Plan for)
                          │
    LOW ──────────────────┼────────────────── HIGH
    EFFORT                │                  EFFORT
                          │
         Fill-ins         │    Reconsider
         (When time)      │    (Maybe never)
                          │
                     LOW IMPACT
```

### Questions to Ask

- How often does this code change?
- How many developers touch it?
- What's the bug rate?
- Does it block upcoming work?
- What's the cost to fix vs. cost to leave?

---

## 4. Paydown Strategies

### Boy Scout Rule

"Leave the code better than you found it."

Make small improvements with every change:
- Rename unclear variable
- Extract small method
- Add missing test
- Fix one warning

### Dedicated Time

| Approach | When to Use |
|----------|-------------|
| **20% time** | Continuous improvement |
| **Tech debt sprints** | Accumulated debt |
| **Pre-feature cleanup** | Debt in feature area |
| **Post-incident fixes** | Debt caused incidents |

### Strangler Fig Pattern

Gradually replace legacy system:

1. Create new implementation alongside old
2. Route new traffic to new implementation
3. Migrate existing traffic incrementally
4. Remove old implementation when empty

### Branch by Abstraction

1. Create abstraction over existing implementation
2. Clients use abstraction
3. Create new implementation behind abstraction
4. Switch over
5. Remove old implementation

---

## 5. Tracking Debt

### Debt Register

Track debt items with:

```markdown
| ID | Description | Type | Impact | Effort | Interest | Status |
|----|-------------|------|--------|--------|----------|--------|
| D-001 | Payment module lacks tests | Test | High | M | High | In progress |
| D-002 | Duplicate validation logic | Code | Medium | S | Medium | Backlog |
| D-003 | Manual deployment process | Infra | High | L | High | Planned |
```

### ADR for Debt Decisions

Record deliberate debt decisions:

```markdown
# ADR-042: Accept payment retry debt

## Status: Accepted

## Context
We need to ship payment feature by Q1.

## Decision
Ship with simple retry logic. Proper exponential backoff deferred.

## Consequences
- May hit rate limits under load
- Must address before scaling
- Tracking as DEBT-087

## Payoff Plan
Address in Q2 reliability sprint.
```

---

## 6. Prevention

### Design Reviews

Catch debt before it's created:
- Architecture decision records
- Design doc reviews
- Proof of concepts for risky areas

### Definition of Done

Include quality gates:
- [ ] Tests written
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Reviewed for complexity

### Continuous Monitoring

- Static analysis in CI
- Test coverage gates
- Complexity metrics
- Dependency vulnerability scanning

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| "Big bang" rewrites | High risk, delayed value |
| Ignoring debt until crisis | Compounds interest |
| Fixing everything at once | Never ships |
| No tracking | Forgotten and repeated |
| Blaming individuals | Debt is systemic |

---

## Quick Reference

**Identify:** Code smells, metrics, hotspots, team friction

**Categorize:** Blocking > Slowing > Annoying > Cosmetic

**Prioritize:** High interest first (frequent changes, bug source, blocks work)

**Pay down:** Boy Scout rule + dedicated time + strategic patterns

**Prevent:** Reviews, DoD, CI quality gates, monitoring

Technical debt is normal. Unmanaged debt is dangerous. Make debt visible, track it, and pay it down strategically.


## Quality Tests

### Correctness Test
- Solution produces correct results for all specified inputs
- **PASS:** Happy path, edge cases, and error cases all handled correctly
- **FAIL:** Works for common cases but breaks on edge cases or errors

### Maintainability Test
- Another developer can understand and modify the code
- **PASS:** Clear naming, single responsibility, minimal coupling
- **FAIL:** Complex logic without explanation, or high coupling to other modules

