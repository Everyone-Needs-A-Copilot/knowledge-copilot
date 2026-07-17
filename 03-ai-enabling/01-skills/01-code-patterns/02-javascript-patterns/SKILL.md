---
last_updated: 2026-02-25
status: active
name: javascript-patterns
description: Modern JavaScript patterns - async/await, closures, destructuring, ES modules. Use when working with JavaScript.
triggers:
  files: ["**/*.js", "**/*.mjs", "**/package.json"]
  keywords: ["promise", "async", "await", "closure", "destructuring", "spread", "module", "callback", "event loop"]
allowed-tools: Read, Write, Edit
---

# JavaScript Patterns: Deep Expertise

Comprehensive guide to modern JavaScript patterns, idioms, and best practices for writing clean, performant, and maintainable code.

## Table of Contents

1. [ES6+ Modern Syntax](#es6-modern-syntax)
2. [Async Patterns](#async-patterns)
3. [Closures and Scope](#closures-and-scope)
4. [Prototypes and Classes](#prototypes-and-classes)
5. [Modules and Imports](#modules-and-imports)
6. [Error Handling](#error-handling)
7. [Functional Patterns](#functional-patterns)
8. [Event Loop and Concurrency](#event-loop-and-concurrency)
9. [Memory Management](#memory-management)
10. [Anti-Patterns](#anti-patterns)

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## ES6+ Modern Syntax

### Destructuring

**Array Destructuring**
```javascript
// Basic array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Skipping elements
const [, , third] = [1, 2, 3];
// third = 3

// Default values
const [a = 10, b = 20] = [5];
// a = 5, b = 20

// Swapping variables
let x = 1, y = 2;
[x, y] = [y, x];
// x = 2, y = 1

// Nested destructuring
const [first, [nestedFirst, nestedSecond]] = [1, [2, 3]];
```

**Object Destructuring**
```javascript
// Basic object destructuring
const { name, age } = { name: 'Alice', age: 30, city: 'NYC' };
// name = 'Alice', age = 30

// Renaming properties
const { name: userName, age: userAge } = user;

// Default values
const { role = 'user', permissions = [] } = user;

// Nested destructuring
const { address: { city, zip } } = user;

// Rest properties
const { id, ...userData } = user;

// Computed property names
const key = 'name';
const { [key]: value } = user;

// Function parameter destructuring
function greet({ name, age = 18 }) {
  return `Hello ${name}, you are ${age}`;
}
greet({ name: 'Bob' }); // "Hello Bob, you are 18"

// Mixed destructuring
const { users: [firstUser, ...otherUsers] } = data;
```

### Spread and Rest Operators

**Spread Operator (...)**
```javascript
// Array spreading
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];
// [1, 2, 3, 4, 5, 6]

// Object spreading (shallow merge)
const defaults = { theme: 'dark', lang: 'en' };
const userPrefs = { lang: 'fr', fontSize: 14 };
const config = { ...defaults, ...userPrefs };
// { theme: 'dark', lang: 'fr', fontSize: 14 }

// Function arguments
const numbers = [1, 2, 3];
Math.max(...numbers); // 3

// Cloning (shallow)
const original = { a: 1, b: 2 };
const clone = { ...original };

// Conditional spreading
const conditionalProps = {
  ...baseProps,
  ...(isAdmin && { role: 'admin' }),
  ...(hasPermissions && permissions),
};
```

**Rest Parameters**
```javascript
// Function rest parameters
function sum(...numbers) {
  return numbers.reduce((acc, n) => acc + n, 0);
}
sum(1, 2, 3, 4); // 10

// Combined with regular parameters
function multiply(multiplier, ...numbers) {
  return numbers.map(n => n * multiplier);
}
multiply(2, 1, 2, 3); // [2, 4, 6]

// Rest in destructuring
const [first, ...remaining] = [1, 2, 3, 4];
const { name, ...rest } = { name: 'Alice', age: 30, city: 'NYC' };
```

### Template Literals

```javascript
// Basic interpolation
const name = 'World';
const greeting = `Hello, ${name}!`;

// Multi-line strings
const message = `
  This is a
  multi-line
  string
`;

// Expression evaluation
const price = 10;
const tax = 0.08;
const total = `Total: $${(price * (1 + tax)).toFixed(2)}`;

// Nested templates
const classes = `container ${isActive ? `active ${modifier}` : 'inactive'}`;

// Tagged templates
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] ? `<mark>${values[i]}</mark>` : '';
    return result + str + value;
  }, '');
}
const name = 'Alice';
const html = highlight`Hello, ${name}!`;
// "Hello, <mark>Alice</mark>!"

// SQL query builder (tagged template)
function sql(strings, ...values) {
  return {
    text: strings.reduce((acc, str, i) => acc + str + (i < values.length ? `$${i + 1}` : ''), ''),
    values: values,
  };
}
const userId = 123;
const query = sql`SELECT * FROM users WHERE id = ${userId}`;
// { text: 'SELECT * FROM users WHERE id = $1', values: [123] }
```

### Arrow Functions

```javascript
// Basic syntax
const add = (a, b) => a + b;

// Single parameter (no parens needed)
const double = x => x * 2;

// No parameters
const random = () => Math.random();

// Block body
const processData = (data) => {
  const cleaned = data.filter(Boolean);
  return cleaned.map(item => item.toUpperCase());
};

// Returning objects (requires parens)
const createUser = (name, age) => ({ name, age, createdAt: Date.now() });

// Lexical this binding
class Timer {
  constructor() {
    this.seconds = 0;
  }

  start() {
    // Arrow function preserves 'this' from Timer instance
    setInterval(() => {
      this.seconds++;
      console.log(this.seconds);
    }, 1000);
  }
}

// When NOT to use arrow functions
const obj = {
  value: 42,
  // BAD: Arrow function doesn't bind 'this'
  getValue: () => this.value, // undefined

  // GOOD: Regular function binds 'this' to obj
  getValue() { return this.value; }, // 42
};

// No arguments object
const regularFunc = function() { return arguments; }; // Works
const arrowFunc = () => arguments; // ReferenceError

// Cannot be used as constructors
const Person = (name) => { this.name = name; }; // BAD
new Person('Alice'); // TypeError
```

### Enhanced Object Literals

```javascript
// Property shorthand
const name = 'Alice';
const age = 30;
const user = { name, age };
// { name: 'Alice', age: 30 }

// Method shorthand
const calculator = {
  // Old way
  add: function(a, b) { return a + b; },

  // New way
  subtract(a, b) { return a - b; },

  // Async method
  async fetchData() { return await fetch('/api/data'); },

  // Generator method
  *generateIds() {
    let id = 0;
    while (true) yield id++;
  },
};

// Computed property names
const propName = 'dynamic';
const obj = {
  [propName]: 'value',
  [`${propName}Count`]: 42,
  [Symbol.iterator]() { /* ... */ },
};

// Getters and setters
const person = {
  firstName: 'John',
  lastName: 'Doe',

  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  },

  set fullName(value) {
    [this.firstName, this.lastName] = value.split(' ');
  },
};
person.fullName = 'Jane Smith';
console.log(person.firstName); // 'Jane'
```

---

## Async Patterns

### Promises

**Promise Fundamentals**
```javascript
// Creating a promise
const promise = new Promise((resolve, reject) => {
  const success = Math.random() > 0.5;

  setTimeout(() => {
    if (success) {
      resolve({ data: 'Success!' });
    } else {
      reject(new Error('Failed!'));
    }
  }, 1000);
});

// Consuming promises
promise
  .then(result => {
    console.log(result.data);
    return processData(result);
  })
  .then(processed => {
    console.log(processed);
  })
  .catch(error => {
    console.error('Error:', error.message);
  })
  .finally(() => {
    console.log('Cleanup');
  });

// Promise chaining
fetchUser(userId)
  .then(user => fetchPosts(user.id))
  .then(posts => posts.map(post => post.title))
  .then(titles => console.log(titles))
  .catch(error => console.error(error));
```

**Promise Combinators**
```javascript
// Promise.all - Wait for all to complete
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments(),
]);
// Fails fast if any promise rejects

// Promise.allSettled - Wait for all, get all results
const results = await Promise.allSettled([
  fetchUsers(),
  fetchPosts(),
  fetchComments(),
]);
results.forEach(result => {
  if (result.status === 'fulfilled') {
    console.log('Success:', result.value);
  } else {
    console.log('Error:', result.reason);
  }
});

// Promise.race - First to complete wins
const timeout = ms => new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Timeout')), ms)
);
const result = await Promise.race([
  fetchData(),
  timeout(5000),
]);

// Promise.any - First to fulfill wins (ignores rejections)
const fastestServer = await Promise.any([
  fetch('https://api1.example.com/data'),
  fetch('https://api2.example.com/data'),
  fetch('https://api3.example.com/data'),
]);
```

**Advanced Promise Patterns**
```javascript
// Retry with exponential backoff
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Promisify callback-based functions
function promisify(fn) {
  return function(...args) {
    return new Promise((resolve, reject) => {
      fn(...args, (error, result) => {
        if (error) reject(error);
        else resolve(result);
      });
    });
  };
}

const readFile = promisify(fs.readFile);
const data = await readFile('file.txt', 'utf8');

// Sequential execution
async function processSequentially(items, asyncFn) {
  const results = [];
  for (const item of items) {
    results.push(await asyncFn(item));
  }
  return results;
}

// Parallel execution with concurrency limit
async function processWithConcurrency(items, asyncFn, limit = 3) {
  const results = [];
  const executing = [];

  for (const item of items) {
    const promise = asyncFn(item).then(result => {
      executing.splice(executing.indexOf(promise), 1);
      return result;
    });

    results.push(promise);
    executing.push(promise);

    if (executing.length >= limit) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
}

// Timeout wrapper
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}
```

### Async/Await

**Fundamentals**
```javascript
// Basic async function
async function fetchUserData(userId) {
  const response = await fetch(`/api/users/${userId}`);
  const data = await response.json();
  return data;
}

// Error handling with try-catch
async function safeAsyncOperation() {
  try {
    const result = await riskyOperation();
    return result;
  } catch (error) {
    console.error('Operation failed:', error);
    return null;
  } finally {
    cleanup();
  }
}

// Multiple awaits (sequential)
async function sequential() {
  const user = await fetchUser();      // Wait
  const posts = await fetchPosts();    // Wait
  const comments = await fetchComments(); // Wait
  return { user, posts, comments };
}

// Parallel execution
async function parallel() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments(),
  ]);
  return { user, posts, comments };
}

// Mixed sequential and parallel
async function optimized() {
  const user = await fetchUser();
  const [posts, comments] = await Promise.all([
    fetchPosts(user.id),
    fetchComments(user.id),
  ]);
  return { user, posts, comments };
}
```

**Advanced Patterns**
```javascript
// Async IIFE (Immediately Invoked Function Expression)
(async () => {
  const data = await fetchData();
  console.log(data);
})();

// Top-level await (ES2022, module context only)
const config = await fetchConfig();
export default config;

// Async iteration
async function* asyncGenerator() {
  for (let i = 0; i < 5; i++) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    yield i;
  }
}

for await (const value of asyncGenerator()) {
  console.log(value); // 0, 1, 2, 3, 4 (one per second)
}

// Async reduce
async function asyncReduce(array, asyncFn, initialValue) {
  let accumulator = initialValue;
  for (const item of array) {
    accumulator = await asyncFn(accumulator, item);
  }
  return accumulator;
}

const total = await asyncReduce(
  [1, 2, 3],
  async (sum, n) => sum + await fetchValue(n),
  0
);

// Conditional async execution
async function conditionalFetch(shouldFetch) {
  const data = shouldFetch ? await fetchData() : getDefaultData();
  return data;
}

// Error boundaries for async operations
class AsyncErrorBoundary {
  constructor(fallback) {
    this.fallback = fallback;
  }

  async execute(asyncFn) {
    try {
      return await asyncFn();
    } catch (error) {
      console.error('Caught in boundary:', error);
      return this.fallback;
    }
  }
}

const boundary = new AsyncErrorBoundary({ error: true });
const result = await boundary.execute(() => fetchData());
```

### Event Loop Understanding

```javascript
// Microtasks vs Macrotasks
console.log('1: Synchronous');

setTimeout(() => {
  console.log('2: Macrotask (setTimeout)');
}, 0);

Promise.resolve().then(() => {
  console.log('3: Microtask (Promise)');
});

console.log('4: Synchronous');

// Output order:
// 1: Synchronous
// 4: Synchronous
// 3: Microtask (Promise)
// 2: Macrotask (setTimeout)

// Microtasks run before macrotasks
Promise.resolve()
  .then(() => console.log('Promise 1'))
  .then(() => console.log('Promise 2'));

setTimeout(() => console.log('Timeout 1'), 0);
setTimeout(() => console.log('Timeout 2'), 0);

// Output:
// Promise 1
// Promise 2
// Timeout 1
// Timeout 2

// Blocking the event loop (BAD)
function blockingOperation() {
  const start = Date.now();
  while (Date.now() - start < 3000) {
    // Blocks for 3 seconds
  }
}

// Non-blocking alternative (GOOD)
async function nonBlockingOperation() {
  const chunks = 100;
  for (let i = 0; i < chunks; i++) {
    await new Promise(resolve => setTimeout(resolve, 30));
    // Work happens in small chunks
  }
}
```

---

## Closures and Scope

### Closure Fundamentals

```javascript
// Basic closure
function createCounter() {
  let count = 0;

  return {
    increment() {
      return ++count;
    },
    decrement() {
      return --count;
    },
    getCount() {
      return count;
    },
  };
}

const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
counter.getCount();  // 2
// 'count' is private, not accessible directly

// Closure with parameters
function multiply(factor) {
  return function(number) {
    return number * factor;
  };
}

const double = multiply(2);
const triple = multiply(3);
double(5); // 10
triple(5); // 15

// Maintaining state
function createBankAccount(initialBalance) {
  let balance = initialBalance;

  return {
    deposit(amount) {
      if (amount > 0) {
        balance += amount;
        return balance;
      }
      throw new Error('Invalid amount');
    },
    withdraw(amount) {
      if (amount > 0 && amount <= balance) {
        balance -= amount;
        return balance;
      }
      throw new Error('Invalid amount or insufficient funds');
    },
    getBalance() {
      return balance;
    },
  };
}

const account = createBankAccount(100);
account.deposit(50);   // 150
account.withdraw(30);  // 120
account.getBalance();  // 120
```

### Advanced Closure Patterns

```javascript
// Module pattern (pre-ES6 modules)
const Calculator = (function() {
  // Private variables and functions
  let lastResult = 0;

  function log(operation, result) {
    console.log(`${operation} = ${result}`);
  }

  // Public API
  return {
    add(a, b) {
      lastResult = a + b;
      log(`${a} + ${b}`, lastResult);
      return lastResult;
    },
    subtract(a, b) {
      lastResult = a - b;
      log(`${a} - ${b}`, lastResult);
      return lastResult;
    },
    getLastResult() {
      return lastResult;
    },
  };
})();

Calculator.add(5, 3);         // 8
Calculator.getLastResult();   // 8

// Factory pattern with closures
function createLogger(prefix) {
  const timestamp = () => new Date().toISOString();

  return {
    info(message) {
      console.log(`[${timestamp()}] [${prefix}] INFO: ${message}`);
    },
    error(message) {
      console.error(`[${timestamp()}] [${prefix}] ERROR: ${message}`);
    },
  };
}

const dbLogger = createLogger('DATABASE');
const apiLogger = createLogger('API');
dbLogger.info('Connected');
apiLogger.error('Request failed');

// Memoization with closures
function memoize(fn) {
  const cache = new Map();

  return function(...args) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      console.log('Cache hit');
      return cache.get(key);
    }

    console.log('Computing...');
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize(function(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});

fibonacci(40); // Computes
fibonacci(40); // Cache hit

// Partial application
function partial(fn, ...fixedArgs) {
  return function(...remainingArgs) {
    return fn(...fixedArgs, ...remainingArgs);
  };
}

function greet(greeting, name) {
  return `${greeting}, ${name}!`;
}

const sayHello = partial(greet, 'Hello');
sayHello('Alice'); // "Hello, Alice!"

// Currying
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...nextArgs) {
      return curried.apply(this, [...args, ...nextArgs]);
    };
  };
}

const sum = (a, b, c) => a + b + c;
const curriedSum = curry(sum);
curriedSum(1)(2)(3); // 6
curriedSum(1, 2)(3); // 6
curriedSum(1)(2, 3); // 6
```

### Scope and Hoisting

```javascript
// var vs let vs const
function scopeExample() {
  // var: function-scoped, hoisted
  console.log(varVariable); // undefined (hoisted, not initialized)
  var varVariable = 'var';

  // let: block-scoped, temporal dead zone
  // console.log(letVariable); // ReferenceError
  let letVariable = 'let';

  // const: block-scoped, must be initialized, immutable binding
  const constVariable = 'const';
  // constVariable = 'new'; // TypeError

  if (true) {
    var functionScoped = 'accessible outside';
    let blockScoped = 'not accessible outside';
  }

  console.log(functionScoped); // 'accessible outside'
  // console.log(blockScoped);  // ReferenceError
}

// Temporal Dead Zone (TDZ)
function tdz() {
  // TDZ starts
  // console.log(value); // ReferenceError

  let value = 42; // TDZ ends
  console.log(value); // 42
}

// Hoisting with functions
// Function declarations are hoisted
greet('Alice'); // Works!

function greet(name) {
  return `Hello, ${name}`;
}

// Function expressions are NOT hoisted
// sayGoodbye('Bob'); // TypeError: sayGoodbye is not a function

const sayGoodbye = function(name) {
  return `Goodbye, ${name}`;
};

// Arrow functions are NOT hoisted
// const add = (a, b) => a + b; // Must be defined before use
```

---

## Prototypes and Classes

### Prototypal Inheritance

```javascript
// Constructor function
function Person(name, age) {
  this.name = name;
  this.age = age;
}

Person.prototype.greet = function() {
  return `Hello, I'm ${this.name}`;
};

const alice = new Person('Alice', 30);
alice.greet(); // "Hello, I'm Alice"

// Prototype chain
console.log(alice.__proto__ === Person.prototype); // true
console.log(Person.prototype.__proto__ === Object.prototype); // true
console.log(Object.prototype.__proto__); // null

// Inheritance with prototypes
function Employee(name, age, title) {
  Person.call(this, name, age);
  this.title = title;
}

Employee.prototype = Object.create(Person.prototype);
Employee.prototype.constructor = Employee;

Employee.prototype.work = function() {
  return `${this.name} is working as ${this.title}`;
};

const bob = new Employee('Bob', 25, 'Developer');
bob.greet(); // "Hello, I'm Bob" (inherited)
bob.work();  // "Bob is working as Developer"

// Checking prototype chain
console.log(bob instanceof Employee); // true
console.log(bob instanceof Person);   // true
console.log(bob instanceof Object);   // true
```

### ES6 Classes

```javascript
// Basic class
class Animal {
  constructor(name, species) {
    this.name = name;
    this.species = species;
  }

  // Instance method
  speak() {
    return `${this.name} makes a sound`;
  }

  // Static method
  static createRandom() {
    const names = ['Max', 'Bella', 'Charlie'];
    const species = ['Dog', 'Cat', 'Bird'];
    return new Animal(
      names[Math.floor(Math.random() * names.length)],
      species[Math.floor(Math.random() * species.length)]
    );
  }

  // Getter
  get info() {
    return `${this.name} (${this.species})`;
  }

  // Setter
  set nickname(value) {
    this._nickname = value;
  }

  get nickname() {
    return this._nickname || this.name;
  }
}

const dog = new Animal('Max', 'Dog');
dog.speak(); // "Max makes a sound"
dog.info;    // "Max (Dog)"
dog.nickname = 'Maxie';

const random = Animal.createRandom();

// Class inheritance
class Dog extends Animal {
  constructor(name, breed) {
    super(name, 'Dog'); // Call parent constructor
    this.breed = breed;
  }

  // Override parent method
  speak() {
    return `${this.name} barks`;
  }

  // New method
  fetch() {
    return `${this.name} fetches the ball`;
  }
}

const rex = new Dog('Rex', 'German Shepherd');
rex.speak();  // "Rex barks" (overridden)
rex.fetch();  // "Rex fetches the ball"
rex.info;     // "Rex (Dog)" (inherited getter)

// Private fields (ES2022)
class BankAccount {
  #balance = 0; // Private field

  constructor(initialBalance) {
    this.#balance = initialBalance;
  }

  deposit(amount) {
    if (amount > 0) {
      this.#balance += amount;
    }
  }

  getBalance() {
    return this.#balance;
  }

  // Private method
  #validateTransaction(amount) {
    return amount > 0 && amount <= this.#balance;
  }

  withdraw(amount) {
    if (this.#validateTransaction(amount)) {
      this.#balance -= amount;
      return true;
    }
    return false;
  }
}

const account = new BankAccount(100);
account.deposit(50);
console.log(account.getBalance()); // 150
// console.log(account.#balance);  // SyntaxError: Private field
```

### Advanced Class Patterns

```javascript
// Abstract base class pattern
class Shape {
  constructor(color) {
    if (new.target === Shape) {
      throw new Error('Cannot instantiate abstract class');
    }
    this.color = color;
  }

  area() {
    throw new Error('Must implement area() method');
  }
}

class Circle extends Shape {
  constructor(radius, color) {
    super(color);
    this.radius = radius;
  }

  area() {
    return Math.PI * this.radius ** 2;
  }
}

// Mixins
const TimestampMixin = {
  initTimestamp() {
    this.createdAt = new Date();
  },
  getAge() {
    return Date.now() - this.createdAt.getTime();
  },
};

const SerializableMixin = {
  toJSON() {
    return JSON.stringify(this);
  },
  fromJSON(json) {
    Object.assign(this, JSON.parse(json));
    return this;
  },
};

class User {
  constructor(name) {
    this.name = name;
  }
}

Object.assign(User.prototype, TimestampMixin, SerializableMixin);

const user = new User('Alice');
user.initTimestamp();
console.log(user.getAge());

// Composition over inheritance
function withLogging(BaseClass) {
  return class extends BaseClass {
    log(message) {
      console.log(`[${this.constructor.name}] ${message}`);
    }
  };
}

function withValidation(BaseClass) {
  return class extends BaseClass {
    validate() {
      return Object.values(this).every(v => v != null);
    }
  };
}

class Product {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
}

const EnhancedProduct = withValidation(withLogging(Product));
const product = new EnhancedProduct('Laptop', 999);
product.log('Created');
console.log(product.validate());
```

---

## Modules and Imports

### ES6 Modules

**Export Patterns**
```javascript
// named-exports.js

// Named exports
export const PI = 3.14159;
export function add(a, b) {
  return a + b;
}
export class Calculator {
  multiply(a, b) {
    return a * b;
  }
}

// Export existing declarations
const CONFIG = { debug: true };
function init() { /* ... */ }
export { CONFIG, init };

// Rename on export
const internalName = 'secret';
export { internalName as publicName };

// default-export.js

// Default export (one per module)
export default class Logger {
  log(message) {
    console.log(message);
  }
}

// Or
class Logger { /* ... */ }
export default Logger;

// Or inline
export default function(message) {
  console.log(message);
}

// mixed-exports.js

// Both named and default
export default class App { /* ... */ }
export const version = '1.0.0';
export function init() { /* ... */ }
```

**Import Patterns**
```javascript
// Named imports
import { PI, add, Calculator } from './named-exports.js';

// Rename on import
import { publicName as secret } from './named-exports.js';

// Import all as namespace
import * as MathUtils from './named-exports.js';
MathUtils.add(1, 2);

// Default import
import Logger from './default-export.js';

// Mixed imports
import App, { version, init } from './mixed-exports.js';

// Side-effect import (runs module code, doesn't import anything)
import './polyfills.js';

// Dynamic import (returns Promise)
const module = await import('./dynamic-module.js');
module.doSomething();

// Conditional dynamic import
if (userWantsFeature) {
  const { Feature } = await import('./feature.js');
  new Feature().activate();
}

// Re-exports (useful for index files)
// index.js
export { User } from './user.js';
export { Product } from './product.js';
export * from './utils.js';
export { default as App } from './app.js';
```

### Module Patterns

```javascript
// Barrel exports (index.js)
export { UserService } from './services/user-service.js';
export { AuthService } from './services/auth-service.js';
export { Database } from './database.js';

// Usage
import { UserService, AuthService } from './services/index.js';

// Singleton pattern with modules
// database.js
class Database {
  constructor() {
    if (!Database.instance) {
      this.connection = createConnection();
      Database.instance = this;
    }
    return Database.instance;
  }
}

export default new Database(); // Single instance exported

// Lazy initialization
// config.js
let config = null;

export function getConfig() {
  if (!config) {
    config = loadConfiguration();
  }
  return config;
}

// Circular dependency handling
// a.js
import { b } from './b.js';
export const a = 'A';
console.log(b); // undefined at first, then 'B' after b.js loads

// b.js
import { a } from './a.js';
export const b = 'B';
console.log(a); // undefined at first, then 'A' after a.js loads

// Solution: Use functions to defer access
// a.js
import { getB } from './b.js';
export const a = 'A';
export function getA() { return a; }
console.log(getB()); // 'B'

// b.js
import { getA } from './a.js';
export const b = 'B';
export function getB() { return b; }
console.log(getA()); // 'A'
```

---

## Error Handling

### Try-Catch Patterns

```javascript
// Basic try-catch
try {
  const result = riskyOperation();
  console.log(result);
} catch (error) {
  console.error('Operation failed:', error.message);
} finally {
  cleanup(); // Always runs
}

// Async error handling
async function fetchData() {
  try {
    const response = await fetch('/api/data');

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof TypeError) {
      console.error('Network error:', error.message);
    } else if (error instanceof SyntaxError) {
      console.error('Invalid JSON:', error.message);
    } else {
      console.error('Unknown error:', error);
    }
    return null;
  }
}

// Multiple catch blocks pattern
try {
  await operation();
} catch (error) {
  if (error instanceof ValidationError) {
    // Handle validation errors
    return { error: error.message, code: 'VALIDATION_ERROR' };
  } else if (error instanceof NetworkError) {
    // Handle network errors
    return { error: 'Network failed', code: 'NETWORK_ERROR' };
  } else {
    // Rethrow unknown errors
    throw error;
  }
}

// Nested try-catch (avoid when possible)
try {
  const data = await fetchData();

  try {
    const processed = processData(data);
    return processed;
  } catch (processingError) {
    console.error('Processing failed:', processingError);
    return data; // Return raw data as fallback
  }
} catch (fetchError) {
  console.error('Fetch failed:', fetchError);
  return null;
}
```

### Custom Errors

```javascript
// Custom error class
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
    this.timestamp = new Date();

    // Maintains proper stack trace
    Error.captureStackTrace(this, this.constructor);
  }
}

class NetworkError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = 'NetworkError';
    this.statusCode = statusCode;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Usage
function validateUser(user) {
  if (!user.email) {
    throw new ValidationError('Email is required', 'email');
  }
  if (!user.age || user.age < 18) {
    throw new ValidationError('Must be 18 or older', 'age');
  }
}

try {
  validateUser({ email: '' });
} catch (error) {
  if (error instanceof ValidationError) {
    console.error(`Validation failed on ${error.field}: ${error.message}`);
  }
}

// Error factory pattern
class AppError extends Error {
  constructor(message, code, statusCode = 500) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
    Error.captureStackTrace(this, this.constructor);
  }

  static badRequest(message) {
    return new AppError(message, 'BAD_REQUEST', 400);
  }

  static notFound(resource) {
    return new AppError(`${resource} not found`, 'NOT_FOUND', 404);
  }

  static unauthorized(message = 'Unauthorized') {
    return new AppError(message, 'UNAUTHORIZED', 401);
  }
}

throw AppError.notFound('User');
throw AppError.badRequest('Invalid email format');
```

### Error Handling Strategies

```javascript
// Result pattern (functional approach)
class Result {
  constructor(value, error) {
    this.value = value;
    this.error = error;
  }

  static ok(value) {
    return new Result(value, null);
  }

  static err(error) {
    return new Result(null, error);
  }

  isOk() {
    return this.error === null;
  }

  isErr() {
    return this.error !== null;
  }

  unwrap() {
    if (this.isErr()) {
      throw new Error('Called unwrap on an error result');
    }
    return this.value;
  }

  unwrapOr(defaultValue) {
    return this.isOk() ? this.value : defaultValue;
  }

  map(fn) {
    return this.isOk() ? Result.ok(fn(this.value)) : this;
  }

  mapErr(fn) {
    return this.isErr() ? Result.err(fn(this.error)) : this;
  }
}

// Usage
function divide(a, b) {
  if (b === 0) {
    return Result.err('Division by zero');
  }
  return Result.ok(a / b);
}

const result = divide(10, 2);
if (result.isOk()) {
  console.log('Result:', result.value);
} else {
  console.error('Error:', result.error);
}

const doubled = divide(10, 2)
  .map(x => x * 2)
  .unwrapOr(0);

// Error boundary for promises
class PromiseErrorBoundary {
  constructor() {
    this.errors = [];
  }

  async wrap(promise) {
    try {
      return await promise;
    } catch (error) {
      this.errors.push({
        error,
        timestamp: new Date(),
        stack: error.stack,
      });
      return null;
    }
  }

  getErrors() {
    return this.errors;
  }

  clearErrors() {
    this.errors = [];
  }
}

const boundary = new PromiseErrorBoundary();
const data = await boundary.wrap(fetchData());

// Global error handlers
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
  // Send to error tracking service
  trackError(event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
  trackError(event.reason);
});

// Process error handler (Node.js)
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
  // Graceful shutdown
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled rejection at:', promise, 'reason:', reason);
});
```

---

## Functional Patterns

### Pure Functions and Immutability

```javascript
// Pure function (same input = same output, no side effects)
function add(a, b) {
  return a + b;
}

// Impure function (depends on external state)
let total = 0;
function addToTotal(value) {
  total += value; // Side effect
  return total;
}

// Immutable array operations
const numbers = [1, 2, 3, 4, 5];

// BAD: Mutates original
numbers.push(6);
numbers.sort((a, b) => b - a);

// GOOD: Returns new array
const withSix = [...numbers, 6];
const sorted = [...numbers].sort((a, b) => b - a);
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);

