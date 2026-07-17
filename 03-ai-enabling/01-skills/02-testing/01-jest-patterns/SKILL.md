---
last_updated: 2026-02-25
status: active
name: jest-patterns
description: Jest testing - mocking, snapshots, async testing, coverage. Use when writing JavaScript/TypeScript tests.
triggers:
  files: ["**/*.test.js", "**/*.spec.js", "**/*.test.ts", "**/*.spec.ts", "**/jest.config.*"]
  keywords: ["jest", "describe", "it", "expect", "mock", "spy", "snapshot", "beforeEach", "afterEach"]
allowed-tools: Read, Write, Edit
---

# Jest Patterns - Deep Expertise Skill

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Test Structure](#test-structure)
3. [Matchers](#matchers)
4. [Mocking](#mocking)
5. [Async Testing](#async-testing)
6. [Snapshot Testing](#snapshot-testing)
7. [Setup and Teardown](#setup-and-teardown)
8. [Testing React Components](#testing-react-components)
9. [Testing Hooks](#testing-hooks)
10. [Module Mocking](#module-mocking)
11. [Timer Mocks](#timer-mocks)
12. [Coverage Configuration](#coverage-configuration)
13. [Anti-Patterns](#anti-patterns)
14. [Best Practices](#best-practices)

---


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Core Concepts

### Jest Philosophy

Jest is a delightful JavaScript testing framework with a focus on simplicity. It works out of the box with minimal configuration and provides:

- **Zero config**: Works with most JavaScript projects
- **Isolated tests**: Each test has its own global state
- **Great error messages**: Clear feedback when tests fail
- **Snapshot testing**: Capture and track component output
- **Built-in coverage**: No additional tools needed
- **Mocking support**: Comprehensive mocking capabilities

### Test Organization

```typescript
// Good: Clear test organization
describe('UserService', () => {
  describe('createUser', () => {
    it('creates a new user with valid data', () => {
      // Test implementation
    });

    it('throws error when email is invalid', () => {
      // Test implementation
    });

    it('hashes password before storing', () => {
      // Test implementation
    });
  });

  describe('getUserById', () => {
    it('returns user when found', () => {
      // Test implementation
    });

    it('returns null when user not found', () => {
      // Test implementation
    });
  });
});
```

### AAA Pattern (Arrange-Act-Assert)

```typescript
it('calculates total price with discount', () => {
  // Arrange: Set up test data and dependencies
  const cart = {
    items: [
      { price: 100, quantity: 2 },
      { price: 50, quantity: 1 }
    ],
    discountCode: 'SAVE10'
  };
  const discountService = new DiscountService();

  // Act: Execute the code under test
  const total = calculateTotal(cart, discountService);

  // Assert: Verify the outcome
  expect(total).toBe(225); // (100*2 + 50*1) * 0.9
});
```

---

## Test Structure

### Describe Blocks

```typescript
// Nested describe blocks for logical grouping
describe('Authentication', () => {
  describe('login', () => {
    describe('with valid credentials', () => {
      it('returns auth token', () => {});
      it('sets user session', () => {});
    });

    describe('with invalid credentials', () => {
      it('throws UnauthorizedError', () => {});
      it('logs failed attempt', () => {});
    });

    describe('with expired password', () => {
      it('requires password reset', () => {});
      it('sends reset email', () => {});
    });
  });

  describe('logout', () => {
    it('clears user session', () => {});
    it('invalidates auth token', () => {});
  });
});
```

### Test Naming Conventions

```typescript
// Good: Descriptive test names that read like requirements
describe('ShoppingCart', () => {
  it('adds item to cart when addItem is called', () => {});
  it('increases quantity when adding duplicate item', () => {});
  it('removes item completely when quantity reaches zero', () => {});
  it('applies discount code only once per order', () => {});
  it('throws error when discount code is invalid', () => {});
});

// Bad: Vague or technical test names
describe('ShoppingCart', () => {
  it('test1', () => {}); // Too vague
  it('addItem function', () => {}); // Not descriptive
  it('should work', () => {}); // Meaningless
});
```

### Test Grouping with describe.each

```typescript
describe.each([
  { role: 'admin', canDelete: true, canEdit: true },
  { role: 'editor', canDelete: false, canEdit: true },
  { role: 'viewer', canDelete: false, canEdit: false }
])('User permissions for $role', ({ role, canDelete, canEdit }) => {
  it(`${canDelete ? 'can' : 'cannot'} delete content`, () => {
    const user = createUser(role);
    expect(user.hasPermission('delete')).toBe(canDelete);
  });

  it(`${canEdit ? 'can' : 'cannot'} edit content`, () => {
    const user = createUser(role);
    expect(user.hasPermission('edit')).toBe(canEdit);
  });
});
```

### Test Focusing and Skipping

```typescript
// Focus on specific tests during development
describe('Feature', () => {
  it.only('runs this test only', () => {
    // Only this test will run
  });

  it('skips this test', () => {
    // This test is skipped
  });
});

// Skip tests temporarily
describe('Feature', () => {
  it.skip('temporarily disabled test', () => {
    // Test is skipped
  });

  it.todo('write test for edge case');
});

// Skip entire suites
describe.skip('Feature under development', () => {
  it('test 1', () => {});
  it('test 2', () => {});
});
```

---

## Matchers

### Basic Matchers

```typescript
describe('Basic matchers', () => {
  it('equality matchers', () => {
    expect(2 + 2).toBe(4); // Strict equality (===)
    expect({ name: 'John' }).toEqual({ name: 'John' }); // Deep equality
    expect([1, 2, 3]).toStrictEqual([1, 2, 3]); // Strict equality including undefined
  });

  it('truthiness matchers', () => {
    expect(null).toBeNull();
    expect(undefined).toBeUndefined();
    expect(true).toBeDefined();
    expect(1).toBeTruthy();
    expect(0).toBeFalsy();
  });

  it('number matchers', () => {
    expect(10).toBeGreaterThan(5);
    expect(5).toBeLessThan(10);
    expect(10).toBeGreaterThanOrEqual(10);
    expect(5).toBeLessThanOrEqual(5);
    expect(0.1 + 0.2).toBeCloseTo(0.3); // For floating point
  });

  it('string matchers', () => {
    expect('Hello World').toMatch(/World/);
    expect('test@example.com').toMatch(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
    expect('abc').not.toMatch(/xyz/);
  });

  it('array and iterable matchers', () => {
    const list = ['apple', 'banana', 'orange'];
    expect(list).toContain('banana');
    expect(list).toHaveLength(3);
    expect(new Set([1, 2, 3])).toContain(2);
  });

  it('object matchers', () => {
    const user = {
      id: 1,
      name: 'John',
      email: 'john@example.com',
      roles: ['user', 'admin']
    };

    expect(user).toHaveProperty('email');
    expect(user).toHaveProperty('email', 'john@example.com');
    expect(user).toMatchObject({ name: 'John', id: 1 });
  });
});
```

### Custom Matchers

```typescript
// Define custom matchers
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () =>
          `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true
      };
    } else {
      return {
        message: () =>
          `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false
      };
    }
  },

  toBeValidEmail(received: string) {
    const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    const pass = emailRegex.test(received);
    return {
      message: () =>
        pass
          ? `expected ${received} not to be a valid email`
          : `expected ${received} to be a valid email`,
      pass
    };
  }
});

// Use custom matchers
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeWithinRange(floor: number, ceiling: number): R;
      toBeValidEmail(): R;
    }
  }
}

it('uses custom matchers', () => {
  expect(15).toBeWithinRange(10, 20);
  expect('test@example.com').toBeValidEmail();
});
```

### Asymmetric Matchers

```typescript
describe('Asymmetric matchers', () => {
  it('matches partial objects', () => {
    const user = {
      id: 123,
      name: 'John Doe',
      email: 'john@example.com',
      createdAt: new Date()
    };

    expect(user).toEqual({
      id: expect.any(Number),
      name: expect.any(String),
      email: expect.stringContaining('@'),
      createdAt: expect.any(Date)
    });
  });

  it('matches array contents', () => {
    const list = [1, 2, 3, 4, 5];

    expect(list).toEqual(
      expect.arrayContaining([2, 4])
    );

    expect(list).not.toEqual(
      expect.arrayContaining([6, 7])
    );
  });

  it('matches object properties', () => {
    const response = {
      data: {
        users: [
          { id: 1, name: 'Alice' },
          { id: 2, name: 'Bob' }
        ]
      },
      meta: {
        total: 2,
        page: 1
      }
    };

    expect(response).toEqual({
      data: {
        users: expect.arrayContaining([
          expect.objectContaining({ name: 'Alice' })
        ])
      },
      meta: expect.objectContaining({ total: 2 })
    });
  });
});
```

---

## Mocking

### Mock Functions (jest.fn)

```typescript
describe('Mock functions', () => {
  it('tracks function calls', () => {
    const mockFn = jest.fn();

    mockFn('arg1', 'arg2');
    mockFn('arg3');

    expect(mockFn).toHaveBeenCalledTimes(2);
    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
    expect(mockFn).toHaveBeenLastCalledWith('arg3');
    expect(mockFn).toHaveBeenNthCalledWith(1, 'arg1', 'arg2');
  });

  it('returns specified values', () => {
    const mockFn = jest.fn()
      .mockReturnValue(42)
      .mockReturnValueOnce(1)
      .mockReturnValueOnce(2);

    expect(mockFn()).toBe(1);
    expect(mockFn()).toBe(2);
    expect(mockFn()).toBe(42);
    expect(mockFn()).toBe(42);
  });

  it('implements custom logic', () => {
    const mockFn = jest.fn((x: number) => x * 2);

    expect(mockFn(5)).toBe(10);
    expect(mockFn).toHaveBeenCalledWith(5);
  });

  it('chains different behaviors', () => {
    const mockFn = jest.fn()
      .mockReturnValueOnce('first')
      .mockReturnValueOnce('second')
      .mockImplementationOnce(() => 'third')
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValue('success');

    expect(mockFn()).toBe('first');
    expect(mockFn()).toBe('second');
    expect(mockFn()).toBe('third');
    expect(mockFn()).rejects.toThrow('fail');
    expect(mockFn()).resolves.toBe('success');
  });
});
```

### Mock Implementation

```typescript
describe('Mock implementations', () => {
  it('mocks a service class', () => {
    class EmailService {
      send(to: string, subject: string, body: string): boolean {
        // Real implementation would send email
        return true;
      }
    }

    const mockSend = jest.fn().mockReturnValue(true);
    const mockEmailService = {
      send: mockSend
    } as EmailService;

    const notifier = new NotificationService(mockEmailService);
    notifier.notifyUser('user@example.com', 'Welcome!');

    expect(mockSend).toHaveBeenCalledWith(
      'user@example.com',
      expect.any(String),
      expect.any(String)
    );
  });

  it('mocks a callback function', () => {
    function processItems(items: string[], callback: (item: string) => void) {
      items.forEach(callback);
    }

    const mockCallback = jest.fn();
    processItems(['a', 'b', 'c'], mockCallback);

    expect(mockCallback).toHaveBeenCalledTimes(3);
    expect(mockCallback.mock.calls).toEqual([['a'], ['b'], ['c']]);
  });

  it('inspects mock call details', () => {
    const mockFn = jest.fn();

    mockFn('first', 1);
    mockFn('second', 2);

    // Access all calls
    expect(mockFn.mock.calls).toEqual([
      ['first', 1],
      ['second', 2]
    ]);

    // Access specific call arguments
    expect(mockFn.mock.calls[0][0]).toBe('first');
    expect(mockFn.mock.calls[1][1]).toBe(2);

    // Access return values
    expect(mockFn.mock.results[0].value).toBeUndefined();
  });
});
```

### Spies (jest.spyOn)

```typescript
describe('Spies', () => {
  it('spies on object methods', () => {
    const calculator = {
      add: (a: number, b: number) => a + b,
      multiply: (a: number, b: number) => a * b
    };

    const addSpy = jest.spyOn(calculator, 'add');
    const multiplySpy = jest.spyOn(calculator, 'multiply');

    calculator.add(2, 3);
    calculator.multiply(4, 5);

    expect(addSpy).toHaveBeenCalledWith(2, 3);
    expect(multiplySpy).toHaveBeenCalledWith(4, 5);

    // Restore original implementation
    addSpy.mockRestore();
    multiplySpy.mockRestore();
  });

  it('mocks and restores method behavior', () => {
    const user = {
      getName: () => 'John Doe'
    };

    const spy = jest.spyOn(user, 'getName')
      .mockReturnValue('Jane Smith');

    expect(user.getName()).toBe('Jane Smith');
    expect(spy).toHaveBeenCalled();

    spy.mockRestore();
    expect(user.getName()).toBe('John Doe');
  });

  it('spies on console methods', () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

    console.log('Test message');
    console.log('Another message');

    expect(consoleSpy).toHaveBeenCalledTimes(2);
    expect(consoleSpy).toHaveBeenCalledWith('Test message');

    consoleSpy.mockRestore();
  });
});
```

### Partial Mocks

```typescript
describe('Partial mocks', () => {
  it('mocks specific methods while keeping others', () => {
    const userService = {
      getUser: (id: number) => ({ id, name: 'John' }),
      saveUser: (user: any) => user,
      deleteUser: (id: number) => true
    };

    // Mock only saveUser
    jest.spyOn(userService, 'saveUser')
      .mockImplementation(() => ({ success: true }));

    // getUser still works normally
    expect(userService.getUser(1)).toEqual({ id: 1, name: 'John' });

    // saveUser uses mock
    expect(userService.saveUser({})).toEqual({ success: true });
  });
});
```

---

## Async Testing

### Testing Promises

```typescript
describe('Promise testing', () => {
  it('resolves with async/await', async () => {
    const data = await fetchData();
    expect(data).toEqual({ name: 'John' });
  });

  it('resolves with return', () => {
    return fetchData().then(data => {
      expect(data).toEqual({ name: 'John' });
    });
  });

  it('resolves with Jest matcher', () => {
    return expect(fetchData()).resolves.toEqual({ name: 'John' });
  });

  it('rejects with async/await', async () => {
    await expect(fetchDataWithError()).rejects.toThrow('Network error');
  });

  it('rejects with Jest matcher', () => {
    return expect(fetchDataWithError()).rejects.toThrow('Network error');
  });

  it('handles multiple promises', async () => {
    const [user, posts, comments] = await Promise.all([
      fetchUser(1),
      fetchPosts(1),
      fetchComments(1)
    ]);

    expect(user).toBeDefined();
    expect(posts).toHaveLength(5);
    expect(comments).toHaveLength(10);
  });
});
```

### Testing Callbacks

```typescript
describe('Callback testing', () => {
  it('tests callback with done', (done) => {
    function callback(data: any) {
      try {
        expect(data).toEqual({ success: true });
        done();
      } catch (error) {
        done(error);
      }
    }

    fetchDataWithCallback(callback);
  });

  it('tests error callback', (done) => {
    function errorCallback(error: Error) {
      try {
        expect(error.message).toBe('Failed to fetch');
        done();
      } catch (e) {
        done(e);
      }
    }

    fetchDataWithError(errorCallback);
  });
});
```

### Mocking Async Functions

```typescript
describe('Async mocking', () => {
  it('mocks resolved promise', async () => {
    const mockFetch = jest.fn()
      .mockResolvedValue({ data: 'success' });

    const result = await mockFetch();
    expect(result).toEqual({ data: 'success' });
  });

  it('mocks rejected promise', async () => {
    const mockFetch = jest.fn()
      .mockRejectedValue(new Error('Network error'));

    await expect(mockFetch()).rejects.toThrow('Network error');
  });

  it('mocks multiple async calls', async () => {
    const mockFetch = jest.fn()
      .mockResolvedValueOnce({ page: 1 })
      .mockResolvedValueOnce({ page: 2 })
      .mockResolvedValueOnce({ page: 3 });

    const page1 = await mockFetch();
    const page2 = await mockFetch();
    const page3 = await mockFetch();

    expect(page1).toEqual({ page: 1 });
    expect(page2).toEqual({ page: 2 });
    expect(page3).toEqual({ page: 3 });
  });

  it('mocks async implementation', async () => {
    const mockFetch = jest.fn()
      .mockImplementation(async (url: string) => {
        if (url.includes('error')) {
          throw new Error('Failed');
        }
        return { url, data: 'success' };
      });

    await expect(mockFetch('/api/users')).resolves.toEqual({
      url: '/api/users',
      data: 'success'
    });

    await expect(mockFetch('/api/error')).rejects.toThrow('Failed');
  });
});
```

### Testing Race Conditions

```typescript
describe('Race condition testing', () => {
  it('handles concurrent requests', async () => {
    const cache = new Map();
    const fetchWithCache = async (key: string) => {
      if (cache.has(key)) {
        return cache.get(key);
      }
      const value = await fetch(key);
      cache.set(key, value);
      return value;
    };

    // Simulate concurrent requests
    const [result1, result2, result3] = await Promise.all([
      fetchWithCache('user:1'),
      fetchWithCache('user:1'),
      fetchWithCache('user:1')
    ]);

    expect(result1).toBe(result2);
    expect(result2).toBe(result3);
    expect(cache.size).toBe(1);
  });
});
```

---

## Snapshot Testing

### Basic Snapshots

```typescript
describe('Snapshot testing', () => {
  it('matches component snapshot', () => {
    const component = {
      type: 'div',
      props: { className: 'container' },
      children: [
        { type: 'h1', props: {}, children: ['Title'] },
        { type: 'p', props: {}, children: ['Content'] }
      ]
    };

    expect(component).toMatchSnapshot();
  });

  it('matches inline snapshot', () => {
    const user = {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com'
    };

    expect(user).toMatchInlineSnapshot(`
      {
        "email": "john@example.com",
        "id": 1,
        "name": "John Doe",
      }
    `);
  });

  it('matches property snapshot', () => {
    const user = {
      id: Math.random(),
      createdAt: new Date(),
      name: 'John Doe',
      email: 'john@example.com'
    };

    expect(user).toMatchSnapshot({
      id: expect.any(Number),
      createdAt: expect.any(Date)
    });
  });
});
```

### React Component Snapshots

```typescript
import { render } from '@testing-library/react';

describe('React snapshots', () => {
  it('matches UserCard snapshot', () => {
    const { container } = render(
      <UserCard
        name="John Doe"
        email="john@example.com"
        role="admin"
      />
    );

    expect(container).toMatchSnapshot();
  });

  it('matches different states', () => {
    const { container, rerender } = render(
      <LoadingButton loading={false}>Click me</LoadingButton>
    );

    expect(container).toMatchSnapshot('not loading');

    rerender(<LoadingButton loading={true}>Click me</LoadingButton>);
    expect(container).toMatchSnapshot('loading');
  });
});
```

### Snapshot Serializers

```typescript
// Custom serializer for dates
expect.addSnapshotSerializer({
  test: (val) => val instanceof Date,
  print: (val) => `Date("${(val as Date).toISOString()}")`
});

// Custom serializer for removing dynamic IDs
expect.addSnapshotSerializer({
  test: (val) => val && typeof val === 'object' && 'id' in val,
  print: (val, serialize) => {
    const { id, ...rest } = val as any;
    return serialize({ ...rest, id: '[ID]' });
  }
});

it('uses custom serializers', () => {
  const data = {
    id: Math.random(),
    createdAt: new Date('2024-01-01'),
    name: 'Test'
  };

  expect(data).toMatchSnapshot();
  // Snapshot will show:
  // {
  //   "createdAt": Date("2024-01-01T00:00:00.000Z"),
  //   "id": "[ID]",
  //   "name": "Test"
  // }
});
```

### Snapshot Best Practices

```typescript
describe('Snapshot best practices', () => {
  // Good: Small, focused snapshots
  it('matches button in default state', () => {
    const { getByRole } = render(<Button>Click me</Button>);
    expect(getByRole('button')).toMatchSnapshot();
  });

  // Good: Named snapshots for clarity
  it('matches modal states', () => {
    const { container, rerender } = render(<Modal open={false} />);
    expect(container).toMatchSnapshot('closed');

    rerender(<Modal open={true} />);
    expect(container).toMatchSnapshot('open');
  });

  // Bad: Snapshot of entire page
  it('matches full page', () => {
    const { container } = render(<HomePage />);
    expect(container).toMatchSnapshot(); // Too large, brittle
  });

  // Good: Snapshot specific sections
  it('matches header section', () => {
    const { getByRole } = render(<HomePage />);
    expect(getByRole('banner')).toMatchSnapshot();
  });
});
```

---

## Setup and Teardown

### Basic Lifecycle Hooks

```typescript
describe('Lifecycle hooks', () => {
  beforeAll(() => {
    // Runs once before all tests in this suite
    console.log('Setup before all tests');
  });

  afterAll(() => {
    // Runs once after all tests in this suite
    console.log('Cleanup after all tests');
  });

  beforeEach(() => {
    // Runs before each test
    console.log('Setup before each test');
  });

  afterEach(() => {
    // Runs after each test
    console.log('Cleanup after each test');
  });

  it('test 1', () => {
    expect(true).toBe(true);
  });

  it('test 2', () => {
    expect(true).toBe(true);
  });
});
```

### Database Setup/Teardown

```typescript
import { PrismaClient } from '@prisma/client';

describe('Database tests', () => {
  let prisma: PrismaClient;

  beforeAll(async () => {
    prisma = new PrismaClient();
    await prisma.$connect();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  beforeEach(async () => {
    // Clean database before each test
    await prisma.user.deleteMany();
    await prisma.post.deleteMany();
  });

  it('creates a user', async () => {
    const user = await prisma.user.create({
      data: { email: 'test@example.com', name: 'Test User' }
    });

    expect(user.email).toBe('test@example.com');
  });

  it('creates a post', async () => {
    const user = await prisma.user.create({
      data: { email: 'test@example.com', name: 'Test User' }
    });

    const post = await prisma.post.create({
      data: {
        title: 'Test Post',
        content: 'Content',
        authorId: user.id
      }
    });

    expect(post.authorId).toBe(user.id);
  });
});
```

### Test Fixtures

```typescript
describe('Test fixtures', () => {
  let testUser: User;
  let testPosts: Post[];

  beforeEach(() => {
    testUser = {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      role: 'admin'
    };

    testPosts = [
      { id: 1, title: 'Post 1', authorId: 1 },
      { id: 2, title: 'Post 2', authorId: 1 },
      { id: 3, title: 'Post 3', authorId: 1 }
    ];
  });

  it('uses test fixtures', () => {
    expect(testUser.role).toBe('admin');
    expect(testPosts).toHaveLength(3);
  });

  it('modifies fixtures independently', () => {
    testUser.role = 'user';
    expect(testUser.role).toBe('user');
  });
});
```

### Cleanup with try/finally

```typescript
describe('Resource cleanup', () => {
  it('ensures cleanup with try/finally', async () => {
    const connection = await createConnection();

    try {
      const result = await connection.query('SELECT * FROM users');
      expect(result).toBeDefined();
    } finally {
      await connection.close();
    }
  });

  it('cleans up mocks', () => {
    const spy = jest.spyOn(console, 'log');

    try {
      console.log('test');
      expect(spy).toHaveBeenCalledWith('test');
    } finally {
      spy.mockRestore();
    }
  });
});
```

---

## Testing React Components

### React Testing Library

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('UserProfile', () => {
  it('renders user information', () => {
    render(
      <UserProfile
        name="John Doe"
        email="john@example.com"
        role="admin"
      />
    );

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('admin')).toBeInTheDocument();
  });

  it('handles edit button click', async () => {
    const onEdit = jest.fn();

    render(
      <UserProfile
        name="John Doe"
        email="john@example.com"
        onEdit={onEdit}
      />
    );

    const editButton = screen.getByRole('button', { name: /edit/i });
    await userEvent.click(editButton);

    expect(onEdit).toHaveBeenCalledTimes(1);
  });

  it('validates form input', async () => {
    render(<UserForm onSubmit={jest.fn()} />);

    const emailInput = screen.getByLabelText(/email/i);
    await userEvent.type(emailInput, 'invalid-email');

    const submitButton = screen.getByRole('button', { name: /submit/i });
    await userEvent.click(submitButton);

    expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
  });
});
```

### Testing Component State

```typescript
describe('Counter component', () => {
  it('increments counter', async () => {
    render(<Counter initialValue={0} />);

    const counter = screen.getByTestId('counter-value');
    const incrementButton = screen.getByRole('button', { name: /increment/i });

    expect(counter).toHaveTextContent('0');

    await userEvent.click(incrementButton);
    expect(counter).toHaveTextContent('1');

    await userEvent.click(incrementButton);
    expect(counter).toHaveTextContent('2');
  });

  it('decrements counter', async () => {
    render(<Counter initialValue={5} />);

    const counter = screen.getByTestId('counter-value');
    const decrementButton = screen.getByRole('button', { name: /decrement/i });

    expect(counter).toHaveTextContent('5');

    await userEvent.click(decrementButton);
    expect(counter).toHaveTextContent('4');
  });

  it('resets counter', async () => {
    render(<Counter initialValue={10} />);

    const counter = screen.getByTestId('counter-value');
    const resetButton = screen.getByRole('button', { name: /reset/i });

    await userEvent.click(resetButton);
    expect(counter).toHaveTextContent('0');
  });
});
```

### Testing Conditional Rendering

```typescript
describe('ConditionalContent', () => {
  it('shows loading state', () => {
    render(<DataView loading={true} data={null} error={null} />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    expect(screen.queryByTestId('data-content')).not.toBeInTheDocument();
  });

  it('shows error state', () => {
    const error = new Error('Failed to load');
    render(<DataView loading={false} data={null} error={error} />);

    expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    expect(screen.queryByTestId('data-content')).not.toBeInTheDocument();
  });

  it('shows data when loaded', () => {
    const data = { id: 1, name: 'Test' };
    render(<DataView loading={false} data={data} error={null} />);

    expect(screen.getByTestId('data-content')).toBeInTheDocument();
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
```

### Testing Lists and Keys

```typescript
describe('UserList', () => {
  const users = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' },
    { id: 3, name: 'Charlie', email: 'charlie@example.com' }
  ];

  it('renders all users', () => {
    render(<UserList users={users} />);

    users.forEach(user => {
      expect(screen.getByText(user.name)).toBeInTheDocument();
      expect(screen.getByText(user.email)).toBeInTheDocument();
    });
  });

  it('handles empty list', () => {
    render(<UserList users={[]} />);

    expect(screen.getByText(/no users found/i)).toBeInTheDocument();
  });

  it('deletes user on button click', async () => {
    const onDelete = jest.fn();
    render(<UserList users={users} onDelete={onDelete} />);

    const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
    await userEvent.click(deleteButtons[0]);

    expect(onDelete).toHaveBeenCalledWith(1);
  });
});
```

---

## Testing Hooks

### Testing Custom Hooks

```typescript
import { renderHook, act } from '@testing-library/react';

describe('useCounter hook', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));

    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it('resets count', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(12);

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

### Testing Async Hooks

```typescript
describe('useFetch hook', () => {
  it('fetches data successfully', async () => {
    const mockData = { id: 1, name: 'Test' };
    global.fetch = jest.fn().mockResolvedValue({
      json: async () => mockData
    });

    const { result } = renderHook(() => useFetch('/api/users/1'));

    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBeNull();

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toEqual(mockData);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    const mockError = new Error('Network error');
    global.fetch = jest.fn().mockRejectedValue(mockError);

    const { result } = renderHook(() => useFetch('/api/users/1'));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toBeNull();
    expect(result.current.error).toEqual(mockError);
  });

  it('refetches data', async () => {
    const mockData1 = { id: 1, name: 'Test 1' };
    const mockData2 = { id: 1, name: 'Test 2' };

    global.fetch = jest.fn()
      .mockResolvedValueOnce({ json: async () => mockData1 })
      .mockResolvedValueOnce({ json: async () => mockData2 });

    const { result } = renderHook(() => useFetch('/api/users/1'));

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData1);
    });

    act(() => {
      result.current.refetch();
    });

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData2);
    });

    expect(global.fetch).toHaveBeenCalledTimes(2);
  });
});
```

### Testing Hooks with Context

```typescript
describe('useAuth hook', () => {
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <AuthProvider>{children}</AuthProvider>
  );

  it('provides authentication state', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
  });

  it('logs in user', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login('user@example.com', 'password');
    });

    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.user).toMatchObject({
      email: 'user@example.com'
    });
  });

  it('logs out user', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login('user@example.com', 'password');
    });

    expect(result.current.isAuthenticated).toBe(true);

    act(() => {
      result.current.logout();
    });

    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
  });
});
```

---

## Module Mocking

### Mocking Entire Modules

```typescript
// Mock entire module
jest.mock('../services/userService');

import { getUserById, createUser } from '../services/userService';

describe('UserController', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('gets user by id', async () => {
    const mockUser = { id: 1, name: 'John' };
    (getUserById as jest.Mock).mockResolvedValue(mockUser);

    const controller = new UserController();
    const result = await controller.getUser(1);

    expect(getUserById).toHaveBeenCalledWith(1);
    expect(result).toEqual(mockUser);
  });

  it('creates user', async () => {
    const newUser = { name: 'Jane', email: 'jane@example.com' };
    const createdUser = { id: 2, ...newUser };
    (createUser as jest.Mock).mockResolvedValue(createdUser);

    const controller = new UserController();
    const result = await controller.createUser(newUser);

    expect(createUser).toHaveBeenCalledWith(newUser);
    expect(result).toEqual(createdUser);
  });
});
```

### Partial Module Mocking

```typescript
jest.mock('../utils/helpers', () => ({
  ...jest.requireActual('../utils/helpers'),
  formatDate: jest.fn()
}));

import { formatDate, formatCurrency } from '../utils/helpers';

describe('Partial mocking', () => {
  it('mocks specific exports', () => {
    (formatDate as jest.Mock).mockReturnValue('2024-01-01');

    // formatDate uses mock
    expect(formatDate(new Date())).toBe('2024-01-01');

    // formatCurrency uses real implementation
    expect(formatCurrency(1000)).toBe('$1,000.00');
  });
});
```

### Mocking ES6 Classes

```typescript
jest.mock('../services/EmailService');

import { EmailService } from '../services/EmailService';

describe('EmailService mocking', () => {
  beforeEach(() => {
    (EmailService as jest.Mock).mockClear();
  });

  it('mocks class constructor', () => {
    const mockSend = jest.fn().mockResolvedValue(true);
    (EmailService as jest.Mock).mockImplementation(() => ({
      send: mockSend
    }));

    const service = new EmailService();
    service.send('test@example.com', 'Subject', 'Body');

    expect(EmailService).toHaveBeenCalledTimes(1);
    expect(mockSend).toHaveBeenCalledWith(
      'test@example.com',
      'Subject',
      'Body'
    );
  });

  it('mocks static methods', () => {
    const mockValidate = jest.fn().mockReturnValue(true);
    (EmailService as any).validateEmail = mockValidate;

    EmailService.validateEmail('test@example.com');

    expect(mockValidate).toHaveBeenCalledWith('test@example.com');
  });
});
```

### Mock Implementations Per Test

```typescript
jest.mock('../api/client');

import { apiClient } from '../api/client';

describe('Dynamic mock implementations', () => {
  it('mocks success response', async () => {
    (apiClient.get as jest.Mock).mockResolvedValueOnce({
      data: { success: true }
    });

    const result = await fetchData();
    expect(result.data.success).toBe(true);
  });

  it('mocks error response', async () => {
    (apiClient.get as jest.Mock).mockRejectedValueOnce(
      new Error('Network error')
    );

    await expect(fetchData()).rejects.toThrow('Network error');
  });

  it('mocks different responses in same test', async () => {
    (apiClient.get as jest.Mock)
      .mockResolvedValueOnce({ data: { page: 1 } })
      .mockResolvedValueOnce({ data: { page: 2 } })
      .mockResolvedValueOnce({ data: { page: 3 } });

    const page1 = await fetchData('/api/users?page=1');
    const page2 = await fetchData('/api/users?page=2');
    const page3 = await fetchData('/api/users?page=3');

    expect(page1.data.page).toBe(1);
    expect(page2.data.page).toBe(2);
    expect(page3.data.page).toBe(3);
  });
});
```

### Manual Mocks

```typescript
// __mocks__/fs.ts
const fs = {
  readFile: jest.fn(),
  writeFile: jest.fn(),
  existsSync: jest.fn(),
  mkdirSync: jest.fn()
};

export default fs;

// test file
jest.mock('fs');

import fs from 'fs';

describe('File operations', () => {
  it('reads file', async () => {
    const mockContent = 'file content';
    (fs.readFile as jest.Mock).mockImplementation(
      (path, encoding, callback) => {
        callback(null, mockContent);
      }
    );

    const content = await readFileAsync('test.txt');
    expect(content).toBe(mockContent);
  });
});
```

---

## Timer Mocks

### Fake Timers

```typescript
describe('Timer mocking', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('runs setTimeout callback', () => {
    const callback = jest.fn();

    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalledTimes(1);
  });

  it('runs multiple timers', () => {
    const callback1 = jest.fn();
    const callback2 = jest.fn();

    setTimeout(callback1, 1000);
    setTimeout(callback2, 2000);

    jest.advanceTimersByTime(1000);
    expect(callback1).toHaveBeenCalledTimes(1);
    expect(callback2).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1000);
    expect(callback2).toHaveBeenCalledTimes(1);
  });

  it('runs all timers', () => {
    const callback1 = jest.fn();
    const callback2 = jest.fn();

    setTimeout(callback1, 1000);
    setTimeout(callback2, 2000);

    jest.runAllTimers();

    expect(callback1).toHaveBeenCalledTimes(1);
    expect(callback2).toHaveBeenCalledTimes(1);
  });

  it('runs only pending timers', () => {
    const callback = jest.fn(() => {
      setTimeout(callback, 1000);
    });

    setTimeout(callback, 1000);

    jest.runOnlyPendingTimers();

    expect(callback).toHaveBeenCalledTimes(1);
  });
});
```

### Testing setInterval

```typescript
describe('setInterval mocking', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('runs interval callback multiple times', () => {
    const callback = jest.fn();

    setInterval(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(3000);

    expect(callback).toHaveBeenCalledTimes(3);
  });

  it('clears interval', () => {
    const callback = jest.fn();

    const intervalId = setInterval(callback, 1000);

    jest.advanceTimersByTime(2000);
    expect(callback).toHaveBeenCalledTimes(2);

    clearInterval(intervalId);

    jest.advanceTimersByTime(2000);
    expect(callback).toHaveBeenCalledTimes(2); // Still 2, not 4
  });
});
```

### Testing Debounce/Throttle

```typescript
describe('Debounce testing', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('debounces function calls', () => {
    const callback = jest.fn();
    const debounced = debounce(callback, 1000);

    debounced();
    debounced();
    debounced();

    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalledTimes(1);
  });

  it('throttles function calls', () => {
    const callback = jest.fn();
    const throttled = throttle(callback, 1000);

    throttled();
    throttled();
    throttled();

    expect(callback).toHaveBeenCalledTimes(1);

    jest.advanceTimersByTime(1000);

    throttled();
    expect(callback).toHaveBeenCalledTimes(2);
  });
});
```

### Testing Date.now()

```typescript
describe('Date mocking', () => {
  beforeEach(() => {
    jest.useFakeTimers();
    jest.setSystemTime(new Date('2024-01-01'));
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('mocks Date.now()', () => {
    expect(Date.now()).toBe(new Date('2024-01-01').getTime());

    jest.advanceTimersByTime(1000);

    expect(Date.now()).toBe(new Date('2024-01-01').getTime() + 1000);
  });

  it('mocks new Date()', () => {
    const date = new Date();
    expect(date.toISOString()).toBe('2024-01-01T00:00:00.000Z');
  });
});
```

---

## Coverage Configuration

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  // Coverage collection
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/__tests__/**',
    '!src/index.{js,ts}'
  ],

  // Coverage thresholds
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    },
    './src/services/': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90
    }
  },

  // Coverage reporters
  coverageReporters: ['text', 'lcov', 'html'],

  // Coverage directory
  coverageDirectory: 'coverage',

  // Test environment
  testEnvironment: 'jsdom',

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

  // Module paths
  modulePaths: ['<rootDir>/src'],

  // Transform
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest'
  },

  // Module name mapper
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
    '^@/(.*)$': '<rootDir>/src/$1'
  }
};
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2",
    "test:debug": "node --inspect-brk node_modules/.bin/jest --runInBand"
  }
}
```

### Istanbul Coverage Comments

```typescript
describe('Coverage annotations', () => {
  it('excludes code from coverage', () => {
    /* istanbul ignore next */
    if (process.env.NODE_ENV === 'development') {
      console.log('Debug info');
    }

    const result = calculateValue();
    expect(result).toBeDefined();
  });

  it('ignores unreachable code', () => {
    try {
      riskyOperation();
    } catch (error) {
      /* istanbul ignore next */
      if (error.code === 'NEVER_HAPPENS') {
        handleRareError(error);
      }
      throw error;
    }
  });
});
```

---

## Anti-Patterns

### What NOT to Do

```typescript
// ❌ Testing implementation details
it('bad: tests internal state', () => {
  const component = new MyComponent();
  expect(component._internalState).toBe('value'); // Don't access private state
});

// ✅ Test behavior instead
it('good: tests public behavior', () => {
  const { getByText } = render(<MyComponent />);
  expect(getByText('Expected Output')).toBeInTheDocument();
});

// ❌ Testing the framework
it('bad: tests React itself', () => {
  const [count, setCount] = useState(0);
  setCount(1);
  expect(count).toBe(1); // Don't test useState
});

// ✅ Test your code
it('good: tests component behavior', () => {
  const { getByText } = render(<Counter />);
  fireEvent.click(getByText('Increment'));
  expect(getByText('Count: 1')).toBeInTheDocument();
});

// ❌ Brittle selectors
it('bad: uses brittle selectors', () => {
  const { container } = render(<UserCard />);
  const element = container.querySelector('.card > div:nth-child(2) > span');
  expect(element).toHaveTextContent('John');
});

// ✅ Semantic queries
it('good: uses semantic queries', () => {
  render(<UserCard name="John" />);
  expect(screen.getByRole('heading', { name: 'John' })).toBeInTheDocument();
});

// ❌ Over-mocking
jest.mock('../utils'); // Mocks entire module unnecessarily
jest.mock('../services/userService');
jest.mock('../services/authService');
jest.mock('../services/emailService');

// ✅ Minimal mocking
// Only mock external dependencies, not your own code

// ❌ Not cleaning up mocks
describe('UserService', () => {
  it('test 1', () => {
    jest.spyOn(api, 'get').mockResolvedValue({ data: {} });
    // Mock not restored
  });

  it('test 2', () => {
    // Previous mock still active
  });
});

// ✅ Clean up after each test
describe('UserService', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });
});

// ❌ Testing multiple things
it('creates user, sends email, logs event, updates cache', async () => {
  // Too much in one test
});

// ✅ One assertion per test
it('creates user', async () => {
  const user = await createUser({ name: 'John' });
  expect(user.name).toBe('John');
});

it('sends welcome email after user creation', async () => {
  await createUser({ name: 'John' });
  expect(emailService.send).toHaveBeenCalled();
});

// ❌ Nested describes too deep
describe('Feature', () => {
  describe('Subfeature', () => {
    describe('Case', () => {
      describe('Scenario', () => {
        it('test', () => {}); // Too nested
      });
    });
  });
});

// ✅ Flat structure
describe('Feature - Subfeature', () => {
  it('handles specific scenario', () => {});
});
```

---

## Best Practices

### 1. Test Behavior, Not Implementation

```typescript
// Good: Tests what the component does
describe('LoginForm', () => {
  it('shows error when credentials are invalid', async () => {
    render(<LoginForm />);

    await userEvent.type(screen.getByLabelText(/email/i), 'invalid@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'wrong');
    await userEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(await screen.findByText(/invalid credentials/i)).toBeInTheDocument();
  });
});
```

### 2. Use Descriptive Test Names

```typescript
// Good: Test names read like requirements
describe('ShoppingCart', () => {
  it('displays empty state when no items in cart', () => {});
  it('calculates correct total with multiple items', () => {});
  it('applies discount code once per order', () => {});
  it('prevents checkout when cart is empty', () => {});
});
```

### 3. Follow AAA Pattern

```typescript
it('updates user profile', async () => {
  // Arrange
  const user = { id: 1, name: 'John' };
  const updates = { name: 'Jane' };
  const mockUpdate = jest.fn().mockResolvedValue({ ...user, ...updates });

  // Act
  const result = await updateUserProfile(user.id, updates);

  // Assert
  expect(mockUpdate).toHaveBeenCalledWith(user.id, updates);
  expect(result.name).toBe('Jane');
});
```

### 4. Keep Tests Independent

```typescript
// Each test should work in isolation
describe('TodoList', () => {
  let todoList: TodoList;

  beforeEach(() => {
    todoList = new TodoList(); // Fresh instance for each test
  });

  it('adds todo', () => {
    todoList.add('Task 1');
    expect(todoList.count()).toBe(1);
  });

  it('removes todo', () => {
    todoList.add('Task 1');
    todoList.remove(0);
    expect(todoList.count()).toBe(0);
  });
});
```

### 5. Test Edge Cases

```typescript
describe('divide', () => {
  it('divides positive numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('divides negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  it('divides by decimal', () => {
    expect(divide(10, 0.5)).toBe(20);
  });

  it('throws error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
  });

  it('handles very large numbers', () => {
    expect(divide(Number.MAX_SAFE_INTEGER, 2)).toBeDefined();
  });
});
```

### 6. Use Test Data Builders

```typescript
// Test data builder pattern
class UserBuilder {
  private user: Partial<User> = {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    role: 'user'
  };

  withId(id: number): this {
    this.user.id = id;
    return this;
  }

  withName(name: string): this {
    this.user.name = name;
    return this;
  }

  withRole(role: string): this {
    this.user.role = role;
    return this;
  }

  build(): User {
    return this.user as User;
  }
}

// Usage in tests
it('grants admin permissions', () => {
  const admin = new UserBuilder()
    .withRole('admin')
    .build();

  expect(hasPermission(admin, 'delete')).toBe(true);
});
```

### 7. Avoid Brittle Tests

```typescript
// Bad: Brittle test tied to implementation
it('bad: brittle', () => {
  const { container } = render(<UserCard />);
  expect(container.firstChild.firstChild.textContent).toBe('John');
});

// Good: Semantic queries
it('good: semantic', () => {
  render(<UserCard name="John" />);
  expect(screen.getByRole('heading')).toHaveTextContent('John');
});
```

### 8. Mock External Dependencies Only

```typescript
// Mock external APIs, databases, third-party services
jest.mock('axios');
jest.mock('@sendgrid/mail');

// Don't mock your own business logic
// Test it directly instead
```

### 9. Use waitFor for Async Updates

```typescript
it('loads user data', async () => {
  render(<UserProfile userId={1} />);

  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
});
```

### 10. Organize Tests Logically

```typescript
describe('UserService', () => {
  describe('CRUD Operations', () => {
    describe('create', () => {
      it('creates user with valid data', () => {});
      it('validates email format', () => {});
      it('hashes password', () => {});
    });

    describe('read', () => {
      it('finds user by id', () => {});
      it('returns null for non-existent user', () => {});
    });

    describe('update', () => {
      it('updates user fields', () => {});
      it('prevents email changes', () => {});
    });

    describe('delete', () => {
      it('soft deletes user', () => {});
      it('requires admin permission', () => {});
    });
  });

  describe('Authentication', () => {
    it('authenticates with valid credentials', () => {});
    it('rejects invalid credentials', () => {});
  });
});
```

---

## Summary

Jest provides a comprehensive testing framework with:

- **Clear test structure** with describe/it/expect
- **Rich matchers** for all assertion types
- **Powerful mocking** capabilities (functions, modules, timers)
- **Async testing** support for promises and callbacks
- **Snapshot testing** for UI components
- **Code coverage** reporting out of the box
- **React testing** utilities for components and hooks

**Key Principles:**

1. Test behavior, not implementation
2. Keep tests independent and isolated
3. Use descriptive test names
4. Follow AAA pattern (Arrange-Act-Assert)
5. Mock external dependencies only
6. Test edge cases and error paths
7. Maintain high coverage on critical code
8. Keep tests fast and focused
9. Use semantic queries for DOM testing
10. Clean up mocks and resources

**Remember:** Good tests give you confidence to refactor, catch bugs early, and serve as living documentation of your code's behavior.


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

