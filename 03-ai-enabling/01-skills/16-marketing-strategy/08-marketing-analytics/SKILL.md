---
last_updated: 2026-02-25
status: active
name: marketing-analytics
description: Define meaningful KPIs, build dashboards, and extract actionable insights from marketing data. Use when measuring marketing effectiveness.
triggers:
  files: ["**/marketing/**", "**/content/**"]
  keywords: ["analytics", "KPIs", "metrics", "dashboard", "data", "insights", "measurement", "ROI", "performance", "marketing metrics"]
allowed-tools: Read, Write, Edit
---

# Marketing Analytics

Data without insight is just noise. The purpose of marketing analytics is not to collect numbers but to answer one question: "Is what we are doing working, and how do we do more of what works?" Every metric you track should either help you make a decision or confirm a decision already made. If a metric does neither, stop tracking it.

The biggest analytics mistake marketers make is drowning in data. They build dashboards with 50 metrics and cannot tell you what any of them mean for the business. Discipline is about choosing the 5-10 metrics that actually matter and ignoring everything else until those metrics tell you to dig deeper.

---

## Framework

### Metric Hierarchy

Organize metrics in a pyramid. Start at the top and only drill down when the top level signals a problem.

| Level | Purpose | Review Frequency | Example |
|-------|---------|-----------------|---------|
| **North Star** | The single metric that best represents value delivery | Weekly | Monthly recurring revenue, active subscribers |
| **Primary Metrics** | 3-5 metrics that drive the North Star | Weekly | Lead volume, conversion rate, customer acquisition cost |
| **Secondary Metrics** | Channel/campaign performance metrics | Bi-weekly | Email open rate, social engagement rate, organic traffic |
| **Diagnostic Metrics** | Detailed metrics for troubleshooting | Only when investigating | Bounce rate by page, click map data, scroll depth |

**Rule:** If your North Star and Primary Metrics are healthy, do not spend time on Diagnostic Metrics. They are for investigation, not monitoring.

### KPI Selection Framework: Vanity vs Actionable

| Test | Vanity Metric | Actionable Metric |
|------|--------------|-------------------|
| **Can you act on it?** | "We got 10K page views" (so what?) | "Organic traffic from target keywords grew 15%" (double down on SEO) |
| **Does it connect to revenue?** | "We gained 500 followers" (followers do not pay bills) | "Email subscribers grew 12%, and subscribers convert at 5%" (revenue path clear) |
| **Is it a rate or a total?** | "We sent 50 emails" (volume says nothing) | "Email conversion rate is 3.2%, up from 2.8%" (efficiency improving) |
| **Can it go down and that is good?** | "Total spend increased" (is that good or bad?) | "Cost per lead dropped 20%" (clearly good) |

### Marketing Dashboard Design

#### What to Include

| Section | Metrics | Purpose |
|---------|---------|---------|
| **North Star** | 1 metric with trend line | Is the business moving in the right direction? |
| **Acquisition** | Traffic sources, lead volume, cost per lead | Where are customers coming from? |
| **Engagement** | Engagement rate, time on site, email metrics | Are people paying attention? |
| **Conversion** | Conversion rate by stage, cost per acquisition | Are we turning attention into action? |
| **Retention** | Churn rate, repeat engagement, NPS | Are people staying? |

#### What to Exclude

| Metric Type | Why Exclude | Exception |
|-------------|------------|-----------|
| Raw page views | No context without source and behavior | Include only as diagnostic |
| Total followers | Vanity unless tied to engagement rate | Include growth rate instead |
| Impressions | Seeing is not engaging | Include only for paid media efficiency |
| Total emails sent | Volume without engagement is spam | Include deliverability rate instead |

### Analytics Cadence

| Review Type | Frequency | Duration | Focus | Participants |
|-------------|-----------|----------|-------|-------------|
| **Daily glance** | Every workday | 5 min | Anomaly detection: anything broken or spiking? | Marketing lead |
| **Weekly review** | Weekly | 30 min | North Star and Primary Metrics trends | Marketing team |
| **Monthly deep dive** | Monthly | 60-90 min | Channel performance, campaign results, spend efficiency | Marketing + leadership |
| **Quarterly strategy** | Quarterly | Half day | KPI targets vs actuals, strategy adjustments, budget reallocation | Marketing + exec team |

---


## Define Done

- [ ] Strategy grounded in audience data and market context
- [ ] Channels and tactics aligned to audience behavior
- [ ] Success metrics defined with specific targets
- [ ] Budget and resource requirements estimated

## Application

### Insight Extraction Methodology

Data becomes useful only when it moves through this pipeline:

| Stage | Activity | Output |
|-------|----------|--------|
| **Data** | Collect raw numbers from platforms and tools | Clean, accurate dataset |
| **Pattern** | Identify trends, anomalies, correlations | "X is going up/down/correlated with Y" |
| **Insight** | Explain why the pattern exists | "X is going up because we changed Y, which affected Z" |
| **Action** | Decide what to do about it | "We will do more of Y" or "We will investigate Z" |

**Example walkthrough:**

| Stage | Example |
|-------|---------|
| Data | Blog traffic increased 40% month-over-month |
| Pattern | The increase came from 3 posts about topic X, all ranking on page 1 |
| Insight | Topic X has high search demand and low competition; our content matches search intent well |
| Action | Create 5 more posts on topic X subtopics this quarter, update the 3 ranking posts for freshness |

