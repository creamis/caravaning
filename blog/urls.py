from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, UserPostsView, PostDeleteView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),               # Lista de posts publicados
    path('create/', PostCreateView.as_view(), name='post_create'),    # Crear post
    path('user/<str:username>/', UserPostsView.as_view(), name='user_posts'), # Mis Blogs
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'), # Detalle del post
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'), # Editar post
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'), # Eliminar post
]
