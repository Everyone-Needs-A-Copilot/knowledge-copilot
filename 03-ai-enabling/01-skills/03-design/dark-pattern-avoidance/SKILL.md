---
last_updated: 2026-02-25
status: active
name: dark-pattern-avoidance
description: Identify and avoid manipulative dark patterns - confirmshaming, forced continuity, hidden costs. Use when reviewing designs for ethical issues.
triggers:
  files: ["**/checkout/**", "**/signup/**", "**/subscription/**", "**/pricing/**"]
  keywords: ["dark pattern", "confirmshaming", "forced continuity", "hidden costs", "roach motel", "privacy zuckering", "ethical design"]
allowed-tools: Read, Write, Edit
---

# Dark Pattern Avoidance

Dark patterns are deceptive design techniques that trick users into unintended actions. Ethical design respects user autonomy and builds lasting trust.

## Core Principle

**Design for user success, not business exploitation.** Short-term gains from manipulation create long-term brand damage and legal risk.


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Categories of Dark Patterns

### Confirmshaming

**Definition:** Using guilt or shame to manipulate user decisions.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| "No thanks, I don't want to save money" | Guilts user for declining | "No thanks" or "Skip" |
| "I'll stay uninformed" | Shames newsletter skip | "Not now" |
| "I prefer to pay full price" | Mocks discount refusal | "Continue without discount" |

**Fix:** Use neutral, non-judgmental decline options.

### Forced Continuity

**Definition:** Making it easy to sign up but hard to cancel.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| Cancel requires phone call | Barrier to exit | Cancel in same place as signup |
| Hidden unsubscribe | Users feel trapped | Clear account settings |
| Renewal buried in fine print | Surprise charges | Prominent renewal notices |

**Fix:** Cancellation should be as easy as signup.

### Hidden Costs

**Definition:** Revealing additional charges late in the flow.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| Service fee at checkout | Bait and switch | Show total cost upfront |
| Shipping costs hidden | Abandoned carts | Estimate shipping early |
| "Convenience fee" surprise | Broken trust | Transparent pricing |

**Fix:** Show full costs on product/pricing pages.

### Bait and Switch

**Definition:** Advertising one thing, delivering another.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| "Free" with asterisks | Misleading | Clear terms upfront |
| Feature only in premium | Frustration | Clear tier comparison |
| Different checkout than shown | Trust violation | WYSIWYG pricing |

**Fix:** What users see is what users get.

### Roach Motel

**Definition:** Easy to get in, hard to get out.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| Account deletion hidden | Data hostage | Prominent delete option |
| Complex unsubscribe | Email spam | One-click unsubscribe |
| Subscription traps | Unwanted charges | Easy cancellation |

**Fix:** Exits should be as clear as entrances.

### Privacy Zuckering

**Definition:** Confusing privacy settings to harvest data.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| Privacy defaults to "share" | Data exploitation | Private by default |
| 50 toggle settings | Decision fatigue | Simple, clear options |
| "Accept all" prominent | Manufactured consent | Equal weight to choices |

**Fix:** Default to privacy; make settings understandable.

### Misdirection

**Definition:** Using visual design to draw attention away from important information.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| Tiny "decline" button | Manipulates clicks | Equal visual weight |
| Auto-checked add-ons | Unwanted purchases | Opt-in, not opt-out |
| Terms buried in design | Hidden obligations | Clear, readable terms |

**Fix:** Important choices deserve equal visual treatment.

### Trick Questions

**Definition:** Confusing wording to produce unintended answers.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| Double negatives | Accidental consent | Simple, direct language |
| "Uncheck to not receive" | Cognitive confusion | "Check to receive" |
| Reversed yes/no meaning | Wrong selections | Consistent patterns |

**Fix:** Language should be clear and consistent.

### Friend Spam

**Definition:** Tricking users into sharing contacts for marketing.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| "Find friends" imports contacts | Privacy violation | Explicit consent |
| Auto-invite contacts | Spam on user's behalf | Manual invite only |
| Social graph harvesting | Data exploitation | Minimal permissions |

