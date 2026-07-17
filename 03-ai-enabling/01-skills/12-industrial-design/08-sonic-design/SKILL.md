---
last_updated: 2026-02-25
status: active
name: sonic-design
description: Design acoustic signatures for product interactions using sound as a quality signal. Use when defining mechanical interactions, feedback mechanisms, or product operation characteristics.
triggers:
  files: ["**/industrial-design/**", "**/mechanical/**", "**/interaction/**", "**/prototype/**"]
  keywords: ["sound", "acoustic", "click", "feedback", "mechanical", "sonic", "audio", "interaction sound", "product sound"]
allowed-tools: Read, Write, Edit
---

# Sonic Design

**Principle:** Sound is the invisible signature of quality. Every mechanical interaction produces sound—intentional or accidental. Great products design for both.

## Framework

### Interaction Sound Map

| Interaction | Sound Consideration | Quality Signal |
|-------------|---------------------|----------------|
| **Activation** | Click, snap, engagement | Precision, responsiveness |
| **Movement** | Glide, resistance, travel | Smooth operation, control |
| **Feedback** | Confirmation, completion | Success, finality |
| **Ambient** | Operational hum, silence | Refinement, non-intrusion |
| **Error** | Warning without alarm | Clear but not aggressive |

### Sound Character Dimensions

| Dimension | Range | Design Intent |
|-----------|-------|---------------|
| **Volume** | Silent → Pronounced | Discretion vs. confirmation |
| **Pitch** | Low → High | Solidity vs. delicacy |
| **Duration** | Brief → Sustained | Instant vs. process |
| **Quality** | Damped → Resonant | Control vs. liveliness |
| **Consistency** | Variable → Uniform | Organic vs. manufactured |


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Design Criteria

### The Four Questions

**1. Does the sound match the action's weight?**

Light actions should sound light, heavy actions substantial:

```
Example: MacBook lid close
- Weight: Significant (1-2kg mass)
- Sound: Deep, damped thud
- Match: YES—substantial sound for substantial action

Counter-example: Cheap laptop lid
- Weight: Similar mass
- Sound: Hollow rattle
- Match: NO—sound undermines perceived quality
```

**2. Is it satisfying or merely informative?**

| Merely Informative | Satisfying |
|-------------------|------------|
| Beep confirms button press | Click provides tactile + sonic reward |
| Buzz signals completion | Gentle chime celebrates success |
| Generic tone for error | Distinctive sound aids diagnosis |

**3. Does it communicate quality?**

Quality sonic signatures:
- **Damped, controlled** (not rattly or hollow)
- **Consistent** (repeatable, predictable)
- **Intentional** (clearly designed, not accidental)
- **Appropriate volume** (neither apologetic nor intrusive)

**4. Is silence intentional or accidental?**

| Intentional Silence | Accidental Silence |
|---------------------|-------------------|
| Fan-less operation (iPad) | Motor that should give feedback doesn't |
| Damped mechanism (car door) | Loose tolerance creates intermittent noise |
| Silent mode switch | Mechanism too weak to produce sound |

## Design Process

### 1. Audit Existing Sounds

Map every sound the product makes:

```markdown
## Sound Audit: [Product Name]

| Interaction | Current Sound | Intentional? | Quality Level |
|-------------|---------------|--------------|---------------|
| Power on | Chime (250ms) | Yes | High |
| Button press | Click (50ms) | Yes | Medium |
| Fan spin-up | Whoosh (2s) | No | Low |
| Placement on desk | Thud | No | Medium |
```

### 2. Define Sonic Goals

For each interaction, specify intent:

| Interaction | Goal | Reference |
|------------|------|-----------|
| Lid close | Premium, controlled closure | MacBook magnetic snap |
| Button press | Confident engagement | iPhone power button |
| Mode switch | Tactile + sonic confirmation | iPhone silent switch |
| Error state | Clear but not alarming | iOS haptic + tone |

### 3. Design Mechanical Sound

Sound is a byproduct of mechanical design:

**Mechanisms for Quality Sound:**

| Desired Sound | Mechanical Approach |
|---------------|---------------------|
| Crisp click | Snap dome, positive detent |
| Damped close | Fluid damper, soft-close hinge |
| Satisfying snap | Magnetic catch with controlled engagement |
| Silent operation | Tight tolerances, vibration isolation |
| Resonant feedback | Tuned spring, acoustic chamber |

