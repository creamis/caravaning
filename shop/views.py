from django.views.generic import ListView
from django.db.models import Q
from .models import Category, Product

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Mostramos solo los productos marcados como activos, ordenados por fecha.
        queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')

        self.search_query = self.request.GET.get('q', '').strip()
        self.category_slug = self.request.GET.get('category', '').strip()
        self.merchant_name = self.request.GET.get('merchant', '').strip()

        if self.search_query:
            queryset = queryset.filter(
                Q(name__icontains=self.search_query)
                | Q(description__icontains=self.search_query)
                | Q(brand__icontains=self.search_query)
                | Q(merchant_name__icontains=self.search_query)
                | Q(recommendation_reason__icontains=self.search_query)
                | Q(best_for__icontains=self.search_query)
                | Q(category__name__icontains=self.search_query)
            )

        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)

        if self.merchant_name:
            queryset = queryset.filter(merchant_name__iexact=self.merchant_name)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(products__is_active=True).distinct().order_by('name')
        context['merchants'] = (
            Product.objects.filter(is_active=True)
            .exclude(merchant_name='')
            .values_list('merchant_name', flat=True)
            .distinct()
            .order_by('merchant_name')
        )
        context['search_query'] = self.search_query
        context['active_category_slug'] = self.category_slug
        context['active_merchant_name'] = self.merchant_name
        return context


from django.contrib.auth.mixins import UserPassesTestMixin


class ProductPreviewView(UserPassesTestMixin, ProductListView):
    """Vista privada de productos en revisión."""

    raise_exception = True

    def test_func(self):
        usuario = self.request.user
        return usuario.is_authenticated and usuario.is_staff

    def get_queryset(self):
        # Inicializa los filtros que utiliza la plantilla.
        self.search_query = ""
        self.category_slug = ""
        self.merchant_name = ""

        return (
            Product.objects
            .filter(pk__in=[1, 2, 3, 4, 5, 6, 7, 18, 19, 20], is_active=False)
            .select_related("category")
            .prefetch_related("images")
            .order_by("pk")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filtros correspondientes a los borradores de la vista previa.
        borradores = Product.objects.filter(
            pk__in=[1, 2, 3, 4, 5, 6, 7, 18, 19, 20],
            is_active=False
        )

        context["categories"] = (
            Category.objects
            .filter(products__in=borradores)
            .distinct()
            .order_by("name")
        )

        context["merchants"] = (
            borradores
            .exclude(merchant_name="")
            .values_list("merchant_name", flat=True)
            .distinct()
            .order_by("merchant_name")
        )

        context["is_preview"] = True
        return context
