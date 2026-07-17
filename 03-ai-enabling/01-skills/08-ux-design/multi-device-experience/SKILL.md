---
last_updated: 2026-02-25
status: active
name: multi-device-experience
description: Design seamless experiences across devices - responsive, adaptive, and cross-device continuity. Use for responsive design and device transitions.
triggers:
  files: ["**/responsive/**", "**/mobile/**", "**/tablet/**", "**/breakpoint/**"]
  keywords: ["multi-device", "responsive", "mobile-first", "breakpoint", "cross-device", "adaptive", "device continuity", "touch", "screen size"]
allowed-tools: Read, Write, Edit
---

# Multi-Device Experience Skill

Master guide for designing experiences that work beautifully across all devices - from phones to desktops, with seamless transitions between them.

## Philosophy

**Users are device-fluid.** The same user might start on mobile, continue on tablet, and finish on desktop. Design for this journey, not for isolated devices.

**Context matters more than screen size.** Mobile isn't just small desktop. Users on mobile have different contexts, goals, and constraints.

**Parity, not duplication.** Users should be able to accomplish their goals on any device, but the experience can (and should) adapt.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Responsive Design Fundamentals

### Breakpoint Strategy

**Common breakpoints**:

```css
/* Mobile-first breakpoints */
/* Default: Mobile (< 640px) */

@media (min-width: 640px) {
  /* Tablet portrait */
}

@media (min-width: 768px) {
  /* Tablet landscape */
}

@media (min-width: 1024px) {
  /* Desktop */
}

@media (min-width: 1280px) {
  /* Large desktop */
}
```

**Breakpoint considerations**:

| Breakpoint | Width | Typical Use |
|------------|-------|-------------|
| Mobile | < 640px | Single column, touch |
| Tablet | 640-1024px | 2 columns, touch/mouse |
| Desktop | > 1024px | Multi-column, mouse |
| Large | > 1280px | Full features |

### Mobile-First Approach

Start with mobile, enhance for larger:

```css
/* Base (mobile) */
.card {
  width: 100%;
  padding: 1rem;
}

/* Enhanced (tablet+) */
@media (min-width: 768px) {
  .card {
    width: 50%;
    padding: 1.5rem;
  }
}

/* Enhanced (desktop+) */
@media (min-width: 1024px) {
  .card {
    width: 33.333%;
    padding: 2rem;
  }
}
```

---

## Layout Patterns

### Stack → Grid

Mobile: Single column
Desktop: Multi-column grid

```
Mobile:         Desktop:
┌────────┐      ┌────┐ ┌────┐ ┌────┐
│   A    │      │ A  │ │ B  │ │ C  │
├────────┤      └────┘ └────┘ └────┘
│   B    │
├────────┤
│   C    │
└────────┘
```

```css
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Sidebar Patterns

**Collapse to drawer**:
```
Desktop:              Mobile:
┌────┬───────────┐    ┌───────────┐
│Nav │  Content  │    │ ☰ Content │
│    │           │    │           │
│    │           │    └───────────┘
└────┴───────────┘
                      ┌───────────┐
                      │ Nav       │ ← Drawer
                      │ (overlay) │
                      └───────────┘
```

**Collapse to tabs**:
```
Desktop:              Mobile:
┌────┬───────────┐    ┌───────────┐
│Nav │  Content  │    │ Content   │
│    │           │    │           │
│    │           │    ├───────────┤
└────┴───────────┘    │ Tab Tab   │
                      └───────────┘
```

### Navigation Patterns

**Desktop: Horizontal nav**
```
┌────────────────────────────────────────┐
│ Logo   Home  Products  About   Contact │
└────────────────────────────────────────┘
```

**Mobile: Hamburger menu**
```
┌────────────────────────────────────────┐
│ Logo                              ☰    │
└────────────────────────────────────────┘
```

**Alternative: Bottom navigation (mobile)**
```
┌────────────────────────────────────────┐
│            Content                     │
├────────────────────────────────────────┤
│  Home   Search   Cart   Profile        │
└────────────────────────────────────────┘
```

---

## Touch vs Mouse

### Touch Targets

**Minimum sizes**:

| Platform | Minimum | Recommended |
|----------|---------|-------------|
| iOS | 44×44pt | 48×48pt |
| Android | 48×48dp | 56×56dp |
| Web | 44×44px | 48×48px |

```css
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
}
```

### Touch Considerations

**Thumb zones** (one-handed use):
```
┌────────────────────┐
│    Difficult       │
│                    │
│   Comfortable      │
│                    │
│     Easy           │
└────────────────────┘
      👍 (thumb)
