from django.views.generic import ListView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Mostramos solo los productos marcados como activos, ordenados por fecha
        return Product.objects.filter(is_active=True).prefetch_related('images').order_by('-created_at')
