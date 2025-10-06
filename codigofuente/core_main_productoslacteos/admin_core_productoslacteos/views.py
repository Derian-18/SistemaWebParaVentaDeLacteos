from django.shortcuts import render

# Aqui iran todas mis vistas

# Esta es la landing pague del proyecto de productos lacteos
def home(request):
    return render(request, 'landing_page.html')


def landing_pague(request):
    return render(request, 'base.html')