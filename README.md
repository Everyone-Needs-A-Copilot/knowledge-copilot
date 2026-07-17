# knowledge-copilot

> The open-source **knowledge foundation** for an AI copilot ecosystem. Clone it, run the
> setup wizard, and it scaffolds a knowledge base your copilots read from — company
> knowledge and personal knowledge, kept as separate layers.

This repository is a **generic starting point**, not a filled-in knowledge base. It ships
the structure, conventions, templates, and a guided **setup wizard** — you provide the
content. It started fresh; there is no inherited history.

## What this is

`knowledge-copilot` is the shared knowledge layer pulled **read-only** into every project's
AI-copilot configuration. Your copilots (coding, CLI, chat) read it to know your company,
your products, and your methods — and, at the personal layer, *you*: how you write, decide,
and work.

It sits at the base of a four-tier inheritance chain:

```
foundation (this repo, public)  →  org (private)  →  department (private)  →  personal (private)
```

Higher tiers stay generic; lower tiers get specific. Content flows **down** only. Secrets
never live here — or in any tier's git. They live in your OS keychain / a managed secret
store; this repo carries only `requires_secret: <NAME>` references.

## Two layers, always separate

Every adopter runs **two** knowledge layers, and the wizard scaffolds both:

- **Company / org layer** — brand, voice, products, methods, capabilities. Its shape scales
  with you (enterprise / SMB / solo).
- **Personal layer** — how *you* specifically write, think, decide, and work. Universal —
  the same value whether you're solo or inside a large enterprise. Lives in your personal
  tier, never mixed into the company layer.

## Get started

Run the setup wizard and answer a few questions; it proposes a structure, you reshape it,
it creates the scaffold:

```
/knowledge-setup
```

See [STRUCTURE.md](STRUCTURE.md) for the taxonomy and [templates/](templates/) for the
baselines the wizard uses.

## Layout

| Directory | Holds |
|---|---|
| `00-best-practices/` | Cross-project standards, templates, handoff guides |
| `01-company/` | Your company: identity, brand, voice, services, GTM, methods |
| `02-products/` | Your product ecosystem (3-layer taxonomy + a dossier template) |
| `03-ai-enabling/` | The AI layer: reusable skills, agent profiles, prompt library |
| `04-shared-systems/` | Cross-cutting systems that aren't products (design system, infra) |
| `templates/` | The wizard's baselines (company profiles + personal layer) |

Nothing here names a real company. Fill it in with the wizard, or by hand.

## License

Open source — add your license of choice.