// Immutable object operations
const user = { name: 'Alice', age: 30 };

// BAD: Mutates original
user.age = 31;

// GOOD: Returns new object
const olderUser = { ...user, age: 31 };
const withEmail = { ...user, email: 'alice@example.com' };

// Deep immutability
function updateNestedValue(obj, path, value) {
  const [head, ...rest] = path;

  if (rest.length === 0) {
    return { ...obj, [head]: value };
  }

  return {
    ...obj,
    [head]: updateNestedValue(obj[head], rest, value),
  };
}

const state = {
  user: {
    profile: {
      name: 'Alice',
    },
  },
};

const newState = updateNestedValue(state, ['user', 'profile', 'name'], 'Bob');
// state.user.profile.name === 'Alice' (unchanged)
// newState.user.profile.name === 'Bob'
```

### Higher-Order Functions

```javascript
// Function that returns a function
function multiplier(factor) {
  return function(number) {
    return number * factor;
  };
}

const double = multiplier(2);
const triple = multiplier(3);
double(5); // 10
triple(5); // 15

// Function that takes function as argument
function repeat(n, action) {
  for (let i = 0; i < n; i++) {
    action(i);
  }
}

repeat(3, i => console.log(`Iteration ${i}`));

// Compose (right to left)
function compose(...fns) {
  return function(value) {
    return fns.reduceRight((acc, fn) => fn(acc), value);
  };
}

