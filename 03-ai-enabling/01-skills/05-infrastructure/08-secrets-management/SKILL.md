---
last_updated: 2026-02-25
status: active
name: secrets-management
description: HashiCorp Vault, AWS Secrets Manager, Kubernetes secrets, and secure credential handling. Use when managing secrets.
triggers:
  files: ["**/vault*.hcl", "**/secrets*.yml", "**/*secret*.tf", "**/.env.example", "**/sealed-secrets*.yml"]
  keywords: ["vault", "secrets manager", "credentials", "API key", "password", "token", "certificate", "KMS", "encryption", "seal"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides implementation of secure secrets management across infrastructure and applications. Apply these patterns when storing credentials, rotating keys, or implementing zero-trust security.

The user provides secrets management requirements: credential storage, secret rotation, access control, or encryption key management.

## Core Principles

Secrets management excellence is built on five pillars:

1. **Never Hardcode**: Secrets are always external to code and configuration.
2. **Least Privilege**: Applications get only the secrets they need.
3. **Encryption at Rest**: All secrets encrypted with managed keys.
4. **Audit Everything**: Full audit trail of who accessed what, when.
5. **Rotate Regularly**: Automated rotation with zero downtime.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Secrets Management Solutions

| Solution | Best For | Complexity | Cost |
|----------|----------|------------|------|
| **HashiCorp Vault** | Enterprise, multi-cloud | High | Self-hosted or Enterprise |
| **AWS Secrets Manager** | AWS-native workloads | Low | Per-secret pricing |
| **AWS SSM Parameter Store** | Simple AWS secrets | Low | Free (standard) |
| **GCP Secret Manager** | GCP-native workloads | Low | Per-secret pricing |
| **Azure Key Vault** | Azure-native workloads | Low | Per-operation pricing |
| **Kubernetes Secrets** | K8s-only, development | Low | Free |
| **Doppler/1Password** | Developer experience | Low | SaaS pricing |

## HashiCorp Vault

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Vault Server                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Secrets   │  │    Auth     │  │     Policies        │ │
│  │   Engines   │  │   Methods   │  │                     │ │
│  │             │  │             │  │  path "secret/*" {  │ │
│  │  - KV v2    │  │  - Token    │  │    capabilities =   │ │
│  │  - Database │  │  - AppRole  │  │    ["read"]         │ │
│  │  - PKI      │  │  - K8s      │  │  }                  │ │
│  │  - Transit  │  │  - AWS IAM  │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Storage Backend                    │   │
│  │  (Consul, Raft, S3, PostgreSQL)                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Docker Compose Setup (Development)

```yaml
version: '3.8'

services:
  vault:
    image: hashicorp/vault:1.15
    container_name: vault
    cap_add:
      - IPC_LOCK
    ports:
      - "8200:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: dev-root-token
      VAULT_DEV_LISTEN_ADDRESS: 0.0.0.0:8200
    volumes:
      - vault_data:/vault/data
      - ./vault/config:/vault/config

  vault-init:
    image: hashicorp/vault:1.15
    container_name: vault-init
    depends_on:
      - vault
    environment:
      VAULT_ADDR: http://vault:8200
      VAULT_TOKEN: dev-root-token
    entrypoint: /bin/sh
    command: -c "sleep 5 && /vault/config/init.sh"
    volumes:
      - ./vault/config:/vault/config

volumes:
  vault_data:
```

### Production Configuration

```hcl
# vault/config/vault.hcl

storage "raft" {
  path    = "/vault/data"
  node_id = "vault-1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/vault/certs/vault.crt"
  tls_key_file  = "/vault/certs/vault.key"
}

api_addr = "https://vault.example.com:8200"
cluster_addr = "https://vault-1.internal:8201"

ui = true

# Auto-unseal with AWS KMS
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-unseal"
}

telemetry {
  prometheus_retention_time = "30s"
  disable_hostname = true
}
```

### Secrets Engines

**KV Secrets Engine (Key-Value):**
```bash
# Enable KV v2
vault secrets enable -path=secret kv-v2

# Write secret
vault kv put secret/myapp/database \
  username="dbuser" \
  password="supersecret"

# Read secret
vault kv get secret/myapp/database

# Get specific field
vault kv get -field=password secret/myapp/database

# List secrets
vault kv list secret/myapp/

# Delete secret
vault kv delete secret/myapp/database
```

**Database Secrets Engine (Dynamic Credentials):**
```bash
# Enable database engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/mydb \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly,readwrite" \
  connection_url="postgresql://{{username}}:{{password}}@db.example.com:5432/mydb?sslmode=require" \
  username="vault" \
  password="vault-admin-password"

# Create role with dynamic credentials
vault write database/roles/readonly \
  db_name=mydb \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Get dynamic credentials
vault read database/creds/readonly
# Returns: username=v-token-readonly-xxx, password=yyy (expires in 1h)
```

**PKI Secrets Engine (Certificates):**
```bash
# Enable PKI engine
vault secrets enable pki

# Configure max TTL
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write pki/root/generate/internal \
  common_name="example.com" \
  ttl=87600h

# Configure CA URLs
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com:8200/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"

# Create role
vault write pki/roles/server \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl="720h"

# Issue certificate
vault write pki/issue/server \
  common_name="api.example.com" \
  ttl="24h"
```

**Transit Secrets Engine (Encryption as a Service):**
```bash
# Enable transit engine
vault secrets enable transit

# Create encryption key
vault write -f transit/keys/myapp

# Encrypt data
vault write transit/encrypt/myapp \
  plaintext=$(echo "secret data" | base64)

# Returns: ciphertext=vault:v1:xxx

# Decrypt data
vault write transit/decrypt/myapp \
  ciphertext="vault:v1:xxx"

# Rotate key (old data still decryptable)
vault write -f transit/keys/myapp/rotate
```

### Authentication Methods

**AppRole (Machine Authentication):**
```bash
# Enable AppRole
vault auth enable approle

# Create policy
vault policy write myapp - <<EOF
path "secret/data/myapp/*" {
  capabilities = ["read"]
}
path "database/creds/readonly" {
  capabilities = ["read"]
}
EOF

# Create AppRole
vault write auth/approle/role/myapp \
  token_policies="myapp" \
  token_ttl=1h \
  token_max_ttl=4h \
  secret_id_ttl=10m \
  secret_id_num_uses=1

# Get Role ID (static, can be baked into config)
vault read auth/approle/role/myapp/role-id

# Get Secret ID (dynamic, delivered securely)
vault write -f auth/approle/role/myapp/secret-id

# Application login
vault write auth/approle/login \
  role_id="xxx" \
  secret_id="yyy"
# Returns: token for accessing secrets
```

**Kubernetes Authentication:**
```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Create role for app
vault write auth/kubernetes/role/myapp \
  bound_service_account_names=myapp \
  bound_service_account_namespaces=production \
  policies=myapp \
  ttl=1h
```

### Policies

```hcl
# vault/policies/myapp.hcl

# Read-only access to app secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Dynamic database credentials
path "database/creds/readonly" {
  capabilities = ["read"]
}

# Encrypt/decrypt with transit
path "transit/encrypt/myapp" {
  capabilities = ["update"]
}

path "transit/decrypt/myapp" {
  capabilities = ["update"]
}

# Deny access to admin paths
path "sys/*" {
  capabilities = ["deny"]
}
```

### Application Integration

**Python (hvac library):**
```python
import hvac
import os

class VaultClient:
    def __init__(self):
        self.client = hvac.Client(url=os.environ['VAULT_ADDR'])

        # AppRole authentication
        role_id = os.environ['VAULT_ROLE_ID']
        secret_id = os.environ['VAULT_SECRET_ID']

        self.client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id,
        )

    def get_secret(self, path: str, key: str) -> str:
        """Get secret from KV v2 engine."""
        response = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point='secret',
        )
        return response['data']['data'][key]

    def get_db_credentials(self, role: str) -> dict:
        """Get dynamic database credentials."""
        response = self.client.secrets.database.generate_credentials(
            name=role,
        )
        return {
            'username': response['data']['username'],
            'password': response['data']['password'],
            'ttl': response['lease_duration'],
        }

# Usage
vault = VaultClient()
db_password = vault.get_secret('myapp/database', 'password')
db_creds = vault.get_db_credentials('readonly')
```

**Node.js (node-vault):**
```typescript
import Vault from 'node-vault';

async function getVaultClient(): Promise<Vault.client> {
  const vault = Vault({
    endpoint: process.env.VAULT_ADDR,
  });

  // AppRole login
  const { auth } = await vault.approleLogin({
    role_id: process.env.VAULT_ROLE_ID,
    secret_id: process.env.VAULT_SECRET_ID,
  });

  vault.token = auth.client_token;
  return vault;
}

async function getSecret(path: string, key: string): Promise<string> {
  const vault = await getVaultClient();
  const { data } = await vault.read(`secret/data/${path}`);
  return data.data[key];
}

// Usage
const dbPassword = await getSecret('myapp/database', 'password');
```

### Kubernetes Sidecar Injection

```yaml
# Vault Agent Injector annotations
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-inject-status: "update"
        vault.hashicorp.com/role: "myapp"
        vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/config"
        vault.hashicorp.com/agent-inject-template-config: |
          {{- with secret "secret/data/myapp/config" -}}
          DATABASE_URL=postgresql://{{ .Data.data.db_user }}:{{ .Data.data.db_password }}@db:5432/myapp
          API_KEY={{ .Data.data.api_key }}
          {{- end }}
    spec:
      serviceAccountName: myapp
      containers:
        - name: myapp
          image: myapp:latest
          command: ["/bin/sh", "-c"]
          args:
            - "source /vault/secrets/config && exec ./app"
```

## AWS Secrets Manager

### Creating Secrets

```bash
# Create secret
aws secretsmanager create-secret \
  --name "production/myapp/database" \
  --description "Database credentials for myapp" \
  --secret-string '{"username":"dbuser","password":"supersecret"}'

# Create secret from file
aws secretsmanager create-secret \
  --name "production/myapp/api-key" \
  --secret-binary fileb://api-key.pem

# Update secret
aws secretsmanager update-secret \
  --secret-id "production/myapp/database" \
  --secret-string '{"username":"dbuser","password":"newsecret"}'

# Get secret
aws secretsmanager get-secret-value \
  --secret-id "production/myapp/database"
```

### Terraform Configuration

```hcl
# Create secret
resource "aws_secretsmanager_secret" "database" {
  name        = "production/myapp/database"
  description = "Database credentials"

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    username = "dbuser"
    password = random_password.db.result
  })
}

# Generate random password
resource "random_password" "db" {
  length  = 32
  special = true
}

# Rotation configuration
resource "aws_secretsmanager_secret_rotation" "database" {
  secret_id           = aws_secretsmanager_secret.database.id
  rotation_lambda_arn = aws_lambda_function.rotate_secret.arn

  rotation_rules {
    automatically_after_days = 30
  }
}
```

### Application Integration (Python)

```python
import boto3
import json
from functools import lru_cache

@lru_cache(maxsize=100)
def get_secret(secret_name: str) -> dict:
    """Get secret from AWS Secrets Manager with caching."""
    client = boto3.client('secretsmanager')

    response = client.get_secret_value(SecretId=secret_name)

    if 'SecretString' in response:
        return json.loads(response['SecretString'])
    else:
        # Binary secret
        return {'binary': response['SecretBinary']}

# Usage
db_creds = get_secret('production/myapp/database')
connection_string = f"postgresql://{db_creds['username']}:{db_creds['password']}@db:5432/myapp"
```

### Automatic Rotation Lambda

```python
import boto3
import json
import string
import secrets

def lambda_handler(event, context):
    """Rotate database password in Secrets Manager."""
    secret_id = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    client = boto3.client('secretsmanager')

    if step == 'createSecret':
        # Generate new password
        current = client.get_secret_value(
            SecretId=secret_id,
            VersionStage='AWSCURRENT'
        )
        secret_dict = json.loads(current['SecretString'])

        # Generate new password
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
        new_password = ''.join(secrets.choice(alphabet) for _ in range(32))
        secret_dict['password'] = new_password

        # Store as pending
        client.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=token,
            SecretString=json.dumps(secret_dict),
            VersionStages=['AWSPENDING']
        )

    elif step == 'setSecret':
        # Update password in database
        pending = client.get_secret_value(
            SecretId=secret_id,
            VersionStage='AWSPENDING',
            VersionId=token
        )
        secret_dict = json.loads(pending['SecretString'])

        # Connect to DB and change password
        change_db_password(secret_dict['username'], secret_dict['password'])

    elif step == 'testSecret':
        # Verify new credentials work
        pending = client.get_secret_value(
            SecretId=secret_id,
            VersionStage='AWSPENDING',
            VersionId=token
        )
        secret_dict = json.loads(pending['SecretString'])

        # Test connection
        test_db_connection(secret_dict['username'], secret_dict['password'])

    elif step == 'finishSecret':
        # Mark pending as current
        metadata = client.describe_secret(SecretId=secret_id)
        current_version = [
            v for v, stages in metadata['VersionIdsToStages'].items()
            if 'AWSCURRENT' in stages
        ][0]

        client.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
            RemoveFromVersionId=current_version
        )
```

## Kubernetes Secrets

### Basic Secrets

```yaml
# Create secret (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: production
type: Opaque
data:
  db-password: c3VwZXJzZWNyZXQ=  # base64 of 'supersecret'
  api-key: YWJjLTEyMy1kZWY=      # base64 of 'abc-123-def'

---
# Use in pod
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          env:
            # From secret key
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: db-password
          # Or mount as file
          volumeMounts:
            - name: secrets
              mountPath: /secrets
              readOnly: true
      volumes:
        - name: secrets
          secret:
            secretName: myapp-secrets
```

### Sealed Secrets (GitOps-Safe)

```yaml
# Install Sealed Secrets controller
# kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Seal a secret (can be committed to Git)
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: myapp-secrets
  namespace: production
spec:
  encryptedData:
    db-password: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
    api-key: AgCtr+JZqp3JKuIvK3+uJ1yZoJ5oLqPh...
  template:
    metadata:
      name: myapp-secrets
      namespace: production
    type: Opaque
```

```bash
# Create sealed secret from literal
kubeseal --format=yaml \
  --controller-name=sealed-secrets \
  --controller-namespace=kube-system \
  < secret.yaml > sealed-secret.yaml

# Create sealed secret from literal
echo -n "supersecret" | kubeseal --raw \
  --name myapp-secrets \
  --namespace production \
  --from-file=/dev/stdin
```

### External Secrets Operator

```yaml
# Install External Secrets Operator
# kubectl apply -f https://github.com/external-secrets/external-secrets/releases/download/v0.9.0/external-secrets.yaml

# SecretStore (cluster-wide or namespace-scoped)
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets
            namespace: external-secrets

---
# ExternalSecret (syncs from AWS to Kubernetes)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
  data:
    - secretKey: db-password
      remoteRef:
        key: production/myapp/database
        property: password
    - secretKey: api-key
      remoteRef:
        key: production/myapp/api-key
```

## Environment Variables

### .env Files (Development Only)

```bash
# .env.example (committed to Git)
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
API_KEY=your-api-key-here
REDIS_URL=redis://localhost:6379

# .env (NEVER committed)
DATABASE_URL=postgresql://realuser:realsecret@db:5432/myapp
API_KEY=abc-123-def
REDIS_URL=redis://redis:6379
```

```gitignore
# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
```

### Docker Secrets

```yaml
# docker-compose.yml
version: '3.8'

services:
  myapp:
    image: myapp:latest
    secrets:
      - db_password
      - api_key
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
      API_KEY_FILE: /run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Created with `docker secret create`
```

```python
# Application code to read Docker secrets
import os

def get_secret(name: str) -> str:
    """Read secret from file or environment variable."""
    file_path = os.environ.get(f'{name}_FILE')
    if file_path:
        with open(file_path, 'r') as f:
            return f.read().strip()
    return os.environ.get(name, '')

db_password = get_secret('DB_PASSWORD')
```

## Secret Rotation

### Zero-Downtime Rotation Pattern

```
1. Create new credential (v2)
2. Update secret store with both v1 and v2
3. Deploy apps that accept both v1 and v2
4. Wait for all connections to switch to v2
5. Revoke v1 credential
6. Remove v1 from secret store
```

### Database Password Rotation

```python
import psycopg2
from datetime import datetime, timedelta

def rotate_db_password(db_host: str, admin_user: str, admin_pass: str,
                       app_user: str, new_password: str):
    """Rotate database password with zero downtime."""

    conn = psycopg2.connect(
        host=db_host,
        user=admin_user,
        password=admin_pass,
        dbname='postgres'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Step 1: Create new password (valid for 24h, overlapping with old)
    cursor.execute(f"""
        ALTER ROLE {app_user}
        WITH PASSWORD '{new_password}'
        VALID UNTIL '{(datetime.now() + timedelta(days=1)).isoformat()}'
    """)

    # Step 2: Test new credentials
    try:
        test_conn = psycopg2.connect(
            host=db_host,
            user=app_user,
            password=new_password,
            dbname='postgres'
        )
        test_conn.close()
    except Exception as e:
        # Rollback if new password doesn't work
        raise RuntimeError(f"New password test failed: {e}")

    # Step 3: Update secret store (done by caller)
    # Step 4: Wait for apps to reconnect (done by caller)
    # Step 5: Remove expiry (make permanent)
    cursor.execute(f"""
        ALTER ROLE {app_user}
        VALID UNTIL 'infinity'
    """)

    cursor.close()
    conn.close()
```

### API Key Rotation

```typescript
// Multi-key acceptance during rotation
const VALID_API_KEYS = new Set([
  process.env.API_KEY_CURRENT,
  process.env.API_KEY_PREVIOUS,  // Still valid during rotation
].filter(Boolean));

function validateApiKey(key: string): boolean {
  return VALID_API_KEYS.has(key);
}

// Rotation process:
// 1. Generate new key, set as API_KEY_CURRENT
// 2. Move old key to API_KEY_PREVIOUS
// 3. Deploy apps
// 4. Wait for clients to update
// 5. Revoke old key, remove API_KEY_PREVIOUS
```

## Security Best Practices

### Access Control

| Principle | Implementation |
|-----------|----------------|
| Least privilege | Grant minimum permissions needed |
| Role-based access | Group permissions by job function |
| Time-limited access | Use short TTLs, require re-auth |
| Audit logging | Log all secret access |
| Separation of duties | Different people manage different secrets |

### Secret Storage Checklist

- [ ] Encrypted at rest (KMS, Vault seal)
- [ ] Encrypted in transit (TLS)
- [ ] Access control policies defined
- [ ] Audit logging enabled
- [ ] Rotation policy configured
- [ ] Backup and recovery tested
- [ ] No secrets in code or Git history

### Detecting Exposed Secrets

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.0
    hooks:
      - id: trufflehog
```

```bash
# Scan Git history for secrets
trufflehog git file://. --since-commit HEAD~100

# Generate baseline (allowed patterns)
detect-secrets scan > .secrets.baseline
```

### Response to Leaked Secrets

1. **Immediately revoke** the compromised credential
2. **Generate new secret** and update all systems
3. **Audit access logs** to determine exposure scope
4. **Notify stakeholders** if data accessed
5. **Post-mortem** to prevent recurrence

## Anti-Patterns

**NEVER do these:**

### 1. Secrets in Code

```python
# NEVER hardcode secrets
API_KEY = "sk-live-abc123def456"
DATABASE_URL = "postgresql://user:password@host/db"

# Use environment variables
API_KEY = os.environ['API_KEY']
DATABASE_URL = os.environ['DATABASE_URL']
```

### 2. Secrets in Git

```bash
# NEVER commit secrets
git add .env
git add secrets.yml
git add *.pem

# Use .gitignore
echo ".env" >> .gitignore
echo "*.pem" >> .gitignore
```

### 3. Plaintext Storage

```yaml
# NEVER store secrets in plaintext ConfigMaps
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DB_PASSWORD: supersecret  # WRONG!

# Use Secrets (still base64, but better)
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  DB_PASSWORD: c3VwZXJzZWNyZXQ=
```

### 4. Shared Credentials

```bash
# NEVER share credentials across environments
# dev, staging, and production should have DIFFERENT secrets

# Use per-environment secrets
secret/dev/myapp/database
secret/staging/myapp/database
secret/production/myapp/database
```

### 5. No Rotation

```python
# NEVER use static, long-lived secrets
API_KEY = "key-created-3-years-ago"

# Implement rotation
# - API keys: 90 days max
# - Passwords: 30-90 days
# - Certificates: Before expiry
```

---

## Quick Reference

**Vault CLI:**
```bash
vault login                     # Authenticate
vault kv put secret/app key=val # Write secret
vault kv get secret/app         # Read secret
vault kv delete secret/app      # Delete secret
vault policy write name file    # Create policy
vault token create -policy=name # Create token
```

**AWS Secrets Manager CLI:**
```bash
aws secretsmanager create-secret --name name --secret-string value
aws secretsmanager get-secret-value --secret-id name
aws secretsmanager update-secret --secret-id name --secret-string value
aws secretsmanager delete-secret --secret-id name
```

**Kubernetes Secrets:**
```bash
kubectl create secret generic name --from-literal=key=value
kubectl get secret name -o jsonpath='{.data.key}' | base64 -d
kubectl delete secret name
```

---

Apply these patterns to implement secure, auditable, scalable secrets management. Prioritize encryption (at rest and in transit), rotation (automated, zero-downtime), and access control (least privilege, audit logging).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

