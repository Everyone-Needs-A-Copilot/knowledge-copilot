---
last_updated: 2026-02-25
status: active
name: keyboard-accessibility-implementation
description: Full keyboard accessibility - tab order, focus management, keyboard shortcuts, screen reader compatibility. Use when building interactive components.
triggers:
  files: ["**/*.tsx", "**/*.jsx", "**/components/**", "**/hooks/**"]
  keywords: ["keyboard", "focus", "tab", "tabIndex", "onKeyDown", "accessibility", "a11y", "navigation", "shortcut"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Keyboard Accessibility Implementation

Implement complete keyboard accessibility for interactive web applications.

## Core Principles

| Principle | Description |
|-----------|-------------|
| All functionality via keyboard | No mouse required |
| Visible focus indicators | Always know where focus is |
| Logical tab order | Matches visual/reading order |
| No keyboard traps | Can always escape |
| Shortcuts don't conflict | Don't override browser/AT shortcuts |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Tab Navigation

### tabIndex Values

| Value | Behavior | Use Case |
|-------|----------|----------|
| `0` | In natural tab order | Interactive elements |
| `-1` | Programmatically focusable | Managed focus targets |
| `> 0` | **Never use** | Breaks natural order |

```tsx
// tabIndex={0}: Add to tab order
<div
  role="button"
  tabIndex={0}  // Keyboard accessible
  onClick={handleClick}
>
  Custom button
</div>

// tabIndex={-1}: Focusable but not in tab order
<main id="main-content" tabIndex={-1}>
  {/* Focus target for skip links */}
</main>

// Native elements: Already in tab order
<button>Already focusable</button>
<input type="text" />
<a href="/page">Link</a>
<select><option>Option</option></select>
```

### Skip Links

```tsx
function Layout({ children }) {
  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <a href="#navigation" className="skip-link">
        Skip to navigation
      </a>

      <header>
        <nav id="navigation" tabIndex={-1}>
          {/* Navigation */}
        </nav>
      </header>

      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
    </>
  );
}

// Skip link styles
const skipLinkStyles = css`
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    padding: 8px 16px;
    background: #000;
    color: #fff;
    text-decoration: none;
    z-index: 9999;
  }

  .skip-link:focus {
    top: 0;
  }
`;
```

## Focus Management

### Focus Indicators

```tsx
// NEVER remove focus without replacement
// BAD:
*:focus { outline: none; }

// GOOD: Enhanced focus indicator
const focusStyles = css`
  /* Default focus style */
  :focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }

  /* Keyboard-only focus (modern browsers) */
  :focus:not(:focus-visible) {
    outline: none;
  }

  :focus-visible {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.2);
  }

  /* High contrast mode support */
  @media (forced-colors: active) {
    :focus {
      outline: 3px solid CanvasText;
    }
  }
`;
```

### useFocusManagement Hook

```tsx
function useFocusManagement<T extends HTMLElement>() {
  const ref = useRef<T>(null);

  const focus = useCallback(() => {
    ref.current?.focus();
  }, []);

  const blur = useCallback(() => {
    ref.current?.blur();
  }, []);

  return { ref, focus, blur };
}

// Usage
function Modal({ isOpen, children }) {
  const { ref, focus } = useFocusManagement<HTMLDivElement>();

  useEffect(() => {
    if (isOpen) {
      focus();
    }
  }, [isOpen, focus]);

  return (
    <div ref={ref} tabIndex={-1} role="dialog">
      {children}
    </div>
  );
}
```

### Focus Trap

