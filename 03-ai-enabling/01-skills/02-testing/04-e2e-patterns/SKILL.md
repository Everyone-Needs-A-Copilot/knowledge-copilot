---
last_updated: 2026-02-25
status: active
name: e2e-patterns
description: E2E testing - Playwright, test design, page objects, visual regression. Use for end-to-end tests.
triggers:
  files: ["**/e2e/**", "**/playwright.config.*", "**/cypress.config.*", "**/*.e2e.*"]
  keywords: ["playwright", "cypress", "e2e", "end-to-end", "browser automation", "page object", "visual regression", "integration test"]
allowed-tools: Read, Write, Edit
---

# E2E Testing Patterns

Comprehensive guide for end-to-end testing using Playwright and modern browser automation patterns.

## Core Principles

### 1. Test Design Philosophy

**User-Centric Testing**
- Test user journeys, not implementation details
- Follow the "Testing Trophy" - prioritize integration over unit tests for UI
- Write tests that mirror actual user behavior
- Focus on critical paths first

**Reliability Over Speed**
- Prefer slower, stable selectors over fast, brittle ones
- Build in proper wait conditions
- Implement retry logic for network-dependent operations
- Use deterministic test data

**Maintainability**
- One assertion concept per test (can have multiple assertions)
- DRY principle through page objects and fixtures
- Clear test naming that describes user actions
- Separate test data from test logic

### 2. The Test Pyramid for E2E

```
         /\
        /  \  E2E Tests (10%)
       /----\
      /      \  Integration Tests (30%)
     /--------\
    /          \  Unit Tests (60%)
   /------------\
```

E2E tests should:
- Cover critical user paths
- Test cross-system integration
- Validate end-user experience
- Run in production-like environments


## Define Done

- [ ] Test strategy covers the appropriate levels (unit/integration/e2e)
- [ ] Test cases are independent, repeatable, and deterministic
- [ ] Edge cases and error paths are covered
- [ ] Tests document expected behavior, not implementation details

## Playwright Setup

