---
last_updated: 2026-02-25
status: active
name: form-derivation
description: Derive form from function - letting shape emerge from purpose, interaction, constraints, and ergonomics. Use when designing physical products or questioning aesthetic decisions.
triggers:
  files: ["**/industrial/**", "**/product/**", "**/physical/**"]
  keywords: ["form follows function", "product design", "shape", "ergonomics", "physical design", "form language", "industrial design", "why this curve"]
allowed-tools: Read, Write, Edit
---

# Form Derivation Skill

Master framework for deriving form from function - answering "what shape does the function demand?" instead of "what shape do I want?"

## Philosophy

**Form is not decorative.** Every curve, angle, radius, and surface should justify its existence through function, interaction, constraint, or ergonomics.

**The question is always WHY.** If you cannot explain why a shape exists, you don't need it. Aesthetic preference is not explanation—functional necessity is.

**Rams Principle #2:** Good design makes a product useful. Function defines form, not the reverse.

---


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## The Form Derivation Framework

| Phase | Question | Output |
|-------|----------|--------|
| **1. Function** | What must this object DO? | List of core functions |
| **2. Interaction** | How do humans engage with it? | Touch points, grip zones, control surfaces |
| **3. Constraint** | What limits the form? | Technical, manufacturing, material constraints |
| **4. Ergonomics** | How does body meet object? | Hand sizes, reach distances, comfort zones |
| **5. Form** | What shape emerges? | Geometry that satisfies 1-4 |

### Phase 1: Define Function

List every function without aesthetic consideration.

```
Example: Coffee Grinder
✓ Hold whole beans (volume: 50g)
✓ Grind beans to adjustable coarseness
✓ Collect grounds without spilling
✓ Generate grinding force (hand crank or motor)
✓ Allow cleaning access
✓ Stable during use

✗ "Look modern" (not a function)
✗ "Match kitchen decor" (not a function)
```

### Phase 2: Map Human Interaction

Identify every point where hands, eyes, or body engages the object.

| Interaction Type | Design Implication |
|------------------|-------------------|
| **Grip zones** | Diameter must fit hand (25-40mm for power grip) |
| **Press surfaces** | Size must match finger/thumb pad (12-15mm min) |
| **Viewing areas** | Angle toward user, not ceiling |
| **Lift points** | Center of mass, not decorative handles |
| **Control surfaces** | Reachable without repositioning |

**Test:** Can you map every interaction without guessing?

### Phase 3: Identify Constraints

Technical and manufacturing limits that dictate form.

```
Material Constraints:
• Minimum wall thickness (injection molding: 0.8-1.5mm)
• Draft angles for mold release (1-3°)
• Material flex (glass breaks, rubber bends)
• Heat resistance requirements

Technical Constraints:
• Motor/mechanism volume and shape
• Electronics clearances
• Fastener locations
• Airflow/ventilation paths

Manufacturing Constraints:
• Parting lines (where molds separate)
• Undercut elimination
• Assembly sequence
• Tooling complexity = cost
```

### Phase 4: Ergonomic Requirements

Human body dimensions and comfort determine form.

| Body Interface | Requirement | Dimension |
|----------------|-------------|-----------|
| **Power grip** | Cylindrical handle | Ø 25-40mm |
| **Precision grip** | Small pinch surface | Ø 8-15mm |
| **Palm rest** | Flat or gentle curve | 40-60mm width |
| **Finger clearance** | Gap for fingers | 20mm minimum |
| **Thumb reach** | Control distance | 60-80mm max |
| **Viewing angle** | Display tilt | 10-30° toward user |
| **Carry weight** | Hand-held limit | <1.5kg comfortable |

**Sources:** Ergonomic data (Henry Dreyfuss, Anthropometric data sets)

### Phase 5: Form Emerges

Shape is the intersection of phases 1-4.

```
Coffee Grinder Example:

Function demands:
→ Cylindrical bean chamber (volume + gravity feed)

Interaction demands:
→ Grip diameter 30mm (hand size)
→ Crank handle offset 80mm (leverage)

Constraints demand:
→ Motor housing cylinder (hard geometry)
→ 1mm wall thickness (molding)
→ 2° draft angle (release)

Ergonomics demand:
→ Base width 100mm (stability)
→ Crank at 900mm height (standing use)

RESULT: Form is cylinder on stable base, crank offset
NOT: "Let's make it look like an hourglass"
```

---

## The Validation Test

### Can You Explain Every Curve?

For each shape element, trace it back to function/interaction/constraint/ergonomics.

