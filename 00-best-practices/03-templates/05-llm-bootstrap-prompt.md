---
last_updated: 2026-06-28
status: active
---

# LLM Bootstrap Prompt (Use in Product Repo)

Use this prompt inside the PRODUCT repo (not here) to generate required local scaffolding. Provide concrete inputs; keep secrets out.

```
You are bootstrapping a new product repo using the shared project-copilot subtree under docs/shared. Generate outputs in THIS repo (product repo), not in the shared subtree.

Inputs (fill in):
- Product slug/name, one-liner purpose
- Stack (frontend/backend/services), hosting platform, auth provider(s)
- DB type and endpoint (remote), SSH tunnel details (host, key path, remote IP:port, local port)
- Package manager(s)/toolchain
- Domains/ports (prod/dev), DNS/proxy approach (Cloudflare, Caddy/Traefik)
- MCP servers desired (if any) + required env var names (no secrets)

Shared guides to follow (from docs/shared):
- Docs: 03-ai-enabling/03-operations/03-documentation-guide.md
- PRDs: 03-ai-enabling/03-operations/09-generating-product-requirements-document.md
- Tasks: 03-ai-enabling/03-operations/10-generating-tasks-from-a-PRD.md
- Task execution: 03-ai-enabling/03-operations/11-task-list-management.md

Outputs to create/update in THIS repo:
1) /claude/development-rules.md (stack-specific; enforce Docker + SSH tunnel; multi-agent: Architect, Developer, Tester always; spawn Data/DB for schema; Ops/Infra for deploy/Makefile/tunnel; add UI/UX, Security, Cost/Perf as scope demands; stop-and-ask if applicable).
2) /claude/project-context.md (seed with environments, tunnel command, domains, current status).
3) /tasks/prd-<slug>.md (draft/updated PRD using the PRD guide).
4) /tasks/tasks-<slug>.md (tasks + subtasks using the tasks guide; note stop-and-ask protocol if used).
5) /docs/ (product-specific docs; include /docs/README.md explaining layout; full product docs live here, not in shared repo).
6) .env.example with env var NAMES only (no secrets), including tunnel vars if used.
7) Makefile targets: dev, tunnel, kill-tunnel, tunnel-status, test-db, db-backup (if applicable), lint, test, build, typecheck, check; ensure `make dev` starts tunnel + app.
8) .mcp.json stub if MCP servers are desired (server entries + env var names only).

Constraints:
- Stack-agnostic language when referencing shared guides; stack-specific details only in this product repo.
- No secrets; only names/paths/commands.
- DB is accessed via SSH tunnel; no local DB clone unless explicitly allowed.
- Mark unknowns as TODO; do not invent data.

Deliver:
- List created/updated files with a short purpose.
- Open TODOs the human must fill (env values, secrets, missing domains, etc.).
```
