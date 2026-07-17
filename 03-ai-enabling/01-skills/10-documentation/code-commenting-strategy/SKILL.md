---
last_updated: 2026-02-25
status: active
name: code-commenting-strategy
description: Code comments - when to comment, JSDoc/docstrings, TODO patterns, self-documenting code. Use for code documentation strategy.
triggers:
  files: ["**/*.ts", "**/*.js", "**/*.py", "**/*.go", "**/*.java"]
  keywords: ["comments", "JSDoc", "docstring", "TODO", "code documentation", "self-documenting", "inline documentation"]
allowed-tools: Read, Write, Edit
---

# Code Commenting Strategy Skill

Write effective code comments that explain "why" not "what". Know when comments add value and when code should speak for itself.

---

## Core Principles

### The Comment Hierarchy

| Level | What | When |
|-------|------|------|
| **Self-documenting code** | Names, structure explain intent | Always prefer |
| **Public API docs** | JSDoc, docstrings | All public interfaces |
| **Why comments** | Non-obvious decisions | When intent unclear from code |
| **What comments** | Step-by-step explanation | Complex algorithms only |

### Golden Rule

**Comments explain WHY, code explains WHAT.**

If you need a comment to explain what code does, consider refactoring first.

---


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## When to Comment

### Always Comment

| Situation | Example |
|-----------|---------|
| **Public APIs** | Functions, classes, methods others will use |
| **Non-obvious decisions** | Why this approach over simpler one |
| **Workarounds** | Hacks, browser quirks, library bugs |
| **Performance optimizations** | Why this seemingly complex code |
| **Regex patterns** | What the pattern matches |
| **Magic numbers** | What 86400 means |
| **TODOs** | With issue number and context |

### Never Comment

| Situation | Why |
|-----------|-----|
| **Obvious code** | `i++` doesn't need "increment i" |
| **Restating the code** | `// Set name to John` for `name = "John"` |
| **Commented-out code** | Use version control instead |
| **Change history** | That's what git log is for |
| **Venting/jokes** | Unprofessional, distracting |

---

## Self-Documenting Code

### Naming Over Comments

```typescript
// Bad: Comment needed because name is unclear
// Calculate the total price including tax
const x = items.reduce((sum, i) => sum + i.price, 0) * 1.1;

// Good: Name explains itself
const totalPriceWithTax = calculateTotalWithTax(items, TAX_RATE);
```

### Extract Functions Over Comments

```typescript
// Bad: Comments explaining steps
function processOrder(order: Order) {
  // Validate the order
  if (!order.items.length) throw new Error('Empty order');
  if (!order.customer) throw new Error('No customer');

  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }

  // Apply discount
  if (order.customer.isPremium) {
    total *= 0.9;
  }

  return total;
}

// Good: Functions are self-documenting
function processOrder(order: Order) {
  validateOrder(order);
  const subtotal = calculateSubtotal(order.items);
  return applyCustomerDiscount(subtotal, order.customer);
}
```

### Constants Over Magic Numbers

```typescript
// Bad: Magic number with comment
// 86400 seconds in a day
const expiry = Date.now() + 86400 * 1000;

// Good: Named constant
const SECONDS_PER_DAY = 86400;
const cacheExpiryMs = Date.now() + SECONDS_PER_DAY * 1000;
```

---

## JSDoc / TSDoc (JavaScript/TypeScript)

### Function Documentation

```typescript
/**
 * Selects relevant evidence for a topic based on semantic similarity.
 *
 * @param topicId - The topic to select evidence for
 * @param options - Selection options
 * @param options.maxResults - Maximum evidence items to return (default: 20)
 * @param options.threshold - Minimum similarity score 0-1 (default: 0.6)
 * @returns Ranked evidence items with relevance scores
 *
 * @throws {TopicNotFoundError} When topic doesn't exist
 * @throws {InsufficientEvidenceError} When no evidence meets threshold
 *
 * @example
 * ```typescript
 * const evidence = await selectEvidence('topic-123', {
 *   maxResults: 10,
 *   threshold: 0.7
 * });
 * ```
 *
 * @see {@link TopicService} for topic management
 */
async function selectEvidence(
  topicId: string,
  options?: SelectionOptions
): Promise<Evidence[]> {
  // ...
}
```

