---
last_updated: 2026-02-25
status: active
name: modularity-design
description: Design products that improve through repair and upgrade rather than replacement. Use when planning component architecture, interfaces, or long-term product evolution.
triggers:
  files: ["**/product/**", "**/assembly/**", "**/repair/**"]
  keywords: ["modular", "upgradeable", "repairable", "right to repair", "component", "interface", "replacement parts", "serviceability"]
allowed-tools: Read, Write, Edit
---

# Modularity Design

## Principle

**Repair and upgrade extend life; replacement ends it.**

Design systems that evolve, not expire.

---


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Core Question

**"How does this get better, not replaced?"**

---

## Anti-Pattern

**Planned obsolescence, sealed components, proprietary interfaces.**

Products designed to be discarded when one component fails or becomes outdated.

---

## Modularity Levels

| Level | Description | User Control | Example |
|-------|-------------|--------------|---------|
| Component | Individual parts replaceable | High | Swappable battery |
| Subsystem | Functional groups upgradeable | Medium | Camera module upgrade |
| Interface | Connections standardized | Medium | USB-C charging port |
| Compatibility | Future parts work with today's base | Low | Backward-compatible mounts |

---

## Design Patterns

| Pattern | Benefit | Implementation |
|---------|---------|----------------|
| Visible fasteners | User can access internals | Phillips/hex screws, not glue |
| Standard connectors | Parts available long-term | Industry standards (USB, HDMI) |
| Upgrade paths | New capabilities without replacement | Modular slots, expansion bays |
| Repair documentation | Users can maintain | Public teardown guides, diagrams |
| Wear indicators | Know when to replace | Visual markers, diagnostic modes |

---

## Interface Design

### Connection Types

| Type | Modularity Strength | Use Case |
|------|-------------------|----------|
| Threaded fastener | User-serviceable, reversible | Structural assembly |
| Snap-fit | Tool-free, repeatable cycles | Battery doors, covers |
| Magnetic | Instant, alignment-free | Accessories, alignment |
| Friction fit | Simple, no tools | Cable retention |
| Adhesive | **Anti-modular** (avoid) | Permanent bonds only |

### Connector Standards

| Standard | Advantage | Longevity Risk |
|----------|-----------|----------------|
| Open standard | Wide availability | Low risk |
| Industry standard | Common parts | Medium risk |
| Proprietary | Vendor control | High risk |

---

## Component Architecture

### Grouping Strategy

| Strategy | Principle | Example |
|----------|-----------|---------|
| Wear-based | Fast-wearing parts isolated | Replaceable bearing cartridge |
| Tech-based | Upgradeable tech separate from durable base | Motherboard in metal chassis |
| Function-based | Independent subsystems | Separate motor and control board |

### Design for Disassembly

| Technique | Purpose | Anti-Pattern |
|-----------|---------|--------------|
| Layered assembly | Sequential removal | Components that block each other |
| Captive fasteners | Fasteners stay with part | Loose screws that get lost |
| Color-coded parts | Easy identification | Unmarked components |
| Single-tool disassembly | Minimal tool set | Multiple proprietary drivers |

---

## Upgrade Paths

| Upgrade Type | Design Consideration | Example |
|--------------|---------------------|---------|
| Performance | Reserve capacity in base | Faster processor in same socket |
| Capacity | Expandable architecture | Additional RAM slots |
| Features | Modular bays | Add-on sensor modules |
| Aesthetics | Swappable covers | Replaceable faceplates |

---

## Critical Questions

### Component Level
- Can users replace worn components?
- Are wear parts clearly identified?
- Do fasteners require special tools?

### Interface Level
- Are connection standards open or proprietary?
- Can interfaces handle future upgrades?
- Are connectors rated for repeated cycles?

### System Level
- Will parts be available in 10 years?
- Does repair require special tools?
- Can one failed component kill the whole product?

### Business Model
- Is revenue from replacement or longevity?
- Are repair parts priced fairly?
- Is repair documentation public?

---

## Signs of Anti-Modularity

| Red Flag | Implication | User Impact |
|----------|-------------|-------------|
| Glued assemblies | Permanent bonds | Unrepairable |
| Proprietary fasteners | Special tools required | Service monopoly |
| Components that fail together | No isolation | Total replacement |
| Upgrade = full replacement | No evolution path | Forced obsolescence |
| Sealed enclosures | "Do not open" | Vendor lock-in |
| Serialized parts pairing | Software blocks repair | Right-to-repair violation |

---

## Repairability Metrics

| Metric | Calculation | Target |
|--------|-------------|--------|
| Fastener variety | Number of driver types | ≤2 types |
| Disassembly steps to [component] | Count from start | ≤10 steps |
| Special tools required | Proprietary tools needed | 0 tools |
| Parts availability | Years parts remain in stock | 10+ years |
| Repair documentation | Publicly available guides | Yes |

---

## Case Study Patterns

### High Modularity
- **Fairphone:** User-replaceable screen, battery, camera
- **Framework Laptop:** Swappable ports, upgradeable mainboard
- **Leatherman tools:** Individual tool replacement

### Low Modularity (Anti-Patterns)
- **Glued smartphones:** Battery replacement requires heat gun
- **Sealed earbuds:** Unrepairable, disposable
- **Proprietary batteries:** Only vendor sells replacements

---

## Design Process Integration

### Requirements Phase
- Define modularity tier for product category
- Identify high-wear components
- Plan upgrade roadmap

### Design Phase
- Specify standard connectors
- Design disassembly sequence
- Create repair documentation

### Manufacturing Phase
- Ensure parts availability pipeline
- Test connector cycle life
- Validate repair procedures

---

## Output Format

When evaluating modularity:

```
Component: [Name]
Replacement: [User/Service/Impossible]
Interface: [Standard/Proprietary]
Lifespan: [Years] vs Product: [Years]
Upgrade Path: [Yes/No]
Documentation: [Public/Private/None]
```

---

## Integration with Other Skills

- **Lifecycle Design:** Modularity extends product life
- **Material Selection:** Choose durable materials for reused base
- **Manufacturing Processes:** Design joints for disassembly
- **Aesthetic Timelessness:** Classic design ages better than trends


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

