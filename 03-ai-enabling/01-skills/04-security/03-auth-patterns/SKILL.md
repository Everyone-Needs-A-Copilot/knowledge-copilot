---
last_updated: 2026-02-25
status: active
name: auth-patterns
description: Authentication patterns - JWT, OAuth 2.0, session management, MFA. Use when implementing auth.
triggers:
  files: ["**/auth/**", "**/login.*", "**/jwt.*", "**/oauth.*", "**/session.*"]
  keywords: ["JWT", "OAuth", "session", "authentication", "authorization", "token", "refresh token", "MFA", "SSO", "OIDC"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Authentication Patterns: Deep Expertise Skill

This skill provides comprehensive guidance on implementing secure authentication and authorization systems. Use this knowledge when building login systems, token-based auth, OAuth flows, session management, or multi-factor authentication.

## Overview

**When to use this skill:**
- Implementing user authentication (login/logout)
- Designing token-based authentication (JWT)
- Integrating OAuth 2.0 or OpenID Connect
- Building session management systems
- Adding multi-factor authentication (MFA)
- Implementing single sign-on (SSO)
- Reviewing authentication code for security

**Core Principle:** Authentication verifies *who* you are (identity), while authorization determines *what* you can do (permissions). Never confuse the two. Always use defense in depth—layer multiple security controls.

---


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## 1. Authentication vs Authorization

### Key Distinction

```python
# Authentication: WHO are you?
def authenticate(email: str, password: str) -> Optional[User]:
    """Verify user identity"""
    user = get_user_by_email(email)
    if user and verify_password(password, user.password_hash):
        return user
    return None

# Authorization: WHAT can you do?
def authorize(user: User, resource: str, action: str) -> bool:
    """Check if user has permission"""
    return user.has_permission(resource, action)

# Usage in API endpoint
@app.get("/api/documents/{doc_id}")
async def get_document(
    doc_id: UUID,
    current_user: User = Depends(get_current_user)  # Authentication
):
    # Authorization check
    if not authorize(current_user, f"document:{doc_id}", "read"):
        raise HTTPException(403, "Forbidden")

    return get_document_by_id(doc_id)
```

### Authentication Factors

**Something you know** - Password, PIN, security question
**Something you have** - Phone, hardware token, smart card
**Something you are** - Biometrics (fingerprint, face, voice)

**Multi-factor authentication (MFA)** combines at least two factors.

---

## 2. Password Authentication

### Secure Password Storage

**NEVER store plaintext passwords.** Always use strong hashing algorithms.

```python
from passlib.context import CryptContext
import secrets

# Use Argon2id (best), bcrypt, or scrypt
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

class User(Base):
    """User model with secure password handling"""
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def set_password(self, password: str):
        """Hash and store password"""
        # Argon2 automatically generates unique salt per password
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        # Constant-time comparison prevents timing attacks
        return pwd_context.verify(password, self.password_hash)

    def needs_password_rehash(self) -> bool:
        """Check if hash needs upgrade (algorithm changed)"""
        return pwd_context.needs_update(self.password_hash)

# Registration endpoint
@app.post("/auth/register")
async def register(
    email: str,
    password: str,
    session: AsyncSession = Depends(get_session)
):
    """Register new user with secure password storage"""

    # Validate password strength
    if not is_password_strong(password):
        raise HTTPException(
            400,
            "Password must be at least 12 characters with uppercase, "
            "lowercase, digit, and special character"
        )

    # Check if user exists
    result = await session.execute(
        select(User).where(User.email == email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(400, "Email already registered")

    # Create user
    user = User(email=email)
    user.set_password(password)
    session.add(user)
    await session.commit()

    return {"message": "User created successfully"}
```

### Password Strength Validation

```python
import re
from typing import List, Tuple

def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
    """
    Validate password meets security requirements.

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Length requirement
    if len(password) < 12:
        errors.append("Password must be at least 12 characters")

    # Character type requirements
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain uppercase letter")

    if not re.search(r'[a-z]', password):
        errors.append("Password must contain lowercase letter")

    if not re.search(r'\d', password):
        errors.append("Password must contain digit")

    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password):
        errors.append("Password must contain special character")

    # Common password check (check against known breached passwords)
    if password.lower() in COMMON_PASSWORDS:
        errors.append("Password is too common")

    return (len(errors) == 0, errors)

# Use in registration
class RegisterRequest(BaseModel):
    email: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        is_valid, errors = validate_password_strength(v)
        if not is_valid:
            raise ValueError("; ".join(errors))
        return v
```

### Password Reset Flow

**Secure password reset process:**

1. User requests reset (provides email)
2. Generate secure token, store with expiration
3. Send token via email (time-limited link)
4. User clicks link, provides new password
5. Verify token, update password, invalidate token

```python
import secrets
from datetime import datetime, timedelta

class PasswordResetToken(Base):
    """Password reset token model"""
    __tablename__ = "password_reset_tokens"

    token = Column(String, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    user = relationship("User")

async def request_password_reset(
    email: str,
    session: AsyncSession
) -> None:
    """Initiate password reset"""

    # Find user
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        # Don't reveal if email exists (prevents enumeration)
        logger.info("password_reset_requested_nonexistent", email=email)
        return  # Still return success to user

    # Generate cryptographically secure token
    token = secrets.token_urlsafe(32)

    # Store token with 1-hour expiration
    reset_token = PasswordResetToken(
        token=token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    session.add(reset_token)
    await session.commit()

    # Send email (don't expose token in logs)
    reset_url = f"https://app.example.com/reset-password?token={token}"
    await send_email(
        to=user.email,
        subject="Password Reset Request",
        body=f"Click here to reset: {reset_url}"
    )

    logger.info("password_reset_sent", user_id=str(user.id))

@app.post("/auth/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    session: AsyncSession = Depends(get_session)
):
    """Reset password with token"""

    # Validate password strength
    is_valid, errors = validate_password_strength(new_password)
    if not is_valid:
        raise HTTPException(400, "; ".join(errors))

    # Find token
    result = await session.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token == token
        )
    )
    reset_token = result.scalar_one_or_none()

    if not reset_token:
        raise HTTPException(400, "Invalid or expired token")

    # Check expiration
    if reset_token.expires_at < datetime.utcnow():
        raise HTTPException(400, "Token expired")

    # Check if already used
    if reset_token.used:
        raise HTTPException(400, "Token already used")

    # Update password
    user = reset_token.user
    user.set_password(new_password)

    # Mark token as used
    reset_token.used = True

    await session.commit()

    # Invalidate all existing sessions for this user
    await invalidate_user_sessions(user.id)

    logger.info("password_reset_complete", user_id=str(user.id))

    return {"message": "Password reset successful"}
```

---

## 3. JSON Web Tokens (JWT)

### JWT Structure

JWTs consist of three Base64-encoded parts separated by dots:

```
header.payload.signature
```

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload (Claims):**
```json
{
  "sub": "user-id-123",
  "email": "user@example.com",
  "exp": 1735689600,
  "iat": 1735686000,
  "jti": "unique-token-id"
}
```

**Signature:**
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

### JWT Implementation

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # NEVER hardcode!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

class TokenPayload(BaseModel):
    """JWT payload structure"""
    sub: str  # Subject (user ID)
    email: str
    exp: datetime  # Expiration
    iat: datetime  # Issued at
    jti: str  # JWT ID (unique token ID)
    type: str  # "access" or "refresh"

def create_access_token(user: User) -> str:
    """Create JWT access token"""
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": expires_at,
        "iat": datetime.utcnow(),
        "jti": secrets.token_urlsafe(16),
        "type": "access"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token(user: User) -> str:
    """Create JWT refresh token (longer lived)"""
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": str(user.id),
        "exp": expires_at,
        "iat": datetime.utcnow(),
        "jti": secrets.token_urlsafe(16),
        "type": "refresh"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str) -> TokenPayload:
    """
    Verify and decode JWT token.

    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Validate token type
        if payload.get("type") != "access":
            raise credentials_exception

        # Validate required fields
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        return TokenPayload(**payload)

    except JWTError:
        raise credentials_exception
    except ValidationError:
        raise credentials_exception
```

### Token Endpoint

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@app.post("/auth/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> dict:
    """
    OAuth2 compatible token endpoint.

    Returns access_token and refresh_token.
    """

    # Authenticate user
    result = await session.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create tokens
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    # Log successful login
    logger.info("user_login", user_id=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dependency to get authenticated user from JWT.

    Use in endpoints: current_user: User = Depends(get_current_user)
    """

    # Verify token
    payload = verify_access_token(token)

    # Get user from database
    result = await session.execute(
        select(User).where(User.id == UUID(payload.sub))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(401, "User not found")

    return user

# Protected endpoint example
@app.get("/api/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user profile (requires authentication)"""
    return UserResponse.from_orm(current_user)
```

### Refresh Token Flow

```python
@app.post("/auth/refresh")
async def refresh_access_token(
    refresh_token: str,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Get new access token using refresh token.

    Implements refresh token rotation for security.
    """

    try:
        # Decode refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        # Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")

        # Check if token is revoked (if using token blacklist)
        token_id = payload.get("jti")
        if await is_token_revoked(token_id):
            raise HTTPException(401, "Token revoked")

        # Get user
        result = await session.execute(
            select(User).where(User.id == UUID(user_id))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(401, "User not found")

        # Create new access token
        new_access_token = create_access_token(user)

        # Rotate refresh token (optional but recommended)
        new_refresh_token = create_refresh_token(user)

        # Revoke old refresh token
        await revoke_token(token_id)

        logger.info("token_refreshed", user_id=str(user.id))

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    except JWTError:
        raise HTTPException(401, "Invalid refresh token")
```

### JWT Best Practices

**✅ DO:**
- Use strong secret keys (256-bit minimum)
- Set short expiration times (15-30 minutes for access tokens)
- Use refresh tokens for longer sessions
- Include `jti` claim for token revocation
- Validate all claims on verification
- Use HTTPS only
- Store tokens in httpOnly cookies (web) or secure storage (mobile)

**❌ DON'T:**
- Store sensitive data in JWT payload (it's Base64, not encrypted)
- Use JWT for sessions if you need immediate revocation
- Share secret keys across environments
- Store JWTs in localStorage (XSS vulnerable)
- Use weak algorithms (none, HS256 with weak secret)
- Forget to validate expiration

---

## 4. OAuth 2.0

### OAuth 2.0 Flow Types

**Authorization Code Flow** - Most secure, for web apps with backend
**Authorization Code + PKCE** - For mobile/SPA (no client secret)
**Client Credentials** - For server-to-server
**Implicit Flow** - DEPRECATED (insecure)
**Resource Owner Password** - For trusted first-party apps only

### Authorization Code Flow

**Best for:** Web applications with backend server

```
User -> Client App -> Authorization Server -> Client App -> Resource Server
```

**Steps:**

1. **Authorization Request**
   ```
   GET https://auth.example.com/authorize?
     response_type=code&
     client_id=abc123&
     redirect_uri=https://app.example.com/callback&
     scope=openid profile email&
     state=random-state-string
   ```

2. **User Authenticates & Consents**

3. **Authorization Server Redirects with Code**
   ```
   GET https://app.example.com/callback?
     code=AUTH_CODE_HERE&
     state=random-state-string
   ```

4. **Exchange Code for Token**
   ```
   POST https://auth.example.com/token
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code&
   code=AUTH_CODE_HERE&
   redirect_uri=https://app.example.com/callback&
   client_id=abc123&
   client_secret=SECRET
   ```

5. **Receive Tokens**
   ```json
   {
     "access_token": "ACCESS_TOKEN",
     "refresh_token": "REFRESH_TOKEN",
     "token_type": "Bearer",
     "expires_in": 3600,
     "id_token": "ID_TOKEN"
   }
   ```

### Implementing OAuth 2.0 Client

```python
import httpx
from urllib.parse import urlencode
import secrets

class OAuth2Config:
    """OAuth 2.0 configuration"""
    authorization_url = "https://auth.example.com/authorize"
    token_url = "https://auth.example.com/token"
    client_id = os.getenv("OAUTH_CLIENT_ID")
    client_secret = os.getenv("OAUTH_CLIENT_SECRET")
    redirect_uri = "https://app.example.com/auth/callback"
    scopes = ["openid", "profile", "email"]

class OAuth2Client:
    """OAuth 2.0 client implementation"""

    def __init__(self, config: OAuth2Config):
        self.config = config

    def get_authorization_url(self) -> tuple[str, str]:
        """
        Generate authorization URL with state.

        Returns:
            Tuple of (authorization_url, state)
        """
        # Generate random state for CSRF protection
        state = secrets.token_urlsafe(32)

        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": " ".join(self.config.scopes),
            "state": state
        }

        url = f"{self.config.authorization_url}?{urlencode(params)}"
        return url, state

    async def exchange_code_for_token(
        self,
        code: str,
        state: str,
        stored_state: str
    ) -> dict:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from callback
            state: State from callback
            stored_state: State stored in session

        Returns:
            Token response with access_token and refresh_token

        Raises:
            HTTPException: If state doesn't match or exchange fails
        """

        # Validate state (CSRF protection)
        if state != stored_state:
            raise HTTPException(400, "Invalid state parameter")

        # Exchange code for token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config.token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.config.redirect_uri,
                    "client_id": self.config.client_id,
                    "client_secret": self.config.client_secret
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )

            if response.status_code != 200:
                logger.error("oauth_token_exchange_failed",
                           status=response.status_code,
                           body=response.text)
                raise HTTPException(500, "Failed to exchange authorization code")

            return response.json()

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token"""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config.token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self.config.client_id,
                    "client_secret": self.config.client_secret
                }
            )

            if response.status_code != 200:
                raise HTTPException(401, "Failed to refresh token")

            return response.json()

    async def get_user_info(self, access_token: str) -> dict:
        """Get user info from authorization server"""

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://auth.example.com/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code != 200:
                raise HTTPException(401, "Failed to get user info")

            return response.json()

# OAuth 2.0 endpoints
oauth2_client = OAuth2Client(OAuth2Config())

@app.get("/auth/login")
async def oauth_login(request: Request):
    """Initiate OAuth 2.0 login"""

    # Generate authorization URL
    auth_url, state = oauth2_client.get_authorization_url()

    # Store state in session
    request.session["oauth_state"] = state

    # Redirect to authorization server
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
async def oauth_callback(
    request: Request,
    code: str,
    state: str,
    session: AsyncSession = Depends(get_session)
):
    """OAuth 2.0 callback endpoint"""

    # Get stored state
    stored_state = request.session.get("oauth_state")

    # Exchange code for token
    token_response = await oauth2_client.exchange_code_for_token(
        code, state, stored_state
    )

    # Get user info
    user_info = await oauth2_client.get_user_info(
        token_response["access_token"]
    )

    # Create or update local user
    result = await session.execute(
        select(User).where(User.email == user_info["email"])
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email=user_info["email"],
            name=user_info.get("name"),
            oauth_provider="google",
            oauth_id=user_info["sub"]
        )
        session.add(user)
        await session.commit()

    # Create session
    access_token = create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

### PKCE (Proof Key for Code Exchange)

**For:** Mobile apps and SPAs without client secret

```python
import hashlib
import base64

def generate_pkce_pair() -> tuple[str, str]:
    """
    Generate PKCE code_verifier and code_challenge.

    Returns:
        Tuple of (code_verifier, code_challenge)
    """
    # Generate code_verifier (43-128 characters)
    code_verifier = secrets.token_urlsafe(64)

    # Generate code_challenge (SHA256 hash of verifier)
    challenge_bytes = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(challenge_bytes).decode().rstrip("=")

    return code_verifier, code_challenge

# In authorization request
code_verifier, code_challenge = generate_pkce_pair()

# Store code_verifier in secure storage
save_to_storage("code_verifier", code_verifier)

# Add to authorization URL
auth_url = f"{auth_url}&code_challenge={code_challenge}&code_challenge_method=S256"

# In token exchange
token_data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "code_verifier": code_verifier  # Prove you initiated the request
}
```

---

## 5. Session Management

### Server-Side Sessions

**Best for:** Traditional web applications, when you need immediate revocation

```python
from datetime import datetime, timedelta
import secrets

class Session(Base):
    """Server-side session model"""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    ip_address = Column(String)
    user_agent = Column(String)

    user = relationship("User")

class SessionManager:
    """Session management service"""

    def __init__(self):
        self.session_timeout = timedelta(minutes=30)  # Inactivity timeout
        self.absolute_timeout = timedelta(hours=12)   # Maximum session length

    async def create_session(
        self,
        user: User,
        ip_address: str,
        user_agent: str,
        session: AsyncSession
    ) -> str:
        """Create new session"""

        # Generate cryptographically secure session ID
        session_id = secrets.token_urlsafe(32)

        # Create session record
        db_session = Session(
            id=session_id,
            user_id=user.id,
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            expires_at=datetime.utcnow() + self.absolute_timeout,
            ip_address=ip_address,
            user_agent=user_agent
        )

        session.add(db_session)
        await session.commit()

        logger.info("session_created",
                   user_id=str(user.id),
                   session_id=session_id)

        return session_id

    async def validate_session(
        self,
        session_id: str,
        session: AsyncSession
    ) -> Optional[User]:
        """
        Validate session and return user.

        Returns None if session invalid or expired.
        """

        # Get session
        result = await session.execute(
            select(Session).where(Session.id == session_id)
        )
        db_session = result.scalar_one_or_none()

        if not db_session:
            return None

        now = datetime.utcnow()

        # Check absolute expiration
        if now > db_session.expires_at:
            await self.delete_session(session_id, session)
            return None

        # Check inactivity timeout
        if now - db_session.last_activity > self.session_timeout:
            await self.delete_session(session_id, session)
            return None

        # Update last activity
        db_session.last_activity = now
        await session.commit()

        return db_session.user

    async def delete_session(
        self,
        session_id: str,
        session: AsyncSession
    ):
        """Delete session (logout)"""

        result = await session.execute(
            select(Session).where(Session.id == session_id)
        )
        db_session = result.scalar_one_or_none()

        if db_session:
            await session.delete(db_session)
            await session.commit()

            logger.info("session_deleted",
                       user_id=str(db_session.user_id),
                       session_id=session_id)

    async def delete_user_sessions(
        self,
        user_id: UUID,
        session: AsyncSession
    ):
        """Delete all sessions for user (logout from all devices)"""

        await session.execute(
            delete(Session).where(Session.user_id == user_id)
        )
        await session.commit()

        logger.info("all_sessions_deleted", user_id=str(user_id))

# Session dependency
session_manager = SessionManager()

async def get_current_user_session(
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Get authenticated user from session cookie.

    Use in endpoints: current_user: User = Depends(get_current_user_session)
    """

    # Get session ID from cookie
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(401, "Not authenticated")

    # Validate session
    user = await session_manager.validate_session(session_id, session)

    if not user:
        raise HTTPException(401, "Session expired")

    return user

# Login endpoint
@app.post("/auth/login")
async def login_session(
    request: Request,
    response: Response,
    email: str,
    password: str,
    db_session: AsyncSession = Depends(get_session)
):
    """Login with session-based authentication"""

    # Authenticate user
    result = await db_session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not user.verify_password(password):
        raise HTTPException(401, "Invalid credentials")

    # Create session
    session_id = await session_manager.create_session(
        user,
        request.client.host,
        request.headers.get("user-agent", ""),
        db_session
    )

    # Set secure cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,      # Prevent JavaScript access (XSS protection)
        secure=True,        # HTTPS only
        samesite="strict",  # CSRF protection
        max_age=43200       # 12 hours
    )

    return {"message": "Login successful"}

# Logout endpoint
@app.post("/auth/logout")
async def logout(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(get_session)
):
    """Logout and delete session"""

    session_id = request.cookies.get("session_id")

    if session_id:
        await session_manager.delete_session(session_id, db_session)

    # Clear cookie
    response.delete_cookie("session_id")

    return {"message": "Logout successful"}
```

### Token Storage Best Practices

**Web Applications:**

```javascript
// ✅ GOOD: httpOnly cookie (set by server)
// Cannot be accessed by JavaScript (XSS protection)
response.set_cookie(
    "access_token",
    token,
    httponly=True,
    secure=True,
    samesite="strict"
)

// ❌ BAD: localStorage (vulnerable to XSS)
localStorage.setItem('access_token', token);

// ❌ BAD: Regular cookie (JavaScript accessible)
document.cookie = `token=${token}`;
```

**Mobile Applications:**

```swift
// ✅ GOOD: Keychain (iOS)
let keychain = KeychainSwift()
keychain.set(accessToken, forKey: "access_token")

// ✅ GOOD: EncryptedSharedPreferences (Android)
val sharedPreferences = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
sharedPreferences.edit().putString("access_token", token).apply()
```

---

## 6. Multi-Factor Authentication (MFA)

### TOTP (Time-Based One-Time Password)

**Most common MFA method** - Uses authenticator app (Google Authenticator, Authy)

```python
import pyotp
import qrcode
from io import BytesIO
import base64

class MFAManager:
    """Multi-factor authentication manager"""

    async def setup_totp(
        self,
        user: User,
        session: AsyncSession
    ) -> dict:
        """
        Set up TOTP for user.

        Returns:
            Dict with secret and QR code for user to scan
        """

        # Generate secret
        secret = pyotp.random_base32()

        # Store encrypted secret
        user.totp_secret = encrypt(secret)  # Use encryption service
        await session.commit()

        # Generate provisioning URI for QR code
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="Your App Name"
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code = base64.b64encode(buffer.getvalue()).decode()

        logger.info("mfa_setup_initiated", user_id=str(user.id))

        return {
            "secret": secret,
            "qr_code": qr_code,
            "provisioning_uri": provisioning_uri
        }

    def verify_totp(
        self,
        user: User,
        token: str
    ) -> bool:
        """
        Verify TOTP token.

        Args:
            user: User with TOTP enabled
            token: 6-digit code from authenticator app

        Returns:
            True if valid, False otherwise
        """

        if not user.totp_secret:
            return False

        # Decrypt secret
        secret = decrypt(user.totp_secret)

        # Verify token (allows ±1 time window for clock skew)
        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(token, valid_window=1)

        if is_valid:
            logger.info("mfa_verification_success", user_id=str(user.id))
        else:
            logger.warning("mfa_verification_failed", user_id=str(user.id))

        return is_valid

    async def disable_totp(
        self,
        user: User,
        session: AsyncSession
    ):
        """Disable TOTP for user"""

        user.totp_secret = None
        await session.commit()

        logger.info("mfa_disabled", user_id=str(user.id))

# MFA endpoints
mfa_manager = MFAManager()

@app.post("/auth/mfa/setup")
async def setup_mfa(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Initialize MFA setup for user"""

    if current_user.totp_secret:
        raise HTTPException(400, "MFA already enabled")

    return await mfa_manager.setup_totp(current_user, session)

@app.post("/auth/mfa/verify")
async def verify_mfa_setup(
    token: str,
    current_user: User = Depends(get_current_user)
) -> dict:
    """Verify MFA setup (confirm user can generate codes)"""

    if not current_user.totp_secret:
        raise HTTPException(400, "MFA not set up")

    is_valid = mfa_manager.verify_totp(current_user, token)

    if not is_valid:
        raise HTTPException(400, "Invalid verification code")

    return {"message": "MFA verified successfully"}

@app.post("/auth/login-mfa")
async def login_with_mfa(
    email: str,
    password: str,
    totp_token: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Login with MFA support"""

    # Authenticate with password
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not user.verify_password(password):
        raise HTTPException(401, "Invalid credentials")

    # Check if MFA required
    if user.totp_secret:
        if not totp_token:
            # Password valid but need MFA
            return {
                "requires_mfa": True,
                "message": "Please provide TOTP code"
            }

        # Verify TOTP
        if not mfa_manager.verify_totp(user, totp_token):
            raise HTTPException(401, "Invalid MFA code")

    # Create token/session
    access_token = create_access_token(user)

    logger.info("user_login_with_mfa", user_id=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

### Backup Codes

Always provide backup codes in case user loses authenticator device.

```python
class BackupCode(Base):
    """MFA backup code"""
    __tablename__ = "mfa_backup_codes"

    code = Column(String, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

async def generate_backup_codes(
    user: User,
    session: AsyncSession,
    count: int = 10
) -> List[str]:
    """Generate backup codes for MFA"""

    codes = []

    for _ in range(count):
        # Generate 8-character alphanumeric code
        code = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                      for _ in range(8))

        # Store hashed version
        hashed = hash_backup_code(code)

        backup_code = BackupCode(
            code=hashed,
            user_id=user.id
        )
        session.add(backup_code)
        codes.append(code)

    await session.commit()

    return codes

async def verify_backup_code(
    user: User,
    code: str,
    session: AsyncSession
) -> bool:
    """Verify and consume backup code"""

    hashed = hash_backup_code(code)

    result = await session.execute(
        select(BackupCode).where(
            BackupCode.user_id == user.id,
            BackupCode.code == hashed,
            BackupCode.used == False
        )
    )
    backup_code = result.scalar_one_or_none()

    if not backup_code:
        return False

    # Mark as used
    backup_code.used = True
    await session.commit()

    logger.info("backup_code_used", user_id=str(user.id))

    return True
```

---

## 7. OpenID Connect (OIDC)

OIDC is an identity layer on top of OAuth 2.0. It adds:
- **ID Token** (JWT with user identity claims)
- **UserInfo endpoint** (get user profile)
- **Standard scopes** (openid, profile, email)

### ID Token Structure

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-id-123",
  "aud": "client-id",
  "exp": 1735689600,
  "iat": 1735686000,
  "nonce": "random-nonce",
  "email": "user@example.com",
  "email_verified": true,
  "name": "John Doe",
  "picture": "https://example.com/avatar.jpg"
}
```

### OIDC Discovery

```python
async def get_oidc_configuration(issuer: str) -> dict:
    """Get OIDC provider configuration"""

    discovery_url = f"{issuer}/.well-known/openid-configuration"

    async with httpx.AsyncClient() as client:
        response = await client.get(discovery_url)

        if response.status_code != 200:
            raise Exception("Failed to get OIDC configuration")

        return response.json()

# Example discovery response
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "userinfo_endpoint": "https://auth.example.com/userinfo",
  "jwks_uri": "https://auth.example.com/.well-known/jwks.json",
  "response_types_supported": ["code", "token", "id_token"],
  "subject_types_supported": ["public"],
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

---

## 8. Single Sign-On (SSO)

### SAML 2.0 Basics

**SAML** (Security Assertion Markup Language) - XML-based SSO standard

**Key Concepts:**
- **Service Provider (SP)** - Your application
- **Identity Provider (IdP)** - Authentication server (Okta, Azure AD)
- **SAML Assertion** - XML document with authentication statement

**Flow:**

1. User accesses SP (your app)
2. SP redirects to IdP with SAML Request
3. User authenticates at IdP
4. IdP redirects back with SAML Response
5. SP validates response and creates session

```python
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings

def init_saml_auth(request):
    """Initialize SAML authentication"""

    saml_settings = {
        "strict": True,
        "debug": False,
        "sp": {
            "entityId": "https://app.example.com/saml/metadata",
            "assertionConsumerService": {
                "url": "https://app.example.com/saml/acs",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "singleLogoutService": {
                "url": "https://app.example.com/saml/sls",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "x509cert": SP_CERTIFICATE,
            "privateKey": SP_PRIVATE_KEY
        },
        "idp": {
            "entityId": "https://idp.example.com",
            "singleSignOnService": {
                "url": "https://idp.example.com/sso",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "singleLogoutService": {
                "url": "https://idp.example.com/slo",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "x509cert": IDP_CERTIFICATE
        }
    }

    return OneLogin_Saml2_Auth(request, saml_settings)

@app.get("/saml/login")
async def saml_login(request: Request):
    """Initiate SAML SSO"""

    auth = init_saml_auth(prepare_request(request))
    return RedirectResponse(auth.login())

@app.post("/saml/acs")
async def saml_acs(request: Request, session: AsyncSession = Depends(get_session)):
    """SAML Assertion Consumer Service - handles IdP response"""

    auth = init_saml_auth(prepare_request(request))
    auth.process_response()

    errors = auth.get_errors()
    if errors:
        logger.error("saml_auth_failed", errors=errors)
        raise HTTPException(401, "SAML authentication failed")

    if not auth.is_authenticated():
        raise HTTPException(401, "Not authenticated")

    # Get user attributes
    attributes = auth.get_attributes()
    name_id = auth.get_nameid()

    # Create or update user
    email = attributes.get('email', [name_id])[0]
    user = await get_or_create_user(email, attributes, session)

    # Create session
    access_token = create_access_token(user)

    return {"access_token": access_token}
```

---

## 9. Rate Limiting & Brute Force Protection

### Login Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta

class LoginRateLimiter:
    """Rate limit login attempts"""

    def __init__(self):
        self.attempts = defaultdict(list)  # email -> [timestamp, ...]
        self.blocked = {}  # email -> unblock_time

        # Configuration
        self.max_attempts = 5
        self.window_minutes = 15
        self.block_duration = timedelta(minutes=30)

    def check_rate_limit(self, identifier: str) -> tuple[bool, Optional[int]]:
        """
        Check if identifier is rate limited.

        Args:
            identifier: Email, IP, or combination

        Returns:
            Tuple of (is_allowed, seconds_until_unblock)
        """

        # Check if blocked
        if identifier in self.blocked:
            unblock_time = self.blocked[identifier]
            if datetime.utcnow() < unblock_time:
                seconds_left = (unblock_time - datetime.utcnow()).seconds
                return False, seconds_left
            else:
                # Unblock
                del self.blocked[identifier]

        # Clean old attempts
        cutoff = datetime.utcnow() - timedelta(minutes=self.window_minutes)
        self.attempts[identifier] = [
            t for t in self.attempts[identifier]
            if t > cutoff
        ]

        # Check rate
        if len(self.attempts[identifier]) >= self.max_attempts:
            # Block
            self.blocked[identifier] = datetime.utcnow() + self.block_duration
            logger.warning("login_rate_limit_triggered", identifier=identifier)
            return False, self.block_duration.seconds

        return True, None

    def record_attempt(self, identifier: str):
        """Record login attempt"""
        self.attempts[identifier].append(datetime.utcnow())

rate_limiter = LoginRateLimiter()

@app.post("/auth/login")
async def login_with_rate_limit(
    request: Request,
    email: str,
    password: str,
    session: AsyncSession = Depends(get_session)
):
    """Login with rate limiting"""

    # Rate limit by email AND IP
    email_key = f"email:{email}"
    ip_key = f"ip:{request.client.host}"

    # Check email-based rate limit
    allowed, wait_seconds = rate_limiter.check_rate_limit(email_key)
    if not allowed:
        raise HTTPException(
            429,
            f"Too many login attempts. Try again in {wait_seconds} seconds."
        )

    # Check IP-based rate limit
    allowed, wait_seconds = rate_limiter.check_rate_limit(ip_key)
    if not allowed:
        raise HTTPException(
            429,
            f"Too many login attempts from this IP. Try again in {wait_seconds} seconds."
        )

    # Attempt authentication
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not user.verify_password(password):
        # Record failed attempt
        rate_limiter.record_attempt(email_key)
        rate_limiter.record_attempt(ip_key)

        raise HTTPException(401, "Invalid credentials")

    # Success - create token
    access_token = create_access_token(user)

    return {"access_token": access_token}
```

### Account Lockout

```python
class User(Base):
    """User model with lockout support"""
    # ... other fields ...

    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    def is_locked(self) -> bool:
        """Check if account is locked"""
        if self.locked_until:
            if datetime.utcnow() < self.locked_until:
                return True
            else:
                # Unlock
                self.locked_until = None
                self.failed_login_attempts = 0
        return False

    def record_failed_login(self):
        """Record failed login attempt"""
        self.failed_login_attempts += 1

        # Lock after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(hours=1)

    def record_successful_login(self):
        """Reset failed attempts on successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None

@app.post("/auth/login")
async def login_with_lockout(
    email: str,
    password: str,
    session: AsyncSession = Depends(get_session)
):
    """Login with account lockout"""

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        # Don't reveal if user exists
        raise HTTPException(401, "Invalid credentials")

    # Check if locked
    if user.is_locked():
        logger.warning("login_attempt_locked_account",
                      user_id=str(user.id))
        raise HTTPException(
            403,
            "Account locked due to too many failed attempts. "
            "Try again later or contact support."
        )

    # Verify password
    if not user.verify_password(password):
        user.record_failed_login()
        await session.commit()

        logger.warning("failed_login_attempt",
                      user_id=str(user.id),
                      attempts=user.failed_login_attempts)

        raise HTTPException(401, "Invalid credentials")

    # Success
    user.record_successful_login()
    await session.commit()

    access_token = create_access_token(user)

    logger.info("successful_login", user_id=str(user.id))

    return {"access_token": access_token}
```

---

## 10. Anti-Patterns & Common Mistakes

### ❌ Storing Passwords in Plain Text

```python
# NEVER DO THIS
class User:
    password = Column(String)  # Plain text - DISASTER!

# ALWAYS hash passwords
class User:
    password_hash = Column(String)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
```

### ❌ Weak JWT Secrets

```python
# BAD: Weak secret
SECRET_KEY = "secret123"

# GOOD: Strong random secret
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Generate with: secrets.token_urlsafe(64)
```

### ❌ Storing Tokens in localStorage

```javascript
// BAD: XSS vulnerable
localStorage.setItem('token', accessToken);

// GOOD: httpOnly cookie (set by server)
// Can't be accessed by JavaScript
```

### ❌ Not Validating Token Expiration

```python
# BAD: Trust token without checking expiration
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
user_id = payload["sub"]  # What if token expired?

# GOOD: jwt.decode() automatically validates expiration
# It raises JWTError if expired
```

### ❌ No CSRF Protection

```python
# BAD: Accept state-changing request without CSRF token
@app.post("/api/change-email")
async def change_email(new_email: str):
    # Anyone can trigger this!
    pass

# GOOD: Require CSRF token or SameSite cookies
@app.post("/api/change-email")
async def change_email(
    new_email: str,
    csrf_token: str = Header(None, alias="X-CSRF-Token")
):
    verify_csrf_token(csrf_token)
    # Safe
```

### ❌ Revealing User Existence

```python
# BAD: Different messages reveal if user exists
if not user:
    raise HTTPException(404, "User not found")
if not verify_password(password, user.password_hash):
    raise HTTPException(401, "Incorrect password")

# GOOD: Generic message
if not user or not verify_password(password, user.password_hash):
    raise HTTPException(401, "Invalid credentials")
```

### ❌ Missing Rate Limiting

```python
# BAD: No protection against brute force
@app.post("/auth/login")
async def login(email: str, password: str):
    # Attacker can try millions of passwords
    pass

# GOOD: Rate limit login attempts
@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(email: str, password: str):
    # Limited to 5 attempts per minute
    pass
```

---

## 11. Security Checklist

When implementing authentication:

### Password Security
- [ ] Passwords hashed with Argon2id, bcrypt, or scrypt
- [ ] Minimum 12 characters required
- [ ] Password strength validation (upper, lower, digit, special)
- [ ] Check against known breached passwords
- [ ] Secure password reset with time-limited tokens

### Token Security
- [ ] JWT secrets are strong (256-bit minimum)
- [ ] Tokens have short expiration (15-30 min for access)
- [ ] Refresh tokens implemented for longer sessions
- [ ] Token revocation mechanism (if needed)
- [ ] Tokens stored securely (httpOnly cookies or secure storage)

### Session Security
- [ ] Cryptographically random session IDs
- [ ] Session timeout implemented
- [ ] Session invalidation on logout
- [ ] Concurrent session limits (optional)

### OAuth/OIDC
- [ ] State parameter used (CSRF protection)
- [ ] PKCE used for mobile/SPA
- [ ] Redirect URI validation
- [ ] Token exchange over HTTPS only

### MFA
- [ ] TOTP implementation with ±1 time window
- [ ] Backup codes provided
- [ ] MFA required for sensitive operations

### Rate Limiting
- [ ] Login endpoints rate limited
- [ ] Account lockout after N failed attempts
- [ ] IP-based rate limiting
- [ ] CAPTCHA for suspicious activity

### General
- [ ] HTTPS enforced in production
- [ ] CSRF protection for state-changing operations
- [ ] Secure cookies (httpOnly, secure, SameSite)
- [ ] No sensitive data in logs
- [ ] Failed login attempts logged
- [ ] Security headers configured

---

## 12. Testing Authentication

```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_successful_login(client: TestClient, test_user: User):
    """Test successful login flow"""

    response = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "Password123!"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""

    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrong"
    })

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_jwt_expiration(client: TestClient):
    """Test JWT expiration"""

    # Create token with 1-second expiration
    token = create_access_token(test_user, expires_delta=timedelta(seconds=1))

    # Wait for expiration
    await asyncio.sleep(2)

    # Try to use expired token
    response = client.get(
        "/api/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_mfa_flow(client: TestClient, test_user: User):
    """Test MFA login flow"""

    # Setup MFA
    setup_response = client.post(
        "/auth/mfa/setup",
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    secret = setup_response.json()["secret"]

    # Generate TOTP code
    totp = pyotp.TOTP(secret)
    code = totp.now()

    # Login with MFA
    login_response = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "Password123!",
        "totp_token": code
    })

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

@pytest.mark.asyncio
async def test_rate_limiting(client: TestClient):
    """Test login rate limiting"""

    # Make multiple failed attempts
    for i in range(10):
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "wrong"
        })

        if response.status_code == 429:
            break

    # Should eventually be rate limited
    assert response.status_code == 429
```

---

## Summary: Authentication Best Practices

1. **Always hash passwords** - Use Argon2id, bcrypt, or scrypt
2. **Use strong secrets** - Generate with `secrets.token_urlsafe(64)`
3. **Short token expiration** - 15-30 minutes for access tokens
4. **Implement refresh tokens** - For longer sessions without re-authentication
5. **Store tokens securely** - httpOnly cookies for web, secure storage for mobile
6. **Use HTTPS everywhere** - No exceptions in production
7. **Implement rate limiting** - Protect against brute force attacks
8. **Add MFA for sensitive accounts** - TOTP is standard
9. **Log security events** - Failed logins, lockouts, MFA changes
10. **Validate everything** - Never trust client input

**Golden Rule:** Assume every request is malicious until proven otherwise. Layer multiple security controls (defense in depth) and always fail secure (deny access on error).

When implementing authentication, security is not optional—it's foundational. Follow these patterns to build robust, secure authentication systems.


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

