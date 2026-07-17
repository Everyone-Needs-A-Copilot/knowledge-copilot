---
last_updated: 2026-07-17
status: active
name: competitive-analysis
description: >-
  Analyze a competitor's market position across product, momentum, and switching-cost dimensions
  using a structured Competitive Pressure Framework. Use when evaluating a competitive threat,
  preparing a battlecard, or deciding how to differentiate.
triggers:
  keywords: ["competitor", "competitive analysis", "battlecard", "market position", "differentiation",
             "positioning", "win-loss", "threat", "switching cost", "momentum"]
allowed-tools: Read, Write, Edit
---

# Competitive Analysis

## Overview

Apply the Competitive Pressure Framework to understand how much ground a competitor is gaining -- or losing -- against you in a specific account, segment, or market. Competitive pressure is made up of visible dynamics -- product advantages, market momentum, real weaknesses, and switching costs -- that shape whether a customer stays, leaves, or never considers you at all. This skill teaches how to identify, categorize, and act on those signals.

## Define Done

A competitive analysis is complete when:

- [ ] All 4 signal types identified (Advantage, Momentum, Weakness, Switching Cost)
- [ ] Each signal has evidence (not speculation)
- [ ] Signals are ranked by intensity (1-5 scale)
- [ ] Net competitive pressure determined (favoring the competitor or favoring you)
- [ ] Recommended actions address the dominant signals

## Prerequisites

- Situation context: which competitor, which account or segment, what's at stake
- Data sources: sales call notes, win/loss interviews, public materials (pricing pages, review sites, job postings)
- For enriched analysis: exported CRM notes or a win/loss interview transcript, if available

## Framework

The Competitive Pressure Framework identifies 4 types of signals acting on any competitive situation:

| Signal Type | Direction | Description | Example |
|-----------|-----------|-------------|---------|
| **Advantage** | Toward losing ground | A specific edge the competitor has today | "Their product ships a feature we don't have yet" |
| **Momentum** | Toward losing ground | The competitor is gaining traction | "They've won 3 deals in our pipeline this quarter" |
| **Weakness** | Toward holding ground | A real gap or vulnerability in the competitor's offering | "Their support SLAs are worse than ours" |
| **Switching Cost** | Toward holding ground | Friction that keeps the customer from moving | "Migrating their data would take 6+ weeks" |

### Threat Intensity Scale

| Level | Intensity | Indicator |
|-------|-----------|-----------|
| 1 | Awareness | Signal is mentioned casually, not yet acted on |
| 2 | Interest | Prospect or customer asks questions about the competitor |
| 3 | Concern | Competitor comes up unprompted in conversations |
| 4 | Urgency | Prospect or customer is actively evaluating the competitor |
| 5 | Crisis | A deal or renewal is actively at risk right now |

### Net Pressure Calculation

```
Net = (Sum of Advantage + Momentum intensities) - (Sum of Weakness + Switching Cost intensities)

Net > 0  -> Competitor is gaining ground -- focus on closing the advantage gap
Net = 0  -> Stalemate -- one signal shift tips the balance
Net < 0  -> You are well-positioned -- competitor unlikely to displace you
```

## Instructions

### Step 1: Gather Competitive Evidence (REQUIRED)

Collect data from available sources:

**From your own records:**
- Recent sales call notes and objection logs
- Past win/loss interview summaries
- Support and renewal conversation notes