### Installation & Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Test directory
  testDir: './tests/e2e',

  // Timeout settings
  timeout: 30 * 1000,
  expect: {
    timeout: 5000
  },

  // Test execution
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  // Reporter configuration
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list']
  ],

  // Shared settings for all projects
  use: {
    // Base URL to make navigations relative
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    // Collect trace on failure
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on retry
    video: 'retain-on-failure',

    // Viewport size
    viewport: { width: 1280, height: 720 },

    // Action timeout
    actionTimeout: 10 * 1000,

    // Navigation timeout
    navigationTimeout: 30 * 1000,
  },

  // Configure projects for major browsers
  projects: [
    // Setup project
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Use authenticated state
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Mobile viewports
    {
      name: 'Mobile Chrome',
      use: {
        ...devices['Pixel 5'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'Mobile Safari',
      use: {
        ...devices['iPhone 12'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],

  // Web server configuration
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

### Package Setup

```json
// package.json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:chromium": "playwright test --project=chromium",
    "test:e2e:report": "playwright show-report"
  },
  "devDependencies": {
    "@playwright/test": "^1.40.0",
    "@axe-core/playwright": "^4.8.0"
  }
}
```

## Test Structure

### Basic Test Anatomy

```typescript
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should login with valid credentials', async ({ page }) => {
    // Arrange - Set up test data
    const email = 'user@example.com';
    const password = 'SecurePassword123!';

    // Act - Perform user actions
    await page.getByLabel('Email').fill(email);
    await page.getByLabel('Password').fill(password);
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Assert - Verify expected outcomes
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
    await expect(page.getByText(`Welcome, ${email}`)).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('invalid@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page.getByText('Invalid email or password')).toBeVisible();
    await expect(page).toHaveURL('/login');
  });

  test('should validate required fields', async ({ page }) => {
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();
  });
});
```

### Test Organization

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   ├── logout.spec.ts
│   │   ├── signup.spec.ts
│   │   └── password-reset.spec.ts
│   ├── dashboard/
│   │   ├── overview.spec.ts
│   │   └── widgets.spec.ts
│   ├── projects/
│   │   ├── create-project.spec.ts
│   │   ├── edit-project.spec.ts
│   │   └── delete-project.spec.ts
│   └── fixtures/
│       ├── test-data.ts
│       ├── custom-fixtures.ts
│       └── api-helpers.ts
```

## Selector Strategies

### Priority Order

1. **Accessible Role Selectors** (Preferred)
2. **Test IDs** (Reliable)
3. **Text Content** (User-visible)
4. **CSS/XPath** (Last resort)

### 1. Role-Based Selectors

```typescript
// BEST: Uses ARIA roles and accessible names
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('link', { name: 'Contact Us' }).click();
await page.getByRole('checkbox', { name: 'Accept Terms' }).check();
await page.getByRole('radio', { name: 'Option A' }).check();
await page.getByRole('combobox', { name: 'Country' }).selectOption('US');

// With additional filters
await page.getByRole('button', {
  name: 'Delete',
  disabled: false
}).click();

await page.getByRole('listitem').filter({
  hasText: 'Active Projects'
}).click();
```

### 2. Test ID Selectors

```typescript
// Component implementation
<button data-testid="submit-form-btn">Submit</button>
<input data-testid="email-input" type="email" />
<div data-testid="error-message">Error text</div>

// Test usage
await page.getByTestId('submit-form-btn').click();
await page.getByTestId('email-input').fill('user@example.com');
await expect(page.getByTestId('error-message')).toBeVisible();

// Custom test ID attribute
// playwright.config.ts
use: {
  testIdAttribute: 'data-qa'
}

// Component
<button data-qa="submit-btn">Submit</button>

// Test
await page.getByTestId('submit-btn').click();
```

### 3. Text-Based Selectors

```typescript
// By label
await page.getByLabel('Email address').fill('user@example.com');
await page.getByLabel(/email/i).fill('user@example.com'); // Case insensitive

// By placeholder
await page.getByPlaceholder('Enter your email').fill('user@example.com');

// By text content
await page.getByText('Welcome back').click();
await page.getByText(/welcome/i).click(); // Case insensitive
await page.getByText('Welcome', { exact: true }).click(); // Exact match

// By title
await page.getByTitle('Close dialog').click();

// By alt text (images)
await page.getByAltText('User avatar').click();
```

### 4. CSS/XPath Selectors (Use Sparingly)

```typescript
// CSS - only when necessary
await page.locator('button.primary').click();
await page.locator('[aria-label="Close"]').click();
await page.locator('#user-menu').click();

// Combining locators
await page.locator('form').getByRole('button', { name: 'Submit' }).click();

// nth element
await page.locator('button').nth(0).click();
await page.locator('button').first().click();
await page.locator('button').last().click();

// XPath - absolute last resort
await page.locator('xpath=//button[contains(text(), "Submit")]').click();
```

### Selector Best Practices

```typescript
// GOOD: Stable, user-centric selectors
await page.getByRole('button', { name: 'Add to Cart' }).click();
await page.getByLabel('Search products').fill('laptop');
await page.getByTestId('checkout-btn').click();

// BAD: Brittle, implementation-dependent selectors
await page.locator('div > div > button:nth-child(3)').click();
await page.locator('.css-1a2b3c4d').fill('laptop');
await page.locator('#root > div > div > button').click();

// GOOD: Resilient to style changes
await page.getByRole('navigation').getByRole('link', { name: 'Products' });

// BAD: Breaks when styles change
await page.locator('nav.header-nav > ul > li:first-child > a');
```

## Page Object Model

### Base Page Pattern

```typescript
// pages/base.page.ts
import { Page, Locator } from '@playwright/test';

export class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto(path: string) {
    await this.page.goto(path);
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }
}
```

### Feature Page Object

```typescript
// pages/login.page.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign In' });
    this.errorMessage = page.getByTestId('error-message');
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot Password?' });
  }

  async goto() {
    await super.goto('/login');
    await this.waitForPageLoad();
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async loginWithValidation(email: string, password: string) {
    await this.emailInput.fill(email);
    await expect(this.emailInput).toHaveValue(email);

    await this.passwordInput.fill(password);
    await expect(this.passwordInput).toHaveValue(password);

    await this.submitButton.click();
    await this.page.waitForURL('**/dashboard');
  }

  async assertErrorMessage(message: string) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toHaveText(message);
  }

  async clickForgotPassword() {
    await this.forgotPasswordLink.click();
    await this.page.waitForURL('**/reset-password');
  }
}
```

### Component Page Object

```typescript
// pages/components/navbar.component.ts
import { Page, Locator } from '@playwright/test';

export class NavbarComponent {
  readonly page: Page;
  readonly userMenu: Locator;
  readonly notificationBell: Locator;
  readonly searchInput: Locator;

  constructor(page: Page) {
    this.page = page;
    const nav = page.getByRole('navigation', { name: 'Main navigation' });
    this.userMenu = nav.getByRole('button', { name: 'User menu' });
    this.notificationBell = nav.getByRole('button', { name: 'Notifications' });
    this.searchInput = nav.getByPlaceholder('Search...');
  }

  async navigateTo(linkName: string) {
    await this.page.getByRole('navigation')
      .getByRole('link', { name: linkName })
      .click();
  }

  async openUserMenu() {
    await this.userMenu.click();
  }

  async logout() {
    await this.openUserMenu();
    await this.page.getByRole('menuitem', { name: 'Logout' }).click();
  }

  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchInput.press('Enter');
  }

  async getNotificationCount(): Promise<number> {
    const badge = this.notificationBell.locator('.badge');
    const count = await badge.textContent();
    return count ? parseInt(count, 10) : 0;
  }
}
```

### Using Page Objects

```typescript
// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';

test.describe('User Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    await loginPage.login('user@example.com', 'password123');

    const dashboard = new DashboardPage(page);
    await dashboard.assertLoaded();
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test('shows error for invalid credentials', async () => {
    await loginPage.login('invalid@example.com', 'wrongpass');
    await loginPage.assertErrorMessage('Invalid email or password');
  });
});
```

## Fixtures & Test Data

### Custom Fixtures

```typescript
// fixtures/custom-fixtures.ts
import { test as base, Page } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';

type CustomFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

export const test = base.extend<CustomFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // Auto-login for tests that need authentication
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(
      process.env.TEST_USER_EMAIL || 'test@example.com',
      process.env.TEST_USER_PASSWORD || 'password123'
    );
    await page.waitForURL('**/dashboard');
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

### Test Data Management

```typescript
// fixtures/test-data.ts
export const testUsers = {
  admin: {
    email: 'admin@example.com',
    password: 'AdminPass123!',
    role: 'admin',
  },
  regularUser: {
    email: 'user@example.com',
    password: 'UserPass123!',
    role: 'user',
  },
  premiumUser: {
    email: 'premium@example.com',
    password: 'PremiumPass123!',
    role: 'premium',
  },
};

export const testProjects = {
  active: {
    name: 'Active Project',
    description: 'This is an active project',
    status: 'active',
  },
  archived: {
    name: 'Archived Project',
    description: 'This project is archived',
    status: 'archived',
  },
};

export const generateTestEmail = () => {
  return `test-${Date.now()}@example.com`;
};

export const generateTestData = {
  user: () => ({
    email: generateTestEmail(),
    password: 'TestPass123!',
    firstName: 'Test',
    lastName: 'User',
  }),

  project: (overrides = {}) => ({
    name: `Test Project ${Date.now()}`,
    description: 'Auto-generated test project',
    ...overrides,
  }),
};
```

### Using Fixtures

```typescript
// tests/e2e/dashboard/overview.spec.ts
import { test, expect } from '../fixtures/custom-fixtures';
import { testUsers } from '../fixtures/test-data';

test.describe('Dashboard Overview', () => {
  test('displays user projects', async ({ authenticatedPage, dashboardPage }) => {
    await dashboardPage.goto();
    await dashboardPage.assertProjectsLoaded();

    const projectCount = await dashboardPage.getProjectCount();
    expect(projectCount).toBeGreaterThan(0);
  });

  test('admin sees all projects', async ({ page, loginPage, dashboardPage }) => {
    await loginPage.goto();
    await loginPage.login(testUsers.admin.email, testUsers.admin.password);

    await dashboardPage.goto();
    await expect(dashboardPage.adminPanel).toBeVisible();
  });
});
```

## Authentication Handling

### Setup Project Pattern

```typescript
// tests/auth.setup.ts
import { test as setup } from '@playwright/test';
import { LoginPage } from './pages/login.page';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();

  await loginPage.login(
    process.env.TEST_USER_EMAIL || 'test@example.com',
    process.env.TEST_USER_PASSWORD || 'password123'
  );

  // Wait for successful login
  await page.waitForURL('**/dashboard');

  // Save signed-in state
  await page.context().storageState({ path: authFile });
});
```

