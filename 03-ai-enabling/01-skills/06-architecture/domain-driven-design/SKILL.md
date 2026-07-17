---
last_updated: 2026-02-25
status: active
name: domain-driven-design
description: Strategic and tactical DDD patterns for modeling complex business domains. Use for bounded contexts, aggregates, entities, and ubiquitous language.
triggers:
  files: ["**/domain/**", "**/entities/**", "**/aggregates/**", "**/bounded-context/**", "**/DDD/**"]
  keywords: ["bounded context", "aggregate", "entity", "value object", "domain event", "ubiquitous language", "DDD", "domain model", "repository pattern", "domain service", "context map", "anti-corruption layer"]
allowed-tools: Read, Write, Edit
---

# Domain-Driven Design

## Overview

Domain-Driven Design (DDD) is an approach to software development that focuses on modeling software to match the business domain it serves. Created by Eric Evans, DDD addresses the complexity inherent in software by connecting the implementation to an evolving model of the core business concepts.

DDD is not about specific technologies or frameworks. It's about understanding the business, establishing a shared language between developers and domain experts, and structuring code to reflect that understanding. The goal is software that accurately represents the domain and can evolve as the business changes.

This skill covers both strategic DDD (high-level organizational patterns) and tactical DDD (implementation patterns for the domain layer).


## Define Done

- [ ] Architecture decisions documented with rationale and trade-offs
- [ ] Component boundaries and interfaces clearly defined
- [ ] Scalability and performance characteristics understood
- [ ] Dependencies identified and coupling minimized

## Core Principles

### 1. Ubiquitous Language

The foundation of DDD is a shared vocabulary used consistently by developers, domain experts, and in the code itself.

**The problem it solves:**
- Developers use technical jargon domain experts don't understand
- Domain experts use business terms that get lost in translation
- Code uses different names than the business uses
- Requirements get misunderstood due to terminology confusion

**How to establish ubiquitous language:**
1. Collaborate with domain experts to identify key concepts
2. Define terms precisely in a glossary
3. Use those exact terms in code (class names, method names, variables)
4. Refactor code when the language evolves
5. Challenge ambiguous terms immediately

**Example:**
```python
# BAD: Technical terms that don't match business language
class DataProcessor:
    def execute_workflow(self, data_packet):
        self.queue.push(data_packet)

# GOOD: Ubiquitous language from insurance domain
class ClaimProcessor:
    def submit_claim(self, insurance_claim):
        self.claims_queue.enqueue(insurance_claim)
```

### 2. Focus on the Core Domain

Not all parts of a system are equally important. DDD prioritizes the core domain—the part that provides competitive advantage.

**Domain categories:**
- **Core Domain**: Competitive advantage, deserves most attention
- **Supporting Subdomain**: Necessary but not differentiating
- **Generic Subdomain**: Commodity functionality, can buy off-the-shelf

**Example for an e-commerce company:**
| Subdomain | Type | Strategy |
|-----------|------|----------|
| Recommendation Engine | Core | Build custom, invest heavily |
| Order Processing | Supporting | Build in-house, moderate investment |
| User Authentication | Generic | Use existing library/service |

### 3. Model-Driven Design

The domain model is not just documentation—it directly shapes the code implementation.

**Principles:**
- Code should express the domain model explicitly
- Changes to the model should drive code changes (and vice versa)
- The model should be refined through continuous collaboration

---

## Strategic Design

Strategic DDD addresses the big-picture organization of a complex domain into manageable parts.

### Bounded Contexts

A bounded context is a linguistic and conceptual boundary where a particular domain model applies. The same term may have different meanings in different contexts.

**Example: "Customer" in different contexts**
```
Sales Context:
  Customer = prospect with contact info, sales history, preferences

Shipping Context:
  Customer = shipping address, delivery preferences

Billing Context:
  Customer = payment methods, billing address, credit terms
```

**Why bounded contexts matter:**
- Prevent model corruption from conflicting meanings
- Allow teams to work independently
- Enable different implementation strategies per context
- Reduce cognitive load (only one model to understand at a time)

**How to identify bounded contexts:**
1. Look for different meanings of the same term
2. Identify natural team boundaries
3. Find places where the ubiquitous language changes
4. Map existing system boundaries

