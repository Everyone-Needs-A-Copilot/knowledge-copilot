---
last_updated: 2026-06-28
status: active
---

# Prototype Hub Requirements

<!--
FACTORY AGENTS: CDO + CTO
==========================
This document is NOT facilitated. It is generated jointly by the CDO and CTO agents
after the prototype standards are published and the design challenge brief is approved.

The CDO defines the stakeholder experience requirements for the hub (what the product
owner needs to be able to see, compare, and respond to). The CTO defines the structural
and technical constraints the hub must satisfy. Neither agent writes this document alone.

INPUTS (read all before writing):
- 03-developer-guides/40-design-challenge/00-brief.md
    The authoritative source for: critical view list, number of concepts per view,
    evaluation criteria, and constraints. The hub must surface every CV in the brief.
    The feedback mechanism must map to the exact evaluation criteria in the brief.
- 03-developer-guides/50-prototypes/00-prototype-standards.md
    Defines the directory structure, naming conventions, branch strategy, and the
    pre-presentation checklist. The hub's URL structure must match the prototype
    standards directory structure.
- 02-user-guides/20-service-design/20-journey-maps.md
    Confirms the persona context. The hub is used by the project owner, not by
    end users of the product. The experience requirements for the hub flow from
    the project owner's review and decision-making context.
- 08-design-factory/GOVERNANCE.md
    Gate G5 requires project owner approval of all CV prototypes. The hub is the
    instrument of that approval. It must support a structured, traceable approval
    decision — not informal feedback.

GATE: G5 — CV Prototype Set Approved
The hub spec must be complete and the hub must be built before the G5 presentation.
The hub IS the presentation tool.

PROCESS:
1. Read the brief. Enumerate every critical view and the number of concepts per view.
   These become the hub's navigation nodes. There is one hub card per CV.
2. Read the prototype standards. Extract the URL and directory convention.
   Hub routes must match: /prototypes/cv-[number]-[view-name]/concept-[letter]/
3. Extract the evaluation criteria from the brief's evaluation criteria table.
   These populate the structured feedback form — verbatim, not paraphrased.
4. Define the hub's top-level structure: landing page, CV overview pages, concept
   detail pages, comparison views, feedback form.
5. Define per-CV entry requirements: what must appear on each CV overview card
   and on each concept detail page.
6. Define the concept comparison view. The product owner will compare concepts side by side.
   The layout must eliminate left-position bias.
7. Define the feedback mechanism. Feedback must be structured (not free-form only),
   timestamped, and exportable. This is the audit trail for the G5 approval decision.
8. Define responsive requirements for the presentation device context.

STYLE:
- Write requirements from the product owner's perspective, not the developer's.
  "The product owner must be able to..." not "The system shall..."
- Every requirement must be verifiable with a yes/no check.
  "Looks good" is not a requirement.
- The hub must work without explanation. No onboarding copy, no tooltips,
  no "how to use this." If the product owner has to ask how to use it, it has failed.
- The hub is a presentation tool, not a CMS or documentation site.
  Every feature must justify its presence by serving the G5 presentation.
-->

## Hub Purpose

The prototype hub is a single entry point (`/prototypes`) that organises all Critical View concepts for the product owner's review, comparison, and decision. It serves one purpose: make it easy to navigate between concepts, compare options, and record a direction decision.

The hub is used in two modes:

- **During the G5 presentation**: the presenter drives navigation on a shared screen.
  The product owner watches and reacts verbally; the presenter records decisions.
- **After the presentation**: the product owner returns independently to review concepts and submit
  written feedback before the design direction is locked.

The hub is not a documentation site. It does not explain the design process. It presents the work.

**What the hub is not:**
- Not a CMS. Content is not editable through the hub.
- Not a project management tool. It does not track task status.
- Not a design review portal. It is a decision-support tool for one stakeholder.

---

## Hub Structure

```
/prototypes                                  ← Hub landing page
│
├── /cv-01-[view-name]                       ← CV overview: all concepts for this view
│   ├── /concept-a-[philosophy]              ← Concept A full detail view
│   ├── /concept-b-[philosophy]              ← Concept B full detail view
│   ├── /concept-c-[philosophy]              ← Concept C (if brief specifies 3)
│   └── /compare                             ← Side-by-side comparison
│
├── /cv-02-[view-name]
│   ├── /concept-a-[philosophy]
│   ├── /concept-b-[philosophy]
│   └── /compare
│
└── /feedback                                ← Consolidated post-presentation feedback form
```

### Landing Page (`/prototypes`)

The landing page must contain exactly the following — no more, no less:

