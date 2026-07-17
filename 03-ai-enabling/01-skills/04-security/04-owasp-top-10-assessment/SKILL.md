---
last_updated: 2026-02-25
status: active
name: owasp-top-10-assessment
description: Systematic assessment against OWASP Top 10 vulnerabilities. Use when auditing applications for common security risks.
triggers:
  files: ["**/security/**", "**/audit/**", "**/pentest/**", "**/compliance/**"]
  keywords: ["OWASP", "security audit", "vulnerability assessment", "penetration test", "security review", "compliance", "A01", "A02", "A03", "broken access", "injection", "cryptographic"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# OWASP Top 10 Assessment

Systematic methodology for assessing applications against the OWASP Top 10 (2021) - the most critical security risks to web applications.

## Assessment Framework

### Pre-Assessment Checklist

| Item | Description |
|------|-------------|
| Scope definition | Define application boundaries, APIs, data flows |
| Access levels | Obtain test accounts at each privilege level |
| Environment | Staging/test environment (never production) |
| Authorization | Written permission for security testing |
| Tools ready | Burp Suite, OWASP ZAP, browser dev tools |


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## A01:2021 - Broken Access Control

**Risk**: Users acting outside intended permissions.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Horizontal privilege escalation | Change user IDs in requests (IDOR) | Critical |
| Vertical privilege escalation | Access admin functions as regular user | Critical |
| Missing function-level access | Direct URL access to restricted pages | High |
| Metadata manipulation | Modify JWT claims, hidden fields | High |
| CORS misconfiguration | Check Access-Control-Allow-Origin | Medium |
| Force browsing | Access /admin, /backup, /config directly | High |

### Testing Approach

```python
# IDOR Test Pattern
# 1. Login as User A, note resource ID
# 2. Login as User B
# 3. Attempt to access User A's resource

# Test endpoints:
GET /api/users/{user_id}           # Can User B see User A?
GET /api/documents/{doc_id}        # Ownership check?
PUT /api/profile/{user_id}         # Can modify others?
DELETE /api/posts/{post_id}        # Authorization check?
```

### Evidence Template

```markdown
## Finding: [IDOR/Privilege Escalation]
- **Endpoint**: GET /api/users/123
- **Authenticated as**: User B (ID: 456)
- **Expected**: 403 Forbidden
- **Actual**: 200 OK with User A data
- **Impact**: All user data accessible
- **Remediation**: Add ownership check
```

## A02:2021 - Cryptographic Failures

**Risk**: Exposure of sensitive data due to weak/missing cryptography.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Data in transit | Check HTTPS, TLS version, cipher suites | Critical |
| Data at rest | Database encryption, file storage | Critical |
| Password storage | Hashing algorithm (bcrypt/argon2 required) | Critical |
| Sensitive data exposure | PII in logs, URLs, error messages | High |
| Weak algorithms | MD5, SHA1, DES, RC4 detection | High |
| Key management | Hardcoded keys, weak key generation | Critical |

### Testing Commands

```bash
# Check TLS configuration
nmap --script ssl-enum-ciphers -p 443 target.com

# Check for HSTS
curl -I https://target.com | grep -i strict

# Test for weak ciphers
openssl s_client -connect target.com:443 -cipher 'LOW:EXP'
```

### Evidence Template

```markdown
## Finding: Weak Password Hashing
- **Location**: users table, password column
- **Current**: MD5 hash detected
- **Required**: bcrypt/argon2 with cost factor >= 12
- **Impact**: Password cracking feasible
- **Remediation**: Migrate to argon2id
```

## A03:2021 - Injection

**Risk**: Untrusted data sent to interpreter as command/query.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| SQL injection | Parameterized query bypass attempts | Critical |
| NoSQL injection | MongoDB operator injection ($ne, $gt) | Critical |
| Command injection | Shell metacharacter injection | Critical |
| LDAP injection | LDAP filter character injection | High |
| XPath injection | XPath query manipulation | High |
| Template injection | SSTI payloads ({{7*7}}) | Critical |

### SQL Injection Test Payloads

```
# Detection
' OR '1'='1
' OR '1'='1'--
' UNION SELECT NULL--
1; SELECT * FROM users--

# Error-based
' AND 1=CONVERT(int,@@version)--
' AND extractvalue(1,concat(0x7e,version()))--

# Time-based blind
' AND SLEEP(5)--
'; WAITFOR DELAY '0:0:5'--
```

### NoSQL Injection Test Payloads

```json
// MongoDB bypass
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": {"$gt": ""}, "password": {"$gt": ""}}
{"$where": "this.password.length > 0"}
```

### Evidence Template

```markdown
## Finding: SQL Injection
- **Endpoint**: POST /api/login
- **Parameter**: email
- **Payload**: `' OR '1'='1'--`
- **Response**: Authentication bypassed
- **Impact**: Complete database compromise
- **Remediation**: Use parameterized queries
```

## A04:2021 - Insecure Design

**Risk**: Missing or ineffective security controls at design level.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Threat modeling | Review architecture for attack surfaces | High |
| Business logic flaws | Test workflow manipulation | High |
| Missing rate limits | Brute force, enumeration possible | Medium |
| Insufficient validation | Business rule bypass | High |
| Race conditions | Concurrent request exploitation | High |

### Business Logic Tests

```
# Test scenarios:
- Can negative quantities be ordered?
- Can prices be manipulated client-side?
- Can steps in multi-step process be skipped?
- Can coupons be applied multiple times?
- Can free tier limits be bypassed?
```

## A05:2021 - Security Misconfiguration

**Risk**: Insecure default configurations, missing hardening.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Default credentials | admin/admin, test/test, etc. | Critical |
| Verbose errors | Stack traces exposed to users | Medium |
| Directory listing | Browse web directories | Medium |
| Unnecessary features | Unused endpoints, debug modes | High |
| Missing security headers | CSP, X-Frame-Options, HSTS | Medium |
| Cloud misconfig | S3 buckets, Azure blobs public | Critical |

### Security Headers Check

```bash
# Required headers
curl -I https://target.com | grep -E "(Content-Security-Policy|X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security)"

# Online tools
# https://securityheaders.com/
# https://observatory.mozilla.org/
```

## A06:2021 - Vulnerable Components

**Risk**: Using components with known vulnerabilities.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Outdated libraries | Compare versions to CVE databases | Varies |
| End-of-life software | Check vendor support status | High |
| Transitive dependencies | Scan nested dependencies | Varies |
| License compliance | Check for problematic licenses | Low |

### Scanning Commands

```bash
# JavaScript/Node
npm audit
yarn audit
npx snyk test

# Python
pip-audit
safety check
snyk test

# General
trivy fs --scanners vuln .
grype .
```

## A07:2021 - Authentication Failures

**Risk**: Broken authentication allowing account compromise.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Credential stuffing | Test known leaked credentials | High |
| Brute force | No rate limiting on login | High |
| Weak passwords | Minimum requirements enforced? | Medium |
| Session fixation | Can session ID be set by attacker? | High |
| Session timeout | Sessions expire appropriately? | Medium |
| MFA bypass | Can MFA be skipped? | Critical |

### Testing Approach

```python
# Brute force test
# Attempt 100+ logins with wrong password
# Check if account locks or rate limits apply

# Session tests:
# 1. Get session before login
# 2. Login
# 3. Check if session ID changed (should change!)

# Password reset tests:
# - Token expiration
# - Token reuse
# - Token predictability
```

## A08:2021 - Software/Data Integrity Failures

**Risk**: Code/infrastructure without integrity verification.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Insecure deserialization | Untrusted data deserialized | Critical |
| CI/CD security | Pipeline tampering possible? | Critical |
| Unsigned updates | Software updates verified? | High |
| CDN integrity | SRI hashes on external scripts? | Medium |

### Deserialization Tests

```python
# Java - ysoserial payloads
# PHP - serialize() injection
# Python - pickle injection
# .NET - BinaryFormatter gadgets

# Check for:
# - User-controlled serialized data
# - Lack of type checking
# - Missing integrity verification
```

## A09:2021 - Logging/Monitoring Failures

**Risk**: Breaches undetected due to insufficient logging.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Login failures logged | Multiple failures trigger alert? | High |
| Access control failures | 403s logged and monitored? | High |
| Input validation failures | Attack signatures logged? | Medium |
| High-value transactions | Audit trail exists? | High |
| Log injection | Can attacker inject log entries? | Medium |

## A10:2021 - Server-Side Request Forgery

**Risk**: Application fetches URLs without validation.

### Assessment Checklist

| Test | Method | Severity |
|------|--------|----------|
| Internal service access | Request internal IPs (127.0.0.1, 10.x) | Critical |
| Cloud metadata | Request 169.254.169.254 | Critical |
| Protocol smuggling | file://, gopher://, dict:// | High |
| DNS rebinding | Time-based DNS resolution attack | High |

### SSRF Test Payloads

```
# Internal access
http://127.0.0.1/admin
http://localhost:6379/  # Redis
http://169.254.169.254/latest/meta-data/  # AWS

# Bypass attempts
http://127.1/
http://0x7f000001/
http://2130706433/  # Decimal IP
http://[::1]/  # IPv6 localhost
```

## Assessment Report Template

```markdown
# Security Assessment Report

## Executive Summary
- **Application**: [Name]
- **Assessment Date**: [Date]
- **Assessor**: [Name]
- **Risk Rating**: Critical/High/Medium/Low

## Scope
- URLs tested
- Features assessed
- Out of scope items

## Findings Summary
| ID | Finding | OWASP Category | Severity | Status |
|----|---------|----------------|----------|--------|
| 01 | [Name] | A01 | Critical | Open |

## Detailed Findings
[One section per finding with evidence]

## Recommendations
[Prioritized remediation steps]

## Appendix
- Test methodology
- Tools used
- Raw evidence
```

## Remediation Priority Matrix

| Severity | SLA | Examples |
|----------|-----|----------|
| Critical | 24-48 hours | SQLi, RCE, authentication bypass |
| High | 1 week | IDOR, weak crypto, privilege escalation |
| Medium | 1 month | Missing headers, verbose errors |
| Low | Next release | Minor info disclosure, best practices |

## Tools Reference

| Tool | Purpose |
|------|---------|
| Burp Suite | Manual testing, interception |
| OWASP ZAP | Automated scanning |
| sqlmap | SQL injection |
| Nuclei | Template-based scanning |
| ffuf | Fuzzing, directory bruteforce |
| Nmap | Port scanning, service detection |


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

