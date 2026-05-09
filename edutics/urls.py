from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
                  path('api/v1/', include('courses.urls')), # courses app URL'leri
    path('api/v1/', include('core.urls')),
    path('api/v1/', include('events.urls')),
    path('api/v1/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)