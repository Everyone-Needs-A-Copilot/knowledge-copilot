---
last_updated: 2026-02-25
status: active
name: interaction-patterns
description: Micro-interactions and motion - animations, transitions, feedback, loading states. Use for interaction design.
triggers:
  files: ["**/animations/**", "**/transitions/**", "**/motion.*"]
  keywords: ["animation", "transition", "micro-interaction", "hover", "loading", "skeleton", "feedback", "motion", "easing"]
allowed-tools: Read, Write, Edit
---

# Interaction Patterns Skill

Master guide for micro-interactions, animations, transitions, and motion design in modern web applications.

## Philosophy

**Motion should have purpose.** Every animation must either:
1. Guide attention to important changes
2. Maintain spatial context during transitions
3. Provide feedback to user actions
4. Communicate system state (loading, processing)
5. Delight without distraction

**Performance is non-negotiable.** Smooth 60fps animations require careful consideration of what properties are animated and how.

**Respect user preferences.** Always honor `prefers-reduced-motion` for accessibility.

---


## Define Done

- [ ] Design decisions are justified by user needs or established principles
- [ ] Visual hierarchy guides attention to the most important elements
- [ ] Design is accessible (WCAG AA minimum)
- [ ] Design is consistent with existing system patterns

## Core Animation Principles

Adapted from Disney's 12 Principles of Animation for UI/UX:

### 1. Timing and Spacing
Control the speed and rhythm of animations to convey weight and personality.

**Quick movements** (100-200ms): Micro-interactions, button feedback
**Medium movements** (200-400ms): Modal appearances, dropdown menus
**Slow movements** (400-600ms): Page transitions, major state changes

```typescript
// Timing scale for consistent UI
const timing = {
  instant: 100,
  quick: 200,
  base: 300,
  slow: 400,
  slower: 600,
  slowest: 800,
} as const;
```

### 2. Easing (Ease In/Out)
Linear motion feels mechanical. Use easing functions for natural movement.

**Ease-out (deceleration)**: Most common, feels responsive
**Ease-in (acceleration)**: Use sparingly, feels sluggish to start
**Ease-in-out**: Symmetric, good for looping animations
**Spring/elastic**: Natural physics, great for interactive elements

```css
/* Standard easing functions */
.ease-out { transition-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1); }
.ease-in { transition-timing-function: cubic-bezier(0.4, 0.0, 1, 1); }
.ease-in-out { transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1); }
.ease-bounce { transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55); }
```

```typescript
// Framer Motion spring presets
const springs = {
  gentle: { type: "spring", stiffness: 120, damping: 14 },
  responsive: { type: "spring", stiffness: 400, damping: 30 },
  bouncy: { type: "spring", stiffness: 300, damping: 10 },
  snappy: { type: "spring", stiffness: 500, damping: 25 },
};
```

### 3. Anticipation
Prepare users for what's about to happen.

```typescript
// Button press with anticipation
const buttonVariants = {
  rest: { scale: 1 },
  hover: { scale: 1.05 },
  press: { scale: 0.95 }, // Anticipates release
  tap: { scale: 1.1 }, // Satisfying release
};
```

### 4. Staging
Direct attention to what's important by controlling where motion occurs.

```typescript
// Stagger children to guide attention
<motion.ul
  variants={{
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1, // Each child appears 100ms apart
      },
    },
  }}
>
  {items.map(item => (
    <motion.li
      variants={{
        hidden: { opacity: 0, x: -20 },
        show: { opacity: 1, x: 0 },
      }}
    />
  ))}
</motion.ul>
```

### 5. Follow Through and Overlapping Action
Not everything stops at once. Create more natural motion with staggered timing.

```typescript
// Card flip with overlapping motion
const cardVariants = {
  front: {
    rotateY: 0,
    transition: { duration: 0.6 },
  },
  back: {
    rotateY: 180,
    transition: { duration: 0.6 },
  },
};

const contentVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { delay: 0.3 }, // Content follows card rotation
  },
};
```

### 6. Secondary Action
Add supporting animations that enhance without overwhelming.

