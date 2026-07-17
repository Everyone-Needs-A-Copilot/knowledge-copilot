---
last_updated: 2026-02-25
status: active
name: funnel-analysis
description: Analyze marketing funnels stage by stage -- identify drop-offs, optimize conversions, and diagnose bottlenecks. Use when improving conversion rates or diagnosing funnel issues.
triggers:
  files: ["**/marketing/**", "**/content/**"]
  keywords: ["funnel", "conversion", "drop-off", "optimization", "leads", "pipeline", "stages", "conversion rate", "bottleneck"]
allowed-tools: Read, Write, Edit
---

# Funnel Analysis

Every business has a funnel, whether they have mapped it or not. People discover you, some get interested, fewer consider buying, and a fraction actually do. Funnel analysis is the discipline of understanding exactly where people drop off and why, so you can fix the biggest leaks first. It is not about optimizing everything simultaneously. It is about finding the one stage where the most value is being lost and fixing that first.

The math is ruthless and clarifying. If 1,000 people visit your site and 1% convert, improving that to 2% doubles your revenue. But if the problem is actually that only 100 people visit in the first place, no conversion optimization will save you. Funnel analysis tells you where to focus.

---

## Framework

### Funnel Stage Framework

| Stage | Definition | User Mindset | Key Metric |
|-------|-----------|-------------|-----------|
| **Awareness** | Person learns you exist | "Huh, what's this?" | Reach, impressions, new visitors |
| **Interest** | Person engages with content | "This is relevant to me" | Engagement rate, time on site, follows |
| **Consideration** | Person evaluates your offering | "Could this solve my problem?" | Page visits (pricing, features), demo requests, email signups |
| **Decision** | Person decides to buy | "I'm going with this" | Cart additions, trial starts, proposal requests |
| **Action** | Person completes purchase | "Done, I bought it" | Purchases, signups, closed deals |
| **Retention** | Person returns and stays | "This was worth it, I'm staying" | Repeat purchase, renewal rate, NPS |

### Stage-by-Stage Analysis Template

For each stage transition, calculate the conversion rate and compare to benchmarks.

| Transition | Calculation | Your Rate | Benchmark Range | Status |
|-----------|------------|-----------|----------------|--------|
| Awareness to Interest | (Engaged visitors / Total visitors) x 100 | _% | 15-30% | |
| Interest to Consideration | (Consideration actions / Engaged visitors) x 100 | _% | 10-25% | |
| Consideration to Decision | (Decision actions / Consideration actions) x 100 | _% | 15-40% | |
| Decision to Action | (Completed purchases / Decision actions) x 100 | _% | 30-70% | |
| Action to Retention | (Repeat customers / First-time customers) x 100 | _% | 20-60% | |

**Note:** Benchmark ranges vary widely by industry, business model, and price point. Use these as starting reference points, then build your own baselines.

### Conversion Rate Benchmarks by Channel

| Channel | Awareness to Interest | Interest to Consideration | Overall Conversion |
|---------|---------------------|--------------------------|-------------------|
| **Organic search** | 20-35% | 10-20% | 2-5% |
| **Paid search** | 25-40% | 15-25% | 3-8% |
| **Social media (organic)** | 10-20% | 5-15% | 0.5-3% |
| **Social media (paid)** | 15-30% | 10-20% | 1-5% |
| **Email marketing** | 30-50% | 15-30% | 3-10% |
| **Referral** | 25-45% | 20-35% | 5-15% |
| **Direct** | 35-55% | 20-40% | 5-15% |

### Drop-Off Diagnosis Framework

When you identify a stage with significant drop-off, diagnose the root cause:

| Drop-Off Location | Common Causes | Diagnostic Steps |
|-------------------|--------------|-----------------|
| **Awareness to Interest** | Wrong audience, weak hook, irrelevant content | Check traffic source quality, landing page relevance, bounce rate by source |
| **Interest to Consideration** | Unclear value prop, poor content quality, no clear next step | Analyze page flow, check CTA clarity, review content engagement depth |
| **Consideration to Decision** | Price objection, trust gap, competitor comparison | Review pricing page behavior, check for social proof, analyze exit pages |
| **Decision to Action** | Friction in purchase process, unexpected costs, complex checkout | Analyze cart abandonment, check form completion rates, review checkout steps |
| **Action to Retention** | Poor onboarding, product-expectation mismatch, no engagement loop | Review onboarding completion, first-use metrics, support tickets |

---


## Define Done

- [ ] Strategy grounded in audience data and market context
- [ ] Channels and tactics aligned to audience behavior
- [ ] Success metrics defined with specific targets
- [ ] Budget and resource requirements estimated

## Application

### Funnel Visualization Best Practices

#### Building a Useful Funnel Visualization

| Principle | Application |
|-----------|------------|
| **Show absolute numbers AND percentages** | "1,000 visitors (100%) -> 200 engaged (20%)" not just percentages |
| **Include time dimension** | How long does each stage take? Where do people stall? |
| **Segment by source** | Different channels produce different funnel shapes |
| **Show week-over-week trend** | A snapshot is less useful than a trend |
| **Highlight the biggest leak** | Visually call out the stage with the largest drop-off |

#### Funnel Shape Diagnosis

