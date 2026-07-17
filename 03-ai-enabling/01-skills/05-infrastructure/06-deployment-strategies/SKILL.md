---
last_updated: 2026-02-25
status: active
name: deployment-strategies
description: Blue-green, canary, rolling deployments, and release strategies. Use when designing deployment pipelines.
triggers:
  files: ["**/deployment*.yml", "**/deploy*.sh", "**/release*.yml", "**/rollout*.yml"]
  keywords: ["deployment", "blue-green", "canary", "rolling", "rollback", "release", "deploy", "rollout", "traffic", "zero downtime"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides selection and implementation of deployment strategies for production systems. Apply these patterns when designing release pipelines, minimizing downtime, or implementing rollback capabilities.

The user provides deployment requirements: release strategy selection, zero-downtime deployment, gradual rollouts, or rollback automation.

## Core Principles

Deployment excellence is built on five pillars:

1. **Zero Downtime**: Users never experience service interruption during deployments.
2. **Reversibility**: Every deployment can be rolled back quickly and safely.
3. **Observability**: Real-time visibility into deployment health and impact.
4. **Gradual Rollout**: New versions reach users incrementally, not all at once.
5. **Automation**: Manual steps are eliminated; deployments are reproducible.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Strategy Comparison

| Strategy | Downtime | Rollback Speed | Resource Cost | Complexity | Best For |
|----------|----------|----------------|---------------|------------|----------|
| **Recreate** | Yes | Slow | Low | Low | Dev/test environments |
| **Rolling** | No | Medium | Low | Medium | Stateless apps |
| **Blue-Green** | No | Instant | 2x | Medium | Critical systems |
| **Canary** | No | Fast | Low-Medium | High | High-traffic apps |
| **A/B Testing** | No | Fast | Low-Medium | High | Feature validation |
| **Shadow** | No | N/A | 2x | High | Performance testing |

## Recreate Deployment

**Description**: Stop all old instances, then start new instances.

**Use Case**: Development environments, non-critical services, batch jobs.

```yaml
# Kubernetes: Recreate Strategy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    type: Recreate
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:v2
```

**Characteristics:**
- Simple implementation
- Brief downtime during transition
- All instances run same version
- Lower resource usage

**When to Use:**
- Development/staging environments
- Stateful applications that can't run mixed versions
- Database schema migrations requiring exclusive access
- Cost-sensitive environments where 2x capacity isn't feasible

## Rolling Deployment

**Description**: Gradually replace old instances with new ones, maintaining availability throughout.

### Kubernetes Implementation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max extra pods during update
      maxUnavailable: 1  # Max pods that can be unavailable
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:v2
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
```

**Parameters:**

| Parameter | Description | Recommendation |
|-----------|-------------|----------------|
| `maxSurge` | Extra pods during update | 25% or 1-2 pods |
| `maxUnavailable` | Pods that can be down | 25% or 0 for critical |

### Rolling Update Visualization

```
Initial State (v1):  [v1] [v1] [v1] [v1] [v1]

Step 1:              [v1] [v1] [v1] [v1] [v2] (new pod created)
Step 2:              [v1] [v1] [v1] [v2] [v2] (old pod terminated)
Step 3:              [v1] [v1] [v2] [v2] [v2]
Step 4:              [v1] [v2] [v2] [v2] [v2]
Step 5:              [v2] [v2] [v2] [v2] [v2]

Final State (v2):    [v2] [v2] [v2] [v2] [v2]
```

### Health Checks (Critical)

```yaml
# Readiness probe: Traffic routing decision
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  successThreshold: 1
  failureThreshold: 3

# Liveness probe: Container restart decision
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  successThreshold: 1
  failureThreshold: 3

# Startup probe: Long-starting containers
startupProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 0
  periodSeconds: 10
  failureThreshold: 30  # 300 seconds max startup time
```

### Rollback

```bash
# Kubernetes: Automatic rollback on failure
kubectl rollout status deployment/myapp

# Manual rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=2

# View rollout history
kubectl rollout history deployment/myapp
```

## Blue-Green Deployment

**Description**: Maintain two identical environments (blue = current, green = new). Switch traffic instantly after validation.

### Architecture

```
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌───────────────┐        ┌───────────────┐
      │    Blue       │        │    Green      │
      │   (v1.0)      │        │   (v2.0)      │
      │   [ACTIVE]    │        │   [STANDBY]   │
      └───────────────┘        └───────────────┘
```

### Kubernetes Implementation

```yaml
# Blue deployment (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    app: myapp
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
        - name: myapp
          image: myapp:v1.0

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  labels:
    app: myapp
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
        - name: myapp
          image: myapp:v2.0

---
# Service: Points to active deployment
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Switch to 'green' to change traffic
  ports:
    - port: 80
      targetPort: 8080
```

### Traffic Switch Script

```bash
#!/bin/bash
# switch-traffic.sh

set -e

NAMESPACE=${NAMESPACE:-default}
SERVICE="myapp"
TARGET_VERSION=$1  # blue or green

if [[ "$TARGET_VERSION" != "blue" && "$TARGET_VERSION" != "green" ]]; then
    echo "Usage: $0 <blue|green>"
    exit 1
fi

# Verify target deployment is healthy
echo "Checking $TARGET_VERSION deployment health..."
kubectl rollout status deployment/myapp-$TARGET_VERSION -n $NAMESPACE

# Get pod count
READY_PODS=$(kubectl get deployment myapp-$TARGET_VERSION -n $NAMESPACE -o jsonpath='{.status.readyReplicas}')
DESIRED_PODS=$(kubectl get deployment myapp-$TARGET_VERSION -n $NAMESPACE -o jsonpath='{.spec.replicas}')

if [[ "$READY_PODS" != "$DESIRED_PODS" ]]; then
    echo "ERROR: Not all pods ready ($READY_PODS/$DESIRED_PODS)"
    exit 1
fi

# Switch traffic
echo "Switching traffic to $TARGET_VERSION..."
kubectl patch service $SERVICE -n $NAMESPACE -p "{\"spec\":{\"selector\":{\"version\":\"$TARGET_VERSION\"}}}"

echo "Traffic switched to $TARGET_VERSION"

# Verify
CURRENT=$(kubectl get service $SERVICE -n $NAMESPACE -o jsonpath='{.spec.selector.version}')
echo "Service now pointing to: $CURRENT"
```

### Blue-Green Workflow

```yaml
# GitHub Actions: Blue-Green Deployment
name: Blue-Green Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Determine target environment
        id: target
        run: |
          CURRENT=$(kubectl get svc myapp -o jsonpath='{.spec.selector.version}')
          if [[ "$CURRENT" == "blue" ]]; then
            echo "target=green" >> $GITHUB_OUTPUT
            echo "current=blue" >> $GITHUB_OUTPUT
          else
            echo "target=blue" >> $GITHUB_OUTPUT
            echo "current=green" >> $GITHUB_OUTPUT
          fi

      - name: Deploy to ${{ steps.target.outputs.target }}
        run: |
          kubectl set image deployment/myapp-${{ steps.target.outputs.target }} \
            myapp=${{ env.REGISTRY }}/myapp:${{ github.sha }}
          kubectl rollout status deployment/myapp-${{ steps.target.outputs.target }}

      - name: Run smoke tests
        run: |
          TARGET_IP=$(kubectl get svc myapp-${{ steps.target.outputs.target }}-internal -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
          ./smoke-tests.sh http://$TARGET_IP

      - name: Switch traffic
        run: |
          kubectl patch svc myapp -p '{"spec":{"selector":{"version":"${{ steps.target.outputs.target }}"}}}'

      - name: Monitor for 5 minutes
        run: |
          ./monitor-deployment.sh --duration=300 --threshold=0.01

      - name: Rollback on failure
        if: failure()
        run: |
          kubectl patch svc myapp -p '{"spec":{"selector":{"version":"${{ steps.target.outputs.current }}"}}}'
```

### Advantages

- **Instant rollback**: Just switch the load balancer back
- **Full testing**: New version is fully deployed before receiving traffic
- **Zero downtime**: Traffic switch is atomic

### Disadvantages

- **Double resources**: Need 2x infrastructure during deployment
- **Database migrations**: Tricky if schema changes are incompatible
- **Session handling**: Active sessions may need special handling

## Canary Deployment

**Description**: Route a small percentage of traffic to the new version, gradually increasing if metrics are healthy.

### Architecture

```
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │ 90%                 10% │
              ▼                         ▼
      ┌───────────────┐        ┌───────────────┐
      │   Stable      │        │    Canary     │
      │   (v1.0)      │        │   (v2.0)      │
      │   9 pods      │        │   1 pod       │
      └───────────────┘        └───────────────┘
```

### Kubernetes with Ingress

```yaml
# Canary deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1  # Single canary instance
  selector:
    matchLabels:
      app: myapp
      version: canary
  template:
    metadata:
      labels:
        app: myapp
        version: canary
    spec:
      containers:
        - name: myapp
          image: myapp:v2.0

---
# Stable deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9  # 90% of traffic
  selector:
    matchLabels:
      app: myapp
      version: stable
  template:
    metadata:
      labels:
        app: myapp
        version: stable
    spec:
      containers:
        - name: myapp
          image: myapp:v1.0

---
# NGINX Ingress canary annotation
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"  # 10% to canary
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-canary
                port:
                  number: 80
```

### Istio Service Mesh

```yaml
# VirtualService with traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp.example.com
  http:
    - route:
        - destination:
            host: myapp-stable
            port:
              number: 80
          weight: 90
        - destination:
            host: myapp-canary
            port:
              number: 80
          weight: 10

---
# DestinationRule for subsets
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:
    - name: stable
      labels:
        version: stable
    - name: canary
      labels:
        version: canary
```

### Progressive Rollout with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:v2.0
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: { duration: 5m }
        - setWeight: 25
        - pause: { duration: 5m }
        - setWeight: 50
        - pause: { duration: 5m }
        - setWeight: 75
        - pause: { duration: 5m }
      canaryService: myapp-canary
      stableService: myapp-stable
      trafficRouting:
        nginx:
          stableIngress: myapp-stable
          annotationPrefix: nginx.ingress.kubernetes.io
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 1
        args:
          - name: service-name
            value: myapp-canary

---
# Analysis template for automated rollback
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

### Canary Metrics to Monitor

| Metric | Threshold | Action if Exceeded |
|--------|-----------|-------------------|
| Error rate | > 1% | Pause rollout |
| Latency p99 | > 500ms | Pause rollout |
| CPU usage | > 80% | Scale up or pause |
| Memory usage | > 80% | Scale up or pause |
| 5xx responses | > 0.5% | Rollback |

### Canary Deployment Script

```bash
#!/bin/bash
# canary-deploy.sh

set -e

IMAGE=$1
STEPS=(10 25 50 75 100)
PAUSE_MINUTES=5
ERROR_THRESHOLD=0.01

for WEIGHT in "${STEPS[@]}"; do
    echo "Setting canary weight to ${WEIGHT}%..."

    kubectl patch virtualservice myapp -p "{
      \"spec\": {
        \"http\": [{
          \"route\": [
            {\"destination\": {\"host\": \"myapp-stable\"}, \"weight\": $((100 - WEIGHT))},
            {\"destination\": {\"host\": \"myapp-canary\"}, \"weight\": $WEIGHT}
          ]
        }]
      }
    }"

    echo "Waiting ${PAUSE_MINUTES} minutes..."
    sleep $((PAUSE_MINUTES * 60))

    # Check error rate
    ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query" \
        --data-urlencode 'query=sum(rate(http_requests_total{service="myapp-canary",status=~"5.."}[5m]))/sum(rate(http_requests_total{service="myapp-canary"}[5m]))' \
        | jq -r '.data.result[0].value[1]')

    if (( $(echo "$ERROR_RATE > $ERROR_THRESHOLD" | bc -l) )); then
        echo "ERROR: Error rate ${ERROR_RATE} exceeds threshold ${ERROR_THRESHOLD}"
        echo "Rolling back..."
        kubectl patch virtualservice myapp -p '{"spec":{"http":[{"route":[{"destination":{"host":"myapp-stable"},"weight":100}]}]}}'
        exit 1
    fi

    echo "Error rate ${ERROR_RATE} is healthy"
