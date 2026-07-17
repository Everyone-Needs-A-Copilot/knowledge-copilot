---
last_updated: 2026-02-25
status: active
name: threat-modeling
description: Identify and analyze security threats using STRIDE, attack trees, and data flow diagrams. Prioritize threats by risk and define mitigations. Use when designing new systems or reviewing existing architecture for security.
triggers:
  files: ["**/security/**", "**/threat-model/**", "**/docs/security*.md", "**/architecture/**"]
  keywords: ["threat model", "STRIDE", "attack tree", "security review", "threat analysis", "data flow diagram", "trust boundary", "attack surface", "mitigation", "risk assessment"]
allowed-tools: Read, Write, Edit
---

# Threat Modeling

## Overview

Threat modeling is the practice of systematically identifying potential security threats to a system and determining appropriate mitigations. It shifts security left—addressing vulnerabilities in design rather than after deployment.

Effective threat modeling answers four questions:
1. **What are we building?** (System model)
2. **What can go wrong?** (Threat identification)
3. **What are we going to do about it?** (Mitigations)
4. **Did we do a good job?** (Validation)


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Instructions

### Step 1: Model the System

Create a Data Flow Diagram (DFD) showing:

| Element | Symbol | Description |
|---------|--------|-------------|
| **Process** | Circle/Rectangle | Code that transforms data |
| **Data Store** | Parallel lines | Where data is stored |
| **External Entity** | Rectangle | Outside the system boundary |
| **Data Flow** | Arrow | Data movement between elements |
| **Trust Boundary** | Dashed line | Where trust levels change |

