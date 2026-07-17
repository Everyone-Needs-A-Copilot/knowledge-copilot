---
last_updated: 2026-02-25
status: active
name: django-patterns
description: Django patterns - ORM, views, middleware, signals, admin. Use when building Django applications.
triggers:
  files: ["**/views.py", "**/models.py", "**/urls.py", "**/admin.py", "**/settings.py", "**/forms.py", "**/serializers.py", "**/middleware.py"]
  keywords: ["django", "ORM", "queryset", "middleware", "signal", "admin", "template", "form", "CBV", "FBV", "DRF", "django-rest-framework"]
allowed-tools: Read, Write, Edit
---

# Django Patterns: Deep Expertise

Comprehensive guide to building production-grade Django applications with best practices for models, views, forms, admin, REST APIs, and more.

## Table of Contents

1. [Model Design Patterns](#model-design-patterns)
2. [QuerySet Optimization](#queryset-optimization)
3. [Views: CBV vs FBV](#views-cbv-vs-fbv)
4. [Forms and Validation](#forms-and-validation)
5. [Admin Customization](#admin-customization)
6. [Django REST Framework](#django-rest-framework)
7. [Middleware Patterns](#middleware-patterns)
8. [Signals (When and When Not)](#signals-when-and-when-not)
9. [Template Patterns](#template-patterns)
10. [Authentication & Permissions](#authentication--permissions)
11. [Testing Django Apps](#testing-django-apps)
12. [Migrations Best Practices](#migrations-best-practices)
13. [Caching Strategies](#caching-strategies)
14. [Anti-Patterns](#anti-patterns)

---


## Define Done

- [ ] Pattern applied correctly in context of the codebase
- [ ] Code follows language-specific idioms and conventions
- [ ] Anti-patterns identified and avoided
- [ ] Code is readable, testable, and maintainable

## Model Design Patterns

### Basic Model Structure

**✅ Good: Comprehensive model with best practices**
```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


class BaseModel(models.Model):
    """Abstract base model with common fields"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Override save to add custom logic"""
        # Custom validation or processing
        super().save(*args, **kwargs)


class Topic(BaseModel):
    """Thought leadership topic"""

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        ACTIVE = 'active', _('Active')
        ARCHIVED = 'archived', _('Archived')

    title = models.CharField(
        max_length=500,
        db_index=True,
        help_text=_("Topic title")
    )
    slug = models.SlugField(
        max_length=500,
        unique=True,
        db_index=True
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text=_("Detailed description")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Topic tags")
    )

    # Foreign keys
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='topics',
        db_index=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='topics',
        null=True,
        blank=True
    )

    # Many-to-many
    collaborators = models.ManyToManyField(
        'auth.User',
        related_name='collaborated_topics',
        blank=True
    )

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['-created_at', 'title']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at', 'status']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(title__length__gt=0),
                name='topic_title_not_empty'
            )
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'slug': self.slug})

    def clean(self):
        """Model-level validation"""
        from django.core.exceptions import ValidationError
        if self.status == self.Status.ACTIVE and not self.description:
            raise ValidationError({
                'description': _('Active topics must have a description')
            })

    @property
    def is_active(self):
        """Computed property"""
        return self.status == self.Status.ACTIVE

    def activate(self):
        """Business logic method"""
        if self.status == self.Status.DRAFT:
            self.status = self.Status.ACTIVE
            self.save(update_fields=['status', 'updated_at'])

    @classmethod
    def get_active_topics(cls):
        """Class method for common queries"""
        return cls.objects.filter(status=cls.Status.ACTIVE)
```

### Model Relationships

**One-to-Many (ForeignKey)**
```python
class Evidence(BaseModel):
    """Evidence linked to a topic"""

    # Always use on_delete explicitly
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,  # Delete evidence when topic is deleted
        related_name='evidence_items',
        db_index=True
    )

    # PROTECT prevents deletion if related objects exist
    source = models.ForeignKey(
        'Source',
        on_delete=models.PROTECT,
        related_name='evidence_items'
    )

    # SET_NULL allows deletion but keeps this record
    reviewer = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_evidence'
    )

    # SET_DEFAULT with default value
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default=get_default_category,
        related_name='evidence_items'
    )


# Accessing relationships
topic = Topic.objects.get(id=topic_id)
evidence_items = topic.evidence_items.all()  # Forward relation

evidence = Evidence.objects.get(id=evidence_id)
topic = evidence.topic  # Reverse relation
```

**Many-to-Many**
```python
class Topic(BaseModel):
    # Simple M2M
    tags = models.ManyToManyField(
        'Tag',
        related_name='topics',
        blank=True
    )

    # M2M with through table (for extra fields)
    related_topics = models.ManyToManyField(
        'self',
        through='TopicRelation',
        symmetrical=False,
        blank=True
    )


class TopicRelation(models.Model):
    """Through model for M2M with extra fields"""
    from_topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='relations_from'
    )
    to_topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='relations_to'
    )
    relation_type = models.CharField(max_length=50)
    strength = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['from_topic', 'to_topic']]


# Using M2M
topic.tags.add(tag1, tag2)
topic.tags.remove(tag1)
topic.tags.set([tag1, tag2, tag3])
topic.tags.clear()

# With through model
TopicRelation.objects.create(
    from_topic=topic1,
    to_topic=topic2,
    relation_type='similar',
    strength=0.85
)
```

**One-to-One**
```python
class UserProfile(models.Model):
    """Extended user profile (one-to-one with User)"""
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


# Access
user = User.objects.get(username='alice')
profile = user.profile  # Direct access

# Create signal for auto-creation
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

### Custom Managers and QuerySets

**✅ Good: Custom QuerySet with chainable methods**
```python
from django.db import models
from django.utils import timezone


class TopicQuerySet(models.QuerySet):
    """Custom QuerySet with domain-specific methods"""

    def active(self):
        """Get active topics"""
        return self.filter(status=Topic.Status.ACTIVE)

    def by_user(self, user):
        """Get topics for specific user"""
        return self.filter(user=user)

    def recent(self, days=7):
        """Get topics from last N days"""
        since = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=since)

    def with_evidence_count(self):
        """Annotate with evidence count"""
        return self.annotate(
            evidence_count=models.Count('evidence_items')
        )

    def published_after(self, date):
        """Get topics published after date"""
        return self.filter(created_at__gte=date)


class TopicManager(models.Manager):
    """Custom manager"""

    def get_queryset(self):
        """Override base queryset"""
        return TopicQuerySet(self.model, using=self._db)

    # Proxy QuerySet methods to manager
    def active(self):
        return self.get_queryset().active()

    def by_user(self, user):
        return self.get_queryset().by_user(user)

    def recent(self, days=7):
        return self.get_queryset().recent(days)

    def with_evidence_count(self):
        return self.get_queryset().with_evidence_count()

    # Manager-only methods
    def create_with_defaults(self, user, title, **kwargs):
        """Custom creation method"""
        from django.utils.text import slugify

        slug = kwargs.pop('slug', slugify(title))
        topic = self.create(
            user=user,
            title=title,
            slug=slug,
            status=Topic.Status.DRAFT,
            **kwargs
        )
        return topic


class Topic(BaseModel):
    # ... fields ...

    objects = TopicManager()  # Default manager
    all_objects = models.Manager()  # Unfiltered manager


# Usage - chainable methods
topics = (
    Topic.objects
    .active()
    .by_user(user)
    .recent(days=30)
    .with_evidence_count()
    .filter(evidence_count__gt=5)
)

# Create with defaults
topic = Topic.objects.create_with_defaults(
    user=request.user,
    title="New Topic",
    description="Description"
)
```

### Model Methods vs Properties

```python
class Topic(BaseModel):
    # ... fields ...

    # Property - computed from fields, no DB access
    @property
    def is_recent(self):
        """Check if topic is less than 7 days old"""
        age = timezone.now() - self.created_at
        return age.days < 7

    # Property with caching
    @cached_property
    def evidence_count(self):
        """Cache evidence count (requires django.utils.functional)"""
        return self.evidence_items.count()

    # Method - may access DB or have side effects
    def add_evidence(self, content, source):
        """Business logic method"""
        return Evidence.objects.create(
            topic=self,
            content=content,
            source=source
        )

    def get_related_topics(self, limit=5):
        """Query related topics"""
        return Topic.objects.filter(
            tags__in=self.tags.all()
        ).exclude(
            id=self.id
        ).distinct()[:limit]

    # Class method - operates on model class
    @classmethod
    def get_popular_topics(cls, limit=10):
        """Get most popular topics"""
        return cls.objects.annotate(
            evidence_count=models.Count('evidence_items')
        ).order_by('-evidence_count')[:limit]

    # Static method - doesn't access instance or class
    @staticmethod
    def validate_title(title):
        """Validation helper"""
        if len(title) < 5:
            raise ValueError("Title too short")
        return title.strip()
```

---

## QuerySet Optimization

### N+1 Query Problem

**❌ Bad: N+1 queries**
```python
# Generates 1 query for topics + N queries for users
topics = Topic.objects.all()
for topic in topics:
    print(topic.user.username)  # Each access hits DB!
```

**✅ Good: select_related for foreign keys**
```python
# Single query with JOIN
topics = Topic.objects.select_related('user').all()
for topic in topics:
    print(topic.user.username)  # No additional query

# Multiple foreign keys
evidence = Evidence.objects.select_related(
    'topic',
    'topic__user',
    'source'
).all()
```

**✅ Good: prefetch_related for many-to-many and reverse foreign keys**
```python
# Efficient for M2M and reverse ForeignKey
topics = Topic.objects.prefetch_related(
    'tags',
    'evidence_items',
    'collaborators'
).all()

for topic in topics:
    print(topic.tags.all())  # No query, uses prefetched cache
    print(topic.evidence_items.count())  # Uses cache
```

### Advanced Prefetching

**Custom Prefetch objects**
```python
from django.db.models import Prefetch

# Prefetch with custom queryset
topics = Topic.objects.prefetch_related(
    Prefetch(
        'evidence_items',
        queryset=Evidence.objects.filter(
            status='verified'
        ).select_related('source'),
        to_attr='verified_evidence'
    )
).all()

for topic in topics:
    # Use custom attribute
    for evidence in topic.verified_evidence:
        print(evidence.source.name)  # source also prefetched

# Multiple levels of prefetching
topics = Topic.objects.prefetch_related(
    Prefetch(
        'evidence_items',
        queryset=Evidence.objects.select_related('source')
    ),
    'tags',
    'collaborators__profile'
).all()
```

### Aggregation and Annotation

**✅ Good: Database-level aggregation**
```python
from django.db.models import Count, Avg, Sum, Max, Min, Q, F

# Annotate each topic with counts
topics = Topic.objects.annotate(
    evidence_count=Count('evidence_items'),
    tag_count=Count('tags'),
    collaborator_count=Count('collaborators')
)

for topic in topics:
    print(f"{topic.title}: {topic.evidence_count} evidence")

# Conditional aggregation
topics = Topic.objects.annotate(
    verified_count=Count(
        'evidence_items',
        filter=Q(evidence_items__status='verified')
    ),
    pending_count=Count(
        'evidence_items',
        filter=Q(evidence_items__status='pending')
    )
)

# Aggregate across entire queryset
stats = Topic.objects.aggregate(
    total_topics=Count('id'),
    avg_evidence=Avg('evidence_items__count'),
    max_evidence=Max('evidence_items__count')
)
# Returns: {'total_topics': 100, 'avg_evidence': 5.5, ...}

# Using F expressions for field comparisons
topics = Topic.objects.filter(
    evidence_items__count__gt=F('collaborators__count')
)

# Arithmetic with F expressions
Evidence.objects.update(
    final_score=F('base_score') * F('weight')
)
```

### Query Optimization Techniques

**only() and defer()**
```python
# Load only specific fields (SELECT specific columns)
topics = Topic.objects.only('id', 'title', 'status')
# Accessing other fields will trigger additional queries

# Defer loading of large fields
topics = Topic.objects.defer('description', 'content')
# description and content loaded only when accessed

# Combine with select_related
topics = Topic.objects.select_related('user').only(
    'id', 'title', 'user__username'
)
```

**values() and values_list()**
```python
# Return dicts instead of model instances (faster)
topic_dicts = Topic.objects.values('id', 'title', 'status')
# [{'id': 1, 'title': '...', 'status': 'active'}, ...]

# Return tuples
topic_tuples = Topic.objects.values_list('id', 'title')
# [(1, 'Title 1'), (2, 'Title 2'), ...]

# Flat list of single values
topic_ids = Topic.objects.values_list('id', flat=True)
# [1, 2, 3, 4, ...]

# Named tuples (Python 3.6+)
from collections import namedtuple
topic_tuples = Topic.objects.values_list(
    'id', 'title', named=True
)
# Returns namedtuple instances
```

**Bulk Operations**
```python
# Bulk create (single query)
topics = [
    Topic(title=f"Topic {i}", user=user)
    for i in range(100)
]
Topic.objects.bulk_create(topics, batch_size=50)

# Bulk update (single query, Django 2.2+)
topics = Topic.objects.filter(status='draft')
for topic in topics:
    topic.status = 'active'
Topic.objects.bulk_update(topics, ['status'], batch_size=50)

# Update query (single query)
Topic.objects.filter(status='draft').update(status='active')

# Delete query (single query)
Topic.objects.filter(status='archived').delete()

# ✅ Atomic operations
from django.db import transaction

@transaction.atomic
def process_topics(topic_ids):
    """Process topics atomically"""
    topics = Topic.objects.select_for_update().filter(
        id__in=topic_ids
    )
    for topic in topics:
        topic.status = 'processing'
        topic.save()
    # All or nothing
```

### Raw SQL (When Necessary)

```python
# Raw SQL query
topics = Topic.objects.raw(
    'SELECT * FROM topics WHERE status = %s',
    ['active']
)

# Execute custom SQL
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(
        "UPDATE topics SET status = %s WHERE created_at < %s",
        ['archived', cutoff_date]
    )
    rows_affected = cursor.rowcount

# Complex query with raw SQL
from django.db import connection

def get_topic_statistics():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                t.status,
                COUNT(*) as count,
                AVG(evidence_count) as avg_evidence
            FROM topics t
            LEFT JOIN (
                SELECT topic_id, COUNT(*) as evidence_count
                FROM evidence
                GROUP BY topic_id
            ) e ON t.id = e.topic_id
            GROUP BY t.status
        """)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
```

---

## Views: CBV vs FBV

### Function-Based Views (FBV)

**✅ Good: Simple, explicit FBV**
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
def topic_create(request):
    """Create new topic"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            form.save_m2m()  # Save M2M relations

            messages.success(request, 'Topic created successfully')
            return redirect('topic-detail', slug=topic.slug)
    else:
        form = TopicForm()

    return render(request, 'topics/create.html', {
        'form': form,
        'title': 'Create Topic'
    })


@login_required
def topic_detail(request, slug):
    """Display topic detail"""
    topic = get_object_or_404(
        Topic.objects.select_related('user').prefetch_related(
            'evidence_items__source',
            'tags',
            'collaborators'
        ),
        slug=slug
    )

    # Permission check
    if not topic.is_active and topic.user != request.user:
        return HttpResponseForbidden("You don't have access to this topic")

    context = {
        'topic': topic,
        'evidence_items': topic.evidence_items.all(),
        'can_edit': topic.user == request.user
    }
    return render(request, 'topics/detail.html', context)


def api_topic_list(request):
    """API endpoint (JSON response)"""
    topics = Topic.objects.active().values(
        'id', 'title', 'status', 'created_at'
    )

    return JsonResponse({
        'topics': list(topics),
        'count': len(topics)
    })
```

### Class-Based Views (CBV)

**✅ Good: Generic CBVs for common patterns**
```python
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count, Q


class TopicListView(ListView):
    """List all active topics"""
    model = Topic
    template_name = 'topics/list.html'
    context_object_name = 'topics'
    paginate_by = 20

    def get_queryset(self):
        """Override queryset"""
        qs = Topic.objects.active().select_related(
            'user'
        ).prefetch_related(
            'tags'
        ).annotate(
            evidence_count=Count('evidence_items')
        )

        # Filter by query parameter
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        # Order by parameter
        order = self.request.GET.get('order', '-created_at')
        qs = qs.order_by(order)

        return qs

    def get_context_data(self, **kwargs):
        """Add extra context"""
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_count'] = Topic.objects.active().count()
        return context


class TopicDetailView(DetailView):
    """Display single topic"""
    model = Topic
    template_name = 'topics/detail.html'
    context_object_name = 'topic'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Optimize query"""
        return Topic.objects.select_related(
            'user', 'category'
        ).prefetch_related(
            'evidence_items__source',
            'tags',
            'collaborators'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.object.user == self.request.user
        context['related_topics'] = self.object.get_related_topics()
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    """Create new topic"""
    model = Topic
    form_class = TopicForm
    template_name = 'topics/create.html'
    success_url = reverse_lazy('topic-list')

    def form_valid(self, form):
        """Set user before saving"""
        form.instance.user = self.request.user
        form.instance.status = Topic.Status.DRAFT

        response = super().form_valid(form)

        messages.success(
            self.request,
            f'Topic "{self.object.title}" created successfully'
        )
        return response

    def get_success_url(self):
        """Dynamic success URL"""
        return reverse('topic-detail', kwargs={'slug': self.object.slug})


class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing topic"""
    model = Topic
    form_class = TopicForm
    template_name = 'topics/edit.html'

    def test_func(self):
        """Permission check"""
        topic = self.get_object()
        return topic.user == self.request.user or self.request.user.is_staff

    def get_success_url(self):
        return reverse('topic-detail', kwargs={'slug': self.object.slug})


class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete topic"""
    model = Topic
    template_name = 'topics/confirm_delete.html'
    success_url = reverse_lazy('topic-list')

    def test_func(self):
        topic = self.get_object()
        return topic.user == self.request.user
```

### Custom Mixins

**✅ Good: Reusable mixins**
```python
class AjaxResponseMixin:
    """Mixin for AJAX responses"""

    def form_invalid(self, form):
        """Return JSON for AJAX requests"""
        if self.request.is_ajax():
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        """Return JSON for AJAX requests"""
        if self.request.is_ajax():
            self.object = form.save()
            return JsonResponse({
                'success': True,
                'object_id': str(self.object.id),
                'redirect_url': self.get_success_url()
            })
        return super().form_valid(form)


class UserOwnerMixin(UserPassesTestMixin):
    """Mixin to check object ownership"""

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class PrefetchRelatedMixin:
    """Mixin to prefetch related objects"""
    prefetch_related_fields = []

    def get_queryset(self):
        qs = super().get_queryset()
        if self.prefetch_related_fields:
            qs = qs.prefetch_related(*self.prefetch_related_fields)
        return qs


# Usage
class TopicUpdateView(
    LoginRequiredMixin,
    UserOwnerMixin,
    AjaxResponseMixin,
    PrefetchRelatedMixin,
    UpdateView
):
    model = Topic
    form_class = TopicForm
    prefetch_related_fields = ['tags', 'evidence_items']
```

---

## Forms and Validation

### ModelForm Patterns

**✅ Good: Comprehensive ModelForm**
```python
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TopicForm(forms.ModelForm):
    """Form for creating/editing topics"""

    # Override field widgets/attributes
    title = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter topic title',
            'autofocus': True
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Describe your topic'
        })
    )

    # Additional field not in model
    accept_terms = forms.BooleanField(
        required=True,
        label=_("I accept the terms and conditions")
    )

    class Meta:
        model = Topic
        fields = ['title', 'description', 'status', 'tags', 'category']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'title': _('Choose a descriptive title'),
            'status': _('Draft topics are not visible to others'),
        }
        labels = {
            'title': _('Topic Title'),
        }

    def __init__(self, *args, user=None, **kwargs):
        """Custom initialization"""
        super().__init__(*args, **kwargs)
        self.user = user

        # Make certain fields required conditionally
        if self.instance.status == Topic.Status.ACTIVE:
            self.fields['description'].required = True

        # Filter category choices by user
        if user:
            self.fields['category'].queryset = Category.objects.filter(
                Q(owner=user) | Q(is_public=True)
            )

    def clean_title(self):
        """Field-level validation"""
        title = self.cleaned_data.get('title')

        # Check uniqueness for this user
        if self.user and Topic.objects.filter(
            user=self.user,
            title__iexact=title
        ).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                _('You already have a topic with this title')
            )

        return title.strip()

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        description = cleaned_data.get('description')

        # Active topics must have description
        if status == Topic.Status.ACTIVE and not description:
            raise ValidationError({
                'description': _('Active topics require a description')
            })

        return cleaned_data

    def save(self, commit=True):
        """Custom save logic"""
        instance = super().save(commit=False)

        # Generate slug from title
        if not instance.slug:
            from django.utils.text import slugify
            instance.slug = slugify(instance.title)

        # Set user if creating
        if self.user and not instance.pk:
            instance.user = self.user

        if commit:
            instance.save()
            self.save_m2m()

        return instance
```

### Form Validation Patterns

**Custom validators**
```python
from django.core.validators import RegexValidator


def validate_no_special_chars(value):
    """Custom validator function"""
    import re
    if re.search(r'[^a-zA-Z0-9\s-]', value):
        raise ValidationError(
            _('%(value)s contains special characters'),
            params={'value': value}
        )


class TopicForm(forms.ModelForm):
    title = forms.CharField(
        validators=[
            validate_no_special_chars,
            MinLengthValidator(5),
            MaxLengthValidator(500)
        ]
    )

    phone = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be 10-15 digits"
            )
        ]
    )
```

### Form Wizards (Multi-Step Forms)

```python
from formtools.wizard.views import SessionWizardView


class TopicWizard(SessionWizardView):
    """Multi-step topic creation"""

    template_name = 'topics/wizard.html'
    form_list = [
        ('basic', TopicBasicForm),
        ('details', TopicDetailsForm),
        ('evidence', EvidenceForm),
    ]

    def get_form_initial(self, step):
        """Initial data for each step"""
        initial = super().get_form_initial(step)
        if step == 'basic':
            initial['user'] = self.request.user
        return initial

    def done(self, form_list, **kwargs):
        """Process all forms when wizard completes"""
        # Combine data from all forms
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        # Create topic
        topic = Topic.objects.create(
            user=self.request.user,
            **data
        )

        return redirect('topic-detail', slug=topic.slug)
```

---

## Admin Customization

### Basic Admin Configuration

**✅ Good: Customized ModelAdmin**
```python
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Topic admin interface"""

    # List display
    list_display = [
        'title',
        'user_link',
        'status_badge',
        'evidence_count',
        'created_at',
        'is_recent'
    ]

    list_filter = [
        'status',
        'created_at',
        'updated_at',
        ('user', admin.RelatedOnlyFieldListFilter),
    ]

    search_fields = [
        'title',
        'description',
        'user__username',
        'user__email'
    ]

    # Edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Classification', {
            'fields': ('status', 'category', 'tags')
        }),
        ('Relationships', {
            'fields': ('user', 'collaborators'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'slug']

    prepopulated_fields = {'slug': ('title',)}

    autocomplete_fields = ['user', 'category']

    filter_horizontal = ['collaborators', 'tags']

    date_hierarchy = 'created_at'

    ordering = ['-created_at']

    list_per_page = 50

    # Custom methods
    @admin.display(description='User', ordering='user__username')
    def user_link(self, obj):
        """Link to user admin"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.user.username
        )

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        """Colored status badge"""
        colors = {
            'draft': 'gray',
            'active': 'green',
            'archived': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )

    @admin.display(description='Evidence', ordering='evidence_count')
    def evidence_count(self, obj):
        """Display evidence count"""
        return obj.evidence_count

    @admin.display(boolean=True, description='Recent')
    def is_recent(self, obj):
        """Boolean indicator for recent topics"""
        return obj.is_recent

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'category').annotate(
            evidence_count=Count('evidence_items')
        )

    # Actions
    actions = ['make_active', 'make_archived']

    @admin.action(description='Mark selected as active')
    def make_active(self, request, queryset):
        """Bulk action to activate topics"""
        updated = queryset.update(status=Topic.Status.ACTIVE)
        self.message_user(
            request,
            f'{updated} topics marked as active'
        )

    @admin.action(description='Archive selected topics')
    def make_archived(self, request, queryset):
        """Bulk action to archive topics"""
        updated = queryset.update(status=Topic.Status.ARCHIVED)
        self.message_user(
            request,
            f'{updated} topics archived'
        )
```

### Inline Admin

```python
class EvidenceInline(admin.TabularInline):
    """Inline evidence items in topic admin"""
    model = Evidence
    extra = 1
    fields = ['content', 'source', 'status', 'confidence_score']
    autocomplete_fields = ['source']

    def get_queryset(self, request):
        """Optimize inline queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('source')


class TopicRelationInline(admin.StackedInline):
    """Stacked inline for related topics"""
    model = TopicRelation
    fk_name = 'from_topic'
    extra = 0
    fields = ['to_topic', 'relation_type', 'strength']
    autocomplete_fields = ['to_topic']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [EvidenceInline, TopicRelationInline]
```

### Custom Admin Actions and Views

```python
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    # ... other config ...

    def get_urls(self):
        """Add custom admin URLs"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/regenerate/',
                self.admin_site.admin_view(self.regenerate_view),
                name='topic-regenerate'
            ),
        ]
        return custom_urls + urls

    def regenerate_view(self, request, object_id):
        """Custom admin view for regenerating topic"""
        topic = self.get_object(request, object_id)

        if request.method == 'POST':
            # Perform regeneration
            topic.regenerate_evidence()
            self.message_user(
                request,
                f'Topic "{topic.title}" regenerated successfully'
            )
            return redirect('admin:myapp_topic_change', topic.id)

        context = {
            **self.admin_site.each_context(request),
            'topic': topic,
            'opts': self.model._meta,
        }
        return render(request, 'admin/topic_regenerate.html', context)
```

---

## Django REST Framework

### Serializer Patterns

**✅ Good: Comprehensive serializers**
```python
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class EvidenceSerializer(serializers.ModelSerializer):
    """Evidence serializer with nested source"""

    source_name = serializers.CharField(
        source='source.name',
        read_only=True
    )

    class Meta:
        model = Evidence
        fields = [
            'id', 'content', 'source', 'source_name',
            'status', 'confidence_score', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TopicListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view"""

    user = UserSerializer(read_only=True)
    evidence_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Topic
        fields = [
            'id', 'title', 'slug', 'status',
            'user', 'evidence_count', 'created_at'
        ]


class TopicDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail view"""

    user = UserSerializer(read_only=True)
    evidence_items = EvidenceSerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True)

    # Computed field
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = [
            'id', 'title', 'slug', 'description', 'status',
            'user', 'evidence_items', 'tags',
            'is_editable', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_is_editable(self, obj):
        """Check if current user can edit"""
        request = self.context.get('request')
        if request and request.user:
            return obj.user == request.user
        return False

    def validate_title(self, value):
        """Field validation"""
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters"
            )
        return value

    def validate(self, attrs):
        """Cross-field validation"""
        if attrs.get('status') == 'active' and not attrs.get('description'):
            raise serializers.ValidationError({
                'description': 'Active topics require a description'
            })
        return attrs


class TopicCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating topics"""

    class Meta:
        model = Topic
        fields = ['title', 'description', 'status', 'tags']

    def create(self, validated_data):
        """Custom creation logic"""
        tags = validated_data.pop('tags', [])
        user = self.context['request'].user

        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['title'])
        validated_data['user'] = user

        topic = Topic.objects.create(**validated_data)
        topic.tags.set(tags)

        return topic
```

### ViewSet Patterns

**✅ Good: Feature-rich ViewSet**
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class TopicViewSet(viewsets.ModelViewSet):
    """Topic API ViewSet"""

    queryset = Topic.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    # Filtering and search
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'user']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'evidence_count']
    ordering = ['-created_at']

    def get_queryset(self):
        """Optimize and filter queryset"""
        qs = super().get_queryset()

        # Optimize based on action
        if self.action == 'list':
            qs = qs.select_related('user').annotate(
                evidence_count=Count('evidence_items')
            )
        elif self.action == 'retrieve':
            qs = qs.select_related('user', 'category').prefetch_related(
                'evidence_items__source',
                'tags',
                'collaborators'
            )

        # Filter by current user if requested
        if self.request.query_params.get('mine'):
            qs = qs.filter(user=self.request.user)

        return qs

    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return TopicListSerializer
        elif self.action == 'create':
            return TopicCreateSerializer
        return TopicDetailSerializer

    def perform_create(self, serializer):
        """Set user when creating"""
        serializer.save(user=self.request.user)

    # Custom actions
    @action(detail=True, methods=['post'])
    def activate(self, request, slug=None):
        """Activate a topic"""
        topic = self.get_object()

        if topic.user != request.user:
            return Response(
                {'error': 'Only the owner can activate this topic'},
                status=status.HTTP_403_FORBIDDEN
            )

        topic.status = Topic.Status.ACTIVE
        topic.save()

        serializer = self.get_serializer(topic)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def evidence(self, request, slug=None):
        """Get evidence for topic"""
        topic = self.get_object()
        evidence = topic.evidence_items.all()

        serializer = EvidenceSerializer(evidence, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent topics"""
        topics = self.get_queryset().filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        )

        page = self.paginate_queryset(topics)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(topics, many=True)
        return Response(serializer.data)
```

### Custom Permissions

```python
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission - owner can edit, others read-only"""

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for owner
        return obj.user == request.user


class IsAdminOrOwner(permissions.BasePermission):
    """Admin or owner can edit"""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff or
            obj.user == request.user
        )


# Usage in ViewSet
class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
```

---

## Middleware Patterns

### Custom Middleware

**✅ Good: Modern middleware (Django 1.10+)**
```python
import structlog
from django.utils.deprecation import MiddlewareMixin

logger = structlog.get_logger(__name__)


class RequestLoggingMiddleware:
    """Log all requests"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code executed before view
        logger.info(
            "request_started",
            method=request.method,
            path=request.path,
            user=str(request.user) if request.user.is_authenticated else 'anonymous'
        )

        # Process request
        response = self.get_response(request)

        # Code executed after view
        logger.info(
            "request_completed",
            method=request.method,
            path=request.path,
            status=response.status_code
        )

        return response

    def process_exception(self, request, exception):
        """Handle exceptions"""
        logger.error(
            "request_exception",
            method=request.method,
            path=request.path,
            error=str(exception),
            exc_info=True
        )
        return None  # Let Django handle the exception


class TimingMiddleware:
    """Add request timing"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import time

        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        response['X-Request-Duration'] = str(duration)

        logger.info(
            "request_timing",
            path=request.path,
            duration=duration
        )

        return response


class APIVersionMiddleware:
    """Handle API versioning"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract version from header or URL
        version = request.META.get('HTTP_API_VERSION', '1.0')
        request.api_version = version

        response = self.get_response(request)
        response['API-Version'] = version

        return response


# Add to settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'myapp.middleware.TimingMiddleware',  # Custom middleware
    'myapp.middleware.RequestLoggingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## Signals (When and When Not)

### When to Use Signals

**✅ Good: Decoupled actions triggered by model events**
```python
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


# Auto-create related model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        UserProfile.objects.create(user=instance)


# Trigger background task
@receiver(post_save, sender=Topic)
def trigger_evidence_generation(sender, instance, created, **kwargs):
    """Generate evidence when topic is created"""
    if created:
        from myapp.tasks import generate_evidence
        generate_evidence.delay(instance.id)


# Clean up related resources
@receiver(pre_delete, sender=Topic)
def cleanup_topic_files(sender, instance, **kwargs):
    """Delete associated files when topic is deleted"""
    # Delete uploaded files
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)
```

### When NOT to Use Signals

**❌ Bad: Using signals for direct model logic**
```python
# DON'T DO THIS
@receiver(post_save, sender=Topic)
def update_topic_slug(sender, instance, **kwargs):
    """Update slug after save - BAD!"""
    from django.utils.text import slugify
    instance.slug = slugify(instance.title)
    instance.save()  # Causes infinite loop!
```

**✅ Good: Use model methods instead**
```python
class Topic(models.Model):
    # ... fields ...

    def save(self, *args, **kwargs):
        """Update slug before save"""
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

### Signal Best Practices

```python
# Use sender parameter to avoid registering for all models
@receiver(post_save, sender=Topic)
def handle_topic_save(sender, instance, created, **kwargs):
    pass

# Disconnect signals when needed (e.g., in tests)
from django.db.models.signals import post_save

post_save.disconnect(handle_topic_save, sender=Topic)

# Prevent infinite loops with update_fields
@receiver(post_save, sender=Topic)
def update_related(sender, instance, created, update_fields, **kwargs):
    if update_fields and 'status' not in update_fields:
        # Don't process if status wasn't changed
        return

    # Process status change
    if instance.status == 'active':
        # Do something
        pass
```

---

## Template Patterns

### Template Inheritance

**base.html**
```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Site{% endblock %}</title>

    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        {% block header %}
            <nav>
                {% include 'includes/nav.html' %}
            </nav>
        {% endblock %}
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        {% block footer %}
            {% include 'includes/footer.html' %}
        {% endblock %}
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

**topic_list.html**
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Topics - {{ block.super }}{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/topics.css' %}">
{% endblock %}

{% block content %}
    <h1>Topics</h1>

    {% if topics %}
        <ul class="topic-list">
            {% for topic in topics %}
                {% include 'topics/_topic_card.html' with topic=topic %}
            {% endfor %}
        </ul>

        {% include 'includes/pagination.html' with page_obj=page_obj %}
    {% else %}
        <p>No topics found.</p>
    {% endif %}
{% endblock %}
```

### Template Tags and Filters

**Custom template tags**
```python
# myapp/templatetags/topic_tags.py
from django import template
from django.utils.html import format_html
from django.urls import reverse

register = template.Library()


@register.simple_tag
def topic_url(topic):
    """Generate topic URL"""
    return reverse('topic-detail', kwargs={'slug': topic.slug})


@register.simple_tag(takes_context=True)
def active_link(context, url_name, **kwargs):
    """Add 'active' class to current page link"""
    request = context['request']
    url = reverse(url_name, kwargs=kwargs)

    if request.path == url:
        return format_html('class="active"')
    return ''


@register.filter
def truncate_smart(value, length=100):
    """Truncate text at word boundary"""
    if len(value) <= length:
        return value

    truncated = value[:length].rsplit(' ', 1)[0]
    return f"{truncated}..."


@register.inclusion_tag('topics/_status_badge.html')
def status_badge(topic):
    """Render status badge"""
    return {'topic': topic}


# Usage in template
{% load topic_tags %}

<a href="{% topic_url topic %}" {% active_link 'topic-detail' slug=topic.slug %}>
    {{ topic.title }}
</a>

<p>{{ topic.description|truncate_smart:150 }}</p>

{% status_badge topic %}
```

---

## Authentication & Permissions

### Custom User Model

**✅ Good: Custom user model (set before first migration)**
```python
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model"""
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'  # Use email for login
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


# settings.py
AUTH_USER_MODEL = 'myapp.User'
```

### Permission Checks

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Function-based view
@login_required
@permission_required('myapp.add_topic', raise_exception=True)
def topic_create(request):
    pass


# Class-based view
class TopicCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'myapp.add_topic'
    raise_exception = True


# Custom permission check
def user_can_edit_topic(user, topic):
    """Check if user can edit topic"""
    return user == topic.user or user.is_staff


# In view
if not user_can_edit_topic(request.user, topic):
    raise PermissionDenied("You cannot edit this topic")
```

---

## Testing Django Apps

### Model Tests

**✅ Good: Comprehensive model tests**
```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from myapp.models import Topic

User = get_user_model()


class TopicModelTest(TestCase):
    """Test Topic model"""

    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase"""
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def setUp(self):
        """Set up for each test method"""
        self.topic = Topic.objects.create(
            title='Test Topic',
            description='Test description',
            user=self.user
        )

    def test_topic_creation(self):
        """Test topic can be created"""
        self.assertIsInstance(self.topic, Topic)
        self.assertEqual(self.topic.title, 'Test Topic')

    def test_topic_str(self):
        """Test string representation"""
        self.assertEqual(str(self.topic), 'Test Topic')

    def test_slug_generation(self):
        """Test slug is auto-generated"""
        topic = Topic.objects.create(
            title='My New Topic',
            user=self.user
        )
        self.assertEqual(topic.slug, 'my-new-topic')

    def test_get_absolute_url(self):
        """Test get_absolute_url method"""
        url = self.topic.get_absolute_url()
        self.assertEqual(url, f'/topics/{self.topic.slug}/')

    def test_is_active_property(self):
        """Test is_active property"""
        self.topic.status = Topic.Status.ACTIVE
        self.assertTrue(self.topic.is_active)

        self.topic.status = Topic.Status.DRAFT
        self.assertFalse(self.topic.is_active)
```

### View Tests

```python
from django.test import TestCase, Client
from django.urls import reverse


class TopicViewTest(TestCase):
    """Test Topic views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.topic = Topic.objects.create(
            title='Test Topic',
            user=self.user
        )

    def test_topic_list_view(self):
        """Test topic list view"""
        response = self.client.get(reverse('topic-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/list.html')
        self.assertContains(response, 'Test Topic')

    def test_topic_detail_view(self):
        """Test topic detail view"""
        url = reverse('topic-detail', kwargs={'slug': self.topic.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['topic'], self.topic)

    def test_topic_create_requires_login(self):
        """Test create view requires authentication"""
        response = self.client.get(reverse('topic-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_topic_create_authenticated(self):
        """Test authenticated user can create topic"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('topic-create'), {
            'title': 'New Topic',
            'description': 'Description',
            'status': 'draft'
        })

        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(
            Topic.objects.filter(title='New Topic').exists()
        )
```

### API Tests (DRF)

```python
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class TopicAPITest(APITestCase):
    """Test Topic API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.topic = Topic.objects.create(
            title='Test Topic',
            user=self.user
        )

    def test_list_topics(self):
        """Test listing topics"""
        response = self.client.get('/api/topics/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_topic_unauthenticated(self):
        """Test creating topic without auth fails"""
        response = self.client.post('/api/topics/', {
            'title': 'New Topic',
            'description': 'Description'
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_topic_authenticated(self):
        """Test authenticated user can create topic"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/topics/', {
            'title': 'New Topic',
            'description': 'Description',
            'status': 'draft'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Topic')
```

---

## Migrations Best Practices

### Creating Migrations

```bash
# Create migration for model changes
python manage.py makemigrations

# Create empty migration for data migration
python manage.py makemigrations myapp --empty

# Name migration descriptively
python manage.py makemigrations myapp --name add_topic_status_field

# Check migration without applying
python manage.py migrate --plan
```

### Data Migration

**✅ Good: Data migration**
```python
# Generated migration file
from django.db import migrations


def populate_slugs(apps, schema_editor):
    """Add slugs to existing topics"""
    Topic = apps.get_model('myapp', 'Topic')
    from django.utils.text import slugify

    for topic in Topic.objects.all():
        if not topic.slug:
            topic.slug = slugify(topic.title)
            topic.save(update_fields=['slug'])


def reverse_populate_slugs(apps, schema_editor):
    """Reverse migration - clear slugs"""
    Topic = apps.get_model('myapp', 'Topic')
    Topic.objects.all().update(slug='')


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            populate_slugs,
            reverse_populate_slugs
        ),
    ]
```

### Migration Best Practices

```python
# ✅ DO: Make migrations small and focused
# ✅ DO: Test migrations on copy of production database
# ✅ DO: Provide reverse migrations when possible
# ❌ DON'T: Edit existing migrations after they're committed
# ❌ DON'T: Run migrations that delete data without backup

# Safe column addition
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='topic',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]

# Safe column removal (two-step)
# Step 1: Make field nullable and optional
# Step 2: Remove field in next migration

# Renaming fields (use RenameField)
operations = [
    migrations.RenameField(
        model_name='topic',
        old_name='desc',
        new_name='description',
    ),
]
```

---

## Caching Strategies

### Cache Patterns

**✅ Good: Cache expensive queries**
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page


# Cache view for 15 minutes
@cache_page(60 * 15)
def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'topics/list.html', {'topics': topics})


# Manual caching
def get_popular_topics():
    """Get popular topics with caching"""
    cache_key = 'popular_topics'
    topics = cache.get(cache_key)

    if topics is None:
        topics = Topic.objects.annotate(
            evidence_count=Count('evidence_items')
        ).order_by('-evidence_count')[:10]

        # Cache for 1 hour
        cache.set(cache_key, topics, 60 * 60)

    return topics


# Cache with versioning
def get_topic(topic_id, version=1):
    cache_key = f'topic_{topic_id}_v{version}'
    topic = cache.get(cache_key)

    if topic is None:
        topic = Topic.objects.get(id=topic_id)
        cache.set(cache_key, topic, 60 * 60)

    return topic


# Invalidate cache when model changes
from django.db.models.signals import post_save

@receiver(post_save, sender=Topic)
def invalidate_topic_cache(sender, instance, **kwargs):
    cache_key = f'topic_{instance.id}'
    cache.delete(cache_key)
    cache.delete('popular_topics')


# Template fragment caching
{% load cache %}
{% cache 500 sidebar request.user.username %}
    .. sidebar for logged in user ..
{% endcache %}
```

### Cache Configuration

```python
# settings.py

# Redis cache (recommended for production)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myapp',
        'TIMEOUT': 300,
    }
}

# Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Local memory cache (development only)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

---

## Anti-Patterns

### Common Django Anti-Patterns

**❌ Bad: Fat views**
```python
def topic_create(request):
    """Don't put all logic in views"""
    if request.method == 'POST':
        # 100 lines of business logic here...
        # Validation, processing, email sending, etc.
        pass
```

**✅ Good: Thin views with service layer**
```python
# services.py
class TopicService:
    @staticmethod
    def create_topic(user, title, description):
        """Business logic in service layer"""
        from django.utils.text import slugify

        topic = Topic.objects.create(
            user=user,
            title=title,
            slug=slugify(title),
            description=description
        )

        # Send notification
        send_topic_created_email(topic)

        return topic


# views.py
def topic_create(request):
    """Thin view"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = TopicService.create_topic(
                user=request.user,
                **form.cleaned_data
            )
            return redirect('topic-detail', slug=topic.slug)
    else:
        form = TopicForm()

    return render(request, 'topics/create.html', {'form': form})
```

**❌ Bad: N+1 queries**
```python
# Generates 101 queries!
topics = Topic.objects.all()
for topic in topics:
    print(topic.user.username)
```

**✅ Good: Eager loading**
```python
topics = Topic.objects.select_related('user').all()
for topic in topics:
    print(topic.user.username)
```

**❌ Bad: Circular imports**
```python
# models.py
from .views import process_topic  # BAD!

# views.py
from .models import Topic
```

**✅ Good: Avoid circular imports**
```python
# models.py
def process(self):
    from .services import process_topic  # Import inside method
    process_topic(self)
```

**❌ Bad: Using signals for everything**
```python
# Signals make code hard to follow
@receiver(post_save, sender=Topic)
def do_something(sender, instance, **kwargs):
    # Business logic here
    pass
```

**✅ Good: Explicit method calls**
```python
class Topic(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.do_something()  # Explicit and clear

    def do_something(self):
        # Business logic
        pass
```

**❌ Bad: Ignoring database indexes**
```python
class Topic(models.Model):
    title = models.CharField(max_length=500)
    # Frequent queries on title without index!
```

**✅ Good: Add indexes for frequently queried fields**
```python
class Topic(models.Model):
    title = models.CharField(max_length=500, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['-created_at']),
        ]
```

---

## Best Practices Summary

### Code Organization

1. **Use apps for modularity** - Keep related models, views, and templates together
2. **Follow Django naming conventions** - `models.py`, `views.py`, `urls.py`, etc.
3. **Keep business logic in models or services** - Not in views or templates
4. **Use managers for common queries** - Encapsulate query logic
5. **Create custom middleware sparingly** - Only for cross-cutting concerns

### Performance

1. **Always optimize queries** - Use `select_related()` and `prefetch_related()`
2. **Use database indexes** - For frequently queried fields
3. **Implement caching** - Cache expensive operations
4. **Use pagination** - For large querysets
5. **Profile with django-debug-toolbar** - Identify bottlenecks

### Security

1. **Never trust user input** - Always validate and sanitize
2. **Use Django's built-in security features** - CSRF, XSS protection
3. **Keep SECRET_KEY secret** - Use environment variables
4. **Use HTTPS in production** - Enable security middleware
5. **Follow OWASP guidelines** - Stay updated on security best practices

### Testing

1. **Write tests for all code** - Models, views, forms, APIs
2. **Use TestCase for database tests** - TransactionTestCase when needed
3. **Mock external dependencies** - Keep tests fast and isolated
4. **Test edge cases** - Not just happy paths
5. **Maintain test coverage** - Aim for >80%

---

## Conclusion

This skill provides comprehensive patterns for building production-grade Django applications. Apply these patterns based on your specific requirements, always prioritizing code clarity, maintainability, and performance.

**Key Takeaways:**

1. **Models**: Design models with proper relationships, indexes, and managers
2. **Queries**: Optimize with `select_related()`, `prefetch_related()`, and annotations
3. **Views**: Choose FBV for simple cases, CBV for common patterns
4. **Forms**: Leverage ModelForms with proper validation
5. **Admin**: Customize for better usability and features
6. **DRF**: Use serializers and viewsets for robust APIs
7. **Middleware**: Create only for cross-cutting concerns
8. **Signals**: Use sparingly, prefer explicit method calls
9. **Testing**: Write comprehensive tests for all components
10. **Migrations**: Keep them small, focused, and reversible
11. **Caching**: Cache expensive queries and computations
12. **Avoid anti-patterns**: Fat views, N+1 queries, circular imports

When in doubt, follow Django's philosophy: "Explicit is better than implicit" and "Don't Repeat Yourself (DRY)".


## Quality Tests

### Idiomatic Test
- Code follows the language's established conventions
- **PASS:** A senior developer in this language would recognize the patterns as standard
- **FAIL:** Code works but uses patterns from a different language or outdated style

### Anti-Pattern Test
- Common mistakes for this pattern are explicitly addressed
- **PASS:** Skill warns against known pitfalls with examples of what NOT to do
- **FAIL:** Only shows the happy path without mentioning common mistakes

