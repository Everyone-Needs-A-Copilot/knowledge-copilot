---
last_updated: 2026-02-25
status: active
name: form-handling-implementation
description: Form validation, error handling, and accessibility patterns. Use when building accessible, user-friendly forms.
triggers:
  files: ["**/*.tsx", "**/*.jsx", "**/components/**", "**/forms/**"]
  keywords: ["form", "input", "validation", "error", "submit", "field", "required", "pattern", "accessible"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Form Handling Implementation

Build accessible, user-friendly forms with proper validation and error handling.

## Form Fundamentals

### Semantic Form Structure

```tsx
function ContactForm() {
  return (
    <form onSubmit={handleSubmit}>
      <fieldset>
        <legend>Contact Information</legend>

        <div className="field">
          <label htmlFor="name">
            Name
            <span aria-label="required">*</span>
          </label>
          <input
            id="name"
            name="name"
            type="text"
            required
            autoComplete="name"
          />
        </div>

        <div className="field">
          <label htmlFor="email">
            Email
            <span aria-label="required">*</span>
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            autoComplete="email"
          />
        </div>
      </fieldset>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Label Association

```tsx
// Method 1: htmlFor (recommended)
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Method 2: Wrapping (works without id)
<label>
  Email
  <input type="email" />
</label>

// Method 3: aria-labelledby (multiple labels)
<span id="email-label">Email</span>
<span id="email-hint">We'll never share your email</span>
<input
  type="email"
  aria-labelledby="email-label"
  aria-describedby="email-hint"
/>
```


## Define Done

- [ ] UI matches design specifications (spacing, colors, typography)
- [ ] Component is responsive across supported breakpoints
- [ ] Keyboard and screen reader accessible
- [ ] Edge cases handled (empty states, overflow, loading)

## Input Types

### Common Input Types

```tsx
// Text inputs
<input type="text" />          // General text
<input type="email" />         // Email with validation
<input type="password" />      // Hidden text
<input type="tel" />           // Phone (mobile keyboard)
<input type="url" />           // URL with validation
<input type="search" />        // Search (clear button)

// Numeric inputs
<input type="number" />        // Number with spinners
<input type="range" />         // Slider

// Date/time inputs
<input type="date" />          // Date picker
<input type="time" />          // Time picker
<input type="datetime-local" /> // Date and time

// Selection inputs
<input type="checkbox" />      // Multiple selection
<input type="radio" />         // Single selection
<select />                     // Dropdown

// File input
<input type="file" />          // File upload
```

### Input Attributes

```tsx
<input
  type="email"
  name="email"                    // Form data key
  id="email"                      // Label association
  required                        // Required field
  disabled                        // Disabled state
  readOnly                        // Read-only state
  placeholder="user@example.com"  // Hint text
  autoComplete="email"            // Browser autofill
  autoFocus                       // Focus on mount
  pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"  // Regex validation
  minLength={5}                   // Minimum length
  maxLength={100}                 // Maximum length
  min={0}                         // Minimum value (number)
  max={100}                       // Maximum value (number)
  step={1}                        // Step value (number)
/>
```

### AutoComplete Values

```tsx
// Personal info
autoComplete="name"              // Full name
autoComplete="given-name"        // First name
autoComplete="family-name"       // Last name
autoComplete="email"             // Email
autoComplete="tel"               // Phone
autoComplete="bday"              // Birthday

// Address
autoComplete="street-address"    // Full address
autoComplete="address-line1"     // Address line 1
autoComplete="city"              // City
autoComplete="state"             // State/Province
autoComplete="postal-code"       // ZIP/Postal code
autoComplete="country"           // Country

// Payment
autoComplete="cc-name"           // Cardholder name
autoComplete="cc-number"         // Card number
autoComplete="cc-exp"            // Expiration date
autoComplete="cc-csc"            // CVV/CVC
```

## Controlled Components

### Basic Controlled Input

```tsx
function ControlledForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
      />
      <input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### useForm Hook

```tsx
interface FormValues {
  [key: string]: string | number | boolean;
}

function useForm<T extends FormValues>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    const newValue = type === 'checkbox'
      ? (e.target as HTMLInputElement).checked
      : value;

    setValues(prev => ({ ...prev, [name]: newValue }));
  };

  const handleBlur = (
    e: React.FocusEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  };

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    setErrors,
    setValues,
    reset,
  };
}

// Usage
function MyForm() {
  const {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
  } = useForm({
    name: '',
    email: '',
  });

  return (
    <form>
      <input
        name="name"
        value={values.name}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      {touched.name && errors.name && <span>{errors.name}</span>}
    </form>
  );
}
```

## Validation

### Client-Side Validation Strategy

```tsx
// Validate on blur + submit (recommended)
function Form() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateField = (name: string, value: string): string | null => {
    switch (name) {
      case 'email':
        if (!value) return 'Email is required';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return 'Invalid email format';
        }
        return null;

      case 'password':
        if (!value) return 'Password is required';
        if (value.length < 8) return 'Password must be at least 8 characters';
        if (!/[A-Z]/.test(value)) return 'Must include uppercase letter';
        if (!/[0-9]/.test(value)) return 'Must include number';
        return null;

      default:
        return null;
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const error = validateField(name, value);
    setErrors(prev => ({
      ...prev,
      [name]: error || '',
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate all fields
    const formData = new FormData(e.target as HTMLFormElement);
    const newErrors: Record<string, string> = {};

    formData.forEach((value, name) => {
      const error = validateField(name, value as string);
      if (error) newErrors[name] = error;
    });

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      // Submit form
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="email"
        type="email"
        onBlur={handleBlur}
        aria-invalid={!!errors.email}
        aria-describedby={errors.email ? 'email-error' : undefined}
      />
      {errors.email && (
        <span id="email-error" role="alert">{errors.email}</span>
      )}
    </form>
  );
}
```

### Validation Schema

```tsx
interface ValidationRule {
  required?: boolean | string;
  minLength?: { value: number; message: string };
  maxLength?: { value: number; message: string };
  pattern?: { value: RegExp; message: string };
  custom?: (value: any) => string | null;
}

interface ValidationSchema {
  [field: string]: ValidationRule;
}

function validate<T extends Record<string, any>>(
  values: T,
  schema: ValidationSchema
): Partial<Record<keyof T, string>> {
  const errors: Partial<Record<keyof T, string>> = {};

  for (const [field, rules] of Object.entries(schema)) {
    const value = values[field];

    // Required
    if (rules.required) {
      if (!value || (typeof value === 'string' && !value.trim())) {
        errors[field as keyof T] = typeof rules.required === 'string'
          ? rules.required
          : `${field} is required`;
        continue;
      }
    }

    // MinLength
    if (rules.minLength && typeof value === 'string') {
      if (value.length < rules.minLength.value) {
        errors[field as keyof T] = rules.minLength.message;
        continue;
      }
    }

    // MaxLength
    if (rules.maxLength && typeof value === 'string') {
      if (value.length > rules.maxLength.value) {
        errors[field as keyof T] = rules.maxLength.message;
        continue;
      }
    }

    // Pattern
    if (rules.pattern && typeof value === 'string') {
      if (!rules.pattern.value.test(value)) {
        errors[field as keyof T] = rules.pattern.message;
        continue;
      }
    }

    // Custom
    if (rules.custom) {
      const customError = rules.custom(value);
      if (customError) {
        errors[field as keyof T] = customError;
      }
    }
  }

  return errors;
}

// Usage
const schema: ValidationSchema = {
  email: {
    required: 'Email is required',
    pattern: {
      value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: 'Invalid email format',
    },
  },
  password: {
    required: true,
    minLength: { value: 8, message: 'Must be at least 8 characters' },
    custom: (value) => {
      if (!/[A-Z]/.test(value)) return 'Must include uppercase';
      if (!/[0-9]/.test(value)) return 'Must include number';
      return null;
    },
  },
};

const errors = validate(formData, schema);
```

## Error Handling

### Accessible Error Display

```tsx
interface FieldProps {
  label: string;
  name: string;
  error?: string;
  touched?: boolean;
  type?: string;
  required?: boolean;
}

function Field({
  label,
  name,
  error,
  touched,
  type = 'text',
  required,
  ...props
}: FieldProps) {
  const id = useId();
  const errorId = `${id}-error`;
  const descriptionId = `${id}-description`;
  const showError = touched && error;

  return (
    <div className="field">
      <label htmlFor={id}>
        {label}
        {required && <span aria-label="required">*</span>}
      </label>

      <input
        id={id}
        name={name}
        type={type}
        aria-required={required}
        aria-invalid={showError ? 'true' : undefined}
        aria-describedby={showError ? errorId : undefined}
        {...props}
      />

      {showError && (
        <span id={errorId} role="alert" className="error">
          {error}
        </span>
      )}
    </div>
  );
}
```

### Error Summary

```tsx
interface ErrorSummaryProps {
  errors: Record<string, string>;
  onFieldClick: (field: string) => void;
}

function ErrorSummary({ errors, onFieldClick }: ErrorSummaryProps) {
  const errorEntries = Object.entries(errors).filter(([, error]) => error);

  if (errorEntries.length === 0) return null;

  return (
    <div
      role="alert"
      aria-labelledby="error-summary-title"
      className="error-summary"
    >
      <h2 id="error-summary-title">
        There {errorEntries.length === 1 ? 'is' : 'are'} {errorEntries.length}{' '}
        error{errorEntries.length === 1 ? '' : 's'} in this form
      </h2>

      <ul>
        {errorEntries.map(([field, error]) => (
          <li key={field}>
            <a
              href={`#${field}`}
              onClick={(e) => {
                e.preventDefault();
                onFieldClick(field);
              }}
            >
              {error}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Focus First Error

```tsx
function useFormWithErrorFocus<T extends Record<string, any>>(
  initialValues: T,
  validate: (values: T) => Partial<Record<keyof T, string>>
) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const fieldRefs = useRef<Map<string, HTMLInputElement>>(new Map());

  const registerRef = (name: string) => (el: HTMLInputElement | null) => {
    if (el) {
      fieldRefs.current.set(name, el);
    } else {
      fieldRefs.current.delete(name);
    }
  };

  const handleSubmit = (onSubmit: (values: T) => void) => (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors = validate(values);
    setErrors(newErrors);

    const errorFields = Object.keys(newErrors);
    if (errorFields.length > 0) {
      // Focus first error field
      const firstErrorField = errorFields[0];
      fieldRefs.current.get(firstErrorField)?.focus();
      return;
    }

    onSubmit(values);
  };

  return {
    values,
    errors,
    setValues,
    registerRef,
    handleSubmit,
  };
}
```

## Async Validation

### Debounced Field Validation

```tsx
function useDebouncedValidation(
  validateFn: (value: string) => Promise<string | null>,
  delay = 300
) {
  const [error, setError] = useState<string | null>(null);
  const [isValidating, setIsValidating] = useState(false);

  const validate = useMemo(
    () =>
      debounce(async (value: string) => {
        setIsValidating(true);
        try {
          const result = await validateFn(value);
          setError(result);
        } finally {
          setIsValidating(false);
        }
      }, delay),
    [validateFn, delay]
  );

  return { error, isValidating, validate };
}

// Usage: Check if email is available
function EmailField() {
  const { error, isValidating, validate } = useDebouncedValidation(
    async (email) => {
      const response = await fetch(`/api/check-email?email=${email}`);
      const { available } = await response.json();
      return available ? null : 'Email already taken';
    }
  );

  return (
    <div>
      <input
        type="email"
        onChange={(e) => validate(e.target.value)}
        aria-invalid={!!error}
        aria-describedby={error ? 'email-error' : undefined}
      />
      {isValidating && <span>Checking...</span>}
      {error && <span id="email-error" role="alert">{error}</span>}
    </div>
  );
}
```

### Submit with Loading State

```tsx
function FormWithSubmit() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const formData = new FormData(e.target as HTMLFormElement);
      await submitToServer(formData);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Submission failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {submitError && (
        <div role="alert" className="error">
          {submitError}
        </div>
      )}

      {/* Form fields */}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Complex Form Patterns

### Multi-Step Form

```tsx
interface Step {
  id: string;
  title: string;
  component: React.ComponentType<StepProps>;
  validate?: (data: any) => Record<string, string>;
}

interface StepProps {
  data: any;
  onChange: (data: any) => void;
  errors: Record<string, string>;
}

function MultiStepForm({ steps, onSubmit }: { steps: Step[]; onSubmit: (data: any) => void }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const step = steps[currentStep];
  const StepComponent = step.component;

  const handleNext = () => {
    if (step.validate) {
      const stepErrors = step.validate(formData);
      if (Object.keys(stepErrors).length > 0) {
        setErrors(stepErrors);
        return;
      }
    }

    setErrors({});
    if (currentStep < steps.length - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      onSubmit(formData);
    }
  };

  const handleBack = () => {
    setCurrentStep(prev => Math.max(0, prev - 1));
  };

  return (
    <div>
      {/* Progress indicator */}
      <nav aria-label="Form progress">
        <ol>
          {steps.map((s, index) => (
            <li
              key={s.id}
              aria-current={index === currentStep ? 'step' : undefined}
            >
              {s.title}
            </li>
          ))}
        </ol>
      </nav>

      {/* Step content */}
      <form onSubmit={(e) => { e.preventDefault(); handleNext(); }}>
        <StepComponent
          data={formData}
          onChange={(data) => setFormData(prev => ({ ...prev, ...data }))}
          errors={errors}
        />

        <div className="form-actions">
          {currentStep > 0 && (
            <button type="button" onClick={handleBack}>
              Back
            </button>
          )}
          <button type="submit">
            {currentStep === steps.length - 1 ? 'Submit' : 'Next'}
          </button>
        </div>
      </form>
    </div>
  );
}
```

### Dynamic Field Array

```tsx
interface FieldArrayProps {
  name: string;
  values: any[];
  onChange: (values: any[]) => void;
  renderField: (index: number, onRemove: () => void) => React.ReactNode;
  addLabel?: string;
}

function FieldArray({
  name,
  values,
  onChange,
  renderField,
  addLabel = 'Add item',
}: FieldArrayProps) {
  const add = () => {
    onChange([...values, {}]);
  };

  const remove = (index: number) => {
    onChange(values.filter((_, i) => i !== index));
  };

  return (
    <div role="group" aria-label={name}>
      {values.map((_, index) => (
        <div key={index}>
          {renderField(index, () => remove(index))}
        </div>
      ))}

      <button type="button" onClick={add}>
        {addLabel}
      </button>
    </div>
  );
}

// Usage
function PhoneNumbers() {
  const [phones, setPhones] = useState([{ number: '', type: 'mobile' }]);

  return (
    <FieldArray
      name="Phone numbers"
      values={phones}
      onChange={setPhones}
      addLabel="Add phone number"
      renderField={(index, onRemove) => (
        <div className="flex gap-2">
          <input
            value={phones[index].number}
            onChange={(e) => {
              const newPhones = [...phones];
              newPhones[index].number = e.target.value;
              setPhones(newPhones);
            }}
            placeholder="Phone number"
          />
          <select
            value={phones[index].type}
            onChange={(e) => {
              const newPhones = [...phones];
              newPhones[index].type = e.target.value;
              setPhones(newPhones);
            }}
          >
            <option value="mobile">Mobile</option>
            <option value="home">Home</option>
            <option value="work">Work</option>
          </select>
          <button type="button" onClick={onRemove}>Remove</button>
        </div>
      )}
    />
  );
}
```

### Dependent Fields

```tsx
function AddressForm() {
  const [country, setCountry] = useState('');
  const [state, setState] = useState('');
  const [states, setStates] = useState<string[]>([]);

  // Load states when country changes
  useEffect(() => {
    if (country) {
      fetchStates(country).then(setStates);
      setState(''); // Reset state when country changes
    } else {
      setStates([]);
    }
  }, [country]);

  return (
    <fieldset>
      <legend>Address</legend>

      <div className="field">
        <label htmlFor="country">Country</label>
        <select
          id="country"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        >
          <option value="">Select country</option>
          <option value="US">United States</option>
          <option value="CA">Canada</option>
        </select>
      </div>

      <div className="field">
        <label htmlFor="state">State/Province</label>
        <select
          id="state"
          value={state}
          onChange={(e) => setState(e.target.value)}
          disabled={!country}
          aria-describedby={!country ? 'state-hint' : undefined}
        >
          <option value="">Select state</option>
          {states.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        {!country && (
          <span id="state-hint" className="hint">
            Please select a country first
          </span>
        )}
      </div>
    </fieldset>
  );
}
```

## Accessibility Checklist

### Form-Level

- [ ] Form has visible submit button
- [ ] Required fields indicated visually and programmatically
- [ ] Error summary at top of form (for multiple errors)
- [ ] Focus moves to error summary or first error on submit

### Field-Level

- [ ] Every input has associated label
- [ ] Labels are visible (not just placeholder)
- [ ] Help text connected via `aria-describedby`
- [ ] Error messages connected via `aria-describedby`
- [ ] `aria-invalid` set when field has error
- [ ] Error messages announced via `role="alert"`

### Validation

- [ ] Errors shown on blur and submit
- [ ] Error messages are specific and helpful
- [ ] Don't validate while typing (except for password strength)
- [ ] Allow form submission even with client-side errors (server validates)

### States

- [ ] Disabled fields styled differently
- [ ] Loading state indicated
- [ ] Success state communicated

## Best Practices Summary

1. **Always use labels** - Never rely on placeholder alone
2. **Validate on blur + submit** - Not on every keystroke
3. **Show errors near fields** - Not just at top
4. **Use specific error messages** - "Invalid email" not "Error"
5. **Mark required fields clearly** - Visual + `aria-required`
6. **Focus first error** - Help users find problems
7. **Support keyboard** - Tab order, Enter to submit
8. **Use autocomplete** - Help browsers autofill
9. **Disable submit during loading** - Prevent double submission
10. **Test with screen readers** - Ensure errors are announced


## Quality Tests

### Visual Fidelity Test
- Implementation matches design within acceptable tolerance
- **PASS:** Spacing, colors, and typography match design tokens exactly
- **FAIL:** Visible deviations from design that aren't documented as intentional

### Accessibility Test
- Component is usable with keyboard-only and screen reader
- **PASS:** All interactive elements reachable by Tab, operable by Enter/Space
- **FAIL:** Mouse-only interactions or missing ARIA labels

