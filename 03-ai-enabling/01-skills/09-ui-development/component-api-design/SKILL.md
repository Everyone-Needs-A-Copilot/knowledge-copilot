---
last_updated: 2026-02-25
status: active
name: component-api-design
description: Clean component APIs - props, events, slots, composition patterns. Use when designing reusable UI components.
triggers:
  files: ["**/*.tsx", "**/*.jsx", "**/components/**", "**/ui/**"]
  keywords: ["component", "props", "interface", "API", "composition", "slots", "children", "render prop", "compound"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Component API Design

Design clean, intuitive, and flexible component APIs that are easy to use and maintain.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Progressive disclosure | Simple use cases should be simple |
| Composability | Small pieces that combine well |
| Consistency | Similar components behave similarly |
| Sensible defaults | Work out of the box |
| Escape hatches | Allow customization when needed |


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Props Interface Design

### Essential Props Only

```tsx
// BAD: Too many required props
interface ButtonProps {
  label: string;           // Required
  onClick: () => void;     // Required
  variant: 'primary' | 'secondary'; // Required
  size: 'sm' | 'md' | 'lg'; // Required
  disabled: boolean;       // Required
  loading: boolean;        // Required
  icon: React.ReactNode;   // Required
}

// GOOD: Minimal required, sensible defaults
interface ButtonProps {
  children: React.ReactNode;  // Required: button content
  onClick?: () => void;       // Optional: may be form submit
  variant?: 'primary' | 'secondary' | 'ghost';  // Default: 'primary'
  size?: 'sm' | 'md' | 'lg';  // Default: 'md'
  disabled?: boolean;         // Default: false
  loading?: boolean;          // Default: false
  icon?: React.ReactNode;     // Optional
}

function Button({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  icon,
}: ButtonProps) {
  return (
    <button
      className={cn('btn', `btn-${variant}`, `btn-${size}`)}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? <Spinner /> : icon}
      {children}
    </button>
  );
}

// Simple usage
<Button>Click me</Button>

// Full usage
<Button
  variant="secondary"
  size="lg"
  icon={<SaveIcon />}
  loading={isSaving}
  onClick={handleSave}
>
  Save Changes
</Button>
```

### Props Naming Conventions

| Pattern | Use Case | Examples |
|---------|----------|----------|
| `is*` / `has*` | Boolean state | `isOpen`, `hasError`, `isLoading` |
| `on*` | Event handlers | `onClick`, `onChange`, `onSubmit` |
| `render*` | Render props | `renderItem`, `renderHeader` |
| `*ClassName` | Style overrides | `className`, `containerClassName` |
| `default*` | Initial values | `defaultValue`, `defaultOpen` |

```tsx
interface DialogProps {
  // State
  isOpen: boolean;
  hasCloseButton?: boolean;

  // Events
  onClose: () => void;
  onConfirm?: () => void;

  // Content
  title: string;
  children: React.ReactNode;

  // Customization
  className?: string;
  overlayClassName?: string;
}
```

### Controlled vs Uncontrolled

```tsx
// Support both patterns
interface InputProps {
  // Uncontrolled
  defaultValue?: string;

  // Controlled
  value?: string;
  onChange?: (value: string) => void;
}

function Input({ defaultValue, value, onChange }: InputProps) {
  // Determine if controlled
  const isControlled = value !== undefined;

  // Internal state for uncontrolled
  const [internalValue, setInternalValue] = useState(defaultValue ?? '');

  const currentValue = isControlled ? value : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;

    if (!isControlled) {
      setInternalValue(newValue);
    }

    onChange?.(newValue);
  };

  return (
    <input
      value={currentValue}
      onChange={handleChange}
    />
  );
}

// Uncontrolled usage
<Input defaultValue="initial" onChange={console.log} />

// Controlled usage
<Input value={name} onChange={setName} />
```

## Composition Patterns

### Children Prop

The most flexible composition pattern.

```tsx
// Basic children
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

function Card({ children, className }: CardProps) {
  return (
    <div className={cn('card', className)}>
      {children}
    </div>
  );
}

// Usage - complete flexibility
<Card>
  <h2>Title</h2>
  <p>Description</p>
  <Button>Action</Button>
</Card>
```

### Slot Props

Named slots for structured layouts.

```tsx
interface PageLayoutProps {
  header?: React.ReactNode;
  sidebar?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

function PageLayout({ header, sidebar, children, footer }: PageLayoutProps) {
  return (
    <div className="page-layout">
      {header && <header className="page-header">{header}</header>}

      <div className="page-body">
        {sidebar && <aside className="page-sidebar">{sidebar}</aside>}
        <main className="page-content">{children}</main>
      </div>

      {footer && <footer className="page-footer">{footer}</footer>}
    </div>
  );
}

// Usage
<PageLayout
  header={<Nav />}
  sidebar={<Sidebar />}
  footer={<Footer />}
>
  <h1>Page Content</h1>
</PageLayout>
```

### Compound Components

Related components that share state.

```tsx
// Context for shared state
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tabs components must be used within Tabs');
  }
  return context;
}

// Parent component
interface TabsProps {
  defaultTab: string;
  children: React.ReactNode;
  onChange?: (tab: string) => void;
}

function Tabs({ defaultTab, children, onChange }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  const handleSetActiveTab = (tab: string) => {
    setActiveTab(tab);
    onChange?.(tab);
  };

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab: handleSetActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Sub-components
function TabList({ children }: { children: React.ReactNode }) {
  return <div role="tablist" className="tab-list">{children}</div>;
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useTabs();
  const isActive = activeTab === id;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      aria-controls={`panel-${id}`}
      className={cn('tab', isActive && 'tab-active')}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab } = useTabs();
  if (activeTab !== id) return null;

  return (
    <div role="tabpanel" id={`panel-${id}`} className="tab-panel">
      {children}
    </div>
  );
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage - intuitive, self-documenting
<Tabs defaultTab="profile" onChange={handleTabChange}>
  <Tabs.List>
    <Tabs.Tab id="profile">Profile</Tabs.Tab>
    <Tabs.Tab id="settings">Settings</Tabs.Tab>
    <Tabs.Tab id="billing">Billing</Tabs.Tab>
  </Tabs.List>

  <Tabs.Panel id="profile">
    <ProfileContent />
  </Tabs.Panel>
  <Tabs.Panel id="settings">
    <SettingsContent />
  </Tabs.Panel>
  <Tabs.Panel id="billing">
    <BillingContent />
  </Tabs.Panel>
</Tabs>
```

### Render Props

Pass rendering logic as a function.

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  renderEmpty?: () => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({
  items,
  renderItem,
  renderEmpty,
  keyExtractor,
}: ListProps<T>) {
  if (items.length === 0) {
    return renderEmpty?.() ?? null;
  }

  return (
    <ul className="list">
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  keyExtractor={user => user.id}
  renderItem={(user, index) => (
    <UserCard user={user} rank={index + 1} />
  )}
  renderEmpty={() => <EmptyState message="No users found" />}
/>
```

### Headless Components

Logic only, no UI.

```tsx
// Headless toggle hook
function useToggle(initialState = false) {
  const [isOn, setIsOn] = useState(initialState);

  const toggle = useCallback(() => setIsOn(prev => !prev), []);
  const turnOn = useCallback(() => setIsOn(true), []);
  const turnOff = useCallback(() => setIsOn(false), []);

  return { isOn, toggle, turnOn, turnOff };
}

// Usage - bring your own UI
function MyComponent() {
  const { isOn, toggle } = useToggle();

  return (
    <div>
      <button onClick={toggle}>
        {isOn ? 'ON' : 'OFF'}
      </button>
    </div>
  );
}

// Headless dropdown hook
function useDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLUListElement>(null);

  const open = () => {
    setIsOpen(true);
    setActiveIndex(0);
  };

  const close = () => {
    setIsOpen(false);
    setActiveIndex(-1);
    triggerRef.current?.focus();
  };

  const getMenuProps = () => ({
    ref: menuRef,
    role: 'menu' as const,
    'aria-hidden': !isOpen,
  });

  const getTriggerProps = () => ({
    ref: triggerRef,
    'aria-haspopup': 'menu' as const,
    'aria-expanded': isOpen,
    onClick: () => (isOpen ? close() : open()),
  });

  const getItemProps = (index: number) => ({
    role: 'menuitem' as const,
    tabIndex: index === activeIndex ? 0 : -1,
    'aria-selected': index === activeIndex,
  });

  return {
    isOpen,
    activeIndex,
    setActiveIndex,
    open,
    close,
    getMenuProps,
    getTriggerProps,
    getItemProps,
  };
}
```

## Event Handler Patterns

### Handler Naming

```tsx
interface FormProps {
  // External handlers (from parent)
  onSubmit: (data: FormData) => void;
  onChange?: (field: string, value: string) => void;

  // Don't expose internal handlers
  // BAD: onClick, handleClick
}

function Form({ onSubmit, onChange }: FormProps) {
  // Internal handlers prefixed with 'handle'
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.name, e.target.value);
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleFormSubmit}>
      <input name="email" onChange={handleInputChange} />
    </form>
  );
}
```

### Event Handler Types

```tsx
// Prefer specific event types
interface InputProps {
  // GOOD: Specific and typed
  onChange?: (value: string) => void;
  onFocus?: () => void;
  onBlur?: () => void;

