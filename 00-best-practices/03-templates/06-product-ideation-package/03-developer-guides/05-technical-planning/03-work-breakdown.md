---
last_updated: 2026-06-28
status: active
---

# Work Breakdown

<!--
FACTORY AGENTS: CTO + TA (Tech Architect)
==========================================
This document is NOT facilitated. It is generated jointly by the CTO and TA agents
as the final synthesis document in the technical planning sequence.

The CTO sets the phase structure and the strategic sequencing — what delivers
value and when, and what must be true about Phase 1 for Phases 2 and 3 to be
buildable without breaking changes. The TA fills in the component details,
complexity ratings, and cross-phase dependency constraints.

This document must be written AFTER all other technical planning documents are complete.
It synthesises every prior document into a sequenced build plan.

INPUTS (read all before writing, in this order):
- 00-overview/00-vision.md
    The product's "one thing." Phase 1 must deliver this.
- 00-overview/10-scope-and-non-goals.md
    Scope defines what is in Phase 1; non-goals are explicitly not built in any phase
    unless the scope changes.
- 00-overview/20-success-metrics.md
    Each phase's success criteria must map to at least one success metric from this document.
- 03-developer-guides/30-requirements/10-user-stories.md
    P0 stories are Phase 1; P1 stories are Phase 2; P2 stories are Phase 3.
- 03-developer-guides/30-requirements/30-acceptance-criteria.md
    Acceptance criteria define what "done" means for each story.
- 03-developer-guides/60-e2e-mapping/00-e2e-journeys.md
    The journey stages map to phases: early stages are Phase 1 minimum.
