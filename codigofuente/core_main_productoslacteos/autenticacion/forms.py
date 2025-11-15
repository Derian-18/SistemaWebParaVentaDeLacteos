# Aqui voy a agregar los formularios de registro y login

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario_personalizado

#Aqui ya creamos el formulario para el registro
class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario_personalizado
        fields = ['username', 'email', 'password1', 'password2']

# Y aqui se crea el formulario para el login
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))