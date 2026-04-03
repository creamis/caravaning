from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    max_num = 5 # Límite de 5 imágenes

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} # Rellena automáticamente el slug

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'brand')
    search_fields = ('name', 'description', 'brand')
    prepopulated_fields = {'slug': ('name',)} # Rellena automáticamente el slug
    date_hierarchy = 'created_at' # Permite navegar por fecha de creación
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category', 'brand', 'description', 'price', 'affiliate_url', 'button_text', 'is_active')}),
        ('Fechas', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',) # created_at no debe ser editable