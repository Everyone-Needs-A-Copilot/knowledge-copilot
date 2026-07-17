---
last_updated: 2026-02-25
status: active
name: ia-structure-design
description: Information architecture design - organizing content, defining hierarchies, creating sitemaps and taxonomies. Use for structuring content.
triggers:
  files: ["**/sitemap/**", "**/navigation/**", "**/taxonomy/**", "**/ia/**"]
  keywords: ["information architecture", "IA", "sitemap", "taxonomy", "hierarchy", "content structure", "organization", "categories", "navigation structure"]
allowed-tools: Read, Write, Edit
---

# Information Architecture Design Skill

Master guide for designing information architecture - organizing content, creating hierarchies, defining taxonomies, and structuring navigation.

## Philosophy

**IA is invisible when done well.** Users find things effortlessly. They don't think about structure; they just accomplish goals.

**Structure follows user mental models.** Organize content how users think about it, not how your organization is structured.

**Findability over elegance.** A simple, findable structure beats an elegant, confusing one.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Core IA Components

### 1. Organization Systems

How content is grouped and classified.

**Organization Schemes**:

| Type | Description | Example |
|------|-------------|---------|
| **Alphabetical** | A-Z ordering | Directory, glossary |
| **Chronological** | Time-based | News, history, activity |
| **Geographic** | Location-based | Store finder, regional content |
| **Topic** | Subject-based | Categories, departments |
| **Task** | Action-based | "Pay bill", "Track order" |
| **Audience** | User-based | "For developers", "For students" |

**Organization Structures**:

**Hierarchy** (tree):
```
         Home
           │
    ┌──────┼──────┐
    │      │      │
Products Services About
    │
 ┌──┴──┐
Cat A  Cat B
```
Best for: Content-heavy sites

**Database** (faceted):
```
Products filtered by:
├─ Category
├─ Price
├─ Rating
└─ Brand
```
Best for: E-commerce, search-heavy

**Network** (hypertext):
```
Page ←→ Related Page
  ↓         ↓
Tag      Category
```
Best for: Wikis, knowledge bases

**Linear** (sequential):
```
Step 1 → Step 2 → Step 3 → Done
```
Best for: Wizards, onboarding

### 2. Labeling Systems

How content is named and described.

**Label Types**:
- Navigation labels (menu items)
- Heading labels (section titles)
- Link labels (inline text links)
- Index labels (tags, categories)
- Iconic labels (icon meanings)

**Labeling Principles**:
- Use user language
- Be consistent
- Be specific ("Email settings" not "Settings")
- Avoid jargon
- Test with users

### 3. Navigation Systems

How users move through content.

**Navigation Types**:

| Type | Purpose | Example |
|------|---------|---------|
| Global | Site-wide access | Main menu |
| Local | Section navigation | Sidebar menu |
| Contextual | Content-related | Related articles |
| Supplemental | Alternative paths | Sitemap, index |
| Utility | Non-content | Search, login |

### 4. Search Systems

How users find specific content.

**Search Components**:
- Search interface
- Query language
- Results display
- Filters/facets
- Search suggestions

---

## IA Design Process

### 1. Research

**Content inventory**:
```markdown
| ID | URL | Title | Type | Owner | Status |
|----|-----|-------|------|-------|--------|
| 1 | /about | About Us | Page | Marketing | Current |
| 2 | /products | Products | Landing | Product | Outdated |
[...]
```

**User research**:
- Card sorting (how users group)
- Tree testing (how users find)
- User interviews (mental models)
- Analytics (current behavior)

### 2. Strategy

Define:
- Primary user tasks
- Key content areas
- Business requirements
- Success metrics

### 3. Design

Create:
- Site map
- Taxonomy
- Page templates
- Navigation model

### 4. Validate

Test with:
- Tree testing
- Card sorting (reverse)
- Usability testing
- First-click testing

---

## Sitemaps

### Sitemap Types

**Structural sitemap**:
```
Home
├─ Products
│  ├─ Category A
│  │  ├─ Product 1
│  │  └─ Product 2
│  └─ Category B
├─ About
│  ├─ Team
│  └─ History
└─ Contact
```

**Detailed sitemap**:
```
┌─────────────────────────────────────┐
│ Home                                │
│ Template: Homepage                  │
│ CMS: Yes                            │
│ Owner: Marketing                    │
├─────────────────────────────────────┤
│ Primary Nav: Products, About, Contact
│ Secondary: Login, Search            │
└─────────────────────────────────────┘
         │
    ┌────┴────┐
    │         │
┌───┴───┐ ┌───┴───┐
│Products│ │ About │
│...     │ │...    │
└────────┘ └───────┘
```

### Sitemap Best Practices

- Show hierarchy clearly
- Include all pages
- Note templates/page types
- Indicate dynamic content
- Show navigation relationships
- Version and date

---

## Taxonomy Design

### Taxonomy Types

**Hierarchical** (category tree):
```
Electronics
├─ Computers
│  ├─ Laptops
│  └─ Desktops
└─ Phones
   ├─ Smartphones
   └─ Accessories
```

**Faceted** (multiple dimensions):
```
Product can have:
├─ Category: Electronics > Computers > Laptops
├─ Brand: Apple, Dell, HP
├─ Price range: $500-$1000
└─ Rating: 4+ stars
```

**Flat** (tags):
```
Tags: javascript, react, tutorial, beginner
```

### Taxonomy Principles

