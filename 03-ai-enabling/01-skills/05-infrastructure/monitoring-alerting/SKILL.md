---
last_updated: 2026-02-25
status: active
name: monitoring-alerting
description: Prometheus, Grafana, and observability patterns. Use when implementing monitoring and alerting systems.
triggers:
  files: ["**/prometheus*.yml", "**/alertmanager*.yml", "**/grafana/**", "**/*dashboard*.json", "**/alerts/**"]
  keywords: ["monitoring", "alerting", "prometheus", "grafana", "metrics", "observability", "SLO", "SLI", "dashboard"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides monitoring and alerting implementation for reliable systems. Apply these patterns when building observability infrastructure, defining SLOs, or configuring alerts.

The user provides monitoring requirements: metrics to track, alerting thresholds, dashboard needs, or SLO definitions.

## Core Principles

Effective monitoring is built on five pillars:

1. **SLI/SLO First**: Define what matters before how to measure it.
2. **Actionable Alerts**: Every alert must have a clear response.
3. **Context-Rich**: Include enough information to diagnose issues.
4. **Layered**: Infrastructure, application, business metrics.
5. **Low Latency**: Fast detection, faster response.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## The Four Golden Signals

| Signal | Description | Example Metric |
|--------|-------------|----------------|
| Latency | Time to serve requests | `http_request_duration_seconds` |
| Traffic | Request volume | `http_requests_total` |
| Errors | Failure rate | `http_requests_total{status=~"5.."}` |
| Saturation | Resource utilization | `container_memory_usage_bytes` |

## Prometheus Configuration

### Basic Setup

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

### Recording Rules

Pre-compute expensive queries for dashboard performance.

```yaml
# rules/recording.yml
groups:
  - name: http_latency
    interval: 30s
    rules:
      - record: http_request_duration_seconds:rate5m
        expr: rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

      - record: http_request_duration_seconds:p99
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

      - record: http_request_duration_seconds:p95
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

  - name: error_rates
    interval: 30s
    rules:
      - record: http_error_rate:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m]))
```

## Alerting Rules

### High-Quality Alerts

```yaml
# rules/alerts.yml
groups:
  - name: service_alerts
    rules:
      - alert: HighErrorRate
        expr: http_error_rate:rate5m > 0.01
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 1%)"
          runbook_url: "https://runbooks.example.com/high-error-rate"
          dashboard_url: "https://grafana.example.com/d/service-overview?var-service={{ $labels.service }}"

      - alert: HighLatency
        expr: http_request_duration_seconds:p99 > 0.5
        for: 10m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "P99 latency high on {{ $labels.service }}"
          description: "P99 latency is {{ $value | humanizeDuration }}"
          runbook_url: "https://runbooks.example.com/high-latency"

      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod {{ $labels.pod }} is crash looping"
          description: "Pod has restarted {{ $value | humanize }} times in 15 minutes"
```

### Alert Severity Levels

| Severity | Response Time | Notification | Example |
|----------|---------------|--------------|---------|
| Critical | Immediate | PagerDuty | Service down |
| Warning | Hours | Slack | High latency |
| Info | Next business day | Ticket | Disk filling |

## Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/xxx'

route:
  receiver: 'slack-default'
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true
    - match:
        severity: critical
      receiver: 'slack-critical'
    - match:
        severity: warning
      receiver: 'slack-warnings'

receivers:
  - name: 'slack-default'
    slack_configs:
      - channel: '#alerts'
        send_resolved: true
        title: '{{ .Status | toUpper }}: {{ .CommonAnnotations.summary }}'
        text: '{{ .CommonAnnotations.description }}'

  - name: 'slack-critical'
    slack_configs:
      - channel: '#alerts-critical'
        send_resolved: true

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<pagerduty-key>'
        severity: critical

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts-warnings'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service']
```

## SLO Implementation

### Define SLIs and SLOs

```yaml
# SLO: 99.9% availability
# SLI: Successful requests / Total requests

# Error budget: 0.1% = 43 minutes/month downtime
```

### Prometheus SLO Rules

```yaml
groups:
  - name: slo_api
    rules:
      # SLI: Success rate
      - record: sli:api_availability:rate5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m])) /
          sum(rate(http_requests_total[5m]))

      # SLO burn rate (30-day window)
      - record: slo:api_error_budget:remaining
        expr: |
          1 - (
            (1 - sli:api_availability:rate5m) /
            (1 - 0.999)
          )

      # Multi-window burn rate alerts
      - alert: SLOBurnRateCritical
        expr: |
          (
            sli:api_availability:rate5m < 0.999 - (14.4 * 0.001)
          ) and (
            sli:api_availability:rate1h < 0.999 - (14.4 * 0.001)
          )
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "API SLO burn rate critical"
          description: "Burning 14.4x error budget. Will exhaust monthly budget in 2 days."

      - alert: SLOBurnRateWarning
        expr: |
          (
            sli:api_availability:rate5m < 0.999 - (6 * 0.001)
          ) and (
            sli:api_availability:rate6h < 0.999 - (6 * 0.001)
          )
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API SLO burn rate elevated"
          description: "Burning 6x error budget. Will exhaust monthly budget in 5 days."
```

## Grafana Dashboards

### Dashboard JSON Structure

```json
{
  "dashboard": {
    "title": "Service Overview",
    "tags": ["production", "api"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{ service }}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "http_error_rate:rate5m * 100"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                { "value": 0, "color": "green" },
                { "value": 1, "color": "yellow" },
                { "value": 5, "color": "red" }
              ]
            }
          }
        }
      }
    ]
  }
}
```

### Key Dashboard Panels

| Panel | Query | Purpose |
|-------|-------|---------|
| Request Rate | `sum(rate(http_requests_total[5m]))` | Traffic |
| Error Rate | `http_error_rate:rate5m * 100` | Reliability |
| P99 Latency | `http_request_duration_seconds:p99` | Performance |
| CPU Usage | `rate(process_cpu_seconds_total[5m])` | Resources |
| Memory | `process_resident_memory_bytes` | Resources |

## Application Instrumentation

### Prometheus Client (Python)

```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Instrument code
@REQUEST_LATENCY.labels(method='GET', endpoint='/api/users').time()
def get_users():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/users', status='200').inc()
    return users
```

### Prometheus Client (Node.js)

```javascript
const promClient = require('prom-client');

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request latency',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
});

app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.route?.path, status_code: res.statusCode });
  });
  next();
});
```

## Best Practices

### Alert Quality

| Do | Don't |
|----|-------|
| Include runbook link | Alert without context |
| Set appropriate `for` duration | Alert on single spike |
| Use severity levels | Page for warnings |
| Test alerts regularly | Assume alerts work |

### Dashboard Design

| Practice | Reason |
|----------|--------|
| Top-to-bottom flow | Most important first |
| Consistent time ranges | Easy comparison |
| Link to related dashboards | Navigation |
| Include alert status | Current state |

### Metric Naming

```
# Format: {namespace}_{metric}_{unit}
http_request_duration_seconds
process_cpu_seconds_total
http_requests_total
node_memory_bytes_total
```

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Too many alerts | Focus on symptoms, not causes |
| No runbooks | Every alert needs response docs |
| Ignoring alerts | Fix alert or remove it |
| Dashboard clutter | Focus on key metrics |
| High cardinality labels | Limit label values |

---

Apply these patterns for comprehensive observability. Start with the four golden signals, define SLOs early, and ensure every alert is actionable with clear runbooks.


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

