---
last_updated: 2026-02-25
status: active
name: threat-modeling
description: STRIDE, PASTA, attack trees, threat identification and risk assessment. Use when designing security architecture or assessing system threats.
triggers:
  files: ["**/security/**", "**/auth/**", "**/design/**", "**/*.threat", "**/architecture/**"]
  keywords: ["threat model", "STRIDE", "PASTA", "attack tree", "attack surface", "threat actor", "risk assessment", "security design", "trust boundary", "data flow diagram", "DFD", "adversary", "mitigation"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Threat Modeling Deep Expertise

This skill provides comprehensive guidance on identifying, analyzing, and mitigating security threats in software systems. Apply this knowledge when designing new systems, reviewing existing architectures, or conducting security assessments.

## Core Threat Modeling Methodologies

### STRIDE Model

Microsoft's STRIDE categorizes threats by violation type:

| Threat | Violation | Example |
|--------|-----------|---------|
| **S**poofing | Authentication | Impersonating another user |
| **T**ampering | Integrity | Modifying data in transit |
| **R**epudiation | Non-repudiation | Denying actions performed |
| **I**nformation Disclosure | Confidentiality | Data leaks, error messages |
| **D**enial of Service | Availability | Resource exhaustion |
| **E**levation of Privilege | Authorization | Gaining admin access |

**STRIDE Analysis Process:**

```
1. Decompose system into components
2. Identify data flows between components
3. For each data flow, ask:
   - Can identity be spoofed?
   - Can data be tampered?
   - Can actions be denied?
   - Can data be disclosed?
   - Can service be denied?
   - Can privileges be elevated?
4. Document and prioritize threats
5. Define mitigations for each threat
```

### PASTA (Process for Attack Simulation and Threat Analysis)

Seven-stage risk-centric methodology:

| Stage | Activity | Deliverable |
|-------|----------|-------------|
| 1 | Define Objectives | Business impact analysis |
| 2 | Define Technical Scope | System architecture diagram |
| 3 | Application Decomposition | Data flow diagrams |
| 4 | Threat Analysis | Threat intelligence report |
| 5 | Vulnerability Analysis | Vulnerability mapping |
| 6 | Attack Modeling | Attack trees |
| 7 | Risk Analysis | Risk-ranked threat list |

### Attack Trees

Hierarchical decomposition of attack goals:

```
[Root Goal: Gain Admin Access]
├── [OR] Steal Credentials
│   ├── [AND] Phishing Attack
│   │   ├── Create fake login page
│   │   └── Social engineer user
│   └── [AND] Brute Force
│       ├── Enumerate usernames
│       └── Password spray attack
├── [OR] Exploit Vulnerability
│   ├── SQL Injection in login
│   └── Authentication bypass
└── [OR] Session Hijacking
    ├── XSS to steal cookie
    └── Network sniffing (HTTP)
```

**Attack Tree Node Types:**
- **OR nodes**: Any child path achieves goal
- **AND nodes**: All children required
- **Leaf nodes**: Atomic attack steps


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Data Flow Diagram (DFD) Components

### DFD Elements

| Symbol | Element | Description |
|--------|---------|-------------|
| ○ | Process | Code that transforms data |
| ═ | Data Store | Database, file, cache |
| □ | External Entity | User, external system |
| → | Data Flow | Data movement |
| --- | Trust Boundary | Security perimeter |

### DFD Security Analysis

```
External User ──[HTTPS]──→ [Web Server] ──[SQL]──→ ═Database═
                              │
                    ....Trust Boundary....
                              │
                              ↓
                         [Auth Service]
```

**Questions per element:**
- **Data Flows**: Encrypted? Authenticated? Validated?
- **Trust Boundaries**: How are boundaries enforced?
- **Processes**: What privileges? Input validation?
- **Data Stores**: Encrypted at rest? Access controls?
- **External Entities**: Authenticated? Authorized?

## Threat Identification Process

### 1. Asset Inventory

```python
class Asset:
    """Security asset for threat modeling"""
    def __init__(self, name: str, type: str, value: str):
        self.name = name
        self.type = type  # data, service, infrastructure
        self.value = value  # low, medium, high, critical
        self.threats = []
        self.controls = []

# Example asset inventory
assets = [
    Asset("User Credentials", "data", "critical"),
    Asset("Payment Info", "data", "critical"),
    Asset("API Gateway", "service", "high"),
    Asset("Database Server", "infrastructure", "critical"),
]
```

### 2. Threat Actor Profiling

| Actor Type | Motivation | Capability | Examples |
|------------|------------|------------|----------|
| Script Kiddie | Fame, curiosity | Low | Automated tools |
| Hacktivist | Ideological | Medium | Website defacement |
| Criminal | Financial | High | Ransomware, fraud |
| Nation State | Espionage | Very High | APT, zero-days |
| Insider | Various | Variable | Data theft |

### 3. Attack Surface Analysis

```python
def analyze_attack_surface(system):
    """Identify all entry points and exposure"""
    attack_surface = {
        "network": [],    # Open ports, services
        "web": [],        # HTTP endpoints, forms
        "api": [],        # API endpoints, methods
        "physical": [],   # Physical access points
        "social": [],     # People, processes
    }

    # Network surface
    for service in system.exposed_services:
        attack_surface["network"].append({
            "service": service.name,
            "port": service.port,
            "protocol": service.protocol,
            "authentication": service.requires_auth,
        })

    # Web surface
    for endpoint in system.web_endpoints:
        attack_surface["web"].append({
            "path": endpoint.path,
            "methods": endpoint.methods,
            "inputs": endpoint.user_inputs,
            "auth_required": endpoint.requires_auth,
        })

    return attack_surface
```

### 4. Risk Assessment Matrix

| Likelihood | Impact → | Low | Medium | High | Critical |
|------------|----------|-----|--------|------|----------|
| High | | Medium | High | Critical | Critical |
| Medium | | Low | Medium | High | Critical |
| Low | | Low | Low | Medium | High |
| Very Low | | Negligible | Low | Low | Medium |

## Threat Modeling Templates

### STRIDE Threat Card

```markdown
## Threat: [Threat Name]

**Category:** [S/T/R/I/D/E]
**Component:** [Affected system component]
**Description:** [How the attack works]

### Attack Scenario
1. Attacker does X
2. System responds with Y
3. Attacker exploits Z

### Prerequisites
- [What attacker needs]

### Impact
- Confidentiality: [High/Medium/Low/None]
- Integrity: [High/Medium/Low/None]
- Availability: [High/Medium/Low/None]

### Likelihood: [High/Medium/Low]
### Risk Rating: [Critical/High/Medium/Low]

### Mitigations
1. [Mitigation 1]
2. [Mitigation 2]

### Detection
- [How to detect this attack]
```

### Threat Model Document Structure

```markdown
# Threat Model: [System Name]

## 1. Executive Summary
- System purpose
- Key findings
- Critical risks

## 2. Scope
- In-scope components
- Out-of-scope components
- Assumptions

## 3. System Description
- Architecture overview
- Data flow diagrams
- Trust boundaries

## 4. Threat Actors
- Relevant adversaries
- Capabilities and motivations

## 5. Assets
- Data assets and classification
- Service assets
- Infrastructure assets

## 6. Threats
### 6.1 STRIDE Analysis
[Threat cards for each identified threat]

## 7. Risk Assessment
- Risk matrix
- Prioritized threat list

## 8. Mitigations
- Recommended controls
- Implementation priority
- Residual risk

## 9. Appendices
- Detailed DFDs
- Attack trees
- References
```

## Common Threat Patterns

### Authentication Threats

| Threat | STRIDE | Mitigation |
|--------|--------|------------|
| Credential stuffing | Spoofing | Rate limiting, MFA |
| Session hijacking | Spoofing | Secure cookies, TLS |
| Password spraying | Spoofing | Account lockout, MFA |
| Credential exposure | Info Disclosure | Encryption, secure storage |

### API Threats

| Threat | STRIDE | Mitigation |
|--------|--------|------------|
| Broken object auth | EoP | Object-level access checks |
| Excessive data exposure | Info Disclosure | Response filtering |
| Lack of rate limiting | DoS | Rate limiting, quotas |
| Injection attacks | Tampering | Input validation, parameterized queries |

### Data Storage Threats

| Threat | STRIDE | Mitigation |
|--------|--------|------------|
| SQL injection | Tampering | Parameterized queries |
| Data exfiltration | Info Disclosure | Encryption, DLP |
| Backup theft | Info Disclosure | Encrypted backups |
| Audit log tampering | Repudiation | Log integrity, SIEM |

## Automated Threat Modeling

### Integration with SDLC

```yaml
# CI/CD Threat Analysis Pipeline
stages:
  - threat-analysis:
      tools:
        - microsoft-threat-modeling-tool
        - OWASP-threat-dragon
      triggers:
        - architecture-changes
        - new-endpoints
      gates:
        - no-unmitigated-critical-threats
        - all-threats-documented
```

### Threat Modeling as Code

```python
from threatspec import ThreatModel, Component, DataFlow

# Define system components
auth_service = Component("Authentication Service", type="process")
user_db = Component("User Database", type="datastore")
web_app = Component("Web Application", type="process")

# Define data flows
login_flow = DataFlow(
    source=web_app,
    destination=auth_service,
    data="credentials",
    protocol="HTTPS"
)

# Build threat model
model = ThreatModel("My Application")
model.add_components([auth_service, user_db, web_app])
model.add_flows([login_flow])

# Analyze with STRIDE
threats = model.analyze_stride()
for threat in threats:
    print(f"{threat.category}: {threat.description}")
    print(f"  Risk: {threat.risk}")
    print(f"  Mitigations: {threat.suggested_mitigations}")
```

## Anti-Patterns (Avoid These)

### Incomplete Scope

```
BAD: "We only model the web application"
GOOD: "We model web app, APIs, databases, third-party integrations,
       and the network infrastructure connecting them"
```

### Ignoring Trust Boundaries

```
BAD: Treating internal network as inherently trusted
GOOD: Zero-trust model - verify at every boundary
```

### One-Time Exercise

```
BAD: Threat model created once, never updated
GOOD: Living document updated with each significant change
```

### Generic Threats Only

```
BAD: "SQL injection is a threat"
GOOD: "SQL injection in the /api/users endpoint allows
       data exfiltration of all user records"
```

## Validation Checklist

When reviewing a threat model:

- [ ] All system components documented
- [ ] Trust boundaries clearly identified
- [ ] Data flows mapped completely
- [ ] STRIDE analysis for each component/flow
- [ ] Threat actors identified and profiled
- [ ] Assets valued and prioritized
- [ ] Risk ratings justified
- [ ] Mitigations specific and actionable
- [ ] Residual risk documented
- [ ] Model updated for recent changes

## Integration with Security Controls

### Mapping Threats to Controls

| Threat Category | Control Types |
|-----------------|---------------|
| Spoofing | Authentication, MFA, certificates |
| Tampering | Integrity checks, signing, validation |
| Repudiation | Logging, audit trails, non-repudiation |
| Info Disclosure | Encryption, access control, masking |
| Denial of Service | Rate limiting, redundancy, scaling |
| Elevation of Privilege | RBAC, least privilege, sandboxing |

## Summary

Effective threat modeling requires:

1. **Systematic approach**: Use proven methodologies (STRIDE, PASTA)
2. **Complete coverage**: Document all components and data flows
3. **Risk prioritization**: Focus on high-impact, high-likelihood threats
4. **Actionable mitigations**: Specific controls for each threat
5. **Continuous updates**: Evolve with system changes
6. **Team involvement**: Include developers, architects, security


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