### Multiple Auth States

```typescript
// tests/auth-setup.ts
import { test as setup } from '@playwright/test';

const adminFile = 'playwright/.auth/admin.json';
const userFile = 'playwright/.auth/user.json';

setup('authenticate as admin', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('admin@example.com');
  await page.getByLabel('Password').fill('admin123');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await page.waitForURL('**/dashboard');
  await page.context().storageState({ path: adminFile });
});

setup('authenticate as user', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('user123');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await page.waitForURL('**/dashboard');
  await page.context().storageState({ path: userFile });
});
```

```typescript
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'admin-tests',
    use: { storageState: 'playwright/.auth/admin.json' },
    dependencies: ['setup'],
    testMatch: '**/admin/**/*.spec.ts',
  },
  {
    name: 'user-tests',
    use: { storageState: 'playwright/.auth/user.json' },
    dependencies: ['setup'],
    testMatch: '**/user/**/*.spec.ts',
  },
],
```

## API Mocking

### Route Interception

```typescript
// tests/e2e/mocking/api-mocks.spec.ts
import { test, expect } from '@playwright/test';

test.describe('API Mocking', () => {
  test('mocks user data endpoint', async ({ page }) => {
    // Mock the API response
    await page.route('**/api/user', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 1,
          email: 'mock@example.com',
          name: 'Mock User',
        }),
      });
    });

    await page.goto('/profile');
    await expect(page.getByText('Mock User')).toBeVisible();
  });

  test('simulates API error', async ({ page }) => {
    await page.route('**/api/projects', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          error: 'Internal server error',
        }),
      });
    });

    await page.goto('/projects');
    await expect(page.getByText('Failed to load projects')).toBeVisible();
  });

  test('modifies API response', async ({ page }) => {
    await page.route('**/api/projects', async (route) => {
      const response = await route.fetch();
      const json = await response.json();

      // Add a test project to the response
      json.projects.push({
        id: 999,
        name: 'Test Project',
        status: 'active',
      });

      await route.fulfill({ response, json });
    });

    await page.goto('/projects');
    await expect(page.getByText('Test Project')).toBeVisible();
  });
});
```

### Network Conditions

```typescript
test('handles slow network', async ({ page, context }) => {
  // Simulate slow network
  await page.route('**/*', (route) => {
    setTimeout(() => route.continue(), 2000);
  });

  await page.goto('/dashboard');
  await expect(page.getByTestId('loading-spinner')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible({
    timeout: 10000,
  });
});

test('handles offline mode', async ({ page, context }) => {
  await context.setOffline(true);

  await page.goto('/dashboard');
  await expect(page.getByText('No internet connection')).toBeVisible();

  await context.setOffline(false);
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});
```

## Waiting Strategies

### Explicit Waits

```typescript
// Wait for navigation
await page.goto('/dashboard');
await page.waitForURL('**/dashboard');
await page.waitForURL(/dashboard/, { timeout: 5000 });

// Wait for load state
await page.waitForLoadState('load'); // Basic HTML loaded
await page.waitForLoadState('domcontentloaded'); // DOM ready
await page.waitForLoadState('networkidle'); // No network activity

// Wait for selector
await page.waitForSelector('[data-testid="content"]');
await page.waitForSelector('button:has-text("Submit")');

// Wait for function
await page.waitForFunction(() => {
  return document.querySelectorAll('.item').length > 5;
});

// Wait for request/response
const responsePromise = page.waitForResponse('**/api/data');
await page.getByRole('button', { name: 'Load Data' }).click();
const response = await responsePromise;
expect(response.status()).toBe(200);

// Wait for event
const [popup] = await Promise.all([
  page.waitForEvent('popup'),
  page.getByRole('button', { name: 'Open Window' }).click(),
]);
await popup.waitForLoadState();
```

### Auto-Waiting

```typescript
// Playwright auto-waits for elements to be:
// - Attached to DOM
// - Visible
// - Stable (not animating)
// - Enabled
// - Receives events (not obscured)

// These actions auto-wait:
await page.getByRole('button').click();
await page.getByLabel('Email').fill('test@example.com');
await page.getByText('Submit').hover();
await page.getByRole('checkbox').check();

// Custom timeout for specific action
await page.getByRole('button', { name: 'Slow Operation' }).click({
  timeout: 30000,
});
```

