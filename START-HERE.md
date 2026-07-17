# Start here

Welcome. `knowledge-copilot` is the open-source **knowledge foundation** your AI copilots
read from. This repo is a generic starting point — you bring the content; it brings the
structure, a library of reusable skills, and a guided wizard to build the rest.

## 1. Run the wizard

```
/knowledge-setup
```

It asks whether you're an **enterprise**, an **SMB/small firm**, or **solo/small team**,
proposes a structure sized to you, lets you reshape it, then scaffolds two **separate**
layers:

- **Company / org layer** — brand, voice, products, methods (this repo, or your `-internal` tier)
- **Personal layer** — how *you* write, decide, and work (your `-private` tier — never mixed in here)

See [`templates/`](templates/) for the baselines it uses.

## 2. What you already have (out of the box)

- **A reusable skill library** — [`03-ai-enabling/01-skills/`](03-ai-enabling/01-skills/):
  hundreds of generic, client-free skills across code, testing, design, security, infra,
  architecture, UX/UI, docs, engineering, research/analysis, copywriting, service design,
  strategy, marketing, industrial design, and theory of constraints. Add your own — see
  [`…/00-reference/how-to-create-a-skill.md`](03-ai-enabling/01-skills/00-reference/how-to-create-a-skill.md).
- **A prompt library** — [`03-ai-enabling/04-prompt-library/`](03-ai-enabling/04-prompt-library/).
- **Conventions & method** — how to build a knowledge base and how it's consumed:
  [`docs/00-knowledge-copilot/`](docs/00-knowledge-copilot/).
- **Templates** — company profiles, personal layer, product dossiers, best-practice packages.

## 3. How it plugs in

This repo is pulled **read-only** into every project's copilot config (`.claude/` / `.copilot/`).
Your coding, CLI, and chat copilots then read it to know your company, your products — and, at
the personal layer, *you*. See the [consumption contract](docs/00-knowledge-copilot/02-consumption-contract.md).

## The one rule

**No secrets here — ever.** Not in this repo, not in any tier's git. Credentials live in your
OS keychain / a managed secret store; content carries only `requires_secret: <NAME>` references.

## Next

Fill in the sections the wizard created, starting with your company overview and your personal
`writing-style` and `working-style`. A paragraph each beats none — this is the highest-leverage
content you can give a copilot.
