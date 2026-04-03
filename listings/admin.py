# listings/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, ListingImage, Review

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1 # Cuántos campos de imagen extra mostrar

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'seller_type', 'listing_type', 'category', 'price', 'is_available', 'location')
    list_filter = ('seller_type', 'listing_type', 'category', 'is_available', 'fuel_type', 'transmission')
    search_fields = ('title', 'description', 'owner__username', 'location')
    inlines = [ListingImageInline]

    fieldsets = (
        (None, {
            'fields': ('owner', 'seller_type', 'title', 'description', 'price', 'location', 'is_available')
        }),
        ('Tipo de Anuncio', {
            'fields': ('listing_type', 'category')
        }),
        ('Características del Vehículo (si aplica)', {
            'classes': ('collapse',),
            'fields': ('year', 'seats', 'berths', 'mileage', 'fuel_type', 'transmission', 'length', 'weight')
        }),
        ('Equipamiento (si aplica)', {
            'classes': ('collapse',),
            'fields': ('has_bathroom', 'has_shower', 'has_kitchen', 'has_heating', 'has_air_conditioning', 'pets_allowed', 'has_solar_panels')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'author', 'rating', 'content_snippet', 'created_at', 'view_on_site')
    list_filter = ('rating', 'created_at')
    search_fields = ('content', 'listing__title', 'author__username')

    def content_snippet(self, obj):
        """Muestra un fragmento del texto para detectar spam o insultos sin entrar al detalle."""
        return obj.content[:70] + '...' if len(obj.content) > 70 else obj.content
    content_snippet.short_description = 'Contenido'

    def view_on_site(self, obj):
        """Proporciona un enlace directo para ver el anuncio en la parte pública y verificar el contexto."""
        url = obj.listing.get_absolute_url()
        return format_html('<a href="{}" target="_blank">Ver anuncio 🔗</a>', url)
    view_on_site.short_description = 'Enlace'

# Register your models here.
