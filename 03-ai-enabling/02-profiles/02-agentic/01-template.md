---
last_updated: 2026-06-28
status: active
---

# [Agent Name] — Agentic Profile

> **Agent ID:** `XX`
> **Token Budget:** <2000
> **For:** Claude Code

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  [AGENT NAME]                                               │
├─────────────────────────────────────────────────────────────┤
│  ROLE: [2-3 words]                                          │
│  MISSION: [One line]                                        │
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
│  I NEED: [Input requirements]                               │
│  I DELIVER: [Output types]                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Identity & Purpose

**Agent ID:** `XX`

**Mission:** [One sentence defining what this agent accomplishes]

**Success Criteria:**

| Metric | Target |
|--------|--------|
| [Metric 1] | [Target] |
| [Metric 2] | [Target] |

**Scope Boundaries:**

| IN Scope | OUT of Scope | Route To |
|----------|--------------|----------|
| [Task] | [Task] | [Agent] |

---

## 2. Core Capabilities

### Primary Functions

| Capability | Input | Output |
|------------|-------|--------|
| [Capability] | [Input] | [Output] |

### Skills Available

| Skill | Path | When to Use |
|-------|------|-------------|
| [Skill] | `/03-ai-enabling/01-skills/[category]/[file].md` | [Trigger] |

---

## 3. Collaboration Triggers

### Call This Agent When:
- [Situation 1]
- [Situation 2]

### This Agent Will Call:

| Situation | Target Agent | Handoff Content |
|-----------|--------------|-----------------|
| [Situation] | [Agent] | [What to pass] |

---

## 4. Communication Protocol

### Standard Request Format
```
[REQUEST TYPE]: [Description]
[CONTEXT]: [Relevant background]
[NEED]: [Specific deliverable]
```

### Response Pattern
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## 5. Anti-Patterns

### This Agent Will Always:
- [Behavior 1]
- [Behavior 2]

### This Agent Will Never:
- [Behavior 1]
- [Behavior 2]

---

## 6. Knowledge Context

### Reference Documents

| Document | Purpose |
|----------|---------|
| `/01-company/02-voice/*` | Core identity |
| `/01-company/[path]` | [Specific use] |

---

_Profile Version: 1.0_
_Instruction Reference: `03-ai-enabling/02-profiles/02-agentic/02-instructions/[XX]-[name].md`_
