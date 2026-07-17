---
last_updated: 2026-02-25
status: active
name: accessibility-patterns
description: WCAG 2.1 AA compliance - ARIA, keyboard navigation, screen readers, focus management. Use for accessible UI.
triggers:
  files: ["**/components/**/*.tsx", "**/components/**/*.jsx", "**/a11y/**"]
  keywords: ["accessibility", "a11y", "WCAG", "ARIA", "screen reader", "keyboard", "focus", "alt text", "semantic HTML"]
allowed-tools: Read, Write, Edit
---

# Accessibility Patterns

Comprehensive guide to building WCAG 2.1 AA compliant web applications with proper ARIA, keyboard navigation, screen reader support, and focus management.

## Table of Contents

1. [WCAG 2.1 Principles](#wcag-21-principles)
2. [Semantic HTML](#semantic-html)
3. [ARIA Roles, States, and Properties](#aria-roles-states-and-properties)
4. [Keyboard Navigation](#keyboard-navigation)
5. [Focus Management](#focus-management)
6. [Screen Reader Compatibility](#screen-reader-compatibility)
7. [Color and Contrast](#color-and-contrast)
8. [Form Accessibility](#form-accessibility)
9. [Table Accessibility](#table-accessibility)
10. [Dynamic Content](#dynamic-content)
11. [Testing Tools and Techniques](#testing-tools-and-techniques)
12. [Common Violations and Fixes](#common-violations-and-fixes)

---


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## WCAG 2.1 Principles

WCAG 2.1 is organized around four principles (POUR):

### Perceivable

Users must be able to perceive the information being presented.

**Key Guidelines:**
- Provide text alternatives for non-text content
- Provide captions and alternatives for multimedia
- Create content that can be presented in different ways without losing meaning
- Make it easier for users to see and hear content

**AA Requirements:**
- Color contrast ratio of at least 4.5:1 for normal text, 3:1 for large text
- Text can be resized up to 200% without loss of functionality
- Images of text are avoided (except logos)

### Operable

Users must be able to operate the interface.

**Key Guidelines:**
- Make all functionality available from a keyboard
- Give users enough time to read and use content
- Do not design content that causes seizures
- Provide ways to help users navigate and find content

**AA Requirements:**
- No keyboard trap
- Skip links provided for repetitive content
- Page titles that describe topic or purpose
- Focus order that preserves meaning and operability
- Link purpose clear from context

### Understandable

Users must be able to understand the information and operation of the interface.

**Key Guidelines:**
- Make text readable and understandable
- Make content appear and operate in predictable ways
- Help users avoid and correct mistakes

**AA Requirements:**
- Language of page is programmatically determined
- Navigation is consistent across pages
- Labels or instructions provided for user input
- Error identification, suggestions, and prevention for critical actions

### Robust

Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

**Key Guidelines:**
- Maximize compatibility with current and future user agents

**AA Requirements:**
- Valid HTML with proper parsing
- Name, role, and value available for all UI components

---

## Semantic HTML

Semantic HTML is the foundation of accessibility. Use elements for their intended purpose.

### Document Structure

```tsx
// GOOD: Proper semantic structure
export function Page() {
  return (
    <>
      <header>
        <nav aria-label="Main navigation">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
          </ul>
        </nav>
      </header>

      <main id="main-content">
        <h1>Page Title</h1>

        <section aria-labelledby="intro-heading">
          <h2 id="intro-heading">Introduction</h2>
          <p>Content here...</p>
        </section>

        <article>
          <h2>Article Title</h2>
          <p>Article content...</p>
        </article>

        <aside aria-label="Related information">
          <h2>Sidebar</h2>
          <p>Additional content...</p>
        </aside>
      </main>

      <footer>
        <p>&copy; 2024 Company Name</p>
      </footer>
    </>
  );
}

// BAD: Generic divs without semantic meaning
export function BadPage() {
  return (
    <div className="container">
      <div className="header">
        <div className="nav">
          <div className="nav-item">Home</div>
        </div>
      </div>
      <div className="content">
        <div className="title">Page Title</div>
      </div>
    </div>
  );
}
```

### Heading Hierarchy

```tsx
// GOOD: Logical heading hierarchy
export function Article() {
  return (
    <article>
      <h1>Main Article Title</h1>

      <section>
        <h2>First Section</h2>
        <p>Content...</p>

        <h3>Subsection</h3>
        <p>More content...</p>
      </section>

      <section>
        <h2>Second Section</h2>
        <p>Content...</p>
      </section>
    </article>
  );
}

// BAD: Skipped heading levels
export function BadArticle() {
  return (
    <div>
      <h1>Title</h1>
      <h4>Subsection</h4> {/* Skipped h2 and h3 */}
      <h2>Out of order</h2> {/* Heading levels go backwards */}
    </div>
  );
}
```

### Lists

```tsx
// GOOD: Semantic lists
export function Navigation() {
  return (
    <nav aria-label="Primary">
      <ul>
        <li><a href="/home">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li>
          <a href="/services">Services</a>
          <ul>
            <li><a href="/services/consulting">Consulting</a></li>
            <li><a href="/services/training">Training</a></li>
          </ul>
        </li>
      </ul>
    </nav>
  );
}

export function Steps() {
  return (
    <ol>
      <li>First step</li>
      <li>Second step</li>
      <li>Third step</li>
    </ol>
  );
}

export function Features() {
  return (
    <dl>
      <dt>Feature Name</dt>
      <dd>Feature description and details</dd>

      <dt>Another Feature</dt>
      <dd>Another description</dd>
    </dl>
  );
}
```

### Buttons vs Links

```tsx
// GOOD: Buttons for actions, links for navigation
export function ButtonsAndLinks() {
  return (
    <>
      {/* Button triggers an action on the current page */}
      <button onClick={handleSubmit}>Submit Form</button>
      <button onClick={handleToggle}>Toggle Menu</button>

      {/* Link navigates to a different page/section */}
      <a href="/contact">Contact Us</a>
      <a href="#section">Jump to Section</a>
    </>
  );
}

// BAD: Wrong elements for purpose
export function BadButtonsAndLinks() {
  return (
    <>
      {/* Don't use div/span as buttons */}
      <div onClick={handleSubmit}>Submit</div>

      {/* Don't use links with onClick for actions */}
      <a href="#" onClick={handleAction}>Do Something</a>

      {/* Don't style buttons to look like links for navigation */}
      <button onClick={() => navigate('/page')}>Go to Page</button>
    </>
  );
}
```

---

## ARIA Roles, States, and Properties

ARIA (Accessible Rich Internet Applications) supplements HTML to communicate roles, states, and properties to assistive technologies.

### The First Rule of ARIA

**"No ARIA is better than bad ARIA."**

If you can use a native HTML element or attribute, do that instead.

```tsx
// GOOD: Native HTML
<button>Click me</button>

// BAD: Unnecessary ARIA
<div role="button" tabIndex={0} onClick={handleClick}>Click me</div>
```

### Common ARIA Roles

```tsx
// Landmark Roles (use sparingly, prefer semantic HTML)
<nav role="navigation" aria-label="Main">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<header role="banner">...</header>
<footer role="contentinfo">...</footer>

// Widget Roles
export function TabWidget() {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div>
      <div role="tablist" aria-label="Sample Tabs">
        <button
          role="tab"
          aria-selected={activeTab === 0}
          aria-controls="panel-1"
          id="tab-1"
          tabIndex={activeTab === 0 ? 0 : -1}
          onClick={() => setActiveTab(0)}
        >
          Tab 1
        </button>
        <button
          role="tab"
          aria-selected={activeTab === 1}
          aria-controls="panel-2"
          id="tab-2"
          tabIndex={activeTab === 1 ? 0 : -1}
          onClick={() => setActiveTab(1)}
        >
          Tab 2
        </button>
      </div>

      <div
        role="tabpanel"
        id="panel-1"
        aria-labelledby="tab-1"
        hidden={activeTab !== 0}
      >
        Content for tab 1
      </div>
      <div
        role="tabpanel"
        id="panel-2"
        aria-labelledby="tab-2"
        hidden={activeTab !== 1}
      >
        Content for tab 2
      </div>
    </div>
  );
}

// Dialog Role
export function Dialog({ isOpen, onClose, title, children }) {
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen && dialogRef.current) {
      dialogRef.current.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
      ref={dialogRef}
      tabIndex={-1}
    >
      <h2 id="dialog-title">{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}

// Alert Role
export function Alert({ message, type = 'info' }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      className={`alert-${type}`}
    >
      {message}
    </div>
  );
}
```

### ARIA States and Properties

```tsx
// aria-expanded (for collapsible content)
export function Accordion({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);
  const contentId = useId();

  return (
    <div>
      <button
        aria-expanded={isOpen}
        aria-controls={contentId}
        onClick={() => setIsOpen(!isOpen)}
      >
        {title}
      </button>
      <div id={contentId} hidden={!isOpen}>
        {children}
      </div>
    </div>
  );
}

// aria-checked (for custom checkboxes)
export function CustomCheckbox({ checked, onChange, label }) {
  return (
    <div
      role="checkbox"
      aria-checked={checked}
      tabIndex={0}
      onClick={() => onChange(!checked)}
      onKeyDown={(e) => {
        if (e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          onChange(!checked);
        }
      }}
    >
      {label}
    </div>
  );
}

// aria-disabled vs disabled
export function DisabledStates() {
  return (
    <>
      {/* Use 'disabled' for form elements */}
      <button disabled>Native Disabled</button>
      <input type="text" disabled />

      {/* Use aria-disabled when element needs to remain focusable */}
      <button aria-disabled="true" onClick={(e) => e.preventDefault()}>
        ARIA Disabled (still focusable)
      </button>
    </>
  );
}

// aria-current (for current page/step)
export function Breadcrumbs({ items }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol>
        {items.map((item, index) => (
          <li key={item.href}>
            <a
              href={item.href}
              aria-current={index === items.length - 1 ? 'page' : undefined}
            >
              {item.label}
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}

// aria-describedby (for additional descriptions)
export function InputWithHelp() {
  const helpId = useId();

  return (
    <div>
      <label htmlFor="username">Username</label>
      <input
        id="username"
        type="text"
        aria-describedby={helpId}
      />
      <span id={helpId}>Must be 3-20 characters</span>
    </div>
  );
}

// aria-invalid and aria-errormessage
export function InputWithError({ error }) {
  const errorId = useId();

  return (
    <div>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        aria-invalid={!!error}
        aria-errormessage={error ? errorId : undefined}
      />
      {error && (
        <span id={errorId} role="alert">
          {error}
        </span>
      )}
    </div>
  );
}

// aria-hidden (hide decorative elements)
export function IconButton({ icon, label }) {
  return (
    <button aria-label={label}>
      <svg aria-hidden="true" focusable="false">
        {icon}
      </svg>
      <span className="sr-only">{label}</span>
    </button>
  );
}
```

### ARIA Live Regions

```tsx
// Polite updates (non-critical)
export function StatusMessage({ message }) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      {message}
    </div>
  );
}

// Assertive updates (critical)
export function ErrorAlert({ error }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      {error}
    </div>
  );
}

// Dynamic loading indicator
export function LoadingIndicator({ isLoading, label = 'Loading' }) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-busy={isLoading}
    >
      {isLoading && (
        <>
          <span className="spinner" aria-hidden="true" />
          <span className="sr-only">{label}</span>
        </>
      )}
    </div>
  );
}

// Search results count
export function SearchResults({ count, isSearching }) {
  return (
    <>
      <div role="status" aria-live="polite" aria-atomic="true">
        {!isSearching && count !== null && (
          <span>Found {count} results</span>
        )}
      </div>
      {/* Results content */}
    </>
  );
}
```

---

## Keyboard Navigation

All interactive elements must be keyboard accessible.

### Tab Order and tabIndex

```tsx
// GOOD: Natural tab order
export function Form() {
  return (
    <form>
      <input type="text" placeholder="First" />
      <input type="text" placeholder="Second" />
      <button type="submit">Submit</button>
    </form>
  );
}

// tabIndex values:
// tabIndex={0}  - Element in natural tab order
// tabIndex={-1} - Element programmatically focusable, not in tab order
// tabIndex={1+} - AVOID: Disrupts natural tab order

// GOOD: Managing tab order in widgets
export function Menu({ items }) {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <ul role="menu">
      {items.map((item, index) => (
        <li
          key={item.id}
          role="menuitem"
          tabIndex={index === activeIndex ? 0 : -1}
          onClick={() => handleItemClick(item)}
        >
          {item.label}
        </li>
      ))}
    </ul>
  );
}
```

### Keyboard Event Handlers

```tsx
// Standard keyboard interactions
export function KeyboardHandlers() {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Enter':
      case ' ': // Space bar
        e.preventDefault();
        handleActivate();
        break;
      case 'Escape':
        handleClose();
        break;
      case 'ArrowUp':
        e.preventDefault();
        handleNavigateUp();
        break;
      case 'ArrowDown':
        e.preventDefault();
        handleNavigateDown();
        break;
      case 'Home':
        e.preventDefault();
        handleNavigateFirst();
        break;
      case 'End':
        e.preventDefault();
        handleNavigateLast();
        break;
    }
  };

  return (
    <div onKeyDown={handleKeyDown} tabIndex={0}>
      Content
    </div>
  );
}

// Custom button
export function CustomButton({ onClick, children }) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick(e);
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}
```

### Skip Links

```tsx
// Provide skip links for repetitive content
export function Layout({ children }) {
  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <a href="#search" className="skip-link">
        Skip to search
      </a>

      <header>
        <nav>...</nav>
      </header>

      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
    </>
  );
}

// CSS for skip links
const styles = `
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px;
    text-decoration: none;
    z-index: 100;
  }

  .skip-link:focus {
    top: 0;
  }
`;
```

### Roving tabIndex Pattern

```tsx
// For toolbar, menu, listbox, etc.
export function Toolbar({ items }) {
  const [focusedIndex, setFocusedIndex] = useState(0);
  const itemRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let newIndex = index;

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
        e.preventDefault();
        newIndex = (index + 1) % items.length;
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        newIndex = (index - 1 + items.length) % items.length;
        break;
      case 'Home':
        e.preventDefault();
        newIndex = 0;
        break;
      case 'End':
        e.preventDefault();
        newIndex = items.length - 1;
        break;
      default:
        return;
    }

    setFocusedIndex(newIndex);
    itemRefs.current[newIndex]?.focus();
  };

  return (
    <div role="toolbar" aria-label="Formatting options">
      {items.map((item, index) => (
        <button
          key={item.id}
          ref={(el) => (itemRefs.current[index] = el)}
          tabIndex={index === focusedIndex ? 0 : -1}
          onClick={() => item.onClick()}
          onKeyDown={(e) => handleKeyDown(e, index)}
          aria-label={item.label}
        >
          {item.icon}
        </button>
      ))}
    </div>
  );
}
```

---

## Focus Management

Proper focus management ensures users know where they are and can navigate efficiently.

### Focus Indicators

```tsx
// ALWAYS provide visible focus indicators
const styles = `
  /* Default focus style (use outline, not border) */
  button:focus,
  a:focus,
  input:focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }

  /* Enhanced focus style */
  .button:focus-visible {
    outline: 3px solid #0066cc;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.2);
  }

  /* NEVER remove focus without replacement */
  /* BAD */
  *:focus {
    outline: none;
  }
`;
```

### Focus Trapping in Modals

```tsx
export function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  // Trap focus within modal
  useEffect(() => {
    if (!isOpen) return;

    // Store previously focused element
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus first focusable element in modal
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements?.length) {
      (focusableElements[0] as HTMLElement).focus();
    }

    // Handle Tab key
    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab' || !modalRef.current) return;

      const focusableElements = Array.from(
        modalRef.current.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
      ) as HTMLElement[];

      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];

      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    };

    document.addEventListener('keydown', handleTab);

    return () => {
      document.removeEventListener('keydown', handleTab);
      // Restore focus when modal closes
      previousFocusRef.current?.focus();
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      ref={modalRef}
      onKeyDown={(e) => {
        if (e.key === 'Escape') {
          onClose();
        }
      }}
    >
      {children}
    </div>
  );
}
```

### Managing Focus After Actions

```tsx
// After deleting an item, move focus to appropriate element
export function ListWithDelete({ items, onDelete }) {
  const itemRefs = useRef<Map<string, HTMLElement>>(new Map());

  const handleDelete = (itemId: string, index: number) => {
    onDelete(itemId);

    // Focus next item, or previous if last item deleted
    const nextIndex = index < items.length - 1 ? index : index - 1;
    if (nextIndex >= 0) {
      const nextItemId = items[nextIndex].id;
      setTimeout(() => {
        itemRefs.current.get(nextItemId)?.focus();
      }, 0);
    }
  };

  return (
    <ul>
      {items.map((item, index) => (
        <li key={item.id}>
          <span>{item.name}</span>
          <button
            ref={(el) => el && itemRefs.current.set(item.id, el)}
            onClick={() => handleDelete(item.id, index)}
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}

// After form submission, focus first error or success message
export function Form() {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const successRef = useRef<HTMLDivElement>(null);
  const firstErrorRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      // Focus first error
      setTimeout(() => {
        firstErrorRef.current?.focus();
      }, 0);
    } else {
      // Submit successful
      await submitForm();
      // Focus success message
      setTimeout(() => {
        successRef.current?.focus();
      }, 0);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <div role="alert" ref={successRef} tabIndex={-1}>
        Form submitted successfully
      </div>
    </form>
  );
}
```

### Programmatic Focus

```tsx
// Focus management hook
export function useFocusManagement() {
  const elementRef = useRef<HTMLElement>(null);

  const setFocus = useCallback(() => {
    elementRef.current?.focus();
  }, []);

  return { elementRef, setFocus };
}

// Usage
export function ExpandableSection({ title, children }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const { elementRef, setFocus } = useFocusManagement();

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
    if (!isExpanded) {
      // Focus content when expanding
      setTimeout(setFocus, 0);
    }
  };

  return (
    <div>
      <button
        aria-expanded={isExpanded}
        onClick={handleToggle}
      >
        {title}
      </button>
      {isExpanded && (
        <div ref={elementRef} tabIndex={-1}>
          {children}
        </div>
      )}
    </div>
  );
}
```

---

## Screen Reader Compatibility

Ensure content is properly announced by screen readers.

### Screen Reader Only Text

```tsx
// CSS class for screen reader only content
const styles = `
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }

  .sr-only-focusable:focus {
    position: static;
    width: auto;
    height: auto;
    padding: inherit;
    margin: inherit;
    overflow: visible;
    clip: auto;
    white-space: normal;
  }
`;

// Usage examples
export function ScreenReaderText() {
  return (
    <>
      {/* Icon with screen reader label */}
      <button aria-label="Close dialog">
        <svg aria-hidden="true">...</svg>
        <span className="sr-only">Close</span>
      </button>

      {/* Additional context */}
      <a href="/profile">
        John Doe
        <span className="sr-only">(current user)</span>
      </a>

      {/* Status information */}
      <div>
        <span className="badge">3</span>
        <span className="sr-only">unread messages</span>
      </div>
    </>
  );
}
```

### Accessible Names and Descriptions

```tsx
// Various ways to provide accessible names
export function AccessibleNames() {
  return (
    <>
      {/* 1. aria-label (direct label) */}
      <button aria-label="Close dialog">
        <CloseIcon />
      </button>

      {/* 2. aria-labelledby (reference label element) */}
      <section aria-labelledby="section-heading">
        <h2 id="section-heading">Products</h2>
        {/* content */}
      </section>

      {/* 3. Native label element */}
      <label htmlFor="email">Email Address</label>
      <input id="email" type="email" />

      {/* 4. aria-describedby (additional description) */}
      <input
        aria-label="Search"
        aria-describedby="search-help"
        type="text"
      />
      <span id="search-help">
        Enter keywords to search
      </span>

      {/* 5. title attribute (last resort) */}
      <iframe title="Google Maps" src="..." />
    </>
  );
}
```

### Images and Alternative Text

```tsx
export function Images() {
  return (
    <>
      {/* Informative images */}
      <img
        src="chart.png"
        alt="Bar chart showing 25% increase in sales from Q1 to Q2"
      />

      {/* Functional images (in links/buttons) */}
      <a href="/home">
        <img src="logo.png" alt="Company Name Home" />
      </a>

      {/* Decorative images */}
      <img src="decorative-border.png" alt="" />
      {/* OR */}
      <img src="decorative-border.png" role="presentation" />

      {/* Complex images */}
      <figure>
        <img
          src="complex-diagram.png"
          alt="System architecture diagram"
          aria-describedby="diagram-description"
        />
        <figcaption id="diagram-description">
          The system consists of three layers: presentation layer
          with React frontend, business logic layer with FastAPI
          backend, and data layer with PostgreSQL database.
        </figcaption>
      </figure>

      {/* SVG images */}
      <svg role="img" aria-labelledby="svg-title">
        <title id="svg-title">Growth trend arrow pointing up</title>
        <path d="..." />
      </svg>

      {/* Icon fonts (decorative) */}
      <i className="icon-star" aria-hidden="true" />
      <span className="sr-only">Favorite</span>
    </>
  );
}
```

### Dynamic Content Announcements

```tsx
// Announce changes to screen reader users
export function NotificationSystem() {
  const [notifications, setNotifications] = useState<string[]>([]);

  return (
    <>
      {/* Live region for announcements */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {notifications[notifications.length - 1]}
      </div>

      {/* Visible notifications */}
      <div className="notification-list">
        {notifications.map((msg, i) => (
          <div key={i}>{msg}</div>
        ))}
      </div>
    </>
  );
}

// Loading states
export function LoadingContent() {
  const [isLoading, setIsLoading] = useState(true);

  return (
    <>
      {isLoading ? (
        <div
          role="status"
          aria-live="polite"
          aria-label="Loading content"
        >
          <span aria-hidden="true">Loading...</span>
        </div>
      ) : (
        <div>
          <h2>Content</h2>
          {/* content here */}
        </div>
      )}
    </>
  );
}
```

---

## Color and Contrast

Ensure sufficient color contrast and don't rely on color alone.

### Contrast Ratios (WCAG AA)

```tsx
// Minimum contrast ratios:
// - Normal text: 4.5:1
// - Large text (18pt+ or 14pt+ bold): 3:1
// - UI components and graphics: 3:1

// GOOD: Sufficient contrast
const styles = `
  .text-primary {
    color: #1a1a1a;        /* Text */
    background: #ffffff;    /* Background */
    /* Contrast ratio: 18.5:1 ✓ */
  }

  .button-primary {
    color: #ffffff;
    background: #0066cc;
    /* Contrast ratio: 4.6:1 ✓ */
  }

  .link-text {
    color: #0052a3;         /* On white background */
    /* Contrast ratio: 5.5:1 ✓ */
  }
`;

// BAD: Insufficient contrast
const badStyles = `
  .text-gray {
    color: #999999;         /* Text */
    background: #ffffff;    /* Background */
    /* Contrast ratio: 2.8:1 ✗ */
  }

  .button-light {
    color: #ffffff;
    background: #90caf9;
    /* Contrast ratio: 1.9:1 ✗ */
  }
`;
```

### Color as Information

```tsx
// DON'T rely on color alone
export function BadStatusIndicator({ status }) {
  return (
    <span className={`status-${status}`}>
      {/* Color only - inaccessible */}
    </span>
  );
}

// DO provide text or icons in addition to color
export function GoodStatusIndicator({ status }) {
  const statusInfo = {
    success: { icon: CheckIcon, label: 'Success' },
    error: { icon: ErrorIcon, label: 'Error' },
    warning: { icon: WarningIcon, label: 'Warning' },
  };

  const { icon: Icon, label } = statusInfo[status];

  return (
    <span className={`status-${status}`}>
      <Icon aria-hidden="true" />
      <span>{label}</span>
    </span>
  );
}

// Form validation with multiple indicators
export function InputWithValidation({ error, success }) {
  return (
    <div>
      <input
        className={error ? 'error' : success ? 'success' : ''}
        aria-invalid={!!error}
        aria-describedby={error ? 'error-msg' : undefined}
      />
      {error && (
        <span id="error-msg" className="error-message">
          <ErrorIcon aria-hidden="true" />
          {error}
        </span>
      )}
      {success && (
        <span className="success-message">
          <CheckIcon aria-hidden="true" />
          Input valid
        </span>
      )}
    </div>
  );
}
```

### High Contrast Mode Support

```tsx
// Support Windows High Contrast Mode
const styles = `
  /* Use currentColor for borders/icons */
  .button {
    border: 2px solid currentColor;
  }

  .icon {
    fill: currentColor;
  }

  /* Provide focus indicators that work in high contrast */
  button:focus {
    outline: 2px solid transparent;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px currentColor;
  }

  /* Test with forced-colors media query */
  @media (forced-colors: active) {
    .custom-checkbox {
      forced-color-adjust: none;
      border: 2px solid CanvasText;
    }
  }
`;
```

---

## Form Accessibility

Forms are critical for user interaction and must be fully accessible.

### Labels and Instructions

```tsx
export function AccessibleForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form onSubmit={handleSubmit}>
      {/* Basic label */}
      <div>
        <label htmlFor="name">Full Name</label>
        <input id="name" type="text" required />
      </div>

      {/* Label with help text */}
      <div>
        <label htmlFor="email">Email Address</label>
        <input
          id="email"
          type="email"
          aria-describedby="email-help"
          required
        />
        <span id="email-help" className="help-text">
          We'll never share your email
        </span>
      </div>

      {/* Label with error */}
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : 'password-help'}
          required
        />
        <span id="password-help" className="help-text">
          Must be at least 8 characters
        </span>
        {errors.password && (
          <span id="password-error" role="alert" className="error">
            {errors.password}
          </span>
        )}
      </div>

      {/* Radio group */}
      <fieldset>
        <legend>Subscription Type</legend>
        <div>
          <input
            type="radio"
            id="monthly"
            name="subscription"
            value="monthly"
          />
          <label htmlFor="monthly">Monthly ($10/mo)</label>
        </div>
        <div>
          <input
            type="radio"
            id="yearly"
            name="subscription"
            value="yearly"
          />
          <label htmlFor="yearly">Yearly ($100/yr)</label>
        </div>
      </fieldset>

      {/* Checkbox group */}
      <fieldset>
        <legend>Interests</legend>
        <div>
          <input type="checkbox" id="tech" value="tech" />
          <label htmlFor="tech">Technology</label>
        </div>
        <div>
          <input type="checkbox" id="design" value="design" />
          <label htmlFor="design">Design</label>
        </div>
      </fieldset>

      {/* Required field indicator */}
      <p>
        <abbr title="required" aria-label="required">*</abbr>
        indicates required field
      </p>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Error Handling

```tsx
export function FormWithErrors() {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const errorSummaryRef = useRef<HTMLDivElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors = validateForm();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);

      // Focus error summary
      setTimeout(() => {
        errorSummaryRef.current?.focus();
      }, 0);
    } else {
      // Submit form
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Error summary at top of form */}
      {Object.keys(errors).length > 0 && (
        <div
          ref={errorSummaryRef}
          role="alert"
          aria-labelledby="error-summary-title"
          tabIndex={-1}
          className="error-summary"
        >
          <h2 id="error-summary-title">
            There {Object.keys(errors).length === 1 ? 'is' : 'are'}{' '}
            {Object.keys(errors).length} error
            {Object.keys(errors).length === 1 ? '' : 's'} in this form
          </h2>
          <ul>
            {Object.entries(errors).map(([field, error]) => (
              <li key={field}>
                <a href={`#${field}`}>{error}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Form fields with inline errors */}
      <div>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          type="text"
          aria-invalid={!!errors.username}
          aria-describedby={errors.username ? 'username-error' : undefined}
        />
        {errors.username && (
          <span id="username-error" role="alert" className="error">
            {errors.username}
          </span>
        )}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Custom Form Controls

```tsx
// Accessible custom select
export function CustomSelect({ options, value, onChange, label }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const listboxRef = useRef<HTMLUListElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (isOpen) {
          setActiveIndex((activeIndex + 1) % options.length);
        } else {
          setIsOpen(true);
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (isOpen) {
          setActiveIndex((activeIndex - 1 + options.length) % options.length);
        }
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen) {
          onChange(options[activeIndex].value);
          setIsOpen(false);
        } else {
          setIsOpen(true);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        break;
    }
  };

  return (
    <div className="custom-select">
      <label id="select-label">{label}</label>
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-labelledby="select-label"
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
      >
        {options.find(opt => opt.value === value)?.label || 'Select...'}
      </button>

      {isOpen && (
        <ul
          ref={listboxRef}
          role="listbox"
          aria-labelledby="select-label"
        >
          {options.map((option, index) => (
            <li
              key={option.value}
              role="option"
              aria-selected={option.value === value}
              className={index === activeIndex ? 'active' : ''}
              onClick={() => {
                onChange(option.value);
                setIsOpen(false);
              }}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

## Table Accessibility

Tables must clearly indicate headers and relationships.

### Data Tables

```tsx
export function AccessibleDataTable({ data }) {
  return (
    <table>
      <caption>Quarterly Sales Report 2024</caption>
      <thead>
        <tr>
          <th scope="col">Quarter</th>
          <th scope="col">Revenue</th>
          <th scope="col">Expenses</th>
          <th scope="col">Profit</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr key={row.quarter}>
            <th scope="row">{row.quarter}</th>
            <td>{row.revenue}</td>
            <td>{row.expenses}</td>
            <td>{row.profit}</td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr>
          <th scope="row">Total</th>
          <td>{totalRevenue}</td>
          <td>{totalExpenses}</td>
          <td>{totalProfit}</td>
        </tr>
      </tfoot>
    </table>
  );
}

// Complex table with multiple header levels
export function ComplexTable() {
  return (
    <table>
      <caption>Sales by Region and Product</caption>
      <thead>
        <tr>
          <th scope="col" rowSpan={2}>Product</th>
          <th scope="colgroup" colSpan={3}>Regions</th>
        </tr>
        <tr>
          <th scope="col">North</th>
          <th scope="col">South</th>
          <th scope="col">West</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Product A</th>
          <td>$100</td>
          <td>$150</td>
          <td>$200</td>
        </tr>
      </tbody>
    </table>
  );
}
```

### Sortable Tables

```tsx
export function SortableTable({ columns, data, onSort, sortConfig }) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((column) => (
            <th key={column.key} scope="col">
              <button
                onClick={() => onSort(column.key)}
                aria-label={`Sort by ${column.label}`}
                aria-sort={
                  sortConfig.key === column.key
                    ? sortConfig.direction === 'asc'
                      ? 'ascending'
                      : 'descending'
                    : 'none'
                }
              >
                {column.label}
                {sortConfig.key === column.key && (
                  <span aria-hidden="true">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </button>
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {columns.map((column) => (
              <td key={column.key}>{row[column.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Responsive Tables

```tsx
export function ResponsiveTable({ data }) {
  return (
    <>
      {/* Mobile: Transform to key-value pairs */}
      <div className="mobile-table" role="table">
        {data.map((item) => (
          <div key={item.id} role="rowgroup">
            <div role="row">
              <span role="columnheader">Name:</span>
              <span role="cell">{item.name}</span>
            </div>
            <div role="row">
              <span role="columnheader">Email:</span>
              <span role="cell">{item.email}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Desktop: Regular table */}
      <table className="desktop-table">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
```

---

## Dynamic Content

Handle dynamic updates accessibly.

### Single Page Applications

```tsx
// Announce route changes
export function RouteAnnouncer() {
  const location = useLocation();
  const [announcement, setAnnouncement] = useState('');

  useEffect(() => {
    // Get page title or heading for announcement
    const pageTitle = document.title;
    setAnnouncement(`Navigated to ${pageTitle}`);
  }, [location]);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {announcement}
    </div>
  );
}

// Focus management on route change
export function RouteLayout({ children }) {
  const mainRef = useRef<HTMLElement>(null);
  const location = useLocation();

  useEffect(() => {
    // Focus main content on route change
    mainRef.current?.focus();
  }, [location]);

  return (
    <main ref={mainRef} tabIndex={-1} id="main-content">
      {children}
    </main>
  );
}
```

### Loading States

```tsx
export function AsyncContent({ isLoading, error, data }) {
  if (isLoading) {
    return (
      <div
        role="status"
        aria-live="polite"
        aria-busy="true"
        aria-label="Loading content"
      >
        <div className="spinner" aria-hidden="true" />
        <span className="sr-only">Loading content, please wait</span>
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" aria-live="assertive">
        <p>Error loading content: {error.message}</p>
        <button onClick={retry}>Try Again</button>
      </div>
    );
  }

  return <div>{/* Render data */}</div>;
}
```

### Infinite Scroll

```tsx
export function InfiniteScrollList({ items, loadMore, hasMore }) {
  const observerRef = useRef<HTMLDivElement>(null);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoadingMore) {
          setIsLoadingMore(true);
          loadMore().finally(() => setIsLoadingMore(false));
        }
      },
      { threshold: 0.1 }
    );

    if (observerRef.current) {
      observer.observe(observerRef.current);
    }

    return () => observer.disconnect();
  }, [hasMore, isLoadingMore, loadMore]);

  return (
    <div>
      <ul aria-label="Search results">
        {items.map((item) => (
          <li key={item.id}>{item.title}</li>
        ))}
      </ul>

      {/* Loading indicator */}
      <div ref={observerRef} role="status" aria-live="polite">
        {isLoadingMore && (
          <span>Loading more items...</span>
        )}
        {!hasMore && (
          <span>No more items to load</span>
        )}
      </div>

      {/* Manual load button as fallback */}
      {hasMore && (
        <button
          onClick={() => loadMore()}
          disabled={isLoadingMore}
        >
          Load More
        </button>
      )}
    </div>
  );
}
```

---

## Testing Tools and Techniques

### Automated Testing Tools

```bash
# Browser extensions
- axe DevTools (Chrome/Firefox)
- WAVE (Chrome/Firefox)
- Lighthouse (Chrome DevTools)

# Command line
npm install -g @axe-core/cli
axe https://example.com

# In tests
npm install --save-dev @axe-core/react jest-axe
```

### Testing with jest-axe

```tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('Button should not have accessibility violations', async () => {
  const { container } = render(<button>Click me</button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

test('Form should be accessible', async () => {
  const { container } = render(
    <form>
      <label htmlFor="name">Name</label>
      <input id="name" type="text" />
    </form>
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

```
Keyboard Testing:
- [ ] Can reach all interactive elements with Tab
- [ ] Tab order is logical
- [ ] Can activate elements with Enter/Space
- [ ] Can close modals with Escape
- [ ] No keyboard trap
- [ ] Focus indicator always visible

Screen Reader Testing:
- [ ] Test with NVDA (Windows), JAWS (Windows), VoiceOver (Mac/iOS), TalkBack (Android)
- [ ] All images have alt text
- [ ] Forms have proper labels
- [ ] Headings are in logical order
- [ ] Dynamic content is announced
- [ ] Error messages are announced

Visual Testing:
- [ ] Text has sufficient contrast
- [ ] Focus indicators are visible
- [ ] Information not conveyed by color alone
- [ ] Works in high contrast mode
- [ ] Text can zoom to 200%

Mobile Testing:
- [ ] Touch targets at least 44x44 CSS pixels
- [ ] Works in portrait and landscape
- [ ] No horizontal scrolling at 320px width
- [ ] Gestures have alternatives
```

### Screen Reader Testing Commands

```
NVDA (Windows):
- Turn on: Ctrl + Alt + N
- Read next: Down Arrow
- Read previous: Up Arrow
- Navigate headings: H
- Navigate links: K
- Navigate form fields: F
- Elements list: Insert + F7

VoiceOver (Mac):
- Turn on: Cmd + F5
- Start reading: VO + A
- Next item: VO + Right Arrow
- Previous item: VO + Left Arrow
- Navigate headings: VO + Cmd + H
- Rotor menu: VO + U

JAWS (Windows):
- Start reading: Insert + Down Arrow
- Next heading: H
- Next link: Tab
- Next form field: F
- Elements list: Insert + F3
```

---

## Common Violations and Fixes

### Missing Alternative Text

```tsx
// VIOLATION
<img src="logo.png" />

// FIX
<img src="logo.png" alt="Company Name" />

// OR (decorative image)
<img src="decorative.png" alt="" />
```

### Low Color Contrast

```tsx
// VIOLATION
const styles = `
  .text {
    color: #999;  /* Light gray */
    background: #fff;
    /* Contrast ratio: 2.8:1 */
  }
`;

// FIX
const styles = `
  .text {
    color: #666;  /* Darker gray */
    background: #fff;
    /* Contrast ratio: 5.7:1 ✓ */
  }
`;
```

### Missing Form Labels

```tsx
// VIOLATION
<input type="text" placeholder="Enter name" />

// FIX
<>
  <label htmlFor="name">Name</label>
  <input id="name" type="text" placeholder="Enter name" />
</>

// OR (if label not visible)
<input
  type="text"
  aria-label="Name"
  placeholder="Enter name"
/>
```

### Empty Links and Buttons

```tsx
// VIOLATION
<a href="/profile">
  <img src="avatar.png" />
</a>

// FIX
<a href="/profile">
  <img src="avatar.png" alt="View profile" />
</a>

// OR
<a href="/profile" aria-label="View profile">
  <img src="avatar.png" alt="" />
</a>
```

### Missing Heading Hierarchy

```tsx
// VIOLATION
<div>
  <h1>Page Title</h1>
  <h3>Section</h3>  {/* Skipped h2 */}
</div>

// FIX
<div>
  <h1>Page Title</h1>
  <h2>Section</h2>
</div>
```

### Non-Descriptive Link Text

```tsx
// VIOLATION
<p>
  To learn more about our services,
  <a href="/services">click here</a>.
</p>

// FIX
<p>
  <a href="/services">Learn more about our services</a>.
</p>

// OR
<p>
  To learn more about our services,
  <a href="/services">
    view our services page
  </a>.
</p>
```

### Keyboard Inaccessibility

```tsx
// VIOLATION
<div onClick={handleClick}>Click me</div>

// FIX
<button onClick={handleClick}>Click me</button>

// OR (if div required)
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Click me
</div>
```

### Missing Language Attribute

```tsx
// VIOLATION
<html>
  <head>...</head>
  <body>...</body>
</html>

// FIX
<html lang="en">
  <head>...</head>
  <body>...</body>
</html>

// For content in different language
<blockquote lang="es">
  <p>Hola mundo</p>
</blockquote>
```

### Inaccessible Modal

```tsx
// VIOLATION
<div className="modal">
  <h2>Modal Title</h2>
  <p>Content</p>
  <button onClick={closeModal}>Close</button>
</div>

// FIX
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  ref={modalRef}
  tabIndex={-1}
>
  <h2 id="modal-title">Modal Title</h2>
  <p>Content</p>
  <button onClick={closeModal}>Close</button>
</div>
```

### Missing ARIA Properties

```tsx
// VIOLATION: Accordion without ARIA
<button onClick={toggle}>Section</button>
<div>{content}</div>

// FIX
<button
  aria-expanded={isOpen}
  aria-controls="content-1"
  onClick={toggle}
>
  Section
</button>
<div id="content-1" hidden={!isOpen}>
  {content}
</div>
```

---

## Quick Reference

### WCAG 2.1 AA Checklist

```
Perceivable:
- [ ] Text alternatives for images
- [ ] Captions for videos
- [ ] Content adaptable to different presentations
- [ ] Color contrast ratio ≥ 4.5:1 (normal text)
- [ ] Color contrast ratio ≥ 3:1 (large text)
- [ ] Text resizable to 200%

Operable:
- [ ] All functionality keyboard accessible
- [ ] No keyboard trap
- [ ] Skip links for navigation
- [ ] Page titles descriptive
- [ ] Focus order logical
- [ ] Link purpose clear

Understandable:
- [ ] Language of page identified
- [ ] Navigation consistent
- [ ] Form labels provided
- [ ] Error identification
- [ ] Error suggestions provided

Robust:
- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Name, role, value for components
```

### Essential ARIA Patterns

| Pattern | Key Attributes | Keyboard |
|---------|----------------|----------|
| Button | `role="button"` | Enter, Space |
| Checkbox | `role="checkbox"` `aria-checked` | Space |
| Tabs | `role="tablist/tab/tabpanel"` `aria-selected` | Arrow keys |
| Accordion | `aria-expanded` `aria-controls` | Enter, Space |
| Dialog | `role="dialog"` `aria-modal` `aria-labelledby` | Escape |
| Menu | `role="menu/menuitem"` | Arrow keys, Enter |
| Alert | `role="alert"` `aria-live="assertive"` | N/A |

### Browser + Screen Reader Combinations

| OS | Browser | Screen Reader |
|----|---------|---------------|
| Windows | Firefox | NVDA (free) |
| Windows | Chrome/Edge | JAWS (paid) |
| macOS | Safari | VoiceOver (built-in) |
| iOS | Safari | VoiceOver (built-in) |
| Android | Chrome | TalkBack (built-in) |

---

## Conclusion

Accessibility is not optional—it's a fundamental requirement for inclusive web applications. By following WCAG 2.1 AA guidelines, using semantic HTML, implementing proper ARIA, ensuring keyboard accessibility, and managing focus correctly, you create applications that work for everyone.

Remember:
1. Use semantic HTML first
2. Test with keyboard only
3. Test with screen readers
4. Verify color contrast
5. Provide text alternatives
6. Manage focus properly
7. Announce dynamic changes
8. Test with real users

Accessibility is an ongoing practice, not a one-time fix. Integrate these patterns into your development workflow from the start.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

