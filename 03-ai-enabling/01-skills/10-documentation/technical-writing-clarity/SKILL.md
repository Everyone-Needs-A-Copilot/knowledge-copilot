---
last_updated: 2026-02-25
status: active
name: technical-writing-clarity
description: Clear technical writing - active voice, simple words, scannable structure. Use for improving documentation clarity.
triggers:
  files: ["**/docs/**", "**/README.md", "**/*.md"]
  keywords: ["clarity", "readability", "active voice", "plain language", "documentation style", "writing guidelines"]
allowed-tools: Read, Write, Edit
---

# Technical Writing Clarity Skill

Write clear, readable technical documentation using active voice, simple words, and scannable structure.

---

## Core Principles

### Voice and Tense

| Principle | Bad | Good |
|-----------|-----|------|
| **Active voice** | "The file is read by the parser" | "The parser reads the file" |
| **Present tense** | "The function will return" | "The function returns" |
| **Imperative mood** | "You should install" | "Install the package" |
| **Direct address** | "Users can configure" | "You can configure" or "Configure..." |

### Word Choice

| Avoid | Use Instead |
|-------|-------------|
| utilize | use |
| terminate | end, stop |
| facilitate | help, enable |
| leverage | use |
| implement | build, create |
| commence | start, begin |
| endeavor | try |
| subsequently | then, next |
| prior to | before |
| in order to | to |

### Sentence Structure

**Keep sentences short**: Target 15-20 words. Split long sentences.

**Bad**:
```
The configuration file, which is located in the root directory of the project and contains all the settings for the application, must be edited before running the server for the first time.
```

**Good**:
```
Edit the configuration file before running the server. The file is in the project root directory.
```

---


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## Scannable Structure

### Use Headers

Break content into sections with descriptive headers:
- H1: Main topic (one per page)
- H2: Major sections
- H3: Subsections
- H4: Rarely needed (consider restructuring)

### Use Lists

**Bullets for unordered items**:
- Feature A
- Feature B
- Feature C

**Numbers for sequences**:
1. Install dependencies
2. Configure settings
3. Start the server

### Use Tables

| Component | Purpose | Location |
|-----------|---------|----------|
| API | Request handling | `/api` |
| Services | Business logic | `/services` |
| Models | Data structures | `/models` |

### Use Code Blocks

Always use fenced code blocks with language hints:

```typescript
const config = loadConfig();
```

---

## Formatting Patterns

### Emphasis

| Type | Usage | Example |
|------|-------|---------|
| **Bold** | Key terms, UI elements | Click **Save** |
| `Code` | Filenames, commands, values | Set `DEBUG=true` |
| *Italic* | Introducing terms | This is called *dependency injection* |

### Links

| Bad | Good |
|-----|------|
| "Click here" | "[API Documentation](./api.md)" |
| "See documentation" | "[See the configuration guide](./config.md)" |

### Callouts

Use callouts sparingly for important information:

> **Note**: Configuration changes require a restart.

> **Warning**: This operation cannot be undone.

> **Tip**: Use `--verbose` for detailed output.

---

## Clarity Checklist

Before publishing documentation:

- [ ] Every sentence uses active voice
- [ ] No jargon without definition
- [ ] Sentences under 25 words
- [ ] Headers describe content clearly
- [ ] Code examples are complete and runnable
- [ ] All acronyms defined on first use
- [ ] No "wall of text" paragraphs
- [ ] Links are descriptive (not "click here")

---

## Anti-Patterns

### Vague Headings

| Bad | Good |
|-----|------|
| "Introduction" | "What This Tool Does" |
| "Details" | "Authentication Methods" |
| "Information" | "Rate Limits and Quotas" |

### Passive Voice

| Bad | Good |
|-----|------|
| "The request is processed by the server" | "The server processes the request" |
| "Errors will be logged" | "The system logs errors" |
| "Data can be exported" | "Export data using..." |

### Abstract Without Examples

| Bad | Good |
|-----|------|
| "Configure the settings appropriately" | "Set `timeout=30` in `config.yml`" |
| "Handle errors properly" | "Catch `NetworkError` and retry after 5 seconds" |

---

## Quick Reference

### Active Voice Test

If you can add "by zombies" after the verb and it makes sense, it's passive voice.

- "The file is read [by zombies]" = Passive
- "The parser reads the file" = Active

### Readability Target

- **Flesch Reading Ease**: 60+ (plain English)
- **Grade Level**: 8th grade or lower
- **Sentence Length**: Average 15 words

---

This skill enables clear, professional technical documentation that readers can understand quickly.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