done

echo "Canary deployment complete. Promoting to stable..."
kubectl set image deployment/myapp-stable myapp=$IMAGE
kubectl scale deployment/myapp-canary --replicas=0
```

## Feature Flags

**Description**: Deploy code with features disabled, enable gradually via configuration.

### Architecture

```
                    ┌─────────────┐
                    │   Feature   │
                    │    Flag     │
                    │   Service   │
                    └──────┬──────┘
                           │
                           ▼
      ┌────────────────────────────────────┐
      │           Application              │
      │   ┌──────────┐  ┌──────────────┐  │
      │   │ Feature  │  │   Feature    │  │
      │   │   OFF    │  │     ON       │  │
      │   │  (old)   │  │   (new)      │  │
      │   └──────────┘  └──────────────┘  │
      └────────────────────────────────────┘
```

### Implementation Pattern

```typescript
// Feature flag client (LaunchDarkly, Unleash, etc.)
import { LDClient } from 'launchdarkly-js-client-sdk';

class FeatureFlags {
  private client: LDClient;

  async isEnabled(flag: string, user: User, defaultValue: boolean = false): Promise<boolean> {
    return this.client.variation(flag, {
      key: user.id,
      email: user.email,
      custom: {
        plan: user.plan,
        region: user.region,
      }
    }, defaultValue);
  }
}

