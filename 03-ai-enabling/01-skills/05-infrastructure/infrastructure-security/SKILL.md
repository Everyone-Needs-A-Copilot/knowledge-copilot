---
last_updated: 2026-02-25
status: active
name: infrastructure-security
description: Network security, IAM, and cloud security patterns. Use when securing infrastructure and cloud resources.
triggers:
  files: ["**/security*.yaml", "**/iam/**", "**/network-policy*.yaml", "**/*firewall*", "**/waf*"]
  keywords: ["infrastructure security", "IAM", "network policy", "firewall", "security groups", "WAF", "cloud security", "zero trust"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides infrastructure security implementation for cloud and on-premise environments. Apply these patterns when securing networks, managing access, or hardening systems.

The user provides security requirements: access control needs, network segmentation, compliance requirements, or threat models.

## Core Principles

Infrastructure security is built on five pillars:

1. **Least Privilege**: Minimum access required for function.
2. **Defense in Depth**: Multiple security layers.
3. **Zero Trust**: Verify explicitly, assume breach.
4. **Encryption Everywhere**: Data at rest and in transit.
5. **Audit Everything**: Log all access and changes.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Network Security

### AWS Security Groups

```hcl
# Terraform - Web tier security group
resource "aws_security_group" "web" {
  name        = "web-tier-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # HTTP from ALB only
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "HTTP from ALB"
  }

  # No direct SSH - use SSM Session Manager
  # ingress for SSH intentionally omitted

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS outbound"
  }

  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.database.id]
    description     = "PostgreSQL to database tier"
  }

  tags = {
    Name = "web-tier-sg"
  }
}
```

### Kubernetes Network Policies

```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
---
# Allow specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - port: 5432
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - port: 53
          protocol: UDP
```

## IAM Best Practices

### AWS IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-bucket",
        "arn:aws:s3:::my-app-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-east-1"
        }
      }
    },
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": "*",
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

### IAM Role Trust Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:sub": "system:serviceaccount:default:my-service-account"
        }
      }
    }
  ]
}
```

### Kubernetes RBAC

```yaml
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-service-account
  namespace: production
---
# Role with minimal permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: api-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["api-config"]
    verbs: ["get"]
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["api-secrets"]
    verbs: ["get"]
---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-role-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: api-service-account
    namespace: production
roleRef:
  kind: Role
  name: api-role
  apiGroup: rbac.authorization.k8s.io
```

## Encryption

### At Rest (AWS KMS)

```hcl
# KMS key for data encryption
resource "aws_kms_key" "main" {
  description             = "Main encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow service role"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.app.arn
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "*"
      }
    ]
  })
}

# Encrypted RDS
resource "aws_db_instance" "main" {
  storage_encrypted = true
  kms_key_id        = aws_kms_key.main.arn
  # ...
}

# Encrypted S3
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.main.arn
      sse_algorithm     = "aws:kms"
    }
  }
}
```

### In Transit (TLS)

```yaml
# Kubernetes - TLS termination at ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 80
```

## WAF Configuration

```hcl
# AWS WAF for common attacks
resource "aws_wafv2_web_acl" "main" {
  name        = "api-waf"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  # AWS Managed Rules - Core Rule Set
  rule {
    name     = "AWS-AWSManagedRulesCommonRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "AWSManagedRulesCommonRuleSetMetric"
      sampled_requests_enabled  = true
    }
  }

  # SQL Injection protection
  rule {
    name     = "AWS-AWSManagedRulesSQLiRuleSet"
    priority = 2

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesSQLiRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "SQLiRuleSetMetric"
      sampled_requests_enabled  = true
    }
  }

  # Rate limiting
  rule {
    name     = "RateLimitRule"
    priority = 3

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "RateLimitRuleMetric"
      sampled_requests_enabled  = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name               = "apiWafMetric"
    sampled_requests_enabled  = true
  }
}
```

## Secrets Management

### AWS Secrets Manager

```hcl
resource "aws_secretsmanager_secret" "db_credentials" {
  name                    = "production/database/credentials"
  recovery_window_in_days = 7

  tags = {
    Environment = "production"
  }
}

resource "aws_secretsmanager_secret_rotation" "db_credentials" {
  secret_id           = aws_secretsmanager_secret.db_credentials.id
  rotation_lambda_arn = aws_lambda_function.secret_rotation.arn

  rotation_rules {
    automatically_after_days = 30
  }
}
```

### Kubernetes External Secrets

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-secrets-manager
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
    - secretKey: username
      remoteRef:
        key: production/database/credentials
        property: username
    - secretKey: password
      remoteRef:
        key: production/database/credentials
        property: password
```

## Security Checklist

### Network

- [ ] Default deny network policies
- [ ] Security groups with minimal access
- [ ] Private subnets for databases
- [ ] VPC endpoints for AWS services
- [ ] WAF for public endpoints

### Identity

- [ ] MFA for all human users
- [ ] Service accounts for workloads
- [ ] Role-based access (RBAC)
- [ ] Regular access reviews
- [ ] No long-lived credentials

### Data

- [ ] Encryption at rest (KMS)
- [ ] Encryption in transit (TLS)
- [ ] Backup encryption
- [ ] Data classification
- [ ] Retention policies

### Monitoring

- [ ] CloudTrail/audit logging
- [ ] Security alerts configured
- [ ] Vulnerability scanning
- [ ] Compliance monitoring
- [ ] Incident response plan

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Wide-open security groups | Minimum required ports/sources |
| Hardcoded credentials | Use secrets management |
| Root/admin access everywhere | Least privilege roles |
| No network segmentation | VPCs, subnets, policies |
| Public S3 buckets | Block public access by default |
| SSH keys on instances | Use SSM Session Manager |

## Compliance Mapping

| Control | AWS | Kubernetes |
|---------|-----|------------|
| Access Control | IAM policies | RBAC |
| Encryption | KMS, ACM | Secrets, cert-manager |
| Logging | CloudTrail | Audit logs |
| Network | Security Groups, NACLs | NetworkPolicies |
| Vulnerability | Inspector | Trivy, Falco |

---

Apply these patterns for defense-in-depth infrastructure security. Start with network segmentation and IAM, add encryption everywhere, and implement comprehensive monitoring and alerting.


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

