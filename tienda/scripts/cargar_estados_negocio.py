# tienda/scripts/cargar_estados_negocio.py

from tienda.models import EstadoNegocio
from django.db import connection

# Eliminar todos los estados anteriores
EstadoNegocio.objects.all().delete()

# Resetear la secuencia del ID
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='tienda_estadonegocio'")

# Volver a cargarlos
estados = ['Pendiente','Preparando', 'Pendiente de Entrega', 'Entregado']
for nombre in estados:
    EstadoNegocio.objects.create(nombre=nombre)

print("Estados de negocio recargados correctamente.")
