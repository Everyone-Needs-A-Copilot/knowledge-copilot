---
last_updated: 2026-02-25
status: active
name: diagram-creation
description: Technical diagrams - Mermaid, PlantUML, sequence diagrams, flowcharts. Use for creating diagrams in documentation.
triggers:
  files: ["**/docs/**", "**/*.md", "**/diagrams/**"]
  keywords: ["diagram", "mermaid", "flowchart", "sequence diagram", "architecture diagram", "PlantUML", "visualization"]
allowed-tools: Read, Write, Edit
---

# Diagram Creation Skill

Create clear, maintainable technical diagrams using text-based tools like Mermaid and PlantUML. Diagrams that live in version control with your code.

---

## Core Principles

### Why Text-Based Diagrams

| Benefit | Description |
|---------|-------------|
| **Version control** | Track changes, review in PRs |
| **Maintenance** | Edit text, not drag-and-drop |
| **Consistency** | Same styling across diagrams |
| **Automation** | Generate from code/data |
| **Portability** | Render in GitHub, GitLab, docs sites |

### Diagram Selection Guide

| Diagram Type | Use When |
|--------------|----------|
| **Flowchart** | Decision logic, processes |
| **Sequence** | Time-ordered interactions |
| **Class/ER** | Data structures, relationships |
| **State** | State machines, lifecycles |
| **Architecture** | System components, deployment |
| **Gantt** | Timelines, schedules |

---


## Define Done

- [ ] Documentation answers the reader's most likely questions
- [ ] Structure follows a logical flow (concept → usage → reference)
- [ ] Code examples are tested and runnable
- [ ] Kept in sync with the code it documents

## Mermaid Diagrams

### Flowcharts

```markdown
```mermaid
flowchart TD
    A[Start] --> B{Is valid?}
    B -->|Yes| C[Process]
    B -->|No| D[Error]
    C --> E[Save]
    E --> F[End]
    D --> F
```
```

**Rendered:**

```mermaid
flowchart TD
    A[Start] --> B{Is valid?}
    B -->|Yes| C[Process]
    B -->|No| D[Error]
    C --> E[Save]
    E --> F[End]
    D --> F
```

**Node Shapes:**

| Shape | Syntax | Use For |
|-------|--------|---------|
| Rectangle | `[text]` | Process/action |
| Rounded | `(text)` | Start/end |
| Diamond | `{text}` | Decision |
| Circle | `((text))` | Connector |
| Parallelogram | `[/text/]` | Input/output |

**Direction:**
- `TD` = Top to Down
- `LR` = Left to Right
- `BT` = Bottom to Top
- `RL` = Right to Left

### Sequence Diagrams

```markdown
```mermaid
sequenceDiagram
    participant U as User
    participant A as API
    participant D as Database

    U->>A: POST /topics
    A->>D: INSERT topic
    D-->>A: topic_id
    A-->>U: 201 Created
```
```

**Arrow Types:**

| Arrow | Syntax | Meaning |
|-------|--------|---------|
| Solid line | `->` | Sync call |
| Dashed line | `-->` | Response |
| Solid arrow | `->>` | Async call |
| Dashed arrow | `-->>` | Async response |

**Advanced Features:**

```mermaid
sequenceDiagram
    participant U as User
    participant A as API
    participant L as LLM

    U->>A: Crystallize topic

    rect rgb(240, 240, 240)
        Note over A,L: Phase 1: Synthesis
        A->>L: Generate concepts
        L-->>A: Concepts
    end

    alt Success
        A-->>U: 200 OK
    else Failure
        A-->>U: 500 Error
    end
```

### Class Diagrams

```markdown
```mermaid
classDiagram
    class Topic {
        +String id
        +String title
        +Status status
        +crystallize()
    }

    class Evidence {
        +String id
        +String content
        +Float score
    }

    class Concept {
        +String title
        +String definition
    }

    Topic "1" --> "*" Evidence : uses
    Topic "1" --> "*" Concept : has
```
```

### Entity Relationship Diagrams

