---
last_updated: 2026-02-25
status: active
name: accessibility-first-design
description: Design with accessibility as a foundation - inclusive design principles that benefit all users. Use for universal design and WCAG compliance.
triggers:
  files: ["**/a11y/**", "**/accessibility/**", "**/wcag/**", "**/aria/**"]
  keywords: ["accessibility", "a11y", "wcag", "aria", "screen reader", "keyboard", "inclusive", "universal design", "assistive technology"]
allowed-tools: Read, Write, Edit
---

# Accessibility-First Design Skill

Master guide for designing interfaces that work for everyone - treating accessibility as a fundamental design principle, not an afterthought.

## Philosophy

**Accessibility is usability.** Designing for accessibility improves the experience for all users, not just those with disabilities.

**Design for the edges.** When you design for users with the greatest constraints, everyone benefits.

**Disability is a spectrum.** Permanent, temporary, and situational disabilities affect everyone at some point. A broken arm, bright sunlight, or loud environment creates similar needs to permanent conditions.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Understanding Disabilities

### Disability Categories

| Category | Permanent | Temporary | Situational |
|----------|-----------|-----------|-------------|
| **Visual** | Blind, low vision | Eye surgery recovery | Bright sunlight |
| **Motor** | Paralysis, tremor | Broken arm | Holding baby |
| **Auditory** | Deaf, hard of hearing | Ear infection | Loud environment |
| **Cognitive** | Learning disability | Concussion | Stress, distraction |
| **Speech** | Mute, stutter | Laryngitis | Heavy accent |

### Assistive Technologies

| Technology | Users | Design Impact |
|------------|-------|---------------|
| Screen readers | Blind users | Semantic HTML, alt text |
| Screen magnifiers | Low vision | Scalable UI, contrast |
| Switch devices | Motor disabilities | Keyboard navigation |
| Voice control | Various | Voice commands |
| Captions | Deaf/HoH | Video/audio transcription |

---

## WCAG Guidelines

### The Four Principles (POUR)

| Principle | Meaning | Example |
|-----------|---------|---------|
| **Perceivable** | Can users perceive the content? | Alt text for images |
| **Operable** | Can users operate the interface? | Keyboard navigation |
| **Understandable** | Can users understand the content? | Clear language |
| **Robust** | Does it work with assistive tech? | Semantic HTML |

### Conformance Levels

| Level | Meaning | Typical Requirement |
|-------|---------|---------------------|
| **A** | Minimum | Legal minimum |
| **AA** | Standard | Most common target |
| **AAA** | Enhanced | Specialized contexts |

---

## Visual Design

### Color Contrast

**WCAG Requirements**:

| Element | AA (Normal) | AA (Large) | AAA |
|---------|-------------|------------|-----|
| Text | 4.5:1 | 3:1 | 7:1 |
| UI Components | 3:1 | 3:1 | N/A |

```css
/* Good contrast examples */
.text-primary {
  color: #1a1a1a; /* On white: 16:1 */
}

.text-secondary {
  color: #595959; /* On white: 7:1 */
}

.text-muted {
  color: #767676; /* On white: 4.5:1 - minimum */
}
```

### Color Independence

Never rely on color alone:

```
❌ Bad: Color only
Red = error, Green = success

✅ Good: Color + icon + text
⚠ Error: Please enter a valid email
✓ Success: Your changes have been saved
```

### Focus Indicators

Visible focus for keyboard navigation:

```css
/* Visible focus ring */
:focus {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}

/* Remove only if custom focus */
:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

### Text Sizing

Allow text scaling:

```css
/* Use relative units */
body {
  font-size: 100%; /* Respects user settings */
}

h1 {
  font-size: 2rem; /* Scales with base */
}

p {
  font-size: 1rem;
  line-height: 1.5;
}

/* DON'T use fixed sizes */
p {
  font-size: 14px; /* Won't scale with user preferences */
}
```

---

## Semantic HTML

### Document Structure

```html
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/products">Products</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Page Title</h1>
    <section>
      <h2>Section Title</h2>
      <p>Content...</p>
    </section>
  </article>
</main>

<aside aria-label="Related content">
  <h2>Related Articles</h2>
</aside>

<footer>
  <nav aria-label="Footer navigation">...</nav>
</footer>
```

### Heading Hierarchy

```html
<!-- Correct hierarchy -->
<h1>Page Title</h1>
  <h2>Main Section</h2>
    <h3>Subsection</h3>
    <h3>Subsection</h3>
  <h2>Another Section</h2>
    <h3>Subsection</h3>

