from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define un admin inline para el modelo Profile
# Esto permitirá editar el perfil desde la página de edición del usuario
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'perfil'
    fk_name = 'user'

# Extiende el UserAdmin por defecto para incluir el ProfileInline
class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Vuelve a registrar el modelo User con nuestro CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