**Diagram:**
```
┌─────────────────────────────────────────────────────────────┐
│                      E-Commerce System                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Sales     │  │   Shipping   │  │   Billing    │       │
│  │   Context    │  │   Context    │  │   Context    │       │
│  │              │  │              │  │              │       │
│  │  Customer:   │  │  Customer:   │  │  Customer:   │       │
│  │  - Name      │  │  - Address   │  │  - PaymentID │       │
│  │  - Email     │  │  - Delivery  │  │  - Credit    │       │
│  │  - History   │  │    Window    │  │    Terms     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Context Mapping

Context mapping describes the relationships between bounded contexts.

**Relationship patterns:**

**Shared Kernel:**
Two contexts share a subset of the model.
```
┌──────────┐     ┌──────────┐
│Context A │     │Context B │
│   ┌──────┼─────┼──────┐   │
│   │Shared│     │Kernel│   │
│   └──────┼─────┼──────┘   │
└──────────┘     └──────────┘
```
- **Use when**: Teams are tightly coupled and can coordinate changes
- **Risk**: Changes affect both contexts, requires coordination

**Customer-Supplier:**
Upstream context (supplier) provides data/services to downstream (customer).
```
┌──────────────┐           ┌──────────────┐
│  Upstream    │ ────────► │  Downstream  │
│  (Supplier)  │           │  (Customer)  │
└──────────────┘           └──────────────┘
```
- **Use when**: Clear dependency direction, downstream has influence on upstream API
- **Example**: Order context supplies data to Reporting context

**Conformist:**
Downstream adopts upstream's model without influence.
```
┌──────────────┐           ┌──────────────┐
│  Upstream    │ ────────► │  Downstream  │
│  (dictates)  │           │  (conforms)  │
└──────────────┘           └──────────────┘
```
- **Use when**: Upstream has no incentive to change (e.g., external API)
- **Example**: Integrating with government tax service

**Anti-Corruption Layer (ACL):**
Downstream protects itself from upstream's model through translation.
```
┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│  External    │ ──►│     ACL     │───►│   Our       │
│  System      │    │ (Translator)│    │   Context   │
└──────────────┘    └─────────────┘    └──────────────┘
```
- **Use when**: Upstream model is incompatible or legacy
- **Example**: Integrating with legacy mainframe system

**Implementation of ACL:**
```python
# External legacy system model
class LegacyCustomerRecord:
    def __init__(self, cust_no, nm_first, nm_last, addr_line_1):
        self.cust_no = cust_no
        self.nm_first = nm_first
        self.nm_last = nm_last
        self.addr_line_1 = addr_line_1

# Our domain model
class Customer:
    def __init__(self, customer_id, full_name, address):
        self.customer_id = customer_id
        self.full_name = full_name
        self.address = address

# Anti-corruption layer
class CustomerTranslator:
    def from_legacy(self, legacy: LegacyCustomerRecord) -> Customer:
        return Customer(
            customer_id=str(legacy.cust_no),
            full_name=f"{legacy.nm_first} {legacy.nm_last}",
            address=Address(street=legacy.addr_line_1)
        )

    def to_legacy(self, customer: Customer) -> LegacyCustomerRecord:
        names = customer.full_name.split(' ', 1)
        return LegacyCustomerRecord(
            cust_no=int(customer.customer_id),
            nm_first=names[0],
            nm_last=names[1] if len(names) > 1 else '',
            addr_line_1=customer.address.street
        )
```

**Open Host Service:**
Context provides a well-defined protocol for integration.
```
┌──────────────┐    ┌─────────────┐
│  Service     │───►│  Published  │
│  Context     │    │  Language   │
└──────────────┘    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │Client 1│   │Client 2│   │Client 3│
         └────────┘   └────────┘   └────────┘
```
- **Use when**: Many consumers need to integrate
- **Example**: REST API with versioned contracts

**Published Language:**
Contexts share a common interchange format.
- **Examples**: Industry standards (HL7 for healthcare, FIX for finance)
- **Use when**: Multiple systems need common understanding

### Subdomains

Within a bounded context, identify subdomains based on business capability.

**Example: Order Context subdomains**
```
Order Bounded Context
├── Order Placement (subdomain)
│   └── Creating and validating orders
├── Order Fulfillment (subdomain)
│   └── Picking, packing, shipping
└── Order Returns (subdomain)
    └── Processing returns and refunds
