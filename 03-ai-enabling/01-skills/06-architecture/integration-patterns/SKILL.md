---
last_updated: 2026-02-25
status: active
name: integration-patterns
description: >-
  Enterprise integration patterns for connecting distributed systems.
  Use when designing system integrations, messaging, ETL pipelines, or API gateways.
triggers:
  files: ["**/integration/**", "**/connectors/**", "**/adapters/**", "**/messaging/**", "**/middleware/**"]
  keywords: ["integration", "enterprise service bus", "message broker", "adapter pattern",
             "middleware", "ETL", "API gateway", "service mesh"]
allowed-tools: Read, Grep, Glob, WebSearch
---

# Integration Patterns

## Overview

Integration patterns provide proven solutions for connecting heterogeneous systems, enabling data flow, and maintaining consistency across distributed architectures. These patterns address challenges in communication, transformation, routing, and orchestration.

## Define Done

- [ ] Integration style selected (messaging, API, event-driven, ETL) with justification
- [ ] Message format and routing patterns defined for each integration point
- [ ] Transformation patterns specified for data format mismatches
- [ ] Error handling strategy documented (dead letter queues, retries, circuit breakers)
- [ ] Anti-patterns identified and avoided in the design

## Quality Tests

### Loose Coupling Test
- Integration design maintains loose coupling between systems
- **PASS:** Systems can be deployed, scaled, and modified independently
- **FAIL:** Changing one system requires coordinated changes in connected systems

### Idempotency Test
- All message handlers are idempotent
- **PASS:** Replaying the same message produces no side effects after the first processing
- **FAIL:** Duplicate messages cause duplicate records, double charges, or inconsistent state

### Failure Isolation Test
- Partial failures don't cascade across the integration
- **PASS:** One downstream system failing doesn't block or crash upstream systems
- **FAIL:** A single service outage causes cascading failures across the integration chain

### Pattern Completeness Test
- All integration points have defined patterns for routing, transformation, and error handling
- **PASS:** Every data flow has a named pattern (e.g., Content-Based Router, Content Enricher, Dead Letter Queue)
- **FAIL:** Integration points rely on ad-hoc, undocumented approaches

## Core Principles

| Principle | Description |
|-----------|-------------|
| Loose Coupling | Systems should interact through well-defined interfaces without internal dependencies |
| Location Transparency | Consumers shouldn't need to know physical location of services |
| Protocol Independence | Support multiple communication protocols through abstraction |
| Reliability | Guarantee message delivery even during partial failures |
| Scalability | Handle increasing load through horizontal scaling |

## Messaging Patterns

### Message Channel Patterns

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| Point-to-Point | One sender, one receiver | Queue-based (SQS, RabbitMQ) |
| Publish-Subscribe | One sender, many receivers | Topic-based (SNS, Kafka) |
| Dead Letter | Failed message handling | Separate queue for failures |
| Request-Reply | Synchronous over async | Correlation IDs |

### Message Construction

```typescript
// Canonical Message Format
interface IntegrationMessage<T> {
  // Header
  messageId: string;
  correlationId?: string;
  timestamp: Date;
  source: string;
  type: string;
  version: string;

  // Routing
  destination?: string;
  replyTo?: string;

  // Payload
  payload: T;

  // Metadata
  metadata: Record<string, string>;
}

// Message Builder
class MessageBuilder<T> {
  private message: Partial<IntegrationMessage<T>> = {};

  withPayload(payload: T): this {
    this.message.payload = payload;
    return this;
  }

  withCorrelationId(id: string): this {
    this.message.correlationId = id;
    return this;
  }

  withType(type: string): this {
    this.message.type = type;
    return this;
  }

  build(): IntegrationMessage<T> {
    return {
      messageId: crypto.randomUUID(),
      timestamp: new Date(),
      source: process.env.SERVICE_NAME!,
      version: '1.0',
      metadata: {},
      ...this.message
    } as IntegrationMessage<T>;
  }
}
```

### Message Routing

