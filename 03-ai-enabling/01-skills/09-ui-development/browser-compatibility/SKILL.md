---
last_updated: 2026-02-25
status: active
name: browser-compatibility
description: Cross-browser CSS compatibility - feature detection, fallbacks, vendor prefixes, progressive enhancement. Use when ensuring styles work across all browsers.
triggers:
  files: ["**/*.css", "**/*.scss", "**/*.tsx", "**/*.jsx", "**/browserslist*"]
  keywords: ["browser compatibility", "cross-browser", "@supports", "vendor prefix", "fallback", "polyfill", "progressive enhancement", "feature detection"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Browser Compatibility

Build CSS that works reliably across all browsers with graceful degradation.

## Browser Support Strategy

| Strategy | Approach | Use Case |
|----------|----------|----------|
| **Progressive Enhancement** | Start simple, enhance for modern | General best practice |
| **Graceful Degradation** | Build modern, add fallbacks | Modern-first apps |
| **Feature Detection** | Check support before using | Specific features |
| **Polyfills** | Add missing functionality | Critical features |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Feature Detection with @supports

### Basic Usage

```css
/* Fallback for all browsers */
.element {
  display: block;
}

/* Enhanced for browsers with grid support */
@supports (display: grid) {
  .element {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

/* Multiple conditions */
@supports (display: grid) and (gap: 1rem) {
  .element {
    display: grid;
    gap: 1rem;
  }
}

/* Negation */
@supports not (display: grid) {
  .element {
    /* Flexbox fallback */
    display: flex;
    flex-wrap: wrap;
  }
}
```

### Common Feature Queries

```css
/* CSS Grid */
@supports (display: grid) { }

/* Flexbox gap */
@supports (gap: 1rem) { }

/* CSS Custom Properties */
@supports (--custom: value) { }

/* Aspect ratio */
@supports (aspect-ratio: 16/9) { }

/* Container queries */
@supports (container-type: inline-size) { }

/* Subgrid */
@supports (grid-template-columns: subgrid) { }

/* Has selector */
@supports selector(:has(*)) { }

/* Individual transform properties */
@supports (translate: 0) { }
```

## Fallback Patterns

### Color Fallbacks

```css
/* Fallback then modern */
.element {
  /* Fallback for older browsers */
  background: #0066cc;
  /* Modern color function */
  background: oklch(59% 0.15 250);
}

/* With @supports */
.element {
  background: #0066cc;
}

@supports (background: oklch(0% 0 0)) {
  .element {
    background: oklch(59% 0.15 250);
  }
}
```

### Layout Fallbacks

```css
/* Float fallback for grid */
.card-grid {
  overflow: hidden; /* Clearfix */
}

.card {
  float: left;
  width: 33.333%;
  padding: 1rem;
  box-sizing: border-box;
}

@supports (display: grid) {
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    overflow: visible;
  }

  .card {
    float: none;
    width: auto;
    padding: 0;
  }
}
```

### Flexbox Gap Fallback

```css
/* Margin-based fallback */
.flex-container {
  display: flex;
  flex-wrap: wrap;
  margin: -0.5rem; /* Negative margin */
}

.flex-item {
  margin: 0.5rem; /* Gap simulation */
}

/* Modern gap */
@supports (gap: 1rem) {
  .flex-container {
    gap: 1rem;
    margin: 0;
  }

  .flex-item {
    margin: 0;
  }
}
```

### Aspect Ratio Fallback

```css
/* Padding-based fallback */
.video-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0;
}

.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Modern aspect-ratio */
@supports (aspect-ratio: 16/9) {
  .video-wrapper {
    aspect-ratio: 16/9;
    padding-bottom: 0;
    height: auto;
  }

  .video-wrapper iframe {
    position: static;
  }
}
```

## Vendor Prefixes

### When Still Needed

```css
/* Still need prefixes (2024) */
.element {
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);

  -webkit-text-stroke: 1px black;

  -webkit-mask-image: url(mask.svg);
  mask-image: url(mask.svg);
}

/* Appearance reset */
button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

/* Scrollbar styling */
.scrollable {
  scrollbar-width: thin; /* Firefox */
}

.scrollable::-webkit-scrollbar {
  width: 8px; /* Chrome, Safari */
}
```

### Autoprefixer (Recommended)

```js
// postcss.config.js
module.exports = {
  plugins: [
    require('autoprefixer')({
      // Uses browserslist config
    }),
  ],
};

// package.json or .browserslistrc
{
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead"
  ]
}
```

## JavaScript Feature Detection

### CSS.supports API

```tsx
// Check CSS support in JavaScript
const supportsGrid = CSS.supports('display', 'grid');
const supportsGap = CSS.supports('gap', '1rem');
const supportsContainerQueries = CSS.supports('container-type', 'inline-size');

// React hook
function useCSSSupport(property: string, value: string) {
  const [supported, setSupported] = useState(false);

  useEffect(() => {
    setSupported(CSS.supports(property, value));
  }, [property, value]);

  return supported;
}

// Usage
function Layout() {
  const supportsSubgrid = useCSSSupport('grid-template-columns', 'subgrid');

  return (
    <div className={supportsSubgrid ? 'subgrid-layout' : 'fallback-layout'}>
      {/* content */}
    </div>
  );
}
```

### Modernizr Alternative

```tsx
// Custom feature detection
const features = {
  grid: CSS.supports('display', 'grid'),
  flexGap: CSS.supports('gap', '1rem'),
  containerQueries: CSS.supports('container-type', 'inline-size'),
  has: CSS.supports('selector(:has(*))'),
};

// Add classes to document
Object.entries(features).forEach(([feature, supported]) => {
  document.documentElement.classList.add(
    supported ? feature : `no-${feature}`
  );
});
```

```css
/* Use feature classes */
.no-grid .element {
  /* Fallback styles */
}

.grid .element {
  /* Grid styles */
}
```

## Progressive Enhancement Examples

### Navigation Menu

```css
/* Base: works everywhere */
.nav {
  list-style: none;
  padding: 0;
}

.nav-item {
  display: block;
  padding: 0.5rem 1rem;
}

/* Enhanced: flexbox */
@supports (display: flex) {
  .nav {
    display: flex;
    gap: 0;
  }

  .nav-item {
    display: inline-block;
  }
}

/* Enhanced: gap */
@supports (gap: 1rem) {
  .nav {
    gap: 1rem;
  }
}
```

### Card Component

```css
/* Level 1: Basic styling (all browsers) */
.card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
}

/* Level 2: Rounded corners */
@supports (border-radius: 0.5rem) {
  .card {
    border-radius: 0.5rem;
  }
}

/* Level 3: Box shadow */
@supports (box-shadow: 0 0 0 black) {
  .card {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: none;
  }
}

/* Level 4: Modern color */
@supports (background: oklch(0% 0 0)) {
  .card {
    background: oklch(99% 0.01 250);
  }
}
```

## Browser-Specific Fixes

### Safari Flexbox Bugs

```css
/* Safari flexbox height fix */
.flex-container {
  display: flex;
  flex-direction: column;
  /* Safari needs explicit height */
  height: 100%;
}

/* Safari gap fallback */
.safari-fix > * + * {
  margin-top: 1rem;
}

@supports (gap: 1rem) {
  .safari-fix {
    gap: 1rem;
  }
  .safari-fix > * + * {
    margin-top: 0;
  }
}
```

### iOS Input Zoom

```css
/* Prevent zoom on iOS inputs */
input, select, textarea {
  font-size: 16px; /* Minimum to prevent zoom */
}

/* Or use max() */
input {
  font-size: max(16px, 1rem);
}
```

### Firefox Scrollbar

```css
/* Firefox uses scrollbar-* properties */
.scrollable {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

/* WebKit browsers use pseudo-elements */
.scrollable::-webkit-scrollbar {
  width: 8px;
}

.scrollable::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.scrollable::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
```

## Testing Strategy

### Manual Testing Checklist

| Browser | Version | Platform |
|---------|---------|----------|
| Chrome | Latest, Latest-1 | Win, Mac |
| Firefox | Latest, Latest-1 | Win, Mac |
| Safari | Latest | Mac, iOS |
| Edge | Latest | Win |
| Samsung Internet | Latest | Android |

### Automated Testing

```js
// BrowserStack/Sauce Labs config
module.exports = {
  browsers: [
    { browserName: 'chrome', browserVersion: 'latest' },
    { browserName: 'firefox', browserVersion: 'latest' },
    { browserName: 'safari', browserVersion: '16' },
    { browserName: 'edge', browserVersion: 'latest' },
  ],
};
```

### Can I Use Integration

```bash
# Install
npm install caniuse-lite browserslist

# Check support
npx browserslist "> 1%, last 2 versions, not dead"

# Update database
npx update-browserslist-db@latest
```

## Best Practices

| Practice | Rationale |
|----------|-----------|
| Start with working fallback | Base functionality for all |
| Enhance with @supports | Feature detection over UA sniffing |
| Use autoprefixer | Automated vendor prefixes |
| Test on real devices | Emulators miss issues |
| Document browser support | Set expectations |
| Progressive enhancement | Accessible to all |

## Quick Reference

```css
/* Feature detection */
@supports (property: value) { }
@supports not (property: value) { }
@supports (a: b) and (c: d) { }
@supports (a: b) or (c: d) { }
@supports selector(:has(*)) { }

/* Fallback pattern */
.element {
  /* Fallback */
  property: old-value;
  /* Modern */
  property: new-value;
}

/* Common fallbacks needed */
aspect-ratio → padding-bottom trick
gap (flex) → margin
grid → flexbox/float
oklch/lch → hex/rgba
container queries → media queries
:has() → JavaScript

/* JavaScript detection */
CSS.supports('property', 'value')
CSS.supports('(property: value)')
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

