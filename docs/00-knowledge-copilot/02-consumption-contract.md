---
last_updated: 2026-06-29
status: active
---

# Knowledge Copilot Consumption Contract

This document defines the stable canonical sub-paths that other projects and agents read against. Resolve all paths relative to `$CC_KNOWLEDGE_REPO` (emitted by `eval "$(cc env)"`).

## Resolution Mechanism

```bash
eval "$(cc env)"
# CC_KNOWLEDGE_REPO=/Volumes/Dev/Sites/COPILOT/knowledge-copilot  (local)
# or the team-configured equivalent on other machines
```

All sub-paths below are relative to `$CC_KNOWLEDGE_REPO`.

---

## Canonical Sub-Paths

| Domain | Sub-path | Key Files |
|--------|----------|-----------|
| Brand identity & visual | `01-company/01-brand/` | `02-tone-of-voice.md`, `01-brand-colors.md`, `03-ui-style-guide.md`, `06-brand-design-brief.md` |
| Voice, tone & principles | `01-company/02-voice/` | `00-overview.md`, `01-identity.md`, `02-principles.md`, `04-philosophy.md`, `08-manifesto.md` |
| Services & offerings | `01-company/03-services/` | `00-overview.md`, `01-engagement-journey.md`, your service overviews (e.g. `05-<service-name>.md`, `06-<service-name>.md`, `07-<service-name>.md`) |
| Go-to-market | `01-company/04-gtm/` | `00-overview.md`, `01-gtm-plan.md` |
| Communication patterns | `01-company/05-patterns/` | messaging frameworks, channel patterns |
| Methodologies & process | `01-company/06-methodologies/` | your methodology docs (e.g. `01-<your-method>.md`, `02-<your-method>.md`, …) |
| Company reference | `01-company/07-reference/` | positioning, market context, competitive landscape |
| Products & capabilities | `02-products/` | `01-ecosystem/`, `02-foundational/`, `03-work/`, `04-applications/` |
| AI skills & profiles | `03-ai-enabling/` | `01-skills/`, `02-profiles/` |
| Shared design system | `04-shared-systems/design-system/` | component library, design tokens |

---

## Agent Consumption Guidance

### Copy / Voice / Content Agents (`cw`, `cco`)

Before writing any copy or brand-aligned content:

1. Read `$CC_KNOWLEDGE_REPO/01-company/02-voice/` for tone, identity, and principles
2. Read `$CC_KNOWLEDGE_REPO/01-company/01-brand/02-tone-of-voice.md` for the tone matrix
3. Cross-reference `$CC_KNOWLEDGE_REPO/01-company/01-brand/06-brand-design-brief.md` for visual context

### Offerings / SOW / Planning Agents (`ta`, `sd`)

Before scoping work or building a service blueprint:

1. Read `$CC_KNOWLEDGE_REPO/01-company/03-services/` for current service offerings
2. Read `$CC_KNOWLEDGE_REPO/01-company/06-methodologies/` for approved methodologies (your company's named frameworks and delivery methods)
3. Read `$CC_KNOWLEDGE_REPO/02-products/` for the product portfolio being supported

---

## Contract Rules

- **Sub-paths are stable.** Do not reorder top-level directories without updating this contract.
- **Never duplicate content.** Agents read from here; they do not copy knowledge into their own files.
- **Always hydrate env first.** Run `eval "$(cc env)"` before any `$CC_KNOWLEDGE_REPO` reference.
- **Verify existence before reading.** If a file is missing, the knowledge is absent — flag it rather than inventing it.
- **This file is the source of truth** for which paths are safe to depend on. If a path changes, update this contract and notify consuming agents.
