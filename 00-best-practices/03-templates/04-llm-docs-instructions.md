---
last_updated: 2026-06-27
status: active
---

# LLM Guide: Generate Product Technical Documentation

Use these instructions when asking an LLM to draft or update product docs under `02-products/<product-slug>/`. The goal is consistent, actionable, and security-aware documentation that matches our repository layout. These docs are shared references; full stack-specific docs live in each product’s `/docs` inside the product repo.

## Inputs to Provide the LLM
- Product name and purpose
- Current architecture/stack (frontend, backend, services, datastores, AI)
- Environments and deployment platform (Coolify, domains, ports)
- Integrations (n8n, OAuth providers, third-party APIs, email/CRM)
- Security requirements (data sensitivity, auth, secrets handling)
- Observability/ops practices (logging, metrics, alerts, backups)
- Known runbooks or common incidents
- Recent technical decisions or ADRs

## Expected Outputs (Files)
Create or update the following files under `02-products/<product-slug>/`:
- `00-overview.md` – What the product is, who it’s for, core value
- `10-architecture.md` – System context, components, data flows, non-functional requirements
- `20-deployment.md` – Environments, platform, env vars (names only)/secrets locations, deploy steps, post-deploy checks
- `30-operations.md` – Monitoring/logging, backups, runbooks, maintenance cadence
- `40-integrations.md` – External services, webhooks, auth providers, imports/exports
- `50-api.md` – Endpoints/contracts/rate limits (state “N/A” if not exposed)
- `60-security.md` – Data classification, access controls, secrets, auditing; reference `03-ai-enabling/03-operations/02-security-guidelines.md`
- `70-decisions.md` – ADR-style table of key decisions with dates and owners

## Structure and Style
- Keep sections concise with bullet points, tables, and checklists.
- Use numbered headings already present in the file; do not change filenames.
- Cross-link to shared standards instead of duplicating (`03-ai-enabling/03-operations/01-development-standards.md`, `02-security-guidelines.md`, `03-documentation-guide.md`).
- Note owners and update cadence where relevant.
- Call out any placeholders or unknowns explicitly with “TODO:” so humans can fill gaps.
- Assume databases are accessed via SSH tunnel for local work; if different, state it explicitly in deployment/setup.

## Required Details per File
- **Architecture:** Diagram description (text), core services, data stores, AI/ML components, queues/jobs, external dependencies, performance/availability targets.
- **Deployment:** Branch → environment mapping, build/runtime versions, env vars (names + purpose, no secrets), secrets locations (Coolify/GitHub), SSL/ACME steps, smoke tests; note SSH tunnel commands/requirements for DB access.
- **Operations:** Log locations, metrics/alerts, backup/restore steps, common incident runbooks with commands to run.
- **Integrations:** Endpoints, auth methods, payload schemas, retry/timeout expectations, rate limits.
- **API:** Auth, major endpoints, request/response examples, error codes, pagination/filters.
- **Security:** Data classification, access model, session handling, secret rotation cadence, PII/PHI handling, audit logs.
- **Decisions:** Table with Date, Decision, Context, Outcome, Owner.

## Quality Checklist for the LLM
- Files exist at correct paths under `02-products/<product-slug>/`.
- References to shared docs are correct and linked.
- No secrets included—only variable names and where to store them.
- Post-deploy checks cover primary user journeys.
- Runbooks include concrete commands or steps to verify/resolve.
- Unknowns are marked with TODOs for humans to complete.
- Outputs are meant for shared understanding; full, stack-specific docs belong in the product repo `/docs` using the product’s own templates.\n*** End Patch"}]}шуда
