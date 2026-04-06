from django.contrib import admin
from .models import Destination, DestinationImage

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 3

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'location', 'created_at')
    inlines = [DestinationImageInline]
