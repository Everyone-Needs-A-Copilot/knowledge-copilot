---
last_updated: 2026-02-25
status: active
name: event-driven-architecture
description: Patterns for building systems that communicate through events. Use for asynchronous processing, decoupled services, and real-time data flows.
triggers:
  files: ["**/events/**", "**/messaging/**", "**/kafka/**", "**/rabbitmq/**", "**/pubsub/**"]
  keywords: ["event-driven", "event sourcing", "CQRS", "message broker", "pub/sub", "Kafka", "RabbitMQ", "event bus", "domain event", "event streaming", "async", "eventual consistency"]
allowed-tools: Read, Write, Edit
---

# Event-Driven Architecture

## Overview

Event-Driven Architecture (EDA) is a software design pattern where the flow of the program is determined by events—significant changes in state that the system cares about. Instead of direct calls between components, producers emit events that are consumed by interested parties.

EDA enables loose coupling, scalability, and real-time responsiveness. Components don't need to know about each other; they only need to know about events. This makes systems more resilient, extensible, and easier to evolve.

This skill covers event design, messaging patterns, event sourcing, CQRS, and operational considerations for event-driven systems.


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Concepts

### What is an Event?

An event is a record of something that happened—a fact about the past that cannot be changed.

**Characteristics of events:**
- **Immutable**: Events are facts; they cannot be modified
- **Past tense**: Named for what happened (OrderPlaced, not PlaceOrder)
- **Self-contained**: Include all relevant data
- **Timestamped**: When did it happen?

**Event structure:**
```python
@dataclass(frozen=True)  # Immutable
class OrderPlaced:
    event_id: UUID
    event_type: str = "OrderPlaced"
    occurred_at: datetime
    aggregate_id: UUID  # order_id

    # Event payload
    customer_id: UUID
    items: List[OrderItem]
    total_amount: Money
    shipping_address: Address
```

**Commands vs Events:**
| Commands | Events |
|----------|--------|
| Request to do something | Record of what happened |
| Imperative (PlaceOrder) | Past tense (OrderPlaced) |
| Can be rejected | Already happened |
| One recipient | Many subscribers |

### Event Types

**Domain Events:**
Business-relevant state changes within a bounded context.
```
OrderPlaced, PaymentReceived, ShipmentDispatched
```

**Integration Events:**
Events published for external systems to consume.
```
CustomerCreated (for CRM sync), InventoryLow (for alerting)
```

**System Events:**
Infrastructure-level events.
```
ServiceStarted, ConfigurationChanged, HealthCheckFailed
```

### Event Flow

```
┌──────────────┐    event    ┌──────────────┐    event    ┌──────────────┐
│   Producer   │────────────►│ Event Broker │────────────►│   Consumer   │
│              │             │   (Topic)    │             │              │
└──────────────┘             └──────────────┘             └──────────────┘
                                    │
                                    │ event
                                    ▼
                             ┌──────────────┐
                             │  Consumer 2  │
                             └──────────────┘
```

---

## Messaging Patterns

### Point-to-Point (Queues)

One producer, one consumer per message.

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│   Producer   │───►│     Queue       │───►│   Consumer   │
│              │    │  ┌───┬───┬───┐  │    │              │
└──────────────┘    │  │ M │ M │ M │  │    └──────────────┘
                    │  └───┴───┴───┘  │
                    └─────────────────┘
```

**Use cases:**
- Task distribution (work queues)
- Load leveling
- Reliable delivery

**Example:**
```python
# Producer
queue.send(ProcessImageTask(image_id="123", operation="resize"))

# Consumer (worker)
while True:
    task = queue.receive()
    process_image(task.image_id, task.operation)
    queue.acknowledge(task)
```

### Publish-Subscribe (Topics)

One producer, multiple consumers receive same message.

```
                                ┌──────────────┐
                           ────►│  Consumer 1  │
