---
last_updated: 2026-02-25
status: active
name: design-honesty-evaluation
description: Material and representation authenticity assessment. Use when evaluating whether design truthfully represents what it is and what it does.
triggers:
  files: ["**/industrial-design/**", "**/product-design/**", "**/material-design/**"]
  keywords: ["honesty", "authenticity", "materials", "truth", "Dieter Rams", "representation", "deception"]
allowed-tools: Read, Write, Edit
---

# Design Honesty Evaluation

**Core Principle:** Be what you claim to be — materials, function, and form should never deceive.

---

## Framework: Authenticity Assessment Matrix

| Evaluation Area | Question | Truth Test | Honesty Violation |
|----------------|----------|------------|-------------------|
| **Material** | Is this what it appears? | Real material matches appearance | Plastic looks like metal |
| **Construction** | How is this made? | Construction visible or implied honestly | Fake screws, false seams |
| **Function** | What can this do? | Form suggests actual capabilities | Looks powerful but isn't |
| **Capability** | What does this deliver? | Claims match performance | Overpromises, underdelivers |

---


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Process

### 1. Material Honesty Check

For each material used:

```markdown
## Material Inventory

| Material | Appearance | Reality | Honest? |
|----------|------------|---------|---------|
| Exterior shell | Appears to be [X] | Actually is [Y] | Yes/No |
| Buttons | Appears to be [X] | Actually is [Y] | Yes/No |
| Finish | Appears to be [X] | Actually is [Y] | Yes/No |
```

**Test:** Would a user feel deceived upon closer inspection?

### 2. Construction Honesty Check

**Ask:**
- Are we hiding construction or celebrating it?
- Do decorative elements pretend to be functional?
- Are structural elements disguised as decoration?

| Element | Appears to be | Actually is | Assessment |
|---------|---------------|-------------|------------|
| Screws | Functional | Decorative caps | Dishonest |
| Seam | Assembly point | Molded-in line | Dishonest |
| Exposed bolt | Decorative | Real fastener | Honest |

### 3. Form Honesty Check

**Does the form suggest false capabilities?**

```markdown
## Form-Function Alignment

### What form suggests: [Capability]
### What product delivers: [Reality]
### Alignment: Honest / Overstated / Understated

Examples:
- Massive cooling vents → Minimal heat generation (overstated)
- Racing stripe → No performance benefit (false association)
- Rugged texture → Not actually durable (misleading)
```

---

## Evaluation Questions

### Material Truth

1. **Does this material match its appearance?**
   - Real metal looks like metal → Honest
   - Plastic chrome looks like metal → Dishonest
   - Plastic looks like plastic → Honest

2. **Are we hiding construction or celebrating it?**
   - Visible screws, honest joints → Celebrating (honest)
   - Fake screw caps, hidden seams → Hiding (dishonest)

3. **Does the material pretend to be something else?**
   - Wood grain plastic → Pretending (dishonest)
   - Brushed aluminum → Being itself (honest)

### Function Truth

4. **Does the form suggest false capabilities?**
   - Aerodynamic shape on static object → False suggestion
   - Grip texture on handle → True functional form

5. **Would a user feel deceived upon closer inspection?**
   - Touch reveals truth → Honest
   - Touch reveals deception → Dishonest

### Construction Truth

6. **Are decorative elements pretending to be functional?**
   - Fake air vents → Dishonest
   - Real vents, styled well → Honest

7. **Are we using "honest" materials honestly?**
   - Aluminum where strength needed → Honest
   - Aluminum where plastic works, for appearance → Questionable

---

## Common Dishonesty Patterns

| Pattern | Why It's Dishonest | Honest Alternative |
|---------|-------------------|-------------------|
| **Chrome plastic** | Pretends to be metal | Use actual metal or honest plastic |
| **Fake screws** | Suggests disassembly that's impossible | Show real fasteners or none |
| **Woodgrain laminate** | Mimics expensive material | Use solid color or real wood |
| **Decorative vents** | Suggests cooling that doesn't exist | Remove or make functional |
| **False leather** | Texture without material quality | Use fabric or real leather |
| **Faux patina** | Artificial aging | Let it age naturally or stay new |

---

## Output Format

```markdown
# Design Honesty Evaluation: [Product Name]

## Overall Assessment
**Honesty Score:** [High / Medium / Low]

## Material Honesty

### Honest Materials
| Material | Appearance | Reality | Why Honest |
|----------|------------|---------|------------|
| Aluminum body | Metal | Aluminum 6061 | What you see is what it is |

### Questionable Materials
| Material | Issue | Recommendation |
|----------|-------|----------------|
| Chrome plastic | Appears metal, is plastic | Use brushed plastic or real metal |

## Construction Honesty

### Honest Construction
- Visible welds show assembly method
- Exposed screws allow serviceability

### Dishonest Elements
- Fake screw caps (not removable)
- Molded-in panel lines (suggest disassembly that's impossible)

## Form Honesty

### Honest Form
- Grip texture matches actual hand position
- Size suggests weight accurately

### Misleading Form
- Cooling vents (no heat generated)
- Racing aesthetic (no performance benefit)

## Recommendations

### Make Honest Immediately
1. [Element] - [Specific change to create honesty]

### Reconsider Approach
1. [Element] - [Why current approach is dishonest + honest alternative]

## Deception Risk Areas
1. [Area where user might feel deceived]
2. [What they'll discover vs what they expected]
```

---

## Calibration Examples

### Dishonest Design
```
❌ Plastic watch case with chrome plating
   → Appears metal, isn't
   → Wears away revealing truth
   → User feels deceived

❌ Decorative screws that can't be removed
   → Suggests serviceability
   → Actually creates false affordance
   → Dishonest construction

❌ "Leather-like" vinyl
   → Mimics expensive material
   → Degrades differently
   → Sets false expectations
```

### Honest Design
```
✅ Unfinished aluminum with natural patina
   → Shows true material
   → Ages authentically
   → Sets accurate expectations

✅ Visible assembly clips
   → Shows how it's made
   → Enables disassembly
   → Celebrates construction

✅ Matte plastic with texture
   → Doesn't pretend to be other material
   → Wears honestly
   → True to itself
```

---

## The Rams Test

**Dieter Rams' honesty principle:**

> "It does not make a product more innovative, powerful or valuable than it really is. It does not attempt to manipulate the consumer with promises that cannot be kept."

**Apply to each element:**
- Does this make the product appear more innovative than it is?
- Does this suggest capabilities it doesn't have?
- Does this pretend to be something it's not?

If any answer is "yes" → Dishonest design

---

## Common Pitfalls

| Pitfall | Why It Happens | Fix |
|---------|----------------|-----|
| **Cost-cutting disguise** | "Can't afford real material" | Use honest alternative, not fake version |
| **Luxury mimicry** | "Want premium appearance" | Create quality through design, not deception |
| **Trend following** | "Everyone uses chrome plastic" | Be honest even if others aren't |
| **Marketing pressure** | "Needs to look more expensive" | Educate stakeholders on honesty value |

---

## Summary

**Design honesty = Materials, construction, and form that truthfully represent the product**

1. Check every material for authenticity
2. Evaluate construction representation
3. Assess form-function alignment
4. Remove deceptive elements
5. Celebrate honest construction
6. Use materials as they truly are

*"Good design is honest. It does not make a product appear more innovative, powerful, or valuable than it really is." — Dieter Rams, Principle #6*


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

