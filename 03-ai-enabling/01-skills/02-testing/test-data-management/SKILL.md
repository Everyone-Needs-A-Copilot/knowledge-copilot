---
last_updated: 2026-02-25
status: active
name: test-data-management
description: Test data strategy - fixtures, factories, seeding, cleanup. Use when managing test data for reliable, isolated tests.
triggers:
  files: ["**/tests/**", "**/*.test.*", "**/*.spec.*", "**/test_*", "**/fixtures/**", "**/factories/**", "**/seeds/**"]
  keywords: ["test data", "test fixture", "factory", "seed data", "test database", "data builder", "test isolation", "mock data"]
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Edit
---

This skill guides test data management strategies for reliable, maintainable tests. Create isolated test environments with predictable data using fixtures, factories, and proper cleanup.

The user provides testing requirements: a test suite needing data strategy, data dependencies between tests, or flaky tests due to data issues. They may include context about database type, test framework, or data complexity.

## Why Test Data Management Matters

**Bad test data causes:**
- Flaky tests (pass sometimes, fail others)
- Test pollution (tests affect each other)
- Slow tests (creating too much data)
- Maintenance burden (hardcoded values everywhere)
- Environment-dependent failures

**Good test data provides:**
- Isolated tests (each test has its own data)
- Fast tests (minimal necessary data)
- Readable tests (clear what data means)
- Maintainable tests (change data in one place)


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Test Data Strategies

### Strategy Comparison

| Strategy | Best For | Pros | Cons |
|----------|----------|------|------|
| Fixtures | Static reference data | Simple, predictable | Rigid, can grow large |
| Factories | Dynamic test-specific data | Flexible, isolated | More setup code |
| Builders | Complex object construction | Readable, chainable | Boilerplate |
| Seeds | Database baseline | Realistic data | Slow, less isolated |

### When to Use Each

```
Fixture: Reference data that rarely changes
  → Countries, status codes, configuration

Factory: Data created fresh per test
  → Users, orders, transactions

Builder: Complex objects with many fields
  → API requests, domain entities

Seed: Realistic baseline for integration tests
  → Sample users, products, categories
```

## Fixtures

### JSON Fixtures

```json
// fixtures/users.json
{
  "admin": {
    "id": 1,
    "email": "admin@test.com",
    "role": "admin",
    "active": true
  },
  "regular": {
    "id": 2,
    "email": "user@test.com",
    "role": "user",
    "active": true
  },
  "inactive": {
    "id": 3,
    "email": "inactive@test.com",
    "role": "user",
    "active": false
  }
}
```

```python
# Using fixtures
def test_admin_can_delete_user(fixtures):
    admin = fixtures["users"]["admin"]
    target = fixtures["users"]["regular"]

    result = delete_user(admin, target.id)

    assert result.success
```

### YAML Fixtures

```yaml
# fixtures/products.yml
laptop:
  id: 1
  name: "MacBook Pro"
  price: 1999.00
  category: electronics
  in_stock: true

out_of_stock_item:
  id: 2
  name: "Rare Widget"
  price: 99.00
  category: widgets
  in_stock: false

free_item:
  id: 3
  name: "Freebie"
  price: 0.00
  category: promotions
  in_stock: true
```

### Fixture Best Practices

| Do | Don't |
|----|-------|
| Use meaningful names | Use `user1`, `user2` |
| Keep fixtures minimal | Create every possible variation |
| Group by domain | One giant fixture file |
| Document special cases | Assume meaning is obvious |

## Factories

### Python Factory Pattern

```python
# factories/user_factory.py
from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class User:
    id: str
    email: str
    name: str
    role: str
    active: bool

class UserFactory:
    _counter = 0

    @classmethod
    def create(
        cls,
        email: Optional[str] = None,
        name: Optional[str] = None,
        role: str = "user",
        active: bool = True
    ) -> User:
        cls._counter += 1
        return User(
            id=str(uuid.uuid4()),
            email=email or f"user{cls._counter}@test.com",
            name=name or f"Test User {cls._counter}",
            role=role,
            active=active
        )

    @classmethod
    def create_admin(cls, **kwargs) -> User:
        return cls.create(role="admin", **kwargs)

    @classmethod
    def create_inactive(cls, **kwargs) -> User:
        return cls.create(active=False, **kwargs)
```

```python
# Using factories
def test_user_creation():
    user = UserFactory.create()
    assert user.email.endswith("@test.com")
    assert user.active is True

def test_admin_permissions():
    admin = UserFactory.create_admin()
    assert admin.role == "admin"

def test_with_custom_data():
    user = UserFactory.create(
        email="specific@example.com",
        name="Specific User"
    )
    assert user.email == "specific@example.com"
```

### JavaScript Factory Pattern

