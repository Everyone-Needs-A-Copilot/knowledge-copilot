---
last_updated: 2026-02-25
status: active
name: terraform-best-practices
description: Terraform modules, state management, workspaces, and IaC patterns. Use when working with infrastructure as code.
triggers:
  files: ["**/*.tf", "**/*.tfvars", "**/terraform.tfstate*", "**/.terraform/**"]
  keywords: ["terraform", "infrastructure as code", "IaC", "module", "state", "tfvars", "workspace", "provider", "resource", "data source"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides creation of production-grade infrastructure using Terraform best practices. Apply these patterns when provisioning cloud resources, managing state, or building reusable modules.

The user provides infrastructure requirements: Terraform configuration, module design, state management, or multi-environment deployments.

## Core Principles

Terraform excellence is built on five pillars:

1. **Modularity**: Reusable modules with clear interfaces. Don't repeat yourself.
2. **State Safety**: Remote state with locking. Never lose infrastructure knowledge.
3. **Immutability**: Replace, don't modify. Predictable infrastructure changes.
4. **Versioning**: Pin all versions (providers, modules). Reproducible deployments.
5. **Least Privilege**: Minimal IAM permissions. Service accounts over user credentials.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Project Structure

### Standard Layout

```
infrastructure/
├── modules/                    # Reusable modules
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── eks/
│   └── rds/
├── environments/               # Environment-specific configs
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
├── global/                     # Shared resources (IAM, DNS)
│   ├── iam/
│   └── route53/
└── scripts/
    └── init.sh
```

### File Conventions

| File | Purpose |
|------|---------|
| `main.tf` | Primary resources and module calls |
| `variables.tf` | Input variable declarations |
| `outputs.tf` | Output value declarations |
| `providers.tf` | Provider configuration |
| `backend.tf` | State backend configuration |
| `locals.tf` | Local values and computed expressions |
| `data.tf` | Data source declarations |
| `versions.tf` | Required provider versions |
| `terraform.tfvars` | Variable values (not committed) |

### Naming Conventions

**Resources:**
```hcl
# Pattern: {service}_{role}_{qualifier}
resource "aws_instance" "web_primary" { }
resource "aws_security_group" "db_access" { }
resource "aws_iam_role" "lambda_execution" { }
```

**Variables:**
```hcl
# Descriptive, snake_case
variable "vpc_cidr_block" { }
variable "enable_nat_gateway" { }
variable "instance_count" { }
```

**Outputs:**
```hcl
# Describe what's being exported
output "vpc_id" { }
output "public_subnet_ids" { }
output "db_connection_string" { }
```

## Provider Configuration

### Version Pinning

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allow 5.x, not 6.x
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

**Version Constraints:**
| Constraint | Meaning |
|------------|---------|
| `= 5.0.0` | Exact version |
| `>= 5.0` | Minimum version |
| `~> 5.0` | Allow 5.x (patch/minor updates) |
| `>= 5.0, < 6.0` | Range |

### Provider Aliases (Multi-Region)

```hcl
# providers.tf
provider "aws" {
  region = "us-east-1"
  alias  = "primary"

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project
      ManagedBy   = "terraform"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
  alias  = "dr"

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project
      ManagedBy   = "terraform"
    }
  }
}

# Using aliased provider
resource "aws_s3_bucket" "replica" {
  provider = aws.dr
  bucket   = "${var.project}-replica-bucket"
}
```

### Assume Role (Cross-Account)

```hcl
provider "aws" {
  region = "us-east-1"

  assume_role {
    role_arn     = "arn:aws:iam::123456789012:role/TerraformRole"
    session_name = "terraform-session"
    external_id  = var.external_id
  }
}
```

## State Management

### Remote State (S3 + DynamoDB)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "environments/production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # Prevent accidental state deletion
    skip_metadata_api_check     = true
    skip_region_validation      = true
    skip_credentials_validation = true
  }
}
```

**State Bucket Setup:**
```hcl
# global/state-bucket/main.tf
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mycompany-terraform-state"
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

### State Data Source (Cross-Stack)

