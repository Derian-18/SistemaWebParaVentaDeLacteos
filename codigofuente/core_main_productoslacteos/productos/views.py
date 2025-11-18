from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from django.contrib.auth.decorators import login_required
# Aqui importo el decorador de autenticacion para usar el solo admin
# Tambien le agrego el nombre admin para que sea mas corto de poner
from autenticacion.decorators import solo_admin as admin

#############################################
#
# CRUD CATEGORIA
#
#############################################

# Listar categorias
@login_required(login_url='login')
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})

# Crear categoria
@admin
@login_required(login_url='login')
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        return redirect('listar_categorias')

    return render(request, 'categorias/crear.html')

# Editar categoria
@admin
@login_required(login_url='login')
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        categoria.save()
        return redirect('listar_categorias')

    return render(request, 'categorias/editar.html', {'categoria': categoria})

# Eliminar categoria
@admin
@login_required(login_url='login')
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'categorias/eliminar.html', {'categoria': categoria})
#############################################
#
# CRUD PRODUCTOS 
#
#############################################

# Listar productos
@login_required(login_url='login')
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

# Crear producto
@admin
@login_required(login_url='login')
def crear_producto(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        stock = request.POST['stock']
        unidad_medida = request.POST['unidad_medida']
        categoria_id = request.POST['categoria']
        imagen = request.FILES.get('imagen')
        categoria = Categoria.objects.get(id=categoria_id)

        Producto.objects.create(
            nombre=nombre,
            precio=precio,
            stock=stock,
            unidad_medida=unidad_medida,
            categoria=categoria,
            imagen=imagen
        )
        return redirect('lista_productos')

    return render(request, 'productos/crear.html', {'categorias': categorias})

# Editar producto
@admin
@login_required(login_url='login')
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

# Eliminar producto
@admin
@login_required(login_url='login')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})