```typescript
// Primary: Modal opens
// Secondary: Background blurs and darkens
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  className="fixed inset-0"
>
  <motion.div
    initial={{ backdropFilter: "blur(0px)" }}
    animate={{ backdropFilter: "blur(8px)" }}
    transition={{ duration: 0.3 }}
    className="absolute inset-0 bg-black/50"
  />
  <motion.div
    initial={{ scale: 0.9, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    transition={{ delay: 0.1 }}
    className="modal-content"
  />
</motion.div>
```

### 7. Exaggeration
Subtle exaggeration makes interactions feel more satisfying.

```typescript
// Favorite button with exaggerated scale
const favoriteVariants = {
  inactive: { scale: 1 },
  active: {
    scale: [1, 1.3, 1], // Bounces up then settles
    transition: { duration: 0.4 },
  },
};
```

---

## CSS Transitions vs Animations

### When to Use CSS Transitions

**Best for:**
- Simple state changes (hover, focus, active)
- Property changes triggered by user interaction
- Performance-critical animations (runs off main thread)

```css
/* Hover state transition */
.button {
  background-color: blue;
  transform: scale(1);
  transition: all 0.2s ease-out;
}

.button:hover {
  background-color: darkblue;
  transform: scale(1.05);
}

/* Multi-property with different timing */
.card {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition:
    transform 0.3s cubic-bezier(0.0, 0.0, 0.2, 1),
    box-shadow 0.3s ease-out;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}
```

### When to Use CSS Animations

**Best for:**
- Complex, multi-step animations
- Looping animations
- Animations that don't require JavaScript state

```css
/* Loading spinner */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}

/* Pulse effect */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading-dot {
  animation: pulse 1.5s ease-in-out infinite;
}

/* Complex multi-step */
@keyframes slideInBounce {
  0% {
    transform: translateX(-100%);
    opacity: 0;
  }
  60% {
    transform: translateX(10px);
    opacity: 1;
  }
  80% {
    transform: translateX(-5px);
  }
  100% {
    transform: translateX(0);
  }
}

.notification {
  animation: slideInBounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### Performance: What Properties to Animate

**GPU-Accelerated (60fps):**
- `transform` (translate, rotate, scale)
- `opacity`
- `filter` (with caution)

**Avoid Animating (causes reflow/repaint):**
- `width`, `height`
- `top`, `left`, `right`, `bottom`
- `margin`, `padding`
- `border-width`

```css
/* BAD: Animates width (causes reflow) */
.bad-expand {
  width: 100px;
  transition: width 0.3s;
}
.bad-expand:hover {
  width: 200px;
}

/* GOOD: Uses transform (GPU accelerated) */
.good-expand {
  transform: scaleX(1);
  transform-origin: left;
  transition: transform 0.3s;
}
.good-expand:hover {
  transform: scaleX(2);
}
```

### Using will-change

Hint to browser that element will animate for better performance.

```css
/* Use sparingly - only on elements that WILL animate */
.modal {
  will-change: transform, opacity;
}

/* Remove after animation completes */
.modal.animating {
  will-change: transform;
}

.modal.static {
  will-change: auto;
}
```

**Warning:** Overusing `will-change` can hurt performance. Only apply to elements actively animating.

---

## Loading States

### Skeleton Screens

Better than spinners for content that will fill specific shapes.

```typescript
// Skeleton component
export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "animate-pulse rounded-md bg-gray-200 dark:bg-gray-800",
        className
      )}
    />
  );
}

// Usage: Mimic actual content structure
function ArticleCardSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="h-48 w-full" /> {/* Image */}
      <Skeleton className="h-4 w-3/4" /> {/* Title */}
      <Skeleton className="h-4 w-1/2" /> {/* Subtitle */}
      <div className="flex gap-2">
        <Skeleton className="h-3 w-16" /> {/* Tag */}
        <Skeleton className="h-3 w-16" /> {/* Tag */}
      </div>
    </div>
  );
}
```

```css
/* Shimmer effect */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 0px,
    #f8f8f8 40px,
    #f0f0f0 80px
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite linear;
}
```

### Spinners

Use when loading time is indeterminate and content structure is unknown.

```typescript
// Simple spinner
export function Spinner({ size = "md" }: { size?: "sm" | "md" | "lg" }) {
  const sizeClasses = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-3",
    lg: "h-12 w-12 border-4",
  };

  return (
    <div
      className={cn(
        "animate-spin rounded-full border-gray-300 border-t-blue-600",
        sizeClasses[size]
      )}
    />
  );
}
```

```css
/* Smooth spinner */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

