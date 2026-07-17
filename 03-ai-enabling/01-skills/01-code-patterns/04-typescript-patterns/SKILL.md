---
last_updated: 2026-02-25
status: active
name: typescript-patterns
description: TypeScript type safety - generics, utility types, type guards, inference. Use when working with TypeScript.
triggers:
  files: ["**/*.ts", "**/*.tsx", "**/tsconfig.json"]
  keywords: ["generic", "type guard", "utility type", "interface", "type inference", "discriminated union", "mapped type", "conditional type"]
allowed-tools: Read, Write, Edit
---

# TypeScript Patterns - Deep Expertise

Comprehensive guide to TypeScript's type system, focusing on type safety, generics, utility types, type guards, and advanced type manipulation patterns.

## Table of Contents

1. [Type System Fundamentals](#type-system-fundamentals)
2. [Generics](#generics)
3. [Utility Types](#utility-types)
4. [Type Guards](#type-guards)
5. [Discriminated Unions](#discriminated-unions)
6. [Mapped Types](#mapped-types)
7. [Conditional Types](#conditional-types)
8. [Type Inference](#type-inference)
9. [Declaration Files](#declaration-files)
10. [Strict Mode](#strict-mode)
11. [Anti-Patterns](#anti-patterns)

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## Type System Fundamentals

### Basic Types and Annotations

**Primitive Types:**
```typescript
// Explicit type annotations
const name: string = "Alice";
const age: number = 30;
const isActive: boolean = true;
const nothing: null = null;
const notDefined: undefined = undefined;

// Special types
const uniqueId: symbol = Symbol("id");
const largeNumber: bigint = 9007199254740991n;
```

**Array Types:**
```typescript
// Array syntax (preferred)
const numbers: number[] = [1, 2, 3];
const strings: string[] = ["a", "b", "c"];

// Generic array syntax
const values: Array<number> = [1, 2, 3];

// Readonly arrays
const immutableNumbers: readonly number[] = [1, 2, 3];
const immutableValues: ReadonlyArray<number> = [1, 2, 3];
```

**Tuple Types:**
```typescript
// Fixed-length arrays with specific types
type Coordinate = [number, number];
type NamedCoordinate = [x: number, y: number, z?: number];

const point: Coordinate = [10, 20];
const namedPoint: NamedCoordinate = [10, 20];

// Rest elements in tuples
type StringNumberBooleans = [string, number, ...boolean[]];
const mixed: StringNumberBooleans = ["hello", 42, true, false, true];

// Readonly tuples
type ReadonlyCoordinate = readonly [number, number];
```

### Interfaces vs Types

**When to Use Interface:**
```typescript
// For object shapes that may be extended
interface User {
  id: string;
  name: string;
  email: string;
}

// Interfaces can be extended
interface AdminUser extends User {
  permissions: string[];
}

// Interfaces can be merged (declaration merging)
interface Window {
  customProperty: string;
}

interface Window {
  anotherProperty: number;
}
// Now Window has both properties

// For class contracts
interface Sortable {
  sort(): void;
}

class Collection implements Sortable {
  sort(): void {
    // Implementation
  }
}
```

**When to Use Type:**
```typescript
// For unions and intersections
type Status = "pending" | "approved" | "rejected";
type ID = string | number;

// For tuple types
type RGB = [number, number, number];

// For mapped types
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

// For conditional types
type NonNullable<T> = T extends null | undefined ? never : T;

// For primitive types
type Timestamp = number;
type JSONValue = string | number | boolean | null | JSONObject | JSONArray;
type JSONObject = { [key: string]: JSONValue };
type JSONArray = JSONValue[];
```

**Best Practice Pattern:**
```typescript
// Use interfaces for public API shapes
export interface ApiResponse {
  data: unknown;
  status: number;
  message: string;
}

// Use types for internal unions and complex types
type RequestStatus = "idle" | "loading" | "success" | "error";
type ApiResult<T> = ApiResponse & { data: T };

// Combine when needed
interface UserResponse extends ApiResponse {
  data: User;
}

// Alternative with type
type UserResponse = ApiResponse & {
  data: User;
};
```

### Object Types and Index Signatures

```typescript
// Basic object type
type User = {
  id: string;
  name: string;
  email?: string; // Optional property
  readonly createdAt: Date; // Readonly property
};

// Index signatures
type Dictionary = {
  [key: string]: string;
};

type NumberDictionary = {
  [key: string]: number;
  length: number; // OK: length is number
  name: string; // Error: name is string, not number
};

// String and number index signatures together
type MixedDictionary = {
  [key: string]: string | number;
  [key: number]: string; // number index must be subtype of string index
};

// Typed index signature
type UserMap = {
  [userId: string]: User;
};

// Record utility type (preferred for dictionaries)
type UserRecord = Record<string, User>;
type StatusRecord = Record<string, boolean>;
```

### Function Types

```typescript
// Function type syntax
type AddFunction = (a: number, b: number) => number;

const add: AddFunction = (a, b) => a + b;

// Function signature in interface
interface MathOperations {
  add(a: number, b: number): number;
  subtract(a: number, b: number): number;
}

// Optional and default parameters
type Greet = (name: string, greeting?: string) => string;

const greet: Greet = (name, greeting = "Hello") => {
  return `${greeting}, ${name}!`;
};

// Rest parameters
type Sum = (...numbers: number[]) => number;

const sum: Sum = (...numbers) => {
  return numbers.reduce((acc, n) => acc + n, 0);
};

// Function overloads
function formatValue(value: string): string;
function formatValue(value: number): string;
function formatValue(value: boolean): string;
function formatValue(value: string | number | boolean): string {
  return String(value);
}

// Generic function types
type MapFunction<T, U> = (item: T, index: number) => U;
type FilterFunction<T> = (item: T, index: number) => boolean;
```

### Literal Types

```typescript
// String literal types
type Direction = "north" | "south" | "east" | "west";
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

// Number literal types
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
type HttpStatus = 200 | 201 | 400 | 401 | 403 | 404 | 500;

// Boolean literal types
type True = true;
type False = false;

// Mixed literal types
type Config = {
  mode: "development" | "production";
  port: 3000 | 8080;
  debug: true | false;
};

// Template literal types (TypeScript 4.1+)
type EventName = "click" | "focus" | "blur";
type ElementEvent = `on${Capitalize<EventName>}`; // "onClick" | "onFocus" | "onBlur"

type HTTPScheme = "http" | "https";
type Domain = string;
type URL = `${HTTPScheme}://${Domain}`;
```

---

## Generics

### Basic Generic Patterns

```typescript
// Generic function
function identity<T>(value: T): T {
  return value;
}

const num = identity(42); // T is number
const str = identity("hello"); // T is string

// Generic with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name"); // string
const age = getProperty(user, "age"); // number

// Multiple type parameters
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

const merged = merge({ name: "Alice" }, { age: 30 });
// merged has type { name: string } & { age: number }

// Generic with default types
function createArray<T = string>(length: number, value: T): T[] {
  return Array(length).fill(value);
}

const strings = createArray(3, "hello"); // string[]
const numbers = createArray<number>(3, 42); // number[]
```

### Generic Interfaces and Classes

```typescript
// Generic interface
interface Box<T> {
  value: T;
  getValue(): T;
  setValue(value: T): void;
}

const numberBox: Box<number> = {
  value: 42,
  getValue() {
    return this.value;
  },
  setValue(value) {
    this.value = value;
  },
};

// Generic class
class Container<T> {
  private contents: T[] = [];

  add(item: T): void {
    this.contents.push(item);
  }

  get(index: number): T | undefined {
    return this.contents[index];
  }

  getAll(): readonly T[] {
    return this.contents;
  }
}

const stringContainer = new Container<string>();
stringContainer.add("hello");

// Generic class with constraints
class DataStore<T extends { id: string }> {
  private items = new Map<string, T>();

  add(item: T): void {
    this.items.set(item.id, item);
  }

  get(id: string): T | undefined {
    return this.items.get(id);
  }
}

// Generic class with static members
class ArrayUtils {
  static first<T>(arr: T[]): T | undefined {
    return arr[0];
  }

  static last<T>(arr: T[]): T | undefined {
    return arr[arr.length - 1];
  }
}
```

### Advanced Generic Constraints

```typescript
// Extending multiple interfaces
interface Timestamped {
  timestamp: number;
}

interface Named {
  name: string;
}

function logItem<T extends Timestamped & Named>(item: T): void {
  console.log(`${item.name} at ${item.timestamp}`);
}

// Constructor constraints
type Constructor<T = {}> = new (...args: any[]) => T;

function createInstance<T>(Ctor: Constructor<T>): T {
  return new Ctor();
}

// Recursive generic constraints
type JSONValue = string | number | boolean | null | JSONObject | JSONArray;
type JSONObject = { [key: string]: JSONValue };
type JSONArray = JSONValue[];

function clone<T extends JSONValue>(value: T): T {
  return JSON.parse(JSON.stringify(value));
}

// Generic constraints with keyof
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const users = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];
const names = pluck(users, "name"); // string[]
const ages = pluck(users, "age"); // number[]
```

### Generic Type Inference

```typescript
// Inference from arguments
function toArray<T>(value: T): T[] {
  return [value];
}

const nums = toArray(42); // number[]
const strs = toArray("hello"); // string[]

// Inference with multiple parameters
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

const p1 = pair(1, "one"); // [number, string]
const p2 = pair(true, 42); // [boolean, number]

// Inference with constraints
function sortBy<T, K extends keyof T>(items: T[], key: K): T[] {
  return items.sort((a, b) => {
    return a[key] < b[key] ? -1 : 1;
  });
}

// Type inference with return type
function makeState<T>(initial: T) {
  let state = initial;
  return {
    get: () => state,
    set: (value: T) => {
      state = value;
    },
  };
}

const counter = makeState(0);
counter.set(1); // OK
counter.set("error"); // Error: string is not assignable to number

// Contextual typing
type EventHandler<T> = (event: T) => void;

const handleClick: EventHandler<MouseEvent> = (event) => {
  // event is inferred as MouseEvent
  console.log(event.clientX, event.clientY);
};
```

### Generic Variance

```typescript
// Covariance (out position)
interface Producer<out T> {
  produce(): T;
}

let producerA: Producer<string> = { produce: () => "hello" };
let producerB: Producer<string | number> = producerA; // OK: covariant

// Contravariance (in position)
interface Consumer<in T> {
  consume(value: T): void;
}

let consumerA: Consumer<string | number> = { consume: (v) => {} };
let consumerB: Consumer<string> = consumerA; // OK: contravariant

// Invariance (both positions)
interface Box<T> {
  get(): T;
  set(value: T): void;
}

let boxA: Box<string> = {
  get: () => "hello",
  set: (v) => {},
};
let boxB: Box<string | number> = boxA; // Error: invariant
```

---

## Utility Types

### Built-in Utility Types

**Partial and Required:**
```typescript
// Partial - makes all properties optional
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

type PartialUser = Partial<User>;
// Equivalent to:
// {
//   id?: string;
//   name?: string;
//   email?: string;
//   age?: number;
// }

function updateUser(user: User, updates: Partial<User>): User {
  return { ...user, ...updates };
}

// Required - makes all properties required
type RequiredUser = Required<PartialUser>;
// Back to original User type

// Deep partial (custom utility)
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
```

**Pick and Omit:**
```typescript
// Pick - select specific properties
type UserPreview = Pick<User, "id" | "name">;
// Equivalent to:
// {
//   id: string;
//   name: string;
// }

// Omit - exclude specific properties
type UserWithoutId = Omit<User, "id">;
// Equivalent to:
// {
//   name: string;
//   email: string;
//   age: number;
// }

// Multiple properties
type PublicUser = Omit<User, "id" | "email">;

// Pick with union types
type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

type StringProperties = PickByType<User, string>;
// { name: string; email: string }
```

**Record:**
```typescript
// Record - create object type with specific keys and values
type Status = "pending" | "approved" | "rejected";
type StatusConfig = Record<Status, { color: string; label: string }>;

const statusConfig: StatusConfig = {
  pending: { color: "yellow", label: "Pending" },
  approved: { color: "green", label: "Approved" },
  rejected: { color: "red", label: "Rejected" },
};

// Record with union keys
type HTTPStatusCode = 200 | 404 | 500;
type StatusMessages = Record<HTTPStatusCode, string>;

const messages: StatusMessages = {
  200: "OK",
  404: "Not Found",
  500: "Internal Server Error",
};

// Record with computed keys
type Keys = "a" | "b" | "c";
type ValueType = { value: number };
type Dictionary = Record<Keys, ValueType>;
```

**Readonly:**
```typescript
// Readonly - make all properties readonly
interface MutableUser {
  id: string;
  name: string;
}

type ImmutableUser = Readonly<MutableUser>;
// Equivalent to:
// {
//   readonly id: string;
//   readonly name: string;
// }

// Deep readonly (custom utility)
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

interface Config {
  database: {
    host: string;
    port: number;
  };
}

type ImmutableConfig = DeepReadonly<Config>;
// All nested properties are readonly
```

**ReturnType and Parameters:**
```typescript
// ReturnType - extract return type of function
function createUser(name: string, age: number) {
  return { name, age, createdAt: new Date() };
}

type User = ReturnType<typeof createUser>;
// { name: string; age: number; createdAt: Date }

// Parameters - extract parameter types as tuple
type CreateUserParams = Parameters<typeof createUser>;
// [string, number]

// Usage with spread
function logAndCreate(...args: Parameters<typeof createUser>) {
  console.log("Creating user with args:", args);
  return createUser(...args);
}

// ConstructorParameters - extract constructor parameter types
class Database {
  constructor(public host: string, public port: number) {}
}

type DatabaseParams = ConstructorParameters<typeof Database>;
// [string, number]

// InstanceType - extract instance type from constructor
type DatabaseInstance = InstanceType<typeof Database>;
// Database
```

**Exclude, Extract, NonNullable:**
```typescript
// Exclude - remove types from union
type T0 = Exclude<"a" | "b" | "c", "a">;
// "b" | "c"

type T1 = Exclude<string | number | (() => void), Function>;
// string | number

// Extract - keep only specified types
type T2 = Extract<"a" | "b" | "c", "a" | "f">;
// "a"

type T3 = Extract<string | number | (() => void), Function>;
// () => void

// NonNullable - remove null and undefined
type T4 = NonNullable<string | number | undefined | null>;
// string | number

// Practical example
type ApiResponse<T> = T | null | undefined;
type ValidResponse<T> = NonNullable<ApiResponse<T>>;

function processResponse<T>(response: ApiResponse<T>): ValidResponse<T> {
  if (response == null) {
    throw new Error("Invalid response");
  }
  return response;
}
```

### Custom Utility Types

```typescript
// Mutable - make all properties mutable
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

interface ReadonlyUser {
  readonly id: string;
  readonly name: string;
}

type MutableUser = Mutable<ReadonlyUser>;
// { id: string; name: string }

// Nullable - make all properties nullable
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

// NonNullableProperties - remove null from all properties
type NonNullableProperties<T> = {
  [K in keyof T]: NonNullable<T[K]>;
};

// Optional - make specific properties optional
type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

interface User {
  id: string;
  name: string;
  email: string;
}

type UserWithOptionalEmail = Optional<User, "email">;
// { id: string; name: string; email?: string }

// RequiredKeys - get union of required property keys
type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

// PickByValue - pick properties by value type
type PickByValue<T, V> = Pick<
  T,
  { [K in keyof T]: T[K] extends V ? K : never }[keyof T]
>;

interface Example {
  a: string;
  b: number;
  c: string;
}

type StringProps = PickByValue<Example, string>;
// { a: string; c: string }

// DeepPartial with arrays
type DeepPartialWithArrays<T> = T extends Array<infer U>
  ? Array<DeepPartialWithArrays<U>>
  : T extends object
  ? { [K in keyof T]?: DeepPartialWithArrays<T[K]> }
  : T;

// Promisify - convert function return type to Promise
type Promisify<T> = T extends (...args: infer A) => infer R
  ? (...args: A) => Promise<R>
  : never;

type SyncFn = (a: number, b: string) => boolean;
type AsyncFn = Promisify<SyncFn>;
// (a: number, b: string) => Promise<boolean>
```

---

## Type Guards

### Built-in Type Guards

```typescript
// typeof type guard
function padLeft(value: string, padding: string | number): string {
  if (typeof padding === "number") {
    // padding is number
    return " ".repeat(padding) + value;
  }
  // padding is string
  return padding + value;
}

// instanceof type guard
class Dog {
  bark() {
    console.log("Woof!");
  }
}

class Cat {
  meow() {
    console.log("Meow!");
  }
}

function makeSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark(); // animal is Dog
  } else {
    animal.meow(); // animal is Cat
  }
}

// in operator type guard
interface Bird {
  fly(): void;
  layEggs(): void;
}

interface Fish {
  swim(): void;
  layEggs(): void;
}

function move(animal: Bird | Fish) {
  if ("fly" in animal) {
    animal.fly(); // animal is Bird
  } else {
    animal.swim(); // animal is Fish
  }
}

// Truthiness type guard
function printAll(strs: string | string[] | null) {
  if (strs && typeof strs === "object") {
    // strs is string[]
    for (const s of strs) {
      console.log(s);
    }
  } else if (typeof strs === "string") {
    // strs is string
    console.log(strs);
  }
}
```

### Custom Type Guards (User-Defined Type Predicates)

```typescript
// Basic type predicate
interface User {
  id: string;
  name: string;
}

interface AdminUser extends User {
  permissions: string[];
}

function isAdminUser(user: User): user is AdminUser {
  return "permissions" in user;
}

function grantAccess(user: User) {
  if (isAdminUser(user)) {
    // user is AdminUser
    console.log(user.permissions);
  }
}

// Type guard with class
class NetworkError extends Error {
  statusCode: number;

  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
  }
}

function isNetworkError(error: Error): error is NetworkError {
  return error instanceof NetworkError;
}

// Type guard for array elements
function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

// Type guard for object shape
interface Point {
  x: number;
  y: number;
}

function isPoint(value: unknown): value is Point {
  return (
    typeof value === "object" &&
    value !== null &&
    "x" in value &&
    "y" in value &&
    typeof (value as Point).x === "number" &&
    typeof (value as Point).y === "number"
  );
}

// Generic type guard
function isArray<T>(value: unknown, itemGuard: (item: unknown) => item is T): value is T[] {
  return Array.isArray(value) && value.every(itemGuard);
}

function isNumber(value: unknown): value is number {
  return typeof value === "number";
}

const value: unknown = [1, 2, 3];
if (isArray(value, isNumber)) {
  // value is number[]
  value.forEach((n) => console.log(n * 2));
}

// Assertion function (alternative to type predicate)
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("Value is not a string");
  }
}

function processValue(value: unknown) {
  assertIsString(value);
  // value is string from this point on
  console.log(value.toUpperCase());
}

// Assertion function with condition
function assert(condition: unknown, message: string): asserts condition {
  if (!condition) {
    throw new Error(message);
  }
}

function getUser(id: string): User | undefined {
  return undefined; // Placeholder
}

function processUser(id: string) {
  const user = getUser(id);
  assert(user !== undefined, "User not found");
  // user is User (not undefined) from this point
  console.log(user.name);
}
```

### Narrowing with Control Flow

```typescript
// Equality narrowing
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    // x and y are both string
    x.toUpperCase();
    y.toUpperCase();
  }
}

// Discriminated union narrowing (see next section)
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; sideLength: number };

function getArea(shape: Shape) {
  if (shape.kind === "circle") {
    // shape is { kind: "circle"; radius: number }
    return Math.PI * shape.radius ** 2;
  } else {
    // shape is { kind: "square"; sideLength: number }
    return shape.sideLength ** 2;
  }
}

// Exhaustiveness checking
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

function getAreaWithExhaustiveness(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
    default:
      return assertNever(shape); // Ensures all cases are handled
  }
}

// Array.isArray narrowing
function processValue(value: string | string[]) {
  if (Array.isArray(value)) {
    // value is string[]
    value.forEach((s) => console.log(s));
  } else {
    // value is string
    console.log(value);
  }
}
```

---

## Discriminated Unions

### Basic Discriminated Unions

```typescript
// Simple discriminated union
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}

