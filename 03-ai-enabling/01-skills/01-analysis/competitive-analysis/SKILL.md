---
last_updated: 2026-02-25
status: active
name: competitive-analysis
description: Analyze competitive landscape to identify positioning opportunities and threats. Map competitors by segment, compare capabilities, and find differentiation angles. Use when entering markets, planning strategy, or responding to competitive moves.
triggers:
  keywords: ["competitive", "analysis", "analyze", "landscape", "identify", "positioning", "opportunities", "threats", "competitors", "segment"]
allowed-tools: Read, Write, Edit, WebSearch
---

# Competitive Analysis

## Overview

Systematically analyze the competitive landscape to inform strategic decisions. Map direct and indirect competitors, assess their strengths and weaknesses, identify positioning opportunities, and monitor competitive moves. Produces actionable intelligence, not just information.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Define Competitive Context

Clarify what competition you're analyzing:

| Context Element | Question |
|-----------------|----------|
| **Market scope** | What market/segment are we analyzing? |
| **Customer job** | What job are customers hiring solutions for? |
| **Decision** | What strategic decision will this inform? |
| **Time horizon** | Current state, 1-year outlook, or 3-year trends? |

```markdown
## Competitive Context

**Market:** [Market/segment definition]
**Customer job:** [Job to be done being addressed]
**Decision this informs:** [Strategic question]
**Time horizon:** [Current / 1 year / 3 year]
```

### Step 2: Identify Competitors

Map the competitive landscape by type:

| Competitor Type | Definition | Examples |
|-----------------|------------|----------|
| **Direct** | Same product, same customer | Competing SaaS tools |
| **Indirect** | Different product, same job | Spreadsheets vs specialized software |
| **Potential** | Could enter market | Adjacent players, well-funded startups |
| **Substitute** | Non-purchase alternatives | DIY, status quo, inaction |

```markdown
## Competitor Map

### Direct Competitors
| Competitor | Market Position | Est. Revenue | Funding |
|------------|-----------------|--------------|---------|
| [Name] | [Position] | [$X] | [$X or Public] |

### Indirect Competitors
| Competitor | How They Solve Job | Overlap |
|------------|-------------------|---------|
| [Name] | [Approach] | [% of use cases] |

### Potential Entrants
| Company | Why They Might Enter | Likelihood |
|---------|---------------------|------------|
| [Name] | [Rationale] | High/Med/Low |

### Substitutes
| Alternative | When Customers Choose This |
|-------------|---------------------------|
| [Alternative] | [Scenario] |
```

### Step 3: Gather Intelligence

Collect data from multiple sources:

| Source | What It Shows | Reliability |
|--------|---------------|-------------|
| **Website/product** | Positioning, features, pricing | High |
| **Reviews (G2, Capterra)** | Customer perception, pain points | Medium |
| **Job postings** | Strategy, growth areas, tech stack | Medium |
| **LinkedIn/social** | Team growth, culture, announcements | Medium |
| **Press/funding** | Strategy, financial health | High |
| **Customer interviews** | Why they chose/rejected | High |
| **Trial/demo** | Actual product experience | High |

```markdown
## Intelligence Sources

| Competitor | Sources Used | Last Updated |
|------------|--------------|--------------|
| [Name] | [Source list] | [Date] |
```

### Step 4: Analyze Product Capabilities

Compare features and capabilities:

```markdown
## Feature Comparison

| Capability | Us | Competitor A | Competitor B | Competitor C |
|------------|----|--------------|--------------|--------------|
| [Feature 1] | [Status] | [Status] | [Status] | [Status] |
| [Feature 2] | [Status] | [Status] | [Status] | [Status] |

**Legend:** ✓ = Strong, ◐ = Partial, ✗ = Missing, ? = Unknown

### Capability Assessment

| Competitor | Strengths | Weaknesses | Differentiation |
|------------|-----------|------------|-----------------|
| [Name] | [List] | [List] | [Unique angle] |
```

### Step 5: Analyze Positioning

Understand how each competitor positions:

