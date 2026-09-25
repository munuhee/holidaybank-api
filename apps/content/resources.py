from django.utils import timezone
from rest_framework import serializers

from apps.common.crud import Resource, assign
from apps.common.validation import (
    STATUS_CHOICES,
    BooleanString,
    ImageSchema,
    OptionalImageSchema,
    PaginationQuery,
    SearchField,
    SeoSchema,
    StringList,
)
from apps.media.services import image_shape, resolve_image

from .models import BlogPost, Faq, FaqGroup, Service, Tag, Testimonial

# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------


def post_shape(p: BlogPost) -> dict:
    return {
        'id': str(p.id),
        '_id': str(p.id),
        'title': p.title,
        'slug': p.slug,
        'excerpt': p.excerpt,
        'content': p.content,
        'coverImage': image_shape(p.cover_image),
        'author': {'name': p.author_name, **({'avatar': p.author_avatar} if p.author_avatar else {})},
        'tags': [t.name for t in p.tags.all()],
        'readingMinutes': p.reading_minutes,
        'publishedAt': p.published_at,
        'featured': p.featured,
        'status': p.status,
        'seo': p.seo,
        'isSample': p.is_sample,
        'sourceNote': p.source_note or None,
        'createdAt': p.created_at,
        'updatedAt': p.updated_at,
    }


class AuthorSchema(serializers.Serializer):
    name = serializers.CharField(max_length=120, default='Holidaybank Expeditions')
    avatar = serializers.CharField(max_length=500, required=False, allow_blank=True)


class BlogSchema(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=160)
    slug = serializers.CharField(max_length=160, required=False, allow_blank=True)
    excerpt = serializers.CharField(min_length=10, max_length=300, error_messages={'min_length': 'Write a short excerpt.'})
    content = serializers.CharField(min_length=20, error_messages={'min_length': 'Write the post body.'})
    coverImage = ImageSchema()
    author = AuthorSchema(required=False)
    tags = StringList(max_items=20, item_max=40, default=list)
    readingMinutes = serializers.IntegerField(min_value=1, required=False)
    publishedAt = serializers.DateTimeField(required=False)
    featured = serializers.BooleanField(default=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='draft')
    seo = SeoSchema(required=False, allow_null=True)
    isSample = serializers.BooleanField(required=False)
    sourceNote = serializers.CharField(max_length=300, required=False, allow_blank=True)


class BlogQuery(PaginationQuery):
    tag = serializers.CharField(max_length=40, required=False)
    featured = BooleanString()
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    q = SearchField()
    sort = serializers.ChoiceField(choices=['newest', 'oldest', 'title-asc', 'title-desc'], required=False)


def apply_post(obj: BlogPost, data: dict, creating: bool) -> None:
    assign(obj, data, {'title': 'title', 'excerpt': 'excerpt', 'content': 'content', 'featured': 'featured',
                       'status': 'status', 'seo': 'seo', 'isSample': 'is_sample', 'sourceNote': 'source_note', 'publishedAt': 'published_at'})
    if 'author' in data:
        obj.author_name = data['author'].get('name') or 'Holidaybank Expeditions'
        obj.author_avatar = data['author'].get('avatar') or ''
    if 'coverImage' in data:
        obj.cover_image = resolve_image(data['coverImage'])
    if creating and not obj.published_at:
        obj.published_at = timezone.now()
    if 'readingMinutes' in data:
        obj.reading_minutes = data['readingMinutes']
    elif 'content' in data:
        # ~220 words a minute, never less than one.
        obj.reading_minutes = max(1, round(len(obj.content.split()) / 220))
    obj.save()
    if 'tags' in data:
        names = sorted({t.strip().lower() for t in data['tags'] if t.strip()})
        obj.tags.set([Tag.objects.get_or_create(name=n)[0] for n in names])


blog = Resource(
    model=BlogPost,
    label='post',
    perm='blog',
    path='blog',
    shape=post_shape,
    create_schema=BlogSchema,
    update_schema=BlogSchema,
    list_query=BlogQuery,
    apply=apply_post,
    search_fields=['title', 'excerpt'],
    sorts={'newest': ['-published_at'], 'oldest': ['published_at'], 'title-asc': ['title'], 'title-desc': ['-title']},
    default_sort=['-published_at'],
    filter=lambda qs, q: _filter_posts(qs, q),
    queryset=lambda: BlogPost.objects.select_related('cover_image').prefetch_related('tags'),
    tags=lambda p: ['blog', f'post:{p.slug}', 'home'],
)