```hcl
# Read outputs from another Terraform stack
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "mycompany-terraform-state"
    key    = "environments/production/vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use outputs from VPC stack
resource "aws_instance" "web" {
  subnet_id = data.terraform_remote_state.vpc.outputs.public_subnet_ids[0]
  vpc_security_group_ids = [
    data.terraform_remote_state.vpc.outputs.default_security_group_id
  ]
}
```

### State Operations

```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_instance.web

# Move resource (refactoring)
terraform state mv aws_instance.web module.compute.aws_instance.web

# Remove resource from state (don't destroy)
terraform state rm aws_instance.web

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Pull remote state to local
terraform state pull > terraform.tfstate.backup
```

## Module Design

### Module Structure

```
modules/vpc/
├── main.tf           # Primary resources
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── locals.tf         # Local values
├── versions.tf       # Provider requirements
└── README.md         # Documentation
```

### Input Variables

```hcl
# variables.tf
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid CIDR block."
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = []
}

variable "enable_nat_gateway" {
  description = "Whether to create NAT gateway for private subnets"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags for all resources"
  type        = map(string)
  default     = {}
}

# Complex type with defaults
variable "subnet_config" {
  description = "Subnet configuration"
  type = object({
    public_subnets  = list(string)
    private_subnets = list(string)
    database_subnets = optional(list(string), [])
  })
  default = {
    public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
    private_subnets = ["10.0.101.0/24", "10.0.102.0/24"]
  }
}
```

### Output Values

```hcl
# outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ip" {
  description = "Elastic IP of NAT gateway"
  value       = var.enable_nat_gateway ? aws_eip.nat[0].public_ip : null
}

# Sensitive output (hidden in logs)
output "db_password" {
  description = "Database master password"
  value       = random_password.db.result
  sensitive   = true
}
```

### Local Values

```hcl
# locals.tf
locals {
  # Common tags
  common_tags = merge(
    var.tags,
    {
      Environment = var.environment
      Project     = var.project
      ManagedBy   = "terraform"
    }
  )

  # Computed values
  azs = length(var.availability_zones) > 0 ? var.availability_zones : data.aws_availability_zones.available.names

  # Conditional naming
  name_prefix = "${var.project}-${var.environment}"

  # Complex computation
  subnet_cidrs = {
    for idx, az in local.azs : az => {
      public  = cidrsubnet(var.vpc_cidr, 8, idx)
      private = cidrsubnet(var.vpc_cidr, 8, idx + 100)
    }
  }
}
```

### Module Usage

```hcl
# environments/production/main.tf
module "vpc" {
  source = "../../modules/vpc"

  environment        = "production"
  vpc_cidr           = "10.0.0.0/16"
  enable_nat_gateway = true

  tags = {
    Team    = "platform"
    CostCenter = "infrastructure"
  }
}

module "eks" {
  source = "../../modules/eks"

  cluster_name       = "production-cluster"
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids

  depends_on = [module.vpc]
}
```

### Versioned Modules (Registry/Git)

```hcl
# Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"
}

# Git (specific tag)
module "vpc" {
  source = "git::https://github.com/myorg/terraform-modules.git//vpc?ref=v1.2.0"
}

# Git (specific branch)
module "vpc" {
  source = "git::https://github.com/myorg/terraform-modules.git//vpc?ref=feature/new-vpc"
}

# S3 bucket
module "vpc" {
  source = "s3::https://s3-eu-west-1.amazonaws.com/mybucket/vpc.zip"
}
```

## Resource Patterns

### Count vs for_each

**Count (index-based, positional):**
```hcl
# Use for homogeneous resources
resource "aws_instance" "web" {
  count = var.instance_count

  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "web-${count.index + 1}"
  }
}
```

**for_each (key-based, stable):**
```hcl
# Use for heterogeneous resources or when order doesn't matter
resource "aws_instance" "services" {
  for_each = toset(["api", "worker", "scheduler"])

  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = each.key
    Role = each.value
  }
}

# With map
resource "aws_instance" "app" {
  for_each = {
    api    = "t3.medium"
    worker = "t3.large"
    cache  = "t3.small"
  }

  ami           = var.ami_id
  instance_type = each.value

  tags = {
    Name = each.key
  }
}
```

