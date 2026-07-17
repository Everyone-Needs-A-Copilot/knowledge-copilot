---
last_updated: 2026-02-25
status: active
name: keyboard-navigation-design
description: Complete keyboard navigation design - tab order, focus management, keyboard shortcuts, screen reader support. Use for accessibility.
triggers:
  files: ["**/accessibility/**", "**/a11y/**", "**/keyboard/**", "**/focus/**"]
  keywords: ["keyboard navigation", "tab order", "focus", "focus trap", "keyboard shortcuts", "screen reader", "a11y", "accessibility"]
allowed-tools: Read, Write, Edit
---

# Keyboard Navigation Design Skill

Master guide for designing complete keyboard navigation - logical tab order, focus management, keyboard shortcuts, and screen reader compatibility.

## Philosophy

**Keyboard-first is inclusive by design.** Screen reader users, motor impairments, power users, and developers all benefit from keyboard navigation. What works for keyboard works for everyone.

**Visible focus is non-negotiable.** Users must always know where they are. Never remove focus indicators without providing better alternatives.

**Match visual and logical order.** Tab order should follow the visual flow. Surprises in focus movement create confusion.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Focus Fundamentals

### What Receives Focus?

**Natively focusable** (tabindex not needed):
- `<a href="...">` (with href)
- `<button>`
- `<input>`, `<textarea>`, `<select>`
- `<details>`/`<summary>`

**Not natively focusable**:
- `<div>`, `<span>`, `<p>`
- `<a>` (without href)
- `<img>`
- Custom components (unless role added)

**Making elements focusable**:
```html
<!-- Add to tab order -->
<div tabindex="0">Focusable div</div>

<!-- Programmatically focusable only (not in tab order) -->
<div tabindex="-1">Focus via JS only</div>

<!-- Never use positive tabindex -->
<div tabindex="1">❌ Don't do this</div>
```

### Focus Order Principles

1. **Match visual order**: Left-to-right, top-to-bottom (LTR languages)
2. **Group related elements**: Form fields, card contents
3. **Skip decorative elements**: Images, dividers
4. **Include all interactive elements**: Buttons, links, inputs
5. **Exclude disabled elements**: They shouldn't receive focus

---

## Tab Order Design

### Logical Flow

**Good tab order**:
```
┌────────────────────────────────────┐
│ [1 Logo] [2 Nav] [3 Nav] [4 Search]│
├────────────────────────────────────┤
│                                    │
│ [5 Main CTA]                       │
│                                    │
│ [6 Card] [7 Card] [8 Card]         │
│                                    │
│ [9 Footer] [10 Footer] [11 Footer] │
└────────────────────────────────────┘
```

**Bad tab order**:
```
┌────────────────────────────────────┐
│ [1 Logo] [5 Nav] [2 Nav] [9 Search]│
├────────────────────────────────────┤
│                                    │
│ [3 Main CTA]                       │
│                                    │
│ [4 Card] [8 Card] [6 Card]         │
│                                    │
│ [11 Footer] [7 Footer] [10 Footer] │
└────────────────────────────────────┘
```

### Common Tab Order Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Wrong order | CSS visual reordering | Match DOM to visual |
| Skip elements | Missing tabindex | Add tabindex="0" |
| Extra stops | Non-interactive focusable | Remove tabindex |
| Focus jumps | Absolute positioning | Reorder DOM |

### DOM Order vs Visual Order

```html
<!-- ❌ BAD: CSS flexbox reverses visual but not tab order -->
<style>.container { display: flex; flex-direction: row-reverse; }</style>
<div class="container">
  <button>First in DOM (shows last)</button>
  <button>Second in DOM (shows first)</button>
</div>

<!-- ✅ GOOD: DOM matches visual order -->
<div class="container">
  <button>First visually and in DOM</button>
  <button>Second visually and in DOM</button>
</div>
```

---

## Focus Indicators

### Visibility Requirements

WCAG 2.4.7 requires visible focus indicators.
WCAG 2.4.11 (Level AAA) requires 3:1 contrast.

**Minimum requirements**:
- Visible on all focusable elements
- Distinguishable from other states
- Sufficient contrast

### Focus Styles

```css
/* Default browser focus (often removed - bad practice) */
:focus {
  outline: none; /* ❌ Never do this without replacement */
}

/* Custom focus ring */
:focus-visible {
  outline: 3px solid var(--focus-color);
  outline-offset: 2px;
}

/* Alternative: Box shadow (more control) */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--focus-color);
}
```

