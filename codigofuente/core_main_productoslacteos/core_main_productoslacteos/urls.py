"""
URL configuration for core_main_productoslacteos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Esta es la pagina del admin
    path('admin/', admin.site.urls),

    # Esta pagina es la de inicio que es donde esta el landing page y la pagina sobre nosotros
    path('', include('admin_core_productoslacteos.urls')),

    # Aqui estan los productos
    path('productos/', include('productos.urls')), # Aqui conectamos la app de productos
    
    # Aqui esta la autenticacion para poder ingresar a los productos
    path('autenticacion/', include('autenticacion.urls')),
]
