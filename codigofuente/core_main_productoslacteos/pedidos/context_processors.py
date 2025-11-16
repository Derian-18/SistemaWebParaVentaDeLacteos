from .models import Carrito

def carrito_context(request):
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        items = carrito.items.all()
        total = carrito.total()
    else:
        items = []
        total = 0

    return {
        'carrito_items': items,
        'carrito_total': total,
    }