┌──────────────┐    ┌─────┴─────┐    └──────────────┘
│   Publisher  │───►│   Topic   │
│              │    └─────┬─────┘    ┌──────────────┐
└──────────────┘         ────────────►│  Consumer 2  │
                                     └──────────────┘
```

**Use cases:**
- Event broadcasting
- Notifications
- Cache invalidation
- Analytics

**Example:**
```python
# Publisher
event_bus.publish("orders", OrderPlaced(order_id="123", ...))

# Subscriber 1: Inventory
@subscribe("orders", event_type=OrderPlaced)
def reserve_inventory(event: OrderPlaced):
    for item in event.items:
        inventory.reserve(item.product_id, item.quantity)

# Subscriber 2: Notifications
@subscribe("orders", event_type=OrderPlaced)
def send_confirmation(event: OrderPlaced):
    email.send_order_confirmation(event.customer_id, event.order_id)
```

### Request-Reply

Async request with correlated response.

```
┌──────────────┐  request   ┌─────────────┐  request   ┌──────────────┐
│   Requester  │───────────►│ Request Q   │───────────►│   Responder  │
│              │            └─────────────┘            │              │
│              │  response  ┌─────────────┐  response  │              │
│              │◄───────────┤ Response Q  │◄───────────┤              │
└──────────────┘            └─────────────┘            └──────────────┘
```

**Correlation ID pattern:**
```python
# Requester
correlation_id = str(uuid4())
request_queue.send(
    GetPriceRequest(product_id="123"),
    headers={"correlation_id": correlation_id, "reply_to": "price-responses"}
)
response = response_queue.receive(correlation_id=correlation_id, timeout=5.0)

# Responder
@consume("price-requests")
def handle_price_request(message):
    price = pricing_service.get_price(message.body.product_id)
    reply_queue = message.headers["reply_to"]
    message_bus.send(
        reply_queue,
        GetPriceResponse(price=price),
        headers={"correlation_id": message.headers["correlation_id"]}
    )
```

### Event Streaming

Continuous flow of events, processed in order.

```
Producer ──► [E1, E2, E3, E4, E5, ...] ──► Consumer
                    (ordered stream)
```

**Characteristics:**
- Events retained for replay
- Consumers track their position (offset)
- Enables event sourcing

**Example (Kafka):**
```python
# Producer
producer.send("order-events", key=order_id, value=OrderPlaced(...))

# Consumer
consumer = KafkaConsumer("order-events", group_id="inventory-service")
for message in consumer:
    event = deserialize(message.value)
    handle_event(event)
    consumer.commit()
```

---

## Event Sourcing

Store state as a sequence of events rather than current state.

### Traditional vs Event Sourcing

**Traditional (state-based):**
```sql
-- Current state only
UPDATE accounts SET balance = 150 WHERE id = 123;

-- What happened? We don't know.
```

**Event Sourcing:**
```
Events:
1. AccountCreated(id=123, initial_balance=0)
2. MoneyDeposited(id=123, amount=200)
3. MoneyWithdrawn(id=123, amount=50)

Current State (derived): balance = 150

-- Full history preserved!
```

### Event Store

```
┌────────────────────────────────────────────────────────┐
│                    Event Store                          │
├──────────┬──────────┬─────────────────────┬────────────┤
│ Event ID │ Sequence │ Event Type          │ Payload    │
├──────────┼──────────┼─────────────────────┼────────────┤
│ e001     │ 1        │ AccountCreated      │ {id: 123}  │
│ e002     │ 2        │ MoneyDeposited      │ {amt: 200} │
│ e003     │ 3        │ MoneyWithdrawn      │ {amt: 50}  │
└──────────┴──────────┴─────────────────────┴────────────┘
```

### Aggregate Reconstruction

```python
class Account:
    def __init__(self, account_id: UUID):
        self.id = account_id
        self.balance = 0
        self.status = "pending"

    # Event handlers for reconstruction
    def apply(self, event):
        if isinstance(event, AccountCreated):
            self.status = "active"
        elif isinstance(event, MoneyDeposited):
            self.balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount


class AccountRepository:
    def get(self, account_id: UUID) -> Account:
        events = self.event_store.get_events(aggregate_id=account_id)
        account = Account(account_id)
        for event in events:
            account.apply(event)
        return account
```

### Commands and Events

```python
class Account:
    def deposit(self, amount: Money) -> List[DomainEvent]:
        """Command handler: validates and returns events."""
        if amount <= 0:
            raise InvalidAmountError()
        if self.status != "active":
            raise AccountNotActiveError()

        return [MoneyDeposited(
            aggregate_id=self.id,
            amount=amount,
            occurred_at=datetime.now()
        )]

    def withdraw(self, amount: Money) -> List[DomainEvent]:
        if amount > self.balance:
            raise InsufficientFundsError()

        return [MoneyWithdrawn(
            aggregate_id=self.id,
            amount=amount,
            occurred_at=datetime.now()
        )]


# Usage
def handle_deposit(command: DepositMoney):
    account = repository.get(command.account_id)
    events = account.deposit(command.amount)
    for event in events:
        account.apply(event)  # Update in-memory state
    event_store.append(events)  # Persist events
```

### Snapshots

Optimization for aggregates with many events.

```
┌────────────────────────────────────────────────────────────┐
│ Account 123 Event Stream                                    │
├──────────────────────────────────────────────────────────────┤
│ [E1, E2, E3, ..., E999, E1000, SNAPSHOT, E1001, E1002, ...] │
│                              ▲                               │
│                     Snapshot at event 1000:                 │
│                     {balance: 5000, status: active}         │
└────────────────────────────────────────────────────────────┘

Reconstruction:
1. Load latest snapshot (event 1000)
2. Apply only events after snapshot (E1001, E1002, ...)
```

```python
class AccountRepository:
    def get(self, account_id: UUID) -> Account:
        snapshot = self.snapshot_store.get_latest(account_id)

        if snapshot:
            account = Account.from_snapshot(snapshot)
            events = self.event_store.get_events(
                aggregate_id=account_id,
                after_sequence=snapshot.sequence
            )
        else:
            account = Account(account_id)
            events = self.event_store.get_events(aggregate_id=account_id)

        for event in events:
            account.apply(event)

        # Create snapshot if too many events since last snapshot
        if len(events) > 100:
            self.snapshot_store.save(account.to_snapshot())

        return account
```

### Benefits of Event Sourcing

| Benefit | Description |
|---------|-------------|
| Complete audit trail | Every change recorded |
| Time travel | Reconstruct state at any point |
| Debugging | Replay events to reproduce issues |
| New projections | Derive new read models from existing events |
| Event replay | Reprocess events when logic changes |

### Challenges

| Challenge | Mitigation |
|-----------|------------|
| Storage growth | Snapshots, archiving old events |
| Event schema evolution | Versioning, upcasters |
| Complexity | Use only where audit/history needed |
| Query performance | CQRS with denormalized read models |

---

## CQRS (Command Query Responsibility Segregation)

Separate read and write models.

### Architecture

```
                    Commands                     Queries
                        │                           │
                        ▼                           ▼
               ┌────────────────┐         ┌────────────────┐
               │ Command Handler│         │ Query Handler  │
               └───────┬────────┘         └───────┬────────┘
                       │                          │
                       ▼                          ▼
               ┌────────────────┐         ┌────────────────┐
               │  Write Model   │         │   Read Model   │
               │  (Domain)      │         │  (Projections) │
               └───────┬────────┘         └───────┬────────┘
                       │                          │
                       ▼                          ▼
               ┌────────────────┐         ┌────────────────┐
               │  Event Store   │────────►│  Read Database │
               │  (PostgreSQL)  │ events  │  (Elasticsearch│
               └────────────────┘         │   /Redis)      │
                                          └────────────────┘
```

### Write Side (Commands)

```python
# Command
@dataclass
class PlaceOrder:
    customer_id: UUID
    items: List[OrderItem]
    shipping_address: Address