| Shape Element | Justification Required |
|---------------|------------------------|
| Curved surface | Why curve? (Ergonomic fit? Structural need? Mold release?) |
| Angle change | Why this angle? (Viewing? Clearance? Strength?) |
| Radius | Why this size? (Safety? Grip? Manufacturing?) |
| Protrusion | Why protrude? (Control? Handle? Mechanism?) |
| Recess | Why recessed? (Finger access? Clearance? Drainage?) |

**If you cannot answer "why" with function/interaction/constraint/ergonomics—remove it.**

### Anti-Pattern Recognition

```
✗ "It looks better with a curve here"
  → Why does it look better? What does curve achieve?

✗ "This makes it more modern"
  → Modern isn't a function. What problem does shape solve?

✗ "Everyone does it this way"
  → Everyone might be wrong. Function hasn't changed.

✗ "The client wanted rounded corners"
  → What radius? Why? What's the functional benefit?
```

---

## Process Application

### Step-by-Step Derivation

```
1. Write Down Every Function
   • No aesthetics
   • No "it should feel..."
   • Only measurable capabilities

2. Map Every Human Interaction Point
   • Where do fingers touch?
   • Where do eyes look?
   • Where does hand grip?
   • What forces are applied?

3. List Every Technical Constraint
   • Material properties
   • Manufacturing method
   • Assembly requirements
   • Internal component geometry

4. Overlay Ergonomic Data
   • Hand/finger dimensions
   • Reach distances
   • Comfort zones
   • Force capabilities

5. Let Form Emerge From Intersection
   • Shape satisfies all 1-4
   • Nothing more, nothing less

6. Validate Every Surface
   • Point to function/interaction/constraint/ergonomic
   • Remove anything unexplainable
```

### Example: Redesigning a Door Handle

```
Phase 1: Function
• Transfer rotational force to latch
• Prevent accidental opening
• Signal pull/push direction
• Withstand 50kg force

Phase 2: Interaction
• Power grip: hand wraps handle
• Downward motion (gravity assists)
• Visual orientation cue

Phase 3: Constraints
• Latch mechanism: 50mm square
• Mounting holes: 38mm spacing
• Material: cast aluminum
• Door thickness: 35-45mm

Phase 4: Ergonomics
• Grip diameter: 30mm (adult hand)
• Lever length: 120mm (mechanical advantage)
• Clearance: 40mm from door (knuckles)
• Height: 1050mm (average reach)

Phase 5: Form Result
→ 30mm diameter cylindrical grip
→ 120mm horizontal lever
→ 90° downward rotation
→ 40mm offset from door surface
→ Simple cylinder—no decoration

NOT: "Let's add decorative ridges"
```

---

## Common Form Derivation Scenarios

### Handheld Objects

```
Derive from:
1. What hand position? (Grip type defines diameter)
2. What force direction? (Shape guides force application)
3. What controls needed? (Thumb/finger reach defines placement)
4. What weight? (Balance point defines mass distribution)
```

### Desktop Objects

```
Derive from:
1. What viewing angle? (Screen/display tilt)
2. What controls? (Button placement, reachability)
3. What footprint? (Desk space constraints)
4. What heat dissipation? (Vent geometry)
```

### Wearable Objects

```
Derive from:
1. What body part? (Anatomical curves)
2. What motion range? (Flex zones, rigid zones)
3. What contact pressure? (Comfort limits)
4. What adjustment range? (Body size variance)
```

---

## Quick Reference

### Form Derivation Checklist

- [ ] Every function listed (no aesthetics)
- [ ] Every interaction point mapped
- [ ] Every constraint documented
- [ ] Ergonomic data applied
- [ ] Form emerges from intersection
- [ ] Every surface justified
- [ ] Nothing unexplainable remains

### Questions to Ask

Before finalizing any shape:
1. What function requires this shape?
2. What interaction demands this geometry?
3. What constraint forces this form?
4. What ergonomic need dictates this curve?
5. Can I remove this and still meet 1-4?

### Red Flags

| Warning Sign | Action |
|--------------|--------|
| "It looks nicer" | Identify functional reason or remove |
| "Everyone does it" | Verify function still applies |
| "The client likes curves" | Define radius by ergonomics/constraints |
| "It needs personality" | Personality emerges from honest function |
| Multiple unexplained shapes | Strip to essentials, rebuild from function |

---

## Summary

**Form is not chosen—it is discovered.**

1. Define function (what it must DO)
2. Map interaction (where humans engage)
3. Identify constraints (technical/manufacturing limits)
4. Apply ergonomics (body meets object)
5. Let form emerge (intersection of 1-4)
6. Validate every curve (function/interaction/constraint/ergonomic)

*If you cannot explain WHY a shape exists—you don't need it.*


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