### Focus-visible vs Focus

```css
/* :focus - All focus (mouse click, keyboard, programmatic) */
button:focus {
  /* Shows for mouse clicks too - often unwanted */
}

/* :focus-visible - Only keyboard/programmatic focus */
button:focus-visible {
  /* Only shows when keyboard navigating - better UX */
}

/* Modern approach */
button:focus {
  outline: none; /* Remove default */
}

button:focus-visible {
  outline: 3px solid blue; /* Custom keyboard focus */
}
```

### Focus Within

For containers with focusable children:
```css
.search-container:focus-within {
  border-color: var(--focus-color);
  box-shadow: 0 0 0 3px var(--focus-color-light);
}
```

---

## Focus Management

### Modal Focus Trap

When modal opens:
1. Store previously focused element
2. Move focus to modal (or first element)
3. Trap Tab within modal
4. Return focus on close

```javascript
class Modal {
  open() {
    this.previouslyFocused = document.activeElement;
    this.modal.removeAttribute('hidden');
    this.firstFocusable.focus();
    this.trapFocus();
  }

  close() {
    this.modal.setAttribute('hidden', '');
    this.previouslyFocused?.focus();
  }

  trapFocus() {
    const focusables = this.modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    this.modal.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });
  }
}
```

### Skip Links

Allow users to bypass repetitive content:
```html
<body>
  <a href="#main-content" class="skip-link">
    Skip to main content
  </a>
  <nav><!-- Long navigation --></nav>
  <main id="main-content" tabindex="-1">
    <!-- Main content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
}

.skip-link:focus {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  padding: 1rem;
  background: white;
}
```

### Focus After Dynamic Content

When content changes:
```javascript
// After loading new content
const newContent = document.getElementById('loaded-content');
newContent.focus(); // Move focus to new content
newContent.setAttribute('tabindex', '-1'); // Temporarily focusable

// After deleting item in list
const nextItem = deletedItem.nextElementSibling || deletedItem.previousElementSibling;
nextItem?.focus();

// After form validation error
const firstError = document.querySelector('[aria-invalid="true"]');
firstError?.focus();
```

---

## Keyboard Shortcuts

### Standard Shortcuts

Common patterns users expect:
| Action | Shortcut |
|--------|----------|
| Save | Ctrl/Cmd + S |
| Undo | Ctrl/Cmd + Z |
| Redo | Ctrl/Cmd + Shift + Z |
| Search | Ctrl/Cmd + K or / |
| New item | Ctrl/Cmd + N |
| Close | Escape |
| Submit | Enter |

### Component Shortcuts

| Component | Keys |
|-----------|------|
| Dropdown | Space/Enter to open, Arrow keys to navigate, Escape to close |
| Menu | Arrow keys, Home/End, Type to jump |
| Tabs | Arrow keys to switch, Enter/Space to activate |
| Dialog | Tab to navigate, Escape to close |
| Slider | Arrow keys to adjust |
| Tree | Arrow keys, Enter to expand/select |

### Custom Shortcuts

Guidelines:
- Don't override browser shortcuts
- Provide visual indicator of shortcuts
- Make discoverable (tooltip, help menu)
- Allow customization if possible

```javascript
// Command palette pattern
document.addEventListener('keydown', (e) => {
  // Cmd/Ctrl + K for command palette
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    openCommandPalette();
  }
});
```

---

## ARIA for Keyboard Navigation

### Roles and Keyboard Behavior

| Role | Expected Keyboard Behavior |
|------|---------------------------|
| `button` | Space/Enter activates |
| `link` | Enter activates |
| `checkbox` | Space toggles |
| `radio` | Arrow keys, Space selects |
| `listbox` | Arrow keys, Enter selects |
| `menu` | Arrow keys, Enter selects |
| `tablist` | Arrow keys switch, Enter activates |
| `slider` | Arrow keys adjust |
| `dialog` | Tab trapped, Escape closes |

### Common ARIA Patterns

**Disclosure (expand/collapse)**:
```html
<button
  aria-expanded="false"
  aria-controls="panel"
>
  Show details
</button>
<div id="panel" hidden>
  Details content
</div>
```

