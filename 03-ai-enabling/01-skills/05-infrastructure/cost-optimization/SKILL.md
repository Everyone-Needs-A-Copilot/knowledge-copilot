---
last_updated: 2026-02-25
status: active
name: cost-optimization
description: Cloud cost management, resource rightsizing, and FinOps patterns. Use when optimizing infrastructure spending.
triggers:
  files: ["**/cost*.yaml", "**/budget*", "**/finops/**", "**/savings-plan*"]
  keywords: ["cost optimization", "FinOps", "rightsizing", "reserved instances", "spot instances", "cloud costs", "budget"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides cloud cost optimization using FinOps principles. Apply these patterns when reducing infrastructure costs, implementing chargebacks, or optimizing resource utilization.

The user provides cost requirements: budget constraints, utilization targets, or specific services to optimize.

## Core Principles

Cost optimization is built on five pillars:

1. **Visibility**: You can't optimize what you can't see.
2. **Accountability**: Teams own their costs.
3. **Right-sizing**: Match resources to actual usage.
4. **Commitment**: Reserved capacity for predictable workloads.
5. **Architecture**: Design for cost efficiency.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Cost Visibility

### AWS Cost Allocation Tags

```hcl
# Terraform - Enforce tagging
resource "aws_organizations_policy" "require_tags" {
  name        = "RequireCostAllocationTags"
  description = "Require cost allocation tags"
  type        = "TAG_POLICY"

  content = jsonencode({
    tags = {
      Environment = {
        tag_key = {
          @@assign = "Environment"
        }
        tag_value = {
          @@assign = ["production", "staging", "development"]
        }
        enforced_for = {
          @@assign = ["ec2:instance", "rds:db", "s3:bucket"]
        }
      }
      Team = {
        tag_key = {
          @@assign = "Team"
        }
        enforced_for = {
          @@assign = ["ec2:instance", "rds:db"]
        }
      }
      CostCenter = {
        tag_key = {
          @@assign = "CostCenter"
        }
        enforced_for = {
          @@assign = ["*"]
        }
      }
    }
  })
}
```

### Budget Alerts

```hcl
# AWS Budget with alerts
resource "aws_budgets_budget" "monthly" {
  name         = "monthly-budget"
  budget_type  = "COST"
  limit_amount = "10000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "TagKeyValue"
    values = ["user:Environment$production"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["platform-team@example.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type            = "PERCENTAGE"
    notification_type         = "FORECASTED"
    subscriber_email_addresses = ["platform-team@example.com", "cto@example.com"]
  }
}
```

### Cost Explorer Query

```python
import boto3
from datetime import datetime, timedelta

ce = boto3.client('ce')

def get_cost_by_service(days=30):
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {'Type': 'DIMENSION', 'Key': 'SERVICE'},
            {'Type': 'TAG', 'Key': 'Team'}
        ]
    )

    return response['ResultsByTime']
```

## Compute Optimization

### Right-sizing Recommendations

```python
import boto3

def get_rightsizing_recommendations():
    ce = boto3.client('ce')

    response = ce.get_rightsizing_recommendation(
        Service='AmazonEC2',
        Configuration={
            'RecommendationTarget': 'SAME_INSTANCE_FAMILY',
            'BenefitsConsidered': True
        }
    )

    for rec in response['RightsizingRecommendations']:
        current = rec['CurrentInstance']
        target = rec['ModifyRecommendationDetail']['TargetInstances'][0]
        savings = rec['ModifyRecommendationDetail']['EstimatedMonthlySavings']

        print(f"Current: {current['InstanceType']} -> Recommended: {target['InstanceType']}")
        print(f"Monthly savings: ${savings['Amount']}")
```

### Spot Instances

```hcl
# EKS Node Group with Spot
resource "aws_eks_node_group" "spot" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "spot-workers"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = aws_subnet.private[*].id

  capacity_type = "SPOT"

  instance_types = [
    "m5.large",
    "m5a.large",
    "m5d.large",
    "m5n.large",
    "m5ad.large"
  ]

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 1
  }

  labels = {
    "node-type" = "spot"
  }

  taint {
    key    = "spot"
    value  = "true"
    effect = "NO_SCHEDULE"
  }
}
```

### Kubernetes Spot Toleration

```yaml
# Deployment using spot instances
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
spec:
  template:
    spec:
      tolerations:
        - key: "spot"
          operator: "Equal"
          value: "true"
          effect: "NoSchedule"
      nodeSelector:
        node-type: spot
      containers:
        - name: processor
          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "1000m"
              memory: "2Gi"
```

## Reserved Capacity

### Savings Plans vs Reserved Instances

| Feature | Savings Plans | Reserved Instances |
|---------|---------------|-------------------|
| Flexibility | High (any size) | Low (specific size) |
| Discount | Up to 72% | Up to 75% |
| Applies to | EC2, Fargate, Lambda | EC2, RDS, ElastiCache |
| Term | 1 or 3 years | 1 or 3 years |

### Coverage Analysis

```python
def analyze_commitment_coverage():
    ce = boto3.client('ce')

    # Get Savings Plans coverage
    sp_coverage = ce.get_savings_plans_coverage(
        TimePeriod={
            'Start': '2024-01-01',
            'End': '2024-01-31'
        },
        Granularity='MONTHLY'
    )

    coverage = sp_coverage['SavingsPlansCoverages'][0]['Coverage']
    print(f"Covered: {coverage['SpendCoveredBySavingsPlans']}")
    print(f"On-Demand: {coverage['OnDemandCost']}")
    print(f"Coverage %: {coverage['CoveragePercentage']}%")
```

## Storage Optimization

### S3 Lifecycle Policies

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }

    expiration {
      days = 2555  # 7 years for compliance
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }

  rule {
    id     = "abort-incomplete-uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}
```

### S3 Intelligent Tiering

```hcl
resource "aws_s3_bucket_intelligent_tiering_configuration" "main" {
  bucket = aws_s3_bucket.main.id
  name   = "entire-bucket"

  tiering {
    access_tier = "DEEP_ARCHIVE_ACCESS"
    days        = 180
  }

  tiering {
    access_tier = "ARCHIVE_ACCESS"
    days        = 90
  }
}
```

### EBS Optimization

```python
def find_unattached_volumes():
    ec2 = boto3.client('ec2')

    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )

    total_savings = 0
    for vol in volumes['Volumes']:
        size = vol['Size']
        vol_type = vol['VolumeType']

        # Approximate monthly cost
        cost = size * 0.10  # gp2 pricing
        total_savings += cost

        print(f"Volume {vol['VolumeId']}: {size}GB ({vol_type}) - ${cost:.2f}/mo")

    print(f"\nTotal potential savings: ${total_savings:.2f}/mo")
