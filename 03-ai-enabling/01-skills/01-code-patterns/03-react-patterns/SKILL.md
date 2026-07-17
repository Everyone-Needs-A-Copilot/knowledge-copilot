---
last_updated: 2026-02-25
status: active
name: react-patterns
description: Modern React patterns with hooks, composition, and state management. Use when building React/Next.js components or working with React codebases.
triggers:
  files: ["**/*.jsx", "**/*.tsx", "**/components/**", "**/app/**", "**/pages/**"]
  keywords: ["hook", "useState", "useEffect", "useContext", "useMemo", "useCallback", "memo", "composition", "render props", "custom hook", "react", "next.js"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# React Patterns

## Overview

Modern React development (Hooks era, React 16.8+) emphasizes functional components, composition, and declarative patterns. This skill covers battle-tested patterns for building maintainable, performant React applications.

**Philosophy:**
- **Composition over inheritance** - Build complex UIs from simple, reusable pieces
- **Unidirectional data flow** - Props down, events up
- **Declarative UI** - Describe what to render, not how to mutate DOM
- **Hooks for logic reuse** - Extract and share stateful logic
- **Separation of concerns** - Presentation vs. behavior vs. data fetching


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## Core Principles

### 1. Component Design

**Single Responsibility**: Each component should do one thing well.

```tsx
// ❌ BAD: Component doing too much
function UserDashboard() {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState([]);

  useEffect(() => {
    fetch('/api/user').then(r => r.json()).then(setUser);
    fetch('/api/posts').then(r => r.json()).then(setPosts);
    fetch('/api/comments').then(r => r.json()).then(setComments);
  }, []);

  return (
    <div>
      {/* Complex rendering logic for user, posts, comments */}
    </div>
  );
}

// ✅ GOOD: Separated concerns
function UserDashboard() {
  return (
    <div>
      <UserProfile />
      <UserPosts />
      <UserComments />
    </div>
  );
}

function UserProfile() {
  const user = useUser();
  return <ProfileCard user={user} />;
}

function UserPosts() {
  const posts = usePosts();
  return <PostsList posts={posts} />;
}
```

**Props Interface Design**: Make components flexible but not overloaded.

```tsx
// ✅ Good props interface
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  className?: string; // Allow style override
}

function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  className
}: ButtonProps) {
  return (
    <button
      className={cn(
        'btn',
        `btn-${variant}`,
        `btn-${size}`,
        className
      )}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### 2. Composition Patterns

**Children Prop**: Most flexible composition.

```tsx
// ✅ Flexible container
function Card({ children }: { children: React.ReactNode }) {
  return <div className="card">{children}</div>;
}

// Usage allows any combination
<Card>
  <CardHeader title="Profile" />
  <CardContent>
    <UserInfo />
  </CardContent>
  <CardFooter>
    <Button>Edit</Button>
  </CardFooter>
</Card>
```

**Compound Components**: Related components that work together.

```tsx
// ✅ Compound component pattern
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined);

function Tabs({
  defaultTab,
  children
}: {
  defaultTab: string;
  children: React.ReactNode;
}) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({
  id,
  children
}: {
  id: string;
  children: React.ReactNode;
}) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');

  const { activeTab, setActiveTab } = context;

  return (
    <button
      className={cn('tab', activeTab === id && 'tab-active')}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({
  id,
  children
}: {
  id: string;
  children: React.ReactNode;
}) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');

  const { activeTab } = context;
  if (activeTab !== id) return null;

  return <div className="tab-panel">{children}</div>;
}

// Export as namespace
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
<Tabs defaultTab="profile">
  <Tabs.List>
    <Tabs.Tab id="profile">Profile</Tabs.Tab>
    <Tabs.Tab id="settings">Settings</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="profile">
    <UserProfile />
  </Tabs.Panel>
  <Tabs.Panel id="settings">
    <UserSettings />
  </Tabs.Panel>
</Tabs>
```

**Render Props**: Pass rendering logic as a function.

```tsx
// ✅ Render prop for flexible rendering
interface MousePositionProps {
  children: (position: { x: number; y: number }) => React.ReactNode;
}

