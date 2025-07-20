"""
URL configuration for resortsathi project.

For more information, see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Local views
from dashboard.views import index
from loan.views import mark_notification_read

urlpatterns = [
    # Admin and Dashboard
    path('admin/', admin.site.urls),
    path('', index, name="home"),

    # Core Modules
    path('bookings/', include('bookings.urls')),
    path('inventory/', include('inventory.urls')),
    path('kot/', include('kot.urls')),
    path('rooms/', include('rooms.urls')),
    path('loan/', include('loan.urls')),
    path('hr/', include('hr.urls')),
    path('accounting/', include('accounting.urls')),
    path('accounts/', include('accounts.urls')),
    path('crm/', include('crm.urls')),
    path('tickets/', include('tickets.urls')),

    # Notifications
    path('notification/read/<int:pk>/', mark_notification_read, name='mark_notification_read'),
]

# Static and Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