```

## Database Optimization

### RDS Right-sizing

```python
def analyze_rds_utilization():
    cw = boto3.client('cloudwatch')
    rds = boto3.client('rds')

    instances = rds.describe_db_instances()

    for db in instances['DBInstances']:
        # Get CPU utilization
        cpu = cw.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': db['DBInstanceIdentifier']}],
            StartTime=datetime.now() - timedelta(days=14),
            EndTime=datetime.now(),
            Period=3600,
            Statistics=['Average', 'Maximum']
        )

        avg_cpu = sum(p['Average'] for p in cpu['Datapoints']) / len(cpu['Datapoints'])
        max_cpu = max(p['Maximum'] for p in cpu['Datapoints'])

        if avg_cpu < 20 and max_cpu < 50:
            print(f"{db['DBInstanceIdentifier']}: Consider downsizing (Avg CPU: {avg_cpu:.1f}%, Max: {max_cpu:.1f}%)")
```

### Aurora Serverless

```hcl
# Cost-efficient for variable workloads
resource "aws_rds_cluster" "serverless" {
  cluster_identifier = "aurora-serverless"
  engine             = "aurora-mysql"
  engine_mode        = "provisioned"  # Aurora Serverless v2

  serverlessv2_scaling_configuration {
    max_capacity = 16
    min_capacity = 0.5  # Scale to near-zero when idle
  }
}

resource "aws_rds_cluster_instance" "serverless" {
  cluster_identifier = aws_rds_cluster.serverless.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.serverless.engine
}
```

## Kubernetes Cost Optimization

### Resource Requests/Limits

```yaml
# Vertical Pod Autoscaler for right-sizing
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: "*"
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2
          memory: 4Gi
```

### Cluster Autoscaler

```yaml
# Scale nodes based on pending pods
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-config
data:
  config: |
    {
      "cluster-name": "production",
      "skip-nodes-with-local-storage": true,
      "skip-nodes-with-system-pods": true,
      "scale-down-enabled": true,
      "scale-down-delay-after-add": "10m",
      "scale-down-unneeded-time": "10m",
      "scale-down-utilization-threshold": "0.5"
    }
```

## Cost Optimization Checklist

### Quick Wins (Days)

- [ ] Delete unattached EBS volumes
- [ ] Remove unused Elastic IPs
- [ ] Terminate idle instances
- [ ] Delete old snapshots
- [ ] Clean up unused load balancers

### Medium-term (Weeks)

- [ ] Right-size instances
- [ ] Implement S3 lifecycle policies
- [ ] Purchase Savings Plans
- [ ] Move to Graviton instances
- [ ] Implement Spot for dev/batch

### Strategic (Months)

- [ ] Re-architect for serverless
- [ ] Implement FinOps team
- [ ] Automate cost anomaly detection
- [ ] Implement chargebacks
- [ ] Multi-cloud cost optimization

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Over-provisioning "just in case" | Right-size with autoscaling |
| All on-demand | Mix of reserved + spot |
| No tagging | Enforce cost allocation tags |
| Set and forget | Regular cost reviews |
| Single account | Multi-account for isolation |

## Monthly Cost Review Template

```markdown
# Cost Review - January 2024

## Summary
- Total spend: $X,XXX
- vs. Budget: +/-X%
- vs. Last month: +/-X%

## Top 5 Services by Cost
1. EC2: $X,XXX (XX%)
2. RDS: $X,XXX (XX%)
3. S3: $XXX (XX%)
4. Data Transfer: $XXX (XX%)
5. Lambda: $XXX (XX%)

## Cost Optimization Actions
- [ ] Action 1: Expected savings $XXX/mo
- [ ] Action 2: Expected savings $XXX/mo

## Anomalies Detected
- Service X increased XX% - Reason: ...

## Reserved Capacity Coverage
- Current: XX%
- Target: XX%
- Action: Purchase $X,XXX Savings Plan
```

---

Apply these patterns for sustainable cost optimization. Start with visibility (tagging, budgets), implement quick wins (cleanup), then move to strategic optimization (reserved capacity, architecture).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

