---
last_updated: 2026-02-25
status: active
name: lifecycle-design
description: Design products with cradle-to-grave responsibility, considering environmental impact at every phase. Use when evaluating material choices, manufacturing processes, or end-of-life scenarios.
triggers:
  files: ["**/sustainability/**", "**/materials/**", "**/manufacturing/**"]
  keywords: ["lifecycle", "sustainability", "recyclable", "end-of-life", "environmental impact", "material sourcing", "embodied energy", "circular economy"]
allowed-tools: Read, Write, Edit
---

# Lifecycle Design

## Principle

**Design responsibility extends from cradle to grave.**

Based on Dieter Rams Principle #9: Good design is environmentally friendly.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Core Question

**"What happens at end of life?"**

Every material choice, joint, and finish determines whether a product becomes future resource or future waste.

---

## Lifecycle Phases Framework

| Phase | Consideration | Design Impact |
|-------|---------------|---------------|
| Sourcing | Where do materials come from? | Material selection, supplier ethics |
| Manufacturing | What's the production impact? | Process efficiency, waste streams |
| Distribution | How does it reach users? | Packaging, shipping weight, bulk |
| Use | Energy/resource consumption | Operational efficiency, maintenance |
| End of life | Recycle, repair, or landfill? | Disassembly, material separation |

---

## Evaluation Criteria

| Criterion | Question | Red Flags |
|-----------|----------|-----------|
| Material efficiency | Minimum material for function? | Excessive wall thickness, unused volume |
| Recyclability | Can materials be separated? | Mixed composites, laminated materials |
| Toxicity | Any hazardous materials? | Heavy metals, persistent chemicals |
| Energy | Embodied + operational energy? | Energy-intensive materials, high-use power |
| Longevity | Years of useful life? | Fashion-driven design, fragile components |

---

## Design Decisions

### Material Selection

| Material Type | Lifecycle Strength | Lifecycle Weakness |
|---------------|-------------------|-------------------|
| Aluminum | Infinitely recyclable, high value | High embodied energy |
| Steel | Durable, recyclable | Corrosion requires coatings |
| Wood | Renewable, low embodied energy | Moisture sensitivity |
| ABS plastic | Moldable, recyclable | Petroleum-based, degrades |
| Composites | Lightweight, strong | Difficult to separate/recycle |

### Manufacturing Processes

| Process | Impact Consideration |
|---------|---------------------|
| Injection molding | High initial energy, efficient at scale |
| CNC machining | Material waste in chips |
| Casting | Energy-intensive, good for complex forms |
| 3D printing | Minimal waste, slow for volume |
| Sheet forming | Efficient material use |

---

## Disassembly Design Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| Mono-material construction | Simplify recycling | All-aluminum laptop body |
| Snap-fit joints | Tool-free disassembly | Battery compartment latches |
| Labeled materials | Aid sorting | Plastic type stamps |
| Gravity separation | Materials fall apart by density | Layered assemblies |

---

## Critical Questions

### Sourcing Phase
- Is this material renewable or finite?
- What's the extraction/harvesting impact?
- How far does raw material travel?

### Manufacturing Phase
- Can waste be reused in the process?
- What emissions result from production?
- Could a simpler process achieve the same result?

### Use Phase
- Does this consume energy during use?
- What maintenance does it require?
- Are consumables renewable?

### End-of-Life Phase
- **Can this be disassembled for recycling?**
- **What happens to this in 50 years?**
- **Could the same function use less material?**
- **Is longevity a feature of the design?**

---

## Red Flags

| Warning Sign | Implication |
|--------------|-------------|
| "Lifetime sealed bearing" | Unrepairable = disposable |
| Mixed material bonding | Inseparable = landfill |
| Fashion-driven aesthetics | Short lifespan by design |
| No material labeling | Recycler can't sort it |
| Exotic alloys | No recycling infrastructure |

---

## Circular Economy Alignment

| Principle | Design Action |
|-----------|---------------|
| Keep materials in use | Design for durability and repair |
| Regenerate natural systems | Use renewable, non-toxic materials |
| Design out waste | Mono-material or easily separable |

---

## Output Format

When evaluating lifecycle impact:

```
Phase: [Sourcing/Manufacturing/Use/End-of-life]
Material: [Primary material]
Impact: [Environmental consideration]
Alternative: [Lower-impact option]
Trade-off: [Performance/cost consideration]
```

---

## Integration with Other Skills

- **Modularity Design:** Extends life through repair/upgrade
- **Material Selection:** Prioritize recyclable, renewable options
- **Manufacturing Processes:** Choose low-waste methods
- **Aesthetic Reduction:** Less material, less impact


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

