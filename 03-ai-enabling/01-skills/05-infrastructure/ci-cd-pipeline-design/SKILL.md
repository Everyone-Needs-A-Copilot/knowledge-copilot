---
last_updated: 2026-02-25
status: active
name: ci-cd-pipeline-design
description: GitHub Actions, GitLab CI, and pipeline patterns. Use when automating build, test, and deployment workflows.
triggers:
  files: ["**/.github/workflows/**", "**/.gitlab-ci.yml", "**/Jenkinsfile", "**/azure-pipelines.yml", "**/buildspec.yml"]
  keywords: ["ci/cd", "pipeline", "github actions", "gitlab ci", "jenkins", "automation", "continuous integration", "continuous deployment"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides CI/CD pipeline design for reliable, automated software delivery. Apply these patterns when building pipelines for testing, building, and deploying applications.

The user provides pipeline requirements: language/framework, deployment targets, testing needs, or security requirements.

## Core Principles

Effective CI/CD is built on five pillars:

1. **Fast Feedback**: Fail fast, surface issues early.
2. **Reproducibility**: Same inputs produce same outputs.
3. **Security**: Secrets management, vulnerability scanning.
4. **Visibility**: Clear status, logs, and notifications.
5. **Automation**: Minimize manual intervention.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## Pipeline Stages

| Stage | Purpose | Typical Time |
|-------|---------|--------------|
| Checkout | Get source code | <30s |
| Install | Dependencies | 1-5 min |
| Lint | Code quality | <1 min |
| Test | Unit/integration | 2-10 min |
| Build | Compile/bundle | 1-5 min |
| Security scan | Vulnerabilities | 1-3 min |
| Deploy | Ship to environment | 2-10 min |

## GitHub Actions

### Basic Workflow

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy to production
        run: |
          # Deployment commands here
          echo "Deploying ${{ github.sha }}"
```

### Matrix Builds

Test across multiple versions/platforms.

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: macos-latest
            node: 18
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci && npm test
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image_tag:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy
        run: |
          echo "Deploying ${{ inputs.image_tag }} to ${{ inputs.environment }}"
```

```yaml
# Calling the reusable workflow
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      image_tag: ${{ github.sha }}
    secrets:
      DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
```

## GitLab CI

```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

.node-cache: &node-cache
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

test:
  stage: test
  image: node:20
  <<: *node-cache
  script:
    - npm ci
    - npm run lint
    - npm test -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - develop

deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - echo "Deploying to staging"
  only:
    - develop

deploy-production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  script:
    - echo "Deploying to production"
  when: manual
  only:
    - main
```

## Security Scanning

### Dependency Scanning

```yaml
# GitHub Actions - npm audit
- name: Security audit
  run: npm audit --audit-level=high

# Snyk
- name: Snyk security scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### Container Scanning

```yaml
- name: Trivy vulnerability scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: '${{ env.IMAGE_NAME }}:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload Trivy scan results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```

### SAST (Static Analysis)

```yaml
- name: CodeQL Analysis
  uses: github/codeql-action/analyze@v3
  with:
    languages: javascript
```

## Caching Strategies

### Node.js

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

### Python

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
```

### Docker Layers

```yaml
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Environment Management

### GitHub Environments

```yaml
deploy:
  runs-on: ubuntu-latest
  environment:
    name: production
    url: https://example.com
  steps:
    - name: Deploy
      env:
        API_KEY: ${{ secrets.API_KEY }}  # Environment-specific secret
      run: deploy.sh
```

### Deployment Protection

| Rule | Purpose |
|------|---------|
| Required reviewers | Manual approval |
| Wait timer | Delay deployment |
| Deployment branches | Restrict sources |

## Notifications

### Slack

```yaml
- name: Slack notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    fields: repo,message,commit,author,action,eventName,ref,workflow
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

### PR Comments

```yaml
- name: Comment on PR
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '## Deployment Preview\n\nURL: https://preview-${{ github.event.pull_request.number }}.example.com'
      })
```

## Best Practices

### Pipeline Performance

| Optimization | Impact |
|--------------|--------|
| Parallel jobs | Reduce total time |
| Aggressive caching | Faster installs |
| Skip unchanged | Monorepo efficiency |
| Self-hosted runners | Faster for large builds |

### Secret Management

```yaml
# Use environment secrets, not repository secrets
# Rotate secrets regularly
# Never echo secrets

- name: Safe secret usage
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    # Never: echo $API_KEY
    # Mask in logs automatically
    ./deploy.sh
```

### Artifact Management

```yaml
# Upload build artifacts
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/
    retention-days: 5

# Download in another job
- uses: actions/download-artifact@v4
  with:
    name: build
```

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Secrets in code | Use secret management |
| No caching | Cache dependencies |
| Sequential when parallel possible | Use matrix/parallel jobs |
| Deploying untested code | Require passing tests |
| No status notifications | Alert on failure |
| Long-running pipelines | Optimize, parallelize |

## Pipeline Template

```yaml
# Complete production-ready template
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high

  build:
    needs: [lint, test, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: app:${{ github.sha }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Deploying"
```

---

Apply these patterns for reliable, fast CI/CD pipelines. Start with test and build stages, add security scanning, and implement proper caching and parallelization for optimal performance.


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

