---
last_updated: 2026-02-25
status: active
name: changelog-management
description: Changelog writing - Keep a Changelog format, semantic versioning, release notes. Use for version history documentation.
triggers:
  files: ["**/CHANGELOG.md", "**/HISTORY.md", "**/RELEASES.md", "**/docs/releases/**"]
  keywords: ["changelog", "release notes", "version history", "semantic versioning", "breaking changes"]
allowed-tools: Read, Write, Edit
---

# Changelog Management Skill

Write clear, user-focused changelogs following Keep a Changelog format and semantic versioning principles. Help users understand what changed and how it affects them.

---

## Core Principles

### Changelog Purpose

| Goal | Description |
|------|-------------|
| **Inform users** | What changed that affects them |
| **Guide upgrades** | Breaking changes, migration steps |
| **Build trust** | Transparent development history |
| **Enable debugging** | When did behavior change? |

### Key Tenets

1. **Write for users, not developers**: Focus on impact, not implementation
2. **Be honest about breaking changes**: Don't hide them
3. **Group by type**: Added, Changed, Fixed, etc.
4. **Link to issues/PRs**: Enable traceability
5. **Keep Unreleased section**: Stage changes for next release

---


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## Keep a Changelog Format

### Standard Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description (#123)

### Changed
- Updated behavior description (#124)

## [1.2.0] - 2024-01-15

### Added
- **Feature Name**: Description of feature (#100)
- Another feature (#101)

### Changed
- Updated X to do Y (#102)

### Deprecated
- Old feature marked for removal (#103)

### Removed
- Removed obsolete feature (#104)

### Fixed
- Fixed bug in X (#105)

### Security
- Patched vulnerability in Y (#106)

## [1.1.0] - 2024-01-01

...

[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/org/repo/releases/tag/v1.1.0
```

### Change Categories

| Category | Use For | Example |
|----------|---------|---------|
| **Added** | New features, capabilities | "Add dark mode toggle" |
| **Changed** | Behavior changes (non-breaking) | "Improve search performance by 50%" |
| **Deprecated** | Features marked for removal | "Deprecate v1 API (use v2)" |
| **Removed** | Features removed | "Remove legacy export format" |
| **Fixed** | Bug fixes | "Fix crash when input empty" |
| **Security** | Vulnerability patches | "Patch XSS vulnerability" |

---

## Semantic Versioning

### Version Format: MAJOR.MINOR.PATCH

| Component | Increment When | Example |
|-----------|---------------|---------|
| **MAJOR** | Breaking changes | `1.0.0` → `2.0.0` |
| **MINOR** | New features (backward compatible) | `1.0.0` → `1.1.0` |
| **PATCH** | Bug fixes (backward compatible) | `1.0.0` → `1.0.1` |

### Breaking Change Examples

| Change | Breaking? | Why |
|--------|-----------|-----|
| Remove public API method | Yes | Existing code fails |
| Change method return type | Yes | Type contracts broken |
| Add new optional parameter | No | Existing calls still work |
| Change internal implementation | No | Public contract unchanged |
| Rename configuration key | Yes | Existing configs fail |
| Add new feature flag | No | Default maintains behavior |

### Pre-release Versions

```
1.0.0-alpha.1    # Early testing
1.0.0-beta.1     # Feature complete, testing
1.0.0-rc.1       # Release candidate
1.0.0            # Stable release
```

---

## Writing Effective Entries

### Entry Format

```markdown
- **Feature Name**: Description of what changed and user impact (#123)
```

### Good vs Bad Entries

| Bad | Good |
|-----|------|
| "Fixed bug" | "Fix crash when uploading files >10MB (#123)" |
| "Updated dependencies" | "Update to React 18 for Suspense support (#124)" |
| "Refactored code" | Don't include (internal, no user impact) |
| "Added feature" | "Add dark mode toggle in Settings > Appearance (#125)" |
| "Performance improvements" | "Reduce API response time by 40% for topic queries (#126)" |

### What NOT to Include

- Internal refactoring (no user impact)
- Test additions (unless testing-related product)
- Documentation updates (unless user-facing)
- Dependency bumps (unless security or feature-related)

### What to Always Include

- Breaking changes (prominently)
- Security fixes (with CVE if applicable)
- Deprecation notices (with timeline)
- Migration guidance for breaking changes

---

## Breaking Changes

### Highlighting Breaking Changes

```markdown
## [2.0.0] - 2024-01-15

### BREAKING CHANGES

- **API v1 removed**: Migrate to API v2 before upgrading. See [Migration Guide](./docs/migration-v2.md) (#200)
- **Node.js 16 required**: Drop support for Node.js 14 (#201)
- **Config format changed**: `settings.yaml` now uses YAML 1.2 syntax (#202)

### Added
- New v2 API with improved performance (#203)

### Removed
- API v1 endpoints (deprecated in 1.5.0) (#200)
```

### Migration Sections

For major versions, include migration guidance:

```markdown
## Upgrading to 2.0

### Breaking Changes Summary

| Change | Action Required |
|--------|-----------------|
| API v1 removed | Update all API calls to v2 |
| Config format | Run `migrate-config` tool |
| Node.js 16 | Upgrade runtime |

### Migration Steps

1. **Update API calls**
   ```diff
   - const response = await api.v1.getTopics();
   + const response = await api.v2.getTopics();
   ```

2. **Migrate configuration**
   ```bash
   npx @project/migrate-config settings.yaml
   ```

3. **Update Node.js**
   ```bash
   nvm install 16
   nvm use 16
   ```
```

---

## Release Notes vs Changelog

### Differences

| Aspect | Changelog | Release Notes |
|--------|-----------|---------------|
| **Audience** | Developers | All users |
| **Detail** | Technical | User-friendly |
| **Format** | Structured list | Narrative |
| **Location** | CHANGELOG.md | GitHub Releases, blog |

### Release Notes Template

```markdown
# Release 1.2.0

We're excited to announce version 1.2.0 with dark mode, improved
performance, and important bug fixes.

## Highlights

### Dark Mode

Toggle dark mode in Settings > Appearance. Your preference syncs
across devices.

### 40% Faster Search

We optimized our search infrastructure. Topic queries now return
in under 100ms.

## Full Changelog

See [CHANGELOG.md](./CHANGELOG.md) for complete details.

## Upgrading

```bash
npm install @project/cli@1.2.0
```

## Known Issues

- Dark mode may flicker on first load (#130)
```

---

## Automation

### Conventional Commits

Use commit messages to generate changelogs:

```
feat: add dark mode toggle (#123)
fix: resolve crash on large file upload (#124)
docs: update API documentation
chore: update dependencies
BREAKING CHANGE: remove API v1 (#125)
```

### Commit Type Mapping

| Commit Prefix | Changelog Section |
|---------------|-------------------|
| `feat:` | Added |
| `fix:` | Fixed |
| `perf:` | Changed |
| `BREAKING CHANGE:` | Breaking Changes |
| `security:` | Security |
| `deprecate:` | Deprecated |
| `revert:` | Removed (if reverting feature) |
| `docs:`, `chore:`, `test:`, `refactor:` | Not included |

### Tools

| Tool | Purpose |
|------|---------|
| **standard-version** | Auto-generate changelog from commits |
| **semantic-release** | Automated versioning and publishing |
| **release-please** | GitHub Action for releases |
| **changesets** | Monorepo changelog management |

---

## Best Practices

### DO

- [ ] Keep `[Unreleased]` section updated as you merge PRs
- [ ] Link every entry to issue/PR number
- [ ] Date every release
- [ ] Include comparison links at bottom
- [ ] Highlight breaking changes prominently
- [ ] Write from user perspective

### DON'T

- [ ] Include internal changes users don't care about
- [ ] Use vague descriptions ("fixed bugs")
- [ ] Batch many changes under one entry
- [ ] Forget to update comparison links
- [ ] Bury breaking changes in Changed section

---

## Examples by Project Type

### Library/SDK

```markdown
## [2.1.0] - 2024-01-15

### Added
- `client.batchCreate()` method for bulk operations (#234)
- TypeScript generics support for response types (#235)

### Changed
- Improve error messages with request IDs (#236)

### Fixed
- Fix memory leak in long-running connections (#237)

### Deprecated
- `client.create()` with array argument (use `batchCreate()`) (#234)
```

### Web Application

```markdown
## [1.5.0] - 2024-01-15

### Added
- Dark mode (Settings > Appearance) (#300)
- Keyboard shortcuts for common actions (#301)
- Export to PDF format (#302)

### Changed
- Redesigned dashboard with improved data visualization (#303)

### Fixed
- Fix incorrect date display in Safari (#304)
- Fix form not submitting on Enter key (#305)
```

### CLI Tool

```markdown
## [3.0.0] - 2024-01-15

### BREAKING CHANGES
- `--output` flag now requires explicit format (#400)
- Remove deprecated `--legacy` flag (#401)

### Added
- `--format json|yaml|table` flag for output formatting (#400)
- `--quiet` flag to suppress progress output (#402)

### Changed
- Improve progress bar visibility (#403)

### Fixed
- Fix crash when running without TTY (#404)
```

---

## Checklist

Before releasing:

- [ ] `[Unreleased]` section moved to new version
- [ ] Version number follows semver
- [ ] Release date added
- [ ] All entries link to issues/PRs
- [ ] Breaking changes prominently marked
- [ ] Comparison links updated
- [ ] Migration guide for breaking changes
- [ ] Security fixes have CVE references

---

This skill enables clear, consistent changelogs that help users understand what changed and how to upgrade safely.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