<!-- Never skip levels -->
❌ <h1>Title</h1>
❌ <h3>Jumped to h3</h3>
```

### Form Labels

```html
<!-- Explicit label association -->
<label for="email">Email address</label>
<input type="email" id="email" name="email">

<!-- Implicit association -->
<label>
  Email address
  <input type="email" name="email">
</label>

<!-- Never use placeholder as label -->
❌ <input type="email" placeholder="Email">
```

### Button vs Link

```html
<!-- Button: Performs action -->
<button type="button" onclick="doSomething()">
  Save Changes
</button>

<!-- Link: Navigates somewhere -->
<a href="/settings">
  Go to Settings
</a>

<!-- NEVER make divs clickable -->
❌ <div onclick="doSomething()">Click me</div>
```

---

## Keyboard Navigation

### Focus Order

Follow visual reading order:

```
Tab order:
[1] Logo/Home link
[2] Navigation items (left to right)
[3] Main content
[4] Sidebar
[5] Footer
```

```css
/* Tab order should match visual order */
/* Avoid negative tabindex except for programmatic focus */

.visually-hidden-but-focusable {
  position: absolute;
  left: -10000px;
}

.visually-hidden-but-focusable:focus {
  position: static;
}
```

### Skip Links

Allow users to skip repetitive navigation:

```html
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<nav>
  <!-- Long navigation -->
</nav>

<main id="main-content" tabindex="-1">
  <!-- Main content -->
</main>
```

```css
.skip-link {
  position: absolute;
  left: -10000px;
}

.skip-link:focus {
  position: fixed;
  top: 0;
  left: 0;
  background: white;
  padding: 1rem;
  z-index: 9999;
}
```

### Keyboard Patterns

| Element | Expected Keyboard Behavior |
|---------|---------------------------|
| Button | Enter/Space activates |
| Link | Enter activates |
| Checkbox | Space toggles |
| Radio | Arrows navigate, Space selects |
| Select | Arrows navigate, Enter selects |
| Tab panel | Arrows switch tabs |
| Modal | Escape closes, Tab traps focus |

---

## ARIA

### When to Use ARIA

**First rule: Don't use ARIA if native HTML works.**

```html
<!-- Prefer native HTML -->
<button>Click me</button>

<!-- Only if necessary -->
<div role="button" tabindex="0"
     onkeydown="handleKeyDown(event)">
  Click me
</div>
```

### Common ARIA Patterns

**Live regions** (dynamic content):
```html
<div aria-live="polite" aria-atomic="true">
  <!-- Announce changes to screen readers -->
  Your message has been sent.
</div>

<div aria-live="assertive" role="alert">
  <!-- Interrupt immediately for errors -->
  Error: Session expired.
</div>
```

**Labeling**:
```html
<!-- aria-label for elements without visible label -->
<button aria-label="Close dialog">×</button>

<!-- aria-labelledby for referencing another element -->
<h2 id="dialog-title">Settings</h2>
<div role="dialog" aria-labelledby="dialog-title">
  ...
</div>

<!-- aria-describedby for additional description -->
<input aria-describedby="email-help">
<p id="email-help">We'll never share your email.</p>
```

**States**:
```html
<button aria-expanded="false" aria-controls="menu">
  Menu
</button>
<ul id="menu" hidden>
  <li>Item 1</li>
</ul>

<input aria-invalid="true" aria-errormessage="email-error">
<span id="email-error">Please enter a valid email</span>
```

---

## Images and Media

### Alt Text

```html
<!-- Informative image: Describe content -->
<img src="chart.png"
     alt="Sales increased 40% from Q1 to Q2">

<!-- Decorative image: Empty alt -->
<img src="decorative.png" alt="">

<!-- Complex image: Link to description -->
<img src="complex-diagram.png"
     alt="System architecture diagram"
     aria-describedby="diagram-desc">
<p id="diagram-desc" class="sr-only">
  Full description of the diagram...
</p>
```

### Video Accessibility

```html
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt"
         srclang="en" label="English">
  <track kind="descriptions" src="desc.vtt"
         srclang="en" label="Audio descriptions">
</video>
```

### Audio Accessibility

```html
<!-- Provide transcript -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
<details>
  <summary>Read transcript</summary>
  <p>Full transcript of audio...</p>
</details>
```

---

## Motion and Animation

### Reduced Motion

```css
/* Default animation */
.animated {
  animation: slide-in 0.3s ease-out;
}

