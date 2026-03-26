from abc import ABC, abstractmethod

class MetodoPagoStrategy(ABC):

    @abstractmethod
    def procesar_pago(self, carrito, usuario, success_url, cancel_url):
        pass