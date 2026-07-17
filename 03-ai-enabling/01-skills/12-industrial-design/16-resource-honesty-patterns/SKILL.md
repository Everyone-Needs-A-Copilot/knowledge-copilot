---
last_updated: 2026-02-25
status: active
name: resource-honesty-patterns
description: Patterns for honest communication of loading states and async operation progress. Use when designing spinners, progress bars, or any waiting state to set accurate user expectations.
category: industrial-design-digital
keywords:
  - loading-states
  - progress
  - spinners
  - honesty
  - feedback
triggers:
  keywords:
    - loading spinner
    - progress bar
    - waiting state
    - async operation
    - loading indicator
  filePatterns:
    - "**/*.tsx"
    - "**/components/**"
    - "**/hooks/**"
allowed-tools: Read, Write, Edit
---

# Resource Honesty Patterns

Design loading states that tell the truth about what's happening.

## Philosophy

A spinner is a lie unless you don't know the duration. A progress bar is a lie unless it tracks real progress. Optimistic UI is a lie unless you handle rollback. The system must tell the truth: if it's instant, show it instantly; if it takes time, show honest progress; if it failed, admit it immediately.

**Rams Principle 6 (Honest):** No tricks. Materials are what they are.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Methodology

### Step 1: Classify Operations

| Operation Type | Duration | Honest Pattern |
|----------------|----------|----------------|
| **Cache hit** | <100ms | Instant (no loading state) |
| **Network request** | 100-500ms | Skeleton + optimistic |
| **Processing** | 500ms-5s | Progress bar with % |
| **Long operation** | >5s | Progress with time/count |
| **Indeterminate** | Unknown | Spinner + cancel button |

### Step 2: Measure Reality

Before showing UI, measure:

```typescript
interface OperationMetrics {
  p50: number;  // 50% complete in X ms
  p95: number;  // 95% complete in X ms
  p99: number;  // 99% complete in X ms
}

// Example: getInsights()
const metrics = {
  p50: 180,   // Usually fast
  p95: 450,   // Sometimes slow
  p99: 2000   // Rarely very slow
};

// Decision tree
if (metrics.p95 < 200) {
  return 'instant';  // No loading state
} else if (metrics.p95 < 1000) {
  return 'skeleton';  // Brief wait
} else {
  return 'progress';  // Show progress
}
```

### Step 3: Honest Loading States

```typescript
function LoadingState({ operation, onCancel }: Props) {
  const [progress, setProgress] = useState<number | null>(null);
  const [elapsed, setElapsed] = useState(0);

  // HONEST: Show what we know
  if (operation.itemCount !== null) {
    return (
      <div>
        Processing {operation.current} of {operation.itemCount} insights
        <ProgressBar value={(operation.current / operation.itemCount) * 100} />
      </div>
    );
  }

  // HONEST: Show we don't know
  if (operation.estimatedDuration === null) {
    return (
      <div>
        Processing... ({elapsed}s elapsed)
        <button onClick={onCancel}>Cancel</button>
      </div>
    );
  }

  // DISHONEST: Fake progress
  // ❌ <ProgressBar value={fakeProgress} />
}
```

### Step 4: Optimistic UI Contract

Optimistic UI must honor three rules:

```typescript
interface OptimisticUI<T> {
  // 1. Show optimistic state immediately
  optimistic: T;

  // 2. Handle rollback explicitly
  rollback: (error: Error) => void;

  // 3. Reconcile with server truth
  reconcile: (serverState: T) => T;
}

// Example: Optimistic delete
async function deleteInsight(id: string) {
  // 1. Optimistic removal
  const removed = removeFromUI(id);

  try {
    await api.delete(`/insights/${id}`);
    // Success: Optimistic state was correct
  } catch (error) {
    // 2. Rollback: Admit we were wrong
    restoreToUI(removed);
    showError('Delete failed. Insight restored.');
  }
}
```

### Step 5: No Fake Delays

```typescript
// DISHONEST: Fake delay to show spinner
async function saveInsight(data: Insight) {
  setLoading(true);
  await new Promise(r => setTimeout(r, 500));  // ❌ LYING
  await api.post('/insights', data);
  setLoading(false);
}

// HONEST: Real timing only
async function saveInsight(data: Insight) {
  setLoading(true);
  const start = Date.now();
  await api.post('/insights', data);
  const duration = Date.now() - start;

  // Only show "success" if operation took time
  if (duration > 200) {
    showSuccess('Saved');
  }
  setLoading(false);
}
```

## Tests