```markdown
## Positioning Analysis

### Competitor: [Name]

**Tagline:** "[Their tagline]"

**Target customer:** [Who they're for]

**Primary value prop:** [Main promise]

**Proof points:** [How they support claims]

**Emotional appeal:** [What feelings they evoke]

**Positioning statement:**
"For [target] who [need], [product] is [category] that [differentiation] unlike [alternative] because [reason to believe]."
```

### Step 6: Map Competitive Dynamics

Understand market forces:

```markdown
## Market Dynamics

### Market Trends
| Trend | Impact on Competition | Timeframe |
|-------|----------------------|-----------|
| [Trend 1] | [How it changes dynamics] | [When] |

### Competitive Moves (Recent)
| Competitor | Move | Our Response |
|------------|------|--------------|
| [Name] | [What they did] | [How we should respond] |

### Barriers to Entry
| Barrier | Strength | Who Benefits |
|---------|----------|--------------|
| [Barrier] | High/Med/Low | [Which competitors] |
```

### Step 7: Identify Strategic Opportunities

Find positioning and competitive advantages:

```markdown
## Strategic Opportunities

### Positioning Gaps
| Gap | Description | Opportunity |
|-----|-------------|-------------|
| [Gap 1] | [Unaddressed need] | [How we can own it] |

### Our Competitive Advantages
| Advantage | Sustainable? | Competitors Can Copy? |
|-----------|--------------|----------------------|
| [Advantage 1] | Yes/No | Yes/No/Hard |

### Threats to Monitor
| Threat | Likelihood | Impact | Early Warning |
|--------|------------|--------|---------------|
| [Threat 1] | High/Med/Low | High/Med/Low | [Signals to watch] |
```

### Step 8: Create Competitive Battlecard

Synthesize for sales/strategy use:

```markdown
## Battlecard: [Competitor Name]

### Quick Facts
- **Founded:** [Year]
- **HQ:** [Location]
- **Size:** [Employees, Funding, Revenue]
- **Target:** [Their customer profile]

### Their Pitch
"[How they describe themselves]"

### When Customers Choose Them
- [Scenario 1]
- [Scenario 2]

### When Customers Choose Us
- [Scenario 1]
- [Scenario 2]

### Their Weaknesses (With Proof)
| Weakness | Evidence | Our Counter |
|----------|----------|-------------|
| [Weakness 1] | "[Customer quote/review]" | "[What we say]" |

### Objection Handling
| Their Claim | Reality | Our Response |
|-------------|---------|--------------|
| "[Claim]" | [Truth] | "[Our counter]" |

### Questions to Ask Prospects
- "[Question that exposes their weakness]"
- "[Question that highlights our strength]"
```

## Examples

**Output: Complete Competitive Analysis**