**Fix:** Request only necessary permissions with clear purpose.

### Disguised Ads

**Definition:** Advertisements disguised as content or navigation.

| Example | Problem | Ethical Alternative |
|---------|---------|---------------------|
| Ads look like articles | Deceptive clicks | Clear "Ad" labels |
| Download buttons (ads) | Wrong clicks | Distinguish from UI |
| Sponsored results unlabeled | Hidden promotion | "Sponsored" label |

**Fix:** Clearly distinguish paid content from organic.

## Ethical Patterns

### Transparent Pricing

```
Instead of:                    Use:
─────────────────────────────────────────────
Product: $49                   Product: $49
[Add to Cart]                  Shipping: $5.99
                              Tax: $4.41
...later at checkout...        ─────────────
Shipping: $5.99               Total: $59.40
Tax: $4.41
─────────────                  [Add to Cart]
Total: $59.40
```

### Clear Opt-In

```
Instead of:                    Use:
─────────────────────────────────────────────
☑ Send me newsletters          ☐ Yes, send me newsletters
☑ Share with partners          ☐ Share my data with partners
(pre-checked)                  (unchecked by default)
```

### Honest Decline Options

```
Instead of:                    Use:
─────────────────────────────────────────────
[Sign Up]                      [Sign Up]
"No thanks, I hate saving"     [No thanks]
                              or
                              [Skip]
```

### Easy Cancellation

```
Instead of:                    Use:
─────────────────────────────────────────────
Settings → Account →           Settings → Subscription
Billing → Contact Support      [Cancel Subscription]
→ Call 1-800-xxx-xxxx →
Wait on hold →                 Are you sure?
Speak to retention             [Keep Subscription] [Cancel]
```

## Dark Pattern Detection Checklist

### Checkout/Payment
- [ ] Total cost visible before entering payment info
- [ ] No surprise fees added at final step
- [ ] Pre-selected add-ons/upgrades are avoided

### Subscriptions
- [ ] Cancellation path is clear and accessible
- [ ] Renewal terms prominently displayed
- [ ] No auto-upgrade without consent

### Account/Privacy
- [ ] Privacy settings are comprehensible
- [ ] Default settings favor user privacy
- [ ] Account deletion is findable and works

### Consent & Communication
- [ ] Marketing is opt-in, not opt-out
- [ ] Decline options are neutral (no shaming)
- [ ] Permissions requests explain why

### Visual Design
- [ ] Important options have equal visual weight
- [ ] Ads are clearly labeled
- [ ] Terms are readable (not hidden)

### Language
- [ ] No double negatives or trick questions
- [ ] Options are clear and consistent
- [ ] Language is honest, not manipulative

## Legal Considerations

Dark patterns face increasing regulation:

| Region | Regulation | Focus |
|--------|------------|-------|
| EU | GDPR, DSA | Consent, cookie walls |
| California | CCPA | Privacy, opt-out rights |
| FTC (US) | Section 5 | Deceptive practices |
| UK | CMA | Subscription traps |

**Risk:** Fines, lawsuits, forced redesigns, brand damage.

## Ethical Design Principles

1. **Transparency** - Users understand what they're agreeing to
2. **Consent** - Opt-in rather than opt-out
3. **Equity** - Options given equal visual treatment
4. **Accessibility** - Important info easy to find and read
5. **Respect** - User autonomy valued over conversion metrics

## Testing for Dark Patterns

| Method | What to Check |
|--------|---------------|
| User testing | Can users complete tasks without tricks? |
| Cognitive walkthrough | Are choices clear and fair? |
| Competitive analysis | Are we worse than ethical competitors? |
| Legal review | Do we comply with regulations? |
| A/B testing ethics | Are we optimizing for user success? |

---

**Remember**: Trust is hard to build and easy to lose. Ethical design creates sustainable growth; dark patterns create churn, complaints, and legal exposure.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

