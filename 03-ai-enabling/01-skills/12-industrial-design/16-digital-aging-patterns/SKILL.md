---
last_updated: 2026-02-25
status: active
name: digital-aging-patterns
description: Design patterns for digital product aging and personalization. Use when considering how products learn, enrich data, and improve through user interaction over time.
category: industrial-design-digital
keywords:
  - personalization
  - learning
  - data-enrichment
  - patina
  - improvement
triggers:
  keywords:
    - personalization
    - user preferences
    - learned behavior
    - data enrichment
    - improving over time
  filePatterns:
    - "**/services/**/*.ts"
    - "**/models/**/*.ts"
    - "**/preferences/**"
allowed-tools: Read, Write, Edit
---

# Digital Aging Patterns

Design products that improve with use through data enrichment and learned preferences.

## Philosophy

Physical products age gracefully—leather develops patina, tools conform to your hand, mechanical watches gain character. Digital products should do the same. Not through artificial "gamification," but through genuine improvement: the system learns, data enriches, patterns emerge. The product becomes more yours the longer you use it.

**Rams Principle 3 (Aesthetic):** Beauty emerges from rightness—including the rightness of age.


## Define Done

- [ ] Design decisions tied to functional requirements and user needs
- [ ] Material choices justified by use context and lifecycle
- [ ] Form follows function — no purely decorative elements
- [ ] Evaluation criteria are specific and measurable

## Methodology

### Step 1: Identify Aging Vectors

| Aging Vector | Physical Analog | Digital Implementation |
|--------------|-----------------|------------------------|
| **Patina** | Leather darkens with use | Frequently-used features surface |
| **Worn paths** | Handles smooth where gripped | UI adapts to user's patterns |
| **Muscle memory** | Tool feels natural | Keyboard shortcuts learned |
| **Personalization** | Adjusted to owner | Settings, preferences persist |
| **Data enrichment** | Notes in margins | Metadata accumulates |
| **Relationship** | Ownership pride | User's work embedded in system |

### Step 2: Design for Enrichment

Data should become more valuable over time:

```typescript
interface Insight {
  id: string;
  title: string;
  content: string;
  created_at: Date;

  // Enrichment over time
  view_count: number;           // Usage patina
  last_viewed: Date;            // Recency
  linked_insights: string[];    // Relationship depth
  user_notes: string[];         // Personal annotations
  confidence_score: number;     // Improves with validation
  related_projects: string[];   // Context grows
}
```

### Step 3: Surface Frequency

Frequently-used features should become easier to access:

```typescript
// Track usage patterns
interface UserPreferences {
  feature_frequency: Record<string, number>;
  quick_access: string[];  // Auto-populated by usage
  keyboard_shortcuts: Record<string, string>;  // Learns habits
}

// Adaptive UI
function getQuickActions(user: User): Action[] {
  return user.preferences.feature_frequency
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);  // Top 5 most-used
}
```

### Step 4: Preserve User Investment

Every action should leave a trace that adds value:

| User Action | Investment Preserved | How |
|-------------|---------------------|-----|
| View insight | Enriches metadata | View count, last viewed |
| Link insights | Builds knowledge graph | Bidirectional relationships |
| Add note | Personal context | Annotations persist |
| Create tag | Classification scheme | Tag taxonomy grows |
| Save filter | Workflow optimization | Quick filters list |

### Step 5: Graceful Degradation

Old data should remain valuable:

```typescript
// Good: Old format still works
interface InsightV1 {
  id: string;
  title: string;
  content: string;
}

interface InsightV2 extends InsightV1 {
  metadata?: EnrichmentData;  // Additive
}

// Migration enriches, doesn't replace
async function enrichOldInsight(old: InsightV1): Promise<InsightV2> {
  return {
    ...old,
    metadata: await calculateMetadata(old)  // Add value
  };
}
```

## Tests

