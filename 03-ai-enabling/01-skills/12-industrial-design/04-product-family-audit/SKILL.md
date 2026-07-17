---
last_updated: 2026-02-25
status: active
name: product-family-audit
description: Design language consistency check across product families. Use when evaluating whether products share coherent visual and interaction DNA.
triggers:
  files: ["**/industrial-design/**", "**/product-family/**", "**/design-system/**"]
  keywords: ["product family", "design language", "consistency", "system", "Jony Ive", "Apple", "coherence"]
allowed-tools: Read, Write, Edit
---

# Product Family Audit

**Core Principle:** Products should be obviously related — shared DNA, not matching uniforms.

---

## Framework: Family Coherence Matrix

| DNA Element | Question | Strong Family | Weak Family |
|-------------|----------|---------------|-------------|
| **Visual Language** | Would a user recognize these as related? | Obvious kinship | No visible relationship |
| **Material Palette** | Do materials speak same language? | Consistent choices | Random selection |
| **Interaction Patterns** | Do interactions feel familiar? | Predictable across products | Relearn each time |
| **Proportion System** | Do sizes relate mathematically? | Harmonious scaling | Arbitrary sizing |

---


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Process

### 1. Visual DNA Extraction

**Identify the family's genetic markers:**

```markdown
## Visual DNA Elements

### Form Language
- [ ] Primary shapes (round, rectangular, organic)
- [ ] Edge treatment (sharp, chamfered, rounded)
- [ ] Surface language (flat, curved, faceted)
- [ ] Transition style (abrupt, gradual, blended)

### Detail Language
- [ ] Button style
- [ ] Vent pattern
- [ ] Seam treatment
- [ ] Corner radius system
- [ ] Texture approach

### Proportion System
- [ ] Size relationships
- [ ] Golden ratio usage
- [ ] Aspect ratios
- [ ] Margin systems
```

### 2. Family Member Comparison

**For each product in family:**

| Product | Form Language | Material Palette | Interaction Pattern | Proportion | Family Fit |
|---------|---------------|------------------|-------------------|------------|------------|
| Product A | Soft rectangles | Aluminum + glass | Touch + gesture | 16:9 | Strong |
| Product B | Sharp angles | Plastic + metal | Buttons only | Random | Weak |
| Product C | Soft rectangles | Aluminum + glass | Touch + gesture | 16:10 | Strong |

### 3. Coherence Evaluation

**Score each consistency area:**

```markdown
## Consistency Scores (1-5)

| Area | Score | Evidence |
|------|-------|----------|
| Visual recognition | [1-5] | Can you tell they're related at a glance? |
| Material consistency | [1-5] | Same material vocabulary? |
| Interaction patterns | [1-5] | Transfer learning between products? |
| Proportion harmony | [1-5] | Sizes feel related? |
| Detail language | [1-5] | Same design voice in details? |

**Overall Family Coherence:** [Average score]
```

---

## Evaluation Questions

### Visual Recognition

1. **Would a user recognize this as part of the family?**
   - 3-second glance test
   - Visual DNA obvious → Strong family
   - Could be any brand → Weak family

2. **Does this share visual DNA with its siblings?**
   - Form language consistent → Yes
   - Random aesthetic → No

3. **Line them up — do they look related?**
   - Obvious kinship → Strong family
   - Random collection → Weak family

### Material Consistency

4. **Does the material palette align?**
   - Same materials across family → Consistent
   - Different materials each product → Inconsistent

5. **Are material finishes speaking the same language?**
   - Brushed metal everywhere → Consistent
   - Mix of chrome, brushed, painted → Inconsistent

6. **Do material transitions happen the same way?**
   - Consistent joinery style → Good
   - Each product different → Poor

### Interaction Consistency

7. **Are interaction patterns consistent across the family?**
   - Learn once, apply everywhere → Good
   - Relearn each product → Poor

8. **Do controls work the same way?**
   - Predictable behavior → Consistent
   - Different per product → Inconsistent

9. **Can a user transfer knowledge between products?**
   - Yes, immediately → Strong family
   - No, must relearn → Weak family

### Proportion Harmony

10. **Would a user recognize this as part of the system?**
    - Sizes feel related → Good
    - Arbitrary sizing → Poor

11. **Do the proportions relate mathematically?**
    - Clear ratio system → Harmonious
    - Random proportions → Disconnected

---

## Output Format