interface Triangle {
  kind: "triangle";
  base: number;
  height: number;
}

type Shape = Circle | Square | Triangle;

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
    case "triangle":
      return (shape.base * shape.height) / 2;
  }
}

// String literal discriminant
type LoadingState = {
  status: "loading";
};

type SuccessState<T> = {
  status: "success";
  data: T;
};

type ErrorState = {
  status: "error";
  error: Error;
};

type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState;

function renderState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case "loading":
      return "Loading...";
    case "success":
      return `Data: ${state.data}`;
    case "error":
      return `Error: ${state.error.message}`;
  }
}
```

### Advanced Discriminated Union Patterns

```typescript
// Multiple discriminants
type UserEvent =
  | {
      type: "login";
      method: "email" | "oauth";
      timestamp: number;
    }
  | {
      type: "logout";
      reason: "manual" | "timeout";
      timestamp: number;
    }
  | {
      type: "purchase";
      itemId: string;
      amount: number;
      timestamp: number;
    };

function handleEvent(event: UserEvent) {
  console.log(`Event at ${event.timestamp}`);

  switch (event.type) {
    case "login":
      console.log(`Login via ${event.method}`);
      break;
    case "logout":
      console.log(`Logout: ${event.reason}`);
      break;
    case "purchase":
      console.log(`Purchase: ${event.itemId} for $${event.amount}`);
      break;
  }
}