```
┌─────────────────────────────────────────────────────────────┐
│                        Trust Boundary                        │
│  ┌──────────┐      ┌──────────┐      ┌───────────────────┐  │
│  │  User    │─────►│  Web     │─────►│   Application     │  │
│  │ (Entity) │      │  Server  │      │   Server          │  │
│  └──────────┘      └──────────┘      └─────────┬─────────┘  │
│                                                 │            │
│                                                 ▼            │
│                                          ╔═══════════╗      │
│                                          ║ Database  ║      │
│                                          ╚═══════════╝      │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Identify Threats with STRIDE

Apply STRIDE to each element crossing a trust boundary:

| Threat | Description | Applies To | Example |
|--------|-------------|------------|---------|
| **S**poofing | Pretending to be someone else | External entities, Processes | Forged authentication |
| **T**ampering | Modifying data or code | Data flows, Data stores | SQL injection |
| **R**epudiation | Denying actions took place | Processes | Missing audit logs |
| **I**nformation Disclosure | Exposing data to unauthorized parties | Data flows, Data stores | Sensitive data in logs |
| **D**enial of Service | Making system unavailable | Processes, Data stores | Resource exhaustion |
| **E**levation of Privilege | Gaining unauthorized access | Processes | Bypassing authorization |

### Step 3: Prioritize Threats

Use DREAD scoring (1-10 scale):

| Factor | Question |
|--------|----------|
| **D**amage | How bad is the impact? |
| **R**eproducibility | How easy to reproduce? |
| **E**xploitability | How easy to exploit? |
| **A**ffected Users | How many users impacted? |
| **D**iscoverability | How easy to discover? |

**Risk Score** = (D + R + E + A + D) / 5

| Score | Priority |
|-------|----------|
| 9-10 | Critical |
| 7-8 | High |
| 4-6 | Medium |
| 1-3 | Low |

### Step 4: Define Mitigations

For each significant threat:

| STRIDE Category | Common Mitigations |
|-----------------|-------------------|
| Spoofing | Authentication (MFA, strong passwords) |
| Tampering | Input validation, digital signatures, hashing |
| Repudiation | Audit logging, digital signatures |
| Info Disclosure | Encryption (at rest, in transit), access controls |
| DoS | Rate limiting, resource quotas, redundancy |
| EoP | Authorization checks, principle of least privilege |

### Step 5: Validate and Document

Create a threat model document including:
- System diagram
- Trust boundaries
- Threat list with DREAD scores
- Mitigations for each threat
- Residual risks accepted

## STRIDE Deep Dive

### Spoofing Identity

**Definition**: Pretending to be another user or system.

**Attack Examples**:
- Credential stuffing
- Session hijacking
- Certificate spoofing
- IP spoofing

**Mitigations**:

| Control | Implementation |
|---------|----------------|
| Strong authentication | MFA, passwordless auth |
| Session management | Secure cookies, short expiry |
| Mutual TLS | Certificate-based auth for services |
| Token validation | JWT signature verification |

### Tampering with Data

**Definition**: Modifying data maliciously.

**Attack Examples**:
- SQL/NoSQL injection
- Parameter manipulation
- Man-in-the-middle attacks
- Database tampering

**Mitigations**:

| Control | Implementation |
|---------|----------------|
| Input validation | Whitelist validation, parameterized queries |
| Integrity checks | Digital signatures, checksums |
| Encryption in transit | TLS 1.3 |
| Immutable audit log | Append-only, cryptographically signed |

### Repudiation

**Definition**: Denying that an action occurred.

**Attack Examples**:
- Denying fraudulent transactions
- Claiming account was compromised
- Modifying logs to hide activity

**Mitigations**:

| Control | Implementation |
|---------|----------------|
| Comprehensive logging | Log all security-relevant events |
| Tamper-evident logs | Centralized, append-only logging |
| Digital signatures | Sign transactions, messages |
| Non-repudiation | Cryptographic proof of origin |

### Information Disclosure

**Definition**: Exposing data to unauthorized parties.

**Attack Examples**:
- Data breach
- Side-channel attacks
- Verbose error messages
- Sensitive data in URLs

**Mitigations**:

| Control | Implementation |
|---------|----------------|
| Encryption at rest | AES-256, database encryption |
| Encryption in transit | TLS 1.3 everywhere |
| Access controls | RBAC, data classification |
| Data minimization | Don't collect/store unnecessary data |

### Denial of Service

**Definition**: Making system unavailable.

**Attack Examples**:
- Volumetric DDoS
- Application-layer attacks
- Resource exhaustion
- Algorithmic complexity attacks

**Mitigations**:

| Control | Implementation |
|---------|----------------|
| Rate limiting | Per-user, per-IP limits |
| DDoS protection | CDN, cloud-based protection |
| Resource quotas | Memory, CPU, connection limits |
| Graceful degradation | Shed load, prioritize critical functions |

### Elevation of Privilege

**Definition**: Gaining access beyond authorized level.

**Attack Examples**:
- Privilege escalation exploits
- Insecure direct object references
- JWT manipulation
- Role assignment bugs

**Mitigations**:

| Control | Implementation |
|---------|----------------|
| Least privilege | Minimal permissions by default |
| Authorization checks | Check at every access point |
| Role separation | Admin ≠ User ≠ Guest |
| Secure defaults | Deny by default |

## Attack Trees

Attack trees model how an attacker achieves a goal.

```
                    [Steal User Data]
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    [Compromise DB]  [Intercept API]  [Social Engineer]
           │               │               │
      ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
      │         │     │         │     │         │
   [SQLi]  [Weak    [MITM]   [API   [Phish] [Pretexting]
           Creds]          Key Leak]
```

**Building attack trees**:
1. Define attacker goal (root)
2. Identify sub-goals (OR nodes: any path works)
3. Identify requirements (AND nodes: all required)
4. Assign difficulty/cost to leaf nodes
5. Calculate path difficulty

## Threat Model Template

```markdown
# Threat Model: [System Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Author:** [Name]
**Reviewers:** [Names]

## 1. System Overview

[Brief description of the system and its purpose]

## 2. Data Flow Diagram

[Include DFD with trust boundaries]

## 3. Assets

| Asset | Classification | Owner |
|-------|---------------|-------|
| [Asset 1] | [Confidential/Internal/Public] | [Team] |

## 4. Trust Boundaries

| Boundary | From | To | Controls |
|----------|------|----|----------|
| [Name] | [Zone] | [Zone] | [Auth, encryption, etc.] |

## 5. Threats

### T-001: [Threat Name]

**STRIDE Category:** [S/T/R/I/D/E]

**Description:** [What could happen]

**Attack Vector:** [How attacker would exploit]

