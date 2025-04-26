from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class EstadoNegocio(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    completado = models.BooleanField(default=False)
    
    estado_negocio = models.ForeignKey(EstadoNegocio, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f'Pedido #{self.id} de {self.usuario.username}'
    
    @property
    def total(self):
        return sum(item.precio * item.cantidad for item in self.items.all())

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    
    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
    
class HistorialCambioEstado(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='historial_cambios')
    estado_anterior = models.ForeignKey('EstadoNegocio', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    estado_nuevo = models.ForeignKey('EstadoNegocio', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    tiempo_entre_estados = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f'Cambio de {self.estado_anterior} a {self.estado_nuevo} para Pedido #{self.pedido.id}'
