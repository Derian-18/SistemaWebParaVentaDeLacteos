from pedidos.models import Pedido, PedidoDetalle
from pagos.estrategias.base import MetodoPagoStrategy

class EfectivoStrategy(MetodoPagoStrategy):

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

        return success_url