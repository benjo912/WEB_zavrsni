from django.contrib import admin
from django.urls import path, include
from tracker.views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', include('tracker.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)