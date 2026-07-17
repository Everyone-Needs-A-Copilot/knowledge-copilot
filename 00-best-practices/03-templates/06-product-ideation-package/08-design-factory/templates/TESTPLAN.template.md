---
last_updated: 2026-06-28
status: active
---

# Test Plan — [Feature / Milestone]

Date: YYYY-MM-DD
Author:
Scope: Feature | Milestone | Release candidate
Risk tier: Tier 1 | Tier 2 | Tier 3

---

## Scope

<!-- What is being tested? What is explicitly not being tested?
     Reference the relevant spec or gate. -->

### In scope
-

### Out of scope
-

---

## Strategy

<!-- How will testing be structured? Which types of tests apply?
     Justify any types that are skipped. -->

| Test type | Applies | Justification if skipped |
|-----------|---------|------------------------|
| Unit tests | Yes / No | |
| Integration tests | Yes / No | |
| E2E smoke tests | Yes / No | |
| Security scans | Yes / No | |
| Manual exploratory | Yes / No | |
| Accessibility audit | Yes / No | |
| Performance check | Yes / No | |

---

## Journey-Based Test Cases

<!-- Organise tests by the user journeys they validate.
     This keeps the test plan connected to real user outcomes. -->

### Journey 1: [Name]
<!-- Describe the journey in one sentence -->

| # | Step | Expected outcome | Pass criteria |
|---|------|-----------------|--------------|
| 1 | | | |

### Journey 2: [Name]

| # | Step | Expected outcome | Pass criteria |
|---|------|-----------------|--------------|
| 1 | | | |

---

## E2E Smoke Tests (Must Always Pass)

<!-- These are the minimum tests that must pass before any merge to main.
     If these fail, the build is blocked. -->

- [ ]
- [ ]

---

## Unit Test Areas

<!-- Which logic units require isolated unit tests?
     Focus on: business logic, calculations, transformations, edge cases. -->

-

---

## Integration Test Areas

<!-- Which integrations need verified against real (or realistic stub) dependencies?
     Focus on: external APIs, database interactions, auth flows. -->

-

---

## Security Test Notes

<!-- Required for Tier 1 and Tier 2. Fill in results when scans are run. -->

| Scan | Tool | Result | Notes |
|------|------|--------|-------|
| Secrets scan | | Pass / Fail | |
| Dependency scan | | Pass / Fail / Exceptions | |
| SAST | | Pass / Fail / Exceptions | |

---

## Test Environment

<!-- Where are tests run? What data, accounts, or configuration is needed? -->

| Environment | Purpose | Notes |
|-------------|---------|-------|
| Local | Unit + integration | |
| Staging | E2E + manual exploratory | |
| Production | Smoke only post-deploy | |

---

## Known Risks

<!-- What could cause tests to give false confidence?
     e.g. test data that doesn't reflect real data, mocked services that behave differently in prod -->

-

---

## Regression Notes

<!-- Which existing features could be broken by this work?
     List the areas to spot-check in addition to the new test cases. -->

-
