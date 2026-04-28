# blog/admin.py
from django.contrib import admin
from .models import Post, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3  # Muestra 3 espacios vacíos para nuevas fotos

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'reading_time')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)} # Autocompleta el slug
    inlines = [PostImageInline]
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author', 'content', 'status')}),
        ('SEO', {'fields': ('meta_description',), 'classes': ('collapse',)}),
    )


# Register your models here.
