# How to create a skill

A **skill** is a packaged, reusable capability your copilots can invoke — a focused set of
instructions for one kind of task. Skills in this foundation are **generic** (they name no
client and carry no business fact); company-specific skills belong in your org tier.

## Anatomy

```
03-ai-enabling/01-skills/<domain>/<skill-name>/
└── SKILL.md
```

`SKILL.md` frontmatter:

```yaml
---
name: <skill-name>
description: <one line — when to use this skill; this is what triggers it>
---
```

Then the body: the method/steps, inputs, outputs, and any examples. Keep it self-contained
and free of secrets or private business facts.

## Organize by domain

Group skills under domain folders, e.g. `01-analysis/`, `02-testing/`, `03-design/`,
`04-security/`, `05-infrastructure/`, `06-architecture/`, `07-copywriting/`,
`08-documentation/`. Reuse the numbering scheme when adding siblings.

## Good skills

- Do **one** thing well; name the trigger precisely in `description`.
- Are portable — any adopter could use them unchanged.
- Cite no clients, endpoints, or credentials.
