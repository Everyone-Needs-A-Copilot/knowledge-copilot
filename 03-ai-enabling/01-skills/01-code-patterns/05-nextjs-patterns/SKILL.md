---
last_updated: 2026-02-25
status: active
name: nextjs-patterns
description: Next.js App Router - Server Components, data fetching, caching, middleware. Use when building Next.js apps.
triggers:
  files: ["**/app/**/*.tsx", "**/app/**/*.ts", "**/next.config.*", "**/middleware.ts"]
  keywords: ["server component", "client component", "use server", "use client", "SSR", "ISR", "route handler", "server action", "metadata"]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Next.js Patterns: Deep Expertise Skill

## Overview

Next.js 13+ with the App Router fundamentally changes how we build React applications. This skill provides comprehensive guidance on Server Components, data fetching, caching, routing, and the full Next.js ecosystem.

**When to use this skill:**
- Building with Next.js App Router (app directory)
- Server vs Client Component architecture
- Data fetching and caching strategies
- Route Handlers and Server Actions
- Metadata API and SEO optimization
- Streaming and Suspense patterns
- Next.js middleware and authentication

**Core Philosophy:** Next.js App Router embraces React Server Components, enabling zero-JavaScript-by-default pages with selective client-side interactivity. Think server-first, hydrate only what needs interactivity.

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## Core Principles

### 1. Server Components by Default

**Everything in `app/` is a Server Component unless marked `'use client'`.**

```tsx
// ✅ Server Component (default)
// app/posts/page.tsx
async function PostsPage() {
  // Runs on the server only
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());

  return (
    <div>
      <h1>Posts</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  );
}

export default PostsPage;
```

**Benefits:**
- Zero JavaScript sent to client for static content
- Direct database/API access without API routes
- Automatic code splitting
- Better SEO (fully rendered HTML)
- Smaller bundle sizes

### 2. Client Components for Interactivity

Use `'use client'` directive for components that need:
- Event handlers (onClick, onChange, etc.)
- Browser APIs (window, localStorage, etc.)
- State (useState, useReducer)
- Effects (useEffect)
- Custom hooks that use client hooks

```tsx
// ✅ Client Component
// components/Counter.tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
    </div>
  );
}
```

### 3. Composition: Server + Client Components

**✅ Good: Server component wrapping client component**

```tsx
// app/dashboard/page.tsx (Server Component)
import { Suspense } from 'react';
import { UserStats } from './UserStats'; // Client Component
import { getServerData } from '@/lib/api';

export default async function DashboardPage() {
  // Server-side data fetching
  const stats = await getServerData();

  return (
    <div>
      <h1>Dashboard</h1>

      {/* Server-rendered static content */}
      <div className="stats">
        <p>Total Users: {stats.totalUsers}</p>
        <p>Active Today: {stats.activeToday}</p>
      </div>

      {/* Interactive client component */}
      <Suspense fallback={<StatsLoading />}>
        <UserStats initialData={stats} />
      </Suspense>
    </div>
  );
}
```

**❌ Bad: Importing Server Component in Client Component**

```tsx
// ❌ This won't work
'use client';

import { ServerOnlyComponent } from './ServerComponent'; // Error!

export function ClientComponent() {
  return <ServerOnlyComponent />; // Can't render server component in client
}
```

**✅ Good: Pass Server Component as children**

```tsx
// ✅ Server Component
// app/layout.tsx
import { ClientLayout } from '@/components/ClientLayout';
import { ServerSidebar } from '@/components/ServerSidebar';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ClientLayout>
          {/* Server Component passed as children */}
          <ServerSidebar />
          {children}
        </ClientLayout>
      </body>
    </html>
  );
}

// ✅ Client Component
// components/ClientLayout.tsx
'use client';

export function ClientLayout({ children }) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className={isOpen ? 'layout-open' : 'layout-closed'}>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {children} {/* Server Components render here */}
    </div>
  );
}
```

---

## File-System Based Routing

### 1. Route Organization

```
app/
├── page.tsx              # /
├── about/
│   └── page.tsx          # /about
├── blog/
│   ├── page.tsx          # /blog
│   └── [slug]/
│       └── page.tsx      # /blog/my-post
├── dashboard/
│   ├── layout.tsx        # Shared layout for /dashboard/*
│   ├── page.tsx          # /dashboard
│   ├── settings/
│   │   └── page.tsx      # /dashboard/settings
│   └── (insights)/       # Route group (doesn't affect URL)
│       ├── topics/
│       │   └── page.tsx  # /dashboard/topics
│       └── stories/
│           └── page.tsx  # /dashboard/stories
└── api/
    └── posts/
        └── route.ts      # /api/posts (Route Handler)
```

### 2. Dynamic Routes

**Single dynamic segment:**

```tsx
// app/posts/[id]/page.tsx
interface PageProps {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function PostPage({ params, searchParams }: PageProps) {
  const post = await getPost(params.id);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// Generate static params at build time (SSG)
export async function generateStaticParams() {
  const posts = await getPosts();

  return posts.map(post => ({
    id: post.id.toString()
  }));
}
```