### Progress Indicators

For operations with known duration or progress.

```typescript
// Determinate progress bar
export function ProgressBar({ progress }: { progress: number }) {
  return (
    <div className="h-2 w-full bg-gray-200 rounded-full overflow-hidden">
      <motion.div
        className="h-full bg-blue-600"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.3, ease: "easeOut" }}
      />
    </div>
  );
}

// Indeterminate progress bar
export function IndeterminateProgress() {
  return (
    <div className="h-1 w-full bg-gray-200 overflow-hidden">
      <motion.div
        className="h-full w-1/3 bg-blue-600"
        animate={{
          x: ["-100%", "400%"],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    </div>
  );
}
```

### Optimistic Updates

Show immediate feedback while waiting for server confirmation.

```typescript
function useOptimisticUpdate() {
  const [items, setItems] = useState<Item[]>([]);
  const [optimisticItems, setOptimisticItems] = useState<Item[]>([]);

  const addItem = async (newItem: Item) => {
    // Immediately show in UI
    setOptimisticItems([...items, { ...newItem, _optimistic: true }]);

    try {
      const savedItem = await api.createItem(newItem);
      setItems([...items, savedItem]);
      setOptimisticItems([]);
    } catch (error) {
      // Revert on error
      setOptimisticItems([]);
      toast.error("Failed to add item");
    }
  };

  return {
    displayItems: [...items, ...optimisticItems],
    addItem,
  };
}

// Visual indicator for optimistic items
function ItemCard({ item }: { item: Item & { _optimistic?: boolean } }) {
  return (
    <motion.div
      initial={item._optimistic ? { opacity: 0.5 } : {}}
      animate={{ opacity: 1 }}
      className={cn(item._optimistic && "opacity-50")}
    >
      {item.name}
      {item._optimistic && (
        <Spinner size="sm" className="ml-2" />
      )}
    </motion.div>
  );
}
```

---

## Interactive States

### Hover States

```typescript
// Basic hover with Framer Motion
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click me
</motion.button>

// Hover with multiple effects
<motion.div
  className="card"
  whileHover={{
    y: -4,
    boxShadow: "0 12px 24px rgba(0,0,0,0.15)",
  }}
  transition={{ duration: 0.2 }}
>
  Card content
</motion.div>
```

```css
/* CSS hover patterns */
.link {
  position: relative;
  color: blue;
}

/* Underline slide-in */
.link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: currentColor;
  transition: width 0.3s ease-out;
}

.link:hover::after {
  width: 100%;
}

/* Glow effect */
.button {
  box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.5);
  transition: box-shadow 0.3s ease-out;
}

.button:hover {
  box-shadow: 0 0 0 8px rgba(59, 130, 246, 0);
}
```

### Focus States

Accessibility requirement - must be visible and distinct.

```css
/* Custom focus ring */
.button {
  outline: none; /* Remove default */
  box-shadow: 0 0 0 0 rgba(59, 130, 246, 0);
  transition: box-shadow 0.2s;
}

.button:focus-visible {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

/* Focus within (for containers) */
.search-container {
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.search-container:focus-within {
  border-color: blue;
}
```

### Active/Press States

Provides tactile feedback for clicks/taps.

```typescript
// Framer Motion tap feedback
<motion.button
  whileTap={{ scale: 0.95 }}
  transition={{ duration: 0.1 }}
>
  Press me
</motion.button>

// Multi-stage press
const buttonVariants = {
  rest: { scale: 1, y: 0 },
  hover: { scale: 1.05, y: -2 },
  press: { scale: 0.95, y: 0 },
};

<motion.button
  variants={buttonVariants}
  initial="rest"
  whileHover="hover"
  whileTap="press"
>
  Interactive button
</motion.button>
```

### Disabled States

Show clearly that interaction is not available.