const addOne = x => x + 1;
const double = x => x * 2;
const square = x => x * x;

const compute = compose(square, double, addOne);
compute(3); // ((3 + 1) * 2)^2 = 64

// Pipe (left to right)
function pipe(...fns) {
  return function(value) {
    return fns.reduce((acc, fn) => fn(acc), value);
  };
}

const process = pipe(addOne, double, square);
process(3); // ((3 + 1) * 2)^2 = 64

// Partial application
function partial(fn, ...fixedArgs) {
  return function(...remainingArgs) {
    return fn(...fixedArgs, ...remainingArgs);
  };
}

function greet(greeting, name) {
  return `${greeting}, ${name}!`;
}

const sayHello = partial(greet, 'Hello');
sayHello('Alice'); // "Hello, Alice!"

// Currying
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...nextArgs) {
      return curried.apply(this, [...args, ...nextArgs]);
    };
  };
}

const sum = (a, b, c) => a + b + c;
const curriedSum = curry(sum);
curriedSum(1)(2)(3);    // 6
curriedSum(1, 2)(3);    // 6
curriedSum(1)(2, 3);    // 6

// Memoization
function memoize(fn) {
  const cache = new Map();

  return function(...args) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key);
    }

    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Debounce
function debounce(fn, delay) {
  let timeoutId;

  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Throttle
function throttle(fn, limit) {
  let inThrottle;

  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Usage
const handleSearch = debounce((query) => {
  console.log('Searching for:', query);
}, 300);

const handleScroll = throttle(() => {
  console.log('Scroll position:', window.scrollY);
}, 100);
```

### Array Methods (Functional)

```javascript
const users = [
  { name: 'Alice', age: 30, active: true },
  { name: 'Bob', age: 25, active: false },
  { name: 'Charlie', age: 35, active: true },
];

// map - Transform each element
const names = users.map(user => user.name);
// ['Alice', 'Bob', 'Charlie']

// filter - Keep elements that match condition
const activeUsers = users.filter(user => user.active);
// [{ name: 'Alice', ... }, { name: 'Charlie', ... }]

// reduce - Accumulate to single value
const totalAge = users.reduce((sum, user) => sum + user.age, 0);
// 90

const usersByName = users.reduce((acc, user) => {
  acc[user.name] = user;
  return acc;
}, {});
// { Alice: {...}, Bob: {...}, Charlie: {...} }

// find - First element that matches
const charlie = users.find(user => user.name === 'Charlie');

// findIndex - Index of first match
const bobIndex = users.findIndex(user => user.name === 'Bob');

// some - At least one matches
const hasInactive = users.some(user => !user.active); // true

// every - All match
const allActive = users.every(user => user.active); // false

// flatMap - Map and flatten
const tags = [
  { id: 1, tags: ['js', 'web'] },
  { id: 2, tags: ['python', 'data'] },
];
const allTags = tags.flatMap(item => item.tags);
// ['js', 'web', 'python', 'data']

// Chaining
const result = users
  .filter(user => user.active)
  .map(user => ({ ...user, age: user.age + 1 }))
  .sort((a, b) => a.age - b.age);

// groupBy (ES2024)
const grouped = Object.groupBy(users, user => user.active ? 'active' : 'inactive');
// { active: [...], inactive: [...] }
```

---

## Event Loop and Concurrency

### Event Loop Mechanics

```javascript
// Call stack, web APIs, callback queue, microtask queue

console.log('1: Sync');

setTimeout(() => console.log('2: Macro (timeout)'), 0);

Promise.resolve()
  .then(() => console.log('3: Micro (promise)'))
  .then(() => console.log('4: Micro (promise chain)'));

console.log('5: Sync');

// Output order:
// 1: Sync
// 5: Sync
// 3: Micro (promise)
// 4: Micro (promise chain)
// 2: Macro (timeout)

// Execution order: Sync → Microtasks → Macrotasks

// Microtasks (high priority, run before next macrotask)
Promise.resolve().then(() => { /* ... */ });
queueMicrotask(() => { /* ... */ });
new MutationObserver(() => { /* ... */ });

// Macrotasks (normal priority, run one per event loop tick)
setTimeout(() => { /* ... */ }, 0);
setInterval(() => { /* ... */ }, 100);
setImmediate(() => { /* ... */ }); // Node.js only
requestAnimationFrame(() => { /* ... */ }); // Browser only
```

### Concurrency Patterns

```javascript
// Sequential execution
async function sequential() {
  const result1 = await operation1(); // Wait
  const result2 = await operation2(); // Wait
  const result3 = await operation3(); // Wait
  return [result1, result2, result3];
}

// Concurrent execution
async function concurrent() {
  const [result1, result2, result3] = await Promise.all([
    operation1(), // Start immediately
    operation2(), // Start immediately
    operation3(), // Start immediately
  ]);
  return [result1, result2, result3];
}

// Race conditions
let counter = 0;

async function increment() {
  const current = counter;
  await new Promise(resolve => setTimeout(resolve, 0));
  counter = current + 1;
}

Promise.all([increment(), increment(), increment()]);
// counter might be 1, not 3 (race condition)

// Solution: Use locks/semaphores
class Mutex {
  constructor() {
    this.locked = false;
    this.waiters = [];
  }

  async acquire() {
    while (this.locked) {
      await new Promise(resolve => this.waiters.push(resolve));
    }
    this.locked = true;
  }

  release() {
    this.locked = false;
    const resolve = this.waiters.shift();
    if (resolve) resolve();
  }
}

const mutex = new Mutex();
let safeCounter = 0;

async function safeIncrement() {
  await mutex.acquire();
  try {
    const current = safeCounter;
    await new Promise(resolve => setTimeout(resolve, 0));
    safeCounter = current + 1;
  } finally {
    mutex.release();
  }
}

// Semaphore for rate limiting
class Semaphore {
  constructor(maxConcurrent) {
    this.maxConcurrent = maxConcurrent;
    this.current = 0;
    this.waiters = [];
  }

  async acquire() {
    while (this.current >= this.maxConcurrent) {
      await new Promise(resolve => this.waiters.push(resolve));
    }
    this.current++;
  }

  release() {
    this.current--;
    const resolve = this.waiters.shift();
    if (resolve) resolve();
  }

  async use(fn) {
    await this.acquire();
    try {
      return await fn();
    } finally {
      this.release();
    }
  }
}

// Limit to 3 concurrent requests
const semaphore = new Semaphore(3);

const results = await Promise.all(
  urls.map(url => semaphore.use(() => fetch(url)))
);

// Queue for ordered execution
class AsyncQueue {
  constructor() {
    this.queue = [];
    this.processing = false;
  }

  async enqueue(asyncFn) {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          const result = await asyncFn();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      });

      this.process();
    });
  }

  async process() {
    if (this.processing || this.queue.length === 0) return;

    this.processing = true;
    const task = this.queue.shift();
    await task();
    this.processing = false;
    this.process();
  }
}