```markdown
```mermaid
erDiagram
    TOPIC ||--o{ CONCEPT : has
    TOPIC ||--o{ EVIDENCE : uses
    CONCEPT ||--o{ EVIDENCE : supports
    USER ||--o{ TOPIC : owns

    TOPIC {
        uuid id PK
        string title
        enum status
        timestamp created_at
    }

    EVIDENCE {
        uuid id PK
        uuid topic_id FK
        string content
        float score
    }
```
```

### State Diagrams

```markdown
```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Discovering : start_discovery
    Discovering --> Candidate : evidence_found
    Candidate --> Crystallizing : start_crystallization
    Crystallizing --> Crystallized : complete
    Crystallizing --> Failed : error

    Crystallized --> Archived : archive
    Failed --> Draft : retry
    Archived --> [*]
```
```

### Architecture Diagrams

```markdown
```mermaid
graph TB
    subgraph Frontend
        WEB[Web App]
    end

    subgraph Backend
        API[API Server]
        WORKER[Worker]
    end

    subgraph Data
        PG[(PostgreSQL)]
        QD[(Qdrant)]
        RD[(Redis)]
    end

    WEB --> API
    API --> PG
    API --> QD
    API --> RD
    WORKER --> PG
    WORKER --> QD
```
```

### Gantt Charts

```markdown
```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1
    Research           :a1, 2024-01-01, 14d
    Design             :a2, after a1, 7d
    section Phase 2
    Implementation     :b1, after a2, 21d
    Testing            :b2, after b1, 14d
```
```

---

## PlantUML

### When to Use PlantUML

- More complex UML diagrams
- Enterprise architecture (C4, ArchiMate)
- Precise control over layout
- Batch diagram generation

### Sequence Diagram

```plantuml
@startuml
actor User
participant "API" as api
database "Database" as db

User -> api: POST /topics
activate api
api -> db: INSERT
db --> api: topic_id
api --> User: 201 Created
deactivate api
@enduml
```

### Component Diagram

```plantuml
@startuml
package "Frontend" {
    [Web App] as web
}

package "Backend" {
    [API Server] as api
    [Worker] as worker
}

database "PostgreSQL" as pg
database "Qdrant" as qdrant

web --> api : REST
api --> pg : SQL
api --> qdrant : Vector Search
worker --> pg : SQL
@enduml
```

### C4 Diagrams

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(user, "Analyst", "Strategic researcher")
System_Boundary(system, "Insights Copilot") {
    Container(web, "Web App", "Next.js", "Admin interface")
    Container(api, "API", "FastAPI", "Business logic")
    ContainerDb(db, "Database", "PostgreSQL", "Primary data")
    ContainerDb(vector, "Vector DB", "Qdrant", "Embeddings")
}

Rel(user, web, "Uses", "HTTPS")
Rel(web, api, "Calls", "REST")
Rel(api, db, "Reads/writes", "SQL")
Rel(api, vector, "Searches", "gRPC")
@enduml
```

---

## ASCII Diagrams

### When to Use ASCII

- Terminal/CLI documentation
- Environments without Mermaid support
- Inline code comments
- Maximum portability

### Box Drawing

```
┌─────────────┐     ┌─────────────┐
│   Client    │────▶│    API      │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Database   │
                    └─────────────┘
```

### Flow Diagram

```
Input ──▶ Validate ──▶ Process ──▶ Output
              │
              ▼
           Error
```

### Box Characters

```
Single line: ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
Double line: ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬
Arrows:      ▶ ◀ ▲ ▼ → ← ↑ ↓
```

---

## Diagram Best Practices

### Keep It Simple

```mermaid
%% Bad: Too much detail
flowchart TD
    A[Receive Request] --> B[Parse JSON]
    B --> C[Validate Schema]
    C --> D[Check Auth Token]
    D --> E[Verify Permissions]
    E --> F[Load from Cache]
    F --> G[Query Database]
    G --> H[Transform Response]
    H --> I[Serialize JSON]
    I --> J[Send Response]
```

```mermaid
%% Good: Key steps only
flowchart TD
    A[Request] --> B[Validate]
    B --> C[Process]
    C --> D[Response]
```

### Use Subgraphs for Grouping

```mermaid
flowchart TB
    subgraph Client
        A[Browser]
    end

    subgraph Server
        B[API]
        C[Worker]
    end

    subgraph Data
        D[(Database)]
    end

    A --> B
    B --> D
    C --> D
```

### Consistent Styling

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f0f0'}}}%%
flowchart LR
    A[Step 1] --> B[Step 2] --> C[Step 3]
```

### Add Context

Always accompany diagrams with explanatory text:

```markdown
## System Architecture

The system consists of three main components:

```mermaid
graph TB
    A[Frontend] --> B[API]
    B --> C[Database]
```

- **Frontend**: Next.js application serving the admin interface
- **API**: FastAPI server handling business logic
- **Database**: PostgreSQL storing topics, evidence, and users
```

---

## Common Diagram Patterns

### Request/Response Flow

```mermaid
sequenceDiagram
    Client->>+API: Request
    API->>+Service: Process
    Service->>+DB: Query
    DB-->>-Service: Data
    Service-->>-API: Result
    API-->>-Client: Response
```

### Error Handling Flow

```mermaid
flowchart TD
    A[Start] --> B{Valid?}
    B -->|Yes| C[Process]
    B -->|No| D[Log Error]
    C --> E{Success?}
    E -->|Yes| F[Return Result]
    E -->|No| G[Rollback]
    D --> H[Return Error]
    G --> H
```

### State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : submit
    Processing --> Success : complete
    Processing --> Failed : error
    Failed --> Idle : reset
    Success --> [*]
```

### Deployment Topology

```mermaid
graph TB
    subgraph Cloud
        LB[Load Balancer]
        subgraph App Tier
            A1[API 1]
            A2[API 2]
        end
        subgraph Data Tier
            DB[(Primary DB)]
            DBR[(Replica)]
        end
    end

    LB --> A1
    LB --> A2
    A1 --> DB
    A2 --> DB
    DB --> DBR
```

---

## Tools and Rendering

### Mermaid Support

| Platform | Support |
|----------|---------|
| GitHub | Native in markdown |
| GitLab | Native in markdown |
| Notion | Via embed |
| VS Code | With extension |
| Docusaurus | Native plugin |
| MkDocs | With plugin |

### PlantUML Support

| Tool | Usage |
|------|-------|
| PlantUML Server | Self-host or public |
| VS Code | With extension |
| IntelliJ | Built-in |
| Confluence | Plugin available |

### Export Options

- PNG: For documentation, presentations
- SVG: For scalable web embedding
- PDF: For print materials

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Too detailed** | Overwhelming, unreadable | Show key steps only |
| **No legend** | Unclear what shapes mean | Add explanatory text |
| **Outdated** | Misleads readers | Update with code changes |
| **Image-only** | Can't edit, version | Use text-based format |
| **Inconsistent** | Confusing across docs | Use style guide |
| **No context** | Diagram alone is ambiguous | Add explanatory paragraphs |

---

## Checklist

Before publishing diagrams:

- [ ] Diagram type matches content (flow for process, sequence for interactions)
- [ ] Key components labeled clearly
- [ ] Not overly detailed (can understand in 30 seconds)
- [ ] Accompanied by explanatory text
- [ ] Uses consistent styling
- [ ] Text-based format (Mermaid/PlantUML)
- [ ] Renders correctly in target platform
- [ ] Accessible (alt text if image export)

---

This skill enables clear, maintainable technical diagrams that enhance documentation and live alongside your code.


## Quality Tests

### Accuracy Test
- All code examples and commands actually work
- **PASS:** Copy-pasting any code block produces the described result
- **FAIL:** Examples are outdated or have syntax errors

### Findability Test
- Readers can find what they need within 30 seconds
- **PASS:** Clear headings, table of contents, and search-friendly terms
- **FAIL:** Important information buried in paragraphs without clear headings

