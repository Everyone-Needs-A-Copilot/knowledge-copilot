---
last_updated: 2026-02-25
status: active
name: pytest-patterns
description: Python testing with pytest - fixtures, parametrization, mocking, async testing. Use when writing Python tests.
triggers:
  files: ["**/test_*.py", "**/conftest.py", "**/tests/**/*.py"]
  keywords: ["fixture", "parametrize", "mark", "conftest", "monkeypatch", "mock", "pytest-asyncio", "coverage", "pytest"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Pytest Patterns

## Overview

Master Python testing with pytest: the most powerful testing framework for Python, emphasizing clarity, composability, and maintainability. This skill covers idiomatic pytest patterns for writing tests that are fast, reliable, and easy to understand.

Pytest's philosophy: tests should be simple Python functions with minimal boilerplate. Power comes from fixtures, parametrization, and a rich plugin ecosystem.


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Core Principles

### 1. Arrange-Act-Assert (AAA)

Every test follows three clear phases:

```python
def test_user_creation():
    # Arrange - Set up test data and dependencies
    username = "testuser"
    email = "test@example.com"

    # Act - Execute the behavior being tested
    user = create_user(username=username, email=email)

    # Assert - Verify the outcome
    assert user.username == username
    assert user.email == email
    assert user.is_active is True
```

**Why this matters:**
- Visual separation improves readability
- Easy to identify what's being tested (the Act phase should be 1-2 lines)
- Failures are immediately understandable

### 2. Test Isolation

Each test must be independent and idempotent:

```python
# BAD - Tests depend on each other
def test_create_user():
    global user
    user = create_user("alice")

def test_user_profile():  # Depends on previous test
    assert user.username == "alice"

# GOOD - Each test is independent
def test_create_user():
    user = create_user("alice")
    assert user.username == "alice"

def test_user_profile():
    user = create_user("alice")
    assert user.username == "alice"
```

**Why this matters:**
- Tests can run in any order
- Parallel execution is possible
- Failures are localized

### 3. Meaningful Names

Test names should describe the behavior being tested and the expected outcome:

```python
# BAD - Generic names
def test_user():
    ...

def test_user_2():
    ...

# GOOD - Descriptive names
def test_user_creation_with_valid_email_succeeds():
    ...

def test_user_creation_with_invalid_email_raises_validation_error():
    ...

def test_inactive_user_cannot_login():
    ...
```

**Naming patterns:**
- `test_<system_under_test>_<condition>_<expected_outcome>`
- `test_<action>_when_<condition>_then_<outcome>`
- Use underscores for readability (not camelCase)

### 4. Single Assertion Per Concept

Prefer testing one concept per test, but multiple assertions on the same concept are fine:

```python
# GOOD - Multiple assertions on same concept
def test_user_creation_sets_all_fields():
    user = create_user(username="alice", email="alice@example.com")
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None

# BETTER - Use parametrize for different scenarios
@pytest.mark.parametrize("username,email,expected_error", [
    ("", "valid@example.com", "Username cannot be empty"),
    ("alice", "invalid-email", "Invalid email format"),
    ("a" * 256, "valid@example.com", "Username too long"),
])
def test_user_creation_validation_errors(username, email, expected_error):
    with pytest.raises(ValidationError, match=expected_error):
        create_user(username=username, email=email)
```

## Fixture Patterns

Fixtures are pytest's killer feature: reusable test setup that's composable, explicit, and automatic.

### Basic Fixtures

```python
import pytest

@pytest.fixture
def user():
    """Provide a test user."""
    return User(username="testuser", email="test@example.com")

def test_user_has_username(user):
    assert user.username == "testuser"

def test_user_has_email(user):
    assert user.email == "test@example.com"
```

**Key points:**
- Fixtures are functions decorated with `@pytest.fixture`
- Tests request fixtures by parameter name
- Each test gets a fresh fixture instance (default scope)

### Fixture Scopes

Control when fixtures are created and torn down:

```python
@pytest.fixture(scope="function")  # Default - new instance per test
def user():
    return User(username="testuser")

@pytest.fixture(scope="class")  # One instance per test class
def database_schema():
    db = Database()
    db.create_schema()
    yield db
    db.drop_schema()

@pytest.fixture(scope="module")  # One instance per test module
def api_client():
    return APIClient(base_url="http://localhost:8000")

@pytest.fixture(scope="session")  # One instance per test session
def docker_containers():
    """Start containers once for entire test session."""
    containers = start_docker_compose()
    yield containers
    stop_docker_compose()
```

**Scope selection:**
- `function` - Fast, isolated, no side effects (default)
- `class` - Shared state across test class
- `module` - Expensive setup (database schema, API client)
- `session` - Very expensive setup (Docker containers, test data)

**Warning:** Wider scopes risk test coupling. Use sparingly.

### Fixture Composition

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def database():
    """Database connection."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def user_repository(database):
    """User repository with database."""
    return UserRepository(database)

@pytest.fixture
def user(user_repository):
    """Persisted test user."""
    user = user_repository.create(username="testuser")
    yield user
    user_repository.delete(user.id)

def test_user_retrieval(user, user_repository):
    # user fixture created the user
    retrieved = user_repository.get(user.id)
    assert retrieved.username == "testuser"
```

**Dependency graph:**
```
database → user_repository → user
```

pytest automatically resolves the dependency chain.

### Factory Fixtures

Return a factory function for flexible test data:

```python
@pytest.fixture
def user_factory():
    """Factory for creating test users."""
    def create_user(username="testuser", email="test@example.com", **kwargs):
        return User(username=username, email=email, **kwargs)
    return create_user

def test_multiple_users(user_factory):
    alice = user_factory(username="alice")
    bob = user_factory(username="bob")

    assert alice.username == "alice"
    assert bob.username == "bob"
```

**When to use:**
- Need multiple instances in one test
- Different variations needed per test
- Complex object creation with many parameters

### Parametrized Fixtures

Fixtures that run multiple times with different values:

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request):
    """Test against multiple database backends."""
    db = Database(backend=request.param)
    db.connect()
    yield db
    db.disconnect()

def test_user_creation(database):
    # This test runs 3 times: once per database backend
    user = database.create_user("testuser")
    assert user.username == "testuser"
```

**Result:** One test function, three test executions.

**Use for:**
- Testing multiple implementations (SQLite vs Postgres)
- Compatibility testing (Python 3.9 vs 3.10 vs 3.11)
- Cross-browser testing (Chrome, Firefox, Safari)

### Autouse Fixtures

Automatically run for every test (use sparingly):

```python
@pytest.fixture(autouse=True)
def reset_database():
    """Ensure clean database state before each test."""
    Database.truncate_all_tables()

@pytest.fixture(autouse=True, scope="session")
def setup_logging():
    """Configure logging for test session."""
    logging.basicConfig(level=logging.DEBUG)
```

**When to use:**
- Essential cleanup/setup that EVERY test needs
- Environment configuration
- Logging setup

**Warning:** Autouse fixtures run even when not needed. Prefer explicit fixture requests.

### conftest.py Organization

Share fixtures across tests via `conftest.py`:

```
tests/
├── conftest.py           # Shared across all tests
├── unit/
│   ├── conftest.py       # Shared across unit tests
│   ├── test_models.py
│   └── test_services.py
└── integration/
    ├── conftest.py       # Shared across integration tests
    ├── test_api.py
    └── test_database.py
```

**Root conftest.py:**
```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def database_url():
    """Database URL for all tests."""
    return "postgresql://localhost/test_db"

@pytest.fixture
def database(database_url):
    """Database connection."""
    db = Database(database_url)
    db.connect()
    yield db
    db.disconnect()
```

**Integration-specific conftest.py:**
```python
# tests/integration/conftest.py
import pytest

@pytest.fixture(scope="module")
def api_client(database):
    """API client with real database."""
    return APIClient(database=database)
```

**Key points:**
- Fixtures in conftest.py are automatically discovered
- More specific conftest.py files override parent fixtures
- Organize by test type (unit/integration/e2e)

## Test Organization

### Directory Structure

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── models.py
│       ├── services.py
│       └── api.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── conftest.py
│   │   ├── test_models.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── conftest.py
│   │   ├── test_api.py
│   │   └── test_database.py
│   └── e2e/
│       ├── conftest.py
│       └── test_user_journey.py
└── pytest.ini
```

**Naming conventions:**
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- Test classes: `Test*` (no `__init__`)

### Test Markers

Categorize tests for selective execution:

```python
import pytest

@pytest.mark.unit
def test_user_model():
    """Fast unit test."""
    user = User(username="alice")
    assert user.username == "alice"

@pytest.mark.integration
def test_user_creation_with_database(database):
    """Integration test with database."""
    user = database.create_user("alice")
    assert user.id is not None

@pytest.mark.slow
@pytest.mark.integration
def test_bulk_user_import(database):
    """Slow integration test."""
    users = database.bulk_create([...])
    assert len(users) == 1000

@pytest.mark.skip(reason="Feature not implemented yet")
def test_user_deletion():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_pattern_matching():
    match user:
        case User(username="alice"):
            assert True
```

**pytest.ini configuration:**
```ini
[pytest]
markers =
    unit: Fast unit tests with no external dependencies
    integration: Integration tests with database/API
    slow: Tests that take >1s to run
    smoke: Critical path smoke tests
```

**Running marked tests:**
```bash
pytest -m unit              # Run only unit tests
pytest -m "not slow"        # Skip slow tests
pytest -m "integration and not slow"  # Integration tests, but not slow ones
```

### Parametrize for DRY Tests

Test multiple scenarios without code duplication:

```python
@pytest.mark.parametrize("username,email,expected_valid", [
    ("alice", "alice@example.com", True),
    ("bob", "bob@example.com", True),
    ("", "test@example.com", False),
    ("alice", "invalid-email", False),
    ("a" * 256, "test@example.com", False),
])
def test_user_validation(username, email, expected_valid):
    user = User(username=username, email=email)
    assert user.is_valid() == expected_valid
```

**Multiple parameters:**
```python
@pytest.mark.parametrize("status_code", [200, 201, 204])
@pytest.mark.parametrize("method", ["GET", "POST", "PUT"])
def test_api_responses(method, status_code, api_client):
    # Runs 3 x 3 = 9 times
    response = api_client.request(method, f"/test/{status_code}")
    assert response.status_code == status_code
```

**With IDs for readable output:**
```python
@pytest.mark.parametrize("user_data,expected_error", [
    ({"username": ""}, "Username cannot be empty"),
    ({"username": "a" * 256}, "Username too long"),
    ({"email": "invalid"}, "Invalid email format"),
], ids=["empty-username", "long-username", "invalid-email"])
def test_user_validation_errors(user_data, expected_error):
    with pytest.raises(ValidationError, match=expected_error):
        create_user(**user_data)
```

**Test output:**
```
test_user_validation_errors[empty-username] PASSED
test_user_validation_errors[long-username] PASSED
test_user_validation_errors[invalid-email] PASSED
```

## Mocking Patterns

Mocking isolates the system under test by replacing dependencies with controlled fakes.

### pytest-mock (mocker fixture)

Prefer `pytest-mock` over `unittest.mock` for automatic cleanup:

```python
def test_user_service_calls_repository(mocker):
    # Arrange
    mock_repository = mocker.Mock()
    mock_repository.get_user.return_value = User(username="alice")
    service = UserService(repository=mock_repository)

    # Act
    user = service.get_user_by_id(123)

    # Assert
    mock_repository.get_user.assert_called_once_with(123)
    assert user.username == "alice"
```

**Key methods:**
- `mocker.Mock()` - Create mock object
- `mocker.patch()` - Replace object/function
- `mocker.spy()` - Wrap real object to track calls

### Patching Strategies

**Where to patch matters:**

```python
# my_app/services.py
from my_app.database import Database

class UserService:
    def get_user(self, user_id):
        db = Database()
        return db.query(user_id)
```

```python
# tests/test_services.py
def test_user_service(mocker):
    # BAD - Patches the original module
    mocker.patch("my_app.database.Database")

    # GOOD - Patches where it's imported
    mocker.patch("my_app.services.Database")

    service = UserService()
    service.get_user(123)
```

**Rule:** Patch where the object is used, not where it's defined.

### Mock Return Values and Side Effects

```python
def test_user_service_with_return_value(mocker):
    mock_db = mocker.Mock()
    mock_db.query.return_value = User(username="alice")

    service = UserService(db=mock_db)
    user = service.get_user(123)

    assert user.username == "alice"

def test_user_service_with_exception(mocker):
    mock_db = mocker.Mock()
    mock_db.query.side_effect = DatabaseError("Connection failed")

    service = UserService(db=mock_db)
    with pytest.raises(DatabaseError):
        service.get_user(123)

def test_user_service_with_multiple_calls(mocker):
    mock_db = mocker.Mock()
    mock_db.query.side_effect = [
        User(username="alice"),
        User(username="bob"),
        DatabaseError("Connection failed"),
    ]

    service = UserService(db=mock_db)
    assert service.get_user(1).username == "alice"
    assert service.get_user(2).username == "bob"
    with pytest.raises(DatabaseError):
        service.get_user(3)
```

### Monkeypatch for Environment and Attributes

Use `monkeypatch` fixture for modifying environment, attributes, and dictionary items:

```python
def test_service_with_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    service = APIService()  # Reads API_KEY from environment
    assert service.api_key == "test-key-123"

def test_service_with_modified_attribute(monkeypatch):
    monkeypatch.setattr("my_app.services.MAX_RETRIES", 1)
    service = RetryService()
    assert service.max_retries == 1

def test_service_with_dict_modification(monkeypatch):
    config = {"timeout": 30}
    monkeypatch.setitem(config, "timeout", 5)
    assert config["timeout"] == 5
```

**Cleanup is automatic** - all changes are reverted after the test.

### When to Mock vs Use Real Objects

**Mock when:**
- External API calls (HTTP, database, filesystem)
- Expensive operations (image processing, ML inference)
- Non-deterministic behavior (random, time, network)
- Hard to test edge cases (network timeout, disk full)

**Use real objects when:**
- Pure functions with no side effects
- Simple data structures
- Business logic calculations
- Mocking would be more complex than using real object

```python
# GOOD - Mock external API
def test_weather_service(mocker):
    mock_api = mocker.patch("my_app.services.weather_api.get_forecast")
    mock_api.return_value = {"temp": 72, "condition": "sunny"}

    service = WeatherService()
    forecast = service.get_forecast("New York")
    assert forecast.temperature == 72

# GOOD - Use real object for pure logic
def test_temperature_converter():
    # No mock needed - pure function
    celsius = convert_fahrenheit_to_celsius(72)
    assert celsius == 22.2
```

### Mock Verification

```python
def test_user_service_calls_repository_correctly(mocker):
    mock_repository = mocker.Mock()
    service = UserService(repository=mock_repository)

    service.create_user("alice", "alice@example.com")

    # Verify call happened
    mock_repository.create.assert_called_once()

    # Verify call arguments
    mock_repository.create.assert_called_once_with(
        username="alice",
        email="alice@example.com"
    )

    # Verify call count
    assert mock_repository.create.call_count == 1

    # Verify no other calls
    mock_repository.delete.assert_not_called()
```

## Async Testing

Use `pytest-asyncio` for testing async code:

```python
import pytest

@pytest.mark.asyncio
async def test_async_user_creation():
    user = await create_user_async("alice")
    assert user.username == "alice"
```

### Async Fixtures

```python
@pytest.fixture
async def async_database():
    """Async database connection."""
    db = await AsyncDatabase.connect()
    yield db
    await db.disconnect()

@pytest.mark.asyncio
async def test_user_repository(async_database):
    user = await async_database.create_user("alice")
    assert user.username == "alice"
```

### Testing Background Tasks

```python
@pytest.mark.asyncio
async def test_background_task_execution(mocker):
    task_executed = False

    async def background_task():
        nonlocal task_executed
        await asyncio.sleep(0.1)
        task_executed = True

    # Start background task
    task = asyncio.create_task(background_task())

    # Wait for completion
    await task

    assert task_executed is True
```

### Mocking Async Functions

```python
@pytest.mark.asyncio
async def test_async_service_with_mock(mocker):
    mock_api = mocker.AsyncMock()
    mock_api.fetch_user.return_value = {"username": "alice"}

    service = UserService(api=mock_api)
    user = await service.get_user(123)

    mock_api.fetch_user.assert_called_once_with(123)
    assert user["username"] == "alice"
```

## Database Testing

### Transaction Rollback Pattern

Keep tests fast by rolling back transactions instead of recreating database:

```python
@pytest.fixture(scope="module")
def database():
    """Module-scoped database connection."""
    db = Database("postgresql://localhost/test_db")
    db.create_schema()
    yield db
    db.drop_schema()

@pytest.fixture
def db_session(database):
    """Function-scoped session with automatic rollback."""
    connection = database.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_user_creation(db_session):
    user = User(username="alice")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    # Transaction rolls back after test - user is not persisted
```

**Benefits:**
- Tests run 10-100x faster (no schema recreation)
- Tests remain isolated (rollback removes all changes)
- Supports parallel test execution (each test gets own transaction)

### Factory Pattern with factory_boy

Generate test data with realistic variation:

```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    is_active = True
    created_at = factory.LazyFunction(datetime.utcnow)

class PostFactory(factory.Factory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    content = factory.Faker("text")
    author = factory.SubFactory(UserFactory)

def test_post_creation():
    post = PostFactory(title="Custom Title")

    assert post.title == "Custom Title"
    assert post.author.username.startswith("user")
    assert "@example.com" in post.author.email

def test_multiple_posts():
    posts = PostFactory.create_batch(10)
    assert len(posts) == 10
    assert len(set(p.title for p in posts)) == 10  # All unique
```

**Benefits:**
- Realistic test data with randomization
- Reduces test brittleness (not tied to specific values)
- Easy to override specific attributes
- Supports relationships and complex objects

### Test Data Builders

Custom builders for complex domain objects:

```python
class UserBuilder:
    def __init__(self):
        self.username = "testuser"
        self.email = "test@example.com"
        self.is_active = True
        self.roles = []

    def with_username(self, username):
        self.username = username
        return self

    def with_email(self, email):
        self.email = email
        return self

    def inactive(self):
        self.is_active = False
        return self

    def with_role(self, role):
        self.roles.append(role)
        return self

    def build(self):
        return User(
            username=self.username,
            email=self.email,
            is_active=self.is_active,
            roles=self.roles,
        )

def test_inactive_user_cannot_login():
    user = UserBuilder().inactive().build()
    assert user.can_login() is False

def test_admin_user_has_permissions():
    user = UserBuilder().with_role("admin").build()
    assert user.has_permission("delete_users") is True
```

**Benefits:**
- Fluent API for readable test setup
- Encapsulates complex object creation
- Documents valid object configurations

## Coverage

### pytest-cov Configuration

```ini
# pytest.ini
[pytest]
addopts =
    --cov=src/myapp
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

**Running with coverage:**
```bash
pytest --cov=src/myapp                    # Coverage report
pytest --cov=src/myapp --cov-report=html  # HTML report
pytest --cov=src/myapp --cov-report=term-missing  # Missing lines
```

### What to Measure

**Prioritize coverage for:**
- Business logic (services, models)
- Critical paths (authentication, payment)
- Error handling and edge cases

**Don't obsess over:**
- Generated code
- Third-party libraries
- Configuration files
- Simple property getters/setters

### Coverage Exclusions

```python
# .coveragerc
[run]
omit =
    */tests/*
    */migrations/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    # Exclude pragma statements
    pragma: no cover

    # Exclude defensive assertions
    raise AssertionError
    raise NotImplementedError

    # Exclude debug code
    if __name__ == .__main__.:

    # Exclude type checking
    if TYPE_CHECKING:
```

```python
# Using pragma in code
def feature_under_development():
    raise NotImplementedError  # pragma: no cover

def complex_edge_case():
    if extremely_rare_condition:  # pragma: no cover
        handle_edge_case()
```

### Coverage Anti-patterns

**Don't chase 100% coverage:**
```python
# BAD - Testing implementation details
def test_internal_method():
    obj = MyClass()
    result = obj._internal_helper_method()
    assert result is not None

# GOOD - Test public interface
def test_public_behavior():
    obj = MyClass()
    result = obj.public_method()
    assert result == expected_value
```

**Coverage doesn't mean quality:**
```python
# BAD - 100% coverage, 0% value
def test_user_creation():
    user = User(username="alice")
    assert True  # This passes but tests nothing

# GOOD - Meaningful assertions
def test_user_creation():
    user = User(username="alice")
    assert user.username == "alice"
    assert user.is_active is True
    assert user.created_at is not None
```

## Anti-Patterns

### 1. Dependent Tests

**BAD:**
```python
# Global state shared between tests
user = None

def test_create_user():
    global user
    user = create_user("alice")

def test_user_profile():  # Depends on previous test
    assert user.username == "alice"
```

**GOOD:**
```python
@pytest.fixture
def user():
    return create_user("alice")

def test_create_user(user):
    assert user.username == "alice"

def test_user_profile(user):
    assert user.username == "alice"
```

### 2. Over-Mocking

**BAD:**
```python
def test_calculate_order_total(mocker):
    # Mocking pure logic defeats the purpose of testing
    mock_item = mocker.Mock()
    mock_item.price = 10
    mock_item.quantity = 2

    mocker.patch("my_app.models.Item.calculate_subtotal", return_value=20)

    order = Order(items=[mock_item])
    assert order.total == 20  # We're testing the mock, not the code!
```

**GOOD:**
```python
def test_calculate_order_total():
    # Test real logic with real objects
    item = Item(price=10, quantity=2)
    order = Order(items=[item])
    assert order.total == 20
```

**Rule:** Only mock external dependencies, not business logic.

### 3. Slow Tests

**BAD:**
```python
def test_user_service():
    # Recreate database for every test
    db = Database()
    db.create_schema()

    user = db.create_user("alice")
    assert user.username == "alice"

    db.drop_schema()
```

**GOOD:**
```python
@pytest.fixture(scope="module")
def database():
    db = Database()
    db.create_schema()
    yield db
    db.drop_schema()

@pytest.fixture
def db_session(database):
    # Use transaction rollback for speed
    session = database.begin_transaction()
    yield session
    session.rollback()

def test_user_service(db_session):
    user = db_session.create_user("alice")
    assert user.username == "alice"
```

### 4. Testing Implementation Details

**BAD:**
```python
def test_user_service_implementation(mocker):
    service = UserService()
    # Spying on private methods
    spy = mocker.spy(service, '_validate_username')

    service.create_user("alice")

    spy.assert_called_once()  # Brittle - breaks on refactoring
```

**GOOD:**
```python
def test_user_service_validates_username():
    service = UserService()

    # Test behavior, not implementation
    with pytest.raises(ValidationError):
        service.create_user("")  # Invalid username
```

### 5. Unclear Test Failure Messages

**BAD:**
```python
def test_user_creation():
    user = create_user("alice")
    assert user  # What failed? User is None? Missing attribute?
```

**GOOD:**
```python
def test_user_creation():
    user = create_user("alice")

    assert user is not None, "User creation returned None"
    assert user.username == "alice", f"Expected username 'alice', got '{user.username}'"
    assert user.is_active is True, "User should be active by default"
```

### 6. Shared Mutable Fixtures

**BAD:**
```python
@pytest.fixture(scope="module")
def user_list():
    return []  # Mutable list shared across tests

def test_add_user(user_list):
    user_list.append("alice")
    assert len(user_list) == 1

def test_another_add(user_list):
    user_list.append("bob")
    assert len(user_list) == 1  # FAILS - list has 2 items from previous test
```

**GOOD:**
```python
@pytest.fixture
def user_list():
    return []  # New list for each test

def test_add_user(user_list):
    user_list.append("alice")
    assert len(user_list) == 1

def test_another_add(user_list):
    user_list.append("bob")
    assert len(user_list) == 1  # PASSES - fresh list
```

## Code Examples

### Complete Test Suite Example

```python
# tests/conftest.py
import pytest
from my_app.database import Database
from my_app.models import User

@pytest.fixture(scope="session")
def database():
    """Session-scoped database with schema."""
    db = Database("postgresql://localhost/test_db")
    db.create_schema()
    yield db
    db.drop_schema()

@pytest.fixture
def db_session(database):
    """Function-scoped session with rollback."""
    connection = database.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def user_factory(db_session):
    """Factory for creating test users."""
    def create_user(username="testuser", email="test@example.com", **kwargs):
        user = User(username=username, email=email, **kwargs)
        db_session.add(user)
        db_session.commit()
        return user
    return create_user
```

```python
# tests/unit/test_models.py
import pytest
from my_app.models import User, ValidationError

class TestUserModel:
    """Unit tests for User model."""

    def test_user_creation_with_valid_data(self):
        user = User(username="alice", email="alice@example.com")
        assert user.username == "alice"
        assert user.email == "alice@example.com"
        assert user.is_active is True

    @pytest.mark.parametrize("username,email,expected_error", [
        ("", "test@example.com", "Username cannot be empty"),
        ("alice", "invalid-email", "Invalid email format"),
        ("a" * 256, "test@example.com", "Username too long"),
    ], ids=["empty-username", "invalid-email", "long-username"])
    def test_user_validation_errors(self, username, email, expected_error):
        with pytest.raises(ValidationError, match=expected_error):
            User(username=username, email=email).validate()

    def test_user_str_representation(self):
        user = User(username="alice", email="alice@example.com")
        assert str(user) == "User(username='alice')"
```

```python
# tests/integration/test_user_repository.py
import pytest
from my_app.repositories import UserRepository
from my_app.models import User

@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)

class TestUserRepository:
    """Integration tests for UserRepository."""

    def test_create_user(self, user_repository):
        # Arrange
        username = "alice"
        email = "alice@example.com"

        # Act
        user = user_repository.create(username=username, email=email)

        # Assert
        assert user.id is not None
        assert user.username == username
        assert user.email == email

    def test_get_user_by_id(self, user_repository, user_factory):
        # Arrange
        created_user = user_factory(username="alice")

        # Act
        retrieved_user = user_repository.get(created_user.id)

        # Assert
        assert retrieved_user.id == created_user.id
        assert retrieved_user.username == "alice"

    def test_get_nonexistent_user_returns_none(self, user_repository):
        user = user_repository.get(99999)
        assert user is None

    def test_update_user(self, user_repository, user_factory):
        # Arrange
        user = user_factory(username="alice")

        # Act
        user_repository.update(user.id, username="alice_updated")
        updated_user = user_repository.get(user.id)

        # Assert
        assert updated_user.username == "alice_updated"

    def test_delete_user(self, user_repository, user_factory):
        # Arrange
        user = user_factory(username="alice")

        # Act
        user_repository.delete(user.id)
        deleted_user = user_repository.get(user.id)

        # Assert
        assert deleted_user is None
```

```python
# tests/integration/test_user_service.py
import pytest
from my_app.services import UserService
from my_app.models import ValidationError

@pytest.fixture
def user_service(db_session):
    return UserService(db_session)

class TestUserService:
    """Integration tests for UserService."""

    def test_create_user_success(self, user_service):
        user = user_service.create_user(
            username="alice",
            email="alice@example.com"
        )

        assert user.id is not None
        assert user.username == "alice"

    def test_create_user_with_duplicate_username_fails(
        self, user_service, user_factory
    ):
        # Arrange
        user_factory(username="alice")

        # Act & Assert
        with pytest.raises(ValidationError, match="Username already exists"):
            user_service.create_user(
                username="alice",
                email="different@example.com"
            )

    @pytest.mark.slow
    def test_bulk_user_creation(self, user_service):
        # Arrange
        users_data = [
            {"username": f"user{i}", "email": f"user{i}@example.com"}
            for i in range(100)
        ]

        # Act
        users = user_service.bulk_create(users_data)

        # Assert
        assert len(users) == 100
        assert all(u.id is not None for u in users)
```

```python
# tests/unit/test_user_service_mocked.py
import pytest
from my_app.services import UserService
from my_app.repositories import UserRepository

def test_user_service_calls_repository(mocker):
    # Arrange
    mock_repository = mocker.Mock(spec=UserRepository)
    mock_repository.create.return_value = mocker.Mock(
        id=1,
        username="alice",
        email="alice@example.com"
    )
    service = UserService(repository=mock_repository)

    # Act
    user = service.create_user(username="alice", email="alice@example.com")

    # Assert
    mock_repository.create.assert_called_once_with(
        username="alice",
        email="alice@example.com"
    )
    assert user.username == "alice"

def test_user_service_handles_repository_error(mocker):
    # Arrange
    mock_repository = mocker.Mock(spec=UserRepository)
    mock_repository.create.side_effect = DatabaseError("Connection failed")
    service = UserService(repository=mock_repository)

    # Act & Assert
    with pytest.raises(DatabaseError):
        service.create_user(username="alice", email="alice@example.com")
```

```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from my_app.main import app

@pytest.fixture
def client():
    return TestClient(app)

class TestUserAPI:
    """Integration tests for User API."""

    def test_create_user_endpoint(self, client):
        response = client.post(
            "/users",
            json={"username": "alice", "email": "alice@example.com"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "alice"
        assert "id" in data

    def test_get_user_endpoint(self, client, user_factory):
        # Arrange
        user = user_factory(username="alice")

        # Act
        response = client.get(f"/users/{user.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "alice"

    def test_get_nonexistent_user_returns_404(self, client):
        response = client.get("/users/99999")
        assert response.status_code == 404

    @pytest.mark.parametrize("invalid_data,expected_error", [
        ({"username": ""}, "Username cannot be empty"),
        ({"username": "alice"}, "Email is required"),
        ({"email": "alice@example.com"}, "Username is required"),
    ])
    def test_create_user_validation(self, client, invalid_data, expected_error):
        response = client.post("/users", json=invalid_data)

        assert response.status_code == 422
        assert expected_error in response.text
```

### Async Test Example

```python
# tests/integration/test_async_service.py
import pytest
from my_app.services import AsyncUserService

@pytest.mark.asyncio
class TestAsyncUserService:
    """Tests for async user service."""

    async def test_create_user_async(self, async_db_session):
        service = AsyncUserService(async_db_session)

        user = await service.create_user(
            username="alice",
            email="alice@example.com"
        )

        assert user.id is not None
        assert user.username == "alice"

    async def test_fetch_user_from_api(self, mocker):
        # Arrange
        mock_api = mocker.AsyncMock()
        mock_api.fetch_user.return_value = {"username": "alice"}
        service = AsyncUserService(api=mock_api)

        # Act
        user = await service.fetch_remote_user(123)

        # Assert
        mock_api.fetch_user.assert_awaited_once_with(123)
        assert user["username"] == "alice"
```

## Quick Reference

### Essential pytest Commands

```bash
# Run all tests
pytest

# Run specific file
pytest tests/unit/test_models.py

# Run specific test
pytest tests/unit/test_models.py::test_user_creation

# Run tests matching pattern
pytest -k "user_creation"

# Run marked tests
pytest -m unit
pytest -m "not slow"

# Run with coverage
pytest --cov=src/myapp

# Run in parallel (requires pytest-xdist)
pytest -n auto

# Show print output
pytest -s

# Show local variables on failure
pytest -l

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run in verbose mode
pytest -v
```

### Common pytest.ini Settings

```ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    unit: Fast unit tests
    integration: Integration tests with database
    slow: Tests that take >1s
    smoke: Critical path smoke tests

# Coverage
addopts =
    --strict-markers
    --cov=src/myapp
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    -ra

# Asyncio
asyncio_mode = auto
```

### Fixture Cheat Sheet

```python
# Basic fixture
@pytest.fixture
def user():
    return User(username="testuser")

# Fixture with teardown
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

# Fixture with scope
@pytest.fixture(scope="session")
def config():
    return load_config()

# Parametrized fixture
@pytest.fixture(params=["sqlite", "postgres"])
def database(request):
    return Database(backend=request.param)

# Factory fixture
@pytest.fixture
def user_factory():
    def create(**kwargs):
        return User(**kwargs)
    return create

# Autouse fixture
@pytest.fixture(autouse=True)
def reset_database():
    Database.truncate()
```

### Assertion Patterns

```python
# Basic assertions
assert value == expected
assert value is not None
assert value in collection
assert isinstance(value, User)

# Exception assertions
with pytest.raises(ValueError):
    function_that_raises()

with pytest.raises(ValueError, match="Invalid input"):
    function_that_raises()

# Approximate comparisons
assert value == pytest.approx(expected, rel=0.01)

# Custom failure messages
assert value == expected, f"Expected {expected}, got {value}"
```



## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

## Guidelines

1. **Test behavior, not implementation** - Tests should verify what the code does, not how it does it
2. **One concept per test** - Each test should verify a single behavior or scenario
3. **Use descriptive names** - Test name should describe the scenario and expected outcome
4. **Arrange-Act-Assert** - Clear structure makes tests readable
5. **Fast tests are good tests** - Use mocks, transaction rollback, and appropriate fixture scopes
6. **Fixtures over setup/teardown** - Pytest fixtures are more flexible and composable
7. **Parametrize for variations** - DRY principle applies to tests too
8. **Mock external dependencies** - But use real objects for business logic
9. **Test edge cases** - Empty inputs, null values, boundary conditions
10. **Coverage is a guide, not a goal** - High coverage doesn't guarantee quality

## References

- pytest documentation: https://docs.pytest.org/
- pytest-mock: https://pytest-mock.readthedocs.io/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/
- factory_boy: https://factoryboy.readthedocs.io/
- Testing patterns: `~/.claude/knowledge/03-ai-enabling/02-patterns/testing/`
