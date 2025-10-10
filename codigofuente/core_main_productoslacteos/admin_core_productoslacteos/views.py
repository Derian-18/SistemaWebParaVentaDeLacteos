from django.shortcuts import render

# Aqui iran todas mis vistas

# Esta es la landing pague del proyecto de productos lacteos
def landingpage(request):
    return render(request, 'landing_page.html')


def Nosotros(request):
    return render(request, 'Nosotros.html')