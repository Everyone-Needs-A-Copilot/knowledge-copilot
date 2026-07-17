---
last_updated: 2026-02-25
status: active
name: security-headers
description: HTTP security headers, CSP, CORS, HSTS, and browser security controls. Use when configuring web application security headers.
triggers:
  files: ["**/middleware/**", "**/config/**", "**/nginx*", "**/apache*", "**/*.conf"]
  keywords: ["security headers", "CSP", "CORS", "HSTS", "X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options", "Referrer-Policy"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Security Headers Deep Expertise

This skill provides comprehensive guidance for implementing HTTP security headers. Apply this knowledge when configuring web servers, implementing middleware, or hardening web applications.

## Security Headers Overview

### Essential Headers

| Header | Purpose | Impact |
|--------|---------|--------|
| Content-Security-Policy | Control resource loading | Prevents XSS, injection |
| Strict-Transport-Security | Enforce HTTPS | Prevents downgrade attacks |
| X-Frame-Options | Prevent framing | Prevents clickjacking |
| X-Content-Type-Options | Prevent MIME sniffing | Prevents content type attacks |
| Referrer-Policy | Control referrer info | Privacy, info leakage |
| Permissions-Policy | Control browser features | Limits attack surface |

### Implementation Priority

| Priority | Header | Risk if Missing |
|----------|--------|-----------------|
| Critical | Content-Security-Policy | XSS vulnerabilities |
| Critical | Strict-Transport-Security | MitM attacks |
| High | X-Frame-Options | Clickjacking |
| High | X-Content-Type-Options | MIME attacks |
| Medium | Referrer-Policy | Information leakage |
| Medium | Permissions-Policy | Feature abuse |


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Content-Security-Policy (CSP)

### CSP Directive Reference

| Directive | Controls | Default |
|-----------|----------|---------|
| default-src | Fallback for all | None |
| script-src | JavaScript | default-src |
| style-src | CSS | default-src |
| img-src | Images | default-src |
| font-src | Fonts | default-src |
| connect-src | XHR, WebSocket, fetch | default-src |
| frame-src | Iframes | default-src |
| object-src | Plugins | default-src |
| media-src | Audio, video | default-src |
| base-uri | Base element | None |
| form-action | Form submissions | None |
| frame-ancestors | Who can frame page | None |

### CSP Source Values

| Value | Meaning |
|-------|---------|
| 'self' | Same origin |
| 'none' | Block all |
| 'unsafe-inline' | Allow inline (avoid!) |
| 'unsafe-eval' | Allow eval (avoid!) |
| 'nonce-{value}' | Nonce-based allowlist |
| 'sha256-{hash}' | Hash-based allowlist |
| https: | HTTPS only |
| data: | Data URIs |
| blob: | Blob URIs |
| *.example.com | Wildcard domain |

### Progressive CSP Implementation

```python
from starlette.middleware.base import BaseHTTPMiddleware
import secrets

class CSPMiddleware(BaseHTTPMiddleware):
    """Content Security Policy middleware"""

    def __init__(self, app, mode: str = "enforce"):
        super().__init__(app)
        self.mode = mode  # "enforce" or "report-only"

    async def dispatch(self, request, call_next):
        # Generate nonce for this request
        nonce = secrets.token_urlsafe(16)
        request.state.csp_nonce = nonce

        response = await call_next(request)

        # Build CSP header
        csp = self.build_csp(nonce)

        header_name = (
            "Content-Security-Policy" if self.mode == "enforce"
            else "Content-Security-Policy-Report-Only"
        )

        response.headers[header_name] = csp
        return response

    def build_csp(self, nonce: str) -> str:
        """Build CSP directives"""
        directives = [
            # Default: only same origin
            "default-src 'self'",

            # Scripts: self + nonce for inline
            f"script-src 'self' 'nonce-{nonce}'",

            # Styles: self + unsafe-inline (CSS-in-JS often needs this)
            "style-src 'self' 'unsafe-inline'",

            # Images: self + data URIs + HTTPS
            "img-src 'self' data: https:",

            # Fonts: self + Google Fonts
            "font-src 'self' https://fonts.gstatic.com",

            # XHR/fetch: self + API
            "connect-src 'self' https://api.example.com",

            # Frames: none (no iframes)
            "frame-src 'none'",

            # Plugins: none
            "object-src 'none'",

            # Base URI: self only
            "base-uri 'self'",

            # Form submission: self only
            "form-action 'self'",

            # Who can frame us: nobody
            "frame-ancestors 'none'",

            # Report violations
            "report-uri /api/csp-report",
        ]

        return "; ".join(directives)

# CSP violation reporting endpoint
@app.post("/api/csp-report")
async def csp_report(request: Request):
    """Receive CSP violation reports"""
    report = await request.json()

    # Log violation for analysis
    logger.warning(f"CSP Violation: {json.dumps(report)}")

    # Track common violations
    await track_csp_violation(report)

    return {"status": "received"}
```

### Nonce-Based Script Loading

```python
# In template context
def get_template_context(request: Request) -> dict:
    return {
        "csp_nonce": request.state.csp_nonce
    }

# In Jinja2 template
"""
<script nonce="{{ csp_nonce }}">
    // Inline script allowed with nonce
    console.log('Hello');
</script>
"""

# React with nonce
"""
// Pass nonce to React
window.__CSP_NONCE__ = '{{ csp_nonce }}';

// In React component for dynamic scripts
const script = document.createElement('script');
script.nonce = window.__CSP_NONCE__;
script.src = 'https://allowed-cdn.com/lib.js';
document.head.appendChild(script);
"""
```

## Strict-Transport-Security (HSTS)

### HSTS Configuration

```python
class HSTSMiddleware(BaseHTTPMiddleware):
    """Enforce HTTPS with HSTS"""

    def __init__(
        self,
        app,
        max_age: int = 31536000,  # 1 year
        include_subdomains: bool = True,
        preload: bool = False
    ):
        super().__init__(app)
        self.max_age = max_age
        self.include_subdomains = include_subdomains
        self.preload = preload

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Build HSTS header
        value = f"max-age={self.max_age}"

        if self.include_subdomains:
            value += "; includeSubDomains"

        if self.preload:
            value += "; preload"

        response.headers["Strict-Transport-Security"] = value

        return response

# Usage
app.add_middleware(
    HSTSMiddleware,
    max_age=31536000,        # 1 year
    include_subdomains=True,
    preload=True             # Only if submitting to preload list
)
```

### HSTS Deployment Steps

```markdown
## HSTS Rollout Plan

### Phase 1: Testing (max-age: 300)
1. Set short max-age (5 minutes)
2. Monitor for issues
3. Ensure all resources load over HTTPS

### Phase 2: Initial Deployment (max-age: 86400)
1. Increase to 1 day
2. Monitor for user reports
3. Check for mixed content

### Phase 3: Standard Deployment (max-age: 31536000)
1. Increase to 1 year
2. Add includeSubDomains if all subdomains support HTTPS

### Phase 4: Preload (optional)
1. Verify all requirements met
2. Add preload directive
3. Submit to hstspreload.org
```

## Cross-Origin Headers

### CORS Configuration

```python
from starlette.middleware.cors import CORSMiddleware

# Strict CORS for API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
    max_age=3600,  # Preflight cache time
)

# Custom CORS middleware for fine-grained control
class CustomCORSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.allowed_origins = {
            "https://app.example.com",
            "https://admin.example.com",
        }

    async def dispatch(self, request, call_next):
        origin = request.headers.get("origin")

        # Handle preflight
        if request.method == "OPTIONS":
            if origin in self.allowed_origins:
                return Response(
                    status_code=204,
                    headers={
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
                        "Access-Control-Allow-Headers": "Authorization, Content-Type",
                        "Access-Control-Allow-Credentials": "true",
                        "Access-Control-Max-Age": "3600",
                    }
                )
            return Response(status_code=403)

        response = await call_next(request)

        # Add CORS headers to response
        if origin in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response
```

### Cross-Origin Isolation

```python
# Enable cross-origin isolation for SharedArrayBuffer, etc.
class CrossOriginIsolationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Required for SharedArrayBuffer and high-resolution timers
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"

        return response
```

## Additional Security Headers

### Complete Security Headers Middleware

```python
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Comprehensive security headers"""

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # XSS protection (legacy browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # DNS prefetch control
        response.headers["X-DNS-Prefetch-Control"] = "off"

        # Disable browser features
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )

        # Remove server identification
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### Permissions-Policy (Feature-Policy)

```python
PERMISSIONS_POLICY = {
    # Completely disable
    "accelerometer": "()",
    "ambient-light-sensor": "()",
    "autoplay": "()",
    "camera": "()",
    "encrypted-media": "()",
    "fullscreen": "()",
    "geolocation": "()",
    "gyroscope": "()",
    "magnetometer": "()",
    "microphone": "()",
    "midi": "()",
    "payment": "()",
    "picture-in-picture": "()",
    "usb": "()",
    "vr": "()",

    # Allow for self only
    # "camera": "(self)",

    # Allow for specific origins
    # "payment": "(self https://payments.example.com)",
}

def build_permissions_policy() -> str:
    return ", ".join(
        f"{feature}={value}"
        for feature, value in PERMISSIONS_POLICY.items()
    )
```

## Server Configuration

### Nginx Configuration

```nginx
# /etc/nginx/conf.d/security-headers.conf

# HSTS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Prevent clickjacking
add_header X-Frame-Options "DENY" always;

# Prevent MIME sniffing
add_header X-Content-Type-Options "nosniff" always;

# Referrer policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# CSP (adjust for your needs)
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'" always;

# Permissions policy
add_header Permissions-Policy "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()" always;

# Remove server header
server_tokens off;

# Hide nginx version
more_clear_headers Server;
```

### Apache Configuration

```apache
# .htaccess or httpd.conf

# HSTS
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

# Prevent clickjacking
Header always set X-Frame-Options "DENY"

# Prevent MIME sniffing
Header always set X-Content-Type-Options "nosniff"

# Referrer policy
Header always set Referrer-Policy "strict-origin-when-cross-origin"

# CSP
Header always set Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"

# Permissions policy
Header always set Permissions-Policy "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"

# Remove server header
ServerTokens Prod
ServerSignature Off
Header unset Server
```

### CloudFlare/CDN Configuration

```javascript
// CloudFlare Worker for security headers
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const response = await fetch(request)
  const newResponse = new Response(response.body, response)

  // Add security headers
  newResponse.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload')
  newResponse.headers.set('X-Frame-Options', 'DENY')
  newResponse.headers.set('X-Content-Type-Options', 'nosniff')
  newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  newResponse.headers.set('Permissions-Policy', 'accelerometer=(), camera=(), geolocation=()')

  // Remove identifying headers
  newResponse.headers.delete('Server')
  newResponse.headers.delete('X-Powered-By')

  return newResponse
}
```

## Testing and Validation

### Header Testing Tools

```bash
# Using curl
curl -I https://example.com

