---
last_updated: 2026-02-25
status: active
name: runbook-creation
description: Operational runbooks - incident response, maintenance procedures, troubleshooting guides. Use for operational documentation.
triggers:
  files: ["**/runbooks/**", "**/playbooks/**", "**/docs/operations/**", "**/docs/incidents/**"]
  keywords: ["runbook", "playbook", "incident response", "operations", "on-call", "maintenance procedure", "troubleshooting"]
allowed-tools: Read, Write, Edit
---

# Runbook Creation Skill

Write effective operational runbooks for incident response, maintenance procedures, and troubleshooting. Enable on-call engineers to resolve issues quickly and consistently.

---

## Core Principles

### Runbook Tenets

| Principle | Description |
|-----------|-------------|
| **Actionable** | Every step produces a clear outcome |
| **Self-contained** | All context and commands in one place |
| **Tested** | Procedures verified in staging/prod |
| **Versioned** | Track changes, rollback if needed |
| **Time-boxed** | Clear escalation points |

### Target Audience

Runbooks are for on-call engineers who may be:
- Unfamiliar with the system
- Working at 3 AM under stress
- Following steps exactly as written

Write accordingly: be explicit, provide commands, avoid assumptions.

---

## Runbook Structure

### Standard Template

```markdown
# Runbook: [Title]

**Last Updated**: YYYY-MM-DD
**Owner**: @team-name
**Reviewed**: YYYY-MM-DD

## Overview

One paragraph: What this runbook addresses, when to use it.


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## Prerequisites

- [ ] Access to production systems
- [ ] VPN connected
- [ ] Required tools installed

## Symptoms

How to recognize this issue:
- Alert name: `alert_name`
- Error message: `specific error text`
- Dashboard: [link to dashboard]

## Severity Assessment

| Condition | Severity | Response Time |
|-----------|----------|---------------|
| All users affected | P1 | Immediate |
| Some users affected | P2 | 15 minutes |
| No user impact | P3 | 1 hour |

## Resolution Steps

### Step 1: Verify the Issue

```bash
# Command to verify
kubectl get pods -n production | grep -v Running
```

**Expected**: List of pods not in Running state
**If different**: Go to [Escalation](#escalation)

### Step 2: Identify Root Cause

[Diagnostic steps...]

### Step 3: Apply Fix

[Resolution steps...]

### Step 4: Verify Resolution

[Verification steps...]

## Rollback

If the fix causes additional issues:

```bash
# Rollback command
kubectl rollout undo deployment/api -n production
```

## Escalation

| Condition | Contact | Channel |
|-----------|---------|---------|
| Not resolved in 15 min | @senior-engineer | #incidents |
| Data loss suspected | @on-call-manager | #incidents + phone |
| Security incident | @security-team | #security-incidents |

## Post-Incident

- [ ] Update this runbook if steps were inaccurate
- [ ] Create post-mortem if P1/P2
- [ ] File tickets for automation opportunities

## Related Runbooks

- [Database Failover](./database-failover.md)
- [Service Restart](./service-restart.md)

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2024-01-15 | @engineer | Added rollback section |
| 2024-01-01 | @engineer | Initial version |
```

---

## Incident Response Runbook

### Example: API High Error Rate

```markdown
# Runbook: API High Error Rate

**Last Updated**: 2024-01-15
**Owner**: @backend-team
**Reviewed**: 2024-01-10

## Overview

Resolve alerts when API error rate exceeds 1%. This runbook covers
diagnosis and resolution for common causes: bad deploys, database
issues, and external service failures.

## Prerequisites

- [ ] SSH access to production bastion
- [ ] kubectl configured for prod cluster
- [ ] Grafana access

## Symptoms

- **Alert**: `api_error_rate_high`
- **Threshold**: >1% 5xx errors over 5 minutes
- **Dashboard**: [API Health Dashboard](https://grafana.example.com/d/api-health)

## Severity Assessment

| Error Rate | User Impact | Severity |
|------------|-------------|----------|
| >10% | Major outage | P1 |
| 5-10% | Degraded experience | P2 |
| 1-5% | Minor impact | P3 |

## Resolution Steps

### Step 1: Confirm Alert

```bash
# Check current error rate
curl -s https://api.example.com/health | jq '.error_rate'
```

**Expected**: Number > 0.01 (1%)
**If <0.01**: Alert may have auto-resolved, monitor for 15 min

### Step 2: Check Recent Deployments

```bash
# List recent deployments
kubectl rollout history deployment/api -n production | head -10
```

**If deployed in last 30 minutes**: Likely cause. Go to [Rollback Deploy](#rollback-deploy).

### Step 3: Check Database Health

```bash
# Check database connections
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"
```

**Expected**: <100 connections
**If >100**: Go to [Database Connection Pool Exhausted](./db-connections.md)

### Step 4: Check External Services

```bash
# Check external service health
curl -s https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_KEY" | jq '.error'
```

**If error**: External service down. Enable fallback or wait.

### Step 5: Check Logs

```bash
# Get recent error logs
kubectl logs -l app=api -n production --since=10m | grep -i error | head -50
```

**Look for**:
- Connection refused (network issue)
- Timeout (slow dependency)
- OOM (memory issue)
- Panic/exception (code bug)

### Rollback Deploy

If recent deployment is the cause:

```bash
# Rollback to previous version
kubectl rollout undo deployment/api -n production

