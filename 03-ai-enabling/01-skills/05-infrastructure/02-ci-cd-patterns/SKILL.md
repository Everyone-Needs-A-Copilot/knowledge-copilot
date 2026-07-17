---
last_updated: 2026-02-25
status: active
name: ci-cd-patterns
description: CI/CD pipelines - GitHub Actions, deployment strategies, artifact management. Use for automation.
triggers:
  files: ["**/.github/workflows/**", "**/.gitlab-ci.yml", "**/Jenkinsfile", "**/azure-pipelines.yml"]
  keywords: ["CI/CD", "pipeline", "GitHub Actions", "deployment", "workflow", "artifact", "release", "continuous integration"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides creation of production-grade CI/CD pipelines using modern automation platforms. Apply these patterns when building workflows, orchestrating deployments, or optimizing release processes.

The user provides automation requirements: GitHub Actions workflows, deployment pipelines, artifact management, release strategies, or pipeline optimization.

## Core Principles

CI/CD excellence is built on five pillars:

1. **Fast Feedback**: Pipelines complete in <10 minutes. Developers get results before context-switching.
2. **Reliable**: Deterministic, reproducible builds. No flaky tests, no "works on my machine".
3. **Secure**: Secrets managed properly, least privilege access, no credential leaks.
4. **Scalable**: Matrix builds, parallel jobs, efficient caching. Handles growth without slowdown.
5. **Observable**: Clear logs, status checks, notifications. Easy to debug failures.


## Define Done

- [ ] Infrastructure configuration is reproducible (code, not clicks)
- [ ] Failure scenarios identified with recovery procedures
- [ ] Resource requirements estimated and within budget
- [ ] Security boundaries and access controls defined

## GitHub Actions

### Workflow Structure

**Basic Anatomy:**
```yaml
name: CI                    # Workflow name (appears in UI)

on:                         # Triggers
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]
  workflow_dispatch:        # Manual trigger

env:                        # Workflow-level environment variables
  NODE_VERSION: '20.x'
  PYTHON_VERSION: '3.11'

jobs:
  test:                     # Job ID
    runs-on: ubuntu-latest  # Runner type

    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

### Workflow Triggers

**Push/Pull Request (most common):**
```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'       # Wildcard
    tags:
      - 'v*'                # All version tags
    paths:
      - 'src/**'            # Only if these files change
      - '!docs/**'          # Exclude docs

  pull_request:
    branches: [main]
    types:
      - opened
      - synchronize        # New commits pushed
      - reopened
```

**Schedule (cron):**
```yaml
on:
  schedule:
    - cron: '0 2 * * *'    # Daily at 2am UTC
    - cron: '0 */6 * * *'  # Every 6 hours
```

**Workflow Dispatch (manual):**
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - staging
          - production
      version:
        description: 'Version to deploy'
        required: false
        type: string
```

**Repository Dispatch (API trigger):**
```yaml
on:
  repository_dispatch:
    types: [deploy-event]
```

**Workflow Call (reusable):**
```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy-key:
        required: true
```

**Multiple Triggers:**
```yaml
on: [push, pull_request, workflow_dispatch]
```

### Job Dependencies

**Sequential Jobs:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  test:
    needs: build           # Waits for build to complete
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: [build, test]   # Waits for both
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

**Conditional Jobs:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && success()
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

**Continue on Error:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  lint:
    runs-on: ubuntu-latest
    continue-on-error: true  # Don't block pipeline
    steps:
      - run: npm run lint

  deploy:
    needs: [test, lint]
    if: always()             # Run even if lint fails
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

### Matrix Builds

**Basic Matrix (test across versions):**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20, 22]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

**Multi-Dimensional Matrix:**
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [18, 20]
        include:
          - os: ubuntu-latest
            node-version: 22
            experimental: true
        exclude:
          - os: windows-latest
            node-version: 18

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

**Fail Fast (default: true):**
```yaml
jobs:
  test:
    strategy:
      fail-fast: false      # Continue running other matrix jobs on failure
      matrix:
        node-version: [16, 18, 20]
```

