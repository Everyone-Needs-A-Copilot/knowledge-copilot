---
last_updated: 2026-02-25
status: active
name: kubernetes-patterns
description: Kubernetes patterns - deployments, services, ingress, helm charts. Use for container orchestration.
triggers:
  files: ["**/k8s/**", "**/kubernetes/**", "**/helm/**", "**/*.yaml"]
  keywords: ["kubernetes", "k8s", "deployment", "service", "ingress", "pod", "helm", "kubectl", "container orchestration"]
allowed-tools: Read, Write, Edit
---

# Kubernetes Patterns Deep Expertise

Comprehensive guide to Kubernetes patterns, best practices, and production-ready configurations for container orchestration.

## Core Concepts

### Cluster Architecture

```yaml
# Kubernetes cluster components
# Control Plane: API Server, Scheduler, Controller Manager, etcd
# Node Components: kubelet, kube-proxy, container runtime

# Namespace isolation
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: prod
    team: platform
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
    team: platform
```

### Pod Fundamentals

```yaml
# Basic Pod - avoid in production (use Deployments instead)
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    version: "1.0"
spec:
  containers:
  - name: nginx
    image: nginx:1.25-alpine
    ports:
    - containerPort: 80
      name: http
      protocol: TCP
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    env:
    - name: ENVIRONMENT
      value: "production"
    volumeMounts:
    - name: config
      mountPath: /etc/nginx/conf.d
  volumes:
  - name: config
    configMap:
      name: nginx-config
  restartPolicy: Always
  terminationGracePeriodSeconds: 30
```

### Multi-Container Pod Patterns

```yaml
# Sidecar Pattern - logging sidecar
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  containers:
  # Main application container
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 8080
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log/app

  # Logging sidecar
  - name: log-shipper
    image: fluent/fluent-bit:2.0
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log/app
      readOnly: true
    - name: fluent-config
      mountPath: /fluent-bit/etc/

  volumes:
  - name: shared-logs
    emptyDir: {}
  - name: fluent-config
    configMap:
      name: fluent-bit-config

---
# Ambassador Pattern - proxy sidecar
apiVersion: v1
kind: Pod
metadata:
  name: app-with-ambassador
spec:
  containers:
  # Main application
  - name: app
    image: myapp:1.0
    env:
    - name: DATABASE_HOST
      value: "localhost"  # Connects to ambassador
    - name: DATABASE_PORT
      value: "5432"

  # Ambassador proxy
  - name: db-proxy
    image: haproxy:2.8
    ports:
    - containerPort: 5432
    volumeMounts:
    - name: proxy-config
      mountPath: /usr/local/etc/haproxy/

  volumes:
  - name: proxy-config
    configMap:
      name: haproxy-config

---
# Adapter Pattern - normalize output
apiVersion: v1
kind: Pod
metadata:
  name: app-with-adapter
spec:
  containers:
  # Application with custom metrics format
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 8080
    volumeMounts:
    - name: metrics
      mountPath: /var/metrics

  # Adapter converts custom format to Prometheus
  - name: metrics-adapter
    image: metrics-adapter:1.0
    ports:
    - containerPort: 9090
      name: prometheus
    volumeMounts:
    - name: metrics
      mountPath: /var/metrics
      readOnly: true

  volumes:
  - name: metrics
    emptyDir: {}
```


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Workload Resources

### Deployments (Recommended for Stateless Apps)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    tier: frontend
spec:
  # Replication
  replicas: 3

  # Pod selector
  selector:
    matchLabels:
      app: web-app
      tier: frontend

  # Rolling update strategy
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # Max extra pods during update
      maxUnavailable: 0    # Min available pods during update

  # Pod template
  template:
    metadata:
      labels:
        app: web-app
        tier: frontend
        version: "2.1.0"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      # Pod scheduling
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web-app
              topologyKey: kubernetes.io/hostname

      # Init containers
      initContainers:
      - name: migration
        image: web-app:2.1.0
        command: ['sh', '-c', 'npm run migrate']
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url

      # Main container
      containers:
      - name: app
        image: web-app:2.1.0
        imagePullPolicy: IfNotPresent

        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP

        # Environment variables
        env:
        - name: NODE_ENV
          value: "production"
        - name: PORT
          value: "3000"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: external-api

        # Environment from ConfigMap/Secret
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets

        # Resource management
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "1000m"

        # Health checks
        startupProbe:
          httpGet:
            path: /health/startup
            port: http
          initialDelaySeconds: 0
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 30  # 150s to start

        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 0
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3

        # Volume mounts
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: cache
          mountPath: /app/cache
        - name: tmp
          mountPath: /tmp

        # Security context
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true

        # Lifecycle hooks
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

      # Volumes
      volumes:
      - name: config
        configMap:
          name: app-config
          items:
          - key: app.json
            path: app.json
      - name: cache
        emptyDir:
          sizeLimit: "1Gi"
      - name: tmp
        emptyDir:
          sizeLimit: "500Mi"

      # Security
      securityContext:
        fsGroup: 1000
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault

      # Image pull secrets
      imagePullSecrets:
      - name: registry-credentials

      # Service account
      serviceAccountName: web-app
      automountServiceAccountToken: false

      # DNS config
      dnsPolicy: ClusterFirst

      # Termination grace period
      terminationGracePeriodSeconds: 30