// Discriminated union with shared properties
type ApiResponse<T> =
  | {
      success: true;
      data: T;
      timestamp: number;
    }
  | {
      success: false;
      error: string;
      timestamp: number;
    };

function handleResponse<T>(response: ApiResponse<T>): T {
  if (response.success) {
    return response.data;
  } else {
    throw new Error(response.error);
  }
}

// Nested discriminated unions
type FormField =
  | {
      type: "text";
      value: string;
      validation: {
        type: "regex";
        pattern: string;
      } | {
        type: "length";
        min: number;
        max: number;
      };
    }
  | {
      type: "number";
      value: number;
      validation: {
        type: "range";
        min: number;
        max: number;
      };
    };

function validateField(field: FormField): boolean {
  if (field.type === "text") {
    if (field.validation.type === "regex") {
      return new RegExp(field.validation.pattern).test(field.value);
    } else {
      return (
        field.value.length >= field.validation.min &&
        field.value.length <= field.validation.max
      );
    }
  } else {
    return (
      field.value >= field.validation.min && field.value <= field.validation.max
    );
  }
}
```

### Tagged Union Helper Types

```typescript
// Extract specific union member by discriminant
type ExtractByType<Union, Type> = Union extends { type: Type } ? Union : never;

type LoginEvent = ExtractByType<UserEvent, "login">;
// { type: "login"; method: "email" | "oauth"; timestamp: number }