# Command Handler
class PlaceOrderHandler:
    def handle(self, command: PlaceOrder) -> UUID:
        # Load aggregate
        order = Order.create(
            customer_id=command.customer_id,
            items=command.items,
            shipping_address=command.shipping_address
        )

        # Persist events
        events = order.get_uncommitted_events()
        self.event_store.append(order.id, events)

        # Publish events for projections
        for event in events:
            self.event_bus.publish(event)

        return order.id
```

### Read Side (Queries)

```python
# Query
@dataclass
class GetOrderSummary:
    order_id: UUID

# Query Handler
class GetOrderSummaryHandler:
    def handle(self, query: GetOrderSummary) -> OrderSummaryDTO:
        # Read from optimized projection
        return self.order_summary_projection.get(query.order_id)

# Projection (event handler that builds read model)
class OrderSummaryProjection:
    def __init__(self, read_db):
        self.db = read_db

    @subscribe(OrderPlaced)
    def on_order_placed(self, event: OrderPlaced):
        self.db.insert("order_summaries", {
            "order_id": event.order_id,
            "customer_name": event.customer_name,
            "total": event.total_amount,
            "item_count": len(event.items),
            "status": "placed",
            "created_at": event.occurred_at
        })

    @subscribe(OrderShipped)
    def on_order_shipped(self, event: OrderShipped):
        self.db.update("order_summaries",
            where={"order_id": event.order_id},
            set={"status": "shipped", "shipped_at": event.occurred_at}
        )
```

### Multiple Projections

Same events can build different read models.

```
                    Events
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Order List   │ │ Order Stats  │ │ Search Index │
│ Projection   │ │ Projection   │ │ Projection   │
│ (for UI)     │ │ (for reports)│ │ (for search) │
└──────────────┘ └──────────────┘ └──────────────┘
        │              │              │
        ▼              ▼              ▼
   PostgreSQL    TimescaleDB    Elasticsearch
```

### Benefits of CQRS

| Benefit | Description |
|---------|-------------|
| Optimized reads | Read models designed for specific queries |
| Scalability | Scale reads independently from writes |
| Simplicity | Queries don't need complex joins |
| Flexibility | Add new read models without changing domain |

---

## Event Design

### Event Naming

**Good names (past tense, domain language):**
```
OrderPlaced
PaymentAuthorized
ShipmentDispatched
CustomerAddressChanged
```

**Bad names:**
```
CreateOrder       (command, not event)
OrderCreation     (noun, unclear when)
Order             (too vague)
HandleOrder       (action, not fact)
```

### Event Payload Design

**Include enough data to be useful:**
```python
# BAD: Too little data
@dataclass
class OrderPlaced:
    order_id: UUID
    # Consumers must call Order Service to get details

# GOOD: Self-contained
@dataclass
class OrderPlaced:
    order_id: UUID
    customer_id: UUID
    customer_email: str  # For notifications
    items: List[OrderItem]
    total_amount: Money
    shipping_address: Address
    occurred_at: datetime
```

**But avoid over-inclusion:**
```python
# BAD: Too much (privacy, coupling)
@dataclass
class OrderPlaced:
    customer_ssn: str  # Sensitive!
    customer_credit_score: int  # Not relevant
    internal_pricing_rules: dict  # Implementation detail
```

### Event Versioning

Events evolve; handle schema changes gracefully.

**Versioning strategies:**

**1. Event type versioning:**
```python
@dataclass
class OrderPlacedV1:
    order_id: UUID
    customer_id: UUID
    total: float

@dataclass
class OrderPlacedV2:
    order_id: UUID
    customer_id: UUID
    total: Money  # Changed to value object
    items: List[OrderItem]  # Added field
```

**2. Upcasting (transform old to new):**
```python
class EventUpcaster:
    def upcast(self, event: dict, version: int) -> dict:
        if event["type"] == "OrderPlaced":
            if version == 1:
                # V1 -> V2: Convert float to Money, add empty items
                event["payload"]["total"] = Money(
                    amount=int(event["payload"]["total"] * 100),
                    currency="USD"
                )
                event["payload"]["items"] = []
                version = 2
        return event