```

### StatefulSets (For Stateful Applications)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: production
spec:
  serviceName: postgres-headless
  replicas: 3

  selector:
    matchLabels:
      app: postgres

  # Persistent volume claim templates
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi

  # Pod management policy
  podManagementPolicy: OrderedReady

  # Update strategy
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0  # Update all pods

  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - name: postgres
          containerPort: 5432

        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name

        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"

        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        - name: config
          mountPath: /etc/postgresql/

        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U postgres
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U postgres
          initialDelaySeconds: 5
          periodSeconds: 5

      volumes:
      - name: config
        configMap:
          name: postgres-config

---
# Headless service for StatefulSet
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
  namespace: production
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: postgres
```

### DaemonSets (One Pod Per Node)

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: node-exporter

  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1

  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      # Run on all nodes including control plane
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        effect: NoSchedule

      hostNetwork: true
      hostPID: true

      containers:
      - name: node-exporter
        image: prom/node-exporter:v1.6.1
        ports:
        - name: metrics
          containerPort: 9100
          hostPort: 9100

        args:
        - --path.procfs=/host/proc
        - --path.sysfs=/host/sys
        - --path.rootfs=/host/root

        resources:
          requests:
            memory: "30Mi"
            cpu: "100m"
          limits:
            memory: "50Mi"
            cpu: "200m"

        volumeMounts:
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: sys
          mountPath: /host/sys
          readOnly: true
        - name: root
          mountPath: /host/root
          readOnly: true

      volumes:
      - name: proc
        hostPath:
          path: /proc
      - name: sys
        hostPath:
          path: /sys
      - name: root
        hostPath:
          path: /
```

### Jobs and CronJobs

```yaml
# One-time job
apiVersion: batch/v1
kind: Job
metadata:
  name: database-backup
  namespace: production
spec:
  # Retry policy
  backoffLimit: 3
  completions: 1
  parallelism: 1

  # Cleanup
  ttlSecondsAfterFinished: 86400  # 24 hours

  template:
    metadata:
      labels:
        app: database-backup
    spec:
      restartPolicy: OnFailure

      containers:
      - name: backup
        image: postgres:15-alpine
        command:
        - /bin/sh
        - -c
        - |
          pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | \
          gzip > /backup/backup-$(date +%Y%m%d-%H%M%S).sql.gz

        env:
        - name: DB_HOST
          value: postgres.production.svc.cluster.local
        - name: DB_USER
          value: postgres
        - name: DB_NAME
          value: myapp
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: password

        volumeMounts:
        - name: backup
          mountPath: /backup

      volumes:
      - name: backup
        persistentVolumeClaim:
          claimName: backup-storage

---
# Scheduled job
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup-daily
  namespace: production
spec:
  # Schedule: daily at 2 AM
  schedule: "0 2 * * *"

  # Concurrency policy
  concurrencyPolicy: Forbid  # Don't run if previous still running

  # Job history
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1

  # Deadline
  startingDeadlineSeconds: 300

  jobTemplate:
    spec:
      backoffLimit: 2
      ttlSecondsAfterFinished: 86400

      template:
        spec:
          restartPolicy: OnFailure

          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - |
              BACKUP_FILE="/backup/backup-$(date +%Y%m%d-%H%M%S).sql.gz"
              pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > "$BACKUP_FILE"

              # Cleanup old backups (keep last 7 days)
              find /backup -name "backup-*.sql.gz" -mtime +7 -delete

            env:
            - name: DB_HOST
              value: postgres.production.svc.cluster.local
            - name: DB_USER
              value: postgres
            - name: DB_NAME
              value: myapp
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password

            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"

            volumeMounts:
            - name: backup
              mountPath: /backup

          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-storage
```

## Services and Networking

### Service Types

```yaml
# ClusterIP - internal cluster access (default)
apiVersion: v1
kind: Service
metadata:
  name: web-app-internal
  namespace: production
  labels:
    app: web-app
spec:
  type: ClusterIP
  selector:
    app: web-app
    tier: frontend
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: metrics
    protocol: TCP
  sessionAffinity: None

---
# NodePort - expose on each node's IP
apiVersion: v1
kind: Service
metadata:
  name: web-app-nodeport
  namespace: production