**When to use which:**
| Use Case | Recommendation |
|----------|----------------|
| Fixed number of identical resources | `count` |
| Resources from a list/set | `for_each` |
| Resources from a map | `for_each` |
| Resources where order matters | `count` |
| Resources that may be added/removed | `for_each` |

### Dynamic Blocks

```hcl
# Dynamic ingress rules
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Variable definition
variable "ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTP"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS"
    }
  ]
}
```

### Conditional Resources

```hcl
# Create resource conditionally
resource "aws_nat_gateway" "main" {
  count = var.enable_nat_gateway ? 1 : 0

  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id
}

# Reference conditional resource
resource "aws_route" "private_nat" {
  count = var.enable_nat_gateway ? length(var.private_subnets) : 0

  route_table_id         = aws_route_table.private[count.index].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main[0].id
}
```

### Lifecycle Rules

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    # Create new before destroying old (blue-green)
    create_before_destroy = true

    # Prevent destruction (data protection)
    prevent_destroy = true

    # Ignore external changes (drift tolerance)
    ignore_changes = [
      tags["LastUpdated"],
      user_data,
    ]

    # Replace when these change
    replace_triggered_by = [
      aws_security_group.web.id
    ]
  }
}
```

### Data Sources

```hcl
# Get latest AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Get availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Get current region
data "aws_region" "current" {}

# Get caller identity
data "aws_caller_identity" "current" {}

# External data (script output)
data "external" "version" {
  program = ["bash", "-c", "echo '{\"version\": \"'$(git describe --tags --always)'\"}'" ]
}
```

## Workspaces

### Workspace Commands

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new staging

# Select workspace
terraform workspace select production

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete staging
```

### Workspace-Aware Configuration

```hcl
# Use workspace name in configuration
locals {
  environment = terraform.workspace

  instance_types = {
    dev        = "t3.micro"
    staging    = "t3.small"
    production = "t3.medium"
  }

  instance_counts = {
    dev        = 1
    staging    = 2
    production = 3
  }
}

resource "aws_instance" "web" {
  count         = local.instance_counts[local.environment]
  instance_type = local.instance_types[local.environment]

  tags = {
    Environment = local.environment
  }
}
```

### State Per Workspace

```hcl
# backend.tf with workspace interpolation
terraform {
  backend "s3" {
    bucket = "mycompany-terraform-state"
    key    = "app/${terraform.workspace}/terraform.tfstate"
    region = "us-east-1"
  }
}
```

**Note**: Workspaces are best for small differences. For significant environment differences, use separate directories.

## Environment Management

### Directory-Based (Recommended)

```
environments/
├── dev/
│   ├── main.tf
│   ├── terraform.tfvars
│   └── backend.tf
├── staging/
│   ├── main.tf
│   ├── terraform.tfvars
│   └── backend.tf
└── production/
    ├── main.tf
    ├── terraform.tfvars
    └── backend.tf
```

**Benefits:**
- Clear separation of concerns
- Different IAM permissions per environment
- Easy to add/remove environments
- Independent state files

### Variable Files

```hcl
# environments/production/terraform.tfvars
environment = "production"
region      = "us-east-1"

vpc_cidr = "10.0.0.0/16"

instance_type  = "t3.medium"
instance_count = 3

enable_monitoring = true
enable_backups    = true

tags = {
  Team       = "platform"
  CostCenter = "prod-infrastructure"
}
```

**Loading Variables:**
```bash
# Auto-loaded: terraform.tfvars, *.auto.tfvars
terraform apply

# Explicit file
terraform apply -var-file="production.tfvars"

# Command line
terraform apply -var="instance_count=5"

# Environment variable
export TF_VAR_instance_count=5
terraform apply
```

## Security Patterns

### Sensitive Variables

```hcl
variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

# Pass via environment
# export TF_VAR_db_password="supersecret"

# Or via file (not committed)
# terraform apply -var-file="secrets.tfvars"
```