// Usage in application
async function checkout(cart: Cart, user: User) {
  const useNewCheckout = await featureFlags.isEnabled('new-checkout-flow', user);

  if (useNewCheckout) {
    return newCheckoutFlow(cart, user);
  } else {
    return legacyCheckoutFlow(cart, user);
  }
}
```

### Rollout Strategies

```yaml
# LaunchDarkly-style targeting rules
flag: new-checkout-flow
environments:
  production:
    on: true
    targets:
      # Specific users (beta testers)
      - variation: true
        values: ["user-123", "user-456"]
    rules:
      # 10% of premium users
      - clauses:
          - attribute: plan
            op: in
            values: ["premium", "enterprise"]
        rollout:
          variations:
            - variation: true
              weight: 10000  # 10%
            - variation: false
              weight: 90000  # 90%
    fallthrough:
      # Default: 1% of all users
      rollout:
        variations:
          - variation: true
            weight: 1000   # 1%
          - variation: false
            weight: 99000  # 99%
```

### Benefits

- **Decouple deployment from release**: Deploy anytime, release when ready
- **Kill switch**: Instantly disable problematic features
- **Gradual rollout**: Control exactly who sees new features
- **A/B testing**: Measure impact of changes

### Best Practices

1. **Clean up old flags**: Remove flags after full rollout
2. **Default to off**: New features should be disabled by default
3. **Log flag evaluations**: Track which users see which versions
4. **Test both paths**: Ensure old and new code paths work

## Shadow Deployment

**Description**: Deploy new version alongside production, mirror traffic without affecting users.

### Architecture

```
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │ Response              Mirror
              ▼                         ▼
      ┌───────────────┐        ┌───────────────┐
      │  Production   │        │    Shadow     │
      │   (v1.0)      │        │   (v2.0)      │
      │   [SERVES]    │        │  [OBSERVES]   │
      └───────────────┘        └───────────────┘
