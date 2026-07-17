---
last_updated: 2026-02-25
status: active
name: testing-patterns
description: Testing philosophy, strategy, and patterns - test pyramid, TDD, test design. Use when planning test strategy.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*"]
  keywords: ["unit test", "integration test", "E2E", "test pyramid", "TDD", "coverage", "flaky test", "mock", "test strategy"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides creation of robust, maintainable test suites that provide confidence without ceremony. Write tests that catch real bugs, document behavior, and enable fearless refactoring - not tests that exist merely to satisfy coverage metrics.

The user provides testing requirements: a feature to test, a bug to reproduce, test strategy to design, or test suite to improve. They may include context about the system, quality requirements, or testing constraints.

## Testing Philosophy

Testing is about **risk management** and **feedback loops**. Good tests:
- Catch bugs before users do
- Make refactoring safe
- Document intended behavior
- Run fast enough to get used
- Fail clearly when something breaks
- Provide confidence, not ceremony

**CRITICAL**: Test strategy should match risk profile. Mission-critical financial calculations need comprehensive testing. Internal admin tools need pragmatic coverage. The goal is appropriate confidence, not 100% coverage.


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Core Principles

### 1. Fast Feedback Wins
- Tests you don't run don't help
- Unit tests: <1ms each, full suite <10s
- Integration tests: <100ms each, full suite <2min
- E2E tests: <10s each, critical path <5min
- Slow tests get skipped, then break in CI

### 2. Fail Fast, Fail Clear
- One assertion per test (when possible)
- Clear test names that describe the scenario
- Explicit error messages that guide debugging
- No cascading failures (independent tests)

### 3. Test Behavior, Not Implementation
- Test what the code does, not how it does it
- Refactoring shouldn't break tests
- Mock external dependencies, not internal methods
- Tests should survive implementation changes

### 4. Meaningful Over Mechanical
- 70% coverage of critical paths > 100% coverage of everything
- One good integration test > five brittle unit tests
- Test edge cases that matter, not every possible input
- Quality over quantity

## The Testing Pyramid

```
        /\
       /E2E\      10% - Critical user journeys (slow, expensive)
      /------\
     /  INT   \   20% - Component interactions (moderate speed)
    /----------\
   /    UNIT    \ 70% - Individual functions (fast, cheap)
  /--------------\
```

### Why This Shape?

**Unit Tests (70%)**: Fast, focused, numerous
- Test individual functions/methods
- Isolated from dependencies
- Run in milliseconds
- Catch logic errors early
- Easy to write, easy to maintain

**Integration Tests (20%)**: Moderate speed, moderate cost
- Test component interactions
- Real database/APIs where practical
- Catch interface mismatches
- Verify end-to-end data flow
- Balance coverage and speed

**E2E Tests (10%)**: Slow, expensive, selective
- Test critical user journeys
- Full stack, real browser
- Catch UI/UX regressions
- Verify business requirements
- Only for high-value paths

### When to Deviate

**More integration tests** when:
- Complex data transformations across boundaries
- Legacy system with poor unit test coverage
- Distributed systems with many services
- API contracts are the primary risk

**More E2E tests** when:
- UI is the primary risk (design systems)
- Business logic lives in frontend
- Visual regressions are common
- User flows are complex

**Fewer unit tests** when:
- Code is mostly glue/configuration
- Framework handles the complexity
- Integration tests provide better ROI

## Test-Driven Development (TDD)

### The Red-Green-Refactor Cycle

1. **Red**: Write a failing test for ONE piece of behavior
2. **Green**: Write minimum code to make it pass
3. **Refactor**: Clean up code while keeping tests green
4. Repeat for next behavior

### When TDD Helps

**Use TDD for:**
- Complex algorithms (parsing, calculations)
- Edge case handling (validation, error paths)
- Business logic with many branches
- Bug fixes (regression tests)
- APIs (contract-first design)

**Benefits:**
- Forces you to think about requirements first
- Creates testable code by default
- Prevents over-engineering
- Documents expected behavior
- Catches regressions immediately

### When TDD Hinders

**Skip TDD when:**
- Exploring/prototyping unclear requirements
- UI layout and visual design
- Simple CRUD operations
- Glue code between frameworks
- Learning a new technology

**Why:**
- Requirements are too fluid
- Tests would just mirror implementation
- Framework provides the behavior
- Writing tests first slows exploration

### TDD Strategies

**Outside-In** (London School):
- Start with high-level behavior
- Mock dependencies as you go
- Work from API/UI down to details
- Good for: Web APIs, user flows

**Inside-Out** (Detroit School):
- Start with core domain logic
- Build up without mocks
- Integrate components last
- Good for: Algorithms, business rules

**Hybrid** (Pragmatic):
- TDD for complex logic
- Tests-after for glue code
- Integration tests for boundaries
- Good for: Most real-world projects

## Test Design Patterns

### Arrange-Act-Assert (AAA)

```
test "deposit increases account balance":
  // Arrange - Set up test data
  account = Account(balance: 100)

  // Act - Execute the behavior
  account.deposit(50)

  // Assert - Verify the outcome
  assert account.balance == 150
```

**Benefits:**
- Clear separation of concerns
- Easy to read and understand
- Natural flow: setup → action → verify

**Tips:**
- Keep Arrange small (use factories/fixtures)
- One logical action in Act
- One concept in Assert (may be multiple assertions)
- Blank lines between sections

### Given-When-Then (BDD Style)

```
Scenario: Customer deposits money into account
  Given a customer has an account with balance $100
  When they deposit $50
  Then their account balance should be $150
  And they should receive a confirmation
```

**Benefits:**
- Business-readable specifications
- Natural language, less code-focused
- Good for stakeholder communication
- Maps to acceptance criteria

**Use when:**
- Writing acceptance tests
- Domain experts review tests
- Business rules drive behavior
- User stories define scope

### Test Naming Conventions

**Pattern 1: Given_When_Then**
```
test_givenEmptyCart_whenAddingItem_thenCartHasOneItem()
test_givenExpiredToken_whenValidating_thenThrowsAuthError()
```

**Pattern 2: MethodName_Scenario_ExpectedBehavior**
```
test_calculateTax_withZeroAmount_returnsZero()
test_sendEmail_withInvalidAddress_throwsValidationError()
```

**Pattern 3: Natural Language**
```
test "empty cart has zero items"
test "cannot checkout with expired payment method"
test "admin can delete user accounts"
```

**Choose consistency** over any specific style. Mix patterns only if you have a good reason (e.g., unit vs. integration tests).

### Edge Cases and Boundary Testing

Test the boundaries where bugs hide:

**Numeric Boundaries:**
- Zero, negative, positive
- Min/max values
- Off-by-one errors
- Integer overflow

**Collections:**
- Empty, single item, many items
- Null/undefined
- Duplicates

**Strings:**
- Empty string
- Single character
- Very long strings
- Special characters, unicode
- Leading/trailing whitespace

**Dates/Times:**
- Past, present, future
- Timezone boundaries
- Leap years, DST transitions
- Unix epoch edge cases

**States:**
- Initial state
- Valid transitions
- Invalid transitions
- Terminal states

**Permissions:**
- Not logged in
- Wrong user
- Expired sessions
- Missing permissions

### Equivalence Partitioning

Group inputs into classes that behave the same way, then test one from each class:

```
// Function: discount(quantity)
// Business rule:
//   0-9 items: no discount
//   10-49 items: 10% discount
//   50+ items: 20% discount

test "no discount for small orders":
  assert discount(5) == 0%   // representative of 0-9

test "10% discount for medium orders":
  assert discount(25) == 10%  // representative of 10-49

test "20% discount for large orders":
  assert discount(100) == 20% // representative of 50+

// Also test boundaries:
test "boundary cases":
  assert discount(9) == 0%
  assert discount(10) == 10%
  assert discount(49) == 10%
  assert discount(50) == 20%
```

**Benefits:**
- Reduces test count without losing coverage
- Makes test suite maintainable
- Focuses on meaningful distinctions
- Catches off-by-one errors

## Mocking Strategy

### When to Mock

**Mock external dependencies:**
- Third-party APIs
- Email/SMS services
- Payment processors
- File system I/O
- Network calls
- System clock

**Mock slow dependencies:**
- Database (in unit tests)
- Search indexes
- Message queues
- Cache layers

**Mock unpredictable dependencies:**
- Random number generators
- Current time/date
- Environment variables
- External configurations

### When NOT to Mock

**Don't mock internal methods:**
```
// BAD - Testing implementation, not behavior
test "processOrder calls validatePayment":
  order = Mock(Order)
  order.processOrder()
  assert order.validatePayment.called

// GOOD - Testing actual behavior
test "processOrder rejects invalid payment":
  order = Order(payment: invalidCard)
  result = order.processOrder()
  assert result.error == "Payment validation failed"
```

**Don't mock the system under test:**
```
// BAD
test "user login":
  user = Mock(User)
  user.login.returns(true)
  assert user.login() == true  // Just testing the mock!

// GOOD
test "user login with valid credentials":
  user = User(email: "test@example.com")
  result = user.login(password: "correct")
  assert result.success == true
```

**Don't mock simple objects:**
```
// BAD - Mocking is more complex than the real thing
account = Mock(Account)
account.balance.returns(100)

// GOOD - Use the real object
account = Account(balance: 100)
```

### Mock Types

**Dummy**: Placeholder, never used
```
// Just filling a parameter
user = DummyUser()
order.process(user: user)  // user is ignored
```

**Stub**: Returns canned answers
```
emailService = Stub()
emailService.send().returns(true)
```

**Spy**: Records how it was used
```
analytics = Spy()
page.view()
assert analytics.track.calledWith("page_view", {page: "home"})
```

**Mock**: Pre-programmed expectations
```
database = Mock()
database.expect.query("SELECT * FROM users").returns([])
database.verify()  // Fails if not called as expected
```

**Fake**: Working implementation (lightweight)
```
database = InMemoryDatabase()  // Real behavior, no I/O
database.insert(user)
assert database.count() == 1
```

### Mocking Best Practices

1. **Mock at the boundaries** - Mock the adapter, not domain logic
2. **Verify behavior, not calls** - Care about outcomes, not method invocations
3. **Use fakes over mocks** - Real behavior > stubbed responses
4. **Keep mocks simple** - Complex mocks indicate poor design
5. **Don't mock what you don't own** - Wrap third-party libraries

## Test Reliability

### Avoiding Flaky Tests

Flaky tests (pass/fail randomly) destroy confidence. Common causes:

**Timing Issues:**
```
// BAD - Race condition
button.click()
assert message.visible()  // Might not have rendered yet

// GOOD - Wait for condition
button.click()
waitFor(() => message.visible())
```

**Shared State:**
```
// BAD - Tests affect each other
globalCounter = 0

test "increment counter":
  increment()
  assert globalCounter == 1  // Fails if tests run in parallel

// GOOD - Isolated state
test "increment counter":
  counter = Counter()
  counter.increment()
  assert counter.value == 1
```

**Non-Determinism:**
```
// BAD - Random output
test "generates unique ID":
  id1 = generateID()
  id2 = generateID()
  assert id1 < id2  // Fails if IDs are random

// GOOD - Control randomness
test "generates unique ID":
  random = MockRandom(seed: 12345)
  id1 = generateID(random)
  id2 = generateID(random)
  assert id1 != id2
```

**External Dependencies:**
```
// BAD - Depends on network
test "fetch user data":
  user = api.getUser(123)
  assert user.name == "Alice"  // Fails if API is down

// GOOD - Mock the API
test "fetch user data":
  api = MockAPI()
  api.stub.getUser(123).returns({name: "Alice"})
  user = api.getUser(123)
  assert user.name == "Alice"
```

**Environment Differences:**
```
// BAD - Depends on local files
test "reads config":
  config = readFile("/etc/app/config.json")
  assert config.port == 8080

// GOOD - Provide test fixtures
test "reads config":
  config = readFile("./fixtures/config.json")
  assert config.port == 8080
```

### Deterministic Tests

**Control time:**
```
// BAD
test "expires after 24 hours":
  session = Session(createdAt: now())
  sleep(24.hours)
  assert session.expired()

// GOOD
test "expires after 24 hours":
  clock = FixedClock(time: "2024-01-01 10:00:00")
  session = Session(createdAt: clock.now())
  clock.advance(24.hours)
  assert session.expired()
```

**Control randomness:**
```
// BAD
test "shuffles deck":
  deck = Deck()
  deck.shuffle()
  assert deck.cards != [1,2,3,4,5]  // Might fail randomly

// GOOD
test "shuffles deck":
  random = SeededRandom(seed: 42)
  deck = Deck(random: random)
  deck.shuffle()
  assert deck.cards == [3,1,5,2,4]  // Predictable
```

**Control sequences:**
```
// BAD
test "generates IDs sequentially":
  id1 = UUID.generate()
  id2 = UUID.generate()
  assert id2 > id1  // UUIDs aren't sequential

// GOOD
test "generates IDs sequentially":
  generator = SequenceGenerator()
  id1 = generator.next()
  id2 = generator.next()
  assert id2 == id1 + 1
```

### Test Isolation

**Each test should:**
- Run independently
- Not depend on test order
- Clean up after itself
- Not modify shared state

**Isolation techniques:**

1. **Setup/Teardown:**
```
beforeEach:
  database = createTestDatabase()

afterEach:
  database.drop()
```

2. **Transactions:**
```
test "creates user":
  database.beginTransaction()
  user = createUser()
  assert user.exists()
  database.rollback()  // Undo changes
```

3. **Test Fixtures:**
```
test "calculates order total":
  order = fixtures.createOrder(items: [
    {price: 10, quantity: 2},
    {price: 5, quantity: 1}
  ])
  assert order.total() == 25
```

4. **Factory Functions:**
```
function createTestUser(overrides = {}):
  return User({
    name: "Test User",
    email: "test@example.com",
    ...overrides
  })

test "sends welcome email":
  user = createTestUser(email: "alice@example.com")
  welcomeUser(user)
  assert emailSent(to: "alice@example.com")
```

### CI/CD Integration

Tests should work reliably in CI environments:

**Parallel execution:**
- Tests must not share state
- Use unique database names
- Avoid fixed port numbers
- Isolate file system changes

**Timeouts:**
```
// Set realistic timeouts
test "API responds quickly":
  response = api.get("/health")
  assert response.time < 100ms
```

**Retry flaky tests (sparingly):**
```
// Last resort - fix flakiness instead
test "eventually processes queue":
  retry(times: 3, delay: 1s):
    assert queue.isEmpty()
```

**Environment detection:**
```
if isCI():
  skipTest("requires local database")
```

## Coverage Metrics

### What Coverage Means

**Code coverage**: Percentage of code executed by tests

**Types:**
- **Line coverage**: Lines executed
- **Branch coverage**: Decision branches taken
- **Function coverage**: Functions called
- **Statement coverage**: Statements executed

### What Coverage Doesn't Mean

**100% coverage ≠ bug-free code**

Coverage measures what code runs, not:
- Whether assertions are correct
- If edge cases are tested
- Whether tests are meaningful
- If requirements are met

```
// 100% line coverage, 0% confidence
function divide(a, b):
  return a / b

test "divide":
  divide(10, 2)  // Passes, but no assertion!
  divide(10, 0)  // Doesn't catch division by zero
```

### Meaningful Coverage Targets

**General guidelines:**
- Critical path: 90-100%
- Business logic: 80-90%
- Utilities/helpers: 70-80%
- Glue code: 50-60%
- UI components: 40-60%

**Focus on risk:**
```
File                   LOC    Coverage   Priority
payment_processor.py   500    95%        HIGH
user_auth.py          300    90%        HIGH
email_templates.py    200    40%        LOW
database_config.py    100    60%        MEDIUM
```

### Mutation Testing

Tests your tests by introducing bugs:

1. Change operator: `>` to `>=`
2. Change constant: `10` to `11`
3. Remove line: delete return statement
4. Run tests - do they catch it?

**Example:**
```
// Original
function isEligible(age):
  return age >= 18

// Mutation: Change >= to >
function isEligible(age):
  return age > 18

// If tests still pass, you're missing:
test "exactly 18 is eligible":
  assert isEligible(18) == true
```

**Tools:**
- Python: mutmut, cosmic-ray
- JavaScript: Stryker
- Java: PIT
- Go: go-mutesting

### Coverage Anti-Patterns

**Chasing 100%:**
```
// BAD - Testing the framework
test "Django admin loads":
  response = client.get("/admin/")
  assert response.status == 200
```

**Ignoring untested paths:**
```
// 90% coverage but error path never tested
function processPayment(amount):
  if amount <= 0:
    throw Error("Invalid amount")  // Never tested!
  return charge(amount)
```

**Gaming metrics:**
```
// BAD - Tests that don't assert anything
test "user creation":
  User.create(name: "Alice")  // No assertions!
```

## Anti-Patterns

### 1. Testing Implementation Details

**BAD:**
```
test "UserService.create calls database.insert":
  database = Mock()
  service = UserService(database)
  service.create(name: "Alice")
  assert database.insert.called
```

**GOOD:**
```
test "UserService.create persists user":
  service = UserService(database)
  user = service.create(name: "Alice")
  assert database.findByName("Alice").exists()
```

**Why:** First test breaks if you refactor to use `database.save()` instead.

### 2. Brittle Tests

**BAD:**
```
test "renders user profile":
  html = render(UserProfile, user: alice)
  assert html.contains('<div class="profile"><h1>Alice</h1></div>')
```

**GOOD:**
```
test "renders user profile":
  html = render(UserProfile, user: alice)
  assert html.findByRole("heading").text == "Alice"
```

**Why:** First test breaks with any HTML change, even if behavior is correct.

### 3. Test Interdependence

**BAD:**
```
test1 "creates user":
  user = User.create(name: "Alice")

test2 "updates user":  // Depends on test1!
  user = User.findByName("Alice")
  user.update(name: "Bob")
```

**GOOD:**
```
test "updates user":
  user = createTestUser(name: "Alice")
  user.update(name: "Bob")
  assert user.name == "Bob"
```

### 4. Overmocking

**BAD:**
```
test "order total":
  item1 = Mock()
  item1.price().returns(10)
  item2 = Mock()
  item2.price().returns(20)
  order = Mock()
  order.items().returns([item1, item2])
  calculator = OrderCalculator()
  assert calculator.total(order) == 30
```

**GOOD:**
```
test "order total":
  order = Order(items: [
    Item(price: 10),
    Item(price: 20)
  ])
  assert order.total() == 30
```

### 5. Slow Tests

**BAD:**
```
test "user registration flow":
  browser.visit("/register")
  browser.fill("email", "test@example.com")
  browser.fill("password", "password123")
  browser.click("Submit")
  sleep(5)  // Wait for email
  email = checkInbox("test@example.com")
  browser.visit(email.confirmationLink)
  assert User.findByEmail("test@example.com").confirmed
```

**GOOD:**
```
// Unit test
test "registration creates unconfirmed user":
  user = registerUser("test@example.com", "password123")
  assert user.confirmed == false

// Integration test
test "confirmation updates user status":
  user = createUser(confirmed: false, token: "abc123")
  confirmUser(token: "abc123")
  assert user.confirmed == true

// E2E test (one for happy path only)
test "complete registration flow":
  // Use API to set up state, UI for critical path only
```

### 6. Unclear Failures

**BAD:**
```
test "validates input":
  result = validate(input)
  assert result == true  // Why did it fail? What was input?
```

**GOOD:**
```
test "validates email format":
  result = validate("invalid-email")
  assert result.valid == false
  assert result.error == "Email must contain @"
```

### 7. Coverage Obsession

**BAD:**
```
// Just to hit 100% coverage
test "toString returns string":
  user = User(name: "Alice")
  assert typeof(user.toString()) == "string"
```

**GOOD:**
```
test "toString includes user name":
  user = User(name: "Alice")
  assert user.toString().contains("Alice")
```

### 8. Giant Setup

**BAD:**
```
test "processes complex order":
  // 50 lines of setup
  database = connectDatabase()
  cache = createCache()
  paymentGateway = initGateway()
  emailService = configureEmail()
  warehouse = setupWarehouse()
  inventory = loadInventory()
  // ... 44 more lines

  result = processOrder(order)
  assert result.success
```

**GOOD:**
```
test "processes complex order":
  context = createTestContext()  // Factory handles setup
  order = fixtures.complexOrder()

  result = processOrder(order, context)

  assert result.success
  assert context.warehouse.shipmentCreated(order.id)
```

## Test Suite Design Examples

### Layered Testing Strategy

```
# Domain Layer (Unit Tests)
tests/unit/
  test_order_calculator.py     # Pure business logic
  test_discount_rules.py       # Complex calculations
  test_inventory_tracker.py    # State management

# Integration Layer
tests/integration/
  test_order_workflow.py       # Service interactions
  test_payment_processing.py   # External API (mocked)
  test_email_notifications.py  # Template rendering

# E2E Layer
tests/e2e/
  test_checkout_flow.py        # Happy path only
  test_admin_dashboard.py      # Critical admin tasks
```

### Test Organization Patterns

**Pattern 1: Mirror Source Structure**
```
src/
  services/
    user_service.py
  models/
    user.py

tests/
  services/
    test_user_service.py
  models/
    test_user.py
```

**Pattern 2: Feature-Based**
```
tests/
  auth/
    test_login.py
    test_registration.py
    test_password_reset.py
  checkout/
    test_cart.py
    test_payment.py
    test_order.py
```

**Pattern 3: Test Type Grouping**
```
tests/
  unit/
    auth/
    checkout/
  integration/
    auth/
    checkout/
  e2e/
    critical_paths.py
```

### Example: Comprehensive Test Suite

```python
# tests/unit/test_order_calculator.py
class TestOrderCalculator:
    """Unit tests for order total calculations"""

    def test_empty_order_has_zero_total(self):
        order = Order(items=[])
        assert order.total() == 0

    def test_single_item_total(self):
        order = Order(items=[Item(price=10, quantity=2)])
        assert order.total() == 20

    def test_multiple_items_total(self):
        order = Order(items=[
            Item(price=10, quantity=2),
            Item(price=5, quantity=3)
        ])
        assert order.total() == 35

    def test_applies_percentage_discount(self):
        order = Order(
            items=[Item(price=100, quantity=1)],
            discount=Discount(type="percentage", value=10)
        )
        assert order.total() == 90

    def test_applies_fixed_discount(self):
        order = Order(
            items=[Item(price=100, quantity=1)],
            discount=Discount(type="fixed", value=15)
        )
        assert order.total() == 85

    def test_discount_cannot_make_total_negative(self):
        order = Order(
            items=[Item(price=10, quantity=1)],
            discount=Discount(type="fixed", value=50)
        )
        assert order.total() == 0


# tests/integration/test_order_workflow.py
class TestOrderWorkflow:
    """Integration tests for order processing"""

    def setup_method(self):
        self.db = create_test_database()
        self.service = OrderService(self.db)

    def teardown_method(self):
        self.db.close()

    def test_successful_order_flow(self):
        # Create order
        order = self.service.create_order(
            user_id=123,
            items=[{"product_id": 1, "quantity": 2}]
        )
        assert order.status == "pending"

        # Process payment (mocked gateway)
        result = self.service.process_payment(order.id)
        assert result.success

        # Verify order updated
        order = self.service.get_order(order.id)
        assert order.status == "paid"

        # Verify inventory reduced
        product = self.db.get_product(1)
        assert product.stock == original_stock - 2

    def test_failed_payment_cancels_order(self):
        order = self.service.create_order(
            user_id=123,
            items=[{"product_id": 1, "quantity": 2}]
        )

        # Simulate payment failure
        with patch('payment_gateway.charge', side_effect=PaymentError):
            result = self.service.process_payment(order.id)
            assert not result.success

        # Verify order cancelled
        order = self.service.get_order(order.id)
        assert order.status == "cancelled"

        # Verify inventory restored
        product = self.db.get_product(1)
        assert product.stock == original_stock


# tests/e2e/test_checkout.py
@pytest.mark.e2e
class TestCheckoutFlow:
    """End-to-end tests for critical user paths"""

    def test_complete_checkout_as_guest(self, browser):
        # Add item to cart
        browser.visit("/products/1")
        browser.click("Add to Cart")

        # Go to checkout
        browser.click("Cart")
        browser.click("Checkout")

        # Fill shipping info
        browser.fill("email", "guest@example.com")
        browser.fill("address", "123 Main St")
        browser.fill("city", "Springfield")

        # Submit payment
        browser.fill("card_number", "4242424242424242")
        browser.fill("expiry", "12/25")
        browser.fill("cvc", "123")
        browser.click("Place Order")

        # Verify confirmation
        assert browser.has_text("Order confirmed")
        assert browser.has_text("guest@example.com")
```

## Quick Reference

### When to Test What

| Code Type | Test Type | Coverage Target | Focus |
|-----------|-----------|-----------------|-------|
| Business logic | Unit | 90%+ | Edge cases, calculations |
| API endpoints | Integration | 80%+ | Request/response flow |
| Database queries | Integration | 70%+ | Data integrity |
| UI components | Integration | 50%+ | User interactions |
| Critical paths | E2E | 100% | Happy path only |
| Configuration | Smoke | 100% | App starts |

### Testing Checklist

Before writing tests:
- [ ] What behavior am I testing?
- [ ] What's the expected outcome?
- [ ] What edge cases matter?
- [ ] Can I test this without mocks?
- [ ] Is this the right test type?

After writing tests:
- [ ] Do tests fail when code breaks?
- [ ] Do tests pass when code works?
- [ ] Are test names descriptive?
- [ ] Can I refactor without breaking tests?
- [ ] Are tests fast enough?

### Test Smells

Watch for these warning signs:
- Tests take >1 minute to run
- Changing code breaks unrelated tests
- Tests fail randomly (flaky)
- Adding feature requires changing many tests
- Tests are more complex than code
- Can't understand test by reading name
- Need to mock many internal methods
- High coverage but bugs still slip through

## Summary

Good testing is about **risk management**, not ritual. Write tests that:

1. **Catch real bugs** - Focus on edge cases and failure modes
2. **Run fast** - Fast tests get run, slow tests get skipped
3. **Fail clearly** - Obvious what broke and where
4. **Test behavior** - Survive refactoring
5. **Provide confidence** - Sleep well knowing critical paths work

Remember: The best test suite is the one that catches bugs before users do, runs fast enough to stay green, and doesn't break when you refactor. Coverage metrics are a tool, not a goal.


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