| Funnel Shape | What It Looks Like | What It Means | Action |
|-------------|-------------------|--------------|--------|
| **Wide top, thin everywhere** | Massive awareness, tiny conversion | Audience-offer mismatch or terrible experience | Fix targeting or dramatically improve offer |
| **Narrow top, decent conversion** | Low awareness but those who find you buy | You have product-market fit but a discovery problem | Invest in awareness and top-of-funnel |
| **Even narrowing** | Steady, proportional drop at each stage | Healthy funnel, optimize incrementally | Find the stage with highest leverage |
| **Cliff at one stage** | Sharp drop at a specific point | Single critical bottleneck | Focus all optimization here |
| **Leaky middle** | Good awareness, good decision-to-action, weak middle | Consideration stage is failing | Improve content, proof, and nurture in the middle |

### Optimization Priority Matrix

Fix the biggest leak first. Use this framework to prioritize:

| Factor | Weight | Assessment |
|--------|--------|-----------|
| **Volume of drop-off** | 40% | How many people are you losing at this stage? |
| **Revenue impact** | 30% | How close to purchase are the people dropping off? (Closer = higher impact) |
| **Ease of fix** | 20% | Can you address this quickly, or is it a structural problem? |
| **Confidence in diagnosis** | 10% | How sure are you about the root cause? |

**Priority scoring:**

| Score | Priority Level | Action |
|-------|---------------|--------|
| 4.0-5.0 | Critical | Fix this now, it is costing significant revenue |
| 3.0-3.9 | High | Address in current sprint/cycle |
| 2.0-2.9 | Medium | Plan for next optimization cycle |
| Below 2.0 | Low | Monitor, do not invest resources yet |

### A/B Testing Framework for Funnel Stages

| Stage | What to Test | Minimum Sample | Test Duration |
|-------|-------------|---------------|--------------|
| **Awareness** | Ad copy, targeting, creative | 1,000 impressions per variant | 1-2 weeks |
| **Interest** | Headlines, content format, CTAs | 500 visitors per variant | 2-3 weeks |
| **Consideration** | Landing page layout, value prop messaging, social proof | 300 visitors per variant | 2-4 weeks |
| **Decision** | Pricing presentation, guarantee language, urgency | 200 visitors per variant | 2-4 weeks |
| **Action** | Checkout flow, form fields, payment options | 100 completions per variant | 2-4 weeks |

**A/B testing rules:**

1. Test one variable at a time per stage
2. Reach statistical significance before declaring a winner (95% confidence minimum)
3. Run tests for full business cycles (include weekdays and weekends)
4. Document every test result, even failures -- they are data
5. Winner becomes the new control for the next test

### Micro-Conversion Tracking

Do not just track stage-to-stage conversion. Track micro-conversions within each stage to pinpoint exactly where friction occurs.

| Stage | Micro-Conversions to Track |
|-------|--------------------------|
| **Awareness** | Ad click, search result click, social post click |
| **Interest** | Scroll depth, video play, content piece started, content piece completed |
| **Consideration** | Pricing page visit, feature comparison viewed, case study read, demo video watched |
| **Decision** | Cart addition, form started, trial started, quote requested |
| **Action** | Form completed, payment entered, purchase confirmed, account created |
| **Retention** | Second login, feature adopted, second purchase, referral made |

---

## Quick Reference

### Funnel Analysis Process

1. Map your funnel stages with clear definitions for each transition
2. Instrument tracking for every stage and micro-conversion
3. Collect baseline data for a full business cycle (minimum 30 days)
4. Calculate conversion rates for each stage transition
5. Compare to benchmarks and your own historical data
6. Identify the stage with the largest absolute drop-off
7. Diagnose root cause using the drop-off diagnosis framework
8. Prioritize using the optimization priority matrix
9. Design and run A/B test on the highest-priority bottleneck
10. Measure impact, document learning, move to next bottleneck

### Funnel Health Quick Check

| Signal | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| **Overall conversion rate** | At or above channel benchmarks | Within 50% of benchmarks | Below 50% of benchmarks |
| **Stage-to-stage consistency** | No single stage drops more than 60% | One stage drops 60-80% | One stage drops 80%+ |
| **Trend direction** | Conversion rates stable or improving | Flat for 3+ months | Declining for 2+ months |
| **Channel variance** | Top and bottom channels within 3x | Within 5x | Greater than 5x difference |
| **Micro-conversion completion** | Above 70% within-stage completion | 50-70% | Below 50% |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | What to Do Instead |
|-------------|-------------|-------------------|
| **Optimizing the wrong stage** | Polishing the checkout when the problem is nobody visits the site | Find the biggest absolute leak first |
| **Percentages without absolutes** | "50% conversion rate!" on 10 visitors means nothing | Always report both absolute numbers and percentages |
| **Funnel without segmentation** | Averaging across channels hides that one channel converts at 10% and another at 0.5% | Segment funnel by source, audience, and campaign |
| **Testing too many things** | Changing headline, CTA, layout, and color simultaneously | Test one variable at a time |
| **Declaring winners too early** | "After 2 days, Variant B is winning!" with 30 conversions | Wait for statistical significance (95% confidence) |
| **Ignoring retention** | Acquiring customers who leave immediately is a leaky bucket | The funnel does not end at purchase |
| **One-time analysis** | Funnels change as traffic sources, audience, and product evolve | Review funnel health monthly, deep-dive quarterly |
| **No micro-conversion tracking** | "People drop off in Consideration" but you do not know where or why | Track specific actions within each stage |


## Quality Tests

### Audience Alignment Test
- Strategy targets where the audience actually is, not assumptions
- **PASS:** Channel selection backed by audience research or data
- **FAIL:** Channels chosen based on trends rather than audience behavior

### Measurability Test
- Every tactic has a specific, measurable success metric
- **PASS:** KPIs defined with target numbers and measurement method
- **FAIL:** Goals are vague ('increase awareness') without measurable targets