```

---

## Tactical Design

Tactical DDD provides building blocks for implementing the domain model within a bounded context.

### Entities

Objects with identity that persists over time. Two entities with the same attributes but different IDs are different entities.

**Characteristics:**
- Have a unique identifier
- Identity remains constant even as attributes change
- Lifecycle spans multiple state changes
- Equality based on identity, not attributes

**Example:**
```python
from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Customer:
    """Entity: identified by customer_id, not by name/email."""
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    email: str = ""

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def change_email(self, new_email: str) -> None:
        """Email changes but identity remains."""
        # Validation logic
        self.email = new_email
```

**When to use entities:**
- Object needs tracking over time (customer, order, account)
- Object has a lifecycle with state changes
- Object must be distinguishable even with identical attributes

### Value Objects

Objects defined by their attributes rather than identity. Two value objects with the same attributes are interchangeable.

**Characteristics:**
- No identity (immutable)
- Equality based on attributes
- Often used to represent domain concepts like Money, Address, DateRange
- Should be immutable

**Example:**
```python
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)  # Immutable
class Money:
    """Value Object: defined entirely by amount and currency."""
    amount: int  # cents to avoid floating point
    currency: str

    def add(self, other: Self) -> Self:
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> Self:
        return Money(self.amount * factor, self.currency)

    def __str__(self):
        return f"{self.currency} {self.amount / 100:.2f}"


@dataclass(frozen=True)
class Address:
    """Value Object: address with no identity."""
    street: str
    city: str
    postal_code: str
    country: str

    def format_for_shipping(self) -> str:
        return f"{self.street}\n{self.city}, {self.postal_code}\n{self.country}"
```

**When to use value objects:**
- Concept is defined by its attributes (address, money, coordinates)
- Object can be freely replaced with another with same values
- Immutability is desirable
- Object represents a measurement or description

**Value Object vs Entity decision:**
| Question | Entity | Value Object |
|----------|--------|--------------|
| Does it have a lifecycle? | Yes | No |
| Must we track changes over time? | Yes | No |
| Can two identical instances be interchanged? | No | Yes |
| Should it be immutable? | Not necessarily | Yes |

### Aggregates

Cluster of entities and value objects treated as a single unit for data changes. Every aggregate has a root entity that controls access to the aggregate.

**Characteristics:**
- Transactional consistency boundary
- Aggregate root is the only entry point
- External objects can only reference the root
- Internal objects deleted when root is deleted

**Example:**
```python
from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

@dataclass
class OrderLine:
    """Value Object within Order aggregate."""
    product_id: UUID
    quantity: int
    unit_price: Money

    @property
    def total(self) -> Money:
        return self.unit_price.multiply(self.quantity)


@dataclass
class Order:
    """Aggregate Root: controls access to order lines."""
    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = field(default_factory=uuid4)
    lines: List[OrderLine] = field(default_factory=list)
    status: str = "draft"

    def add_line(self, product_id: UUID, quantity: int, unit_price: Money) -> None:
        """Only the aggregate root can modify internal objects."""
        if self.status != "draft":
            raise InvalidOperationError("Cannot modify submitted order")

        # Check invariants
        existing = self._find_line(product_id)
        if existing:
            # Update existing line
            idx = self.lines.index(existing)
            self.lines[idx] = OrderLine(product_id, existing.quantity + quantity, unit_price)
        else:
            self.lines.append(OrderLine(product_id, quantity, unit_price))

    def submit(self) -> None:
        """Enforce aggregate invariants."""
        if not self.lines:
            raise InvalidOperationError("Cannot submit empty order")
        self.status = "submitted"

    @property
    def total(self) -> Money:
        if not self.lines:
            return Money(0, "USD")
        return sum((line.total for line in self.lines), Money(0, self.lines[0].unit_price.currency))

    def _find_line(self, product_id: UUID) -> OrderLine | None:
        return next((l for l in self.lines if l.product_id == product_id), None)
```

**Aggregate design rules:**

1. **Reference by identity**: External objects reference aggregate roots by ID, not direct object reference.
```python
# BAD: Direct reference
class Shipment:
    order: Order  # Direct object reference

# GOOD: Reference by identity
class Shipment:
    order_id: UUID  # Reference by ID
```

2. **Small aggregates**: Keep aggregates small. Large aggregates have concurrency issues.

3. **Update one aggregate per transaction**: Don't modify multiple aggregates in one transaction.

4. **Use eventual consistency between aggregates**: If updating multiple aggregates, use domain events.

### Domain Events

Represent something that happened in the domain. Events are immutable facts about the past.

**Characteristics:**
- Named in past tense (OrderPlaced, PaymentReceived)
- Immutable
- Contain data relevant to what happened
- Published by aggregates, consumed by handlers

**Example:**
```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class OrderPlaced:
    """Domain Event: published when order is submitted."""
    order_id: UUID
    customer_id: UUID
    total_amount: Money
    occurred_at: datetime


