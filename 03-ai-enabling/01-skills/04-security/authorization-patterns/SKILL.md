---
last_updated: 2026-02-25
status: active
name: authorization-patterns
description: Access control patterns, RBAC, ABAC, permissions, and authorization best practices. Use when implementing or reviewing authorization systems.
triggers:
  files: ["**/auth/**", "**/permissions/**", "**/roles/**", "**/access/**", "**/policy/**", "**/*authz*"]
  keywords: ["authorization", "permission", "role", "RBAC", "ABAC", "access control", "ACL", "policy", "privilege", "scope", "grant", "deny"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Authorization Patterns Deep Expertise

This skill provides comprehensive guidance for implementing secure authorization systems. Apply this knowledge when building access control, implementing permissions, or reviewing authorization code.

## Authorization Fundamentals

### Authentication vs Authorization

| Aspect | Authentication | Authorization |
|--------|---------------|---------------|
| Question | "Who are you?" | "What can you do?" |
| When | Login time | Every request |
| Outcome | Identity established | Access granted/denied |

### Authorization Models

| Model | Best For | Complexity |
|-------|----------|------------|
| ACL | Simple file/resource permissions | Low |
| RBAC | Enterprise applications | Medium |
| ABAC | Complex, dynamic policies | High |
| ReBAC | Social/relationship-based | Medium-High |


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Role-Based Access Control (RBAC)

### RBAC Implementation

```python
from enum import Enum
from typing import Set
from functools import wraps

class Permission(str, Enum):
    # Resource: Action pattern
    USERS_READ = "users:read"
    USERS_WRITE = "users:write"
    USERS_DELETE = "users:delete"
    POSTS_READ = "posts:read"
    POSTS_WRITE = "posts:write"
    POSTS_DELETE = "posts:delete"
    ADMIN_PANEL = "admin:access"
    REPORTS_VIEW = "reports:view"
    SETTINGS_MANAGE = "settings:manage"

class Role(str, Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

# Role to permissions mapping
ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.VIEWER: {
        Permission.USERS_READ,
        Permission.POSTS_READ,
    },
    Role.EDITOR: {
        Permission.USERS_READ,
        Permission.POSTS_READ,
        Permission.POSTS_WRITE,
    },
    Role.MODERATOR: {
        Permission.USERS_READ,
        Permission.POSTS_READ,
        Permission.POSTS_WRITE,
        Permission.POSTS_DELETE,
    },
    Role.ADMIN: {
        Permission.USERS_READ,
        Permission.USERS_WRITE,
        Permission.POSTS_READ,
        Permission.POSTS_WRITE,
        Permission.POSTS_DELETE,
        Permission.ADMIN_PANEL,
        Permission.REPORTS_VIEW,
    },
    Role.SUPER_ADMIN: set(Permission),  # All permissions
}

class RBACManager:
    def __init__(self):
        self.role_permissions = ROLE_PERMISSIONS
        self.user_roles: dict[str, Set[Role]] = {}

    def assign_role(self, user_id: str, role: Role):
        """Assign role to user"""
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        self.user_roles[user_id].add(role)

    def remove_role(self, user_id: str, role: Role):
        """Remove role from user"""
        if user_id in self.user_roles:
            self.user_roles[user_id].discard(role)

    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get all permissions for a user"""
        permissions = set()
        for role in self.user_roles.get(user_id, set()):
            permissions.update(self.role_permissions.get(role, set()))
        return permissions

    def has_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has specific permission"""
        return permission in self.get_user_permissions(user_id)

    def has_any_permission(self, user_id: str, permissions: Set[Permission]) -> bool:
        """Check if user has any of the permissions"""
        user_perms = self.get_user_permissions(user_id)
        return bool(user_perms & permissions)

    def has_all_permissions(self, user_id: str, permissions: Set[Permission]) -> bool:
        """Check if user has all permissions"""
        user_perms = self.get_user_permissions(user_id)
        return permissions.issubset(user_perms)

rbac = RBACManager()

# FastAPI decorator for permission checking
def require_permission(permission: Permission):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not rbac.has_permission(current_user.id, permission):
                raise HTTPException(403, "Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@app.delete("/api/posts/{post_id}")
@require_permission(Permission.POSTS_DELETE)
async def delete_post(post_id: int, current_user: User):
    # User has permission to delete posts
    return await delete_post_by_id(post_id)
```

### Hierarchical RBAC

```python
class HierarchicalRBAC:
    """RBAC with role inheritance"""

    def __init__(self):
        # Role hierarchy: child inherits from parent
        self.role_hierarchy = {
            Role.SUPER_ADMIN: [Role.ADMIN],
            Role.ADMIN: [Role.MODERATOR],
            Role.MODERATOR: [Role.EDITOR],
            Role.EDITOR: [Role.VIEWER],
            Role.VIEWER: [],
        }
        self.role_permissions = ROLE_PERMISSIONS

    def get_inherited_roles(self, role: Role) -> Set[Role]:
        """Get all roles including inherited ones"""
        roles = {role}
        for child in self.role_hierarchy.get(role, []):
            roles.update(self.get_inherited_roles(child))
        return roles

    def get_role_permissions(self, role: Role) -> Set[Permission]:
        """Get all permissions for a role including inherited"""
        permissions = set()
        for r in self.get_inherited_roles(role):
            permissions.update(self.role_permissions.get(r, set()))
        return permissions
```

## Attribute-Based Access Control (ABAC)

### ABAC Implementation

```python
from dataclasses import dataclass
from typing import Any, Callable
from enum import Enum

class Effect(Enum):
    ALLOW = "allow"
    DENY = "deny"

@dataclass
class Subject:
    """Who is making the request"""
    id: str
    roles: list[str]
    department: str
    clearance_level: int
    attributes: dict[str, Any]

@dataclass
class Resource:
    """What is being accessed"""
    type: str
    id: str
    owner_id: str
    classification: str
    department: str
    attributes: dict[str, Any]

@dataclass
class Action:
    """What operation is being performed"""
    name: str
    attributes: dict[str, Any] = None

@dataclass
class Environment:
    """Contextual information"""
    time: datetime
    ip_address: str
    location: str
    attributes: dict[str, Any] = None

@dataclass
class Policy:
    """Access control policy"""
    id: str
    description: str
    effect: Effect
    condition: Callable[[Subject, Resource, Action, Environment], bool]
    priority: int = 0  # Higher priority evaluated first

class ABACEngine:
    def __init__(self):
        self.policies: list[Policy] = []

    def add_policy(self, policy: Policy):
        """Add policy to engine"""
        self.policies.append(policy)
        # Sort by priority (higher first)
        self.policies.sort(key=lambda p: p.priority, reverse=True)

    def evaluate(
        self,
        subject: Subject,
        resource: Resource,
        action: Action,
        environment: Environment
    ) -> tuple[bool, str]:
        """Evaluate all policies and return decision"""

        # Default deny if no policies match
        for policy in self.policies:
            try:
                if policy.condition(subject, resource, action, environment):
                    allowed = policy.effect == Effect.ALLOW
                    return allowed, policy.description
            except Exception as e:
                # Log error, continue to next policy
                logger.error(f"Policy {policy.id} error: {e}")
                continue

        return False, "No matching policy - default deny"

# Create ABAC engine with policies
abac = ABACEngine()

# Policy: Owner can do anything with their resources
abac.add_policy(Policy(
    id="owner-full-access",
    description="Resource owner has full access",
    effect=Effect.ALLOW,
    priority=100,
    condition=lambda s, r, a, e: s.id == r.owner_id
))

# Policy: Same department can read
abac.add_policy(Policy(
    id="department-read",
    description="Same department can read resources",
    effect=Effect.ALLOW,
    priority=50,
    condition=lambda s, r, a, e: (
        s.department == r.department and
        a.name == "read"
    )
))

# Policy: Clearance level for classified resources
abac.add_policy(Policy(
    id="clearance-required",
    description="Clearance level must match or exceed classification",
    effect=Effect.DENY,
    priority=200,  # High priority deny
    condition=lambda s, r, a, e: (
        r.classification == "classified" and
        s.clearance_level < 3
    )
))

# Policy: No access outside business hours for sensitive data
abac.add_policy(Policy(
    id="business-hours-only",
    description="Sensitive data only during business hours",
    effect=Effect.DENY,
    priority=150,
    condition=lambda s, r, a, e: (
        r.classification in ["sensitive", "classified"] and
        not (9 <= e.time.hour < 17)
    )
))

# Usage
@app.get("/api/documents/{doc_id}")
async def get_document(
    doc_id: str,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    doc = await get_document_by_id(doc_id)

    subject = Subject(
        id=current_user.id,
        roles=current_user.roles,
        department=current_user.department,
        clearance_level=current_user.clearance_level,
        attributes={}
    )

    resource = Resource(
        type="document",
        id=doc.id,
        owner_id=doc.owner_id,
        classification=doc.classification,
        department=doc.department,
        attributes={}
    )

    action = Action(name="read")

    environment = Environment(
        time=datetime.utcnow(),
        ip_address=request.client.host,
        location="",
        attributes={}
    )

    allowed, reason = abac.evaluate(subject, resource, action, environment)

    if not allowed:
        raise HTTPException(403, f"Access denied: {reason}")

    return doc
```

## Object-Level Authorization

### Preventing IDOR

```python
from typing import Optional, TypeVar, Generic
from sqlalchemy.orm import Query

T = TypeVar('T')

class SecureQueryBuilder(Generic[T]):
    """Query builder that enforces authorization"""

    def __init__(self, model: type[T], user: User):
        self.model = model
        self.user = user
        self.base_query = db.query(model)

    def owned_by_user(self) -> Query[T]:
        """Filter to only resources owned by user"""
        return self.base_query.filter(self.model.owner_id == self.user.id)

    def in_user_organization(self) -> Query[T]:
        """Filter to resources in user's organization"""
        return self.base_query.filter(
            self.model.organization_id == self.user.organization_id
        )

    def with_permission(self, permission: str) -> Query[T]:
        """Filter to resources user has permission for"""
        # Join with permissions table
        return self.base_query.join(
            ResourcePermission,
            ResourcePermission.resource_id == self.model.id
        ).filter(
            ResourcePermission.user_id == self.user.id,
            ResourcePermission.permission == permission
        )

    def get_by_id(self, resource_id: str) -> Optional[T]:
        """Get resource by ID with ownership check"""
        return self.owned_by_user().filter(self.model.id == resource_id).first()

# Usage
@app.get("/api/documents/{doc_id}")
async def get_document(doc_id: str, current_user: User = Depends(get_current_user)):
    query = SecureQueryBuilder(Document, current_user)

    # Only returns document if user owns it
    doc = query.get_by_id(doc_id)

    if not doc:
        # Don't reveal if document exists
        raise HTTPException(404, "Document not found")

    return doc

@app.get("/api/documents")
async def list_documents(current_user: User = Depends(get_current_user)):
    query = SecureQueryBuilder(Document, current_user)

    # Only returns user's documents
    return query.owned_by_user().all()
```

### Resource-Level Permissions

```python
class ResourcePermission(Base):
    """Explicit permissions on resources"""
    __tablename__ = "resource_permissions"

    id = Column(String, primary_key=True)
    resource_type = Column(String, nullable=False)  # 'document', 'folder', etc.
    resource_id = Column(String, nullable=False)
    grantee_type = Column(String, nullable=False)   # 'user', 'role', 'group'
    grantee_id = Column(String, nullable=False)
    permission = Column(String, nullable=False)     # 'read', 'write', 'admin'
    granted_by = Column(String, nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('resource_type', 'resource_id', 'grantee_type',
                        'grantee_id', 'permission'),
    )

class PermissionManager:
    def __init__(self):
        self.permission_hierarchy = {
            'admin': ['write', 'read'],
            'write': ['read'],
            'read': [],
        }

    def grant_permission(
        self,
        resource_type: str,
        resource_id: str,
        grantee_type: str,
        grantee_id: str,
        permission: str,
        granted_by: str
    ):
        """Grant permission on resource"""
        perm = ResourcePermission(
            id=str(uuid4()),
            resource_type=resource_type,
            resource_id=resource_id,
            grantee_type=grantee_type,
            grantee_id=grantee_id,
            permission=permission,
            granted_by=granted_by,
        )
        db.add(perm)
        db.commit()

    def check_permission(
        self,
        user: User,
        resource_type: str,
        resource_id: str,
        required_permission: str
    ) -> bool:
        """Check if user has permission on resource"""

        # Get all valid permissions (including inherited)
        valid_permissions = {required_permission}
        for perm, includes in self.permission_hierarchy.items():
            if required_permission in includes:
                valid_permissions.add(perm)

        # Check direct user permission
        user_perm = db.query(ResourcePermission).filter(
            ResourcePermission.resource_type == resource_type,
            ResourcePermission.resource_id == resource_id,
            ResourcePermission.grantee_type == 'user',
            ResourcePermission.grantee_id == user.id,
            ResourcePermission.permission.in_(valid_permissions)
        ).first()

        if user_perm:
            return True

        # Check role-based permission
        role_perm = db.query(ResourcePermission).filter(
            ResourcePermission.resource_type == resource_type,
            ResourcePermission.resource_id == resource_id,
            ResourcePermission.grantee_type == 'role',
            ResourcePermission.grantee_id.in_(user.roles),
            ResourcePermission.permission.in_(valid_permissions)
        ).first()

        return role_perm is not None
```

## Function-Level Authorization

### Endpoint Protection

```python
from functools import wraps
from typing import Callable, List, Union

def require_roles(*roles: Role):
    """Decorator to require specific roles"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            user_roles = set(current_user.roles)
            required_roles = set(roles)

            if not user_roles & required_roles:
                raise HTTPException(403, "Insufficient role")

            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

def require_all_roles(*roles: Role):
    """Decorator to require ALL specified roles"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            user_roles = set(current_user.roles)
            required_roles = set(roles)

            if not required_roles.issubset(user_roles):
                raise HTTPException(403, "Missing required roles")

            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@app.post("/api/admin/users")
@require_roles(Role.ADMIN, Role.SUPER_ADMIN)
async def create_user(user_data: UserCreate, current_user: User):
    """Only admins can create users"""
    return await create_new_user(user_data)

@app.delete("/api/admin/system-config")
@require_all_roles(Role.ADMIN, Role.SUPER_ADMIN)
async def delete_config(config_id: str, current_user: User):
    """Requires BOTH admin AND super_admin roles"""
    return await delete_system_config(config_id)
```

### Action-Based Authorization

```python
class ActionAuthorizer:
    """Authorize specific actions on resources"""

    def __init__(self):
        self.action_rules: dict[str, Callable] = {}

    def register_rule(self, action: str, rule: Callable[[User, Any], bool]):
        """Register authorization rule for action"""
        self.action_rules[action] = rule

    def authorize(self, action: str, user: User, resource: Any) -> bool:
        """Check if user can perform action on resource"""
        rule = self.action_rules.get(action)
        if not rule:
            return False
        return rule(user, resource)

authorizer = ActionAuthorizer()

# Register rules
authorizer.register_rule(
    "post:edit",
    lambda user, post: (
        post.author_id == user.id or  # Author can edit
        "moderator" in user.roles or  # Moderators can edit
        "admin" in user.roles         # Admins can edit
    )
)

authorizer.register_rule(
    "post:delete",
    lambda user, post: (
        post.author_id == user.id or  # Author can delete own
        "admin" in user.roles         # Only admins can delete others
    )
)

authorizer.register_rule(
    "post:publish",
    lambda user, post: (
        "editor" in user.roles or
        "admin" in user.roles
    )
)

# Usage
@app.put("/api/posts/{post_id}")
async def update_post(
    post_id: str,
    update: PostUpdate,
    current_user: User = Depends(get_current_user)
):
    post = await get_post_by_id(post_id)

    if not authorizer.authorize("post:edit", current_user, post):
        raise HTTPException(403, "Cannot edit this post")

    return await update_post_content(post, update)
```

## Scope-Based Authorization (OAuth)

### OAuth Scopes

```python
class OAuthScope(str, Enum):
    # Read scopes
    READ_PROFILE = "read:profile"
    READ_POSTS = "read:posts"
    READ_MESSAGES = "read:messages"

    # Write scopes
    WRITE_PROFILE = "write:profile"
    WRITE_POSTS = "write:posts"
    WRITE_MESSAGES = "write:messages"

    # Admin scopes
    ADMIN_USERS = "admin:users"
    ADMIN_SYSTEM = "admin:system"

class ScopeManager:
    """Manage OAuth scopes"""

    def __init__(self):
        # Scope hierarchy
        self.scope_includes = {
            OAuthScope.WRITE_PROFILE: [OAuthScope.READ_PROFILE],
            OAuthScope.WRITE_POSTS: [OAuthScope.READ_POSTS],
            OAuthScope.WRITE_MESSAGES: [OAuthScope.READ_MESSAGES],
            OAuthScope.ADMIN_USERS: [
                OAuthScope.READ_PROFILE,
                OAuthScope.WRITE_PROFILE
            ],
        }

    def expand_scopes(self, scopes: set[OAuthScope]) -> set[OAuthScope]:
        """Expand scopes to include implied scopes"""
        expanded = set(scopes)
        for scope in scopes:
            expanded.update(self.scope_includes.get(scope, []))
        return expanded

    def check_scope(
        self,
        token_scopes: set[OAuthScope],
        required_scope: OAuthScope
    ) -> bool:
        """Check if token has required scope"""
        expanded = self.expand_scopes(token_scopes)
        return required_scope in expanded

scope_manager = ScopeManager()

def require_scope(scope: OAuthScope):
    """Decorator to require OAuth scope"""
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            token: OAuth2Token = Depends(get_current_token),
            **kwargs
        ):
            if not scope_manager.check_scope(token.scopes, scope):
                raise HTTPException(
                    403,
                    f"Token missing required scope: {scope}"
                )
            return await func(*args, token=token, **kwargs)
        return wrapper
    return decorator

# Usage
@app.get("/api/profile")
@require_scope(OAuthScope.READ_PROFILE)
async def get_profile(token: OAuth2Token):
    return await get_user_profile(token.user_id)

@app.put("/api/profile")
@require_scope(OAuthScope.WRITE_PROFILE)
async def update_profile(update: ProfileUpdate, token: OAuth2Token):
    return await update_user_profile(token.user_id, update)
```

## Audit Logging

### Authorization Audit Trail

```python
from datetime import datetime
from typing import Optional

@dataclass
class AuthorizationEvent:
    timestamp: datetime
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    decision: str  # 'allowed' or 'denied'
    reason: str
    ip_address: str
    user_agent: str

class AuthorizationAuditor:
    def __init__(self):
        self.events = []  # Use database in production

    def log_decision(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        allowed: bool,
        reason: str,
        request: Request
    ):
        """Log authorization decision"""
        event = AuthorizationEvent(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            decision="allowed" if allowed else "denied",
            reason=reason,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", ""),
        )

        self.events.append(event)

        # Alert on denied access attempts
        if not allowed:
            self._check_suspicious_activity(user_id)

    def _check_suspicious_activity(self, user_id: str):
        """Detect suspicious authorization patterns"""
        recent_denials = [
            e for e in self.events
            if e.user_id == user_id
            and e.decision == "denied"
            and (datetime.utcnow() - e.timestamp).seconds < 300  # Last 5 min
        ]

        if len(recent_denials) > 5:
            alert_security_team(
                f"Multiple authorization failures for user {user_id}"
            )

auditor = AuthorizationAuditor()
```

## Anti-Patterns to Avoid

### Common Authorization Mistakes

```python
# BAD: No authorization check
@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str):
    return await db.query(Document).filter(Document.id == doc_id).delete()

# BAD: Client-side only authorization
# Frontend: if (user.isAdmin) showDeleteButton()
# Backend has no check!

# BAD: Role check but no ownership check
@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str, user: User):
    if "admin" not in user.roles:
        raise HTTPException(403)
    # Missing: Check if user can delete THIS document
    return await delete_doc(doc_id)

# BAD: Mass assignment allows privilege escalation
@app.put("/api/users/me")
async def update_profile(data: dict, user: User):
    for key, value in data.items():
        setattr(user, key, value)  # Can set 'roles': ['admin']!
    db.commit()

# BAD: Implicit trust of authenticated users
@app.get("/api/admin/users")
async def list_all_users(user: User = Depends(get_current_user)):
    # Being authenticated doesn't mean admin!
    return await get_all_users()
```

### Correct Patterns

```python
# GOOD: Full authorization check
@app.delete("/api/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    user: User = Depends(get_current_user)
):
    doc = await get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(404)

    # Check ownership OR admin role
    if doc.owner_id != user.id and "admin" not in user.roles:
        raise HTTPException(403, "Cannot delete this document")

    return await delete_doc(doc_id)

# GOOD: Explicit field whitelist
class ProfileUpdate(BaseModel):
    name: Optional[str]
    bio: Optional[str]
    # Note: NO roles field!

@app.put("/api/users/me")
async def update_profile(data: ProfileUpdate, user: User):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
```

## Security Checklist

### Authorization Security
- [ ] Every endpoint has authorization check
- [ ] Object-level access control (IDOR prevention)
- [ ] Function-level access control
- [ ] No mass assignment vulnerabilities
- [ ] Fail-secure on authorization errors
- [ ] Authorization decisions logged
- [ ] Principle of least privilege applied
- [ ] Role hierarchy properly implemented
- [ ] Scopes validated for API tokens

## Summary

Secure authorization requires:

1. **Every request checked**: Authorization on all endpoints
2. **Object-level control**: Verify access to specific resources
3. **Function-level control**: Verify permission for operation
4. **Explicit over implicit**: Whitelist allowed actions
5. **Audit everything**: Log authorization decisions
6. **Fail secure**: Deny on errors or ambiguity


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