```css
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none; /* Prevent hover effects */
}

/* Animated disabled state */
.button {
  transition: opacity 0.2s, filter 0.2s;
}

.button:disabled {
  opacity: 0.6;
  filter: grayscale(0.5);
}
```

---

## Feedback Patterns

### Toast Notifications

```typescript
// Toast with entrance/exit animations
export function Toast({ message, onClose }: ToastProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.3 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.2 } }}
      className="toast"
    >
      {message}
      <button onClick={onClose}>×</button>
    </motion.div>
  );
}

// Toast container with stacking
export function ToastContainer({ toasts }: { toasts: Toast[] }) {
  return (
    <div className="fixed bottom-4 right-4 space-y-2">
      <AnimatePresence mode="popLayout">
        {toasts.map(toast => (
          <Toast key={toast.id} {...toast} />
        ))}
      </AnimatePresence>
    </div>
  );
}
```

### Success/Error Animations

```typescript
// Checkmark animation
const checkmarkVariants = {
  hidden: {
    pathLength: 0,
    opacity: 0,
  },
  visible: {
    pathLength: 1,
    opacity: 1,
    transition: {
      pathLength: { type: "spring", duration: 0.6, bounce: 0 },
      opacity: { duration: 0.01 },
    },
  },
};

export function SuccessCheckmark() {
  return (
    <motion.svg
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 260, damping: 20 }}
      className="w-16 h-16"
    >
      <motion.circle
        cx="32"
        cy="32"
        r="30"
        stroke="green"
        strokeWidth="2"
        fill="none"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 0.5 }}
      />
      <motion.path
        d="M 20 32 L 28 40 L 44 24"
        stroke="green"
        strokeWidth="3"
        fill="none"
        variants={checkmarkVariants}
        initial="hidden"
        animate="visible"
      />
    </motion.svg>
  );
}

// Error shake
export function ErrorShake({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      animate={{
        x: [0, -10, 10, -10, 10, 0],
        transition: { duration: 0.4 },
      }}
    >
      {children}
    </motion.div>
  );
}
```

### Form Validation Feedback

```typescript
// Input with validation animation
export function ValidatedInput({ value, error }: ValidatedInputProps) {
  return (
    <div>
      <motion.input
        value={value}
        animate={error ? { x: [0, -10, 10, -10, 10, 0] } : {}}
        className={cn(
          "input",
          error && "border-red-500"
        )}
      />
      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="text-red-500 text-sm mt-1"
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}
```

### Button Loading States

```typescript
// Button with loading spinner
export function LoadingButton({
  loading,
  children,
  ...props
}: LoadingButtonProps) {
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      className="relative"
    >
      <motion.span
        animate={{ opacity: loading ? 0 : 1 }}
        transition={{ duration: 0.1 }}
      >
        {children}
      </motion.span>
      <AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <Spinner size="sm" />
          </motion.div>
        )}
      </AnimatePresence>
    </button>
  );
}
```

---

## Framer Motion Patterns

### Layout Animations

Animate layout changes automatically.

```typescript
// Layout animation when items reorder
<motion.div layout>
  {items.map(item => (
    <motion.div
      key={item.id}
      layout // Animates when position changes
      transition={{ type: "spring", stiffness: 350, damping: 25 }}
    >
      {item.name}
    </motion.div>
  ))}
</motion.div>

// Shared layout animations (magic motion)
function Gallery() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <>
      {items.map(item => (
        <motion.div
          layoutId={item.id}
          onClick={() => setSelected(item.id)}
        >
          <img src={item.thumbnail} />
        </motion.div>
      ))}

      <AnimatePresence>
        {selected && (
          <motion.div
            layoutId={selected}
            className="fullscreen-overlay"
          >
            <img src={items.find(i => i.id === selected)?.full} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
```

### Scroll-Triggered Animations

```typescript
import { useScroll, useTransform } from "framer-motion";

function ParallaxSection() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -100]);

  return (
    <motion.div style={{ y }}>
      Parallax content
    </motion.div>
  );
}

// Fade in on scroll
function FadeInOnScroll({ children }: { children: React.ReactNode }) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0]);

  return (
    <motion.div ref={ref} style={{ opacity }}>
      {children}
    </motion.div>
  );
}
```

