---
last_updated: 2026-04-02
status: active
name: critical-chain
description: Manage projects using Critical Chain methodology — identify the critical chain, size buffers, and manage by buffer consumption. Use when planning projects, tracking project health, or managing multiple projects sharing resources. Triggers on project planning, buffer management, project scheduling, resource contention, and multi-project management.
allowed-tools: Bash(python3:*) Read Write
---

# Critical Chain Project Management (CCPM)

Critical Chain Project Management is Goldratt's application of the Theory of Constraints to projects. The core insight: projects fail because of bad human psychology around estimates (Student Syndrome, Parkinson's Law) and poor buffer management, not because of bad execution. CCPM removes individual task safety, aggregates it into project buffers, and manages by buffer consumption rather than task-level due dates.

## Why Traditional Project Management Fails

Traditional scheduling gives each task a padded estimate. Tasks finish late more often than early (Student Syndrome + Parkinson's Law). Delays cascade. Buffers are invisible so managers can't act proactively.

CCPM fixes this by making the buffer explicit and visible — and managing the project by how fast the buffer is being consumed, not whether individual tasks hit their dates.

---

## Critical Path vs Critical Chain

**Critical Path** (traditional): The longest path through the task network by duration. Ignores resource conflicts — assumes different tasks can share the same person simultaneously.

**Critical Chain**: The longest path through the task network **after resolving resource contention**. If two tasks on parallel paths need the same resource, one must wait. This serialization often makes the critical chain longer than the critical path.

The critical chain is the true constraint of the project. Everything else is a feeding chain.

---

## The Two Root Causes CCPM Targets

### Student Syndrome
People don't start work until the deadline is close. A task with a 10-day estimate gets started on day 7. Any problem encountered leaves no recovery time. Safety added to individual tasks evaporates before work begins.

### Parkinson's Law
Work expands to fill the time available. A task that could be done in 3 days takes the full 10-day estimate because there's no reason to finish early (finishing early just means the next task starts early but that benefit is invisible and rarely rewarded).

**Together:** Tasks finish late (Student Syndrome) but never early (Parkinson's Law). The result is systematic late delivery despite having "enough" time in the estimates.

---

## Buffer Types

### Project Buffer (PB)
Placed at the end of the critical chain, before the project due date. Absorbs delays from critical chain tasks. Sized as 50% of the sum of safety removed from critical chain tasks.

```
Project Buffer = 0.5 × Σ(safe_duration − aggressive_duration) for critical chain tasks
```

### Feeding Buffers (FB)
Placed where feeding chains merge into the critical chain. Prevent delays from non-critical-chain paths from disrupting the critical chain. Sized the same way — 50% of the safety removed from feeding chain tasks.

```
Feeding Buffer = 0.5 × Σ(safe_duration − aggressive_duration) for feeding chain tasks
```

### Resource Buffers
Alerts placed before critical chain tasks to warn the resource they'll be needed soon. Not a time buffer — they are signals to prevent resource starvation on the critical chain.

---

## Buffer Sizing: The 50% Rule

Safe estimates include significant safety margin. Aggressive estimates remove that safety. The difference is the safety that was embedded.

Aggregating safety into a project buffer works because:
1. Not all tasks will use their full safety — statistical aggregation means the total variability is less than the sum of individual variances
2. Safety that's explicit and protected is used more efficiently than safety hidden in individual tasks

**Aggressive estimate** = what you could reliably do if everything went well, no interruptions, focused work. Typically 50% of the "safe" estimate for knowledge work.

**Adjustment factors:**
- High novelty/uncertainty: increase buffer to 60-65% of safety
- Well-understood repeating work: decrease to 40-45%
- Projects with many external dependencies: increase buffer
- Projects with highly skilled, available resources: decrease buffer

---

## Buffer Management: Green / Yellow / Red

Track two numbers: buffer consumed (%) and chain completed (%).

| Zone | Condition | Action |
|------|-----------|--------|
| **Green** | Buffer consumed < chain completion % | Ahead of plan. No action needed. |
| **Yellow** | Buffer consumed moderately exceeds completion % | Develop contingency plans. Identify likely causes. |
| **Red** | Buffer consumed significantly exceeds completion % | Execute contingency plans now. Escalate. Consider scope changes. |

The insight: you don't manage individual tasks. You manage the buffer. If a task runs long but the buffer is still green, there's no crisis. If the buffer hits red, it's a crisis regardless of which task caused it.

---

## Drum-Buffer-Rope in Projects

In multi-project environments, resources are shared. The **drum** is the most-loaded resource — the one that limits throughput across all projects. CCPM uses the drum resource to stagger project starts so it's never double-booked.

**Staggering rule:** Don't start a new project until the drum resource has capacity. This feels counterintuitive (slowing starts) but actually delivers all projects faster by eliminating the multitasking penalty.

---

## Scripts

### `scripts/critical_chain.py`

Identifies the critical chain and sizes all buffers for a project.

```bash
python3 scripts/critical_chain.py --file project.json
```

Input:
```json
{
  "tasks": [
    {
      "id": "A",
      "name": "Requirements",
      "duration_aggressive": 3,
      "duration_safe": 6,
      "dependencies": [],
      "resource": "analyst"
    },
    {
      "id": "B",
      "name": "Design",
      "duration_aggressive": 4,
      "duration_safe": 8,
      "dependencies": ["A"],
      "resource": "designer"
    }
  ]
}
```

Output: critical chain task list, project buffer size, feeding buffers, total project duration, full schedule.

**Use when:** Planning a new project, creating a schedule, or understanding which tasks are truly critical.

### `scripts/buffer_management.py`

Classifies current project health based on buffer consumption vs chain completion.

```bash
python3 scripts/buffer_management.py --file status.json
```

Input:
```json
{
  "buffer_size": 10,
  "buffer_consumed": 4,
  "chain_completion_pct": 0.5
}
```

Output: zone (green/yellow/red), trend assessment, recommended action.

**Use when:** Doing a weekly project status review, escalating to stakeholders, or deciding whether to activate contingency plans.

### `scripts/multi_project.py`

Staggers multiple projects sharing resources to avoid drum resource contention.

```bash
python3 scripts/multi_project.py --file portfolio.json
```

Input:
```json
{
  "projects": [
    {
      "id": "P1",
      "name": "Project Alpha",
      "tasks": [...]
    }
  ],
  "shared_resources": ["senior_dev", "architect"]
}
```

Output: drum resource identification, staggered project start dates, utilization analysis.

**Use when:** Planning a portfolio of projects, deciding project start dates, or investigating why all projects feel late simultaneously.

---

## Common Mistakes

**Mistake:** Padding individual tasks back after CCPM removes safety.
**Fix:** Explain that the safety still exists — it's just moved to the project buffer where it's visible and managed.

**Mistake:** Penalizing people when tasks run over their aggressive estimate.
**Fix:** Aggressive estimates are meant to be exceeded ~50% of the time. Late on a task is fine as long as the buffer is green.

**Mistake:** Celebrating when tasks finish under the aggressive estimate by immediately moving the next task up.
**Fix:** Early finishes should flow immediately to the next task (student syndrome prevention), but the schedule doesn't compress — the buffer grows, which is good.

**Mistake:** Managing by task completion dates instead of buffer consumption.
**Fix:** Remove due dates from individual tasks. Report only buffer status. Shift the culture from "did you hit your date" to "is the buffer green."
