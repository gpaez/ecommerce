from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('pedido/realizar/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido/historial/', views.PedidoListView.as_view(), name='historial_pedidos'),
    path('pedido/<int:pk>/', views.PedidoDetailView.as_view(), name='detalle_pedido'),
    path('', views.InicioView.as_view(), name='inicio'),
    
    path('admin/dashboard/', views.DashboardView.as_view(), name='admin_dashboard'),
    
    # Categorías
    path('admin/categorias/', views.CategoriaListView.as_view(), name='listar_categorias'),
    path('admin/categorias/nueva/', views.CategoriaCreateView.as_view(), name='crear_categoria'),
    path('admin/categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('admin/categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='eliminar_categoria'),

    # Productos
    path('admin/productos/', views.ProductoListView.as_view(), name='listar_productos'),
    path('admin/productos/nuevo/', views.ProductoCreateView.as_view(), name='crear_producto'),
    path('admin/productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='editar_producto'),
    path('admin/productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='eliminar_producto'),
    
    # Pedidos
    path('admin/pedidos/', views.PedidoAdminListView.as_view(), name='admin_listado_pedidos'),
    path('admin/pedidos/<int:pk>/editar/', views.PedidoAdminUpdateView.as_view(), name='admin_editar_pedido'),


]