### 4. Prototype and Record

Capture and evaluate sound objectively:

**Testing Protocol:**
1. Record interaction (high-quality mic, controlled environment)
2. Analyze waveform (frequency, duration, consistency)
3. Compare to reference products
4. Blind A/B test with users
5. Iterate mechanism design

### 5. Tune Acoustic Properties

Adjust mechanical design to refine sound:

| Sound Issue | Mechanical Adjustment |
|-------------|----------------------|
| Too loud/harsh | Add damping material, increase surface contact |
| Too quiet/weak | Increase detent force, add acoustic reflector |
| Rattly/loose | Tighten tolerances, add interference fit |
| Inconsistent | Improve manufacturing precision, stabilize mechanism |

## Ive Reference

Jonathan Ive's sonic design philosophy:

> "We spent months tuning the sound of the MacBook lid closing. It had to sound deliberate, controlled, premium."

**Examples:**
- **MacBook lid:** Magnetic latch creates soft, controlled close (no slam)
- **iPhone silent switch:** Two-stage detent with distinct click (tactile + sonic)
- **AirPods case:** Magnetic snap closure—satisfying without being loud
- **Car door (Range Rover):** Deep, damped thud signals solidity and refinement

## Sound Design Patterns

### Pattern: Confirmation Click

**Use when:** User needs immediate feedback that action was registered

**Characteristics:**
- Duration: 30-80ms
- Pitch: Mid-range (500-2000Hz)
- Volume: Clear but not loud
- Mechanism: Snap dome, tactile switch

**Example:** Keyboard keys, trackpad click, button press

### Pattern: Premium Closure

**Use when:** Lid, door, or cover needs to communicate quality

**Characteristics:**
- Duration: 200-500ms
- Pitch: Low (80-300Hz)
- Volume: Moderate
- Mechanism: Damped hinge, magnetic catch

**Example:** MacBook lid, car door, premium luggage

### Pattern: Intentional Silence

**Use when:** Sound would detract from experience

**Characteristics:**
- Target: <30dB ambient noise
- Mechanism: Vibration isolation, tight tolerances
- Context: Focus-intensive use (writing, reading, recording)

**Example:** Fan-less iPad, silent keyboard switches

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|--------------|--------------|-----------------|
| Arbitrary beeps | Generic, unmemorable, annoying | Design mechanical feedback instead |
| Hollow sounds | Signals cheap construction | Add internal structure, damping |
| Inconsistent acoustics | Undermines quality perception | Tighten tolerances, improve repeatability |
| Ignoring ambient sound | Product intrudes on environment | Design for operational silence or pleasant hum |

## Testing Framework

### Comparative Listening Test

Present users with three variants (blind):

```
Variant A: Current/baseline mechanism
Variant B: Refined mechanism (iteration 1)
Variant C: Alternative approach

Questions:
1. Which sounds most premium?
2. Which gives clearest feedback?
3. Which would you want to use repeatedly?
4. Describe the sound in one word each.
```

### Acoustic Measurements

| Metric | Measurement | Target Range |
|--------|-------------|--------------|
| Peak volume | dB SPL @ 30cm | 40-65 dB (feedback), <35 dB (ambient) |
| Frequency | Hz (fundamental) | 200-1000 Hz (satisfying), avoid 2-4kHz (harsh) |
| Duration | Milliseconds | 30-100ms (instant), 200-500ms (closure) |
| Consistency | Variance across 100 cycles | <5% variation in peak dB |

## Output Format

When documenting sonic design decisions:

```markdown
## Sonic Design Specification

### Interaction: [Name]

**Sonic Goal:** [e.g., "Confident, tactile confirmation of engagement"]

**Mechanism:** [e.g., "Snap dome (50gf actuation force)"]

**Acoustic Properties:**
- Peak volume: 55 dB SPL @ 30cm
- Dominant frequency: 800 Hz
- Duration: 45ms
- Character: Crisp, damped click

**Reference Product:** [e.g., "Similar to iPhone power button"]

**User Testing:**
- Preference score: 8.5/10
- Quote: "Feels deliberate and premium"
```

---

**Remember:** Sound is not an afterthought. It's designed into the mechanism from the start. A product that sounds cheap will be perceived as cheap, regardless of materials.


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

