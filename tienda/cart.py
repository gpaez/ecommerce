from decimal import Decimal
from django.conf import settings
from tienda.models import Producto

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id not in self.cart:
            self.cart[producto_id] = {'cantidad': 0, 'precio': str(producto.precio)}
        self.cart[producto_id]['cantidad'] += cantidad
        self.save()

    def remove(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)

        for producto in productos:
            self.cart[str(producto.id)]['producto'] = producto

        for item in self.cart.values():
            item['precio'] = Decimal(item['precio'])
            item['total'] = item['precio'] * item['cantidad']
            yield item

    def get_total(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values())

    def __len__(self):
        return sum(item['cantidad'] for item in self.cart.values())