spec:
  type: NodePort
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 3000
    nodePort: 30080  # 30000-32767 range
    protocol: TCP

---
# LoadBalancer - cloud load balancer
apiVersion: v1
kind: Service
metadata:
  name: web-app-lb
  namespace: production
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 3000
    protocol: TCP
  - name: https
    port: 443
    targetPort: 3000
    protocol: TCP
  loadBalancerSourceRanges:
  - 10.0.0.0/8
  - 172.16.0.0/12

---
# Headless Service - no load balancing, direct pod IPs
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
  namespace: production
spec:
  clusterIP: None  # Headless
  selector:
    app: postgres
  ports:
  - name: postgres
    port: 5432
    targetPort: 5432
    protocol: TCP
  publishNotReadyAddresses: true  # Include non-ready pods in DNS

---
# ExternalName - DNS CNAME alias
apiVersion: v1
kind: Service
metadata:
  name: external-db
  namespace: production
spec:
  type: ExternalName
  externalName: db.example.com
  ports:
  - port: 5432
```

### Ingress Resources

```yaml
# Nginx Ingress with TLS
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: production
  annotations:
    # Nginx specific
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"

    # Rate limiting
    nginx.ingress.kubernetes.io/limit-rps: "100"
    nginx.ingress.kubernetes.io/limit-connections: "10"

    # CORS
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://example.com"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"

    # Timeouts
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"

    # WebSocket support
    nginx.ingress.kubernetes.io/websocket-services: "web-app"

    # Client body size
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"

    # Cert-manager
    cert-manager.io/cluster-issuer: "letsencrypt-prod"

spec:
  ingressClassName: nginx

  tls:
  - hosts:
    - app.example.com
    - api.example.com
    secretName: app-tls-cert

  rules:
  # Web application
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app
            port:
              name: http

  # API service
  - host: api.example.com
    http:
      paths:
      - path: /v1
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
      - path: /v2
        pathType: Prefix
        backend:
          service:
            name: api-service-v2
            port:
              number: 8080

