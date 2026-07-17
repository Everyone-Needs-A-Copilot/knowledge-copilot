---
last_updated: 2026-02-25
status: active
name: logging-infrastructure
description: Centralized logging setup with ELK/EFK stack, log aggregation, and observability patterns. Use when setting up logging systems.
triggers:
  files: ["**/fluentd*.conf", "**/fluent-bit*.conf", "**/logstash*.conf", "**/filebeat*.yml", "**/elasticsearch*.yml", "**/loki*.yml"]
  keywords: ["logging", "ELK", "EFK", "Elasticsearch", "Fluentd", "Logstash", "Kibana", "Grafana Loki", "log aggregation", "observability"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides setup of production-grade centralized logging infrastructure. Apply these patterns when building log aggregation pipelines, setting up observability stacks, or debugging distributed systems.

The user provides logging requirements: centralized log collection, log aggregation setup, search and visualization, or log retention policies.

## Core Principles

Logging excellence is built on five pillars:

1. **Centralization**: All logs flow to a single searchable location.
2. **Structured Data**: JSON logs with consistent fields for queryability.
3. **Retention**: Right-sized storage with lifecycle policies.
4. **Correlation**: Request IDs trace across services.
5. **Alerting**: Proactive notification on error patterns.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Logging Stack Comparison

| Stack | Best For | Storage | Complexity | Cost |
|-------|----------|---------|------------|------|
| **ELK** (Elasticsearch, Logstash, Kibana) | Full-text search, analytics | High | High | High |
| **EFK** (Elasticsearch, Fluentd, Kibana) | Kubernetes native | High | Medium | High |
| **Loki + Grafana** | Cost-effective, metrics correlation | Low | Low | Low |
| **CloudWatch/Stackdriver** | AWS/GCP native | Variable | Low | Variable |

## Structured Logging

### Log Format Standards

**JSON structured logging (recommended):**
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "ERROR",
  "service": "api-gateway",
  "version": "1.2.3",
  "environment": "production",
  "request_id": "abc-123-def",
  "trace_id": "trace-789",
  "span_id": "span-456",
  "user_id": "user-42",
  "message": "Failed to process payment",
  "error": {
    "type": "PaymentGatewayError",
    "message": "Connection timeout",
    "stack": "..."
  },
  "context": {
    "payment_id": "pay-123",
    "amount": 99.99,
    "currency": "USD"
  },
  "duration_ms": 5032
}
```

### Standard Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `timestamp` | ISO 8601 | Event time in UTC | Yes |
| `level` | String | DEBUG, INFO, WARN, ERROR, FATAL | Yes |
| `service` | String | Service name | Yes |
| `version` | String | Application version | Yes |
| `environment` | String | dev, staging, production | Yes |
| `request_id` | String | Unique request identifier | Recommended |
| `trace_id` | String | Distributed tracing ID | Recommended |
| `message` | String | Human-readable description | Yes |
| `error` | Object | Error details (type, message, stack) | On errors |
| `context` | Object | Additional context | Optional |
| `duration_ms` | Number | Operation duration | For requests |

### Python Structured Logging

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": "my-service",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add request context if available
        if hasattr(record, 'request_id'):
            log_record["request_id"] = record.request_id

        # Add exception info
        if record.exc_info:
            log_record["error"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stack": self.formatException(record.exc_info),
            }

        # Add extra fields
        if hasattr(record, 'context'):
            log_record["context"] = record.context

        return json.dumps(log_record)

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.root.handlers = [handler]
logging.root.setLevel(logging.INFO)

# Usage
logger = logging.getLogger(__name__)
logger.info("User logged in", extra={"request_id": "abc-123", "context": {"user_id": 42}})
```

### Node.js Structured Logging (Pino)

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label.toUpperCase() }),
  },
  base: {
    service: 'my-service',
    version: process.env.APP_VERSION || '1.0.0',
    environment: process.env.NODE_ENV || 'development',
  },
  timestamp: () => `,"timestamp":"${new Date().toISOString()}"`,
});

