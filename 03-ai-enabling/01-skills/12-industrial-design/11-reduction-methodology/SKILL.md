---
last_updated: 2026-02-25
status: active
name: reduction-methodology
description: Systematic subtraction methodology - removing everything non-essential until only the necessary remains. Use when simplifying designs or eliminating complexity.
triggers:
  files: ["**/industrial/**", "**/simplify/**", "**/reduction/**"]
  keywords: ["less but better", "simplification", "reduction", "minimal", "essential", "subtract", "remove features", "overcomplicated", "simplify design"]
allowed-tools: Read, Write, Edit
---

# Reduction Methodology Skill

Master framework for systematic reduction—removing everything non-essential until only the necessary remains. Dieter Rams' "Less, but better" made actionable.

## Philosophy

**Subtract until it breaks, then add one thing back.**

Most products are over-designed. Complexity accumulates. Features multiply. Controls proliferate. The discipline of reduction reveals what truly matters.

**Rams Principle #10:** Good design is as little design as possible. Back to purity, back to simplicity.

---


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## The Reduction Framework

| Level | Question | Action |
|-------|----------|--------|
| **Features** | Does this function justify its complexity? | Remove features used <20% of time |
| **Components** | Can two parts become one? | Consolidate, integrate, eliminate |
| **Materials** | Can we use fewer distinct materials? | Reduce material palette |
| **Surfaces** | Can finishes be simplified? | Unify surface treatments |
| **Colors** | Can the palette be reduced? | Single color or two-color max |
| **Controls** | Can interactions be combined? | Merge redundant controls |

---

## The Reduction Process

### Step 1: List Every Element

Create exhaustive inventory.

```
Example: Coffee Grinder

Features:
• Grind adjustment (8 settings)
• Bean capacity indicator
• Grind timer
• Dose counter
• Cleaning brush storage
• Bean freshness display
• Grinding sound dampening
• Anti-static coating
• Bean hopper lock
• Portafilter holder

Components:
• Upper housing
• Lower housing
• Bean hopper
• Hopper lid
• Grind chamber
• Burr set (upper/lower)
• Motor assembly
• Power switch
• Timer dial
• Adjustment dial
• Catch cup
• Cleaning brush
• Rubber feet (4x)
• Power cord
```

### Step 2: Test Removal

For each element: "What happens if we remove this?"

| Element | Removal Test | Keep? |
|---------|--------------|-------|
| **Grind adjustment** | Can't vary grind size → BREAKS | ✓ Keep |
| **Bean capacity indicator** | User can see beans through hopper → WORKS | ✗ Remove |
| **Grind timer** | User can count/watch → OPTIONAL | ? Test |
| **Dose counter** | Nice but not essential → WORKS | ✗ Remove |
| **Brush storage** | Brush can live elsewhere → WORKS | ✗ Remove |
| **Freshness display** | User can date label → WORKS | ✗ Remove |
| **Sound dampening** | Louder but functional → WORKS | ✗ Remove |
| **Anti-static** | Some mess but usable → WORKS | ✗ Remove |
| **Hopper lock** | Gravity holds hopper → TEST REQUIRED | ? Test |
| **Portafilter holder** | User can hold it → WORKS | ✗ Remove |

**Rule:** If it works without it—remove it.

### Step 3: Component Consolidation

Can separate parts become one?

```
Before Reduction:
• Upper housing + lower housing = 2 parts
• Bean hopper + hopper lid = 2 parts
• Catch cup (separate component)

After Reduction:
• Single housing (clamshell design)
• Hopper with integrated lid (hinge or press-fit)
• Catch cup eliminated (grind directly to portafilter)

Result: 6 parts → 2 parts
```

### Step 4: Material Reduction

How many distinct materials?

```
Before:
• ABS plastic (housing)
• Polycarbonate (hopper - clear)
• Aluminum (burr housing)
• Stainless steel (burrs)
• Silicone (feet)
• Rubber (power switch)
• Glass (catch cup)

After:
• Aluminum (entire housing + burr assembly)
• Stainless steel (burrs only)
• Silicone (feet only)

Result: 7 materials → 3 materials
```

### Step 5: Surface Simplification

One finish, one treatment.

```
Before:
• Brushed aluminum top
• Glossy black sides
• Matte black base
• Chrome accents
• Textured grip zones

After:
• Natural anodized aluminum (entire exterior)
• No texture (form provides grip)

Result: 5 finishes → 1 finish
```

### Step 6: Color Reduction

Single color or two-color maximum.

```
Before:
• Black housing
• Silver accents
• Red power indicator
• Blue capacity indicator
• White labels
• Chrome trim

After:
• Natural aluminum (silver)
• Black text (labels only)

Result: 6 colors → 2 colors
```

### Step 7: Control Consolidation

Can controls be combined?

```
Before:
• Power switch (on/off)
• Timer dial (0-60 seconds)
• Grind adjustment (8 positions)
• Dose button (single/double)

After:
• Grind adjustment dial (integrated on/off at position 0)
• Manual operation (user controls timing)

Result: 4 controls → 1 control
```

---

## Signs of Over-Design

### Feature Bloat

```
✗ Multiple ways to do the same thing
  → Pick one method

✗ Controls rarely or never used
  → Remove

✗ "Premium" features that add complexity
  → Question necessity

✗ Features requiring explanation
  → Remove or redesign
```

### Component Excess