**Multiple dynamic segments:**

```tsx
// app/blog/[category]/[slug]/page.tsx
interface PageProps {
  params: { category: string; slug: string };
}

export default async function BlogPostPage({ params }: PageProps) {
  const post = await getPostBySlug(params.category, params.slug);
  return <article>{/* ... */}</article>;
}

export async function generateStaticParams() {
  const posts = await getAllPosts();

  return posts.map(post => ({
    category: post.category,
    slug: post.slug
  }));
}
```

**Catch-all routes:**

```tsx
// app/docs/[...slug]/page.tsx
// Matches: /docs/a, /docs/a/b, /docs/a/b/c

interface PageProps {
  params: { slug: string[] };
}

export default async function DocsPage({ params }: PageProps) {
  const path = params.slug.join('/');
  const doc = await getDoc(path);
  return <article>{doc.content}</article>;
}
```

**Optional catch-all:**

```tsx
// app/shop/[[...slug]]/page.tsx
// Matches: /shop, /shop/electronics, /shop/electronics/phones

export default async function ShopPage({ params }: PageProps) {
  const category = params.slug ? params.slug.join('/') : 'all';
  const products = await getProducts(category);
  return <ProductList products={products} />;
}
```

### 3. Route Groups (Organization Only)

Route groups don't affect URLs - they're for organization.

```
app/
├── (marketing)/
│   ├── about/page.tsx      # /about
│   └── contact/page.tsx    # /contact
├── (dashboard)/
│   ├── settings/page.tsx   # /settings
│   └── profile/page.tsx    # /profile
└── (auth)/
    ├── login/page.tsx      # /login
    └── signup/page.tsx     # /signup
```

### 4. Parallel Routes

Render multiple pages in the same layout simultaneously.

```
app/
├── @analytics/
│   └── page.tsx
├── @team/
│   └── page.tsx
└── layout.tsx

// layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
}) {
  return (
    <div>
      <div>{children}</div>
      <div className="grid grid-cols-2">
        <div>{analytics}</div>
        <div>{team}</div>
      </div>
    </div>
  );
}
```

### 5. Intercepting Routes

Intercept routes to show in modal while preserving background page.

```
app/
├── photos/
│   └── [id]/
│       └── page.tsx        # /photos/123
└── @modal/
    └── (..)photos/
        └── [id]/
            └── page.tsx    # Intercepts /photos/123
```

```tsx
// app/@modal/(..)photos/[id]/page.tsx
export default function PhotoModal({ params }: { params: { id: string } }) {
  return (
    <Modal>
      <Photo id={params.id} />
    </Modal>
  );
}
```

---

## Data Fetching

### 1. Server Component Data Fetching

**✅ Good: Async Server Components**

```tsx
// app/topics/page.tsx
import { db } from '@/lib/db';

export default async function TopicsPage() {
  // Direct database access - no API route needed
  const topics = await db.topic.findMany({
    where: { status: 'published' },
    include: { author: true },
    orderBy: { createdAt: 'desc' }
  });

  return (
    <div>
      <h1>Topics</h1>
      <TopicsList topics={topics} />
    </div>
  );
}
```

**Parallel data fetching:**

```tsx
async function getData() {
  // These run in parallel
  const [topics, authors, tags] = await Promise.all([
    fetch('https://api.example.com/topics').then(r => r.json()),
    fetch('https://api.example.com/authors').then(r => r.json()),
    fetch('https://api.example.com/tags').then(r => r.json())
  ]);

  return { topics, authors, tags };
}

export default async function DashboardPage() {
  const { topics, authors, tags } = await getData();

  return (
    <div>
      <TopicsList topics={topics} />
      <AuthorsList authors={authors} />
      <TagCloud tags={tags} />
    </div>
  );
}
```

**Sequential data fetching (when needed):**

```tsx
export default async function PostPage({ params }: { params: { id: string } }) {
  // Sequential: wait for post first
  const post = await getPost(params.id);

  // Then fetch related data based on post
  const relatedPosts = await getRelatedPosts(post.category);

  return (
    <div>
      <Post data={post} />
      <RelatedPosts posts={relatedPosts} />
    </div>
  );
}
```

### 2. Fetch API with Caching

Next.js extends `fetch()` with caching options.

**Cache strategies:**

```tsx
// ✅ Force cache (default)
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache' // Cached indefinitely
});

// ✅ Revalidate every 60 seconds (ISR)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 }
});

// ✅ No caching (always fresh)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
});

// ✅ Tag-based revalidation
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
});

// Later: revalidate all fetches with 'posts' tag
import { revalidateTag } from 'next/cache';
revalidateTag('posts');
```

**Real-world example:**

