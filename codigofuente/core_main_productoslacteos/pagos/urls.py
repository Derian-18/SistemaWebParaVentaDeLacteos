from django.urls import path
from .views import crear_sesion_checkout, pago_exitoso, pago_cancelado, stripe_webhook, paypal_webhook

urlpatterns = [
    path('crear-checkout/', crear_sesion_checkout, name='crear_checkout'),
    path('exito/', pago_exitoso, name='pago_exitoso'),
    path('cancelado/', pago_cancelado, name='pago_cancelado'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path("paypal/webhook/", paypal_webhook, name="paypal_webhook"),
]
