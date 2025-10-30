from django.db import models

# Create your models here.

# Tabla Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

# Tabla Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    # Modificar aqui, el precio puede ser negativoy no es asi
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    UNIDAD_MEDIDA = (
        ('kg', 'Kg'),
        ('g', 'G'),
        ('l', 'L'),
        ('ml', 'Ml'),
    )
    unidad_medida = models.CharField(max_length=50, choices=UNIDAD_MEDIDA)
    # Esta es la relacion con la tabla Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)