def _filter_posts(qs, q):
    if q.get('tag'):
        qs = qs.filter(tags__name=q['tag'].lower())
    if 'featured' in q:
        qs = qs.filter(featured=q['featured'])
    return qs


# ---------------------------------------------------------------------------
# Testimonials
# ---------------------------------------------------------------------------


def testimonial_shape(t: Testimonial) -> dict:
    return {
        'id': str(t.id),
        '_id': str(t.id),
        'authorName': t.author_name,
        'authorLocation': t.author_location or None,
        'avatar': t.avatar,
        'quote': t.quote,
        'rating': t.rating,
        'tour': str(t.tour_id) if t.tour_id else None,
        'tourName': t.tour_name or (t.tour.title if t.tour_id else None),
        'travelledOn': t.travelled_on,
        'featured': t.featured,
        'status': t.status,
        'order': t.order,
        'isSample': t.is_sample,
        'sourceNote': t.source_note or None,
        'createdAt': t.created_at,
    }


class TestimonialSchema(serializers.Serializer):
    authorName = serializers.CharField(min_length=2, max_length=120, error_messages={'min_length': 'Enter the reviewer name.'})
    authorLocation = serializers.CharField(max_length=120, required=False, allow_blank=True, allow_null=True)
    avatar = OptionalImageSchema(required=False, allow_null=True)
    quote = serializers.CharField(min_length=10, max_length=600, error_messages={'min_length': 'Enter the testimonial.'})
    rating = serializers.IntegerField(min_value=1, max_value=5, default=5)
    tour = serializers.UUIDField(required=False, allow_null=True)
    tourName = serializers.CharField(max_length=140, required=False, allow_blank=True, allow_null=True)
    travelledOn = serializers.DateField(required=False, allow_null=True)
    featured = serializers.BooleanField(default=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='draft')
    order = serializers.IntegerField(min_value=0, default=0)
    isSample = serializers.BooleanField(required=False)
    sourceNote = serializers.CharField(max_length=300, required=False, allow_blank=True)


class TestimonialQuery(PaginationQuery):
    featured = BooleanString()
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    q = SearchField()
    sort = serializers.ChoiceField(choices=['newest', 'oldest', 'author-asc', 'rating-desc'], required=False)


def apply_testimonial(obj: Testimonial, data: dict, creating: bool) -> None:
    assign(obj, data, {'authorName': 'author_name', 'quote': 'quote', 'rating': 'rating', 'travelledOn': 'travelled_on',
                       'featured': 'featured', 'status': 'status', 'order': 'order', 'isSample': 'is_sample', 'sourceNote': 'source_note',
                       'avatar': 'avatar'})
    if 'authorLocation' in data:
        obj.author_location = data['authorLocation'] or ''
    if 'tourName' in data:
        obj.tour_name = data['tourName'] or ''
    if 'tour' in data:
        obj.tour_id = data['tour']
    obj.save()


testimonials = Resource(
    model=Testimonial,
    label='testimonial',
    perm='testimonials',
    path='testimonials',
    shape=testimonial_shape,
    create_schema=TestimonialSchema,
    update_schema=TestimonialSchema,
    list_query=TestimonialQuery,
    apply=apply_testimonial,
    title_field=None,
    slug_field=None,
    search_fields=['author_name', 'quote'],
    sorts={'newest': ['-created_at'], 'oldest': ['created_at'], 'author-asc': ['author_name'],
           'rating-desc': ['-rating', '-created_at']},
    default_sort=['-featured', 'order', '-created_at'],
    filter=lambda qs, q: qs.filter(featured=q['featured']) if 'featured' in q else qs,
    queryset=lambda: Testimonial.objects.select_related('tour'),
    tags=lambda t: ['testimonials', 'home'],
)


# ---------------------------------------------------------------------------
# FAQs
# ---------------------------------------------------------------------------


def faq_shape(f: Faq) -> dict:
    return {
        'id': str(f.id),
        '_id': str(f.id),
        'question': f.question,
        'answer': f.answer,
        'group': f.group,
        'order': f.order,
        'status': f.status,
        'isSample': f.is_sample,
        'sourceNote': f.source_note or None,
    }