  // ALSO GOOD: When event object needed
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

// Implementation
function Input({ onChange, onFocus, onBlur, onKeyDown }: InputProps) {
  return (
    <input
      onChange={(e) => onChange?.(e.target.value)}
      onFocus={onFocus}
      onBlur={onBlur}
      onKeyDown={onKeyDown}
    />
  );
}
```

## Style Customization

### className Prop

```tsx
interface CardProps {
  children: React.ReactNode;
  className?: string;  // Always support className
}

function Card({ children, className }: CardProps) {
  return (
    <div className={cn('card', className)}>
      {children}
    </div>
  );
}

// Usage
<Card className="my-custom-card">Content</Card>
```

### Style Variants

```tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
        ghost: 'hover:bg-gray-100',
        destructive: 'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  children: React.ReactNode;
}

function Button({ children, variant, size, className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    >
      {children}
    </button>
  );
}
```

### Style Props (Escape Hatch)

```tsx
interface BoxProps {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;  // Allow inline styles
}

function Box({ children, className, style }: BoxProps) {
  return (
    <div className={cn('box', className)} style={style}>
      {children}
    </div>
  );
}

// Usage for one-off customizations
<Box style={{ marginTop: 32 }}>Content</Box>
```

## Polymorphic Components

Components that can render as different elements.

```tsx
type PolymorphicRef<C extends React.ElementType> =
  React.ComponentPropsWithRef<C>['ref'];