# Using httpie
http --headers https://example.com

# Using security-headers.com API
curl "https://securityheaders.com/?q=example.com&followRedirects=on"
```

### Automated Testing

```python
import pytest
import httpx

class TestSecurityHeaders:
    """Test security headers are properly configured"""

    @pytest.fixture
    def client(self):
        return httpx.Client(base_url="https://example.com")

    def test_hsts_header(self, client):
        response = client.get("/")
        hsts = response.headers.get("Strict-Transport-Security")

        assert hsts is not None
        assert "max-age=" in hsts
        assert int(hsts.split("max-age=")[1].split(";")[0]) >= 31536000

    def test_csp_header(self, client):
        response = client.get("/")
        csp = response.headers.get("Content-Security-Policy")

        assert csp is not None
        assert "default-src" in csp
        assert "'unsafe-eval'" not in csp

    def test_x_frame_options(self, client):
        response = client.get("/")
        xfo = response.headers.get("X-Frame-Options")

        assert xfo in ["DENY", "SAMEORIGIN"]

    def test_x_content_type_options(self, client):
        response = client.get("/")

        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    def test_referrer_policy(self, client):
        response = client.get("/")
        rp = response.headers.get("Referrer-Policy")

        safe_policies = [
            "no-referrer",
            "strict-origin",
            "strict-origin-when-cross-origin"
        ]
        assert rp in safe_policies

    def test_no_server_header(self, client):
        response = client.get("/")

        # Server header should be removed or generic
        server = response.headers.get("Server", "")
        assert "nginx" not in server.lower()
        assert "apache" not in server.lower()