const queue = new AsyncQueue();
queue.enqueue(() => operation1());
queue.enqueue(() => operation2());
queue.enqueue(() => operation3());
```

---

## Memory Management

### Memory Leaks

```javascript
// Common memory leak: Detached DOM nodes
const button = document.getElementById('myButton');
button.addEventListener('click', handleClick);
// If button is removed from DOM but event listener persists:
// button.remove(); // Button still in memory due to event listener

// Fix: Remove event listener
button.removeEventListener('click', handleClick);
button.remove();

// Or use once option
button.addEventListener('click', handleClick, { once: true });

// Memory leak: Closures retaining references
function createHugeArray() {
  const hugeArray = new Array(1000000).fill('data');

  return function() {
    // This closure keeps hugeArray in memory
    console.log(hugeArray[0]);
  };
}

const leak = createHugeArray(); // hugeArray never gets garbage collected

// Fix: Only capture what you need
function createHugeArrayFixed() {
  const hugeArray = new Array(1000000).fill('data');
  const firstElement = hugeArray[0];

  return function() {
    console.log(firstElement); // Only firstElement is retained
  };
}

// Memory leak: Timers
const intervalId = setInterval(() => {
  // Keeps running forever
  doSomething();
}, 1000);

// Fix: Clear timers
clearInterval(intervalId);

