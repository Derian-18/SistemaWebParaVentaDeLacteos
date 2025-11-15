from django.shortcuts import redirect
from django.contrib import messages

def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión.")
            return redirect('login')

        if request.user.rol != 'admin':
            messages.error(request, "No tienes permisos para acceder aquí.")
            return redirect('landingpage')

        return view_func(request, *args, **kwargs)
    return wrapper