type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

type PolymorphicComponentPropWithRef<
  C extends React.ElementType,
  Props = {}
> = PolymorphicComponentProp<C, Props> & { ref?: PolymorphicRef<C> };

// Simple polymorphic Text component
type TextProps<C extends React.ElementType> = PolymorphicComponentPropWithRef<
  C,
  { size?: 'sm' | 'md' | 'lg' }
>;

function Text<C extends React.ElementType = 'span'>({
  as,
  size = 'md',
  className,
  children,
  ...props
}: TextProps<C>) {
  const Component = as || 'span';

  return (
    <Component
      className={cn('text', `text-${size}`, className)}
      {...props}
    >
      {children}
    </Component>
  );
}

// Usage
<Text>Default span</Text>
<Text as="p" size="lg">Paragraph</Text>
<Text as="h1" size="lg">Heading</Text>
<Text as="a" href="/page">Link</Text>
```

## Forward Ref

Expose underlying DOM element.

```tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, ...props }, ref) => {
    const id = useId();

    return (
      <div className="input-wrapper">
        {label && <label htmlFor={id}>{label}</label>}
        <input
          ref={ref}
          id={id}
          className={cn('input', error && 'input-error', className)}
          aria-invalid={!!error}
          {...props}
        />
        {error && <span className="input-error-message">{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';

// Usage - parent can access DOM node
function Form() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <div>
      <Input ref={inputRef} label="Email" />
      <button onClick={focusInput}>Focus input</button>
    </div>
  );
}
```

## TypeScript Best Practices

### Generic Components

```tsx
interface SelectProps<T> {
  options: T[];
  value: T | null;
  onChange: (value: T) => void;
  getOptionLabel: (option: T) => string;
  getOptionValue: (option: T) => string;
}

function Select<T>({
  options,
  value,
  onChange,
  getOptionLabel,
  getOptionValue,
}: SelectProps<T>) {
  return (
    <select
      value={value ? getOptionValue(value) : ''}
      onChange={(e) => {
        const selected = options.find(
          opt => getOptionValue(opt) === e.target.value
        );
        if (selected) onChange(selected);
      }}
    >
      <option value="">Select...</option>
      {options.map(option => (
        <option key={getOptionValue(option)} value={getOptionValue(option)}>
          {getOptionLabel(option)}
        </option>
      ))}
    </select>
  );
}

// Usage with type inference
interface User {
  id: string;
  name: string;
}

<Select<User>
  options={users}
  value={selectedUser}
  onChange={setSelectedUser}
  getOptionLabel={user => user.name}
  getOptionValue={user => user.id}
/>
```

### Discriminated Unions

```tsx
// Different props based on variant
type AlertProps =
  | { variant: 'info'; message: string }
  | { variant: 'error'; message: string; onRetry?: () => void }
  | { variant: 'success'; message: string; onDismiss?: () => void };

function Alert(props: AlertProps) {
  switch (props.variant) {
    case 'info':
      return <div className="alert-info">{props.message}</div>;

    case 'error':
      return (
        <div className="alert-error">
          {props.message}
          {props.onRetry && <button onClick={props.onRetry}>Retry</button>}
        </div>
      );

    case 'success':
      return (
        <div className="alert-success">
          {props.message}
          {props.onDismiss && <button onClick={props.onDismiss}>×</button>}
        </div>
      );
  }
}
```

## API Design Checklist

### Before Implementation

- [ ] What is the simplest use case?
- [ ] What are the common customizations?
- [ ] What are the rare edge cases?
- [ ] How will this compose with other components?

### Props

- [ ] Required props are truly required
- [ ] Optional props have sensible defaults
- [ ] Names follow conventions (is*, on*, render*)
- [ ] Types are specific (not `any`)
- [ ] className supported for styling

### Events

- [ ] Handler names start with `on`
- [ ] Event types are specific
- [ ] Handlers receive useful arguments

### Composition

- [ ] Supports children prop
- [ ] Compound components if complex
- [ ] Render props for custom rendering
- [ ] Headless option if needed

### Accessibility

- [ ] Semantic HTML used
- [ ] ARIA attributes where needed
- [ ] Keyboard navigation works
- [ ] Focus management handled

### Documentation

- [ ] Props documented
- [ ] Usage examples provided
- [ ] Edge cases noted
- [ ] TypeScript types exported


## Quality Tests

### Visual Fidelity Test
- Implementation matches design within acceptable tolerance
- **PASS:** Spacing, colors, and typography match design tokens exactly
- **FAIL:** Visible deviations from design that aren't documented as intentional

### Accessibility Test
- Component is usable with keyboard-only and screen reader
- **PASS:** All interactive elements reachable by Tab, operable by Enter/Space
- **FAIL:** Mouse-only interactions or missing ARIA labels