```

**Design implications**:
- Primary actions in bottom zone
- Navigation at bottom (not top)
- Avoid top corners for frequent actions

### Hover States

Hover doesn't exist on touch:

```css
/* Desktop only hover */
@media (hover: hover) {
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
}

/* Touch: Use active state instead */
.card:active {
  transform: scale(0.98);
}
```

### Touch Gestures

Common gestures to support:

| Gesture | Action | Example |
|---------|--------|---------|
| Tap | Select/activate | Button click |
| Long press | Context menu | Additional options |
| Swipe horizontal | Navigate/dismiss | Delete, switch tabs |
| Swipe vertical | Scroll | List scrolling |
| Pull down | Refresh | Pull to refresh |
| Pinch | Zoom | Map, image |

---

## Typography Scaling

### Fluid Typography

Scale smoothly between breakpoints:

```css
/* Fluid font size */
html {
  font-size: clamp(14px, 2vw + 10px, 18px);
}

/* Or stepped scaling */
html {
  font-size: 14px;
}

@media (min-width: 768px) {
  html {
    font-size: 16px;
  }
}

@media (min-width: 1024px) {
  html {
    font-size: 18px;
  }
}
```

### Line Length

Optimize reading on all sizes:

```css
.content {
  max-width: 65ch; /* ~65 characters per line */
  padding: 0 1rem;
}
```

---

## Images and Media

### Responsive Images

```html
<picture>
  <source media="(min-width: 1024px)" srcset="large.jpg">
  <source media="(min-width: 640px)" srcset="medium.jpg">
  <img src="small.jpg" alt="Description">
</picture>
```

### Art Direction

Different crops for different devices:

```
Desktop: Landscape hero
┌────────────────────────────────────────┐
│          Person in context             │
└────────────────────────────────────────┘

Mobile: Portrait crop
┌────────────┐
│            │
│   Person   │
│   closeup  │
│            │
└────────────┘
```

### Video Considerations

```css
/* Responsive video container */
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 ratio */
  height: 0;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

---

## Cross-Device Continuity

### State Synchronization

Allow users to continue across devices:

```
Start on mobile → Continue on desktop

┌──────────────┐    ┌────────────────────────┐
│ Cart: 3 items│ →  │ Cart: 3 items          │
│ [Checkout]   │    │ [Continue to checkout] │
└──────────────┘    └────────────────────────┘
```

**Implementation**:
- Sync cart state
- Sync form progress
- Sync reading position
- Sync preferences

### Handoff Patterns

**Email continuation**:
```
┌────────────────────────────────────────┐
│ Continue on desktop?                   │
│                                        │
│ [Send link to email]                   │
└────────────────────────────────────────┘
```

**QR code continuation**:
```
┌────────────────────────────────────────┐
│ Mobile:          Desktop:              │
│                  ┌──────┐              │
│ [Continue]  →    │ QR   │              │
│                  │ code │              │
│                  └──────┘              │
│                  Scan to continue      │
└────────────────────────────────────────┘
```

### Account-Based Sync

```
Logged in anywhere → State follows

Mobile session:
- Draft email saved
- Cart updated
- Preferences set

Desktop session:
- Same draft available
- Same cart items
- Same preferences applied
```

---

## Performance by Device

### Mobile Performance

Mobile networks are often slower:

| Optimization | Technique |
|--------------|-----------|
| Images | Lazy load, WebP, responsive |
| Fonts | System fonts or subset |
| JavaScript | Code splitting, defer |
| CSS | Critical CSS inline |
| Requests | Minimize, combine |

### Conditional Loading

Load features based on device:

```javascript
// Only load heavy features on desktop
if (window.matchMedia('(min-width: 1024px)').matches) {
  import('./heavy-feature.js');
}
```

### Offline Support

More critical on mobile:

```javascript
// Service worker for offline
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

---

## Device-Specific Features

### Mobile-Only

| Feature | Use Case |
|---------|----------|
| Camera | Scanning, upload |
| GPS | Location services |
| Haptics | Feedback |
| Touch ID/Face ID | Authentication |
| Share sheet | Native sharing |

### Desktop-Only

| Feature | Use Case |
|---------|----------|
| Keyboard shortcuts | Power users |
| Right-click context | Quick actions |
| Drag and drop | File upload, reorder |
| Multi-window | Side-by-side work |
| Hover previews | Quick info |

### Progressive Enhancement

```javascript
// Feature detection
if ('geolocation' in navigator) {
  showLocationFeature();
} else {
  showManualAddressInput();
}

if ('share' in navigator) {
  showNativeShare();
} else {
  showCopyLink();
}
```

---

## Testing Strategy

### Device Testing Matrix

| Device Type | Priority | Testing Method |
|-------------|----------|----------------|
| Top 3 mobile | Critical | Real devices |
| iOS/Android | High | Real devices |
| Tablets | Medium | Real + emulation |
| Desktop browsers | High | Real browsers |
| Edge cases | Low | Emulation |

### Responsive Testing

```javascript
// Breakpoint visualization (dev only)
const breakpoint = document.createElement('div');
breakpoint.style.cssText = `
  position: fixed;
  bottom: 0;
  right: 0;
  padding: 4px 8px;
  background: black;
  color: white;
  font-size: 12px;
`;

function updateBreakpoint() {
  const width = window.innerWidth;
  breakpoint.textContent =
    width < 640 ? 'Mobile' :
    width < 1024 ? 'Tablet' : 'Desktop';
}

window.addEventListener('resize', updateBreakpoint);
updateBreakpoint();
document.body.appendChild(breakpoint);
```

---

## Anti-Patterns

### 1. Desktop-First Design

```
❌ Bad: Desktop first, squeeze for mobile
✅ Good: Mobile first, enhance for desktop
```

### 2. Hiding Content on Mobile

```
❌ Bad: "View full site" link
Mobile users deserve full functionality

✅ Good: Adapted but complete experience
Same features, optimized presentation
```

### 3. Fixed Viewport

```
❌ Bad:
<meta name="viewport" content="width=1024">

✅ Good:
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### 4. Tiny Touch Targets

```
❌ Bad: 20×20px buttons
✅ Good: 44×44px minimum
```

### 5. Assuming Mouse

```
❌ Bad: Hover-only interactions
✅ Good: Touch + mouse supported
```

### 6. Blocking Zoom

```
❌ Bad:
<meta name="viewport" content="user-scalable=no">

✅ Good:
Allow users to zoom for accessibility
```

---

## Quick Reference

### Responsive Checklist

- [ ] Mobile-first approach
- [ ] Fluid layouts (no fixed widths)
- [ ] Touch targets ≥ 44px
- [ ] Readable text without zoom
- [ ] No horizontal scroll
- [ ] Images scale properly
- [ ] Navigation works on all sizes
- [ ] Forms are usable on mobile
- [ ] Performance optimized for mobile
- [ ] Tested on real devices

### Breakpoint Quick Guide

```css
/* Mobile: default */
/* Tablet: min-width: 640px */
/* Desktop: min-width: 1024px */
/* Large: min-width: 1280px */
```

### Touch vs Click

| Mouse | Touch |
|-------|-------|
| Click | Tap |
| Double-click | Double-tap |
| Right-click | Long press |
| Hover | (None - use tap) |
| Drag | Touch drag |
| Scroll wheel | Swipe |

---

## Summary

**Design for the journey, not the device.**

1. Start mobile-first
2. Make touch targets generous (44px+)
3. Adapt layouts, not just shrink
4. Support device transitions
5. Test on real devices
6. Optimize performance for mobile

*Great multi-device experiences feel native everywhere.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