function MousePosition({ children }: MousePositionProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return <>{children(position)}</>;
}

// Usage
<MousePosition>
  {({ x, y }) => (
    <div>Mouse at: {x}, {y}</div>
  )}
</MousePosition>
```

## Hook Patterns

### useState - Local Component State

**Basic State:**

```tsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(c => c + 1)}>Increment (functional)</button>
    </div>
  );
}
```

**Functional Updates**: Always use when next state depends on previous.

```tsx
// ❌ BAD: Race condition with multiple rapid clicks
const [count, setCount] = useState(0);
setCount(count + 1);

// ✅ GOOD: Functional update
setCount(c => c + 1);
```

**Lazy Initialization**: Expensive initial state computation.

```tsx
// ❌ BAD: Runs on every render
const [data, setData] = useState(expensiveComputation());

// ✅ GOOD: Only runs once
const [data, setData] = useState(() => expensiveComputation());
```

**Complex State Objects:**

```tsx
interface FormState {
  name: string;
  email: string;
  age: number;
}

function Form() {
  const [formData, setFormData] = useState<FormState>({
    name: '',
    email: '',
    age: 0
  });

  // ✅ Update single field while preserving others
  const updateField = (field: keyof FormState, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <form>
      <input
        value={formData.name}
        onChange={e => updateField('name', e.target.value)}
      />
      <input
        value={formData.email}
        onChange={e => updateField('email', e.target.value)}
      />
      <input
        type="number"
        value={formData.age}
        onChange={e => updateField('age', parseInt(e.target.value))}
      />
    </form>
  );
}
```

### useEffect - Side Effects

**Basic Effect:**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(setUser);
  }, [userId]); // Re-run when userId changes

  return <div>{user?.name}</div>;
}
```

**Cleanup Pattern**: Always cleanup subscriptions, timers, listeners.

```tsx
function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);

    // ✅ Cleanup on unmount or before re-running effect
    return () => clearInterval(interval);
  }, []);

  return <div>Seconds: {seconds}</div>;
}
```

**Effect Dependencies**: Be explicit and complete.

```tsx
// ❌ BAD: Missing dependency
function SearchResults({ query }: { query: string }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetchResults(query).then(setResults);
  }, []); // Bug: won't update when query changes

  return <ResultsList results={results} />;
}

// ✅ GOOD: All dependencies listed
function SearchResults({ query }: { query: string }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetchResults(query).then(setResults);
  }, [query]); // Updates when query changes

  return <ResultsList results={results} />;
}
```

**Async Effects**: Proper cancellation and race condition handling.

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        if (!cancelled) {
          setUser(data);
          setLoading(false);
        }
      });

    // ✅ Cancel if userId changes before fetch completes
    return () => {
      cancelled = true;
    };
  }, [userId]);

  if (loading) return <Spinner />;
  return <div>{user?.name}</div>;
}
```

**Modern: AbortController for fetch cancellation:**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    fetch(`/api/users/${userId}`, { signal: controller.signal })
      .then(r => r.json())
      .then(setUser)
      .catch(err => {
        if (err.name === 'AbortError') return; // Ignore cancellation
        console.error(err);
      });

    return () => controller.abort();
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

### useContext - Avoid Prop Drilling

**Context Definition:**

```tsx
interface ThemeContextValue {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(t => t === 'light' ? 'dark' : 'light');
  };

  const value = { theme, toggleTheme };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// ✅ Custom hook for consuming context
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage in components
function ThemedButton() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      className={`btn btn-${theme}`}
      onClick={toggleTheme}
    >
      Toggle Theme
    </button>
  );
}
```

**Context Optimization**: Split contexts to prevent unnecessary re-renders.

```tsx
// ❌ BAD: Single context causes all consumers to re-render
const AppContext = createContext({ user, theme, settings });

// ✅ GOOD: Separate contexts for independent concerns
const UserContext = createContext({ user });
const ThemeContext = createContext({ theme });
const SettingsContext = createContext({ settings });
```

### useReducer - Complex State Logic

**When to use useReducer:**
- State transitions are complex
- Multiple sub-values or related state
- Next state depends on previous state
- Want to centralize state logic

```tsx
interface State {
  user: User | null;
  loading: boolean;
  error: string | null;
}

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: User }
  | { type: 'FETCH_ERROR'; payload: string }
  | { type: 'LOGOUT' };

function userReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_SUCCESS':
      return { user: action.payload, loading: false, error: null };
    case 'FETCH_ERROR':
      return { ...state, loading: false, error: action.payload };
    case 'LOGOUT':
      return { user: null, loading: false, error: null };
    default:
      return state;
  }
}

function UserProfile({ userId }: { userId: string }) {
  const [state, dispatch] = useReducer(userReducer, {
    user: null,
    loading: false,
    error: null
  });

  useEffect(() => {
    dispatch({ type: 'FETCH_START' });

    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(user => dispatch({ type: 'FETCH_SUCCESS', payload: user }))
      .catch(err => dispatch({ type: 'FETCH_ERROR', payload: err.message }));
  }, [userId]);

  if (state.loading) return <Spinner />;
  if (state.error) return <Error message={state.error} />;
  if (!state.user) return null;

  return <UserCard user={state.user} />;
}
```

### useMemo - Expensive Computations

**When to use useMemo:**
- Expensive calculations that would run on every render
- Creating objects/arrays that are passed as props (referential equality)
- Filtering/sorting large datasets

```tsx
function ProductList({ products, filters }: Props) {
  // ✅ Memoize expensive filtering
  const filteredProducts = useMemo(() => {
    return products
      .filter(p => p.category === filters.category)
      .filter(p => p.price >= filters.minPrice && p.price <= filters.maxPrice)
      .sort((a, b) => a.price - b.price);
  }, [products, filters]);

  return (
    <div>
      {filteredProducts.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  );
}
```

**Premature optimization warning:**

```tsx
// ❌ BAD: Unnecessary memoization
const doubled = useMemo(() => count * 2, [count]); // Overkill

// ✅ GOOD: Just compute it
const doubled = count * 2;

// ✅ GOOD: Memoize when expensive
const expensiveResult = useMemo(() => {
  return heavyComputation(data);
}, [data]);
```

### useCallback - Memoized Functions

**When to use useCallback:**
- Passing callbacks to optimized child components (wrapped in React.memo)
- Functions used as effect dependencies
- Preventing unnecessary effect re-runs

```tsx
interface TodoListProps {
  todos: Todo[];
}

function TodoList({ todos }: TodoListProps) {
  // ❌ BAD: New function on every render
  const handleDelete = (id: string) => {
    deleteTodo(id);
  };

  return (
    <div>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onDelete={handleDelete} // New reference each render
        />
      ))}
    </div>
  );
}

// ✅ GOOD: Stable function reference
function TodoList({ todos }: TodoListProps) {
  const handleDelete = useCallback((id: string) => {
    deleteTodo(id);
  }, []); // Function never changes

  return (
    <div>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}

// TodoItem can now be memoized effectively
const TodoItem = React.memo(({ todo, onDelete }: TodoItemProps) => {
  return (
    <div>
      {todo.title}
      <button onClick={() => onDelete(todo.id)}>Delete</button>
    </div>
  );
});
```

**useCallback with dependencies:**

```tsx
function SearchBox({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState('');
  const [debounceMs, setDebounceMs] = useState(300);

  // ✅ Recreate when dependencies change
  const debouncedSearch = useCallback(
    debounce((q: string) => onSearch(q), debounceMs),
    [onSearch, debounceMs]
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };

  return <input value={query} onChange={handleChange} />;
}
```

### Custom Hooks - Reusable Logic

**Extract stateful logic into custom hooks:**

```tsx
// ✅ Custom hook for data fetching
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    setLoading(true);
    fetch(url, { signal: controller.signal })
      .then(r => r.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        if (err.name === 'AbortError') return;
        setError(err.message);
        setLoading(false);
      });

    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useFetch<User>(`/api/users/${userId}`);

  if (loading) return <Spinner />;
  if (error) return <Error message={error} />;
  return <UserCard user={user!} />;
}
```

**Custom hook for local storage:**

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStoredValue = (newValue: T | ((prev: T) => T)) => {
    try {
      const valueToStore = newValue instanceof Function ? newValue(value) : newValue;
      setValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [value, setStoredValue] as const;
}

// Usage
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');

  return (
    <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
      Current: {theme}
    </button>
  );
}
```