// Usage
logger.info({ requestId: 'abc-123', userId: 42 }, 'User logged in');
logger.error({ err, paymentId: 'pay-123' }, 'Payment failed');

// Child logger with context
const requestLogger = logger.child({ requestId: 'abc-123' });
requestLogger.info('Processing request');
requestLogger.info('Request complete');
```

### Go Structured Logging (Zap)

```go
package main

import (
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
)

func initLogger() *zap.Logger {
    config := zap.NewProductionConfig()
    config.EncoderConfig.TimeKey = "timestamp"
    config.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder

    logger, _ := config.Build(
        zap.Fields(
            zap.String("service", "my-service"),
            zap.String("version", "1.0.0"),
            zap.String("environment", os.Getenv("ENVIRONMENT")),
        ),
    )
    return logger
}

func main() {
    logger := initLogger()
    defer logger.Sync()

    // Usage
    logger.Info("User logged in",
        zap.String("request_id", "abc-123"),
        zap.Int("user_id", 42),
    )

    logger.Error("Payment failed",
        zap.Error(err),
        zap.String("payment_id", "pay-123"),
    )
}
```

## ELK Stack (Elasticsearch, Logstash, Kibana)

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Apps      │────▶│  Logstash   │────▶│Elasticsearch│────▶│   Kibana    │
│  (Filebeat) │     │  (Process)  │     │  (Storage)  │     │ (Visualize) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Docker Compose Setup

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200 | grep -q 'cluster_name'"]
      interval: 30s
      timeout: 10s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml:ro
    ports:
      - "5044:5044"  # Beats input
      - "5000:5000"  # TCP input
    environment:
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
    depends_on:
      elasticsearch:
        condition: service_healthy

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
    depends_on:
      elasticsearch:
        condition: service_healthy

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    container_name: filebeat
    user: root
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      - logstash

volumes:
  elasticsearch_data:
```

### Logstash Configuration

```ruby
# logstash/pipeline/logstash.conf

input {
  beats {
    port => 5044
  }

  tcp {
    port => 5000
    codec => json
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
      target => "parsed"
    }
    mutate {
      remove_field => ["message"]
      rename => { "[parsed][message]" => "message" }
    }
  }

  # Parse timestamp
  date {
    match => ["[parsed][timestamp]", "ISO8601"]
    target => "@timestamp"
  }

  # Add geo-IP for client IPs
  if [parsed][client_ip] {
    geoip {
      source => "[parsed][client_ip]"
      target => "geoip"
    }
  }

  # Enrich with environment info
  mutate {
    add_field => {
      "[@metadata][index]" => "logs-%{[parsed][environment]}-%{+YYYY.MM.dd}"
    }
  }

  # Drop debug logs in production
  if [parsed][environment] == "production" and [parsed][level] == "DEBUG" {
    drop { }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    user => "elastic"
    password => "${ELASTIC_PASSWORD}"
    index => "%{[@metadata][index]}"
  }
}
```

### Filebeat Configuration

```yaml
# filebeat/filebeat.yml

filebeat.inputs:
  # Docker container logs
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    processors:
      - add_docker_metadata:
          host: "unix:///var/run/docker.sock"

  # Application logs
  - type: log
    enabled: true
    paths:
      - /var/log/app/*.log
    json:
      keys_under_root: true
      overwrite_keys: true
      add_error_key: true

output.logstash:
  hosts: ["logstash:5044"]

processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - add_kubernetes_metadata: ~
```

### Elasticsearch Index Template

```json
PUT _index_template/logs-template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs"
    },
    "mappings": {
      "properties": {
        "timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "service": { "type": "keyword" },
        "environment": { "type": "keyword" },
        "request_id": { "type": "keyword" },
        "trace_id": { "type": "keyword" },
        "message": { "type": "text" },
        "error": {
          "properties": {
            "type": { "type": "keyword" },
            "message": { "type": "text" },
            "stack": { "type": "text" }
          }
        },
        "duration_ms": { "type": "long" }
      }
    }
  }
}
```

