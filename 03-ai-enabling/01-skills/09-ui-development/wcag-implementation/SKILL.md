---
last_updated: 2026-02-25
status: active
name: wcag-implementation
description: WCAG 2.1 AA/AAA compliance implementation - perceivable, operable, understandable, robust. Use when building accessible web applications.
triggers:
  files: ["**/*.tsx", "**/*.jsx", "**/*.html", "**/components/**", "**/a11y/**"]
  keywords: ["WCAG", "accessibility", "a11y", "compliance", "AA", "AAA", "perceivable", "operable", "understandable", "robust"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# WCAG Implementation

Implement WCAG 2.1 AA compliance with practical patterns for each success criterion.

## WCAG Overview

| Level | Description | Target |
|-------|-------------|--------|
| A | Minimum accessibility | Baseline |
| AA | Standard accessibility | **Required for most** |
| AAA | Enhanced accessibility | Where feasible |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## POUR Principles

### Perceivable

Users must be able to perceive information.

#### 1.1 Text Alternatives

```tsx
// 1.1.1 Non-text Content (Level A)

// Informative image
<img
  src="chart.png"
  alt="Bar chart showing 25% revenue increase Q1 to Q4 2024"
/>

// Decorative image
<img src="divider.png" alt="" role="presentation" />

// Complex image with long description
<figure>
  <img
    src="diagram.png"
    alt="System architecture diagram"
    aria-describedby="diagram-desc"
  />
  <figcaption id="diagram-desc">
    Three-tier architecture: React frontend connects to FastAPI
    middleware, which communicates with PostgreSQL database.
  </figcaption>
</figure>

// Icon button
<button aria-label="Close dialog">
  <CloseIcon aria-hidden="true" />
</button>

// Form input with label
<label htmlFor="email">Email Address</label>
<input id="email" type="email" />
```

#### 1.3 Adaptable

```tsx
// 1.3.1 Info and Relationships (Level A)
// Structure conveyed visually must be programmatic

// Data table with proper headers
<table>
  <caption>Quarterly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Quarter</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Q1</th>
      <td>$100,000</td>
      <td>+5%</td>
    </tr>
  </tbody>
</table>

// 1.3.2 Meaningful Sequence (Level A)
// DOM order matches visual order
<div className="card">
  <h2>Title</h2>      {/* 1st in DOM, 1st visually */}
  <p>Content</p>      {/* 2nd in DOM, 2nd visually */}
  <button>Action</button> {/* 3rd in DOM, 3rd visually */}
</div>

// 1.3.5 Identify Input Purpose (Level AA)
<input
  type="text"
  autoComplete="name"  // Browser knows this is a name field
  name="name"
/>
<input
  type="email"
  autoComplete="email"
  name="email"
/>
<input
  type="tel"
  autoComplete="tel"
  name="phone"
/>
```

#### 1.4 Distinguishable

```tsx
// 1.4.1 Use of Color (Level A)
// Don't rely on color alone

// BAD: Color only indicates error
<input className={hasError ? 'border-red' : ''} />

// GOOD: Color + text + icon
<div>
  <input
    className={hasError ? 'border-red' : ''}
    aria-invalid={hasError}
    aria-describedby={hasError ? 'error-msg' : undefined}
  />
  {hasError && (
    <span id="error-msg" className="error-text">
      <ErrorIcon aria-hidden="true" />
      Email is required
    </span>
  )}
</div>

// 1.4.3 Contrast Minimum (Level AA)
// 4.5:1 for normal text, 3:1 for large text (18pt or 14pt bold)
const goodContrast = {
  text: '#333333',      // On white: 12.6:1 ✓
  background: '#ffffff',
};

const badContrast = {
  text: '#999999',      // On white: 2.8:1 ✗
  background: '#ffffff',
};

// 1.4.4 Resize Text (Level AA)
// Text must be resizable to 200% without loss of function
const styles = css`
  /* Use relative units */
  font-size: 1rem;      /* Not px */
  line-height: 1.5;     /* Unitless */
  max-width: 65ch;      /* Character-based */

  /* Don't disable zoom */
  /* BAD: <meta name="viewport" content="user-scalable=no"> */
`;

// 1.4.10 Reflow (Level AA)
// Content reflows at 320px width without horizontal scroll
const responsiveStyles = css`
  .container {
    max-width: 100%;
    padding: 1rem;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
  }
`;

// 1.4.11 Non-text Contrast (Level AA)
// UI components need 3:1 contrast
const buttonStyles = css`
  .button {
    border: 2px solid #666;  /* 3.9:1 on white ✓ */
    background: #0066cc;     /* Clear boundary */
  }

  .button:focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }
`;

// 1.4.12 Text Spacing (Level AA)
// Must work with user-applied spacing:
// - Line height: 1.5x font size
// - Paragraph spacing: 2x font size
// - Letter spacing: 0.12x font size
// - Word spacing: 0.16x font size
const textStyles = css`
  p {
    /* These are minimums - don't break if user increases */
    line-height: 1.5;
    margin-bottom: 1.5em;
  }
`;
```

### Operable

Users must be able to operate the interface.

#### 2.1 Keyboard Accessible

```tsx
// 2.1.1 Keyboard (Level A)
// All functionality available via keyboard

function InteractiveCard({ onClick, children }) {
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {children}
    </div>
  );
}

// BETTER: Just use a button
function InteractiveCard({ onClick, children }) {
  return (
    <button onClick={onClick} className="card">
      {children}
    </button>
  );
}

// 2.1.2 No Keyboard Trap (Level A)
function Modal({ isOpen, onClose, children }) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose(); // User can always escape
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true">
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

#### 2.4 Navigable

```tsx
// 2.4.1 Bypass Blocks (Level A)
function Layout({ children }) {
  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <header>
        <nav>{/* Navigation */}</nav>
      </header>
      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
    </>
  );
}

// Skip link CSS
const skipLinkStyles = css`
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    padding: 8px 16px;
    background: #000;
    color: #fff;
    z-index: 100;
  }

  .skip-link:focus {
    top: 0;
  }
`;

// 2.4.2 Page Titled (Level A)
// Every page needs unique, descriptive title
<head>
  <title>Dashboard - My Application</title>
</head>

// Dynamic title in React
useEffect(() => {
  document.title = `${pageTitle} - My Application`;
}, [pageTitle]);

// 2.4.3 Focus Order (Level A)
// Focus order matches visual/logical order
<form>
  <label htmlFor="first">First Name</label>
  <input id="first" />  {/* Tab 1 */}

  <label htmlFor="last">Last Name</label>
  <input id="last" />   {/* Tab 2 */}

  <button type="submit">Submit</button>  {/* Tab 3 */}
</form>

// 2.4.4 Link Purpose (Level A)
// Link text describes destination

// BAD
<a href="/docs">Click here</a>

// GOOD
<a href="/docs">View documentation</a>

// GOOD: Context clarifies
<p>
  Learn about our <a href="/services">consulting services</a>.
</p>

// 2.4.6 Headings and Labels (Level AA)
// Headings describe content
<h1>Account Settings</h1>
<h2>Personal Information</h2>
<h2>Security Settings</h2>
<h2>Notification Preferences</h2>

// 2.4.7 Focus Visible (Level AA)
const focusStyles = css`
  :focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }

  /* Optional: Use focus-visible for keyboard-only */
  :focus:not(:focus-visible) {
    outline: none;
  }

  :focus-visible {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }
`;
```

#### 2.5 Input Modalities

```tsx
// 2.5.1 Pointer Gestures (Level A)
// Complex gestures have simple alternatives

function Carousel({ items }) {
  const [index, setIndex] = useState(0);

  // Swipe gesture for touch users
  const handlers = useSwipeable({
    onSwipedLeft: () => setIndex(i => Math.min(i + 1, items.length - 1)),
    onSwipedRight: () => setIndex(i => Math.max(i - 1, 0)),
  });

  return (
    <div {...handlers}>
      {items[index]}
      {/* Simple alternative: buttons */}
      <button
        onClick={() => setIndex(i => Math.max(i - 1, 0))}
        aria-label="Previous slide"
      >
        ←
      </button>
      <button
        onClick={() => setIndex(i => Math.min(i + 1, items.length - 1))}
        aria-label="Next slide"
      >
        →
      </button>
    </div>
  );
}

// 2.5.3 Label in Name (Level A)
// Accessible name includes visible label

// GOOD: aria-label matches visible text
<button aria-label="Search">Search</button>

// BAD: Mismatch between visible and accessible name
<button aria-label="Find products">Search</button>

// 2.5.5 Target Size (Level AAA, recommended for AA)
// Minimum 44x44 CSS pixels
const touchTargetStyles = css`
  button, a {
    min-width: 44px;
    min-height: 44px;
    padding: 12px 16px;
  }
`;
```

### Understandable

Users must be able to understand information and operation.

#### 3.1 Readable

```tsx
// 3.1.1 Language of Page (Level A)
<html lang="en">

// 3.1.2 Language of Parts (Level AA)
<p>
  The French word <span lang="fr">bonjour</span> means hello.
