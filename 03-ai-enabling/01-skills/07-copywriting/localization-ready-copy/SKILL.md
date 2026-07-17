---
last_updated: 2026-02-25
status: active
name: localization-ready-copy
description: Write copy that translates well and adapts easily to different languages and cultures. Use for internationalization (i18n), preparing content for translation, and culturally-aware writing.
triggers:
  files: ["**/i18n/**", "**/locales/**", "**/translations/**", "**/*.json", "**/lang/**"]
  keywords: ["localization", "i18n", "translation", "internationalization", "l10n", "multilingual", "global content", "translate"]
allowed-tools: Read, Write, Edit
---

# Localization-Ready Copy Skill

Write copy that translates well and works across languages and cultures. Good localization-ready copy avoids translation pitfalls, accommodates text expansion, and maintains meaning across cultural contexts.

---

## Core Principles

### Localization-Ready Mindset

| Principle | Description | Example |
|-----------|-------------|---------|
| Clear source | Simple, direct English translates better | "Save file" not "Go ahead and save that file" |
| Context-complete | Meaning clear without surrounding context | Full phrases, not fragments |
| Culturally neutral | Avoids culture-specific references | "Autumn" not "Fall" |
| Flexible layout | Accommodates text expansion | UI handles 30-50% longer text |
| Separable | Text separated from code | Strings in resource files |

### Why It Matters

| Issue | Impact |
|-------|--------|
| Poor source | Costly translation errors |
| No context | Translators guess wrong |
| Text expansion | UI breaks in other languages |
| Cultural references | Content doesn't resonate |
| Hardcoded text | Can't translate without code changes |

---


## Define Done

- [ ] Copy serves the user's goal at this specific touchpoint
- [ ] Tone matches the brand voice and emotional context
- [ ] Copy is concise — no unnecessary words
- [ ] Accessible language (no jargon unless audience expects it)

## Writing for Translation

### Sentence Structure

| Avoid | Use | Why |
|-------|-----|-----|
| Sentence fragments | Complete sentences | Fragments lack context for translators |
| Embedded variables mid-sentence | Variables at start/end | Word order differs by language |
| Multiple clauses | Simple sentences | Complex syntax doesn't translate well |
| Passive voice | Active voice | Clearer, translates more consistently |

### Word Choice

| Avoid | Use | Why |
|-------|-----|-----|
| Idioms | Literal expressions | "Piece of cake" → "Easy to do" |
| Phrasal verbs | Simple verbs | "Put off" → "Postpone" |
| Colloquialisms | Standard language | "Gonna" → "Going to" |
| Abbreviations | Full words | "Approx." → "Approximately" |
| Homonyms | Unambiguous words | "Right" (correct vs direction) |

### Technical Terms

| Guideline | Example |
|-----------|---------|
| Use consistent terminology | Always "dashboard" not "homepage/overview/main" |
| Define jargon | Provide glossary for translators |
| Consider translatability | Some terms may need adaptation |
| Allow for non-translation | Some tech terms stay English |

---

## Variables and Placeholders

### Variable Placement

Place variables where grammar allows flexibility:

```
Bad:  "{name}'s {item} has been deleted"  (possessive varies by language)
Good: "The {item} belonging to {name} has been deleted"
Better: "{item} deleted for {name}"
```

### Variable Context

Always provide context for variables:

```json
{
  "deleteConfirm": "Delete {itemName}?",
  "_deleteConfirm.description": "itemName is the title of the project being deleted"
}
```

### Pluralization

Use proper plural handling:

```json
{
  "itemCount": {
    "zero": "No items",
    "one": "{count} item",
    "other": "{count} items"
  }
}
```

Note: Some languages have more than 2 plural forms (Arabic has 6).

### Number and Date Formatting

| Element | Approach |
|---------|----------|
| Numbers | Use locale-aware formatting |
| Dates | Use locale date formats or explicit format |
| Currency | Use locale currency formatting |
| Units | Use locale-appropriate units |

```
Bad:  "10/4/24"  (ambiguous: Oct 4 or Apr 10?)
Good: Use date formatting library with locale
```

---

## Text Length and Expansion

### Expansion Rates

| Source Language | Expansion Estimate |
|-----------------|-------------------|
| English → German | +30% |
| English → French | +20% |
| English → Spanish | +25% |
| English → Chinese | -10 to -30% |
| English → Japanese | Variable |

### UI Accommodation

| Element | Recommendation |
|---------|----------------|
| Buttons | Allow 30-50% expansion |
| Navigation | Avoid fixed widths |
| Headlines | Test at 150% length |
| Labels | Allow wrapping |
| Error messages | Plan for expansion |

### Short Copy Challenges

| Issue | Solution |
|-------|----------|
| Single-word buttons | Choose words that translate to similar length |
| Abbreviations | Avoid or provide full form for translation |
| Character limits | Document limits for translators |

---

## Cultural Considerations

### Things to Avoid

| Category | Examples to Avoid |
|----------|-------------------|
| Holidays | "Black Friday sale", "Christmas special" |
| Sports | "Home run", "Slam dunk", "Touchdown" |
| Cultural references | "Uncle Sam", historical figures |
| Food references | "Apple pie", "as American as..." |
| Gestures | Thumbs up, OK sign (meanings vary) |
| Colors | Cultural color meanings differ |

### Neutral Alternatives

