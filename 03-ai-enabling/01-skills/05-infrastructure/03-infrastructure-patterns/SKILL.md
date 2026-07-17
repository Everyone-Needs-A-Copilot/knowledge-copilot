---
last_updated: 2026-02-25
status: active
name: infrastructure-patterns
description: Infrastructure as Code - Terraform, scaling, monitoring, cloud patterns. Use for infrastructure design.
triggers:
  files: ["**/terraform/**", "**/infrastructure/**", "**/*.tf", "**/pulumi/**"]
  keywords: ["terraform", "infrastructure as code", "IaC", "scaling", "monitoring", "cloud", "AWS", "GCP", "load balancer"]
allowed-tools: Read, Write, Edit
---

# Infrastructure Patterns

Comprehensive guide to Infrastructure as Code (IaC), cloud architecture patterns, scaling strategies, and operational excellence.

## Table of Contents

1. [Infrastructure as Code Fundamentals](#infrastructure-as-code-fundamentals)
2. [Terraform Patterns](#terraform-patterns)
3. [Cloud Architecture Patterns](#cloud-architecture-patterns)
4. [Scaling Strategies](#scaling-strategies)
5. [Monitoring and Observability](#monitoring-and-observability)
6. [Security Infrastructure](#security-infrastructure)
7. [Disaster Recovery and Business Continuity](#disaster-recovery-and-business-continuity)
8. [Cost Optimization](#cost-optimization)
9. [Anti-Patterns](#anti-patterns)

---


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Infrastructure as Code Fundamentals

### Core Principles

**Declarative over Imperative**
```hcl
# Good: Declarative - describe desired state
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"

  tags = {
    Name        = "web-server"
    Environment = var.environment
  }
}

# Avoid: Imperative scripts that execute commands
# aws ec2 run-instances --image-id ami-xxx --instance-type t3.medium
```

**Immutable Infrastructure**
```hcl
# Good: Replace instances instead of modifying them
resource "aws_launch_template" "app" {
  name_prefix   = "app-"
  image_id      = var.ami_id  # New AMI = new instances
  instance_type = "t3.medium"

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    version = var.app_version
  }))

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "app" {
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  min_size         = 2
  max_size         = 10
  desired_capacity = 3

  # Replace all instances on template change
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
    }
  }
}
```

**Version Control Everything**
```
infrastructure/
├── .gitignore              # Exclude sensitive files
├── README.md               # Setup and usage docs
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── prod/
│       ├── main.tf
│       ├── terraform.tfvars
│       └── backend.tf
├── modules/
│   ├── vpc/
│   ├── compute/
│   ├── database/
│   └── monitoring/
└── global/
    ├── iam/
    ├── route53/
    └── s3/
```

**.gitignore for IaC**
```gitignore
# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl
terraform.tfvars
override.tf
override.tf.json

# Sensitive files
*.pem
*.key
*.crt
secrets.yaml
credentials.json

# Pulumi
Pulumi.*.yaml
.pulumi/

# Environment files
.env
.env.local
```

---

## Terraform Patterns

### Module Design

**Well-Structured Module**
```hcl
# modules/vpc/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Input validation
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be valid IPv4 CIDR block"
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least 2 availability zones required for HA"
  }
}

variable "environment" {
  description = "Environment name"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

# Default tags applied to all resources
variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}

# Local values for computed attributes
locals {
  common_tags = merge(
    var.tags,
    {
      Environment = var.environment
      ManagedBy   = "terraform"
      Module      = "vpc"
    }
  )

  # Calculate subnet CIDRs
  subnet_count = length(var.availability_zones)
  subnet_bits  = ceil(log(local.subnet_count * 3, 2))  # 3 subnets per AZ

  public_subnet_cidrs = [
    for i in range(local.subnet_count) :
    cidrsubnet(var.vpc_cidr, local.subnet_bits, i)
  ]

  private_subnet_cidrs = [
    for i in range(local.subnet_count) :
    cidrsubnet(var.vpc_cidr, local.subnet_bits, i + local.subnet_count)
  ]

  database_subnet_cidrs = [
    for i in range(local.subnet_count) :
    cidrsubnet(var.vpc_cidr, local.subnet_bits, i + (local.subnet_count * 2))
  ]
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-vpc"
    }
  )
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-igw"
    }
  )
}

# Public Subnets
resource "aws_subnet" "public" {
  count = local.subnet_count

  vpc_id                  = aws_vpc.main.id
  cidr_block              = local.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-public-${var.availability_zones[count.index]}"
      Type = "public"
    }
  )
}

# Private Subnets
resource "aws_subnet" "private" {
  count = local.subnet_count

  vpc_id            = aws_vpc.main.id
  cidr_block        = local.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-private-${var.availability_zones[count.index]}"
      Type = "private"
    }
  )
}

# Database Subnets
resource "aws_subnet" "database" {
  count = local.subnet_count

  vpc_id            = aws_vpc.main.id
  cidr_block        = local.database_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-database-${var.availability_zones[count.index]}"
      Type = "database"
    }
  )
}

# Elastic IPs for NAT Gateways
resource "aws_eip" "nat" {
  count = local.subnet_count

  domain = "vpc"

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-nat-eip-${var.availability_zones[count.index]}"
    }
  )

  depends_on = [aws_internet_gateway.main]
}

# NAT Gateways
resource "aws_nat_gateway" "main" {
  count = local.subnet_count

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-nat-${var.availability_zones[count.index]}"
    }
  )
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-public-rt"
    }
  )
}

resource "aws_route_table" "private" {
  count = local.subnet_count

  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-private-rt-${var.availability_zones[count.index]}"
    }
  )
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count = local.subnet_count

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = local.subnet_count

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# Outputs with descriptions
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "database_subnet_ids" {
  description = "List of database subnet IDs"
  value       = aws_subnet.database[*].id
}

output "nat_gateway_ips" {
  description = "Elastic IPs of NAT gateways"
  value       = aws_eip.nat[*].public_ip
}
```

### State Management

**Remote State with Locking**
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"

    # Use IAM role for authentication
    role_arn = "arn:aws:iam::123456789012:role/TerraformBackend"
  }
}

# Create backend resources (run once)
# backend-setup/main.tf
resource "aws_s3_bucket" "terraform_state" {
  bucket = "company-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
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
      sse_algorithm = "AES256"
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

resource "aws_dynamodb_table" "terraform_state_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }
}
```

**State Data Sources**
```hcl
# Reference outputs from other state files
data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket   = "company-terraform-state"
    key      = "prod/vpc/terraform.tfstate"
    region   = "us-east-1"
    role_arn = "arn:aws:iam::123456789012:role/TerraformBackend"
  }
}

data "terraform_remote_state" "database" {
  backend = "s3"

  config = {
    bucket   = "company-terraform-state"
    key      = "prod/database/terraform.tfstate"
    region   = "us-east-1"
    role_arn = "arn:aws:iam::123456789012:role/TerraformBackend"
  }
}

# Use outputs from other states
resource "aws_security_group" "app" {
  name_prefix = "app-"
  vpc_id      = data.terraform_remote_state.vpc.outputs.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.terraform_remote_state.vpc.outputs.vpc_cidr]
  }
}

resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  subnet_id     = data.terraform_remote_state.vpc.outputs.private_subnet_ids[0]

  environment_variables = {
    DB_HOST = data.terraform_remote_state.database.outputs.endpoint
  }
}
```

### Workspace Strategies

**Environment-Based Workspaces**
```hcl
# Use workspaces for environment separation
# terraform workspace new dev
# terraform workspace new staging
# terraform workspace new prod

locals {
  environment = terraform.workspace

  # Environment-specific configuration
  config = {
    dev = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 3
      db_instance   = "db.t3.small"
    }
    staging = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 5
      db_instance   = "db.t3.medium"
    }
    prod = {
      instance_type = "t3.large"
      min_size      = 3
      max_size      = 10
      db_instance   = "db.r5.xlarge"
    }
  }

  env_config = local.config[local.environment]
}

