---
last_updated: 2026-06-28
status: active
---

# Risk Classification

> Every piece of work is assigned a risk tier before it is started.
> The tier determines the minimum review and audit requirements.
> Tiers cannot be downgraded without documented rationale and project owner approval.

---

## Tier 1 — Critical

Work that directly touches authentication, payments, PII, or external API keys.

**Surfaces that are always Tier 1:**

| Surface | Examples |
|---------|---------|
| Authentication | Login, session management, token handling, OAuth flows, password reset |
| Payments | Any integration with payment processors, billing, invoicing |
| PII | Collection, storage, display, or transmission of personally identifiable information |
| External API keys | Storage or use of third-party API credentials (LLM providers, external services, etc.) |

**What Tier 1 requires:**

- Full test suite (unit, integration, E2E) must pass
- Security scans: secrets scan, dependency scan, SAST — all clean
- **Independent audit lane:** a separate agent or reviewer who did not write the
  code must review and sign off before merge. Self-review does not satisfy this.
- Project owner informed before merge

---

## Tier 2 — High

Work that mutates data, handles file uploads, or enforces access control.

**Surfaces that are always Tier 2:**

| Surface | Examples |
|---------|---------|
| Data mutations | Create, update, delete operations on any persisted data |
| File uploads | Document ingestion, attachment handling, any file written to storage |
| Role-based access | Permission checks, feature flags by role, admin-only routes |
| External integrations | API calls to third-party services that have side effects |

**What Tier 2 requires:**

- Full test suite must pass
- Security scans: secrets scan, dependency scan — both clean
- Enhanced code review: reviewer must explicitly check the mutation logic,
  error handling, and failure modes — not just that the feature works when
  things go right
- If the work touches auth, uploads, storage, or PII even incidentally,
  escalate to Tier 1

---

## Tier 3 — Standard

Read-only views, static content, and UI components with no data side effects.

**Typical Tier 3 work:**

| Surface | Examples |
|---------|---------|
| Read-only views | Dashboard displays, search results, detail pages (read only) |
| Static content | Marketing copy, help text, empty states |
| UI components | Buttons, cards, typography, spacing adjustments with no logic |
| Refactoring | Internal restructuring with no behaviour change (must be verified) |

**What Tier 3 requires:**

- Lint and format clean
- Unit tests pass (new components have snapshot or behaviour tests)
- E2E smoke tests pass — existing journeys have not regressed
- Standard code review

---

## Escalation Rule

When in doubt, escalate. Downgrading a tier requires explicit justification.

If a piece of work starts as Tier 3 and during implementation touches an
authentication check, a database write, or a user's data — it escalates
to the appropriate tier immediately. The reviewer is responsible for catching
this if the implementer misses it.

---

## Tier Summary

| Tier | Label | Key surfaces | Minimum gate |
|------|-------|-------------|-------------|
| 1 | Critical | Auth, payments, PII, API keys | Independent audit + full scans + full tests |
| 2 | High | Data mutations, uploads, RBAC | Enhanced review + security scans + full tests |
| 3 | Standard | Read-only, static, UI components | Standard review + lint + smoke tests |
