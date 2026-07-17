---
last_updated: 2026-02-25
status: active
name: usability-test-facilitation
description: Facilitate usability tests with think-aloud protocol - moderating sessions, probing without leading, capturing insights. Use for running user tests.
triggers:
  files: ["**/research/**", "**/usability/**", "**/user-testing/**"]
  keywords: ["moderate", "facilitation", "think aloud", "user test", "session", "observe", "probe", "usability testing"]
allowed-tools: Read, Write, Edit
---

# Usability Test Facilitation Skill

Master guide for facilitating usability testing sessions - running tests, using think-aloud protocol, probing without leading, and capturing actionable insights.

## Philosophy

**Be a fly on the wall.** Your job is to observe, not influence. Every intervention changes the data.

**Silence is golden.** Users thinking through problems reveal more than users being helped.

**Curiosity, not judgment.** There are no wrong answers - only insights into how users think.

---


## Define Done

- [ ] Design decisions based on user needs and behavior patterns
- [ ] Interaction flows tested against common user tasks
- [ ] Accessibility requirements met (WCAG AA)
- [ ] Edge cases and error states designed, not just happy path

## Think-Aloud Protocol

### What is Think-Aloud?

Users verbalize their thoughts while performing tasks:
- What they're looking at
- What they're thinking
- What they expect
- Why they're taking actions
- When they're confused

### Teaching Think-Aloud

**Introduction script**:
```
"As you work through these tasks, please think aloud.
Tell me what you're looking at, what you're thinking,
and what you're trying to do. Pretend you're alone
and talking to yourself.

For example, if I was looking for a book online, I
might say: 'Okay, I want to find books about cooking.
I see a search box at the top - I'll try typing
'cooking' there. Now I see results... these look like
cookbooks. I'll click on this one to learn more...'

Let's do a quick practice. [Demo website/simple task]"
```

### Maintaining Think-Aloud

When users go quiet:

**Neutral prompts** (use these):
- "What are you thinking?"
- "What are you looking at?"
- "Tell me more about that."
- "What happened there?"
- "Keep talking."

**Leading prompts** (avoid these):
- "Did you see the button over there?"
- "Why don't you try the menu?"
- "Most people click here."
- "That's not right."

---

## Session Facilitation

### Session Flow

```
1. WELCOME (2-3 min)
   └─ Greeting, rapport building

2. SETUP (3-5 min)
   ├─ Explain session
   ├─ Consent/recording
   └─ Teach think-aloud

3. BACKGROUND (3-5 min)
   └─ Relevant context questions

4. TASKS (30-45 min)
   ├─ Present scenario
   ├─ Observe & prompt
   └─ Post-task questions
   [Repeat for each task]

5. DEBRIEF (5-10 min)
   ├─ Overall impressions
   ├─ Follow-up questions
   └─ Thank you
```

### Welcome & Rapport

**Goals**:
- Put participant at ease
- Establish trust
- Set expectations

```
"Hi [Name], thank you so much for coming in today.
I'm [Your name]. Before we start, I want to emphasize
that we're testing the [product], not you. There are
no wrong answers or mistakes - you're helping us
understand how people actually use this.

Your honest feedback, even if negative, is incredibly
valuable. Does that make sense?"
```

### Explaining Recording

```
"With your permission, I'd like to record this session.
The recording will only be used by our team to review
the session and will not be shared publicly. You can
ask me to stop recording at any time. Is that okay?"
```

---

## During Tasks

### Presenting Scenarios

**Do**:
- Hand written scenario to user (they can reference it)
- Read aloud once
- Ask if they have questions about the scenario
- Indicate starting point

**Don't**:
- Give step-by-step instructions
- Hint at where to go
- Use product terminology

```
"Here's your first task. Take a moment to read it,
then let me know when you're ready to begin. You can
refer back to this at any time.

[Hand scenario]

I'll start you on this page. Begin whenever you're ready."
```

### Observing

**Watch for**:
- Where eyes/cursor go
- Hesitation before clicking
- Backtracking
- Expressions of confusion
- Unexpected paths
- Comments ("hmm", "oh", "what?")

**Note**:
- Timestamps of issues
- Exact quotes
- Path taken vs expected path
- Non-verbal cues

### Probing Techniques

**Echoing** (repeat their words):
```
User: "This is kind of confusing"
You: "Confusing?"
User: [Explains what's confusing]
```

**Clarifying** (understand what they mean):
```
User: "I thought this would be over here"
You: "What were you expecting to find?"
```

**Reflecting** (acknowledge and continue):
```
User: "This is really frustrating"
You: "I can see that. What's frustrating about it?"
```

**Exploring** (dig deeper):
```
User: "I guess I'd click this"
You: "What makes you think that would work?"
```

### When Users Ask Questions

**Questions about the task**:
```
User: "Can I use the search?"
You: "You can use whatever you'd normally use."

User: "Am I supposed to sign in?"
You: "What would you do if you were at home?"
```

**Questions about the product**:
```
User: "What does this button do?"
You: "What do you think it does?"

User: "Is this right?"
You: "I'm curious what you think."
```

**When truly stuck**:
```
User: "I have no idea what to do"
You: "Where would you normally go for help in this
     situation?" [If still stuck after 2+ min]
     "Let's move on to the next task."
```

### Handling Struggle

**The 2-minute rule**:
- Let users struggle for ~2 minutes
- Struggling reveals issues
- After 2 minutes with no progress, offer to move on

**Script for moving on**:
```
"This is giving us great information about where the
product needs improvement. Let's move on to the next
task so we have time for everything."
```