```markdown
# Competitive Analysis: Project Management SaaS

## Competitive Context

**Market:** Project management software for tech teams (100-500 employees)
**Customer job:** Keep distributed teams aligned on priorities and progress
**Decision this informs:** Q3 product roadmap and positioning refresh
**Time horizon:** Current state + 1-year outlook

---

## Competitor Landscape

### Direct Competitors
| Competitor | Position | Est. ARR | Funding | Trend |
|------------|----------|----------|---------|-------|
| Asana | Enterprise-first PM | $600M+ | Public | Stable |
| Monday.com | Visual work OS | $700M+ | Public | Growing |
| Linear | Modern dev teams | $50M+ | $52M Series B | Fast growth |
| ClickUp | All-in-one | $150M+ | $537M | Growing |
| Notion | Flexible docs+PM | $500M+ | $275M | Fast growth |

### Indirect Competitors
| Competitor | Approach | Overlap |
|------------|----------|---------|
| Jira | Issue tracking | High with dev teams |
| GitHub Projects | Built into code | Medium with eng |
| Spreadsheets | Manual tracking | Low but persistent |
| Slack + docs | Communication-based | Medium for small teams |

### Potential Entrants
| Company | Why They Might Enter | Likelihood |
|---------|---------------------|------------|
| Figma | Already has FigJam, expanding | Medium |
| Miro | Whiteboard expanding to PM | Medium |
| GitHub | Native project management | High |

---

## Feature Comparison

| Capability | Us | Asana | Linear | ClickUp | Monday |
|------------|----|----|--------|---------|--------|
| Task management | ✓ | ✓ | ✓ | ✓ | ✓ |
| Agile/Sprint planning | ✓ | ◐ | ✓ | ✓ | ◐ |
| Roadmapping | ✓ | ◐ | ✓ | ◐ | ◐ |
| GitHub integration | ✓ | ◐ | ✓ | ◐ | ◐ |
| Real-time collaboration | ✓ | ◐ | ◐ | ◐ | ◐ |
| AI features | ✓ | ◐ | ✓ | ◐ | ✓ |
| Speed/performance | ✓ | ◐ | ✓ | ✗ | ◐ |
| Custom workflows | ◐ | ✓ | ✗ | ✓ | ✓ |
| Portfolio view | ◐ | ✓ | ◐ | ✓ | ✓ |
| Time tracking | ✗ | ◐ | ✗ | ✓ | ✓ |

**Legend:** ✓ = Strong, ◐ = Partial, ✗ = Missing

---

## Positioning Analysis

### Asana
**Tagline:** "Manage your team's work, projects, & tasks online"
**Target:** Enterprise cross-functional teams, PMOs
**Primary value prop:** Scalable work management for complex organizations
**Differentiation:** Enterprise features, mature integrations
**Weakness:** Slow, complex, engineering teams find it clunky

### Linear
**Tagline:** "The issue tracking tool you'll enjoy using"
**Target:** Product and engineering teams at startups/scale-ups
**Primary value prop:** Speed, craft, developer experience
**Differentiation:** Keyboard-first, beautifully fast, opinionated
**Weakness:** Limited customization, no time tracking, eng-only focus

### ClickUp
**Tagline:** "One app to replace them all"
**Target:** Teams wanting everything in one place
**Primary value prop:** Comprehensive features at low price
**Differentiation:** Feature breadth, aggressive pricing
**Weakness:** Overwhelming, slow, buggy, jack of all trades

### Monday.com
**Tagline:** "A Work OS that lets you shape workflows your way"
**Target:** Broad business teams (not dev-specific)
**Primary value prop:** Visual, flexible, easy to start
**Differentiation:** Visual boards, marketing strength
**Weakness:** Not dev-native, can get expensive, limited depth

---

## Customer Decision Patterns

### Why Customers Choose Linear Over Us
1. **Brand perception:** Seen as "cool" startup choice
2. **Speed:** Actually faster for simple workflows
3. **Opinionated:** Less decisions, just works their way

### Why Customers Choose Us Over Linear
1. **Flexibility:** Customization Linear doesn't allow
2. **Roadmapping:** Native strategic planning features
3. **Collaboration:** Better for cross-functional teams

### Why Customers Leave ClickUp
- "Too many features, impossible to find things" — G2 Review
- "Performance got worse as we grew" — Interview P4
- "We needed something that was actually fast" — Interview P7

---

## Market Dynamics

### Trends Reshaping Competition
| Trend | Impact | Timeframe |
|-------|--------|-----------|
| AI copilots | Everyone adding AI; will commoditize basic features | 6-12 months |
| Tool consolidation | Buyers want fewer tools; favors all-in-ones | Ongoing |
| Dev experience premium | Engineering teams demand speed, hate bloat | Ongoing |
| Remote/async | Async features more valued | Ongoing |

### Recent Competitive Moves
| Competitor | Move | Response |
|------------|------|----------|
| Linear | Launched "Projects" (roadmapping) | Accelerate our roadmap features |
| ClickUp | Cut prices 20% | Don't compete on price; emphasize quality |
| Monday | Added dev integrations | Monitor; not yet competitive |

---

## Strategic Opportunities

### Positioning Gaps
| Gap | Description | Opportunity |
|-----|-------------|-------------|
| "Linear for grown-ups" | Speed + enterprise features | Position as "Linear quality, enterprise ready" |
| Cross-functional | Linear is eng-only, Asana is clunky | Own "fast PM for product teams" |
| AI-native | Others adding AI as feature; we could be AI-first | Lead with AI roadmapping |

### Our Sustainable Advantages
| Advantage | Can Competitors Copy? |
|-----------|----------------------|
| Speed (architecture) | Hard — requires rebuild |
| Dev experience focus | Medium — cultural not just features |
| AI investment | Easy — temporary advantage |

### Threats
| Threat | Likelihood | Impact | Warning Signs |
|--------|------------|--------|---------------|
| Linear expands upmarket | High | High | Enterprise features, Sales team hires |
| GitHub native PM improves | Medium | High | GitHub Roadmap announcements |
| ClickUp fixes performance | Low | Medium | Engineering hiring, architecture posts |

---

## Battlecard: Linear

### Quick Facts
- **Founded:** 2019
- **HQ:** San Francisco (remote-first)
- **Size:** ~100 employees, $52M raised
- **Target:** Modern product/eng teams, startups to scale-ups

### Their Pitch
"The issue tracking tool you'll enjoy using. Streamline issues, sprints, and product roadmaps."

### When Customers Choose Linear
- Small eng team wanting speed and simplicity
- "Anti-Jira" sentiment strong
- Keyboard-power-users
- Don't need customization

### When Customers Choose Us
- Need roadmapping + issue tracking together
- Cross-functional team (not eng-only)
- Want flexibility without complexity
- Growing team needing to scale

### Their Weaknesses (With Evidence)
| Weakness | Evidence | Our Counter |
|----------|----------|-------------|
| Limited customization | "Can't change workflow to match our process" — G2 | "We're flexible without being overwhelming" |
| Eng-only focus | "PM team couldn't use it" — Interview | "Built for the whole product team" |
| No time tracking | Feature request #3 on their forum | "Native time tracking included" |

### Objection Handling
| Linear Claims | Reality | Our Response |
|--------------|---------|--------------|
| "We're faster" | Marginal in real use | "We're fast AND flexible" |
| "Less bloat" | Also less capability | "Focused features, not stripped down" |

### Questions to Ask Prospects
- "How much does your PM team use the tool, or is it eng-only?"
- "Do you need to customize workflows, or is one-size-fits-all okay?"
- "How do you handle roadmap planning — separate tool?"
```



