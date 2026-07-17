---
last_updated: 2026-02-25
status: active
name: aria-implementation
description: ARIA roles, states, and properties for custom UI components. Use when building accessible interactive widgets.
triggers:
  files: ["**/*.tsx", "**/*.jsx", "**/components/**", "**/ui/**"]
  keywords: ["ARIA", "aria-", "role", "accessibility", "screen reader", "assistive technology", "widget", "landmark", "live region"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# ARIA Implementation

Implement ARIA (Accessible Rich Internet Applications) correctly for custom UI components.

## The First Rule of ARIA

**"No ARIA is better than bad ARIA."**

| Approach | When to Use |
|----------|-------------|
| Native HTML | Always prefer semantic elements |
| ARIA | Only when native elements insufficient |

```tsx
// GOOD: Use native element
<button onClick={handleClick}>Submit</button>

// BAD: Unnecessary ARIA
<div role="button" tabIndex={0} onClick={handleClick}>Submit</div>
```


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## ARIA Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| Roles | Define what element is | `button`, `dialog`, `tab` |
| States | Current condition | `aria-expanded`, `aria-selected` |
| Properties | Characteristics | `aria-label`, `aria-describedby` |

## Landmark Roles

Landmarks define page structure for screen reader navigation.

```tsx
function PageLayout() {
  return (
    <>
      <header role="banner">
        <nav role="navigation" aria-label="Main">
          {/* Primary navigation */}
        </nav>
      </header>

      <main role="main">
        {/* Primary content */}
      </main>

      <aside role="complementary" aria-label="Related content">
        {/* Sidebar */}
      </aside>

      <footer role="contentinfo">
        {/* Footer content */}
      </footer>
    </>
  );
}
```

| Role | HTML Equivalent | Purpose |
|------|-----------------|---------|
| `banner` | `<header>` | Site header |
| `navigation` | `<nav>` | Navigation links |
| `main` | `<main>` | Primary content |
| `complementary` | `<aside>` | Supporting content |
| `contentinfo` | `<footer>` | Footer information |
| `search` | None | Search functionality |
| `form` | `<form>` (with name) | Form region |
| `region` | `<section>` (with name) | Generic landmark |

**Note**: HTML5 elements have implicit roles. Add explicit roles only when needed for older AT.

## Widget Roles

### Buttons

```tsx
// Standard button - use native element
<button onClick={handleClick}>Click me</button>

// Toggle button
function ToggleButton({ pressed, onClick, children }) {
  return (
    <button
      aria-pressed={pressed}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

// Menu button
function MenuButton({ options }) {
  const [isOpen, setIsOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);

  return (
    <div>
      <button
        ref={buttonRef}
        aria-haspopup="menu"
        aria-expanded={isOpen}
        aria-controls="dropdown-menu"
        onClick={() => setIsOpen(!isOpen)}
      >
        Options
      </button>
      {isOpen && (
        <ul id="dropdown-menu" role="menu">
          {options.map(opt => (
            <li key={opt.id} role="menuitem">
              <button onClick={opt.action}>{opt.label}</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Tabs

```tsx
function Tabs({ tabs, defaultTab }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  const tabRefs = useRef<Map<string, HTMLButtonElement>>(new Map());

  const handleKeyDown = (e: React.KeyboardEvent, tabId: string) => {
    const tabIds = tabs.map(t => t.id);
    const currentIndex = tabIds.indexOf(tabId);
    let nextIndex: number;

    switch (e.key) {
      case 'ArrowRight':
        nextIndex = (currentIndex + 1) % tabIds.length;
        break;
      case 'ArrowLeft':
        nextIndex = (currentIndex - 1 + tabIds.length) % tabIds.length;
        break;
      case 'Home':
        nextIndex = 0;
        break;
      case 'End':
        nextIndex = tabIds.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    const nextId = tabIds[nextIndex];
    setActiveTab(nextId);
    tabRefs.current.get(nextId)?.focus();
  };

  return (
    <div>
      <div role="tablist" aria-label="Content tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            ref={el => el && tabRefs.current.set(tab.id, el)}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            aria-controls={`panel-${tab.id}`}
            tabIndex={activeTab === tab.id ? 0 : -1}
            onClick={() => setActiveTab(tab.id)}
            onKeyDown={(e) => handleKeyDown(e, tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map(tab => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== tab.id}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

### Dialog (Modal)

```tsx
function Dialog({ isOpen, onClose, title, children }) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
      dialogRef.current?.focus();

      // Prevent body scroll
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.body.style.overflow = '';
      previousFocusRef.current?.focus();
    };
  }, [isOpen]);

  // Focus trap
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
        return;
      }

      if (e.key !== 'Tab') return;

      const focusable = dialogRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ) as NodeListOf<HTMLElement>;

      if (!focusable?.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="dialog-backdrop"
        aria-hidden="true"
        onClick={onClose}
      />

      {/* Dialog */}
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
        aria-describedby="dialog-description"
        tabIndex={-1}
        className="dialog"
      >
        <header>
          <h2 id="dialog-title">{title}</h2>
          <button
            onClick={onClose}
            aria-label="Close dialog"
          >
            ×
          </button>
        </header>

        <div id="dialog-description">
          {children}
        </div>

        <footer>
          <button onClick={onClose}>Cancel</button>
          <button onClick={handleConfirm}>Confirm</button>
        </footer>
      </div>
    </>
  );
}
```

### Alert Dialog

```tsx
function AlertDialog({ isOpen, onClose, onConfirm, title, message }) {
  return (
    <div
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="alert-title"
      aria-describedby="alert-message"
      hidden={!isOpen}
    >
      <h2 id="alert-title">{title}</h2>
      <p id="alert-message">{message}</p>
      <button onClick={onClose}>Cancel</button>
      <button onClick={onConfirm}>Confirm</button>
    </div>
  );
}
```

### Accordion

```tsx
function Accordion({ items }) {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setExpandedIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <div>
      {items.map(item => {
        const isExpanded = expandedIds.has(item.id);
        const headerId = `accordion-header-${item.id}`;
        const panelId = `accordion-panel-${item.id}`;

        return (
          <div key={item.id}>
            <h3>
              <button
                id={headerId}
                aria-expanded={isExpanded}
                aria-controls={panelId}
                onClick={() => toggle(item.id)}
              >
                {item.title}
                <span aria-hidden="true">{isExpanded ? '−' : '+'}</span>
              </button>
            </h3>
            <div
              id={panelId}
              role="region"
              aria-labelledby={headerId}
              hidden={!isExpanded}
            >
              {item.content}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

### Combobox (Autocomplete)

```tsx
function Combobox({ options, value, onChange, label }) {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState(value);
  const [activeIndex, setActiveIndex] = useState(-1);
  const listboxId = useId();

  const filteredOptions = options.filter(opt =>
    opt.label.toLowerCase().includes(inputValue.toLowerCase())
  );

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(i => Math.min(i + 1, filteredOptions.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex(i => Math.max(i - 1, 0));
        break;
      case 'Enter':
        if (activeIndex >= 0 && filteredOptions[activeIndex]) {
          e.preventDefault();
          const selected = filteredOptions[activeIndex];
          setInputValue(selected.label);
          onChange(selected.value);
          setIsOpen(false);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setActiveIndex(-1);
        break;
    }
  };

  return (
    <div>
      <label htmlFor="combo-input">{label}</label>
      <input
        id="combo-input"
        type="text"
        role="combobox"
        aria-autocomplete="list"
        aria-expanded={isOpen}
        aria-controls={listboxId}
        aria-activedescendant={
          activeIndex >= 0 ? `option-${activeIndex}` : undefined
        }
        value={inputValue}
        onChange={(e) => {
          setInputValue(e.target.value);
          setIsOpen(true);
        }}
        onKeyDown={handleKeyDown}
        onFocus={() => setIsOpen(true)}
        onBlur={() => setTimeout(() => setIsOpen(false), 200)}
      />

      {isOpen && filteredOptions.length > 0 && (
        <ul id={listboxId} role="listbox">
          {filteredOptions.map((opt, index) => (
            <li
              key={opt.value}
              id={`option-${index}`}
              role="option"
              aria-selected={index === activeIndex}
              onClick={() => {
                setInputValue(opt.label);
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
```

### Slider

```tsx
function Slider({ min, max, value, onChange, label }) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    let newValue = value;
    const step = (max - min) / 10;

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowUp':
        newValue = Math.min(value + step, max);
        break;
      case 'ArrowLeft':
      case 'ArrowDown':
        newValue = Math.max(value - step, min);
        break;
      case 'Home':
        newValue = min;
        break;
      case 'End':
        newValue = max;
        break;
      default:
        return;
    }

    e.preventDefault();
    onChange(newValue);
  };

  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <div>
      <label id="slider-label">{label}: {value}</label>
      <div
        role="slider"
        aria-labelledby="slider-label"
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={value}
        aria-valuetext={`${value} of ${max}`}
        tabIndex={0}
        onKeyDown={handleKeyDown}
        style={{ '--percentage': `${percentage}%` } as React.CSSProperties}
      >
        <div className="slider-track">
          <div className="slider-fill" />
          <div className="slider-thumb" />
        </div>
      </div>
    </div>
  );
}
```

## Live Regions

Announce dynamic content changes to screen readers.

### Politeness Levels

| Level | Use Case | Behavior |
|-------|----------|----------|
| `polite` | Status updates | Waits for pause in speech |
| `assertive` | Urgent messages | Interrupts immediately |
| `off` | No announcement | Silences region |

```tsx
// Polite: Status messages, search results
function SearchStatus({ count, isSearching }) {
  return (
    <div role="status" aria-live="polite" aria-atomic="true">
      {isSearching ? 'Searching...' : `Found ${count} results`}
    </div>
  );
}

// Assertive: Errors, urgent alerts
function ErrorAlert({ error }) {
  return (
    <div role="alert" aria-live="assertive">
      Error: {error}
    </div>
  );
}

// Status role (implicit aria-live="polite")
function LoadingIndicator({ isLoading }) {
  return (
    <div role="status">
      {isLoading ? 'Loading...' : 'Ready'}
    </div>
  );
}

// Alert role (implicit aria-live="assertive")
function ValidationError({ message }) {
  return (
    <div role="alert">
      {message}
    </div>
  );
}
```

### Live Region Attributes

```tsx
// aria-atomic: Announce entire region or just changes
<div aria-live="polite" aria-atomic="true">
  {/* Entire content announced on any change */}
  Items in cart: {count}
</div>

<div aria-live="polite" aria-atomic="false">
  {/* Only changed parts announced */}
  <ul>
    {items.map(item => <li key={item.id}>{item.name}</li>)}
  </ul>
</div>

// aria-relevant: What changes to announce
<div
  aria-live="polite"
  aria-relevant="additions removals"  // additions | removals | text | all
>
  {notifications.map(n => <div key={n.id}>{n.message}</div>)}
</div>

// aria-busy: Suppress announcements during updates
function DataGrid({ data, isLoading }) {
  return (
    <div aria-live="polite" aria-busy={isLoading}>
      {data.map(row => <Row key={row.id} data={row} />)}
    </div>
  );
}
```

## Common ARIA States

### aria-expanded

```tsx
// Dropdown, accordion, collapsible
<button aria-expanded={isOpen} aria-controls="content">
  Toggle
</button>
<div id="content" hidden={!isOpen}>
  Content
</div>
```

### aria-selected

```tsx
// Tabs, listbox, tree items
<li role="option" aria-selected={isSelected}>
  Option
</li>
```

### aria-checked

```tsx
// Checkbox, radio, toggle
<div role="checkbox" aria-checked={isChecked}>
  Checkbox
</div>

// Mixed state (indeterminate)
<div role="checkbox" aria-checked="mixed">
  Parent checkbox
</div>
```

### aria-pressed

```tsx
// Toggle button
<button aria-pressed={isActive}>
  Bold
</button>
```

### aria-current

```tsx
// Current page, step, date
<a href="/about" aria-current="page">About</a>

<li aria-current="step">Step 2</li>

<td aria-current="date">Today</td>
```

### aria-disabled

```tsx
// Disabled but focusable (for tooltips on disabled elements)
<button
  aria-disabled="true"
  onClick={(e) => {
    if (true) e.preventDefault();
  }}
>
  Disabled Action
</button>

// vs native disabled (not focusable)
<button disabled>Disabled</button>
```

### aria-invalid

```tsx
// Form validation
<input
  aria-invalid={hasError}
  aria-describedby={hasError ? 'error-msg' : undefined}
/>
{hasError && <span id="error-msg">{error}</span>}
```

## ARIA Properties

### Labeling

```tsx
// aria-label: Direct label
<button aria-label="Close dialog">×</button>

// aria-labelledby: Reference existing text
<section aria-labelledby="section-title">
  <h2 id="section-title">Products</h2>
</section>

// aria-describedby: Additional description
<input
  aria-label="Password"
  aria-describedby="password-help"
/>
<span id="password-help">Must be 8+ characters</span>

// Multiple references
<input
  aria-labelledby="label error"
  aria-describedby="help"
/>
```

### Relationships

```tsx
// aria-controls: Element controls another
<button aria-controls="menu" aria-expanded={isOpen}>
  Menu
</button>
<ul id="menu">{/* menu items */}</ul>

// aria-owns: Virtual parent-child relationship
<div role="listbox" aria-owns="option-1 option-2">
  {/* Options rendered elsewhere in DOM */}
</div>

// aria-activedescendant: Current active option
<div
  role="listbox"
  tabIndex={0}
  aria-activedescendant={`option-${activeIndex}`}
>
  {options.map((opt, i) => (
    <div
      key={opt.id}
      id={`option-${i}`}
      role="option"
      aria-selected={i === activeIndex}
    >
      {opt.label}
    </div>
  ))}
</div>
```

### Hiding Content

```tsx
// aria-hidden: Hide from assistive tech
<span aria-hidden="true">👍</span>  {/* Decorative */}
<span className="sr-only">Thumbs up</span>

// inert: Hide and prevent interaction (HTML attribute)
<div inert={isModalOpen}>
  {/* Background content when modal is open */}
</div>
```

## Common Patterns Reference

| Pattern | Required ARIA |
|---------|---------------|
| Accordion | `aria-expanded`, `aria-controls` |
| Alert | `role="alert"` or `aria-live="assertive"` |
| Breadcrumb | `aria-current="page"` |
| Carousel | `aria-roledescription`, `aria-label` |
| Combobox | `role="combobox"`, `aria-expanded`, `aria-autocomplete` |
| Dialog | `role="dialog"`, `aria-modal`, `aria-labelledby` |
| Disclosure | `aria-expanded`, `aria-controls` |
| Feed | `role="feed"`, `aria-busy` |
| Listbox | `role="listbox"`, `role="option"`, `aria-selected` |
| Menu | `role="menu"`, `role="menuitem"` |
| Tabs | `role="tablist/tab/tabpanel"`, `aria-selected` |
| Tooltip | `role="tooltip"`, `aria-describedby` |
| Tree | `role="tree/treeitem"`, `aria-expanded` |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Duplicate labels | Redundant announcements | Use one labeling method |
| role="button" on `<button>` | Redundant | Remove unnecessary role |
| aria-hidden on focusable | Focus trap | Remove focusable elements |
| Empty aria-label | No accessible name | Provide meaningful label |
| aria-live on changing parent | Multiple announcements | Use on stable container |
| tabindex > 0 | Breaks tab order | Use 0 or -1 only |

## Testing ARIA

```bash
# Browser tools
- Chrome DevTools Accessibility panel
- Firefox Accessibility Inspector
- axe DevTools extension

# Screen readers
- NVDA (Windows, free)
- JAWS (Windows, paid)
- VoiceOver (Mac, built-in)
- TalkBack (Android, built-in)

# Automated testing
npm install --save-dev @axe-core/react jest-axe
```

```tsx
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('component has no ARIA violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
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

