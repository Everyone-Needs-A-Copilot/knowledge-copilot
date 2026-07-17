---
last_updated: 2026-02-25
status: active
name: readme-excellence
description: README writing - project overviews, quick starts, badges, installation guides. Use for creating effective README files.
triggers:
  files: ["**/README.md", "**/readme.md", "**/README.rst"]
  keywords: ["readme", "project overview", "quick start", "getting started", "installation guide"]
allowed-tools: Read, Write, Edit
---

# README Excellence Skill

Write compelling README files that help users understand, install, and use your project quickly. The README is often the first thing users see - make it count.

---

## Core Principles

### README Goals

| Goal | Description |
|------|-------------|
| **Hook** | Grab attention in first 10 seconds |
| **Explain** | What does this do? Why should I care? |
| **Enable** | Get running in <5 minutes |
| **Guide** | Point to detailed docs when needed |

### Key Tenets

1. **Show, don't tell**: Code examples > descriptions
2. **Quick start first**: Running code in <5 commands
3. **Progressive disclosure**: Simple → complex
4. **Keep it current**: Outdated READMEs erode trust
5. **Mobile-friendly**: Many read on phones

---

## README Structure

### Optimal Section Order

```markdown
# Project Name

One-line tagline

[Badges]

## Overview / What is this?

## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## Features
## Quick Start
## Installation
## Usage
## Configuration
## API Reference (or link)
## Development
## Contributing
## License
```

### Minimal README (Small Projects)

```markdown
# Project Name

Brief description.

## Quick Start

```bash
npm install project-name
```

```javascript
import { thing } from 'project-name';
thing.doSomething();
```

## License

MIT
```

### Full README (Major Projects)

See template below.

---

## README Template

```markdown
# Project Name

One-sentence description of what this project does and who it's for.

[![Build Status](https://img.shields.io/github/actions/workflow/status/org/repo/ci.yml)](https://github.com/org/repo/actions)
[![npm version](https://img.shields.io/npm/v/package-name)](https://www.npmjs.com/package/package-name)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

2-3 sentences expanding on the tagline:
- What problem does this solve?
- How is it different from alternatives?
- Who should use this?

## Features

- **Feature 1**: Brief description
- **Feature 2**: Brief description
- **Feature 3**: Brief description

## Quick Start

Get running in under 2 minutes:

```bash
npm install package-name
```

```javascript
import { Client } from 'package-name';

const client = new Client({ apiKey: 'your-key' });
const result = await client.doThing();
console.log(result);
```

## Installation

### Prerequisites

- Node.js 18+
- npm 9+

### npm

```bash
npm install package-name
```

### yarn

```bash
yarn add package-name
```

### pnpm

```bash
pnpm add package-name
```

## Usage

### Basic Example

```javascript
import { Client } from 'package-name';

const client = new Client({
  apiKey: process.env.API_KEY
});

// Fetch data
const data = await client.getData({ id: '123' });
console.log(data);
```

### Advanced Usage

#### With Custom Options

```javascript
const client = new Client({
  apiKey: process.env.API_KEY,
  timeout: 5000,
  retries: 3
});
```

#### Error Handling

```javascript
try {
  const data = await client.getData({ id: '123' });
} catch (error) {
  if (error.code === 'NOT_FOUND') {
    console.log('Item not found');
  } else {
    throw error;
  }
}
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_KEY` | Yes | - | Your API key |
| `TIMEOUT` | No | `5000` | Request timeout in ms |
| `DEBUG` | No | `false` | Enable debug logging |

### Configuration File

```javascript
// config.js
module.exports = {
  apiKey: process.env.API_KEY,
  options: {
    timeout: 5000,
    retries: 3
  }
};
```

## API Reference

See [API Documentation](./docs/api.md) for full reference.

### Key Methods

| Method | Description |
|--------|-------------|
| `client.getData(id)` | Fetch item by ID |
| `client.createData(data)` | Create new item |
| `client.updateData(id, data)` | Update existing item |
| `client.deleteData(id)` | Delete item |

## Development

### Setup

```bash
git clone https://github.com/org/repo.git
cd repo
npm install
```

### Running Tests

```bash
npm test                 # Run all tests
npm run test:watch       # Watch mode
npm run test:coverage    # With coverage
```

### Building

```bash
npm run build           # Production build
npm run build:dev       # Development build
```

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Library A](https://example.com) - Used for X
- [Person B](https://github.com/person) - Original idea
```

---

## Section Deep Dives

### Title and Tagline

```markdown
# Insights Copilot

Strategic intelligence platform that synthesizes insights from multiple data sources.
```

**Tips**:
- Name should be memorable and searchable
- Tagline: what it does in one sentence
- Avoid buzzwords ("revolutionary", "cutting-edge")

### Badges

```markdown
[![Build](https://img.shields.io/github/actions/workflow/status/org/repo/ci.yml)](link)
[![Coverage](https://img.shields.io/codecov/c/github/org/repo)](link)
[![npm](https://img.shields.io/npm/v/package)](link)
[![Downloads](https://img.shields.io/npm/dm/package)](link)
[![License](https://img.shields.io/badge/license-MIT-blue)](link)
```

**Common badges**:

| Badge | Shows |
|-------|-------|
| Build status | CI passing |
| Coverage | Test coverage % |
| Version | Latest npm/PyPI version |
| Downloads | Popularity |
| License | Open source license |
| TypeScript | Has type definitions |

### Overview

Answer these questions:
1. What problem does this solve?
2. Who is it for?
3. Why use this over alternatives?

