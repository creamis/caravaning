from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.DestinationListView.as_view(), name='destination_list'),
    path('<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('nuevo/', views.DestinationCreateView.as_view(), name='destination_create'),
    path('<int:pk>/editar/', views.DestinationUpdateView.as_view(), name='destination_update'),
    path('<int:pk>/eliminar/', views.DestinationDeleteView.as_view(), name='destination_delete'),
    path('usuario/<str:username>/', views.UserDestinationsView.as_view(), name='user_destinations'),
]