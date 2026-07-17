---
last_updated: 2026-06-27
status: active
---

# Product Card & Dossier Spec

**Authoritative format for every product documented under `02-products/`.**
The goal: any Claude session in any project on this machine can read a product's
doc, learn **where it lives, how it operates, and which files implement which
feature** — so it can go grab that feature. Accuracy over completeness.

---

## 1. The card — every product has `00-overview.md`

Begin the file with this YAML frontmatter (all fields required unless noted):

```yaml
---
product: <repo-name>                 # kebab-case, matches the GitHub repo
layer: 1-foundational | 2-work | 3-applications
status: active | dormant | defunct
repo: <full git remote URL>          # read it: git -C <local> remote get-url origin
local: <absolute path on this machine>
visibility: public | private         # public = open source
oneliner: <one sentence, what it is>
operates: <how it runs — stack + runtime, e.g. "Laravel app + Postgres; MCP server">
entry_points: [<dir/file>, ...]      # the dirs/files worth opening first
related: [<other products>]          # optional
tags: [<keyword>, ...]
---
```

Then the body:

```markdown
# <Product Name>

## Overview
What it is, who it's for, why it exists. 2–4 sentences.

## How it operates
Tech stack, how to run/use it, key runtime facts (entry command, ports,
deploy target). Enough that a new session can boot or invoke it.

## Key features
Each feature as a bullet with a POINTER to the file/dir that implements it —
this is what makes "go grab that feature" work:
- **<Feature>** — <one line> → `path/to/implementation`

## Entry points
The handful of dirs/files to open first to understand the codebase.
```

## 2. Accuracy rules (non-negotiable)

- **Read the repo.** Open README, the manifest (package.json / composer.json /
  pyproject.toml), and skim the top-level dirs. Never invent structure.
- **Get the real remote** via `git -C <local> remote get-url origin`.
- **Verify the local path exists** and list its real top-level dirs.
- **Status**: `active` if commits in last ~90 days, else `dormant`.
- If something is unknown, write `UNKNOWN` — do not guess.

## 3. Layer depth

| Layer | Files to produce |
|-------|------------------|
| **1 — Foundational** | `00-overview.md` (card) + `## How to extend` section appended to it |
| **2 — Work** | `00-overview.md` (card) + `## Operations` section appended to it |
| **3 — Applications** | Full dossier (below) |

### Layer-3 dossier file set

Produce/refresh these (skip a file only if genuinely N/A — say so in the file):

| File | Contents |
|------|----------|
| `00-overview.md` | Card (frontmatter + body above) |
| `10-architecture.md` | System design, components, data model, key flows |
| `20-deployment.md` | How it's built, hosted, deployed (env, CI, target) |
| `30-operations.md` | Running it day-to-day, jobs, monitoring |
| `40-integrations.md` | External services, APIs, MCP, other ecosystem products |
| `50-api.md` | Public endpoints / interfaces / commands |
| `60-security.md` | Auth, secrets, data handling |
| `70-decisions.md` | Notable architecture decisions and why |

When **updating** an existing dossier: read each existing file, reconcile it
against the current repo, fix what's stale, keep what's still true. Add the
frontmatter card to `00-overview.md` if missing.