```

**3. Tolerant reader:**
```python
def deserialize_order_placed(data: dict) -> OrderPlaced:
    return OrderPlaced(
        order_id=UUID(data["order_id"]),
        customer_id=UUID(data["customer_id"]),
        total=data.get("total", Money(0, "USD")),
        items=data.get("items", [])  # Handle missing field
    )
```

### Event Ordering

**Within an aggregate:** Events must be ordered (sequence numbers).
```
Account 123:
  Seq 1: AccountCreated
  Seq 2: MoneyDeposited
  Seq 3: MoneyWithdrawn
```

**Across aggregates:** Often no guarantee; design for it.
```
# These may arrive out of order
OrderPlaced (Order aggregate)
InventoryReserved (Inventory aggregate)
```

**Handling out-of-order events:**
```python
class InventoryProjection:
    def handle(self, event):
        if isinstance(event, InventoryReserved):
            if not self.order_exists(event.order_id):
                # Order event not yet processed
                self.pending_reservations.add(event)
                return

        if isinstance(event, OrderPlaced):
            # Process any pending reservations for this order
            pending = self.pending_reservations.get(event.order_id)
            if pending:
                self.process_reservation(pending)
```

---

## Message Delivery Guarantees

### At-Most-Once

Message may be lost but never duplicated.

```
Producer ──► Broker ──► Consumer
               │
          (may drop)
```

**Use when:** Losing some messages is acceptable (metrics, logs).

### At-Least-Once

Message will be delivered but may be duplicated.

```
Producer ──► Broker ──► Consumer
               │           │
          (will retry) (may receive twice)
```

**Use when:** Can't lose messages; consumers must be idempotent.

**Idempotent consumer:**
```python
class OrderEventHandler:
    def handle(self, event: OrderPlaced):
        # Check if already processed
        if self.processed_events.contains(event.event_id):
            return  # Already handled

        # Process event
        self.reserve_inventory(event)

        # Mark as processed
        self.processed_events.add(event.event_id)
```

### Exactly-Once

Message delivered exactly once (hard to achieve).

**Approaches:**
1. **Idempotent operations**: At-least-once + idempotency = exactly-once effect
2. **Transactional outbox**: Combine database write + message send in transaction
3. **Deduplication**: Broker-level deduplication (Kafka exactly-once)

---

## Transactional Outbox Pattern

Ensure events are published reliably without distributed transactions.

### The Problem

```python
# BROKEN: Not atomic
def place_order(order: Order):
    database.save(order)     # Step 1: DB write
    event_bus.publish(OrderPlaced(order))  # Step 2: Publish
    # If step 2 fails, order exists but event never sent
```

### The Solution

```
┌────────────────────────────────────────────────────────┐
│                    Database Transaction                 │
│  ┌──────────────┐          ┌──────────────────────┐   │
│  │    Orders    │          │   Outbox Table       │   │
│  │ ┌──────────┐ │          │ ┌──────────────────┐ │   │
│  │ │  Order   │ │          │ │ Event (unpublished)│ │  │
│  │ └──────────┘ │          │ └──────────────────┘ │   │
│  └──────────────┘          └──────────────────────┘   │
└────────────────────────────────────────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │   Outbox Publisher      │
                         │   (separate process)    │
                         └────────────┬────────────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │  Event Bus   │
                              └──────────────┘
```

**Implementation:**
```python
# Step 1: Write both in same transaction
def place_order(order: Order):
    with database.transaction():
        database.save(order)
        database.save(OutboxEvent(
            id=uuid4(),
            aggregate_type="Order",
            aggregate_id=order.id,
            event_type="OrderPlaced",
            payload=serialize(OrderPlaced(order)),
            created_at=datetime.now()
        ))