### Polling

```typescript
// Poll until condition is met
await expect(async () => {
  const status = await page.getByTestId('status').textContent();
  expect(status).toBe('Complete');
}).toPass({
  timeout: 10000,
  intervals: [1000, 2000, 5000],
});

// Poll with custom logic
async function waitForTaskComplete(page: Page, taskId: string) {
  await page.waitForFunction(
    (id) => {
      const element = document.querySelector(`[data-task-id="${id}"]`);
      return element?.getAttribute('data-status') === 'complete';
    },
    taskId,
    { timeout: 30000, polling: 1000 }
  );
}
```

## Visual Regression Testing

### Screenshot Comparison

```typescript
// tests/e2e/visual/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage looks correct', async ({ page }) => {
    await page.goto('/');

    // Full page screenshot
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });

  test('login form looks correct', async ({ page }) => {
    await page.goto('/login');

    // Element screenshot
    const loginForm = page.getByTestId('login-form');
    await expect(loginForm).toHaveScreenshot('login-form.png');
  });

  test('responsive design - mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });

  test('button states', async ({ page }) => {
    await page.goto('/components/buttons');

    const button = page.getByRole('button', { name: 'Submit' });

    // Default state
    await expect(button).toHaveScreenshot('button-default.png');

    // Hover state
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');

    // Focus state
    await button.focus();
    await expect(button).toHaveScreenshot('button-focus.png');

    // Disabled state
    await page.evaluate(() => {
      const btn = document.querySelector('button');
      btn?.setAttribute('disabled', 'true');
    });
    await expect(button).toHaveScreenshot('button-disabled.png');
  });
});
```

### Screenshot Options

```typescript
// Mask dynamic content
await expect(page).toHaveScreenshot('dashboard.png', {
  mask: [
    page.getByTestId('timestamp'),
    page.getByTestId('user-avatar'),
    page.locator('.dynamic-chart'),
  ],
});

// Threshold for acceptable differences
await expect(page).toHaveScreenshot('page.png', {
  maxDiffPixels: 100,
  threshold: 0.2,
});

// Clip to specific area
await expect(page).toHaveScreenshot('header.png', {
  clip: { x: 0, y: 0, width: 1280, height: 100 },
});

// Disable animations
await expect(page).toHaveScreenshot('animated.png', {
  animations: 'disabled',
});

// Wait for fonts to load
await page.evaluate(() => document.fonts.ready);
await expect(page).toHaveScreenshot('text.png');
```

### Updating Baselines

```bash
# Update all screenshots
npm run test:e2e -- --update-snapshots

# Update specific test
npm run test:e2e -- visual/homepage.spec.ts --update-snapshots

# Update specific project
npm run test:e2e -- --project=chromium --update-snapshots
```

## Accessibility Testing

### Axe Integration

```typescript
// tests/e2e/accessibility/a11y.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage has no accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('form has proper labels', async ({ page }) => {
    await page.goto('/contact');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .include('#contact-form')
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('navigation is keyboard accessible', async ({ page }) => {
    await page.goto('/');

    // Tab through navigation
    await page.keyboard.press('Tab');
    await expect(page.getByRole('link', { name: 'Home' })).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByRole('link', { name: 'About' })).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByRole('link', { name: 'Contact' })).toBeFocused();
  });

  test('modal traps focus', async ({ page }) => {
    await page.goto('/dashboard');
    await page.getByRole('button', { name: 'Open Dialog' }).click();

    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeFocused();

    // Tab should cycle within modal
    await page.keyboard.press('Tab');
    const firstButton = dialog.getByRole('button').first();
    await expect(firstButton).toBeFocused();

    // Escape closes modal
    await page.keyboard.press('Escape');
    await expect(dialog).not.toBeVisible();
  });
});
```

## Parallel Execution

### Test Isolation

