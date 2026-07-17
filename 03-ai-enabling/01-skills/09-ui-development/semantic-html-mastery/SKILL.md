---
last_updated: 2026-02-25
status: active
name: semantic-html-mastery
description: HTML5 semantic elements for document structure, content sectioning, and accessibility. Use when building page layouts or reviewing HTML structure.
triggers:
  files: ["**/*.html", "**/*.jsx", "**/*.tsx", "**/components/**", "**/pages/**", "**/app/**"]
  keywords: ["semantic", "HTML5", "header", "footer", "main", "nav", "article", "section", "aside", "figure", "document structure", "landmark"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Semantic HTML Mastery

Master HTML5 semantic elements to create well-structured, accessible, and SEO-friendly web pages.

## Why Semantic HTML Matters

| Benefit | Description |
|---------|-------------|
| Accessibility | Screen readers use landmarks to navigate |
| SEO | Search engines understand content hierarchy |
| Maintainability | Code is self-documenting |
| Styling | Elements have meaning, not just appearance |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Document Structure Elements

### Page-Level Landmarks

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
</head>
<body>
  <header>
    <!-- Site header: logo, navigation, search -->
  </header>

  <nav aria-label="Main">
    <!-- Primary navigation -->
  </nav>

  <main id="main-content">
    <!-- Primary page content (one per page) -->
  </main>

  <aside>
    <!-- Complementary content: sidebar, related links -->
  </aside>

  <footer>
    <!-- Site footer: copyright, links, contact -->
  </footer>
</body>
</html>
```

### Element Reference

| Element | Purpose | Use Case |
|---------|---------|----------|
| `<header>` | Introductory content | Site header, article header |
| `<nav>` | Navigation links | Main nav, breadcrumbs, TOC |
| `<main>` | Primary content | One per page, skip link target |
| `<aside>` | Tangentially related | Sidebar, pull quotes, ads |
| `<footer>` | Closing content | Copyright, contact, sitemap |
| `<article>` | Self-contained content | Blog post, comment, widget |
| `<section>` | Thematic grouping | Chapters, tabbed content |

## Content Sectioning

### Article vs Section

```tsx
// Article: Self-contained, independently distributable
function BlogPost({ post }) {
  return (
    <article>
      <header>
        <h2>{post.title}</h2>
        <time dateTime={post.date}>{formatDate(post.date)}</time>
        <address>By {post.author}</address>
      </header>

      <p>{post.content}</p>

      <footer>
        <p>Tags: {post.tags.join(', ')}</p>
      </footer>
    </article>
  );
}

// Section: Thematic grouping within a larger context
function ProductPage({ product }) {
  return (
    <main>
      <h1>{product.name}</h1>

      <section aria-labelledby="description-heading">
        <h2 id="description-heading">Description</h2>
        <p>{product.description}</p>
      </section>

      <section aria-labelledby="specs-heading">
        <h2 id="specs-heading">Specifications</h2>
        <dl>
          {product.specs.map(spec => (
            <Fragment key={spec.name}>
              <dt>{spec.name}</dt>
              <dd>{spec.value}</dd>
            </Fragment>
          ))}
        </dl>
      </section>

      <section aria-labelledby="reviews-heading">
        <h2 id="reviews-heading">Reviews</h2>
        {product.reviews.map(review => (
          <article key={review.id}>
            <h3>{review.title}</h3>
            <p>{review.content}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
```

### Heading Hierarchy

**Rule**: One `<h1>` per page, no skipped levels.

```tsx
// Correct heading hierarchy
<main>
  <h1>Main Page Title</h1>

  <section>
    <h2>First Section</h2>
    <p>Content...</p>

    <h3>Subsection</h3>
    <p>More content...</p>

    <h3>Another Subsection</h3>
    <p>Even more...</p>
  </section>

  <section>
    <h2>Second Section</h2>
    <p>Content...</p>
  </section>
</main>

// BAD: Skipped heading level
<h1>Title</h1>
<h3>Section</h3>  // Should be h2
```

## Text Content Elements

### Lists

```tsx
// Unordered list: Items without sequence
<ul>
  <li>Feature one</li>
  <li>Feature two</li>
  <li>Feature three</li>
</ul>

// Ordered list: Sequential items
<ol>
  <li>First step</li>
  <li>Second step</li>
  <li>Third step</li>
</ol>

// Description list: Term-description pairs
<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language</dd>

  <dt>CSS</dt>
  <dd>Cascading Style Sheets</dd>

  <dt>JS</dt>
  <dd>JavaScript</dd>
</dl>

// Nested navigation
<nav aria-label="Main">
  <ul>
    <li><a href="/">Home</a></li>
    <li>
      <a href="/products">Products</a>
      <ul>
        <li><a href="/products/software">Software</a></li>
        <li><a href="/products/hardware">Hardware</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

### Quotations and Citations

```tsx
// Block quote with citation
<figure>
  <blockquote cite="https://example.com/source">
    <p>The only way to do great work is to love what you do.</p>
  </blockquote>
  <figcaption>
    — <cite>Steve Jobs</cite>, Stanford Commencement Speech
  </figcaption>
</figure>

// Inline quote
<p>As Einstein said, <q>Imagination is more important than knowledge.</q></p>

// Citation (title of work)
<p>Read <cite>The Design of Everyday Things</cite> by Don Norman.</p>
```

### Time and Address

```tsx
// Time element with machine-readable format
<time dateTime="2024-12-25">December 25, 2024</time>
<time dateTime="14:30">2:30 PM</time>
<time dateTime="2024-12-25T14:30:00">Dec 25 at 2:30 PM</time>
<time dateTime="P3D">3 days</time>

// Address for contact information
<address>
  Written by <a href="mailto:jane@example.com">Jane Doe</a>.<br />
  Visit us at: 123 Main St, City, Country
</address>
```

## Interactive Elements

### Details and Summary

```tsx
// Native collapsible content
function FAQ({ items }) {
  return (
    <div>
      {items.map(item => (
        <details key={item.id}>
          <summary>{item.question}</summary>
          <p>{item.answer}</p>
        </details>
      ))}
    </div>
  );
}

// Styled accordion
<details className="accordion-item">
  <summary className="accordion-header">
    <span>Section Title</span>
    <span className="icon" aria-hidden="true">+</span>
  </summary>
  <div className="accordion-content">
    <p>Expandable content here...</p>
  </div>
</details>
```

### Dialog (Native Modal)

```tsx
function Modal({ isOpen, onClose, title, children }) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      dialog.showModal();
    } else {
      dialog.close();
    }
  }, [isOpen]);

  return (
    <dialog ref={dialogRef} onClose={onClose}>
      <header>
        <h2>{title}</h2>
        <button onClick={onClose} aria-label="Close">×</button>
      </header>
      <div>{children}</div>
    </dialog>
  );
}
```

## Media Elements

### Figure and Figcaption

```tsx
// Image with caption
<figure>
  <img src="chart.png" alt="Sales growth chart showing 25% increase" />
  <figcaption>Figure 1: Q4 2024 Sales Growth</figcaption>
</figure>

// Code snippet with caption
<figure>
  <pre><code>{codeSnippet}</code></pre>
  <figcaption>Example: React component lifecycle</figcaption>
</figure>

// Video with caption
<figure>
  <video controls>
    <source src="demo.mp4" type="video/mp4" />
    <track kind="captions" src="captions.vtt" srclang="en" label="English" />
  </video>
  <figcaption>Product demonstration video</figcaption>
</figure>
```

### Picture Element

```tsx
// Responsive images with art direction
<picture>
  <source
    media="(min-width: 1200px)"
    srcSet="hero-large.webp"
    type="image/webp"
  />
  <source
    media="(min-width: 768px)"
    srcSet="hero-medium.webp"
    type="image/webp"
  />
  <source srcSet="hero-small.webp" type="image/webp" />
  <img
    src="hero-fallback.jpg"
    alt="Hero image description"
    loading="lazy"
  />
</picture>
```

## Text-Level Semantics

| Element | Purpose | Example |
|---------|---------|---------|
| `<strong>` | Strong importance | `<strong>Warning:</strong> Critical info` |
| `<em>` | Stress emphasis | `I <em>really</em> mean it` |
| `<mark>` | Highlighted text | `Search results: <mark>keyword</mark>` |
| `<code>` | Code fragment | `Use <code>const</code> for constants` |
| `<kbd>` | Keyboard input | `Press <kbd>Ctrl</kbd>+<kbd>C</kbd>` |
| `<samp>` | Computer output | `<samp>File not found</samp>` |
| `<var>` | Variable | `<var>x</var> = <var>y</var> + 5` |
| `<abbr>` | Abbreviation | `<abbr title="HyperText">HTML</abbr>` |
| `<dfn>` | Definition term | `<dfn>API</dfn> means Application...` |
| `<sub>` | Subscript | `H<sub>2</sub>O` |
| `<sup>` | Superscript | `E=mc<sup>2</sup>` |
| `<small>` | Side comment | `<small>Terms apply</small>` |
| `<del>` | Deleted text | `<del>$100</del> $75` |
| `<ins>` | Inserted text | `<ins>New content</ins>` |

## Common Patterns

### Card Component

```tsx
function Card({ title, description, image, link }) {
  return (
    <article className="card">
      <figure className="card-image">
        <img src={image.src} alt={image.alt} />
      </figure>
      <header className="card-header">
        <h3><a href={link}>{title}</a></h3>
      </header>
      <p className="card-body">{description}</p>
    </article>
  );
}
```

### Navigation with Skip Link

```tsx
function Layout({ children }) {
  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <header>
        <nav aria-label="Main navigation">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </nav>
      </header>

      <main id="main-content" tabIndex={-1}>
        {children}
      </main>

      <footer>
        <nav aria-label="Footer navigation">
          <ul>
            <li><a href="/privacy">Privacy</a></li>
            <li><a href="/terms">Terms</a></li>
          </ul>
        </nav>
      </footer>
    </>
  );
}
```

### Breadcrumb Navigation

```tsx
function Breadcrumbs({ items }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol>
        {items.map((item, index) => (
          <li key={item.href}>
            {index === items.length - 1 ? (
              <span aria-current="page">{item.label}</span>
            ) : (
              <a href={item.href}>{item.label}</a>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `<div>` for everything | No semantic meaning | Use appropriate elements |
| `<br>` for spacing | Misuse of element | Use CSS margins/padding |
| `<b>` instead of `<strong>` | Presentational | Use semantic elements |
| `<i>` instead of `<em>` | Presentational | Use semantic elements |
| Skipped heading levels | Confuses screen readers | Follow h1→h2→h3 order |
| Multiple `<main>` | Invalid structure | One `<main>` per page |
| `<table>` for layout | Misuse of element | Use CSS Grid/Flexbox |

## Best Practices

1. **Start with content structure**, not styling
2. **One `<main>` per page** - it's unique
3. **Every section needs a heading** (even if visually hidden)
4. **Use `aria-label` for multiple navs** - distinguish them
5. **`<article>` should make sense standalone** - could be syndicated
6. **`<section>` groups related content** - don't use for styling
7. **Test with screen reader** - verify landmark navigation works
8. **Validate HTML** - catch structural errors early

## Quick Reference

```
Document Structure:
html > head + body
body > header + nav + main + aside? + footer

Content Hierarchy:
main > article/section > header + content + footer
article = standalone content
section = themed grouping

Headings:
h1 (one per page) > h2 > h3 > h4 > h5 > h6

Lists:
ul = unordered items
ol = ordered/sequential
dl = term/definition pairs

Interactive:
details + summary = native accordion
dialog = native modal
```


## Quality Tests

### Visual Fidelity Test
- Implementation matches design within acceptable tolerance
- **PASS:** Spacing, colors, and typography match design tokens exactly
- **FAIL:** Visible deviations from design that aren't documented as intentional

### Accessibility Test
- Component is usable with keyboard-only and screen reader
- **PASS:** All interactive elements reachable by Tab, operable by Enter/Space
- **FAIL:** Mouse-only interactions or missing ARIA labels

