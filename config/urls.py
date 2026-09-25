from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from apps.common.views import health, json_not_found, json_server_error

urlpatterns = [
    # Django's own admin, for superusers. The day-to-day dashboard is the
    # Next.js app at /admin on the web origin, which talks to /api/admin/*.
    path('django-admin/', admin.site.urls),
    path('api/health', health),
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.catalog.urls')),
    path('api/', include('apps.content.urls')),
    path('api/', include('apps.enquiries.urls')),
    path('api/', include('apps.media.urls')),
    # Anything else under /api answers in the API's own error envelope, in
    # development too (handler404 only applies when DEBUG is off).
    re_path(r'^api/', json_not_found),
]

if settings.SERVE_MEDIA:
    urlpatterns.append(
        re_path(r'^uploads/(?P<path>[^/]+)$', serve, {'document_root': settings.MEDIA_ROOT})
    )

handler404 = json_not_found
handler500 = json_server_error