// Get all discriminant values
type DiscriminantValue<Union, Key extends keyof Union> = Union extends Record<Key, infer D>
  ? D
  : never;

type EventTypes = DiscriminantValue<UserEvent, "type">;
// "login" | "logout" | "purchase"

// Create discriminated union from object
type CreateUnion<T extends Record<string, any>> = {
  [K in keyof T]: { type: K } & T[K];
}[keyof T];

type Events = CreateUnion<{
  click: { x: number; y: number };
  scroll: { top: number; left: number };
  resize: { width: number; height: number };
}>;
// { type: "click"; x: number; y: number }
// | { type: "scroll"; top: number; left: number }
// | { type: "resize"; width: number; height: number }
```

---

## Mapped Types

### Basic Mapped Types

```typescript
// Simple mapped type
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

type Partial<T> = {
  [K in keyof T]?: T[K];
};

// Mapped type with union
type Flags = {
  [K in "option1" | "option2" | "option3"]: boolean;
};
// { option1: boolean; option2: boolean; option3: boolean }

// Mapped type from object keys
interface Person {
  name: string;
  age: number;
}

type PersonFlags = {
  [K in keyof Person]: boolean;
};
// { name: boolean; age: boolean }

// Transform values
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

type Stringify<T> = {
  [K in keyof T]: string;
};
```

### Mapped Type Modifiers

```typescript
// Remove readonly modifier
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