**MECE** (Mutually Exclusive, Collectively Exhaustive):
- Each item belongs in one place
- All items have a place

**Depth vs Breadth**:
```
Deep (narrow):          Shallow (wide):
Home                    Home
└─ Cat                  ├─ Cat A
   └─ Subcat            ├─ Cat B
      └─ Sub-subcat     ├─ Cat C
         └─ Content     ├─ Cat D
                        └─ Cat E

Recommendation: 2-4 levels, 5-9 items per level
```

**Controlled vocabulary**:
```
Preferred term: "Documentation"
Variants: "Docs", "Help", "Manual"
→ Always use "Documentation"
```

---

## Navigation Design

### Global Navigation

**Desktop pattern**:
```
┌────────────────────────────────────────────┐
│ [Logo] Products Services Resources About   │
│                           [Search] [Login] │
└────────────────────────────────────────────┘
```

**Mega menu**:
```
Products ▼
┌─────────────────────────────────────────────┐
│ Category A     Category B     Featured      │
│ ─────────      ─────────      ─────────     │
│ Item 1         Item 1         [Image]       │
│ Item 2         Item 2         New product   │
│ Item 3         Item 3         Learn more →  │
│                                             │
│ [View all products →]                       │
└─────────────────────────────────────────────┘
```

### Local Navigation

**Sidebar**:
```
Section Title
├─ Current Page ← (highlighted)
├─ Sibling Page
├─ Sibling Page
└─ Parent Section ▼
   ├─ Child Page
   └─ Child Page
```

**Breadcrumbs**:
```
Home > Products > Laptops > MacBook Pro
```

### Mobile Navigation

**Priority+**:
```
Desktop: [Home] [Products] [Services] [About] [Contact]
Mobile:  [Home] [Products] [More ▼]
```

**Hamburger**:
```
[☰]  App Name
     ─────────────
     [Content area]
```

### Navigation Patterns Comparison

| Pattern | Pros | Cons |
|---------|------|------|
| Horizontal nav | Familiar, visible | Limited items |
| Mega menu | Many items, organized | Complex |
| Sidebar | Flexible, expandable | Takes space |
| Hamburger | Saves space | Hidden, extra tap |
| Tab bar | Mobile-friendly | Limited items |
| Bottom sheet | Mobile native | Requires gesture |

---

## Testing IA

### Card Sorting

**Open sort** (users create groups):
```
Instructions: Group these items and name the groups

Cards: [Product A] [Feature B] [Service C] [About] ...

Results reveal natural groupings
```

**Closed sort** (predefined groups):
```
Instructions: Sort items into these categories

Categories: [Products] [Services] [Support] [Company]
Cards: [Product A] [Feature B] ...

Results show agreement with proposed structure
```

### Tree Testing

Test findability without UI:
```
Task: "Where would you find pricing information?"

Tree:
Home
├─ Products
│  ├─ Features
│  └─ Pricing ← 85% found it here
├─ Resources
└─ Company

Success rate: 85%
Directness: 78% (no backtracking)
```

### First-Click Testing

```
Task: "Find customer support"
Show: Homepage screenshot

Results:
- 60% clicked "Help" icon
- 20% clicked "Contact"
- 10% clicked search
- 10% other

Conclusion: Help icon works but consider label
```

---

## IA Documentation

### Page Tables

| Page | URL | Template | Parent | Content Type |
|------|-----|----------|--------|--------------|
| Home | / | Homepage | - | Dynamic |
| Products | /products | Listing | Home | Dynamic |
| Product A | /products/a | Product | Products | CMS |

### Content Models

```yaml
Product:
  title: string (required)
  description: text
  price: number
  category: reference → Category
  images: array → Image
  tags: array → Tag

Category:
  name: string
  parent: reference → Category
  description: text
```

### Navigation Specifications

```markdown
## Global Navigation

**Location:** Header, sticky on scroll
**Items:**
1. Logo → Home
2. Products → /products (mega menu)
3. Services → /services
4. Resources → /resources (dropdown)
5. About → /about

**Utility:**
- Search → /search
- Login → /login (or "My Account" if logged in)

**Mobile behavior:**
- Collapses to hamburger at 768px
- Logo always visible
- Search icon separate
```

---

## Quick Reference

### IA Design Checklist

- [ ] Content inventory complete
- [ ] User research conducted
- [ ] Mental models understood
- [ ] Organization scheme chosen
- [ ] Taxonomy defined
- [ ] Navigation designed
- [ ] Sitemap documented
- [ ] Labeling consistent
- [ ] Tree testing passed
- [ ] Card sorting validated

### Common IA Mistakes

| Mistake | Solution |
|---------|----------|
| Too deep | Max 4 levels, flatten structure |
| Too wide | Max 7±2 items per level |
| Internal naming | Use user language |
| Inconsistent labels | Create controlled vocabulary |
| No search | Add search for 50+ pages |
| Single path | Multiple ways to find content |

### Depth Guidelines

| Content Size | Max Depth | Notes |
|--------------|-----------|-------|
| Small (< 50 pages) | 2 levels | Home + pages |
| Medium (50-500) | 3 levels | Add categories |
| Large (500-5000) | 4 levels | Add subcategories |
| Enterprise (5000+) | 4 levels + search | Never deeper |

---

## Summary

**Good IA = Invisible structure**

1. Research user mental models
2. Organize content how users think
3. Use clear, consistent labels
4. Design navigation for key tasks
5. Test structure before building
6. Document for implementation

*Users should never think about where to find things - they just find them.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