```tsx
// app/topics/[id]/page.tsx
import { notFound } from 'next/navigation';

interface Topic {
  id: string;
  title: string;
  description: string;
  updatedAt: string;
}

async function getTopic(id: string): Promise<Topic | null> {
  const res = await fetch(`${process.env.API_URL}/topics/${id}`, {
    next: {
      revalidate: 300, // 5 minutes
      tags: ['topic', `topic-${id}`]
    }
  });

  if (!res.ok) return null;
  return res.json();
}

export default async function TopicPage({ params }: { params: { id: string } }) {
  const topic = await getTopic(params.id);

  if (!topic) {
    notFound(); // Shows app/not-found.tsx
  }

  return (
    <article>
      <h1>{topic.title}</h1>
      <p>{topic.description}</p>
      <time>{new Date(topic.updatedAt).toLocaleDateString()}</time>
    </article>
  );
}

// Generate static pages for top 100 topics at build time
export async function generateStaticParams() {
  const topics = await fetch(`${process.env.API_URL}/topics?limit=100`)
    .then(r => r.json());

  return topics.map((topic: Topic) => ({
    id: topic.id
  }));
}

// SEO metadata
export async function generateMetadata({ params }: { params: { id: string } }) {
  const topic = await getTopic(params.id);

  if (!topic) return { title: 'Topic Not Found' };

  return {
    title: topic.title,
    description: topic.description,
    openGraph: {
      title: topic.title,
      description: topic.description,
      type: 'article',
      publishedTime: topic.updatedAt
    }
  };
}
```

### 3. Client-Side Data Fetching

Use client-side fetching for:
- User-specific data
- Real-time updates
- Infinite scroll
- Search/filter interactions

**With SWR:**

```tsx
'use client';

import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export function TopicsList() {
  const { data, error, isLoading, mutate } = useSWR('/api/topics', fetcher, {
    refreshInterval: 10000, // Poll every 10s
    revalidateOnFocus: true
  });

  if (isLoading) return <Skeleton />;
  if (error) return <Error message="Failed to load" />;

  return (
    <div>
      {data.topics.map(topic => (
        <TopicCard key={topic.id} topic={topic} onUpdate={() => mutate()} />
      ))}
    </div>
  );
}
```

**With React Query:**

```tsx
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function TopicsList() {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ['topics'],
    queryFn: async () => {
      const res = await fetch('/api/topics');
      if (!res.ok) throw new Error('Failed to fetch');
      return res.json();
    },
    staleTime: 5 * 60 * 1000 // 5 minutes
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      await fetch(`/api/topics/${id}`, { method: 'DELETE' });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['topics'] });
    }
  });

  if (isLoading) return <Skeleton />;
  if (error) return <Error error={error} />;

  return (
    <div>
      {data.topics.map(topic => (
        <TopicCard
          key={topic.id}
          topic={topic}
          onDelete={() => deleteMutation.mutate(topic.id)}
        />
      ))}
    </div>
  );
}
```

---

## Route Handlers (API Routes)

Route Handlers replace API routes from Pages Router.

### 1. Basic Route Handler

```ts
// app/api/topics/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db';

// GET /api/topics
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const status = searchParams.get('status');

    const topics = await db.topic.findMany({
      where: status ? { status } : undefined,
      orderBy: { createdAt: 'desc' }
    });

    return NextResponse.json({ topics });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch topics' },
      { status: 500 }
    );
  }
}

// POST /api/topics
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate
    if (!body.title) {
      return NextResponse.json(
        { error: 'Title is required' },
        { status: 400 }
      );
    }

    const topic = await db.topic.create({
      data: {
        title: body.title,
        description: body.description,
        userId: body.userId
      }
    });

    return NextResponse.json({ topic }, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create topic' },
      { status: 500 }
    );
  }
}
```

### 2. Dynamic Route Handlers

```ts
// app/api/topics/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

interface RouteContext {
  params: { id: string };
}

// GET /api/topics/:id
export async function GET(
  request: NextRequest,
  { params }: RouteContext
) {
  const topic = await db.topic.findUnique({
    where: { id: params.id },
    include: { concepts: true }
  });

  if (!topic) {
    return NextResponse.json(
      { error: 'Topic not found' },
      { status: 404 }
    );
  }

  return NextResponse.json({ topic });
}

// PATCH /api/topics/:id
export async function PATCH(
  request: NextRequest,
  { params }: RouteContext
) {
  const body = await request.json();

  const topic = await db.topic.update({
    where: { id: params.id },
    data: body
  });

  return NextResponse.json({ topic });
}

// DELETE /api/topics/:id
export async function DELETE(
  request: NextRequest,
  { params }: RouteContext
) {
  await db.topic.delete({
    where: { id: params.id }
  });

  return NextResponse.json({ success: true });
}
```

### 3. Streaming Responses

```ts
// app/api/stream/route.ts
import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      try {
        // Simulating streaming data
        for (let i = 0; i < 10; i++) {
          const data = JSON.stringify({ count: i, timestamp: Date.now() });
          controller.enqueue(encoder.encode(`data: ${data}\n\n`));
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
        controller.close();
      } catch (error) {
        controller.error(error);
      }
    }
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  });
}
```

### 4. Route Handler with Auth

```ts
// app/api/topics/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';

export async function GET(request: NextRequest) {
  const session = await getServerSession(authOptions);

  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const topics = await db.topic.findMany({
    where: { userId: session.user.id }
  });

  return NextResponse.json({ topics });
}
```