interface ReadonlyPerson {
  readonly name: string;
  readonly age: number;
}

type MutablePerson = Mutable<ReadonlyPerson>;
// { name: string; age: number }

// Remove optional modifier
type Required<T> = {
  [K in keyof T]-?: T[K];
};

interface OptionalPerson {
  name?: string;
  age?: number;
}

type RequiredPerson = Required<OptionalPerson>;
// { name: string; age: number }

// Add readonly modifier
type Immutable<T> = {
  +readonly [K in keyof T]: T[K];
};

// Add optional modifier
type AllOptional<T> = {
  +? [K in keyof T]: T[K];
};
```

### Key Remapping (TypeScript 4.1+)

```typescript
// Rename keys
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person {
  name: string;
  age: number;
}

type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }

// Filter keys
type RemoveKind<T> = {
  [K in keyof T as Exclude<K, "kind">]: T[K];
};

interface Shape {
  kind: string;
  radius: number;
}

type ShapeWithoutKind = RemoveKind<Shape>;
// { radius: number }

// Conditional key mapping
type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

interface Mixed {
  a: string;
  b: number;
  c: string;
  d: boolean;
}

type StringProperties = PickByType<Mixed, string>;
// { a: string; c: string }

// Transform keys based on condition
type PrefixWithUnderscore<T> = {
  [K in keyof T as K extends string ? `_${K}` : K]: T[K];
};

type PrivatePerson = PrefixWithUnderscore<Person>;
// { _name: string; _age: number }
```

### Advanced Mapped Type Patterns

```typescript
// Deep readonly
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object
    ? T[K] extends Function
      ? T[K]
      : DeepReadonly<T[K]>
    : T[K];
};

// Deep partial with handling for arrays
type DeepPartial<T> = T extends Function
  ? T
  : T extends Array<infer U>
  ? DeepPartialArray<U>
  : T extends object
  ? DeepPartialObject<T>
  : T | undefined;

interface DeepPartialArray<T> extends Array<DeepPartial<T>> {}

type DeepPartialObject<T> = {
  [K in keyof T]?: DeepPartial<T[K]>;
};

// Proxy type for getters and setters
type Proxify<T> = {
  [K in keyof T]: {
    get(): T[K];
    set(value: T[K]): void;
  };
};

interface Person {
  name: string;
  age: number;
}

type ProxifiedPerson = Proxify<Person>;
// {
//   name: { get(): string; set(value: string): void };
//   age: { get(): number; set(value: number): void };
// }

// Flatten nested types
type Flatten<T> = T extends Array<infer U> ? U : T;

type Str = Flatten<string[]>; // string
type Num = Flatten<number>; // number

// Create union of property values
type ValueOf<T> = T[keyof T];

type PersonValues = ValueOf<Person>;
// string | number
```

---

## Conditional Types

### Basic Conditional Types

```typescript
// Simple conditional type
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false

// Conditional type with inference
type ArrayElement<T> = T extends Array<infer E> ? E : T;

type ItemType = ArrayElement<string[]>; // string
type SingleType = ArrayElement<number>; // number

// Nested conditional types
type TypeName<T> = T extends string
  ? "string"
  : T extends number
  ? "number"
  : T extends boolean
  ? "boolean"
  : T extends undefined
  ? "undefined"
  : T extends Function
  ? "function"
  : "object";

type T0 = TypeName<string>; // "string"
type T1 = TypeName<"a">; // "string"
type T2 = TypeName<true>; // "boolean"
type T3 = TypeName<() => void>; // "function"
type T4 = TypeName<string[]>; // "object"
```

### Distributive Conditional Types

```typescript
// Distributive over unions
type ToArray<T> = T extends any ? T[] : never;

type StrArrOrNumArr = ToArray<string | number>;
// string[] | number[] (distributes over union)

// Non-distributive (wrap in tuple)
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;

type StrOrNumArr = ToArrayNonDist<string | number>;
// (string | number)[] (does not distribute)

// Filter union members
type Filter<T, U> = T extends U ? T : never;

type T0 = Filter<string | number | boolean, string | number>;
// string | number

// Exclude implementation
type MyExclude<T, U> = T extends U ? never : T;

type T1 = MyExclude<"a" | "b" | "c", "a">;
// "b" | "c"

// Extract implementation
type MyExtract<T, U> = T extends U ? T : never;

type T2 = MyExtract<"a" | "b" | "c", "a" | "f">;
// "a"

// NonNullable implementation
type MyNonNullable<T> = T extends null | undefined ? never : T;

type T3 = MyNonNullable<string | number | null | undefined>;
// string | number
```

### Conditional Type Inference

```typescript
// Infer function return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type Func1 = () => string;
type Ret1 = ReturnType<Func1>; // string

// Infer function parameters
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

type Func2 = (a: string, b: number) => void;
type Params = Parameters<Func2>; // [string, number]

// Infer array element type
type Unpacked<T> = T extends Array<infer U>
  ? U
  : T extends Promise<infer U>
  ? U
  : T extends (...args: any[]) => infer U
  ? U
  : T;

type T0 = Unpacked<string[]>; // string
type T1 = Unpacked<Promise<number>>; // number
type T2 = Unpacked<() => boolean>; // boolean
type T3 = Unpacked<string>; // string

// Infer tuple elements
type First<T> = T extends [infer F, ...any[]] ? F : never;
type Last<T> = T extends [...any[], infer L] ? L : never;

type Tuple = [string, number, boolean];
type F = First<Tuple>; // string
type L = Last<Tuple>; // boolean

// Infer object property types
type PropertyType<T, K extends keyof T> = T extends { [P in K]: infer V }
  ? V
  : never;