- One sentence describing the design challenge (drawn verbatim from the brief's first paragraph)
- One card per critical view, ordered by CV number
- Each card links to the CV overview page for that view
- A status indicator per CV: `Not Started` | `Ready for Review` | `Decision Made`
- A link to the consolidated feedback form
- No authentication required

The landing page must not contain: navigation instructions, process explanations, agent names, phase labels, or any content that requires context to interpret.

---

## Per-CV Entry Requirements

Each critical view must have an overview page at `/prototypes/cv-[number]-[view-name]`.

### CV Overview Page Contents

| Element | Content | Source |
|---------|---------|--------|
| View title | Exact CV name from the brief | Brief |
| What this view does | One sentence — what the user accomplishes here | Brief |
| What we are deciding | One sentence — the design decision this CV resolves | Brief |
| Concept cards | One card per concept (see below) | Concepts |
| Navigation | Previous CV / Next CV links | Hub structure |

### Concept Card (on CV Overview Page)

Each concept within a CV must have a card on the CV overview page:

| Element | Content |
|---------|---------|
| Concept letter and name | e.g., "Concept A: Command Center" |
| Design hypothesis | One sentence — the assumption this concept tests |
| Thumbnail | Static screenshot of the primary state (WebP, max 200KB) |
| "View concept" link | Opens the full concept detail page |
| "Compare" link | Opens the `/compare` page for this CV |
| Feedback status indicator | `No feedback yet` or `Feedback submitted` |

### Concept Detail Page (`/prototypes/cv-[n]/concept-[letter]`)

Each concept detail page must show:

| Element | Content |
|---------|---------|
| Concept name and CV context | e.g., "CV-01 — Concept A: Command Center" |
| Design hypothesis | Full hypothesis from the concept's `README.md` |
| Key decisions | Bulleted list of decisions and their rationale |
| What to look for | What the product owner should focus on during review |
| What this concept does not address | Known gaps — set expectations explicitly |
| The concept itself | Interactive page (preferred) or full-size static screenshots |
| "Give feedback on this concept" link | Links to the feedback form pre-filled for this concept |
| Back to CV overview | Breadcrumb navigation |

---

## Concept Comparison View (`/prototypes/cv-[n]/compare`)

Each CV with two or more concepts must have a `/compare` page for direct side-by-side evaluation.

### Layout Requirements

| Requirement | Detail |
|-------------|--------|
| Column count | Two equal-width columns at desktop (1280px+) |
| Per-column contents | Concept name, design hypothesis, primary screen |
| Primary screen display | Scrollable iframe (if interactive) or full-size screenshot |
| Position swap | A toggle control to swap left/right positions; eliminates left-position bias |
| Feedback prompt | "Which do you prefer, and why?" prompt — one free-text input per concept |

### Behavior Requirements

- The comparison view is read-only for the concept content. Interaction within embedded iframes is not required — static screenshots are acceptable.
- If concepts are interactive pages, they may be embedded in iframes; otherwise static screenshots are used.
- Feedback submitted on the comparison view is stored in the same feedback store as the main feedback form — not separately.
- The comparison view must be accessible without navigating through the full concept detail pages first.

---

## Feedback Mechanism

The feedback mechanism must allow the product owner to record a structured reaction to each concept during or after the presentation. "I liked it" is not sufficient. The mechanism must capture a decision with traceable reasoning.

### Feedback Form Structure

Each concept receives a separate feedback entry. The form fields:

| Field | Type | Required |
|-------|------|----------|
| CV number and name | Read-only display | — |
| Concept letter and name | Read-only display | — |
| Reviewer name or identifier | Text input | Yes |
| Overall reaction | 5-point scale: 1 = Not for us → 5 = This is it | Yes |
| Per evaluation criterion rating | One 1–5 rating per criterion from the brief | Yes |
| What works | Free text | No |
| What does not work | Free text | No |
| Would you proceed with this concept? | Yes / No / Yes with changes | Yes |

### Evaluation Criteria

The per-criterion ratings are drawn directly from the design challenge brief's evaluation criteria table. The factory agent filling in this section must copy the criterion names and weights from the brief verbatim. Do not invent criteria; do not paraphrase criterion names.

<!-- Fill in from 03-developer-guides/40-design-challenge/00-brief.md once the brief is completed:

| Criterion | Weight |
|-----------|--------|
| [from brief — copy verbatim] | [from brief] |

-->

### Feedback Storage

For the prototype phase, feedback must be stored using one of these options:

| Option | When to Use |
|--------|-------------|
| Local JSON file (`/data/feedback.json`) | Small team, no external services; suitable for internal-only presentations |
| Google Form linked from the hub | When the product owner submits feedback independently after the presentation |
| Vercel KV or equivalent edge store | When the hub is deployed for remote access |

Regardless of storage method, every submission must satisfy:

- Timestamped on submission (ISO 8601, UTC)
- Reviewer identifier captured (name or email)
- Concept identifier captured (CV number + concept letter)
- All field values persisted — no partial submissions stored
- Exportable as CSV or JSON for post-presentation synthesis

### Post-Presentation Decision Recording

After the G5 presentation, the CDO reviews all feedback and records a direction decision per CV. The hub must display a decision indicator on each CV card once the decision is recorded:

| Status | Meaning |
|--------|---------|
| `Not Started` | No concepts ready for review |
| `Ready for Review` | All concepts for this CV are complete |
| `Feedback Submitted` | Product owner has submitted structured feedback |
| `Decision Made` | CDO has recorded the approved direction |

---

## Responsive Design Requirements

The hub must work on the devices used in a G5 presentation context.

| Device | Viewport | Requirement |
|--------|----------|-------------|
| Presenter's laptop | 1280px+ | Full layout; all features available; no horizontal scroll |
| External monitor / projector | 1440px–1920px | Must scale without overflow; no zoom required |
| Tablet (product owner reviewing independently) | 768px | Concept cards stack vertically; comparison view stacks vertically |
| Mobile | Below 768px | Best-effort only; not required for presentation scenarios |

### Typography Standards

| Element | Minimum Size | Reason |
|---------|-------------|--------|
| Base body text | 16px | Legibility on projector at viewing distance |
| Concept names and headings | 20px | Scannable from across a conference table |
| All body text | 4.5:1 contrast ratio minimum | WCAG AA — the hub itself must be accessible |

### Performance Standards

| Metric | Target | Rationale |
|--------|--------|-----------|
| Hub landing page load | < 2 seconds on office Wi-Fi | Presentations have no tolerance for load delays |
| Concept thumbnail size | Max 200KB per image, WebP preferred | Multiply by total concepts — keep the total page weight reasonable |
| Concept detail page load | < 3 seconds | Product owner must not wait |
| Interactive concept loading | On-demand only — not preloaded on landing page | Prevents the hub from loading the entire prototype set on first visit |