### Class Documentation

```typescript
/**
 * Client for the Insights API.
 *
 * Handles authentication, request/response serialization, and error handling.
 *
 * @example
 * ```typescript
 * const client = new InsightsClient({ apiKey: 'your-key' });
 * const topics = await client.topics.list();
 * ```
 */
export class InsightsClient {
  /**
   * Creates a new API client.
   *
   * @param config - Client configuration
   * @param config.apiKey - API key for authentication
   * @param config.baseUrl - Override default API URL (optional)
   * @param config.timeout - Request timeout in ms (default: 5000)
   */
  constructor(config: ClientConfig) {
    // ...
  }
}
```

### Interface Documentation

```typescript
/**
 * Configuration for evidence selection.
 */
interface SelectionOptions {
  /** Maximum number of evidence items to return (1-100) */
  maxResults?: number;

  /** Minimum similarity score for inclusion (0.0-1.0) */
  threshold?: number;

  /** Filter by source types */
  sourceTypes?: ('assessment' | 'research' | 'web')[];
}
```

---

## Python Docstrings

### Google Style (Recommended)

```python
def select_evidence(
    topic_id: str,
    max_results: int = 20,
    threshold: float = 0.6
) -> list[Evidence]:
    """Select relevant evidence for a topic.

    Uses semantic similarity to rank and filter evidence from
    all connected sources.

    Args:
        topic_id: The topic to select evidence for.
        max_results: Maximum items to return. Defaults to 20.
        threshold: Minimum similarity score (0-1). Defaults to 0.6.

    Returns:
        List of Evidence objects ranked by relevance score.

    Raises:
        TopicNotFoundError: If topic_id doesn't exist.
        InsufficientEvidenceError: If no evidence meets threshold.

    Example:
        >>> evidence = select_evidence('topic-123', max_results=10)
        >>> print(evidence[0].score)
        0.89
    """
    pass
```

### Class Docstring

```python
class InsightsClient:
    """Client for the Insights API.

    Handles authentication, request/response serialization, and retries.

    Attributes:
        base_url: The API base URL.
        timeout: Request timeout in seconds.

    Example:
        >>> client = InsightsClient(api_key='your-key')
        >>> topics = client.topics.list()
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = 'https://api.example.com',
        timeout: int = 30
    ) -> None:
        """Initialize the client.

        Args:
            api_key: API key for authentication.
            base_url: Override default API URL.
            timeout: Request timeout in seconds.
        """
        pass
```

---

## Why Comments

### Non-Obvious Decisions

```typescript
// Use array instead of Set for evidence IDs because:
// 1. Order matters for relevance ranking
// 2. Set iteration is slower for small collections (<100 items)
// 3. We need index-based access in crystallization phases
const evidenceIds: string[] = [];
```

### Workarounds

```typescript
// WORKAROUND: Qdrant v1.7 returns incorrect results when using
// OR filters. Split into separate queries and merge client-side.
// Remove when upgrading to v1.8+
// Issue: https://github.com/qdrant/qdrant/issues/12345
const resultsA = await client.search(filterA);
const resultsB = await client.search(filterB);
const merged = dedupeAndMerge(resultsA, resultsB);
```

### Performance Optimizations

```typescript
// Cache embeddings in Redis (1h TTL) because:
// 1. OpenAI API calls cost $0.0001 per embedding
// 2. Same evidence is often re-processed across topics
// 3. Embeddings are deterministic for same input
const cached = await redis.get(`embedding:${hash}`);
if (cached) return JSON.parse(cached);
```

### External Dependencies