type Person = { name: string; age: number };
type NameType = PropertyType<Person, "name">; // string
```

### Advanced Conditional Type Patterns

```typescript
// Recursive conditional types
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

type P1 = Awaited<Promise<string>>; // string
type P2 = Awaited<Promise<Promise<number>>>; // number

// Flatten array type recursively
type DeepFlatten<T> = T extends Array<infer U> ? DeepFlatten<U> : T;

type Nested = number[][][][];
type Flat = DeepFlatten<Nested>; // number

// Get required keys
type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

interface User {
  id: string;
  name: string;
  email?: string;
  age?: number;
}

type Req = RequiredKeys<User>; // "id" | "name"
type Opt = OptionalKeys<User>; // "email" | "age"

// Merge types with conditional override
type Merge<T, U> = {
  [K in keyof T | keyof U]: K extends keyof U
    ? U[K]
    : K extends keyof T
    ? T[K]
    : never;
};

type A = { a: string; b: number };
type B = { b: boolean; c: string };
type C = Merge<A, B>;
// { a: string; b: boolean; c: string }

// Function overload extraction
type OverloadedReturnType<T> = T extends {
  (...args: any[]): infer R;
  (...args: any[]): infer R;
  (...args: any[]): infer R;
  (...args: any[]): infer R;
}
  ? R
  : T extends {
      (...args: any[]): infer R;
      (...args: any[]): infer R;
      (...args: any[]): infer R;
    }
  ? R
  : T extends { (...args: any[]): infer R; (...args: any[]): infer R }
  ? R
  : T extends (...args: any[]) => infer R
  ? R
  : never;
```

---

## Type Inference

### Contextual Typing

```typescript
// Contextual typing in callbacks
const numbers = [1, 2, 3];

// Parameter type inferred from array type
numbers.map((n) => n * 2); // n is number

// Contextual typing with generic functions
function forEach<T>(arr: T[], callback: (item: T, index: number) => void) {
  for (let i = 0; i < arr.length; i++) {
    callback(arr[i], i);
  }
}

forEach(["a", "b", "c"], (item, index) => {
  // item is string, index is number (both inferred)
  console.log(item.toUpperCase(), index);
});

// Contextual typing with object literals
interface Point {
  x: number;
  y: number;
}

const point: Point = {
  x: 10,
  y: 20,
  // z: 30, // Error: object literal may only specify known properties
};

// Contextual typing with event handlers
const button = document.querySelector("button");

button?.addEventListener("click", (event) => {
  // event is MouseEvent (inferred from addEventListener signature)
  console.log(event.clientX, event.clientY);
});
```

### Type Inference with Generics

```typescript
// Generic function inference
function identity<T>(value: T): T {
  return value;
}

const num = identity(42); // T inferred as number
const str = identity("hello"); // T inferred as string

// Multiple generic parameters
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

const p = pair(1, "one"); // T is number, U is string

// Inference with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name"); // string inferred
const age = getProperty(user, "age"); // number inferred

// Generic class inference
class Box<T> {
  constructor(public value: T) {}
}

const box1 = new Box(42); // Box<number>
const box2 = new Box("hello"); // Box<string>

// Explicit generic arguments when needed
const box3 = new Box<string | number>(42); // Box<string | number>
```

### Return Type Inference

```typescript
// Infer return type from implementation
function createUser(name: string, age: number) {
  return {
    name,
    age,
    createdAt: new Date(),
  };
}

// Return type inferred as:
// { name: string; age: number; createdAt: Date }

// Use ReturnType utility
type User = ReturnType<typeof createUser>;

// Infer from conditional logic
function getValue(condition: boolean) {
  if (condition) {
    return "yes";
  } else {
    return 42;
  }
}

// Return type inferred as: string | number

// Discriminated union return
function getShape(kind: "circle" | "square") {
  if (kind === "circle") {
    return { kind: "circle" as const, radius: 10 };
  } else {
    return { kind: "square" as const, sideLength: 20 };
  }
}

// Return type inferred as:
// { kind: "circle"; radius: number } | { kind: "square"; sideLength: number }
```

### Best Practices for Type Inference

```typescript
// Use const assertions for literal types
const config = {
  api: "https://api.example.com",
  timeout: 5000,
} as const;

// Type is:
// {
//   readonly api: "https://api.example.com";
//   readonly timeout: 5000;
// }

// Without as const:
// {
//   api: string;
//   timeout: number;
// }

// Infer tuple types
const tuple1 = [1, "hello"]; // (string | number)[]
const tuple2 = [1, "hello"] as const; // readonly [1, "hello"]
const tuple3: [number, string] = [1, "hello"]; // [number, string]

// Helper function for tuple inference
function tuple<T extends any[]>(...args: T): T {
  return args;
}

const t = tuple(1, "hello", true); // [number, string, boolean]

// Narrow types with satisfies operator (TypeScript 4.9+)
type Color = { r: number; g: number; b: number };

const palette = {
  red: { r: 255, g: 0, b: 0 },
  green: { r: 0, g: 255, b: 0 },
  blue: { r: 0, g: 0, b: 255 },
} satisfies Record<string, Color>;

// palette.red is inferred as { r: number; g: number; b: number }
// but palette type is still the specific object literal type
```

---

## Declaration Files

### Basic Declaration File Structure

```typescript
// example.d.ts

// Declare global variable
declare const API_KEY: string;

// Declare global function
declare function myFunction(arg: string): number;

// Declare namespace
declare namespace MyLibrary {
  function initialize(config: Config): void;

  interface Config {
    apiKey: string;
    debug?: boolean;
  }

  class Client {
    constructor(config: Config);
    request(endpoint: string): Promise<Response>;
  }
}

// Declare module
declare module "my-library" {
  export function doSomething(value: string): number;
  export interface Options {
    timeout: number;
  }
}

// Ambient module for CSS modules
declare module "*.module.css" {
  const classes: { [key: string]: string };
  export default classes;
}

// Ambient module for images
declare module "*.png" {
  const content: string;
  export default content;
}
```

### Module Augmentation

```typescript
// Augment existing module
declare module "express" {
  interface Request {
    user?: {
      id: string;
      email: string;
    };
  }
}

