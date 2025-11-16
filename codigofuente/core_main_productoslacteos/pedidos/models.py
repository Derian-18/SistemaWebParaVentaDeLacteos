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

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"


# Tabla pedidos_detalle
class PedidoDetalle(models.Model):
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    # Esta es la relacion con la tabla Pedidos
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    # Esta es la relacion con la tabla Producto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def subtotal(self):
        return self.precio_compra * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido #{self.pedido.id})"


# Crear nuevos modelos
# Carrito y carrito detalle
class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario_personalizado, on_delete=models.CASCADE)

    def total(self):
        """Retorna el total del carrito sumando subtotales de cada item."""
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class CarritoDetalle(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