```

### Istio Traffic Mirroring

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp.example.com
  http:
    - route:
        - destination:
            host: myapp-v1
      mirror:
        host: myapp-v2
      mirrorPercentage:
        value: 100.0  # Mirror 100% of traffic
```

### Use Cases

- **Performance testing**: Compare v2 latency/throughput to v1
- **Bug detection**: Find issues before users see them
- **Load testing**: Test v2 under production traffic patterns
- **Data validation**: Verify v2 produces correct results

### Considerations

- **Side effects**: Shadow must not trigger writes/payments/notifications
- **Resource cost**: 2x traffic processing
- **Response comparison**: Need tooling to compare v1 vs v2 responses

## Rollback Strategies

### Automatic Rollback Triggers

```yaml
# Kubernetes: Rollback on failed deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  minReadySeconds: 30  # Pod must be ready for 30s
  progressDeadlineSeconds: 600  # Fail deployment if not complete in 10 min
  template:
    spec:
      containers:
        - name: myapp
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            failureThreshold: 3
```

### Manual Rollback Commands

```bash
# Kubernetes
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=5

# Helm
helm rollback myapp 5

# Argo CD
argocd app rollback myapp

# AWS ECS
aws ecs update-service --service myapp --task-definition myapp:5
```

### Rollback Automation Script

