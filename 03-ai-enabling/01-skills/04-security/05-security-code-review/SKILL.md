---
last_updated: 2026-02-25
status: active
name: security-code-review
description: Systematic code review for security vulnerabilities. Use when auditing source code for security issues.
triggers:
  files: ["**/src/**", "**/lib/**", "**/app/**", "**/*.py", "**/*.js", "**/*.ts"]
  keywords: ["security review", "code audit", "vulnerability", "secure code", "code review", "SAST", "static analysis"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Security Code Review

Systematic methodology for reviewing source code to identify security vulnerabilities before they reach production.

## Review Methodology

### Pre-Review Setup

| Step | Action |
|------|--------|
| 1 | Understand application architecture and data flows |
| 2 | Identify entry points (APIs, forms, file uploads) |
| 3 | Map sensitive data (credentials, PII, tokens) |
| 4 | Review authentication/authorization boundaries |
| 5 | Set up code navigation tools |

### Review Priorities

| Priority | Focus Area | Risk Level |
|----------|-----------|------------|
| 1 | Authentication & session management | Critical |
| 2 | Input validation & output encoding | Critical |
| 3 | Access control checks | Critical |
| 4 | Cryptographic implementations | High |
| 5 | Error handling & logging | Medium |
| 6 | Third-party integrations | Medium |


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Vulnerability Patterns by Language

### Python Security Patterns

```python
# DANGEROUS: Command injection
import os, subprocess

# BAD - shell=True with user input
os.system(f"convert {user_input}")
subprocess.call(user_input, shell=True)
subprocess.Popen(user_input, shell=True)

# GOOD - Use list arguments, no shell
subprocess.run(['convert', filename], shell=False)

# DANGEROUS: SQL injection
# BAD - String formatting
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
cursor.execute("SELECT * FROM users WHERE id = " + user_id)
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)

# GOOD - Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
cursor.execute("SELECT * FROM users WHERE id = %(id)s", {'id': user_id})

# DANGEROUS: Deserialization
import pickle, yaml
# BAD - Arbitrary code execution
pickle.loads(user_data)
yaml.load(user_data)  # Default loader is unsafe

# GOOD - Safe alternatives
yaml.safe_load(user_data)
json.loads(user_data)

# DANGEROUS: Path traversal
# BAD
open(f"/uploads/{user_filename}")
os.path.join("/uploads", user_input)  # Still vulnerable!

# GOOD
import pathlib
base = pathlib.Path("/uploads").resolve()
requested = (base / user_filename).resolve()
if not str(requested).startswith(str(base)):
    raise ValueError("Path traversal attempt")

# DANGEROUS: SSTI (Server-Side Template Injection)
# BAD - Jinja2 without sandboxing
template = Template(user_input)
render_template_string(user_input)

# GOOD - Never render user input as template
render_template("page.html", user_content=user_input)
```

### JavaScript/TypeScript Security Patterns

```javascript
// DANGEROUS: XSS vulnerabilities
// BAD - innerHTML with user input
element.innerHTML = userInput;
document.write(userInput);
$(element).html(userInput);

// GOOD - Use textContent or sanitize
element.textContent = userInput;
element.innerHTML = DOMPurify.sanitize(userInput);

// DANGEROUS: eval and friends
// BAD - Code execution
eval(userInput);
new Function(userInput)();
setTimeout(userInput, 1000);
setInterval(userInput, 1000);

// DANGEROUS: Prototype pollution
// BAD - Merging untrusted objects
Object.assign(target, userObject);
_.merge(target, userObject);
{...target, ...userObject};

// GOOD - Validate keys, use null prototype
const safe = Object.create(null);
for (const key of allowedKeys) {
  if (key in userObject) safe[key] = userObject[key];
}

// DANGEROUS: Path traversal in Node.js
// BAD
const file = path.join(__dirname, userInput);
fs.readFile(req.params.filename);

// GOOD
const safePath = path.normalize(userInput).replace(/^(\.\.(\/|\\|$))+/, '');
const fullPath = path.join(__dirname, 'uploads', safePath);
if (!fullPath.startsWith(path.join(__dirname, 'uploads'))) {
  throw new Error('Invalid path');
}

// DANGEROUS: NoSQL injection (MongoDB)
// BAD
db.users.find({ username: req.body.username });

// GOOD - Type check inputs
if (typeof req.body.username !== 'string') {
  throw new Error('Invalid input');
}
db.users.find({ username: req.body.username });

// DANGEROUS: Open redirect
// BAD
res.redirect(req.query.returnUrl);

// GOOD - Whitelist or validate
const allowedHosts = ['example.com', 'app.example.com'];
const url = new URL(req.query.returnUrl, 'https://example.com');
if (!allowedHosts.includes(url.hostname)) {
  throw new Error('Invalid redirect');
}
```

### SQL Query Patterns (All Languages)

```sql
-- DANGEROUS patterns to search for:
-- String concatenation
"SELECT * FROM users WHERE id = " + id
"SELECT * FROM users WHERE id = ${id}"
"SELECT * FROM users WHERE id = " . $id
f"SELECT * FROM users WHERE id = {id}"

-- Dynamic table/column names
"SELECT * FROM " + tableName
"ORDER BY " + sortColumn

-- SAFE patterns:
-- Parameterized queries
"SELECT * FROM users WHERE id = ?"
"SELECT * FROM users WHERE id = $1"
"SELECT * FROM users WHERE id = :id"

-- For dynamic identifiers, use whitelist
ALLOWED_COLUMNS = {'name', 'email', 'created_at'}
if column not in ALLOWED_COLUMNS:
    raise ValueError("Invalid column")
```

## Search Patterns for Common Vulnerabilities

### Grep/Search Patterns

```bash
# Authentication issues
grep -rn "password.*=.*['\"]" .
grep -rn "api[_-]?key.*=.*['\"]" .
grep -rn "secret.*=.*['\"]" .
grep -rn "token.*=.*['\"]" .

# SQL injection
grep -rn "execute.*%s" .
grep -rn "execute.*\+" .
grep -rn "raw.*sql" .

# Command injection
grep -rn "os.system" .
grep -rn "subprocess.*shell.*True" .
grep -rn "exec(" .
grep -rn "eval(" .

# XSS
grep -rn "innerHTML" .
grep -rn "dangerouslySetInnerHTML" .
grep -rn "document.write" .
grep -rn "v-html" .  # Vue

# Insecure deserialization
grep -rn "pickle.load" .
grep -rn "yaml.load" .
grep -rn "unserialize" .
grep -rn "readObject" .

# Path traversal
grep -rn "open.*\+" .
grep -rn "readFile.*req\." .
grep -rn "path.join.*req\." .

# Crypto issues
grep -rn "MD5\|md5" .
grep -rn "SHA1\|sha1" .
grep -rn "DES\|des" .
grep -rn "ECB" .
grep -rn "random()" .  # Non-crypto random
```

## Code Review Checklist

### Input Validation

| Check | Status |
|-------|--------|
| All user inputs validated (type, length, format) | |
| Whitelist validation preferred over blacklist | |
| Input validation on server-side (not just client) | |
| File uploads: type, size, content validated | |
| JSON/XML parsers configured safely | |

### Output Encoding

| Check | Status |
|-------|--------|
| HTML context: entities encoded | |
| JavaScript context: JSON.stringify or escape | |
| URL context: URL-encoded | |
| SQL: parameterized queries only | |
| Command line: no shell=True with user input | |

### Authentication

| Check | Status |
|-------|--------|
| Passwords hashed with bcrypt/argon2/scrypt | |
| Password requirements enforced | |
| Account lockout after failed attempts | |
| Session tokens cryptographically random | |
| Session invalidated on logout | |
| Session timeout implemented | |
| MFA available for sensitive operations | |

### Authorization

| Check | Status |
|-------|--------|
| Authorization checked on every request | |
| IDOR prevention (ownership verification) | |
| Role-based access control implemented | |
| Sensitive functions require re-authentication | |
| API endpoints have proper access controls | |

### Cryptography

| Check | Status |
|-------|--------|
| Modern algorithms (AES-256, SHA-256+) | |
| No hardcoded keys/secrets | |
| Secrets from environment/vault | |
| TLS 1.2+ enforced | |
| Certificates validated properly | |
| Cryptographic random for security-sensitive values | |

### Error Handling

| Check | Status |
|-------|--------|
| Generic errors to users | |
| Detailed errors logged securely | |
| No stack traces in production | |
| Errors don't reveal system info | |
| Failed operations logged | |

### Logging

| Check | Status |
|-------|--------|
| Security events logged | |
| No sensitive data in logs | |
| Log injection prevented | |
| Logs protected from tampering | |

## Severity Classification

| Severity | Criteria | Examples |
|----------|----------|----------|
| Critical | Remote code execution, authentication bypass | SQLi, RCE, deserialization |
| High | Data exposure, privilege escalation | IDOR, path traversal, XSS |
| Medium | Limited impact, requires conditions | CSRF, open redirect |
| Low | Information disclosure, best practices | Verbose errors, missing headers |

## Finding Report Template

```markdown
## Finding: [Vulnerability Name]

### Location
- File: `src/api/users.py`
- Line: 45-52
- Function: `get_user_by_email()`

### Description
[Brief description of the vulnerability]

### Vulnerable Code
```python
def get_user_by_email(email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return db.execute(query)
```

### Attack Scenario
1. Attacker provides input: `' OR '1'='1'--`
2. Query becomes: `SELECT * FROM users WHERE email = '' OR '1'='1'--'`
3. Returns all users in database

### Impact
- **Confidentiality**: All user data exposed
- **Integrity**: Data modification possible
- **Availability**: Database could be deleted

### Remediation
```python
def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = ?"
    return db.execute(query, (email,))
```

### References
- CWE-89: SQL Injection
- OWASP: A03:2021 Injection
```

## Automated Tools Integration

| Tool | Purpose | Integration |
|------|---------|-------------|
| Semgrep | Pattern-based SAST | CI/CD, pre-commit |
| Bandit | Python security linter | CI/CD, pre-commit |
| ESLint security plugins | JS/TS security rules | CI/CD, pre-commit |
| SonarQube | Comprehensive SAST | CI/CD |
| CodeQL | Semantic code analysis | GitHub Actions |
| Snyk Code | AI-powered SAST | CI/CD, IDE |

### Semgrep Example Rules

```yaml
rules:
  - id: sql-injection
    patterns:
      - pattern: cursor.execute($QUERY % ...)
      - pattern: cursor.execute($QUERY + ...)
      - pattern: cursor.execute(f"...")
    message: "Potential SQL injection"
    severity: ERROR

  - id: command-injection
    patterns:
      - pattern: subprocess.call(..., shell=True, ...)
      - pattern: os.system(...)
    message: "Potential command injection"
    severity: ERROR
```

## Review Workflow

```
1. Automated scan (SAST tools)
        ↓
2. Triage automated findings
        ↓
3. Manual review of high-risk areas
        ↓
4. Document findings
        ↓
5. Prioritize remediation
        ↓
6. Verify fixes
        ↓
7. Update security tests
```


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

