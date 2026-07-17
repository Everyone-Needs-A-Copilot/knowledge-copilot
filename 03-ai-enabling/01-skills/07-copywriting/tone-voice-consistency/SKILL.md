---
last_updated: 2026-02-25
status: active
name: tone-voice-consistency
description: Maintain consistent brand voice and tone across all content. Use for establishing voice guidelines, auditing copy consistency, and adapting tone for different contexts while preserving brand identity.
triggers:
  files: ["**/content/**", "**/copy/**", "**/brand/**", "**/style-guide/**", "**/*.md"]
  keywords: ["brand voice", "tone", "voice consistency", "style guide", "brand personality", "content standards", "writing guidelines", "voice audit"]
allowed-tools: Read, Write, Edit
---

# Tone and Voice Consistency Skill

Maintain a consistent brand voice while adapting tone for different contexts. Voice is who you are; tone is how you express it based on situation. This skill helps create and enforce voice standards across all touchpoints.

---

## Voice vs Tone

### Understanding the Difference

| Aspect | Voice | Tone |
|--------|-------|------|
| Definition | Brand personality | Emotional inflection |
| Consistency | Always the same | Adapts to context |
| Analogy | Your personality | Your mood |
| Example | "We're direct and helpful" | "Celebratory" vs "Apologetic" |

### Voice Stays Constant

```
Our voice is always: Direct, helpful, knowledgeable, human
```

### Tone Adapts

| Context | Tone Adjustment |
|---------|-----------------|
| Success message | Celebratory, encouraging |
| Error message | Supportive, solution-focused |
| Warning | Serious, clear |
| Marketing | Energetic, benefit-focused |
| Support | Patient, thorough |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Building a Voice Framework

### Voice Attribute Matrix

Define voice through attributes with spectrums:

| Attribute | We Are | We're Not | Example |
|-----------|--------|-----------|---------|
| Confidence | Assured, not arrogant | Timid, uncertain | "Here's how" not "Maybe try" |
| Warmth | Friendly, not casual | Cold, robotic | "Great choice" not "Selection confirmed" |
| Clarity | Direct, not blunt | Verbose, vague | "3 steps left" not "A few more items" |
| Knowledge | Helpful, not condescending | Jargon-heavy | Explain terms when needed |

### Voice Principles

Structure voice around 3-5 core principles:

```
1. Be direct: Get to the point. Respect users' time.
2. Be helpful: Anticipate needs. Provide solutions.
3. Be human: Sound like a person. Avoid corporate speak.
4. Be confident: State things clearly. Avoid hedging.
```

### Voice Don'ts

| Avoid | Because | Instead |
|-------|---------|---------|
| "Please be advised" | Corporate jargon | Just state the information |
| "We regret to inform" | Overly formal | Direct statement |
| "At this time" | Filler phrase | "Now" or "Currently" |
| "Per your request" | Bureaucratic | "As you asked" |
| Multiple exclamation marks | Unprofessional | Single or none |

---

## Tone Calibration

### Tone by Emotion

| User Feeling | Tone Response | Example |
|--------------|---------------|---------|
| Frustrated | Patient, solution-focused | "Let's fix this. Here's what to do." |
| Confused | Clear, guiding | "Here's what's happening and what to do next." |
| Excited | Match energy | "Great choice! Here's what comes next." |
| Uncertain | Reassuring | "You're in the right place. Let's get started." |
| Accomplished | Celebratory | "Done! Your changes are live." |

### Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| Homepage | Confident, welcoming | "The better way to manage [X]" |
| Error state | Empathetic, helpful | "That didn't work. Let's try this instead." |
| Pricing page | Clear, transparent | "Simple pricing. No surprises." |
| Legal/Terms | Professional, plain | Clear language, not legalese |
| Email marketing | Engaging, personal | "Hi [Name], we thought you'd like this" |

### Tone Spectrum

Create a spectrum for common tone shifts:

```
Formal ←————————————→ Casual
Professional homepage    Support chat

Serious ←————————————→ Playful
Security warning         Achievement badge

Reserved ←————————————→ Enthusiastic
Account settings         Product launch
```

---

## Consistency Patterns

### Terminology Consistency

Create a terminology table:

| Concept | Always Use | Never Use |
|---------|------------|-----------|
| Account | Account | Profile (when meaning account) |
| Delete | Delete | Remove, Destroy, Erase |
| Error | Couldn't | Failed to, Unable to |
| User | You | User, Customer (in UI) |
| Company | We | [Company name] (in UI) |

### Capitalization Rules

| Element | Style | Example |
|---------|-------|---------|
| Headlines | Sentence case | "How to get started" |
| Buttons | Sentence case | "Create project" |
| Feature names | Title case when proper noun | "Dashboard" |
| Product names | As branded | "Slack", "GitHub" |

### Punctuation Standards