| Instead of | Use |
|------------|-----|
| "Home run" | "Great success" |
| "Fall season" | "Autumn" |
| "Holiday sale" | "Seasonal sale" |
| "Business hours 9-5" | Specify timezone |

### Dates, Times, and Formats

| Element | Consideration |
|---------|---------------|
| Date format | Use ISO or locale-specific |
| Time zones | Display user's timezone |
| First day of week | Varies (Sunday vs Monday) |
| Number formatting | Comma vs period for decimals |
| Address format | Varies significantly by country |

---

## Content Structure

### Keep Strings Complete

| Bad | Good |
|-----|------|
| "You have" + count + "items" | "You have {count} items" (one string) |
| "Error:" + errorMessage | Include prefix in translated string |

### Reusable Strings

Create translation-friendly, reusable strings:

| String ID | String | Context |
|-----------|--------|---------|
| `save.button` | "Save" | Generic save action |
| `save.changes` | "Save changes" | Saving modified content |
| `save.draft` | "Save draft" | Saving incomplete work |

### String Keys

| Approach | Example |
|----------|---------|
| Descriptive keys | `dashboard.welcome.title` |
| Include component | `nav.home.label` |
| Include context | `error.validation.email` |

---

## Comments and Context

### Translator Notes

Provide context for every string:

```json
{
  "welcomeBack": "Welcome back, {name}!",
  "_welcomeBack.description": "Greeting shown on dashboard after user logs in. {name} is the user's first name.",
  "_welcomeBack.maxLength": 50
}
```

### Context to Include

| Information | Why |
|-------------|-----|
| Where it appears | Helps translator choose register |
| Variable content | Explains placeholders |
| Character limits | Technical constraints |
| Related strings | Maintain consistency |
| Screenshots | Visual context |

---

## Testing Localized Copy

### Pseudo-Localization

Test with pseudo-localization to catch issues:

```
"Save changes" → "[Šåvé çhåñgéš]" (for expansion/character testing)
```

| What It Tests | How |
|---------------|-----|
| Text expansion | Adds ~30% length |
| Character support | Uses accented characters |
| Hardcoded strings | Untranslated text stands out |
| Truncation | Reveals UI constraints |

### Checklist Before Translation

| Check | Question |
|-------|----------|
| Complete strings | Are all strings externalized? |
| Variables documented | Is context provided for all placeholders? |
| Plurals handled | Is plural logic implemented? |
| Dates/numbers | Are formats locale-aware? |
| Cultural references | Have idioms been neutralized? |
| UI flexibility | Can layouts handle expansion? |
| Screenshots | Are visual references provided? |

---

## Common Mistakes

### String Issues

| Mistake | Problem | Fix |
|---------|---------|-----|
| Concatenation | Grammar breaks in translation | Use complete sentences |
| Hardcoded text | Can't translate | Externalize all strings |
| Assuming word order | Languages structure differently | Full phrases, not fragments |
| Shared strings | Same word, different contexts | Context-specific strings |

### Technical Issues

| Mistake | Problem | Fix |
|---------|---------|-----|
| Fixed widths | Text overflow | Flexible layouts |
| Embedded images with text | Can't translate | Separate text layers |
| Right-to-left ignored | Broken UI for Arabic/Hebrew | Support RTL |
| Sort assumptions | Alphabetical order varies | Locale-aware sorting |

---

## Style Guide for Localization

### Keep It Simple

| Complex | Simple |
|---------|--------|
| "You've got to check this out!" | "See this feature." |
| "What you'll wanna do is..." | "Do this:" |
| "Kind of like..." | "Similar to..." |
| "Let's go ahead and..." | "[Action]" directly |

### Consistent Terminology

Create a glossary:

| Term | Definition | Notes |
|------|------------|-------|
| Dashboard | Main overview screen | Always "dashboard", never "homepage" |
| Project | User-created work container | Capitalize when referring to feature |
| Member | Person in workspace | Not "user" or "teammate" |

### Tone Adjustments

| Consideration | Guidance |
|---------------|----------|
| Formality | Some languages require formal/informal choice |
| Humor | Often doesn't translate; use sparingly |
| Directness | Some cultures prefer more/less direct |
| Politeness markers | "Please" may be unnecessary or required |

---

## Templates

### String Resource Template

```json
{
  "stringKey": "String value with {variable}",
  "_stringKey.description": "Context explaining where this appears and what {variable} contains",
  "_stringKey.maxLength": 50
}
```

### Plural String Template

```json
{
  "itemsSelected": {
    "zero": "No items selected",
    "one": "{count} item selected",
    "two": "{count} items selected",
    "few": "{count} items selected",
    "many": "{count} items selected",
    "other": "{count} items selected"
  },
  "_itemsSelected.description": "Count of selected items in list view"
}
```

### Translator Context Template

```
String: "{count} projects remaining"
Location: Dashboard > Progress section
Variables: {count} = number (1-100)
Max length: 30 characters
Related strings: "All projects complete", "No projects started"
Notes: Shown when user has incomplete projects
Screenshot: [attached or linked]
```

---

This skill enables you to write copy that translates effectively and works across languages and cultures.


## Quality Tests

### Clarity Test
- A first-time user understands the copy without context
- **PASS:** Copy uses plain language and active voice
- **FAIL:** Copy requires domain knowledge or re-reading to understand

### Action Test
- User knows exactly what to do after reading the copy
- **PASS:** Clear call-to-action or next step is obvious
- **FAIL:** Copy describes a situation but doesn't guide the user forward

