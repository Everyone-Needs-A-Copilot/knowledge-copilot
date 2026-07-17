---
last_updated: 2026-02-25
status: active
name: docker-patterns
description: Container best practices, multi-stage builds, Docker Compose, image optimization. Use when working with containers.
triggers:
  files: ["**/Dockerfile", "**/docker-compose.yml", "**/docker-compose.yaml", "**/.dockerignore"]
  keywords: ["docker", "container", "image", "Dockerfile", "docker-compose", "multi-stage", "layer", "volume", "build"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides creation of production-grade containerized applications using Docker best practices. Apply these patterns when building images, orchestrating services, or optimizing container workflows.

The user provides containerization requirements: Dockerfile creation, Docker Compose setup, image optimization, or debugging container issues.

## Core Principles

Container excellence is built on five pillars:

1. **Immutability**: Images are immutable artifacts. Configuration varies via environment variables, not image rebuilds.
2. **Minimalism**: Smaller images mean faster deployments, reduced attack surface, and lower costs.
3. **Security**: Run as non-root, scan for vulnerabilities, never bake secrets into images.
4. **Reproducibility**: Pin all versions (base images, dependencies). Avoid `:latest` in production.
5. **Layering**: Optimize layer cache for faster builds. Order instructions from least-to-most frequently changed.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Dockerfile Patterns

### Multi-Stage Builds (Builder Pattern)

The gold standard for production images. Build artifacts in one stage, copy only what's needed to runtime stage.

**Python (FastAPI) Example:**
```dockerfile
# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Minimal final image
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Node.js (Next.js) Example:**
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy necessary files
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

**Go Example:**
```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files first (cache layer)
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build static binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Runtime (distroless)
FROM gcr.io/distroless/static-debian11

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/main .

# Distroless runs as non-root by default
USER nonroot:nonroot

EXPOSE 8080

CMD ["./main"]
```

### Layer Caching Optimization

Order Dockerfile instructions from least-to-most frequently changed:

```dockerfile
# 1. Base image (changes rarely)
FROM python:3.11-slim

# 2. System packages (changes rarely)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Dependencies (changes occasionally)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Application code (changes frequently)
COPY . .

# 5. Runtime command (changes rarely)
CMD ["python", "app.py"]
```

**WRONG** (application changes invalidate dependency cache):
```dockerfile
FROM python:3.11-slim
COPY . .  # ❌ Copies everything first
RUN pip install -r requirements.txt  # Cache invalidated on every code change
CMD ["python", "app.py"]
```

### Base Image Selection

Choose the right base for your use case:

| Base Image | Size | Use Case | Security |
|------------|------|----------|----------|
| `alpine` | ~5MB | Minimal, space-constrained | Good (minimal packages) |
| `slim` | ~40MB | Python, balance of size/compatibility | Good |
| `distroless` | ~20MB | Go, Java, static binaries | Excellent (no shell, no package manager) |
| `scratch` | 0MB | Static binaries only (Go, Rust) | Excellent (nothing but your binary) |
| `full` (e.g., `python:3.11`) | ~300MB | Development, debugging | Fair (many packages) |

**Recommendation by Language:**
- **Python**: `python:3.11-slim` (good compatibility with C extensions)
- **Node.js**: `node:20-alpine` (npm works well on Alpine)
- **Go**: `gcr.io/distroless/static` or `scratch` (static binaries)
- **Java**: `eclipse-temurin:17-jre-alpine` (JRE only, not full JDK)

### COPY vs ADD

**Always prefer COPY unless you need ADD's special features:**

```dockerfile
# ✅ COPY - Explicit, predictable
COPY requirements.txt .
COPY src/ /app/src/

# ❌ ADD - Auto-extracts tarballs, downloads URLs (confusing)
ADD archive.tar.gz /app/  # Only use if you want auto-extraction
```

**ADD's special features:**
1. Auto-extracts `.tar.gz` archives
2. Downloads files from URLs

Unless you need these, use `COPY`.

### RUN Instruction Optimization

Combine commands to reduce layers and clean up in the same layer:

```dockerfile
# ✅ GOOD - Single layer, cleaned up
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ❌ BAD - Multiple layers, cache not cleaned
RUN apt-get update
RUN apt-get install -y curl git
RUN rm -rf /var/lib/apt/lists/*  # Too late, layer already created
```

**Why?** Each `RUN` creates a new layer. Cleanup in a separate `RUN` doesn't reduce image size because previous layers still contain the cached files.

### USER Instruction (Non-Root Containers)

**Never run containers as root in production:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy application code (owned by appuser)
COPY --chown=appuser:appuser . .

CMD ["python", "app.py"]
```

**Why?** If an attacker escapes the container, they'll have root privileges on the host if the container runs as root.

### HEALTHCHECK Instruction

Define health checks for orchestration systems (Docker Compose, Kubernetes):

```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Python-specific (if curl not available)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

# TCP check (if no HTTP endpoint)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD nc -z localhost 5432 || exit 1
```

**Parameters:**
- `--interval`: Time between checks (default: 30s)
- `--timeout`: Max time for check to complete (default: 30s)
- `--start-period`: Grace period before checks start (default: 0s)
- `--retries`: Consecutive failures to mark unhealthy (default: 3)

### ARG vs ENV

**ARG**: Build-time variables (not available at runtime)
**ENV**: Runtime environment variables (persisted in image)

```dockerfile
# ARG - Build-time only (e.g., version, build flags)
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ARG BUILD_DATE
ARG GIT_COMMIT
LABEL build_date=$BUILD_DATE
LABEL git_commit=$GIT_COMMIT

# ENV - Runtime variables (available in running container)
ENV APP_ENV=production
ENV LOG_LEVEL=info

# ARG can be overridden at build time:
# docker build --build-arg PYTHON_VERSION=3.10 .
```

**Use ARG for:**
- Base image versions
- Build flags
- Metadata (commit SHA, build date)

**Use ENV for:**
- Application configuration
- Runtime behavior
- Service endpoints

### ENTRYPOINT vs CMD

**ENTRYPOINT**: Main executable (hard to override)
**CMD**: Default arguments (easy to override)

```dockerfile
# Pattern 1: ENTRYPOINT + CMD (recommended for most apps)
ENTRYPOINT ["python", "app.py"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
# Run: docker run myapp
# Override: docker run myapp --port 9000

# Pattern 2: CMD only (flexible)
CMD ["python", "app.py", "--host", "0.0.0.0"]
# Run: docker run myapp
# Override: docker run myapp python debug.py

# Pattern 3: ENTRYPOINT only (enforced)
ENTRYPOINT ["python", "app.py", "--host", "0.0.0.0"]
# Run: docker run myapp
# Override: docker run --entrypoint bash myapp
```

**Best Practice**: Use `ENTRYPOINT` for the main command, `CMD` for default arguments.

## Image Optimization

### Minimize Layers

Each `RUN`, `COPY`, `ADD` creates a new layer. Combine where possible:

```dockerfile
# ✅ GOOD - 3 layers
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt

# ❌ BAD - 6 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
```

### .dockerignore Best Practices

Exclude unnecessary files from build context (faster builds, smaller images):

```
# .dockerignore

# Version control
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# Node.js
node_modules/
npm-debug.log
yarn-error.log
.next/
out/
.cache/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Documentation
README.md
docs/
*.md

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Environment
.env
.env.local
*.env

# Logs
*.log
logs/

# Test files
tests/
test/
*.test.js
*.spec.ts
```

**Size Impact**: A typical Python project with `.dockerignore` can reduce build context from 500MB to 50MB.

### Dependency Caching Strategies

**Python (pip):**
```dockerfile
# Copy only requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code after (doesn't invalidate pip cache)
COPY . .
```

**Node.js (npm):**
```dockerfile
# Copy only package files first
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Copy application code after
COPY . .
```

**Go (modules):**
```dockerfile
# Copy only go.mod/go.sum first
COPY go.mod go.sum ./
RUN go mod download

# Copy source code after
COPY . .
```

**Why?** If only application code changes (not dependencies), Docker reuses the cached dependency layer.

### Image Size Reduction Techniques

**1. Use slim/alpine base images:**
```dockerfile
# Before: 900MB
FROM python:3.11

# After: 150MB
FROM python:3.11-slim
```

**2. Clean up package manager cache:**
```dockerfile
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*  # Clean apt cache

RUN apk add --no-cache curl  # Alpine: --no-cache flag
```

**3. Multi-stage builds (remove build tools):**
```dockerfile
FROM python:3.11 AS builder
RUN pip install --target=/app/deps -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /app/deps /usr/local/lib/python3.11/site-packages/
```

**4. Remove unnecessary files:**
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt && \
    find /usr/local/lib/python3.11 -name "*.pyc" -delete && \
    find /usr/local/lib/python3.11 -name "__pycache__" -delete
```

### Pinning Versions (Avoid :latest)

**Never use `:latest` in production:**

```dockerfile
# ❌ BAD - Non-reproducible builds
FROM python:latest
RUN pip install flask

# ✅ GOOD - Reproducible builds
FROM python:3.11.6-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
```

**requirements.txt:**
```
flask==3.0.0
requests==2.31.0
sqlalchemy==2.0.23
```

**Why?** `:latest` changes over time. A build that works today may break tomorrow.

## Docker Compose

### Service Definition Patterns

**Full-Stack Application Example:**
```yaml
version: '3.8'

services:
  # Backend API
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
      args:
        BUILD_DATE: ${BUILD_DATE}
    image: myapp/api:latest
    container_name: myapp_api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/myapp
      REDIS_URL: redis://redis:6379/0
      LOG_LEVEL: ${LOG_LEVEL:-info}
    env_file:
      - .env
    volumes:
      - ./api:/app  # Development: hot reload
      - /app/__pycache__  # Exclude cache
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - backend
      - frontend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s

  # Frontend (Next.js)
  web:
    build:
      context: ./web
      dockerfile: Dockerfile
      target: development  # Multi-stage target
    image: myapp/web:latest
    container_name: myapp_web
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    volumes:
      - ./web:/app
      - /app/node_modules
      - /app/.next
    depends_on:
      - api
    networks:
      - frontend

  # PostgreSQL
  db:
    image: postgres:16-alpine
    container_name: myapp_db
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    container_name: myapp_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Worker (Celery)
  worker:
    build:
      context: ./api
      dockerfile: Dockerfile
    image: myapp/api:latest
    container_name: myapp_worker
    restart: unless-stopped
    command: celery -A app.celery worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/myapp
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis
    networks:
      - backend

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

### Networks (Bridge, Host, Custom)

**Bridge (default)**: Isolated network, containers can communicate by name.
```yaml
networks:
  mynetwork:
    driver: bridge
```

**Host**: Container shares host network (no isolation, better performance).
```yaml
services:
  app:
    network_mode: host
```

**Custom Bridge**: Define subnets, IP ranges.
```yaml
networks:
  custom:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

**Overlay**: Multi-host networking (Docker Swarm, Kubernetes).

### Volumes (Named vs Bind Mounts)

**Named Volumes** (managed by Docker, persistent):
```yaml
volumes:
  postgres_data:
    driver: local

services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**Bind Mounts** (host directory, development):
```yaml
services:
  api:
    volumes:
      - ./api:/app  # Hot reload
      - /app/__pycache__  # Anonymous volume (exclude)
```

**tmpfs** (in-memory, ephemeral):
```yaml
services:
  app:
    tmpfs:
      - /tmp
      - /run
```

**Recommendation:**
- **Production**: Named volumes (persistent, backed up)
- **Development**: Bind mounts (hot reload)
- **Secrets/Temp**: tmpfs (no disk writes)

### Environment Variables and .env Files

**docker-compose.yml:**
```yaml
services:
  api:
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/myapp
      LOG_LEVEL: ${LOG_LEVEL:-info}  # Default: info
    env_file:
      - .env
      - .env.local  # Override .env
```

**.env:**
```bash
DB_PASSWORD=secretpassword
LOG_LEVEL=debug
BUILD_DATE=2024-01-01
```

**Variable Precedence** (highest to lowest):
1. Shell environment
2. `docker-compose.yml` `environment:` section
3. `env_file:`
4. Dockerfile `ENV`

### depends_on and Health Checks

**Basic Dependency (starts in order):**
```yaml
services:
  api:
    depends_on:
      - db
```

**Health Check Dependency (waits for healthy):**
```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy

  db:
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Conditions:**
- `service_started`: Default, just waits for container to start
- `service_healthy`: Waits for health check to pass
- `service_completed_successfully`: Waits for container to exit with 0

### Development vs Production Configs

**docker-compose.yml** (base config):
```yaml
version: '3.8'
services:
  api:
    build: ./api
    environment:
      LOG_LEVEL: info
```

**docker-compose.override.yml** (development overrides, auto-loaded):
```yaml
version: '3.8'
services:
  api:
    volumes:
      - ./api:/app  # Hot reload
    environment:
      LOG_LEVEL: debug  # Verbose logging
    ports:
      - "8000:8000"  # Expose port
```

**docker-compose.prod.yml** (production):
```yaml
version: '3.8'
services:
  api:
    image: myapp/api:1.0.0  # Use specific version
    restart: always
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

**Usage:**
```bash
# Development (auto-loads docker-compose.override.yml)
docker-compose up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Override Files

**Load order:**
1. `docker-compose.yml` (base)
2. `docker-compose.override.yml` (auto-loaded, development)
3. `-f` flag overrides (explicit)

**Example: Testing Config**
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up
```

## Security

### Non-Root User Containers

**Why?** Root in container = root on host if escaping. Always drop privileges:

```dockerfile
FROM python:3.11-slim

# Install dependencies as root
RUN apt-get update && apt-get install -y curl

# Create non-root user
RUN useradd -m -u 1000 appuser

# Create app directory and set ownership
WORKDIR /app
RUN chown appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

CMD ["python", "app.py"]
```

**Docker Compose:**
```yaml
services:
  api:
    user: "1000:1000"  # UID:GID
```

### Secret Management (Don't Bake Secrets)

**❌ NEVER:**
```dockerfile
# ❌ Secret in image
ENV DATABASE_PASSWORD=secretpassword

# ❌ Secret in build
COPY .env .
```

**✅ RECOMMENDED:**

**1. Environment variables (development):**
```yaml
services:
  api:
    environment:
      DATABASE_PASSWORD: ${DATABASE_PASSWORD}
```

**2. Docker secrets (production):**
```yaml
services:
  api:
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**3. External secret managers:**
- AWS Secrets Manager
- HashiCorp Vault
- Kubernetes Secrets

### Image Scanning (Trivy, Snyk)

**Trivy (free, fast):**
```bash
# Install
brew install aquasecurity/trivy/trivy

# Scan image
trivy image myapp/api:latest

# Fail on critical vulnerabilities
trivy image --severity CRITICAL,HIGH --exit-code 1 myapp/api:latest
```

**Snyk:**
```bash
# Install
npm install -g snyk

# Authenticate
snyk auth

# Scan image
snyk container test myapp/api:latest
```

**CI/CD Integration:**
```yaml
# .github/workflows/docker.yml
- name: Scan image
  run: |
    trivy image --severity CRITICAL,HIGH --exit-code 1 myapp/api:latest
```

### Minimal Attack Surface

**Reduce what's in the container:**
1. Use minimal base images (alpine, distroless)
2. Remove package managers in final stage
3. No SSH, no shell (distroless)
4. Only include runtime dependencies

**Distroless Example (no shell, no package manager):**
```dockerfile
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o main .

FROM gcr.io/distroless/static
COPY --from=builder /app/main /main
CMD ["/main"]
```

**Can't even exec into distroless containers:**
```bash
docker exec -it mycontainer sh  # ❌ No shell!
```

### Read-Only Filesystems

**Force immutability:**
```yaml
services:
  api:
    read_only: true
    tmpfs:
      - /tmp  # Allow temporary writes
      - /run
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
RUN useradd -m appuser
USER appuser
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]
```

**Why?** Even if attacker gains code execution, they can't modify binaries or write persistent backdoors.

### Capability Dropping

**Drop Linux capabilities:**
```yaml
services:
  api:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port <1024
```

**Common capabilities to keep:**
- `NET_BIND_SERVICE`: Bind to ports <1024
- `CHOWN`: Change file ownership
- `DAC_OVERRIDE`: Bypass file permissions

**Default Docker capabilities** (too permissive, drop all and add only what's needed):
- `CHOWN`, `DAC_OVERRIDE`, `FOWNER`, `FSETID`, `KILL`, `SETGID`, `SETUID`, `SETPCAP`, `NET_BIND_SERVICE`, `NET_RAW`, `SYS_CHROOT`, `MKNOD`, `AUDIT_WRITE`, `SETFCAP`

## Networking

### Bridge vs Host vs Overlay

**Bridge** (default): Isolated network, NAT to host.
```yaml
services:
  api:
    networks:
      - mynetwork

networks:
  mynetwork:
    driver: bridge
```

**Host**: No isolation, container uses host network directly.
```yaml
services:
  api:
    network_mode: host
```
**Use case**: High-performance, no port mapping overhead.
**Downside**: No isolation, port conflicts.

**Overlay**: Multi-host networking (Swarm, Kubernetes).
```yaml
networks:
  overlay:
    driver: overlay
```

### Service Discovery

**Within Docker Compose network, containers resolve by service name:**

```yaml
services:
  api:
    networks:
      - mynetwork

  db:
    networks:
      - mynetwork
```

**api container can connect to db:**
```python
# In api container
DATABASE_URL = "postgresql://postgres:password@db:5432/myapp"
# 'db' resolves to db container's IP
```

**DNS resolution provided by Docker's embedded DNS server (127.0.0.11).**

### Port Mapping Patterns

**Basic mapping:**
```yaml
ports:
  - "8000:8000"  # host:container
```

**Host IP binding:**
```yaml
ports:
  - "127.0.0.1:8000:8000"  # Only accessible from localhost
```

**Random host port:**
```yaml
ports:
  - "8000"  # Docker assigns random host port
```

**UDP:**
```yaml
ports:
  - "53:53/udp"
```

**Multiple ports:**
```yaml
ports:
  - "8000-8010:8000-8010"
```

### Container-to-Container Communication

**Same network (no port mapping needed):**
```yaml
services:
  api:
    networks:
      - backend

  db:
    networks:
      - backend
    # No ports: section needed for internal communication
```

**api can connect to db:5432 directly (port not exposed to host).**

**Cross-network communication:**
```yaml
services:
  api:
    networks:
      - frontend
      - backend

  web:
    networks:
      - frontend

  db:
    networks:
      - backend
```

**web can reach api, but NOT db.**

## Volume Management

### Named Volumes vs Bind Mounts

**Named Volumes** (Docker-managed, persistent):
```yaml
volumes:
  postgres_data:

services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**Location**: `/var/lib/docker/volumes/postgres_data/_data` (Linux)

**Bind Mounts** (host directory):
```yaml
services:
  api:
    volumes:
      - ./api:/app  # Relative path
      - /absolute/path:/app  # Absolute path
```

**Comparison:**

| Feature | Named Volume | Bind Mount |
|---------|--------------|------------|
| Location | Docker-managed | Host path |
| Persistence | Backed up with Docker | Host backup |
| Performance | Native Docker performance | May be slower (macOS, Windows) |
| Portability | Portable | Host-dependent |
| Use Case | Production data | Development (hot reload) |

### Data Persistence Strategies

**1. Named volumes (production):**
```yaml
volumes:
  postgres_data:
    driver: local

services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**2. Volume drivers (cloud storage):**
```yaml
volumes:
  data:
    driver: rexray/ebs
    driver_opts:
      size: 100
```

**3. External volumes (managed outside compose):**
```yaml
volumes:
  data:
    external: true
```

**4. Read-only volumes:**
```yaml
services:
  api:
    volumes:
      - ./config:/app/config:ro  # Read-only
```

### Backup and Restore Patterns

**Backup named volume:**
```bash
# Start a temporary container
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres_data.tar.gz /data
```

**Restore named volume:**
```bash
# Create volume if it doesn't exist
docker volume create postgres_data

# Restore data
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres_data.tar.gz -C /
```

**Database-specific backup (better):**
```bash
# PostgreSQL
docker exec myapp_db pg_dump -U postgres myapp > backup.sql

# Restore
docker exec -i myapp_db psql -U postgres myapp < backup.sql
```

### tmpfs for Sensitive Data

**In-memory storage (ephemeral, fast):**
```yaml
services:
  api:
    tmpfs:
      - /tmp
      - /run
      - /app/cache  # Ephemeral cache
```

**Or with options:**
```yaml
services:
  api:
    tmpfs:
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100000000  # 100MB
          mode: 1777
```

**Use case**: Store secrets temporarily, cache, temp files that shouldn't hit disk.

## Development Workflow

### Hot Reload with Volumes

**Python (FastAPI):**
```yaml
services:
  api:
    build: ./api
    volumes:
      - ./api:/app
      - /app/__pycache__  # Exclude cache
    command: uvicorn app.main:app --reload --host 0.0.0.0
```

**Node.js (Next.js):**
```yaml
services:
  web:
    build: ./web
    volumes:
      - ./web:/app
      - /app/node_modules
      - /app/.next
    command: npm run dev
```

**Why exclude `/app/node_modules`?** Prevents host's node_modules from overriding container's (platform-specific binaries).

### Debugging Containers

**1. Exec into running container:**
```bash
docker exec -it mycontainer bash
```

**2. Check logs:**
```bash
docker logs -f mycontainer
docker-compose logs -f api
```

**3. Inspect container:**
```bash
docker inspect mycontainer
docker-compose ps
```

**4. Attach debugger:**
```yaml
services:
  api:
    ports:
      - "5678:5678"  # Debugger port
    command: python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.main:app
```

**5. Override command:**
```bash
docker run -it --entrypoint bash myapp/api
docker-compose run --entrypoint bash api
```

### Log Management

**Docker Compose logging:**
```yaml
services:
  api:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

**Logging drivers:**
- `json-file`: Default, JSON logs to disk
- `syslog`: Send to syslog
- `journald`: Send to systemd journal
- `gelf`: Send to Graylog
- `fluentd`: Send to Fluentd
- `awslogs`: Send to CloudWatch

**Centralized logging (Fluentd):**
```yaml
services:
  api:
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: api.logs
```

### Local Development Setup

**Full-stack development compose:**
```yaml
version: '3.8'

services:
  api:
    build:
      context: ./api
      target: development  # Multi-stage development target
    volumes:
      - ./api:/app
      - /app/__pycache__
    environment:
      DATABASE_URL: postgresql://postgres:dev@db:5432/myapp
      LOG_LEVEL: debug
    command: uvicorn app.main:app --reload --host 0.0.0.0
    ports:
      - "8000:8000"
      - "5678:5678"  # Debugger
    depends_on:
      - db
      - redis

  web:
    build:
      context: ./web
      target: development
    volumes:
      - ./web:/app
      - /app/node_modules
      - /app/.next
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    command: npm run dev
    ports:
      - "3000:3000"
    depends_on:
      - api

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Start development:**
```bash
docker-compose up
```

**Rebuild after dependency changes:**
```bash
docker-compose up --build
```

**Clean rebuild:**
```bash
docker-compose down -v  # Remove volumes
docker-compose build --no-cache
docker-compose up
```

## Anti-Patterns

**NEVER do these:**

### 1. Running as Root
```dockerfile
# ❌ BAD
FROM python:3.11
COPY . /app
CMD ["python", "app.py"]  # Runs as root
```

**Fix**: Add `USER` instruction.

### 2. Large Images
```dockerfile
# ❌ BAD - 1.2GB
FROM python:3.11
RUN apt-get update && apt-get install -y build-essential
COPY . /app
RUN pip install -r requirements.txt
```

**Fix**: Use slim base, multi-stage build, clean up caches.

### 3. Secrets in Images
```dockerfile
# ❌ BAD
ENV DATABASE_PASSWORD=secretpassword
COPY .env /app/.env
```

**Fix**: Use environment variables or Docker secrets.

### 4. :latest Tag
```dockerfile
# ❌ BAD
FROM python:latest
```

**Fix**: Pin specific version (`python:3.11.6-slim`).

### 5. No .dockerignore
```
# ❌ BAD - Copies everything
COPY . /app
```

**Fix**: Create `.dockerignore` to exclude unnecessary files.

### 6. Inefficient Layer Caching
```dockerfile
# ❌ BAD - Application changes invalidate dependencies
COPY . /app
RUN pip install -r /app/requirements.txt
```

**Fix**: Copy `requirements.txt` first, install, then copy application code.

### 7. One Service Per Container Violated
```dockerfile
# ❌ BAD - Multiple processes in one container
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
```

**Fix**: Use Docker Compose to orchestrate multiple containers.

### 8. Ignoring Health Checks
```yaml
# ❌ BAD - No way to know if service is healthy
services:
  api:
    image: myapp/api
```

**Fix**: Add `healthcheck` to service and `HEALTHCHECK` to Dockerfile.

### 9. Bind Mounts in Production
```yaml
# ❌ BAD - Host-dependent paths in production
services:
  api:
    volumes:
      - ./api:/app
```

**Fix**: Use named volumes for production data persistence.

### 10. No Resource Limits
```yaml
# ❌ BAD - Container can consume all host resources
services:
  api:
    image: myapp/api
```

**Fix**: Set memory and CPU limits:
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Production-Grade Examples

### Python (FastAPI) Production Dockerfile

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Use exec form for proper signal handling
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Node.js (Next.js) Production Dockerfile

```dockerfile
FROM node:20-alpine AS deps

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --only=production

FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### Go Production Dockerfile

```dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install git (for go mod download)
RUN apk add --no-cache git

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build static binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-extldflags "-static"' -o main .

FROM gcr.io/distroless/static-debian11

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/main .

# Distroless runs as non-root by default
USER nonroot:nonroot

EXPOSE 8080

CMD ["./main"]
```

### Production Docker Compose

```yaml
version: '3.8'

services:
  api:
    image: myapp/api:${VERSION}
    container_name: myapp_api_prod
    restart: always
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/myapp
      REDIS_URL: redis://redis:6379/0
      LOG_LEVEL: info
    env_file:
      - .env.prod
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - backend
      - frontend
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s

  web:
    image: myapp/web:${VERSION}
    container_name: myapp_web_prod
    restart: always
    environment:
      NEXT_PUBLIC_API_URL: https://api.myapp.com
    depends_on:
      - api
    networks:
      - frontend
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: myapp_db_prod
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp_redis_prod
    restart: always
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: myapp_nginx_prod
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
      - api
    networks:
      - frontend
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

---

## Quick Reference

**Build and Tag:**
```bash
docker build -t myapp/api:1.0.0 .
docker build -t myapp/api:latest --build-arg VERSION=1.0.0 .
```

**Multi-stage Target:**
```bash
docker build --target development -t myapp/api:dev .
```

**Compose:**
```bash
docker-compose up -d  # Start in background
docker-compose logs -f api  # Follow logs
docker-compose exec api bash  # Exec into container
docker-compose down -v  # Stop and remove volumes
```

**Cleanup:**
```bash
docker system prune -a  # Remove all unused images
docker volume prune  # Remove all unused volumes
docker builder prune  # Clear build cache
```

**Scan:**
```bash
trivy image myapp/api:latest
docker scan myapp/api:latest
```

**Inspect:**
```bash
docker inspect myapp/api:latest
docker history myapp/api:latest
docker images --tree  # See image layers
```

---

Apply these patterns to build secure, efficient, production-grade containerized applications. Prioritize security (non-root, scanning), optimization (multi-stage, caching), and operational excellence (health checks, logging, resource limits).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