| Pattern | Description | Example |
|---------|-------------|---------|
| Content-Based Router | Route based on message content | Order type → fulfillment service |
| Message Filter | Drop unwanted messages | Filter by region |
| Splitter | Break composite into parts | Split batch into items |
| Aggregator | Combine related messages | Collect responses |
| Resequencer | Restore message order | Order by sequence number |

```typescript
// Content-Based Router
class ContentBasedRouter<T> {
  private routes: Map<string, MessageHandler<T>> = new Map();

  addRoute(predicate: string, handler: MessageHandler<T>): void {
    this.routes.set(predicate, handler);
  }

  async route(message: IntegrationMessage<T>): Promise<void> {
    for (const [predicate, handler] of this.routes) {
      if (this.evaluate(message, predicate)) {
        await handler.handle(message);
        return;
      }
    }
    throw new NoMatchingRouteError(message);
  }

  private evaluate(message: IntegrationMessage<T>, predicate: string): boolean {
    // JSONPath or expression evaluation
    return jsonpath.query(message, predicate).length > 0;
  }
}

// Splitter Pattern
class MessageSplitter<T, R> {
  constructor(private splitFn: (payload: T) => R[]) {}

  split(message: IntegrationMessage<T>): IntegrationMessage<R>[] {
    const parts = this.splitFn(message.payload);
    return parts.map((part, index) => ({
      ...message,
      messageId: crypto.randomUUID(),
      correlationId: message.messageId,
      payload: part,
      metadata: {
        ...message.metadata,
        splitIndex: String(index),
        splitTotal: String(parts.length)
      }
    }));
  }
}

// Aggregator Pattern
class MessageAggregator<T, R> {
  private pending: Map<string, T[]> = new Map();

  constructor(
    private completionFn: (messages: T[]) => boolean,
    private aggregateFn: (messages: T[]) => R
  ) {}

  async add(message: IntegrationMessage<T>): Promise<IntegrationMessage<R> | null> {
    const correlationId = message.correlationId!;

    const messages = this.pending.get(correlationId) || [];
    messages.push(message.payload);
    this.pending.set(correlationId, messages);

    if (this.completionFn(messages)) {
      this.pending.delete(correlationId);
      return {
        messageId: crypto.randomUUID(),
        correlationId,
        timestamp: new Date(),
        source: process.env.SERVICE_NAME!,
        type: 'aggregated',
        version: '1.0',
        payload: this.aggregateFn(messages),
        metadata: {}
      };
    }

    return null;
  }
}
```

## Transformation Patterns

### Data Transformation

| Pattern | Purpose | Example |
|---------|---------|---------|
| Message Translator | Convert between formats | XML → JSON |
| Envelope Wrapper | Add/remove wrapper | SOAP envelope |
| Content Enricher | Add missing data | Lookup customer details |
| Content Filter | Remove sensitive data | Strip PII |
| Canonical Data Model | Common format | Enterprise data model |

```typescript
// Message Translator
interface Translator<S, T> {
  translate(source: S): T;
}

class OrderTranslator implements Translator<LegacyOrder, ModernOrder> {
  translate(source: LegacyOrder): ModernOrder {
    return {
      id: source.ORDER_ID,
      customerId: source.CUST_NO,
      items: source.LINE_ITEMS.map(item => ({
        productId: item.PROD_ID,
        quantity: parseInt(item.QTY),
        price: parseFloat(item.PRICE)
      })),
      createdAt: new Date(source.ORDER_DATE)
    };
  }
}

// Content Enricher
class ContentEnricher<T, E> {
  constructor(
    private enrichmentService: (message: T) => Promise<E>,
    private mergeFn: (original: T, enrichment: E) => T
  ) {}

  async enrich(message: IntegrationMessage<T>): Promise<IntegrationMessage<T>> {
    const enrichment = await this.enrichmentService(message.payload);
    return {
      ...message,
      payload: this.mergeFn(message.payload, enrichment)
    };
  }
}

// Canonical Data Model
interface CanonicalCustomer {
  id: string;
  name: string;
  email: string;
  addresses: CanonicalAddress[];
  createdAt: Date;
}

class CustomerCanonicalizer {
  fromSalesforce(sf: SalesforceContact): CanonicalCustomer {
    return {
      id: `sf:${sf.Id}`,
      name: `${sf.FirstName} ${sf.LastName}`,
      email: sf.Email,
      addresses: sf.MailingAddress ? [this.mapAddress(sf.MailingAddress)] : [],
      createdAt: new Date(sf.CreatedDate)
    };
  }

  fromHubspot(hs: HubspotContact): CanonicalCustomer {
    return {
      id: `hs:${hs.vid}`,
      name: hs.properties.name.value,
      email: hs.properties.email.value,
      addresses: [],
      createdAt: new Date(parseInt(hs.properties.createdate.value))
    };
  }
}
```

