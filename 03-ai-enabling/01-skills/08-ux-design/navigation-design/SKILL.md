---
last_updated: 2026-02-25
status: active
name: navigation-design
description: Design navigation systems - menus, breadcrumbs, tabs, mobile patterns. Use for wayfinding and structure.
triggers:
  files: ["**/navigation/**", "**/menu/**", "**/nav/**", "**/header/**"]
  keywords: ["navigation", "menu", "breadcrumb", "tabs", "sidebar", "header", "footer", "mobile nav", "hamburger"]
allowed-tools: Read, Write, Edit
---

# Navigation Design Skill

Master guide for designing navigation systems that help users understand where they are, where they can go, and how to get there.

## Philosophy

**Navigation is wayfinding.** Like signage in a building, navigation tells users their location and available paths. Good navigation is invisible; users just know where things are.

**Every page needs three answers.** Where am I? Where can I go? How do I get back?

**Consistency beats cleverness.** Novel navigation patterns require learning. Standard patterns work instantly.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Navigation Fundamentals

### The Three Questions

Every screen should answer:
1. **Where am I?** (Current location indicator)
2. **Where can I go?** (Available destinations)
3. **How do I go back?** (Return path)

### Navigation Types

| Type | Purpose | Example |
|------|---------|---------|
| **Global** | Site-wide access | Main header menu |
| **Local** | Section-specific | Sidebar, section tabs |
| **Contextual** | Content-related | Related articles, "See also" |
| **Supplemental** | Alternative paths | Sitemap, footer links |
| **Utility** | Tools & account | Search, login, settings |

---

## Global Navigation

### Header Navigation

**Desktop pattern**:
```
┌────────────────────────────────────────────────┐
│ [Logo]  Products  Services  About  Contact    │
│                             [Search] [Login]  │
└────────────────────────────────────────────────┘
```

**Design guidelines**:
- 5-7 primary items maximum
- Most important items first (L-to-R)
- Utility items on right
- Logo links to home
- Current section highlighted

### Mega Menus

For sites with many pages:
```
Products ▼
┌─────────────────────────────────────────────────┐
│                                                 │
│ Category A    Category B    Category C          │
│ ──────────    ──────────    ──────────          │
│ • Item 1      • Item 1      • Item 1            │
│ • Item 2      • Item 2      • Item 2            │
│ • Item 3      • Item 3      • Item 3            │
│ • Item 4      • Item 4      • Item 4            │
│                                                 │
│ [Featured Image]   New arrivals →               │
│                    Best sellers →               │
│                                                 │
│ [View all Products →]                           │
└─────────────────────────────────────────────────┘
```

**When to use mega menus**:
- 25+ navigation items
- Clear category structure
- Space for featured content
- Desktop-focused users

### Dropdown Menus

For simpler hierarchies:
```
About ▼
┌─────────────┐
│ Our Story   │
│ Team        │
│ Careers     │
│ Press       │
│ Contact     │
└─────────────┘
```

**Guidelines**:
- Max 7-10 items
- One level deep
- Clear hover/focus states
- Close on click outside

---

## Local Navigation

### Sidebar Navigation

```
┌──────────────────┐
│ Section Name     │
├──────────────────┤
│ > Current Page   │  ← highlighted
│   Sibling Page   │
│   Sibling Page   │
│                  │
│ ▼ Subsection     │  ← expanded
│   └ Child Page   │
│   └ Child Page   │
│                  │
│ ▶ Subsection     │  ← collapsed
│ ▶ Subsection     │
└──────────────────┘
```

**Best for**:
- Documentation
- Settings
- Dashboards
- Deep hierarchies

**Guidelines**:
- Show current location
- Allow expand/collapse
- Sticky on scroll
- Consider mobile behavior

### Tab Navigation

**Horizontal tabs**:
```
[Tab 1] [Tab 2●] [Tab 3] [Tab 4]
─────────────────────────────────
Content for Tab 2
```

