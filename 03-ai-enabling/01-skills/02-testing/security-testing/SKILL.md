---
last_updated: 2026-02-25
status: active
name: security-testing
description: Security testing fundamentals - OWASP Top 10, penetration testing basics, vulnerability assessment. Use when testing security controls.
triggers:
  files: ["**/security/**", "**/auth/**", "**/*auth*", "**/*login*", "**/*password*", "**/tests/security/**"]
  keywords: ["security test", "penetration test", "OWASP", "vulnerability", "SQL injection", "XSS", "CSRF", "authentication test", "authorization test"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides security testing practices aligned with OWASP standards. The goal is identifying vulnerabilities before attackers do through systematic testing of security controls.

The user provides security testing requirements: an application to assess, a feature with security implications, or a security test suite to design. They may include context about threat model, compliance requirements, or specific vulnerabilities to test.

## Security Testing Philosophy

**Defensive testing approach:**
- Assume all inputs are malicious
- Test authentication at every layer
- Verify authorization for every action
- Validate output encoding
- Check error handling for information leakage

**Attacker mindset (ethical):**
- What would an attacker try?
- What data is valuable?
- What paths bypass controls?
- What happens when things fail?


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## OWASP Top 10 Testing Guide

### A01: Broken Access Control

**What to test:**
- Horizontal privilege escalation (access other users' data)
- Vertical privilege escalation (access admin functions)
- Missing access controls on functions
- CORS misconfiguration

**Test cases:**
```python
def test_cannot_access_other_users_data():
    # Login as user A
    token_a = login("user_a")

    # Try to access user B's data
    response = client.get("/users/user_b/profile", auth=token_a)
    assert response.status == 403

def test_cannot_access_admin_without_role():
    # Login as regular user
    token = login("regular_user")

    # Try to access admin endpoint
    response = client.get("/admin/users", auth=token)
    assert response.status == 403

def test_direct_object_reference():
    # Create order as user A
    order = create_order(user="user_a")

    # Login as user B
    token_b = login("user_b")

    # Try to access user A's order directly
    response = client.get(f"/orders/{order.id}", auth=token_b)
    assert response.status == 403
```

### A02: Cryptographic Failures

**What to test:**
- Sensitive data in transit (HTTPS)
- Sensitive data at rest (encryption)
- Password storage (hashing algorithm)
- Key management

**Test cases:**
```python
def test_passwords_are_hashed():
    user = create_user(password="secret123")

    # Password should not be stored in plaintext
    db_user = database.get_user(user.id)
    assert db_user.password != "secret123"
    assert len(db_user.password) > 50  # Hashed length

def test_sensitive_data_not_in_logs():
    response = login(password="secret123")

    logs = get_recent_logs()
    assert "secret123" not in logs
    assert "password" not in logs.lower() or "password=***" in logs

def test_https_redirect():
    response = client.get("http://example.com/login", allow_redirects=False)
    assert response.status == 301 or response.status == 302
    assert response.headers["Location"].startswith("https://")
```

### A03: Injection

**What to test:**
- SQL injection
- NoSQL injection
- Command injection
- LDAP injection

**SQL Injection test cases:**
```python
def test_sql_injection_in_search():
    payloads = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "1; SELECT * FROM users",
        "' UNION SELECT password FROM users --",
    ]

    for payload in payloads:
        response = client.get(f"/search?q={payload}")
        # Should not cause error or return unexpected data
        assert response.status == 200
        assert "error" not in response.text.lower()
        assert "password" not in response.text

def test_parameterized_queries():
    # This should work safely
    response = client.get("/users?name=O'Brien")
    assert response.status == 200  # Handles apostrophe correctly
```

**Command injection test cases:**
```python
def test_command_injection_in_filename():
    payloads = [
        "; rm -rf /",
        "| cat /etc/passwd",
        "$(whoami)",
        "`ls -la`",
    ]

    for payload in payloads:
        response = client.post("/upload", data={"filename": payload})
        # Should reject or sanitize malicious filenames
        assert response.status in [200, 400]  # Accepted or rejected safely
        # Verify no command execution
```

### A04: Insecure Design

**What to test:**
- Business logic flaws
- Missing rate limiting
- Insufficient anti-automation

**Test cases:**
```python
def test_rate_limiting_on_login():
    # Attempt many failed logins
    for i in range(10):
        response = client.post("/login", data={
            "username": "user",
            "password": f"wrong{i}"
        })

    # Should be rate limited
    response = client.post("/login", data={
        "username": "user",
        "password": "correct"
    })
    assert response.status == 429  # Too Many Requests

def test_cannot_skip_payment_step():
    # Start checkout
    client.post("/checkout/start")

    # Try to skip directly to confirmation
    response = client.post("/checkout/confirm")
    assert response.status == 400  # Should require payment step
```

### A05: Security Misconfiguration

**What to test:**
- Default credentials
- Unnecessary features enabled
- Error messages with sensitive info
- Missing security headers

**Test cases:**
```python
def test_security_headers_present():
    response = client.get("/")

    headers = response.headers
    assert "X-Content-Type-Options" in headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert "X-Frame-Options" in headers
    assert "Content-Security-Policy" in headers
    assert "Strict-Transport-Security" in headers

def test_no_stack_trace_in_errors():
    response = client.get("/api/nonexistent")

    assert response.status == 404
    assert "traceback" not in response.text.lower()
    assert "exception" not in response.text.lower()
    assert "line" not in response.text  # No line numbers

def test_default_credentials_removed():
    # Try common default credentials
    defaults = [
        ("admin", "admin"),
        ("admin", "password"),
        ("root", "root"),
        ("admin", "123456"),
    ]

    for username, password in defaults:
        response = client.post("/login", data={
            "username": username,
            "password": password
        })
        assert response.status != 200  # Should fail
```

### A06: Vulnerable and Outdated Components

**What to test:**
- Known CVEs in dependencies
- Outdated libraries
- Unnecessary dependencies

**Test approach:**
```bash
# JavaScript
npm audit
npm audit --json > audit-results.json

# Python
safety check
pip-audit

# General
trivy image myapp:latest
```

### A07: Identification and Authentication Failures

**What to test:**
- Weak password policies
- Session management
- Multi-factor authentication bypass
- Credential stuffing protection

**Test cases:**
```python
def test_weak_password_rejected():
    weak_passwords = [
        "123456",
        "password",
        "qwerty",
        "abc",  # Too short
    ]

    for password in weak_passwords:
        response = client.post("/register", data={
            "username": "testuser",
            "password": password
        })
        assert response.status == 400
        assert "password" in response.json()["error"].lower()

def test_session_expires():
    token = login("user")

    # Advance time beyond session timeout
    time_travel(hours=25)

    response = client.get("/profile", auth=token)
    assert response.status == 401

def test_session_invalidated_on_logout():
    token = login("user")

    # Logout
    client.post("/logout", auth=token)

    # Old token should not work
    response = client.get("/profile", auth=token)
    assert response.status == 401

def test_session_invalidated_on_password_change():
    token = login("user")

    # Change password
    client.post("/change-password", auth=token, data={
        "old_password": "oldpass",
        "new_password": "newpass123!"
    })

    # Old session should be invalid
    response = client.get("/profile", auth=token)
    assert response.status == 401
```

### A08: Software and Data Integrity Failures

**What to test:**
- CI/CD pipeline security
- Unsigned updates
- Deserialization vulnerabilities

**Test cases:**
```python
def test_insecure_deserialization():
    # Python pickle payload (malicious)
    import pickle
    malicious = pickle.dumps({"__reduce__": (os.system, ("id",))})

    response = client.post("/api/import", data=malicious)
    # Should reject or safely handle
    assert response.status in [400, 415]  # Bad request or unsupported type

def test_signature_verification():
    # Modify signed data
    signed_data = get_signed_data()
    modified = signed_data.replace("amount=100", "amount=1")

    response = client.post("/process", data=modified)
    assert response.status == 400  # Signature invalid
```

### A09: Security Logging and Monitoring Failures

**What to test:**
- Login attempts logged
- Access control failures logged
- Sensitive data not logged
- Log injection prevention

**Test cases:**
```python
def test_failed_login_logged():
    client.post("/login", data={
        "username": "user",
        "password": "wrong"
    })

    logs = get_security_logs()
    assert any("login failed" in log.lower() for log in logs)
    assert any("user" in log for log in logs)

def test_log_injection_prevented():
    # Try to inject fake log entry
    client.post("/login", data={
        "username": "user\n[INFO] Admin logged in successfully",
        "password": "test"
    })

    logs = get_security_logs()
    # Should not have injected entry
    assert not any("Admin logged in successfully" in log for log in logs)
```

### A10: Server-Side Request Forgery (SSRF)

**What to test:**
- URL parameter handling
- Internal network access
- Cloud metadata access

**Test cases:**
```python
def test_ssrf_internal_network():
    internal_urls = [
        "http://localhost/admin",
        "http://127.0.0.1/admin",
        "http://192.168.1.1/",
        "http://10.0.0.1/",
        "http://169.254.169.254/",  # AWS metadata
    ]

    for url in internal_urls:
        response = client.post("/fetch-url", data={"url": url})
        assert response.status in [400, 403]  # Blocked

def test_ssrf_protocol_bypass():
    payloads = [
        "file:///etc/passwd",
        "gopher://localhost:25/",
        "dict://localhost:11211/",
    ]

    for payload in payloads:
        response = client.post("/fetch-url", data={"url": payload})
        assert response.status in [400, 403]
```

## XSS Testing

### Reflected XSS

```python
def test_reflected_xss():
    payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert(1)",
        "<svg onload=alert(1)>",
        "'><script>alert(1)</script>",
    ]

    for payload in payloads:
        response = client.get(f"/search?q={payload}")
        # Payload should be escaped in response
        assert payload not in response.text
        assert "&lt;script&gt;" in response.text or "script" not in response.text
```

### Stored XSS

```python
def test_stored_xss():
    # Store malicious content
    client.post("/comments", data={
        "text": "<script>alert(document.cookie)</script>"
    })

    # Retrieve and verify escaped
    response = client.get("/comments")
    assert "<script>" not in response.text
    assert "&lt;script&gt;" in response.text or "script" not in response.text
```

## CSRF Testing

```python
def test_csrf_token_required():
    # Login to get session
    login("user")

    # Try action without CSRF token
    response = client.post("/transfer", data={
        "to": "attacker",
        "amount": 1000
    }, csrf=False)

    assert response.status == 403

def test_csrf_token_validated():
    login("user")

    # Try with invalid CSRF token
    response = client.post("/transfer", data={
        "to": "attacker",
        "amount": 1000,
        "csrf_token": "invalid"
    })

    assert response.status == 403
```

## Authentication Testing

### Password Testing

```python
def test_password_requirements():
    test_cases = [
        ("short", False),           # Too short
        ("nouppercase1!", False),   # No uppercase
        ("NOLOWERCASE1!", False),   # No lowercase
        ("NoNumbers!", False),      # No numbers
        ("NoSpecial123", False),    # No special chars
        ("ValidPass1!", True),      # Valid
    ]

    for password, should_pass in test_cases:
        response = client.post("/register", data={
            "username": "test",
            "password": password
        })
        if should_pass:
            assert response.status == 200
        else:
            assert response.status == 400

def test_password_not_in_response():
    response = client.post("/register", data={
        "username": "test",
        "password": "SecretPass1!"
    })

    assert "SecretPass1!" not in response.text
    assert "password" not in response.json().get("user", {})
```

### Session Testing

```python
def test_session_token_entropy():
    tokens = set()
    for _ in range(100):
        token = login("user")
        logout(token)
        tokens.add(token)

    # All tokens should be unique
    assert len(tokens) == 100

    # Tokens should be long enough
    assert all(len(t) >= 32 for t in tokens)

def test_session_fixation():
    # Get session before login
    session_before = client.get_session_id()

    # Login
    login("user")

    # Session should change after login
    session_after = client.get_session_id()
    assert session_before != session_after
```

## Security Test Organization

### Test File Structure

```
tests/
  security/
    test_authentication.py
    test_authorization.py
    test_injection.py
    test_xss.py
    test_csrf.py
    test_session.py
    test_headers.py
    test_crypto.py
```

### CI Integration

```yaml
security-tests:
  stage: test
  script:
    - pytest tests/security/ -v --junitxml=security-results.xml
    - npm audit --audit-level=high
    - trivy image $IMAGE --severity HIGH,CRITICAL
  allow_failure: false
```

## Quick Reference

### Security Test Checklist

| Area | Tests |
|------|-------|
| Authentication | Login, logout, password policy, session management |
| Authorization | Role checks, object access, privilege escalation |
| Input validation | Injection, XSS, path traversal |
| Output encoding | HTML, JSON, URL encoding |
| Cryptography | Hashing, encryption, key management |
| Configuration | Headers, error handling, defaults |
| Logging | Security events logged, sensitive data excluded |

### Common Payloads

| Attack | Payload Examples |
|--------|-----------------|
| SQL Injection | `' OR '1'='1`, `'; DROP TABLE--` |
| XSS | `<script>alert(1)</script>`, `<img onerror=alert(1)>` |
| Command Injection | `; ls -la`, `| cat /etc/passwd` |
| Path Traversal | `../../../etc/passwd`, `....//....//` |
| SSRF | `http://localhost`, `http://169.254.169.254` |

## Summary

Security testing is about **finding vulnerabilities before attackers**:

1. **Follow OWASP Top 10** as baseline coverage
2. **Test all input points** for injection
3. **Verify access controls** at every layer
4. **Check authentication** thoroughly
5. **Validate security headers** and configuration
6. **Automate in CI** for continuous security
7. **Think like an attacker** (ethically)


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

