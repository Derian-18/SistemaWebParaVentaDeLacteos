from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario_personalizado(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=50, choices=ROLES, default='cliente')