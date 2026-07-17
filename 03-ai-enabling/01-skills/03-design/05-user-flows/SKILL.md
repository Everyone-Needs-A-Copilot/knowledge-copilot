---
last_updated: 2026-02-25
status: active
name: user-flows
description: Task analysis and information architecture - wireframes, user journeys, navigation. Use for UX design.
triggers:
  files: ["**/flows/**", "**/wireframes/**", "**/ux/**"]
  keywords: ["user flow", "wireframe", "information architecture", "navigation", "task flow", "user journey", "sitemap", "IA"]
allowed-tools: Read, Write, Edit
---

# User Flows & Information Architecture

Comprehensive guide to designing, documenting, and testing user flows, task analysis, information architecture, and navigation patterns.

## Table of Contents

1. [Foundations](#foundations)
2. [User Flow Diagramming](#user-flow-diagramming)
3. [Task Analysis](#task-analysis)
4. [Information Architecture Principles](#information-architecture-principles)
5. [Navigation Patterns](#navigation-patterns)
6. [Wireframing Techniques](#wireframing-techniques)
7. [Progressive Disclosure](#progressive-disclosure)
8. [Form Design Flows](#form-design-flows)
9. [Error Recovery Paths](#error-recovery-paths)
10. [Onboarding Flows](#onboarding-flows)
11. [Multi-Step Process Design](#multi-step-process-design)
12. [Mobile Navigation Patterns](#mobile-navigation-patterns)
13. [Testing User Flows](#testing-user-flows)
14. [Anti-Patterns](#anti-patterns)

---


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Foundations

### Core Principles

**1. User-Centered Design**
- Start with user goals, not system capabilities
- Map to real-world mental models
- Minimize cognitive load at each decision point
- Provide clear feedback at every step

**2. Task Efficiency**
- Minimize steps to completion
- Reduce decision fatigue
- Support both novice and expert paths
- Enable shortcuts for frequent tasks

**3. Context Awareness**
- Preserve context across steps
- Show progress and location
- Enable easy backtracking
- Maintain state appropriately

**4. Error Prevention & Recovery**
- Design to prevent errors
- Make errors reversible
- Provide clear recovery paths
- Learn from failure patterns

### The User Flow Stack

```
┌─────────────────────────────────────┐
│    User Goals & Mental Models       │  Strategy Layer
├─────────────────────────────────────┤
│    Information Architecture         │  Structure Layer
├─────────────────────────────────────┤
│    Navigation Systems               │  Wayfinding Layer
├─────────────────────────────────────┤
│    Task Flows & Sequences           │  Interaction Layer
├─────────────────────────────────────┤
│    Wireframes & Screen States       │  Interface Layer
└─────────────────────────────────────┘
```

### Flow Design Philosophy

**Progressive Reduction**
- Start with complete context
- Progressively focus attention
- Reduce options as commitment increases
- Provide summary before final action

**Graceful Degradation**
- Support partial completion
- Save progress automatically
- Enable resume from interruption
- Provide offline capabilities where possible

**Accessibility Integration**
- Keyboard navigation throughout
- Screen reader friendly flow
- Clear focus indicators
- Logical tab order

---

## User Flow Diagramming

### Flow Diagram Types

**1. Task Flow**
Single path, single user, linear sequence:
```
[Start] → [Step 1] → [Decision] → [Step 2] → [End]
```

**2. User Flow**
Multiple paths, single user type, includes decisions:
```
[Entry] → [Action] → {Decision?}
                        ├─ Yes → [Path A] → [End]
                        └─ No  → [Path B] → [End]
```

**3. Workflow**
Multiple users, complex interactions:
```
[User A: Submit] → [System: Process] → [User B: Review]
                                            ├─ Approve → [Complete]
                                            └─ Reject  → [User A: Revise]
```

### Flow Diagram Notation

**Standard Symbols**
```
┌──────────┐
│  Screen  │  Rectangular box = UI screen/page
└──────────┘

   (Action)   Rounded rectangle = User action

  {Decision?} Diamond = Decision point

──────────>   Arrow = Flow direction

  ((System))  Double parentheses = System action

  [[ Note ]]  Double brackets = Annotation
```

**Complete Flow Example**
```
┌─────────────┐
│   Landing   │
└──────┬──────┘
       │
       v
   (Click CTA)
       │
       v
  {Logged in?}
   ├─ Yes ──> ┌──────────┐
   │          │Dashboard │
   │          └──────────┘
   │
   └─ No ──> ┌──────────┐
             │  Sign Up │
             └────┬─────┘
                  │
                  v
            ((Create Account))
                  │
                  v
             ((Send Email))
                  │
                  v
          {Email Verified?}
           ├─ Yes ──> ┌──────────┐
           │          │Dashboard │
           │          └──────────┘
           │
           └─ No ──> ┌──────────────┐
                     │Check Email   │
                     │Resend Option │
                     └──────────────┘
```

### Flow States to Document

**Entry Points**
- Direct URL access
- Navigation click
- External link
- Deep link (mobile)
- Email link
- Search result
- Notification tap

**Exit Points**
- Task completion
- User abandonment
- Error termination
- Session timeout
- External redirect
- App close (mobile)

**Intermediate States**
- Loading/processing
- Validation feedback
- Confirmation dialogs
- Progress indicators
- Empty states
- Partial data states

### Flow Documentation Template

```markdown
## Flow Name: [Task Name]

**Goal**: [What user wants to accomplish]

**Entry Points**:
- [List all ways to enter this flow]

**Success Criteria**:
- [Observable outcome that defines success]

**Flow Diagram**:
[Insert diagram]

**Screen Details**:

### 1. [Screen Name]
- **Purpose**: [Why this screen exists]
- **Key Elements**: [Critical UI components]
- **User Actions**: [Available interactions]
- **Validation**: [Rules applied]
- **Next Steps**: [Where user can go]

### 2. [Next Screen]
...

**Edge Cases**:
- [Scenario] → [Handling approach]

**Error Paths**:
- [Error type] → [Recovery flow]

**Analytics**:
- Track: [Key events to measure]
- Success metric: [How to measure completion]
- Drop-off points: [Where to monitor abandonment]
```

---

## Task Analysis

### Hierarchical Task Analysis (HTA)

Break down complex tasks into hierarchical subtasks:

```
0. Book a Flight
   1. Search for Flights
      1.1 Enter departure city
      1.2 Enter destination city
      1.3 Select departure date
      1.4 Select return date
      1.5 Specify passengers
      1.6 Submit search
   2. Review Results
      2.1 Filter by price
      2.2 Filter by duration
      2.3 Sort results
      2.4 Compare options
   3. Select Flight
      3.1 Review flight details
      3.2 Choose seat
      3.3 Add to cart
   4. Complete Booking
      4.1 Enter passenger details
      4.2 Add baggage
      4.3 Enter payment
      4.4 Confirm booking
```

**HTA Notation**:
- **Plan**: Describes order/conditions (sequential, parallel, conditional)
- **Operation**: Lowest level action
- **Subordinate goal**: Task requiring further decomposition

### Task Analysis Framework

**1. Task Identification**
```yaml
Task: Update profile picture
Frequency: Occasional (once per year)
Importance: Medium
User Type: All authenticated users
Context: Settings section
Trigger: User decision, onboarding prompt
```

**2. Task Decomposition**
```yaml
Main Steps:
  - Navigate to settings
  - Access profile section
  - Upload new image
  - Crop/adjust image
  - Save changes

Prerequisites:
  - User must be logged in
  - Image file must be available
  - Image must meet size/format requirements

Dependencies:
  - File upload system
  - Image processing service
  - Storage service
```

**3. Cognitive Walkthrough**

For each step, answer:
- **Will users know what to do?** (Affordance clarity)
- **Can users see how to do it?** (Visibility)
- **Will users recognize progress?** (Feedback)
- **Will users understand outcome?** (Confirmation)

**Example**:
```
Step: Upload new image

Q: Will users know what to do?
A: Yes, if button says "Upload Photo" or shows camera icon
   No, if button says "Update" without context

Q: Can users see how to do it?
A: Yes, if button is prominent and labeled
   No, if hidden in dropdown menu

Q: Will users recognize progress?
A: Yes, if upload progress bar shown
   No, if no feedback during upload

Q: Will users understand outcome?
A: Yes, if preview updates and confirmation shown
   No, if page just refreshes without message
```

### Task Complexity Metrics

**Simple Task** (1-3 steps, 0-1 decisions):
- Click button → Confirm → Done
- Example: Delete item, Like post

**Medium Task** (4-7 steps, 2-4 decisions):
- Navigate → Input → Validate → Review → Confirm
- Example: Update settings, Send message

**Complex Task** (8+ steps, 5+ decisions):
- Multiple screens, branching paths, validation points
- Example: Checkout process, Application form

**Task Complexity Score**:
```
Score = Steps + (Decisions × 2) + (Inputs × 1.5) + (External dependencies × 3)

< 10 = Simple
10-25 = Medium
> 25 = Complex (consider breaking down)
```

### Task Frequency vs. Importance Matrix

```
High Importance
     ↑
     │  Streamline        Optimize
     │  Make visible      Provide shortcuts
     │  Reduce friction   Expert paths
     │
     │  Monitor           Adequate
     │  Improve on        Don't over-invest
     │  data
     └──────────────────────────> High Frequency
   Low
```

**Design Implications**:
- **High frequency + High importance**: Primary navigation, prominent placement, keyboard shortcuts
- **High frequency + Low importance**: Efficient but not prominent, batch operations
- **Low frequency + High importance**: Guided flows, clear instructions, safety checks
- **Low frequency + Low importance**: Secondary navigation, help system

---

## Information Architecture Principles

### Core IA Concepts

**1. Organization Schemes**

**Exact Organization** (objective, unambiguous):
- **Alphabetical**: Directory, glossary, index
- **Chronological**: Timeline, activity feed, version history
- **Geographical**: Store locator, regional content
- **Format**: Documents, videos, images

**Ambiguous Organization** (subjective, interpretive):
- **Topic/Category**: News sections, product categories
- **Task**: "Book a trip", "File taxes", "Learn to code"
- **Audience**: "For students", "For businesses"
- **Metaphor**: Desktop, folders, shopping cart

**2. Organization Structures**

**Hierarchy** (tree structure):
```
                    Home
                     |
        ┌───────────┼───────────┐
     Products    Services    About
        |           |           |
    ┌───┴───┐   ┌──┴──┐    ┌───┴───┐
  Phones Laptops Web  App  Team  History
```
- Best for: Content-heavy sites, clear categories
- Pros: Familiar, scalable, SEO-friendly
- Cons: Can be rigid, deep navigation

**Database** (faceted):
```
Products filtered by:
├─ Category: [Laptops]
├─ Brand: [Apple, Dell, HP]
├─ Price: [$500-$1000]
└─ Rating: [4+ stars]
```
- Best for: E-commerce, search results, catalogs
- Pros: Flexible, powerful filtering
- Cons: Requires metadata, can overwhelm

**Hypertext** (web/network):
```
Article ←→ Related Article
   ↓           ↓
 Author    Category
   ↓           ↓
Other      Similar
Posts      Content
```
- Best for: Knowledge bases, wikis, documentation
- Pros: Natural discovery, contextual
- Cons: Can disorient, requires good navigation

**Linear** (sequence):
```
Step 1 → Step 2 → Step 3 → Step 4 → Complete
```
- Best for: Onboarding, checkout, setup wizards
- Pros: Clear progress, focused
- Cons: Inflexible, can't skip ahead easily

### Content Grouping Methods

**Card Sorting**

Open card sort (users create categories):
```
Cards: [Feature A, Feature B, Feature C, ...]
Users create groups and name them

Results:
Group "Core Tools": [Feature A, Feature C, Feature G]
Group "Advanced": [Feature B, Feature E]
Group "Settings": [Feature D, Feature F]
```

Closed card sort (predefined categories):
```
Categories: [Tools, Reports, Settings]
Users place cards into categories

Results show agreement/disagreement on placement
```

**Affinity Mapping**

1. Individual ideas on sticky notes
2. Group similar concepts
3. Create hierarchy of themes
4. Label groups
5. Identify patterns

### Navigation Depth vs. Breadth

**Depth Trade-offs**:
```
Deep (Narrow):
Home → Category → Subcategory → Sub-subcategory → Content

Pros: Fewer choices per level
Cons: More clicks, can get lost

Shallow (Wide):
Home → [20 categories shown] → Content

Pros: Fewer clicks
Cons: Overwhelming choice, harder to scan
```

**The 3-Click Rule** (myth but useful guideline):
- Users should reach any content in ~3 clicks
- Reality: Clear path matters more than click count
- Focus on making each step obvious

**Optimal depth**: 2-4 levels for most content
- Level 1: Home/Main sections
- Level 2: Categories
- Level 3: Subcategories
- Level 4: Content

### Information Scent

Users follow "scent" (cues that content is relevant):

**Strong scent**:
- Link text matches user's goal
- Preview shows relevant content
- Breadcrumbs confirm location
- Progress indicators show advancement

**Weak scent**:
- Generic labels ("Click here", "More")
- Unexpected destinations
- Unclear hierarchy
- Ambiguous icons

**Design for scent**:
```
Poor: Click here for more → Generic page
Good: View pricing plans → /pricing with clear options

Poor: Resources → Huge list of everything
Good: Resources → [Guides, Templates, Videos, Case Studies]

Poor: [Settings icon] → ???
Good: [Settings icon] + "Account Settings" → Expected settings
```

### Labeling Systems

**Types of Labels**:
- **Contextual links**: Within content ("Learn more about X")
- **Headings**: Section titles
- **Navigation**: Menu items, tabs
- **Index terms**: Tags, keywords
- **Iconic**: Visual representation

**Labeling Principles**:

1. **Consistency**: Same term for same concept
   - Don't mix "Delete" and "Remove"
   - Don't switch between "Settings" and "Preferences"

2. **Clarity**: Avoid jargon unless audience-specific
   - Technical docs can use technical terms
   - Consumer apps should use plain language

3. **Specificity**: Descriptive, not generic
   - "Export as CSV" not "Export"
   - "Email Preferences" not "Settings"

4. **User language**: Match mental models
   - Test with actual users
   - Monitor search terms and support questions
   - Use analytics to find confusion points

**Labeling Template**:
```yaml
Label: [Display text]
Alternatives considered: [Other options]
Context: [Where it appears]
Destination: [What happens on interaction]
Rationale: [Why this label was chosen]
```

### Metadata & Taxonomies

**Metadata Structure**:
```yaml
Content Item:
  title: "Complete Guide to User Flows"
  type: article
  category: UX Design
  subcategory: Information Architecture
  tags: [user flows, wireframes, IA]
  difficulty: intermediate
  read_time: 15 minutes
  author: UX Team
  published: 2026-01-14
  updated: 2026-01-14
  related_content: [id1, id2, id3]
```

**Controlled Vocabulary**:
- Maintain list of approved terms
- Document synonyms and preferred terms
- Establish taxonomy governance
- Regular review and updates

**Folksonomy** (user-generated tags):
- Allow users to add tags
- Monitor for useful patterns
- Promote common tags to taxonomy
- Handle variations (merge "UX", "user-experience")

---

## Navigation Patterns

### Navigation Types

**1. Global Navigation**

Primary site-wide navigation, always visible:

```
┌─────────────────────────────────────────────────────┐
│ [Logo]  Products  Solutions  Pricing  Resources  │
│                                  [Search] [Login]   │
└─────────────────────────────────────────────────────┘
```

**Characteristics**:
- Persistent across all pages
- 5-7 primary items maximum
- Left-to-right importance (or right-to-left for RTL languages)
- Utility items on right (search, account, cart)

**Patterns**:

*Horizontal Bar* (most common):
```
[Logo] [Link] [Link] [Link] [Link]        [Utility]
```

*Mega Menu*:
```
Products ▼
┌────────────────────────────────────────┐
│ Category 1    Category 2    Category 3│
│ - Item        - Item        - Item    │
│ - Item        - Item        - Item    │
│ - Item        - Item        - Item    │
│                                         │
│ [Featured content or image]            │
└────────────────────────────────────────┘
```

*Hamburger Menu* (mobile, sometimes desktop):
```
☰ [Logo]                    [Search] [Cart]
```

**2. Local Navigation**

Section-specific, changes by area:

```
┌─────────────────────────┐
│ Section Name            │
├─────────────────────────┤
│ > Current Page          │
│   Sibling Page          │
│   Sibling Page          │
│   Parent Topic ▼        │
│     - Child Page        │
│     - Child Page        │
└─────────────────────────┘
```

**Patterns**:

*Sidebar* (desktop):
- Vertical list of section content
- Shows hierarchy
- Highlights current page
- Collapsible sections

*Tabs* (desktop/mobile):
```
[Tab 1] [Tab 2] [Tab 3*] [Tab 4]
─────────────────────────────────
Content for Tab 3
```

*Segmented Control* (mobile):
```
┌───────┬───────┬───────┐
│ View1 │ View2•│ View3 │
└───────┴───────┴───────┘
```

**3. Contextual Navigation**

Embedded in content, context-specific:

```
Article Text...

Related Articles:
- [Link to related content 1]
- [Link to related content 2]

Next: [Continue to Part 2 →]
```

**Patterns**:
- Inline links within text
- Related content modules
- "Next" / "Previous" navigation
- Cross-references
- Table of contents
- Anchor links

**4. Utility Navigation**

Functional, not content-focused:

```
[Search] [Account] [Notifications] [Help] [Settings]
```

**Common Utilities**:
- Search
- Login/Account
- Shopping cart
- Language selector
- Accessibility settings
- Help/Support

**5. Supplemental Navigation**

Footer, sitemap, secondary:

```
┌─────────────────────────────────────────┐
│ Footer Navigation                       │
├───────────┬──────────┬──────────┬───────┤
│ Products  │ Company  │ Resources│ Legal │
│ - Item    │ - About  │ - Blog   │ - TOS │
│ - Item    │ - Careers│ - Docs   │ - Priv│
│ - Item    │ - Press  │ - API    │       │
└───────────┴──────────┴──────────┴───────┘
```

### Navigation State Management

**Active State** (current page):
```css
/* Visual indicators */
- Bold text
- Different color
- Underline
- Background highlight
- Left border
- Icon
```

**Hover State** (interactive feedback):
```css
/* Indicate interactivity */
- Color change
- Underline appear
- Background change
- Cursor change to pointer
```

**Focus State** (keyboard navigation):
```css
/* Accessibility critical */
- Visible outline
- Background highlight
- Must be obvious
- Different from hover
```

**Disabled State**:
```css
/* Non-interactive */
- Greyed out
- No hover effect
- Cursor: not-allowed
- Lower opacity
```

### Breadcrumbs

Show hierarchical location:

```
Home > Products > Laptops > MacBook Pro
```

**Best Practices**:
- Show path from home to current page
- Make each level clickable except current
- Use chevrons (>) or slashes (/) as separators
- Keep visible on scroll (sticky)
- Use schema.org markup for SEO

**Breadcrumb Patterns**:

*Location-based*:
```
Home > Category > Subcategory > Current Page
```

*Path-based* (history):
```
Previous Page > Previous Page > Current Page
```

*Attribute-based*:
```
All Products > [Price: $500-$1000] > [Brand: Apple] > [Type: Laptop]
```

### Navigation Accessibility

**Keyboard Support**:
```
Tab       - Move to next interactive element
Shift+Tab - Move to previous interactive element
Enter     - Activate link/button
Space     - Activate button, scroll
Escape    - Close menu/modal
Arrow keys - Navigate within menus
```

**ARIA Landmarks**:
```html
<nav aria-label="Main navigation">
  <!-- Primary nav -->
</nav>

<nav aria-label="Section navigation">
  <!-- Local nav -->
</nav>

<nav aria-label="Breadcrumb">
  <!-- Breadcrumb -->
</nav>
```

**Screen Reader Support**:
- Use semantic HTML (`<nav>`, `<ul>`, `<li>`)
- Provide `aria-label` for multiple navs
- Use `aria-current="page"` for active page
- Announce dropdown state (`aria-expanded`)
- Skip links for bypassing navigation

### Mobile Navigation Patterns

**Priority+** (progressive collapse):
```
Desktop: [Item1] [Item2] [Item3] [Item4] [Item5]
Mobile:  [Item1] [Item2] [More ▼]
```

**Tap Bar** (iOS):
```
┌─────────────────────────────────┐
│                                 │
│        App Content              │
│                                 │
├───────┬────────┬────────┬───────┤
│ 🏠 Home│📊 Stats│👤 Profile│⚙️ More│
└───────┴────────┴────────┴───────┘
```

**Bottom Sheet**:
```
Tap "☰" or button:
┌─────────────────────────────────┐
│         ── Handle ──            │
│ Menu Item 1                     │
│ Menu Item 2                     │
│ Menu Item 3                     │
│ Menu Item 4                     │
└─────────────────────────────────┘
(Swipe down to dismiss)
```

**Full-Screen Overlay**:
```
Tap "☰":
┌─────────────────────────────────┐
│ ✕                               │
│                                 │
│   Menu Item 1                   │
│   Menu Item 2                   │
│   Menu Item 3                   │
│   Menu Item 4                   │
│                                 │
│   [Secondary Items]             │
└─────────────────────────────────┘
```

---

## Wireframing Techniques

### Wireframe Fidelity Levels

**1. Low-Fidelity (Sketches)**

Purpose: Rapid ideation, early exploration

```
┌─────────────────────────────┐
│ [LOGO]    [NAV] [NAV] [NAV] │
├─────────────────────────────┤
│                             │
│   ┌───────────────────┐     │
│   │     [IMAGE]       │     │
│   │                   │     │
│   └───────────────────┘     │
│                             │
│   Headline Text             │
│   ─────────────────         │
│   Body copy here            │
│   more text                 │
│                             │
│   [Button]                  │
│                             │
└─────────────────────────────┘
```

**Characteristics**:
- Boxes and lines
- Simple annotations
- No real content
- Fast to create/modify
- Focus on layout and hierarchy

**Tools**: Paper, whiteboard, Balsamiq, Sketch, Figma (low-fi mode)

**2. Mid-Fidelity (Detailed Wireframes)**

Purpose: Document structure, content, functionality

```
┌─────────────────────────────────────────┐
│ CompanyLogo   Products About Contact    │
│                            [Search] [🛒] │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ Hero Image (1200x400)               │ │
│ │ [Headline: New Product Launch]      │ │
│ │ [Subhead: Description text here]    │ │
│ │ [Primary CTA Button]                │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Feature Section                         │
│ ┌───────┐ ┌───────┐ ┌───────┐          │
│ │ Icon  │ │ Icon  │ │ Icon  │          │
│ │ Title │ │ Title │ │ Title │          │
│ │ Lorem │ │ Lorem │ │ Lorem │          │
│ │ ipsum │ │ ipsum │ │ ipsum │          │
│ └───────┘ └───────┘ └───────┘          │
└─────────────────────────────────────────┘
```

**Characteristics**:
- Real content structure
- Actual labels and text
- Specific dimensions
- UI patterns defined
- Annotations and notes

**Tools**: Figma, Sketch, Adobe XD, Axure

**3. High-Fidelity (Interactive Prototypes)**

Purpose: User testing, stakeholder validation, development specs

```
[Actual visual design with:]
- Real typography
- Brand colors
- Imagery
- Iconography
- Interactive states
- Micro-interactions
- Actual content
```

**Characteristics**:
- Looks like real product
- Clickable interactions
- State changes
- Animations
- Realistic data

**Tools**: Figma, Framer, ProtoPie, Principle

### Wireframe Content

**Essential Elements to Document**:

**1. Layout & Structure**
- Grid system
- Column structure
- Spacing (padding, margins)
- Breakpoints
- Z-axis (layers, overlays)

**2. Navigation**
- Global navigation
- Local navigation
- Breadcrumbs
- Pagination
- Search

**3. Content Zones**
- Headlines
- Body copy
- Images/media
- CTAs
- Forms
- Lists
- Tables

**4. Interactive Elements**
- Buttons (primary, secondary, tertiary)
- Links
- Form inputs
- Dropdowns
- Toggles/switches
- Modals
- Tooltips

**5. System Feedback**
- Loading states
- Empty states
- Error states
- Success messages
- Validation feedback
- Progress indicators

### Wireframe Annotation

**Annotation Types**:

**Functional**:
```
[1] Login Button
    - Primary CTA
    - Opens login modal
    - Keyboard: Enter
    - If already logged in, show "Dashboard"
```

**Content**:
```
[2] Product Title
    - H1 tag
    - Max 60 characters
    - Dynamic from database
    - Fallback: "Untitled Product"
```

**Behavioral**:
```
[3] Image Gallery
    - Click to enlarge
    - Swipe on mobile
    - Lazy load
    - Alt text required
```

**Conditional**:
```
[4] Admin Panel
    - Visible only if user.role === "admin"
    - Redirect to /login if unauthenticated
```

### Wireframe States Matrix

Document all screen states:

```markdown
## Screen: Product Detail Page

| State | Trigger | Changes | Notes |
|-------|---------|---------|-------|
| Default | Page load | Show product info | |
| Loading | Initial request | Show skeleton | Timeout: 10s |
| Success | Data received | Render product | Cache 5min |
| Error | Request failed | Show error message | Retry button |
| Empty | No data | Show empty state | Suggest alternatives |
| Out of Stock | stock === 0 | Disable buy button | Show "Notify me" |
| Sale Price | sale_price exists | Show strikethrough price | Highlight discount |
| Favorited | User clicked heart | Fill heart icon | Toggle on/off |
```

### Responsive Wireframe Patterns

**Breakpoint Strategy**:
```
Mobile:   320px - 767px
Tablet:   768px - 1023px
Desktop:  1024px - 1439px
Wide:     1440px+
```

**Layout Transformations**:

*Desktop to Mobile*:
```
Desktop:
┌────────────────────────────────┐
│ [Nav Items Horizontal]         │
├──────────────┬─────────────────┤
│ Sidebar      │ Main Content    │
│ - Item       │                 │
│ - Item       │                 │
└──────────────┴─────────────────┘

Mobile:
┌─────────────┐
│ [☰ Menu]    │
├─────────────┤
│ Main Content│
│             │
│             │
├─────────────┤
│ (Sidebar    │
│  moved to   │
│  accordion  │
│  or bottom) │
└─────────────┘
```

*Responsive Grid*:
```
Desktop (4 columns):
┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │
└───┴───┴───┴───┘

Tablet (2 columns):
┌───────┬───────┐
│   1   │   2   │
├───────┼───────┤
│   3   │   4   │
└───────┴───────┘

Mobile (1 column):
┌───────────────┐
│       1       │
├───────────────┤
│       2       │
├───────────────┤
│       3       │
├───────────────┤
│       4       │
└───────────────┘
```

### Wireframe Component Library

Build reusable patterns:

```
Components/
├─ Navigation/
│  ├─ Global Nav
│  ├─ Sidebar Nav
│  └─ Mobile Menu
├─ Forms/
│  ├─ Input Field
│  ├─ Dropdown
│  ├─ Checkbox/Radio
│  └─ Form Layout
├─ Cards/
│  ├─ Product Card
│  ├─ Article Card
│  └─ User Card
├─ Modals/
│  ├─ Confirmation
│  ├─ Form Modal
│  └─ Alert Modal
└─ States/
   ├─ Loading
   ├─ Empty
   └─ Error
```

---

## Progressive Disclosure

### Principles

**Definition**: Reveal information gradually as needed, rather than all at once.

**Benefits**:
- Reduces cognitive load
- Prevents overwhelm
- Improves focus
- Maintains context
- Supports learning curve

### Progressive Disclosure Patterns

**1. Show on Demand**

*Accordion*:
```
▶ Section 1 Title
▼ Section 2 Title
  ├─ Content line 1
  ├─ Content line 2
  └─ Content line 3
▶ Section 3 Title
```

*Expandable Details*:
```
Product Summary [Show Details ▼]
Price: $99
Stock: Available

[After click:]
Product Summary [Hide Details ▲]
Price: $99
Stock: Available
SKU: ABC123
Weight: 2.5 lbs
Dimensions: 10x8x6 in
Warranty: 1 year
```

**2. Progressive Enhancement**

*Basic → Advanced*:
```
[Simple Search]
┌─────────────────────┐
│ Search...           │
└─────────────────────┘

[Advanced Filters ▼]
┌─────────────────────┐
│ Keyword: _______    │
│ Date: [___] to [___]│
│ Category: [v]       │
│ Sort: [v]           │
└─────────────────────┘
```

*Novice → Expert Paths*:
```
Novice: Guided wizard (5 steps)
Expert: Advanced form (all options)

Toggle: "Switch to advanced mode"
```

**3. Staged Disclosure**

*Multi-Step Form*:
```
Step 1: Basic Info → Step 2: Details → Step 3: Review

Only show next step when current is valid
```

*Conditional Reveal*:
```
Shipping Method:
( ) Standard
( ) Express
(•) Store Pickup

[When Store Pickup selected:]
┌─────────────────────┐
│ Choose Store:       │
│ ( ) Downtown        │
│ ( ) North Mall      │
│ ( ) Airport         │
└─────────────────────┘
```

**4. Layered Information**

*Tooltip*:
```
Field Label [?]

[Hover on ?:]
┌──────────────────────┐
│ Brief explanation of │
│ what this field does │
└──────────────────────┘
```

*Popover*:
```
[Info icon] → Click
┌────────────────────────────┐
│ More detailed information  │
│ with links:                │
│ - [Learn more]             │
│ - [See example]            │
└────────────────────────────┘
```

*Drawer/Sheet*:
```
[View Details] → Slide in panel
┌──────────────────┐
│ Detail Panel  [×]│
│                  │
│ [Full content]   │
│                  │
└──────────────────┘
```

**5. Smart Defaults**

*Pre-filled Options*:
```
Country: [United States ▼]
(Auto-detected from IP, user can change)

Time Zone: [EST ▼]
(Auto-selected based on country)
```

*Recommended Settings*:
```
Privacy Settings:
(•) Recommended   [What's this?]
( ) Custom

[If Custom selected, show all options]
```

### When to Use Progressive Disclosure

**Use when**:
- Information is secondary or optional
- User is learning a new system
- Choices are complex or numerous
- Context varies by user type
- Screen space is limited (mobile)

**Don't use when**:
- Information is critical for decision
- User needs to compare all options
- Hiding creates more clicks than value
- Users expect all info upfront
- Disclosure breaks user flow

### Progressive Disclosure Anti-Patterns

**Mystery Meat**:
```
❌ Bad:
[Button] → ??? (unclear what happens)

✅ Good:
[See More Options ▼] → (clear what's revealed)
```

**Excessive Nesting**:
```
❌ Bad:
Click 1 → Reveal 2 → Click 2 → Reveal 3 → Click 3 → Content

✅ Good:
Click 1 → Content (max 2 levels)
```

**Hidden Critical Info**:
```
❌ Bad:
Price: $99 [click for total]
  → Reveals: $99 + $50 shipping + $15 tax = $164

✅ Good:
Subtotal: $99
Shipping: $50
Tax: $15
Total: $164
```

---

## Form Design Flows

### Form Structure

**Basic Anatomy**:
```
┌────────────────────────────────┐
│ Form Title                     │
│ Brief description of purpose   │
├────────────────────────────────┤
│                                │
│ Section 1 Heading              │
│                                │
│ Field Label *                  │
│ [Input field]                  │
│ Helper text                    │
│                                │
│ Field Label                    │
│ [Input field]                  │
│                                │
│ Section 2 Heading              │
│                                │
│ Field Label *                  │
│ [Input field]                  │
│ Error message in red           │
│                                │
├────────────────────────────────┤
│         [Cancel] [Submit]      │
└────────────────────────────────┘

* = Required field
```

### Form Field Types & When to Use

**Text Input**:
```
Name: [________________________]
```
Use for: Names, addresses, custom text

**Email Input**:
```
Email: [________________________]
       @
```
Use for: Email (validates format, mobile keyboard)

**Number Input**:
```
Age: [____] years
     [- 25 +]
```
Use for: Quantities, ages (provide +/- buttons)

**Date Picker**:
```
Birth Date: [MM] / [DD] / [YYYY]
            📅 (calendar picker)
```
Use for: Dates (provide calendar for selection)

**Dropdown/Select**:
```
Country: [United States        ▼]
```
Use for: 5-15 options, single selection

**Radio Buttons**:
```
Size:
( ) Small
(•) Medium
( ) Large
```
Use for: 2-5 options, single selection, show all

**Checkboxes**:
```
Toppings:
[✓] Cheese
[ ] Pepperoni
[✓] Mushrooms
```
Use for: Multiple selections, opt-ins

**Toggle Switch**:
```
Email notifications: [ON ●─────]
```
Use for: Binary choice, immediate effect

**Textarea**:
```
Comments:
┌────────────────────────┐
│                        │
│                        │
│                        │
└────────────────────────┘
```
Use for: Multi-line text, comments

**Slider**:
```
Budget: ────●────────── $500K
        $0            $1M
```
Use for: Range selection, approximate values

### Form Layout Patterns

**Single Column** (recommended):
```
┌─────────────────┐
│ Field 1         │
│ [___________]   │
│                 │
│ Field 2         │
│ [___________]   │
│                 │
│ Field 3         │
│ [___________]   │
│                 │
│ [Submit]        │
└─────────────────┘
```
- Fastest completion time
- Mobile-friendly
- Best for most forms

**Multi-Column** (use sparingly):
```
┌──────────────────────────┐
│ First Name    Last Name  │
│ [________]    [________]  │
│                          │
│ City          State      │
│ [________]    [____]     │
│                          │
│ [Submit]                 │
└──────────────────────────┘
```
- Only for related fields
- Example: First/Last name, City/State
- Don't use just to save space

**Stepped/Wizard**:
```
(Step 1●) ─── (Step 2○) ─── (Step 3○)
Account       Details       Confirm

┌─────────────────────────────┐
│ Step 1: Account Info        │
│                             │
│ Email: [_________________]  │
│                             │
│ Password: [_____________]   │
│                             │
│          [Cancel] [Next →]  │
└─────────────────────────────┘
```
- For long/complex forms
- Group related fields
- Show progress

### Form Validation

**When to Validate**:

**Inline (Real-time)**:
```
Email: [user@example]
       ✗ Invalid email format

[User continues typing: user@example.com]
       ✓ Valid email
```
Use for: Format validation, availability checks

**On Blur (After field exit)**:
```
[User enters "abc" in phone field]
[User tabs to next field]
       ✗ Phone number must be 10 digits
```
Use for: Most validations, less intrusive

**On Submit**:
```
[User clicks Submit]

┌─────────────────────────────┐
│ ⚠ Please fix these errors:  │
│ - Email is required          │
│ - Password too short         │
└─────────────────────────────┘

[Scroll to first error]
```
Use for: Final check, required fields

**Validation Messages**:

```
❌ Bad:
- "Invalid input"
- "Error"
- "Wrong"

✅ Good:
- "Email must include @ symbol"
- "Password must be at least 8 characters"
- "Please select a date"
```

**Validation States**:

```css
/* Default */
border: 1px solid #ccc;

/* Focus */
border: 2px solid blue;
box-shadow: 0 0 4px blue;

/* Valid */
border: 2px solid green;
✓ icon

/* Invalid */
border: 2px solid red;
✗ icon + error message below
```

### Form Optimization Techniques

**Reduce Fields**:
- Remove optional fields
- Ask only what you need now
- Progressive profiling (gather over time)

**Smart Defaults**:
- Pre-fill when possible
- Remember previous entries
- Use sensible defaults

**Input Masks**:
```
Phone: (___) ___-____
       (555) 123-4567

Credit Card: ____ ____ ____ ____
             1234 5678 9012 3456
```

**Auto-Advance**:
```
Code: [_] [_] [_] [_]
      (Auto-focus next after input)
```

**Autosave**:
```
Draft saved at 2:34 PM ✓
```

**Inline Addition**:
```
Shipping Address: [123 Main St...     ▼]
                  [+ Add new address]
```

### Form Error Handling

**Error Summary** (top of form):
```
┌──────────────────────────────────┐
│ ⚠ 2 errors prevent submission:   │
│ 1. Email is required              │
│ 2. Password too short             │
└──────────────────────────────────┘
```

**Inline Errors** (below field):
```
Password: [********]
          ✗ Must be at least 8 characters
          ✗ Must include a number
```

**Prevention Over Correction**:
```
Instead of:
  Quantity: [____]
  Error: "Must be a number"

Use:
  Quantity: [- 1 +]
  (Only allows numbers)
```

### Form Success States

**Confirmation Message**:
```
┌──────────────────────────────────┐
│ ✓ Account created successfully!  │
│   Redirecting to dashboard...    │
└──────────────────────────────────┘
```

**Success Page**:
```
┌──────────────────────────────────┐
│            ✓                     │
│                                  │
│    Registration Complete!        │
│                                  │
│ What happens next:               │
│ 1. Check your email              │
│ 2. Verify your account           │
│ 3. Complete your profile         │
│                                  │
│     [Go to Dashboard →]          │
└──────────────────────────────────┘
```

**Email Confirmation**:
- Send immediately
- Summarize what was submitted
- Provide reference number
- Include next steps

---

## Error Recovery Paths

### Error Types & Responses

**1. User Errors** (user mistake)

*Invalid Input*:
```
Action: User enters "abc" in number field
Response: Inline validation
Recovery: Clear instruction, format example
```

*Missing Required Field*:
```
Action: User skips required field
Response: Prevent submission, highlight field
Recovery: Scroll to field, focus input
```

*Incorrect Format*:
```
Action: User enters "555-1234" for phone
Response: "Phone must be 10 digits: (555) 555-1234"
Recovery: Show correct format, mask input
```

**2. System Errors** (technical failure)

*Server Error*:
```
┌────────────────────────────────────┐
│ ⚠ Unable to save changes           │
│                                    │
│ Our servers are experiencing       │
│ issues. Your data is safe.         │
│                                    │
│ [Try Again] [Save for Later]      │
└────────────────────────────────────┘
```

*Network Error*:
```
┌────────────────────────────────────┐
│ ⚠ No internet connection           │
│                                    │
│ Your changes are saved locally and │
│ will sync when reconnected.        │
│                                    │
│ [Dismiss]                          │
└────────────────────────────────────┘
```

*Timeout*:
```
┌────────────────────────────────────┐
│ ⚠ Request timed out                │
│                                    │
│ This is taking longer than usual.  │
│                                    │
│ [Keep Waiting] [Cancel]            │
└────────────────────────────────────┘
```

**3. Permission Errors** (access denied)

*Authentication Required*:
```
┌────────────────────────────────────┐
│ 🔒 Sign in required                │
│                                    │
│ To access this feature, please     │
│ sign in to your account.           │
│                                    │
│ [Sign In] [Create Account]         │
└────────────────────────────────────┘
```

*Insufficient Permissions*:
```
┌────────────────────────────────────┐
│ ⚠ Access denied                    │
│                                    │
│ This feature requires admin        │
│ privileges. Contact your manager.  │
│                                    │
│ [Contact Support] [Go Back]        │
└────────────────────────────────────┘
```

**4. Business Logic Errors** (constraint violation)

*Out of Stock*:
```
┌────────────────────────────────────┐
│ ⚠ Item unavailable                 │
│                                    │
│ This item is currently out of      │
│ stock. Expected restock: Jan 20    │
│                                    │
│ [Notify Me] [View Similar]         │
└────────────────────────────────────┘
```

*Conflict*:
```
┌────────────────────────────────────┐
│ ⚠ Booking conflict                 │
│                                    │
│ This time slot is no longer        │
│ available. Choose another time:    │
│                                    │
│ [View Available Times]             │
└────────────────────────────────────┘
```

### Error Message Components

**Anatomy of a Good Error Message**:

```
┌────────────────────────────────────┐
│ [Icon] [Title]                     │
│                                    │
│ [Explanation]                      │
│                                    │
│ [Recovery Actions]                 │
└────────────────────────────────────┘
```

**1. Icon** (visual cue):
- ⚠ Warning (yellow): User action needed
- ✗ Error (red): Something failed
- ℹ Info (blue): FYI, not critical
- 🔒 Security: Authentication/permission

**2. Title** (concise problem):
- "Unable to save changes"
- "Connection lost"
- "File too large"

**3. Explanation** (what happened & why):
- "The file you selected is 50MB. Maximum size is 10MB."
- "Our payment processor is temporarily unavailable."

**4. Recovery Actions** (what user can do):
- Primary: Fixes the problem
- Secondary: Workaround or help
- Tertiary: Cancel or go back

### Error Recovery Principles

**1. Prevent Errors**
```
Before: Allow any text in "Quantity"
After:  Provide +/- buttons, restrict to numbers

Before: Let user submit without required fields
After:  Disable submit until valid
```

**2. Detect Early**
```
Before: Wait until submit to validate
After:  Validate as user types (for format)

Before: Let invalid data through
After:  Client-side and server-side validation
```

**3. Clear Messaging**
```
❌ Bad: "Error 500"
✅ Good: "Unable to process request. Our team has been notified."

❌ Bad: "Invalid input"
✅ Good: "Email must include @ symbol"
```

**4. Easy Recovery**
```
❌ Bad: Show error, make user figure out fix
✅ Good: Explain error + provide clear action

❌ Bad: Lose all form data on error
✅ Good: Preserve entered data, let user fix and retry
```

**5. Helpful Guidance**
```
❌ Bad: "Username taken"
✅ Good: "Username taken. Try: username123, user_name"

❌ Bad: "Payment failed"
✅ Good: "Payment failed. Common fixes:
         - Check card number
         - Verify expiration date
         - Contact your bank"
```

### Error State Design Patterns

**Inline Error** (field-level):
```
Email: [user@example]
       ✗ Invalid email format
       Try: user@example.com
```

**Banner Error** (page-level):
```
┌────────────────────────────────────┐
│ ⚠ Changes not saved                │
│   Please fix 2 errors below        │
└────────────────────────────────────┘

[Field with error highlighted]
```

**Modal Error** (blocking):
```
┌────────────────────────────────────┐
│                [×]                 │
│  ⚠ Payment Failed                  │
│                                    │
│  Your card was declined.           │
│                                    │
│  [Update Payment Method] [Cancel]  │
└────────────────────────────────────┘
```

**Toast/Snackbar** (non-blocking):
```
                ┌──────────────────────┐
                │ ⚠ File not uploaded  │
                │   [Retry] [×]        │
                └──────────────────────┘
```

**Empty State with Error**:
```
┌────────────────────────────────────┐
│        [Empty icon]                │
│                                    │
│   Unable to Load Content           │
│                                    │
│   Check your internet connection   │
│   and try again.                   │
│                                    │
│       [Retry]                      │
└────────────────────────────────────┘
```

### Recovery Flow Examples

**Payment Failure Flow**:
```
1. User submits payment
2. Payment fails
3. Show error: "Card declined"
4. Keep form data
5. Offer actions:
   - Update payment method
   - Try different card
   - Contact support
6. User fixes → Retry
7. Success → Confirmation
```

**File Upload Error Flow**:
```
1. User selects file
2. Validation: File too large
3. Show error immediately
4. Offer solutions:
   - "Reduce file size" (link to tool)
   - "Upload different file"
   - "Max size: 10MB"
5. User fixes → Upload succeeds
```

**Form Validation Error Flow**:
```
1. User fills form
2. Clicks Submit
3. Validation fails on 3 fields
4. Prevent submission
5. Show error summary at top
6. Scroll to first error
7. Highlight all invalid fields
8. Preserve valid entries
9. User fixes → Enable submit
10. Submit → Success
```

### Error Logging & Monitoring

**What to Log**:
```javascript
{
  timestamp: "2026-01-14T10:30:00Z",
  userId: "user123",
  action: "form_submit",
  error_type: "validation_error",
  error_fields: ["email", "phone"],
  error_messages: [
    "Email format invalid",
    "Phone number required"
  ],
  user_agent: "...",
  session_id: "...",
  page_url: "/signup"
}
```

**Monitor**:
- Error frequency by type
- Drop-off points in flows
- Repeated errors (user stuck)
- Resolution rate (did retry work?)

---

## Onboarding Flows

### Onboarding Goals

**1. Activation**: User experiences core value
**2. Education**: User learns key features
**3. Habit Formation**: User develops routine usage

### Onboarding Types

**1. Product Tours** (guided walkthrough)

```
┌────────────────────────────────────┐
│ [Spotlight on feature]             │
│                                    │
│  ┌──────────────────────┐          │
│  │ This is the Dashboard│          │
│  │ Here you can see...  │          │
│  │                      │          │
│  │ [Skip] [Next 1/5]    │          │
│  └──────────────────────┘          │
└────────────────────────────────────┘
```

**When to use**:
- Complex interfaces
- Many features to discover
- Different user roles

**Best practices**:
- Keep to 3-5 steps maximum
- Allow skip/dismiss
- Show progress
- Highlight actual UI (not overlay entire screen)

**2. Progressive Onboarding** (contextual, as-needed)

```
[User encounters feature for first time]

┌────────────────────────────────────┐
│ 💡 New Feature                     │
│                                    │
│ Click here to create your first    │
│ project. [Got it]                  │
└────────────────────────────────────┘

[Tooltip appears when relevant]
```

**When to use**:
- Frequent product updates
- Advanced features
- Optional workflows

**Best practices**:
- Trigger based on context
- Don't interrupt core flow
- One tip at a time
- Allow dismiss forever

**3. Account Setup** (required configuration)

```
Step 1/3: Create Account
┌────────────────────────────────────┐
│ Email: [____________________]      │
│ Password: [_________________]      │
│                                    │
│          [Continue →]              │
└────────────────────────────────────┘

Step 2/3: Profile Setup
┌────────────────────────────────────┐
│ Name: [____________________]       │
│ Company: [_________________]       │
│                                    │
│          [← Back] [Continue →]     │
└────────────────────────────────────┘

Step 3/3: Customize
┌────────────────────────────────────┐
│ What brings you here?              │
│ [ ] Personal use                   │
│ [ ] Business                       │
│ [ ] Education                      │
│                                    │
│          [← Back] [Get Started]    │
└────────────────────────────────────┘
```

**When to use**:
- Required before product use
- Personalization needed
- Data collection necessary

**Best practices**:
- Minimize steps (3-5 max)
- Show progress clearly
- Allow back navigation
- Explain why you're asking

**4. Empty State Onboarding** (action-prompted)

```
┌────────────────────────────────────┐
│         [Empty state icon]         │
│                                    │
│    No projects yet                 │
│                                    │
│    Create your first project to    │
│    get started.                    │
│                                    │
│    [+ Create Project]              │
│                                    │
│    [Watch Video] [See Example]     │
└────────────────────────────────────┘
```

**When to use**:
- Simple products
- Self-explanatory workflows
- User-initiated content

**Best practices**:
- Clear call-to-action
- Provide examples/templates
- Link to help resources
- Make first action easy

### Onboarding Flow Structure

**Setup Phase**:
```
[Entry] → [Account Creation] → [Profile Setup] → [Preferences]
                ↓
         [Email Verification]
                ↓
         [Welcome Email]
```

**Activation Phase**:
```
[First Login] → [Product Tour] → [First Action] → [Quick Win]
                                        ↓
                                  [Encouragement]
```

**Habit Formation Phase**:
```
[Day 2 Email] → [Feature Discovery] → [Repeated Use] → [Advanced Features]
                      ↓                    ↓
              [Contextual Tips]    [Milestone Celebration]
```

### Onboarding Checklists

**Example Checklist**:
```
┌────────────────────────────────────┐
│ Get Started                   2/5  │
├────────────────────────────────────┤
│ ✓ Create account                   │
│ ✓ Verify email                     │
│ ○ Create first project             │
│ ○ Invite team member               │
│ ○ Customize settings               │
└────────────────────────────────────┘
```

**Checklist Best Practices**:
- 3-7 items maximum
- Order by priority
- Quick wins first
- Visual progress
- Celebrate completion
- Optional items clearly marked
- Link directly to actions

### Personalization in Onboarding

**Segmentation Questions**:
```
What's your role?
( ) Developer
( ) Designer
( ) Product Manager
( ) Other

[Based on answer, show relevant features]
```

**Adaptive Content**:
```
If (role === "Developer"):
  Show: API docs, code samples, CLI setup

If (role === "Designer"):
  Show: Design tools, asset library, templates
```

**Progressive Profiling**:
```
First visit: Name, email
Day 2: Company size
Day 7: Industry
Week 2: Specific use case

(Spread over time, not all at once)
```

### Onboarding Metrics

**Track**:
- **Completion rate**: % who finish onboarding
- **Time to complete**: How long setup takes
- **Drop-off points**: Where users abandon
- **Activation rate**: % who reach "aha moment"
- **Time to activation**: How long to first value
- **Feature adoption**: Which features used first
- **Retention**: % active after 7, 30 days

**Aha Moment Examples**:
- Slack: Send 2,000 messages (team engaged)
- Dropbox: Store file on one device, access on another
- Facebook: Add 7 friends in 10 days

### Onboarding Anti-Patterns

**Forced Tutorial**:
```
❌ Bad: Block product use until 20-step tour complete
✅ Good: Optional tour, allow skip, learn by doing
```

**Information Overload**:
```
❌ Bad: Show all features at once
✅ Good: Introduce progressively as needed
```

**Generic Experience**:
```
❌ Bad: Same onboarding for all users
✅ Good: Personalized based on role/goal
```

**Premature Data Collection**:
```
❌ Bad: Ask 20 questions before showing value
✅ Good: Collect data progressively, explain why
```

**No Clear Path**:
```
❌ Bad: "Here's the app, good luck!"
✅ Good: Guide to first successful action
```

---

## Multi-Step Process Design

### When to Use Multi-Step

**Use multi-step when**:
- Process is complex (10+ fields)
- Logical grouping exists
- Steps are sequential
- Each step requires focus
- Mobile experience matters

**Don't use when**:
- Simple form (< 5 fields)
- Fields are unrelated
- User needs to see all at once
- Back-and-forth navigation needed

### Step Patterns

**Linear Steps** (can't skip):
```
(1●)──────(2○)──────(3○)──────(4○)
Info      Details   Payment   Confirm

[Must complete in order]
```

**Non-Linear Steps** (can skip):
```
(1✓)──────(2○)──────(3○)──────(4○)
Profile   Optional  Settings  Finish

[Can skip step 2 and 3]
```

**Conditional Steps** (dynamic):
```
(1●)──────(2○)──────(3○?)─────(4○)
Type      Details   If Yes    Review

[Step 3 only if certain answer in Step 2]
```

### Progress Indicators

**Stepped Indicator**:
```
●─────────○─────────○─────────○
1         2         3         4
```

**Labeled Steps**:
```
   ●              ○              ○              ○
Account       Details        Payment        Complete
```

**Progress Bar**:
```
Step 2 of 4
[██████████░░░░░░░░░░] 50%
```

**Checklist**:
```
✓ Account info
✓ Personal details
→ Payment method  ← You are here
○ Confirmation
```

**Numeric**:
```
Step 2 of 4
```

### Step Navigation

**Forward/Back Buttons**:
```
┌────────────────────────────────────┐
│ [Step content]                     │
│                                    │
│                                    │
│ [← Back]              [Continue →] │
└────────────────────────────────────┘
```

**Clickable Steps** (if non-linear):
```
1. Info ── 2. Details* ── 3. Payment ── 4. Review
   (✓)        (active)        (○)          (○)

[Can click on completed steps to edit]
```

**Save and Continue Later**:
```
┌────────────────────────────────────┐
│ [Step content]                     │
│                                    │
│                                    │
│ [Save Draft] [← Back] [Continue →] │
└────────────────────────────────────┘
```

### Step Content Design

**Each Step Should**:
1. Have clear title
2. Show progress
3. Contain related fields only
4. Have obvious action
5. Provide exit option

**Example Step**:
```
┌────────────────────────────────────┐
│ Step 2 of 4: Shipping Address      │  ← Title
│ ──────────────────────────          │  ← Progress
│                                    │
│ Street Address:                    │
│ [____________________________]     │
│                                    │
│ City:                              │  ← Related
│ [____________________________]     │     fields
│                                    │
│ State:        ZIP:                 │
│ [________]    [_________]          │
│                                    │
│ [Save as default address]          │
│                                    │
│ [← Back]              [Continue →] │  ← Actions
│                                    │
│ [Save and Exit]                    │  ← Exit option
└────────────────────────────────────┘
```

### Data Persistence

**Auto-Save**:
```
Draft saved at 2:34 PM ✓
```

**Warn Before Exit**:
```
┌────────────────────────────────────┐
│ ⚠ Unsaved Changes                  │
│                                    │
│ You have unsaved changes.          │
│ What would you like to do?         │
│                                    │
│ [Save Draft] [Discard] [Continue]  │
└────────────────────────────────────┘
```

**Resume from Where Left**:
```
[On return visit]

┌────────────────────────────────────┐
│ Welcome back!                      │
│                                    │
│ You were on Step 2 of 4.           │
│                                    │
│ [Continue] [Start Over]            │
└────────────────────────────────────┘
```

### Review/Confirmation Step

**Final Review**:
```
┌────────────────────────────────────┐
│ Step 4 of 4: Review & Submit       │
│                                    │
│ Account Information        [Edit]  │
│ Email: user@example.com            │
│ Name: John Doe                     │
│                                    │
│ Shipping Address          [Edit]   │
│ 123 Main St                        │
│ Anytown, CA 12345                  │
│                                    │
│ Payment Method            [Edit]   │
│ Visa ending in 1234                │
│                                    │
│ [ ] I agree to terms of service    │
│                                    │
│ [← Back]              [Submit]     │
└────────────────────────────────────┘
```

**Edit Capability**:
- Link to specific step
- Preserve other data
- Return to review after edit

### Mobile Considerations

**Mobile-Specific Patterns**:

*Full-Screen Steps*:
```
┌─────────────────┐
│ [< Back] 2/4    │
├─────────────────┤
│                 │
│ [Step content]  │
│                 │
│                 │
│                 │
├─────────────────┤
│   [Continue]    │
└─────────────────┘
```

*Bottom Sheet Steps*:
```
┌─────────────────┐
│                 │
│ [Previous       │
│  content        │
│  visible]       │
├─────────────────┤
│ ── Handle ──    │
│ Step 2          │
│ [Fields]        │
│ [Continue]      │
└─────────────────┘
```

*Swipe Navigation*:
```
← Swipe for previous step
→ Swipe for next step
(If step is valid)
```

### Multi-Step Best Practices

**1. Minimize Steps**
- Combine related fields
- Remove optional fields
- Ask only what's necessary

**2. Clear Progress**
- Show where user is
- Show how many steps remain
- Show what's completed

**3. Flexible Navigation**
- Allow back navigation
- Enable step editing
- Support save and resume

**4. Validation Strategy**
- Validate per step (on continue)
- Don't allow invalid progress
- But allow back navigation
- Show error count if multiple

**5. Mobile Optimization**
- One column layout
- Large tap targets
- Sticky navigation
- Auto-advance on completion

---

## Mobile Navigation Patterns

### Mobile Navigation Challenges

**Constraints**:
- Limited screen space
- Touch targets need 44x44px minimum
- Thumb zones (bottom easier to reach)
- One-handed use consideration
- Context switching cost

### Primary Mobile Navigation Patterns

**1. Bottom Tab Bar** (Most common)

```
┌─────────────────────────────────┐
│                                 │
│         App Content             │
│                                 │
│                                 │
├───────┬────────┬────────┬───────┤
│ 🏠    │ 🔍     │ ➕     │ 👤    │
│ Home  │ Search │ Post   │ Profile
└───────┴────────┴────────┴───────┘
```

**Best for**:
- 3-5 primary sections
- Frequent switching
- Co-equal sections
- Direct access

**Best practices**:
- Always visible
- Highlight active tab
- Icons + labels (or icon only if space tight)
- Keep order consistent
- Don't hide on scroll

**2. Hamburger Menu**

```
┌─────────────────────────────────┐
│ ☰ App Name         [Search] [+] │
├─────────────────────────────────┤
│                                 │
│         App Content             │
│                                 │
└─────────────────────────────────┘

[Tap ☰]
┌──────────────┐
│ ✕            │
│              │
│ Home         │
│ Profile      │
│ Settings     │
│ Help         │
│ Logout       │
└──────────────┘
```

**Best for**:
- Many navigation items
- Less frequent access
- Secondary navigation
- Account/settings

**Best practices**:
- Clearly indicate menu icon
- Smooth slide-in animation
- Tap outside to close
- Show active section
- Group related items

**3. Hybrid (Tab Bar + Hamburger)**

```
┌─────────────────────────────────┐
│ ☰ Section Title    [Search] [+] │
├─────────────────────────────────┤
│                                 │
│         App Content             │
│                                 │
├───────┬────────┬────────┬───────┤
│ Home  │ Browse │ Save   │ More  │
└───────┴────────┴────────┴───────┘

["More" tap reveals additional options]
```

**Best for**:
- Many features
- Clear primary actions
- Secondary functions
- Complex apps

**4. Bottom Sheet/Action Sheet**

```
[User taps action button]

┌─────────────────────────────────┐
│                                 │
│         App Content             │
│                                 │
├─────────────────────────────────┤
│         ── Handle ──            │
│                                 │
│  [Icon] Action 1                │
│  [Icon] Action 2                │
│  [Icon] Action 3                │
│                                 │
│  [Cancel]                       │
└─────────────────────────────────┘
```

**Best for**:
- Context actions
- Share options
- Creation flows
- Temporary choices

**5. Nested/Drill-Down**

```
Level 1:                Level 2:
┌──────────────────┐    ┌──────────────────┐
│ < Back           │    │ < Category       │
│                  │    │                  │
│ Category 1    >  │ -> │ Item 1        >  │
│ Category 2    >  │    │ Item 2        >  │
│ Category 3    >  │    │ Item 3        >  │
└──────────────────┘    └──────────────────┘
```

**Best for**:
- Hierarchical content
- Deep navigation
- Settings screens
- File browsers

**6. Floating Action Button (FAB)**

```
┌─────────────────────────────────┐
│                                 │
│         App Content             │
│                                 │
│                         ┌───┐   │
│                         │ + │   │
│                         └───┘   │
└─────────────────────────────────┘
```

**Best for**:
- Primary creation action
- Most common action
- Quick access

**Best practices**:
- One primary action only
- Bottom-right or bottom-center
- Larger touch target (56x56dp)
- Animate on reveal
- Hide on scroll down, show on scroll up

### Mobile Gesture Navigation

**Common Gestures**:

*Swipe*:
```
← Swipe right: Back/Previous
→ Swipe left: Forward/Delete/Archive
↑ Swipe up: Reveal more/Refresh
↓ Swipe down: Close/Refresh
```

*Pull to Refresh*:
```
[User pulls down from top]
[Loading indicator appears]
[Content refreshes]
```

*Edge Swipe*:
```
[Swipe from left edge]
[Menu appears]

[Swipe from right edge]
[Previous screen/back navigation]
```

*Long Press*:
```
[User holds on item]
[Context menu appears]
```

### Thumb Zone Optimization

**Thumb Zone Heatmap**:
```
┌─────────────────────────────────┐
│ ❄️ Hard to reach                 │
│                                 │
│     ⚠️ Stretch zone              │
│                                 │
│         ✓ Natural zone          │
│                                 │
│             ✓✓ Easy zone        │
├─────────────────────────────────┤
│ ✓✓✓✓ Easy zone (bottom bar)     │
└─────────────────────────────────┘
```

**Design Implications**:
- Primary actions at bottom
- Secondary/destructive at top
- Large tap targets
- Spacing between targets
- Consider one-handed use

### Mobile Navigation States

**Loading Navigation**:
```
┌─────────────────────────────────┐
│ [Skeleton of nav bar]           │
├─────────────────────────────────┤
│ [Skeleton content]              │
└─────────────────────────────────┘
```

**Offline Navigation**:
```
┌─────────────────────────────────┐
│ ⚠️ Offline ─ Last synced 5m ago  │
├─────────────────────────────────┤
│ [Cached content]                │
│ [Offline-available sections]    │
└─────────────────────────────────┘
```

**Error Navigation**:
```
┌─────────────────────────────────┐
│ ✗ Failed to load                │
│                                 │
│ [Retry button]                  │
└─────────────────────────────────┘
```

### Mobile Navigation Best Practices

**1. Prioritize Ruthlessly**
- 3-5 items in primary nav
- Hide less-used features
- Progressive disclosure
- Contextual access

**2. Clear Signifiers**
- Icons with labels when possible
- Active state clearly different
- Tap targets 44x44px minimum
- Visual feedback on tap

**3. Minimize Taps**
- Direct access to top tasks
- Reduce navigation depth
- Smart defaults
- Remember context

**4. Performance**
- Instant feedback
- Optimistic UI updates
- Preload likely destinations
- Smooth animations (60fps)

**5. Consistency**
- Platform conventions (iOS vs Android)
- Maintain nav structure
- Predictable behavior
- Standard gestures

### iOS vs Android Navigation

**iOS Patterns**:
- Bottom tab bar (primary)
- Back button (top-left)
- Swipe from edge to go back
- Large titles
- Modal sheets

**Android Patterns**:
- Bottom nav or drawer
- System back button
- FAB for primary action
- App bar at top
- Bottom sheets

**Cross-Platform Considerations**:
- Follow platform conventions
- Test on both
- Adapt patterns appropriately
- Don't force one model on the other

---

## Testing User Flows

### Testing Methods

**1. Usability Testing**

**Setup**:
- Recruit representative users (5-8 per round)
- Define tasks matching key flows
- Prepare test environment
- Record sessions (with consent)

**Process**:
```
1. Welcome & explain
2. Pre-test questions
3. Task scenarios:
   "You want to [goal]. Show me how you'd do that."
4. Think-aloud protocol
5. Post-task questions
6. Post-test questionnaire
7. Debrief
```

**What to Measure**:
- **Task completion rate**: % who complete successfully
- **Time on task**: How long it takes
- **Error rate**: Mistakes made
- **Path efficiency**: Optimal vs actual path
- **User satisfaction**: Post-task rating

**2. A/B Testing**

Compare flow variations:

```
Flow A (Control):
Home → Search → Results → Product → Add to Cart → Checkout

Flow B (Variant):
Home → Search → Results → [Quick Add] → Checkout

Measure:
- Conversion rate
- Time to purchase
- Abandonment rate
```

**3. Analytics Analysis**

**Funnel Analysis**:
```
Step 1: Land on page       10,000 users (100%)
Step 2: Start signup        3,000 users (30%)
Step 3: Complete form       1,500 users (50% of step 2)
Step 4: Verify email        1,200 users (80% of step 3)
Step 5: Complete setup        900 users (75% of step 4)

Conversion: 9% overall
Biggest drop-off: Step 1 → Step 2 (70% drop)
```

**Heatmaps & Recordings**:
- Where users click
- Scroll depth
- Rage clicks (frustration)
- Dead clicks (non-interactive)
- Session recordings

**4. Card Sorting**

Test information architecture:

```
Open Sort:
- Give users cards (features, content)
- Users group and label
- Identify natural groupings

Closed Sort:
- Provide categories
- Users place cards
- Test proposed structure
```

**5. Tree Testing**

Test navigation without UI:

```
Task: "Where would you find pricing information?"

Home
├─ Products
│  ├─ Features
│  └─ Pricing ✓ [User selects this]
├─ Resources
└─ Company
   └─ About

Result: 85% found it, 15% failed
```

**6. First Click Testing**

Where users click first indicates scent:

```
Show mockup
Ask: "Where would you click to [task]?"

Measure:
- % who clicked correct area
- % who clicked wrong area
- Time to first click
```

### Testing Metrics & KPIs

**Effectiveness Metrics**:
- Task success rate
- Error rate
- Completion time
- Steps to completion

**Efficiency Metrics**:
- Time on task
- Number of clicks
- Path deviation
- Backtracking frequency

**Satisfaction Metrics**:
- System Usability Scale (SUS)
- Net Promoter Score (NPS)
- Task ease rating
- Qualitative feedback

**Engagement Metrics**:
- Feature adoption rate
- Daily/monthly active users
- Session duration
- Return frequency

### User Flow Testing Protocol

**Pre-Test**:
```
1. Define flow to test
2. Identify success criteria
3. Create task scenarios
4. Recruit users
5. Prepare materials
6. Set up recording
```

**During Test**:
```
1. Explain think-aloud
2. Give task scenario
3. Observe (don't help)
4. Ask probing questions:
   - "What are you looking for?"
   - "What do you expect to happen?"
   - "Why did you click that?"
5. Note issues, confusion, errors
6. Rate task difficulty
```

**Post-Test**:
```
1. Debrief questions
2. Satisfaction rating
3. Ask about confusing parts
4. Gather improvement ideas
5. Thank participant
```

**Analysis**:
```
1. Review recordings
2. Note patterns across users
3. Categorize issues:
   - Critical (blockers)
   - Major (significant friction)
   - Minor (small annoyances)
4. Prioritize fixes
5. Iterate design
6. Re-test
```

### Remote Testing Tools

**Moderated Remote**:
- Zoom, Google Meet (video call)
- Screen sharing
- Real-time observation
- Can ask questions

**Unmoderated Remote**:
- UserTesting, Lookback
- Task-based
- Recorded sessions
- Scalable

**Analytics**:
- Google Analytics
- Mixpanel, Amplitude
- Hotjar (heatmaps)
- FullStory (session replay)

**Survey Tools**:
- Typeform, Google Forms
- In-app surveys
- Email surveys

### Accessibility Testing

**Testing with Assistive Tech**:
- Screen readers (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation
- Voice control
- Screen magnification
- High contrast mode

**Key Checks**:
```
✓ All interactive elements keyboard accessible
✓ Logical tab order
✓ Focus visible
✓ ARIA labels present
✓ Error messages announced
✓ Form labels associated
✓ Alt text on images
✓ Color contrast sufficient (4.5:1)
✓ Text resizable to 200%
✓ No keyboard traps
```

**WCAG Compliance Levels**:
- A: Basic (minimum)
- AA: Mid-range (target for most)
- AAA: Highest (government, education)

---

## Anti-Patterns

### Navigation Anti-Patterns

**1. Mystery Meat Navigation**
```
❌ Bad: Icons without labels
🏠 📊 ⚙️ ❓
(User must guess meaning)

✅ Good: Icons with labels
🏠 Home  📊 Stats  ⚙️ Settings  ❓ Help
```

**2. Inconsistent Navigation**
```
❌ Bad:
Page 1: Nav at top
Page 2: Nav at side
Page 3: Nav at bottom

✅ Good:
All pages: Nav in same location
```

**3. Hidden Primary Actions**
```
❌ Bad: Essential feature buried in dropdown

✅ Good: Primary actions always visible
```

**4. Too Many Levels**
```
❌ Bad:
Home → Cat → Subcat → Sub-subcat → Sub-sub-subcat → Content

✅ Good:
Home → Category → Content (2-3 levels max)
```

**5. Breaking Browser Back**
```
❌ Bad: Back button doesn't work as expected
         (Modal closes page, AJAX breaks history)

✅ Good: Back behaves predictably
```

### Flow Anti-Patterns

**1. No Clear Starting Point**
```
❌ Bad: User lands on page with no clear action

✅ Good: Clear primary CTA, obvious next step
```

**2. Premature Data Collection**
```
❌ Bad:
Step 1: 20 questions before any value

✅ Good:
Step 1: Quick win / See value
Step 2: Progressive questions
```

**3. Forced Linear Path**
```
❌ Bad: Can't skip optional steps
         Can't go back to edit

✅ Good: Allow skipping, editing, flexible order
```

**4. No Progress Indication**
```
❌ Bad: Multi-step form with no indicator
         User doesn't know how long it will take

✅ Good: Show progress: "Step 2 of 5"
```

**5. Context Loss**
```
❌ Bad: User clicks link, can't remember where they came from

✅ Good: Breadcrumbs, clear navigation, back option
```

### Form Anti-Patterns

**1. Asking for Too Much**
```
❌ Bad: 30 fields in signup form

✅ Good: Essential only, progressive profiling
```

**2. Unclear Required Fields**
```
❌ Bad: No indication which fields are required
         Or all marked as required

✅ Good: Mark required with *, explain at top
```

**3. Generic Error Messages**
```
❌ Bad: "Error" "Invalid input" "Failed"

✅ Good: "Email must include @ symbol"
         "Password must be at least 8 characters"
```

**4. Losing Data on Error**
```
❌ Bad: Form submission fails, all data cleared

✅ Good: Preserve entered data, highlight errors
```

**5. Unclear Input Format**
```
❌ Bad:
Date: [________]
User enters: 1/14/2026
Error: "Invalid format"

✅ Good:
Date: [MM] / [DD] / [YYYY]
      📅 or use date picker
```

### Content Anti-Patterns

**1. Jargon Overload**
```
❌ Bad: "Utilize the egress functionality"

✅ Good: "Exit" or "Leave"
```

**2. Wall of Text**
```
❌ Bad: Dense paragraphs, no structure

✅ Good: Headings, bullet points, short paragraphs
```

**3. Ambiguous Labels**
```
❌ Bad: "Click here" "Submit" "OK"

✅ Good: "Download report" "Create account" "Save changes"
```

**4. Inconsistent Terminology**
```
❌ Bad: "Delete" on one screen, "Remove" on another

✅ Good: Pick one term, use consistently
```

### Interaction Anti-Patterns

**1. Fake Buttons**
```
❌ Bad: Non-interactive elements look clickable

✅ Good: Clear affordance (buttons look like buttons)
```

**2. Hover-Only Actions**
```
❌ Bad: Critical action only on hover
         (Fails on mobile, accessibility)

✅ Good: Actions always accessible
```

**3. Unclear Clickability**
```
❌ Bad: Links look like regular text
         Buttons look flat, unclickable

✅ Good: Clear visual affordance
```

**4. Accidental Actions**
```
❌ Bad: Delete button next to save button
         No confirmation for destructive action

✅ Good: Separate dangerous actions, confirm
```

**5. Inconsistent Interactions**
```
❌ Bad: Click to expand in one place, click to navigate in another

✅ Good: Same interaction pattern throughout
```

### Mobile Anti-Patterns

**1. Tiny Tap Targets**
```
❌ Bad: 20px buttons on mobile

✅ Good: Minimum 44x44px tap targets
```

**2. Desktop UI on Mobile**
```
❌ Bad: Desktop site shrunk down

✅ Good: Mobile-specific design, thumb-friendly
```

**3. Horizontal Scrolling**
```
❌ Bad: Requires horizontal scroll to see content

✅ Good: Vertical scroll only, responsive layout
```

**4. Fat Finger Issues**
```
❌ Bad: Tiny checkboxes, close-together links

✅ Good: Large targets, adequate spacing
```

**5. Fixed Elements Blocking Content**
```
❌ Bad: Fixed header/footer covers 50% of screen

✅ Good: Minimal fixed elements, hide on scroll
```

### Accessibility Anti-Patterns

**1. No Keyboard Access**
```
❌ Bad: Must use mouse to interact

✅ Good: Full keyboard navigation
```

**2. No Focus Indicator**
```
❌ Bad: Can't see where keyboard focus is

✅ Good: Clear, visible focus state
```

**3. Low Contrast**
```
❌ Bad: Light gray text on white background

✅ Good: 4.5:1 contrast ratio minimum
```

**4. Missing Alt Text**
```
❌ Bad: <img src="product.jpg">

✅ Good: <img src="product.jpg" alt="Blue running shoes">
```

**5. Keyboard Trap**
```
❌ Bad: Can tab in but can't tab out of modal

✅ Good: Escape key closes, focus trapped appropriately
```

---

## Conclusion

User flows and information architecture are the foundation of good UX. By carefully structuring information, designing clear navigation, and optimizing task flows, you create experiences that are intuitive, efficient, and delightful.

### Key Takeaways

**Always**:
- Start with user goals
- Test with real users
- Iterate based on data
- Follow accessibility standards
- Maintain consistency
- Provide clear feedback
- Design for recovery

**Never**:
- Assume you know best
- Skip testing
- Hide critical information
- Break expected patterns
- Overwhelm with choices
- Ignore mobile experience
- Forget accessibility

### Further Resources

**Books**:
- "Information Architecture" by Louis Rosenfeld & Peter Morville
- "Don't Make Me Think" by Steve Krug
- "The Design of Everyday Things" by Don Norman

**Tools**:
- Figma, Sketch (wireframing)
- Optimal Workshop (card sorting, tree testing)
- UserTesting (usability testing)
- Hotjar (analytics, heatmaps)
- Miro, FigJam (collaborative diagramming)

**Standards**:
- WCAG 2.1 (accessibility)
- Material Design (Android patterns)
- Human Interface Guidelines (iOS patterns)

---

*Remember: Good user flows are invisible. The best designs guide users seamlessly to their goals without them thinking about navigation at all.*


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

