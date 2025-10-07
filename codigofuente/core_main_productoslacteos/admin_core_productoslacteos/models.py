from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Aqui es donde creare las tablas de mi base de datos.

# No se ocupa crear esto importando la libreria User de Python
# Tabla Usuario (Python ya lo crea solo agrego datos que necesito)
# Aqui extiendo con AbstractUser los datos que yo necesito a User de Django
class Usuario_personalizado(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=50, choices=ROLES, default='cliente')

# Tabla Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

# Tabla Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
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
    # Agregar descripcion

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
    usuario = models.ForeignKey(Usuario_personalizado, on_delete=models.CASCADE)

# Tabla pedidos_detalle
class PedidoDetalle(models.Model):
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    # Esta es la relacion con la tabla Pedidos
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    # Esta es la relacion con la tabla Producto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)