```typescript
// Each test gets isolated context
test.describe.configure({ mode: 'parallel' });

test.describe('User Operations', () => {
  test('create user', async ({ page }) => {
    // Runs in parallel
  });

  test('edit user', async ({ page }) => {
    // Runs in parallel
  });

  test('delete user', async ({ page }) => {
    // Runs in parallel
  });
});

// Serial execution when needed
test.describe.configure({ mode: 'serial' });

test.describe('Workflow Steps', () => {
  test('step 1: setup', async ({ page }) => {
    // Must complete before step 2
  });

  test('step 2: process', async ({ page }) => {
    // Depends on step 1
  });

  test('step 3: verify', async ({ page }) => {
    // Depends on step 2
  });
});
```

### Worker Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 1 : 4,

  // Limit parallel tests per worker
  fullyParallel: true,

  // Retry failed tests
  retries: process.env.CI ? 2 : 0,

  // Timeout
  timeout: 30 * 1000,
});
```

### Shared State Between Tests

```typescript
// fixtures/worker-fixtures.ts
import { test as base } from '@playwright/test';

type WorkerFixtures = {
  sharedData: { token: string };
};

export const test = base.extend<{}, WorkerFixtures>({
  // Worker-scoped fixture runs once per worker
  sharedData: [
    async ({}, use, workerInfo) => {
      // Setup once per worker
      const token = await generateAuthToken();
      await use({ token });
      // Cleanup once per worker
    },
    { scope: 'worker' },
  ],
});
```

## Debugging

### Interactive Debugging

```bash
# Debug mode - opens inspector
npm run test:e2e -- --debug

# Debug specific test
npm run test:e2e -- login.spec.ts --debug

# Headed mode - see browser
npm run test:e2e -- --headed

# Slow motion
npm run test:e2e -- --headed --slow-mo=1000
```

### Programmatic Debugging

```typescript
test('debug example', async ({ page }) => {
  await page.goto('/dashboard');

  // Pause execution - opens inspector
  await page.pause();

  // Console logs appear in terminal
  console.log(await page.title());

  // Take screenshot
  await page.screenshot({ path: 'debug.png' });

  // Print HTML
  console.log(await page.content());

  // Evaluate in browser context
  const result = await page.evaluate(() => {
    console.log('Browser console');
    return window.location.href;
  });
  console.log(result);
});
```

### Trace Viewer

```typescript
// playwright.config.ts
use: {
  trace: 'on-first-retry', // or 'on', 'off', 'retain-on-failure'
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

```bash
# View trace after test
npx playwright show-trace trace.zip

# Open last trace
npx playwright show-trace test-results/*/trace.zip
```

### Common Debugging Patterns

```typescript
// Check element existence
await page.locator('button').count(); // Returns number of matches
await page.locator('button').isVisible(); // Returns boolean

// Get element info
const button = page.getByRole('button', { name: 'Submit' });
console.log(await button.textContent());
console.log(await button.getAttribute('class'));
console.log(await button.boundingBox());

// Wait and log
await page.waitForLoadState('networkidle');
console.log('Page loaded');

// Network logging
page.on('request', (request) => {
  console.log('>>', request.method(), request.url());
});

page.on('response', (response) => {
  console.log('<<', response.status(), response.url());
});

// Console logging from browser
page.on('console', (msg) => {
  console.log('BROWSER:', msg.text());
});
```

## CI Integration

### GitHub Actions

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          BASE_URL: http://localhost:3000
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: test-results/
          retention-days: 30
```

### Sharding for Parallel CI

```yaml
# .github/workflows/e2e-tests.yml
jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run tests
        run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ matrix.shardIndex }}
          path: playwright-report
```

## Anti-Patterns

### 1. Testing Implementation Details

```typescript
// BAD: Tests internal structure
test('counter increments', async ({ page }) => {
  await page.goto('/counter');
  await page.locator('.counter-component > div > button.increment').click();
  await expect(page.locator('.counter-value')).toHaveText('1');
});

// GOOD: Tests user behavior
test('counter increments', async ({ page }) => {
  await page.goto('/counter');
  await page.getByRole('button', { name: 'Increment' }).click();
  await expect(page.getByText('Count: 1')).toBeVisible();
});
```

### 2. Brittle Selectors

```typescript
// BAD: Breaks when structure changes
await page.locator('div > div > div > button:nth-child(2)').click();
await page.locator('.css-1a2b3c4d > span').click();

// GOOD: Resilient selectors
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByTestId('submit-button').click();
```

### 3. No Wait Conditions

```typescript
// BAD: Race condition
await page.getByRole('button', { name: 'Load' }).click();
const text = await page.getByTestId('result').textContent();

