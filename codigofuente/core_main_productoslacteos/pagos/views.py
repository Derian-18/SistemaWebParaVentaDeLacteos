from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pedidos.models import Carrito, Pedido, PedidoDetalle
from autenticacion.models import Usuario_personalizado
from pagos.services import PagoService
from pagos.estrategias.stripe_strategy import StripeStrategy
from pagos.estrategias.efectivo_strategy import EfectivoStrategy
from pagos.estrategias.paypal_strategy import PaypalStrategy 


@login_required
def crear_sesion_checkout(request):
    usuario = request.user
    carrito = Carrito.objects.get(usuario=usuario)

    metodo = request.POST.get("metodo_pago")

    estrategias = {
    "stripe": StripeStrategy,
    "efectivo": EfectivoStrategy,
    "paypal": PaypalStrategy
}

    strategy = estrategias[metodo]()
    servicio = PagoService(strategy)

    success_url = request.build_absolute_uri(reverse('pago_exitoso'))
    cancel_url = request.build_absolute_uri(reverse('pago_cancelado'))

    url = servicio.procesar(carrito, usuario, success_url, cancel_url)

    return redirect(url)


@login_required
def pago_exitoso(request):
    return render(request, 'pagos/exito.html')


@login_required
def pago_cancelado(request):
    return render(request, 'pagos/cancelado.html')


@csrf_exempt
def stripe_webhook(request):
    import stripe
    from django.conf import settings

    stripe.api_key = settings.STRIPE_SECRET_KEY

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

        pedido = Pedido.objects.create(
            usuario=usuario,
            total=sum(i.subtotal() for i in items),
            metodo_pago="stripe",
            estado="completado"
        )

        for item in items:
            PedidoDetalle.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_compra=item.producto.precio
            )

        items.delete()

    return HttpResponse(status=200)

# Este es el webhook para paypal, se que es mala practica pero es por el momento
@csrf_exempt
def paypal_webhook(request):
    import paypalrestsdk
    from django.conf import settings

    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    import json
    payload = json.loads(request.body)

    # Verificar que el evento es de un pago completado
    if payload.get("event_type") != "PAYMENT.SALE.COMPLETED":
        return HttpResponse(status=200)

    # PayPal manda el payer_id y el email del pagador
    payer_email = payload["resource"]["transaction_fee"].get("payer_email")
    usuario = Usuario_personalizado.objects.get(email=payer_email)
    carrito = Carrito.objects.get(usuario=usuario)
    items = carrito.items.all()

    pedido = Pedido.objects.create(
        usuario=usuario,
        total=sum(i.subtotal() for i in items),
        metodo_pago="paypal",
        estado="completado"
    )

    for item in items:
        PedidoDetalle.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_compra=item.producto.precio
        )

    items.delete()

    return HttpResponse(status=200)