---
last_updated: 2026-04-02
status: active
---

# Necessary But Not Sufficient

Goldratt's core claim about technology, taken from the book of the same name: technology is a necessary condition for the value it promises, but it is never sufficient on its own. The missing ingredient is always a change in the rules.

This document adapts that framework for modern technology purchasing decisions, digital transformation programs, and software-as-a-service adoption.

---

## The Central Claim

When an organization buys technology, it typically expects the technology to deliver a specific outcome: faster processing, better decisions, reduced errors, higher throughput. The technology is purchased because it represents a new capability.

Goldratt's observation: the capability is real. The technology does what it says. But the outcome — the business result — requires more than the capability. It requires that the organization change how it operates in response to the new capability.

The formula:

```
Technology + Same Old Rules = Same Old Results (at higher cost)
Technology + New Rules = Desired Business Result
```

The "necessary but not sufficient" language is precise:
- **Necessary:** without the technology, the new rules cannot function
- **Not sufficient:** the technology alone, without new rules, cannot produce the result

---

## Why Organizations Resist Rule Changes

The natural response to a new technology is to map it onto existing processes. "We do it this way — the technology needs to fit into how we already work." This is rational from a short-term disruption standpoint. It is catastrophic from a value realization standpoint.

Several forces drive this resistance:

### 1. The Invisible Rule Problem
Most operational rules are invisible. They are embedded in job descriptions, approval chains, meeting rhythms, and cultural norms. Nobody questions them because they work. Nobody notices they exist because they've always been there. A rule invented to cope with a 1990s limitation may be operating unchanged in a modern organization.

### 2. The Disruption Fear
Changing rules means changing how people work. This creates uncertainty, training burden, resistance from people who are skilled at the current way, and risk of things going wrong during transition. The path of least resistance is to implement the technology without disrupting the rules.

### 3. The Measurement Problem
The benefits of rule changes are often diffuse and delayed. The costs of rule changes are immediate and visible. The technology budget was approved for the technology, not for the change management program that makes the technology work.

### 4. The Vendor Incentive Problem
Technology vendors are incentivized to make implementation easy. Easy implementation means minimal process disruption. Minimal process disruption means minimal rule change. Maximum ease of adoption produces minimum value realization. The vendor wins. The customer doesn't.

---

## The Three Scenarios

### Scenario A: Technology + No Rule Change

The technology is implemented. The old rules continue. The organization now has:
- All the costs of the technology (license, implementation, training, maintenance)
- None of the capability benefits (because the rules don't use the new capability)
- Additional complexity (two systems in parallel, workarounds, confusion)

This is the most common scenario. It is so common that "technology ROI disappointment" has become an accepted industry norm rather than a diagnostic signal.

### Scenario B: Technology + Partial Rule Change

Some rules are changed; most are not. The organization captures part of the value but leaves the majority unrealized. Over time, the unchanged rules reassert dominance because they are:
- Familiar to longer-tenured employees
- Embedded in systems and processes the technology wasn't designed to replace
- Defended by stakeholders who benefit from the current arrangement

This is the second most common scenario. It produces "we got some value but less than expected" outcomes.

### Scenario C: Technology + Complete Rule Change

All rules that existed because of the old limitation are replaced with rules designed for the new capability. The technology delivers the outcome it promised. This scenario requires:
- Explicit identification of all rules created by the old limitation
- Deliberate design of replacement rules
- Formal adoption and enforcement of new rules
- Explicit retirement of old rules

This is the least common scenario. It is also the only one that reliably produces the advertised ROI.

---

## Application to Modern Technology Contexts

### SaaS Software Adoption

SaaS vendors design their products to be adopted quickly. Quick adoption means the software fits into existing workflows. Existing workflows contain old rules. The result: SaaS tools are adopted at low implementation cost and low value realization.

The four-question discipline is especially important for SaaS because the implementation vendor (or internal IT team) has no incentive to challenge your processes.

Ask before any SaaS purchase: "What would we have to change about how we work for this software to be more than a prettier interface for our current process?"

### Digital Transformation Programs

Large-scale digital transformation programs typically fail because they treat "digital" as a synonym for "automated current process." The ERP system automates the manual order tracking process. The CRM automates the manual sales reporting process. The HRIS automates the manual HR tracking process.

Automation of a process designed for a pre-digital world produces a digital process that is still designed for a pre-digital world. It's faster. It's still wrong.

True digital transformation means using Q3 and Q4: identifying the rules that exist because the old analog process required them, and replacing those rules with ones designed for the digital capability.

### Build vs. Buy Decisions

The build-vs-buy decision is often framed as: "Do we buy a vendor's solution or build our own?" The Necessary But Not Sufficient framework reveals a third option: "Are we solving the right problem?"

Building a custom tool because the vendor's product doesn't fit your workflow often means you're encoding your current (rule-laden) workflow into software. You've built a more expensive version of your current constraint.

Before building: run the four questions. If Q2 (the limitation being diminished) is not the binding constraint, building the perfect solution for it is exactly as useless as buying the perfect solution for it.

### AI and Automation Tools

AI tools follow the same pattern with heightened risk. The power of an AI tool (Q1) is often genuine and significant. The limitation it diminishes (Q2) is often real. But the rules that governed work before the AI tool was available (Q3) are often deeply embedded in organizational culture, legal frameworks, compliance requirements, and individual job definitions.

An AI tool that speeds up an analyst's research by 10x does not deliver value if the organization's approval process still requires the same review cycles the 10x speedup was supposed to eliminate. The rule — "all research must go through the 3-stage review process" — exists because research used to take a week. It takes an hour now. The rule hasn't changed.

---

## Diagnosing an Underperforming Technology Investment

When a technology investment has not delivered expected value, run this diagnosis:

1. **Can you clearly state Q1?** If not, the investment rationale was unclear from the start. Clarify the power statement and reassess.

2. **Is the limitation in Q2 actually your binding constraint?** If the technology addresses a non-binding limitation, value realization will be low regardless of rule changes. Identify the actual binding constraint and reassess whether the technology addresses it.

3. **Have Q3 rules been identified?** If not, conduct the archaeology now. Interview people who have been in the organization longest. Ask "why do we do this?" until you find rules whose root cause is the old limitation.

4. **Are Q3 rules still active?** If yes, this is where your unrealized value lives. Design Q4 replacements and implement them.

5. **Are Q4 rules being followed in practice?** It's possible Q4 rules were designed but never enforced. Observe whether people are actually operating under the new rules or reverting to old ones.

The most recoverable situation: Q3 rules identified, Q4 rules designed, not yet enforced. The value is still there — it requires change management, not additional technology.

---

## The Portfolio View

Across a portfolio of technology investments, the correlation between rule-change completeness and value realization should be strong and positive. If it is not:

- The binding constraint may not be the one the investments address
- Rule changes may have been designed but not enforced
- The organization may have structural barriers to rule change (political, regulatory, cultural) that override technical capability

Use `rule_change_audit.py` to surface this pattern across your investment portfolio.