```markdown
## Overview

Insights Copilot helps strategic teams discover patterns across disparate
data sources. Instead of manually reviewing assessments, research projects,
and web content, analysts can surface strategic insights automatically.

**Why Insights Copilot?**
- Consolidates evidence from 5+ source types
- AI-powered topic discovery
- Maintains evidence provenance
```

### Quick Start

Goal: Working code in <5 commands and <2 minutes reading.

```markdown
## Quick Start

```bash
# Install
npm install @insights/sdk

# Set API key
export INSIGHTS_API_KEY=your-key

# Run
npx insights discover --source assessments
```

That's it! See [Usage](#usage) for more options.
```

### Features

Scannable list with brief descriptions:

```markdown
## Features

- **Topic Discovery**: AI clusters related evidence into topics
- **Evidence Selection**: Relevance-ranked from all your sources
- **Crystallization**: Three-phase refinement into insights
- **Pinned Evidence**: Guarantee specific data points are included
- **Export**: PDF, Markdown, JSON formats
```

---

## README by Project Type

### Library/SDK

Focus on: Installation, API usage, code examples

```markdown
# @insights/sdk

JavaScript SDK for the Insights API.

## Install

```bash
npm install @insights/sdk
```

## Usage

```javascript
import { InsightsClient } from '@insights/sdk';

const client = new InsightsClient({ apiKey: 'your-key' });
const topics = await client.topics.list();
```

## API

### `client.topics.list(options?)`

Returns paginated list of topics.

```javascript
const { data, pagination } = await client.topics.list({
  limit: 20,
  status: 'active'
});
```
```

### CLI Tool

Focus on: Installation, commands, flags, examples

```markdown
# insights-cli

Command-line interface for Insights Copilot.

## Install

```bash
npm install -g @insights/cli
```

## Commands

### `insights discover`

Discover topics from sources.

```bash
insights discover --source assessments --limit 10
```

**Flags**:

| Flag | Description | Default |
|------|-------------|---------|
| `--source` | Source type | all |
| `--limit` | Max topics | 20 |
| `--format` | Output format | table |

### `insights export`

Export topics to file.

```bash
insights export topic-123 --format pdf -o report.pdf
```
```

### Web Application

Focus on: What it does, screenshots, deployment

```markdown
# Insights Copilot

Strategic intelligence platform for synthesizing insights.

![Dashboard Screenshot](./docs/images/dashboard.png)

## Features

- Topic discovery from multiple sources
- Evidence curation and pinning
- AI-powered crystallization
- Team collaboration

## Quick Start (Development)

```bash
git clone https://github.com/org/insights-copilot
cd insights-copilot
docker-compose up
```

Open http://localhost:3000

## Deployment

See [Deployment Guide](./docs/deployment.md) for production setup.
```

### Internal Tool

Focus on: Context, who uses it, support contacts

```markdown
# Insights Copilot (Internal)

Strategic intelligence platform used by the Research team.

**Owner**: @research-team
**Support**: #research-tools in Slack

## Who Uses This

- Research analysts for topic discovery
- Strategy team for insight review
- Leadership for strategic decisions

## Access

Request access via [IT Service Desk](https://servicedesk.internal).

## Quick Start

1. Log in at https://insights.internal
2. Connect your data sources (Settings > Integrations)
3. Run discovery (Topics > Discover)

## Support

- Slack: #research-tools
- Wiki: [Insights Copilot Guide](https://wiki.internal/insights)
- Issues: [Jira Board](https://jira.internal/insights)
```

---

## Writing Tips

### Good vs Bad

| Element | Bad | Good |
|---------|-----|------|
| **Tagline** | "A tool for data" | "Extract insights from customer interviews in minutes" |
| **Install** | "Install via npm" | `npm install package-name` |
| **Usage** | "Call the API" | Working code example |
| **Prerequisites** | "Node.js" | "Node.js 18+" |
| **Links** | "Click here" | "[API Documentation](./api.md)" |

### Code Examples

Always:
- Complete and runnable
- Include imports
- Show expected output
- Handle common errors

```javascript
// Good: Complete example
import { Client } from 'package';

const client = new Client({ apiKey: 'demo-key' });
const result = await client.fetch({ id: '123' });

console.log(result);
// { id: '123', name: 'Example', status: 'active' }
```

```javascript
// Bad: Incomplete
const result = client.fetch(id);
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Wall of text** | Hard to scan | Use headers, bullets, code |
| **No quick start** | Users give up | 5 commands or less to running |
| **Outdated examples** | Broken trust | Test examples in CI |
| **No badges** | Unknown quality | Add build/coverage badges |
| **Jargon heavy** | Excludes newcomers | Define terms or link to glossary |
| **Missing prerequisites** | Install fails | List exact versions |
| **Dead links** | Frustration | Check links in CI |

---

## Maintenance

### Quarterly Review

- [ ] Test all installation commands
- [ ] Verify code examples work
- [ ] Check all links
- [ ] Update version badges
- [ ] Update screenshots if UI changed

### Automated Checks

```yaml
# .github/workflows/readme.yml
name: README Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check links
        uses: lycheeverse/lychee-action@v1
        with:
          args: README.md

      - name: Test code examples
        run: |
          # Extract and test code blocks
          npm run test:readme-examples
```

---

## Checklist

Before publishing:

- [ ] Title and one-line description
- [ ] Badges (build, version, license)
- [ ] Overview explains what and why
- [ ] Quick Start in <5 commands
- [ ] Prerequisites with versions
- [ ] Code examples are complete
- [ ] Configuration documented
- [ ] Links work (test them)
- [ ] License specified
- [ ] Contributing info (if open source)

---

This skill enables compelling README files that help users understand and adopt your project quickly.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