```typescript
// Rate limit to 60 req/min per OpenAI tier 1 limits
// See: https://platform.openai.com/docs/guides/rate-limits
const rateLimiter = new RateLimiter({ tokensPerMinute: 60 });
```

---

## TODO Comments

### Format

```typescript
// TODO(#123): Extract to separate service when adding more source types
// TODO(@username): Review security implications before merging
// FIXME(#456): Memory leak in long-running connections
// HACK: Temporary fix until upstream library patches CVE-2024-1234
```

### Rules

| Rule | Why |
|------|-----|
| **Always include issue number** | Trackable, searchable |
| **Brief context** | Why it's a TODO |
| **Owner or team** | Who should address it |
| **No stale TODOs** | Review quarterly |

### Anti-Patterns

```typescript
// Bad: Vague, no tracking
// TODO: fix this later

// Bad: Ancient TODO (from 2019)
// TODO: optimize when we have more users

// Bad: Wishful thinking (no plan to do it)
// TODO: rewrite entire system in Rust
```

---

## Comment Formatting

### Line Length

Keep comments under 80-100 characters. Break long comments:

```typescript
// This algorithm uses exponential backoff with jitter to avoid
// thundering herd problems when multiple clients retry simultaneously.
// See: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
```

### Placement

```typescript
// Above the code it describes
const result = complexOperation();

// Not at end of line (hard to read)
const result = complexOperation(); // Don't do this for long comments
```

### Multi-Line Comments

```typescript
/*
 * Use block comments for longer explanations that span
 * multiple paragraphs.
 *
 * This format works well for:
 * - File headers
 * - Complex algorithm explanations
 * - License notices
 */
```

---

## Comment Anti-Patterns

### Restating Code

```typescript
// Bad: Just repeating what code says
// Set the user name to the input value
userName = input.value;

// Good: No comment needed - code is clear
userName = input.value;
```

### Commented-Out Code

```typescript
// Bad: Use version control instead
// const oldImplementation = () => {
//   // ... 50 lines of dead code
// };

// Good: Delete it. Git remembers.
```

### Journal Comments

```typescript
// Bad: That's what git log is for
// 2024-01-15: Added retry logic (John)
// 2024-01-10: Fixed null check (Jane)
// 2024-01-05: Initial implementation (John)

// Good: Use git blame
```

### Misleading Comments

```typescript
// Bad: Comment says one thing, code does another
// Returns the user's full name
function getName(user: User) {
  return user.email; // Actually returns email!
}
```

### Excessive Comments

```typescript
// Bad: Comments on obvious code
// Declare a variable to hold the count
let count = 0;
// Loop through each item
for (const item of items) {
  // Increment the count
  count++;
}
// Return the final count
return count;

// Good: Let code speak
return items.length;
```

---

## Language-Specific Guidelines

### TypeScript/JavaScript

- Use JSDoc for all exported functions/classes
- Prefer TypeScript types over JSDoc types
- Use `@see`, `@example`, `@throws` tags

### Python

- Use docstrings (Google or NumPy style)
- Document all public functions/classes
- Include type hints (Python 3.9+)

### Go

- Godoc comments start with function name
- Full sentences with periods
- First paragraph is summary

```go
// SelectEvidence returns relevant evidence for a topic.
// It uses semantic similarity to rank results from all sources.
func SelectEvidence(topicID string, opts Options) ([]Evidence, error) {
```

### Java

- Javadoc for all public methods
- `@param`, `@return`, `@throws` required
- First sentence is method summary

---

## Checklist

Before committing:

- [ ] Public APIs have doc comments
- [ ] No commented-out code
- [ ] No obvious/redundant comments
- [ ] TODOs have issue numbers
- [ ] Workarounds explain why and link to issue
- [ ] Magic numbers are constants or explained
- [ ] Complex regex patterns are documented
- [ ] Self-documenting names used where possible

---

This skill enables effective code documentation that helps future developers (including yourself) understand intent without cluttering the codebase.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

