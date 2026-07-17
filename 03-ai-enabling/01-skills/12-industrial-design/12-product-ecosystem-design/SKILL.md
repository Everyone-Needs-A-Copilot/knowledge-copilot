---
last_updated: 2026-02-25
status: active
name: product-ecosystem-design
description: Design coherent product families and ecosystems where products share visual DNA, interaction patterns, and semantic alignment. Use when designing multiple related products, extending product lines, or ensuring ecosystem coherence.
triggers:
  files: ["**/product-family/**", "**/ecosystem/**", "**/platform/**"]
  keywords: ["product family", "ecosystem", "product line", "visual language", "design system", "product platform"]
allowed-tools: Read, Write, Edit
---

# Product Ecosystem Design

**Principle:** A product is never alone—it exists in a family, an ecosystem, a life.

**Reference:** Braun product families (Rams), Apple ecosystem (Ive)

## The Question

**"How do these products relate?"**

A great product ecosystem feels like it comes from the same mind, the same moment, the same belief system. Users should recognize siblings instantly.

---


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Ecosystem Coherence Framework

| Dimension | Consistency Check | Transfer Test |
|-----------|-------------------|---------------|
| **Visual DNA** | Shared formal language, proportions, signature details | "Would a user recognize these as siblings?" |
| **Material Palette** | Common materials, finishes, textures | "Do these feel like they come from the same place?" |
| **Interaction Patterns** | Similar behaviors, gestures, responses across products | "Does learning one help with another?" |
| **Semantic Alignment** | Shared meaning of controls, indicators, feedback | "Do symbols/gestures mean the same thing?" |
| **Scale Relationship** | Products feel intentionally sized relative to each other | "Is the sizing logic evident?" |

---

## Design Process

### 1. Define Ecosystem Principles

Before designing products, define the family's design belief system.

**Essential Questions:**
- What is the unifying design philosophy?
- What is the core formal language? (geometry, proportions, relationships)
- What is the material truth? (honest use of materials)
- What is the interaction ethos? (minimal, gestural, tactile)

**Output:** 3-5 design principles that govern all products in ecosystem.

### 2. Establish Shared Design Language

**Visual Elements:**
| Element | Definition | Application |
|---------|------------|-------------|
| Formal vocabulary | Core shapes, angles, radii | Consistent across all products |
| Proportional system | Ratios, golden sections | Governs sizing relationships |
| Detail signature | Chamfers, edges, transitions | Recognizable family trait |
| Surface language | Textures, finishes, reveals | Material continuity |

**Example (Apple ecosystem):**
- Rounded rectangles with specific radius
- Chamfered edges on metal products
- Minimal visible seams
- Continuity of aluminum finishes

### 3. Map Transferable Interactions

**Interaction Transfer Matrix:**

| Interaction | Product A | Product B | Transfer Success |
|-------------|-----------|-----------|------------------|
| Power on/off | [Method] | [Method] | Does knowledge transfer? |
| Volume/intensity | [Method] | [Method] | Same logic? |
| Mode switching | [Method] | [Method] | Consistent pattern? |
| Status indication | [Method] | [Method] | Same visual language? |

**Goal:** User learns once, applies everywhere.

### 4. Design for "First Transfer"

**Critical moment:** User moves from Product A to Product B in the ecosystem.

**Test Scenario:**
1. User masters Product A
2. User encounters Product B
3. What happens in first 30 seconds?

**Success Criteria:**
- User recognizes family relationship immediately
- User tries familiar interaction from Product A
- Interaction works as expected on Product B
- User feels confidence, not confusion

### 5. Validate Coherence

**Blind Test Protocol:**

1. **Visual Test:**
   - Show products without branding
   - Ask: "Which belong together?"
   - Success: >90% group correctly

2. **Interaction Test:**
   - User learns Product A
   - Give Product B without instruction
   - Measure: Time to perform same task
   - Success: <2x the learning time

3. **Semantic Test:**
   - Show control/indicator from Product A
   - Ask: "What would this do on Product B?"
   - Success: >85% correct prediction

---

## Common Ecosystem Patterns

### Nested Products (Russian Doll)

Products designed to nest, stack, or contain each other.

**Examples:**
- Braun audio components
- Apple device families (iPhone in iPad in MacBook scale)

**Design Considerations:**
- Proportional relationships must be intentional
- Nesting should feel inevitable, not forced
- Negative space between products matters

### Modular Systems

Products that connect, expand, or reconfigure.

**Examples:**
- Vitsœ shelving (Rams)
- Modular synthesizers

**Design Considerations:**
- Connection language must be consistent
- Modules should feel complete alone or together
- Growth path should be intuitive

### Ambient Families

Products that coexist in space without physical connection.

**Examples:**
- Braun household products
- Apple ecosystem devices

**Design Considerations:**
- Visual harmony when seen together
- Shared design language without uniformity
- Each product has clear role/identity

---

## Anti-Patterns

### The Forced Family

**Symptom:** Products with superficial similarities (logo slap, color match) but no deeper coherence.

**Fix:** Return to ecosystem principles. Find true formal/interaction DNA.

### The Uncanny Similarity

**Symptom:** Products so similar users can't distinguish purpose.

**Fix:** Maintain family language, but give each clear formal differentiation based on function.

### The Broken Promise

**Symptom:** Visual similarity suggests interaction transfer, but products behave differently.

**Fix:** Either align interactions or differentiate visual language to signal difference.

---

## Evaluation Questions

**Visual Coherence:**
- Would a user recognize these as siblings in a blind test?
- Is the formal language consistent but not repetitive?
- Do proportional relationships feel intentional?

**Interaction Coherence:**
- Does learning one product help with another?
- Are there jarring differences in any dimension?
- Do similar controls mean the same thing across products?

**Ecosystem Logic:**
- Is there a clear reason these products belong together?
- Does the ecosystem enable something impossible with individual products?
- Can users predict how a new product in the family will work?

---

## Reference: Braun Product Families (Dieter Rams)

**Coherence Strategy:**
- Rigorous geometric language (circles, rectangles, precise radii)
- Consistent proportional system
- Material honesty (no fake finishes)
- Control semantics (same symbols, same meanings)
- Color restraint (white, black, gray, yellow accents)

**Result:** Decades of products instantly recognizable as family members, despite evolving technology.

---

## Reference: Apple Ecosystem (Jony Ive)

**Coherence Strategy:**
- Signature formal elements (rounded rectangles, chamfers)
- Material continuity (aluminum, glass)
- Interaction patterns (swipe, pinch, tap transfer across devices)
- Proportional harmony (devices feel right next to each other)
- Software-hardware coherence (physical and digital share language)

**Result:** Users move between devices with near-zero learning curve.


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