```bash
#!/bin/bash
# auto-rollback.sh

SERVICE=$1
METRIC_THRESHOLD=0.01
CHECK_INTERVAL=30
MAX_CHECKS=10

for i in $(seq 1 $MAX_CHECKS); do
    ERROR_RATE=$(get_error_rate $SERVICE)

    if (( $(echo "$ERROR_RATE > $METRIC_THRESHOLD" | bc -l) )); then
        echo "ERROR: Error rate $ERROR_RATE exceeds threshold"
        echo "Triggering rollback..."

        kubectl rollout undo deployment/$SERVICE

        # Notify team
        curl -X POST "$SLACK_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"text\":\"Automatic rollback triggered for $SERVICE. Error rate: $ERROR_RATE\"}"

        exit 1
    fi

    echo "Check $i/$MAX_CHECKS: Error rate $ERROR_RATE OK"
    sleep $CHECK_INTERVAL
done

echo "Deployment stable"
```

## Database Migration Strategies

### Backward-Compatible Migrations

```sql
-- Phase 1: Add new column (nullable)
ALTER TABLE users ADD COLUMN email_verified_at TIMESTAMP;

-- Phase 2: Backfill data (background job)
UPDATE users SET email_verified_at = created_at WHERE email_verified = true;

-- Phase 3: Deploy new code that uses new column

-- Phase 4: Make column NOT NULL (after verification)
ALTER TABLE users ALTER COLUMN email_verified_at SET NOT NULL;

-- Phase 5: Remove old column (after full rollout)
ALTER TABLE users DROP COLUMN email_verified;
```

### Expand-Contract Pattern

```
Phase 1: EXPAND
┌─────────────────────────────────────┐
│  old_column  │  new_column (null)  │
│     data     │       null          │
└─────────────────────────────────────┘

Phase 2: MIGRATE
┌─────────────────────────────────────┐
│  old_column  │  new_column         │
│     data     │     data            │
└─────────────────────────────────────┘

Phase 3: CONTRACT
┌─────────────────────────────────────┐
│  new_column                         │
│     data                            │
└─────────────────────────────────────┘
```

### Zero-Downtime Migration Checklist

1. **Add new column as nullable**
2. **Deploy code that writes to both columns**
3. **Backfill existing data**
4. **Deploy code that reads from new column**
5. **Add NOT NULL constraint**
6. **Deploy code that only writes to new column**
7. **Drop old column**

## Anti-Patterns

**NEVER do these:**

### 1. Big Bang Deployment

```bash
# Deploy to 100% of users immediately without testing
kubectl set image deployment/myapp myapp=myapp:v2
```

**Instead**: Use canary or blue-green for gradual rollout.

### 2. No Health Checks

```yaml
# Deployment without readiness probe
spec:
  containers:
    - name: myapp
      image: myapp:v2
      # No health checks = traffic to unready pods
```

**Instead**: Always define readiness and liveness probes.

### 3. No Rollback Plan

```bash
# Deploy without knowing how to rollback
./deploy.sh production
```

**Instead**: Test rollback procedure before every deployment.

### 4. Manual Traffic Switching

```bash
# Manually updating load balancer rules
ssh lb1 "vim /etc/nginx/nginx.conf"
```

**Instead**: Automate traffic switching with kubectl/API calls.

### 5. Incompatible Database Migrations

```sql
-- Breaking change: rename column during deployment
ALTER TABLE users RENAME COLUMN email TO email_address;
```

**Instead**: Use expand-contract pattern for schema changes.

---

## Quick Reference

**Kubernetes Commands:**
```bash
# Check rollout status
kubectl rollout status deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp

# View history
kubectl rollout history deployment/myapp

# Pause/resume rollout
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp
```

**Strategy Selection Guide:**

| Question | Blue-Green | Canary | Rolling |
|----------|------------|--------|---------|
| Need instant rollback? | Yes | Medium | No |
| Limited resources? | No | Yes | Yes |
| Want gradual rollout? | No | Yes | Yes |
| Need to test at scale? | Yes | Partial | No |
| Complex monitoring setup? | No | Yes | No |

---

Apply these patterns to achieve reliable, zero-downtime deployments. Prioritize reversibility (instant rollback), observability (metrics-driven decisions), and gradual rollout (canary for critical services).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

