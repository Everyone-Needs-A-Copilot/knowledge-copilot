---
last_updated: 2026-04-02
status: active
---

# Little's Law

## The Formula

```
L = λ × W
```

| Variable | Meaning | Example |
|----------|---------|---------|
| **L** | Average number of items in the system (WIP) | 20 tasks in progress |
| **λ** (lambda) | Throughput — items completed per unit time | 5 tasks/week |
| **W** | Average time an item spends in the system (lead time) | 4 weeks |

The relationship: 20 = 5 × 4. ✓

Little's Law is a mathematical theorem, not a heuristic or rule of thumb. It holds for any stable system, regardless of distribution of arrival times, service times, or number of servers. The only requirement is that the system is stable (average arrival rate ≤ average service rate).

---

## The Key Insight

**Lead time is directly proportional to WIP.** If you want shorter lead times, reduce WIP. This is the single most powerful insight in flow management.

To cut lead time in half: cut WIP in half. No process improvements required. No more people needed. No technology investment. Just do less at once.

This feels wrong to managers. "We have 30 items in progress because we have 30 items to deliver. If we limit WIP we'll deliver fewer things." But that's not what happens:

- With WIP = 30 and throughput = 5/week: lead time = 6 weeks
- With WIP = 10 and throughput = 5/week: lead time = 2 weeks
- **Throughput is unchanged. Lead time is cut by 67%.**

The items don't disappear. They get delivered faster. The 30 items that previously took 6 weeks to deliver now take the same time — but each individual item is delivered in 2 weeks instead of waiting in queue.

---

## Practical Implications

### 1. WIP limits are a lead time control

Setting a WIP limit is not about working less. It's about controlling the promise you make to stakeholders: "When we take something on, here's how long it takes."

Without WIP limits, lead times are unpredictable because WIP fluctuates. With WIP limits, lead time becomes predictable.

### 2. Multitasking always increases lead time

Adding a third project to a person who is already on two doesn't deliver the third project faster. It slows all three. Little's Law proves this: total WIP increases, throughput stays the same (the person isn't faster), so lead time increases for everything.

### 3. "Starting is not finishing"

A common failure: teams start new work as fast as possible to "show progress." This maximizes WIP. Little's Law says this maximizes lead time. The opposite of the intent.

The correct behavior: finish items before starting new ones. "Stop starting, start finishing."

### 4. Batch size affects lead time

Even without changing throughput or WIP limits, breaking large work items into smaller ones reduces average lead time. A 10-day task has a longer expected lead time than 5 two-day tasks, because each two-day task completes and delivers value sooner.

---

## Applying Little's Law

### To find optimal WIP:
```
WIP = throughput × target_lead_time
```
Example: If we complete 8 items per week and want a 2-week lead time, max WIP = 16.

### To diagnose current lead time:
```
lead_time = current_WIP / throughput
```
Example: 40 items in progress, completing 5/week → average lead time = 8 weeks.

### To set WIP limits from a throughput target:
```
WIP_limit = desired_throughput × acceptable_lead_time
```
Example: We want to deliver 10 features per month (≈2.5/week) with a max 3-week lead time → WIP limit = 7.5, round down to 7.

---

## When Little's Law Doesn't Apply Directly

Little's Law assumes a **stable system**: arrival rate ≤ service rate, and averages are meaningful. Watch out for:

**Non-stationary systems:** If demand is growing rapidly or the team size is changing, averages are unstable. Trend analysis is more useful than point-in-time calculations.

**Multi-class work:** If some items are urgent (bugs) and some are planned (features), they have different lead time expectations. Separate them into different queues, each with its own WIP limit, rather than applying one global WIP limit.

**Outliers distorting means:** A few very long-running items inflate average lead time. Use median and P85 for planning rather than mean. Little's Law still holds for medians (approximately) if the system is symmetric.

**Blocked items:** Items that are in WIP but not actively being worked (waiting for a dependency, waiting for an external decision) inflate WIP without representing genuine system load. Track "active WIP" separately from "blocked WIP."

---

## Little's Law and the TOC Connection

Little's Law and DBR are complementary. DBR tells you where to place the buffer (in front of the constraint) and how fast to release work (rope = drum rate). Little's Law tells you what WIP level corresponds to your lead time target.

Together they give you a complete flow management system:
1. Identify the constraint (drum)
2. Set the rope (WIP limit = drum_rate × target_lead_time)
3. Protect the constraint with a time buffer
4. Manage by buffer health

The rope setting from Little's Law ensures the system doesn't exceed lead time targets even under variable demand.
