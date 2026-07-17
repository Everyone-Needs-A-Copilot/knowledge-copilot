---
last_updated: 2026-04-02
status: active
---

# The Four-Column Structure

## Why Four Columns

Most action plans have two columns: task and owner. Some have three: task, owner, due date. The Transition Tree uses four columns because a plan without cause-effect reasoning is just a list of intentions. The four columns force the planner to articulate the logic that connects one step to the next.

| Column | What It Captures |
|--------|-----------------|
| `current_reality` | The verifiable state of the world before this step |
| `action` | The one concrete thing done in this step |
| `expected_effect` | The verifiable state of the world after this step |
| `rationale` | Why the action produces the expected effect |

The `rationale` column is where the plan becomes a hypothesis. Every step is a prediction: "if we do X in context Y, we expect Z." When Z doesn't happen, the rationale tells you which assumption failed.

## How the Chain Works

The chain is the load-bearing structure of a TrT. It works because each step's `expected_effect` describes the world the next step will operate on.

```
Step 1
  current_reality: [Starting state]
          action:  [What we do]
  expected_effect: [New state after step 1]
                        ↓  ← This connection must be plausible
Step 2
  current_reality: [Same as step 1's expected_effect, or a natural continuation]
          action:  [What we do next]
  expected_effect: [New state after step 2]
```

If step 2's `current_reality` assumes something that step 1's `expected_effect` didn't produce, there is a hidden step between them. Inserting the missing step is not "adding work" — it's making visible something the plan was already implicitly counting on.

## Business Example: Implementing a Pricing Change

A B2B SaaS company has three pricing tiers. Customers frequently complain that pricing is confusing. Conversion from the pricing page is low. The company wants to simplify to a single transparent tier and communicate value more clearly.

Here is the Transition Tree for the first phase of execution — communicating the change to the market.

---

### Step 1

| Column | Content |
|--------|---------|
| **current_reality** | We have no public pricing page; prospects must contact sales to learn pricing, and most leave before doing so |
| **action** | Publish a redesigned pricing page with one plan, transparent monthly pricing, and a self-serve trial CTA |
| **expected_effect** | Prospects can discover and understand our pricing without contacting sales |
| **rationale** | 34% of pre-sale support contacts are pricing questions (ticket analysis, Q3). A public page eliminates this friction. Self-serve information discovery is a proven conversion accelerant in B2B SaaS — prospects who can self-qualify convert at 2–3x the rate of those who must wait for sales outreach. |

---

### Step 2

| Column | Content |
|--------|---------|
| **current_reality** | Prospects can discover and understand our pricing without contacting sales |
| **action** | Send an email sequence to all free-tier users announcing the new pricing and offering a 20% discount if they upgrade within 30 days |
| **expected_effect** | Free users who have seen value are prompted to convert, and early upgraders are rewarded for acting before the broader announcement |
| **rationale** | Free-tier users have already experienced the product. Pricing opacity was the barrier, not product fit. A time-limited discount creates urgency without cheapening the brand. Historical A/B tests show time-limited upgrade offers convert at 3–4x standard upgrade prompts for this user cohort. |

---

### Step 3

| Column | Content |
|--------|---------|
| **current_reality** | Free users who have seen value are prompted to convert, and early upgraders are rewarded |
| **action** | Update all marketing channels (homepage, ads, social bio) to reflect the new simplified pricing message |
| **expected_effect** | New visitors to any marketing channel receive a consistent, simplified pricing message from first contact |
| **rationale** | Inconsistent messaging across channels creates cognitive friction. A prospect who sees "transparent, simple pricing" in an ad but lands on a page that says "contact us for pricing" loses trust. Consistency is the minimum requirement for the new pricing narrative to hold. |

---

### Step 4

| Column | Content |
|--------|---------|
| **current_reality** | New visitors receive a consistent, simplified pricing message from first contact |
| **action** | Run a 30-day analysis of pricing page conversion rate, trial start rate, and sales-assisted deal rate against pre-change baseline |
| **expected_effect** | We have evidence of whether the pricing change improved self-serve conversion or displaced it toward sales-assisted deals |
| **rationale** | The hypothesis is that transparent pricing increases self-serve conversion. This could fail if: (a) the price point is wrong, (b) the tier structure is still confusing, or (c) the product doesn't justify the price without sales explanation. Measuring before acting on signals prevents premature optimization. |

---

## What Makes This Plan Better Than a Task List

The equivalent task list:

```
TODO:
- Redesign pricing page
- Email free users
- Update marketing channels
- Review metrics after 30 days
```

Compare the two approaches:

| Dimension | Task List | Transition Tree |
|-----------|-----------|----------------|
| Why is step 1 first? | Unknown — assumed | Explicit: prospects can't evaluate without pricing information |
| What does step 2 depend on? | Unclear | Step 1's effect: prospects must first be able to self-serve the information before the email is useful |
| What does "success" look like after step 3? | Not defined | "New visitors receive a consistent pricing message from first contact" |
| What assumption are we testing in step 4? | None stated | The hypothesis that transparent pricing increases self-serve conversion |
| If step 2 fails to drive conversions, what do we learn? | Nothing — we just move to step 3 | The rationale points to three specific failure modes to investigate |

## Analyzing Rationale Strength

The rationale column is a risk register in disguise. The weaker the rationale, the higher the execution risk.

| Rationale Quality | Example | Risk |
|-------------------|---------|------|
| **Strong** | "34% of pre-sale contacts are pricing questions (ticket analysis, Q3). Removing this friction reduces sales team load and accelerates prospect decisions." | Low — based on data, specific causal theory |
| **Moderate** | "Self-serve pricing pages are a standard practice in B2B SaaS and generally improve conversion." | Medium — based on industry pattern, not your specific data |
| **Weak** | "This should help prospects understand pricing better." | High — no mechanism, no basis, no testable claim |
| **Missing** | *(no rationale provided)* | Very high — pure assertion with no visibility into assumptions |

When the rationale is weak or missing, the planner has two options:

1. **Gather evidence before executing.** Run a small experiment, check comparable cases, or interview customers.
2. **Accept the risk explicitly and plan a checkpoint.** Execute the step and immediately measure whether the expected effect materialized before proceeding.

The worst option: proceed as if the step will definitely produce the expected effect without acknowledging the uncertainty.

## When the Chain Breaks

If a step's expected effect doesn't materialize, stop. Do not proceed to the next step as planned.

The chain assumption has been violated. The next step's `current_reality` is no longer true, which means the next step's `action` may be operating on a world that doesn't exist.

Diagnosis:
1. Revisit the rationale of the failed step — which assumption failed?
2. Check whether the `current_reality` of the failed step was accurate
3. Insert a corrective step that addresses the failed assumption
4. Re-evaluate the remaining chain from the new actual state

This is a feature, not a bug. The TrT makes chain breaks visible instead of letting them silently corrupt downstream steps.
