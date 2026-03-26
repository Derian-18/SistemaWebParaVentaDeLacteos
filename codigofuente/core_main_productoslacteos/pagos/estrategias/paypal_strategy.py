import paypalrestsdk
from django.conf import settings
from pagos.estrategias.base import MetodoPagoStrategy


class PaypalStrategy(MetodoPagoStrategy):

    def procesar_pago(self, carrito, usuario, success_url, cancel_url):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET,
        })

        items = carrito.items.all()

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": success_url,
                "cancel_url": cancel_url,
            },
            "transactions": [{
                "amount": {
                    "total": str(sum(i.subtotal() for i in items)),
                    "currency": "MXN",
                },
                "description": f"Pedido de {usuario.username}",
                "item_list": {
                    "items": [
                        {
                            "name": item.producto.nombre,
                            "quantity": str(item.cantidad),
                            "price": str(item.producto.precio),
                            "currency": "MXN",
                        }
                        for item in items
                    ]
                }
            }]
        })

        if not payment.create():
            raise ValueError(f"Error al crear pago en PayPal: {payment.error}")

        # Buscar la URL de aprobación para redirigir al usuario
        for link in payment.links:
            if link.rel == "approval_url":
                return link.href

        raise ValueError("No se encontró la URL de aprobación de PayPal")