// Augment global scope
declare global {
  interface Window {
    myCustomProperty: string;
  }

  namespace NodeJS {
    interface ProcessEnv {
      DATABASE_URL: string;
      API_KEY: string;
    }
  }
}

// Export to make this a module
export {};

// Usage
window.myCustomProperty = "value";
const dbUrl = process.env.DATABASE_URL;
```

### Triple-Slash Directives

```typescript
/// <reference path="./types.d.ts" />
/// <reference types="node" />
/// <reference lib="es2020" />

// Triple-slash directives must be at the top of the file

// Reference path - include another file
/// <reference path="./custom-types.d.ts" />

// Reference types - include @types package
/// <reference types="jquery" />

// Reference lib - include built-in library
/// <reference lib="dom" />
/// <reference lib="es2015" />
```

### Writing Declaration Files for Libraries

```typescript
// mylib.d.ts - Declaration file for JavaScript library

// Default export
declare module "mylib" {
  // Named exports
  export function initialize(config: Config): void;
  export function process(data: Data): Result;

  // Type exports
  export interface Config {
    apiKey: string;
    endpoint?: string;
  }

  export interface Data {
    id: string;
    value: any;
  }

  export interface Result {
    success: boolean;
    data?: any;
    error?: string;
  }

  // Class export
  export class Client {
    constructor(config: Config);
    request<T>(endpoint: string): Promise<T>;
    upload(file: File): Promise<void>;
  }

  // Constant export
  export const VERSION: string;

  // Default export
  const mylib: {
    initialize: typeof initialize;
    process: typeof process;
    Client: typeof Client;
  };

  export default mylib;
}

// UMD module pattern
export as namespace MyLib;
export = MyLib;

declare namespace MyLib {
  function doSomething(): void;
}
```

---

## Strict Mode

### Strict Mode Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    // Enable all strict type checking options
    "strict": true,

    // Individual strict options (enabled by "strict": true)
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional strict options
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### strictNullChecks

```typescript
// With strictNullChecks enabled

// Error: Type 'null' is not assignable to type 'string'
let name: string = null;

// Correct: use union type
let name: string | null = null;

// Handling null/undefined
function greet(name: string | null) {
  if (name === null) {
    console.log("Hello, stranger!");
  } else {
    console.log(`Hello, ${name}!`);
  }
}

// Non-null assertion operator (use sparingly)
function getLength(str: string | null): number {
  return str!.length; // Asserts str is not null
}

// Optional chaining
const user = { name: "Alice", address: { city: "NYC" } };
const city = user?.address?.city; // string | undefined

// Nullish coalescing
const displayName = name ?? "Anonymous";
```

### strictFunctionTypes

```typescript
// With strictFunctionTypes enabled

interface Animal {
  name: string;
}

interface Dog extends Animal {
  breed: string;
}

// Error: function types are checked contravariantly
let animalHandler: (animal: Animal) => void;
let dogHandler: (dog: Dog) => void;

animalHandler = dogHandler; // Error
dogHandler = animalHandler; // OK

// Method syntax bypasses contravariance check
interface Comparer<T> {
  compare(a: T, b: T): number;
}

let animalComparer: Comparer<Animal>;
let dogComparer: Comparer<Dog>;

animalComparer = dogComparer; // OK (method syntax)
```

### strictPropertyInitialization

```typescript
// With strictPropertyInitialization enabled

class User {
  // Error: Property has no initializer
  name: string;
  age: number;

  // Solutions:

  // 1. Initialize in constructor
  email: string;

  constructor(email: string) {
    this.email = email;
  }

  // 2. Provide default value
  isActive: boolean = false;

  // 3. Declare as optional
  phone?: string;

  // 4. Use definite assignment assertion
  id!: string; // Asserts it will be assigned before use

  initialize() {
    this.id = crypto.randomUUID();
  }
}
```

### noImplicitAny

```typescript
// With noImplicitAny enabled

// Error: Parameter 'x' implicitly has an 'any' type
function log(x) {
  console.log(x);
}

// Correct: explicit type annotation
function log(x: unknown) {
  console.log(x);
}

// Error: Variable 'data' implicitly has an 'any' type
const data = JSON.parse(jsonString);

// Correct: type annotation
const data: MyType = JSON.parse(jsonString);

// Or use unknown and type guard
const data: unknown = JSON.parse(jsonString);
if (isMyType(data)) {
  // data is MyType
}
```

### noUncheckedIndexedAccess

```typescript
// With noUncheckedIndexedAccess enabled

const users: Record<string, User> = {};

// Type is User | undefined (not just User)
const user = users["alice"];

// Must check before use
if (user) {
  console.log(user.name);
}

// Array access also affected
const arr = [1, 2, 3];
const item = arr[10]; // number | undefined

// Safe access
if (item !== undefined) {
  console.log(item * 2);
}
```

---

## Anti-Patterns

### 1. Overusing `any`

```typescript
// BAD: Defeats type safety
function processData(data: any): any {
  return data.value.toString();
}

// GOOD: Use specific types or generics
function processData<T extends { value: string | number }>(data: T): string {
  return data.value.toString();
}

// GOOD: Use unknown when type is truly unknown
function processData(data: unknown): string {
  if (typeof data === "object" && data !== null && "value" in data) {
    const value = (data as { value: unknown }).value;
    if (typeof value === "string" || typeof value === "number") {
      return value.toString();
    }
  }
  throw new Error("Invalid data");
}
```

### 2. Type Assertions Instead of Type Guards

```typescript
// BAD: Unsafe type assertion
function getUser(id: string): User {
  const data = fetchData(id);
  return data as User; // No runtime check
}

// GOOD: Type guard with validation
function getUser(id: string): User {
  const data = fetchData(id);
  if (isUser(data)) {
    return data;
  }
  throw new Error("Invalid user data");
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    typeof (value as User).id === "string" &&
    typeof (value as User).name === "string"
  );
}
```

### 3. Ignoring Null/Undefined

```typescript
// BAD: Assumes value exists
function greet(user: User | null) {
  return `Hello, ${user.name}!`; // Error with strictNullChecks
}

