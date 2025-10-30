from django.urls import path
from .views import *

# Si quiero que se muestre primero una pagina como por ejemplo la principal
# Tengo que ponerla de primero en la urlpatterns

urlpatterns = [
    # Aqui va a ir la pagina sobre la tienda web
    path('', landingpage, name="landingpage"),
    
    # Esta es la pagina sobre nosotros los desarrolladores
    path('nosotros/', Nosotros, name='Nosotros'),
]   