from django.contrib import admin
from .models import Pedido, PedidoDetalle, Carrito, CarritoDetalle

# Register your models here.

admin.site.register(Pedido)
admin.site.register(PedidoDetalle)
admin.site.register(Carrito)
admin.site.register(CarritoDetalle)
