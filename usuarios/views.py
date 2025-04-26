from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistroForm
from django.contrib.auth.models import User

class RegistroUsuarioView(CreateView):
    model = User
    template_name = 'usuarios/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('login')

class LoginUsuarioView(LoginView):
    template_name = 'usuarios/login.html'

class LogoutUsuarioView(LogoutView):
    next_page = '/'
