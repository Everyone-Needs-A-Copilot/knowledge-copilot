---
last_updated: 2026-06-28
status: active
---

# Product Technical Docs Template

Use this structure for each product so teams and AI projects know where to find technical details. Place files under `02-products/<product-slug>/`.

## Required Files
- `00-overview.md` – Product description, who it's for, high-level value (existing marketing/overview content).
- `10-architecture.md` – System context, components, data flows, non-functional requirements (diagrams encouraged).
- `20-deployment.md` – Environments, platform, deploy process, env vars/secrets, post-deploy checks.
- `30-operations.md` – Monitoring/logging, backups, runbooks, maintenance.
- `40-integrations.md` – External services, auth providers, webhooks, data imports/exports.
- `50-api.md` – Endpoints/contracts/rate limits (mark N/A if not applicable).
- `60-security.md` – Data classification, access controls, secrets, auditing; reference `03-ai-enabling/03-operations/02-security-guidelines.md`.
- `70-decisions.md` – Lightweight ADR log (date, decision, context, outcome, owner).

## Conventions
- Keep numbering consistent so cross-product navigation is predictable.
- Link back to shared standards in `03-ai-enabling/03-operations/` and shared platform docs in `04-shared-systems/platform/` instead of duplicating.
- Note owners and update cadence in each file where relevant.
- Prefer concise checklists and tables for runbooks and env vars.