## Integration Styles

### API Gateway Pattern

```typescript
// API Gateway with rate limiting and transformation
class APIGateway {
  private rateLimiter: RateLimiter;
  private circuitBreaker: CircuitBreaker;
  private cache: Cache;

  async handleRequest(request: GatewayRequest): Promise<GatewayResponse> {
    // Rate limiting
    if (!await this.rateLimiter.allow(request.clientId)) {
      return { status: 429, body: 'Rate limit exceeded' };
    }

    // Check cache
    const cacheKey = this.buildCacheKey(request);
    const cached = await this.cache.get(cacheKey);
    if (cached) return cached;

    // Route to backend
    const backend = this.routeToBackend(request);

    // Circuit breaker
    try {
      const response = await this.circuitBreaker.execute(
        backend.name,
        () => this.callBackend(backend, request)
      );

      // Cache if cacheable
      if (this.isCacheable(request, response)) {
        await this.cache.set(cacheKey, response, backend.cacheTTL);
      }

      return response;
    } catch (error) {
      return this.handleError(error);
    }
  }

  private routeToBackend(request: GatewayRequest): BackendConfig {
    // Path-based routing
    for (const route of this.routes) {
      if (request.path.match(route.pattern)) {
        return route.backend;
      }
    }
    throw new NoRouteError(request.path);
  }
}
```

### Event-Driven Integration

```typescript
// Event Bridge Pattern
class EventBridge {
  private handlers: Map<string, EventHandler[]> = new Map();
  private deadLetterQueue: Queue;

  subscribe(eventType: string, handler: EventHandler): void {
    const handlers = this.handlers.get(eventType) || [];
    handlers.push(handler);
    this.handlers.set(eventType, handlers);
  }

  async publish(event: DomainEvent): Promise<void> {
    const handlers = this.handlers.get(event.type) || [];

    const results = await Promise.allSettled(
      handlers.map(h => this.invokeHandler(h, event))
    );

    // Handle failures
    const failures = results.filter(r => r.status === 'rejected');
    if (failures.length > 0) {
      await this.handleFailures(event, failures);
    }
  }

  private async invokeHandler(
    handler: EventHandler,
    event: DomainEvent
  ): Promise<void> {
    const maxRetries = 3;
    let attempt = 0;

    while (attempt < maxRetries) {
      try {
        await handler.handle(event);
        return;
      } catch (error) {
        attempt++;
        if (attempt >= maxRetries) throw error;
        await this.delay(Math.pow(2, attempt) * 100);
      }
    }
  }
}
```

### Service Mesh Integration

```typescript
// Service Mesh Sidecar Pattern
class ServiceMeshClient {
  private sidecarUrl: string;

  async invoke(service: string, request: ServiceRequest): Promise<ServiceResponse> {
    // All traffic goes through sidecar proxy
    const response = await fetch(`${this.sidecarUrl}/invoke/${service}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': request.requestId,
        'X-Trace-ID': request.traceId
      },
      body: JSON.stringify(request.body)
    });

    return {
      status: response.status,
      body: await response.json(),
      headers: Object.fromEntries(response.headers)
    };
  }
}

// Service Discovery Integration
class ServiceDiscovery {
  private consul: ConsulClient;
  private cache: Map<string, ServiceInstance[]> = new Map();