```markdown
# Product Family Audit: [Family Name]

## Family Overview
**Products evaluated:** [List]
**Family established:** [Date]
**Design language version:** [If versioned]

## DNA Analysis

### Core Family DNA
| Element | Definition | Consistency Score (1-5) |
|---------|------------|-------------------------|
| Form language | [Description] | [Score] |
| Material palette | [Materials] | [Score] |
| Interaction pattern | [Patterns] | [Score] |
| Proportion system | [Ratios] | [Score] |
| Detail language | [Style] | [Score] |

**Overall Family Coherence:** [Average] / 5

## Individual Product Assessment

### [Product 1]
**Family Fit:** Strong / Moderate / Weak

| DNA Element | Family Standard | This Product | Aligned? |
|-------------|----------------|--------------|----------|
| Form language | Soft rectangles | Soft rectangles | ✅ |
| Materials | Al + glass | Al + glass | ✅ |
| Corners | 4mm radius | 4mm radius | ✅ |
| Buttons | Flush, tactile | Flush, tactile | ✅ |

### [Product 2]
**Family Fit:** Strong / Moderate / Weak

| DNA Element | Family Standard | This Product | Aligned? |
|-------------|----------------|--------------|----------|
| Form language | Soft rectangles | Sharp angles | ❌ |
| Materials | Al + glass | Plastic + metal | ❌ |
| Corners | 4mm radius | Sharp corners | ❌ |
| Buttons | Flush, tactile | Raised, clicky | ❌ |

## Consistency Analysis

### Strong Consistency
- [Element] across [Products]: [Description]

### Weak Consistency
- [Element] varies between [Products]: [Description]

### Missing Elements
- [Element] not present in [Products]: [Impact]

## User Recognition Test

**Can users identify family membership?**
- At 10 feet: [Yes/No/Sometimes]
- At 3 feet: [Yes/No/Sometimes]
- When handling: [Yes/No/Sometimes]

## Recommendations

### Strengthen Family Coherence
1. [Product] - [Change to align with family DNA]
2. [Element] - [Make consistent across family]

### Evolve Family DNA
1. [New element] - [Add to all family members]

### Document Standards
1. [Create/update] design language specification
2. [Element] needs clear definition

## Family DNA Specification

### Required Elements (must be present)
1. [Element]: [Specification]
2. [Element]: [Specification]

### Optional Elements (may vary)
1. [Element]: [Acceptable range]

### Forbidden Elements (breaks family)
1. [Element]: [Why incompatible]
```

---

## Coherence Levels

### Strong Family (Score 4-5)
```
✅ Apple (iPhone, iPad, Mac, Watch)
   - Shared aluminum + glass
   - Consistent chamfered edges
   - Same button style
   - Related proportions
   - Instantly recognizable

✅ Braun (1960s product line)
   - Consistent grid system
   - Same material palette
   - Unified button language
   - Obvious kinship
```

### Weak Family (Score 1-2)
```
❌ Random materials per product
❌ Different form languages
❌ Inconsistent interaction patterns
❌ No visual relationship
❌ Each product could be different brand
```

---

## The Apple Test

**Jony Ive's approach to product families:**

1. **Shared Material Vocabulary**
   - Aluminum used consistently
   - Glass treatment same across products
   - Finish language unified

2. **Consistent Detail Language**
   - Chamfered edges everywhere
   - Button style predictable
   - Port treatment unified

3. **Proportional Relationships**
   - Sizes feel related
   - Aspect ratios harmonize
   - Scaling feels intentional

4. **Interaction Coherence**
   - Gestures transfer between devices
   - Button behavior predictable
   - Learning is cumulative

**Test your family:**
- Remove logos — can you still tell they're related? → Strong family
- User learns one, can use others? → Good consistency
- Products look like they were designed together? → Coherent language

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Forced matching** | Products look identical, not related | Shared DNA, not uniforms |
| **Cost variation** | Cheap products use different materials | Scale quality, keep language |
| **Designer rotation** | Each product different style | Document family DNA |
| **Timeline spread** | Later products drift from family | Maintain or evolve consciously |
| **Category bias** | "This category needs different approach" | Find DNA that works across all |

---

## Family DNA Documentation Template

**Create clear specification:**

```markdown
# [Family Name] Design Language

## Visual DNA

### Form Language
- Primary shapes: [Specification]
- Edge treatment: [Radius, chamfer, sharp]
- Surface character: [Flat, curved, faceted]
- Transition style: [How surfaces meet]

### Material Palette
**Primary materials:**
1. [Material] - [Finish] - [Usage]
2. [Material] - [Finish] - [Usage]

**Secondary materials:**
1. [Material] - [Finish] - [Usage]

**Forbidden:**
- [Material/finish that breaks family]

### Proportion System
- Base unit: [Size]
- Size progression: [Ratio]
- Aspect ratios: [Standards]
- Margin system: [Rules]

### Detail Language
- Corner radius: [Specification]
- Button style: [Description]
- Vent pattern: [If applicable]
- Seam treatment: [How parts join]
- Texture: [Surface treatment]

## Interaction DNA

### Control Language
- Button behavior: [Specification]
- Touch response: [If applicable]
- Gesture set: [Standards]
- Feedback: [Audio/haptic/visual]

### Transfer Learning
What users learn from Product A applies to Product B:
- [Interaction 1]
- [Interaction 2]

## Recognition Checklist

At 10 feet:
- [ ] Recognizable as [brand]
- [ ] Recognizable as family member

At 3 feet:
- [ ] Material language obvious
- [ ] Detail language visible

When handling:
- [ ] Interaction pattern familiar
- [ ] Build quality consistent
```

---

## Summary

**Product family audit = Ensuring coherent visual and interaction DNA across products**

1. Extract family's visual DNA
2. Compare each product against DNA
3. Score consistency across elements
4. Identify weak coherence areas
5. Strengthen family language
6. Document standards clearly

*"We believe that there is a profound and enduring beauty in simplicity, in clarity, in efficiency. True simplicity is derived from so much more than just the absence of clutter and ornamentation — it's about bringing order to complexity." — Jony Ive*


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

