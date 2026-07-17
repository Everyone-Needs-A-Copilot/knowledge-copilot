---
last_updated: 2026-06-28
status: active
---

# Integration Prompt: New Product Onboarding

Use this when connecting to a *new* product repo that needs to be added to the Copilot ecosystem. It mirrors the existing product integration prompts and ensures documentation, integration contracts, and development rules are captured end-to-end.

---

## Prompt

```
You are connected to the <PRODUCT NAME> repository. I need to onboard this product into the Copilot ecosystem and produce the complete shared documentation and integration contracts.

Please analyze the codebase and deliver the following:

1) **Create/refresh shared product docs** under `02-products/<product-slug>/` using `02-products/LLM-DOCS-INSTRUCTIONS.md` and `02-products/TECH-DOCS-TEMPLATE.md`:
   - `00-overview.md`, `10-architecture.md`, `20-deployment.md`, `30-operations.md`, `40-integrations.md`, `50-api.md`, `60-security.md`, `70-decisions.md`
   - Keep existing numbering/headings; mark unknowns with TODO

2) **Map integration contracts (inbound & outbound events)** similar to other product prompts:
   - For each inbound event: endpoint/route, auth, expected payload schema (JSON), processing path, persistence
   - For each outbound event: trigger, implementation status, payload schema (JSON), targets (internal products, n8n, third parties), retries/error handling
   - Note data ownership and shared entity alignment (use `03-ai-enabling/03-operations/10-shared-glossary.md`)

3) **API & surface area audit**
   - List all public/internal APIs, webhooks, queues, jobs, and CLI/cron entrypoints
   - Capture rate limits, auth methods, and error models
   - Identify required env vars (names only) and secrets locations (Coolify/GitHub)

4) **Data & infra inventory**
   - Datastores, vector DBs, cache/queue usage, migrations, backup/restore paths
   - AI/LLM dependencies (models, providers, embedding dims), content moderation
   - Observability: logs, metrics, alerts, dashboards

5) **Development rules alignment**
   - Draft or update `.claude/development-rules.md` in the product repo using `03-ai-enabling/03-operations/01-developer-rules-template.md`
   - Enforce: Docker-first, SSH tunnel for DBs, no secrets in code, multi-agent workflow (Architect/Developer/Tester minimum), stop-and-ask when destructive or ambiguous
   - Add stack-specific setup, test, lint, format, and data seeding commands

6) **Gap analysis & tasks**
   - What integrations/endpoints are missing or stubbed?
   - What documentation files are absent?
   - What monitoring/backup/security gaps exist?
   - Produce a short task list with owners/priority if known

Search the codebase for:
- API route definitions/controllers, middleware, policies, serializers
- Event dispatchers/listeners, webhook handlers, background jobs
- n8n workflows or other orchestration hooks
- Env var usage, config files, infra-as-code, deployment manifests
- LLM/model clients, embedding generators, vector DB client usage
```

---

## Expected Output

1. Fully populated docs in `02-products/<product-slug>/` using the standard file set
2. Integration contract tables with payload schemas and implementation status
3. API surface summary with auth/rate limits/error handling
4. Data/infra/AI dependency inventory with observability and backup notes
5. A complete `.claude/development-rules.md` draft for the product repo (aligned to the template)
6. Gap list with actionable tasks and priorities

---

## After Generating Documentation

1. Commit the new `02-products/<product-slug>/` docs to this repo (keep numbering/files consistent)
2. Update `02-products/01-ecosystem/00-overview.md` to add the product, flows, and status
3. Update `50-claude-projects/02-integration-architect.md` with the integration map and tasks
4. If new shared terms emerge, add them to `03-ai-enabling/03-operations/10-shared-glossary.md`
5. Ensure the product repo contains an updated `.claude/development-rules.md` (based on `03-ai-enabling/03-operations/01-developer-rules-template.md`) plus `project-context.md` if missing
6. Capture any unresolved TODOs and assign follow-up owners in the task list