resource "aws_autoscaling_group" "app" {
  name     = "${local.environment}-app-asg"
  min_size = local.env_config.min_size
  max_size = local.env_config.max_size

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "Environment"
    value               = local.environment
    propagate_at_launch = true
  }
}
```

**Directory-Based Environments (Preferred)**
```
infrastructure/
├── modules/
│   ├── app/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── database/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev/
    │   ├── main.tf
    │   ├── terraform.tfvars
    │   └── backend.tf
    ├── staging/
    │   ├── main.tf
    │   ├── terraform.tfvars
    │   └── backend.tf
    └── prod/
        ├── main.tf
        ├── terraform.tfvars
        └── backend.tf

# environments/prod/main.tf
module "app" {
  source = "../../modules/app"

  environment       = "prod"
  instance_type     = "t3.large"
  min_size          = 3
  max_size          = 10
  vpc_id            = data.terraform_remote_state.vpc.outputs.vpc_id
  subnet_ids        = data.terraform_remote_state.vpc.outputs.private_subnet_ids
}

# environments/prod/terraform.tfvars
region          = "us-east-1"
instance_type   = "t3.large"
min_size        = 3
max_size        = 10
```

### Advanced Patterns

**Dynamic Blocks**
```hcl
# Good: Dynamic blocks for repeating nested blocks
variable "ingress_rules" {
  description = "Map of ingress rules"
  type = map(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
}

resource "aws_security_group" "app" {
  name_prefix = "app-"
  vpc_id      = var.vpc_id

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
}

# terraform.tfvars
ingress_rules = {
  http = {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP"
  }
  https = {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS"
  }
  ssh = {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
    description = "Allow SSH from VPN"
  }
}
```

**Conditional Resources**
```hcl
# Create resources conditionally
variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring"
  type        = bool
  default     = false
}

variable "enable_backup" {
  description = "Enable automated backups"
  type        = bool
  default     = false
}

resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.enable_monitoring ? 1 : 0

  alarm_name          = "${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
}

resource "aws_backup_plan" "daily" {
  count = var.enable_backup ? 1 : 0

  name = "${var.environment}-daily-backup"

  rule {
    rule_name         = "daily_backup"
    target_vault_name = aws_backup_vault.main[0].name
    schedule          = "cron(0 2 * * ? *)"

    lifecycle {
      delete_after = 30
    }
  }
}

resource "aws_backup_vault" "main" {
  count = var.enable_backup ? 1 : 0

  name = "${var.environment}-backup-vault"
}
```

**For-Each with Maps**
```hcl
# Create multiple similar resources from a map
variable "applications" {
  description = "Map of applications to deploy"
  type = map(object({
    instance_type = string
    min_size      = number
    max_size      = number
    port          = number
  }))
}

# Create ASG for each application
resource "aws_autoscaling_group" "apps" {
  for_each = var.applications

  name     = "${var.environment}-${each.key}-asg"
  min_size = each.value.min_size
  max_size = each.value.max_size

  launch_template {
    id      = aws_launch_template.apps[each.key].id
    version = "$Latest"
  }

  tag {
    key                 = "Application"
    value               = each.key
    propagate_at_launch = true
  }
}

# Create target group for each application
resource "aws_lb_target_group" "apps" {
  for_each = var.applications

  name     = "${var.environment}-${each.key}-tg"
  port     = each.value.port
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# terraform.tfvars
applications = {
  api = {
    instance_type = "t3.medium"
    min_size      = 2
    max_size      = 8
    port          = 8000
  }
  worker = {
    instance_type = "t3.small"
    min_size      = 1
    max_size      = 5
    port          = 8001
  }
  admin = {
    instance_type = "t3.small"
    min_size      = 1
    max_size      = 3
    port          = 3000
  }
}
```

---

## Cloud Architecture Patterns

### High Availability Architecture

**Multi-AZ Application Stack**
```hcl
# Load Balancer spanning multiple AZs
resource "aws_lb" "app" {
  name               = "${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "prod"
  enable_http2              = true
  enable_cross_zone_load_balancing = true

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.bucket
    enabled = true
  }
}

# Target groups for blue/green deployments
resource "aws_lb_target_group" "blue" {
  name     = "${var.environment}-blue-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  deregistration_delay = 30

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
}

resource "aws_lb_target_group" "green" {
  name     = "${var.environment}-green-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  deregistration_delay = 30

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
}

# Listener with weighted routing
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = var.certificate_arn

  default_action {
    type = "forward"

    forward {
      target_group {
        arn    = aws_lb_target_group.blue.arn
        weight = 90
      }

      target_group {
        arn    = aws_lb_target_group.green.arn
        weight = 10
      }

      stickiness {
        enabled  = true
        duration = 3600
      }
    }
  }
}

# Auto Scaling Group with multiple AZs
resource "aws_autoscaling_group" "app" {
  name = "${var.environment}-app-asg"

  min_size         = 3
  max_size         = 12
  desired_capacity = 3

  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.blue.arn]

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  health_check_type         = "ELB"
  health_check_grace_period = 300

  # Ensure even distribution across AZs
  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupTotalInstances"
  ]

  # Lifecycle hooks for graceful shutdown
  initial_lifecycle_hook {
    name                 = "instance-terminating"
    default_result       = "CONTINUE"
    heartbeat_timeout    = 300
    lifecycle_transition = "autoscaling:EC2_INSTANCE_TERMINATING"
  }

  tag {
    key                 = "Name"
    value               = "${var.environment}-app"
    propagate_at_launch = true
  }
}

# Multi-AZ RDS
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-db"

  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.r5.xlarge"

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  multi_az               = true
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  deletion_protection = var.environment == "prod"
  skip_final_snapshot = var.environment != "prod"

  final_snapshot_identifier = var.environment == "prod" ? "${var.environment}-db-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null
}

# Read replicas for scaling reads
resource "aws_db_instance" "replica" {
  count = var.environment == "prod" ? 2 : 0

  identifier = "${var.environment}-db-replica-${count.index + 1}"

  replicate_source_db = aws_db_instance.main.identifier
  instance_class      = "db.r5.large"

  publicly_accessible = false

  tags = {
    Name        = "${var.environment}-db-replica-${count.index + 1}"
    Environment = var.environment
  }
}
```

### Multi-Region Architecture

**Cross-Region Replication**
```hcl
# Primary region
provider "aws" {
  alias  = "primary"
  region = "us-east-1"
}

# Secondary region
provider "aws" {
  alias  = "secondary"
  region = "us-west-2"
}

# S3 bucket with cross-region replication
resource "aws_s3_bucket" "primary" {
  provider = aws.primary
  bucket   = "${var.company}-data-primary"
}

resource "aws_s3_bucket_versioning" "primary" {
  provider = aws.primary
  bucket   = aws_s3_bucket.primary.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "secondary" {
  provider = aws.secondary
  bucket   = "${var.company}-data-secondary"
}

resource "aws_s3_bucket_versioning" "secondary" {
  provider = aws.secondary
  bucket   = aws_s3_bucket.secondary.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_replication_configuration" "primary" {
  provider = aws.primary

  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.primary.id

  rule {
    id     = "replicate-all"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.secondary.arn
      storage_class = "STANDARD_IA"

      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }

      metrics {
        status = "Enabled"
        event_threshold {
          minutes = 15
        }
      }
    }
  }
}

# Global DynamoDB table
resource "aws_dynamodb_table" "global" {
  provider = aws.primary

  name         = "${var.environment}-sessions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "SessionId"

  attribute {
    name = "SessionId"
    type = "S"
  }

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  replica {
    region_name = "us-west-2"
  }

  replica {
    region_name = "eu-west-1"
  }
}

# Route53 health checks and failover
resource "aws_route53_health_check" "primary" {
  fqdn              = aws_lb.primary.dns_name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = "3"
  request_interval  = "30"

  tags = {
    Name = "${var.environment}-primary-health-check"
  }
}

resource "aws_route53_health_check" "secondary" {
  fqdn              = aws_lb.secondary.dns_name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = "3"
  request_interval  = "30"

  tags = {
    Name = "${var.environment}-secondary-health-check"
  }
}

