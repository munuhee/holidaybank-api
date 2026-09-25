from django.contrib import admin

from .models import BlogPost, Faq, Service, SiteSettings, Tag, Testimonial


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_at', 'featured', 'is_sample')
    list_filter = ('status', 'featured', 'is_sample', 'tags')
    search_fields = ('title', 'excerpt')
    filter_horizontal = ('tags',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'tour_name', 'status', 'is_sample')
    list_filter = ('status', 'is_sample', 'rating')


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'group', 'order', 'status', 'is_sample')
    list_filter = ('group', 'status')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'status', 'is_sample')


admin.site.register(Tag)
admin.site.register(SiteSettings)
