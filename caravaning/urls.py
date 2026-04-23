from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Rutas de las aplicaciones
    path('', views.index, name='home'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('listings/', include('listings.urls', namespace='listings')),
    path('users/', include('users.urls', namespace='users')),
    path('messaging/', include('messaging.urls', namespace='messaging')),
    path('destinations/', include('destinations.urls', namespace='destinations')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('info/', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)