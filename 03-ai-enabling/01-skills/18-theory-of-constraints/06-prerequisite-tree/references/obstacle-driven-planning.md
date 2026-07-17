---
last_updated: 2026-04-02
status: active
---

# Obstacle-Driven Planning

## Why PRT Is Different from a Task List

A task list describes what to do. A Prerequisite Tree explains why each step is necessary.

This distinction matters because it changes how teams reason about scope, sequencing, and tradeoffs.

### The Problem with Task Lists

Task lists are activity-oriented. They answer "what will we do?" but not "why must we do it in this order?" or "what happens if we skip this step?"

When a task has no traceable obstacle behind it, two bad things happen:

1. **Scope creep is invisible.** Anyone can add a task. Nobody challenges it because the list doesn't require justification. The PRT does: every IO must trace to a named obstacle. "Nice to have" steps fail this test.

2. **Dependencies become tribal knowledge.** Experienced team members carry the dependency logic in their heads. When they say "we can't do B until A is done," they're doing PRT reasoning implicitly. Writing it down makes the logic inspectable and correctable.

### What Obstacles Reveal

Obstacles expose the WHY behind every step. When you name the obstacle, you can:

- **Challenge it.** Is this really an obstacle, or an assumption? Can we remove it rather than route around it?
- **Measure it.** When is the obstacle actually gone? The IO gives you the definition of done.
- **Deprioritize intelligently.** If the obstacle isn't real yet, the IO isn't necessary yet.

## Business Example: Launching an Enterprise Tier

A SaaS company wants to launch an enterprise tier. The initial task list looks like:

```
TODO:
- Build admin UI
- Add SSO
- Create enterprise pricing page
- Train sales team
- Write security documentation
- Set up dedicated onboarding
```

This list doesn't explain why each task exists or in what order they should run. The team debates priorities for a week.

Now the same planning done as a PRT:

**Ambitious Target:** Enterprise tier is live, generating revenue from at least 3 paying enterprise customers within the first 90 days.

**Obstacles identified:**

| ID | Obstacle | Intermediate Objective |
|----|----------|------------------------|
| O1 | We have no SSO integration | SSO authenticates users via SAML 2.0 against at least one enterprise identity provider |
| O2 | We have no admin UI for team management | Admins can invite, remove, and reassign roles to team members without contacting support |
| O3 | Enterprise pricing has not been validated | At least 3 enterprise prospects confirm willingness to pay at the proposed price point |
| O4 | Sales team has no enterprise pitch or materials | Sales deck, security FAQ, and ROI calculator are approved and practiced |
| O5 | We have no enterprise security documentation | SOC 2 readiness report or equivalent is complete and shareable under NDA |
| O6 | We have no onboarding process for multi-seat accounts | Enterprise onboarding playbook has been piloted with one real customer end-to-end |

**Dependencies:**

- O2 depends on O1 (admin UI must use SSO-authenticated roles)
- O4 depends on O3 (pitch must include validated pricing)
- O6 depends on O2 and O4 (onboarding requires admin UI and a sales motion to create customers to onboard)

**Resulting phases:**

- **Phase 1 (parallel):** O1, O3, O5 — all independent, can run concurrently
- **Phase 2 (parallel):** O2 (needs O1), O4 (needs O3) — two parallel tracks
- **Phase 3:** O6 (needs O2 and O4)

**Critical path:** O1 → O2 → O6 (or O3 → O4 → O6)

### What the PRT Reveals That the Task List Didn't

1. **O5 (security docs) is not on the critical path.** It can be done whenever, independently. The task list created false urgency around it because it appeared in sequence.

2. **O3 (pricing validation) should be first.** It's on the critical path and requires no technical work. It also de-risks O4. The task list buried it.

3. **O6 cannot start until both O2 and O4 are done.** The task list didn't show this dependency. Teams often start onboarding process design too early without the admin UI ready, then rework it.

4. **Every task is now justified.** "Build admin UI" exists because the obstacle is "we have no way for enterprise admins to manage their teams." If that obstacle doesn't matter for our first enterprise customers, maybe O2 is less urgent than it looks.

## The Planning Conversation This Changes

Without PRT:

> "Should we do SSO before admin UI, or admin UI first?"
> "I think SSO."
> "I think admin UI — our first customer asked for it."
> [30-minute debate with no resolution]

With PRT:

> "Admin UI depends on SSO because admin roles are managed via SSO identity claims. We need O1 before O2."
> "Is that actually true for our first customer? They're using Google Workspace, which is SAML-compatible."
> "Then O1 is simpler than we thought — it might be a one-week integration, not a month."
> [Focused, resolvable conversation]

## When the Obstacle List Is Wrong

The most common failure mode is an incomplete obstacle list. Signs:

- The plan keeps breaking mid-execution because "we didn't realize we needed X first"
- Obstacles are described as tasks ("build X") rather than gaps ("we lack X")
- Soft obstacles (people, knowledge, process) are missing from the list
- Dependencies feel surprising rather than obvious in retrospect

When this happens, stop and rebuild the obstacle list rather than patch the task list. The problem is not the plan — it's the map of reality the plan was built on.
