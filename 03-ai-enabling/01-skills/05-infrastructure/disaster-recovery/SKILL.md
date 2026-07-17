---
last_updated: 2026-02-25
status: active
name: disaster-recovery
description: Backup strategies, RTO/RPO planning, and failover patterns. Use when designing business continuity solutions.
triggers:
  files: ["**/backup*.yaml", "**/dr-*", "**/disaster-recovery/**", "**/failover*"]
  keywords: ["disaster recovery", "DR", "backup", "RTO", "RPO", "failover", "business continuity", "high availability"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides disaster recovery planning and implementation for resilient systems. Apply these patterns when designing backup strategies, failover mechanisms, or business continuity plans.

The user provides DR requirements: RTO/RPO targets, critical systems, compliance requirements, or budget constraints.

## Core Principles

Disaster recovery is built on five pillars:

1. **Define RTO/RPO**: Know recovery objectives before designing.
2. **Automate**: Manual recovery fails under pressure.
3. **Test Regularly**: Untested backups aren't backups.
4. **Document**: Runbooks for every scenario.
5. **Layer Protection**: Multiple recovery strategies.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Key Metrics

| Metric | Definition | Example |
|--------|------------|---------|
| RTO | Recovery Time Objective - max acceptable downtime | 4 hours |
| RPO | Recovery Point Objective - max acceptable data loss | 1 hour |
| MTTR | Mean Time To Recovery | 30 minutes |
| MTBF | Mean Time Between Failures | 6 months |

## DR Strategy Tiers

| Tier | Strategy | RTO | RPO | Cost |
|------|----------|-----|-----|------|
| 1 | Backup & Restore | Hours-Days | Hours | $ |
| 2 | Pilot Light | Hours | Minutes | $$ |
| 3 | Warm Standby | Minutes | Minutes | $$$ |
| 4 | Hot Standby/Active-Active | Seconds | Near-zero | $$$$ |

## Backup Strategies

### 3-2-1 Rule

```
3 copies of data
2 different storage types
1 offsite copy
```

### AWS Backup Configuration

```hcl
# AWS Backup plan
resource "aws_backup_plan" "main" {
  name = "production-backup-plan"

  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 5 * * ? *)"  # Daily at 5 AM

    lifecycle {
      cold_storage_after = 30
      delete_after       = 365
    }

    copy_action {
      destination_vault_arn = aws_backup_vault.dr_region.arn
      lifecycle {
        delete_after = 90
      }
    }
  }

  rule {
    rule_name         = "hourly-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 * * * ? *)"  # Hourly

    lifecycle {
      delete_after = 7
    }
  }

  advanced_backup_setting {
    backup_options = {
      WindowsVSS = "enabled"
    }
    resource_type = "EC2"
  }
}

# Backup selection
resource "aws_backup_selection" "main" {
  name         = "production-resources"
  plan_id      = aws_backup_plan.main.id
  iam_role_arn = aws_iam_role.backup.arn

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}
```

### Database Backup (PostgreSQL)

```yaml
# Kubernetes CronJob for PostgreSQL backup
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: postgres:15
              command:
                - /bin/sh
                - -c
                - |
                  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                  pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | \
                    gzip | \
                    aws s3 cp - s3://$BACKUP_BUCKET/postgres/$TIMESTAMP.sql.gz

                  # Cleanup old backups (keep 7 days)
                  aws s3 ls s3://$BACKUP_BUCKET/postgres/ | \
                    awk '{print $4}' | \
                    sort -r | \
                    tail -n +169 | \
                    xargs -I {} aws s3 rm s3://$BACKUP_BUCKET/postgres/{}
              env:
                - name: DB_HOST
                  value: postgres.database.svc
                - name: DB_USER
                  valueFrom:
                    secretKeyRef:
                      name: postgres-credentials
                      key: username
                - name: PGPASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: postgres-credentials
                      key: password
                - name: DB_NAME
                  value: production
                - name: BACKUP_BUCKET
                  value: my-backups
          restartPolicy: OnFailure
```

## Failover Patterns

### Multi-Region Architecture

```hcl
# Primary region
provider "aws" {
  alias  = "primary"
  region = "us-east-1"
}

# DR region
provider "aws" {
  alias  = "dr"
  region = "us-west-2"
}

# Route 53 health check
resource "aws_route53_health_check" "primary" {
  fqdn              = "api.us-east-1.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "primary-health-check"
  }
}

# DNS failover
resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.example.com"
  type    = "A"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier  = "primary"
  health_check_id = aws_route53_health_check.primary.id

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "api_secondary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.example.com"
  type    = "A"

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "secondary"

  alias {
    name                   = aws_lb.dr.dns_name
    zone_id                = aws_lb.dr.zone_id
    evaluate_target_health = true
  }
}
```

### Database Replication

```hcl
# RDS with read replica in DR region
resource "aws_db_instance" "primary" {
  provider               = aws.primary
  identifier            = "production-db"
  engine                = "postgres"
  engine_version        = "15"
  instance_class        = "db.r6g.large"
  allocated_storage     = 100
  storage_encrypted     = true
  kms_key_id           = aws_kms_key.primary.arn

  backup_retention_period = 7
  backup_window          = "03:00-04:00"

  multi_az = true

  tags = {
    Name = "production-db-primary"
  }
}

resource "aws_db_instance" "replica" {
  provider             = aws.dr
  identifier          = "production-db-replica"
  replicate_source_db = aws_db_instance.primary.arn
  instance_class      = "db.r6g.large"

  kms_key_id = aws_kms_key.dr.arn

  tags = {
    Name = "production-db-dr-replica"
  }
}
```

## Recovery Procedures

### Failover Runbook Template

```markdown
# Failover Runbook: Database

## Trigger Conditions
- Primary database unreachable for > 5 minutes
- Primary region experiencing outage
- Corruption detected in primary

## Pre-Failover Checklist
- [ ] Confirm primary is actually down (not network issue)
- [ ] Notify stakeholders
- [ ] Verify replica is in sync (check replication lag)
- [ ] Confirm DR region resources are healthy

## Failover Steps

### 1. Stop Writes to Primary (2 min)
```bash
# Scale down applications
kubectl scale deployment api --replicas=0

# Verify no active connections
psql -h primary.db -c "SELECT count(*) FROM pg_stat_activity WHERE state='active';"
```

### 2. Promote Replica (5 min)
```bash
# AWS CLI to promote
aws rds promote-read-replica --db-instance-identifier production-db-replica

# Wait for promotion
aws rds wait db-instance-available --db-instance-identifier production-db-replica
```

### 3. Update DNS (2 min)
```bash
# Update Route53 to point to DR
aws route53 change-resource-record-sets --hosted-zone-id ZONE_ID --change-batch file://failover-dns.json
```

### 4. Verify and Scale Up (5 min)
```bash
# Test connectivity
psql -h dr.db -c "SELECT 1;"

# Scale applications
kubectl scale deployment api --replicas=3

# Run smoke tests
./scripts/smoke-test.sh
```

## Post-Failover
- [ ] Update monitoring to watch DR
- [ ] Document timeline and decisions
- [ ] Plan failback procedure
- [ ] Conduct post-incident review
```

## Testing DR

### Types of DR Tests

| Test Type | Description | Frequency |
|-----------|-------------|-----------|
| Tabletop | Walk through runbooks | Monthly |
| Component | Test individual backups | Weekly |
| Partial | Failover non-critical systems | Quarterly |
| Full | Complete DR activation | Annually |

### Chaos Engineering

```yaml
# Chaos Mesh - Pod failure injection
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill-test
  namespace: chaos-testing
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      app: api
  duration: "60s"
  scheduler:
    cron: "@every 24h"
```

```yaml
# Network partition test
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-partition
spec:
  action: partition
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      app: api
  direction: both
  target:
    selector:
      namespaces:
        - production
      labelSelectors:
        app: database
  duration: "30s"
```

## Recovery Automation

### Automated Failover Script

```python
#!/usr/bin/env python3
"""Automated DR failover with safety checks."""

import boto3
import time
import sys

class DRFailover:
    def __init__(self, config):
        self.rds = boto3.client('rds', region_name=config['dr_region'])
        self.route53 = boto3.client('route53')
        self.config = config

    def check_primary_health(self):
        """Verify primary is actually unhealthy."""
        # Multiple checks to avoid false positives
        for _ in range(3):
            if self._ping_database(self.config['primary_endpoint']):
                return True
            time.sleep(10)
        return False

    def check_replica_lag(self):
        """Ensure replica is caught up."""
        response = self.rds.describe_db_instances(
            DBInstanceIdentifier=self.config['replica_id']
        )
        lag = response['DBInstances'][0].get('ReplicaLag', 0)
        return lag < 60  # Less than 60 seconds

    def promote_replica(self):
        """Promote read replica to standalone."""
        self.rds.promote_read_replica(
            DBInstanceIdentifier=self.config['replica_id']
        )

        waiter = self.rds.get_waiter('db_instance_available')
        waiter.wait(DBInstanceIdentifier=self.config['replica_id'])

    def update_dns(self):
        """Update Route53 to point to DR."""
        self.route53.change_resource_record_sets(
            HostedZoneId=self.config['zone_id'],
            ChangeBatch={
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': self.config['dns_name'],
                        'Type': 'CNAME',
                        'TTL': 60,
                        'ResourceRecords': [
                            {'Value': self.config['dr_endpoint']}
                        ]
                    }
                }]
            }
        )

    def execute(self):
        """Run failover with safety checks."""
        print("Starting DR failover...")

        if self.check_primary_health():
            print("ERROR: Primary appears healthy. Aborting.")
            sys.exit(1)

        if not self.check_replica_lag():
            print("WARNING: Replica lag detected. Data loss possible.")
            # Could add confirmation prompt here

        print("Promoting replica...")
        self.promote_replica()

        print("Updating DNS...")
        self.update_dns()

        print("Failover complete!")
```

## Checklist

### Pre-Disaster

- [ ] RTO/RPO defined and documented
- [ ] Backup strategy implemented
- [ ] Cross-region replication configured
- [ ] Runbooks written and tested
- [ ] Monitoring and alerting in place
- [ ] Team trained on procedures

### During Disaster

- [ ] Incident declared and communicated
- [ ] Runbook being followed
- [ ] Stakeholders updated
- [ ] Changes logged
- [ ] Recovery validated

### Post-Disaster

- [ ] Root cause analysis
- [ ] Runbooks updated
- [ ] Failback planned
- [ ] Lessons learned documented
- [ ] DR test scheduled

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Untested backups | Regular restore tests |
| Manual failover | Automated with safety checks |
| Single region | Multi-region or multi-cloud |
| No runbooks | Documented, tested procedures |
| RPO/RTO undefined | Clear objectives with stakeholders |

---

Apply these patterns for resilient disaster recovery. Start by defining RTO/RPO with stakeholders, implement appropriate backup strategy, automate failover where possible, and test regularly.


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

