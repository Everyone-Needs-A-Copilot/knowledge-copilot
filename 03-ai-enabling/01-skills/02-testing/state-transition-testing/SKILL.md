---
last_updated: 2026-02-25
status: active
name: state-transition-testing
description: State machine testing - verify valid transitions, guard conditions, and invalid state changes. Use when testing stateful systems.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*", "**/*state*", "**/*machine*", "**/*workflow*"]
  keywords: ["state machine", "state transition", "workflow test", "status change", "finite state", "state diagram", "transition test"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides state transition testing for systems with defined states and transitions. Test that valid transitions work, invalid transitions are rejected, and guard conditions enforce business rules.

The user provides testing requirements: a state machine to test, workflow logic with states, or an existing system with status changes. They may include context about state diagrams, transition rules, or edge cases.

## Why State Transition Testing

**Stateful systems have hidden complexity:**
- Valid actions depend on current state
- Order of operations matters
- Invalid transitions cause bugs or security issues
- Edge cases hide at state boundaries

**Example: Order status bugs**
```
Bug: Order marked "shipped" while payment still "pending"
Cause: Missing transition guard
Impact: Lost revenue, inventory mismatch
```


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## State Machine Fundamentals

### Core Components

| Component | Description | Example |
|-----------|-------------|---------|
| State | Current condition | Order: Draft, Submitted, Paid |
| Event | Trigger for transition | submit, pay, ship |
| Transition | State change | Draft → Submitted |
| Guard | Condition for transition | payment.valid? |
| Action | Side effect of transition | send_confirmation_email |

### Example: Order State Machine

```
         submit        pay         ship
[Draft] -------→ [Submitted] ---→ [Paid] ---→ [Shipped]
   ↓                  ↓             ↓            ↓
   cancel            cancel       refund       refund
   ↓                  ↓             ↓            ↓
[Cancelled]      [Cancelled]   [Refunded]   [Refunded]
```

**States:** Draft, Submitted, Paid, Shipped, Cancelled, Refunded
**Events:** submit, cancel, pay, ship, refund

## Designing State Transition Tests

### Step 1: Define State Table

| Current State | Event | Guard | Next State | Action |
|---------------|-------|-------|------------|--------|
| Draft | submit | items.present? | Submitted | notify_warehouse |
| Draft | cancel | - | Cancelled | - |
| Submitted | pay | payment.valid? | Paid | process_payment |
| Submitted | cancel | - | Cancelled | release_inventory |
| Paid | ship | inventory.available? | Shipped | create_shipment |
| Paid | refund | - | Refunded | process_refund |
| Shipped | refund | within_return_window? | Refunded | process_refund |

### Step 2: Test Valid Transitions

```python
class TestOrderTransitions:
    def test_draft_to_submitted(self):
        order = Order(status="draft", items=[item])

        order.submit()

        assert order.status == "submitted"
        assert warehouse_notified(order)

    def test_submitted_to_paid(self):
        order = Order(status="submitted")
        payment = valid_payment()

        order.pay(payment)

        assert order.status == "paid"
        assert payment_processed(payment)

    def test_paid_to_shipped(self):
        order = Order(status="paid")
        reserve_inventory(order)

        order.ship()

        assert order.status == "shipped"
        assert shipment_created(order)
```

### Step 3: Test Invalid Transitions

```python
class TestInvalidTransitions:
    def test_cannot_ship_unpaid_order(self):
        order = Order(status="submitted")  # Not paid

        with pytest.raises(InvalidTransitionError):
            order.ship()

        assert order.status == "submitted"  # Unchanged

    def test_cannot_submit_empty_order(self):
        order = Order(status="draft", items=[])  # Empty

        with pytest.raises(InvalidTransitionError):
            order.submit()

        assert order.status == "draft"

    def test_cannot_refund_draft_order(self):
        order = Order(status="draft")

        with pytest.raises(InvalidTransitionError):
            order.refund()
```

### Step 4: Test Guard Conditions

```python
class TestTransitionGuards:
    def test_pay_requires_valid_payment(self):
        order = Order(status="submitted")
        invalid_payment = Payment(card_expired=True)

        with pytest.raises(PaymentError):
            order.pay(invalid_payment)

        assert order.status == "submitted"

    def test_ship_requires_inventory(self):
        order = Order(status="paid")
        deplete_inventory(order.items)  # No stock

        with pytest.raises(InventoryError):
            order.ship()

        assert order.status == "paid"

    def test_refund_within_return_window(self):
        order = Order(status="shipped", shipped_at=days_ago(45))  # Beyond 30-day window

        with pytest.raises(RefundWindowExpiredError):
            order.refund()
```

## Transition Coverage Strategies

### 0-Switch Coverage (All States)

Test that each state can be reached.

```python
def test_all_states_reachable():
    # Draft state (initial)
    order = Order()
    assert order.status == "draft"

    # Submitted state
    order.submit()
    assert order.status == "submitted"

    # Paid state
    order.pay(valid_payment())
    assert order.status == "paid"

    # Shipped state
    order.ship()
    assert order.status == "shipped"

def test_cancelled_state():
    order = Order(status="draft")
    order.cancel()
    assert order.status == "cancelled"

def test_refunded_state():
    order = Order(status="paid")
    order.refund()
    assert order.status == "refunded"
```

### 1-Switch Coverage (All Transitions)

Test every valid transition at least once.

```python
class TestAllTransitions:
    # Draft transitions
    def test_draft_submit(self): ...
    def test_draft_cancel(self): ...

    # Submitted transitions
    def test_submitted_pay(self): ...
    def test_submitted_cancel(self): ...

    # Paid transitions
    def test_paid_ship(self): ...
    def test_paid_refund(self): ...

    # Shipped transitions
    def test_shipped_refund(self): ...
```

### 2-Switch Coverage (Transition Sequences)

Test pairs of consecutive transitions.

```python
class TestTransitionSequences:
    def test_draft_submit_pay(self):
        order = Order(status="draft", items=[item])
        order.submit()
        order.pay(valid_payment())
        assert order.status == "paid"

    def test_draft_submit_cancel(self):
        order = Order(status="draft", items=[item])
        order.submit()
        order.cancel()
        assert order.status == "cancelled"

    def test_submit_pay_ship(self):
        order = Order(status="submitted")
        order.pay(valid_payment())
        order.ship()
        assert order.status == "shipped"

    def test_submit_pay_refund(self):
        order = Order(status="submitted")
        order.pay(valid_payment())
        order.refund()
        assert order.status == "refunded"
```

### Full Path Coverage

Test complete paths through the state machine.

```python
class TestCompletePaths:
    def test_happy_path_to_shipped(self):
        order = Order(status="draft", items=[item])
        order.submit()
        order.pay(valid_payment())
        order.ship()

        assert order.status == "shipped"
        assert order.history == ["draft", "submitted", "paid", "shipped"]

    def test_cancellation_path(self):
        order = Order(status="draft", items=[item])
        order.submit()
        order.cancel()

        assert order.status == "cancelled"
        assert order.history == ["draft", "submitted", "cancelled"]

    def test_refund_after_ship_path(self):
        order = Order(status="draft", items=[item])
        order.submit()
        order.pay(valid_payment())
        order.ship()
        order.refund()

        assert order.status == "refunded"
```

## Testing Transition Side Effects

### Actions on Entry

```python
def test_shipped_state_triggers_notification(self):
    order = Order(status="paid")
    email_spy = mock_email_service()

    order.ship()

    assert email_spy.called_with(
        to=order.customer.email,
        template="order_shipped",
        tracking=order.tracking_number
    )

def test_paid_state_processes_payment(self):
    order = Order(status="submitted")
    payment = valid_payment()
    payment_processor = mock_payment_service()

    order.pay(payment)

    assert payment_processor.charged(
        amount=order.total,
        card=payment.card
    )
```

### Actions on Exit

```python
def test_leaving_draft_reserves_inventory(self):
    order = Order(status="draft", items=[item])
    inventory = mock_inventory_service()

    order.submit()

    assert inventory.reserved(item.sku, quantity=1)

def test_leaving_submitted_releases_inventory_on_cancel(self):
    order = Order(status="submitted", items=[item])
    inventory = mock_inventory_service()

    order.cancel()

    assert inventory.released(item.sku, quantity=1)
```

## Complex State Machine Patterns

### Hierarchical States

```
[Active]
  ├── [Processing]
  │     ├── [Validating]
  │     └── [Calculating]
  └── [Waiting]
        ├── [Waiting for Input]
        └── [Waiting for Approval]
```

```python
def test_hierarchical_state_transitions():
    workflow = Workflow()

    assert workflow.state == "active.processing.validating"

    workflow.validation_complete()
    assert workflow.state == "active.processing.calculating"

    workflow.calculation_complete()
    assert workflow.state == "active.waiting.waiting_for_approval"

    workflow.approved()
    assert workflow.state == "completed"
```

### Parallel States

```
[Order Processing]
  ├── [Payment] ─── pending → authorized → captured
  └── [Fulfillment] ─── pending → picking → packed → shipped
```

```python
def test_parallel_state_transitions():
    order = Order()

    # Both tracks start pending
    assert order.payment_state == "pending"
    assert order.fulfillment_state == "pending"

    # Payment track advances
    order.authorize_payment()
    assert order.payment_state == "authorized"
    assert order.fulfillment_state == "pending"

    # Fulfillment track advances
    order.start_picking()
    assert order.fulfillment_state == "picking"

    # Both must complete for order completion
    order.capture_payment()
    order.pack()
    order.ship()

    assert order.is_complete()
```

### Guard Condition Testing

```python
class TestGuardConditions:
    def test_guard_passes(self):
        order = Order(
            status="submitted",
            payment=Payment(amount=100, card_valid=True)
        )

        order.pay()

        assert order.status == "paid"

    def test_guard_fails_insufficient_funds(self):
        order = Order(
            status="submitted",
            payment=Payment(amount=100, card_balance=50)
        )

        with pytest.raises(InsufficientFundsError):
            order.pay()

        assert order.status == "submitted"

    def test_guard_fails_expired_card(self):
        order = Order(
            status="submitted",
            payment=Payment(card_expired=True)
        )

        with pytest.raises(CardExpiredError):
            order.pay()

        assert order.status == "submitted"
```

## Common State Machine Patterns

### User Account States

```
[Pending] → verify → [Active] → suspend → [Suspended]
                         ↓                      ↓
                       delete                reactivate
                         ↓                      ↓
                    [Deleted]               [Active]
```

```python
class TestAccountStates:
    def test_verify_activates_account(self):
        account = Account(status="pending")
        account.verify(token="valid_token")
        assert account.status == "active"

    def test_cannot_suspend_pending_account(self):
        account = Account(status="pending")
        with pytest.raises(InvalidTransitionError):
            account.suspend()

    def test_reactivate_suspended_account(self):
        account = Account(status="suspended")
        account.reactivate()
        assert account.status == "active"
```

### Document Workflow States

```
[Draft] → submit → [Review] → approve → [Published]
             ↓          ↓
          save_draft  reject
             ↓          ↓
         [Draft]    [Draft]
```

```python
class TestDocumentWorkflow:
    def test_full_approval_flow(self):
        doc = Document(status="draft")
        doc.submit()
        doc.approve(reviewer="editor")

        assert doc.status == "published"
        assert doc.approved_by == "editor"

    def test_rejection_returns_to_draft(self):
        doc = Document(status="review")
        doc.reject(reason="Needs revision")

        assert doc.status == "draft"
        assert doc.rejection_reason == "Needs revision"
```

## State Transition Test Matrix

### Generating Test Cases

| From State | To State | Valid? | Test |
|------------|----------|--------|------|
| Draft | Submitted | Yes | test_draft_to_submitted |
| Draft | Paid | No | test_cannot_pay_draft |
| Draft | Shipped | No | test_cannot_ship_draft |
| Draft | Cancelled | Yes | test_draft_to_cancelled |
| Submitted | Paid | Yes | test_submitted_to_paid |
| Submitted | Shipped | No | test_cannot_ship_unpaid |
| ... | ... | ... | ... |

### Invalid Transition Coverage

```python
class TestInvalidTransitions:
    @pytest.mark.parametrize("from_state,event", [
        ("draft", "ship"),
        ("draft", "pay"),
        ("draft", "refund"),
        ("submitted", "ship"),
        ("submitted", "refund"),
        ("cancelled", "submit"),
        ("cancelled", "pay"),
        ("cancelled", "ship"),
        ("cancelled", "refund"),
        ("shipped", "submit"),
        ("shipped", "pay"),
        ("shipped", "ship"),
    ])
    def test_invalid_transitions_rejected(self, from_state, event):
        order = Order(status=from_state)

        with pytest.raises(InvalidTransitionError):
            getattr(order, event)()

        assert order.status == from_state  # Unchanged
```

## Quick Reference

### Test Coverage Levels

| Level | What to Test | Test Count |
|-------|--------------|------------|
| 0-Switch | All states reachable | n states |
| 1-Switch | All transitions | n transitions |
| 2-Switch | Transition pairs | n × n (filtered) |
| Full Path | Complete paths | Varies |
| Invalid | Rejected transitions | m invalid transitions |

### State Transition Test Checklist

- [ ] Every state is reachable from initial state
- [ ] Every valid transition works correctly
- [ ] Every invalid transition is rejected
- [ ] Guard conditions are tested (pass and fail)
- [ ] Side effects (actions) are verified
- [ ] Terminal states cannot be exited
- [ ] State history is correct

### Common Bugs Found

| Bug Type | Example | Test Strategy |
|----------|---------|---------------|
| Missing guard | Ship without payment | Test guard conditions |
| Wrong next state | Submit goes to Paid | Test each transition |
| Missing transition | Can't cancel submitted | Test expected transitions |
| Side effect skip | Email not sent | Test actions |
| State corruption | Status = "invalid" | Test state after transition |

## Summary

State transition testing ensures stateful systems behave correctly:

1. **Map the state machine** - States, events, transitions, guards
2. **Test valid transitions** - Each one should work
3. **Test invalid transitions** - Each one should be rejected
4. **Test guard conditions** - Both passing and failing
5. **Test side effects** - Actions should execute correctly
6. **Test sequences** - Multi-step paths through states
7. **Use parametrization** - Systematic coverage of all cases


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

