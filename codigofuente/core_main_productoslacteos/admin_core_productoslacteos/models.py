from django.db import models
from django.contrib.auth.models import AbstractUser

# Aqui es donde creare las tablas de mi base de datos.

# Tabla Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ROLES = (
        ('admin', 'Admin'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=50, choices=ROLES, default='cliente')
    fecha_registro = models.DateTimeField(auto_now_add=True)

# Tabla Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

# Tabla Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    unidad_medida = models.CharField(max_length=50)
    # Esta es la relacion con la tabla Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

# Tabla Pedidos
class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    ESTADO = (
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    estado = models.CharField(max_length=50, choices=ESTADO, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    # Esta es la relacion con la tabla Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

# Tabla pedidos_detalle
class PedidoDetalle(models.Model):
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    # Esta es la relacion con la tabla Pedidos
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    # Esta es la relacion con la tabla Producto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)