## Quality Tests

### Evidence Test
- Every finding cites specific data, quotes, or observations
- **PASS:** Each insight traces back to a named source or data point
- **FAIL:** Findings use vague language like 'it seems' or 'generally' without evidence

### Completeness Test
- All relevant dimensions of the framework have been considered
- **PASS:** Analysis addresses each framework dimension, noting gaps where data is unavailable
- **FAIL:** Key dimensions skipped without acknowledgment

### Actionability Test
- Recommendations are specific enough to act on immediately
- **PASS:** Each recommendation names who should do what by when
- **FAIL:** Recommendations are vague ('improve communication') without concrete actions

## Guidelines

1. **Focus on insights, not data** — Analysis should drive decisions
2. **Triangulate sources** — No single source is complete
3. **Be specific** — "Good UI" is useless; "keyboard-first navigation" is useful
4. **Update regularly** — Markets move; stale analysis misleads
5. **Include proof** — Claims need evidence (quotes, data)
6. **Be honest about weaknesses** — Know where you lose, not just win

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Feature checklist only | Misses positioning, strategy | Analyze positioning and dynamics |
| Outdated analysis | Market changed | Set update cadence |
| Only direct competitors | Misses disruption | Include indirect and potential |
| Own-company bias | Can't see weaknesses | Interview lost deals |
| Information without action | Doesn't drive decisions | Every section should imply action |
| Public info only | Misses customer reality | Include customer interviews |

## References

- pattern-recognition: Finding patterns across competitors
- interview-synthesis: Extracting competitive insights from interviews
- forces-analysis: Understanding market forces
- mental-models: Strategic frameworks for analysis