### Reporting Templates

#### Weekly Report Structure

| Section | Content |
|---------|---------|
| **Headline** | One sentence: what was the most important thing that happened this week? |
| **North Star** | Current value, trend direction, week-over-week change |
| **Wins** | 2-3 things that worked well, with specific numbers |
| **Concerns** | 1-2 things that need attention, with context |
| **Actions** | What we are going to do about the concerns |

#### Monthly Report Structure

| Section | Content |
|---------|---------|
| **Executive summary** | 3-5 bullet points: month in review |
| **KPI scorecard** | All primary metrics vs targets, with traffic lights (green/yellow/red) |
| **Channel performance** | Each channel's contribution and efficiency |
| **Campaign highlights** | Top-performing campaigns with ROI |
| **Budget vs actual** | Spend efficiency and allocation review |
| **Insights and actions** | 3-5 insights with specific next steps |
| **Next month focus** | What we are prioritizing and why |

### Common Metric Traps

| Trap | What Happens | How to Avoid |
|------|-------------|-------------|
| **Correlation vs causation** | "We posted on Tuesday and got more traffic, so Tuesday is best" | Control variables, test over multiple instances |
| **Small sample size** | "This email had a 50% open rate!" (sent to 10 people) | Set minimum sample thresholds before drawing conclusions |
| **Survivorship bias** | "Our blog posts average 5 min read time" (ignoring 80% who bounced in 3 seconds) | Include the full picture, not just successful interactions |
| **Attribution confusion** | "Organic search drove 100 conversions" (they saw 3 ads first) | Use multi-touch attribution for high-stakes decisions |
| **Averaging averages** | Averaging channel averages gives wrong numbers | Weight averages by volume or use medians |
| **Period-over-period only** | "Traffic is up 20% month-over-month!" (but it is seasonal) | Compare to same period last year and month-over-month |
| **Metric gaming** | Team optimizes for the metric, not the outcome | Pair every metric with a counter-metric |

### Counter-Metric Pairing

For every metric you incentivize, track a counter-metric that prevents gaming:

| Primary Metric | Gaming Risk | Counter-Metric |
|---------------|-------------|----------------|
| Lead volume | Low-quality leads to hit numbers | Lead-to-opportunity conversion rate |
| Email list size | Buying lists or loose opt-ins | Engagement rate, unsubscribe rate |
| Traffic | Clickbait titles, irrelevant keywords | Bounce rate, time on page |
| Conversion rate | Reducing traffic to only high-intent visitors | Total conversions (absolute number) |
| Social followers | Buying followers, follow-for-follow | Engagement rate per post |
| Content output | Quantity over quality | Engagement per piece, traffic per piece |

---

## Quick Reference

### Analytics Setup Checklist

1. Define North Star metric tied to business value
2. Select 3-5 Primary Metrics that drive the North Star
3. Pair each primary metric with a counter-metric
4. Set targets for each metric (baseline + goal)
5. Build a dashboard with only North Star and Primary Metrics visible by default
6. Establish analytics cadence (daily, weekly, monthly, quarterly)
7. Create reporting templates for weekly and monthly reviews
8. Set anomaly alerts for critical metrics (significant drops or spikes)
9. Train the team on insight extraction: data, pattern, insight, action
10. Review and prune metrics quarterly (remove anything nobody acts on)

### Data Storytelling Principles

| Principle | Application |
|-----------|------------|
| **Lead with the insight, not the data** | "We should invest more in SEO" not "Here is a chart of organic traffic" |
| **Context over numbers** | "15% growth vs our 10% target" not just "15% growth" |
| **Comparisons make numbers meaningful** | "Better than last quarter" or "above industry benchmark" |
| **One chart, one message** | Each visualization should make exactly one point |
| **So what? Now what?** | Every data point should end with implication and action |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | What to Do Instead |
|-------------|-------------|-------------------|
| **Tracking everything** | Data overload paralyzes decision-making | Track 5-10 metrics that drive decisions |
| **Dashboard as decoration** | Beautiful dashboards nobody looks at waste everyone's time | If nobody reviews it weekly, delete it |
| **Reporting without insight** | "Here are the numbers" without "here is what they mean" | Every report must include insight and action |
| **Monthly-only review** | Problems fester for 30 days before detection | Daily glance for anomalies, weekly for trends |
| **Vanity metric presentations** | Showing big numbers that mean nothing to the business | Connect every metric to revenue or strategic objective |
| **Post-hoc rationalization** | Finding data to support a decision already made | Define hypotheses before looking at data |
| **Ignoring counter-metrics** | Optimizing one number at the expense of everything else | Always pair metrics to prevent gaming |
| **No baseline** | "We got 1,000 leads this month" -- is that good? | Establish baselines before setting targets |


## Quality Tests

### Audience Alignment Test
- Strategy targets where the audience actually is, not assumptions
- **PASS:** Channel selection backed by audience research or data
- **FAIL:** Channels chosen based on trends rather than audience behavior

### Measurability Test
- Every tactic has a specific, measurable success metric
- **PASS:** KPIs defined with target numbers and measurement method
- **FAIL:** Goals are vague ('increase awareness') without measurable targets

