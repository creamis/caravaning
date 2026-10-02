from django.urls import path
from .views import ProductListView, ProductPreviewView

app_name = 'shop'

urlpatterns = [
    path(
        'preview/',
        ProductPreviewView.as_view(),
        name='product_preview'
    ),
    path('', ProductListView.as_view(), name='product_list'),
]