# Step 2: Separate process publishes events
class OutboxPublisher:
    def run(self):
        while True:
            events = database.query(
                "SELECT * FROM outbox WHERE published_at IS NULL"
            )
            for event in events:
                event_bus.publish(event.event_type, event.payload)
                database.update(
                    "outbox",
                    where={"id": event.id},
                    set={"published_at": datetime.now()}
                )
            sleep(100)  # Poll interval
```

**CDC (Change Data Capture) alternative:**
```
┌──────────────┐       ┌───────────────┐       ┌──────────────┐
│   Database   │──────►│   Debezium    │──────►│    Kafka     │
│ (transaction │  CDC  │ (captures     │       │  (events)    │
│    log)      │       │  changes)     │       │              │
└──────────────┘       └───────────────┘       └──────────────┘
```

---

## Saga Pattern

Manage distributed transactions across services using events.

### Choreography (Event-Based)

Services react to events; no central coordinator.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Event Flow                                │
│                                                                  │
│  Order Service          Inventory           Payment             │
│       │                    │                   │                │
│       │ OrderCreated       │                   │                │
│       │───────────────────►│                   │                │
│       │                    │ InventoryReserved │                │
│       │                    │──────────────────►│                │
│       │                    │                   │ PaymentCompleted│
│       │◄───────────────────│◄──────────────────│                │
│       │                    │                   │                │
│       │ OrderConfirmed     │                   │                │
│       │                    │                   │                │
└─────────────────────────────────────────────────────────────────┘
```

**Compensation on failure:**
```
If PaymentFailed:
  Inventory publishes: InventoryReleased
  Order publishes: OrderCancelled
```

**Implementation:**
```python
# Order Service
@subscribe(PaymentCompleted)
def on_payment_completed(event: PaymentCompleted):
    order = order_repository.get(event.order_id)
    order.confirm()
    event_bus.publish(OrderConfirmed(order_id=order.id))

@subscribe(PaymentFailed)
def on_payment_failed(event: PaymentFailed):
    order = order_repository.get(event.order_id)
    order.cancel(reason=event.reason)
    event_bus.publish(OrderCancelled(order_id=order.id, reason=event.reason))

# Inventory Service
@subscribe(OrderCancelled)
def on_order_cancelled(event: OrderCancelled):
    inventory.release(event.order_id)
    event_bus.publish(InventoryReleased(order_id=event.order_id))
```

### Orchestration (Coordinator-Based)

Central coordinator directs the saga.

```
┌────────────────────────────────────────────────────────────────┐
│                    Saga Orchestrator                            │
│                                                                 │
│  State: [STARTED] ─► [INVENTORY_RESERVED] ─► [PAYMENT_DONE]    │
│                          ─► [COMPLETED]                        │
│                                                                 │
│  1. Command: ReserveInventory ──────► Inventory Service        │
│  2. Event: InventoryReserved ◄────────                         │
│  3. Command: ProcessPayment ────────► Payment Service          │
│  4. Event: PaymentCompleted ◄─────────                         │
│  5. Command: ConfirmOrder ──────────► Order Service            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**Implementation:**
```python
class PlaceOrderSaga:
    def __init__(self):
        self.state = "STARTED"

    def handle(self, event):
        if self.state == "STARTED" and isinstance(event, OrderCreated):
            self.order_id = event.order_id
            self.command_bus.send(ReserveInventory(
                order_id=self.order_id,
                items=event.items
            ))
            self.state = "AWAITING_INVENTORY"

        elif self.state == "AWAITING_INVENTORY":
            if isinstance(event, InventoryReserved):
                self.command_bus.send(ProcessPayment(
                    order_id=self.order_id,
                    amount=event.total
                ))
                self.state = "AWAITING_PAYMENT"
            elif isinstance(event, InventoryUnavailable):
                self.command_bus.send(CancelOrder(
                    order_id=self.order_id,
                    reason="Out of stock"
                ))
                self.state = "FAILED"

        elif self.state == "AWAITING_PAYMENT":
            if isinstance(event, PaymentCompleted):
                self.command_bus.send(ConfirmOrder(order_id=self.order_id))
                self.state = "COMPLETED"
            elif isinstance(event, PaymentFailed):
                self.command_bus.send(ReleaseInventory(order_id=self.order_id))
                self.command_bus.send(CancelOrder(
                    order_id=self.order_id,
                    reason=event.reason
                ))
                self.state = "COMPENSATING"