### Index Lifecycle Policy

```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "1d"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 0
          }
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

## EFK Stack (Kubernetes)

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Pods      │────▶│  Fluentd    │────▶│Elasticsearch│────▶│   Kibana    │
│  (stdout)   │     │ (DaemonSet) │     │ (StatefulSet)│    │ (Deployment)│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Fluentd DaemonSet

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccountName: fluentd
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule
      containers:
        - name: fluentd
          image: fluent/fluentd-kubernetes-daemonset:v1.16-debian-elasticsearch8-1
          env:
            - name: FLUENT_ELASTICSEARCH_HOST
              value: elasticsearch.logging.svc.cluster.local
            - name: FLUENT_ELASTICSEARCH_PORT
              value: "9200"
            - name: FLUENT_ELASTICSEARCH_USER
              valueFrom:
                secretKeyRef:
                  name: elasticsearch-credentials
                  key: username
            - name: FLUENT_ELASTICSEARCH_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: elasticsearch-credentials
                  key: password
          resources:
            limits:
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 256Mi
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
            - name: config
              mountPath: /fluentd/etc/fluent.conf
              subPath: fluent.conf
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
        - name: config
          configMap:
            name: fluentd-config
```

### Fluentd Configuration

```xml
# fluentd/fluent.conf

<source>
  @type tail
  path /var/log/containers/*.log
  pos_file /var/log/fluentd-containers.log.pos
  tag kubernetes.*
  read_from_head true
  <parse>
    @type json
    time_key time
    time_format %Y-%m-%dT%H:%M:%S.%NZ
  </parse>
</source>

<filter kubernetes.**>
  @type kubernetes_metadata
  @id filter_kube_metadata
</filter>

<filter kubernetes.**>
  @type parser
  key_name log
  reserve_data true
  remove_key_name_field true
  <parse>
    @type json
  </parse>
</filter>

<match kubernetes.**>
  @type elasticsearch
  host "#{ENV['FLUENT_ELASTICSEARCH_HOST']}"
  port "#{ENV['FLUENT_ELASTICSEARCH_PORT']}"
  user "#{ENV['FLUENT_ELASTICSEARCH_USER']}"
  password "#{ENV['FLUENT_ELASTICSEARCH_PASSWORD']}"
  scheme https
  ssl_verify true

  logstash_format true
  logstash_prefix kubernetes
  logstash_dateformat %Y.%m.%d

  include_tag_key true
  type_name _doc

  <buffer>
    @type file
    path /var/log/fluentd-buffers/kubernetes.buffer
    flush_mode interval
    flush_interval 5s
    flush_thread_count 2
    retry_type exponential_backoff
    retry_forever true
    chunk_limit_size 8M
    queue_limit_length 512
    overflow_action block
  </buffer>
</match>
```

## Grafana Loki

### Architecture (Lightweight Alternative)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Apps      │────▶│  Promtail   │────▶│    Loki     │
│  (stdout)   │     │  (Collect)  │     │  (Storage)  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │   Grafana   │
                                        │ (Visualize) │
                                        └─────────────┘
```

### Docker Compose Setup

```yaml
version: '3.8'

services:
  loki:
    image: grafana/loki:2.9.0
    container_name: loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/local-config.yaml
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:2.9.0
    container_name: promtail
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml

  grafana:
    image: grafana/grafana:10.2.0
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}

volumes:
  loki_data:
  grafana_data:
```

### Loki Configuration

```yaml
# loki/loki-config.yml

auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  wal:
    enabled: true
    dir: /loki/wal
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 1h
  max_chunk_age: 1h
  chunk_target_size: 1048576
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/boltdb-shipper-active
    cache_location: /loki/boltdb-shipper-cache
    cache_ttl: 24h
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

compactor:
  working_directory: /loki/boltdb-shipper-compactor
  shared_store: filesystem

limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  retention_period: 744h  # 31 days

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: true
  retention_period: 744h
```

### Promtail Configuration

```yaml
# promtail/promtail-config.yml