---

## Server Actions

Server Actions are asynchronous functions that run on the server, called from Client or Server Components.

### 1. Defining Server Actions

**In a Server Component file:**

```tsx
// app/topics/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { db } from '@/lib/db';

export async function createTopic(formData: FormData) {
  // Extract form data
  const title = formData.get('title') as string;
  const description = formData.get('description') as string;

  // Validate
  if (!title || title.length < 3) {
    return { error: 'Title must be at least 3 characters' };
  }

  // Create in database
  const topic = await db.topic.create({
    data: {
      title,
      description,
      userId: 'user-id' // Get from session
    }
  });

  // Revalidate cache
  revalidatePath('/topics');

  // Redirect
  redirect(`/topics/${topic.id}`);
}

export async function updateTopic(id: string, formData: FormData) {
  const title = formData.get('title') as string;

  await db.topic.update({
    where: { id },
    data: { title }
  });

  revalidatePath(`/topics/${id}`);
  revalidatePath('/topics');

  return { success: true };
}

export async function deleteTopic(id: string) {
  await db.topic.delete({
    where: { id }
  });

  revalidatePath('/topics');
  redirect('/topics');
}
```

### 2. Using Server Actions in Forms

**Simple form submission:**

```tsx
// app/topics/new/page.tsx
import { createTopic } from '../actions';

export default function NewTopicPage() {
  return (
    <form action={createTopic}>
      <div>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          required
        />
      </div>

      <div>
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
        />
      </div>

      <button type="submit">Create Topic</button>
    </form>
  );
}
```

**With client-side validation and loading states:**

```tsx
'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { createTopic } from '../actions';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Topic'}
    </button>
  );
}

export default function NewTopicForm() {
  const [state, formAction] = useFormState(createTopic, { error: null });

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          required
        />
        {state?.error && (
          <p className="text-red-500">{state.error}</p>
        )}
      </div>

      <div>
        <label htmlFor="description">Description</label>
        <textarea id="description" name="description" />
      </div>

      <SubmitButton />
    </form>
  );
}
```

### 3. Programmatic Server Actions

Call Server Actions programmatically, not just from forms.

```tsx
'use client';

import { deleteTopic } from '../actions';
import { useTransition } from 'react';

export function TopicCard({ topic }) {
  const [isPending, startTransition] = useTransition();

  const handleDelete = () => {
    startTransition(async () => {
      await deleteTopic(topic.id);
    });
  };

  return (
    <div>
      <h3>{topic.title}</h3>
      <button
        onClick={handleDelete}
        disabled={isPending}
      >
        {isPending ? 'Deleting...' : 'Delete'}
      </button>
    </div>
  );
}
```

### 4. Server Actions with Return Values

```tsx
// actions.ts
'use server';

export async function pinEvidence(topicId: string, evidenceId: string) {
  try {
    await db.evidence.update({
      where: { id: evidenceId },
      data: { pinned: true }
    });

    revalidatePath(`/topics/${topicId}`);

    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Component
'use client';

export function EvidenceItem({ evidence, topicId }) {
  const [isPinned, setIsPinned] = useState(evidence.pinned);

  const handlePin = async () => {
    const result = await pinEvidence(topicId, evidence.id);

    if (result.success) {
      setIsPinned(true);
    } else {
      alert(`Failed: ${result.error}`);
    }
  };

  return (
    <div>
      <p>{evidence.content}</p>
      <button onClick={handlePin} disabled={isPinned}>
        {isPinned ? 'Pinned' : 'Pin'}
      </button>
    </div>
  );
}
```

---

## Streaming and Suspense

### 1. Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

async function TopicsWidget() {
  const topics = await fetchTopics(); // Slow
  return <TopicsList topics={topics} />;
}

async function StatsWidget() {
  const stats = await fetchStats(); // Fast
  return <Stats data={stats} />;
}

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Stats load fast, show immediately */}
      <Suspense fallback={<StatsLoading />}>
        <StatsWidget />
      </Suspense>

      {/* Topics load slow, stream when ready */}
      <Suspense fallback={<TopicsLoading />}>
        <TopicsWidget />
      </Suspense>
    </div>
  );
}
```

### 2. Nested Suspense Boundaries

```tsx
export default function Page() {
  return (
    <div>
      <Suspense fallback={<HeaderLoading />}>
        <Header />

        <div className="grid grid-cols-2">
          <Suspense fallback={<SidebarLoading />}>
            <Sidebar />
          </Suspense>

          <Suspense fallback={<ContentLoading />}>
            <Content />
          </Suspense>
        </div>
      </Suspense>
    </div>
  );
}
```

### 3. Loading UI

Special `loading.tsx` file creates automatic Suspense boundary.

```tsx
// app/topics/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
      <div className="space-y-3">
        <div className="h-20 bg-gray-200 rounded"></div>
        <div className="h-20 bg-gray-200 rounded"></div>
        <div className="h-20 bg-gray-200 rounded"></div>
      </div>
    </div>
  );
}