| Test | Pass Criteria | Fail Criteria |
|------|---------------|---------------|
| **Value Increase** | Data/features more useful after 6 months | Same value as day 1 |
| **User Investment** | Every action leaves valuable trace | Actions are ephemeral |
| **Adaptive UI** | Interface learns user patterns | Static UI regardless of usage |
| **Data Enrichment** | Metadata grows over time | Data degrades or stays static |
| **Graceful Migration** | Old data gains new features | Old data abandoned |

## Anti-Patterns

| Anti-Pattern | Why Wrong | Alternative |
|--------------|-----------|-------------|
| **Streaks/badges** | Artificial engagement, not value | Real usage patterns surfaced |
| **Reset on new version** | Destroys user investment | Migrate and enrich data |
| **Static UI** | Doesn't learn user habits | Adaptive quick access |
| **Ephemeral actions** | No trace of user's work | Every action enriches data |
| **Forced personalization** | Setup burden upfront | Learn from usage automatically |
| **Data rot** | Old data becomes less useful | Old data enriched by new context |

## Examples

### Good Example

```typescript
// Insight service that improves with use
export class InsightsService {
  async getInsight(id: string, userId: string): Promise<Insight> {
    const insight = await this.db.insights.findUnique({ where: { id } });

    // Enrich on access (patina)
    await this.db.insights.update({
      where: { id },
      data: {
        view_count: { increment: 1 },
        last_viewed: new Date(),
        viewers: { connect: { id: userId } }
      }
    });

    // Calculate enriched relationships
    const related = await this.findRelatedInsights(insight, userId);

    return {
      ...insight,
      related,  // Relationships deepen over time
      user_context: await this.getUserContext(insight, userId)
    };
  }

  async getUserQuickActions(userId: string): Promise<Action[]> {
    // UI adapts to user's patterns
    const usage = await this.db.userActions.groupBy({
      by: ['action_type'],
      where: { user_id: userId },
      _count: true,
      orderBy: { _count: { action_type: 'desc' } }
    });

    return usage.slice(0, 5).map(u => this.actions[u.action_type]);
  }

  async addUserNote(insightId: string, userId: string, note: string) {
    // User investment preserved
    await this.db.insightNotes.create({
      data: { insight_id: insightId, user_id: userId, content: note }
    });

    // Note enriches the insight for this user
    await this.reindexInsight(insightId, userId);
  }
}
```

### Bad Example

```typescript
// Static service that doesn't improve
export class InsightsService {
  async getInsight(id: string): Promise<Insight> {
    // No tracking of usage
    // No enrichment
    return await this.db.insights.findUnique({ where: { id } });
  }

  // UI never adapts
  getQuickActions(): Action[] {
    return DEFAULT_ACTIONS;  // Static
  }

  // Data not enriched
  async addTag(insightId: string, tag: string) {
    await this.db.tags.create({ data: { insight_id: insightId, name: tag } });
    // Tag doesn't improve search, relationships, or UI
  }

  // Old data abandoned
  async migrateToV2() {
    await this.db.insights.deleteMany({ where: { version: 1 } });
    // User investment destroyed
  }
}
```

## Implementation Checklist

- [ ] Usage patterns tracked (view count, last accessed, frequency)
- [ ] UI adapts to user's most-used features
- [ ] Every user action enriches data
- [ ] Relationships between entities calculated and surfaced
- [ ] User annotations/notes persist and enrich search
- [ ] Quick access list auto-populated by usage
- [ ] Old data migrated with enrichment, not replacement
- [ ] Metadata grows over time (tags, links, context)
- [ ] Search improves as data enriches
- [ ] No gamification (no streaks, badges, points)


## Quality Tests

### Functional Necessity Test
- Every design element serves a clear purpose
- **PASS:** Each element can be justified by a user need or functional requirement
- **FAIL:** Decorative elements that don't serve function or communication

### Longevity Test
- Design ages gracefully in its intended use context
- **PASS:** Materials and form will look appropriate after years of use
- **FAIL:** Trend-dependent styling that will look dated within 2 years