---
# Path-based routing with rewrites
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-path-routing
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: services.example.com
    http:
      paths:
      # /api/v1/users -> service-a/users
      - path: /api/v1(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: service-a
            port:
              number: 80
      # /api/v2/products -> service-b/products
      - path: /api/v2(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: service-b
            port:
              number: 80

---
# Canary deployment with traffic splitting
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-canary
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"  # 10% traffic
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-canary
            port:
              number: 80
```

### Network Policies

```yaml
# Deny all traffic by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Allow frontend to backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: backend

  policyTypes:
  - Ingress

  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: frontend
    ports:
    - protocol: TCP
      port: 8080

---
# Allow backend to database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-db
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgres

  policyTypes:
  - Ingress

  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: backend
    ports:
    - protocol: TCP
      port: 5432

---
# Allow egress to external services
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: backend

  policyTypes:
  - Egress

  egress:
  # DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53

  # HTTPS to external
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443

  # Specific external IPs
  - to:
    - ipBlock:
        cidr: 203.0.113.0/24
    ports:
    - protocol: TCP
      port: 443

---
# Allow ingress from specific namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-monitoring
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-app

  policyTypes:
  - Ingress

  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    - podSelector:
        matchLabels:
          app: prometheus
    ports:
    - protocol: TCP
      port: 9090
```

## Configuration Management

### ConfigMaps

```yaml
# ConfigMap from literal values
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  # Simple key-value
  database.host: "postgres.production.svc.cluster.local"
  database.port: "5432"
  log.level: "info"

  # JSON configuration
  app.json: |
    {
      "server": {
        "port": 3000,
        "timeout": 30
      },
      "features": {
        "enableCache": true,
        "cacheSize": 1000
      }
    }

  # Configuration file
  nginx.conf: |
    server {
      listen 80;
      server_name _;

      location / {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
      }

      location /health {
        return 200 "OK\n";
        add_header Content-Type text/plain;
      }
    }

  # Script file
  init.sh: |
    #!/bin/bash
    set -e

    echo "Running initialization..."
    npm run migrate
    npm run seed
    echo "Initialization complete"

---
# Using ConfigMap in Pod
apiVersion: v1
kind: Pod
metadata:
  name: app-with-config
spec:
  containers:
  - name: app
    image: myapp:1.0

    # Environment variables from ConfigMap
    env:
    - name: DB_HOST
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database.host
    - name: DB_PORT
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database.port

    # All keys as environment variables
    envFrom:
    - configMapRef:
        name: app-config
        prefix: APP_  # Keys become APP_database.host, etc.

    # Mount as files
    volumeMounts:
    - name: config-json
      mountPath: /app/config/app.json
      subPath: app.json
    - name: config-nginx
      mountPath: /etc/nginx/nginx.conf
      subPath: nginx.conf
    - name: scripts
      mountPath: /scripts

  volumes:
  # Mount specific keys
  - name: config-json
    configMap:
      name: app-config
      items:
      - key: app.json
        path: app.json

  - name: config-nginx
    configMap:
      name: app-config
      items:
      - key: nginx.conf
        path: nginx.conf

  # Mount all keys
  - name: scripts
    configMap:
      name: app-config
      defaultMode: 0755  # Executable
```

### Secrets

```yaml
# Opaque secret (generic)
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: production
type: Opaque
data:
  # Base64 encoded values
  username: cG9zdGdyZXM=
  password: c3VwZXJzZWNyZXQ=
  url: cG9zdGdyZXNxbDovL3Bvc3RncmVzOnN1cGVyc2VjcmV0QHBvc3RncmVzOjU0MzIvbXlhcHA=
stringData:
  # Plain text (will be base64 encoded)
  connection-string: "postgresql://postgres:supersecret@postgres:5432/myapp"

---
# TLS secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-cert
  namespace: production
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi... # Base64 encoded certificate
  tls.key: LS0tLS1CRUdJTi... # Base64 encoded private key

---
# Docker registry secret
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials
  namespace: production
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: eyJhdXRocyI6eyJyZWdpc3RyeS5leGFtcGxlLmNvbSI6eyJ1c2VybmFtZSI6InVzZXIiLCJwYXNzd29yZCI6InBhc3MiLCJhdXRoIjoiZFhObGNqcHdZWE56In19fQ==

---
# SSH auth secret
apiVersion: v1
kind: Secret
metadata:
  name: ssh-key
  namespace: production
type: kubernetes.io/ssh-auth
data:
  ssh-privatekey: LS0tLS1CRUdJTi... # Base64 encoded private key

---
# Basic auth secret
apiVersion: v1
kind: Secret
metadata:
  name: basic-auth
  namespace: production
type: kubernetes.io/basic-auth
stringData:
  username: admin
  password: supersecret

---
# Using secrets in Pod
apiVersion: v1
kind: Pod
metadata:
  name: app-with-secrets
spec:
  containers:
  - name: app
    image: myapp:1.0

    # Environment variables from Secret
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password

    # All keys as environment variables
    envFrom:
    - secretRef:
        name: db-credentials
        prefix: DB_

    # Mount as files
    volumeMounts:
    - name: tls
      mountPath: /etc/tls
      readOnly: true
    - name: ssh-key
      mountPath: /root/.ssh
      readOnly: true
      defaultMode: 0400

  volumes:
  - name: tls
    secret:
      secretName: tls-cert
      items:
      - key: tls.crt
        path: cert.pem
      - key: tls.key
        path: key.pem

  - name: ssh-key
    secret:
      secretName: ssh-key

  # Image pull secret
  imagePullSecrets:
  - name: registry-credentials
```

## Storage

### PersistentVolumes and Claims

```yaml
# PersistentVolume (cluster-level resource)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv-1
  labels:
    type: fast-ssd
spec:
  capacity:
    storage: 100Gi

  accessModes:
  - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  storageClassName: fast-ssd

  # Host path (local testing only)
  hostPath:
    path: /mnt/data/postgres
    type: DirectoryOrCreate

---
# PersistentVolume with NFS
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 1Ti
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    server: nfs-server.example.com
    path: /exports/data

---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: production
spec:
  accessModes:
  - ReadWriteOnce

  resources:
    requests:
      storage: 100Gi

  storageClassName: fast-ssd

  selector:
    matchLabels:
      type: fast-ssd

---
# StorageClass (dynamic provisioning)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete

---
# Using PVC in Pod
apiVersion: v1
kind: Pod
metadata:
  name: postgres
spec:
  containers:
  - name: postgres
    image: postgres:15-alpine
    volumeMounts:
    - name: data
      mountPath: /var/lib/postgresql/data

  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: postgres-pvc

---
# Dynamic PVC (automatically creates PV)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
  namespace: production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd  # Uses StorageClass provisioner
  resources:
    requests:
      storage: 50Gi
```

### Volume Types

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-examples
spec:
  containers:
  - name: app
    image: busybox
    command: ['sh', '-c', 'sleep 3600']

    volumeMounts:
    # EmptyDir - temporary storage
    - name: cache
      mountPath: /cache

    # EmptyDir with memory backing
    - name: tmp-memory
      mountPath: /tmp-memory

    # ConfigMap
    - name: config
      mountPath: /config

    # Secret
    - name: secrets
      mountPath: /secrets

    # PVC
    - name: data
      mountPath: /data

    # HostPath
    - name: host-logs
      mountPath: /host-logs
      readOnly: true

    # Projected volume (multiple sources)
    - name: combined
      mountPath: /combined

    # Downward API (pod metadata)
    - name: podinfo
      mountPath: /etc/podinfo

  volumes:
  # EmptyDir
  - name: cache
    emptyDir:
      sizeLimit: "1Gi"

  # EmptyDir in memory
  - name: tmp-memory
    emptyDir:
      medium: Memory
      sizeLimit: "256Mi"

  # ConfigMap
  - name: config
    configMap:
      name: app-config

  # Secret
  - name: secrets
    secret:
      secretName: app-secrets
      defaultMode: 0400

  # PVC
  - name: data
    persistentVolumeClaim:
      claimName: app-data

  # HostPath (use with caution)
  - name: host-logs
    hostPath:
      path: /var/log
      type: Directory

  # Projected volume
  - name: combined
    projected:
      sources:
      - configMap:
          name: config1
      - configMap:
          name: config2
      - secret:
          name: secret1

  # Downward API
  - name: podinfo
    downwardAPI:
      items:
      - path: "labels"
        fieldRef:
          fieldPath: metadata.labels
      - path: "annotations"
        fieldRef:
          fieldPath: metadata.annotations
      - path: "namespace"
        fieldRef:
          fieldPath: metadata.namespace
      - path: "name"
        fieldRef:
          fieldPath: metadata.name
```

## Resource Management

### Resource Requests and Limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-demo
spec:
  containers:
  # Standard application
  - name: app
    image: myapp:1.0
    resources:
      requests:
        memory: "256Mi"  # Guaranteed memory
        cpu: "250m"      # 0.25 CPU cores
      limits:
        memory: "512Mi"  # Max memory before OOMKill
        cpu: "1000m"     # Max CPU (throttled)

  # Memory-intensive job
  - name: batch-processor
    image: processor:1.0
    resources:
      requests:
        memory: "2Gi"
        cpu: "1000m"
      limits:
        memory: "4Gi"
        cpu: "4000m"

  # Burstable workload
  - name: worker
    image: worker:1.0
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "2000m"

---
# ResourceQuota - namespace limits
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    # Compute
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi

    # Storage
    requests.storage: "1Ti"
    persistentvolumeclaims: "50"

    # Objects
    pods: "100"
    services: "50"
    secrets: "100"
    configmaps: "100"

    # Services
    services.loadbalancers: "5"
    services.nodeports: "10"

---
# LimitRange - default and max resources
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-limits
  namespace: production
spec:
  limits:
  # Container defaults
  - type: Container
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "250m"
      memory: "256Mi"
    max:
      cpu: "4000m"
      memory: "8Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    maxLimitRequestRatio:
      cpu: "4"      # Limit can be max 4x request
      memory: "2"   # Limit can be max 2x request

  # Pod limits
  - type: Pod
    max:
      cpu: "16000m"
      memory: "32Gi"
    min:
      cpu: "100m"
      memory: "128Mi"

  # PVC limits
  - type: PersistentVolumeClaim
    max:
      storage: "100Gi"
    min:
      storage: "1Gi"

---
# PriorityClass - pod scheduling priority
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "High priority for critical services"

---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 100
globalDefault: false
description: "Low priority for batch jobs"

---
# Using PriorityClass
apiVersion: v1
kind: Pod
metadata:
  name: critical-app
spec:
  priorityClassName: high-priority
  containers:
  - name: app
    image: critical-app:1.0
```

## Health Checks and Probes

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-check-demo
spec:
  containers:
  - name: app
    image: myapp:1.0

    # Startup probe - initial startup check
    # Prevents liveness/readiness from running until successful
    startupProbe:
      httpGet:
        path: /health/startup
        port: 8080
        httpHeaders:
        - name: User-Agent
          value: "Kubernetes-Startup"
      initialDelaySeconds: 0
      periodSeconds: 5
      timeoutSeconds: 3
      successThreshold: 1
      failureThreshold: 30  # 150 seconds to start

    # Liveness probe - restart if failing
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8080
        scheme: HTTP
      initialDelaySeconds: 0  # Startup probe handles initial delay
      periodSeconds: 10
      timeoutSeconds: 3
      successThreshold: 1
      failureThreshold: 3  # Restart after 3 failures

    # Readiness probe - remove from service if failing
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8080
      initialDelaySeconds: 0
      periodSeconds: 5
      timeoutSeconds: 3
      successThreshold: 1
      failureThreshold: 3

---
# TCP probe
apiVersion: v1
kind: Pod
metadata:
  name: tcp-probe
spec:
  containers:
  - name: redis
    image: redis:7-alpine
    livenessProbe:
      tcpSocket:
        port: 6379
      initialDelaySeconds: 15
      periodSeconds: 10
    readinessProbe:
      tcpSocket:
        port: 6379
      initialDelaySeconds: 5
      periodSeconds: 5

---
# Exec probe
apiVersion: v1
kind: Pod
metadata:
  name: exec-probe
spec:
  containers:
  - name: postgres
    image: postgres:15-alpine
    livenessProbe:
      exec:
        command:
        - /bin/sh
        - -c
        - pg_isready -U postgres
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      exec:
        command:
        - /bin/sh
        - -c
        - |
          pg_isready -U postgres && \
          psql -U postgres -c "SELECT 1" > /dev/null
      initialDelaySeconds: 5
      periodSeconds: 5

---
# gRPC probe (requires gRPC health checking protocol)
apiVersion: v1
kind: Pod
metadata:
  name: grpc-probe
spec:
  containers:
  - name: grpc-service
    image: grpc-service:1.0
    livenessProbe:
      grpc:
        port: 9090
      initialDelaySeconds: 10
      periodSeconds: 10
    readinessProbe:
      grpc:
        port: 9090
        service: myservice.v1.HealthCheck
      initialDelaySeconds: 5
      periodSeconds: 5
```

## Autoscaling

### Horizontal Pod Autoscaler

```yaml
# HPA based on CPU/Memory
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app

  minReplicas: 3
  maxReplicas: 50

  metrics:
  # CPU utilization
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Target 70% CPU

  # Memory utilization
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80  # Target 80% memory

  # Custom metrics (requires metrics server)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"

  # External metrics (e.g., queue length)
  - type: External
    external:
      metric:
        name: queue_messages
        selector:
          matchLabels:
            queue: work-queue
      target:
        type: AverageValue
        averageValue: "100"

  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5min before scaling down
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60  # Max 50% reduction per minute
      - type: Pods
        value: 5
        periodSeconds: 60  # Max 5 pods per minute
      selectPolicy: Min  # Use most conservative

    scaleUp:
      stabilizationWindowSeconds: 0  # Scale up immediately
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15  # Double every 15 seconds
      - type: Pods
        value: 10
        periodSeconds: 15  # Max 10 pods every 15 seconds
      selectPolicy: Max  # Use most aggressive

---
# Vertical Pod Autoscaler (requires VPA controller)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-app-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app

  updatePolicy:
    updateMode: "Auto"  # or "Recreate", "Initial", "Off"

  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: "100m"
        memory: "128Mi"
      maxAllowed:
        cpu: "4000m"
        memory: "8Gi"
      controlledResources: ["cpu", "memory"]
      mode: Auto
```

## Security

### Pod Security

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  # Security context for all containers
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    fsGroupChangePolicy: "OnRootMismatch"
    seccompProfile:
      type: RuntimeDefault

  containers:
  - name: app
    image: myapp:1.0

    # Container-specific security context
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE  # Only if needed
      seccompProfile:
        type: RuntimeDefault

    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache

  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}

  # Service account
  serviceAccountName: app-sa
  automountServiceAccountToken: false  # Don't mount unless needed

---
# ServiceAccount with minimal permissions
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
automountServiceAccountToken: false

---
# Role with limited permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["app-secrets"]  # Specific secret only
  verbs: ["get"]

---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: production
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRole for cluster-wide resources
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]