// app/topics/page.tsx
// This automatically wraps in <Suspense fallback={<Loading />}>
export default async function TopicsPage() {
  const topics = await fetchTopics();
  return <TopicsList topics={topics} />;
}
```

### 4. Streaming Server Actions

```tsx
'use server';

import { createStreamableValue } from 'ai/rsc';

export async function generateConcepts(topicId: string) {
  const stream = createStreamableValue('');

  (async () => {
    const concepts = await streamFromAPI(topicId);

    for await (const chunk of concepts) {
      stream.update(chunk);
    }

    stream.done();
  })();

  return { output: stream.value };
}

// Client Component
'use client';

import { readStreamableValue } from 'ai/rsc';

export function ConceptGenerator({ topicId }) {
  const [content, setContent] = useState('');

  const handleGenerate = async () => {
    const { output } = await generateConcepts(topicId);

    for await (const delta of readStreamableValue(output)) {
      setContent(delta);
    }
  };

  return (
    <div>
      <button onClick={handleGenerate}>Generate</button>
      <div>{content}</div>
    </div>
  );
}
```

---

## Metadata and SEO

### 1. Static Metadata

```tsx
// app/about/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
  keywords: ['company', 'about', 'team'],
  openGraph: {
    title: 'About Us',
    description: 'Learn more about our company',
    images: ['/og-image.jpg']
  },
  twitter: {
    card: 'summary_large_image',
    title: 'About Us',
    description: 'Learn more about our company',
    images: ['/og-image.jpg']
  }
};

export default function AboutPage() {
  return <div>About content</div>;
}
```

### 2. Dynamic Metadata

```tsx
// app/topics/[id]/page.tsx
import { Metadata } from 'next';

interface PageProps {
  params: { id: string };
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const topic = await fetchTopic(params.id);

  if (!topic) {
    return {
      title: 'Topic Not Found'
    };
  }

  return {
    title: topic.title,
    description: topic.description,
    keywords: topic.tags,
    openGraph: {
      title: topic.title,
      description: topic.description,
      type: 'article',
      publishedTime: topic.createdAt,
      modifiedTime: topic.updatedAt,
      authors: [topic.author.name],
      images: [
        {
          url: topic.coverImage || '/default-og.jpg',
          width: 1200,
          height: 630,
          alt: topic.title
        }
      ]
    },
    twitter: {
      card: 'summary_large_image',
      title: topic.title,
      description: topic.description,
      images: [topic.coverImage || '/default-og.jpg']
    },
    alternates: {
      canonical: `https://example.com/topics/${params.id}`
    }
  };
}

export default async function TopicPage({ params }: PageProps) {
  const topic = await fetchTopic(params.id);
  return <article>{/* ... */}</article>;
}
```

### 3. Metadata from Layout

```tsx
// app/layout.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'Insights Copilot',
    template: '%s | Insights Copilot' // Topic Title | Insights Copilot
  },
  description: 'AI-powered strategic insights',
  metadataBase: new URL('https://insights.example.com'),
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://insights.example.com',
    siteName: 'Insights Copilot',
    images: ['/og-default.jpg']
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1
    }
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png'
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### 4. JSON-LD for Structured Data

```tsx
// app/topics/[id]/page.tsx
export default async function TopicPage({ params }: { params: { id: string } }) {
  const topic = await fetchTopic(params.id);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: topic.title,
    description: topic.description,
    author: {
      '@type': 'Person',
      name: topic.author.name
    },
    datePublished: topic.createdAt,
    dateModified: topic.updatedAt,
    image: topic.coverImage,
    publisher: {
      '@type': 'Organization',
      name: 'Insights Copilot',
      logo: {
        '@type': 'ImageObject',
        url: 'https://example.com/logo.png'
      }
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>
        <h1>{topic.title}</h1>
        <p>{topic.description}</p>
      </article>
    </>
  );
}
```

---

## Caching and Revalidation

### 1. Request Memoization

React automatically deduplicates identical requests during a render.

```tsx
// These make only ONE request (React deduplication)
async function Header() {
  const user = await getUser(); // Fetches
  return <div>{user.name}</div>;
}

async function Sidebar() {
  const user = await getUser(); // Cached (same render)
  return <div>{user.email}</div>;
}

async function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  );
}
```

### 2. Data Cache (Fetch)

```tsx
// Cached indefinitely (default)
const data = await fetch('https://api.example.com/data');

// Revalidate every 60 seconds
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 }
});

// Never cache
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
});
```

### 3. Full Route Cache

Pages are automatically cached at build time (SSG).

```tsx
// app/topics/page.tsx
// Automatically cached at build time

export const revalidate = 3600; // Revalidate every hour

export default async function TopicsPage() {
  const topics = await fetchTopics();
  return <TopicsList topics={topics} />;
}
```

**Force dynamic rendering:**

```tsx
// Force dynamic (no caching)
export const dynamic = 'force-dynamic';

// Or use dynamic functions
import { cookies, headers } from 'next/headers';

export default async function Page() {
  const cookieStore = cookies(); // Forces dynamic
  // ...
}
```

