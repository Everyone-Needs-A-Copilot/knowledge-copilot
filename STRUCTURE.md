# Repository Structure

> The map of `knowledge-copilot` — a **generic foundation**. This describes the intended
> structure and the conventions for adding to it. The setup wizard creates and fills these;
> you can also edit by hand.

## Root layout

```
knowledge-copilot/
├── README.md                 # What this is + how to start
├── STRUCTURE.md              # This file
├── knowledge-manifest.json   # Extension declarations consumed by the framework
├── ECOSYSTEM.md              # (created by the wizard) your product registry
│
├── 00-best-practices/        # Cross-project standards, templates, handoff guides
├── 01-company/               # Company: identity, brand, voice, services, GTM, methods
├── 02-products/              # Product ecosystem (3-layer taxonomy)
├── 03-ai-enabling/           # AI layer: skills, profiles, prompt library
├── 04-shared-systems/        # Cross-cutting systems that aren't products
├── templates/                # Wizard baselines (company profiles + personal layer)
└── .claude/commands/         # The setup wizard
```

## Conventions

1. **One home per content type.** New content goes in the most specific existing directory.
2. **Numbered prefixes order things** (`NN-`). Reuse the scheme when adding siblings.
3. **Products are registered, not just filed.** Add a product → update `ECOSYSTEM.md` *and*
   its dossier under `02-products/<layer>/<name>/`.
4. **Secrets never live here.** Keychain / managed store only; carry `requires_secret: <NAME>`.
5. **Archive, don't delete.** Superseded content → `_archive/<date>-<reason>/`.

## The 3-layer product taxonomy (`02-products/`)

- `01-foundational/` — tools used to *make* things
- `02-work/` — tools used to *do* the work
- `03-applications/` — client-facing products
- `99-innovation-roadmap/` — future ideation, kept separate
- `_dossier-template/` — copy this per product

## The AI layer (`03-ai-enabling/`)

- `01-skills/` — reusable skills by domain (see `00-reference/` for how to author one)
- `02-profiles/` — agent profiles (see `00-template.md`)
- `03-operations/` — operating docs and protocols
- `04-prompt-library/` — reusable, client-free prompts
