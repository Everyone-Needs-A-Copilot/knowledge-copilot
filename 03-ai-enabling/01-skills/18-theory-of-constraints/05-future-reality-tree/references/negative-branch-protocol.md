---
last_updated: 2026-04-02
status: active
---

# Negative Branch Protocol

A negative branch is a chain of cause-effect logic that starts from an injection and leads to a new undesirable effect. Detecting negative branches before implementation is one of the primary purposes of the Future Reality Tree.

This protocol provides a systematic, repeatable approach to negative branch identification and resolution.

---

## Why Negative Branches Occur

Good solutions change the system. Any change to a system creates ripple effects. Some of those effects are unintended and harmful. Three reasons they are missed:

1. **Tunnel vision:** Analysis focuses only on the problem being solved, ignoring the system's broader dynamics
2. **Optimism bias:** People proposing a solution naturally see the positives and discount the downsides
3. **Incomplete stakeholder perspective:** Effects on parties other than the primary beneficiary are not examined

The protocol addresses all three by making the search systematic and perspective-taking mandatory.

---

## Step 1: List All Stakeholders

Begin by listing every group of people who will be affected by the injection — directly or indirectly. Err on the side of inclusion. Common stakeholder categories:

- People who implement the injection (cost of change)
- People whose work processes change (disruption)
- People who depended on the current state (loss of benefit)
- Customers who interact with the changed system
- Partners, suppliers, or vendors in the affected flow
- People competing for the same resources

For each stakeholder, write one sentence: "How does this injection change what [stakeholder] experiences?"

---

## Step 2: Apply the Four Lenses

For each stakeholder, examine the injection through four lenses. Each lens reveals a category of negative branch.

### Lens 1 — Capacity

**Question:** Does this injection create new work, demand, or load on existing resources?

**Examples:**
- "This injection requires the QA team to run additional test cycles — do they have the capacity?"
- "This injection will generate 3x more inbound support tickets in the first 30 days"
- "The system that processes these new outputs is already at 90% utilization"

**Pattern:** An injection that removes a constraint in one place often moves the constraint elsewhere. The new constraint appears as a negative branch.

### Lens 2 — Incentives

**Question:** Does this injection change how someone is evaluated, measured, or rewarded in a way that creates perverse behavior?

**Examples:**
- "If we measure NPS at onboarding completion, customer success will pressure customers to give high scores prematurely"
- "If engineers are rewarded for shipping features quickly, they will skip the architectural improvements the injection requires"
- "If team A is measured on cycle time and team B is measured on defect rate, the injection that improves cycle time will increase defects"

**Pattern:** Measurement and incentive misalignment is a reliable source of negative branches in organizational injections.

### Lens 3 — Dependencies

**Question:** Does this injection depend on or remove a condition that something else in the system depends on?

**Examples:**
- "The current pricing process depends on the approval step this injection removes — without that step, pricing exceptions will go undetected"
- "This injection requires the CRM to be updated in real time — but the current CRM is only updated weekly"
- "Team B's workflow depends on receiving a specific artifact from Team A at a specific time; this injection changes when that artifact is produced"

**Pattern:** Systems are more interdependent than their change designs account for. What looks like a local change often removes a pin that holds something else in place.

### Lens 4 — Perception and Adoption

**Question:** How might stakeholders perceive this change, and how might their reaction undermine the injection?

**Examples:**
- "Customers may perceive the new onboarding structure as bureaucracy, reducing their engagement"
- "The sales team may perceive the new value quantification tool as extra work before they can close — they will use it inconsistently or not at all"
- "Management may interpret reduced headcount requests as an indication that the team is overstaffed — they will make cuts"

**Pattern:** Injections that require behavior change from people who did not request the change are especially vulnerable to adoption resistance.

---

## Step 3: Score Each Branch

For each identified negative effect, score it:

| Dimension | Scale | Description |
|-----------|-------|-------------|
| Likelihood | 1–5 | How probable is this effect if the injection proceeds as planned? |
| Severity | 1–5 | If this effect occurs, how harmful is it to the system's goal? |

**Risk score = Likelihood × Severity (max 25)**

| Score | Level | Action required |
|-------|-------|----------------|
| 15–25 | High | Trimming injection required. Do not proceed without one. |
| 6–14 | Medium | Design contingency plan. Consider trimming. |
| 1–5 | Low | Document. Monitor. No trimming required. |

Use `negative_branch.py` to run this scoring automatically and get stakeholder-grouped output.

---

## Step 4: Design Trimming Injections

For each high or medium-risk negative branch, design a trimming injection.

### Trimming injection criteria

A trimming injection must:
1. **Prevent or substantially reduce the negative branch** — it targets the cause of the negative effect, not its downstream symptoms
2. **Not undermine the original injection** — it is additive, not a compromise
3. **Be specific and actionable** — "monitor closely" is not a trimming injection; "assign a weekly review owner who has authority to pause the rollout if X metric drops below Y" is

### Trimming injection types

**Capacity trimming:** Free up capacity before or concurrent with the injection. Automate, reassign, or temporarily reduce load elsewhere.

**Incentive trimming:** Adjust measurement and reward structures so the new behavior is valued. Change what gets measured, or add a balancing metric.

**Dependency trimming:** Fix the upstream system that the injection disrupts. Ensure dependent processes are updated before the injection takes effect.

**Communication trimming:** Proactively address perception issues. Explain the injection's purpose, expected disruption timeline, and anticipated benefits to affected stakeholders before rollout.

---

## Step 5: Re-Test the Trimming Injections

A trimming injection is itself a change to the system. After designing it, apply this same protocol to it:

- Does the trimming injection create its own negative branches?
- Are those negative branches low enough risk to proceed?

Usually trimming injections are smaller in scope and their negative branches are minor. But if a trimming injection creates a significant new negative branch, it may need to be redesigned.

---

## Step 6: Document and Gate

Before implementation proceeds, the FRT with negative branches documented must be reviewed by:
- The person responsible for the injection's implementation
- A representative from each high-impact stakeholder group
- Someone not involved in the design (for blind-spot identification)

The review gate question is: "Are there any negative branches we have not identified?" Not "are all branches acceptable?" — because the purpose is completeness, not approval.

---

## Red Flags That Indicate Missing Negative Branches

- **Nobody is disadvantaged by this injection.** Every system change creates winners and losers. If nobody loses, the analysis is incomplete.
- **The injection requires no behavior change.** Real injections always require someone to do something differently. Who? What do they have to give up?
- **The injection solves the problem immediately.** Real changes take time and have transition costs. What happens during the transition period?
- **All stakeholders are enthusiastic.** Genuine enthusiasm is rare. If universal support is reported, assumptions about stakeholder impact have not been tested.

---

## Output of a Complete Negative Branch Protocol

1. Stakeholder list with one-sentence impact descriptions
2. Scored negative branches (minimum one per stakeholder per lens applied)
3. Trimming injection for every high-risk branch
4. Documented decision to accept, monitor, or defer medium-risk branches
5. Confirmation that trimming injections pass their own basic negative branch check

This output is appended to the FRT and handed to the Prerequisite Tree for sequencing.