```tsx
function useFocusTrap(isActive: boolean) {
  const containerRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isActive) return;

    // Store previous focus
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus first focusable element
    const focusableElements = getFocusableElements(containerRef.current);
    focusableElements[0]?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      const focusable = getFocusableElements(containerRef.current);
      if (!focusable.length) return;

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

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      previousFocusRef.current?.focus();
    };
  }, [isActive]);

  return containerRef;
}

function getFocusableElements(container: HTMLElement | null): HTMLElement[] {
  if (!container) return [];

  const selector = [
    'button:not([disabled])',
    'a[href]',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(', ');

  return Array.from(container.querySelectorAll(selector));
}

// Usage
function Dialog({ isOpen, onClose, children }) {
  const containerRef = useFocusTrap(isOpen);

  return (
    <div ref={containerRef} role="dialog" aria-modal="true">
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

### Roving tabIndex

For composite widgets (toolbars, menus, tabs), use roving tabIndex.

```tsx
function useRovingTabIndex<T extends HTMLElement>(itemCount: number) {
  const [activeIndex, setActiveIndex] = useState(0);
  const itemRefs = useRef<Map<number, T>>(new Map());

  const setRef = useCallback((index: number) => (el: T | null) => {
    if (el) {
      itemRefs.current.set(index, el);
    } else {
      itemRefs.current.delete(index);
    }
  }, []);

  const getTabIndex = useCallback((index: number) => {
    return index === activeIndex ? 0 : -1;
  }, [activeIndex]);

  const focusItem = useCallback((index: number) => {
    const boundedIndex = Math.max(0, Math.min(index, itemCount - 1));
    setActiveIndex(boundedIndex);
    itemRefs.current.get(boundedIndex)?.focus();
  }, [itemCount]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
        e.preventDefault();
        focusItem((activeIndex + 1) % itemCount);
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        focusItem((activeIndex - 1 + itemCount) % itemCount);
        break;
      case 'Home':
        e.preventDefault();
        focusItem(0);
        break;
      case 'End':
        e.preventDefault();
        focusItem(itemCount - 1);
        break;
    }
  }, [activeIndex, itemCount, focusItem]);

  return { setRef, getTabIndex, handleKeyDown, activeIndex };
}

// Usage: Toolbar
function Toolbar({ items }) {
  const { setRef, getTabIndex, handleKeyDown } = useRovingTabIndex(items.length);

  return (
    <div role="toolbar" aria-label="Formatting">
      {items.map((item, index) => (
        <button
          key={item.id}
          ref={setRef(index)}
          tabIndex={getTabIndex(index)}
          onKeyDown={handleKeyDown}
          onClick={item.action}
          aria-label={item.label}
        >
          {item.icon}
        </button>
      ))}
    </div>
  );
}
```

## Keyboard Event Handling

### Standard Key Bindings

| Key | Action |
|-----|--------|
| `Enter` | Activate button, submit form |
| `Space` | Activate button, toggle checkbox |
| `Escape` | Close modal, cancel, clear |
| `Tab` | Move to next focusable |
| `Shift+Tab` | Move to previous focusable |
| `Arrow keys` | Navigate within widget |
| `Home` | First item |
| `End` | Last item |

### Event Handler Patterns

```tsx
// Custom button
function Button({ onClick, children }) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick();
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

// Menu navigation
function Menu({ items }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex(i => Math.min(i + 1, items.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex(i => Math.max(i - 1, 0));
        break;
      case 'Home':
        e.preventDefault();
        setActiveIndex(0);
        break;
      case 'End':
        e.preventDefault();
        setActiveIndex(items.length - 1);
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        items[activeIndex].action();
        break;
    }
  };

  return (
    <ul role="menu" onKeyDown={handleKeyDown}>
      {items.map((item, index) => (
        <li
          key={item.id}
          role="menuitem"
          tabIndex={index === activeIndex ? 0 : -1}
        >
          {item.label}
        </li>
      ))}
    </ul>
  );
}

// Type-ahead search in list
function useTypeahead<T extends { label: string }>(
  items: T[],
  onMatch: (index: number) => void
) {
  const searchRef = useRef('');
  const timeoutRef = useRef<number>();

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    // Only single printable characters
    if (e.key.length !== 1) return;

    // Accumulate search string
    searchRef.current += e.key.toLowerCase();

    // Find matching item
    const matchIndex = items.findIndex(item =>
      item.label.toLowerCase().startsWith(searchRef.current)
    );

    if (matchIndex >= 0) {
      onMatch(matchIndex);
    }

    // Clear search after delay
    clearTimeout(timeoutRef.current);
    timeoutRef.current = window.setTimeout(() => {
      searchRef.current = '';
    }, 500);
  }, [items, onMatch]);

  return handleKeyDown;
}
```

## Keyboard Shortcuts

### useKeyboardShortcut Hook

```tsx
interface ShortcutConfig {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  meta?: boolean;
  action: () => void;
  description?: string;
}

function useKeyboardShortcut(shortcuts: ShortcutConfig[]) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger in input fields
      if (
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement ||
        (e.target as HTMLElement).isContentEditable
      ) {
        return;
      }

      for (const shortcut of shortcuts) {
        const keyMatch = e.key.toLowerCase() === shortcut.key.toLowerCase();
        const ctrlMatch = !!shortcut.ctrl === (e.ctrlKey || e.metaKey);
        const shiftMatch = !!shortcut.shift === e.shiftKey;
        const altMatch = !!shortcut.alt === e.altKey;

        if (keyMatch && ctrlMatch && shiftMatch && altMatch) {
          e.preventDefault();
          shortcut.action();
          break;
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts]);
}

