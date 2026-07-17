---
last_updated: 2026-02-25
status: active
name: input-validation-security
description: Input validation patterns, whitelist validation, sanitization techniques. Use when implementing or reviewing input handling.
triggers:
  files: ["**/validators/**", "**/schemas/**", "**/forms/**", "**/api/**", "**/input/**"]
  keywords: ["validation", "sanitize", "sanitization", "whitelist", "input", "escape", "encode", "filter", "validate", "schema"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Input Validation Security

Comprehensive patterns for validating, sanitizing, and encoding user input to prevent injection attacks and data corruption.

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Never trust input** | All input is malicious until validated |
| **Whitelist over blacklist** | Define what IS allowed, not what isn't |
| **Validate on server** | Client validation is UX only |
| **Validate early** | Reject bad input at system boundary |
| **Fail secure** | Reject input on validation error |
| **Context-specific** | Encode output for its context |


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Validation Strategy

```
User Input → Type Check → Format Validation → Business Rules → Sanitize/Encode → Use
                ↓              ↓                    ↓
             Reject         Reject               Reject
```

## Input Types and Validation

### String Validation

```python
from pydantic import BaseModel, validator, constr
import re

class UserInput(BaseModel):
    # Length constraints
    username: constr(min_length=3, max_length=30)

    # Regex pattern
    email: constr(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    # Alphanumeric only
    code: constr(regex=r'^[a-zA-Z0-9]+$')

    @validator('username')
    def validate_username(cls, v):
        # Whitelist: only alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric')
        # No reserved words
        if v.lower() in ['admin', 'root', 'system']:
            raise ValueError('Reserved username')
        return v
```

```javascript
// JavaScript/TypeScript validation with Zod
import { z } from 'zod';

const UserSchema = z.object({
  username: z.string()
    .min(3)
    .max(30)
    .regex(/^[a-zA-Z0-9_]+$/),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

// Validate
const result = UserSchema.safeParse(input);
if (!result.success) {
  throw new Error(result.error.message);
}
```

### Numeric Validation

```python
from pydantic import BaseModel, validator

class OrderInput(BaseModel):
    quantity: int
    price: float
    discount_percent: float

    @validator('quantity')
    def validate_quantity(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('Quantity must be 1-1000')
        return v

    @validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price cannot be negative')
        if v > 1000000:
            raise ValueError('Price exceeds maximum')
        # Prevent floating point issues
        return round(v, 2)

    @validator('discount_percent')
    def validate_discount(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Discount must be 0-100')
        return v
```

### Email Validation

```python
import re
from email_validator import validate_email, EmailNotValidError

def validate_email_strict(email: str) -> str:
    """Comprehensive email validation"""
    # Basic format check
    if not email or len(email) > 254:
        raise ValueError("Invalid email length")

    # Use robust library
    try:
        valid = validate_email(email, check_deliverability=False)
        return valid.email
    except EmailNotValidError as e:
        raise ValueError(str(e))

# Additional checks for security
def is_disposable_email(email: str) -> bool:
    """Check against disposable email domains"""
    disposable_domains = {'tempmail.com', 'throwaway.com', ...}
    domain = email.split('@')[1].lower()
    return domain in disposable_domains
```

### URL Validation

```python
from urllib.parse import urlparse
import ipaddress

def validate_url_safe(url: str) -> str:
    """Validate URL and prevent SSRF"""
    try:
        parsed = urlparse(url)
    except Exception:
        raise ValueError("Invalid URL format")

    # Scheme whitelist
    if parsed.scheme not in ('http', 'https'):
        raise ValueError("Only HTTP(S) URLs allowed")

    # No credentials in URL
    if parsed.username or parsed.password:
        raise ValueError("Credentials not allowed in URL")

    # Block internal IPs
    try:
        hostname = parsed.hostname
        if hostname:
            import socket
            ip = ipaddress.ip_address(socket.gethostbyname(hostname))
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                raise ValueError("Internal URLs not allowed")
    except socket.gaierror:
        pass  # DNS resolution failed, may be acceptable

    return url
```

### File Upload Validation

```python
import magic
import hashlib
from pathlib import Path

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf'}
ALLOWED_MIMETYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'application/pdf'
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file_upload(file_content: bytes, filename: str) -> dict:
    """Comprehensive file upload validation"""

    # Size check
    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError(f"File exceeds {MAX_FILE_SIZE} bytes")

    if len(file_content) == 0:
        raise ValueError("Empty file")

    # Extension whitelist
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension {ext} not allowed")

    # MIME type from content (magic bytes)
    detected_mime = magic.from_buffer(file_content, mime=True)
    if detected_mime not in ALLOWED_MIMETYPES:
        raise ValueError(f"Content type {detected_mime} not allowed")

    # Filename sanitization
    safe_filename = sanitize_filename(filename)

    return {
        'content': file_content,
        'filename': safe_filename,
        'mime_type': detected_mime,
        'size': len(file_content),
        'hash': hashlib.sha256(file_content).hexdigest()
    }

def sanitize_filename(filename: str) -> str:
    """Remove dangerous characters from filename"""
    import re
    # Remove path separators and null bytes
    filename = filename.replace('/', '_').replace('\\', '_').replace('\x00', '')
    # Remove non-printable characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Prevent hidden files
    filename = filename.lstrip('.')
    # Limit length
    name, ext = Path(filename).stem[:100], Path(filename).suffix[:10]
    return f"{name}{ext}" if name else "unnamed"
```

### JSON/Object Validation

```python
from pydantic import BaseModel, validator
from typing import Any, Dict

class SafeJsonInput(BaseModel):
    data: Dict[str, Any]

    @validator('data')
    def validate_json_depth(cls, v, values):
        """Prevent deeply nested JSON (DoS prevention)"""
        def check_depth(obj, current_depth=0, max_depth=10):
            if current_depth > max_depth:
                raise ValueError("JSON too deeply nested")
            if isinstance(obj, dict):
                for value in obj.values():
                    check_depth(value, current_depth + 1, max_depth)
            elif isinstance(obj, list):
                for item in obj:
                    check_depth(item, current_depth + 1, max_depth)
        check_depth(v)
        return v

    @validator('data')
    def validate_json_size(cls, v):
        """Prevent oversized JSON"""
        import json
        if len(json.dumps(v)) > 1_000_000:  # 1MB
            raise ValueError("JSON payload too large")
        return v
```

## Output Encoding by Context

### HTML Context

```python
from markupsafe import escape

def encode_html(text: str) -> str:
    """Encode for HTML content"""
    return escape(text)

# Results:
# < → &lt;
# > → &gt;
# & → &amp;
# " → &quot;
# ' → &#39;
```

### JavaScript Context

```python
import json

def encode_for_js(value: any) -> str:
    """Encode value for JavaScript context"""
    # JSON encoding handles most cases
    encoded = json.dumps(value)
    # Additional escaping for </script>
    encoded = encoded.replace('</script>', '<\\/script>')
    return encoded
```

### URL Context

```python
from urllib.parse import quote, quote_plus

def encode_url_param(value: str) -> str:
    """Encode for URL parameter"""
    return quote(value, safe='')

def encode_form_data(value: str) -> str:
    """Encode for form data"""
    return quote_plus(value)
```

### SQL Context

```python
# NEVER encode/escape for SQL - use parameterized queries

# BAD - manual escaping is error-prone
def bad_escape(value):
    return value.replace("'", "''")  # Incomplete!

# GOOD - parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Shell Context

```python
import shlex

def encode_shell_arg(value: str) -> str:
    """Encode for shell argument"""
    return shlex.quote(value)

# But better: avoid shell entirely
import subprocess
subprocess.run(['command', arg1, arg2], shell=False)
```

## Sanitization Patterns

### HTML Sanitization (Rich Text)

```python
import bleach

ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'a', 'ul', 'ol', 'li', 'br']
ALLOWED_ATTRS = {'a': ['href', 'title']}

