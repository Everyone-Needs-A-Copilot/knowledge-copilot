---
last_updated: 2026-02-25
status: active
name: log-aggregation
description: ELK stack, Loki, and centralized logging patterns. Use when implementing log collection and analysis.
triggers:
  files: ["**/logstash*.conf", "**/filebeat*.yml", "**/fluent*.conf", "**/loki*.yml", "**/promtail*.yml"]
  keywords: ["logging", "log aggregation", "elasticsearch", "logstash", "kibana", "ELK", "loki", "fluentd", "centralized logging"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides centralized logging implementation for debugging and analysis. Apply these patterns when building log collection pipelines, structuring logs, or implementing log search.

The user provides logging requirements: log sources, retention needs, search patterns, or compliance requirements.

## Core Principles

Effective logging is built on five pillars:

1. **Structured**: JSON logs with consistent fields.
2. **Centralized**: All logs in one searchable location.
3. **Correlated**: Request IDs link logs across services.
4. **Retained**: Appropriate retention for debugging and compliance.
5. **Indexed**: Fast search on relevant fields.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| ERROR | Failures requiring attention | Database connection failed |
| WARN | Potential issues | Retry attempt 3/5 |
| INFO | Normal operations | Request completed |
| DEBUG | Development details | Query parameters |
| TRACE | Verbose debugging | Full request/response |

## Structured Logging

### JSON Log Format

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "service": "api-gateway",
  "version": "1.2.3",
  "environment": "production",
  "request_id": "abc-123-def",
  "trace_id": "trace-456",
  "user_id": "user-789",
  "message": "Request completed",
  "http": {
    "method": "GET",
    "path": "/api/users",
    "status_code": 200,
    "duration_ms": 45
  }
}
```

### Standard Fields

| Field | Purpose | Required |
|-------|---------|----------|
| timestamp | When event occurred | Yes |
| level | Severity | Yes |
| service | Source service | Yes |
| request_id | Correlation ID | Yes |
| message | Human description | Yes |
| trace_id | Distributed trace | Recommended |
| user_id | User context | When applicable |

### Application Logging (Node.js)

```javascript
const pino = require('pino');

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: {
    service: 'api-gateway',
    version: process.env.APP_VERSION,
    environment: process.env.NODE_ENV,
  },
});

// Usage
logger.info({
  request_id: req.id,
  http: { method: req.method, path: req.path },
}, 'Request received');
```

### Application Logging (Python)

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Usage
logger.info(
    "Request completed",
    request_id=request_id,
    http_method="GET",
    http_path="/api/users",
    duration_ms=45
)
```

## ELK Stack

### Filebeat Configuration

```yaml
# filebeat.yml
filebeat.inputs:
  - type: container
    paths:
      - /var/lib/docker/containers/*/*.log
    processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
            - logs_path:
                logs_path: "/var/lib/docker/containers/"

  - type: log
    paths:
      - /var/log/app/*.log
    json:
      keys_under_root: true
      add_error_key: true
    fields:
      type: application

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "logs-%{[fields.type]}-%{+yyyy.MM.dd}"

setup.template:
  name: "logs"
  pattern: "logs-*"

setup.ilm:
  enabled: true
  rollover_alias: "logs"
  policy_name: "logs-policy"
```

### Logstash Pipeline

```ruby
# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Parse JSON logs
  json {
    source => "message"
    target => "parsed"
  }

  # Extract fields
  mutate {
    rename => {
      "[parsed][level]" => "level"
      "[parsed][service]" => "service"
      "[parsed][request_id]" => "request_id"
    }
  }

  # Parse timestamps
  date {
    match => ["[parsed][timestamp]", "ISO8601"]
    target => "@timestamp"
  }

  # Add geo data for IPs
  if [client_ip] {
    geoip {
      source => "client_ip"
    }
  }

  # Remove sensitive data
  mutate {
    remove_field => ["password", "token", "credit_card"]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{service}-%{+YYYY.MM.dd}"
  }
}
```

### Elasticsearch Index Lifecycle

```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50gb",
            "max_age": "1d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

## Grafana Loki

Lightweight, cost-effective logging for Kubernetes.

### Promtail Configuration

```yaml
# promtail.yml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
    pipeline_stages:
      - json:
          expressions:
            level: level
            service: service
            request_id: request_id
      - labels:
          level:
          service:
```

### Loki Configuration

```yaml
# loki.yml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

compactor:
  working_directory: /loki/compactor
  shared_store: filesystem
```

### LogQL Queries

```logql
# Find errors in service
{service="api"} |= "error"

# JSON parsing with filters
{app="api"} | json | level="error" | duration_ms > 1000

# Rate of errors
sum(rate({service="api"} |= "error" [5m])) by (service)

# Top 10 slowest requests
topk(10, {service="api"} | json | duration_ms > 0 | duration_ms)

# Logs with specific request ID
{service=~".*"} |= "request_id=abc-123"
```

## Fluentd / Fluent Bit

### Fluent Bit (Lightweight)

```ini
# fluent-bit.conf
[SERVICE]
    Flush        1
    Log_Level    info
    Parsers_File parsers.conf

[INPUT]
    Name              tail
    Path              /var/log/containers/*.log
    Parser            docker
    Tag               kube.*
    Mem_Buf_Limit     5MB
    Skip_Long_Lines   On

[FILTER]
    Name                kubernetes
    Match               kube.*
    Kube_URL            https://kubernetes.default.svc:443
    Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
    Merge_Log           On
    K8S-Logging.Parser  On

[OUTPUT]
    Name            es
    Match           *
    Host            elasticsearch
    Port            9200
    Index           fluent-bit
    Type            _doc
```

## Correlation IDs

### Implementation Pattern

```javascript
// Express middleware
const { v4: uuidv4 } = require('uuid');

app.use((req, res, next) => {
  req.requestId = req.headers['x-request-id'] || uuidv4();
  res.setHeader('x-request-id', req.requestId);

  // Add to logger context
  req.log = logger.child({ request_id: req.requestId });

  next();
});

// Propagate to downstream services
async function callService(req, data) {
  return fetch('http://service-b/api', {
    headers: {
      'x-request-id': req.requestId,
      'x-trace-id': req.traceId,
    },
    body: JSON.stringify(data),
  });
}
```

## Log Retention

| Environment | Hot | Warm | Cold | Delete |
|-------------|-----|------|------|--------|
| Development | 3d | - | - | 7d |
| Staging | 7d | 14d | - | 30d |
| Production | 7d | 30d | 90d | 1y |

## Best Practices

### What to Log

| Do Log | Don't Log |
|--------|-----------|
| Request IDs | Passwords/tokens |
| User IDs (hashed) | Credit card numbers |
| Error stack traces | PII without consent |
| Performance metrics | Full request bodies |
| Business events | Sensitive headers |

### Performance

| Practice | Benefit |
|----------|---------|
| Async logging | Non-blocking |
| Batch writes | Reduced I/O |
| Sampling in production | Cost control |
| Log rotation | Disk management |

### Security

```javascript
// Sanitize sensitive data
function sanitizeLog(data) {
  const sensitive = ['password', 'token', 'secret', 'credit_card'];
  const sanitized = { ...data };

  for (const key of Object.keys(sanitized)) {
    if (sensitive.some(s => key.toLowerCase().includes(s))) {
      sanitized[key] = '[REDACTED]';
    }
  }

  return sanitized;
}
```

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Unstructured logs | Use JSON with consistent schema |
| No correlation IDs | Add request_id to every log |
| Logging everything | Log meaningful events |
| Ignoring log levels | Use appropriate severity |
| No retention policy | Define and automate retention |

## Kubernetes Deployment

```yaml
# Fluent Bit DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluent-bit
  template:
    spec:
      serviceAccountName: fluent-bit
      containers:
        - name: fluent-bit
          image: fluent/fluent-bit:2.1
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: containers
              mountPath: /var/lib/docker/containers
              readOnly: true
            - name: config
              mountPath: /fluent-bit/etc/
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: containers
          hostPath:
            path: /var/lib/docker/containers
        - name: config
          configMap:
            name: fluent-bit-config
```

---

Apply these patterns for comprehensive log management. Start with structured JSON logging, implement correlation IDs, and choose the right stack (ELK for search-heavy, Loki for cost-efficient Kubernetes logging).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