server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Docker container logs
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*.log

    pipeline_stages:
      - json:
          expressions:
            output: log
            stream: stream
            timestamp: time
      - timestamp:
          source: timestamp
          format: RFC3339Nano
      - output:
          source: output

      # Extract labels from JSON log
      - json:
          expressions:
            level: level
            service: service
            request_id: request_id
          source: output
      - labels:
          level:
          service:

  # System logs
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: syslog
          __path__: /var/log/syslog
```

### LogQL Queries

```logql
# Find all errors in the last hour
{job="containerlogs"} |= "ERROR" | json

# Filter by service and level
{service="api-gateway", level="ERROR"}

# Count errors per service
sum by (service) (rate({job="containerlogs"} |= "ERROR" [5m]))

# Search for specific request
{job="containerlogs"} | json | request_id="abc-123"

# Latency percentiles
quantile_over_time(0.99, {service="api"} | json | unwrap duration_ms [5m]) by (service)

# Error rate
sum(rate({service="api"} | json | level="ERROR" [5m]))
/
sum(rate({service="api"} [5m]))
```

## Log Aggregation Patterns

### Request Tracing

```typescript
// Middleware to inject request ID
import { v4 as uuidv4 } from 'uuid';

app.use((req, res, next) => {
  req.requestId = req.headers['x-request-id'] || uuidv4();
  res.setHeader('x-request-id', req.requestId);

  // Attach to logger context
  req.logger = logger.child({ requestId: req.requestId });

  next();
});

// Use throughout request lifecycle
app.get('/api/users', async (req, res) => {
  req.logger.info('Fetching users');

  const users = await userService.getAll();

  req.logger.info({ count: users.length }, 'Users fetched');

  res.json(users);
});
```

### Distributed Tracing Correlation

```typescript
// Propagate trace context
import { trace, context } from '@opentelemetry/api';

function getTraceContext(): Record<string, string> {
  const span = trace.getSpan(context.active());
  if (!span) return {};

  const spanContext = span.spanContext();
  return {
    traceId: spanContext.traceId,
    spanId: spanContext.spanId,
  };
}

// Include in all logs
logger.info({
  ...getTraceContext(),
  message: 'Processing payment',
});
```

### Log Sampling (High-Volume)

```typescript
// Sample debug logs (1%)
const shouldSampleDebug = () => Math.random() < 0.01;

function log(level: string, message: string, context?: object) {
  if (level === 'DEBUG' && !shouldSampleDebug()) {
    return;  // Skip 99% of debug logs
  }

  logger.log(level, message, context);
}
```

### Error Aggregation

```python
# Group similar errors
import hashlib

def error_fingerprint(error: Exception) -> str:
    """Generate fingerprint for error grouping."""
    error_type = type(error).__name__
    error_message = str(error)

    # Normalize dynamic parts
    normalized = re.sub(r'\d+', 'N', error_message)
    normalized = re.sub(r'[a-f0-9-]{36}', 'UUID', normalized)

    return hashlib.md5(f"{error_type}:{normalized}".encode()).hexdigest()[:8]

# Log with fingerprint
try:
    process_payment()
except Exception as e:
    logger.error({
        "message": "Payment processing failed",
        "error": {
            "type": type(e).__name__,
            "message": str(e),
            "fingerprint": error_fingerprint(e),
        }
    })