def sanitize_html(html: str) -> str:
    """Sanitize HTML for rich text display"""
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True
    )

# Link sanitization
def sanitize_link(url: str) -> str:
    """Ensure links are safe"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https', 'mailto'):
        return '#'
    return url
```

```javascript
// JavaScript with DOMPurify
import DOMPurify from 'dompurify';

const sanitized = DOMPurify.sanitize(userHtml, {
  ALLOWED_TAGS: ['p', 'b', 'i', 'a', 'ul', 'ol', 'li'],
  ALLOWED_ATTR: ['href'],
  ALLOW_DATA_ATTR: false
});
```

### Path Sanitization

```python
from pathlib import Path

def sanitize_path(base_dir: str, user_path: str) -> Path:
    """Safely join paths, preventing traversal"""
    base = Path(base_dir).resolve()

    # Normalize and resolve
    requested = (base / user_path).resolve()

    # Verify still under base
    if not str(requested).startswith(str(base)):
        raise ValueError("Path traversal detected")

    return requested
```

## Validation Framework Comparison

| Framework | Language | Features |
|-----------|----------|----------|
| Pydantic | Python | Type coercion, nested validation |
| Marshmallow | Python | Serialization focus |
| Cerberus | Python | Flexible rules |
| Zod | TypeScript | Type inference |
| Joi | JavaScript | Comprehensive validation |
| class-validator | TypeScript | Decorator-based |

## Common Validation Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Client-only validation | Easily bypassed | Always validate server-side |
| Blacklist filtering | Incomplete, bypassable | Use whitelist |
| Regex without anchors | Partial matching | Use `^...$` |
| Type coercion trust | `"123" == 123` issues | Strict type checking |
| Encoding instead of rejecting | Hiding bad input | Reject invalid input |
| Missing length limits | DoS via large input | Always set max length |

## Testing Validation

```python
import pytest

class TestInputValidation:
    def test_rejects_sql_injection(self):
        with pytest.raises(ValueError):
            validate_username("admin'--")

    def test_rejects_xss(self):
        with pytest.raises(ValueError):
            validate_name("<script>alert(1)</script>")

    def test_rejects_path_traversal(self):
        with pytest.raises(ValueError):
            sanitize_path("/uploads", "../etc/passwd")

    def test_rejects_oversized_input(self):
        with pytest.raises(ValueError):
            validate_bio("x" * 100001)

    def test_accepts_valid_input(self):
        result = validate_username("john_doe_123")
        assert result == "john_doe_123"

# Fuzzing test
def test_validation_fuzzing():
    """Test with malicious payloads"""
    payloads = [
        "' OR '1'='1",
        "<script>alert(1)</script>",
        "../../../etc/passwd",
        "\x00hidden",
        "A" * 1000000,
        {"$ne": 1},  # NoSQL injection
    ]

    for payload in payloads:
        with pytest.raises((ValueError, TypeError)):
            validate_input(payload)
```

## Validation Cheat Sheet

| Input Type | Validation | Encoding |
|------------|------------|----------|
| Username | `^[a-zA-Z0-9_]{3,30}$` | HTML encode on display |
| Email | Library validation | HTML encode on display |
| URL | Parse, whitelist schemes | URL encode params |
| Integer | Type + range check | N/A |
| File name | Whitelist chars, no path sep | N/A |
| HTML content | Sanitize with allowlist | Pre-sanitized |
| SQL values | Type validation | Parameterized query |
| Shell args | Whitelist or reject | Avoid shell |


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