| Test | Pass Criteria | Fail Criteria |
|------|---------------|---------------|
| **No Spinners for <200ms ops** | Instant operations show instantly | Spinner for cache hits |
| **Real Progress** | Progress bar tracks actual completion | Fake/animated progress |
| **Honest Duration** | Show time or count when known | Generic "Loading..." |
| **Rollback Honesty** | Failed optimistic updates rollback | Failed updates stay visible |
| **No Fake Delays** | UI reflects real system timing | Artificial delays |

## Anti-Patterns

| Anti-Pattern | Why Wrong | Alternative |
|--------------|-----------|-------------|
| **Spinner for everything** | Lying about instant operations | Only show loading if >200ms |
| **Fake progress bars** | Animated 0→100% without tracking | Real progress or spinner |
| **Optimistic without rollback** | Lies about failure | Always handle error case |
| **Generic "Loading..."** | No information | "Loading 23 of 50 insights" |
| **Fake delays** | Theater, not honesty | Show real duration |
| **Permanent spinners** | No timeout, no cancel | Always allow cancel >5s |
| **Success theater** | Fake "Saving..." pause | Instant if instant, progress if slow |

## Examples

### Good Example

```typescript
// Honest resource loading
export function InsightsList() {
  const { insights, loading, error, progress } = useInsights();

  // Instant if cached
  if (insights && !loading) {
    return <InsightCards insights={insights} />;
  }

  // Honest error
  if (error) {
    return (
      <div className="text-red-600">
        Failed to load insights: {error.message}
        <button onClick={retry}>Retry</button>
      </div>
    );
  }

  // Honest progress
  if (progress?.total) {
    return (
      <div>
        <p>Loading {progress.current} of {progress.total} insights</p>
        <ProgressBar value={(progress.current / progress.total) * 100} />
        <p className="text-sm text-gray-500">
          {progress.estimatedRemaining}s remaining
        </p>
      </div>
    );
  }

  // Honest uncertainty
  return (
    <div>
      <Spinner />
      <p>Loading insights... ({elapsed}s)</p>
      <button onClick={cancel}>Cancel</button>
    </div>
  );
}

// Optimistic deletion with honest rollback
export function useDeleteInsight() {
  const [insights, setInsights] = useState<Insight[]>([]);

  const deleteInsight = async (id: string) => {
    // Optimistic removal
    const backup = insights;
    setInsights(insights.filter(i => i.id !== id));

    try {
      await api.delete(`/insights/${id}`);
      // Success: optimistic state was correct
    } catch (error) {
      // Rollback: admit we were wrong
      setInsights(backup);
      toast.error('Delete failed. Insight restored.');
    }
  };

  return { insights, deleteInsight };
}
```

### Bad Example

```typescript
// Dishonest resource loading
export function InsightsList() {
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState<Insight[]>([]);

  useEffect(() => {
    async function load() {
      setLoading(true);
      await new Promise(r => setTimeout(r, 500));  // ❌ Fake delay
      const data = await api.get('/insights');
      await new Promise(r => setTimeout(r, 300));  // ❌ "Success theater"
      setInsights(data);
      setLoading(false);
    }
    load();
  }, []);

  // Generic spinner (no info)
  if (loading) {
    return <Spinner />;  // ❌ How long? How many? Can cancel?
  }

  // Silent failure
  if (insights.length === 0) {
    return <div>No insights</div>;  // ❌ Error or truly empty?
  }

  return <InsightCards insights={insights} />;
}

// Dishonest optimistic UI
export function useDeleteInsight() {
  const [insights, setInsights] = useState<Insight[]>([]);

  const deleteInsight = async (id: string) => {
    setInsights(insights.filter(i => i.id !== id));
    await api.delete(`/insights/${id}`);
    // ❌ No error handling
    // ❌ No rollback
    // ❌ Failed delete stays deleted in UI
  };

  return { insights, deleteInsight };
}
```

## Implementation Checklist

- [ ] Operations <200ms show no loading state
- [ ] Operations 200ms-1s show skeleton screens
- [ ] Operations >1s show progress (%, count, or time)
- [ ] Progress bars track real completion (not fake animation)
- [ ] Indeterminate operations show elapsed time
- [ ] Long operations (>5s) have cancel button
- [ ] Optimistic UI has explicit rollback handlers
- [ ] Failed optimistic updates rollback visibly
- [ ] Error states show actual error messages
- [ ] No artificial delays for "polish"
- [ ] RUM metrics tracked for p50/p95/p99 timing
- [ ] Loading states match measured reality


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

