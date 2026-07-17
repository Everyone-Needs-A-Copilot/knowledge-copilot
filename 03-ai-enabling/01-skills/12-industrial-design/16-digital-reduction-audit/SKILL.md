---
last_updated: 2026-02-25
status: active
name: digital-reduction-audit
description: Audit patterns for reducing complexity and simplifying digital products. Use when evaluating features to remove, simplifying interfaces, or applying minimalist design principles.
category: industrial-design-digital
keywords:
  - reduction
  - simplicity
  - minimalism
  - feature-audit
  - subtract
triggers:
  keywords:
    - too complex
    - simplify
    - reduce features
    - remove clutter
    - minimal interface
  filePatterns:
    - "**/*.tsx"
    - "**/components/**"
    - "**/routes/**"
allowed-tools: Read, Write, Edit
---

# Digital Reduction Audit

Subtract features and UI elements until function breaks.

## Philosophy

"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away." Every feature, button, field, option, and animation must pass the removal test. Delete it. Does function break? No? It was decoration. Keep deleting.

**Rams Principle 10 (As little design as possible):** Back to purity, back to simplicity.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Methodology

### Step 1: Inventory Everything

Create complete list of elements:

```typescript
interface UIInventory {
  features: Feature[];        // Every feature
  screens: Screen[];          // Every screen/route
  components: Component[];    // Every UI component
  fields: Field[];            // Every form field
  actions: Action[];          // Every button/link
  options: Option[];          // Every setting/config
  animations: Animation[];    // Every transition
  notifications: Notice[];    // Every alert/toast
}
```

### Step 2: The Removal Test

For each element, execute:

```typescript
async function removalTest(element: UIElement): Promise<Decision> {
  // 1. Remove it
  const removed = await remove(element);

  // 2. Test core function
  const coreStillWorks = await testCoreFunction();

  if (!coreStillWorks) {
    // Function broke → element is necessary
    await restore(element);
    return { keep: true, reason: 'Core function requires this' };
  }

  // 3. Test user can complete job
  const jobCompletable = await testJobCompletion();

  if (!jobCompletable) {
    // Job can't be done → element is necessary
    await restore(element);
    return { keep: true, reason: 'Job requires this' };
  }

  // Function works without it → element was decoration
  return { keep: false, reason: 'Not necessary' };
}
```

### Step 3: Merge Consolidation

After removal test, consolidate survivors:

| Before | After | Why |
|--------|-------|-----|
| Edit button + Actions menu | Actions menu only | Edit is an action |
| Save + Save & Close buttons | Save button (auto-close) | One action, one button |
| Name field + Display name field | Name field | Don't ask twice |
| Light/Dark/Auto theme | Light/Dark (detect auto) | Reduce choice |

### Step 4: Information Hierarchy

What remains must be layered:

```typescript
interface InformationLayer {
  critical: Element[];     // Always visible, <5 items
  primary: Element[];      // Visible by default, <10 items
  secondary: Element[];    // Collapsed/expandable
  tertiary: Element[];     // Advanced/Settings
}

// Rule: Move elements down, never up
// If user never expands "Advanced", those features weren't needed
```

### Step 5: Default Elimination

Every configurable option is a decision burden:

```typescript
// BEFORE: 8 decisions
interface Config {
  theme: 'light' | 'dark' | 'auto';
  density: 'compact' | 'comfortable' | 'spacious';
  sortOrder: 'asc' | 'desc';
  pageSize: 10 | 25 | 50 | 100;
  showImages: boolean;
  showDates: boolean;
  animationSpeed: 'slow' | 'normal' | 'fast';
  confirmDeletes: boolean;
}

// AFTER: 0 decisions, smart defaults
interface Config {
  theme: 'auto';           // Detect system preference
  density: 'comfortable';  // Research-backed default
  sortOrder: 'desc';       // Newest first (temporal data)
  pageSize: 25;            // Balance performance/scrolling
  showImages: true;        // Content is visual
  showDates: true;         // Temporal context matters
  animationSpeed: 'fast';  // <200ms transitions
  confirmDeletes: true;    // Destructive actions always confirm
}
// User can't configure → no decisions → faster
```

