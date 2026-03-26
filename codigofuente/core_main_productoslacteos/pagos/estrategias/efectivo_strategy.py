class EfectivoStrategy:

    def procesar_pago(self, carrito, usuario, success_url, cancel_url):
        # Aquí no hay redirección externa
        return success_url
    
from pedidos.models import Pedido, PedidoDetalle

class EfectivoStrategy:

    def procesar_pago(self, carrito, usuario, success_url, cancel_url):

        items = carrito.items.all()

        pedido = Pedido.objects.create(
            usuario=usuario,
            total=sum(i.subtotal() for i in items),
            metodo_pago="efectivo",
            estado="pendiente"
        )

        for item in items:
            PedidoDetalle.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_compra=item.producto.precio
            )

        #items.delete()

        return success_url