**From public sources:**
- Competitor pricing pages and feature comparison pages
- Review sites (G2, Capterra, or your industry's equivalent)
- Job postings (signal where the competitor is investing)

**From direct observation:** quotes, behaviors, decisions, hesitations from prospects or customers.

### Step 2: Categorize Each Signal (REQUIRED)

For each signal identified, determine:
1. **Type:** Advantage, Momentum, Weakness, or Switching Cost
2. **Evidence:** Specific quote, data point, or observed behavior
3. **Intensity:** 1-5 scale
4. **Validated:** Has this been confirmed directly, or is it inferred?

### Step 3: Calculate Net Pressure (REQUIRED)

Sum the ground-losing signals (Advantage + Momentum) and ground-holding signals (Weakness + Switching Cost). Determine the net direction and magnitude.

### Step 4: Recommend Actions (REQUIRED)

Based on the net pressure direction:

| Net Direction | Strategy | Actions |
|---------------|----------|---------|
| Strong positive (>5) | Respond now | Close the top advantage gap, escalate internally |
| Weak positive (1-5) | Reinforce | Address the top weakness signal, lean on switching costs |
| Neutral (0) | Tip the balance | Find the one signal that's easiest to shift |
| Weak negative (-1 to -5) | Monitor | Keep tracking; no urgent action needed |
| Strong negative (<-5) | Hold position | Situation is stable -- revisit if new signals appear |

### Step 5: Validate Signals (OPTIONAL)

Use the next customer or prospect conversation to test your analysis, then mark which signals were confirmed versus which turned out to be inferred only.

## Examples

### Example: Renewal at Risk

**Situation:** Existing customer's renewal is approaching; a competitor has entered the conversation.

**Signals identified:**

| # | Type | Signal | Evidence | Intensity |
|---|------|--------|----------|-----------|
| 1 | Advantage | Competitor has a native mobile app | "Their app was the first thing our field team asked about" | 4 |
| 2 | Momentum | Competitor recently raised a large funding round | Public press release, increased ad spend observed | 2 |
| 3 | Weakness | Competitor's onboarding takes 2x longer | Reference call with a mutual former prospect | 3 |
| 4 | Switching Cost | Customer has 3 years of historical data and integrations | "We'd lose our whole audit trail if we moved" | 4 |

**Net calculation:**
- Ground-losing: 4 + 2 = 6
- Ground-holding: 3 + 4 = 7
- **Net: -1 (weak negative)**

**Strategy:** Monitor -- reinforce the switching-cost advantage in the renewal conversation while quietly scoping the mobile-app gap for next quarter's roadmap.

### Example: New Logo Evaluation

**Situation:** A prospect is actively comparing you against a well-known competitor.

| # | Type | Signal | Evidence | Intensity |
|---|------|--------|----------|-----------|
| 1 | Momentum | Competitor is the default choice in this vertical | "Everyone we talked to already uses them" | 4 |
| 2 | Advantage | Competitor has a lower entry price | Public pricing page comparison | 3 |
| 3 | Weakness | Competitor's support is community-forum-only | Review-site complaints about response time | 3 |
| 4 | Weakness | Competitor lacks a feature the prospect called "must-have" | Discovery call notes | 4 |

**Net: 7 - 7 = 0 (stalemate)**

**Strategy:** Tip the balance -- lead with the missing "must-have" feature, since it's the single easiest signal to shift in this deal.

## Quality Tests

### Signal Completeness Test
- All 4 signal types have been considered (not just advantage and momentum)
- **PASS:** Analysis includes at least one signal from each of the 4 types, or explicitly notes why a type has no signals
- **FAIL:** Only advantage and momentum signals listed -- weakness and switching cost ignored

### Evidence Test
- Every signal has specific evidence, not vague assertions
- **PASS:** Each signal cites a quote, data point, or observation
- **FAIL:** Signal listed as "they seem to be winning" without specific evidence

### Actionability Test
- Recommended actions directly address the dominant signals
- **PASS:** Top-intensity signal has a specific recommended action
- **FAIL:** Generic advice ("compete harder") that doesn't target a specific signal

### Validation Test
- Analysis distinguishes between observed and inferred signals
- **PASS:** Each signal marked as "validated" (confirmed directly) or "inferred" (analyst's assessment)
- **FAIL:** All signals presented with equal confidence regardless of evidence quality

## Guidelines

1. Always check all 4 signal types -- weakness and switching cost are easy to skip when a competitor feels scary
2. Higher-intensity signals deserve more investigation, not just acknowledgment
3. Net pressure direction determines strategy -- don't overreact to a single strong-negative signal
4. Validate inferred signals in the next conversation before acting on them
5. Signals change over time -- re-analyze after a lost deal, a won deal, or a competitor product launch
6. Cross-reference account-level signals (this specific deal) with market-level signals (the broader competitive landscape) for the full picture

## References

- Related skills: `pricing-models`
- Signal types reference: `reference/signal-types.md`
- Output template: `reference/output-template.md`
