from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
    path('',views.bienvenida),
    path('login',views.login),
    path('logout',views.logout),
    path('agregarPacientes',views.agregarPacientes),
    path('bienvenida',views.bienvenida),
    url(r'crudPacientes$', views.crudPacientes, name='crudPacientes'),
    url(r'createPaciente$', views.createPaciente, name='createPaciente'),
    url(r'^edit/(?P<id>\d+)$', views.editPaciente, name='editPaciente'),
    url(r'^edit/update/(?P<id>\d+)$', views.updatePaciente, name='updatePaciente'),
    url(r'^delete/(?P<id>\d+)$', views.deletePaciente, name='deletePaciente'),

    url(r'crudTurnos$', views.crudTurnos, name='crudTurnos'),
    url(r'createTurno$', views.createTurno, name='createTurno'),
    url(r'^editturno/(?P<id>\d+)$', views.editTurnos, name='editTurnos'),
    url(r'^editturno/update/(?P<id>\d+)$', views.updateTurnos, name='updateTurnos'),
    url(r'^deleteturno/(?P<id>\d+)$', views.deleteTurnos, name='deleteTurnos'),
    url(r'crudMedicos$', views.crudMedicos, name='crudMedicos'),

    url(r'CrudHistorias$', views.crudHistorias, name='crudHistorias'),
    url(r'^edithistoria/(?P<id>\d+)$', views.editHistorias, name='editHistorias'),
    url(r'^edithistoria/update/(?P<id>\d+)$', views.updateHistorias, name='updateHistorias'),

    url(r'crudPedidos$', views.crudPedidos, name='crudPedidos'),
    url(r'createPedido$', views.createPedido, name='createPedido'),
    url(r'^editpedido/(?P<id>\d+)$', views.editPedido, name='editPedido'),
    url(r'^editpedido/update/(?P<id>\d+)$', views.updatePedido, name='updatePedido'),
    url(r'^deletepedido/(?P<id>\d+)$', views.deletePedido, name='deletePedido'),

    url(r'^editpedidoproducto/(?P<id>\d+)$', views.editPedidoProducto, name='editPedidoProducto'),
    url(r'updatePedidosProducto/(?P<id>\d+)$', views.updatePedidosProducto, name='updatePedidosProducto'),
    url(r'^editpedidoproducto/deletepedidoproducto/(?P<id>\d+)/(?P<id2>\d+)$', views.deletePedidoProducto, name='deletePedidoProducto'),

    url(r'^crudtaller$', views.crudTaller, name='crudTaller'),
    url(r'^finalizarTaller/(?P<id>\d+)$', views.finalizarTaller, name='finalizarTaller'),

    url(r'^asistenciaPacientes$', views.asistenciaPacientes, name='asistenciaPacientes'),
    url(r'^pedidosDePacientes$', views.pedidosDePacientes, name='pedidosDePacientes'),
    url(r'^productosmasvendidos$', views.productosmasvendidos, name='productosmasvendidos'),
    url(r'^vtastotalesxmesxvendedor$', views.vtastotalesxmesxvendedor, name='vtastotalesxmesxvendedor')
    
]