### Gesture Animations

```typescript
// Drag
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 300 }}
  dragElastic={0.2}
  dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
>
  Drag me
</motion.div>

// Swipe to dismiss
function SwipeableCard({ onDismiss }: { onDismiss: () => void }) {
  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={(e, { offset, velocity }) => {
        if (Math.abs(offset.x) > 100 || Math.abs(velocity.x) > 500) {
          onDismiss();
        }
      }}
    >
      Swipe to dismiss
    </motion.div>
  );
}

// Pan gesture
<motion.div
  onPan={(e, info) => {
    console.log(info.offset, info.velocity);
  }}
>
  Pan handler
</motion.div>
```

### Exit Animations

```typescript
// AnimatePresence for mount/unmount
<AnimatePresence mode="wait">
  {show && (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ duration: 0.2 }}
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>

// Mode options:
// - "sync": All exit, then all enter
// - "wait": Exit completes before enter starts
// - "popLayout": Exiting elements stay in layout
```

### Variants System

Define reusable animation states.

```typescript
const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

<motion.ul
  variants={containerVariants}
  initial="hidden"
  animate="show"
>
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

---

## Accessibility: Reduced Motion

**CRITICAL**: Always respect user motion preferences.

```css
/* Disable animations for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```typescript
// React hook for reduced motion
function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  return prefersReducedMotion;
}

// Usage
function AnimatedComponent() {
  const prefersReducedMotion = usePrefersReducedMotion();

  return (
    <motion.div
      animate={
        prefersReducedMotion
          ? { opacity: 1 } // Simple fade only
          : { opacity: 1, y: 0, scale: 1 } // Full animation
      }
    />
  );
}
```

```typescript
// Framer Motion: Automatic reduced motion support
import { MotionConfig } from "framer-motion";

function App() {
  return (
    <MotionConfig reducedMotion="user"> {/* Respects system preference */}
      <YourApp />
    </MotionConfig>
  );
}
```

---

## Page Transitions

### Route Transitions (Next.js)

```typescript
// app/template.tsx (Next.js App Router)
"use client";

import { motion } from "framer-motion";

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

### Modal Transitions

```typescript
// Modal with backdrop
export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm"
          />

          {/* Modal content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="fixed inset-0 flex items-center justify-center p-4"
          >
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

### Drawer/Sidebar Transitions

```typescript
// Slide-out drawer
export function Drawer({ isOpen, onClose, children }: DrawerProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50"
          />

          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 30, stiffness: 300 }}
            className="fixed right-0 top-0 h-full w-80 bg-white shadow-xl"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

### Accordion Transitions

```typescript
// Smooth accordion with height animation
export function AccordionItem({
  title,
  children,
  isOpen,
  onToggle,
}: AccordionItemProps) {
  return (
    <div>
      <button
        onClick={onToggle}
        className="flex items-center justify-between w-full p-4"
      >
        {title}
        <motion.svg
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="w-5 h-5"
        >
          <path d="M19 9l-7 7-7-7" />
        </motion.svg>
      </button>

      <motion.div
        initial={false}
        animate={{
          height: isOpen ? "auto" : 0,
          opacity: isOpen ? 1 : 0,
        }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className="overflow-hidden"
      >
        <div className="p-4">{children}</div>
      </motion.div>
    </div>
  );
}
```

---

## Advanced Patterns

### Morphing Shapes

```typescript
// SVG path morphing
const pathVariants = {
  circle: {
    d: "M50,50 m-40,0 a40,40 0 1,0 80,0 a40,40 0 1,0 -80,0",
  },
  square: {
    d: "M10,10 L90,10 L90,90 L10,90 Z",
  },
};

<motion.svg viewBox="0 0 100 100">
  <motion.path
    variants={pathVariants}
    animate={isCircle ? "circle" : "square"}
    transition={{ duration: 0.5, ease: "easeInOut" }}
    fill="blue"
  />
</motion.svg>
```

### Sequence Animations

