---
last_updated: 2026-02-25
status: active
name: clean-code-principles
description: Self-documenting code through naming, functions, and abstractions. Use when writing or reviewing code for clarity.
triggers:
  files: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.go", "**/*.rs"]
  keywords: ["refactor", "clean code", "naming", "readability", "self-documenting", "code smell", "code review", "maintainability"]
allowed-tools: Read, Write, Edit
---

# Clean Code Principles: Deep Expertise Skill

Write code that reads like well-written prose. This skill provides guidance on creating self-documenting, maintainable code through thoughtful naming, function design, and appropriate abstractions.

## Philosophy: Code as Communication

Code is read far more often than it's written. Every line you write is a message to future developers (including yourself). Clean code:

- **Reveals intent** - The "what" and "why" are obvious
- **Minimizes cognitive load** - Readers don't need to hold context
- **Prevents misunderstanding** - No ambiguity or surprises
- **Adapts to change** - Easy to modify without breaking

**The test of clean code:** Can a new team member understand this code without asking questions?

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## 1. Naming: The Foundation of Readability

### Names Reveal Intent

Names should answer: **What does this do? Why does it exist?**

**Bad: Cryptic or generic names**
```python
# What is d? What are these items?
d = 7
lst = []
for i in items:
    if i.a > d:
        lst.append(i)
```

**Good: Self-documenting names**
```python
DAYS_UNTIL_STALE = 7
active_users = []
for user in all_users:
    if user.days_since_login > DAYS_UNTIL_STALE:
        active_users.append(user)
```

### Naming Conventions by Type

| Type | Convention | Example |
|------|------------|---------|
| Variables | Nouns describing data | `user_count`, `active_orders` |
| Booleans | Questions/predicates | `is_valid`, `has_permission`, `can_edit` |
| Functions | Verbs describing action | `calculate_total()`, `send_notification()` |
| Classes | Nouns describing entity | `UserService`, `OrderProcessor` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Private | Leading underscore | `_internal_state`, `_helper_method()` |

### Name Length Guidelines

**Variables:** Length proportional to scope

```python
# Short scope = short name is OK
users = [u for u in all_users if u.active]

# Long scope = descriptive name required
authenticated_premium_users = get_users_with_subscription("premium")
```

**Functions:** Long enough to describe the action

```python
# Too short - what does it do?
def proc(data):
    pass

# Too long - excessive detail
def process_user_data_and_validate_email_and_send_welcome_notification(data):
    pass

# Just right - clear action
def onboard_new_user(user_data: dict) -> User:
    pass
```

### Avoid Meaningless Names

**Never use:**
- Single letters (except `i`, `j`, `k` for simple loops, `x`, `y` for coordinates)
- Generic names: `data`, `info`, `temp`, `result`, `stuff`, `obj`
- Number suffixes: `user1`, `user2`, `data2`
- Hungarian notation: `strName`, `intCount` (type is obvious from context)

**Transform meaningless to meaningful:**

```python
# Bad
def process(data):
    result = []
    for item in data:
        temp = transform(item)
        result.append(temp)
    return result

# Good
def normalize_user_emails(users: list[User]) -> list[User]:
    normalized_users = []
    for user in users:
        user_with_lowercase_email = normalize_email(user)
        normalized_users.append(user_with_lowercase_email)
    return normalized_users
```

### Consistency in Naming

Pick conventions and stick to them:

```python
# Inconsistent - confusing
get_user()      # Returns one
fetch_orders()  # Returns many
retrieve_data() # What's the pattern?

# Consistent - predictable
get_user()      # get_ = single item
list_orders()   # list_ = collection
find_products() # find_ = search with filter
```

---

## 2. Functions: Single Purpose, Clear Interface

### Single Responsibility Principle (SRP)

Each function does **one thing** and does it well.

**Signs a function does too much:**
- Name contains "and" or "or"
- Multiple levels of abstraction
- More than 2-3 responsibilities
- Hard to describe in one sentence

**Bad: Multiple responsibilities**
```python
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Empty order")
    if not order.customer:
        raise ValueError("No customer")

    # Calculate totals
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * 0.1
    total = subtotal + tax

    # Save to database
    db.orders.insert(order)

    # Send email
    email_service.send(
        to=order.customer.email,
        subject="Order Confirmation",
        body=f"Your order total is ${total}"
    )

    return total
```

**Good: Single responsibility each**
```python
def place_order(order: Order) -> OrderConfirmation:
    """Place a validated order and notify customer."""
    validate_order(order)
    totals = calculate_order_totals(order)
    saved_order = save_order(order, totals)
    send_order_confirmation(saved_order)
    return OrderConfirmation(order_id=saved_order.id, total=totals.total)

def validate_order(order: Order) -> None:
    """Raise ValueError if order is invalid."""
    if not order.items:
        raise ValueError("Order must have at least one item")
    if not order.customer:
        raise ValueError("Order must have a customer")

def calculate_order_totals(order: Order) -> OrderTotals:
    """Calculate subtotal, tax, and total for order."""
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * TAX_RATE
    return OrderTotals(subtotal=subtotal, tax=tax, total=subtotal + tax)

def save_order(order: Order, totals: OrderTotals) -> SavedOrder:
    """Persist order to database."""
    return db.orders.insert(order, totals)

def send_order_confirmation(order: SavedOrder) -> None:
    """Send confirmation email to customer."""
    email_service.send(
        to=order.customer.email,
        subject="Order Confirmation",
        body=render_confirmation_email(order)
    )
```

### Function Size Guidelines

**Ideal function:** 5-15 lines
**Maximum:** 20-30 lines (rare exceptions)

If a function needs scrolling to read, it's too long.

### Parameters: Fewer is Better

| Count | Assessment |
|-------|------------|
| 0-2 | Ideal |
| 3 | Acceptable |
| 4+ | Refactor needed |

**Too many parameters:**
```python
def create_user(name, email, password, role, department, manager_id,
                start_date, salary, is_contractor, permissions):
    pass
```

**Better: Use objects**
```python
@dataclass
class NewUserRequest:
    name: str
    email: str
    password: str
    role: str
    employment: EmploymentDetails
    permissions: list[str]

def create_user(request: NewUserRequest) -> User:
    pass
```

### Avoid Flag Arguments

Booleans that change behavior are code smells.

**Bad: Flag argument**
```python
def render_page(page, include_header=True):
    if include_header:
        # 50 lines of header logic
        pass
    # Rest of rendering
    pass
```

**Good: Separate functions**
```python
def render_page_with_header(page):
    render_header(page)
    render_page_content(page)

def render_page_without_header(page):
    render_page_content(page)
```

### Command-Query Separation

Functions should either:
- **Command:** Change state (return nothing)
- **Query:** Return data (no side effects)

**Bad: Mixed command-query**
```python
def set_and_get_user_status(user_id: int, status: str) -> str:
    user = db.get(user_id)
    old_status = user.status
    user.status = status
    db.save(user)
    return old_status  # Confusing: side effect + return
```

**Good: Separated**
```python
def get_user_status(user_id: int) -> str:
    """Query: returns status without changing anything."""
    return db.get(user_id).status

def set_user_status(user_id: int, status: str) -> None:
    """Command: changes status, returns nothing."""
    user = db.get(user_id)
    user.status = status
    db.save(user)
```

---

## 3. Abstractions: The Right Level

### One Level of Abstraction Per Function

Don't mix high-level and low-level operations.

**Bad: Mixed levels**
```python
def generate_report(data):
    # High level: Report structure
    report = {"title": "Monthly Report", "sections": []}

    # Low level: String manipulation
    for row in data:
        formatted_date = f"{row['date'].month}/{row['date'].day}/{row['date'].year}"
        amount_str = f"${row['amount']:,.2f}"
        report["sections"].append({"date": formatted_date, "amount": amount_str})

    # High level: Save report
    save_report_to_s3(report)
```

**Good: Consistent abstraction**
```python
def generate_monthly_report(data: list[Transaction]) -> Report:
    """Generate and save monthly financial report."""
    transactions = format_transactions(data)
    report = build_report(title="Monthly Report", sections=transactions)
    save_report(report)
    return report

def format_transactions(transactions: list[Transaction]) -> list[Section]:
    """Convert raw transactions to report sections."""
    return [
        Section(
            date=format_date(t.date),
            amount=format_currency(t.amount)
        )
        for t in transactions
    ]

def format_date(date: datetime) -> str:
    """Format date as MM/DD/YYYY."""
    return date.strftime("%m/%d/%Y")

def format_currency(amount: Decimal) -> str:
    """Format amount as $X,XXX.XX."""
    return f"${amount:,.2f}"
```

### Extract Till You Drop

Keep extracting until each function is at one level of abstraction.

**Heuristic:** If you can give a block of code a meaningful name, extract it.

```python
# Before: One long function
def process_payment(payment):
    # Validate
    if payment.amount <= 0:
        raise ValueError("Amount must be positive")
    if not payment.customer_id:
        raise ValueError("Customer required")

    # Check fraud
    risk_score = fraud_service.score(payment)
    if risk_score > 0.8:
        flag_for_review(payment)
        return PaymentResult(status="review")

    # Process
    result = gateway.charge(payment)
    if result.success:
        send_receipt(payment)

    return result

# After: Composed of well-named functions
def process_payment(payment: Payment) -> PaymentResult:
    """Process a customer payment with fraud checking."""
    validate_payment(payment)

    if requires_fraud_review(payment):
        return flag_for_manual_review(payment)

    result = charge_payment(payment)

    if result.success:
        send_payment_receipt(payment)

    return result
```

### Avoid Premature Abstraction

Don't create abstractions until you need them.

**Rule of Three:** Wait until you have 3 similar cases before abstracting.

**Too early:**
```python
# Only one use case, but created complex abstraction
class AbstractPaymentProcessor(ABC):
    @abstractmethod
    def process(self, payment): pass

class StripePaymentProcessor(AbstractPaymentProcessor):
    def process(self, payment):
        stripe.charge(payment)

# Just use directly!
def process_payment(payment):
    stripe.charge(payment)
```

**Right time (3+ use cases):**
```python
# Now we have Stripe, PayPal, and Square
class PaymentProcessor(Protocol):
    def charge(self, amount: Decimal, token: str) -> ChargeResult: ...

class StripeProcessor:
    def charge(self, amount: Decimal, token: str) -> ChargeResult:
        return stripe.charge(amount, token)

class PayPalProcessor:
    def charge(self, amount: Decimal, token: str) -> ChargeResult:
        return paypal.charge(amount, token)

def process_payment(processor: PaymentProcessor, payment: Payment) -> ChargeResult:
    return processor.charge(payment.amount, payment.token)
```

---

## 4. Comments: When Code Isn't Enough

### The Best Comment is No Comment

If you need a comment, first try to make the code self-explanatory.

**Bad: Comment explains unclear code**
```python
# Check if user can edit
if u.r == 1 or (u.r == 2 and u.d == d.id):
    pass
```

**Good: Code explains itself**
```python
def user_can_edit_document(user: User, document: Document) -> bool:
    is_admin = user.role == Role.ADMIN
    is_document_owner = user.role == Role.EDITOR and user.department_id == document.department_id
    return is_admin or is_document_owner
```

### When Comments ARE Valuable

**1. Explain WHY, not WHAT**
```python
# WHAT (bad - obvious from code)
# Increment counter by 1
counter += 1

# WHY (good - explains intent)
# Retry with exponential backoff to avoid overwhelming the API
delay = min(base_delay * (2 ** attempt), max_delay)
```

**2. Warn about consequences**
```python
# WARNING: This query is expensive. Only call for admin users.
# Consider caching for non-admin use cases.
def get_full_audit_log() -> list[AuditEntry]:
    pass
```

**3. Explain complex algorithms**
```python
def calculate_optimal_route(locations: list[Location]) -> Route:
    """
    Uses modified Dijkstra's algorithm with traffic weighting.

    The algorithm prioritizes routes with consistent traffic over
    shorter routes with unpredictable congestion, based on research
    showing this reduces average arrival time by 15%.

    See: https://example.com/routing-paper for details.
    """
    pass
```

**4. Document public APIs**
```python
def create_subscription(
    customer_id: str,
    plan_id: str,
    trial_days: int = 14
) -> Subscription:
    """
    Create a new subscription for a customer.

    Args:
        customer_id: The unique identifier for the customer
        plan_id: The subscription plan to enroll in
        trial_days: Number of free trial days (default: 14)

    Returns:
        The created Subscription object

    Raises:
        CustomerNotFoundError: If customer_id doesn't exist
        PlanNotFoundError: If plan_id doesn't exist
        ActiveSubscriptionError: If customer already has active subscription
    """
    pass
```

### Comments to Avoid

**1. Redundant comments**
```python
# Bad: Says what code already says
# Set the user's name
user.name = name

# Set the user's email
user.email = email
```

**2. Commented-out code**
```python
# Bad: Delete it or keep it, don't comment
# old_implementation()
# def deprecated_function():
#     pass
new_implementation()
```

**3. Journal comments**
```python
# Bad: Use git for history
# 2024-01-15: Fixed bug in validation
# 2024-01-20: Added email field
# 2024-02-01: Refactored by John
```

**4. Noise comments**
```python
# Bad: Adds no value
# Constructor
def __init__(self):
    pass

# Default value
default = 0
```

---

## 5. Code Organization

### Vertical Density

Related code should be close together.

**Bad: Related code scattered**
```python
class OrderService:
    def __init__(self):
        self.db = Database()

    def _validate_items(self, items):
        pass

    def get_order(self, order_id):  # Unrelated to create_order
        pass

    def _calculate_total(self, items):
        pass

    def create_order(self, items):  # Uses _validate and _calculate
        self._validate_items(items)
        total = self._calculate_total(items)
        pass
```

**Good: Related code grouped**
```python
class OrderService:
    def __init__(self):
        self.db = Database()

    # Order creation group
    def create_order(self, items):
        self._validate_items(items)
        total = self._calculate_total(items)
        pass

    def _validate_items(self, items):
        pass

    def _calculate_total(self, items):
        pass

    # Order retrieval group
    def get_order(self, order_id):
        pass
```

### The Newspaper Metaphor

Structure code like a newspaper article:
1. **Headline** (class/function name) - Most important
2. **Lead** (public methods) - High-level overview
3. **Details** (private methods) - Supporting details at bottom

```python
class ReportGenerator:
    """Generate and distribute monthly reports."""  # Headline

    # Public interface (lead)
    def generate_and_send_report(self, month: date) -> Report:
        data = self._fetch_report_data(month)
        report = self._build_report(data)
        self._distribute_report(report)
        return report

    # Private implementation (details)
    def _fetch_report_data(self, month: date) -> ReportData:
        pass

    def _build_report(self, data: ReportData) -> Report:
        pass

    def _distribute_report(self, report: Report) -> None:
        pass
```

### File Organization

**One concept per file.** If a file has multiple unrelated classes or functions, split it.

```
# Bad: Everything in one file
services.py  # 2000 lines with UserService, OrderService, PaymentService

# Good: Organized by domain
services/
    __init__.py
    user_service.py
    order_service.py
    payment_service.py
```

---

## 6. Error Handling

### Exceptions Over Return Codes

**Bad: Return codes**
```python
def create_user(data):
    if not data.get("email"):
        return -1  # What does -1 mean?
    if not is_valid_email(data["email"]):
        return -2  # What does -2 mean?
    # ... create user
    return 0  # Success?
```

**Good: Exceptions**
```python
def create_user(data: dict) -> User:
    if not data.get("email"):
        raise ValueError("Email is required")
    if not is_valid_email(data["email"]):
        raise ValidationError("Invalid email format")
    return User.create(data)
```

### Use Specific Exceptions

**Bad: Generic exception**
```python
if not user:
    raise Exception("User not found")
```

**Good: Specific exception**
```python
class UserNotFoundError(Exception):
    """Raised when a requested user does not exist."""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

if not user:
    raise UserNotFoundError(user_id)
```

### Don't Return Null

Null forces callers to check for null everywhere.

**Bad: Return null**
```python
def find_user(email: str) -> User | None:
    user = db.query(User).filter_by(email=email).first()
    return user  # Caller must check for None

# Caller
user = find_user("test@example.com")
if user:  # Must remember to check!
    print(user.name)
```

**Good: Return empty or raise**
```python
# Option 1: Raise exception
def get_user(email: str) -> User:
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise UserNotFoundError(email)
    return user

# Option 2: Return Optional with clear name
def find_user_or_none(email: str) -> User | None:
    return db.query(User).filter_by(email=email).first()

# Option 3: Return default
def get_user_or_guest(email: str) -> User:
    user = db.query(User).filter_by(email=email).first()
    return user or GuestUser()
```

---

## 7. Code Smells and Refactoring

### Common Code Smells

| Smell | Symptom | Solution |
|-------|---------|----------|
| **Long Method** | Can't fit on screen | Extract functions |
| **Long Parameter List** | 4+ parameters | Create parameter object |
| **Duplicated Code** | Copy-paste patterns | Extract common function |
| **Feature Envy** | Method uses more of another class's data | Move method to that class |
| **Data Clumps** | Same data always passed together | Create class for the data |
| **Primitive Obsession** | Using primitives for domain concepts | Create value objects |
| **Shotgun Surgery** | One change requires many file edits | Consolidate related code |
| **Divergent Change** | One class changed for many reasons | Split into focused classes |

### Refactoring Patterns

**Extract Variable:**
```python
# Before
if user.subscription.plan.price > 100 and user.subscription.status == "active":
    pass

# After
is_premium_subscriber = (
    user.subscription.plan.price > 100
    and user.subscription.status == "active"
)
if is_premium_subscriber:
    pass
```

**Extract Function:**
```python
# Before
def process_order(order):
    # 20 lines of validation
    if not order.items: ...
    for item in order.items: ...

    # 20 lines of pricing
    subtotal = ...
    tax = ...

    # 20 lines of saving
    db.save(...)

# After
def process_order(order):
    validate_order(order)
    totals = calculate_totals(order)
    save_order(order, totals)
```

**Replace Conditional with Polymorphism:**
```python
# Before
def calculate_shipping(order):
    if order.type == "standard":
        return 5.99
    elif order.type == "express":
        return 15.99
    elif order.type == "overnight":
        return 29.99

# After
class ShippingMethod(Protocol):
    def calculate_cost(self) -> Decimal: ...

class StandardShipping:
    def calculate_cost(self) -> Decimal:
        return Decimal("5.99")

class ExpressShipping:
    def calculate_cost(self) -> Decimal:
        return Decimal("15.99")
```

---

## Quick Reference: Clean Code Checklist

### Naming
- [ ] Names reveal intent
- [ ] No cryptic abbreviations
- [ ] Consistent conventions
- [ ] No meaningless names (data, info, temp)
- [ ] Pronounceable names

### Functions
- [ ] Do one thing
- [ ] 5-15 lines (max 30)
- [ ] 0-3 parameters
- [ ] No flag arguments
- [ ] Command or query, not both

### Abstraction
- [ ] One level per function
- [ ] No premature abstraction
- [ ] DRY applied appropriately
- [ ] Clear interfaces

### Comments
- [ ] Explain why, not what
- [ ] No redundant comments
- [ ] No commented-out code
- [ ] Public API documented

### Organization
- [ ] Related code grouped
- [ ] Public before private
- [ ] One concept per file
- [ ] Clear file structure

### Error Handling
- [ ] Exceptions over return codes
- [ ] Specific exception types
- [ ] No null returns (when avoidable)
- [ ] Error messages are helpful

---

Clean code isn't about perfection—it's about empathy for the humans who will read your code. Every choice should make the next person's job easier. When in doubt, optimize for readability over cleverness. The best code is code that doesn't need explanation.


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