### IAM Least Privilege

```hcl
# Terraform execution role (minimal permissions)
data "aws_iam_policy_document" "terraform_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "terraform" {
  name               = "terraform-execution"
  assume_role_policy = data.aws_iam_policy_document.terraform_assume.json
}

# Scoped permissions (not AdministratorAccess)
resource "aws_iam_role_policy_attachment" "terraform" {
  role       = aws_iam_role.terraform.name
  policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"  # Or custom policy
}
```

### Encryption

```hcl
# KMS key for encryption
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
      }
    ]
  })
}

# Encrypted S3 bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.main.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# Encrypted RDS
resource "aws_db_instance" "main" {
  storage_encrypted = true
  kms_key_id        = aws_kms_key.main.arn
}
```

## Testing and Validation

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.5
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_docs
      - id: terraform_tfsec
      - id: terrascan
```

### Terraform Validate

```bash
# Initialize (required before validate)
terraform init

# Validate configuration
terraform validate

# Output: Success! The configuration is valid.
```

### TFLint

```hcl
# .tflint.hcl
plugin "aws" {
  enabled = true
  version = "0.27.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}
```

```bash
tflint --init
tflint
```

### Checkov (Security Scanning)

```bash
# Scan directory
checkov -d .

# Scan specific file
checkov -f main.tf

# Skip specific checks
checkov -d . --skip-check CKV_AWS_18,CKV_AWS_21
```

### Terratest (Integration Testing)

```go
// test/vpc_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPC(t *testing.T) {
    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "environment": "test",
            "vpc_cidr":    "10.99.0.0/16",
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcID)
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infrastructure/**']
  pull_request:
    branches: [main]
    paths: ['infrastructure/**']

env:
  TF_VERSION: '1.5.0'
  AWS_REGION: 'us-east-1'

jobs:
  plan:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: infrastructure/environments/production

    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActions
          aws-region: ${{ env.AWS_REGION }}

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan -out=tfplan

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: infrastructure/environments/production/tfplan

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Download Plan
        uses: actions/download-artifact@v4
        with:
          name: tfplan
          path: infrastructure/environments/production

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActions
          aws-region: ${{ env.AWS_REGION }}

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure/environments/production

      - name: Terraform Apply
        run: terraform apply -auto-approve tfplan
        working-directory: infrastructure/environments/production
```

## Anti-Patterns

**NEVER do these:**

### 1. Hardcoded Credentials

```hcl
# NEVER
provider "aws" {
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# Use environment variables or IAM roles instead
```

### 2. State in Version Control

```bash
# .gitignore must include:
*.tfstate
*.tfstate.*
.terraform/
*.tfvars  # If contains secrets
```

### 3. Unpinned Versions

```hcl
# NEVER
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

# Always pin versions
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### 4. Large Monolithic Configurations

```hcl
# NEVER - Everything in one file
# main.tf with 5000 lines

# Use modules and separate environments
module "vpc" { source = "../../modules/vpc" }
module "eks" { source = "../../modules/eks" }
module "rds" { source = "../../modules/rds" }
```

### 5. Manual State Manipulation

```bash
# NEVER edit state files manually
# Use terraform state commands instead
terraform state mv
terraform state rm
terraform import
```

---

## Quick Reference

**Essential Commands:**
```bash
terraform init              # Initialize working directory
terraform plan              # Preview changes
terraform apply             # Apply changes
terraform destroy           # Destroy resources
terraform fmt               # Format code
terraform validate          # Validate configuration
terraform output            # Show outputs
terraform state list        # List resources in state
terraform import            # Import existing resource
terraform workspace         # Manage workspaces
```

**Debugging:**
```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform apply

# Log to file
export TF_LOG_PATH=terraform.log
```

**Lock Provider Versions:**
```bash
terraform providers lock -platform=linux_amd64 -platform=darwin_amd64
```

---

Apply these patterns to build maintainable, secure, scalable infrastructure. Prioritize modularity (reusable modules), safety (remote state, version pinning), and operational excellence (testing, CI/CD integration).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

