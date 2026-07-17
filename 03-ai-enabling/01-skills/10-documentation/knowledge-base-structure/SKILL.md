---
last_updated: 2026-02-25
status: active
name: knowledge-base-structure
description: Knowledge base organization - information architecture, doc site structure, search optimization. Use for structuring documentation sites.
triggers:
  files: ["**/docs/**", "**/wiki/**", "**/knowledge/**", "**/mkdocs.yml", "**/docusaurus.config.js"]
  keywords: ["knowledge base", "documentation site", "information architecture", "doc structure", "wiki", "docs organization"]
allowed-tools: Read, Write, Edit
---

# Knowledge Base Structure Skill

Organize documentation into a discoverable, maintainable knowledge base. Create information architecture that helps users find what they need quickly.

---

## Core Principles

### Knowledge Base Goals

| Goal | Description |
|------|-------------|
| **Findable** | Users locate information quickly |
| **Understandable** | Content matches user mental models |
| **Maintainable** | Authors can update easily |
| **Scalable** | Structure grows with content |

### Key Tenets

1. **User-centered organization**: Group by user task, not internal structure
2. **Progressive disclosure**: Overview → details → reference
3. **Multiple paths**: Browse, search, cross-links all work
4. **Clear hierarchy**: Max 3-4 levels deep
5. **Consistent naming**: Predictable, descriptive titles

---

## Documentation Types (Diátaxis Framework)

### The Four Quadrants

| Type | Purpose | User Mode | Format |
|------|---------|-----------|--------|
| **Tutorials** | Learn by doing | Study | Step-by-step guide |
| **How-To Guides** | Solve specific problems | Work | Goal-oriented recipes |
| **Explanation** | Understand concepts | Study | Narrative discussion |
| **Reference** | Look up details | Work | Structured facts |

### Organizing by Type

```
docs/
├── tutorials/           # Learning-oriented
│   ├── getting-started/
│   └── build-first-topic/
├── how-to/              # Task-oriented
│   ├── configure-sources/
│   ├── pin-evidence/
│   └── export-topics/
├── concepts/            # Understanding-oriented
│   ├── crystallization-process/
│   └── evidence-selection/
└── reference/           # Information-oriented
    ├── api/
    ├── cli/
    └── configuration/
```

---

## Directory Structures

### Product Documentation

```
docs/
├── index.md                    # Landing page
├── getting-started/
│   ├── index.md               # Quick start
│   ├── installation.md
│   ├── first-project.md
│   └── concepts.md
├── guides/                     # How-to guides
│   ├── index.md
│   ├── topics/
│   │   ├── create-topic.md
│   │   ├── crystallize-topic.md
│   │   └── export-topic.md
│   ├── evidence/
│   │   ├── add-sources.md
│   │   ├── pin-evidence.md
│   │   └── filter-evidence.md
│   └── admin/
│       ├── user-management.md
│       └── integrations.md
├── concepts/                   # Explanations
│   ├── index.md
│   ├── evidence-model.md
│   ├── crystallization.md
│   └── relevance-scoring.md
├── reference/                  # Reference docs
│   ├── index.md
│   ├── api/
│   │   ├── index.md
│   │   ├── topics.md
│   │   ├── evidence.md
│   │   └── users.md
│   ├── cli/
│   │   └── commands.md
│   └── configuration/
│       ├── environment.md
│       └── config-file.md
├── troubleshooting/            # Problem-solving
│   ├── index.md
│   ├── common-errors.md
│   └── faq.md
└── changelog.md
```

### Internal Knowledge Base

```
knowledge/
├── company/
│   ├── overview.md
│   ├── values.md
│   └── org-chart.md
├── processes/
│   ├── onboarding/
│   ├── development/
│   └── support/
├── products/
│   ├── product-a/
│   └── product-b/
├── tools/
│   ├── engineering/
│   ├── design/
│   └── operations/
├── runbooks/
│   ├── incidents/
│   └── maintenance/
└── templates/
```

### API Documentation

```
docs/
├── index.md                    # API overview
├── authentication.md
├── rate-limits.md
├── errors.md
├── endpoints/
│   ├── topics.md
│   ├── evidence.md
│   └── users.md
├── webhooks/
│   ├── overview.md
│   └── events.md
├── sdks/
│   ├── javascript.md
│   ├── python.md
│   └── go.md
└── changelog.md
```

---

## Navigation Design

### Primary Navigation

Keep top-level navigation to 5-7 items:

```yaml
# mkdocs.yml or docusaurus.config.js
nav:
  - Home: index.md
  - Getting Started: getting-started/
  - Guides: guides/
  - Concepts: concepts/
  - Reference: reference/
  - Support: troubleshooting/
```

### Sidebar Organization

Group related content, use clear headings:

```yaml
sidebar:
  - section: Getting Started
    items:
      - Quick Start
      - Installation
      - First Project
  - section: Guides
    collapsed: true
    items:
      - Topics
      - Evidence
      - Administration
  - section: Reference
    collapsed: true
    items:
      - API
      - CLI
      - Configuration
```

### Breadcrumbs

Help users understand location:

```
Home > Guides > Topics > Create Topic
```

---

## File Naming Conventions

### URL-Friendly Names

| Good | Bad |
|------|-----|
| `getting-started.md` | `Getting Started.md` |
| `api-reference.md` | `API_Reference.md` |
| `create-topic.md` | `How to Create a Topic.md` |

### Index Files

Use `index.md` for section landing pages:

```
guides/
├── index.md          # "Guides" landing page
├── topics/
│   ├── index.md      # "Topics" section overview
│   └── create.md
```