```javascript
// factories/userFactory.js
let counter = 0;

const createUser = (overrides = {}) => {
  counter++;
  return {
    id: `user-${counter}`,
    email: `user${counter}@test.com`,
    name: `Test User ${counter}`,
    role: 'user',
    active: true,
    createdAt: new Date(),
    ...overrides
  };
};

const createAdmin = (overrides = {}) =>
  createUser({ role: 'admin', ...overrides });

const createInactiveUser = (overrides = {}) =>
  createUser({ active: false, ...overrides });

module.exports = { createUser, createAdmin, createInactiveUser };
```

```javascript
// Using factories
describe('User permissions', () => {
  it('grants admin access', () => {
    const admin = createAdmin();
    expect(hasAdminAccess(admin)).toBe(true);
  });

  it('denies regular user access', () => {
    const user = createUser();
    expect(hasAdminAccess(user)).toBe(false);
  });
});
```

### Factory with Associations

```python
class OrderFactory:
    @classmethod
    def create(
        cls,
        user: Optional[User] = None,
        items: Optional[List[Item]] = None,
        status: str = "pending"
    ) -> Order:
        return Order(
            id=str(uuid.uuid4()),
            user=user or UserFactory.create(),
            items=items or [ItemFactory.create()],
            status=status,
            created_at=datetime.now()
        )

    @classmethod
    def create_with_multiple_items(cls, count: int = 3, **kwargs) -> Order:
        items = [ItemFactory.create() for _ in range(count)]
        return cls.create(items=items, **kwargs)

    @classmethod
    def create_shipped(cls, **kwargs) -> Order:
        return cls.create(status="shipped", **kwargs)
```

## Builder Pattern

### Fluent Builder

```python
class UserBuilder:
    def __init__(self):
        self._data = {
            "id": str(uuid.uuid4()),
            "email": "default@test.com",
            "name": "Default User",
            "role": "user",
            "active": True,
            "settings": {}
        }

    def with_email(self, email: str) -> "UserBuilder":
        self._data["email"] = email
        return self

    def with_name(self, name: str) -> "UserBuilder":
        self._data["name"] = name
        return self

    def as_admin(self) -> "UserBuilder":
        self._data["role"] = "admin"
        return self

    def inactive(self) -> "UserBuilder":
        self._data["active"] = False
        return self

    def with_settings(self, **settings) -> "UserBuilder":
        self._data["settings"].update(settings)
        return self

    def build(self) -> User:
        return User(**self._data)
```

```python
# Using builder
def test_complex_user_scenario():
    user = (
        UserBuilder()
        .with_email("admin@company.com")
        .with_name("Admin User")
        .as_admin()
        .with_settings(theme="dark", notifications=True)
        .build()
    )

    assert user.role == "admin"
    assert user.settings["theme"] == "dark"
```

### Request Builder

```python
class APIRequestBuilder:
    def __init__(self, method: str, path: str):
        self._method = method
        self._path = path
        self._headers = {}
        self._body = None
        self._params = {}

    def with_auth(self, token: str) -> "APIRequestBuilder":
        self._headers["Authorization"] = f"Bearer {token}"
        return self

    def with_header(self, key: str, value: str) -> "APIRequestBuilder":
        self._headers[key] = value
        return self

    def with_json(self, data: dict) -> "APIRequestBuilder":
        self._headers["Content-Type"] = "application/json"
        self._body = data
        return self

    def with_params(self, **params) -> "APIRequestBuilder":
        self._params.update(params)
        return self

    def build(self) -> Request:
        return Request(
            method=self._method,
            path=self._path,
            headers=self._headers,
            body=self._body,
            params=self._params
        )
```

## Database Test Data

### Setup and Teardown

```python
import pytest
from database import db

@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test."""
    yield
    db.session.rollback()
    # Or truncate tables
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

@pytest.fixture
def sample_user():
    """Create a user that exists in the database."""
    user = UserFactory.create()
    db.session.add(user)
    db.session.commit()
    return user
```

### Transaction Rollback Strategy

```python
@pytest.fixture
def db_session():
    """Provide a transactional scope for tests."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_user_creation(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.flush()

    assert user.id is not None
    # Automatically rolled back after test
```

### Data Seeding

```python
# seeds/development.py
def seed_development_data():
    """Seed database with development data."""
    # Create admin user
    admin = User(
        email="admin@example.com",
        role="admin",
        password=hash_password("admin123")
    )
    db.session.add(admin)

    # Create sample categories
    categories = [
        Category(name="Electronics"),
        Category(name="Books"),
        Category(name="Clothing"),
    ]
    db.session.add_all(categories)

    # Create sample products
    products = [
        Product(name="Laptop", category=categories[0], price=999),
        Product(name="Python Book", category=categories[1], price=49),
    ]
    db.session.add_all(products)

    db.session.commit()
```