resource "aws_route53_record" "primary" {
  zone_id = var.route53_zone_id
  name    = "app.example.com"
  type    = "A"

  set_identifier = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.primary.id
}

resource "aws_route53_record" "secondary" {
  zone_id = var.route53_zone_id
  name    = "app.example.com"
  type    = "A"

  set_identifier = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  alias {
    name                   = aws_lb.secondary.dns_name
    zone_id                = aws_lb.secondary.zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.secondary.id
}
```

### CDN and Caching Architecture

**CloudFront with Origin Failover**
```hcl
# CloudFront distribution with multiple origins
resource "aws_cloudfront_distribution" "app" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${var.environment} CDN"
  default_root_object = "index.html"
  price_class         = "PriceClass_100"  # US, Canada, Europe

  aliases = ["app.example.com"]

  # Primary origin (ALB)
  origin {
    domain_name = aws_lb.primary.dns_name
    origin_id   = "primary-alb"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    custom_header {
      name  = "X-CloudFront-Secret"
      value = var.cloudfront_secret
    }
  }

  # Failover origin
  origin {
    domain_name = aws_lb.secondary.dns_name
    origin_id   = "secondary-alb"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    custom_header {
      name  = "X-CloudFront-Secret"
      value = var.cloudfront_secret
    }
  }

  # S3 origin for static assets
  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "static-s3"
    origin_path = "/assets"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.static.cloudfront_access_identity_path
    }
  }

  # Origin group with failover
  origin_group {
    origin_id = "alb-group"

    failover_criteria {
      status_codes = [500, 502, 503, 504]
    }

    member {
      origin_id = "primary-alb"
    }

    member {
      origin_id = "secondary-alb"
    }
  }

  # Default cache behavior (dynamic content)
  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "alb-group"

    forwarded_values {
      query_string = true
      headers      = ["Host", "Authorization", "CloudFront-Forwarded-Proto"]

      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
    compress               = true

    # Lambda@Edge for custom logic
    lambda_function_association {
      event_type   = "viewer-request"
      lambda_arn   = aws_lambda_function.edge_auth.qualified_arn
      include_body = false
    }
  }

  # Static assets cache behavior
  ordered_cache_behavior {
    path_pattern     = "/static/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "static-s3"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400   # 1 day
    max_ttl                = 31536000 # 1 year
    compress               = true
  }

  # API cache behavior (shorter TTL)
  ordered_cache_behavior {
    path_pattern     = "/api/*"
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "alb-group"

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Accept", "Content-Type"]

      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 60   # 1 minute
    max_ttl                = 300  # 5 minutes
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  custom_error_response {
    error_code            = 404
    response_code         = 404
    response_page_path    = "/404.html"
    error_caching_min_ttl = 300
  }

  custom_error_response {
    error_code            = 500
    response_code         = 500
    response_page_path    = "/500.html"
    error_caching_min_ttl = 0
  }

  logging_config {
    include_cookies = false
    bucket          = aws_s3_bucket.cdn_logs.bucket_domain_name
    prefix          = "cloudfront/"
  }

  tags = {
    Environment = var.environment
  }
}

# ElastiCache for session storage
resource "aws_elasticache_replication_group" "session" {
  replication_group_id       = "${var.environment}-sessions"
  replication_group_description = "Session storage cluster"

  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.r5.large"
  number_cache_clusters = 3

  port = 6379

  parameter_group_name = aws_elasticache_parameter_group.redis.name
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.redis_auth_token

  automatic_failover_enabled = true
  multi_az_enabled          = true

  snapshot_retention_limit = 5
  snapshot_window          = "03:00-05:00"
  maintenance_window       = "sun:05:00-sun:07:00"

  notification_topic_arn = aws_sns_topic.alerts.arn

  tags = {
    Environment = var.environment
  }
}
```

---

## Scaling Strategies

### Auto Scaling Policies

**Target Tracking Scaling**
```hcl
# CPU-based scaling
resource "aws_autoscaling_policy" "cpu_target" {
  name                   = "${var.environment}-cpu-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }

    target_value = 70.0
  }
}

# Request count per target scaling
resource "aws_autoscaling_policy" "request_count_target" {
  name                   = "${var.environment}-request-count-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = "${aws_lb.app.arn_suffix}/${aws_lb_target_group.blue.arn_suffix}"
    }

    target_value = 1000.0
  }
}

# Custom metric scaling (queue depth)
resource "aws_autoscaling_policy" "queue_depth_target" {
  name                   = "${var.environment}-queue-depth-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.worker.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    customized_metric_specification {
      metric_dimension {
        name  = "QueueName"
        value = aws_sqs_queue.tasks.name
      }

      metric_name = "ApproximateNumberOfMessagesVisible"
      namespace   = "AWS/SQS"
      statistic   = "Average"
      unit        = "Count"
    }

    target_value = 100.0
  }
}
```

**Step Scaling for Rapid Changes**
```hcl
# Scale up quickly under heavy load
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.environment}-scale-up"
  autoscaling_group_name = aws_autoscaling_group.app.name
  adjustment_type        = "PercentChangeInCapacity"
  policy_type            = "StepScaling"

  step_adjustment {
    scaling_adjustment          = 10
    metric_interval_lower_bound = 0
    metric_interval_upper_bound = 10
  }

  step_adjustment {
    scaling_adjustment          = 20
    metric_interval_lower_bound = 10
    metric_interval_upper_bound = 20
  }

  step_adjustment {
    scaling_adjustment          = 30
    metric_interval_lower_bound = 20
  }
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.environment}-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = "70"
  alarm_description   = "Triggers scale up when CPU is high"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}

# Scale down conservatively
resource "aws_autoscaling_policy" "scale_down" {
  name                   = "${var.environment}-scale-down"
  autoscaling_group_name = aws_autoscaling_group.app.name
  adjustment_type        = "ChangeInCapacity"
  policy_type            = "StepScaling"

  step_adjustment {
    scaling_adjustment          = -1
    metric_interval_upper_bound = 0
  }
}

resource "aws_cloudwatch_metric_alarm" "cpu_low" {
  alarm_name          = "${var.environment}-cpu-low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "10"  # Wait longer before scaling down
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "20"
  alarm_description   = "Triggers scale down when CPU is low"
  alarm_actions       = [aws_autoscaling_policy.scale_down.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}
```

**Scheduled Scaling**
```hcl
# Scale up for business hours
resource "aws_autoscaling_schedule" "scale_up_morning" {
  scheduled_action_name  = "${var.environment}-scale-up-morning"
  min_size               = 5
  max_size               = 20
  desired_capacity       = 10
  recurrence             = "0 7 * * MON-FRI"  # 7 AM weekdays
  time_zone              = "America/New_York"
  autoscaling_group_name = aws_autoscaling_group.app.name
}

# Scale down for evening
resource "aws_autoscaling_schedule" "scale_down_evening" {
  scheduled_action_name  = "${var.environment}-scale-down-evening"
  min_size               = 2
  max_size               = 10
  desired_capacity       = 3
  recurrence             = "0 19 * * MON-FRI"  # 7 PM weekdays
  time_zone              = "America/New_York"
  autoscaling_group_name = aws_autoscaling_group.app.name
}

# Minimum capacity for weekends
resource "aws_autoscaling_schedule" "scale_down_weekend" {
  scheduled_action_name  = "${var.environment}-scale-down-weekend"
  min_size               = 1
  max_size               = 5
  desired_capacity       = 2
  recurrence             = "0 0 * * SAT"  # Midnight Saturday
  time_zone              = "America/New_York"
  autoscaling_group_name = aws_autoscaling_group.app.name
}
```

### Database Scaling

**RDS Auto Scaling Storage**
```hcl
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-db"

  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.r5.xlarge"

  allocated_storage     = 100
  max_allocated_storage = 1000  # Auto-scale up to 1TB
  storage_type          = "gp3"
  iops                  = 3000
  storage_throughput    = 125

  # Enable Performance Insights
  performance_insights_enabled    = true
  performance_insights_retention_period = 7

  # Enable enhanced monitoring
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring.arn

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
}

