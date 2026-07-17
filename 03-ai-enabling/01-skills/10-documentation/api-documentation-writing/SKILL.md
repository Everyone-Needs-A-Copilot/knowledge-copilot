---
last_updated: 2026-02-25
status: active
name: api-documentation-writing
description: API documentation - endpoints, parameters, responses, examples. Use for REST API, SDK, and service documentation.
triggers:
  files: ["**/api/**", "**/openapi.yaml", "**/swagger.*", "**/routes/**"]
  keywords: ["API documentation", "endpoint", "REST", "OpenAPI", "Swagger", "API reference", "parameters", "responses"]
allowed-tools: Read, Write, Edit
---

# API Documentation Writing Skill

Document REST APIs with clear endpoint descriptions, parameter specifications, response formats, and working examples.

---

## Endpoint Documentation Structure

### Required Elements

| Element | Description |
|---------|-------------|
| **HTTP Method** | GET, POST, PUT, PATCH, DELETE |
| **Path** | `/api/v1/topics/{topic_id}` |
| **Summary** | One-line description |
| **Description** | Detailed explanation |
| **Parameters** | Path, query, header, body params |
| **Responses** | All possible status codes |
| **Examples** | Request/response examples |

### Endpoint Template

```markdown

## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## GET /api/v1/topics

Returns a paginated list of topics.

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `limit` | query | integer | No | Results per page (default: 20, max: 100) |
| `offset` | query | integer | No | Number to skip (default: 0) |
| `status` | query | string | No | Filter by status: `draft`, `active`, `archived` |

### Responses

#### 200 OK

```json
{
  "data": [
    {
      "id": "abc123",
      "title": "AI in Healthcare",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 145
  }
}
```

#### 401 Unauthorized

```json
{
  "error": "unauthorized",
  "message": "Invalid or missing API key"
}
```

### Example

```bash
curl -X GET "https://api.example.com/v1/topics?status=active&limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```
```

---

## Parameter Documentation

### Path Parameters

```markdown
| Name | Type | Description |
|------|------|-------------|
| `topic_id` | string (UUID) | Unique topic identifier |
```

### Query Parameters

```markdown
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `limit` | integer | No | 20 | Results per page (1-100) |
| `sort` | string | No | `created_at` | Sort field: `created_at`, `updated_at`, `title` |
| `order` | string | No | `desc` | Sort order: `asc`, `desc` |
```

### Request Body

```markdown
### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Topic title (1-200 characters) |
| `description` | string | No | Topic description (max 2000 characters) |
| `tags` | array[string] | No | List of tag IDs |

#### Example

```json
{
  "title": "AI in Healthcare",
  "description": "Exploring AI applications in medical diagnosis",
  "tags": ["ai", "healthcare"]
}
```
```

---

## Response Documentation

### Status Code Reference

| Code | Name | When to Use |
|------|------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource state conflict (duplicate, etc.) |
| 422 | Unprocessable Entity | Semantic errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |

### Response Format

Document every possible response:

```markdown
### Responses

#### 201 Created

Returns the created topic.

```json
{
  "id": "abc123",
  "title": "AI in Healthcare",
  "status": "draft",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 400 Bad Request

Returned when validation fails.

```json
{
  "error": "validation_error",
  "message": "Title is required",
  "details": {
    "field": "title",
    "constraint": "required"
  }
}
```
```

---

## OpenAPI Specification

### Basic Structure

```yaml
openapi: 3.0.0
info:
  title: Topics API
  version: 1.0.0
  description: |
    API for managing strategic topics.

    ## Authentication
    All endpoints require Bearer token:
    ```
    Authorization: Bearer YOUR_API_KEY
    ```

servers:
  - url: https://api.example.com/v1
    description: Production

paths:
  /topics:
    get:
      summary: List topics
      operationId: listTopics
      tags: [Topics]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TopicList'
```

### Schema Definitions

```yaml
components:
  schemas:
    Topic:
      type: object
      required: [id, title, status, created_at]
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
          example: "abc123"
        title:
          type: string
          minLength: 1
          maxLength: 200
          description: Topic title
          example: "AI in Healthcare"
        status:
          type: string
          enum: [draft, active, archived]
          example: "active"
        created_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"
```

---

## Authentication Documentation

### Required Sections

```markdown
## Authentication

### API Keys

Obtain your API key from the [dashboard](https://app.example.com/settings/api).

Include in the `Authorization` header:

```bash
Authorization: Bearer YOUR_API_KEY
```

### Scopes

| Scope | Access |
|-------|--------|
| `read:topics` | Read topic data |
| `write:topics` | Create and update topics |
| `delete:topics` | Delete topics |

### Rate Limits

| Plan | Requests/Hour |
|------|---------------|
| Free | 100 |
| Pro | 10,000 |
| Enterprise | Unlimited |

Rate limit headers:
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset timestamp (Unix)
```

---

## Best Practices

### Always Include

- [ ] Complete request example with headers
- [ ] All response status codes
- [ ] Error response format
- [ ] Authentication requirements
- [ ] Rate limit information
- [ ] Data types and constraints (min/max, regex)

### Code Examples

Provide examples in multiple languages:

```markdown
### Examples

#### cURL

```bash
curl -X POST "https://api.example.com/v1/topics" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Topic"}'
```

#### Python

```python
import requests

response = requests.post(
    "https://api.example.com/v1/topics",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"title": "New Topic"}
)
```

#### JavaScript

```javascript
const response = await fetch("https://api.example.com/v1/topics", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ title: "New Topic" })
});
```
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Missing error examples | Document all error responses |
| Vague parameter descriptions | Specify type, constraints, examples |
| No authentication docs | Show how to obtain and use credentials |
| Outdated examples | Test examples in CI |
| Missing rate limits | Document limits and headers |

---

This skill enables comprehensive, developer-friendly API documentation.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