**Custom hook for window size:**

```tsx
function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
}

// Usage
function ResponsiveComponent() {
  const { width } = useWindowSize();

  return (
    <div>
      {width < 768 ? <MobileNav /> : <DesktopNav />}
    </div>
  );
}
```

## Component Patterns

### Controlled vs Uncontrolled Components

**Controlled**: React state controls the input value.

```tsx
// ✅ Controlled input
function ControlledForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log({ name, email });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

**Uncontrolled**: DOM controls the value, React reads via ref.

```tsx
// ✅ Uncontrolled input (for simple forms)
function UncontrolledForm() {
  const nameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log({
      name: nameRef.current?.value,
      email: emailRef.current?.value
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input ref={nameRef} placeholder="Name" />
      <input ref={emailRef} placeholder="Email" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

**Rule of thumb**: Use controlled for dynamic validation, uncontrolled for simple forms.

### Error Boundaries

```tsx
// ✅ Error boundary component
interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>Something went wrong</h2>
          <pre>{this.state.error?.message}</pre>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <UserProfile userId={userId} />
</ErrorBoundary>
```

### Lazy Loading and Suspense

```tsx
// ✅ Code splitting with lazy loading
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyComponent />
    </Suspense>
  );
}

// ✅ Route-based code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));

function AppRouter() {
  return (
    <Router>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Suspense>
    </Router>
  );
}
```

### Higher-Order Components (HOC)

**Note**: Hooks are usually preferred, but HOCs are still useful for cross-cutting concerns.

```tsx
// ✅ HOC for authentication
function withAuth<P extends object>(
  Component: React.ComponentType<P>
) {
  return function AuthenticatedComponent(props: P) {
    const { user, loading } = useAuth();

    if (loading) return <Spinner />;
    if (!user) return <Navigate to="/login" />;

    return <Component {...props} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

## State Management

### When to Lift State Up

**Lift state when**:
- Multiple components need the same state
- State needs to be synchronized across components
- Parent needs to coordinate child behaviors

```tsx
// ✅ Lifted state pattern
function ParentForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: ''
  });

  const updateField = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <form>
      <NameFields
        firstName={formData.firstName}
        lastName={formData.lastName}
        onChange={updateField}
      />
      <EmailField
        email={formData.email}
        onChange={updateField}
      />
      <SubmitButton disabled={!formData.email} />
    </form>
  );
}
```

### Context vs External State

**Use Context when**:
- Data is truly global (theme, auth, locale)
- Data doesn't change frequently
- You want to avoid prop drilling

**Use external state (Zustand, Redux) when**:
- Frequent updates
- Complex state logic
- Need middleware (logging, persistence)
- Performance is critical

```tsx
// ✅ Zustand for global state
import create from 'zustand';

interface StoreState {
  count: number;
  increment: () => void;
  decrement: () => void;
}

const useStore = create<StoreState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

// Usage - no provider needed
function Counter() {
  const { count, increment, decrement } = useStore();

  return (
    <div>
      <p>{count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

### Server State (React Query / SWR)

**React Query for server state management:**

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// ✅ Fetching data
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json())
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error error={error} />;
  return <UserCard user={user} />;
}

// ✅ Mutations
function UpdateUserForm({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (userData: Partial<User>) =>
      fetch(`/api/users/${userId}`, {
        method: 'PATCH',
        body: JSON.stringify(userData)
      }).then(r => r.json()),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['user', userId] });
    }
  });

  return (
    <form onSubmit={e => {
      e.preventDefault();
      mutation.mutate({ name: 'New Name' });
    }}>
      <button type="submit" disabled={mutation.isPending}>
        Update
      </button>
    </form>
  );
}
```

## Performance Optimization

### React.memo - Prevent Unnecessary Re-renders

```tsx
// ✅ Memoized component
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

