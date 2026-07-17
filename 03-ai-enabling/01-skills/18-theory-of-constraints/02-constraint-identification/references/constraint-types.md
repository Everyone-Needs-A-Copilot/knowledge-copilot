---
last_updated: 2026-04-02
status: active
---

# Constraint Types

Goldratt identified five categories of constraints. Understanding the type is essential because the exploitation strategy differs radically between them.

---

## Physical Constraints

**Definition:** A tangible resource with limited capacity — a person, machine, tool, space, or infrastructure component.

**How to recognize it:**
- Work visibly queues in front of it
- It runs at near-100% utilization while others wait
- Adding one more unit of this resource would directly increase throughput

**Exploitation strategy:** Protect it from idle time and non-throughput work. Eliminate defects entering it. Cross-train a second person. Extend its effective hours before adding headcount.

**SaaS examples:**
- A single senior engineer who owns a critical codebase module
- A database server that becomes the bottleneck under peak load
- A single QA engineer covering all 8 developers

**Consulting examples:**
- A partner who must approve all client proposals
- A specialist (e.g., data engineer) shared across multiple project teams
- One conference room that all teams compete for

---

## Policy Constraints

**Definition:** A rule, habit, metric, approval gate, or decision process that limits throughput — not a physical shortage.

**How to recognize it:**
- The physical resources are available but work still waits
- Phrases like "we always do it this way" or "that needs to go through X"
- Removing the rule would increase flow immediately, with no capital expense

**Exploitation strategy:** Challenge whether the policy still serves its original purpose. Ask: "What was the risk this policy was designed to prevent? Does that risk still exist? Is the cost of the policy greater than the risk it prevents?"

**Why this type is so important:** Policy constraints are the most common type in knowledge work and the most overlooked. They are invisible because they feel like "correct behavior." A physical constraint is embarrassing; a policy constraint feels like governance.

**SaaS examples:**
- All code changes require a 48-hour review window regardless of size
- New features need approval from three separate teams before development starts
- Deployments only happen on Tuesdays to "reduce risk"
- Engineers must estimate in story points and re-estimate if scope changes

**Consulting examples:**
- All client deliverables require partner review before sharing
- New engagement pricing must go through finance for margin approval
- Consultants cannot contact client stakeholders without engagement manager involvement

---

## Market Constraints

**Definition:** The market will not absorb more output at the current price. Demand is the limiting factor, not internal capacity.

**How to recognize it:**
- Resources are underutilized across the board
- You could deliver more but clients are not buying
- Sales pipeline is thin relative to delivery capacity

**Exploitation strategy:** Improving internal flow does not help a market constraint. The investment goes into demand generation: marketing, sales enablement, product-market fit, pricing experiments, and new segments.

**The failure mode:** Organizations treat market constraints as internal constraints and optimize delivery when they should be building pipeline. Throughput Accounting will reveal this — if T/CU is low across all products and OE is the dominant cost, you have a market problem.

**SaaS examples:**
- Churn exceeds new ARR — you can deliver, but you cannot retain
- Product is technically excellent but has no market awareness
- Pricing is above what the target segment will pay

**Consulting examples:**
- Strong delivery reputation but no outbound marketing
- Referral-only pipeline that has plateaued
- Service offering that has no differentiated positioning

---

## Knowledge Constraints

**Definition:** Missing expertise, skill, or information required to proceed. Work stops because no one knows how to do it, not because of capacity.

**How to recognize it:**
- Work is waiting on one person who "knows how"
- Teams are blocked by decisions that require expertise they do not have
- Rework is high because work was done incorrectly due to missing knowledge

**Exploitation strategy:** Document what the knowledge-holder knows — remove the constraint from residing in one person. Pair programming, shadowing, and structured knowledge transfer are exploitation moves. Hiring is elevation.

**The failure mode:** Treating a knowledge constraint as a physical one. You cannot "add capacity" in hours when the bottleneck is expertise, not time.

**SaaS examples:**
- One engineer who understands the legacy authentication system
- A founder who is the only person who can do sales discovery calls effectively
- No one on the team who understands database query optimization

**Consulting examples:**
- A single partner with a specific industry relationship or domain expertise
- Methodology knowledge that lives only in the heads of senior staff
- Proposal writing that only one person knows how to do at the firm's quality standard

---

## Time Constraints

**Definition:** A fixed deadline or duration that limits options, regardless of available resources or knowledge.

**How to recognize it:**
- A hard external deadline (contract, regulatory, seasonal)
- A duration that cannot be compressed (curing time, legal waiting periods, client decision cycles)
- A sequencing dependency that creates forced waiting

**Exploitation strategy:** Identify which time constraints are truly fixed externally vs. internally assumed. Many time constraints are policy constraints in disguise ("we always give the client two weeks to review" is a policy, not a law).

**When time is the real constraint:** Focus on parallel work, pre-work before the trigger event, and identifying what can be done during the enforced wait.

**SaaS examples:**
- Annual renewal window — pipeline must be built before contract expiry, not after
- Regulatory approval process with fixed timelines
- A/B test requiring statistical significance before a decision can be made

**Consulting examples:**
- A client's budget cycle — proposals must land before Q4 planning, or wait a year
- A regulatory filing deadline that structures the whole engagement
- A client executive who is only available quarterly to make decisions

---

## Identifying Constraint Type in Practice

Use this sequence:

1. Is demand lower than capacity? → **Market constraint**
2. Is there a physical resource at near-100% utilization with queues? → **Physical constraint**
3. Is work waiting despite available people and tools? → **Policy constraint** (most common answer)
4. Is work blocked because nobody knows how to proceed? → **Knowledge constraint**
5. Is work waiting for an external clock to tick? → **Time constraint**

If you answered no to all of these and still have throughput problems, you likely have multiple overlapping constraints or a measurement problem — you are not observing where work actually waits.
