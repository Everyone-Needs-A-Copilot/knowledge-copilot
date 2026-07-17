---
last_updated: 2026-04-02
status: active
---

# Layer-to-Tool Mapping

Quick reference: each resistance layer, the TOC Thinking Process tool that addresses it, and why that tool works for that layer.

---

## At a Glance

| Layer | Name | TOC Tool | Core Move |
|-------|------|----------|-----------|
| 1 | Disagree on the Problem | Current Reality Tree (CRT) | Build shared diagnosis from shared undesirable effects |
| 2 | Disagree on Direction | Evaporating Cloud (EC) | Surface and challenge the hidden assumption driving the conflict |
| 3 | Solution Won't Fix It | Future Reality Tree (FRT) | Make every causal step explicit and testable |
| 4 | Will Cause Damage | Negative Branch (FRT extension) | Model the side effect; design an injection to neutralize it |
| 5 | Can't Implement It | Prerequisite Tree (PRT) | Convert obstacles into intermediate objectives |
| 6 | Unverbalized Fear | Open dialogue | Create psychological safety for the real concern to emerge |

---

## Layer 1 → Current Reality Tree (CRT)

**The tool:** A directed graph mapping undesirable effects (UDEs) to their root causes using "if... then..." cause-effect logic.

**Why it works here:** At Layer 1, the person doesn't agree there's a problem. Argument and data fail because the dispute is interpretive, not factual. The CRT sidesteps this by starting from effects that both parties can directly observe — not diagnoses or interpretations. By building the tree together, the stakeholder co-authors the diagnosis. A root cause they helped discover cannot be dismissed the way an externally imposed conclusion can.

**How to use it:**
1. List all undesirable effects (UDEs) you both observe in the current situation
2. Ask: what conditions would have to be true to cause all of these?
3. Draw cause-effect arrows until you converge on a small number of root causes
4. The root cause is the problem. They helped find it. That's buy-in at Layer 1.

**Common mistake:** Starting the CRT with your hypothesis for the root cause. Start from the UDEs, not the conclusion.

---

## Layer 2 → Evaporating Cloud (EC)

**The tool:** A diagram that maps the conflict between two positions by surfacing the underlying needs and assumptions each position is trying to satisfy.

**Why it works here:** At Layer 2, both parties want to solve the problem but disagree on how. The disagreement feels like stubbornness but is almost always based on an assumption neither party has made explicit. The EC makes the assumption visible — and once visible, it can be questioned. Often it turns out to be false, outdated, or only partially true. When the assumption evaporates, so does the conflict.

**Structure:**
```
Objective
├── Need A → Prerequisite A (your approach)
└── Need B → Prerequisite B (their approach)
      [Conflict: A and B appear incompatible]
```

**How to use it:**
1. State both parties' preferred approaches (Prerequisite A and B)
2. Ask: what need is each approach satisfying?
3. Ask: what shared objective are both needs serving?
4. For each need: "What assumption makes me believe I need [Prerequisite] to achieve [Need]?"
5. Challenge the assumption: is it always true? Under what conditions might it be false?

**Common mistake:** Using the EC to argue for your position rather than genuinely examining the conflict.

---

## Layer 3 → Future Reality Tree (FRT)

**The tool:** A directed graph mapping from proposed actions (injections) through intermediate effects to desired outcomes.

**Why it works here:** At Layer 3, the person says "it won't work." This means they see a break in your causal chain — a step where cause doesn't actually produce the claimed effect. The FRT forces you to spell out every step. When a step is made explicit, it can be examined. Either the logic holds (and the skeptic is satisfied) or it doesn't (and your solution needs revision). In both cases, you've moved forward.

**How to use it:**
1. State your injection (the proposed action)
2. Map each intermediate effect: "If we do X, then Y will happen, because..."
3. Continue until you reach the desired outcomes
4. For each arrow, ask: "Is this cause-effect relationship always true? Under what conditions might it fail?"

**Common mistake:** Asserting effects without showing the mechanism. "This will improve throughput" is not a step in an FRT. "This will reduce WIP at the constraint by 30%, which will reduce average cycle time, which will enable more orders to be completed per month" is.

---

## Layer 4 → Negative Branch (FRT extension)

**The tool:** An extension of the FRT that explicitly traces a proposed injection forward to its undesirable side effects, then designs a counter-injection to cut the branch.

**Why it works here:** At Layer 4, the person accepts your logic but sees a downstream damage path. Dismissing this concern loses credibility. Tracing it explicitly shows you've taken it seriously — and either proves it won't happen (reassurance with reasoning) or produces a supplementary fix (solution improvement).

**How to use it:**
1. Add the stakeholder's feared negative effect to your FRT
2. Trace backward: what would have to be true for your injection to lead to that effect?
3. Option A: Show that one of those intermediate steps won't actually occur (cut the branch)
4. Option B: Design a new injection that specifically prevents the branch from occurring

**Common mistake:** Adding an injection to "address concerns" without tracing whether it actually cuts the negative branch.

---

## Layer 5 → Prerequisite Tree (PRT)

**The tool:** A diagram that maps the obstacles between current state and goal, derives intermediate objectives (IOs) for each obstacle, and sequences the IOs into an implementation path.

**Why it works here:** At Layer 5, the person is bought in but sees obstacles. The PRT converts "we can't because X" into "to achieve this, we first need Y." It makes obstacles visible as problems to solve rather than reasons to stop. The output is a project plan, not a debate.

**Structure:**
```
Goal: [Desired state]
├── Obstacle: We don't have X
│   └── Intermediate Objective: Acquire X by [method]
└── Obstacle: We lack authority to Y
    └── Intermediate Objective: Secure approval from Z
```

**How to use it:**
1. State the goal clearly
2. List all obstacles that prevent reaching it
3. For each obstacle, derive the IO: "In order to overcome [obstacle], we must [IO]"
4. Sequence the IOs: which must be done first for others to become possible?
5. The result is an ordered action plan

**Common mistake:** Listing obstacles without deriving IOs. The PRT is not a complaint list — each obstacle requires a response.

---

## Layer 6 → Open Dialogue

**The tool:** Structured listening with no formal diagram.

**Why it works here:** Layer 6 is not a logic problem. It's a human problem. The person has a concern they haven't expressed — possibly because it's personal, embarrassing, politically sensitive, or because they haven't fully identified it themselves. No diagram resolves unexpressed fear. Only a conversation where the fear can safely surface can do that.

**How to use it:**
1. Create a private, low-stakes setting (not a group meeting)
2. Open with genuine curiosity, not persuasion: "I want to understand what I'm missing"
3. Ask questions that create space: "What would need to be true for this to feel right to you?"
4. Listen fully before responding — resist the urge to counter-argue
5. Reflect what you hear: "It sounds like your concern is [X] — is that right?"
6. If appropriate, name the unspoken: "Are you concerned about how this might affect your team?"

**Common mistake:** Treating Layer 6 as a variant of Layer 3. You cannot logic someone out of a fear they haven't named. The tool is empathy and patience, not argument.

---

## Diagnostic Questions by Layer

Use these questions to identify which layer you're at before choosing a tool:

| Question to Ask Yourself | If Yes, You're at Layer... |
|-------------------------|--------------------------|
| Does the person deny there's a problem? | 1 |
| Does the person agree there's a problem but want a different solution? | 2 |
| Does the person like your approach but doubt it'll work? | 3 |
| Does the person accept it'll work but worry about side effects? | 4 |
| Does the person want to proceed but cite practical obstacles? | 5 |
| Is the person's resistance vague, inconsistent, or unexplained? | 6 |
