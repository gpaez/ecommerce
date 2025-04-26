from django.contrib import admin
from .models import Categoria, Producto, Pedido, DetallePedido

class ItemPedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'precio', 'cantidad')
    can_delete = False

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'creado', 'actualizado', 'completado', 'total')
    list_filter = ('completado', 'creado')
    search_fields = ('usuario__username',)
    readonly_fields = ('creado', 'actualizado')
    inlines = [ItemPedidoInline]

    def total(self, obj):
        return obj.total

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido, PedidoAdmin)