  async getInstances(serviceName: string): Promise<ServiceInstance[]> {
    // Check cache first
    const cached = this.cache.get(serviceName);
    if (cached) return cached;

    // Query service registry
    const instances = await this.consul.health.service({
      service: serviceName,
      passing: true
    });

    const mapped = instances.map(i => ({
      id: i.Service.ID,
      address: i.Service.Address,
      port: i.Service.Port,
      metadata: i.Service.Meta
    }));

    this.cache.set(serviceName, mapped);
    return mapped;
  }
}
```

## ETL/ELT Patterns

### Extract-Transform-Load

```typescript
// ETL Pipeline
class ETLPipeline<S, T> {
  constructor(
    private extractor: Extractor<S>,
    private transformer: Transformer<S, T>,
    private loader: Loader<T>
  ) {}

  async execute(): Promise<ETLResult> {
    const result: ETLResult = {
      extracted: 0,
      transformed: 0,
      loaded: 0,
      errors: []
    };

    // Extract in batches
    for await (const batch of this.extractor.extract()) {
      result.extracted += batch.length;

      // Transform
      const transformed: T[] = [];
      for (const record of batch) {
        try {
          transformed.push(await this.transformer.transform(record));
          result.transformed++;
        } catch (error) {
          result.errors.push({ record, error });
        }
      }

      // Load
      await this.loader.load(transformed);
      result.loaded += transformed.length;
    }

    return result;
  }
}

// Change Data Capture
class CDCConnector {
  private position: string;

  async *captureChanges(): AsyncGenerator<ChangeEvent> {
    while (true) {
      const changes = await this.fetchChanges(this.position);

      for (const change of changes) {
        yield {
          table: change.table,
          operation: change.op, // INSERT, UPDATE, DELETE
          before: change.before,
          after: change.after,
          timestamp: new Date(change.ts_ms)
        };

        this.position = change.position;
      }

      await this.checkpoint(this.position);
      await this.delay(100);
    }
  }
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Point-to-Point Spaghetti | Tight coupling, unmanageable | Use message broker or ESB |
| Shared Database | Hidden coupling | Use APIs or events |
| Synchronous Chains | Cascading failures | Use async messaging |
| Big Bang Integration | All-or-nothing risk | Incremental integration |
| Ignoring Idempotency | Duplicate processing | Design idempotent handlers |

## Integration Testing

```typescript
// Integration Test with Testcontainers
describe('Order Integration', () => {
  let kafka: StartedKafkaContainer;
  let postgres: StartedPostgreSQLContainer;

  beforeAll(async () => {
    kafka = await new KafkaContainer().start();
    postgres = await new PostgreSQLContainer().start();
  });

  afterAll(async () => {
    await kafka.stop();
    await postgres.stop();
  });

  it('should process order through integration pipeline', async () => {
    // Arrange
    const producer = kafka.getProducer();
    const order = createTestOrder();

    // Act
    await producer.send({
      topic: 'orders',
      messages: [{ value: JSON.stringify(order) }]
    });

    // Assert - wait for downstream effect
    await waitFor(async () => {
      const result = await postgres.query(
        'SELECT * FROM processed_orders WHERE id = $1',
        [order.id]
      );
      expect(result.rows).toHaveLength(1);
    });
  });
});
```

## Technology Selection

| Requirement | Technology Options |
|-------------|-------------------|
| Message Queue | RabbitMQ, Amazon SQS, Azure Service Bus |
| Event Streaming | Apache Kafka, Amazon Kinesis, Pulsar |
| API Gateway | Kong, AWS API Gateway, Apigee |
| Service Mesh | Istio, Linkerd, Consul Connect |
| ETL/ELT | Apache Airflow, dbt, Fivetran |
| iPaaS | MuleSoft, Boomi, Workato |

## References

| Resource | Description |
|----------|-------------|
| Enterprise Integration Patterns | Hohpe & Woolf's canonical reference |
| Designing Data-Intensive Applications | Kleppmann on distributed systems |
| Building Event-Driven Microservices | Bellemare on event architecture |
| Apache Kafka Documentation | Event streaming reference |