```

### Choreography vs Orchestration

| Aspect | Choreography | Orchestration |
|--------|--------------|---------------|
| Coupling | Loose | Central coordinator |
| Visibility | Hard to follow flow | Clear workflow |
| Complexity | Distributed | Centralized |
| Single point of failure | No | Orchestrator |
| Adding steps | Modify multiple services | Modify orchestrator |

---

## Operational Considerations

### Dead Letter Queues

Handle messages that repeatedly fail processing.

```
┌──────────┐    ┌──────────┐    ┌──────────────┐
│  Queue   │───►│ Consumer │───►│ Dead Letter  │
│          │    │ (fails)  │    │    Queue     │
└──────────┘    └──────────┘    └──────────────┘
                     │
                (retry N times, then DLQ)
```

**Handling DLQ:**
```python
class DLQProcessor:
    def process(self):
        while True:
            message = dlq.receive()
            try:
                # Attempt to fix and reprocess
                fixed = self.attempt_fix(message)
                if fixed:
                    main_queue.send(message)
                    dlq.delete(message)
                else:
                    # Alert for manual intervention
                    self.alert_ops(message)
            except Exception as e:
                logger.error(f"DLQ processing failed: {e}")
```

### Event Replay

Rebuild state by replaying events.

**Use cases:**
- Bug fix: Replay to fix corrupted projections
- New projection: Build from historical events
- Testing: Reproduce production issues

```python
class ProjectionRebuilder:
    def rebuild(self, projection: Projection, from_sequence: int = 0):
        # Reset projection state
        projection.reset()

        # Replay all events
        events = event_store.get_all_events(from_sequence=from_sequence)
        for event in events:
            projection.handle(event)
            if events.index(event) % 10000 == 0:
                logger.info(f"Replayed {events.index(event)} events")
```

### Monitoring and Alerting

**Key metrics:**
```
# Consumer lag
event_consumer_lag{topic="orders", consumer_group="inventory"}

# Processing latency
event_processing_duration_seconds{event_type="OrderPlaced"}

# DLQ depth
dead_letter_queue_depth{queue="orders-dlq"}

# Event throughput
events_published_total{topic="orders"}
events_consumed_total{topic="orders", consumer="inventory"}
```

**Alerts:**
```yaml
- alert: HighConsumerLag
  expr: event_consumer_lag > 10000
  for: 5m
  annotations:
    summary: "Consumer lag too high"

- alert: DLQNotEmpty
  expr: dead_letter_queue_depth > 0
  for: 1m
  annotations:
    summary: "Messages in dead letter queue"
```

### Schema Registry

Manage event schemas for compatibility.

```
┌──────────────┐        ┌────────────────────┐
│   Producer   │───────►│  Schema Registry   │
│              │        │  ┌──────────────┐  │
└──────────────┘        │  │ OrderPlaced  │  │
                        │  │   v1, v2, v3 │  │
┌──────────────┐        │  └──────────────┘  │
│   Consumer   │◄───────│                    │
│              │        └────────────────────┘
└──────────────┘
```

**Compatibility modes:**
- **Backward**: New schema can read old data
- **Forward**: Old schema can read new data
- **Full**: Both backward and forward compatible

---

## Anti-Patterns

### Event Soup

Too many fine-grained events without clear boundaries.

```
# BAD: Every field change is an event
CustomerFirstNameChanged
CustomerLastNameChanged
CustomerEmailChanged
CustomerPhoneChanged