@dataclass(frozen=True)
class PaymentReceived:
    """Domain Event: published when payment is confirmed."""
    order_id: UUID
    payment_id: UUID
    amount: Money
    occurred_at: datetime


# Publishing events from aggregate
class Order:
    def __init__(self):
        self._events: List[DomainEvent] = []

    def submit(self) -> None:
        if not self.lines:
            raise InvalidOperationError("Cannot submit empty order")
        self.status = "submitted"

        # Record domain event
        self._events.append(OrderPlaced(
            order_id=self.id,
            customer_id=self.customer_id,
            total_amount=self.total,
            occurred_at=datetime.now()
        ))

    def collect_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
```

**Event handlers:**
```python
class OrderPlacedHandler:
    def __init__(self, inventory_service, notification_service):
        self.inventory = inventory_service
        self.notifications = notification_service

    def handle(self, event: OrderPlaced) -> None:
        # Reserve inventory
        self.inventory.reserve_for_order(event.order_id)

        # Send confirmation
        self.notifications.send_order_confirmation(
            event.customer_id,
            event.order_id
        )
```

### Domain Services

Operations that don't naturally belong to an entity or value object but are still part of the domain.

**When to use domain services:**
- Operation involves multiple aggregates
- Operation requires external information
- Operation is a significant domain process

**Example:**
```python
class PricingService:
    """Domain Service: calculates prices using complex rules."""

    def __init__(self, discount_repository, tax_service):
        self.discounts = discount_repository
        self.taxes = tax_service

    def calculate_order_total(self, order: Order, customer: Customer) -> Money:
        subtotal = order.subtotal

        # Apply customer-specific discounts
        discount = self.discounts.get_discount_for_customer(customer.id)
        discounted = discount.apply_to(subtotal)

        # Calculate taxes based on shipping address
        tax = self.taxes.calculate(discounted, order.shipping_address)

        return discounted.add(tax)


class TransferService:
    """Domain Service: handles money transfer between accounts."""

    def transfer(self, from_account: Account, to_account: Account, amount: Money) -> None:
        if from_account.balance < amount:
            raise InsufficientFundsError()

        from_account.debit(amount)
        to_account.credit(amount)
```

### Repositories

Abstraction for retrieving and persisting aggregates. Repositories hide persistence details from the domain.

**Characteristics:**
- One repository per aggregate root
- Returns and accepts only aggregate roots
- Simulates an in-memory collection
- Implementation details hidden behind interface

**Example:**
```python
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