// GOOD: Wait for element
await page.getByRole('button', { name: 'Load' }).click();
await page.waitForSelector('[data-testid="result"]');
const text = await page.getByTestId('result').textContent();

// BETTER: Use assertion
await page.getByRole('button', { name: 'Load' }).click();
await expect(page.getByTestId('result')).toContainText('Success');
```

### 4. Not Testing User Journeys

```typescript
// BAD: Isolated actions
test('click button', async ({ page }) => {
  await page.getByRole('button').click();
});

test('fill form', async ({ page }) => {
  await page.getByLabel('Name').fill('John');
});

// GOOD: Complete user journey
test('user completes registration', async ({ page }) => {
  await page.goto('/signup');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('SecurePass123!');
  await page.getByLabel('Confirm Password').fill('SecurePass123!');
  await page.getByRole('button', { name: 'Sign Up' }).click();

  await expect(page).toHaveURL('/welcome');
  await expect(page.getByText('Welcome to our platform!')).toBeVisible();
});
```

### 5. Sharing State Between Tests

```typescript
// BAD: Tests depend on each other
let userId: string;

test('create user', async ({ page }) => {
  // Creates user
  userId = 'user-123';
});

test('edit user', async ({ page }) => {
  // Uses userId from previous test - FRAGILE
  await page.goto(`/users/${userId}/edit`);
});

// GOOD: Independent tests
test('create user', async ({ page }) => {
  const userId = await createTestUser();
  await page.goto(`/users/${userId}`);
  await expect(page.getByRole('heading')).toContainText('User Details');
});

test('edit user', async ({ page }) => {
  const userId = await createTestUser(); // Each test creates own data
  await page.goto(`/users/${userId}/edit`);
  await expect(page.getByRole('heading')).toContainText('Edit User');
});
```

### 6. Hard-Coded Waits

```typescript
// BAD: Arbitrary timeout
await page.getByRole('button', { name: 'Submit' }).click();
await page.waitForTimeout(3000); // Magic number

// GOOD: Wait for specific condition
await page.getByRole('button', { name: 'Submit' }).click();
await page.waitForResponse('**/api/submit');
await expect(page.getByText('Success')).toBeVisible();
```

### 7. Overly Complex Page Objects

```typescript
// BAD: God object with too many responsibilities
class ApplicationPage {
  // 50+ methods for every possible action
  async loginAsAdmin() {}
  async loginAsUser() {}
  async createProject() {}
  async editProject() {}
  async deleteProject() {}
  async sendEmail() {}
  async processPayment() {}
  // ...
}

// GOOD: Focused page objects
class LoginPage {
  async login(email: string, password: string) {}
}

class ProjectsPage {
  async createProject(data: ProjectData) {}
  async editProject(id: string, data: ProjectData) {}
  async deleteProject(id: string) {}
}

class PaymentPage {
  async processPayment(amount: number) {}
}
```

## Best Practices Summary

1. **Write User-Centric Tests**: Test what users do, not implementation
2. **Use Stable Selectors**: Prefer roles and labels over CSS classes
3. **Keep Tests Independent**: No shared state between tests
4. **Use Page Objects**: Encapsulate page logic, keep tests clean
5. **Handle Waits Properly**: Use explicit waits, avoid hard-coded timeouts
6. **Mock External Dependencies**: Control external APIs and services
7. **Test Critical Paths**: Focus on user journeys that matter
8. **Run in Parallel**: Leverage Playwright's parallelization
9. **Integrate with CI**: Automate test execution on every commit
10. **Debug Effectively**: Use traces, screenshots, and videos

## Resources

- [Playwright Documentation](https://playwright.dev)
- [Testing Library Principles](https://testing-library.com/docs/guiding-principles)
- [Page Object Model Pattern](https://playwright.dev/docs/pom)
- [Accessibility Testing](https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright)


## Quality Tests

### Coverage Test
- All critical paths have test coverage
- **PASS:** Happy path, error paths, and edge cases each have at least one test
- **FAIL:** Only happy path tested, error handling untested

### Maintainability Test
- Tests are resilient to implementation changes
- **PASS:** Tests verify behavior/outcomes, not internal method calls
- **FAIL:** Tests break when refactoring without changing behavior