```

## Common Mistakes

### Anti-Patterns

```python
# BAD: Overly permissive CSP
"default-src *; script-src * 'unsafe-inline' 'unsafe-eval'"

# BAD: No HSTS on HTTPS site
# (Missing Strict-Transport-Security header)

# BAD: Allowing all origins in CORS
"Access-Control-Allow-Origin: *"  # With credentials!

# BAD: Short HSTS max-age
"max-age=300"  # Only 5 minutes

# BAD: X-Frame-Options with ALLOW-FROM (deprecated)
"X-Frame-Options: ALLOW-FROM https://example.com"
# Use CSP frame-ancestors instead
```

## Security Checklist

### Headers Audit
- [ ] HSTS enabled with max-age >= 1 year
- [ ] CSP configured and enforced
- [ ] X-Frame-Options set to DENY
- [ ] X-Content-Type-Options set to nosniff
- [ ] Referrer-Policy configured
- [ ] Permissions-Policy restricts unused features
- [ ] Server header removed/generic
- [ ] CORS properly restricted
- [ ] No unsafe-inline/unsafe-eval in CSP
- [ ] CSP reporting enabled

## Summary

Effective security headers require:

1. **Defense in depth**: Multiple headers for layered protection
2. **Strict defaults**: Start restrictive, loosen if needed
3. **Testing**: Validate headers in CI/CD
4. **Monitoring**: Track CSP violations
5. **Gradual rollout**: Use report-only mode first


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