# Verify rollback
kubectl rollout status deployment/api -n production

# Check error rate
curl -s https://api.example.com/health | jq '.error_rate'
```

**Expected**: Error rate drops within 2-3 minutes

### Step 6: Verify Resolution

1. Error rate below 1% for 5 minutes
2. No new error alerts
3. Spot-check API endpoints manually

```bash
# Test key endpoints
curl -s https://api.example.com/api/topics | jq '.data | length'
curl -s https://api.example.com/api/health | jq '.status'
```

## Escalation

| Condition | Contact | Action |
|-----------|---------|--------|
| Not resolved in 15 min | @senior-backend | Page via PagerDuty |
| Requires database change | @dba-oncall | Add to incident channel |
| Security suspected | @security-oncall | Follow security incident process |

## Post-Incident

- [ ] If rollback: Create ticket to fix forward
- [ ] If config issue: Update IaC
- [ ] If new failure mode: Update this runbook
- [ ] If P1/P2: Schedule post-mortem

## Related Runbooks

- [API Pod Restart](./api-pod-restart.md)
- [Database Connection Pool](./db-connections.md)
- [Redis Connection Issues](./redis-issues.md)
```

---

## Maintenance Runbook

### Example: Database Migration

```markdown
# Runbook: Database Migration

**Last Updated**: 2024-01-15
**Owner**: @backend-team
**Reviewed**: 2024-01-10

## Overview

Execute database migrations safely in production. Migrations are run
during low-traffic windows with rollback capability.

## Prerequisites

- [ ] Migration tested in staging
- [ ] Backup completed (verify below)
- [ ] Maintenance window scheduled
- [ ] Rollback script prepared

## Pre-Migration Checklist

### 1. Verify Backup

```bash
# Check latest backup timestamp
aws s3 ls s3://backups/postgres/ | tail -5
```

**Expected**: Backup within last 4 hours

### 2. Check Traffic

```bash
# Current request rate
curl -s http://metrics.internal/api_requests_per_minute
```

**Proceed if**: <100 requests/min (off-peak)

### 3. Notify Team

Post in #engineering:
```
Starting database migration for [ticket-number].
Expected duration: 15 minutes.
Rollback plan ready.
```

## Migration Steps

### Step 1: Enable Maintenance Mode

```bash
# Set maintenance flag
kubectl set env deployment/api MAINTENANCE_MODE=true -n production

# Verify
curl -s https://api.example.com/health | jq '.maintenance_mode'
```

### Step 2: Wait for Traffic to Drain

```bash
# Monitor active connections
watch -n 5 'psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity WHERE state = '\''active'\'';"'
```

**Wait until**: Active connections <5

### Step 3: Run Migration

```bash
# Run migration
cd /app && python manage.py migrate --no-input

# Expected output:
# Operations to perform:
#   Apply all migrations: ...
# Running migrations:
#   Applying app.0042_add_evidence_pinned... OK
```

### Step 4: Verify Migration

```bash
# Check migration status
python manage.py showmigrations | grep -v "\[X\]"
```

**Expected**: Empty output (all migrations applied)

### Step 5: Test Application

```bash
# Run smoke tests
pytest tests/smoke/ -v

# Test critical endpoints
curl -s https://api.example.com/api/topics | jq '.data | length'
```

### Step 6: Disable Maintenance Mode

```bash
# Clear maintenance flag
kubectl set env deployment/api MAINTENANCE_MODE=false -n production

# Verify
curl -s https://api.example.com/health | jq '.maintenance_mode'
```

**Expected**: `false`

## Rollback

If migration fails or causes issues:

```bash
# Rollback last migration
python manage.py migrate app 0041_previous_migration

