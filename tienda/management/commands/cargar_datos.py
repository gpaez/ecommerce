from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto
from django.core.files.base import ContentFile
import requests

class Command(BaseCommand):
    help = 'Carga categorías y productos de ejemplo con imágenes desde la web'

    def handle(self, *args, **kwargs):
        # Eliminar datos anteriores
        Producto.objects.all().delete()
        Categoria.objects.all().delete()
        self.stdout.write(self.style.WARNING("🗑️ Categorías y productos anteriores eliminados."))

        # Datos de ejemplo
        categorias_data = [
            {"nombre": "Electrónica", "descripcion": "Productos electrónicos como celulares, tablets, laptops y accesorios."},
            {"nombre": "Hogar y Cocina", "descripcion": "Utensilios, electrodomésticos y artículos para el hogar."},
            {"nombre": "Ropa", "descripcion": "Ropa para hombres, mujeres y niños."},
            {"nombre": "Juguetes", "descripcion": "Juegos y juguetes para niños de todas las edades."},
            {"nombre": "Belleza", "descripcion": "Cosméticos, maquillaje y productos de cuidado personal."},
            {"nombre": "Deportes", "descripcion": "Artículos para entrenamiento, running, fútbol, etc."},
            {"nombre": "Oficina", "descripcion": "Material de oficina, escritorios, sillas y accesorios."},
            {"nombre": "Mascotas", "descripcion": "Comida, juguetes y accesorios para perros, gatos y otras mascotas."},
            {"nombre": "Herramientas", "descripcion": "Herramientas manuales y eléctricas para bricolaje o profesionales."},
            {"nombre": "Libros", "descripcion": "Libros de ficción, no ficción, educativos y más."},
        ]

        productos_data = [
            {
                "nombre": "Smartphone Galaxy S23",
                "descripcion": "Celular Samsung con pantalla AMOLED y 128 GB de almacenamiento.",
                "precio": 3500000,
                "categoria": "Electrónica",
                "imagen_url": "https://images.unsplash.com/photo-1611078489935-bc49c8fcdb82"
            },
            {
                "nombre": "Licuadora Oster",
                "descripcion": "Licuadora de alta potencia ideal para batidos y jugos naturales.",
                "precio": 480000,
                "categoria": "Hogar y Cocina",
                "imagen_url": "https://images.unsplash.com/photo-1590080876063-4be4a4f0c835"
            },
            {
                "nombre": "Remera básica blanca",
                "descripcion": "Remera de algodón para uso diario, unisex.",
                "precio": 75000,
                "categoria": "Ropa",
                "imagen_url": "https://images.unsplash.com/photo-1584467735871-b36dc8462254"
            },
            {
                "nombre": "Muñeca Barbie Fashionista",
                "descripcion": "Muñeca Barbie con ropa moderna y accesorios incluidos.",
                "precio": 190000,
                "categoria": "Juguetes",
                "imagen_url": "https://images.pexels.com/photos/3661192/pexels-photo-3661192.jpeg"
            },
            {
                "nombre": "Set de maquillaje Maybelline",
                "descripcion": "Base, rubor y máscara de pestañas en un solo combo.",
                "precio": 230000,
                "categoria": "Belleza",
                "imagen_url": "https://images.unsplash.com/photo-1581089781785-603411fa81b7"
            },
            {
                "nombre": "Pelota de fútbol Adidas",
                "descripcion": "Pelota de fútbol oficial tamaño 5 para entrenamientos y partidos.",
                "precio": 160000,
                "categoria": "Deportes",
                "imagen_url": "https://images.unsplash.com/photo-1612361127355-2a1bccc1f9e9"
            },
            {
                "nombre": "Silla ergonómica negra",
                "descripcion": "Silla de oficina con soporte lumbar y ajuste de altura.",
                "precio": 850000,
                "categoria": "Oficina",
                "imagen_url": "https://images.unsplash.com/photo-1626882048554-84cfb169b469"
            },
            {
                "nombre": "Comida para gato Whiskas",
                "descripcion": "Alimento completo para gatos adultos sabor carne.",
                "precio": 60000,
                "categoria": "Mascotas",
                "imagen_url": "https://images.pexels.com/photos/10537680/pexels-photo-10537680.jpeg"
            },
            {
                "nombre": "Taladro Black & Decker",
                "descripcion": "Taladro inalámbrico recargable con batería de litio.",
                "precio": 590000,
                "categoria": "Herramientas",
                "imagen_url": "https://images.unsplash.com/photo-1571055107551-3e67626c8364"
            },
            {
                "nombre": "Libro: Cien Años de Soledad",
                "descripcion": "Novela clásica de Gabriel García Márquez.",
                "precio": 95000,
                "categoria": "Libros",
                "imagen_url": "https://images.pexels.com/photos/4528938/pexels-photo-4528938.jpeg"
            },
        ]

        # Crear categorías
        categoria_objs = {}
        for data in categorias_data:
            cat, _ = Categoria.objects.get_or_create(nombre=data['nombre'], defaults={"descripcion": data['descripcion']})
            categoria_objs[data['nombre']] = cat
            self.stdout.write(self.style.SUCCESS(f"✔️ Categoría creada: {cat.nombre}"))

        # Crear productos
        for prod in productos_data:
            categoria = categoria_objs.get(prod["categoria"])
            producto = Producto(
                nombre=prod["nombre"],
                descripcion=prod["descripcion"],
                precio=prod["precio"],
                categoria=categoria,
                stock=10
            )

            try:
                response = requests.get(prod["imagen_url"])
                if response.status_code == 200:
                    producto.imagen.save(
                        prod["nombre"].replace(" ", "_") + ".jpg",
                        ContentFile(response.content),
                        save=True
                    )
                else:
                    producto.save()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Imagen no cargada para {prod['nombre']}: {e}"))
                producto.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Producto creado: {producto.nombre}"))