// Memory leak: Global variables
window.leakedData = new Array(1000000); // Never gets GC'd

// Fix: Use local scope
function processData() {
  const data = new Array(1000000);
  // data gets GC'd when function completes
}

// Memory leak: Event listeners accumulation
class Component {
  constructor() {
    this.data = new Array(1000000);

    // BAD: Creates new listener on every render
    this.render = () => {
      window.addEventListener('resize', () => {
        this.handleResize();
      });
    };
  }

  handleResize() {
    // Uses this.data
  }
}

// Fix: Store reference and clean up
class ComponentFixed {
  constructor() {
    this.data = new Array(1000000);
    this.handleResize = this.handleResize.bind(this);
  }

  mount() {
    window.addEventListener('resize', this.handleResize);
  }

  unmount() {
    window.removeEventListener('resize', this.handleResize);
    this.data = null; // Help GC
  }

  handleResize() {
    // Uses this.data
  }
}
```

### WeakMap and WeakSet

```javascript
// WeakMap: Keys are weakly held (can be GC'd)
const cache = new WeakMap();

function processObject(obj) {
  if (cache.has(obj)) {
    return cache.get(obj);
  }

  const result = expensiveOperation(obj);
  cache.set(obj, result);
  return result;
}

let obj = { data: 'example' };
processObject(obj);
obj = null; // Object and cache entry can be GC'd