### 4. Tag-Based Revalidation

```tsx
// Fetch with tags
const topics = await fetch('https://api.example.com/topics', {
  next: { tags: ['topics'] }
});

const topicDetail = await fetch(`https://api.example.com/topics/${id}`, {
  next: { tags: ['topics', `topic-${id}`] }
});

// Revalidate in Server Action
'use server';

import { revalidateTag } from 'next/cache';

export async function createTopic(data) {
  await db.topic.create({ data });

  // Revalidate all fetches tagged 'topics'
  revalidateTag('topics');
}

export async function updateTopic(id, data) {
  await db.topic.update({ where: { id }, data });

  // Revalidate specific topic and list
  revalidateTag(`topic-${id}`);
  revalidateTag('topics');
}
```

### 5. Path-Based Revalidation

```tsx
'use server';

import { revalidatePath } from 'next/cache';

export async function createTopic(data) {
  await db.topic.create({ data });

  // Revalidate specific path
  revalidatePath('/topics');

  // Revalidate all paths under /topics
  revalidatePath('/topics', 'layout');
}
```

### 6. On-Demand Revalidation (Webhook)

```ts
// app/api/revalidate/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { revalidatePath, revalidateTag } from 'next/cache';

export async function POST(request: NextRequest) {
  const secret = request.nextUrl.searchParams.get('secret');

  // Validate secret
  if (secret !== process.env.REVALIDATE_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  const body = await request.json();

  if (body.path) {
    revalidatePath(body.path);
  }

  if (body.tag) {
    revalidateTag(body.tag);
  }

  return NextResponse.json({ revalidated: true, now: Date.now() });
}

// Trigger: POST /api/revalidate?secret=xxx
// Body: { "path": "/topics" } or { "tag": "topics" }
```

---

## Middleware

Middleware runs before a request is completed, useful for auth, redirects, headers.

### 1. Basic Middleware

```ts
// middleware.ts (root level)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Log all requests
  console.log(`${request.method} ${request.url}`);

  // Add custom header
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');

  return response;
}

// Apply to specific paths
export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/:path*'
  ]
};
```

### 2. Authentication Middleware

```ts
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function middleware(request: NextRequest) {
  const token = await getToken({
    req: request,
    secret: process.env.NEXTAUTH_SECRET
  });

  const isAuthPage = request.nextUrl.pathname.startsWith('/login');
  const isProtectedPage = request.nextUrl.pathname.startsWith('/dashboard');

  // Redirect to login if accessing protected page without auth
  if (isProtectedPage && !token) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('callbackUrl', request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect to dashboard if accessing login while authenticated
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/login']
};
```

### 3. Feature Flags Middleware

```ts
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const url = request.nextUrl;

  // Check feature flag (could be from cookie, header, or config)
  const hasNewDashboard = request.cookies.get('new_dashboard')?.value === 'true';

  if (url.pathname === '/dashboard' && hasNewDashboard) {
    // Redirect to new dashboard
    return NextResponse.rewrite(new URL('/dashboard-v2', request.url));
  }

  return NextResponse.next();
}
```

### 4. Rate Limiting Middleware

```ts
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!
});

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, '10 s') // 10 requests per 10 seconds
});

export async function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const ip = request.ip ?? '127.0.0.1';
    const { success, limit, reset, remaining } = await ratelimit.limit(ip);

    if (!success) {
      return NextResponse.json(
        { error: 'Rate limit exceeded' },
        {
          status: 429,
          headers: {
            'X-RateLimit-Limit': limit.toString(),
            'X-RateLimit-Remaining': remaining.toString(),
            'X-RateLimit-Reset': reset.toString()
          }
        }
      );
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/api/:path*'
};
```

---

## Error Handling

### 1. Error Boundaries

```tsx
// app/error.tsx (catches errors in route segment)
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### 2. Global Error Handling

```tsx
// app/global-error.tsx (catches errors in root layout)
'use client';

export default function GlobalError({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Application Error</h2>
        <p>{error.message}</p>
        <button onClick={reset}>Reload</button>
      </body>
    </html>
  );
}
```

### 3. Not Found Pages

```tsx
// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div>
      <h1>404 - Page Not Found</h1>
      <p>Could not find requested resource</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}

// Trigger programmatically
import { notFound } from 'next/navigation';

export default async function Page({ params }) {
  const topic = await getTopic(params.id);

  if (!topic) {
    notFound(); // Shows not-found.tsx
  }

  return <div>{topic.title}</div>;
}
```

### 4. Route Segment Not Found

```tsx
// app/topics/[id]/not-found.tsx
export default function TopicNotFound() {
  return (
    <div>
      <h2>Topic Not Found</h2>
      <p>The topic you're looking for doesn't exist.</p>
    </div>
  );
}
```

---

## Performance Patterns

### 1. Image Optimization

