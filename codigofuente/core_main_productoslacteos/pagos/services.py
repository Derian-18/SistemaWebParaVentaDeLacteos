from pagos.estrategias.stripe_strategy import StripeStrategy
from pagos.estrategias.efectivo_strategy import EfectivoStrategy

class PagoService:

    def __init__(self, metodo_pago):
        if metodo_pago == "stripe":
            self.strategy = StripeStrategy()
        elif metodo_pago == "efectivo":
            self.strategy = EfectivoStrategy()
        else:
            raise ValueError("Método de pago no válido")

    def procesar(self, carrito, usuario, success_url, cancel_url):
        return self.strategy.procesar_pago(carrito, usuario, success_url, cancel_url)