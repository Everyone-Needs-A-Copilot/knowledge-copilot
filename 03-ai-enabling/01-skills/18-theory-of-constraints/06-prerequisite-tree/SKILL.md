---
last_updated: 2026-04-02
status: active
name: prerequisite-tree
description: Plan implementation by identifying obstacles and intermediate objectives. Use when planning how to implement a change, when a goal seems too ambitious, or when you need to sequence work by dependencies. Answers "how to cause the change?" Triggers on implementation planning, obstacle analysis, sequencing, and dependency mapping.
allowed-tools: Bash(python3:*) Read Write
---

# Prerequisite Tree (PRT)

The Prerequisite Tree answers one question: **how do we get from here to the ambitious target?** It does this by surfacing every obstacle that stands between the current state and the goal, then defining the minimum intermediate objective (IO) required to overcome each one. The result is a dependency map that sequences work by necessity, not preference.

The key insight: **obstacles drive the plan**. Unlike task lists that describe activities, PRTs explain why each step must happen. Every IO exists because a specific obstacle demands it.

## When to Use PRT

| Situation | Why PRT Helps |
|-----------|--------------|
| Goal feels too big to start | Breaks the distance into necessary steps |
| Team disagrees on where to begin | Obstacles create objective sequencing |
| "We can't do X until we do Y" conversations | Makes dependencies explicit and visible |
| Plan keeps changing mid-execution | Obstacle list was incomplete — redo the PRT |
| Scope creep accumulating | Every new task must trace to an obstacle |

## The Four-Step Process

### Step 1: State the Ambitious Target (AT)

Write a single clear sentence describing what you want to achieve. Make it ambitious enough to matter. Vague targets produce vague obstacle lists.

Good: "Launch enterprise tier with SSO, admin controls, and dedicated onboarding."
Bad: "Improve the product."

### Step 2: List Every Obstacle

Ask: "What stands between where we are now and the ambitious target?" Write down every condition, gap, missing capability, or dependency that must change before the target can be reached.

Rules for good obstacles:
- State them as current negative conditions ("We have no admin UI", not "Build admin UI")
- Be specific — vague obstacles produce useless IOs
- Include people, process, and knowledge obstacles, not just technical ones
- Don't self-censor: if it feels like an obstacle, list it

### Step 3: Define the Intermediate Objective for Each Obstacle

For each obstacle, ask: "What is the minimum condition that would neutralize this obstacle?" This is the IO. It must be:
- **Positive** — stated as a condition that exists, not an activity to do
- **Necessary** — without it, the obstacle remains
- **Sufficient** — once achieved, the obstacle is gone
- **Verifiable** — you can confirm when it's been reached

| Obstacle | Weak IO | Strong IO |
|----------|---------|-----------|
| "No SSO integration" | "Implement SSO" | "SSO authenticates users via SAML 2.0 against at least one enterprise identity provider" |
| "Enterprise pricing not validated" | "Do pricing research" | "3 target enterprise prospects have confirmed willingness to pay at the proposed price point" |

### Step 4: Sequence by Dependencies

Ask for each IO: "Which other IOs must exist before this one can be achieved?" This reveals the dependency structure and creates a naturally phased plan.

IOs with no dependencies form Phase 1 (start here in parallel).
IOs whose dependencies are all in Phase 1 form Phase 2.
And so on.

The longest chain of sequential dependencies is the critical path — it determines the minimum time to reach the target regardless of resources applied to other tracks.

## Anatomy of a PRT

```
Ambitious Target
    └── Obstacle A → IO-A (Phase 1, no deps)
    └── Obstacle B → IO-B (Phase 1, no deps)
    └── Obstacle C → IO-C (Phase 2, depends on IO-A)
    └── Obstacle D → IO-D (Phase 2, depends on IO-A, IO-B)
    └── Obstacle E → IO-E (Phase 3, depends on IO-C, IO-D)
```

IO-A → IO-C → IO-E is one dependency chain.
IO-A → IO-D → IO-E is another.
IO-B → IO-D → IO-E is a third.

If IO-A → IO-D → IO-E is the longest chain, it is the critical path.

## Scripts

### `scripts/prt_builder.py`

Build and validate a Prerequisite Tree from a list of obstacles and their IOs.

```bash
python3 scripts/prt_builder.py --file input.json
python3 scripts/prt_builder.py '{"target": "...", "obstacles": [...]}'
```

Input: JSON with `target` (string) and `obstacles[]` — each with `id`, `description`, `intermediate_objective`, `dependencies[]`.

Output:
- Phased implementation sequence
- Parallel tracks within each phase
- Critical path (longest dependency chain)
- Circular dependency warnings
- Total phase count and obstacle count per phase

**Use when:** You have identified obstacles and need to sequence the work. Also useful to verify that a planned sequence is logically sound.

See `assets/prt-schema.json` for the full input schema.

## Common Mistakes

**Confusing obstacles with tasks.** "Build SSO" is a task. "We have no SSO integration" is an obstacle. The PRT needs obstacles — the tasks emerge from the IOs.

**Missing soft obstacles.** Technical teams often list only technical gaps. Obstacles like "the sales team doesn't understand the enterprise value proposition" or "we have no enterprise customer references" are just as real and often more critical.

**Defining IOs too broadly.** An IO of "SSO is done" leaves open what "done" means. Precision matters: the IO should be verifiable by any observer.

**Forcing sequential work that could be parallel.** Review the dependency list critically. Many teams default to sequential execution when the actual dependency structure allows parallel tracks.

**Skipping the obstacle for an IO.** Every IO must trace back to a specific obstacle. If you can't name the obstacle an IO addresses, remove the IO — it's scope creep.

## Relationship to Other TOC Tools

The PRT is typically built after the Future Reality Tree (FRT) confirms the direction is correct. Once the target is validated, PRT answers "how." The Transition Tree (TrT) then converts each IO into a detailed cause-effect action plan.

| Tool | Question Answered |
|------|------------------|
| Current Reality Tree | Why do current problems exist? |
| Evaporating Cloud | What conflict must be resolved? |
| Future Reality Tree | Will this solution actually work? |
| **Prerequisite Tree** | **How do we implement the change?** |
| Transition Tree | What exactly do we do, step by step? |

## References

- [Obstacle-Driven Planning](references/obstacle-driven-planning.md) — Why PRT produces better plans than activity lists, with a business example