---

## Post-Task Debrief

### Immediate Post-Task Questions

After each task:
```
"How easy or difficult was that? On a scale of 1-7,
where 1 is very difficult and 7 is very easy."

"What, if anything, was confusing?"

"Is that how you expected it to work?"
```

### Session Debrief

After all tasks:
```
"Now that you've seen the [product], what's your
overall impression?"

"What stood out to you as particularly good?"

"What would you change if you could?"

"Any questions for me about what we're building?"
```

### Capturing Feedback

- Write exact quotes (in quotation marks)
- Note severity of issues
- Capture positive feedback too
- Ask clarifying questions
- Thank them for honesty

---

## Handling Difficult Situations

### Talkative Participants

```
Participant: [Long tangent unrelated to task]
You: "That's interesting. For the purpose of this test,
     let's focus on [task]. What would you do next?"
```

### Silent Participants

```
[Long pause with no verbalization]
You: "What are you thinking right now?"

[Still silent]
You: "Just talk me through what you see on this page."
```

### Frustrated Participants

```
Participant: "This is so annoying!"
You: "I hear you. What specifically is frustrating?"

Participant: "I hate this"
You: "That's exactly the kind of feedback we need.
     Can you tell me more about what's not working?"
```

### Emotional Participants

```
[Participant seems upset]
You: "Would you like to take a short break?"

[If they apologize for struggling]
You: "Please don't apologize. The product should work
     for you, not the other way around. This is helping
     us find where we need to improve."
```

### Technical Issues

```
[Prototype breaks]
You: "Sorry about that technical glitch. Let me get
     us back on track."
     [Fix issue quickly]
     "Okay, we're back. You were just about to..."

[If unfixable]
You: "Unfortunately we have a technical issue. Let's
     skip to the next task."
```

---

## Note-Taking

### What to Capture

| Category | Examples |
|----------|----------|
| Behaviors | Clicked wrong button, scrolled past CTA |
| Quotes | "I thought this would be..." |
| Non-verbals | Sighed, laughed, grimaced |
| Timestamps | 4:32 - confusion at checkout |
| Paths | Home → Products → ❌ → Search → ✓ |
| Severity | Critical / Major / Minor |

### Note-Taking Format

```markdown
## Task 2: Add item to cart

**Time:** 3:45
**Result:** Partial success (needed help)

**Path taken:**
Home → Category → Filter (unexpected) → Product →
Size (confused) → Add to Cart ✓

**Observations:**
- 1:20 - Hesitated at category page
- 2:05 - Clicked filter expecting search
- 2:45 - "Which size should I pick?" (confusion)
- 3:30 - Finally found size selector

**Quotes:**
- "I'm not sure if this is the right size"
- "Oh, there it is" (finding add to cart)

**Issues:**
1. Size selector not prominent - Major
2. Filter confused with search - Minor

**Positive:**
- "I like how the images change when I hover"
```

### Observer Notes

If you have observers:
- Brief before session
- Silent during session
- Questions only after debrief
- Separate note-taking from facilitator

---

## Remote Session Tips

### Setup

- Test technology beforehand
- Send joining instructions early
- Have backup plan (phone dial-in)
- Check participant's audio/video
- Ensure they can screen share

### Adaptation

**Building rapport**:
```
"Can you hear me okay? And I can see your screen clearly.
Before we start, where are you joining from today?"
[Brief small talk to establish comfort]
```

**Think-aloud remotely**:
```
"Since I can't see your face, it's especially important
to hear what you're thinking. If you go quiet, I might
check in with you."
```

**Managing technology**:
```
[If they struggle with share]
"Take your time. Let me know when you've found the
share screen button."

[If video freezes]
"Your screen froze for a moment - can you describe
what you're seeing?"
```

---

## Quick Reference

### Facilitation Dos and Don'ts

| Do | Don't |
|----|-------|
| Stay neutral | Show agreement/disagreement |
| Ask open questions | Ask leading questions |
| Echo user's words | Put words in their mouth |
| Let them struggle | Jump in to help |
| Capture quotes | Paraphrase |
| Note non-verbals | Focus only on words |
| Thank for honest feedback | Get defensive |

### Neutral Prompt Cheatsheet

| Situation | Prompt |
|-----------|--------|
| User goes quiet | "What are you thinking?" |
| User clicks something | "What made you click that?" |
| User hesitates | "What's going on?" |
| User expresses frustration | "Tell me more about that." |
| User asks for help | "What would you normally do?" |
| User gives vague feedback | "Can you give me an example?" |

### Red Flags to Note

- Long pauses before action
- "I guess I'll try..."
- Clicking back multiple times
- Scanning without clicking
- "Is this right?" questions
- Sighs, grimaces, confusion sounds
- Using search for basic features
- Missing obvious elements

---

## Summary

**Great facilitation = Authentic insights**

1. Establish rapport and comfort
2. Teach and maintain think-aloud
3. Observe without influencing
4. Probe with neutral questions
5. Let users struggle (within reason)
6. Capture behaviors, quotes, and issues
7. Stay curious, not judgmental

*Your silence creates space for truth.*


## Quality Tests

### Task Completion Test
- Users can complete primary tasks without confusion
- **PASS:** Task flow has 5 or fewer steps, with clear progress indication
- **FAIL:** Users get lost, need to backtrack, or can't find key features

### Error Recovery Test
- Users can recover from mistakes without losing progress
- **PASS:** Error messages explain what went wrong and how to fix it
- **FAIL:** Generic error messages or data loss on mistakes