## Test Data Isolation

### Isolation Strategies

| Strategy | How It Works | Best For |
|----------|--------------|----------|
| Transaction rollback | Wrap test in transaction, rollback after | Unit tests |
| Truncate tables | Delete all data between tests | Integration tests |
| Separate database | Each test run gets fresh DB | Parallel tests |
| Schema per test | Isolated schema namespace | Complex isolation |

### Ensuring Isolation

```python
class TestUserService:
    def setup_method(self):
        """Run before each test."""
        self.user = UserFactory.create()
        db.session.add(self.user)
        db.session.commit()

    def teardown_method(self):
        """Run after each test."""
        db.session.query(User).delete()
        db.session.commit()

    def test_update_user(self):
        update_user(self.user.id, name="New Name")
        refreshed = db.session.query(User).get(self.user.id)
        assert refreshed.name == "New Name"

    def test_delete_user(self):
        delete_user(self.user.id)
        assert db.session.query(User).get(self.user.id) is None
```

### Avoiding Test Pollution

```python
# BAD: Shared mutable state
shared_user = UserFactory.create()

def test_one():
    shared_user.name = "Modified"  # Pollutes other tests

def test_two():
    assert shared_user.name == "Test User"  # Fails!

# GOOD: Fresh data per test
def test_one():
    user = UserFactory.create()
    user.name = "Modified"
    # Only affects this test

def test_two():
    user = UserFactory.create()
    assert user.name.startswith("Test User")  # Passes
```

## Mock Data for External Services

### API Response Mocks

```python
# mocks/payment_responses.py
SUCCESSFUL_PAYMENT = {
    "id": "pay_123",
    "status": "succeeded",
    "amount": 1000,
    "currency": "usd",
    "created": 1609459200
}

FAILED_PAYMENT = {
    "id": "pay_456",
    "status": "failed",
    "error": {
        "code": "card_declined",
        "message": "Your card was declined."
    }
}

PENDING_PAYMENT = {
    "id": "pay_789",
    "status": "pending",
    "amount": 1000,
    "currency": "usd"
}
```

```python
# Using mock responses
def test_successful_payment(mocker):
    mocker.patch(
        "payment_service.charge",
        return_value=SUCCESSFUL_PAYMENT
    )

    result = process_order(order)

    assert result.status == "paid"

def test_failed_payment(mocker):
    mocker.patch(
        "payment_service.charge",
        return_value=FAILED_PAYMENT
    )

    result = process_order(order)

    assert result.status == "payment_failed"
    assert "declined" in result.error
```

## Generating Test Data

### Fake Data Libraries

```python
from faker import Faker

fake = Faker()

def create_realistic_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": fake.phone_number(),
        "company": fake.company(),
        "job": fake.job()
    }

def create_realistic_order():
    return {
        "id": fake.uuid4(),
        "customer": create_realistic_user(),
        "items": [
            {"name": fake.word(), "price": fake.pydecimal(min_value=1, max_value=100)}
            for _ in range(random.randint(1, 5))
        ],
        "created_at": fake.date_time_this_month()
    }
```

### Deterministic Fake Data

```python
from faker import Faker

# Seeded faker for reproducible tests
fake = Faker()
Faker.seed(12345)

def test_user_display():
    # Always generates same data
    user = create_realistic_user()
    # User will have same name/email every run
    assert "John" in user["name"] or True  # Predictable
```

## Quick Reference

### Test Data Checklist

Before writing tests:
- [ ] What data does this test need?
- [ ] Is data shared or isolated?
- [ ] How is data cleaned up?
- [ ] Are there dependencies between data?

For each test:
- [ ] Create only necessary data
- [ ] Use factories for dynamic data
- [ ] Use fixtures for static data
- [ ] Clean up after test

### Data Strategy Decision Tree

```
Is data static reference data?
  Yes → Use fixtures
  No ↓

Does each test need unique data?
  Yes → Use factories
  No ↓

Is the object complex with many fields?
  Yes → Use builder pattern
  No → Use simple factory
```

### Common Patterns

| Pattern | Use Case |
|---------|----------|
| `UserFactory.create()` | Need any valid user |
| `UserFactory.create_admin()` | Need user with admin role |
| `UserBuilder().as_admin().build()` | Need customized admin |
| `fixtures["users"]["admin"]` | Need consistent admin data |

## Summary

Good test data management enables reliable tests:

1. **Use factories** for test-specific data
2. **Use fixtures** for static reference data
3. **Use builders** for complex objects
4. **Isolate tests** with transactions or cleanup
5. **Generate realistically** with faker when needed
6. **Keep data minimal** - only what the test needs
7. **Name meaningfully** - data should explain itself
8. **Clean up properly** - no test pollution


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