class OrderRepository(ABC):
    """Repository interface: defined in domain layer."""

    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def find_by_customer(self, customer_id: UUID) -> List[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def delete(self, order: Order) -> None:
        pass


# Infrastructure implementation
class PostgresOrderRepository(OrderRepository):
    """Concrete implementation in infrastructure layer."""

    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        row = self.session.query(OrderModel).filter_by(id=order_id).first()
        return self._to_domain(row) if row else None

    def save(self, order: Order) -> None:
        model = self._to_model(order)
        self.session.merge(model)
        self.session.commit()

    def _to_domain(self, model: OrderModel) -> Order:
        # Map from persistence model to domain model
        pass

    def _to_model(self, order: Order) -> OrderModel:
        # Map from domain model to persistence model
        pass
```

### Factories

Encapsulate complex object creation logic.

**When to use factories:**
- Object creation is complex
- Creation involves multiple steps or validations
- Creating objects requires knowledge the client shouldn't have

**Example:**
```python
class OrderFactory:
    """Factory: encapsulates complex order creation."""

    def __init__(self, pricing_service, inventory_service):
        self.pricing = pricing_service
        self.inventory = inventory_service

    def create_order(
        self,
        customer_id: UUID,
        items: List[CartItem],
        shipping_address: Address
    ) -> Order:
        order = Order(customer_id=customer_id)

        for item in items:
            # Validate inventory availability
            if not self.inventory.is_available(item.product_id, item.quantity):
                raise OutOfStockError(item.product_id)

            # Get current price
            price = self.pricing.get_price(item.product_id)
            order.add_line(item.product_id, item.quantity, price)

        order.set_shipping_address(shipping_address)
        return order
```

---

## Aggregate Design Guidelines

### Finding Aggregate Boundaries

1. **Identify true invariants**: What rules must always be consistent?
2. **Start small**: Begin with single-entity aggregates
3. **Group by consistency requirement**: Not by conceptual relationship

**Example analysis:**
```
Order domain analysis:
- Order and OrderLines: Strong consistency (totals must be correct)
  → Same aggregate

- Order and Customer: Reference only (customer can exist without order)
  → Separate aggregates, reference by ID

- Order and Payment: Eventually consistent (payment can fail)
  → Separate aggregates, connected by events
```

### Common Mistakes

**Mistake 1: Too-large aggregates**
```python
# BAD: Giant aggregate with everything
class Customer:
    orders: List[Order]      # All historical orders
    preferences: Preferences
    addresses: List[Address]
    payment_methods: List[PaymentMethod]
    reviews: List[Review]
    # Concurrency nightmare, slow to load

# GOOD: Focused aggregate
class Customer:
    id: UUID
    name: str
    email: str
    # Reference other aggregates by ID
    default_address_id: UUID
    default_payment_method_id: UUID
```

**Mistake 2: Breaking aggregate boundaries**
```python
# BAD: Directly accessing internal objects
order = order_repository.find_by_id(order_id)
order.lines[0].quantity = 10  # Bypassing aggregate root!

# GOOD: Go through aggregate root
order.update_line_quantity(product_id, 10)  # Root enforces invariants
```

**Mistake 3: Multi-aggregate transactions**
```python
# BAD: Transaction across aggregates
def place_order(order, inventory, customer):
    with transaction():
        order_repository.save(order)
        inventory.reserve(order.items)  # Different aggregate
        customer.add_order(order.id)    # Different aggregate

# GOOD: Eventual consistency with events
def place_order(order):
    order_repository.save(order)
    # OrderPlaced event triggers:
    # - InventoryReservationHandler
    # - CustomerOrderHistoryHandler
```

---

## Implementation Patterns

### Layered Architecture for DDD

```
┌─────────────────────────────────────────────┐
│           Presentation Layer                │
│     (Controllers, API endpoints, CLI)       │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│           Application Layer                 │
│   (Use cases, application services,         │
│    command/query handlers, DTOs)            │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│             Domain Layer                    │
│  (Entities, Value Objects, Aggregates,      │
│   Domain Services, Repository interfaces)   │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│          Infrastructure Layer               │
│   (Repository implementations, external     │
│    APIs, message brokers, persistence)      │
└─────────────────────────────────────────────┘
```

**Dependency rule**: Inner layers don't depend on outer layers.

### Project Structure

```
src/
├── ordering/                    # Bounded context
│   ├── domain/                  # Domain layer
│   │   ├── model/
│   │   │   ├── order.py         # Order aggregate
│   │   │   ├── customer.py      # Customer entity
│   │   │   └── money.py         # Value objects
│   │   ├── events/
│   │   │   └── order_events.py  # Domain events
│   │   ├── services/
│   │   │   └── pricing.py       # Domain services
│   │   └── repositories/
│   │       └── order_repo.py    # Repository interfaces
│   │
│   ├── application/             # Application layer
│   │   ├── commands/
│   │   │   └── place_order.py   # Command handlers
│   │   ├── queries/
│   │   │   └── get_order.py     # Query handlers
│   │   └── services/
│   │       └── order_service.py # Application services
│   │
│   └── infrastructure/          # Infrastructure layer
│       ├── persistence/
│       │   └── postgres_order_repo.py
│       └── messaging/
│           └── event_publisher.py
│
├── shipping/                    # Another bounded context
│   └── ...
│
└── shared_kernel/               # Shared code (if any)
    └── money.py
```

### Application Services

Orchestrate domain objects without containing business logic.

```python
class PlaceOrderCommand:
    customer_id: UUID
    items: List[OrderItemDTO]
    shipping_address: AddressDTO


class PlaceOrderHandler:
    """Application service: orchestrates domain objects."""

    def __init__(
        self,
        order_factory: OrderFactory,
        order_repository: OrderRepository,
        event_publisher: EventPublisher
    ):
        self.factory = order_factory
        self.orders = order_repository
        self.events = event_publisher

    def handle(self, command: PlaceOrderCommand) -> UUID:
        # Create aggregate using factory
        order = self.factory.create_order(
            customer_id=command.customer_id,
            items=command.items,
            shipping_address=command.shipping_address
        )

        # Submit order (domain logic in aggregate)
        order.submit()

        # Persist
        self.orders.save(order)

        # Publish domain events
        for event in order.collect_events():
            self.events.publish(event)

        return order.id
```

---

## Anti-Patterns

### Anemic Domain Model

Domain objects with only getters/setters, all logic in services.

```python
# ANTI-PATTERN: Anemic model
class Order:
    id: UUID
    status: str
    lines: List[OrderLine]
    # No behavior, just data

class OrderService:
    def submit_order(self, order: Order):
        if not order.lines:
            raise ValidationError("No lines")
        order.status = "submitted"  # Logic outside the model


# GOOD: Rich domain model
class Order:
    def submit(self) -> None:
        """Domain logic inside the aggregate."""
        if not self.lines:
            raise CannotSubmitEmptyOrderError()
        self.status = "submitted"
        self._events.append(OrderSubmitted(self.id))
```

### Leaking Domain Logic

Business rules scattered across layers.

```python
# ANTI-PATTERN: Logic in controller
@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: UUID):
    order = order_repository.find_by_id(order_id)

    # Business rule in controller!
    if order.status == "shipped":
        raise HTTPException(400, "Cannot cancel shipped order")

    order.status = "cancelled"

