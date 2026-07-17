---
last_updated: 2026-02-25
status: active
name: tutorial-writing
description: Tutorial writing - goals, prerequisites, step-by-step instructions. Use for learning-oriented documentation.
triggers:
  files: ["**/tutorials/**", "**/getting-started/**", "**/quickstart/**"]
  keywords: ["tutorial", "getting started", "walkthrough", "step-by-step", "learn", "guide", "quickstart"]
allowed-tools: Read, Write, Edit
---

# Tutorial Writing Skill

Create effective tutorials that guide learners through hands-on experiences with clear goals, prerequisites, and step-by-step instructions.

---

## Tutorial Structure

### Required Sections

| Section | Purpose |
|---------|---------|
| **Title** | Clear, action-oriented |
| **Introduction** | What they'll build/learn |
| **Prerequisites** | Required knowledge, tools, accounts |
| **Time Estimate** | Expected duration |
| **Steps** | Numbered, sequential instructions |
| **Verification** | How to confirm success |
| **Next Steps** | Where to go from here |
| **Troubleshooting** | Common issues and solutions |

---


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## Tutorial Template

```markdown
# Building a [Feature Name]

Learn how to [specific outcome] by building [concrete deliverable].

**What you'll build**: [Screenshot or description of end result]

**Time**: [X] minutes
**Level**: Beginner | Intermediate | Advanced
**Prerequisites**:
- [Tool/language] version X+
- [Account/access] for [service]
- Basic knowledge of [topic]

## What You'll Learn

- [Skill/concept 1]
- [Skill/concept 2]
- [Skill/concept 3]

## Step 1: [Setup/First Action]

[Brief intro to what this step accomplishes]

```bash
# Command to run
command --flag value
```

You should see:

```
Expected output here
```

**What just happened?**
[1-2 sentences explaining what the step did]

## Step 2: [Next Action]

[Continue pattern...]

## Verification

Your setup is complete when:
- [ ] [Checkable outcome 1]
- [ ] [Checkable outcome 2]

## Next Steps

- [Related tutorial link]
- [Documentation link]
- [Advanced topic link]

## Troubleshooting

### [Common Error Message]

**Cause**: [Why this happens]

**Solution**:
```bash
# Fix command
```
```

---

## Writing Effective Steps

### Step Structure

Each step should contain:

1. **Goal**: What this step accomplishes
2. **Action**: Exact commands or UI actions
3. **Expected Result**: What success looks like
4. **Explanation**: Why this matters (optional)

### Example Step

```markdown
## Step 3: Create the Database

Set up the PostgreSQL database for storing topics.

Run the migration script:

```bash
npm run db:migrate
```

You should see:

```
Running migrations...
✓ Created table: users
✓ Created table: topics
✓ Created table: evidence
Migration complete.
```

**What just happened?**
The script created three tables in your database. The `topics` table stores discovered insights, while `evidence` links supporting data from various sources.
```

---

## Prerequisites Section

### Be Specific

| Vague | Specific |
|-------|----------|
| "Node.js installed" | "Node.js 18+ (check with `node --version`)" |
| "Database running" | "PostgreSQL 14+ running on localhost:5432" |
| "API access" | "OpenAI API key (get one at platform.openai.com)" |

### Check Commands

Provide verification commands:

```markdown
## Prerequisites

### Node.js 18+

```bash
node --version
# Should output v18.x.x or higher
```

### Docker

```bash
docker --version
# Should output Docker version 24.x.x or higher
```

### API Keys

You'll need:
- **OpenAI API Key**: [Get one here](https://platform.openai.com/api-keys)
- **Database URL**: `postgresql://user:pass@localhost:5432/mydb`
```

---

## Code Examples

### Complete and Runnable

Every code block should be copy-paste ready:

```markdown
Create a new file `index.ts`:

```typescript
import { Client } from "@example/sdk";

const client = new Client({
  apiKey: process.env.API_KEY,
});

async function main() {
  const topics = await client.listTopics();
  console.log("Found", topics.length, "topics");
}

main().catch(console.error);
```

Run it:

```bash
npx ts-node index.ts
```

Expected output:

```
Found 3 topics
```
```

### Show Full Context

When modifying existing code, show enough context:

```markdown
Update `src/config.ts` to add the new setting:

```typescript
// src/config.ts
export const config = {
  apiUrl: process.env.API_URL,
  timeout: 5000,
  // Add this line:
  retries: 3,
};
```
```

---

## Verification Points

### After Each Major Step

```markdown
At this point, your project structure should look like:

```
my-project/
├── src/
│   ├── index.ts
│   └── config.ts
├── package.json
└── tsconfig.json
```

Verify the server is running:

```bash
curl http://localhost:3000/health
# Should return: {"status": "ok"}
```
```

### Final Verification

```markdown
## Verification

Your tutorial is complete when all checks pass:

- [ ] Server responds at http://localhost:3000
- [ ] API returns topics from `/api/topics`
- [ ] Database contains seeded data
- [ ] Logs show no errors
```

---

## Troubleshooting Section

### Common Issue Format

```markdown
## Troubleshooting

### "Connection refused" error

**Symptom**:
```
Error: connect ECONNREFUSED 127.0.0.1:5432
```

**Cause**: PostgreSQL is not running

**Solution**:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Verify it's running
docker-compose ps
```

---

### "Module not found" error

**Symptom**:
```
Error: Cannot find module '@example/sdk'
```

**Cause**: Dependencies not installed

**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```
```

---

## Best Practices

### Do

- [ ] Start with a working end state in mind
- [ ] Test every step before publishing
- [ ] Use realistic data and examples
- [ ] Explain "why" after showing "how"
- [ ] Include screenshots for UI steps
- [ ] Provide checkpoint verification
- [ ] Link to reference docs for deep dives

### Don't

- [ ] Skip steps (even "obvious" ones)
- [ ] Use placeholder values without explanation
- [ ] Assume tools are installed
- [ ] Leave errors unexplained
- [ ] Mix multiple concepts in one step
- [ ] Write steps that only work on one OS

---

## Difficulty Levels

| Level | Prerequisites | Explanation Depth |
|-------|---------------|-------------------|
| **Beginner** | None assumed | Explain everything, slower pace |
| **Intermediate** | Basic familiarity | Focus on new concepts, skip basics |
| **Advanced** | Working knowledge | Assume context, focus on nuances |

---

This skill enables creation of effective, learner-friendly tutorials.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