---
# ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-reader-binding
subjects:
- kind: ServiceAccount
  name: monitoring-sa
  namespace: monitoring
roleRef:
  kind: ClusterRole
  name: node-reader
  apiGroup: rbac.authorization.k8s.io

---
# PodSecurityPolicy (deprecated in 1.25, use Pod Security Standards)
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
  volumes:
  - 'configMap'
  - 'emptyDir'
  - 'projected'
  - 'secret'
  - 'downwardAPI'
  - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true
```

## Helm Charts

### Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/          # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl   # Template helpers
│   └── NOTES.txt      # Post-install notes
├── charts/            # Chart dependencies
└── .helmignore        # Files to ignore
```

### Chart.yaml

```yaml
apiVersion: v2
name: web-app
description: A Helm chart for web application
type: application
version: 1.2.3        # Chart version
appVersion: "2.1.0"   # Application version

keywords:
- web
- api
- nodejs

maintainers:
- name: Team Platform
  email: platform@example.com

dependencies:
- name: postgresql
  version: "12.x.x"
  repository: "https://charts.bitnami.com/bitnami"
  condition: postgresql.enabled

- name: redis
  version: "17.x.x"
  repository: "https://charts.bitnami.com/bitnami"
  condition: redis.enabled
```

### values.yaml

```yaml
# Default values for web-app chart

replicaCount: 3

image:
  repository: myregistry.io/web-app
  pullPolicy: IfNotPresent
  tag: ""  # Defaults to Chart.appVersion

imagePullSecrets:
- name: registry-credentials

nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""
  automountServiceAccountToken: false

podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "9090"

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop:
    - ALL

service:
  type: ClusterIP
  port: 80
  targetPort: 3000
  annotations: {}

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
  - host: app.example.com
    paths:
    - path: /
      pathType: Prefix
  tls:
  - secretName: app-tls
    hosts:
    - app.example.com

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "1000m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 50
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - web-app
        topologyKey: kubernetes.io/hostname

env:
  NODE_ENV: production
  PORT: "3000"

envFrom:
- configMapRef:
    name: app-config
- secretRef:
    name: app-secrets

configMap:
  create: true
  data:
    LOG_LEVEL: "info"

probes:
  startup:
    enabled: true
    path: /health/startup
    initialDelaySeconds: 0
    periodSeconds: 5
    failureThreshold: 30

  liveness:
    enabled: true
    path: /health/live
    initialDelaySeconds: 0
    periodSeconds: 10
    failureThreshold: 3

  readiness:
    enabled: true
    path: /health/ready
    initialDelaySeconds: 0
    periodSeconds: 5
    failureThreshold: 3

# Dependency settings
postgresql:
  enabled: true
  auth:
    username: myapp
    database: myapp
  primary:
    persistence:
      enabled: true
      size: 100Gi

redis:
  enabled: true
  master:
    persistence:
      enabled: true
      size: 10Gi
```

