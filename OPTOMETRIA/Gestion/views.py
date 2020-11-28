from collections import UserList
from django.db.models.aggregates import Count,Sum
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.models import User,Group, models
from .models import Pacientes
from .models import Turnos
from .models import Medicos
from .models import PedidoProductos
from .models import DetallePedido
from .models import Productos
from datetime import datetime, date, time, timedelta
from django.db import connection

from .forms import regPaciente
from django.http import HttpResponseRedirect

# Create your views here.
#def index(request):
#    return HttpResponse("Pagina de Inicio Optometria")
#---------Esto es del proceso de login---------------------
def bienvenida(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Secretaria').exists():
            rol="SECRETARIA"
        elif request.user.groups.filter(name='Medicos').exists():
            rol="MEDICOS"
        elif request.user.groups.filter(name='Ventas').exists():
            rol="VENTAS"
        elif request.user.groups.filter(name='Gerencia').exists():
            rol="GERENCIA"
        else:
            rol="TALLER"

        return render(request, "Gestion/bienvenida.html",{'quegrupo':rol})
    return render(request,"Gestion/login.html")

def login(request):
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                do_login(request,user)
                return redirect('/Gestion')
    return render(request,"Gestion/login.html",{'form': form})

def logout(request):
    do_logout(request)
    return render(request,"Gestion/login.html")
#----------Fin de esto es del login-------------------


#Borrar, lo uso en el login para saber la sesion del current user
def elRol(request):
        elgrupo=request.user.groups.all()
        return  render(request, "Gestion/bienvenida.html",{'quegrupo':elgrupo})
#Borrar, lo uso en el login para saber la sesion del current user

def agregarPacientes(request):
    form=regPaciente(request.POST)
    if form.is_valid():
        form_data=form.cleaned_data
        ape=form_data.get("apellidos")
        nom=form_data.get("nombres")
        obj=Pacientes.objects.create(apellidos=ape,nombres=nom)
        return HttpResponseRedirect(request.path)
    return render(request,"Gestion/agregar.html",{"regPac":form})


#Para los pacientes
def crudPacientes(request):
    Pacientex = Pacientes.objects.all()
    context = {'members': Pacientex}
    return render(request, 'Gestion/index.html', context)

def createPaciente(request):
    nomb=request.POST.get('nombre')
    apel=request.POST.get('apellido')
    Pacientex = Pacientes(nombres=nomb, apellidos=apel)
    Pacientex.save()
    Pacientex1 = Pacientes.objects.all()
    context = {'members': Pacientex1}
    return render(request, 'Gestion/index.html', context)

def editPaciente(request, id):
    Pacientex = Pacientes.objects.get(id=id)
    context = {'members': Pacientex}
    return render(request, 'Gestion/edit.html', context)

def updatePaciente(request, id):
    Pacientex = Pacientes.objects.get(id=id)
    Pacientex.nombres = request.POST['firstname']
    Pacientex.apellidos = request.POST['lastname']
    Pacientex.save()
    return redirect('/Gestion/crudPacientes')

def deletePaciente(request, id):
    Pacientex = Pacientes.objects.get(id=id)
    Pacientex.delete()
    return redirect('/Gestion/crudPacientes')
#Para los pacientes

#Medicos
def crudMedicos(request):
    medicosxx = Medicos.objects.all()
    context = {'medicos': medicosxx}
    return render(request, 'Gestion/2_A_index_turno.html', context)
#Medicos

#Para los turnos
def crudTurnos(request):
    Turnox = Turnos.objects.all()    
    medicosxx = User.objects.filter(groups__name='Medicos')
    Pacientex = Pacientes.objects.all()
    return render(request, 'Gestion/2_A_index_turno.html', {'turnos': Turnox,'medicos': medicosxx,'members': Pacientex})

def createTurno(request):
    i=0
    ban=0
    txt=len(str(request.POST.get('paciente')))
    codigo=""
    while i<txt and ban==0:
        if str(request.POST.get('paciente'))[i]=="-":
            ban=1
        else:
            codigo=codigo+str(request.POST.get('paciente'))[i]
        i=i+1
    i=0
    ban=0
    txt=len(str(request.POST.get('medico')))
    codigom=""
    while i<txt and ban==0:
        if str(request.POST.get('medico'))[i]=="-":
            ban=1
        else:
            codigom=codigom+str(request.POST.get('medico'))[i]
        i=i+1
    tipo = Pacientes.objects.get(pk =codigo)
    tipo2 = User.objects.get(pk=codigom)
    
    fecha_hora1=request.POST.get('fecha_hora')
    Turnox3 = Turnos(id_paciente=tipo, id_medico=tipo2,fecha_hora=fecha_hora1,Estado="NOPRESENTE")
    Turnox3.save()
    Turnox = Turnos.objects.all()
    medicosxx = User.objects.filter(groups__name='Medicos')
    Pacientex = Pacientes.objects.all()
    return render(request, 'Gestion/2_A_index_turno.html', {'turnos': Turnox,'medicos': medicosxx,'members': Pacientex})


def editTurnos(request,id):
    #print(med)
    Turnox2 = Turnos.objects.get(id=id)
    Turnox = Turnos.objects.all()
    medicosxx=User.objects.filter(groups__name='Medicos')
    Pacientex = Pacientes.objects.all()
    return render(request, 'Gestion/2_B_edit-turno.html', {'turnos': Turnox,
        'medicos': medicosxx,'members': Pacientex,'elturno':Turnox2})

def updateTurnos(request, id):
    Turnos3 = Turnos.objects.get(id=id)
    i=0
    pacien=str(request.POST.get('paciente'))
    ban=0
    txt=len(str(request.POST.get('paciente')))
    codigo=""
    while i<txt and ban==0:
        if str(request.POST.get('paciente'))[i]=="-":
            ban=1
        else:
            codigo=codigo+str(request.POST.get('paciente'))[i]
        i=i+1
    i=0
    ban=0
    txt=len(str(request.POST.get('medix')))
    medi=str(request.POST.get('medix'))
    codigom=""
    while i<txt and ban==0:
        if str(request.POST.get('medix'))[i]=="-":
            ban=1
        else:
            codigom=codigom+str(request.POST.get('medix'))[i]
        i=i+1
    tipo = Pacientes.objects.get(pk=codigo)
    tipo2 = User.objects.get(pk=codigom)

    Turnos3.id_paciente = tipo
    Turnos3.id_medico = tipo2
    Turnos3.fecha_hora = request.POST['fecha_hora']
    Turnos3.save()
    return redirect('/Gestion/crudTurnos')

def deleteTurnos(request, id):
    Turnoxc =Turnos.objects.get(id=id)
    Turnoxc.delete()
    return redirect('/Gestion/crudTurnos')
#Para los turnos

#Modulo de medicos, la historia clinicay demas yerbas
def crudHistorias(request):  
    Turnox = Turnos.objects.filter(id_medico_id=request.user.id)
    if request.method=="POST":
        desde=request.POST.get('desde')
        hasta=request.POST.get('hasta')
        estado=request.POST.get('estado')
        Turnoxpost = Turnos.objects.filter(fecha_hora__range=(desde,hasta),Estado=estado,id_medico_id=request.user.id)
        return render(request, 'Gestion/3_A_index_historia.html', {'usuarios': Turnoxpost})
    return render(request, 'Gestion/3_A_index_historia.html', {'usuarios': Turnox})


def editHistorias(request, id):
    Turnox2 = Turnos.objects.get(id=id)
    Turnox = Turnos.objects.all()
    Pacientex = Pacientes.objects.all()
    return render(request, 'Gestion/3_B_edit-historia.html', {'turnos': Turnox,
       'members': Pacientex,'elturno':Turnox2})

def updateHistorias(request, id):
    Turnos3 = Turnos.objects.get(id=id)
    Turnos3.descrip = request.POST['descrip']
    Turnos3.Estado = request.POST['estado']
    Turnos3.save()
    return redirect('/Gestion/CrudHistorias')
#Modulo de medicos, la historia clinicay demas yerbas

#Parte de los vendedores
def crudPedidos(request):
    Pedidosx=PedidoProductos.objects.all()
    Pacientesxx=Pacientes.objects.all()
    Pacientex = Pacientes.objects.all()
    return render(request, 'Gestion/4_A_index_ventas.html', {'pedidos': Pedidosx,'members': Pacientesxx})

def createPedido(request):
    i=0
    ban=0
    txt=len(str(request.POST.get('paciente')))
    codigo=""
    while i<txt and ban==0:
        if str(request.POST.get('paciente'))[i]=="-":
            ban=1
        else:
            codigo=codigo+str(request.POST.get('paciente'))[i]
        i=i+1
    vende=User.objects.get(pk=request.user.id)
    tipo = Pacientes.objects.get(pk=codigo)
    Pedidex=PedidoProductos(id_paciente=tipo,id_vendedor=vende,descrip="",estado="PENDIENTE",pago=request.POST.get('formapago'),total=0,fecha=datetime.now())
    Pedidex.save()
    Pedidosz = PedidoProductos.objects.all()
    Pacientex = Pacientes.objects.all()
    return render(request, 'Gestion/4_A_index_ventas.html', {'pedidos': Pedidosz,'members': Pacientex})


def editPedido(request, id):
    elpedidex=PedidoProductos.objects.get(id=id)
    return render(request, 'Gestion/4_B_edit-ventas.html', {'pedidos':elpedidex})#, {'listapa':pacientes})


def editPedidoProducto(request, id):
    listaproductos = Productos.objects.all()
    elpedidox=PedidoProductos.objects.get(id=id)
    detallep=DetallePedido.objects.filter(id_pedido_id=elpedidox.id)
    return render(request, 'Gestion/4_C_edit-ventas.html', {'productos': listaproductos,'idped':id,'pedidos':detallep,'datospedido':elpedidox})#,
    


def updatePedido(request, id):
    elpedidex=PedidoProductos.objects.get(id=id)
    #elpedidex.fecha=request.POST.get('fecha')
    if request.POST.get('Estado')is not None:
        elpedidex.estado=request.POST.get('Estado')
    elpedidex.pago=request.POST.get('formapago')
    if request.method=="POST":        
        elpedidex.save()
    return redirect('/Gestion/crudPedidos')


def updatePedidosProducto(request, id):
    #aca busco el producto
    i=0
    ban=0
    txt=len(str(request.POST.get('productos')))
    codigom=""
    elpre=0
    while i<txt and ban==0:
        if str(request.POST.get('productos'))[i]=="-":
            ban=1
        else:
            codigom=codigom+str(request.POST.get('productos'))[i]
        i=i+1
    #fin aca busque el producto
    #busco el precio inicio
    txt=str(request.POST.get('productos'))
    labarra=str(request.POST.get('productos')).find("|")
    dospunto=str(request.POST.get('productos')).find(":")
    tipopro=str(txt[dospunto+1:dospunto+20])
    elpre=float(txt[labarra+1:dospunto])
    #termine de buscar el precio
    elproducto=Productos.objects.get(id=int(codigom))   
    cantidad=request.POST.get('cantidad')
    le=request.POST.get('lejos')
    ce=request.POST.get('cenrca')
    iz=request.POST.get('izquierda')
    de=request.POST.get('derecha')
    ma=request.POST.get('marco')
    if (le is None):
        le=" "
    elif (ce is None):
        ce=" "
    elif (iz is None):
        iz=" "
    elif (de is None):
        de=" "
    elif (ma is None):
        ma= " "
    subt=int(cantidad)*elpre
    elpedidox=PedidoProductos.objects.get(id=id)
    elpedidox.total=elpedidox.total+subt
    elpedidex=DetallePedido(cantidad=cantidad,LE=le,CE=ce,IZ=iz,DE=de,MA=ma,id_producto_id=elproducto.id,id_pedido_id=elpedidox.id,subtotal=subt,tipo_P=tipopro)
    if request.method=="POST":        
        elpedidex.save()
        elpedidox.save()
    listaproductos = Productos.objects.all()
    detallep=DetallePedido.objects.filter(id_pedido_id=elpedidox.id)
    dire="/Gestion/editpedidoproducto/"+str(id)
    return redirect(dire,{'productos': listaproductos,'idped':id,'pedidos':detallep})


def deletePedido(request, id):
    #No hay baja de pedidos
    return redirect('/Gestion/crudTurnos')


def deletePedidoProducto(request, id,id2):
    elpedidox=PedidoProductos.objects.get(id=id2)
    listaproductos = Productos.objects.all()
    detallep=DetallePedido.objects.get(id=id)
    subto=detallep.subtotal
    tot=elpedidox.total
    elpedidox.total=tot-subto
    elpedidox.save()
    detallep.delete()
    dire="/Gestion/editpedidoproducto/"+str(id2)
    return redirect(dire,{'productos': listaproductos,'idped':id,'pedidos':detallep})
#Parte de los vendedores

#Taller
def crudTaller(request):
    elpedidex=PedidoProductos.objects.all()
    detallex=DetallePedido.objects.all()
    return render(request,'Gestion/5_A_index_taller.html', {'pedidos':elpedidex,'detalle':detallex})


def finalizarTaller(request,id):
    elpedidex=PedidoProductos.objects.get(id=id)
    elpedidex.estado="FINALIZADO"
    if request.method=="GET":
        elpedidex.save()
    return redirect('/Gestion/crudtaller')
#Taller

#Reportes
def asistenciaPacientes(request):
    if request.GET.get('desde') is None and request.GET.get('hasta') is None:
        desde=datetime.now()
        hasta=datetime.now()
    else:
        desde=request.GET.get('desde')
        hasta=request.GET.get('hasta')
    prenopre=request.GET.get('estado')
    losturnex=Turnos.objects.filter(fecha_hora__gte=desde,fecha_hora__lte=hasta,Estado=prenopre)
    return render(request,"Gestion/6_A_index_informes.html",{'losturnos':losturnex})


def pedidosDePacientes(request):
    if request.GET.get('desde') is None and request.GET.get('hasta') is None:
        desde=datetime.now()
        hasta=datetime.now()
    else:
        desde=request.GET.get('desde')
        hasta=request.GET.get('hasta')
    if request.method=="GET":
        list=DetallePedido.pedidosDePacientes(desde,hasta)
        return render(request,"Gestion/6_B_index_informes.html",{'lospedidos':list})
    else:
        return render(request,"Gestion/6_B_index_informes.html")


def productosmasvendidos(request):
    if request.GET.get('desde') is None and request.GET.get('hasta') is None:
        desde=datetime.now()
        hasta=datetime.now()
    else:
        desde=request.GET.get('desde')
        hasta=request.GET.get('hasta')
    if request.method=="GET":
        list=DetallePedido.productosmasvendidos(desde,hasta)
        return render(request,"Gestion/6_C_index_informes.html",{'lospedidos':list})
    else:
        return render(request,"Gestion/6_C_index_informes.html")


def vtastotalesxmesxvendedor(request):
    if request.GET.get('desde') is None and request.GET.get('hasta') is None:
        desde=datetime.now()
        hasta=datetime.now()
    else:
        desde=request.GET.get('desde')
        hasta=request.GET.get('hasta')
    if request.method=="GET":
        list=PedidoProductos.vtastotalesxmesxvendedor(desde,hasta)
        return render(request,"Gestion/6_D_index_informes.html",{'elmasve':list})
    else:
        return render(request,"Gestion/6_D_index_informes.html")
#Fin de reportes