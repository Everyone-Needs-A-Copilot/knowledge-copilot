---
last_updated: 2026-02-25
status: active
name: digital-material-audit
description: Audit patterns for evaluating digital material costs like performance, bundle size, and memory. Use when assessing resource usage and optimizing loading times.
category: industrial-design-digital
keywords:
  - performance
  - resources
  - latency
  - bundle-size
  - memory
triggers:
  keywords:
    - performance budget
    - bundle size
    - loading time
    - resource usage
  filePatterns:
    - "*.tsx"
    - "*.ts"
    - "*.js"
    - "package.json"
allowed-tools: Read, Write, Edit
---

# Digital Material Audit

Evaluate performance budgets, latency, and system resources as honest materials.

## Philosophy

Digital materials are milliseconds, kilobytes, and CPU cycles. Like physical materials, they must be used honestly. A 500ms delay cannot pretend to be instant. A 2MB bundle cannot pretend to be lightweight. The digital equivalent of "this aluminum is what it appears to be" is "this interface performs as it feels."

**Rams Principle 6 (Honest):** No tricks. Materials are what they are.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Methodology

### Step 1: Identify Digital Materials

| Digital Material | Physical Analog | Unit |
|-----------------|-----------------|------|
| Latency | Weight | Milliseconds |
| Bundle size | Volume | Kilobytes |
| Memory usage | Footprint | Megabytes |
| CPU cycles | Energy | Percentage |
| Network requests | Dependencies | Count |

### Step 2: Measure Baseline

```typescript
// Establish budget first
const PERFORMANCE_BUDGET = {
  firstContentfulPaint: 1000,  // 1s
  timeToInteractive: 3000,     // 3s
  bundleSize: 200,             // 200kb
  memoryHeap: 50,              // 50MB
  apiLatency: 200              // 200ms
};
```

### Step 3: Honesty Check

For each digital material, ask:
- **Perception:** What does the UI promise?
- **Reality:** What does instrumentation show?
- **Gap:** Is the UI lying?

### Step 4: Material Selection

| Decision | Question | Pass Criteria |
|----------|----------|---------------|
| Add dependency | Do we use >50% of this library? | Yes → Allow |
| Add animation | Does this communicate state or decorate? | State → Allow |
| Add request | Can this be cached/batched/eliminated? | No alternatives → Allow |
| Add computation | Can this run off main thread? | Yes/Not needed → Allow |

### Step 5: Reduction Test

Remove the material. Does function break?
- **Breaks:** Material is honest (necessary)
- **Doesn't break:** Material is dishonest (decoration)

## Tests

| Test | Pass Criteria | Fail Criteria |
|------|---------------|---------------|
| **Perception = Reality** | UI feels fast, measures fast | UI feels fast, measures slow |
| **Budget Compliance** | All materials within budget | Any material exceeds budget |
| **Material Justification** | Every kb/ms has functional purpose | Resources used for decoration |
| **No Fake Optimization** | Real caching, not spinner theater | Spinners hiding poor performance |

## Anti-Patterns

| Anti-Pattern | Why Wrong | Alternative |
|--------------|-----------|-------------|
| **Spinner to hide latency** | Dishonest about performance | Fix latency, show progress honestly |
| **Unused library code** | Waste masquerading as features | Import only what you use |
| **"Premium feel" animations** | Decoration consuming resources | Animate only state changes |
| **Optimistic UI without rollback** | Lying about success | Show real state |
| **Heavy framework for simple task** | Wrong material for job | Match material to function |

## Examples

### Good Example

```typescript
// Honest material usage
import { debounce } from './utils/debounce';  // 0.2kb, single function
// Not: import _ from 'lodash';              // 71kb, 1% used

// Performance budget enforced
if (bundle.size > BUDGET.bundleSize) {
  throw new Error('Bundle exceeds honest material budget');
}

// Honest latency communication
<Button disabled={loading} aria-label="Saving... 2s remaining">
  {loading ? `Saving... ${timeRemaining}s` : 'Save'}
</Button>
```

### Bad Example

```typescript
// Dishonest materials
import _ from 'lodash';  // 71kb for one function
import moment from 'moment';  // 288kb for date formatting
import animejs from 'animejs';  // 23kb for decoration

// Fake optimization
<Button onClick={async () => {
  setLoading(true);
  await new Promise(r => setTimeout(r, 500));  // Fake delay
  await actualSave();  // Real delay
}}>
  Save  {/* Lying about duration */}
</Button>

// No budget
// Ship first, optimize never
```

## Implementation Checklist

- [ ] Performance budget defined for all digital materials
- [ ] Bundle analyzer configured (webpack-bundle-analyzer)
- [ ] Lighthouse CI in deployment pipeline
- [ ] Real User Monitoring (RUM) capturing p95 latency
- [ ] Every dependency >10kb justified in docs
- [ ] No spinners without honest duration estimates
- [ ] Memory profiling in Chrome DevTools
- [ ] Network waterfall reviewed monthly


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