</p>
```

#### 3.2 Predictable

```tsx
// 3.2.1 On Focus (Level A)
// Focus doesn't cause unexpected changes

// BAD: Auto-submits on focus
<select onFocus={() => submit()}>

// GOOD: Submit button required
<select value={value} onChange={setValue}>
  <option>Option 1</option>
</select>
<button onClick={submit}>Apply</button>

// 3.2.2 On Input (Level A)
// Input doesn't cause unexpected changes

// BAD: Auto-navigates on selection
<select onChange={(e) => navigate(e.target.value)}>

// GOOD: Explicit action required
<select value={destination} onChange={setDestination}>
  <option value="/page1">Page 1</option>
  <option value="/page2">Page 2</option>
</select>
<button onClick={() => navigate(destination)}>Go</button>

// 3.2.3 Consistent Navigation (Level AA)
// Navigation appears in same order across pages
function Navigation() {
  return (
    <nav aria-label="Main">
      <ul>
        <li><a href="/">Home</a></li>      {/* Always 1st */}
        <li><a href="/about">About</a></li> {/* Always 2nd */}
        <li><a href="/contact">Contact</a></li> {/* Always 3rd */}
      </ul>
    </nav>
  );
}

// 3.2.4 Consistent Identification (Level AA)
// Same functionality = same label
<button aria-label="Search">🔍</button>  {/* Same everywhere */}
```

#### 3.3 Input Assistance

```tsx
// 3.3.1 Error Identification (Level A)
function FormField({ error, children }) {
  return (
    <div>
      {children}
      {error && (
        <span role="alert" className="error">
          {error}
        </span>
      )}
    </div>
  );
}

// 3.3.2 Labels or Instructions (Level A)
<form>
  <label htmlFor="email">
    Email Address
    <span className="required" aria-label="required">*</span>
  </label>
  <input
    id="email"
    type="email"
    required
    aria-describedby="email-hint"
  />
  <span id="email-hint" className="hint">
    We'll send a confirmation to this address
  </span>
</form>

// 3.3.3 Error Suggestion (Level AA)
function validateEmail(email: string): string | null {
  if (!email) return 'Email is required';
  if (!email.includes('@')) return 'Please include @ in the email address';
  return null;
}

// 3.3.4 Error Prevention (Level AA)
// For legal/financial: review before submit
function CheckoutForm() {
  const [showReview, setShowReview] = useState(false);

  if (showReview) {
    return (
      <div>
        <h2>Review Your Order</h2>
        {/* Show all entered data */}
        <button onClick={submit}>Confirm Purchase</button>
        <button onClick={() => setShowReview(false)}>Edit</button>
      </div>
    );
  }

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      setShowReview(true);
    }}>
      {/* Form fields */}
      <button type="submit">Review Order</button>
    </form>
  );
}
```

### Robust

Content must be robust enough for assistive technologies.

#### 4.1 Compatible

```tsx
// 4.1.1 Parsing (Level A)
// Valid HTML: unique IDs, proper nesting, closed tags
// React handles most of this, but watch for:

// BAD: Duplicate IDs
<label htmlFor="name">Name</label>
<input id="name" />
<label htmlFor="name">Other</label>  {/* Duplicate! */}
<input id="name" />

// GOOD: Unique IDs
<label htmlFor="first-name">First Name</label>
<input id="first-name" />
<label htmlFor="last-name">Last Name</label>
<input id="last-name" />

// 4.1.2 Name, Role, Value (Level A)
// Custom components expose correct semantics

// Custom checkbox
function Checkbox({ checked, onChange, label }) {
  return (
    <div
      role="checkbox"
      aria-checked={checked}
      tabIndex={0}
      onClick={() => onChange(!checked)}
      onKeyDown={(e) => {
        if (e.key === ' ') {
          e.preventDefault();
          onChange(!checked);
        }
      }}
    >
      {label}
    </div>
  );
}