const TodoItem = React.memo(({ todo, onToggle, onDelete }: TodoItemProps) => {
  console.log('Rendering TodoItem:', todo.id);

  return (
    <div>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      <span>{todo.title}</span>
      <button onClick={() => onDelete(todo.id)}>Delete</button>
    </div>
  );
});

// Custom comparison function
const TodoItem = React.memo(
  ({ todo, onToggle, onDelete }: TodoItemProps) => {
    // Component body
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip render)
    return prevProps.todo.id === nextProps.todo.id &&
           prevProps.todo.completed === nextProps.todo.completed;
  }
);
```

### Virtualization for Long Lists

```tsx
// ✅ Virtual scrolling with react-window
import { FixedSizeList } from 'react-window';

interface RowProps {
  index: number;
  style: React.CSSProperties;
}

function VirtualizedList({ items }: { items: any[] }) {
  const Row = ({ index, style }: RowProps) => (
    <div style={style}>
      <ItemComponent item={items[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

### Code Splitting Strategies

```tsx
// ✅ Route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));

// ✅ Component-based splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));

// ✅ Conditional rendering with lazy
function Analytics() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Spinner />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

### Debouncing and Throttling

```tsx
// ✅ Debounced search input
function SearchInput({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState('');

  // Debounce the search
  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch(query);
    }, 300);

    return () => clearTimeout(timer);
  }, [query, onSearch]);

  return (
    <input
      value={query}
      onChange={e => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
}

// ✅ Using a debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchResults() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 500);

  const { data } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => searchAPI(debouncedQuery),
    enabled: debouncedQuery.length > 0
  });

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <SearchResultsList results={data} />
    </>
  );
}
```

## Anti-Patterns to Avoid

### 1. Index as Key

```tsx
// ❌ BAD: Index as key causes issues with reordering
items.map((item, index) => <Item key={index} item={item} />)

// ✅ GOOD: Use stable unique identifier
items.map(item => <Item key={item.id} item={item} />)
```

### 2. Mutating State Directly

```tsx
// ❌ BAD: Mutating state
const [items, setItems] = useState([]);
items.push(newItem); // Mutation!
setItems(items);

// ✅ GOOD: Create new array
setItems([...items, newItem]);
```

### 3. Overusing useEffect

```tsx
// ❌ BAD: Effect for derived state
const [count, setCount] = useState(0);
const [doubled, setDoubled] = useState(0);

useEffect(() => {
  setDoubled(count * 2);
}, [count]);

// ✅ GOOD: Just compute it
const [count, setCount] = useState(0);
const doubled = count * 2;
```

### 4. Not Cleaning Up Effects

```tsx
// ❌ BAD: Memory leak
useEffect(() => {
  const timer = setInterval(() => {
    console.log('tick');
  }, 1000);
  // No cleanup!
}, []);

// ✅ GOOD: Cleanup
useEffect(() => {
  const timer = setInterval(() => {
    console.log('tick');
  }, 1000);

  return () => clearInterval(timer);
}, []);
```

### 5. Prop Drilling

```tsx
// ❌ BAD: Passing props through many levels
<GrandParent user={user}>
  <Parent user={user}>
    <Child user={user}>
      <GrandChild user={user} />
    </Child>
  </Parent>
</GrandParent>

// ✅ GOOD: Use Context
const UserContext = createContext<User | undefined>(undefined);

<UserContext.Provider value={user}>
  <GrandParent>
    <Parent>
      <Child>
        <GrandChild />
      </Child>
    </Parent>
  </GrandParent>
</UserContext.Provider>

// In GrandChild:
const user = useContext(UserContext);
```

### 6. Premature Optimization

```tsx
// ❌ BAD: Memoizing everything
const Component = React.memo(() => {
  const value = useMemo(() => 1 + 1, []);
  const callback = useCallback(() => {}, []);
  const otherValue = useMemo(() => 'hello', []);

  return <div>{value}</div>;
});

