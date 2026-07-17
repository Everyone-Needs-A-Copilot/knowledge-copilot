---
last_updated: 2026-02-25
status: active
name: example-driven-documentation
description: Example-driven documentation - concrete examples for every concept. Use for reference documentation and API guides.
triggers:
  files: ["**/docs/**", "**/examples/**", "**/README.md"]
  keywords: ["example", "sample", "demo", "code example", "usage", "snippet", "how to use"]
allowed-tools: Read, Write, Edit
---

# Example-Driven Documentation Skill

Write documentation where every concept, parameter, and feature is illustrated with concrete, working examples.

---

## Core Principle

**Every abstraction needs a concrete example.**

| Abstract | Concrete |
|----------|----------|
| "Pass configuration options" | `{ timeout: 5000, retries: 3 }` |
| "Handle errors appropriately" | `catch (error) { if (error.code === 'NOT_FOUND') ... }` |
| "Set the environment variable" | `export API_KEY=sk-abc123` |

---


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## Example Patterns

### Before/After Examples

Show transformation:

```markdown
### Formatting Dates

**Input**:
```javascript
formatDate(new Date('2024-01-15T10:30:00Z'))
```

**Output**:
```
January 15, 2024 at 10:30 AM
```
```

### Minimal Examples

Start with the simplest case:

```markdown
### Basic Usage

```typescript
const client = new Client({ apiKey: 'your-key' });
const topics = await client.getTopics();
```
```

### Progressive Examples

Build complexity gradually:

```markdown
### Basic Usage

```typescript
const topics = await client.getTopics();
```

### With Filtering

```typescript
const topics = await client.getTopics({
  status: 'active',
  limit: 10
});
```

### With Pagination

```typescript
let offset = 0;
let allTopics = [];

while (true) {
  const { data, pagination } = await client.getTopics({
    limit: 100,
    offset
  });

  allTopics.push(...data);

  if (data.length < 100) break;
  offset += 100;
}
```
```

---

## Parameter Documentation

### Every Parameter Gets an Example

```markdown
## Parameters

### `timeout` (number)

Request timeout in milliseconds.

**Default**: `30000`

**Example**:
```typescript
const client = new Client({
  apiKey: 'your-key',
  timeout: 5000  // 5 second timeout
});
```

---

### `retries` (number)

Number of retry attempts on failure.

**Default**: `3`

**Example**:
```typescript
const client = new Client({
  apiKey: 'your-key',
  retries: 5  // More retries for unreliable networks
});
```

---

### `baseURL` (string)

Custom API endpoint URL.

**Default**: `https://api.example.com`

**Example**:
```typescript
// For staging environment
const client = new Client({
  apiKey: 'your-key',
  baseURL: 'https://staging.api.example.com'
});
```
```

---

## Function Documentation

### Every Function Gets Usage Examples

```markdown
## `selectEvidence(params)`

Selects relevant evidence for a topic.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topicId` | string | Yes | Topic ID |
| `maxResults` | number | No | Max items (default: 20) |
| `filters` | object | No | Filter criteria |

### Returns

`Promise<Evidence[]>` - Array of evidence items

### Examples

**Basic usage**:
```typescript
const evidence = await selector.selectEvidence({
  topicId: 'abc123'
});
// Returns: [{ id: 'ev-1', content: '...', score: 0.89 }, ...]
```

**With limit**:
```typescript
const evidence = await selector.selectEvidence({
  topicId: 'abc123',
  maxResults: 5
});
```

**With filters**:
```typescript
const evidence = await selector.selectEvidence({
  topicId: 'abc123',
  filters: {
    sourceTypes: ['assessment', 'research'],
    dateRange: {
      start: '2024-01-01',
      end: '2024-12-31'
    }
  }
});
```
```

---

## Error Handling Examples

### Show How to Handle Each Error