// Private data using WeakMap
const privateData = new WeakMap();

class BankAccount {
  constructor(balance) {
    privateData.set(this, { balance });
  }

  getBalance() {
    return privateData.get(this).balance;
  }

  deposit(amount) {
    const data = privateData.get(this);
    data.balance += amount;
  }
}

// WeakSet: Items are weakly held
const visitedNodes = new WeakSet();

function traverse(node) {
  if (visitedNodes.has(node)) return;

  visitedNodes.add(node);
  node.children.forEach(child => traverse(child));
}

// When nodes are removed, they're automatically removed from WeakSet
```

### Performance Tips

```javascript
// Object pooling
class ObjectPool {
  constructor(factory, resetFn) {
    this.factory = factory;
    this.resetFn = resetFn;
    this.pool = [];
  }

  acquire() {
    if (this.pool.length > 0) {
      return this.pool.pop();
    }
    return this.factory();
  }

  release(obj) {
    this.resetFn(obj);
    this.pool.push(obj);
  }
}

const vectorPool = new ObjectPool(
  () => ({ x: 0, y: 0 }),
  (v) => { v.x = 0; v.y = 0; }
);

const v1 = vectorPool.acquire();
// Use v1
vectorPool.release(v1); // Reuse instead of creating new

// Avoid creating functions in loops
// BAD
for (let i = 0; i < 1000; i++) {
  element.addEventListener('click', function() {
    console.log(i);
  });
}

