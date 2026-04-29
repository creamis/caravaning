from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views # Importar las vistas de autenticación de Django
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
    # Ruta para cerrar sesión
    path('users/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Ruta para robots.txt
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)