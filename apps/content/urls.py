from django.urls import path

from apps.common.crud import build_views

from . import views
from .resources import blog, faqs, services, testimonials

urlpatterns = [
    path('settings', views.SettingsView.as_view()),
    path('admin/settings', views.AdminSettingsView.as_view()),
    *build_views(blog),
    *build_views(testimonials),
    *build_views(faqs),
    *build_views(services),
]