**Best for**:
- Parallel content views
- 3-7 related sections
- Content that doesn't need simultaneous view

**Guidelines**:
- Clear active state
- Content area directly below
- Don't use for sequential steps
- Don't nest tabs

### Segmented Controls

**For filtering/views**:
```
┌───────┬───────┬───────┐
│ All   │ Active│ Done  │
│   ●   │       │       │
└───────┴───────┴───────┘
```

**Best for**:
- Filtering same content
- View switching
- 2-5 options

---

## Contextual Navigation

### Breadcrumbs

**Path-based**:
```
Home › Products › Laptops › MacBook Pro
```

**Location-based**:
```
You are here: Products / Laptops / MacBook Pro
```

**Guidelines**:
- Show hierarchy, not history
- Current page not linked
- Separator: › or / or >
- Use schema.org markup
- Keep sticky or accessible

### Related Content

```
Related Articles
─────────────────
• Similar topic 1 →
• Similar topic 2 →
• Similar topic 3 →
```

### Pagination

**Numbered pagination**:
```
← Previous  1  2  [3]  4  5  ...  20  Next →
```

**Load more**:
```
[Showing 20 of 100]
     [Load More]
```

**Infinite scroll**:
- Auto-load on scroll
- Provide position indicator
- Allow jump to top

---

## Utility Navigation

### Search

**Placement**:
```
Standard: Top-right of header
Alternative: Center of header (search-heavy)
Mobile: Icon that expands
```

**Search bar anatomy**:
```
┌──────────────────────────────────┐
│ 🔍  Search products...           │
│     ↑ icon    ↑ placeholder      │
└──────────────────────────────────┘
```

**Search suggestions**:
```
[Search: "laptop"]
┌─────────────────────────────┐
│ laptop cases               │
│ laptop stands              │
│ laptop computers           │
│ ────────────────────       │
│ See all results for "laptop"
└─────────────────────────────┘
```

### User Account

**Logged out**:
```
[Log In] [Sign Up]
```

**Logged in**:
```
[Avatar ▼]
┌─────────────────┐
│ Profile         │
│ Settings        │
│ Billing         │
│ ────────        │
│ Log Out         │
└─────────────────┘
```

---

## Mobile Navigation

### Bottom Tab Bar

Most common mobile pattern:
```
┌─────────────────────────────┐
│                             │
│     [App Content]           │
│                             │
├───────┬───────┬───────┬─────┤
│ 🏠    │ 🔍    │ ♡     │ 👤  │
│ Home  │Search │ Saved │ Me  │
└───────┴───────┴───────┴─────┘
```

**Guidelines**:
- 3-5 items maximum
- Icons + labels
- Highlight active tab
- Primary destinations only
- Always visible

### Hamburger Menu

```
┌─────────────────────────────┐
│ ☰  App Name                 │
├─────────────────────────────┤
│                             │
│     [Content Area]          │
│                             │
└─────────────────────────────┘

[Tap ☰]

┌─────────────────────────────┐
│ ✕         User Name         │
│           user@email.com    │
├─────────────────────────────┤
│ 🏠 Home                     │
│ 📦 Products                 │
│ 💳 Orders                   │
│ ⚙️ Settings                 │
│ ❓ Help                     │
├─────────────────────────────┤
│ 🚪 Log Out                  │
└─────────────────────────────┘
```

**Guidelines**:
- Clear ☰ icon
- Slide-in animation
- Close on tap outside
- Show user info
- Group related items

### Bottom Sheet Navigation

```
[Content Area]

[Tap action button]

┌─────────────────────────────┐
│       ── Handle ──          │
│                             │
│ 📷 Take Photo               │
│ 🖼 Choose from Gallery      │
│ 📄 Choose File              │
│                             │
│     [Cancel]                │
└─────────────────────────────┘
```

**Best for**:
- Action selection
- Share options
- Creation flows

### Priority+ Pattern