### Numbered Prefixes (Optional)

For explicit ordering:

```
01-introduction/
02-installation/
03-configuration/
04-usage/
```

---

## Content Templates

### Section Index Page

```markdown
# Topics Guides

Learn how to create, manage, and export topics.

## Guides in This Section

### [Create a Topic](./create-topic.md)
Start a new topic and add initial evidence.

### [Crystallize a Topic](./crystallize-topic.md)
Refine a topic into a strategic insight.

### [Export Topics](./export-topics.md)
Export topics to PDF, Markdown, or JSON.

## Related

- [Evidence Guides](../evidence/)
- [Topic Concepts](../../concepts/topics.md)
```

### Guide Page

```markdown
# Create a Topic

Create a new topic to organize related evidence.

## Prerequisites

- Active user account
- At least one data source configured

## Steps

1. Navigate to Topics
2. Click "Create Topic"
3. Enter title and description
4. Click "Save"

## Next Steps

- [Add Evidence](./add-evidence.md)
- [Crystallize Topic](./crystallize-topic.md)
```

### Concept Page

```markdown
# Topic Crystallization

Crystallization is a three-phase process that refines raw evidence
into strategic insights.

## Overview

[High-level explanation]


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## How It Works

### Phase 1: Synthesis
[Detailed explanation]

### Phase 2: Challenge
[Detailed explanation]

### Phase 3: Narrative
[Detailed explanation]

## Diagram

[Mermaid or image]

## Related

- [How to Crystallize](../guides/crystallize-topic.md)
- [Crystallization API](../reference/api/crystallize.md)
```

---

## Search Optimization

### Frontmatter for Search

```yaml
---
title: Create a Topic
description: Step-by-step guide to creating topics in Insights Copilot
keywords: topic, create, new, add
---
```

### Heading Structure

- One H1 per page (title)
- H2 for major sections
- H3 for subsections
- Include keywords users search for

### Common Search Terms

Document synonyms and alternative terms:

```markdown
# Authentication

Also known as: login, sign in, auth, credentials

## Overview
...
```

---

## Cross-Linking Strategy

### Link Types

| Type | When to Use |
|------|-------------|
| **Inline links** | When term is mentioned naturally |
| **See also** | Related topics at section end |
| **Prerequisites** | What to read first |
| **Next steps** | What to read after |

### Link Patterns

```markdown
## Prerequisites

Before starting, read [Installation](../installation.md).

## Steps

1. Open the [Topics page](/guides/topics/)
2. Configure [authentication](../reference/auth.md)

## See Also

- [Evidence Selection](../concepts/evidence.md)
- [API Reference](../reference/api/topics.md)
```

### Avoiding Dead Links

```yaml
# CI check for broken links
- name: Check links
  run: |
    npm install -g markdown-link-check
    find docs -name "*.md" | xargs markdown-link-check
```

---

## Platform-Specific Setup

### MkDocs (Material)

```yaml
# mkdocs.yml
site_name: Insights Copilot
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight
    - search.suggest

nav:
  - Home: index.md
  - Getting Started:
    - Quick Start: getting-started/index.md
    - Installation: getting-started/installation.md
  - Guides:
    - guides/index.md
    - Topics: guides/topics/
    - Evidence: guides/evidence/
  - Reference:
    - API: reference/api/
    - CLI: reference/cli.md

plugins:
  - search
  - tags

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true
```

### Docusaurus

```javascript
// docusaurus.config.js
module.exports = {
  title: 'Insights Copilot',
  themeConfig: {
    navbar: {
      items: [
        { to: 'docs/', label: 'Docs' },
        { to: 'docs/api/', label: 'API' },
      ],
    },
    docs: {
      sidebar: {
        autoCollapseCategories: true,
      },
    },
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_API_KEY',
      indexName: 'YOUR_INDEX',
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
      },
    ],
  ],
};
```

### GitBook

```yaml
# .gitbook.yaml
root: ./docs
structure:
  readme: index.md
  summary: SUMMARY.md
```

---

## Maintenance

### Content Audits

Quarterly review checklist:
- [ ] Remove outdated content
- [ ] Update screenshots
- [ ] Fix broken links
- [ ] Check search analytics for gaps
- [ ] Review feedback/questions

### Analytics to Track

| Metric | Indicates |
|--------|-----------|
| **Top pages** | What users need most |
| **Search queries** | What's hard to find |
| **Exit pages** | Where users give up |
| **Time on page** | Content quality |
| **Bounce rate** | Navigation issues |

### Feedback Loops

```markdown
<!-- At bottom of each page -->
---

Was this helpful? [Yes](#) / [No](#)

[Edit this page](https://github.com/org/repo/edit/main/docs/page.md)
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Deep nesting** | Hard to navigate | Max 3-4 levels |
| **Duplicate content** | Maintenance burden | Single source, link to it |
| **Jargon navigation** | Users can't find content | Use user terminology |
| **Orphan pages** | Not discoverable | Link from parent pages |
| **No landing pages** | Unclear where to start | Add index.md to sections |
| **Inconsistent naming** | Confusing patterns | Follow naming convention |

---

## Checklist

Before publishing knowledge base:

- [ ] Clear top-level navigation (5-7 items)
- [ ] Content organized by user task
- [ ] Index page for each section
- [ ] Max 3-4 levels of nesting
- [ ] URL-friendly file names
- [ ] Cross-links between related content
- [ ] Search configured and working
- [ ] Breadcrumbs for orientation
- [ ] No orphan pages
- [ ] Link checking in CI

---

This skill enables well-organized knowledge bases that help users find information quickly and authors maintain content easily.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

