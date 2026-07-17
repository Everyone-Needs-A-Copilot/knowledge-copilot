---
last_updated: 2026-02-25
status: active
name: container-orchestration
description: Kubernetes, Docker Compose, and container management patterns. Use when deploying containerized applications.
triggers:
  files: ["**/Dockerfile", "**/docker-compose*.yml", "**/k8s/**", "**/*.yaml", "**/helm/**", "**/Chart.yaml"]
  keywords: ["kubernetes", "k8s", "docker", "container", "pod", "deployment", "service", "helm", "orchestration"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides container orchestration with Kubernetes and Docker Compose. Apply these patterns when deploying, scaling, and managing containerized applications.

The user provides orchestration requirements: application architecture, scaling needs, networking, or resource management.

## Core Principles

Container orchestration excellence is built on five pillars:

1. **Immutability**: Containers are replaced, not modified.
2. **Declarative**: Describe desired state, let orchestrator reconcile.
3. **Self-healing**: Automatic restarts and rescheduling.
4. **Scalability**: Horizontal scaling based on demand.
5. **Isolation**: Resource limits and namespaces for multi-tenancy.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Kubernetes Core Resources

### Pod

Smallest deployable unit. Contains one or more containers.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  containers:
    - name: app
      image: myapp:1.0.0
      ports:
        - containerPort: 8080
      resources:
        requests:
          memory: "128Mi"
          cpu: "250m"
        limits:
          memory: "256Mi"
          cpu: "500m"
      env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

### Deployment

Manages pod replicas with rolling updates.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: myapp:1.0.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
```

### Service

Network endpoint for pod access.

```yaml
# ClusterIP (internal)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
---
# LoadBalancer (external)
apiVersion: v1
kind: Service
metadata:
  name: myapp-public
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 443
      targetPort: 8080
```

**Service types:**

| Type | Access | Use Case |
|------|--------|----------|
| ClusterIP | Internal only | Microservices |
| NodePort | Node IP:Port | Development |
| LoadBalancer | External LB | Production |
| ExternalName | DNS alias | External services |

### ConfigMap and Secret

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  CACHE_TTL: "300"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-password: "supersecret"
  api-key: "key123"
```

**Usage in pods:**
```yaml
spec:
  containers:
    - name: app
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: app-config
```

## Resource Management

### Requests and Limits

```yaml
resources:
  requests:     # Guaranteed resources (scheduling)
    memory: "128Mi"
    cpu: "250m"
  limits:       # Maximum resources (throttling)
    memory: "256Mi"
    cpu: "500m"
```

**Guidelines:**

| Resource | Request | Limit |
|----------|---------|-------|
| CPU | Based on steady-state | 2-4x request |
| Memory | Based on steady-state | ~1.5x request |

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### Pod Disruption Budget

Ensure minimum availability during voluntary disruptions.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  # Or: maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

## Networking

### Ingress

HTTP/HTTPS routing to services.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
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
                name: myapp
                port:
                  number: 80
```

### Network Policies

Control pod-to-pod traffic.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - port: 5432
```

## Helm Charts

Package Kubernetes manifests.

### Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/          # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── _helpers.tpl
└── charts/             # Dependencies
```

### values.yaml

```yaml
replicaCount: 3
image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  requests:
    memory: "128Mi"
    cpu: "250m"
  limits:
    memory: "256Mi"
    cpu: "500m"

ingress:
  enabled: true
  host: api.example.com
```

### Template Example

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

### Helm Commands

```bash
helm install myapp ./mychart              # Install
helm upgrade myapp ./mychart              # Upgrade
helm rollback myapp 1                     # Rollback
helm uninstall myapp                      # Uninstall
helm list                                 # List releases
helm template ./mychart                   # Render templates
```

## Docker Compose

For local development and simple deployments.

```yaml
version: "3.8"

services:
  api:
    build: ./api
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  db:
    image: postgres:15
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: app
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Best Practices

### Image Management

| Practice | Example |
|----------|---------|
| Use specific tags | `myapp:1.2.3` not `myapp:latest` |
| Multi-stage builds | Reduce image size |
| Run as non-root | `USER 1000` in Dockerfile |
| Scan for vulnerabilities | Trivy, Snyk |

### Resource Guidelines

```yaml
# CPU: 1000m = 1 core
# Memory: Mi = mebibytes, Gi = gibibytes

# Small service
resources:
  requests: { cpu: "100m", memory: "128Mi" }
  limits: { cpu: "500m", memory: "256Mi" }

# Medium service
resources:
  requests: { cpu: "250m", memory: "256Mi" }
  limits: { cpu: "1000m", memory: "512Mi" }

# Large service
resources:
  requests: { cpu: "500m", memory: "512Mi" }
  limits: { cpu: "2000m", memory: "1Gi" }
```

### Security

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
    - name: app
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

## Useful Commands

```bash
# Kubectl essentials
kubectl get pods -w                    # Watch pods
kubectl describe pod <name>            # Pod details
kubectl logs <pod> -f                  # Stream logs
kubectl exec -it <pod> -- /bin/sh      # Shell into pod
kubectl port-forward svc/myapp 8080:80 # Local access
kubectl rollout status deployment/myapp # Deployment status
kubectl top pods                       # Resource usage
```

---

Apply these patterns for reliable container orchestration. Start with Deployments and Services, add Ingress for external access, and use Helm for complex applications requiring configuration management.


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