// GOOD
function handleClick(i) {
  return function() {
    console.log(i);
  };
}

for (let i = 0; i < 1000; i++) {
  element.addEventListener('click', handleClick(i));
}

// Use array buffer for large numeric arrays
const buffer = new ArrayBuffer(1000000 * 4); // 4 bytes per int
const int32View = new Int32Array(buffer);

// More memory efficient than:
const array = new Array(1000000);
```

---

## Anti-Patterns

### Common Mistakes

```javascript
// 1. Callback hell
// BAD
getData(function(a) {
  getMoreData(a, function(b) {
    getEvenMoreData(b, function(c) {
      getEvenEvenMoreData(c, function(d) {
        getFinalData(d, function(final) {
          console.log(final);
        });
      });
    });
  });
});

// GOOD
async function fetchAllData() {
  const a = await getData();
  const b = await getMoreData(a);
  const c = await getEvenMoreData(b);
  const d = await getEvenEvenMoreData(c);
  const final = await getFinalData(d);
  return final;
}

// 2. Modifying function arguments
// BAD
function addProperty(obj) {
  obj.newProp = 'value'; // Mutates input
  return obj;
}

// GOOD
function addProperty(obj) {
  return { ...obj, newProp: 'value' };
}

// 3. Using var instead of let/const
// BAD
var x = 1;
if (true) {
  var x = 2; // Same variable!
}

// GOOD
let x = 1;
if (true) {
  let x = 2; // Different variable
}

// 4. Not handling promise rejections
// BAD
async function fetchData() {
  const data = await fetch('/api/data'); // Unhandled error
  return data;
}