```tsx
import Image from 'next/image';

// ✅ Optimized image
export function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={630}
      priority // Load immediately (above fold)
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  );
}

// ✅ Responsive images
export function ResponsiveImage() {
  return (
    <Image
      src="/image.jpg"
      alt="Responsive image"
      width={800}
      height={600}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  );
}

// ✅ Fill mode (unknown dimensions)
export function Cover() {
  return (
    <div className="relative h-96">
      <Image
        src="/cover.jpg"
        alt="Cover"
        fill
        style={{ objectFit: 'cover' }}
      />
    </div>
  );
}
```

### 2. Font Optimization

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter'
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono'
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}

// CSS: font-family: var(--font-inter);
```

### 3. Script Optimization

```tsx
import Script from 'next/script';

export default function Page() {
  return (
    <>
      {/* Load after page is interactive */}
      <Script
        src="https://www.googletagmanager.com/gtag/js"
        strategy="afterInteractive"
      />

      {/* Load when browser is idle */}
      <Script
        src="https://example.com/analytics.js"
        strategy="lazyOnload"
      />

      {/* Inline script */}
      <Script id="analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        `}
      </Script>
    </>
  );
}
```

### 4. Dynamic Imports (Code Splitting)

```tsx
import dynamic from 'next/dynamic';

// ✅ Dynamic import with loading state
const HeavyComponent = dynamic(() => import('@/components/HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false // Disable SSR for this component
});

// ✅ Dynamic import with named export
const SpecificComponent = dynamic(
  () => import('@/components/Module').then(mod => mod.SpecificComponent)
);

export default function Page() {
  return (
    <div>
      <HeavyComponent />
    </div>
  );
}
```

### 5. Partial Prerendering (Experimental)

```tsx
// next.config.js
module.exports = {
  experimental: {
    ppr: true
  }
};

// app/page.tsx
export default function Page() {
  return (
    <div>
      {/* Static shell */}
      <Header />

      {/* Dynamic content streamed */}
      <Suspense fallback={<Skeleton />}>
        <DynamicContent />
      </Suspense>

      {/* Static footer */}
      <Footer />
    </div>
  );
}
```

---

## Best Practices

### 1. Component Organization

```
app/
├── (dashboard)/
│   ├── topics/
│   │   ├── [id]/
│   │   │   ├── page.tsx           # Route
│   │   │   ├── loading.tsx        # Loading UI
│   │   │   ├── error.tsx          # Error boundary
│   │   │   └── not-found.tsx      # 404
│   │   ├── _components/           # Private components (not routes)
│   │   │   ├── TopicCard.tsx
│   │   │   └── TopicFilters.tsx
│   │   ├── actions.ts             # Server actions
│   │   └── page.tsx
│   └── layout.tsx                 # Shared layout
└── components/                     # Shared components
    ├── ui/                         # UI primitives
    └── shared/                     # Shared business components
```

### 2. Type Safety

```tsx
// types/topic.ts
export interface Topic {
  id: string;
  title: string;
  description: string;
  status: 'draft' | 'published' | 'archived';
  createdAt: string;
  updatedAt: string;
}

// app/topics/[id]/page.tsx
import { Topic } from '@/types/topic';

interface PageProps {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

async function getTopic(id: string): Promise<Topic> {
  const res = await fetch(`${process.env.API_URL}/topics/${id}`);
  if (!res.ok) throw new Error('Failed to fetch topic');
  return res.json();
}

export default async function TopicPage({ params }: PageProps) {
  const topic = await getTopic(params.id);
  return <TopicDetail topic={topic} />;
}
```

### 3. Environment Variables

```ts
// .env.local
DATABASE_URL="postgresql://..."
NEXT_PUBLIC_API_URL="https://api.example.com"

// Access in Server Components/Route Handlers
const dbUrl = process.env.DATABASE_URL;

// Access in Client Components (must be prefixed with NEXT_PUBLIC_)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// Type-safe environment variables
// env.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXT_PUBLIC_API_URL: z.string().url(),
  OPENAI_API_KEY: z.string().min(1)
});

export const env = envSchema.parse(process.env);

// Usage
import { env } from '@/lib/env';
const apiKey = env.OPENAI_API_KEY;
```

### 4. Error Handling Patterns

```tsx
// lib/api.ts
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export async function fetchAPI<T>(url: string): Promise<T> {
  const res = await fetch(url);

  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: 'Unknown error' }));
    throw new APIError(
      error.message || 'Request failed',
      res.status,
      error.code
    );
  }

  return res.json();
}

// Usage in Server Component
export default async function Page() {
  try {
    const data = await fetchAPI<Topic[]>('/api/topics');
    return <TopicsList topics={data} />;
  } catch (error) {
    if (error instanceof APIError) {
      if (error.status === 404) {
        notFound();
      }
      throw error; // Caught by error.tsx
    }
    throw error;
  }
}
```

---

## Anti-Patterns

### 1. Using Client Components Unnecessarily

```tsx
// ❌ BAD: Client component for static content
'use client';

export default function About() {
  return (
    <div>
      <h1>About Us</h1>
      <p>Static content</p>
    </div>
  );
}

