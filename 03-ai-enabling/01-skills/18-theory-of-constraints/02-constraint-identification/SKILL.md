---
last_updated: 2026-04-02
status: active
name: constraint-identification
description: Identify system constraints using Goldratt's Five Focusing Steps (Identify, Exploit, Subordinate, Elevate, Repeat). Use when diagnosing bottlenecks, analyzing capacity, or deciding where to invest limited resources. Triggers on bottleneck analysis, capacity planning, resource allocation, constraint, and system optimization.
allowed-tools: Bash(python3:*) Read Write
---

# Constraint Identification

Every system has exactly one constraint at any given time — the weakest link that limits total throughput. The Theory of Constraints teaches that improving anything other than the constraint is an illusion. You get faster at feeding the bottleneck, not at delivering output.

Goldratt's Five Focusing Steps give you a rigorous process: find the constraint, squeeze everything out of it without spending money, align the rest of the system to support it, and only then invest to expand it. Then repeat — because once you elevate the constraint, the bottleneck shifts.

## The Five Focusing Steps

### Step 1: Identify the Constraint

Find the one resource, policy, or capability that limits overall system throughput. The constraint is where work piles up, where waits are longest, where utilization is highest. In manufacturing, this is easy to see (inventory queues). In knowledge work, it is often invisible — a policy, an approval process, a single expert.

**Signals a resource is the constraint:**
- Work-in-progress accumulates in front of it
- It is always busy while others wait
- Utilization consistently above 85-90%
- Teams upstream are producing faster than it can consume
- Delays in this step cascade into missed delivery dates

### Step 2: Exploit the Constraint

Before spending a single dollar, extract maximum output from the current constraint. This is the highest-leverage step. Common exploitation moves:

- Eliminate waste at the constraint (rework, waiting, context-switching)
- Protect it from interruptions and non-constraint work
- Ensure it is never idle due to upstream failures
- Offload non-bottleneck work to non-constraints
- Improve quality gates before the constraint so it never processes defects

### Step 3: Subordinate Everything Else

Once the constraint is identified and being exploited, the rest of the system must serve it — not optimize itself. A non-constraint running at 100% efficiency while the constraint starves is waste disguised as productivity.

Subordination often requires uncomfortable decisions:
- Let non-constraint resources sit idle rather than build WIP ahead of the constraint
- Reduce batch sizes to keep the constraint fed steadily
- Restructure incentives so non-constraints are measured on feeding the constraint, not on their own utilization

### Step 4: Elevate the Constraint

Only after exploiting and subordinating — when you've gotten everything possible from the current setup — invest to increase constraint capacity. This means adding resources, buying tools, hiring, or redesigning processes.

Elevating too early (before exploiting) wastes money. You often find the constraint disappears through exploitation alone.

### Step 5: Repeat

When the constraint is broken, it moves. The system is now limited by a different resource or policy. Return to Step 1. Never declare victory — the bottleneck always exists somewhere.

**Warning:** Inertia is the enemy of Step 5. Organizations lock in the solutions from the previous cycle and stop looking for the new constraint. This is why Goldratt added "Do not let inertia become the constraint" as an explicit warning.

## Constraint Types

Not all constraints are physical. In knowledge work, policy and knowledge constraints dominate. See:

- [Constraint Types Reference](references/constraint-types.md) — Physical, policy, market, knowledge, time
- [Knowledge Work Constraints](references/knowledge-work-constraints.md) — How constraints manifest differently than in manufacturing

**The most important insight:** Policy constraints are the most common in knowledge work and the most overlooked. Physical constraints are visible. Policy constraints are invisible — they masquerade as "how we do things here."

## Scripts

### `scripts/five_focusing_steps.py`

Analyze system steps using utilization, WIP, and wait time to identify the constraint and generate exploitation, subordination, and elevation recommendations.

```bash
python3 scripts/five_focusing_steps.py --file input.json
```

Input: JSON with `system_steps[]` where each step has:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Step name |
| `utilization` | float 0-1 | Current capacity utilization |
| `wip` | int | Work items currently queued or in-progress |
| `wait_time` | float | Average wait time in hours |

Example:

```json
{
  "system_steps": [
    { "name": "Design",     "utilization": 0.65, "wip": 3,  "wait_time": 4  },
    { "name": "Development","utilization": 0.91, "wip": 12, "wait_time": 48 },
    { "name": "QA Review",  "utilization": 0.78, "wip": 6,  "wait_time": 16 },
    { "name": "Deployment", "utilization": 0.45, "wip": 1,  "wait_time": 2  }
  ]
}
```

Output: Composite constraint score for each step, ranked list, identified constraint, and three sets of recommendations: exploit (free), subordinate (realign), and elevate (invest).

**Use when:** You have observable data on where work accumulates and where waits are longest. Particularly useful after a sprint retrospective or when a delivery cycle feels "stuck."

### `scripts/constraint_assessment.py`

Classify and rank constraints by type and business impact, with special attention to policy constraints.

```bash
python3 scripts/constraint_assessment.py --file input.json
```

Input: JSON with `constraints[]` where each has:

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Plain-language description of the constraint |
| `type` | string | `physical`, `policy`, `market`, `knowledge`, or `time` |
| `evidence` | string | Observable evidence that this is a constraint |
| `impact_score` | int 1-10 | Estimated business impact (10 = highest) |

Example:

```json
{
  "constraints": [
    {
      "description": "All production deploys require VP approval",
      "type": "policy",
      "evidence": "Average 3-day delay between code-complete and production",
      "impact_score": 9
    },
    {
      "description": "Only one engineer knows the payment integration",
      "type": "knowledge",
      "evidence": "All payment issues queued until that engineer is available",
      "impact_score": 8
    }
  ]
}
```

Output: Constraints ranked by impact, classification summary by type, policy constraint count and prominence flag, and a warning if no policy constraints are identified (they are almost always present in knowledge work and are often missed).

**Use when:** You have qualitative observations about where the system is limited, especially when the team suspects the constraint but has not formally analyzed it.

## Key Principles

- **There is always exactly one constraint.** Improving two things simultaneously means one of them is not the constraint.
- **Exploit before elevating.** Most constraints can be reduced significantly without spending money.
- **Subordination is the hardest step.** It requires telling productive people to slow down or idle, which feels wrong.
- **Policy constraints are invisible.** Ask "what would we have to change to double throughput?" — the answer is usually a policy.
- **The goal is throughput, not utilization.** 100% utilization everywhere guarantees queuing. Non-constraint slack is healthy.

## When NOT to Use

- When the system has no clear flow of work (e.g., pure research with no output metric)
- When every resource is severely underutilized — the constraint is market demand, not internal capacity
- As a substitute for strategic prioritization — identifying the constraint tells you where to focus optimization, not what to build

For market-constrained systems, use throughput accounting to evaluate what mix of work generates the most value from available capacity. See the `throughput-accounting` skill.
