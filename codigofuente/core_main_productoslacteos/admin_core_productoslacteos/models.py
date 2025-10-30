from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Aqui es donde creare las tablas de mi base de datos.

# No se ocupa crear la tabla User importando la libreria User de Python
# Tabla Usuario (Python ya lo crea, solo agrego datos que necesito)
# Aqui extiendo con AbstractUser los datos que yo necesito a User de Django
class Usuario_personalizado(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=50, choices=ROLES, default='cliente')