// ✅ GOOD: Server component (default)
export default function About() {
  return (
    <div>
      <h1>About Us</h1>
      <p>Static content</p>
    </div>
  );
}
```

### 2. Data Fetching in Client Components

```tsx
// ❌ BAD: Fetch in client component
'use client';

import { useEffect, useState } from 'react';

export default function Topics() {
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    fetch('/api/topics')
      .then(r => r.json())
      .then(setTopics);
  }, []);

  return <div>{/* ... */}</div>;
}

// ✅ GOOD: Fetch in Server Component
export default async function Topics() {
  const topics = await fetch('/api/topics').then(r => r.json());
  return <TopicsList topics={topics} />;
}
```

### 3. Not Using Suspense for Async Components

```tsx
// ❌ BAD: No loading state
export default async function Page() {
  return (
    <div>
      <SlowComponent /> {/* Page hangs until loaded */}
    </div>
  );
}

// ✅ GOOD: Suspense boundary
export default async function Page() {
  return (
    <div>
      <Suspense fallback={<Loading />}>
        <SlowComponent />
      </Suspense>
    </div>
  );
}
```

### 4. Mixing Pages and App Router

```tsx
// ❌ BAD: Don't mix pages/ and app/ for same routes
pages/
  blog/
    [slug].tsx          # Old Pages Router

app/
  blog/
    [slug]/
      page.tsx          # New App Router

// ✅ GOOD: Choose one router
app/
  blog/
    [slug]/
      page.tsx          # App Router only
```

### 5. Not Memoizing Expensive Computations

```tsx
// ❌ BAD: Recalculating on every render
'use client';

export function ExpensiveComponent({ data }) {
  const processed = heavyComputation(data); // Runs on every render
  return <div>{processed}</div>;
}

// ✅ GOOD: useMemo
'use client';

import { useMemo } from 'react';

export function ExpensiveComponent({ data }) {
  const processed = useMemo(() => heavyComputation(data), [data]);
  return <div>{processed}</div>;
}
```

---

## Testing Patterns

### 1. Testing Server Components

```tsx
// __tests__/app/topics/page.test.tsx
import { render, screen } from '@testing-library/react';
import TopicsPage from '@/app/topics/page';

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([
      { id: '1', title: 'Topic 1' },
      { id: '2', title: 'Topic 2' }
    ])
  })
) as jest.Mock;

describe('TopicsPage', () => {
  it('renders topics', async () => {
    const component = await TopicsPage();
    render(component);

    expect(screen.getByText('Topic 1')).toBeInTheDocument();
    expect(screen.getByText('Topic 2')).toBeInTheDocument();
  });
});
```

### 2. Testing Server Actions

```tsx
// __tests__/actions/topics.test.ts
import { createTopic } from '@/app/topics/actions';

jest.mock('@/lib/db', () => ({
  topic: {
    create: jest.fn()
  }
}));

describe('createTopic', () => {
  it('creates topic with valid data', async () => {
    const formData = new FormData();
    formData.append('title', 'New Topic');
    formData.append('description', 'Description');

    const result = await createTopic(formData);

    expect(result).toEqual({ success: true });
    expect(db.topic.create).toHaveBeenCalled();
  });

  it('returns error with invalid data', async () => {
    const formData = new FormData();
    formData.append('title', ''); // Invalid

    const result = await createTopic(formData);

    expect(result).toEqual({ error: 'Title is required' });
  });
});
```

### 3. E2E Testing with Playwright

```ts
// tests/topics.spec.ts
import { test, expect } from '@playwright/test';

test('create topic flow', async ({ page }) => {
  await page.goto('/topics');

  await page.click('text=New Topic');

  await page.fill('[name="title"]', 'Test Topic');
  await page.fill('[name="description"]', 'Test description');

  await page.click('button:has-text("Create")');

  await expect(page).toHaveURL(/\/topics\/[a-z0-9-]+/);
  await expect(page.locator('h1')).toContainText('Test Topic');
});
```

---

## Summary

**Next.js App Router Essentials:**

1. **Server Components by default** - Zero JavaScript, direct data access
2. **Client Components** - Use `'use client'` only when needed
3. **File-based routing** - `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`
4. **Data fetching** - Async Server Components, extended `fetch()`, caching
5. **Server Actions** - Type-safe mutations without API routes
6. **Streaming** - Suspense boundaries for progressive rendering
7. **Metadata API** - SEO-friendly dynamic metadata
8. **Middleware** - Auth, redirects, headers before request completes
9. **Caching** - Request memoization, Data Cache, Full Route Cache
10. **Performance** - Image/Font/Script optimization, code splitting

**Mental Model:**
- Think server-first
- Minimize client JavaScript
- Compose Server + Client strategically
- Leverage streaming for better UX
- Use built-in caching intelligently

---

When building with Next.js App Router:
1. Default to Server Components
2. Add `'use client'` only for interactivity
3. Fetch data in Server Components
4. Use Suspense for loading states
5. Implement proper error boundaries
6. Optimize metadata for SEO
7. Cache strategically
8. Stream when possible
9. Test server and client separately
10. Monitor bundle size and performance


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