# GOOD: Meaningful business events
CustomerProfileUpdated
CustomerContactInfoChanged
```

### Chatty Events

Events that require additional queries.

```python
# BAD: Consumers must query for details
@dataclass
class OrderPlaced:
    order_id: UUID
    # Consumer: "What's in the order? Let me call Order Service..."

# GOOD: Self-contained
@dataclass
class OrderPlaced:
    order_id: UUID
    items: List[OrderItem]
    total: Money
    customer_id: UUID
```

### Ignoring Idempotency

Processing same event twice causes problems.

```python
# BAD: Not idempotent
def on_payment_received(event):
    account.credit(event.amount)  # Double credit on retry!

# GOOD: Idempotent
def on_payment_received(event):
    if processed_events.contains(event.id):
        return
    account.credit(event.amount)
    processed_events.add(event.id)
```

### Synchronous Event Processing

Blocking until all handlers complete.

```python
# BAD: Sync processing
def place_order(order):
    event = OrderPlaced(order)
    inventory_handler.handle(event)  # Blocks
    notification_handler.handle(event)  # Blocks
    analytics_handler.handle(event)  # Blocks

# GOOD: Async processing
def place_order(order):
    event = OrderPlaced(order)
    event_bus.publish(event)  # Returns immediately
```

---

## Technology Choices

### Message Brokers

| Broker | Best For | Characteristics |
|--------|----------|-----------------|
| Kafka | Event streaming, high throughput | Ordered, persistent, replay |
| RabbitMQ | Task queues, routing | Flexible routing, AMQP |
| AWS SQS | Simple queuing | Managed, at-least-once |
| AWS SNS | Pub/sub fanout | Managed, push-based |
| Redis Streams | Real-time, caching | Fast, in-memory |

### Event Stores

| Store | Best For | Characteristics |
|-------|----------|-----------------|
| EventStoreDB | Event sourcing | Purpose-built, projections |
| PostgreSQL | General, ACID | Append-only table pattern |
| Kafka | Streaming + storage | Log retention, compaction |

---



## Quality Tests

### Trade-Off Test
- Alternatives were considered before choosing this architecture
- **PASS:** At least 2 alternative approaches evaluated with pros/cons
- **FAIL:** Architecture chosen without considering alternatives

### Scalability Test
- Architecture handles 10x current load without redesign
- **PASS:** Bottlenecks identified with specific scaling strategies
- **FAIL:** No analysis of how the system behaves under increased load

## Guidelines

### When to Use Event-Driven Architecture

**Good fit:**
- Decoupled services that need to react to changes
- Asynchronous workflows
- Audit/compliance requirements
- Real-time data processing
- Systems with multiple consumers per event

**Not a good fit:**
- Simple request-response interactions
- Strong consistency requirements
- Small, tightly-coupled systems
- When debugging complexity outweighs benefits

### How to Apply

1. **Identify domain events**: Work with domain experts
2. **Design event schemas**: Include necessary data, version from start
3. **Choose delivery guarantees**: At-least-once is usually right
4. **Ensure idempotency**: Consumers must handle duplicates
5. **Plan for failures**: DLQ, monitoring, replay
6. **Start simple**: Pub/sub before event sourcing

### Red Flags

- Events named as commands (PlaceOrder instead of OrderPlaced)
- Consumers that query producer for data
- No idempotency handling
- No monitoring of consumer lag
- Synchronous event processing
- Missing dead letter queue strategy

---

## References

### Books
- *Designing Event-Driven Systems* by Ben Stopford
- *Building Event-Driven Microservices* by Adam Bellemare
- *Domain-Driven Design* by Eric Evans (domain events)

### Online Resources
- Martin Fowler's event-driven articles
- Confluent's Kafka documentation
- Microsoft's CQRS/ES guidance

### Tools
- Event stores: EventStoreDB, Marten, Axon
- Message brokers: Kafka, RabbitMQ, Pulsar
- Schema registry: Confluent Schema Registry
- Monitoring: Kafka Manager, RabbitMQ Management
