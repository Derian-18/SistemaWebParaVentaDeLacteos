from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario_personalizado

admin.site.register(Usuario_personalizado, UserAdmin)