// ✅ GOOD: Optimize when needed
function Component() {
  const expensiveValue = useMemo(() =>
    heavyComputation(data),
    [data]
  );

  return <div>{expensiveValue}</div>;
}
```

### 7. Large Components

```tsx
// ❌ BAD: Monolithic component
function Dashboard() {
  // 500 lines of code
  return <div>/* massive JSX */</div>;
}

// ✅ GOOD: Break into smaller components
function Dashboard() {
  return (
    <div>
      <DashboardHeader />
      <DashboardStats />
      <DashboardCharts />
      <DashboardActivity />
    </div>
  );
}
```

## Next.js Specific Patterns

### Server Components (App Router)

```tsx
// ✅ Server Component (default in app directory)
// app/users/page.tsx
async function UsersPage() {
  // This runs on the server
  const users = await fetch('https://api.example.com/users').then(r => r.json());

  return (
    <div>
      <h1>Users</h1>
      <UsersList users={users} />
    </div>
  );
}

// No need for useEffect or loading states!
```

### Client Components

```tsx
// ✅ Client Component (interactive)
// components/Counter.tsx
'use client'; // Mark as client component

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}
```

### Mixing Server and Client Components

```tsx
// ✅ Server component wrapping client component
// app/dashboard/page.tsx
async function DashboardPage() {
  const stats = await fetchDashboardStats();

  return (
    <div>
      <h1>Dashboard</h1>
      {/* Server-rendered */}
      <StatsDisplay stats={stats} />
      {/* Client-rendered for interactivity */}
      <InteractiveChart data={stats.chartData} />
    </div>
  );
}
```

### Server Actions

```tsx
// ✅ Server action for form submission
// app/actions.ts
'use server';

export async function createUser(formData: FormData) {
  const name = formData.get('name');
  const email = formData.get('email');

  await db.users.create({ name, email });
  revalidatePath('/users');
}

// app/users/new/page.tsx
import { createUser } from '../actions';

function NewUserPage() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Create User</button>
    </form>
  );
}
```

## Testing Patterns

### Component Testing with Testing Library

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Counter', () => {
  it('increments count when button clicked', async () => {
    render(<Counter />);

    const button = screen.getByRole('button', { name: /increment/i });
    const count = screen.getByText(/count: 0/i);

    expect(count).toBeInTheDocument();

    await userEvent.click(button);

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });
});
```

### Custom Hook Testing

```tsx
import { renderHook, act } from '@testing-library/react';

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## Best Practices Summary

1. **Prefer functional components** over class components
2. **Use hooks** for logic reuse instead of HOCs/render props
3. **Keep components small** and focused on one responsibility
4. **Lift state up** only when necessary
5. **Use Context sparingly** - not all state needs to be global
6. **Clean up effects** - always return cleanup function
7. **Memoize strategically** - not everything needs optimization
8. **Use TypeScript** for better developer experience
9. **Test behavior, not implementation** - use Testing Library
10. **Embrace composition** - build complex UIs from simple pieces

## Common Patterns Reference

| Pattern | Use Case | Key Hook(s) |
|---------|----------|-------------|
| Data Fetching | Load data from API | `useEffect`, custom hooks |
| Form Handling | Controlled inputs | `useState`, `useReducer` |
| Modal/Dialog | Show/hide overlay | `useState`, Portal |
| Accordion | Expand/collapse sections | `useState`, compound components |
| Tabs | Switch between views | `useState`, Context |
| Infinite Scroll | Load more on scroll | `useEffect`, `useRef` |
| Authentication | Protect routes | Context, HOC |
| Theme Switching | Light/dark mode | Context, localStorage hook |
| Debounced Search | Delay search requests | `useEffect`, custom debounce hook |
| Optimistic UI | Update UI before server | React Query mutations |

## Resources

- **Official React Docs**: https://react.dev
- **React Patterns**: https://reactpatterns.com
- **React Query**: https://tanstack.com/query
- **Next.js**: https://nextjs.org
- **Testing Library**: https://testing-library.com

---

When implementing React components:
1. Start with the simplest solution
2. Add complexity only when needed
3. Optimize based on profiling, not assumptions
4. Test user interactions, not implementation details
5. Follow the patterns that match your use case


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

