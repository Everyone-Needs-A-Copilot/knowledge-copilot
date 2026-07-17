---
last_updated: 2026-02-25
status: active
name: material-intention
description: Intentional material selection methodology that treats material choice as communication. Use when selecting materials for products, evaluating material decisions, or ensuring material honesty in industrial design.
triggers:
  files: ["**/materials/**", "**/specifications/**", "**/product-design/**", "**/cad/**"]
  keywords: ["material selection", "material choice", "finish", "texture", "tactile", "sustainability", "manufacturing", "CMF", "patina", "honesty"]
allowed-tools: Read, Write, Edit
---

# Material Intention

Material selection is communication. Every material choice tells the user something about the product's purpose, quality, and values.

## Core Principle

**Materials should be honest.** They should look like what they are, feel appropriate for their function, and age in ways that enhance rather than diminish the product.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Material Selection Framework

| Criterion | Question | Red Flags |
|-----------|----------|-----------|
| **Function** | Does the material serve the use case? | Material can't withstand expected use, requires protective coatings to function |
| **Honesty** | Does it look like what it is? | Plastic made to look like wood, faux finishes, deceptive treatments |
| **Tactile** | What does it feel like in use? | High-touch surfaces feel unpleasant, temperature extremes, slippery when wet |
| **Aging** | How does it degrade over time? | Shows wear in ugly ways, scratches easily, discolors unevenly |
| **Sustainability** | What's the environmental cost? | Non-recyclable, high embodied energy, toxic production, short lifespan |
| **Manufacturing** | Can it be made at scale with quality? | Requires extreme tolerances, inconsistent results, high reject rate |

## Process

### 1. Define Functional Requirements

```
Questions to answer:
- What forces will this material experience? (stress, impact, temperature)
- What environmental conditions? (UV, moisture, chemicals)
- What are the dimensional stability requirements?
- What safety certifications are needed?
```

**Output:** Functional material constraints

### 2. Identify Tactile Experience Goals

```
Map high-touch surfaces:
- Where does the user grip it?
- Where does skin contact occur?
- What temperature should it feel? (warm, cool, neutral)
- What texture communicates the right message? (soft, grippy, smooth)
```

**Output:** Tactile material targets for each surface zone

### 3. Evaluate Honesty of Appearance

```
Test for deception:
- Does the material pretend to be something it's not?
- Are surface treatments obscuring the base material?
- Would the user be surprised to learn what it's made of?
- Does it pass the "knock test"? (sounds like what it looks like)
```

**Dieter Rams principle:** "Good design is honest. It does not make a product more innovative, powerful or valuable than it really is."

**Output:** Material authenticity assessment

### 4. Assess Aging Characteristics

```
Evaluate how the material changes:
- Does it develop patina or just look worn?
- Are scratches/marks visible? Do they enhance or detract?
- Does color shift gracefully or fade badly?
- How does it look after 1 year? 5 years? 10 years?
```

**Output:** Aging behavior prediction (see `graceful-aging-design` skill)

### 5. Consider Environmental Impact

```
Lifecycle assessment:
- Embodied energy (extraction, processing, transport)
- Manufacturing waste and emissions
- Product lifespan and durability
- End-of-life: recyclable? biodegradable? reusable?
- Repairability and part replacement
```

**Output:** Environmental impact summary

### 6. Validate Manufacturing Feasibility

```
Production readiness:
- Can suppliers hit quality targets consistently?
- What are the tooling costs and lead times?
- What's the reject rate at scale?
- Are there secondary operations needed? (finishing, coating)
- What quality control is required?
```

**Output:** Manufacturing viability assessment

## Material Families

### Metals

| Material | Character | Best For | Watch For |
|----------|-----------|----------|-----------|
| Aluminum | Light, modern, cool-touch | Structural, heat dissipation | Scratches show, anodizing can wear |
| Steel | Strong, substantial, honest | Durability, mechanisms | Corrosion, weight, cold-touch |
| Brass | Warm, ages beautifully | Accents, connectors | Tarnish (can be feature or bug) |
| Copper | Distinctive patina, antimicrobial | Touch surfaces, accents | Color shift dramatic |

### Polymers

| Material | Character | Best For | Watch For |
|----------|-----------|----------|-----------|
| ABS | Durable, matte, inexpensive | Enclosures, structural | Can feel cheap, scratches visible |
| PC | Clear, impact-resistant | Lenses, guards | Yellows with UV exposure |
| PETG | Recyclable, clear, tough | Sustainable enclosures | Lower heat resistance |
| Liquid silicone | Soft-touch, hygienic | Grips, seals, wearables | Attracts dust, can tear |

### Natural Materials

| Material | Character | Best For | Watch For |
|----------|-----------|----------|-----------|
| Wood | Warm, living, unique grain | Handles, enclosures, accents | Moisture sensitivity, consistency |
| Leather | Ages beautifully, tactile | Grips, covers, straps | Requires maintenance, cost |
| Cork | Renewable, soft-touch, light | Grips, gaskets, sustainable choice | Limited structural strength |
| Bamboo | Fast-growing, distinctive | Sustainable enclosures | Quality varies widely |

## CMF (Color, Material, Finish) Strategy

```
Develop coherent CMF story:

1. Hero material: What's the primary material expression?
2. Accent materials: What contrasts or complements?
3. Finish strategy: Matte, gloss, textured? Where and why?
4. Color palette: How do materials constrain or enable color?
5. Visual hierarchy: Do materials support functional zoning?
```

## Common Material Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| Chrome plastic | Looks cheap, ages poorly | Use real metal or honest plastic with matte finish |
| Wood-grain plastic | Deceptive, tacky | Use real wood or honest material appropriate to context |
| Glossy black everything | Shows fingerprints, scratches | Matte or textured finishes for high-touch surfaces |
| Single material | Monotonous, no hierarchy | Strategic material contrast for visual/tactile interest |
| Fashion over function | Trends date quickly | Timeless materials chosen for use, not trend |

## Material Honesty Test

```
Ask these questions:
1. Would I be embarrassed to tell the user what this is made of?
2. Does the material choice respect the user's intelligence?
3. If this were twice the price, would I choose the same material?
4. Does the material support the product's intended lifespan?
5. Will this material choice matter in 10 years?
```

If any answer is "no," reconsider the material choice.

## Documentation

### Material Specification Template

```
Material: [Name]
Supplier: [Source]
Grade/Spec: [Technical spec]
Finish: [Surface treatment]

Why This Material:
- Function: [How it serves the use case]
- Honesty: [Why it's the right expression]
- Experience: [Tactile/visual qualities]
- Aging: [How it degrades]
- Sustainability: [Environmental rationale]
- Manufacturing: [Production feasibility]

Alternatives Considered:
- [Material A]: Rejected because [reason]
- [Material B]: Rejected because [reason]
```

## Integration

- Pair with `graceful-aging-design` for lifecycle thinking
- Inform `form-follows-function` with material constraints
- Support `manufacturing-for-quality` with production specs
- Connect to sustainability goals in product strategy

## Output

Deliver material specifications that are:
- Functionally appropriate
- Honest in expression
- Pleasant to touch and use
- Graceful in aging
- Environmentally responsible
- Manufacturable at quality and scale

**Material choice is a promise to the user. Make it a promise you can keep.**


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