- 03-developer-guides/60-e2e-mapping/10-view-map.md
    Critical views (CV# assigned) are Phase 1. Non-critical views are Phase 2+.
    Empty and error states are Phase 1 — never defer them.
- 04-architecture/10-data-model.md
    Foundational entities required for Phase 1 features to work go in Phase 1.
- 04-architecture/20-architecture.md
    The "Essential Minimum" section is Phase 1.
- 03-developer-guides/70-technical-planning/30-test-plan.md
    Test infrastructure is Phase 1. It is never deferred.
- 03-developer-guides/70-technical-planning/40-security.md
    Baseline security (auth, TLS, secrets management, input validation) is Phase 1.

GATE: G8 — Technical Plan Approved
This is the final document before implementation begins. It must be approved before
any code is written. Changes to this document after G8 require a documented ADR.

PROCESS:
1. Read the vision. Write one sentence per phase: what capability becomes possible
   that was impossible before?
2. Read the scope. Map every in-scope capability to a phase.
3. Read user stories. Assign P0 to Phase 1. Decide on each P1. Document exceptions.
4. Read the view map. Assign critical views to Phase 1. Non-critical to Phase 2.
   Empty/error states always Phase 1.
5. Read the data model. Foundational entities in Phase 1. Evolving entities in their
   respective phases.
6. Read the architecture essential minimum — all of it is Phase 1.
7. Map cross-phase dependencies. If Phase 2 needs a Phase 1 DB column, add it to
   Phase 1 deliverables now to avoid a breaking migration later.
8. Write success criteria per phase. Each criterion must map to an acceptance
   criterion and be objectively testable.
9. Write deliverables per phase. A deliverable is a demonstrable thing — not a task.

STYLE:
- No time estimates. No durations. No dates. Use complexity ratings instead.
- Complexity: Low / Medium / High / Very High (captures risk and interdependency,
  not effort in hours).
- Priority: Must / Should / Could (MoSCoW, simplified to three levels).
- A phase delivers a meaningful increment of value — not a collection of tickets.
- Deliverables are nouns. "A working dashboard" not "implement the dashboard."
- The cross-phase dependency section is critical. The CTO is responsible for ensuring
  Phase 1 decisions do not require Phase 2 to undo Phase 1 work.
-->

## Phase Structure

| Phase | Name | What this phase makes possible |
|-------|------|---------------------------------|
| Phase 1 | MLP Core Workflow | [A user can do the core workflow end-to-end — the full value proposition is demonstrable] |
| Phase 2 | Intelligence Layer | [The system becomes configurable; AI features are fully context-aware; a real client can complete a full cycle] |
| Phase 3 | Ecosystem Integration | [The system supports team collaboration, higher volume, and connections to external workflows] |

**Gate:** All three phases together represent the full product vision. Phase 1 alone is the minimum lovable product. A client can do real work in Phase 1 — the experience is complete, not a preview.

---

## Phase 1: MLP Core Workflow

Phase 1 delivers the core end-to-end workflow. The product is demonstrably useful by the end of Phase 1.

### Components

| Component | Features | Priority | Complexity | Story IDs |
|-----------|---------|---------|-----------|----------|
| **Database schema** | All Phase 1 entities | Must | Medium | — |
| **[Core pipeline component]** | [Core capability] | Must | High | [Story IDs] |
| **Authentication** | User login; session management; `HttpOnly` cookie; route protection; minimum roles | Must | Medium | — |
| **[Primary dashboard view]** | [Core display capability] | Must | Medium | [Story IDs] |
| **[Core workflow view]** | [Core action capability] | Must | Medium | [Story IDs] |
| **[Editor / creator view]** | [Creation capability] | Must | Very High | [Story IDs] |
| **[Review view]** | [Review capability] | Must | Low | [Story IDs] |
| **[Export / output]** | [Output generation] | Must | Medium | [Story IDs] |
| **Settings — [Category]** | [Core configuration] | Must | Medium | [Story IDs] |
| **Empty states** | [Primary empty state with call to action] | Must | Low | — |
| **Error states** | [Core error states] | Must | Low | — |
| **Test infrastructure** | Unit test runner; integration test setup with test database; E2E suite; CI pipeline with blocking gate | Must | Medium | — |
| **Security baseline** | HTTPS enforcement; HSTS; `HttpOnly`/`Secure`/`SameSite` cookies; environment-variable secrets; CORS restricted to own origin; input validation on all API routes; dependency scan in CI | Must | Medium | — |

### Out of Scope for Phase 1

| Item | Reason | Deferred to |
|------|--------|------------|
| [Advanced configuration UI] | Core version works with defaults in Phase 1 | Phase 2 |
| [Advanced intelligence features] | Foundational data exists; enrichment is Phase 2 | Phase 2 |
| [Collaboration features] | Single-user workflow is Phase 1 | Phase 3 |

### Phase 1 Success Criteria

Each criterion maps to an acceptance criterion in `03-developer-guides/30-requirements/30-acceptance-criteria.md`. A phase is not complete until every criterion is verified — not assumed.

| Criterion | Acceptance condition | AC / Story ref |
|-----------|---------------------|---------------|
| [Core pipeline works] | [Observable end state] | [Story ID] |
| [Core display works] | [Observable end state] | [Story ID] |
| [Core workflow completes] | [Observable end state] | [Story ID] |
| [Output is generated] | [Observable end state] | [Story ID] |
| E2E smoke test passes | ST-001 (full happy path smoke test) passes in a staging environment without console errors | Test plan ST-001 |
| Security baseline verified | Dependency scan clean; secret scan clean; protected routes reject unauthenticated requests | 40-security.md |

### Phase 1 Deliverables

When Phase 1 is complete, the following can be demonstrated without qualification:

- A running application accessible at a staging URL
- The complete primary journey navigable end to end with one user
- A CI pipeline that passes: unit tests, integration tests, E2E smoke test, dependency scan, secret scan

---

## Phase 2: Intelligence Layer

Phase 2 makes the system's intelligence configurable and the core experience genuinely powerful. A client can complete a full cycle, configured for their specific context.

### Components

| Component | Features | Priority | Complexity | Depends On |
|-----------|---------|---------|-----------|-----------|
| **[Advanced configuration UI]** | [Full configuration capability] | Must | High | Phase 1 data model; Phase 1 settings shell |
| **[Intelligence enrichment]** | [Background intelligence job] | Must | High | Phase 1 core entity |
| **[Enhanced context]** | [Context-aware AI features] | Must | High | Phase 1 core AI interface |
| **[Advanced review workflow]** | [Full reviewer experience] | Should | High | Phase 1 review view |
| **[Notification surface]** | [In-app alerts] | Should | Medium | Phase 1 pipeline |

### Out of Scope for Phase 2

| Item | Deferred to |
|------|------------|
| Team collaboration | Phase 3 |
| Semantic search | Phase 3 |
| Additional export formats | Phase 3 |

### Phase 2 Success Criteria

| Criterion | Acceptance condition |
|-----------|---------------------|
| [Core configuration is usable] | [Observable end state] |
| [Intelligence enriches the experience] | [Observable end state] |
| [Full cycle is completable] | [Observable end state] |

---

## Phase 3: Ecosystem Integration

Phase 3 extends the system beyond a single user and a single session.

### Components

| Component | Features | Priority | Complexity | Depends On |
|-----------|---------|---------|-----------|-----------|
| **Team Collaboration** | [Collaboration features] | Should | Very High | Phase 1 user model; Phase 1 core editor |
| **[Additional source/input adapters]** | [Extended input coverage] | Should | High | Phase 1 core pipeline architecture |
| **Semantic Search** | [Embedding-based search] | Could | High | Phase 1 database with vector extension |
| **Pipeline Scaling** | [Dedicated job queue service] | Should | High | Phase 1 background worker architecture designed as a separate process |
| **[Additional export formats]** | [More output formats] | Could | High | Phase 1 export pipeline |
| **Audit Trail View** | [Queryable log of key actions] | Should | Medium | Phase 1 timestamps on all entities |

### Phase 3 Success Criteria

| Criterion | Acceptance condition |
|-----------|---------------------|
| Team collaboration is usable | Two users can work on different sections without conflicts |
| Pipeline handles production volume | The system processes [N]+ items per day without delays |

---

## Cross-Phase Dependency Diagram

The following Phase 1 decisions constrain Phase 2 and Phase 3. They must be implemented correctly in Phase 1 to prevent breaking migrations later.

```
Phase 1 Implementation Decision
        │
        ├── Vector extension installed at schema creation
        │     └── Enables: Phase 3 Semantic Search
        │           Without this: adding vector extension to a production DB is a migration risk
        │
        ├── [Core config entity] exists in Phase 1 (even with one default)
        │     └── Enables: Phase 2 Configuration UI
        │           Without this: Phase 2 requires a refactor from hardcoded to data-driven
        │
        ├── Background workers run as a separate process from the web server
        │     └── Enables: Phase 3 Pipeline Scaling
        │           Without this: extracting workers to a dedicated queue requires infrastructure surgery
        │
        ├── createdAt + updatedAt timestamps on every entity
        │     └── Enables: Phase 3 Audit Trail View
        │           Without this: retroactive timestamp backfills on production data
        │
        └── User.role implemented in Phase 1 (minimum roles)
              └── Enables: Phase 2 additional roles; Phase 3 Team Collaboration
                    Without this: adding role-based access later requires retrofitting every route
```

### Cross-Phase Breaking Change Rules

These constraints apply to all phases after Phase 1:

1. **API contract stability**: Route paths and response shapes defined in `04-architecture/20-architecture.md` must not change without a versioned migration plan and a documented ADR.

2. **Database migration safety**: Every Phase 2 or 3 database migration must be backward-compatible with Phase 1 data. No destructive column renames or drops without a documented two-step migration (add new → migrate data → drop old).

3. **No silent deferrals**: If a Phase 1 component is deferred to Phase 2 during implementation, it must be documented in this file as an explicit exception, approved by the CTO, and reflected in the Phase 1 success criteria.

---

## Deliverable Summary

| Phase | Status | Key deliverable |
|-------|--------|----------------|
| Phase 1 — MLP Core Workflow | [ ] Not started | [Full E2E primary workflow: discovery → processing → evaluation → action → output] |
| Phase 2 — Intelligence Layer | [ ] Not started | [Configurable intelligence + full reviewer workflow] |
| Phase 3 — Ecosystem Integration | [ ] Not started | [Team collaboration + production pipeline volume] |

**Gate G8 is passed when this document is approved by the CTO and the project owner. Implementation does not begin before G8.**