# Read replica auto scaling
resource "aws_appautoscaling_target" "rds_replicas" {
  max_capacity       = 5
  min_capacity       = 1
  resource_id        = "cluster:${aws_rds_cluster.main.cluster_identifier}"
  scalable_dimension = "rds:cluster:ReadReplicaCount"
  service_namespace  = "rds"
}

resource "aws_appautoscaling_policy" "rds_replicas" {
  name               = "${var.environment}-rds-replica-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.rds_replicas.resource_id
  scalable_dimension = aws_appautoscaling_target.rds_replicas.scalable_dimension
  service_namespace  = aws_appautoscaling_target.rds_replicas.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "RDSReaderAverageCPUUtilization"
    }

    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

### Container Orchestration Scaling

**ECS Service Auto Scaling**
```hcl
# ECS Service
resource "aws_ecs_service" "app" {
  name            = "${var.environment}-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3

  launch_type = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8000
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }
}

# Auto Scaling Target
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = 20
  min_capacity       = 3
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# CPU-based scaling
resource "aws_appautoscaling_policy" "ecs_cpu" {
  name               = "${var.environment}-ecs-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# Memory-based scaling
resource "aws_appautoscaling_policy" "ecs_memory" {
  name               = "${var.environment}-ecs-memory-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }

    target_value       = 80.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# ALB request count scaling
resource "aws_appautoscaling_policy" "ecs_requests" {
  name               = "${var.environment}-ecs-requests-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = "${aws_lb.app.arn_suffix}/${aws_lb_target_group.app.arn_suffix}"
    }

    target_value       = 1000.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

---

## Monitoring and Observability

### Prometheus and Grafana Stack

**ECS Deployment of Monitoring Stack**
```hcl
# Prometheus ECS Task Definition
resource "aws_ecs_task_definition" "prometheus" {
  family                   = "${var.environment}-prometheus"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.prometheus.arn

  container_definitions = jsonencode([
    {
      name  = "prometheus"
      image = "prom/prometheus:latest"

      portMappings = [
        {
          containerPort = 9090
          protocol      = "tcp"
        }
      ]

      mountPoints = [
        {
          sourceVolume  = "prometheus-data"
          containerPath = "/prometheus"
        },
        {
          sourceVolume  = "prometheus-config"
          containerPath = "/etc/prometheus"
        }
      ]

      command = [
        "--config.file=/etc/prometheus/prometheus.yml",
        "--storage.tsdb.path=/prometheus",
        "--storage.tsdb.retention.time=30d",
        "--web.enable-lifecycle"
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.prometheus.name
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "prometheus"
        }
      }
    }
  ])

  volume {
    name = "prometheus-data"

    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.prometheus.id
      transit_encryption = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.prometheus_data.id
      }
    }
  }

  volume {
    name = "prometheus-config"

    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.prometheus.id
      transit_encryption = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.prometheus_config.id
      }
    }
  }
}

# Grafana ECS Task Definition
resource "aws_ecs_task_definition" "grafana" {
  family                   = "${var.environment}-grafana"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution.arn

  container_definitions = jsonencode([
    {
      name  = "grafana"
      image = "grafana/grafana:latest"

      portMappings = [
        {
          containerPort = 3000
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "GF_SECURITY_ADMIN_PASSWORD"
          value = var.grafana_admin_password
        },
        {
          name  = "GF_SERVER_ROOT_URL"
          value = "https://grafana.${var.domain}"
        },
        {
          name  = "GF_DATABASE_TYPE"
          value = "postgres"
        },
        {
          name  = "GF_DATABASE_HOST"
          value = aws_db_instance.main.endpoint
        },
        {
          name  = "GF_DATABASE_NAME"
          value = "grafana"
        }
      ]

      secrets = [
        {
          name      = "GF_DATABASE_PASSWORD"
          valueFrom = aws_secretsmanager_secret.grafana_db_password.arn
        }
      ]

      mountPoints = [
        {
          sourceVolume  = "grafana-data"
          containerPath = "/var/lib/grafana"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.grafana.name
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "grafana"
        }
      }
    }
  ])

  volume {
    name = "grafana-data"

    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.grafana.id
      transit_encryption = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.grafana.id
      }
    }
  }
}