```typescript
// Multi-step animation sequence
const sequence = async () => {
  await controls.start({ scale: 1.2, transition: { duration: 0.2 } });
  await controls.start({ rotate: 180, transition: { duration: 0.3 } });
  await controls.start({ scale: 1, transition: { duration: 0.2 } });
};

// With variants
const sequenceVariants = {
  step1: { scale: 1.2 },
  step2: { rotate: 180 },
  step3: { scale: 1 },
};
```

### Inertia Animations

Physics-based animations with velocity.

```typescript
<motion.div
  drag
  dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
  dragElastic={0.5}
>
  Drag with physics
</motion.div>
```

### Stagger Grid

```typescript
function StaggerGrid({ items }: { items: any[] }) {
  return (
    <motion.div
      className="grid grid-cols-3 gap-4"
      variants={{
        hidden: { opacity: 0 },
        show: {
          opacity: 1,
          transition: {
            staggerChildren: 0.05,
          },
        },
      }}
      initial="hidden"
      animate="show"
    >
      {items.map((item, i) => (
        <motion.div
          key={i}
          variants={{
            hidden: { opacity: 0, scale: 0.8 },
            show: { opacity: 1, scale: 1 },
          }}
        >
          {item}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

---

## Performance Optimization

### 1. Use Transform and Opacity Only

```typescript
// BAD: Animates width (triggers layout)
<motion.div animate={{ width: 300 }} />

// GOOD: Uses transform (GPU accelerated)
<motion.div animate={{ scaleX: 1.5 }} />
```

### 2. Set layout="position" for Layout Animations

```typescript
// Only animate position, not size (more performant)
<motion.div layout="position">
  Content
</motion.div>
```

### 3. Use layoutId Sparingly

```typescript
// Shared layout animations are expensive
// Only use when the magic motion effect is essential
<motion.div layoutId="unique-id" />
```

### 4. Lazy Load Animations

```typescript
// Don't animate off-screen elements
function LazyAnimatedCard({ children }: { children: React.ReactNode }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
    >
      {children}
    </motion.div>
  );
}
```

### 5. Throttle/Debounce Expensive Animations

```typescript
import { useScroll } from "framer-motion";
import { throttle } from "lodash";

function ScrollAnimation() {
  const { scrollY } = useScroll();
  const [y, setY] = useState(0);

  useEffect(() => {
    const updateY = throttle((latest: number) => {
      setY(latest * 0.5);
    }, 16); // 60fps

    return scrollY.onChange(updateY);
  }, [scrollY]);

  return <motion.div style={{ y }} />;
}
```

---

## Anti-Patterns

### 1. Animating Everything

**BAD:**
```typescript
// Excessive animations that distract
<motion.div
  animate={{
    scale: [1, 1.1, 1],
    rotate: [0, 5, -5, 0],
    x: [0, 10, -10, 0],
  }}
  transition={{ repeat: Infinity }}
>
  This is annoying
</motion.div>
```

**GOOD:**
```typescript
// Subtle, purposeful hover animation
<motion.button
  whileHover={{ scale: 1.05 }}
  transition={{ duration: 0.2 }}
>
  Click me
</motion.button>
```

### 2. Slow Animations

**BAD:**
```typescript
// Too slow - user waits for animation
<motion.div
  animate={{ opacity: 1 }}
  transition={{ duration: 1.5 }}
/>
```

**GOOD:**
```typescript
// Quick and responsive
<motion.div
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
/>
```

### 3. Ignoring Reduced Motion

**BAD:**
```typescript
// Forces animation on all users
<motion.div
  animate={{ x: 100, rotate: 360 }}
  transition={{ duration: 0.5 }}
/>
```

**GOOD:**
```typescript
const prefersReducedMotion = usePrefersReducedMotion();

<motion.div
  animate={
    prefersReducedMotion
      ? { x: 100 } // Position change only
      : { x: 100, rotate: 360 } // Full animation
  }
/>
```

### 4. Animating Non-GPU Properties

**BAD:**
```typescript
// Animates width (causes reflow)
<motion.div animate={{ width: 300 }} />
```

**GOOD:**
```typescript
// Uses scale (GPU accelerated)
<motion.div
  style={{ transformOrigin: "left" }}
  animate={{ scaleX: 1.5 }}
