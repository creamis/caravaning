from django.urls import path
from .views import (
    ListingDetailView, ListingListView, ListingCreateView, ListingUpdateView, ListingDeleteView, UserListingsView
)

app_name = 'listings'

urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),
    path('anuncio/crear/', ListingCreateView.as_view(), name='listing_create'),
    path('anuncio/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('anuncio/<int:pk>/editar/', ListingUpdateView.as_view(), name='listing_update'),
    path('anuncio/<int:pk>/eliminar/', ListingDeleteView.as_view(), name='listing_delete'),
    path('usuario/<str:username>/', UserListingsView.as_view(), name='user_listings'),
]