## Tests

| Test | Pass Criteria | Fail Criteria |
|------|---------------|---------------|
| **Removal Test** | Core function works without element | Element required for core function |
| **Job Completion** | User completes job without element | Job impossible without element |
| **One Path** | Single clear path to goal | Multiple ways to do same thing |
| **No Dead Code** | All code executed in normal use | Features never used |
| **Default Sufficiency** | Default config works for 95% of users | Customization required |

## Anti-Patterns

| Anti-Pattern | Why Wrong | Alternative |
|--------------|-----------|-------------|
| **Feature parity** | "Competitor has it" ≠ necessary | Only add if job requires |
| **Power user syndrome** | Optimizing for 1% of users | Optimize for 95%, hide advanced |
| **Customization theater** | Options that don't matter | Remove options, set smart defaults |
| **Multiple paths** | Edit button + right-click + menu | One path to each action |
| **Defensive features** | "Some user might need..." | Wait for evidence |
| **Settings creep** | Every decision = setting | Research best answer, make it default |

## Examples

### Good Example

```typescript
// Insights list: Reduced to essence
export function InsightsList() {
  const { insights } = useInsights();

  return (
    <div className="space-y-2">
      {insights.map(insight => (
        <InsightCard
          key={insight.id}
          insight={insight}
          // No: onEdit, onDelete, onDuplicate, onShare, onExport
          // User clicks card → opens insight → actions there
        />
      ))}
    </div>
  );
}

// Insight card: One action
function InsightCard({ insight }: { insight: Insight }) {
  return (
    <Link href={`/insights/${insight.id}`}>  {/* One path */}
      <div className="p-4 border rounded hover:border-blue-500">
        <h3>{insight.title}</h3>
        <p className="text-sm text-gray-600">{insight.summary}</p>
        {/* No: buttons, icons, badges, counts, dates */}
        {/* Opens → user sees full detail */}
      </div>
    </Link>
  );
}

// Settings: Removed
// No theme picker (auto-detect)
// No density options (one correct density)
// No sort options (newest first is correct)
```

### Bad Example

```typescript
// Insights list: Feature bloat
export function InsightsList() {
  const { insights, view, setView, sort, setSort, filters, setFilters } = useInsights();

  return (
    <div>
      {/* Toolbar: 8 controls */}
      <div className="flex gap-2 mb-4">
        <ViewToggle value={view} onChange={setView} />  {/* Grid/List */}
        <SortDropdown value={sort} onChange={setSort} />  {/* 5 options */}
        <FilterMenu filters={filters} onChange={setFilters} />  {/* 12 filters */}
        <ColumnPicker />  {/* Which columns to show */}
        <DensityToggle />  {/* Compact/Normal/Spacious */}
        <RefreshButton />  {/* Auto-refresh exists */}
        <ExportButton />  {/* Who exports lists? */}
        <HelpButton />  {/* If needed, UI failed */}
      </div>

      {insights.map(insight => (
        <InsightCard
          key={insight.id}
          insight={insight}
          // 6 actions per card
          onView={() => {}}
          onEdit={() => {}}
          onDelete={() => {}}
          onDuplicate={() => {}}
          onShare={() => {}}
          onExport={() => {}}
        />
      ))}
    </div>
  );
}

// Remove toolbar → list still works
// Remove 5 of 6 actions → jobs still completable
// Failed removal test
```

## Implementation Checklist

- [ ] Complete UI inventory created
- [ ] Removal test executed on every element
- [ ] Core function verified without each element
- [ ] Job completion tested without each element
- [ ] Multiple paths to same action consolidated
- [ ] Settings reduced to <5 options
- [ ] Smart defaults replace customization
- [ ] Advanced features moved to tertiary layer
- [ ] Usage analytics confirm all features used
- [ ] "Advanced" section exists for <5% edge cases


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