**Max Parallel:**
```yaml
jobs:
  test:
    strategy:
      max-parallel: 2       # Run max 2 matrix jobs concurrently
      matrix:
        node-version: [16, 18, 20, 22]
```

### Secrets Management

**Repository Secrets (Settings > Secrets):**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to AWS
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          aws s3 sync ./dist s3://my-bucket
```

**Environment Secrets:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production    # Use 'production' environment secrets
    steps:
      - name: Deploy
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: ./deploy.sh
```

**Organization Secrets (shared across repos):**
```yaml
# Automatically available if org admin set them up
env:
  NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Secrets in Outputs (NEVER DO THIS):**
```yaml
# ❌ BAD - Exposes secret in logs
- name: Get secret
  run: echo "SECRET=${{ secrets.MY_SECRET }}"

# ✅ GOOD - Use secret directly
- name: Use secret
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}
  run: |
    # Secret not echoed to logs
    ./deploy.sh
```

**Mask Secrets:**
```yaml
- name: Add secret to output
  run: |
    echo "::add-mask::${{ secrets.MY_SECRET }}"
    echo "Secret: ${{ secrets.MY_SECRET }}"  # Now masked in logs
```

### Caching Strategies

**Node.js Dependencies:**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'           # Automatically cache node_modules
    cache-dependency-path: package-lock.json

- run: npm ci
```

**Python Dependencies:**
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
    cache-dependency-path: requirements.txt

- run: pip install -r requirements.txt
```

**Custom Cache:**
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      ~/.npm
      ./build
    key: ${{ runner.os }}-deps-${{ hashFiles('**/requirements.txt', '**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-deps-
      ${{ runner.os }}-
```

**Docker Layer Cache:**
```yaml
- uses: docker/setup-buildx-action@v3

- uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: myapp:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Cache Hit Detection:**
```yaml
- uses: actions/cache@v4
  id: cache
  with:
    path: ./build
    key: ${{ runner.os }}-build-${{ hashFiles('src/**') }}

- name: Build
  if: steps.cache.outputs.cache-hit != 'true'
  run: npm run build
```

**Cache Management:**
```yaml
# Caches are automatically deleted after 7 days of no access
# Manual deletion via GitHub UI: Settings > Actions > Caches