// GOOD: Handle null case
function greet(user: User | null): string {
  if (!user) {
    return "Hello, stranger!";
  }
  return `Hello, ${user.name}!`;
}

// GOOD: Use optional chaining
function greet(user: User | null): string {
  return `Hello, ${user?.name ?? "stranger"}!`;
}
```

### 4. Not Using Readonly

```typescript
// BAD: Mutable when should be immutable
interface Config {
  apiKey: string;
  endpoints: string[];
}

function updateConfig(config: Config) {
  config.apiKey = "new-key"; // Unexpected mutation
  config.endpoints.push("new-endpoint");
}

// GOOD: Use readonly
interface Config {
  readonly apiKey: string;
  readonly endpoints: readonly string[];
}

// GOOD: Deep readonly
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

type ImmutableConfig = DeepReadonly<Config>;
```

### 5. Excessive Union Types

```typescript
// BAD: Too broad, loses type safety
type Result = string | number | boolean | null | undefined | object;

function process(value: Result): void {
  // No meaningful narrowing possible
}

// GOOD: Discriminated union
type Result =
  | { type: "string"; value: string }
  | { type: "number"; value: number }
  | { type: "boolean"; value: boolean }
  | { type: "error"; error: Error };

function process(result: Result): void {
  switch (result.type) {
    case "string":
      console.log(result.value.toUpperCase());
      break;
    case "number":
      console.log(result.value.toFixed(2));
      break;
    case "boolean":
      console.log(result.value ? "yes" : "no");
      break;
    case "error":
      console.error(result.error);
      break;
  }
}
```

### 6. Not Using Const Assertions

```typescript
// BAD: Widened types
const colors = ["red", "green", "blue"]; // string[]
const config = { apiKey: "key", timeout: 5000 }; // { apiKey: string; timeout: number }

// GOOD: Const assertion for literal types
const colors = ["red", "green", "blue"] as const; // readonly ["red", "green", "blue"]
const config = { apiKey: "key", timeout: 5000 } as const;
// { readonly apiKey: "key"; readonly timeout: 5000 }
```

### 7. Ignoring Function Return Types

```typescript
// BAD: Implicit return type
function calculate(a: number, b: number) {
  if (a > b) {
    return a - b;
  }
  // Oops, forgot to return in else case (returns undefined)
}

// GOOD: Explicit return type
function calculate(a: number, b: number): number {
  if (a > b) {
    return a - b;
  }
  return b - a; // Compiler enforces return
}

// GOOD: Enable noImplicitReturns in tsconfig
```

### 8. Overcomplicating Types

```typescript
// BAD: Overly complex type
type ComplexType<T> = T extends Array<infer U>
  ? U extends object
    ? {
        [K in keyof U]: U[K] extends Function
          ? never
          : U[K] extends object
          ? ComplexType<[U[K]]>
          : U[K];
      }
    : U
  : T;

// GOOD: Break into smaller, named types
type NonFunctionKeys<T> = {
  [K in keyof T]: T[K] extends Function ? never : K;
}[keyof T];

type NonFunctionProps<T> = Pick<T, NonFunctionKeys<T>>;

type DeepNonFunctionProps<T> = {
  [K in keyof NonFunctionProps<T>]: NonFunctionProps<T>[K] extends object
    ? DeepNonFunctionProps<NonFunctionProps<T>[K]>
    : NonFunctionProps<T>[K];
};
```

### 9. Not Using Index Signatures Properly

```typescript
// BAD: Overly permissive
interface UserMap {
  [key: string]: User;
}

const users: UserMap = {
  alice: { id: "1", name: "Alice" },
  count: { id: "2", name: "Bob" }, // Accidentally shadows a potential method
};

// GOOD: Use Record or Map
type UserMap = Record<string, User>;
// Or better:
const users = new Map<string, User>();

// GOOD: Specific keys with index signature
interface ApiResponse {
  status: number;
  message: string;
  [key: string]: unknown; // Additional dynamic properties
}
```

### 10. Mutating Parameters

```typescript
// BAD: Mutates input parameter
function addItem<T>(arr: T[], item: T): T[] {
  arr.push(item); // Mutates original array
  return arr;
}

// GOOD: Pure function
function addItem<T>(arr: readonly T[], item: T): T[] {
  return [...arr, item]; // Returns new array
}

// GOOD: Clear mutation intent
function addItemMutate<T>(arr: T[], item: T): void {
  arr.push(item);
}
```

---

## Best Practices Summary

### 1. Enable Strict Mode
Always use `"strict": true` in `tsconfig.json` for maximum type safety.

### 2. Prefer Type Inference
Let TypeScript infer types when possible, but provide explicit annotations for public APIs.

### 3. Use Discriminated Unions
For complex state or variants, use discriminated unions instead of optional properties.

### 4. Leverage Utility Types
Use built-in utility types (`Partial`, `Pick`, `Omit`, `Record`, etc.) instead of reinventing them.

### 5. Write Type Guards
Create type guards for runtime validation and type narrowing.

### 6. Avoid Type Assertions
Use type guards and validation instead of type assertions (`as`) when possible.

### 7. Use Const Assertions
Use `as const` for literal types and immutable data structures.

### 8. Document Complex Types
Add JSDoc comments to complex type definitions for better IDE support.

### 9. Test Your Types
Use tools like `expect-type` or `tsd` to test type definitions.

### 10. Keep Types Simple
Break complex types into smaller, composable pieces with clear names.

---

## Conclusion

TypeScript's type system is powerful and expressive, enabling you to write safer, more maintainable code. By mastering generics, utility types, type guards, and advanced patterns like discriminated unions and conditional types, you can leverage the full power of TypeScript's static analysis.

Key takeaways:
- Use strict mode for maximum type safety
- Prefer type inference but provide explicit types for APIs
- Use discriminated unions for complex state modeling
- Create custom type guards for runtime validation
- Leverage utility types and build your own when needed
- Avoid `any` and type assertions; use `unknown` and type guards instead
- Use const assertions for literal types
- Keep types simple and composable

By following these patterns and avoiding anti-patterns, you'll write TypeScript code that is both type-safe and maintainable.


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