/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
  .animated {
    animation: none;
    transition: none;
  }

  /* Or provide subtle alternative */
  .animated {
    animation: fade-in 0.1s ease-out;
  }
}
```

### Safe Animation Practices

- Avoid flashing (> 3 flashes per second)
- Allow pause/stop for moving content
- Provide reduced motion alternative
- Don't auto-play videos

---

## Forms

### Form Best Practices

```html
<form>
  <fieldset>
    <legend>Personal Information</legend>

    <div class="field">
      <label for="name">Full name *</label>
      <input type="text" id="name" required
             aria-describedby="name-hint">
      <p id="name-hint" class="hint">
        As it appears on your ID
      </p>
    </div>

    <div class="field">
      <label for="email">Email *</label>
      <input type="email" id="email" required
             aria-invalid="false">
      <p class="error" role="alert" hidden>
        Please enter a valid email
      </p>
    </div>
  </fieldset>

  <button type="submit">Submit</button>
</form>
```

### Error Handling

```html
<!-- Error summary at top -->
<div role="alert" aria-labelledby="error-summary">
  <h2 id="error-summary">2 errors found</h2>
  <ul>
    <li><a href="#email">Email is required</a></li>
    <li><a href="#password">Password too short</a></li>
  </ul>
</div>

<!-- Inline errors -->
<label for="email">Email *</label>
<input type="email" id="email"
       aria-invalid="true"
       aria-describedby="email-error">
<p id="email-error" class="error">
  Please enter a valid email address
</p>
```

---

## Testing

### Automated Testing

```javascript
// Using axe-core
import { axe } from 'axe-core';

const results = await axe.run(document);
console.log(results.violations);
```

### Manual Testing Checklist

| Test | Method |
|------|--------|
| Keyboard only | Unplug mouse, navigate with keyboard |
| Screen reader | VoiceOver (Mac), NVDA (Windows) |
| Zoom | Zoom to 200%, check layout |
| Color contrast | Use browser dev tools |
| Color blindness | Use simulation tools |
| Reduced motion | Enable in OS settings |

### Common Tools

| Tool | Purpose |
|------|---------|
| axe DevTools | Browser extension for testing |
| WAVE | Web accessibility evaluation |
| Lighthouse | Accessibility audits |
| Color Contrast Checker | Verify contrast ratios |
| Screen reader | Real assistive tech testing |

---

## Anti-Patterns

### 1. Placeholder as Label

```html
❌ Bad:
<input placeholder="Enter your email">

✅ Good:
<label for="email">Email</label>
<input id="email" placeholder="you@example.com">
```

### 2. Color-Only Information

```
❌ Bad: "Required fields are in red"
✅ Good: "Required fields are marked with *"
```

### 3. Auto-Playing Media

```html
❌ Bad:
<video autoplay>

✅ Good:
<video controls>
```

### 4. Focus Traps

```
❌ Bad: Modal that can't be escaped
✅ Good: Modal with Escape key and close button
```

### 5. Images of Text

```
❌ Bad: <img src="welcome.png" alt="Welcome">
✅ Good: <h1>Welcome</h1>
```

### 6. Missing Form Labels

```html
❌ Bad:
<input type="email">

✅ Good:
<label for="email">Email</label>
<input type="email" id="email">
```

---

## Quick Reference

### Accessibility Checklist

**Perceivable**
- [ ] Alt text for images
- [ ] Captions for video
- [ ] Color contrast ≥ 4.5:1
- [ ] Color not only indicator
- [ ] Text resizable to 200%

**Operable**
- [ ] All functionality via keyboard
- [ ] Focus visible
- [ ] Skip links present
- [ ] No keyboard traps
- [ ] Adequate time limits

**Understandable**
- [ ] Labels on form fields
- [ ] Error messages helpful
- [ ] Consistent navigation
- [ ] Clear language

**Robust**
- [ ] Valid HTML
- [ ] Semantic markup
- [ ] ARIA used correctly
- [ ] Works with assistive tech

### Quick Wins

1. Add alt text to all images
2. Use semantic HTML elements
3. Ensure sufficient color contrast
4. Add visible focus indicators
5. Label all form fields
6. Test with keyboard only

---

## Summary

**Accessibility is not extra work - it's good design.**

1. Use semantic HTML first
2. Ensure keyboard accessibility
3. Maintain sufficient contrast
4. Never rely on color alone
5. Provide text alternatives
6. Test with real assistive tech

*When you design for everyone, you design better for everyone.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