# Prometheus configuration
resource "aws_ssm_parameter" "prometheus_config" {
  name  = "/${var.environment}/prometheus/config"
  type  = "String"
  value = templatefile("${path.module}/templates/prometheus.yml", {
    environment = var.environment
  })
}
```

**Prometheus Configuration Template**
```yaml
# templates/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    environment: ${environment}
    cluster: main

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Rule files
rule_files:
  - /etc/prometheus/rules/*.yml

# Scrape configurations
scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # EC2 service discovery
  - job_name: 'ec2-nodes'
    ec2_sd_configs:
      - region: us-east-1
        port: 9100
        filters:
          - name: tag:Environment
            values: [${environment}]
          - name: tag:Monitoring
            values: ['true']
    relabel_configs:
      - source_labels: [__meta_ec2_tag_Name]
        target_label: instance
      - source_labels: [__meta_ec2_instance_id]
        target_label: instance_id
      - source_labels: [__meta_ec2_availability_zone]
        target_label: availability_zone

  # ECS service discovery
  - job_name: 'ecs-services'
    ecs_sd_configs:
      - region: us-east-1
        cluster: ${environment}-cluster
        refresh_interval: 60s
    relabel_configs:
      - source_labels: [__meta_ecs_task_definition_family]
        target_label: job
      - source_labels: [__meta_ecs_service_name]
        target_label: service
      - source_labels: [__meta_ecs_cluster_name]
        target_label: cluster

  # RDS monitoring
  - job_name: 'rds'
    static_configs:
      - targets: ['cloudwatch-exporter:9106']
    params:
      region: [us-east-1]

  # Application metrics
  - job_name: 'application'
    dns_sd_configs:
      - names:
          - 'app.service.consul'
        type: 'A'
        port: 8000
    metrics_path: '/metrics'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
```

### CloudWatch Dashboards and Alarms

**Comprehensive CloudWatch Dashboard**
```hcl
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.environment}-overview"

  dashboard_body = jsonencode({
    widgets = [
      # Application Load Balancer metrics
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "TargetResponseTime", { stat = "Average" }],
            [".", "RequestCount", { stat = "Sum" }],
            [".", "HTTPCode_Target_2XX_Count", { stat = "Sum" }],
            [".", "HTTPCode_Target_4XX_Count", { stat = "Sum" }],
            [".", "HTTPCode_Target_5XX_Count", { stat = "Sum" }]
          ]
          period = 300
          stat   = "Average"
          region = var.region
          title  = "Load Balancer Metrics"
        }
      },

      # EC2/ECS metrics
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/EC2", "CPUUtilization", { stat = "Average" }],
            ["AWS/ECS", "CPUUtilization", { stat = "Average" }],
            ["AWS/ECS", "MemoryUtilization", { stat = "Average" }]
          ]
          period = 300
          stat   = "Average"
          region = var.region
          title  = "Compute Metrics"
        }
      },

      # RDS metrics
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/RDS", "CPUUtilization", { stat = "Average" }],
            [".", "DatabaseConnections", { stat = "Average" }],
            [".", "ReadLatency", { stat = "Average" }],
            [".", "WriteLatency", { stat = "Average" }],
            [".", "FreeableMemory", { stat = "Average" }]
          ]
          period = 300
          stat   = "Average"
          region = var.region
          title  = "Database Metrics"
        }
      },

      # Custom application metrics
      {
        type = "metric"
        properties = {
          metrics = [
            ["${var.environment}/App", "RequestDuration", { stat = "p99" }],
            [".", "RequestDuration", { stat = "p95" }],
            [".", "RequestDuration", { stat = "p50" }]
          ]
          period = 300
          region = var.region
          title  = "Application Latency Percentiles"
        }
      }
    ]
  })
}

# Composite alarm for overall application health
resource "aws_cloudwatch_composite_alarm" "app_health" {
  alarm_name          = "${var.environment}-app-health"
  alarm_description   = "Overall application health"
  actions_enabled     = true
  alarm_actions       = [aws_sns_topic.critical_alerts.arn]
  ok_actions          = [aws_sns_topic.critical_alerts.arn]

  alarm_rule = "ALARM(${aws_cloudwatch_metric_alarm.high_error_rate.alarm_name}) OR ALARM(${aws_cloudwatch_metric_alarm.high_latency.alarm_name}) OR ALARM(${aws_cloudwatch_metric_alarm.low_healthy_hosts.alarm_name})"
}

# Error rate alarm
resource "aws_cloudwatch_metric_alarm" "high_error_rate" {
  alarm_name          = "${var.environment}-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  threshold           = "5"
  alarm_description   = "Error rate exceeds 5%"
  treat_missing_data  = "notBreaching"

  metric_query {
    id          = "error_rate"
    expression  = "errors / requests * 100"
    label       = "Error Rate"
    return_data = true
  }

  metric_query {
    id = "errors"

    metric {
      metric_name = "HTTPCode_Target_5XX_Count"
      namespace   = "AWS/ApplicationELB"
      period      = "300"
      stat        = "Sum"

      dimensions = {
        LoadBalancer = aws_lb.app.arn_suffix
      }
    }
  }

  metric_query {
    id = "requests"

    metric {
      metric_name = "RequestCount"
      namespace   = "AWS/ApplicationELB"
      period      = "300"
      stat        = "Sum"

      dimensions = {
        LoadBalancer = aws_lb.app.arn_suffix
      }
    }
  }

  alarm_actions = [aws_sns_topic.critical_alerts.arn]
}

# Latency alarm
resource "aws_cloudwatch_metric_alarm" "high_latency" {
  alarm_name          = "${var.environment}-high-latency"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "3"
  metric_name         = "TargetResponseTime"
  namespace           = "AWS/ApplicationELB"
  period              = "300"
  statistic           = "Average"
  threshold           = "1.0"
  alarm_description   = "Average response time exceeds 1 second"

  dimensions = {
    LoadBalancer = aws_lb.app.arn_suffix
  }

  alarm_actions = [aws_sns_topic.critical_alerts.arn]
}

# Healthy host count alarm
resource "aws_cloudwatch_metric_alarm" "low_healthy_hosts" {
  alarm_name          = "${var.environment}-low-healthy-hosts"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "HealthyHostCount"
  namespace           = "AWS/ApplicationELB"
  period              = "60"
  statistic           = "Average"
  threshold           = "2"
  alarm_description   = "Less than 2 healthy hosts available"

  dimensions = {
    LoadBalancer = aws_lb.app.arn_suffix
    TargetGroup  = aws_lb_target_group.blue.arn_suffix
  }

  alarm_actions = [aws_sns_topic.critical_alerts.arn]
}

# Database connection alarm
resource "aws_cloudwatch_metric_alarm" "db_connections_high" {
  alarm_name          = "${var.environment}-db-connections-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Database connection count is high"

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

### Logging Infrastructure

**Centralized Logging with CloudWatch Logs**
```hcl
# Log groups with retention
resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/${var.environment}/app"
  retention_in_days = var.environment == "prod" ? 90 : 30

  kms_key_id = aws_kms_key.logs.arn

  tags = {
    Environment = var.environment
    Application = "app"
  }
}

resource "aws_cloudwatch_log_group" "alb" {
  name              = "/aws/${var.environment}/alb"
  retention_in_days = 30
}

# Metric filters for custom metrics
resource "aws_cloudwatch_log_metric_filter" "error_count" {
  name           = "${var.environment}-error-count"
  log_group_name = aws_cloudwatch_log_group.app.name
  pattern        = "[time, request_id, level = ERROR, ...]"

  metric_transformation {
    name      = "ErrorCount"
    namespace = "${var.environment}/App"
    value     = "1"
    unit      = "Count"
  }
}

resource "aws_cloudwatch_log_metric_filter" "slow_requests" {
  name           = "${var.environment}-slow-requests"
  log_group_name = aws_cloudwatch_log_group.app.name
  pattern        = "[time, request_id, level, msg, duration > 1000, ...]"

  metric_transformation {
    name      = "SlowRequestCount"
    namespace = "${var.environment}/App"
    value     = "1"
    unit      = "Count"
  }
}

# Log subscription to Elasticsearch
resource "aws_cloudwatch_log_subscription_filter" "elasticsearch" {
  name            = "${var.environment}-to-elasticsearch"
  log_group_name  = aws_cloudwatch_log_group.app.name
  filter_pattern  = ""
  destination_arn = aws_lambda_function.logs_to_es.arn
}

# Lambda function to ship logs to Elasticsearch
resource "aws_lambda_function" "logs_to_es" {
  filename      = "logs_to_es.zip"
  function_name = "${var.environment}-logs-to-es"
  role          = aws_iam_role.logs_to_es.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  timeout       = 60

  environment {
    variables = {
      ES_ENDPOINT = aws_elasticsearch_domain.logs.endpoint
    }
  }

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
}
```

**Elasticsearch/OpenSearch for Log Analytics**
```hcl
resource "aws_elasticsearch_domain" "logs" {
  domain_name           = "${var.environment}-logs"
  elasticsearch_version = "7.10"

  cluster_config {
    instance_type            = "r5.large.elasticsearch"
    instance_count           = 3
    zone_awareness_enabled   = true
    dedicated_master_enabled = true
    dedicated_master_type    = "r5.large.elasticsearch"
    dedicated_master_count   = 3

    zone_awareness_config {
      availability_zone_count = 3
    }
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 100
    volume_type = "gp3"
    iops        = 3000
    throughput  = 125
  }

  encrypt_at_rest {
    enabled    = true
    kms_key_id = aws_kms_key.elasticsearch.arn
  }

  node_to_node_encryption {
    enabled = true
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

  vpc_options {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.elasticsearch.id]
  }

  advanced_options = {
    "rest.action.multi.allow_explicit_index" = "true"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.es_application_logs.arn
    log_type                 = "ES_APPLICATION_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.es_slow_logs.arn
    log_type                 = "SEARCH_SLOW_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.es_index_slow_logs.arn
    log_type                 = "INDEX_SLOW_LOGS"
  }

  snapshot_options {
    automated_snapshot_start_hour = 3
  }

  tags = {
    Environment = var.environment
  }
}
```

---

## Security Infrastructure

### Network Security

**Security Groups with Principle of Least Privilege**
```hcl
# ALB security group
resource "aws_security_group" "alb" {
  name_prefix = "${var.environment}-alb-"
  description = "Security group for Application Load Balancer"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP from internet (redirect to HTTPS)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description     = "To application instances"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "${var.environment}-alb-sg"
    Environment = var.environment
  }
}

# Application security group
resource "aws_security_group" "app" {
  name_prefix = "${var.environment}-app-"
  description = "Security group for application instances"
  vpc_id      = var.vpc_id

  ingress {
    description     = "HTTP from ALB"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description     = "To database"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.database.id]
  }

  egress {
    description     = "To Redis"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.redis.id]
  }

  egress {
    description = "HTTPS to internet (for API calls)"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "${var.environment}-app-sg"
    Environment = var.environment
  }
}

# Database security group
resource "aws_security_group" "database" {
  name_prefix = "${var.environment}-db-"
  description = "Security group for RDS database"
  vpc_id      = var.vpc_id

  ingress {
    description     = "PostgreSQL from application"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  ingress {
    description     = "PostgreSQL from bastion"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "${var.environment}-db-sg"
    Environment = var.environment
  }
}

# Bastion security group
resource "aws_security_group" "bastion" {
  name_prefix = "${var.environment}-bastion-"
  description = "Security group for bastion host"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH from office IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.office_ip_ranges
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "${var.environment}-bastion-sg"
    Environment = var.environment
  }
}
```

### Secrets Management

**AWS Secrets Manager Integration**
```hcl
# Database credentials
resource "aws_secretsmanager_secret" "db_credentials" {
  name                    = "${var.environment}/db/credentials"
  description             = "Database credentials"
  recovery_window_in_days = 30

  kms_key_id = aws_kms_key.secrets.arn
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id

  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    engine   = "postgres"
    host     = aws_db_instance.main.endpoint
    port     = 5432
    dbname   = var.db_name
  })
}

# API keys
resource "aws_secretsmanager_secret" "api_keys" {
  name                    = "${var.environment}/api/keys"
  description             = "Third-party API keys"
  recovery_window_in_days = 30

  kms_key_id = aws_kms_key.secrets.arn
}

# Automatic rotation
resource "aws_secretsmanager_secret_rotation" "db_credentials" {
  secret_id           = aws_secretsmanager_secret.db_credentials.id
  rotation_lambda_arn = aws_lambda_function.rotate_secret.arn

  rotation_rules {
    automatically_after_days = 30
  }
}

# Lambda function for secret rotation
resource "aws_lambda_function" "rotate_secret" {
  filename      = "rotate_secret.zip"
  function_name = "${var.environment}-rotate-db-secret"
  role          = aws_iam_role.rotate_secret.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  timeout       = 30

  environment {
    variables = {
      SECRETS_MANAGER_ENDPOINT = "https://secretsmanager.${var.region}.amazonaws.com"
    }
  }

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
}

# Grant ECS tasks access to secrets
resource "aws_iam_role_policy" "ecs_secrets" {
  name = "${var.environment}-ecs-secrets"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "kms:Decrypt"
        ]
        Resource = [
          aws_secretsmanager_secret.db_credentials.arn,
          aws_secretsmanager_secret.api_keys.arn,
          aws_kms_key.secrets.arn
        ]
      }
    ]
  })
}
```

### KMS Encryption

**KMS Key Management**
```hcl
# Application data encryption key
resource "aws_kms_key" "app_data" {
  description             = "${var.environment} application data encryption key"
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
        Sid    = "Allow services to use the key"
        Effect = "Allow"
        Principal = {
          Service = [
            "s3.amazonaws.com",
            "rds.amazonaws.com",
            "logs.amazonaws.com"
          ]
        }
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "*"
      },
      {
        Sid    = "Allow ECS tasks to decrypt"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.ecs_task.arn
        }
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Name        = "${var.environment}-app-data"
    Environment = var.environment
  }
}

resource "aws_kms_alias" "app_data" {
  name          = "alias/${var.environment}-app-data"
  target_key_id = aws_kms_key.app_data.key_id
}

# Secrets encryption key
resource "aws_kms_key" "secrets" {
  description             = "${var.environment} secrets encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name        = "${var.environment}-secrets"
    Environment = var.environment
  }
}

resource "aws_kms_alias" "secrets" {
  name          = "alias/${var.environment}-secrets"
  target_key_id = aws_kms_key.secrets.key_id
}
```

### WAF Configuration

**AWS WAF for Application Protection**
```hcl
resource "aws_wafv2_web_acl" "main" {
  name  = "${var.environment}-waf"
  scope = "REGIONAL"

  default_action {
    allow {}
  }

  # Rate limiting
  rule {
    name     = "rate-limit"
    priority = 1

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
      metric_name                = "RateLimitRule"
      sampled_requests_enabled   = true
    }
  }

  # AWS Managed Rules - Common Rule Set
  rule {
    name     = "aws-common-rule-set"
    priority = 2

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"

        excluded_rule {
          name = "SizeRestrictions_BODY"
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }

  # AWS Managed Rules - SQL Injection
  rule {
    name     = "aws-sql-injection-rule-set"
    priority = 3

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
      metric_name                = "AWSSQLiRuleSet"
      sampled_requests_enabled   = true
    }
  }

  # Block known bad inputs
  rule {
    name     = "block-known-bad-inputs"
    priority = 4

    action {
      block {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSKnownBadInputsRuleSet"
      sampled_requests_enabled   = true
    }
  }

  # Geo-blocking (optional)
  rule {
    name     = "geo-block"
    priority = 5

    action {
      block {}
    }

    statement {
      not_statement {
        statement {
          geo_match_statement {
            country_codes = var.allowed_countries
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "GeoBlockRule"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.environment}WAF"
    sampled_requests_enabled   = true
  }

  tags = {
    Name        = "${var.environment}-waf"
    Environment = var.environment
  }
}

# Associate WAF with ALB
resource "aws_wafv2_web_acl_association" "alb" {
  resource_arn = aws_lb.app.arn
  web_acl_arn  = aws_wafv2_web_acl.main.arn
}

# CloudWatch dashboard for WAF metrics
resource "aws_cloudwatch_dashboard" "waf" {
  dashboard_name = "${var.environment}-waf"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/WAFV2", "BlockedRequests", { stat = "Sum" }],
            [".", "AllowedRequests", { stat = "Sum" }]
          ]
          period = 300
          stat   = "Sum"
          region = var.region
          title  = "WAF Request Status"
        }
      }
    ]
  })
}
```

---

## Disaster Recovery and Business Continuity

### Backup Strategies

**AWS Backup for Automated Backups**
```hcl
# Backup vault
resource "aws_backup_vault" "main" {
  name        = "${var.environment}-backup-vault"
  kms_key_arn = aws_kms_key.backup.arn

  tags = {
    Name        = "${var.environment}-backup-vault"
    Environment = var.environment
  }
}

# Backup plan
resource "aws_backup_plan" "main" {
  name = "${var.environment}-backup-plan"

  # Hourly backups (retained for 1 day)
  rule {
    rule_name         = "hourly_backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 * * * ? *)"

    lifecycle {
      delete_after = 1
    }

    recovery_point_tags = {
      Frequency   = "hourly"
      Environment = var.environment
    }
  }

  # Daily backups (retained for 7 days)
  rule {
    rule_name         = "daily_backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 * * ? *)"

    lifecycle {
      delete_after = 7
    }

    recovery_point_tags = {
      Frequency   = "daily"
      Environment = var.environment
    }
  }

  # Weekly backups (retained for 30 days)
  rule {
    rule_name         = "weekly_backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 ? * SUN *)"

    lifecycle {
      delete_after = 30
    }

    recovery_point_tags = {
      Frequency   = "weekly"
      Environment = var.environment
    }
  }

  # Monthly backups (retained for 365 days)
  rule {
    rule_name         = "monthly_backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 1 * ? *)"

    lifecycle {
      delete_after = 365
    }

    recovery_point_tags = {
      Frequency   = "monthly"
      Environment = var.environment
    }
  }

  tags = {
    Name        = "${var.environment}-backup-plan"
    Environment = var.environment
  }
}

# Backup selection
resource "aws_backup_selection" "main" {
  name         = "${var.environment}-backup-selection"
  plan_id      = aws_backup_plan.main.id
  iam_role_arn = aws_iam_role.backup.arn

  resources = [
    aws_db_instance.main.arn,
    aws_dynamodb_table.sessions.arn,
    aws_efs_file_system.app_data.arn
  ]

  # Select resources by tag
  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Environment"
    value = var.environment
  }
}

# Copy backups to another region
resource "aws_backup_region_settings" "main" {
  resource_type_opt_in_preference = {
    "Aurora"          = true
    "DynamoDB"        = true
    "EBS"             = true
    "EC2"             = true
    "EFS"             = true
    "RDS"             = true
    "Storage Gateway" = true
  }
}

# Cross-region backup copy
resource "aws_backup_vault" "secondary_region" {
  provider = aws.secondary

  name        = "${var.environment}-backup-vault"
  kms_key_arn = aws_kms_key.backup_secondary.arn

  tags = {
    Name        = "${var.environment}-backup-vault-secondary"
    Environment = var.environment
  }
}

# Add copy rule to backup plan
resource "aws_backup_plan" "main_with_copy" {
  name = "${var.environment}-backup-plan"

  rule {
    rule_name         = "daily_backup_with_copy"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 * * ? *)"

    lifecycle {
      delete_after = 7
    }

    copy_action {
      destination_vault_arn = aws_backup_vault.secondary_region.arn

      lifecycle {
        delete_after = 14
      }
    }
  }
}
```

### Database Point-in-Time Recovery

**RDS Automated Backups and PITR**
```hcl
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-db"

  # Enable automated backups
  backup_retention_period = 35  # Maximum for RDS
  backup_window          = "03:00-04:00"

  # Enable automatic minor version upgrades
  auto_minor_version_upgrade = true
  maintenance_window         = "sun:04:00-sun:05:00"

  # Enable deletion protection for production
  deletion_protection = var.environment == "prod"

  # Create final snapshot before deletion
  skip_final_snapshot       = var.environment != "prod"
  final_snapshot_identifier = var.environment == "prod" ? "${var.environment}-db-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null

  # Copy tags to snapshots
  copy_tags_to_snapshot = true

  tags = {
    Name        = "${var.environment}-db"
    Environment = var.environment
    Backup      = "true"
  }
}

# Lambda function for automated snapshot testing
resource "aws_lambda_function" "test_snapshot" {
  filename      = "test_snapshot.zip"
  function_name = "${var.environment}-test-db-snapshot"
  role          = aws_iam_role.test_snapshot.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  timeout       = 900  # 15 minutes

  environment {
    variables = {
      ENVIRONMENT         = var.environment
      DB_INSTANCE_ID      = aws_db_instance.main.id
      NOTIFICATION_TOPIC  = aws_sns_topic.alerts.arn
    }
  }
}

# Schedule weekly snapshot tests
resource "aws_cloudwatch_event_rule" "test_snapshot" {
  name                = "${var.environment}-test-snapshot"
  description         = "Trigger weekly database snapshot test"
  schedule_expression = "cron(0 3 ? * SUN *)"
}

resource "aws_cloudwatch_event_target" "test_snapshot" {
  rule      = aws_cloudwatch_event_rule.test_snapshot.name
  target_id = "TestSnapshot"
  arn       = aws_lambda_function.test_snapshot.arn
}
```

### Disaster Recovery Runbooks

**Automated DR Procedures**
```hcl
# Systems Manager documents for DR procedures
resource "aws_ssm_document" "failover_to_secondary" {
  name          = "${var.environment}-failover-to-secondary"
  document_type = "Automation"

  content = jsonencode({
    schemaVersion = "0.3"
    description   = "Failover to secondary region"

    parameters = {
      PrimaryRegion = {
        type        = "String"
        description = "Primary region"
        default     = "us-east-1"
      }
      SecondaryRegion = {
        type        = "String"
        description = "Secondary region"
        default     = "us-west-2"
      }
    }

    mainSteps = [
      {
        name   = "CheckPrimaryHealth"
        action = "aws:executeScript"
        inputs = {
          Runtime = "python3.8"
          Handler = "check_health"
          Script  = file("${path.module}/scripts/check_health.py")
        }
      },
      {
        name   = "UpdateRoute53"
        action = "aws:executeAwsApi"
        inputs = {
          Service = "route53"
          Api     = "ChangeResourceRecordSets"
          HostedZoneId = var.route53_zone_id
          ChangeBatch = {
            Changes = [
              {
                Action = "UPSERT"
                ResourceRecordSet = {
                  Name = "app.example.com"
                  Type = "A"
                  SetIdentifier = "secondary"
                  Weight = 100
                  AliasTarget = {
                    HostedZoneId = var.secondary_lb_zone_id
                    DNSName = var.secondary_lb_dns_name
                    EvaluateTargetHealth = true
                  }
                }
              }
            ]
          }
        }
      },
      {
        name   = "PromoteSecondaryDatabase"
        action = "aws:executeAwsApi"
        inputs = {
          Service = "rds"
          Api     = "PromoteReadReplica"
          DBInstanceIdentifier = var.secondary_db_instance_id
        }
      },
      {
        name   = "SendNotification"
        action = "aws:executeAwsApi"
        inputs = {
          Service = "sns"
          Api     = "Publish"
          TopicArn = aws_sns_topic.critical_alerts.arn
          Message = "Failover to secondary region completed"
          Subject = "DR Failover Executed"
        }
      }
    ]
  })
}

# Disaster recovery testing schedule
resource "aws_ssm_maintenance_window" "dr_test" {
  name     = "${var.environment}-dr-test"
  schedule = "cron(0 2 ? * SUN#1 *)"  # First Sunday of each month
  duration = 4
  cutoff   = 1

  tags = {
    Name        = "${var.environment}-dr-test"
    Environment = var.environment
  }
}

resource "aws_ssm_maintenance_window_task" "dr_test" {
  window_id        = aws_ssm_maintenance_window.dr_test.id
  task_type        = "AUTOMATION"
  task_arn         = aws_ssm_document.dr_test.arn
  priority         = 1
  service_role_arn = aws_iam_role.ssm_maintenance.arn

  max_concurrency = "1"
  max_errors      = "0"

  targets {
    key    = "WindowTargetIds"
    values = [aws_ssm_maintenance_window_target.dr_test.id]
  }
}
```

---

## Cost Optimization

### Resource Tagging Strategy

**Comprehensive Tagging for Cost Allocation**
```hcl
# Standard tags applied to all resources
locals {
  common_tags = {
    Environment  = var.environment
    Project      = var.project_name
    ManagedBy    = "terraform"
    CostCenter   = var.cost_center
    Owner        = var.owner_email
    CreatedDate  = formatdate("YYYY-MM-DD", timestamp())
  }

  # Environment-specific tags
  environment_tags = {
    dev = {
      AutoShutdown = "true"
      ShutdownTime = "20:00"
      StartupTime  = "07:00"
    }
    staging = {
      AutoShutdown = "false"
    }
    prod = {
      AutoShutdown        = "false"
      BackupRetention     = "30"
      DisasterRecovery    = "true"
      ComplianceRequired  = "true"
    }
  }
}

# Apply tags to resources
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = local.env_config.instance_type

  tags = merge(
    local.common_tags,
    local.environment_tags[var.environment],
    {
      Name        = "${var.environment}-app-${count.index + 1}"
      Application = "web-app"
      Component   = "application-server"
    }
  )

  volume_tags = merge(
    local.common_tags,
    {
      Name = "${var.environment}-app-${count.index + 1}-root"
    }
  )
}

# Cost allocation tags
resource "aws_ce_cost_category" "environment" {
  name         = "Environment"
  rule_version = "CostCategoryExpression.v1"

  rule {
    value = "Production"
    rule {
      tags {
        key    = "Environment"
        values = ["prod"]
      }
    }
  }

  rule {
    value = "Non-Production"
    rule {
      tags {
        key    = "Environment"
        values = ["dev", "staging"]
      }
    }
  }
}
```

### Auto-Shutdown for Non-Production

**Lambda Function for Resource Scheduling**
```hcl
# Lambda function to stop/start resources
resource "aws_lambda_function" "resource_scheduler" {
  filename      = "resource_scheduler.zip"
  function_name = "resource-scheduler"
  role          = aws_iam_role.resource_scheduler.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  timeout       = 300

  environment {
    variables = {
      DRY_RUN = "false"
    }
  }
}

# IAM role for scheduler
resource "aws_iam_role" "resource_scheduler" {
  name = "resource-scheduler"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "resource_scheduler" {
  name = "resource-scheduler-policy"
  role = aws_iam_role.resource_scheduler.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:StopInstances",
          "ec2:StartInstances",
          "rds:DescribeDBInstances",
          "rds:StopDBInstance",
          "rds:StartDBInstance",
          "autoscaling:DescribeAutoScalingGroups",
          "autoscaling:UpdateAutoScalingGroup",
          "ecs:DescribeServices",
          "ecs:UpdateService"
        ]
        Resource = "*"
      }
    ]
  })
}

# Schedule shutdown at 8 PM
resource "aws_cloudwatch_event_rule" "shutdown" {
  name                = "resource-shutdown"
  description         = "Shutdown non-production resources"
  schedule_expression = "cron(0 20 * * ? *)"
}

resource "aws_cloudwatch_event_target" "shutdown" {
  rule      = aws_cloudwatch_event_rule.shutdown.name
  target_id = "ResourceShutdown"
  arn       = aws_lambda_function.resource_scheduler.arn

  input = jsonencode({
    action = "stop"
    filters = {
      tags = {
        AutoShutdown = "true"
      }
    }
  })
}

# Schedule startup at 7 AM
resource "aws_cloudwatch_event_rule" "startup" {
  name                = "resource-startup"
  description         = "Start non-production resources"
  schedule_expression = "cron(0 7 * * ? *)"
}

resource "aws_cloudwatch_event_target" "startup" {
  rule      = aws_cloudwatch_event_rule.startup.name
  target_id = "ResourceStartup"
  arn       = aws_lambda_function.resource_scheduler.arn

  input = jsonencode({
    action = "start"
    filters = {
      tags = {
        AutoShutdown = "true"
      }
    }
  })
}
```

### Reserved Instances and Savings Plans

**Cost Optimization Recommendations**
```hcl
# Cost anomaly detection
resource "aws_ce_anomaly_monitor" "main" {
  name              = "${var.environment}-cost-anomaly-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_subscription" "main" {
  name      = "${var.environment}-cost-anomaly-subscription"
  frequency = "DAILY"

  monitor_arn_list = [
    aws_ce_anomaly_monitor.main.arn
  ]

  subscriber {
    type    = "SNS"
    address = aws_sns_topic.cost_alerts.arn
  }

  threshold {
    expression = "COST"
    value      = 100
  }
}

# Budget alerts
resource "aws_budgets_budget" "monthly" {
  name         = "${var.environment}-monthly-budget"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_limit
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name = "TagKeyValue"
    values = [
      "Environment$${var.environment}"
    ]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = var.budget_alert_emails
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = var.budget_alert_emails
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = var.budget_alert_emails
  }
}
```

### Right-Sizing Recommendations

**CloudWatch Insights for Resource Utilization**
```hcl
# CloudWatch Insights query for underutilized instances
resource "aws_cloudwatch_query_definition" "underutilized_ec2" {
  name = "${var.environment}/ec2/underutilized"

  query_string = <<-EOT
    fields @timestamp, instance_id, avg_cpu, max_cpu
    | filter namespace = "AWS/EC2"
    | stats avg(CPUUtilization) as avg_cpu, max(CPUUtilization) as max_cpu by instance_id
    | filter avg_cpu < 10 and max_cpu < 30
    | sort avg_cpu asc
  EOT

  log_group_names = [
    "/aws/${var.environment}/ec2"
  ]
}

# Trusted Advisor cost optimization checks
data "aws_organizations_organization" "main" {}

# Enable Trusted Advisor notifications
resource "aws_cloudwatch_event_rule" "trusted_advisor" {
  name        = "${var.environment}-trusted-advisor-cost-optimization"
  description = "Trigger on Trusted Advisor cost optimization recommendations"

  event_pattern = jsonencode({
    source      = ["aws.trustedadvisor"]
    detail-type = ["Trusted Advisor Check Item Refresh Notification"]
    detail = {
      check-name = [
        "Low Utilization Amazon EC2 Instances",
        "Underutilized Amazon EBS Volumes",
        "Idle Load Balancers",
        "Unassociated Elastic IP Addresses"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "trusted_advisor" {
  rule      = aws_cloudwatch_event_rule.trusted_advisor.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.cost_optimization.arn
}
```

---

## Anti-Patterns

### What NOT To Do

**1. Hardcoded Credentials**
```hcl
# BAD: Never hardcode credentials
resource "aws_db_instance" "bad" {
  username = "admin"
  password = "SuperSecret123!"  # Never do this!
}

# GOOD: Use Secrets Manager or variables
resource "aws_db_instance" "good" {
  username = var.db_username
  password = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db.id
  secret_string = random_password.db_password.result
}
```

**2. Overly Permissive Security Groups**
```hcl
# BAD: Open to the world
resource "aws_security_group" "bad" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# GOOD: Specific ports and sources
resource "aws_security_group" "good" {
  ingress {
    description     = "HTTPS from ALB only"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
}
```

**3. No State Locking**
```hcl
# BAD: Local state with no locking
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# GOOD: Remote state with locking
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

**4. Count Instead of For-Each for Resources**
```hcl
# BAD: Using count creates fragile indexes
resource "aws_instance" "bad" {
  count         = 3
  ami           = var.ami_id
  instance_type = "t3.medium"
}

# GOOD: Use for_each with stable keys
resource "aws_instance" "good" {
  for_each = {
    web1 = "t3.medium"
    web2 = "t3.medium"
    web3 = "t3.medium"
  }

  ami           = var.ami_id
  instance_type = each.value

  tags = {
    Name = each.key
  }
}
```

**5. No Resource Lifecycle Management**
```hcl
# BAD: Resource can be deleted accidentally
resource "aws_db_instance" "bad" {
  identifier = "production-db"
}

# GOOD: Prevent accidental deletion
resource "aws_db_instance" "good" {
  identifier = "production-db"

  lifecycle {
    prevent_destroy = true
    create_before_destroy = false
  }

  deletion_protection = true
  skip_final_snapshot = false
}
```

**6. Mixing Environments in Same State**
```hcl
# BAD: All environments in one state file
# terraform.tfvars
environments = ["dev", "staging", "prod"]

# GOOD: Separate state files per environment
# environments/prod/backend.tf
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "prod/terraform.tfstate"
  }
}

# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "dev/terraform.tfstate"
  }
}
```

**7. No Monitoring or Alerting**
```hcl
# BAD: Infrastructure with no observability
resource "aws_autoscaling_group" "bad" {
  name     = "app-asg"
  min_size = 2
  max_size = 10
}

# GOOD: Include comprehensive monitoring
resource "aws_autoscaling_group" "good" {
  name     = "app-asg"
  min_size = 2
  max_size = 10

  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupPendingInstances",
    "GroupStandbyInstances",
    "GroupTerminatingInstances",
    "GroupTotalInstances"
  ]

  health_check_type         = "ELB"
  health_check_grace_period = 300
}

resource "aws_cloudwatch_metric_alarm" "good_unhealthy" {
  alarm_name          = "app-unhealthy-instances"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "HealthyHostCount"
  namespace           = "AWS/ApplicationELB"
  period              = "60"
  statistic           = "Average"
  threshold           = "2"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

**8. Single Point of Failure**
```hcl
# BAD: Single AZ deployment
resource "aws_instance" "bad" {
  ami           = var.ami_id
  instance_type = "t3.large"
  subnet_id     = var.subnet_id  # Single subnet
}

# GOOD: Multi-AZ with auto scaling
resource "aws_autoscaling_group" "good" {
  name                = "app-asg"
  vpc_zone_identifier = var.subnet_ids  # Multiple AZs
  min_size            = 3
  max_size            = 10

  health_check_type         = "ELB"
  health_check_grace_period = 300
}

resource "aws_db_instance" "good" {
  identifier = "db"
  multi_az   = true  # Enable multi-AZ
}
```

---

## Best Practices Summary

### Infrastructure Code Organization
- Use modules for reusable components
- Separate environments with directory structure
- Version control everything
- Use remote state with locking
- Implement proper secret management

### High Availability
- Deploy across multiple availability zones
- Use Auto Scaling Groups
- Implement health checks
- Configure automatic failover
- Test disaster recovery procedures

### Security
- Principle of least privilege
- Encrypt data at rest and in transit
- Use security groups effectively
- Implement WAF rules
- Regular security audits

### Monitoring and Operations
- Comprehensive metrics and logs
- Automated alerting
- Dashboards for visibility
- Regular backup testing
- Documented runbooks

### Cost Management
- Tag all resources
- Right-size instances
- Use auto-shutdown for non-prod
- Monitor cost anomalies
- Regular optimization reviews

---

This infrastructure patterns guide provides comprehensive coverage of modern cloud infrastructure practices, from IaC fundamentals to advanced disaster recovery strategies. Always adapt these patterns to your specific requirements and constraints.


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

