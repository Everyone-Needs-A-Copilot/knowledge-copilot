---
last_updated: 2026-02-25
status: active
name: secrets-management
description: Secure secrets storage, rotation, vault integration, and credential management. Use when handling API keys, passwords, certificates, or other sensitive credentials.
triggers:
  files: ["**/.env*", "**/vault/**", "**/secrets/**", "**/credentials/**", "**/config/**"]
  keywords: ["secrets", "credentials", "API key", "password", "vault", "encryption key", "certificate", "secret management", "KMS", "HSM", "rotation", "environment variable"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

# Secrets Management Deep Expertise

This skill provides comprehensive guidance for secure secrets management. Apply this knowledge when handling credentials, implementing secret rotation, or integrating with vault systems.

## Secrets Management Principles

### Core Principles

| Principle | Description |
|-----------|-------------|
| Never Hardcode | No secrets in source code |
| Encrypt at Rest | Secrets encrypted when stored |
| Encrypt in Transit | Secrets encrypted when transmitted |
| Least Privilege | Minimal access to secrets |
| Audit Access | Log all secret access |
| Rotate Regularly | Change secrets periodically |

### Secret Types

| Type | Examples | Rotation Frequency |
|------|----------|-------------------|
| API Keys | Third-party service keys | 90 days |
| Database Credentials | DB username/password | 30-90 days |
| Encryption Keys | Data encryption keys | Annually |
| TLS Certificates | Server certificates | Before expiry |
| OAuth Secrets | Client secrets | 90 days |
| Service Account Keys | Cloud IAM keys | 90 days |


## Define Done

- [ ] Threat vectors identified for the target system
- [ ] Vulnerabilities assessed with severity ratings
- [ ] Mitigation strategies provided with implementation guidance
- [ ] Security measures don't create unacceptable usability barriers

## Environment-Based Configuration

### Environment Variables

```python
import os
from typing import Optional
from dataclasses import dataclass
from functools import lru_cache

@dataclass
class SecretConfig:
    """Application secrets configuration"""
    database_url: str
    api_key: str
    encryption_key: str
    jwt_secret: str
    oauth_client_secret: str

    @classmethod
    def from_environment(cls) -> 'SecretConfig':
        """Load secrets from environment variables"""
        required_vars = [
            'DATABASE_URL',
            'API_KEY',
            'ENCRYPTION_KEY',
            'JWT_SECRET',
            'OAUTH_CLIENT_SECRET',
        ]

        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")

        return cls(
            database_url=os.environ['DATABASE_URL'],
            api_key=os.environ['API_KEY'],
            encryption_key=os.environ['ENCRYPTION_KEY'],
            jwt_secret=os.environ['JWT_SECRET'],
            oauth_client_secret=os.environ['OAUTH_CLIENT_SECRET'],
        )

@lru_cache()
def get_config() -> SecretConfig:
    """Get cached configuration"""
    return SecretConfig.from_environment()

# Usage
config = get_config()
db = create_engine(config.database_url)
```

### dotenv for Development

```python
# .env.example (commit this)
DATABASE_URL=postgresql://user:password@localhost/db
API_KEY=your-api-key
ENCRYPTION_KEY=your-32-byte-key
JWT_SECRET=your-jwt-secret
OAUTH_CLIENT_SECRET=your-oauth-secret

# .env (NEVER commit this - add to .gitignore)
DATABASE_URL=postgresql://user:actual_password@localhost/db
API_KEY=sk-1234567890abcdef

# Python loading
from dotenv import load_dotenv

# Load only in development
if os.environ.get('ENVIRONMENT') != 'production':
    load_dotenv()
```

### .gitignore for Secrets

```gitignore
# Environment files
.env
.env.local
.env.*.local
*.env

# Secrets
secrets/
credentials/
*.pem
*.key
*.p12
*.pfx

# AWS
.aws/credentials

# GCP
*-credentials.json
service-account.json

# Azure
azure.json

# Vault
.vault-token
```

## Vault Integration

### HashiCorp Vault Client

```python
import hvac
from typing import Optional, Dict, Any
from functools import lru_cache
import os

class VaultClient:
    """HashiCorp Vault client wrapper"""

    def __init__(
        self,
        url: str = None,
        token: str = None,
        namespace: str = None
    ):
        self.url = url or os.environ.get('VAULT_ADDR')
        self.token = token or os.environ.get('VAULT_TOKEN')
        self.namespace = namespace or os.environ.get('VAULT_NAMESPACE')

        self.client = hvac.Client(
            url=self.url,
            token=self.token,
            namespace=self.namespace,
        )

        if not self.client.is_authenticated():
            raise ValueError("Vault authentication failed")

    def get_secret(self, path: str, key: str = None) -> Dict[str, Any]:
        """Get secret from KV v2 secrets engine"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret',
            )
            data = response['data']['data']
            return data[key] if key else data
        except hvac.exceptions.InvalidPath:
            raise ValueError(f"Secret not found: {path}")

    def set_secret(self, path: str, data: Dict[str, Any]) -> None:
        """Store secret in KV v2 secrets engine"""
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=data,
            mount_point='secret',
        )

    def generate_database_credentials(
        self,
        role: str
    ) -> Dict[str, str]:
        """Generate dynamic database credentials"""
        response = self.client.secrets.database.generate_credentials(
            name=role,
        )
        return {
            'username': response['data']['username'],
            'password': response['data']['password'],
            'lease_id': response['lease_id'],
            'lease_duration': response['lease_duration'],
        }

    def renew_lease(self, lease_id: str) -> None:
        """Renew a secret lease"""
        self.client.sys.renew_lease(lease_id=lease_id)

@lru_cache()
def get_vault_client() -> VaultClient:
    return VaultClient()

# Usage
vault = get_vault_client()
api_key = vault.get_secret('myapp/api', 'stripe_key')
db_creds = vault.generate_database_credentials('myapp-db')
```

### AWS Secrets Manager

```python
import boto3
from botocore.exceptions import ClientError
import json
from typing import Optional, Dict, Any
from functools import lru_cache

class AWSSecretsManager:
    """AWS Secrets Manager client"""

    def __init__(self, region_name: str = 'us-east-1'):
        self.client = boto3.client(
            'secretsmanager',
            region_name=region_name,
        )

    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve secret from AWS Secrets Manager"""
        try:
            response = self.client.get_secret_value(
                SecretId=secret_name
            )

            # Parse secret value
            if 'SecretString' in response:
                return json.loads(response['SecretString'])
            else:
                # Binary secret
                return {'binary': response['SecretBinary']}

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise ValueError(f"Secret not found: {secret_name}")
            raise

    def create_secret(
        self,
        secret_name: str,
        secret_value: Dict[str, Any],
        description: str = None
    ) -> str:
        """Create a new secret"""
        response = self.client.create_secret(
            Name=secret_name,
            SecretString=json.dumps(secret_value),
            Description=description or f"Secret for {secret_name}",
        )
        return response['ARN']

    def rotate_secret(
        self,
        secret_name: str,
        rotation_lambda_arn: str,
        rotation_days: int = 30
    ) -> None:
        """Enable automatic rotation"""
        self.client.rotate_secret(
            SecretId=secret_name,
            RotationLambdaARN=rotation_lambda_arn,
            RotationRules={
                'AutomaticallyAfterDays': rotation_days,
            },
        )

@lru_cache()
def get_aws_secrets() -> AWSSecretsManager:
    return AWSSecretsManager()

# Usage
secrets = get_aws_secrets()
db_config = secrets.get_secret('myapp/database')
```

### Google Cloud Secret Manager

```python
from google.cloud import secretmanager
from typing import Optional
from functools import lru_cache

class GCPSecretManager:
    """Google Cloud Secret Manager client"""

    def __init__(self, project_id: str = None):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id or self._get_project_id()

    def _get_project_id(self) -> str:
        """Get project ID from environment or metadata"""
        import os
        return os.environ.get('GCP_PROJECT', 'default-project')

    def get_secret(
        self,
        secret_id: str,
        version: str = 'latest'
    ) -> str:
        """Get secret value"""
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version}"

        response = self.client.access_secret_version(
            request={"name": name}
        )

        return response.payload.data.decode('UTF-8')

    def create_secret(
        self,
        secret_id: str,
        secret_value: str,
        labels: dict = None
    ) -> None:
        """Create a new secret"""
        parent = f"projects/{self.project_id}"

        # Create the secret
        secret = self.client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {
                    "replication": {"automatic": {}},
                    "labels": labels or {},
                },
            }
        )

        # Add the secret version
        self.client.add_secret_version(
            request={
                "parent": secret.name,
                "payload": {"data": secret_value.encode("UTF-8")},
            }
        )

    def add_secret_version(
        self,
        secret_id: str,
        secret_value: str
    ) -> str:
        """Add new version to existing secret"""
        parent = f"projects/{self.project_id}/secrets/{secret_id}"

        response = self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": secret_value.encode("UTF-8")},
            }
        )

        return response.name

@lru_cache()
def get_gcp_secrets() -> GCPSecretManager:
    return GCPSecretManager()
```

## Secret Rotation

### Rotation Strategy

```python
from datetime import datetime, timedelta
from typing import Callable, Dict, Any
import secrets
import string

class SecretRotator:
    """Automated secret rotation"""

    def __init__(self, vault_client: VaultClient):
        self.vault = vault_client
        self.rotation_handlers: Dict[str, Callable] = {}

    def register_handler(
        self,
        secret_type: str,
        handler: Callable[[str], Dict[str, Any]]
    ):
        """Register rotation handler for secret type"""
        self.rotation_handlers[secret_type] = handler

    async def rotate_secret(
        self,
        secret_path: str,
        secret_type: str
    ) -> Dict[str, Any]:
        """Rotate a secret"""
        handler = self.rotation_handlers.get(secret_type)
        if not handler:
            raise ValueError(f"No handler for secret type: {secret_type}")

        # Generate new secret
        new_secret = handler(secret_path)

        # Store in vault
        self.vault.set_secret(secret_path, new_secret)

        # Log rotation
        await self._log_rotation(secret_path, secret_type)

        return new_secret

    async def _log_rotation(
        self,
        secret_path: str,
        secret_type: str
    ):
        """Log secret rotation for audit"""
        logger.info(f"Secret rotated: {secret_path} ({secret_type})")

def generate_api_key(prefix: str = "sk") -> str:
    """Generate secure API key"""
    key = secrets.token_urlsafe(32)
    return f"{prefix}_{key}"

def generate_password(length: int = 32) -> str:
    """Generate secure password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_encryption_key() -> str:
    """Generate encryption key (base64)"""
    return secrets.token_urlsafe(32)

# Register handlers
rotator = SecretRotator(vault_client)
rotator.register_handler('api_key', lambda p: {'key': generate_api_key()})
rotator.register_handler('password', lambda p: {'password': generate_password()})
rotator.register_handler('encryption_key', lambda p: {'key': generate_encryption_key()})
```

### Database Credential Rotation

```python
import asyncpg
from typing import Tuple

class DatabaseCredentialRotator:
    """Rotate database credentials without downtime"""

    def __init__(
        self,
        admin_connection_string: str,
        vault_client: VaultClient
    ):
        self.admin_dsn = admin_connection_string
        self.vault = vault_client

    async def rotate_credentials(
        self,
        db_name: str,
        user_name: str
    ) -> Dict[str, str]:
        """Rotate database user password"""
        # Generate new password
        new_password = generate_password(32)

        # Connect as admin
        conn = await asyncpg.connect(self.admin_dsn)

        try:
            # Update password in database
            await conn.execute(
                f"ALTER USER {user_name} WITH PASSWORD $1",
                new_password
            )

            # Store new credentials in vault
            self.vault.set_secret(
                f"database/{db_name}",
                {
                    'username': user_name,
                    'password': new_password,
                    'rotated_at': datetime.utcnow().isoformat(),
                }
            )

            return {
                'username': user_name,
                'password': new_password,
            }

        finally:
            await conn.close()

    async def create_temporary_user(
        self,
        db_name: str,
        base_user: str,
        ttl_hours: int = 1
    ) -> Dict[str, str]:
        """Create temporary database user with TTL"""
        temp_user = f"{base_user}_temp_{secrets.token_hex(4)}"
        temp_password = generate_password(32)

        conn = await asyncpg.connect(self.admin_dsn)

        try:
            # Create temporary user
            await conn.execute(f"""
                CREATE USER {temp_user} WITH PASSWORD $1
                VALID UNTIL $2
            """, temp_password, datetime.utcnow() + timedelta(hours=ttl_hours))

            # Grant same permissions as base user
            await conn.execute(f"""
                GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {temp_user}
            """)

            return {
                'username': temp_user,
                'password': temp_password,
                'expires_at': (datetime.utcnow() + timedelta(hours=ttl_hours)).isoformat(),
            }

        finally:
            await conn.close()
```

## Kubernetes Secrets

### Kubernetes Secret Management

```yaml
# kubernetes/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: production
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@db:5432/mydb"
  API_KEY: "sk-1234567890"
---
# Using External Secrets Operator for Vault integration
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: myapp-secrets
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: secret/myapp/database
        property: url
    - secretKey: API_KEY
      remoteRef:
        key: secret/myapp/api
        property: key
```

### Secret Injection in Pods

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: app
      image: myapp:latest
      env:
        # From secret
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: DATABASE_URL
        # From secret as file
      volumeMounts:
        - name: secrets-volume
          mountPath: /etc/secrets
          readOnly: true
  volumes:
    - name: secrets-volume
      secret:
        secretName: myapp-secrets
```

## Secret Detection and Prevention

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

### Gitleaks Configuration

```toml
# .gitleaks.toml
[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key"
regex = '''(?i)api[_-]?key[_-]?[=:]\s*['"]?[a-z0-9]{32,}['"]?'''
tags = ["api", "key"]

[[rules]]
id = "custom-password"
description = "Password in config"
regex = '''(?i)password[_-]?[=:]\s*['"][^'"]{8,}['"]'''
tags = ["password"]

[allowlist]
paths = [
    '''\.env\.example''',
    '''\.secrets\.baseline''',
]
regexes = [
    '''EXAMPLE_''',
    '''your-.*-here''',
]
```

### Secret Scanning in CI/CD

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Gitleaks scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: TruffleHog scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
```

## Application Integration

### FastAPI Dependency Injection

```python
from fastapi import Depends, HTTPException
from functools import lru_cache

class SecretsDependency:
    """Secrets injection for FastAPI"""

    def __init__(self):
        self._vault = None
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes

    @property
    def vault(self) -> VaultClient:
        if self._vault is None:
            self._vault = VaultClient()
        return self._vault

    def get_secret(self, path: str) -> str:
        """Get secret with caching"""
        cache_key = f"{path}:{int(time.time() // self._cache_ttl)}"

        if cache_key not in self._cache:
            self._cache[cache_key] = self.vault.get_secret(path)

        return self._cache[cache_key]

secrets_dep = SecretsDependency()

def get_api_key() -> str:
    return secrets_dep.get_secret('myapp/api/key')

def get_db_connection_string() -> str:
    creds = secrets_dep.get_secret('myapp/database')
    return f"postgresql://{creds['username']}:{creds['password']}@{creds['host']}/{creds['database']}"

# Usage in endpoints
@app.get("/api/data")
async def get_data(
    api_key: str = Depends(get_api_key),
    db_url: str = Depends(get_db_connection_string),
):
    # Use secrets
    pass
```

### Configuration Class with Secrets

```python
from pydantic import BaseSettings, SecretStr
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with secret handling"""

    # Non-sensitive
    app_name: str = "MyApp"
    debug: bool = False

    # Sensitive - wrapped in SecretStr
    database_url: SecretStr
    api_key: SecretStr
    jwt_secret: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_database_url(self) -> str:
        """Get actual database URL value"""
        return self.database_url.get_secret_value()

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Usage
settings = get_settings()
# In logs, SecretStr shows '**********' not the actual value
print(settings.database_url)  # SecretStr('**********')
# Get actual value when needed
db_url = settings.get_database_url()
```

## Security Best Practices

### Anti-Patterns to Avoid

```python
# BAD: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "super_secret"

# BAD: Secrets in logs
logger.info(f"Connected with password: {password}")

# BAD: Secrets in error messages
raise ValueError(f"Invalid API key: {api_key}")

# BAD: Secrets in URLs
requests.get(f"https://api.example.com?key={api_key}")

# BAD: Committing .env files
# .gitignore missing .env

# BAD: Secrets in command line arguments
subprocess.run(["cmd", "--password", password])  # Visible in ps
```

### Correct Patterns

```python
# GOOD: Environment variables
API_KEY = os.environ.get("API_KEY")

# GOOD: Secrets from vault
api_key = vault.get_secret("myapp/api")

# GOOD: Masked logging
logger.info("Connected to database", extra={"db_host": db_host})

# GOOD: Generic error messages
raise ValueError("Invalid API key")

# GOOD: Headers for auth
requests.get(url, headers={"Authorization": f"Bearer {api_key}"})

# GOOD: Environment for subprocess
subprocess.run(["cmd"], env={"PASSWORD": password})
```

## Security Checklist

### Secrets Management
- [ ] No secrets in source code
- [ ] Secrets stored in vault/secret manager
- [ ] Environment variables used for injection
- [ ] .gitignore includes secret files
- [ ] Pre-commit hooks scan for secrets
- [ ] CI/CD scans for leaked secrets
- [ ] Secrets rotated regularly
- [ ] Access to secrets is audited
- [ ] Least privilege access to secrets
- [ ] Secrets masked in logs
- [ ] TLS for secret transmission

## Summary

Effective secrets management requires:

1. **Centralized storage**: Use vault or secret manager
2. **No hardcoding**: Never commit secrets
3. **Rotation**: Regular credential rotation
4. **Access control**: Least privilege
5. **Audit logging**: Track all access
6. **Detection**: Scan for leaked secrets
7. **Encryption**: Protect secrets at rest and in transit


## Quality Tests

### Threat Coverage Test
- Analysis covers relevant OWASP categories for the system type
- **PASS:** Each relevant threat category assessed, even if risk is low
- **FAIL:** Only obvious threats checked, subtle attack vectors ignored

### Recovery Path Test
- Each vulnerability has a specific remediation path
- **PASS:** Mitigation includes exact code changes or configuration steps
- **FAIL:** Advice is generic ('use encryption') without implementation specifics