```
✗ Decorative panels (non-structural)
  → Eliminate

✗ Snap-fit covers over screws
  → Expose screws or eliminate

✗ Separate indicator windows
  → Integrate into main surface

✗ Redundant fasteners
  → Reduce to minimum
```

### Material Variety

```
✗ Chrome accent trim
  → Same material as base

✗ Different plastics for each component
  → Single material family

✗ Rubber overmolding for "premium feel"
  → Form provides grip
```

### Surface Treatment Proliferation

```
✗ Glossy + matte + textured + brushed
  → Pick one

✗ Decorative patterns
  → Remove

✗ Fake material textures (faux leather, carbon fiber)
  → Honest materials
```

---

## Validation Tests

### The "Explain the Absence" Test

After removal, can you explain why it's missing?

```
"Why no timer display?"
✓ "User controls timing manually—no need"

"Why no bean capacity indicator?"
✓ "Transparent hopper shows beans directly"

"Why no brush storage?"
✗ "Uh... we wanted it simpler?" → Not justified
```

If you can't explain the absence with functional reasoning, test adding it back.

### The "First-Time User" Test

Can someone use it without instructions?

```
✓ Single dial, obvious rotation → intuitive
✗ Three buttons, unclear sequence → not intuitive
```

If removal breaks intuitiveness, reconsider.

### The "20% Rule"

Features used <20% of the time are candidates for removal.

```
Usage analysis:
• Grind adjustment: 5% of interactions (set once, rarely changed)
• Power on: 100% of interactions
• Timer: 30% of interactions (many users stop manually)
• Dose counter: 2% of interactions (niche use case)

Remove:
✗ Dose counter (2%)
? Timer (30% - borderline, test)

Keep:
✓ Grind adjustment (essential despite low frequency)
✓ Power on (100%)
```

---

## Reduction Strategies

### Strategy 1: Integration

Combine functions into fewer parts.

```
Before: Separate hopper + lid + lock
After: Hopper with press-fit lid (friction holds)

Before: Switch + indicator light
After: Switch illuminates when on (integrated)
```

### Strategy 2: Elimination

Remove entirely.

```
Before: Cleaning brush with storage clip
After: Standard brush (user stores elsewhere)

Before: Dose counter
After: User counts (visual/tactile feedback)
```

### Strategy 3: Substitution

Replace complex with simple.

```
Before: Digital timer display (electronics, screen, buttons)
After: Mechanical timer dial (single moving part)

Before: LED capacity indicator (electronics, sensors)
After: Transparent hopper (direct viewing)
```

### Strategy 4: Unification

Make everything the same.

```
Before: 3 screw types (Phillips, hex, Torx)
After: All hex screws (single tool)

Before: Multiple plastics (ABS, PC, PP)
After: Single aluminum (one material)
```

---

## Reduction Scenarios

### Handheld Device Reduction

```
Start:
• 8 buttons
• 3 indicators
• 2 screens
• 4 materials
• 6 colors

Process:
• Combine functions → 3 buttons
• Eliminate redundant indicators → 1 LED
• Single screen → 1 display
• Unify materials → 2 materials (body + screen)
• Reduce palette → 2 colors (body + text)

Result:
• 3 buttons, 1 LED, 1 screen
• 2 materials, 2 colors
```

### Kitchen Appliance Reduction

```
Start:
• 12 function modes
• 4 control dials
• Digital display
• Timer
• Keep-warm function
• Auto-shutoff

Process:
• Question necessity → 3 essential modes
• Consolidate controls → 2 dials (mode + intensity)
• Remove display → Visual feedback (lights/sounds)
• Manual timing → User controls duration
• Remove keep-warm → Not core function
• Keep auto-shutoff → Safety essential

Result:
• 3 modes, 2 dials, auto-shutoff
```

---

## When NOT to Reduce

### Safety-Critical Elements

```
✓ Keep: Emergency stop button
✓ Keep: Safety interlocks
✓ Keep: Warning labels (essential only)
```

### Regulatory Requirements

```
✓ Keep: CE marking
✓ Keep: Electrical certifications
✓ Keep: Waste disposal symbols
```

### True User Needs (Not Wants)

```
Test: Does removal harm core function?
• If YES → keep
• If NO → remove
```

---

## Quick Reference

### Reduction Checklist

- [ ] Every element listed
- [ ] Removal test performed for each
- [ ] Components consolidated where possible
- [ ] Materials reduced to minimum
- [ ] Surfaces unified
- [ ] Color palette simplified (1-2 colors)
- [ ] Controls combined or eliminated
- [ ] Result tested with first-time user

### Questions to Ask

Before keeping any element:
1. What happens if we remove this?
2. Can this be integrated with something else?
3. Is this used >20% of the time?
4. Does this require explanation to understand?
5. Can we achieve the same result more simply?

### Reduction Red Flags

| Warning Sign | Action |
|--------------|--------|
| "But it's a nice feature" | Remove if usage <20% |
| "Users might want it someday" | Remove (add later if needed) |
| "It makes it look premium" | Premium comes from simplicity |
| "Everyone else has it" | Not a justification |
| "It only adds $1 to cost" | Cost isn't the point—complexity is |

---

## Summary

**Less, but better.**

1. List every element (features, parts, materials, finishes, colors, controls)
2. Test removal (what breaks? what still works?)
3. Consolidate components (two parts → one part)
4. Reduce materials (many → few)
5. Simplify surfaces (one finish)
6. Reduce colors (one or two)
7. Combine controls (fewer interactions)

**Stop when you've removed everything non-essential.**

*The result should feel inevitable—nothing more, nothing less.*


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

