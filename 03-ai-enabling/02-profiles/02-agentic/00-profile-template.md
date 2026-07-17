---
last_updated: 2026-06-28
status: active
---

# Project Collaboration Profile: [AGENT_NAME]

> **Template Version:** 1.1
> **Purpose:** Agent-to-agent collaboration interface (1 of 3 files per agent)
> **Audience:** Other Claude agents needing to understand this agent's capabilities
> **Architecture Guide:** `03-ai-enabling/02-profiles/00-overview.md`

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  [AGENT_NAME]                                               │
├─────────────────────────────────────────────────────────────┤
│  ROLE: [2-3 word role description]                          │
│  MISSION: [One line mission]                                │
├─────────────────────────────────────────────────────────────┤
│  CALL ME FOR:                                               │
│  • [Trigger 1]                                              │
│  • [Trigger 2]                                              │
│  • [Trigger 3]                                              │
├─────────────────────────────────────────────────────────────┤
│  DON'T CALL ME FOR:                                         │
│  • [Anti-pattern 1] → [Correct Agent]                       │
│  • [Anti-pattern 2] → [Correct Agent]                       │
├─────────────────────────────────────────────────────────────┤
│  I NEED: [Key inputs in 5-10 words]                         │
│  I DELIVER: [Key outputs in 5-10 words]                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Identity & Purpose

**Agent ID:** `[XX-agent-name]`

**Mission:** [One sentence describing core purpose]

**Success Criteria:**
| Metric | Target |
|--------|--------|
| [Outcome 1] | [Measurable target] |
| [Outcome 2] | [Measurable target] |
| [Outcome 3] | [Measurable target] |

**Scope Boundaries:**

| IN Scope | OUT of Scope | Route To |
|----------|--------------|----------|
| [Task 1] | [Task A] | [Agent] |
| [Task 2] | [Task B] | [Agent] |
| [Task 3] | [Task C] | [Agent] |

---

## 2. Core Capabilities

### Primary Functions
| Capability | Input | Output |
|------------|-------|--------|
| [What I can do 1] | [What I need] | [What I produce] |
| [What I can do 2] | [What I need] | [What I produce] |
| [What I can do 3] | [What I need] | [What I produce] |

### Unique Capabilities (Only This Agent)
- [Capability no other agent has]
- [Capability no other agent has]

---

## 3. Integration Interfaces

### What I Provide

| Output | Description | Receiving Agent(s) | Format |
|--------|-------------|-------------------|--------|
| [Output 1] | [Description] | [Agent(s)] | [Format] |
| [Output 2] | [Description] | [Agent(s)] | [Format] |

### What I Need

| Input | Description | Source Agent | Request Method |
|-------|-------------|--------------|----------------|
| [Input 1] | [Description] | [Agent] | [How to request] |
| [Input 2] | [Description] | [Agent] | [How to request] |

---

## 4. Collaboration Triggers

### Call This Agent When:
- [Situation/signal 1]
- [Situation/signal 2]
- [Situation/signal 3]
- [Situation/signal 4]

### This Agent Will Call:
| Situation | Target Agent | Handoff Content |
|-----------|--------------|-----------------|
| [When X happens] | [Agent] | [What I pass along] |
| [When Y happens] | [Agent] | [What I pass along] |

---

## 5. Communication Protocol

### Standard Request Format
```
CONTEXT: [Background situation]
REQUEST: [Specific ask]
CONSTRAINTS: [Limitations, timeline]
SUCCESS: [What good output looks like]
```

### Expected Response Pattern
1. [Step 1 of how agent responds]
2. [Step 2]
3. [Step 3]

### Handoff Protocol
| Direction | Trigger | Deliverable |
|-----------|---------|-------------|
| Receiving | [When I get work] | [What I need to start] |
| Sending | [When I hand off] | [What I provide] |

---

## 6. Anti-Patterns

### Don't Ask This Agent To:

| Request | Why Not | Correct Agent |
|---------|---------|---------------|
| [Bad request 1] | [Reason] | [Right agent] |
| [Bad request 2] | [Reason] | [Right agent] |
| [Bad request 3] | [Reason] | [Right agent] |

### This Agent Will Always:
- [Guaranteed behavior 1]
- [Guaranteed behavior 2]
- [Guaranteed behavior 3]

### This Agent Will Never:
- [Guaranteed non-behavior 1]
- [Guaranteed non-behavior 2]

---

## 7. Knowledge Context

### Key Documents
| Document | Purpose |
|----------|---------|
| `[path]` | [Why this agent uses it] |
| `[path]` | [Why this agent uses it] |

### Shared Vocabulary
| Term | Definition | Usage Context |
|------|------------|---------------|
| [Term 1] | [Definition] | [When used] |
| [Term 2] | [Definition] | [When used] |

---

## 8. Current State

**Active Priorities:**
1. [Current focus 1]
2. [Current focus 2]

**Known Limitations:**
- [Limitation 1]
- [Limitation 2]

**Dependencies:**
| Dependency | Risk if Unavailable | Mitigation |
|------------|---------------------|------------|
| [Dependency 1] | [Impact] | [Workaround] |
| [Dependency 2] | [Impact] | [Workaround] |

---

_Profile Version: 1.0_
_Last Updated: [DATE]_

**Related Files (Three-File System):**
- **This file:** Profile — Who the agent IS
- **Instructions:** `03-ai-enabling/02-profiles/02-agentic/02-instructions/[XX-agent].md` — How the agent BEHAVES
- **Command:** `03-ai-enabling/02-profiles/02-agentic/02-commands/[XX-agent-id].md` — How to INVOKE the agent
