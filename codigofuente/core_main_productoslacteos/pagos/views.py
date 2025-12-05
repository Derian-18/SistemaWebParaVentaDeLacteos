import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render
from pedidos.models import Carrito, Pedido, PedidoDetalle
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from autenticacion.models import Usuario_personalizado

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def crear_sesion_checkout(request):
    usuario = request.user
    carrito = Carrito.objects.get(usuario=usuario)
    items_carrito = carrito.items.all()

    line_items = []
    for item in items_carrito:
        line_items.append({
            "price_data": {
                "currency": "mxn",
                "product_data": {
                    "name": item.producto.nombre,
                },
                "unit_amount": int(item.producto.precio * 100),  # MXN → centavos
            },
            "quantity": item.cantidad,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('pago_exitoso')),
        cancel_url=request.build_absolute_uri(reverse('pago_cancelado')),
        metadata={"usuario_id": usuario.id},
    )

    return redirect(session.url, code=303)

@login_required
def pago_exitoso(request):
    return render(request, 'pagos/exito.html')

@login_required
def pago_cancelado(request):
    return render(request, 'pagos/cancelado.html')

@login_required
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        usuario_id = session["metadata"]["usuario_id"]
        usuario = Usuario_personalizado.objects.get(id=usuario_id)

        carrito = Carrito.objects.get(usuario=usuario)
        items = carrito.items.all()

        # Crear pedido
        pedido = Pedido.objects.create(
            usuario=usuario,
            total=sum(i.subtotal() for i in items),
            metodo_pago="stripe",
            estado="completado"
        )

        # Crear detalles del pedido
        for item in items:
            PedidoDetalle.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_compra=item.producto.precio
            )

        # Vaciar carrito
        items.delete()

    return HttpResponse(status=200)