```

## Alerting

### Elasticsearch Watcher

```json
PUT _watcher/watch/error_rate_alert
{
  "trigger": {
    "schedule": { "interval": "5m" }
  },
  "input": {
    "search": {
      "request": {
        "indices": ["logs-production-*"],
        "body": {
          "query": {
            "bool": {
              "must": [
                { "term": { "level": "ERROR" } },
                { "range": { "@timestamp": { "gte": "now-5m" } } }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.hits.total.value": { "gt": 100 }
    }
  },
  "actions": {
    "slack_notification": {
      "webhook": {
        "scheme": "https",
        "host": "hooks.slack.com",
        "port": 443,
        "method": "post",
        "path": "/services/XXX/YYY/ZZZ",
        "body": "{\"text\": \"High error rate detected: {{ctx.payload.hits.total.value}} errors in last 5 minutes\"}"
      }
    }
  }
}
```

### Grafana Alert Rules (Loki)

```yaml
# grafana/provisioning/alerting/alerts.yml

apiVersion: 1
groups:
  - orgId: 1
    name: LogAlerts
    folder: Logs
    interval: 1m
    rules:
      - uid: error_rate_alert
        title: High Error Rate
        condition: B
        data:
          - refId: A
            queryType: range
            datasourceUid: loki
            model:
              expr: sum(rate({job="containerlogs"} |= "ERROR" [5m]))
              intervalMs: 1000
              maxDataPoints: 43200
          - refId: B
            queryType: ''
            datasourceUid: __expr__
            model:
              type: threshold
              expression: A
              conditions:
                - evaluator:
                    type: gt
                    params: [10]
        noDataState: NoData
        execErrState: Error
        for: 5m
        annotations:
          summary: High error rate detected
        labels:
          severity: critical
```

## Best Practices

### Log Levels

| Level | When to Use |
|-------|-------------|
| **FATAL** | Application cannot continue, immediate attention required |
| **ERROR** | Operation failed, requires attention |
| **WARN** | Unexpected condition, but operation continued |
| **INFO** | Significant events (startup, shutdown, major operations) |
| **DEBUG** | Detailed diagnostic information |
| **TRACE** | Very detailed tracing (rarely used in production) |

### What to Log

**DO Log:**
- Application startup/shutdown
- Incoming requests (method, path, status, duration)
- External service calls (latency, success/failure)
- Authentication events
- Business-critical operations
- Errors with full context

**DON'T Log:**
- Passwords, tokens, API keys
- Personal data (PII) without consent
- Credit card numbers
- Health check endpoints (too noisy)
- Successful database queries (too verbose)

### Performance Considerations

```typescript
// Lazy evaluation for expensive operations
logger.debug(() => `User data: ${JSON.stringify(largeObject)}`);

// Avoid logging in hot paths
if (logger.isDebugEnabled()) {
  logger.debug({ data: expensiveComputation() }, 'Debug info');
}

// Async logging (don't block request)
logger.info.async({ data }, 'Large payload logged');
```

## Anti-Patterns

**NEVER do these:**

### 1. Logging Sensitive Data

```typescript
// NEVER log passwords, tokens, or PII
logger.info({ password: user.password }, 'User login');

// Instead, redact sensitive fields
logger.info({ email: user.email }, 'User login');
```

### 2. Unstructured Logs

```typescript
// NEVER concatenate strings
logger.info('User ' + userId + ' purchased ' + product);

// Use structured data
logger.info({ userId, product }, 'Purchase completed');
```

### 3. Missing Context

```typescript
// NEVER log without context
logger.error('An error occurred');

// Include request ID, user ID, operation context
logger.error({
  requestId,
  userId,
  operation: 'checkout',
  error: err.message,
}, 'Checkout failed');
```

### 4. Excessive Logging

```typescript
// NEVER log in tight loops
for (const item of items) {
  logger.debug('Processing item');  // 10000 log entries
}

// Log summary instead
logger.info({ count: items.length }, 'Processing batch');
```

---

## Quick Reference

**Log Query Examples (Elasticsearch):**
```json
# Find errors
{"query": {"term": {"level": "ERROR"}}}

# Full-text search
{"query": {"match": {"message": "payment failed"}}}

# By request ID
{"query": {"term": {"request_id": "abc-123"}}}

# Time range
{"query": {"range": {"@timestamp": {"gte": "now-1h"}}}}
```

**Log Query Examples (Loki/LogQL):**
```logql
{service="api"} |= "error"
{service="api"} | json | level="ERROR"
{service="api"} | json | duration_ms > 1000
```

---

Apply these patterns to build observable, searchable, production-grade logging infrastructure. Prioritize structured data (JSON logs), correlation (request IDs), and retention policies (lifecycle management).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