**DREAD Score:**
- Damage: X
- Reproducibility: X
- Exploitability: X
- Affected Users: X
- Discoverability: X
- **Total: X.X**

**Mitigation:** [Control to implement]

**Status:** [Open/Mitigated/Accepted]

### T-002: [Next threat...]

## 6. Risk Summary

| Risk Level | Count | Examples |
|------------|-------|----------|
| Critical | X | T-001 |
| High | X | T-003, T-005 |
| Medium | X | T-002 |
| Low | X | T-004 |

## 7. Accepted Risks

| Threat | Justification | Review Date |
|--------|---------------|-------------|
| [ID] | [Why accepting] | [Date] |

## 8. Action Items

| Item | Owner | Due Date | Status |
|------|-------|----------|--------|
| [Action] | [Name] | [Date] | [Status] |
```

## Examples

### Example 1: Web Application Threat Model

```markdown
# Threat Model: E-Commerce Checkout

## System Overview

Payment processing flow: User → Web App → Payment Gateway → Bank

## Data Flow Diagram

┌──────────────────────────────────────────────────────────────┐
│                     Internet (Untrusted)                     │
│  ┌────────┐                                                  │
│  │ User   │──HTTPS──┐                                       │
│  │Browser │         │                                       │
│  └────────┘         │                                       │
└─────────────────────┼────────────────────────────────────────┘
                      │ Trust Boundary
┌─────────────────────┼────────────────────────────────────────┐
│                     ▼           Internal Network             │
│              ┌───────────┐                                   │
│              │ Web App   │──────┐                           │
│              └───────────┘      │                           │
│                                 ▼                           │
│                          ╔═══════════╗                      │
│                          ║ Database  ║                      │
│                          ╚═══════════╝                      │
└─────────────────────────────────────────────────────────────┘
                      │ Trust Boundary
┌─────────────────────┼────────────────────────────────────────┐
│                     ▼           Payment Network              │
│              ┌───────────┐                                   │
│              │ Payment   │                                   │
│              │ Gateway   │                                   │
│              └───────────┘                                   │
└─────────────────────────────────────────────────────────────┘

## Threats

### T-001: Credit Card Data Theft (Information Disclosure)

**DREAD:** D:10, R:7, E:5, A:9, D:6 = **7.4 (High)**

**Attack Vector:** SQLi to extract stored card numbers

**Mitigation:**
- Don't store full card numbers (tokenization)
- Parameterized queries
- PCI DSS compliance

### T-002: Session Hijacking (Spoofing)

**DREAD:** D:8, R:6, E:5, A:7, D:5 = **6.2 (Medium)**

**Attack Vector:** Steal session cookie via XSS

**Mitigation:**
- HttpOnly, Secure cookie flags
- Content Security Policy
- Session binding to IP/device
```



## Quality Tests

### Trade-Off Test
- Alternatives were considered before choosing this architecture
- **PASS:** At least 2 alternative approaches evaluated with pros/cons
- **FAIL:** Architecture chosen without considering alternatives

### Scalability Test
- Architecture handles 10x current load without redesign
- **PASS:** Bottlenecks identified with specific scaling strategies
- **FAIL:** No analysis of how the system behaves under increased load

## Guidelines

### When to Threat Model

| Trigger | Action |
|---------|--------|
| New system design | Full threat model |
| Major architecture change | Update threat model |
| New integration | Focused threat analysis |
| Security incident | Retrospective analysis |
| Regular cadence | Annual review |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too abstract | Model actual implementation |
| Incomplete boundaries | Map all trust transitions |
| Generic threats | Be specific to your system |
| No prioritization | Use DREAD or similar |
| Documentation only | Threat model is input to action |

### Integration with Development

1. **Design phase**: Initial threat model
2. **Development**: Security requirements from threat model
3. **Code review**: Check mitigations implemented
4. **Testing**: Security tests based on threats
5. **Production**: Monitor for threat indicators

## References

- STRIDE (Microsoft)
- OWASP Threat Modeling
- Attack Trees (Bruce Schneier)
- PASTA: Process for Attack Simulation and Threat Analysis
- NIST Cybersecurity Framework
