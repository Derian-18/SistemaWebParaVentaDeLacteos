from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pedidos.models import Carrito, Pedido, PedidoDetalle
from autenticacion.models import Usuario_personalizado
from pagos.services import PagoService



@login_required
def crear_sesion_checkout(request):
    usuario = request.user
    carrito = Carrito.objects.get(usuario=usuario)

    metodo = request.POST.get("metodo_pago")  # stripe / efectivo

    success_url = request.build_absolute_uri(reverse('pago_exitoso'))
    cancel_url = request.build_absolute_uri(reverse('pago_cancelado'))

    servicio = PagoService(metodo)
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