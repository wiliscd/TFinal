from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,Group
from datetime import datetime, date, time, timedelta
from django.db import connection

# Create your models here.
class Pacientes(models.Model):
    apellidos=models.CharField(max_length=40)
    nombres=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.nombres}, {self.apellidos}"



class Medicos(models.Model):
    apellidos=models.CharField(max_length=40)
    nombres=models.CharField(max_length=40)
    especialidad=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.nombres}, {self.apellidos} - {self.especialidad}"


class Turnos(models.Model):
    id_paciente=models.ForeignKey(Pacientes,on_delete=models.CASCADE ,related_name="elpaciente")
    id_medico=models.ForeignKey(User,on_delete=models.CASCADE ,related_name="elmedico")
    descrip=models.CharField(max_length=255)
    Estado=models.CharField(max_length=20)
    fecha_hora=models.DateTimeField()
    
    def __str__(self):
        return f"{self.id_paciente}- {self.id_medico} - {self.fecha_hora}-{self.descrip}/{self.Estado}"



class Productos(models.Model):
    nompro=models.CharField(max_length=40)
    precio=models.FloatField()
    tipo=models.CharField(max_length=40)

    def __str__(self):
        return f"{self.nompro}"#" - {self.precio} : {self.tipo}"


class PedidoProductos(models.Model):
    id_vendedor=models.ForeignKey(User,on_delete=models.CASCADE ,related_name="elvendedor")
    id_paciente=models.ForeignKey(Pacientes,on_delete=models.CASCADE ,related_name="elpacientep")
    descrip=models.CharField(max_length=40)
    estado=models.CharField(max_length=40)
    pago=models.CharField(max_length=40)
    total=models.FloatField()
    fecha=models.DateTimeField()
    
    def __str__(self):
        return f"{self.id_vendedor}-{self.id_paciente}-{self.descrip} - {self.estado} - {self.pago} - {self.total}"

    def vtastotalesxmesxvendedor(desde,hasta):
        cursor = connection.cursor()
        cursor.execute("select ven.username,SUM(gpp.total) as tot from Gestion_pedidoproductos as gpp,auth_user as ven where gpp.id_vendedor_id=ven.id and (gpp.fecha>=%s and gpp.fecha<=%s) group by ven.username order by tot desc",[desde,hasta])
        results = cursor.fetchall()
        list = []
        i = 0
        for row in results:
            list.append(str(results[i][0])) 
            i = i + 1
        return list

class DetallePedido(models.Model):
    id_pedido=models.ForeignKey(PedidoProductos,on_delete=models.CASCADE ,related_name="elnrodelpedido")
    id_producto=models.ForeignKey(Productos,on_delete=models.CASCADE ,related_name="elprodelpedido")
    cantidad=models.IntegerField()
    LE=models.CharField(max_length=2)
    CE=models.CharField(max_length=2)
    IZ=models.CharField(max_length=2)
    DE=models.CharField(max_length=2)
    MA=models.CharField(max_length=2)
    subtotal=models.FloatField()
    tipo_P=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id_pedido}-{self.id_producto}-{self.cantidad},{self.LE},{self.CE},{self.IZ},{self.DE},{self.MA},{self.subtotal},{self.tipo_P}"
    

    def productosmasvendidos(desde,hasta):
            cursor = connection.cursor()
            cursor.execute("select produ.nompro,SUM(gpe.cantidad) as tot from Gestion_productos as produ, Gestion_detallepedido as gpe,Gestion_pedidoproductos as pedi where produ.id=gpe.id_producto_id and pedi.id=gpe.id_pedido_id and (pedi.fecha>=%s and pedi.fecha<=%s) group by produ.nompro order by tot desc",[desde,hasta])
            results = cursor.fetchall()
            list = []
            i = 0
            for row in results:
                list.append(str(results[i][0])) 
                i = i + 1
            return list
    
    def pedidosDePacientes(desde,hasta):
        cursor = connection.cursor()
        cursor.execute("select (gpa.apellidos||','||gpa.nombres) as apenom,count(gpe.id) as ped from Gestion_pedidoproductos as gpe,Gestion_pacientes as gpa where gpe.id_paciente_id=gpa.id and (gpe.fecha>=%s and gpe.fecha<=%s) group by apenom",[desde,hasta])
        results = cursor.fetchall()
        list = []
        i = 0
        for row in results:
            list.append(str(results[i][0])) 
            i = i + 1
        return list