| Element | Rule | Example |
|---------|------|---------|
| Headlines | No period | "Welcome to your dashboard" |
| Button text | No period | "Save changes" |
| Tooltips | Period if sentence | "Click to copy link." |
| Error messages | Period | "Email is required." |
| Lists | Consistent ending | All periods or none |

---

## Voice Audit Checklist

### Content Review Questions

| Check | Question |
|-------|----------|
| On-voice | Does this sound like us? |
| Consistent | Does terminology match our standards? |
| Appropriate tone | Does tone fit the context? |
| Clear | Would a new user understand? |
| Helpful | Does it guide the user forward? |
| Human | Would you say this in conversation? |

### Common Inconsistencies to Catch

| Type | Example Problem | Fix |
|------|-----------------|-----|
| Terminology drift | "Users" vs "Members" vs "People" | Pick one, document it |
| Tone mismatch | Playful error messages | Match tone to seriousness |
| Formality shifts | "Click here" vs "Tap to continue" | Align across surfaces |
| Capitalization | "sign up" vs "Sign Up" vs "Sign up" | Establish standard |

---

## Voice in Different Channels

### Channel Adaptation

| Channel | Voice Adjustments |
|---------|-------------------|
| Marketing site | More energetic, benefit-focused |
| Product UI | More concise, action-focused |
| Email | More personal, conversational |
| Help docs | More thorough, instructional |
| Social media | More casual, timely |
| Legal/Privacy | More formal, clear |

### Channel Examples

Same message, adapted by channel:

| Channel | Copy |
|---------|------|
| Marketing | "Collaborate with your team in real-time" |
| Product UI | "Invite team members" |
| Email | "Ready to bring your team aboard?" |
| Help doc | "To invite team members, click Settings > Team > Invite" |

---

## Voice Documentation

### Voice Guide Structure

```
1. Voice Overview
   - Who we are
   - Who we're not

2. Voice Principles (3-5)
   - Principle + explanation + examples

3. Tone Guidance
   - When to shift tone
   - Tone by context matrix

4. Word List
   - Preferred terminology
   - Words to avoid

5. Examples
   - Before/after rewrites
   - Channel-specific examples
```

### Example Voice Principle Format

```
## Be Direct

Get to the point. Respect users' time.

| Instead of | Write |
|------------|-------|
| "In order to save your changes, you'll need to click the button below" | "Click Save to keep your changes" |
| "It seems like there might be a problem with your connection" | "Connection problem. Check your network." |

What this sounds like:
- Confident, not aggressive
- Clear, not curt
- Helpful, not bossy
```

---

## Handling Exceptions

### When to Break Rules

| Situation | Adjustment |
|-----------|------------|
| Legal requirements | Priority: compliance over voice |
| Emergency communications | Priority: clarity and urgency |
| Cultural adaptation | Adjust while preserving core identity |
| User testing feedback | Data beats guidelines |

### Escalation Path

When unsure about voice decisions:

1. Check voice documentation
2. Look at similar existing examples
3. Test with users if possible
4. Document decision for future reference

---

## Common Voice Problems

### Problem: Robotic Copy

| Robotic | Human |
|---------|-------|
| "Your request has been submitted" | "Got it! We'll be in touch soon." |
| "The operation completed successfully" | "Done!" |
| "An error has occurred" | "Something went wrong. Here's what to do." |

### Problem: Inconsistent Formality

| Inconsistent | Consistent |
|--------------|------------|
| "Hey! Click here to continue" → "Please proceed to the next step" | Match formality across the flow |

### Problem: Jargon Creep

| Jargon | Plain Language |
|--------|----------------|
| "Leverage your synergies" | "Work together more effectively" |
| "Optimize your workflow" | "Work faster" |
| "Seamless integration" | "Works with [X]" |

---

## Measuring Voice Consistency

### Quantitative Metrics

| Metric | What It Measures |
|--------|------------------|
| Terminology variance | How many terms used for same concept |
| Reading level | Consistency of complexity |
| Sentence length | Consistency of rhythm |
| Voice audit score | Pass rate on voice checklist |

### Qualitative Assessment

| Method | Application |
|--------|-------------|
| User interviews | "How would you describe our brand?" |
| Blind comparison | Can users identify which copy is yours? |
| Team review | Regular copy review sessions |

---

## Templates

### Voice Principle Template

```
## [Principle Name]

[One sentence explanation]

We are: [positive attributes]
We're not: [negative attributes to avoid]

| Instead of | Write |
|------------|-------|
| [Weak example] | [Strong example] |
| [Weak example] | [Strong example] |
```

### Terminology Entry Template

```
**[Term]**
- Use: [preferred usage]
- Don't use: [alternatives to avoid]
- Context: [when this applies]
- Example: "[sample sentence]"
```

### Tone Guidance Template

```
**[Context/Situation]**

Tone: [tone description]
User feeling: [what user is experiencing]
Our response: [how we sound]

Example:
- Before: [off-tone example]
- After: [on-tone example]
```

---

This skill enables you to maintain a consistent, recognizable voice while adapting tone appropriately across all content.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

