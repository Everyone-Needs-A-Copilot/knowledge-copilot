---
last_updated: 2026-07-11
status: active
---

# Initiative Package Template — The 40-Initiatives Standard

Use this package for formal multi-phase work in any project.

**The gate IS the standard.** Every rule below states the check that
enforces it (`R1`..`R12`, implemented in `bin/check-initiatives.sh`). If a
rule has no check next to it, it is not part of the standard — do not add
a rule here without also adding its enforcement in `bin/check-initiatives.sh`,
and do not add a check without documenting the rule here. The two files
must never drift apart. (This is not a hypothetical: one real internal
product's initiatives standard rotted exactly this way — its spec asserted 4
required things, its checker verified 2, and it had no git hook, only a
README asking a human to remember to run `npm run verify:docs`. Result: 19 of
36 initiative folders drifted from the spec, 10 had empty ceremony
directories, and 3 were missing from the hand-maintained index. A rule that
isn't checked mechanically, and checked on every commit, is not a rule —
it's a wish.)

## What an initiative is

An initiative is a **multi-phase program with a defined goal and explicit
exit criteria**. It is distinct from:

- a **task** — a single bounded unit of work tracked in the project's
  authoritative task system (Task Copilot, Jira, Linear, GitHub Issues,
  whatever the project uses);
- a **feature spec** — a description of one shippable feature, usually
  scoped to a single phase or even a single task.

An initiative spans multiple sessions, may involve multiple agents or
contributors, and produces durable artifacts: a goal statement, a phase
breakdown, the decisions made along the way, and the validation evidence
that proves each phase's exit criteria were met.

**Keep live task state in the authoritative task system.** Assignments,
in-flight status, blockers-of-the-day, and QA state belong there, not in
initiative documents. The initiative README links to that system; it does
not duplicate it.

## Directory layout

```text
docs/40-initiatives/
├── README.md                  # generated index — see "The generated index" below (R7)
└── NN-slug/
    ├── README.md               # required — frontmatter + Goal/Scope/Non-Goals/... (R2, R3)
    ├── phases/                 # created on first phase document, never scaffolded empty (R11)
    │   └── phase-N-*.md        # (R12, warn-only)
    ├── decisions/               # created on first ADR, never scaffolded empty (R11)
    │   └── ADR-NNN-*.md
    └── retrospectives/          # created on first retro, never scaffolded empty (R11)
        └── *.md
```

`NN-slug` is a zero-padded 2-or-3-digit sequence number, a hyphen, and a
lowercase slug — e.g. `07-review-redesign`, `108-launch-audit` (**R1**:
`^[0-9]{2,3}-[a-z0-9-]+$`).

### The lazy-creation rule

`phases/`, `decisions/`, and `retrospectives/` are **created on first use,
never scaffolded empty.** If an initiative has no decisions yet, there is no
`decisions/` directory — not an empty one "for later." An empty ceremony
directory is exactly the kind of drift this standard exists to prevent
(**R11** fails on any of the three existing as an empty directory; the fix
is always to delete the empty directory, not to populate it with a
placeholder file).

**A directory holding only placeholder files is empty for this rule's
purposes.** `.gitkeep`, `.keep`, `.gitignore`, and `.DS_Store` don't count as
content — a `retrospectives/.gitkeep`-only directory exists for no reason
other than to hold an empty folder open in git, which *is* the empty
ceremony directory defect R11 bans, not an exception to it. The fix is the
same: delete the directory (and its placeholder), not add a real file just
to justify keeping it around before there's real content to put there.

## Frontmatter (required on every initiative README.md)

```yaml
---
initiative: NN-slug          # MUST equal the directory name
title: Initiative Name
status: proposed             # enum below
status_note: One-line human detail
owner: Team or person
created: YYYY-MM-DD
execution_context:           # optional; the tc/PRD join. null is valid.
  prd: null
  tasks: null
superseded_by: null          # required non-null when status is absorbed
---
```

- **R2**: every `NN-slug/` directory has a `README.md`.
- **R3**: that `README.md` opens with a YAML frontmatter block (`---` ...
  `---`) containing non-empty values for `initiative`, `title`, `status`,
  `owner`, and `created`.
- **R5**: the `initiative:` value equals the actual directory name — this
  is what makes the frontmatter self-describing instead of copy-paste-stale
  the moment a folder gets renamed.

### Status enum (closed set)

```text
proposed | discovery | planned | active | blocked | complete | absorbed | abandoned
```

- **R4**: `status` must be one of these eight values. Nothing else — no
  "In Progress (Phase 4 active)" free text in the field itself; put that
  detail in `status_note` instead, which is free text by design.
- **R6**: `status: absorbed` requires a non-null `superseded_by` (the
  `NN-slug` of the initiative that absorbed this one). An initiative cannot
  be marked absorbed and simultaneously fail to say what absorbed it.

## The canonical path (R8)

Initiatives live at **`docs/40-initiatives/`**. Nowhere else.
`docs/initiatives/` and `docs/80-initiatives/` must not exist non-empty —
both are real paths this exact standard has drifted to across the
ecosystem's history, and both are hard failures if populated. Pick one
canonical path and enforce it, don't let two conventions coexist "for now."

## The generated index (R7 — the rule that matters most)

`docs/40-initiatives/README.md` is a **generated file**, produced by
`bin/gen-initiatives-index.sh` from each initiative's frontmatter. It is
never hand-edited below its `<!-- BEGIN GENERATED INDEX -->` marker — any
prose a project wants above that marker is preserved across regeneration,
but the table itself is always machine-derived.

`check-initiatives.sh` enforces this by regenerating the index into a temp
file and diffing it against the committed one (**R7**); any difference is a
hard failure. This is the check that structurally kills index drift — a
hand-maintained index can always silently fall behind reality; a generated,
diffed index cannot, because the diff itself is the proof.

## Duplicate and stray rules

- **R9**: no two initiative folders may share the same `NN` prefix.
- **R10** (warn-only; hard fail under `--strict`): loose `.md` files at an
  initiative's root other than `README.md` should live under `phases/`,
  `decisions/`, or `retrospectives/` instead.
- **R12** (warn-only; hard fail under `--strict`): files inside `phases/`
  should match `phase-N-*.md`.

Why warn instead of fail for R10/R12: a legacy repo with years of loose
notes files needs to be able to turn the hook on **today**, see the debt,
and converge over time — not be told the hook can't be installed until a
big-bang cleanup happens first. If failing on day one is the only option,
teams disable the hook, and we're back to the drifted-standard outcome
described above. `--strict`
exists for new repos that want the tighter bar from the start.

## Rule reference (complete)

| Rule | What it checks | Enforcement | Severity |
| --- | --- | --- | --- |
| R1 | Folder name matches `^[0-9]{2,3}-[a-z0-9-]+$` | `check-initiatives.sh` | fail |
| R2 | Every initiative folder has `README.md` | `check-initiatives.sh` | fail |
| R3 | `README.md` has YAML frontmatter with `initiative`, `title`, `status`, `owner`, `created` | `check-initiatives.sh` | fail |
| R4 | `status` is in the closed enum | `check-initiatives.sh` | fail |
| R5 | `initiative:` value equals the directory name | `check-initiatives.sh` | fail |
| R6 | `status: absorbed` requires non-null `superseded_by` | `check-initiatives.sh` | fail |
| R7 | `docs/40-initiatives/README.md` matches a fresh regeneration | `check-initiatives.sh` + `gen-initiatives-index.sh` | fail |
| R8 | `docs/initiatives/` and `docs/80-initiatives/` don't exist non-empty | `check-initiatives.sh` | fail |
| R9 | No duplicate `NN` prefixes | `check-initiatives.sh` | fail |
| R10 | No loose `.md` files at an initiative root besides `README.md` | `check-initiatives.sh` | warn (fail with `--strict`) |
| R11 | `decisions/`, `phases/`, `retrospectives/` don't exist while empty (a `.gitkeep`/`.keep`/`.gitignore`/`.DS_Store`-only directory counts as empty) | `check-initiatives.sh` | fail |
| R12 | `phases/*.md` files match `phase-N-*.md` | `check-initiatives.sh` | warn (fail with `--strict`) |

## How to adopt in a repo

1. Copy this package's `bin/` directory into the target repo (any stable
   location — `bin/`, `scripts/`, `tools/` — as long as `check-initiatives.sh`,
   `gen-initiatives-index.sh`, `lib-initiatives.sh`, and
   `install-initiatives-hook.sh` stay together as siblings).