// Usage
function App() {
  useKeyboardShortcut([
    { key: 'k', ctrl: true, action: openSearch, description: 'Open search' },
    { key: 'n', ctrl: true, action: createNew, description: 'Create new item' },
    { key: '?', shift: true, action: showHelp, description: 'Show shortcuts' },
  ]);

  return <div>...</div>;
}
```

### Shortcut Display Component

```tsx
function ShortcutHelp({ shortcuts }) {
  return (
    <div role="dialog" aria-label="Keyboard shortcuts">
      <h2>Keyboard Shortcuts</h2>
      <table>
        <thead>
          <tr>
            <th>Shortcut</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {shortcuts.map(shortcut => (
            <tr key={shortcut.description}>
              <td>
                <kbd>{shortcut.ctrl && 'Ctrl+'}{shortcut.key}</kbd>
              </td>
              <td>{shortcut.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Styled kbd element
const kbdStyles = css`
  kbd {
    display: inline-block;
    padding: 2px 6px;
    font-family: monospace;
    font-size: 0.875em;
    background: #f4f4f4;
    border: 1px solid #ccc;
    border-radius: 3px;
    box-shadow: 0 1px 0 #ccc;
  }
`;
```

### Avoiding Conflicts

```tsx
// Reserved shortcuts to avoid
const reservedShortcuts = {
  browser: [
    'Ctrl+N', 'Ctrl+T', 'Ctrl+W',  // Window/tab
    'Ctrl+F', 'Ctrl+G',             // Find
    'Ctrl+P', 'Ctrl+S',             // Print/Save
    'Ctrl+H', 'Ctrl+J',             // History/Downloads
    'F1', 'F5', 'F11', 'F12',       // Browser functions
  ],
  screenReader: [
    'Insert+*',  // NVDA/JAWS commands
    'Ctrl+Alt+*', // VoiceOver commands
    'CapsLock+*', // Some screen reader modifier
  ],
};

// Safe custom shortcuts
const safeShortcuts = [
  'Ctrl+K',     // Often unused
  'Ctrl+/',     // Often for help
  'Ctrl+\\',    // Often for sidebar
  '?',          // Help (without modifier)
];
```

## Focus After Actions

### After Delete

```tsx
function List({ items, onDelete }) {
  const itemRefs = useRef<Map<string, HTMLElement>>(new Map());

  const handleDelete = (id: string, index: number) => {
    onDelete(id);

    // Focus next item, or previous if last
    setTimeout(() => {
      const nextIndex = index < items.length - 1 ? index : index - 1;
      if (nextIndex >= 0) {
        const nextItem = items[nextIndex];
        itemRefs.current.get(nextItem.id)?.focus();
      }
    }, 0);
  };

  return (
    <ul>
      {items.map((item, index) => (
        <li key={item.id}>
          <span>{item.name}</span>
          <button
            ref={el => el && itemRefs.current.set(item.id, el)}
            onClick={() => handleDelete(item.id, index)}
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### After Form Submit

```tsx
function Form({ onSubmit }) {
  const successRef = useRef<HTMLDivElement>(null);
  const errorRef = useRef<HTMLDivElement>(null);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await onSubmit();
      setStatus('success');
      setTimeout(() => successRef.current?.focus(), 0);
    } catch {
      setStatus('error');
      setTimeout(() => errorRef.current?.focus(), 0);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {status === 'success' && (
        <div ref={successRef} tabIndex={-1} role="alert">
          Form submitted successfully!
        </div>
      )}

      {status === 'error' && (
        <div ref={errorRef} tabIndex={-1} role="alert">
          Submission failed. Please try again.
        </div>
      )}

      {/* Form fields */}
      <button type="submit">Submit</button>
    </form>
  );
}
```

### After Navigation

```tsx
function useRouteAnnouncer() {
  const mainRef = useRef<HTMLElement>(null);
  const location = useLocation();

  useEffect(() => {
    // Focus main content on route change
    mainRef.current?.focus();

    // Announce new page
    const title = document.title;
    announceToScreenReader(`Navigated to ${title}`);
  }, [location]);

  return mainRef;
}

function announceToScreenReader(message: string) {
  const announcer = document.createElement('div');
  announcer.setAttribute('role', 'status');
  announcer.setAttribute('aria-live', 'polite');
  announcer.setAttribute('aria-atomic', 'true');
  announcer.className = 'sr-only';
  announcer.textContent = message;

  document.body.appendChild(announcer);
  setTimeout(() => announcer.remove(), 1000);
}
```

## Common Widget Patterns

### Modal Keyboard Handling

```tsx
function Modal({ isOpen, onClose, children }) {
  const containerRef = useFocusTrap(isOpen);

  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div ref={containerRef} role="dialog" aria-modal="true">
      {children}
    </div>
  );
}
```

### Dropdown Keyboard Handling

```tsx
function Dropdown({ trigger, items }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const menuRef = useRef<HTMLUListElement>(null);

  const handleTriggerKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
      case 'ArrowDown':
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(0);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(items.length - 1);
        break;
    }
  };

  const handleMenuKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex(i => Math.min(i + 1, items.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex(i => Math.max(i - 1, 0));
        break;
      case 'Home':
        e.preventDefault();
        setActiveIndex(0);
        break;
      case 'End':
        e.preventDefault();
        setActiveIndex(items.length - 1);
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        items[activeIndex].action();
        setIsOpen(false);
        break;
      case 'Escape':
      case 'Tab':
        setIsOpen(false);
        break;
    }
  };

  return (
    <div>
      <button
        aria-haspopup="menu"
        aria-expanded={isOpen}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleTriggerKeyDown}
      >
        {trigger}
      </button>

      {isOpen && (
        <ul
          ref={menuRef}
          role="menu"
          onKeyDown={handleMenuKeyDown}
        >
          {items.map((item, index) => (
            <li
              key={item.id}
              role="menuitem"
              tabIndex={index === activeIndex ? 0 : -1}
              onClick={item.action}
            >
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Testing Keyboard Accessibility

### Manual Testing Checklist

```markdown
## Keyboard Navigation
- [ ] Can Tab to all interactive elements
- [ ] Tab order matches visual order
- [ ] Focus indicator always visible
- [ ] Can Tab away from any element (no trap)
- [ ] Skip link works and is visible on focus

## Interactive Elements
- [ ] Buttons activate with Enter and Space
- [ ] Links activate with Enter
- [ ] Checkboxes toggle with Space
- [ ] Radio buttons change with arrows
- [ ] Selects open with Space/Enter/arrows

## Custom Widgets
- [ ] Arrow keys navigate within widget
- [ ] Home/End go to first/last
- [ ] Escape closes overlays
- [ ] Focus managed after actions

## Forms
- [ ] All inputs have visible labels
- [ ] Error messages associated with inputs
- [ ] Submit works with Enter
- [ ] Validation errors announced
```

### Automated Testing

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Keyboard accessibility', () => {
  it('button responds to Enter', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    const button = screen.getByRole('button');
    button.focus();
    await userEvent.keyboard('{Enter}');

    expect(handleClick).toHaveBeenCalled();
  });

  it('modal traps focus', async () => {
    render(<Modal isOpen>Content</Modal>);

    const closeButton = screen.getByRole('button', { name: /close/i });
    closeButton.focus();

    // Tab should cycle within modal
    await userEvent.tab();
    expect(document.activeElement).not.toBe(document.body);
  });

  it('escape closes modal', async () => {
    const onClose = jest.fn();
    render(<Modal isOpen onClose={onClose}>Content</Modal>);

    await userEvent.keyboard('{Escape}');

    expect(onClose).toHaveBeenCalled();
  });
});
```

## Best Practices Summary

1. **Use native elements** when possible - they're keyboard accessible by default
2. **Don't remove focus styles** - users need to see where focus is
3. **Maintain logical tab order** - don't use positive tabindex
4. **Implement focus traps** for modals and dialogs
5. **Use roving tabindex** for composite widgets
6. **Handle Escape to close** overlays and modals
7. **Manage focus after actions** - delete, submit, navigation
8. **Test without mouse** - can you do everything?
9. **Avoid conflicting shortcuts** with browser/AT
10. **Announce dynamic changes** with live regions


## Quality Tests

### Visual Fidelity Test
- Implementation matches design within acceptable tolerance
- **PASS:** Spacing, colors, and typography match design tokens exactly
- **FAIL:** Visible deviations from design that aren't documented as intentional

### Accessibility Test
- Component is usable with keyboard-only and screen reader
- **PASS:** All interactive elements reachable by Tab, operable by Enter/Space
- **FAIL:** Mouse-only interactions or missing ARIA labels