class FaqSchema(serializers.Serializer):
    question = serializers.CharField(min_length=5, max_length=240, error_messages={'min_length': 'Enter the question.'})
    answer = serializers.CharField(min_length=5, error_messages={'min_length': 'Enter the answer.'})
    group = serializers.ChoiceField(choices=FaqGroup.values, default='general')
    order = serializers.IntegerField(min_value=0, default=0)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='draft')
    isSample = serializers.BooleanField(required=False)
    sourceNote = serializers.CharField(max_length=300, required=False, allow_blank=True)


class FaqQuery(PaginationQuery):
    group = serializers.ChoiceField(choices=FaqGroup.values, required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    q = SearchField()
    sort = serializers.ChoiceField(choices=['order-asc', 'newest', 'question-asc'], required=False)


def apply_faq(obj: Faq, data: dict, creating: bool) -> None:
    assign(obj, data, {'question': 'question', 'answer': 'answer', 'group': 'group', 'order': 'order',
                       'status': 'status', 'isSample': 'is_sample', 'sourceNote': 'source_note'})
    obj.save()


faqs = Resource(
    model=Faq,
    label='FAQ',
    perm='faqs',
    path='faqs',
    shape=faq_shape,
    create_schema=FaqSchema,
    update_schema=FaqSchema,
    list_query=FaqQuery,
    apply=apply_faq,
    title_field=None,
    slug_field=None,
    search_fields=['question', 'answer'],
    sorts={'order-asc': ['group', 'order'], 'newest': ['-created_at'], 'question-asc': ['question']},
    default_sort=['group', 'order'],
    filter=lambda qs, q: qs.filter(group=q['group']) if q.get('group') else qs,
    tags=lambda f: ['faqs', 'home'],
)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


def service_shape(s: Service) -> dict:
    return {
        'id': str(s.id),
        '_id': str(s.id),
        'title': s.title,
        'slug': s.slug,
        'summary': s.summary,
        'body': s.body,
        'icon': s.icon,
        'image': image_shape(s.image),
        'highlights': s.highlights or [],
        'cta': {'label': s.cta_label, 'href': s.cta_href} if s.cta_label and s.cta_href else None,
        'order': s.order,
        'status': s.status,
        'isSample': s.is_sample,
        'sourceNote': s.source_note or None,
    }


class CtaSchema(serializers.Serializer):
    label = serializers.CharField(max_length=60, required=False, allow_blank=True)
    href = serializers.CharField(max_length=200, required=False, allow_blank=True)


class ServiceSchema(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=120)
    slug = serializers.CharField(max_length=120, required=False, allow_blank=True)
    summary = serializers.CharField(min_length=10, max_length=300)
    body = serializers.CharField(required=False, allow_blank=True)
    icon = serializers.CharField(max_length=40, required=False, allow_blank=True)
    image = ImageSchema(required=False, allow_null=True)
    highlights = StringList(default=list)
    cta = CtaSchema(required=False, allow_null=True)
    order = serializers.IntegerField(min_value=0, default=0)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='draft')
    isSample = serializers.BooleanField(required=False)
    sourceNote = serializers.CharField(max_length=300, required=False, allow_blank=True)


class ServiceQuery(PaginationQuery):
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    q = SearchField()
    sort = serializers.ChoiceField(choices=['order-asc', 'title-asc', 'newest'], required=False)


def apply_service(obj: Service, data: dict, creating: bool) -> None:
    assign(obj, data, {'title': 'title', 'summary': 'summary', 'body': 'body', 'icon': 'icon',
                       'highlights': 'highlights', 'order': 'order', 'status': 'status', 'isSample': 'is_sample', 'sourceNote': 'source_note'})
    if 'image' in data:
        obj.image = resolve_image(data['image'])
    if 'cta' in data:
        cta = data['cta'] or {}
        obj.cta_label, obj.cta_href = cta.get('label', ''), cta.get('href', '')
    obj.save()


services = Resource(
    model=Service,
    label='service',
    perm='services',
    path='services',
    shape=service_shape,
    create_schema=ServiceSchema,
    update_schema=ServiceSchema,
    list_query=ServiceQuery,
    apply=apply_service,
    search_fields=['title', 'summary'],
    sorts={'order-asc': ['order', 'title'], 'title-asc': ['title'], 'newest': ['-created_at']},
    default_sort=['order', 'title'],
    queryset=lambda: Service.objects.select_related('image'),
    tags=lambda s: ['services', 'home'],
)
