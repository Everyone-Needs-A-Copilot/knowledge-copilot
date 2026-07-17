---
last_updated: 2026-02-25
status: active
name: research-ethics
description: Apply ethical principles to research design and execution. Address bias mitigation, informed consent, participant protection, and research limitations. Use when designing studies, handling sensitive data, or documenting research integrity.
triggers:
  keywords: ["research", "ethics", "apply", "ethical", "principles", "design", "execution", "address", "bias", "mitigation"]
allowed-tools: Read, Write, Edit
---

# Research Ethics

## Overview

Ensure research respects participants, produces valid findings, and acknowledges limitations. Covers informed consent, bias mitigation, data protection, and honest reporting. Ethical research is both morally required and produces better insights.


## Define Done

- [ ] Analysis inputs gathered from relevant data sources
- [ ] Framework/methodology applied systematically (not ad hoc)
- [ ] Findings supported by specific evidence, not assumptions
- [ ] Actionable recommendations produced with clear next steps

## Instructions

### Step 1: Assess Research Risk Level

Determine ethical scrutiny needed:

| Risk Level | Characteristics | Requirements |
|------------|-----------------|--------------|
| **Low** | Anonymous, public data, no sensitive topics | Basic consent, standard protections |
| **Medium** | Identifiable data, personal opinions, behavioral tracking | Written consent, data protection plan |
| **High** | Sensitive topics, vulnerable populations, potential harm | IRB review, detailed protocols |

```markdown
## Risk Assessment

**Research activity:** [Description]

### Risk Factors
| Factor | Level | Notes |
|--------|-------|-------|
| Data sensitivity | Low/Med/High | [What data collected] |
| Participant vulnerability | Low/Med/High | [Population characteristics] |
| Potential for harm | Low/Med/High | [How could this hurt someone] |
| Deception involved | Yes/No | [If yes, justify] |

**Overall risk level:** [Low/Medium/High]
**Required protections:** [List]
```

### Step 2: Design Informed Consent

Participants must understand what they're agreeing to:

