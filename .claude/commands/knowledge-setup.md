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

Independent of company size, propose the personal layer from `templates/personal/` (indexed by
`templates/personal-layer.md`). It's their professional **second brain** — durable operating
knowledge, not a diary or secrets. The set:
- **How I operate:** how-i-communicate · how-i-process-information · how-i-decide · working-preferences
- **What I work on:** what-i-work-on · recurring-and-automation (surfaces automation candidates)
- **Memory & people:** durable-facts · key-people
- **Competence & tools:** role-and-expertise · tools-and-stack

Explain it shapes how every copilot writes *and* works for them, and have them **start with the
three anchors** (how-i-communicate, how-i-process-information, what-i-work-on) + durable-facts —
not fill everything at once. Let them reshape the set. Each `personal/<doc>` template carries
guiding prompts + a worked example.

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