**Tabs**:
```html
<div role="tablist">
  <button
    role="tab"
    aria-selected="true"
    aria-controls="panel1"
    tabindex="0"
  >Tab 1</button>
  <button
    role="tab"
    aria-selected="false"
    aria-controls="panel2"
    tabindex="-1"
  >Tab 2</button>
</div>
<div role="tabpanel" id="panel1">Content 1</div>
<div role="tabpanel" id="panel2" hidden>Content 2</div>
```

**Roving tabindex** (for tab-like widgets):
```javascript
// Only one item in tab order; use arrow keys to move
tabs.forEach((tab, i) => {
  tab.tabIndex = i === activeIndex ? 0 : -1;
});

// Arrow key handler moves focus AND updates tabindex
tabList.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') {
    tabs[activeIndex].tabIndex = -1;
    activeIndex = (activeIndex + 1) % tabs.length;
    tabs[activeIndex].tabIndex = 0;
    tabs[activeIndex].focus();
  }
});
```

---

## Testing Keyboard Navigation

### Manual Testing Checklist

```markdown
## Keyboard Testing Checklist

Navigation:
- [ ] Can reach all interactive elements with Tab
- [ ] Tab order follows visual order
- [ ] No keyboard traps
- [ ] Skip link works
- [ ] Focus visible on all elements

Components:
- [ ] Buttons activate with Enter/Space
- [ ] Links activate with Enter
- [ ] Dropdowns open/close correctly
- [ ] Modals trap focus
- [ ] Modals close with Escape
- [ ] Forms submit with Enter

Focus Management:
- [ ] Focus moves to modal when opened
- [ ] Focus returns when modal closes
- [ ] Focus moves to errors on validation
- [ ] Focus moves appropriately on content changes
```

### Testing Tools

**Browser DevTools**:
- Tab through page
- Check focus indicator visibility
- Accessibility inspector

**Automated**:
- axe-core
- WAVE
- Lighthouse

**Screen Readers**:
- VoiceOver (Mac)
- NVDA (Windows, free)
- JAWS (Windows)

---

## Common Patterns

### Card Navigation

**Non-interactive card**:
```html
<article class="card">
  <h3><a href="/article">Title</a></h3>
  <p>Description</p>
</article>
<!-- Only the link is focusable -->
```

**Interactive card (click entire card)**:
```html
<article class="card">
  <h3><a href="/article" class="card-link">Title</a></h3>
  <p>Description</p>
</article>

<style>
.card-link::before {
  content: '';
  position: absolute;
  inset: 0;
}
</style>
<!-- Pseudo-element makes entire card clickable -->
```

### Toolbar Navigation

```html
<div role="toolbar" aria-label="Text formatting">
  <button aria-pressed="false">Bold</button>
  <button aria-pressed="false">Italic</button>
  <button aria-pressed="false">Underline</button>
</div>
```

Arrow keys move between buttons; Tab moves out of toolbar.

### Data Tables

```html
<table>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
      <th scope="col">Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John</td>
      <td>john@example.com</td>
      <td>
        <button>Edit</button>
        <button>Delete</button>
      </td>
    </tr>
  </tbody>
</table>
```

---

## Quick Reference

### Keyboard Shortcuts Cheatsheet

| Key | Standard Function |
|-----|------------------|
| Tab | Next focusable |
| Shift+Tab | Previous focusable |
| Enter | Activate link/button |
| Space | Activate button, scroll, toggle |
| Escape | Close, cancel |
| Arrow keys | Navigate within widgets |
| Home/End | First/last item |
| Page Up/Down | Scroll |

### Focus Management Checklist

- [ ] Modal focus trap implemented
- [ ] Skip link present
- [ ] Focus moves on content change
- [ ] Focus returns after modal close
- [ ] Focus visible on all elements
- [ ] Tab order matches visual order
- [ ] No positive tabindex values

### ARIA Keyboard Patterns

| Widget | Arrow keys | Enter/Space | Escape |
|--------|-----------|-------------|--------|
| Menu | Navigate | Select | Close |
| Tabs | Switch tabs | Activate | - |
| Listbox | Navigate | Select | - |
| Dialog | - | - | Close |
| Combobox | Navigate list | Select | Close |
| Slider | Adjust value | - | - |

---

## Summary

**Keyboard navigation = Universal access**

1. All interactive elements must be reachable
2. Tab order must match visual order
3. Focus must always be visible
4. Complex widgets need arrow key navigation
5. Modals must trap focus
6. Test with keyboard only

*If you can't use it without a mouse, many users can't use it at all.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

