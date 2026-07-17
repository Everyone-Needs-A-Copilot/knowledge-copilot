---
last_updated: 2026-07-11
initiative: NN-slug          # MUST equal the directory name
title: Initiative Name
status: proposed             # enum: proposed | discovery | planned | active | blocked | complete | absorbed | abandoned
status_note: One-line human detail
owner: Team or person
created: YYYY-MM-DD
execution_context:           # optional; the tc/PRD join. null is valid.
  prd: null
  tasks: null
superseded_by: null          # required non-null when status is absorbed
---

# Initiative Name

> Mode: Initiative  
> Status: Proposed  
> Execution context: PRD-TBD / TASK-TBD

## Goal

State the outcome this initiative exists to produce.

## Scope

Describe the included systems, users, and decisions.

## Non-Goals

Name what this initiative will not attempt.

## Target Outcomes

- Outcome with an observable success condition.

## Phase Index

`phases/` does not exist yet — create it only when the first phase document is
written (see the lazy-creation rule in the package README), named
`phase-N-*.md` (exemplar: `../exemplars/phases/phase-1-plan.md`).

| Phase | Goal | Status | Document |
| --- | --- | --- | --- |
| Phase 1 | Define the first bounded outcome | Proposed | `phases/phase-1-plan.md` |

## Decisions

`decisions/` does not exist yet — create it only when the first ADR is
written (exemplar: `../exemplars/decisions/ADR-001-template.md`). Link
durable choices from `decisions/` once it exists.

## Validation Contract

State the rerunnable checks and external artifacts required before completion. Link the corresponding QA or validation record.

## Current Summary

Summarize the current phase and blockers. Keep live task state in the authoritative task system.
