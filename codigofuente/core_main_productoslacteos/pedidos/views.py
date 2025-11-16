from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Carrito, CarritoDetalle, Pedido, PedidoDetalle
from productos.models import Producto

# ============================
#   OBTENER O CREAR CARRITO
# ============================

def obtener_carrito(usuario):
    """Si el usuario no tiene carrito, se crea uno automáticamente."""
    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    return carrito


# ============================
#     AGREGAR AL CARRITO
# ============================

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito(request.user)

    # Crear o aumentar cantidad
    item, creado = CarritoDetalle.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )

    if not creado:
        item.cantidad += 1

    item.save()

    return redirect('lista_productos')   # importante: no usa sidebar_carrito


# ============================
#       VER CARRITO
# ============================

@login_required
def ver_carrito(request):
    carrito = obtener_carrito(request.user)
    items = carrito.items.all()
    total = carrito.total()

    return render(request, 'pedidos/ver_carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total
    })


# ============================
#   ACTUALIZAR CANTIDAD ITEM
# ============================

# Nota, aqui agregue dos metodos, peeeero, creo que no deberia ser asi por el manejo de recursos y codigo basura que se reutiliza
# Esta fue la mejor solucion que encontre para que se pudiera aumentar/disminuir la cantidad de items desde el sidebar
# ESTO ESTA MAL Y EN UN FUTURO SE DEBERIA ARREGLAR ESTA PARTE

@login_required
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(CarritoDetalle, id=item_id, carrito__usuario=request.user)

    accion = request.GET.get('accion',None)

    if accion == "sumar":
        item.cantidad += 1
        item.save()
    elif accion == "restar":
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

    return redirect('ver_carrito')


@login_required
def actualizar_cantidadsidebar(request, item_id):
    item = get_object_or_404(CarritoDetalle, id=item_id, carrito__usuario=request.user)

    accion = request.GET.get('accion',None)

    if accion == "sumar":
        item.cantidad += 1
        item.save()
    elif accion == "restar":
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

    return redirect('lista_productos')


# ============================
#    ELIMINAR PRODUCTO
# ============================

#NOTA: De igual manera que con el metodo actualizar item
# Arreglar despues

@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(CarritoDetalle, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect('ver_carrito')

@login_required
def eliminar_itemsidebar(request, item_id):
    item = get_object_or_404(CarritoDetalle, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect('lista_productos')


# ============================
#      VACIAR CARRITO
# ============================

@login_required
def vaciar_carrito(request):
    carrito = obtener_carrito(request.user)
    carrito.items.all().delete()
    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito = obtener_carrito(request.user)
    carrito.items.all().delete()
    return redirect('lista_productos')


######################
# PROCESAR PEDIDOS
#######################

@login_required
def procesar_pedido(request):
    usuario = request.user
    carrito = obtener_carrito(usuario)
    items = carrito.items.all()

    if not items:
        return redirect('ver_carrito')   # Si no hay items, no procesa

    # ==========================
    #   1. Crear el Pedido
    # ==========================
    pedido = Pedido.objects.create(
        usuario=usuario,
        total=carrito.total(),
        metodo_pago="pendiente",
        estado="pendiente"
    )

    # ==========================
    #   2. Crear PedidoDetalle
    # ==========================
    for item in items:
        PedidoDetalle.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_compra=item.producto.precio
        )

    # ==========================
    #   3. Vaciar el carrito
    # ==========================
    carrito.items.all().delete()

    # ==========================
    #   4. Redirigir
    # ==========================
    return redirect('pedido_completado', pedido_id=pedido.id)


#=====================
# PEDIDO COMPLETADO
#=====================
@login_required
def pedido_completado(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
    detalles = pedido.detalles.all()

    return render(request, 'pedidos/pedido_completado.html', {
        'pedido': pedido,
        'detalles': detalles
    })