// GOOD
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error('Fetch failed');
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

// 5. Implicit type coercion
// BAD
if (value == null) { /* ... */ } // Matches null AND undefined

// GOOD
if (value === null || value === undefined) { /* ... */ }
// Or
if (value == null) { /* intentional coercion */ }

// 6. Excessive use of arrow functions
// BAD
const obj = {
  value: 42,
  getValue: () => this.value, // 'this' is not obj
};

// GOOD
const obj = {
  value: 42,
  getValue() { return this.value; },
};

// 7. Not cleaning up side effects
// BAD
function Component() {
  setInterval(() => {
    updateState();
  }, 1000); // Never cleaned up
}

// GOOD
function Component() {
  const intervalId = setInterval(() => {
    updateState();
  }, 1000);

  return function cleanup() {
    clearInterval(intervalId);
  };
}

// 8. Overusing nested ternaries
// BAD
const result = condition1 ? value1 : condition2 ? value2 : condition3 ? value3 : value4;

// GOOD
function getResult() {
  if (condition1) return value1;
  if (condition2) return value2;
  if (condition3) return value3;
  return value4;
}

// 9. Ignoring context (this)
// BAD
class Timer {
  constructor() {
    this.seconds = 0;
  }

  start() {
    setInterval(function() {
      this.seconds++; // 'this' is not Timer instance
    }, 1000);
  }
}

// GOOD
class Timer {
  constructor() {
    this.seconds = 0;
  }

  start() {
    setInterval(() => {
      this.seconds++; // Arrow function preserves 'this'
    }, 1000);
  }
}

// 10. Not using optional chaining/nullish coalescing
// BAD
const city = user && user.address && user.address.city;
const name = user.name !== null && user.name !== undefined ? user.name : 'Guest';

// GOOD
const city = user?.address?.city;
const name = user.name ?? 'Guest';
```

### Performance Anti-Patterns

```javascript
// 1. Inefficient array operations
// BAD
const results = [];
for (let i = 0; i < items.length; i++) {
  if (items[i].active) {
    results.push(items[i].name.toUpperCase());
  }
}

// GOOD
const results = items
  .filter(item => item.active)
  .map(item => item.name.toUpperCase());

// 2. Repeated DOM queries
// BAD
for (let i = 0; i < 100; i++) {
  document.getElementById('container').appendChild(createItem());
}

// GOOD
const container = document.getElementById('container');
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
  fragment.appendChild(createItem());
}
container.appendChild(fragment);

// 3. Synchronous blocking operations
// BAD
const data = fs.readFileSync('huge-file.json'); // Blocks entire thread

// GOOD
const data = await fs.promises.readFile('huge-file.json');

// 4. Not memoizing expensive computations
// BAD
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2); // Recalculates same values
}

// GOOD
const fibonacci = memoize(function(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});

// 5. Creating objects in hot loops
// BAD
for (let i = 0; i < 1000000; i++) {
  const point = { x: i, y: i * 2 }; // Creates 1M objects
  process(point);
}

// GOOD (object pooling)
const point = { x: 0, y: 0 };
for (let i = 0; i < 1000000; i++) {
  point.x = i;
  point.y = i * 2;
  process(point);
}
```

---

## Best Practices Summary

### Code Organization

```javascript
// 1. Use modules
// user-service.js
export class UserService {
  async getUser(id) { /* ... */ }
}

// main.js
import { UserService } from './user-service.js';

// 2. Single Responsibility Principle
// BAD: God class
class UserManager {
  validateUser() { /* ... */ }
  saveUser() { /* ... */ }
  sendEmail() { /* ... */ }
  logActivity() { /* ... */ }
}

// GOOD: Separate concerns
class UserValidator {
  validate(user) { /* ... */ }
}

class UserRepository {
  save(user) { /* ... */ }
}

class EmailService {
  send(to, subject, body) { /* ... */ }
}

// 3. Dependency Injection
class UserService {
  constructor(userRepo, emailService) {
    this.userRepo = userRepo;
    this.emailService = emailService;
  }

  async createUser(userData) {
    const user = await this.userRepo.save(userData);
    await this.emailService.send(user.email, 'Welcome', '...');
    return user;
  }
}

// 4. Configuration management
const config = {
  development: {
    apiUrl: 'http://localhost:3000',
    debug: true,
  },
  production: {
    apiUrl: 'https://api.example.com',
    debug: false,
  },
};

export default config[process.env.NODE_ENV];
```

### Error Handling

```javascript
// 1. Always handle errors
async function operation() {
  try {
    return await riskyOperation();
  } catch (error) {
    console.error('Operation failed:', error);
    throw error; // Re-throw or return default
  }
}

// 2. Use custom errors
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

// 3. Fail fast
function processUser(user) {
  if (!user) throw new Error('User is required');
  if (!user.email) throw new ValidationError('Email is required', 'email');
  // Continue processing
}
```

### Async Best Practices

```javascript
// 1. Use async/await over raw promises
// GOOD
async function fetchData() {
  const response = await fetch('/api/data');
  return await response.json();
}

// 2. Handle errors with try-catch
async function safeOperation() {
  try {
    return await operation();
  } catch (error) {
    console.error(error);
    return null;
  }
}

// 3. Parallelize independent operations
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
]);

// 4. Use Promise.allSettled for non-critical operations
const results = await Promise.allSettled([
  fetchAnalytics(),
  fetchMetrics(),
  fetchLogs(),
]);
```

### Testing Considerations

```javascript
// Write testable code
// BAD: Hard to test
function processData() {
  const data = fetchFromAPI();
  return transformData(data);
}

// GOOD: Easy to test
function processData(fetchFn, transformFn) {
  const data = fetchFn();
  return transformFn(data);
}

// Test
processData(
  () => mockData,
  data => data.map(x => x * 2)
);

// Pure functions are easiest to test
function add(a, b) {
  return a + b;
}

// No mocking needed
assert(add(2, 3) === 5);
```

---

## Conclusion

This skill covers the essential patterns and practices for modern JavaScript development. Apply these patterns judiciously based on your specific use case, team conventions, and performance requirements. Always prioritize readability and maintainability over clever code.

**Key Takeaways:**
- Use modern ES6+ syntax for cleaner code
- Master async/await for asynchronous operations
- Understand closures and scope for proper encapsulation
- Prefer functional patterns and immutability
- Handle errors explicitly and meaningfully
- Manage memory and avoid leaks
- Avoid common anti-patterns
- Write testable, maintainable code


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

