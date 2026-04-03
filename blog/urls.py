from django.urls import path
from .views import PostCreateView, PostListView, PostDetailView

from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),               # Lista de posts publicados
    path('create/', PostCreateView.as_view(), name='post_create'),    # Crear post
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'), # Detalle del post
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'), # Editar post
]

