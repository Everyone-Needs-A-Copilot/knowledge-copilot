---
last_updated: 2026-06-28
status: active
---

# Definition of Done

> A piece of work is **Done** only when every applicable item below is verified —
> not assumed, not estimated, not delegated to "later." Verified.

---

## A) Experience + Design

These items confirm the implementation matches the approved design intent.

- [ ] Meets approved design intent — CDO approval has been given, within design system rules
- [ ] No view or layout integrity issues at core breakpoints (mobile, tablet, desktop)
- [ ] Mobile friendliness validated on a real device or accurate emulator
- [ ] Accessibility validated against WCAG AA — keyboard navigation, colour contrast,
      screen reader compatibility, focus management

If the approved prototype did not cover this view or interaction, stop. Resolve
design intent before shipping.

---

## B) Engineering Quality

These items confirm the code is clean, tested, and will not silently break other things.

- [ ] Lint and format checks pass with no suppressed warnings
- [ ] Unit tests pass — new behaviour has new test coverage
- [ ] Integration tests pass — existing integrations have not regressed
- [ ] E2E smoke tests pass — the critical user journeys work end-to-end

Tests that are skipped or marked pending do not count. If a test is failing and
the decision is to skip it, that decision must be documented and approved.

---

## C) Security

Security checks are non-negotiable. They apply to every piece of work, not just
features explicitly categorised as security-relevant.

- [ ] Secrets scanning clean — no credentials, API keys, or tokens in source
- [ ] Dependency scanning clean — no Critical or High CVEs. If exceptions exist,
      each is documented with rationale and approved in writing
- [ ] SAST clean — no static analysis findings. If exceptions exist, each is
      documented with rationale and approved in writing
- [ ] If auth, file uploads, data storage, or any PII surface was touched:
      independent audit lane completed before merge

See `RISK-CLASSIFICATION.md` for which surfaces always trigger the audit lane.

---

## D) Operational Verification

These items confirm the implementation works in its running state, not just in
tests.

- [ ] Browser JavaScript console: no errors (warnings reviewed; none suppressed without reason)
- [ ] Terminal / server logs: no runtime errors or unexpected warnings
- [ ] View inspected in browser: no broken layouts, missing assets, or visual regressions

---

## Exceptions

If any item is not applicable to a specific piece of work, document why in the
PR or task. "Not applicable" is a decision, not a default. Blanket exceptions
are not accepted.

If anything on this checklist is unverified, the work is not done.