```markdown
## Error Handling

### NotFoundError

Thrown when the topic doesn't exist.

```typescript
try {
  const topic = await client.getTopic('invalid-id');
} catch (error) {
  if (error.code === 'NOT_FOUND') {
    console.log('Topic not found:', error.topicId);
    // Create a new topic or show error to user
  }
}
```

### RateLimitError

Thrown when API rate limit is exceeded.

```typescript
try {
  const topics = await client.getTopics();
} catch (error) {
  if (error.code === 'RATE_LIMITED') {
    const retryAfter = error.retryAfter; // seconds
    console.log(`Rate limited. Retry after ${retryAfter}s`);
    await sleep(retryAfter * 1000);
    // Retry the request
  }
}
```

### ValidationError

Thrown when request data is invalid.

```typescript
try {
  await client.createTopic({ title: '' }); // Empty title
} catch (error) {
  if (error.code === 'VALIDATION_ERROR') {
    console.log('Invalid field:', error.field);
    console.log('Message:', error.message);
    // Show validation error to user
  }
}
```
```

---

## Configuration Examples

### Show Complete Config Files

```markdown
## Configuration

### Minimal Configuration

```yaml
# config.yml
api_key: your-api-key
```

### Full Configuration

```yaml
# config.yml
api_key: your-api-key

# API settings
api:
  base_url: https://api.example.com
  timeout: 30000
  retries: 3

# Database settings
database:
  url: postgresql://localhost:5432/mydb
  pool_size: 10
  ssl: true

# Logging
logging:
  level: info
  format: json
  output: stdout

# Features
features:
  caching: true
  analytics: false
```
```

---

## Real-World Scenarios

### Use Cases with Complete Examples

```markdown
## Common Use Cases

### Batch Processing Topics

Process multiple topics in parallel with rate limiting:

```typescript
import pLimit from 'p-limit';

const limit = pLimit(5); // Max 5 concurrent

const topicIds = ['id1', 'id2', 'id3', /* ... */];

const results = await Promise.all(
  topicIds.map(id =>
    limit(() => client.crystallizeTopic(id))
  )
);

console.log(`Processed ${results.length} topics`);
```

### Webhook Integration

Handle incoming webhooks for topic updates:

```typescript
app.post('/webhooks/topics', async (req, res) => {
  const { event, topic } = req.body;

  switch (event) {
    case 'topic.created':
      await notifyTeam(`New topic: ${topic.title}`);
      break;

    case 'topic.crystallized':
      await exportToPdf(topic.id);
      break;

    case 'topic.deleted':
      await cleanupResources(topic.id);
      break;
  }

  res.status(200).send('OK');
});
```

### Retry with Exponential Backoff

Handle transient failures gracefully:

```typescript
async function fetchWithRetry(fn, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;

      const delay = Math.pow(2, attempt) * 1000;
      console.log(`Retry ${attempt + 1} after ${delay}ms`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
}

// Usage
const topics = await fetchWithRetry(() =>
  client.getTopics({ limit: 100 })
);
```
```

---

## Example Quality Checklist

### Every Example Should Be

- [ ] **Complete**: Can be copied and run without modification
- [ ] **Realistic**: Uses plausible data, not "foo" and "bar"
- [ ] **Correct**: Actually works (test in CI)
- [ ] **Minimal**: No unnecessary code
- [ ] **Commented**: Explains non-obvious parts

### Example Data Guidelines

| Bad | Good |
|-----|------|
| `"foo"` | `"AI in Healthcare"` |
| `123` | `topicId: 'abc123'` |
| `"test@test.com"` | `"developer@example.com"` |
| `"xxx"` | `apiKey: process.env.API_KEY` |

---

## Testing Examples

### Validate Examples in CI

```yaml
# .github/workflows/docs.yml
- name: Test documentation examples
  run: |
    # Extract TypeScript examples from docs
    npx ts-extract-examples docs/**/*.md -o test-examples/

    # Compile and run them
    npx tsc test-examples/**/*.ts --noEmit
```

---

This skill ensures documentation is grounded in concrete, working examples.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