Progressive collapse:
```
Desktop: [Home] [Products] [Services] [About] [Contact]
Tablet:  [Home] [Products] [Services] [More ▼]
Mobile:  [Home] [Products] [☰]
```

---

## Navigation States

### Visual States

| State | Indicator |
|-------|-----------|
| Default | Normal appearance |
| Hover | Background change, underline |
| Focus | Visible outline (accessibility) |
| Active/Current | Bold, highlight, underline |
| Disabled | Grayed out |

### Active Indicators

```css
/* Common active state patterns */

/* Underline */
.nav-item.active {
  border-bottom: 2px solid var(--primary);
}

/* Background */
.nav-item.active {
  background: var(--primary-light);
}

/* Left border */
.nav-item.active {
  border-left: 3px solid var(--primary);
}

/* Bold text */
.nav-item.active {
  font-weight: 600;
}
```

---

## Accessibility

### Keyboard Navigation

```
Tab       → Move to next item
Shift+Tab → Move to previous item
Enter     → Activate link
Space     → Activate button
Escape    → Close dropdown
Arrow keys → Navigate within dropdown
```

### ARIA Attributes

```html
<!-- Main navigation -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
  </ul>
</nav>

<!-- Breadcrumbs -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Laptops</li>
  </ol>
</nav>

<!-- Dropdown -->
<button
  aria-expanded="false"
  aria-controls="dropdown-menu"
  aria-haspopup="true"
>
  Menu
</button>
<ul id="dropdown-menu" hidden>
  <li><a href="/item1">Item 1</a></li>
</ul>
```

### Skip Links

```html
<a href="#main-content" class="skip-link">
  Skip to main content
</a>
```

---

## Navigation Anti-Patterns

### 1. Too Many Items

```
❌ Bad: 15 items in main nav
✅ Good: 5-7 items, more in mega menu
```

### 2. Deep Nesting

```
❌ Bad: 5+ levels of dropdowns
✅ Good: 2-3 levels maximum
```

### 3. Hidden Navigation

```
❌ Bad: Essential nav only in hamburger on desktop
✅ Good: Primary nav always visible on desktop
```

### 4. No Current Indicator

```
❌ Bad: Can't tell which page you're on
✅ Good: Clear active state on current section
```

### 5. Inconsistent Placement

```
❌ Bad: Nav moves between pages
✅ Good: Same position throughout
```

### 6. Click-Only Mega Menus

```
❌ Bad: Mega menu only on click (breaks mouse flow)
✅ Good: Hover to open, click to navigate
```

---

## Quick Reference

### Navigation Checklist

- [ ] Primary nav limited to 5-7 items
- [ ] Current location clearly indicated
- [ ] Breadcrumbs for deep hierarchies
- [ ] Mobile navigation pattern appropriate
- [ ] Keyboard navigation works
- [ ] ARIA attributes present
- [ ] Skip link provided
- [ ] Consistent across site
- [ ] Logo links to home
- [ ] Search easily accessible

### Pattern Selection Guide

| Scenario | Recommended Pattern |
|----------|-------------------|
| 5-7 main sections | Horizontal header nav |
| 10+ categories | Mega menu |
| Deep hierarchy | Sidebar + breadcrumbs |
| Settings/docs | Sidebar navigation |
| 3-5 parallel views | Tabs |
| Mobile app | Bottom tab bar |
| Mobile site | Hamburger menu |
| E-commerce | Mega menu + filters |

### Mobile-First Considerations

```
1. Essential destinations in tab bar
2. Everything else in hamburger
3. Search always accessible
4. Back gesture support
5. Sticky header for long pages
```

---

## Summary

**Good navigation = Clear wayfinding**

1. Answer the three questions on every page
2. Limit main navigation to 5-7 items
3. Use standard patterns users know
4. Always show current location
5. Make keyboard navigation work
6. Test navigation with real users

*If users have to think about navigation, you've already failed.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

