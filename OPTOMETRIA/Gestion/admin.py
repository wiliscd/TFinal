from django.contrib import admin

from .models import Pacientes
from .models import Turnos
from .models import Productos
from .models import PedidoProductos
from .models import DetallePedido

# Register your models here.

admin.site.register(Pacientes)
admin.site.register(Turnos)
admin.site.register(PedidoProductos)
admin.site.register(DetallePedido)
admin.site.register(Productos)