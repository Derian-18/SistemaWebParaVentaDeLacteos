import stripe
from django.conf import settings
from pagos.estrategias.base import MetodoPagoStrategy


class StripeStrategy(MetodoPagoStrategy):

    def procesar_pago(self, carrito, usuario, success_url, cancel_url):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if not carrito.items.exists():
            raise ValueError("El carrito está vacío")

        line_items = []
        for item in carrito.items.all():
            line_items.append({
                "price_data": {
                    "currency": "mxn",
                    "product_data": {
                        "name": item.producto.nombre,
                    },
                    "unit_amount": int(item.producto.precio * 100),
                },
                "quantity": item.cantidad,
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"usuario_id": usuario.id},
        )

        return session.url