---
last_updated: 2026-04-02
status: active
---

# The Four Questions Framework

Goldratt's four questions for evaluating any technology investment. Use them before purchasing, during implementation planning, and as a post-implementation audit.

---

## Overview

| Question | What It Surfaces |
|----------|-----------------|
| Q1: What is the power of the technology? | The specific new capability being purchased |
| Q2: What limitation does it diminish? | The constraint the technology addresses |
| Q3: What rules helped us accommodate the limitation? | The compensating behaviors to be retired |
| Q4: What rules should we use now? | The redesigned processes that capture the technology's value |

Value realization depends on completing all four. Investments that stop at Q2 — "we identified the limitation and bought the fix" — routinely disappoint.

---

## Question 1: What is the Power of the Technology?

This question asks for the specific new capability: what can you do now that was previously impossible or impractical?

### What a Good Answer Looks Like

"This technology enables [specific new capability] that was previously [impossible / required X hours / error-prone / available only to certain roles]."

Examples:
- "Enables any team member to see whether a part is available in any warehouse in real time, without calling anyone"
- "Enables sales managers to see deal velocity metrics updated continuously throughout the day, without collecting reports"
- "Enables the finance team to close the books in 2 days instead of 12 by automating reconciliation"

### What a Bad Answer Looks Like

- "It's faster and more efficient" (faster than what? efficient how?)
- "It improves our processes" (which processes? what does improved mean?)
- "Everyone else in our industry uses it" (not a power statement — a competitive pressure argument)
- "It's cloud-based" (a delivery mechanism, not a power)

### Why It Matters

If you cannot articulate the power of the technology, you cannot identify which limitation it diminishes (Q2). And if you can't answer Q2, you cannot identify the rules to change (Q3 and Q4). The vagueness of Q1 is the single most common root cause of underperforming technology investments.

---

## Question 2: What Limitation Does It Diminish?

This question asks which specific constraint in your current system the technology reduces. It is not asking which limitation the vendor says it reduces. It is asking which limitation in YOUR system.

### How to Find Your Real Limitation

Start from the undesirable effects you experience:
- Where are orders/requests delayed?
- Where do errors concentrate?
- What do your customers or internal teams complain about most?
- Where does work pile up?

Then ask: "Is this limitation something the technology in Q1 actually addresses?"

### The Constraint Match Test

The technology is addressing a real constraint if:
- The limitation in Q2 is currently causing measurable throughput loss
- Removing the limitation would change what you can accomplish, not just how you accomplish it
- The limitation is currently the BINDING constraint — not a secondary bottleneck

If the technology addresses a limitation that is not the binding constraint, it is addressing a non-constraint. By definition, improving a non-constraint cannot improve system throughput, no matter how well the technology works.

### Example: The Wrong Limitation

A company buys document management software because "finding files is slow." The actual binding constraint is: client onboarding takes 6 weeks because legal review is a bottleneck. Fast file finding doesn't help legal review speed. The document management software was technically excellent and completely irrelevant to the binding constraint.

---

## Question 3: What Rules Helped Us Accommodate the Limitation?

Every limitation generates compensating rules. These rules were rational responses to a real problem. The problem with them is that they persist long after the limitation that caused them has been removed.

### How to Find Your Rules

For each limitation in Q2, ask:
- "What do we do today because we can't [old limitation]?"
- "What policies did we put in place to reduce the risk caused by [old limitation]?"
- "What workarounds do people use because [old limitation] exists?"
- "What safeguards did we build because [old limitation] made mistakes expensive?"

Then work backward: "Why do we have this policy/rule/process?" Keep asking why until you hit the limitation.

### Examples

| Technology | Limitation Diminished | Old Rules Created by Limitation |
|-----------|----------------------|--------------------------------|
| Real-time inventory system | No visibility without physical count | Weekly cycle counts; safety stock rules; batch ordering minimums |
| Automated testing | Manual testing is slow and error-prone | Feature freeze 2 weeks before release; large QA team; no deployments on Fridays |
| CRM with pipeline tracking | Pipeline status required manual collection | Weekly sales meetings; Friday forecast updates; no coaching between meetings |
| Cloud computing | Long hardware provisioning cycles | IT infrastructure committee approval for new servers; 6-month capacity planning cycles |

### The Invisible Rules Problem

Most rules are invisible because they've become "the way we work." They're embedded in job descriptions, meeting rhythms, approval chains, and unwritten norms. The archaeology required to surface them is often the most difficult part of the four-question process.

Useful prompt: ask recently hired employees what they find surprising or inefficient about how things are done. People who haven't yet internalized the rules can often see them more clearly.

---

## Question 4: What Rules Should We Use Now?

This is where the value of the technology actually lives. With the limitation diminished, what would you design if you were starting from scratch?

### The Design Principle

Don't ask "how do we update our current rules?" Ask "if this capability had existed from day one, how would we have designed our process?"

The current rules were optimized for a world with the old limitation. The new rules should be optimized for a world without it.

### Examples

| Old Rule (from Q3) | New Rule (for Q4) |
|-------------------|------------------|
| Weekly inventory cycle counts | Continuous reconciliation via real-time system; cycle counts only when system flags discrepancy |
| Feature freeze 2 weeks pre-release | Deploy continuously; automated test suite runs on every commit; no freeze needed |
| Friday forecast updates | Pipeline health metrics monitored continuously; alerts when deal velocity drops below threshold |
| 6-month hardware capacity planning | Infrastructure capacity allocated and provisioned on-demand per project; no planning cycle |

### The Rule Change Must Be Mandatory

New rules don't enforce themselves. The most common failure at Q4: the new rules are defined but the old rules continue to operate in parallel. People fall back on the familiar when the new process is unclear or when the technology is unavailable.

New rules must be:
1. **Specific and measurable** — not "review pipeline more often" but "daily 15-minute pipeline review every morning at 9am using CRM dashboard"
2. **Formally adopted** — announced, documented, and enforced by leadership
3. **Backed by accountability** — someone is responsible for whether the new rule is being followed
4. **Sunset the old rule explicitly** — formally discontinue the compensating behavior, don't just add the new one alongside it

---

## Worked Example: ERP System

### Q1: What is the power of the technology?
"Enables real-time visibility into production status, inventory levels, and order fulfilment across all departments without manual data collection."

### Q2: What limitation does it diminish?
"Previously, production status was tracked in department-specific spreadsheets updated manually at end of shift. Cross-department visibility required email chains or weekly operations meetings."

### Q3: What rules accommodated the limitation?
- Monday operations meeting (only way to share cross-department status)
- 2-week order confirmation window (buffer for uncertainty in production status)
- Department managers manually compiled status reports on Friday
- Expediting team existed to track hot orders through the system
- Safety stock of 3 weeks on all finished goods (to buffer for status uncertainty)

### Q4: What rules should we use now?
- Daily 15-minute stand-up using live ERP dashboard replaces Monday operations meeting
- Order confirmation in 24 hours (status is now visible in real time; no buffer needed)
- Department managers review ERP daily; no manual compilation required
- Expediting role eliminated; ERP flags late orders automatically
- Safety stock reduced to 1 week; ERP manages replenishment triggers

### Value at Stake

If Q3 rules are retained after ERP implementation:
- Monday operations meeting still runs (consuming time with no information advantage)
- 2-week confirmation window remains (losing competitive advantage)
- Expediting team still employed (adding cost with no function)
- 3-week safety stock maintained (tying up capital the ERP makes unnecessary)

The ERP works perfectly. The organization simply continues to behave as if it doesn't exist.
