from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Pedido, DetallePedido, Categoria, Producto, EstadoNegocio, HistorialCambioEstado
from .cart import Cart
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import CategoriaForm, ProductoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import TemplateView
from django.utils import timezone

from .mixins import SoloSuperuserMixin

def es_superusuario(user):
    return user.is_superuser

@login_required
@user_passes_test(es_superusuario)
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    estados = EstadoNegocio.objects.all()

    if request.method == 'POST':
        nuevo_estado_id = request.POST.get('estado_negocio')
        nuevo_estado = get_object_or_404(EstadoNegocio, id=nuevo_estado_id)

        estado_anterior = pedido.estado_negocio
        tiempo_diferencia = None

        if estado_anterior and pedido.actualizado:
            tiempo_diferencia = timezone.now() - pedido.actualizado

        # Guardar historial
        HistorialCambioEstado.objects.create(
            pedido=pedido,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=request.user,
            tiempo_entre_estados=tiempo_diferencia
        )

        # Actualizar el pedido
        pedido.estado_negocio = nuevo_estado
        pedido.save()

        return redirect('admin_lista_pedidos')

    return render(request, 'tienda/pedido/cambiar_estado.html', {
        'pedido': pedido,
        'estados': estados,
    })


@login_required
def agregar_al_carrito(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    cart.add(producto)
    return redirect('ver_carrito')
    
@login_required
def eliminar_del_carrito(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    cart.remove(producto)
    return redirect('ver_carrito')
    
@login_required
def vaciar_carrito(request):
    cart = Cart(request)
    cart.clear()
    return redirect('ver_carrito')
    
@login_required
def ver_carrito(request):
    cart = Cart(request)
    return render(request, 'tienda/carrito.html', {'cart': cart})

@login_required
def realizar_pedido(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('ver_carrito')
    
        # Obtener estado inicial del negocio ("Preparando")
    estado_pendiente = EstadoNegocio.objects.filter(nombre__iexact='Pendiente').first()

    pedido = Pedido.objects.create(usuario=request.user, completado=True, estado_negocio=estado_pendiente)

    for item in cart:
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item['producto'],
            precio=item['precio'],
            cantidad=item['cantidad']
        )

    cart.clear()
    return render(request, 'tienda/pedido_realizado.html', {'pedido': pedido})

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'tienda/historial_pedidos.html'

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by('-creado')

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'tienda/detalle_pedido.html'

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)
    
class InicioView(ListView):
    model = Producto
    template_name = 'tienda/inicio.html'
    context_object_name = 'productos'
  
# --- Inicio de vistas administrativas --- #    
# --- CATEGORÍAS ---
class CategoriaListView(LoginRequiredMixin, SoloSuperuserMixin, ListView):
    model = Categoria
    template_name = 'tienda/categorias/listar.html'

class CategoriaCreateView(LoginRequiredMixin, SoloSuperuserMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'tienda/categorias/formulario.html'
    success_url = reverse_lazy('listar_categorias')

class CategoriaUpdateView(LoginRequiredMixin, SoloSuperuserMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'tienda/categorias/formulario.html'
    success_url = reverse_lazy('listar_categorias')

class CategoriaDeleteView(LoginRequiredMixin, SoloSuperuserMixin, DeleteView):
    model = Categoria
    template_name = 'tienda/categorias/eliminar.html'
    success_url = reverse_lazy('listar_categorias')

# --- PRODUCTOS ---
class ProductoListView(LoginRequiredMixin, SoloSuperuserMixin, ListView):
    model = Producto
    template_name = 'tienda/productos/listar.html'

class ProductoCreateView(LoginRequiredMixin, SoloSuperuserMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/productos/formulario.html'
    success_url = reverse_lazy('listar_productos')

class ProductoUpdateView(LoginRequiredMixin, SoloSuperuserMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/productos/formulario.html'
    success_url = reverse_lazy('listar_productos')

class ProductoDeleteView(LoginRequiredMixin, SoloSuperuserMixin, DeleteView):
    model = Producto
    template_name = 'tienda/productos/eliminar.html'
    success_url = reverse_lazy('listar_productos')
    
class DashboardView(LoginRequiredMixin, SoloSuperuserMixin, TemplateView):
    template_name = 'tienda/dashboard.html'
    
class PedidoAdminListView(LoginRequiredMixin, SoloSuperuserMixin, ListView):
    model = Pedido
    template_name = 'tienda/pedido/listado.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        return Pedido.objects.filter(completado=True).order_by('-creado')


class PedidoAdminUpdateView(LoginRequiredMixin, SoloSuperuserMixin, UpdateView):
    model = Pedido
    fields = ['estado_negocio']
    template_name = 'tienda/pedido/editar.html'
    success_url = reverse_lazy('admin_listado_pedidos')
    
    def form_valid(self, form):
        # Guarda el historial de cambio de estado
        pedido = form.save(commit=False)
        estado_anterior = pedido.estado_negocio
        nuevo_estado = form.cleaned_data['estado_negocio']
        tiempo_diferencia = None

        # Calcular tiempo entre cambios de estado
        if estado_anterior and pedido.actualizado:
            tiempo_diferencia = timezone.now() - pedido.actualizado

        # Registrar en el historial de cambios
        HistorialCambioEstado.objects.create(
            pedido=pedido,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=self.request.user,
            tiempo_entre_estados=tiempo_diferencia
        )

        # Guardar el pedido
        pedido.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = EstadoNegocio.objects.all()
        context['pedido'] = self.object  # asegurarse que esté disponible en el template
        context['historial'] = self.object.historial_cambios.all().order_by('-fecha_cambio')
        return context