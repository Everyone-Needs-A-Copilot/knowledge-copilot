---
last_updated: 2026-06-28
status: active
---

# Security Review — [Feature / Component]

Date: YYYY-MM-DD
Author:
Risk tier: Tier 1 (Critical) | Tier 2 (High)
Reviewer (independent):

---

## Scope

<!-- What work is this review covering? Be specific.
     Include: which files, routes, or components were changed.
     Exclude: what was explicitly out of scope. -->

---

## Data Classification

<!-- What data does this feature create, read, update, or delete?
     Classify each data type. -->

| Data type | Classification | Notes |
|-----------|---------------|-------|
| | Public / Internal / Confidential / PII | |

---

## Threat Model

### Assets
<!-- What is being protected? -->

-

### Threat actors
<!-- Who might attack this surface, and what is their motivation? -->

| Actor | Motivation | Capability |
|-------|-----------|-----------|
| | | |

### Threat scenarios
<!-- For each realistic threat, describe the attack scenario. -->

| Scenario | Likelihood | Impact | Mitigation |
|----------|-----------|--------|-----------|
| | Low/Med/High | Low/Med/High | |

---

## Attack Surface

<!-- List every input, output, and integration point this feature exposes. -->

| Surface | Type | Controls in place |
|---------|------|-------------------|
| | HTTP endpoint / file input / DB query / etc. | |

---

## Always-High Surfaces (check all that apply)

- [ ] Authentication — login, session, token handling, OAuth
- [ ] File uploads — any file written to storage
- [ ] Data storage — writes to database or external storage
- [ ] PII — collection, storage, or display of personal data
- [ ] External API keys — handling of third-party credentials

If any box is checked, an independent audit lane is required (a reviewer who
did not write the code must sign off before merge).

---

## Mitigations

<!-- For each threat scenario above, describe the mitigation in detail.
     Link to the specific code, config, or process that implements it. -->

-

---

## Security Scan Results

| Scan | Result | Notes |
|------|--------|-------|
| Secrets scan | Pass / Fail | |
| Dependency scan (CVEs) | Pass / Fail / Exceptions documented | |
| SAST | Pass / Fail / Exceptions documented | |

---

## Residual Risk

<!-- What risk remains after mitigations?
     Every system has residual risk. Being honest here is more useful than claiming zero risk. -->

-

---

## Independent Audit Sign-off

<!-- Required for Tier 1 and any work touching Always-High surfaces. -->

Reviewer:
Date:
Findings:
Decision: Approved | Approved with conditions | Rejected

Conditions (if any):