/>
```

### 5. Complex Layout Animations Without layoutId

**BAD:**
```typescript
// Animates complex layout changes without layoutId
// Results in janky animations
{items.map(item => (
  <motion.div animate={{ /* complex positioning */ }} />
))}
```

**GOOD:**
```typescript
// Uses layout animations for smooth reordering
{items.map(item => (
  <motion.div layout key={item.id} />
))}
```

### 6. Over-Using will-change

**BAD:**
```css
/* Applied to every element */
* {
  will-change: transform, opacity;
}
```

**GOOD:**
```css
/* Only on elements actively animating */
.button:hover {
  will-change: transform;
}

.button {
  will-change: auto; /* Reset after animation */
}
```

### 7. Infinite Animations Without Purpose

**BAD:**
```typescript
// Constant motion with no purpose
<motion.div
  animate={{ rotate: 360 }}
  transition={{ repeat: Infinity, duration: 2 }}
>
  Look at me spin!
</motion.div>
```

**GOOD:**
```typescript
// Loading spinner with clear purpose
{isLoading && (
  <motion.div
    animate={{ rotate: 360 }}
    transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
  >
    <LoadingIcon />
  </motion.div>
)}
```

---

## Testing Animations

### Visual Regression Testing

```typescript
// Storybook stories for different animation states
export const HoverState = () => (
  <Button className="hover:scale-105">Hover me</Button>
);

export const LoadingState = () => (
  <LoadingButton loading={true}>Loading</LoadingButton>
);

export const AnimationSequence = () => {
  const [step, setStep] = useState(0);
  return (
    <AnimatedComponent step={step} />
  );
};
```

### Interaction Testing

```typescript
// Playwright test
test('button animates on hover', async ({ page }) => {
  await page.goto('/');
  const button = page.locator('button');

  // Capture before hover
  await button.screenshot({ path: 'before-hover.png' });

  // Hover and wait for animation
  await button.hover();
  await page.waitForTimeout(300); // Wait for animation

  // Capture after hover
  await button.screenshot({ path: 'after-hover.png' });
});
```

### Performance Testing

```typescript
// Measure animation performance
function measureAnimationFPS() {
  let lastTime = performance.now();
  let frames = 0;

  function countFrame() {
    frames++;
    const currentTime = performance.now();

    if (currentTime >= lastTime + 1000) {
      console.log(`FPS: ${frames}`);
      frames = 0;
      lastTime = currentTime;
    }

    requestAnimationFrame(countFrame);
  }

  requestAnimationFrame(countFrame);
}
```

---

## Quick Reference

### Timing Scale
- **100-200ms**: Micro-interactions, button feedback
- **200-400ms**: Modals, dropdowns, tooltips
- **400-600ms**: Page transitions, large state changes

### Easing Functions
- **ease-out**: Most common, feels responsive (use ~80% of time)
- **ease-in-out**: Symmetric motion, loops
- **spring**: Natural physics, interactive elements

### Properties to Animate
**GPU-accelerated:**
- `transform` (translate, scale, rotate)
- `opacity`

**Avoid:**
- `width`, `height`
- `top`, `left`
- `margin`, `padding`

### Accessibility Checklist
- [ ] Respect `prefers-reduced-motion`
- [ ] Focus states are visible
- [ ] Animations don't exceed 5 seconds
- [ ] No flashing/strobing (seizure risk)
- [ ] Important content not hidden by animation

---

## Summary

**Motion design is about communication, not decoration.**

Every animation should:
1. Have a clear purpose
2. Be performant (60fps)
3. Respect user preferences
4. Complete quickly
5. Feel natural

Start with no animations. Add motion only where it:
- Guides attention
- Provides feedback
- Maintains context
- Delights without distracting

When in doubt, make it faster or remove it entirely.


## Quality Tests

### Accessibility Test
- Design meets WCAG AA contrast ratios and interaction requirements
- **PASS:** All text passes 4.5:1 contrast ratio, interactive elements have visible focus states
- **FAIL:** Low-contrast text or missing keyboard navigation support

### Consistency Test
- Design uses established patterns and tokens from the design system
- **PASS:** Colors, spacing, and typography match existing components
- **FAIL:** New custom values introduced without justification