| Consent Element | What to Include |
|-----------------|-----------------|
| **Purpose** | Why research is being done |
| **Procedures** | What participant will do |
| **Duration** | How long it takes |
| **Data use** | How information will be used |
| **Confidentiality** | How identity is protected |
| **Risks** | Potential discomfort or harm |
| **Benefits** | What they get (or don't) |
| **Voluntary** | Right to stop anytime |
| **Contact** | Who to reach with questions |

```markdown
## Consent Form Template

### About This Research
We are researching [topic] to better understand [goal]. This will help us
[how findings will be used].

### What You'll Do
- [Activity 1] (~X minutes)
- [Activity 2] (~X minutes)
- Total time: approximately X minutes

### How We'll Use Your Information
- [What we record/collect]
- [Who has access]
- [How long we keep it]
- [Whether it's anonymized]

### Your Rights
- Participation is voluntary
- You may stop at any time without penalty
- You may skip questions you don't want to answer
- You may request deletion of your data

### Questions?
Contact [Name] at [email/phone]

[ ] I understand and agree to participate
```

### Step 3: Mitigate Researcher Bias

Identify and address sources of bias:

| Bias Type | Description | Mitigation |
|-----------|-------------|------------|
| **Confirmation bias** | Seeking evidence for existing beliefs | Pre-register hypotheses, blind analysis |
| **Selection bias** | Non-representative sample | Explicit sampling criteria, document gaps |
| **Leading questions** | Influencing responses | Neutral question wording, pilot testing |
| **Interpretation bias** | Seeing what you expect | Multiple coders, inter-rater reliability |
| **Publication bias** | Only reporting positive results | Report all findings including null results |

```markdown
## Bias Mitigation Plan

### Pre-study
- [ ] Hypotheses documented before data collection
- [ ] Sampling criteria explicit and justified
- [ ] Interview guide reviewed for leading questions

### During study
- [ ] Consistent procedures across participants
- [ ] Interviewer remains neutral on topic
- [ ] All data recorded, not just "interesting" parts

### Analysis
- [ ] Coding done before checking demographics
- [ ] Multiple researchers review themes
- [ ] Disconfirming evidence actively sought

### Reporting
- [ ] All findings reported, not just significant ones
- [ ] Limitations section honest and complete
- [ ] Alternative interpretations acknowledged
```

### Step 4: Protect Participant Data

Handle data responsibly:

| Data Stage | Protection Measures |
|------------|---------------------|
| **Collection** | Encrypt transmission, minimize data collected |
| **Storage** | Secure systems, access controls, encryption at rest |
| **Processing** | Pseudonymization, need-to-know access |
| **Retention** | Delete when no longer needed, define timeline |
| **Sharing** | Anonymize, aggregate, get consent |

```markdown
## Data Protection Plan

### Data Inventory
| Data Type | Sensitivity | Storage | Access | Retention |
|-----------|-------------|---------|--------|-----------|
| Audio recordings | High | Encrypted drive | Researcher only | Delete after transcription |
| Transcripts | Medium | Secure server | Research team | 2 years |
| Anonymized quotes | Low | Research docs | Team + stakeholders | Indefinite |

### Security Measures
- [ ] Encrypted storage
- [ ] Strong access controls
- [ ] Audit logging
- [ ] Secure deletion procedures

### Breach Protocol
- [Steps if data is compromised]
```

### Step 5: Address Vulnerable Populations

Extra care for at-risk participants:

| Population | Additional Considerations |
|------------|---------------------------|
| **Minors** | Parental consent, assent from child |
| **Employees** | Power dynamics, anonymity critical |
| **Patients** | Health sensitivity, medical review |
| **Low literacy** | Verbal consent, simple language |
| **Marginalized groups** | Cultural sensitivity, community benefit |

```markdown
## Vulnerable Population Protocol

**Population:** [Description]
**Vulnerability factors:** [What makes them at-risk]

### Additional Protections
- [Protection 1]
- [Protection 2]

### Consent Modifications
- [How consent process is adapted]

### Benefit-sharing
- [How community benefits from research]
```

### Step 6: Document Limitations Honestly

Every study has weaknesses — acknowledge them:

| Limitation Category | Examples |
|--------------------|----------|
| **Sample** | Size, representativeness, recruitment bias |
| **Method** | Self-report inaccuracy, observer effects |
| **Measurement** | Construct validity, reliability |
| **Analysis** | Confounds, alternative explanations |
| **Generalizability** | What populations/contexts findings apply to |

```markdown
## Limitations Statement

### Sample Limitations
- [Limitation 1]: [Impact on findings]
- [Limitation 2]: [Impact on findings]

### Methodological Limitations
- [Limitation 1]: [Impact on findings]

### What We Cannot Claim
- [Overclaim to avoid]

### Future Research Needed
- [What would address these limitations]
```

### Step 7: Plan for Responsible Reporting

Report findings ethically:

```markdown
## Reporting Checklist

### Accuracy
- [ ] Findings accurately represent data
- [ ] Quotes in context
- [ ] No selective reporting

### Anonymity
- [ ] Participants cannot be identified
- [ ] Demographic combinations not identifying
- [ ] Quotes don't reveal identity

### Impact
- [ ] Considered how findings might be misused
- [ ] Framing doesn't stigmatize groups
- [ ] Caveats clear to prevent over-interpretation

### Attribution
- [ ] All contributors acknowledged
- [ ] Sources cited
- [ ] Conflicts of interest disclosed
```

## Examples

**Output: Research Ethics Protocol**

```markdown
# Research Ethics Protocol: Customer Churn Study

## Study Overview
**Purpose:** Understand why customers cancel subscriptions
**Method:** 30-minute phone interviews with recent churners
**Sample:** 20 customers who cancelled in past 30 days

## Risk Assessment

| Factor | Assessment | Rationale |
|--------|------------|-----------|
| Data sensitivity | Medium | Financial behavior, satisfaction issues |
| Participant vulnerability | Low | Adult consumers, voluntary |
| Potential for harm | Low | May surface frustration, manageable |
| Deception | None | Transparent about purpose |

**Overall risk:** Medium
**Review required:** Internal ethics review (not IRB)

## Informed Consent

### Consent Script (Verbal)
"Hi, this is [Name] from [Company]. We're conducting research to understand
how we can improve. The interview takes about 30 minutes.

I'll ask about your experience as a customer and why you decided to cancel.
Your feedback is confidential — we won't attach your name to any quotes we
share internally.

You can stop anytime or skip questions. There's no penalty for doing so.

With your permission, I'd like to record for accuracy. The recording is
only used for note-taking and deleted after.

Do you have any questions? Are you willing to participate?"

### Documentation
- Verbal consent recorded at interview start
- Consent confirmation in interview notes

## Bias Mitigation

### Recruitment
- Randomized selection from churned customer list
- Include both short-tenure and long-tenure customers
- Track declined participation to assess selection bias

### Interview
- Neutral question wording (reviewed by second researcher)
- No leading questions about specific product flaws
- Record all interviews to prevent selective note-taking

### Analysis
- Two researchers code independently
- Discuss disagreements to consensus
- Track themes that don't fit narrative

## Data Protection

| Data | Storage | Access | Retention |
|------|---------|--------|-----------|
| Consent records | CRM notes | CS team | 3 years |
| Audio | Encrypted laptop | Researcher | Delete after transcription |
| Transcripts | Research drive | Research team | 1 year |
| Analysis docs | Shared drive | Team + stakeholders | Indefinite |
| Final report | Wiki | Company-wide | Indefinite |

### Anonymization
- Replace names with participant codes (P1, P2...)
- Remove company names from quotes
- Aggregate any sensitive financials

## Special Considerations

### Emotional Participants
If participant becomes upset:
1. Pause recording
2. Acknowledge: "I understand that was frustrating"
3. Offer to stop: "We can end here if you prefer"
4. If continuing, redirect to constructive framing

### Unexpected Disclosures
If participant reveals concerning information (e.g., fraud):
- Thank them for sharing
- Do not promise confidentiality for illegal activity
- Consult with legal after interview if needed

## Limitations to Acknowledge

### In Final Report
- Sample is customers who agreed to talk (may exclude most dissatisfied)
- Interviews conducted 30 days post-churn (memory decay)
- Self-reported reasons may not reflect unconscious factors
- Small sample (n=20) limits generalizability
- Qualitative insights, not quantified prevalence

## Reporting Standards

### Quote Usage
- Use verbatim quotes only
- Include context if meaning depends on it
- Never composite quotes from multiple participants

### Framing
- Present churn reasons neutrally, not as "customer failures"
- Include positive feedback, not just complaints
- Note what we cannot conclude from this study
```



## Quality Tests

### Evidence Test
- Every finding cites specific data, quotes, or observations
- **PASS:** Each insight traces back to a named source or data point
- **FAIL:** Findings use vague language like 'it seems' or 'generally' without evidence

### Completeness Test
- All relevant dimensions of the framework have been considered
- **PASS:** Analysis addresses each framework dimension, noting gaps where data is unavailable
- **FAIL:** Key dimensions skipped without acknowledgment

### Actionability Test
- Recommendations are specific enough to act on immediately
- **PASS:** Each recommendation names who should do what by when
- **FAIL:** Recommendations are vague ('improve communication') without concrete actions

## Guidelines

1. **Consent is ongoing** — Participants can withdraw at any time
2. **Minimize data collection** — Only collect what you need
3. **Be transparent** — Tell participants what you're doing and why
4. **Honor commitments** — If you promise anonymity, ensure it
5. **Consider power dynamics** — Are participants truly free to refuse?
6. **Report honestly** — Include findings that don't support your hypothesis

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Buried consent | People agree without understanding | Clear, upfront, plain language |
| Incentive coercion | Payment too high = no real choice | Modest, appropriate compensation |
| Deceptive framing | Hiding true research purpose | Honest about goals (or justify deception) |
| Data hoarding | Keeping everything "just in case" | Delete when no longer needed |
| Cherry-picking quotes | Misleading representation | Show range of responses |
| Ignoring null results | Publication bias | Report all findings |

## Ethical Principles Reference

| Principle | Meaning | Application |
|-----------|---------|-------------|
| **Beneficence** | Do good | Research should benefit participants/society |
| **Non-maleficence** | Do no harm | Minimize risks to participants |
| **Autonomy** | Respect choice | Informed consent, right to withdraw |
| **Justice** | Fairness | Benefits and burdens distributed fairly |
| **Integrity** | Honesty | Report truthfully, acknowledge limitations |

## References

- Belmont Report: Foundational research ethics principles
- GDPR/CCPA: Data protection requirements
- interview-guide-design: Ethical interview practices
- research-design: Ethics in study design
