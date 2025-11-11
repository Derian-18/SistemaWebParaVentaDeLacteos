from django.db import models

# Importamos las demas tablas necesarias de las otras Apps 
from autenticacion.models import Usuario_personalizado
from productos.models import Producto

# Create your models here.

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
    # Aqui podemos agregar mas campos relacionados con el pago para que el usuario pueda elegir
    # cual usara al momento de pagar
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