2. Run the installer from inside the target repo:

   ```bash
   bin/install-initiatives-hook.sh [DOCS_DIR]   # DOCS_DIR defaults to "docs"
   ```

   This installs (or updates) a `pre-commit` hook that runs
   `check-initiatives.sh` on every commit. It is idempotent, it chains onto
   (never clobbers) any existing `pre-commit` hook content, and it honors
   `core.hooksPath` if the repo has one configured.
3. Copy `initiative/` (from this package) into
   `docs/40-initiatives/NN-slug/` for each new initiative, fill in the
   frontmatter and sections, and let `phases/`, `decisions/`, and
   `retrospectives/` come into existence only when there's a real document
   to put in them.
4. Run `bin/gen-initiatives-index.sh [DOCS_DIR]` once to create the initial
   `docs/40-initiatives/README.md`, then let the pre-commit hook keep it
   honest from then on.
5. For a legacy repo with existing initiatives that predate this standard,
   run `check-initiatives.sh` once without `--strict` to see the warning
   debt, backfill frontmatter incrementally, and only reach for `--strict`
   once the repo is clean.

## Package contents

```text
07-initiative-package/
├── README.md                          # this file — the standard definition
├── initiative/
│   └── README.md                      # the copyable skeleton (frontmatter + sections)
├── exemplars/                         # reference documents — NOT part of the copyable skeleton
│   ├── phases/phase-1-plan.md
│   ├── decisions/ADR-001-template.md
│   └── retrospectives/README.md
└── bin/
    ├── lib-initiatives.sh             # shared frontmatter parsing (sourced, not run directly)
    ├── check-initiatives.sh           # the enforcer — the gate
    ├── gen-initiatives-index.sh       # regenerates docs/40-initiatives/README.md
    └── install-initiatives-hook.sh    # installs/updates the pre-commit hook
```

`initiative/` contains only `README.md` on purpose — copying it never
creates an empty `phases/`, `decisions/`, or `retrospectives/` directory
(that would violate R11 the moment it's copied). The `exemplars/` folder
holds fully worked reference documents for each ceremony type so authors
have something concrete to copy from once they actually need a phase plan,
an ADR, or a retrospective — but they are exemplars to copy *from*, not
scaffolding that ships inside every new initiative.
