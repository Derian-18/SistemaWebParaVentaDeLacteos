from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from django.contrib.auth.decorators import login_required

# Listar productos
@login_required(login_url='login')
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

@login_required(login_url='login')
# Crear producto
def crear_producto(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        stock = request.POST['stock']
        unidad_medida = request.POST['unidad_medida']
        categoria_id = request.POST['categoria']
        categoria = Categoria.objects.get(id=categoria_id)

        Producto.objects.create(
            nombre=nombre,
            precio=precio,
            stock=stock,
            unidad_medida=unidad_medida,
            categoria=categoria
        )
        return redirect('lista_productos')

    return render(request, 'productos/crear.html', {'categorias': categorias})

@login_required(login_url='login')
# Editar producto
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.unidad_medida = request.POST['unidad_medida']
        producto.categoria = Categoria.objects.get(id=request.POST['categoria'])
        producto.save()
        return redirect('lista_productos')

    return render(request, 'productos/editar.html', {
        'producto': producto,
        'categorias': categorias
    })

@login_required(login_url='login')
# Eliminar producto
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})