### templates/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "web-app.fullname" . }}
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "web-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "web-app.selectorLabels" . | nindent 6 }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "web-app.selectorLabels" . | nindent 8 }}
        version: {{ .Chart.AppVersion | quote }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "web-app.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        {{- if .Values.probes.startup.enabled }}
        startupProbe:
          httpGet:
            path: {{ .Values.probes.startup.path }}
            port: http
          initialDelaySeconds: {{ .Values.probes.startup.initialDelaySeconds }}
          periodSeconds: {{ .Values.probes.startup.periodSeconds }}
          failureThreshold: {{ .Values.probes.startup.failureThreshold }}
        {{- end }}
        {{- if .Values.probes.liveness.enabled }}
        livenessProbe:
          httpGet:
            path: {{ .Values.probes.liveness.path }}
            port: http
          initialDelaySeconds: {{ .Values.probes.liveness.initialDelaySeconds }}
          periodSeconds: {{ .Values.probes.liveness.periodSeconds }}
          failureThreshold: {{ .Values.probes.liveness.failureThreshold }}
        {{- end }}
        {{- if .Values.probes.readiness.enabled }}
        readinessProbe:
          httpGet:
            path: {{ .Values.probes.readiness.path }}
            port: http
          initialDelaySeconds: {{ .Values.probes.readiness.initialDelaySeconds }}
          periodSeconds: {{ .Values.probes.readiness.periodSeconds }}
          failureThreshold: {{ .Values.probes.readiness.failureThreshold }}
        {{- end }}
        env:
        {{- range $key, $value := .Values.env }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        {{- with .Values.envFrom }}
        envFrom:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

### templates/_helpers.tpl

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "web-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "web-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "web-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "web-app.labels" -}}
helm.sh/chart: {{ include "web-app.chart" . }}
{{ include "web-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "web-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "web-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "web-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "web-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

### Helm Commands

```bash
# Create new chart
helm create mychart

# Lint chart
helm lint ./mychart

# Template rendering (dry-run)
helm template myrelease ./mychart
helm template myrelease ./mychart --values custom-values.yaml

# Install
helm install myrelease ./mychart
helm install myrelease ./mychart --values production.yaml
helm install myrelease ./mychart --set replicaCount=5

# Upgrade
helm upgrade myrelease ./mychart
helm upgrade --install myrelease ./mychart  # Install if not exists

# Rollback
helm rollback myrelease
helm rollback myrelease 3  # To specific revision

# List releases
helm list
helm list --all-namespaces

# Get release info
helm get all myrelease
helm get values myrelease
helm get manifest myrelease

# Uninstall
helm uninstall myrelease

# Repository management
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo postgresql

# Package chart
helm package ./mychart
helm push mychart-1.2.3.tgz oci://registry.example.com/charts
```

## Debugging and Troubleshooting

```bash
# Pod logs
kubectl logs pod-name
kubectl logs pod-name -c container-name
kubectl logs pod-name --previous  # Previous crashed container
kubectl logs -f pod-name  # Follow
kubectl logs pod-name --tail=100
kubectl logs pod-name --since=1h

# Execute commands in pod
kubectl exec -it pod-name -- /bin/sh
kubectl exec pod-name -- env
kubectl exec pod-name -- cat /etc/config/app.json

# Describe resources (events, status)
kubectl describe pod pod-name
kubectl describe node node-name
kubectl describe deployment deployment-name

# Get events
kubectl get events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector involvedObject.name=pod-name

# Port forwarding
kubectl port-forward pod-name 8080:80
kubectl port-forward service/web-app 8080:80

# Copy files
kubectl cp pod-name:/path/to/file ./local-file
kubectl cp ./local-file pod-name:/path/to/file

# Resource usage
kubectl top nodes
kubectl top pods
kubectl top pods --all-namespaces
kubectl top pods -l app=web-app

# Debug pod (ephemeral container)
kubectl debug pod-name -it --image=busybox
kubectl debug pod-name -it --image=nicolaka/netshoot --target=container-name

# Create debug copy of pod
kubectl debug pod-name -it --copy-to=debug-pod --image=ubuntu

# API resources
kubectl api-resources
kubectl api-versions

# Explain resource fields
kubectl explain pod.spec.containers
kubectl explain deployment.spec.strategy

# Diff before apply
kubectl diff -f deployment.yaml

# Apply with dry-run
kubectl apply -f deployment.yaml --dry-run=client
kubectl apply -f deployment.yaml --dry-run=server

# Get raw JSON/YAML
kubectl get pod pod-name -o yaml
kubectl get pod pod-name -o json | jq '.spec.containers[0].image'

# Watch resources
kubectl get pods --watch
kubectl get pods -w

# Drain node (maintenance)
kubectl drain node-name --ignore-daemonsets
kubectl uncordon node-name

# Cordon node (prevent scheduling)
kubectl cordon node-name
```

## Best Practices

### Resource Organization

```yaml
# Use namespaces for logical separation
production/
  web-app/
  database/
  monitoring/

staging/
  web-app/
  database/

# Label everything consistently
labels:
  app.kubernetes.io/name: myapp
  app.kubernetes.io/instance: myapp-prod
  app.kubernetes.io/version: "1.2.3"
  app.kubernetes.io/component: frontend
  app.kubernetes.io/part-of: ecommerce
  app.kubernetes.io/managed-by: helm
  environment: production
  team: platform
  cost-center: engineering

# Annotations for metadata
annotations:
  description: "Web application frontend"
  contact: "platform@example.com"
  runbook: "https://docs.example.com/runbooks/web-app"
  deployment.kubernetes.io/revision: "12"
```

### Configuration Management

1. **Use ConfigMaps for config**, Secrets for sensitive data
2. **Mount as files** rather than environment variables when possible
3. **Use immutable ConfigMaps/Secrets** for better caching
4. **Version your configs** with labels
5. **Never hardcode** environment-specific values

### Resource Management

1. **Always set requests and limits**
2. **Requests should match typical usage**
3. **Limits should allow for bursts** (2-4x requests)
4. **Use VPA for workloads with variable resource needs**
5. **Set PodDisruptionBudgets** for high availability

### Health Checks

1. **Use all three probes** (startup, liveness, readiness)
2. **Startup probe** handles slow-starting apps
3. **Liveness probe** restarts hung containers
4. **Readiness probe** controls service traffic
5. **Separate endpoints** for each probe type
6. **Fast probe responses** (< 1 second)

### Security

1. **Run as non-root** user
2. **Drop all capabilities**, add back only what's needed
3. **Read-only root filesystem**
4. **Use seccomp profiles**
5. **NetworkPolicies** for micro-segmentation
6. **Minimize ServiceAccount** permissions
7. **Image scanning** in CI/CD
8. **Regular security updates**

### Deployment Strategies

```yaml
# Blue-Green: Full switch
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 100%
    maxUnavailable: 0

# Canary: Gradual rollout
# Use multiple Deployments with Service selector
# Or use service mesh (Istio, Linkerd)

# Recreate: Downtime acceptable
strategy:
  type: Recreate
```

## Anti-Patterns to Avoid

1. **Don't run databases in Kubernetes** (unless using operator with expertise)
2. **Don't use latest tag** in production
3. **Don't skip resource limits**
4. **Don't ignore health checks**
5. **Don't use hostPath** unless absolutely necessary
6. **Don't run as root**
7. **Don't store secrets in ConfigMaps**
8. **Don't use Deployment for stateful workloads**
9. **Don't skip testing** in staging environment
10. **Don't ignore pod disruption budgets** for critical services

## Observability

```yaml
# Prometheus scraping annotations
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"

# Structured logging
- name: LOG_FORMAT
  value: "json"
- name: LOG_LEVEL
  value: "info"

# Distributed tracing
- name: JAEGER_AGENT_HOST
  value: "jaeger-agent.monitoring.svc"
- name: JAEGER_AGENT_PORT
  value: "6831"

# Custom metrics
- name: STATSD_HOST
  value: "statsd.monitoring.svc"
```

---

This skill covers comprehensive Kubernetes patterns for production deployments. Use these patterns as building blocks and adapt to specific requirements.



## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

