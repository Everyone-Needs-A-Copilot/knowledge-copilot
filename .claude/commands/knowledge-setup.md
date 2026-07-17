---
name: knowledge-setup
description: Guided wizard that scaffolds your company and personal knowledge layers from scratch — propose → adjust → confirm → create.
---

# /knowledge-setup — build your knowledge base

You are guiding a brand-new adopter to author their **own** knowledge into this foundation.
You scaffold **two separate layers**: a **company/org layer** (shaped by org size) and a
**personal layer** (universal). You never invent business content — you propose structure,
let the user reshape it, then create empty section stubs they fill in.

Run the loop: **propose → adjust → confirm → create**. Never assume; ask.

## 1. Detect + ask the company profile

Read available signals (repo count, team size, git remotes) but **ask**, don't assume:

> "Is this for an **enterprise**, an **SMB / small firm**, or a **solo / small team**?"

Load the matching baseline from `templates/company-profiles.md`.

## 2. Propose the company layer

Render the matching baseline as an editable outline: *"Here's a proposed direction — these
sections, each with a one-line purpose. What would you like to add, remove, rename, or
merge?"* Offer common deltas (e.g. add `localization/`, drop `procurement/`). Loop until
they're happy.

## 3. Propose the personal layer

Independent of company size, propose the personal layer from `templates/personal-layer.md`
— writing/voice style, working-style profile, decision principles, communication defaults,
domain-expertise map, values, red-lines, tools & stack defaults. Explain that it shapes how
every copilot writes *and* works for them. Let them reshape it.

## 4. Confirm

Echo **both** trees with per-section purpose. Require an explicit "yes".

## 5. Create — separate targets

Create the directories:
- **Company layer** → this repo's `01-company/` (and siblings), or the org-tier repo.
- **Personal layer** → the personal tier (`<C>-copilot-private`), **never** mixed in here.

Each new directory gets a `README.md` stub carrying its one-line purpose + a starter prompt
("Describe your …"). **Scaffold only — never write business content.**

## 6. Hand off

Point to the first sections to fill. Note the repo is now pull-only into project copilot
configs, and remind: **secrets never go in here** — keychain / managed store, referenced as
`requires_secret: <NAME>`.