# GOOD: Logic in domain
class Order:
    def cancel(self) -> None:
        if self.status == "shipped":
            raise OrderAlreadyShippedError()
        self.status = "cancelled"

# Controller just orchestrates
@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: UUID):
    order = order_repository.find_by_id(order_id)
    order.cancel()
    order_repository.save(order)
```

### Ignoring Bounded Contexts

Using a single model for the entire system.

```python
# ANTI-PATTERN: God class
class Customer:
    # Sales concerns
    sales_rep_id: UUID
    pipeline_stage: str

    # Billing concerns
    payment_terms: str
    credit_limit: Money

    # Shipping concerns
    shipping_address: Address
    delivery_preferences: str

    # Support concerns
    support_tier: str
    ticket_history: List[Ticket]

# GOOD: Separate models per context
# In Sales context
class Prospect:
    sales_rep_id: UUID
    pipeline_stage: str

# In Billing context
class BillingAccount:
    payment_terms: str
    credit_limit: Money
```

---

## When to Use DDD

### Good Fit

- Complex domain with intricate business rules
- Domain experts available for collaboration
- Long-term project with evolving requirements
- Team willing to invest in domain understanding
- Multiple bounded contexts or subdomains

### Not a Good Fit

- Simple CRUD applications
- Technical infrastructure projects
- Short-term or throwaway projects
- No access to domain experts
- Team unfamiliar with DDD concepts

### Adoption Strategy

1. **Start strategic**: Identify bounded contexts and relationships
2. **Apply tactical patterns selectively**: In complex areas
3. **Iterate on the model**: Refactor as understanding deepens
4. **Invest in ubiquitous language**: Glossary, diagrams, documentation

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

### When to Use This Skill

- Modeling complex business domains
- Designing bounded context boundaries
- Implementing aggregates and entities
- Establishing ubiquitous language
- Integrating with legacy systems (ACL)
- Reviewing domain model designs

### How to Apply

1. **Collaborate with domain experts**: Learn the language
2. **Model the domain**: Identify entities, value objects, aggregates
3. **Define bounded contexts**: Find natural boundaries
4. **Design aggregates carefully**: Small, consistency-focused
5. **Use events for cross-aggregate communication**
6. **Keep domain layer pure**: No infrastructure dependencies

### Red Flags

- Anemic domain models (all logic in services)
- God objects spanning multiple contexts
- Direct database access from domain objects
- Business rules in controllers or UI
- Aggregates that are too large
- Shared database across bounded contexts

---

## References

### Books
- *Domain-Driven Design* by Eric Evans
- *Implementing Domain-Driven Design* by Vaughn Vernon
- *Domain-Driven Design Distilled* by Vaughn Vernon
- *Patterns, Principles, and Practices of Domain-Driven Design* by Scott Millett

### Online Resources
- DDD Community: dddcommunity.org
- Martin Fowler's DDD articles
- Vaughn Vernon's blog

### Tools
- Event Storming (collaborative modeling)
- Context Mapper (visualization)
- PlantUML/Mermaid (diagrams)