// Custom combobox
function Combobox({ value, options, onChange, label }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <label id="combo-label">{label}</label>
      <button
        role="combobox"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-labelledby="combo-label"
        aria-controls="combo-listbox"
        onClick={() => setIsOpen(!isOpen)}
      >
        {value || 'Select...'}
      </button>
      {isOpen && (
        <ul id="combo-listbox" role="listbox">
          {options.map(opt => (
            <li
              key={opt.value}
              role="option"
              aria-selected={value === opt.value}
              onClick={() => {
                onChange(opt.value);
                setIsOpen(false);
              }}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// 4.1.3 Status Messages (Level AA)
// Status messages announced without focus

function SearchResults({ count, isSearching }) {
  return (
    <div role="status" aria-live="polite" aria-atomic="true">
      {isSearching ? 'Searching...' : `Found ${count} results`}
    </div>
  );
}

function FormSubmit({ status }) {
  return (
    <>
      <button type="submit">Submit</button>
      <div role="status" aria-live="polite">
        {status === 'submitting' && 'Submitting...'}
        {status === 'success' && 'Form submitted successfully'}
        {status === 'error' && 'Submission failed. Please try again.'}
      </div>
    </>
  );
}
```

## WCAG AA Checklist

### Perceivable

- [ ] 1.1.1 Non-text content has text alternatives
- [ ] 1.2.1 Captions for prerecorded audio
- [ ] 1.2.2 Captions for prerecorded video
- [ ] 1.2.3 Audio description or text alternative
- [ ] 1.2.5 Audio description for video
- [ ] 1.3.1 Info and relationships programmatic
- [ ] 1.3.2 Meaningful sequence preserved
- [ ] 1.3.3 Instructions not sensory-only
- [ ] 1.3.4 Orientation not restricted
- [ ] 1.3.5 Input purpose identified
- [ ] 1.4.1 Color not sole indicator
- [ ] 1.4.2 Audio control available
- [ ] 1.4.3 Contrast ratio 4.5:1 (normal), 3:1 (large)
- [ ] 1.4.4 Text resizable to 200%
- [ ] 1.4.5 Images of text avoided
- [ ] 1.4.10 Reflow at 320px width
- [ ] 1.4.11 Non-text contrast 3:1
- [ ] 1.4.12 Text spacing adjustable
- [ ] 1.4.13 Hover/focus content dismissible

### Operable

- [ ] 2.1.1 Keyboard accessible
- [ ] 2.1.2 No keyboard trap
- [ ] 2.1.4 Character key shortcuts
- [ ] 2.2.1 Timing adjustable
- [ ] 2.2.2 Pause/stop/hide moving content
- [ ] 2.3.1 No flashing content (3/sec)
- [ ] 2.4.1 Skip blocks mechanism
- [ ] 2.4.2 Page titled
- [ ] 2.4.3 Focus order logical
- [ ] 2.4.4 Link purpose clear
- [ ] 2.4.5 Multiple ways to find pages
- [ ] 2.4.6 Headings and labels descriptive
- [ ] 2.4.7 Focus visible
- [ ] 2.5.1 Pointer gestures have alternatives
- [ ] 2.5.2 Pointer cancellation available
- [ ] 2.5.3 Label in accessible name
- [ ] 2.5.4 Motion actuation has alternatives

### Understandable

- [ ] 3.1.1 Language of page declared
- [ ] 3.1.2 Language of parts declared
- [ ] 3.2.1 On focus doesn't change context
- [ ] 3.2.2 On input doesn't change context
- [ ] 3.2.3 Consistent navigation
- [ ] 3.2.4 Consistent identification
- [ ] 3.3.1 Error identification
- [ ] 3.3.2 Labels or instructions
- [ ] 3.3.3 Error suggestion
- [ ] 3.3.4 Error prevention (legal/financial)

### Robust

- [ ] 4.1.1 Valid markup (no duplicate IDs)
- [ ] 4.1.2 Name, role, value for components
- [ ] 4.1.3 Status messages announced

## Testing Tools

| Tool | Type | Purpose |
|------|------|---------|
| axe DevTools | Browser extension | Automated testing |
| WAVE | Browser extension | Visual indicators |
| Lighthouse | Chrome DevTools | Audit reports |
| NVDA | Screen reader | Manual testing (Windows) |
| VoiceOver | Screen reader | Manual testing (Mac) |
| Colour Contrast Analyser | Desktop app | Contrast checking |
| ANDI | Bookmarklet | Section 508 testing |

## Quick Reference

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| Text alternatives | A | All non-text content |
| Color contrast | AA | 4.5:1 normal, 3:1 large |
| Keyboard access | A | All functionality |
| Focus visible | AA | Clear focus indicator |
| Skip links | A | Bypass repeated content |
| Page titles | A | Descriptive, unique |
| Error messages | A | Identify the error |
| Error suggestions | AA | How to fix it |
| Language | A | Declare page language |
| Status messages | AA | Announce without focus |


## Quality Tests

### Visual Fidelity Test
- Implementation matches design within acceptable tolerance
- **PASS:** Spacing, colors, and typography match design tokens exactly
- **FAIL:** Visible deviations from design that aren't documented as intentional

### Accessibility Test
- Component is usable with keyboard-only and screen reader
- **PASS:** All interactive elements reachable by Tab, operable by Enter/Space
- **FAIL:** Mouse-only interactions or missing ARIA labels

