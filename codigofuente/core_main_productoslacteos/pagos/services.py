class PagoService:

    def __init__(self, strategy):
        self.strategy = strategy

    def procesar(self, carrito, usuario, success_url, cancel_url):
        return self.strategy.procesar_pago(
            carrito, usuario, success_url, cancel_url
        )