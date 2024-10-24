from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    
    path('', include('index.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('profiles/', include('profiles.urls')),
    path('cookies/', include('cookie_consent.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.handler404'