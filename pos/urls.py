from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
    path('api/', include([
        path('auth/', include('api.auth.urls', namespace='api_auth')),
        path('activity/', include('api.activity.urls', namespace='api_activity')),

        path('choices/', include('api.choices.urls', namespace='api_choices')),
    ]))
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)