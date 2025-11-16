from django.urls import path
from . import views

urlpatterns = [
    # Ver carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),

    # Agregar producto al carrito
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),

    # Actualizar cantidad
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),

    path('carrito/actualizarsidebar/<int:item_id>/', views.actualizar_cantidadsidebar, name='actualizar_cantidadsidebar'),

    # Eliminar item del carrito
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),

    path('carrito/eliminarsidebar/<int:item_id>/', views.eliminar_itemsidebar, name='eliminar_itemsidebar'),

    # Vaciar carrito
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),

    path('carrito/procesar/', views.procesar_pedido, name='procesar_pedido'),
    
    path('pedido/completado/<int:pedido_id>/', views.pedido_completado, name='pedido_completado'),

]
