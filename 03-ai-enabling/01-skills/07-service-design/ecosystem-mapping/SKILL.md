---
last_updated: 2026-02-25
status: active
name: ecosystem-mapping
description: Map service ecosystems showing actors, relationships, value flows, and dependencies. Use when understanding complex multi-stakeholder environments, identifying partnership opportunities, or analyzing competitive landscapes.
triggers:
  keywords: ["ecosystem", "mapping", "service", "ecosystems", "showing", "actors", "relationships", "value", "flows", "dependencies"]
allowed-tools: Read, Write, Edit
---

# Ecosystem Mapping

## Overview

Visualize the complete network of actors, relationships, and value exchanges that enable or affect service delivery, revealing dependencies, opportunities, and risks.


## Define Done

- [ ] Service experience mapped from the customer's perspective
- [ ] Touchpoints across all channels identified and evaluated
- [ ] Pain points prioritized by impact and frequency
- [ ] Improvement opportunities linked to business outcomes

## Instructions

### Step 1: Identify Ecosystem Actors

Catalog all entities in the ecosystem:

| Actor Type | Examples | Questions |
|------------|----------|-----------|
| **Core** | Your organization, primary customers | Who delivers and receives core value? |
| **Direct** | Suppliers, partners, distributors | Who directly enables delivery? |
| **Indirect** | Regulators, industry bodies, media | Who influences but doesn't participate? |
| **Adjacent** | Complementors, substitutes, competitors | Who offers related value? |
| **Emerging** | Startups, new entrants, disruptors | Who might change the ecosystem? |

### Step 2: Map Relationships

Define connections between actors:

| Relationship Type | Symbol | Description |
|-------------------|--------|-------------|
| **Value exchange** | ↔ | Mutual benefit (money, data, service) |
| **Dependency** | → | One-way reliance |
| **Competition** | ⇄ | Competing for same resources |
| **Regulation** | ⊢ | Governance or compliance |
| **Information** | ⋯→ | Data or knowledge flow |

### Step 3: Analyze Value Flows

For each significant relationship, document:

| Element | Description |
|---------|-------------|
| **What flows** | Money, data, goods, services, influence |
| **Direction** | One-way, bidirectional, multi-directional |
| **Volume/Frequency** | Scale and cadence of exchange |
| **Criticality** | Impact if disrupted |

### Step 4: Identify Strategic Positions

Assess ecosystem dynamics:

| Position | Indicator | Strategic Implication |
|----------|-----------|----------------------|
| **Keystone** | Many dependencies on this actor | High influence, high responsibility |
| **Dominator** | Extracts disproportionate value | Risk of ecosystem damage |
| **Niche** | Specialized, limited connections | Protected but limited growth |
| **Hub** | Connects otherwise separate actors | Opportunity for platform play |

### Step 5: Surface Opportunities and Risks

Analyze the map for:

1. **Gaps** — Unserved needs or missing actors
2. **Bottlenecks** — Single points of failure
3. **Weak ties** — Relationships that could strengthen
4. **Threats** — Actors that could disintermediate you

## Examples

**Output format:**
```markdown
## Ecosystem Map: [Domain/Service]

### Actors
| Actor | Type | Role | Importance |
|-------|------|------|------------|
| [Name] | Core/Direct/Indirect/Adjacent | [Description] | High/Med/Low |

### Relationships
| From | To | Type | Value Flow | Criticality |
|------|-----|------|------------|-------------|
| [Actor A] | [Actor B] | Exchange/Dependency | [What flows] | High/Med/Low |

### Strategic Positions
| Actor | Position | Implication |
|-------|----------|-------------|
| [Name] | Keystone/Hub/Niche | [Strategic meaning] |

### Ecosystem Health
- **Diversity:** [Assessment of actor variety]
- **Resilience:** [Assessment of redundancy]
- **Productivity:** [Assessment of value creation]

### Opportunities
1. [Gap or opportunity with rationale]
2. [Second opportunity]

### Risks
1. [Threat or vulnerability with mitigation]
2. [Second risk]
```



## Quality Tests

### Customer Perspective Test
- Analysis reflects actual customer experience, not internal assumptions
- **PASS:** Insights are based on customer data, quotes, or observed behavior
- **FAIL:** Journey map reflects what we think customers experience, not reality

### Systemic Test
- Analysis considers the full service ecosystem, not just one touchpoint
- **PASS:** Cross-channel handoffs and backstage processes are included
- **FAIL:** Only the digital touchpoint analyzed, ignoring phone/in-person/email

## Guidelines

- Include at least 10 actors across different types
- Map both current and emerging actors
- Quantify value flows where possible
- Identify your organization's strategic position
- Surface at least 2 opportunities and 2 risks

## References

- Stakeholder mapping: `07-service-design/stakeholder-mapping/SKILL.md`
- Forces Framework: `01-company/06-methodologies/10-forces-framework.md`
- Systems thinking: `07-service-design/systems-thinking/SKILL.md`
