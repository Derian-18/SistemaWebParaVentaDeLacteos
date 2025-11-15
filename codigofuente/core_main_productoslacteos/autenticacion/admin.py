from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario_personalizado

class UsuarioPersonalizadoAdmin(UserAdmin):
    model = Usuario_personalizado

    # Campos que aparecerán en el admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Rol del usuario', {'fields': ('rol',)}),
    )

    # Campos que salen al crear un usuario nuevo
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rol', 'is_staff', 'is_active')}
        ),
    )

    list_display = ['username', 'email', 'rol', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

admin.site.register(Usuario_personalizado, UsuarioPersonalizadoAdmin)