# Re-run tests
pytest tests/smoke/ -v
```

## Post-Migration

- [ ] Post completion in #engineering
- [ ] Update ticket status
- [ ] Monitor error rate for 30 minutes
- [ ] Document any issues encountered

## Estimated Duration

| Step | Time |
|------|------|
| Pre-checks | 5 min |
| Maintenance mode | 2 min |
| Migration | 5 min |
| Verification | 5 min |
| **Total** | **17 min** |
```

---

## Troubleshooting Runbook

### Example: Service Not Starting

```markdown
# Runbook: Service Not Starting

**Last Updated**: 2024-01-15
**Owner**: @platform-team

## Overview

Diagnose and resolve issues when a service fails to start or
repeatedly crashes (CrashLoopBackOff in Kubernetes).

## Symptoms

- Pod status: `CrashLoopBackOff` or `Error`
- Service unavailable
- Alert: `pod_crash_loop`

## Diagnostic Steps

### Step 1: Check Pod Status

```bash
kubectl get pods -l app=api -n production
```

**Look for**: Status other than `Running`

### Step 2: Check Pod Events

```bash
kubectl describe pod <pod-name> -n production | tail -20
```

**Common issues**:

| Event | Cause | Solution |
|-------|-------|----------|
| `OOMKilled` | Out of memory | Increase memory limit |
| `ImagePullBackOff` | Can't pull image | Check image exists, registry auth |
| `CrashLoopBackOff` | App crashes | Check logs |
| `Pending` | No resources | Scale down other services |

### Step 3: Check Logs

```bash
# Get logs from crashing pod
kubectl logs <pod-name> -n production --previous

# If no previous logs
kubectl logs <pod-name> -n production
```

**Look for**:
- Stack traces
- Connection errors
- Missing environment variables
- Permission errors

### Step 4: Common Fixes

#### Missing Environment Variable

```bash
# Check environment
kubectl exec <pod-name> -n production -- env | sort

# Add missing variable
kubectl set env deployment/api MISSING_VAR=value -n production
```

#### Out of Memory

```bash
# Increase memory limit
kubectl patch deployment api -n production -p '{"spec":{"template":{"spec":{"containers":[{"name":"api","resources":{"limits":{"memory":"2Gi"}}}]}}}}'
```

#### Bad Image

```bash
# Rollback to previous image
kubectl rollout undo deployment/api -n production
```

#### Database Connection

```bash
# Test database connectivity from pod
kubectl exec -it <pod-name> -n production -- psql $DATABASE_URL -c "SELECT 1"
```

## Resolution Verification

```bash
# Watch pod status
kubectl get pods -l app=api -n production -w

# Expected: Running status, 1/1 Ready
```

## Escalation

If not resolved in 20 minutes, escalate to @platform-oncall.
```

---

## Writing Guidelines

### Command Formatting

Always use code blocks with copy-paste-ready commands:

```bash
# Good: Complete command
kubectl logs -l app=api -n production --since=10m | grep ERROR

# Bad: Placeholder that requires editing
kubectl logs <pod> -n <namespace>
```

### Expected Outcomes

Every command should state expected output:

```bash
# Check service health
curl -s https://api.example.com/health | jq '.status'
```

**Expected**: `"healthy"`
**If different**: Service may be degraded, continue to Step 2.

### Decision Points

Use tables for decision trees:

| Condition | Action |
|-----------|--------|
| Error rate <1% | Monitor, no action needed |
| Error rate 1-5% | Continue to Step 2 |
| Error rate >5% | Skip to [Emergency Response](#emergency) |

### Time Boxes

Include time expectations:

**Time limit**: 15 minutes before escalation

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Vague commands** | "Check the logs" | Provide exact command |
| **Missing context** | Assumes system knowledge | Include all prerequisites |
| **No verification** | Can't confirm fix worked | Add verification step |
| **No rollback** | Stuck if fix fails | Always include rollback |
| **Outdated** | Commands don't work | Test quarterly, version control |
| **Too long** | Hard to follow at 3 AM | Split into focused runbooks |

---

## Runbook Maintenance

### Quarterly Review

- [ ] Test all commands in staging
- [ ] Update screenshots/dashboards
- [ ] Remove obsolete procedures
- [ ] Add new failure modes discovered

### Post-Incident Updates

After every incident:
1. Did the runbook help?
2. What steps were missing?
3. What steps were wrong?
4. Update immediately while fresh

---

## Checklist

Before publishing a runbook:

- [ ] Every step has a command or action
- [ ] Expected outcomes documented
- [ ] Rollback procedure included
- [ ] Escalation path defined
- [ ] Tested in staging environment
- [ ] Reviewed by team member
- [ ] Added to runbook index

---

This skill enables clear, actionable operational runbooks that help on-call engineers resolve issues quickly and safely.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