# Clear cache by changing key:
key: v2-${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
```

### Artifact Management

**Upload Artifacts:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

      - uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: |
            dist/
            build/
          retention-days: 30
          if-no-files-found: error
```

**Download Artifacts:**
```yaml
jobs:
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-artifacts
          path: ./dist

      - run: ls -la ./dist
```

**Multiple Artifacts:**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: logs-${{ matrix.os }}-${{ matrix.node-version }}
    path: logs/*.log
```

**Artifact Retention:**
```yaml
# Default: 90 days (repo setting)
# Override per artifact:
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results/
    retention-days: 7      # Delete after 7 days
```

**Download from Different Workflow:**
```yaml
# Not directly supported in actions/download-artifact
# Use GitHub API or third-party actions
```

### Environment Variables

**Workflow-Level:**
```yaml
env:
  NODE_VERSION: '20'
  DEPLOY_ENV: production

jobs:
  build:
    steps:
      - run: echo $NODE_VERSION
```

**Job-Level:**
```yaml
jobs:
  build:
    env:
      BUILD_TYPE: release
    steps:
      - run: echo $BUILD_TYPE
```

**Step-Level:**
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    REGION: us-east-1
  run: ./deploy.sh
```

**Default Environment Variables (GitHub):**
```yaml
- run: |
    echo "Repository: ${{ github.repository }}"
    echo "Branch: ${{ github.ref_name }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
    echo "Event: ${{ github.event_name }}"
    echo "Run ID: ${{ github.run_id }}"
    echo "Runner OS: ${{ runner.os }}"
```

**Set Environment Variable for Subsequent Steps:**
```yaml
- name: Set version
  run: echo "VERSION=$(cat version.txt)" >> $GITHUB_ENV

- name: Use version
  run: echo "Deploying version $VERSION"
```

**Set Output (for other jobs):**
```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.set-version.outputs.version }}
    steps:
      - id: set-version
        run: echo "version=1.2.3" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.version }}"
```

### Reusable Workflows

**Caller Workflow:**
```yaml
# .github/workflows/deploy-prod.yml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: production
      version: ${{ github.sha }}
    secrets:
      deploy-key: ${{ secrets.PROD_DEPLOY_KEY }}
```

**Reusable Workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: true
        type: string
    secrets:
      deploy-key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ inputs.version }}

      - name: Deploy
        env:
          DEPLOY_KEY: ${{ secrets.deploy-key }}
        run: |
          echo "Deploying to ${{ inputs.environment }}"
          ./deploy.sh
```

**Reusable Workflow with Matrix:**
```yaml
# .github/workflows/test.yml
on:
  workflow_call:
    inputs:
      node-versions:
        required: true
        type: string  # JSON array: '["16", "18", "20"]'

jobs:
  test:
    strategy:
      matrix:
        node-version: ${{ fromJSON(inputs.node-versions) }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Composite Actions

**Define Composite Action:**
```yaml
# .github/actions/setup-node-pnpm/action.yml
name: Setup Node with pnpm
description: Setup Node.js and install dependencies with pnpm

inputs:
  node-version:
    description: 'Node.js version'
    required: true
    default: '20'

runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - name: Install pnpm
      shell: bash
      run: npm install -g pnpm

    - name: Install dependencies
      shell: bash
      run: pnpm install --frozen-lockfile
```

**Use Composite Action:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-node-pnpm
        with:
          node-version: '20'
      - run: pnpm build
```

**Composite Action with Outputs:**
```yaml
# action.yml
outputs:
  version:
    description: 'Package version'
    value: ${{ steps.get-version.outputs.version }}

runs:
  using: composite
  steps:
    - id: get-version
      shell: bash
      run: echo "version=$(node -p "require('./package.json').version")" >> $GITHUB_OUTPUT
```

### Conditional Execution

**If Conditions:**
```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

- name: Deploy to staging
  if: startsWith(github.ref, 'refs/heads/staging')
  run: ./deploy-staging.sh

- name: Notify on failure
  if: failure()
  run: ./notify-failure.sh

- name: Always run cleanup
  if: always()
  run: ./cleanup.sh

- name: Run on success
  if: success()
  run: ./notify-success.sh
```

**Complex Conditions:**
```yaml
- name: Deploy
  if: |
    github.event_name == 'push' &&
    github.ref == 'refs/heads/main' &&
    !contains(github.event.head_commit.message, '[skip ci]')
  run: ./deploy.sh
```

**Job-Level Conditions:**
```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

**Status Check Functions:**
- `success()`: All previous steps succeeded
- `failure()`: Any previous step failed
- `cancelled()`: Workflow was cancelled
- `always()`: Always run (even if cancelled)

### Self-Hosted Runners

**Register Self-Hosted Runner:**
```bash
# On your server
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
./config.sh --url https://github.com/myorg/myrepo --token YOUR_TOKEN
./run.sh
```

**Use Self-Hosted Runner:**
```yaml
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - run: npm build
```

**Runner Labels:**
```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64, gpu]
    steps:
      - run: nvidia-smi
```

**Runner Groups (Enterprise):**
```yaml
jobs:
  build:
    runs-on: [self-hosted, production-runners]
```

**Considerations:**
- **Security**: Self-hosted runners in public repos are dangerous (untrusted code)
- **Maintenance**: You manage OS updates, security patches, dependencies
- **Isolation**: Use ephemeral runners (Docker) for better isolation
- **Cost**: No minute limits, but hardware/maintenance costs

## Deployment Strategies

### Blue-Green Deployment

**Zero-downtime deployment with instant rollback:**

```yaml
name: Blue-Green Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to green environment
        run: |
          # Deploy to inactive (green) environment
          ./deploy.sh green

      - name: Run smoke tests
        run: |
          # Test green environment
          ./smoke-tests.sh https://green.myapp.com

      - name: Switch traffic to green
        run: |
          # Update load balancer to point to green
          ./switch-traffic.sh green

      - name: Monitor new deployment
        run: |
          # Watch metrics for 5 minutes
          ./monitor.sh green 300

      - name: Rollback if metrics fail
        if: failure()
        run: |
          # Switch back to blue (old version)
          ./switch-traffic.sh blue
```

**Infrastructure:**
- 2 identical environments (blue = live, green = staging)
- Load balancer switches between them
- **Pros**: Instant rollback, zero downtime
- **Cons**: 2x infrastructure cost, database migrations tricky

### Canary Deployment

**Gradual rollout to subset of users:**

```yaml
name: Canary Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-canary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy canary (10% traffic)
        run: |
          ./deploy.sh canary
          ./set-traffic-split.sh stable=90 canary=10

      - name: Monitor canary metrics
        run: |
          # Watch error rates, latency for 30 minutes
          ./monitor-canary.sh 1800

      - name: Increase canary to 50%
        if: success()
        run: ./set-traffic-split.sh stable=50 canary=50

      - name: Monitor at 50%
        run: ./monitor-canary.sh 1800

      - name: Promote canary to stable
        if: success()
        run: |
          ./set-traffic-split.sh stable=0 canary=100
          ./promote-canary.sh

      - name: Rollback canary
        if: failure()
        run: ./set-traffic-split.sh stable=100 canary=0
```

**Traffic Split (Kubernetes):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9  # 90% traffic
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1  # 10% traffic
```

**Pros**: Low risk, gradual rollout
**Cons**: Complex routing, requires monitoring infrastructure

### Rolling Deployment

**Update instances one by one:**

```yaml
name: Rolling Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 1  # Deploy one at a time
      matrix:
        instance: [1, 2, 3, 4, 5]
    steps:
      - uses: actions/checkout@v4

      - name: Remove instance from load balancer
        run: ./lb-deregister.sh instance-${{ matrix.instance }}

      - name: Deploy new version
        run: ./deploy.sh instance-${{ matrix.instance }}

      - name: Health check
        run: ./health-check.sh instance-${{ matrix.instance }}

      - name: Add instance back to load balancer
        run: ./lb-register.sh instance-${{ matrix.instance }}

      - name: Wait before next instance
        run: sleep 60
```

**Kubernetes Rolling Update:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max 1 extra pod during update
      maxUnavailable: 1  # Max 1 pod unavailable during update
```

**Pros**: Simple, no extra infrastructure
**Cons**: Slower, mixed versions during rollout

### Feature Flags

**Deploy code, control features separately:**

```yaml
name: Deploy with Feature Flags

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy new code (features disabled)
        run: ./deploy.sh

      - name: Enable feature for 10% users
        run: |
          curl -X POST https://api.launchdarkly.com/api/v2/flags/default/new-checkout/environments/production \
            -H "Authorization: ${{ secrets.LAUNCHDARKLY_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"rollout": {"variations": [{"variation": 0, "weight": 90000}, {"variation": 1, "weight": 10000}]}}'

      - name: Monitor metrics
        run: ./monitor-feature.sh new-checkout 3600

      - name: Increase to 100% if healthy
        if: success()
        run: |
          curl -X POST https://api.launchdarkly.com/api/v2/flags/default/new-checkout/environments/production \
            -H "Authorization: ${{ secrets.LAUNCHDARKLY_TOKEN }}" \
            -d '{"on": true}'
```

**Application Code:**
```python
from launchdarkly import LDClient

client = LDClient(os.environ['LAUNCHDARKLY_SDK_KEY'])

if client.variation('new-checkout', user, False):
    # New checkout flow
    checkout_v2()
else:
    # Old checkout flow
    checkout_v1()
```

**Pros**: Deploy anytime, control rollout separately, instant rollback
**Cons**: Code complexity, technical debt from old code paths

### Deployment Approval

**Require manual approval for production:**

```yaml
name: Deploy with Approval

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh production
```

**Environment Protection Rules (Settings > Environments > production):**
- Required reviewers (1-6 people must approve)
- Wait timer (e.g., 5 minutes before deployment)
- Deployment branches (only main can deploy to production)

**Approval Flow:**
1. Pipeline pauses at `environment: production`
2. GitHub notifies required reviewers
3. Reviewer checks staging, clicks "Approve"
4. Pipeline continues to production deployment

## Environment Protection Rules

**Configure in GitHub UI: Settings > Environments**

### Required Reviewers

```yaml
# Workflow file
jobs:
  deploy:
    environment: production  # Must be approved by configured reviewers
    steps:
      - run: ./deploy.sh
```

**GitHub UI Settings:**
- Add up to 6 required reviewers (users or teams)
- Any reviewer can approve (not all required)
- Reviewer cannot approve their own workflow run

### Wait Timer

**Delay deployment by N minutes (safety buffer):**

```yaml
environment:
  name: production  # Wait timer configured in GitHub UI
```

**Use case**: Allow time to cancel if deployment triggered accidentally.

### Deployment Branches

**Restrict which branches can deploy to environment:**

```yaml
# Only main branch can deploy to production
environment: production
```

**GitHub UI Settings:**
- Selected branches: `main`, `release/*`
- All branches (not recommended for production)

### Environment Secrets

**Environment-specific secrets:**

```yaml
jobs:
  deploy:
    environment: production
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}  # Uses 'production' environment secret
        run: ./deploy.sh
```

**Secrets hierarchy:**
1. Environment secrets (highest priority)
2. Repository secrets
3. Organization secrets

## Pipeline Optimization

### Parallel Jobs

**Run independent jobs concurrently:**

```yaml
jobs:
  test-unit:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:unit

  test-integration:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:integration

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  # All 3 jobs run in parallel
```

**Sequential when needed:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  test:
    needs: build  # Waits for build
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

### Job Splitting

**Split large test suites:**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]  # Split tests into 4 shards
    steps:
      - uses: actions/checkout@v4
      - run: npm test -- --shard=${{ matrix.shard }}/4
```

**Playwright Example:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]
    steps:
      - run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
```

### Dependency Caching

**Cache strategy:**

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

**Cache hit reduces `npm ci` from 60s to 5s.**

### Conditional Steps

**Skip unnecessary work:**

```yaml
- name: Build docs
  if: contains(github.event.head_commit.message, '[docs]')
  run: npm run docs

- name: Run tests
  if: |
    !contains(github.event.head_commit.message, '[skip tests]') &&
    !startsWith(github.ref, 'refs/heads/docs/')
  run: npm test
```

### Path Filtering

**Only run pipeline if relevant files change:**

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
      - 'package-lock.json'
  pull_request:
    paths:
      - 'src/**'
```

**Separate workflows for different paths:**

```yaml
# .github/workflows/api.yml
on:
  push:
    paths: ['api/**']

# .github/workflows/web.yml
on:
  push:
    paths: ['web/**']
```

### Fast Failure

**Fail fast on critical errors:**

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint  # Fail fast if linting fails

  test:
    needs: lint  # Don't run tests if lint fails
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

### Concurrency Control

**Cancel in-progress runs on new push:**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Example: New commit pushed to PR**
- Old workflow run cancelled
- New workflow run starts
- Saves minutes, faster feedback

**Per-environment concurrency:**
```yaml
jobs:
  deploy:
    environment: production
    concurrency:
      group: production-deploy
      cancel-in-progress: false  # Don't cancel production deployments
```

## Advanced Patterns

### Monorepo CI

**Detect changes and run relevant jobs:**

```yaml
name: Monorepo CI

on: [push, pull_request]

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
      shared: ${{ steps.filter.outputs.shared }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            api:
              - 'packages/api/**'
            web:
              - 'packages/web/**'
            shared:
              - 'packages/shared/**'

  test-api:
    needs: changes
    if: needs.changes.outputs.api == 'true' || needs.changes.outputs.shared == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test --workspace=api

  test-web:
    needs: changes
    if: needs.changes.outputs.web == 'true' || needs.changes.outputs.shared == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test --workspace=web
```

### Dynamic Matrix

**Generate matrix from script:**

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: set-matrix
        run: |
          # Generate matrix based on changed files
          MATRIX=$(node scripts/generate-matrix.js)
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  test:
    needs: setup
    strategy:
      matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}
    runs-on: ubuntu-latest
    steps:
      - run: npm test -- ${{ matrix.package }}
```

**scripts/generate-matrix.js:**
```javascript
const packages = require('./packages.json');
const matrix = { package: packages.map(p => p.name) };
console.log(JSON.stringify(matrix));
```

### Scheduled Cleanup

**Cleanup stale resources:**

```yaml
name: Cleanup

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday 2am

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Delete old artifacts
        run: |
          # Delete artifacts older than 30 days
          gh api repos/${{ github.repository }}/actions/artifacts \
            --jq '.artifacts[] | select(.created_at < (now - 2592000)) | .id' \
            | xargs -I {} gh api -X DELETE repos/${{ github.repository }}/actions/artifacts/{}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Clean up Docker images
        run: |
          # Delete untagged images
          docker image prune -a -f --filter "until=720h"
```

### Docker Build and Push

**Multi-platform Docker images:**

```yaml
name: Docker

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-qemu-action@v3

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Release Automation

**Semantic versioning with automatic releases:**

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for changelog

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install semantic-release
        run: npm install -g semantic-release @semantic-release/git @semantic-release/changelog

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

**.releaserc.json:**
```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    ["@semantic-release/git", {
      "assets": ["package.json", "CHANGELOG.md"],
      "message": "chore(release): ${nextRelease.version} [skip ci]"
    }]
  ]
}
```

**Commit Convention:**
```
feat: add new feature       → 1.1.0 (minor)
fix: fix bug                → 1.0.1 (patch)
feat!: breaking change      → 2.0.0 (major)
docs: update docs           → no release
```

## Full-Stack CI/CD Example

**Complete workflow for FastAPI + Next.js application:**

```yaml
name: CI/CD

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '20'

jobs:
  # Backend Tests
  test-api:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd api
          pip install -r requirements.txt

      - name: Run linting
        run: |
          cd api
          ruff check .
          black --check .

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
        run: |
          cd api
          pytest --cov=app --cov-report=xml

      - uses: codecov/codecov-action@v4
        with:
          file: ./api/coverage.xml
          flags: api

  # Frontend Tests
  test-web:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: web/package-lock.json

      - name: Install dependencies
        run: |
          cd web
          npm ci

      - name: Run linting
        run: |
          cd web
          npm run lint

      - name: Run tests
        run: |
          cd web
          npm test -- --coverage

      - uses: codecov/codecov-action@v4
        with:
          file: ./web/coverage/coverage-final.json
          flags: web

  # E2E Tests
  test-e2e:
    needs: [test-api, test-web]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Start services
        run: docker-compose up -d

      - name: Wait for services
        run: |
          npx wait-on http://localhost:8000/health
          npx wait-on http://localhost:3000

      - name: Run E2E tests
        run: npx playwright test

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/

  # Build Images
  build:
    needs: [test-api, test-web, test-e2e]
    if: github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push API
        uses: docker/build-push-action@v5
        with:
          context: ./api
          push: true
          tags: ghcr.io/${{ github.repository }}/api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push Web
        uses: docker/build-push-action@v5
        with:
          context: ./web
          push: true
          tags: ghcr.io/${{ github.repository }}/web:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Deploy to Staging
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/dev'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.myapp.com

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG_STAGING }}
        run: |
          kubectl set image deployment/api api=ghcr.io/${{ github.repository }}/api:${{ github.sha }}
          kubectl set image deployment/web web=ghcr.io/${{ github.repository }}/web:${{ github.sha }}
          kubectl rollout status deployment/api
          kubectl rollout status deployment/web

  # Deploy to Production
  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG_PRODUCTION }}
        run: |
          kubectl set image deployment/api api=ghcr.io/${{ github.repository }}/api:${{ github.sha }}
          kubectl set image deployment/web web=ghcr.io/${{ github.repository }}/web:${{ github.sha }}
          kubectl rollout status deployment/api
          kubectl rollout status deployment/web

      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh https://myapp.com

      - name: Notify deployment
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deployment to production ${{ job.status }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Deployment to production *${{ job.status }}*\nCommit: ${{ github.sha }}\nActor: ${{ github.actor }}"
                  }
                }
              ]
            }
```

## Anti-Patterns

**NEVER do these:**

### 1. Secrets in Logs

```yaml
# ❌ BAD - Secret exposed in logs
- run: echo "API_KEY=${{ secrets.API_KEY }}"

# ✅ GOOD - Use secret in environment
- env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

### 2. No Caching

```yaml
# ❌ BAD - Reinstalls dependencies every run (60s)
- run: npm install

# ✅ GOOD - Cache dependencies (5s on cache hit)
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
- run: npm ci
```

### 3. Sequential Jobs That Could Be Parallel

```yaml
# ❌ BAD - 10 minutes sequential
jobs:
  test-unit:
    needs: lint
  test-integration:
    needs: test-unit

# ✅ GOOD - 5 minutes parallel
jobs:
  lint:
  test-unit:
  test-integration:
```

### 4. No Health Checks on Deploy

```yaml
# ❌ BAD - Deploy and hope it works
- run: kubectl apply -f deployment.yml

# ✅ GOOD - Verify deployment succeeded
- run: |
    kubectl apply -f deployment.yml
    kubectl rollout status deployment/myapp
    ./smoke-tests.sh
```

### 5. Hardcoded Versions

```yaml
# ❌ BAD - Outdated action versions
- uses: actions/checkout@v2
- uses: actions/setup-node@v2

# ✅ GOOD - Latest versions
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
```

### 6. No Timeout

```yaml
# ❌ BAD - Hangs forever
- run: ./flaky-script.sh

# ✅ GOOD - Timeout after 10 minutes
- run: ./flaky-script.sh
  timeout-minutes: 10
```

### 7. Deployment Without Approval

```yaml
# ❌ BAD - Auto-deploy to production
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

# ✅ GOOD - Require manual approval
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    environment: production  # Requires approval in settings
    runs-on: ubuntu-latest
```

### 8. No Matrix for Multi-Version Support

```yaml
# ❌ BAD - Only test on Node 20
- uses: actions/setup-node@v4
  with:
    node-version: '20'

# ✅ GOOD - Test on all supported versions
strategy:
  matrix:
    node-version: [18, 20, 22]
```

### 9. No Artifact Retention

```yaml
# ❌ BAD - Artifacts stored for 90 days (default)
- uses: actions/upload-artifact@v4
  with:
    name: logs

# ✅ GOOD - Clean up after 7 days
- uses: actions/upload-artifact@v4
  with:
    name: logs
    retention-days: 7
```

### 10. No Concurrency Control

```yaml
# ❌ BAD - Multiple deploys run simultaneously
on: push

# ✅ GOOD - Cancel old runs on new push
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

## Quick Reference

**Common Actions:**
```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
- uses: actions/setup-python@v5
- uses: actions/cache@v4
- uses: actions/upload-artifact@v4
- uses: actions/download-artifact@v4
- uses: docker/build-push-action@v5
```

**Useful Commands:**
```bash
# Test workflow locally (act)
brew install act
act push

# Validate workflow syntax
actionlint .github/workflows/*.yml

# Trigger workflow manually
gh workflow run deploy.yml

# List workflow runs
gh run list

# Watch workflow run
gh run watch

# Cancel workflow run
gh run cancel 12345
```

**Context Variables:**
```yaml
${{ github.repository }}      # owner/repo
${{ github.ref }}             # refs/heads/main
${{ github.ref_name }}        # main
${{ github.sha }}             # commit SHA
${{ github.actor }}           # user who triggered
${{ github.event_name }}      # push, pull_request, etc.
${{ runner.os }}              # Linux, Windows, macOS
${{ secrets.MY_SECRET }}      # Repository secret
```

---

Apply these patterns to build fast, reliable, secure CI/CD pipelines. Prioritize fast feedback (caching, parallelism), security (secrets management, approval gates), and operational excellence (monitoring, rollback strategies).


## Quality Tests

### Reproducibility Test
- Infrastructure can be recreated from configuration alone
- **PASS:** All steps are scripted or documented as code
- **FAIL:** Setup requires manual console clicks or undocumented steps

### Rollback Test
- Changes can be reversed without data loss
- **PASS:** Rollback procedure documented and tested
- **FAIL:** No rollback path defined for infrastructure changes

