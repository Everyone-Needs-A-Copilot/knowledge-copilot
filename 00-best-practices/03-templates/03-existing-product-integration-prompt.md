---
last_updated: 2026-06-28
status: active
---

# Integration Prompt: Existing Product Alignment

Use this when connecting to an **existing** product repo that is not yet represented under `02-products/`. It mirrors the product integration prompts and ensures documentation, integration contracts, and development rules are fully aligned with the Copilot ecosystem.

---

## Prompt

```
You are connected to the <PRODUCT NAME> repository. This product already exists but is not yet documented under `02-products/<product-slug>/`. I need to fully integrate it into the Copilot shared docs and alignment framework.

Deliver the following:

1) **Create/refresh shared product docs** under `02-products/<product-slug>/` (in this repo) using `02-products/LLM-DOCS-INSTRUCTIONS.md` and `02-products/TECH-DOCS-TEMPLATE.md`:
   - `00-overview.md`, `10-architecture.md`, `20-deployment.md`, `30-operations.md`, `40-integrations.md`, `50-api.md`, `60-security.md`, `70-decisions.md`
   - Preserve numbering/headings; mark unknowns with TODO

2) **Integration contracts (inbound & outbound events)**
   - For each inbound event: endpoint/route, auth, expected payload schema (JSON), processing path, persistence, idempotency, retries
   - For each outbound event: trigger, implementation status, payload schema (JSON), targets (internal products, n8n, third parties), delivery/retry strategy, error handling
   - Map data ownership and shared entity alignment (use `03-ai-enabling/03-operations/10-shared-glossary.md`)

3) **API & surface area audit**
   - Public/internal APIs, webhooks, queues, jobs, cron/CLI entrypoints
   - Rate limits, auth methods, error models, pagination/filters
   - Required env vars (names only) and secrets locations (Coolify/GitHub)

4) **Data, infra, and AI inventory**
   - Datastores, vector DBs, caches/queues, migrations, backup/restore paths
   - AI/LLM dependencies (models/providers/embedding dims), safety/mode checks
   - Observability: logs, metrics, alerts, dashboards; note gaps

5) **Development rules alignment**
   - Draft or update the product repo’s `.claude/development-rules.md` using `03-ai-enabling/03-operations/01-developer-rules-template.md`
   - Enforce: Docker-first, SSH tunnel for DBs, no secrets in code, multi-agent workflow (Architect/Developer/Tester minimum), stop-and-ask on destructive/ambiguous work
   - Add stack-specific setup/test/lint/format/data seeding commands and any required make targets

6) **Integration readiness tasks (beyond docs)**
   - Identify missing or stubbed endpoints/webhooks/queues and outline code changes needed
   - List required n8n (or other orchestration) flows to add/update
   - Call out monitoring/backup/security gaps and propose concrete tasks
   - Flag env var naming inconsistencies or missing secrets locations
   - Add test coverage needs (happy/edge/error paths) for integration points

Search the codebase for:
- API routes/controllers, middleware/policies/serializers
- Event dispatchers/listeners, webhook handlers, background jobs
- n8n workflows or other orchestration hooks
- Env var usage, config files, infra-as-code, deployment manifests
- LLM/model clients, embedding generators, vector DB clients
```

---

## Expected Output

1. Standard doc set in `02-products/<product-slug>/` populated with findings
2. Integration contract tables with payload schemas, auth, status, and retry/error handling
3. API surface summary with auth/rate limits/error models
4. Data/infra/AI dependency inventory plus observability and backup notes
5. Updated or newly drafted `.claude/development-rules.md` for the product repo
6. Concrete gap list with prioritized tasks (code, infra, monitoring, docs)

---

## After Generating Documentation

1. Commit the new `02-products/<product-slug>/` docs to this repo (keep numbering/files consistent)
2. Update `02-products/01-ecosystem/00-overview.md` to include the product, flows, and status
3. Update `50-claude-projects/02-integration-architect.md` with integration map, tasks, and owners
4. If new shared terms emerge, add them to `03-ai-enabling/03-operations/10-shared-glossary.md`
5. In the product repo, ensure `.claude/development-rules.md` and `project-context.md` are present and aligned to `03-ai-enabling/03-operations/01-developer-rules-template.md`
6. Open follow-up issues/PRs for required code/infra changes, tests, and n8n workflows; note unresolved TODOs with owners/priority
