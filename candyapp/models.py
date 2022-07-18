
from django.db import models

# Create your models here.
    
class lugar(models.Model):
    id_lg = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Lugar")


class producto(models.Model):
    id_pd = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, verbose_name="nombre")
    descripcion = models.TextField(max_length=100, null=True, verbose_name="descripcion")
    precio = models.FloatField(verbose_name="Precio base")
    estado = models.CharField(max_length=20, verbose_name="estado")
    id_lg = models.ForeignKey(lugar, verbose_name="Lugar", on_delete=models.CASCADE)

class materia_s(models.Model):
    id_ms = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, verbose_name="nombre")
    descripcion = models.TextField(max_length=100, verbose_name="descripcion")
    estado = models.CharField(max_length=20, verbose_name="estado")
    id_lg = models.ForeignKey(lugar, verbose_name="Lugar", on_delete=models.CASCADE)  

class materia_p(models.Model):
    id_mp = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, verbose_name="nombre")
    cantidad = models.IntegerField(verbose_name="cantidad")
    unidad = models.CharField(max_length=10, verbose_name="unidad")
    costo = models.FloatField(verbose_name="costo")
    costo_u = models.FloatField(verbose_name="costo unitario")
    proveedor = models.CharField(max_length=30, verbose_name="proveedor")
    contacto = models.CharField(max_length=14, verbose_name="contacto", null=True)
    tiempo = models.CharField(max_length=14, verbose_name="tiempo de entrega", null=True)
    mincant = models.IntegerField(verbose_name="cantidad minima", null=True)
    descripcion = models.TextField(max_length=100, verbose_name="descripcion", null=True)
    estado = models.CharField(max_length=20, verbose_name="estado")
    fecha = models.CharField(max_length=50, verbose_name="Fecha")
    id_lg = models.ForeignKey(lugar, verbose_name="Lugar", on_delete=models.CASCADE)

class basepd(models.Model):
    id_bp = models.AutoField(primary_key=True)
    id_pd = models.ForeignKey(producto, verbose_name="Producto", on_delete=models.CASCADE)
    id_mp = models.ForeignKey(materia_p, verbose_name="Materia", on_delete=models.CASCADE) 
    cantidad = models.IntegerField(verbose_name="cantidad") 

class mezcla(models.Model):
    id_mz = models.AutoField(primary_key=True)
    id_ms = models.ForeignKey(materia_s, verbose_name="materia secundaria", on_delete=models.CASCADE)
    id_mp = models.ForeignKey(materia_p, verbose_name="materia primaria", on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="cantidad")
    costo = models.FloatField(verbose_name="costo")

class posicion(models.Model):
    id_ps = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, verbose_name="nombre")
    precio = models.FloatField(verbose_name="precio")
    id_pd = models.ForeignKey(producto, verbose_name="producto", on_delete=models.CASCADE)

class menu(models.Model):
    id_mn = models.AutoField(primary_key=True)
    id_ms = models.ForeignKey(materia_s, verbose_name="materia secundaria", on_delete=models.CASCADE)
    id_ps = models.ForeignKey(posicion, verbose_name="posicion", on_delete=models.CASCADE)

class factura(models.Model):
    id_ft = models.AutoField(primary_key=True)
    id_lg = models.ForeignKey(lugar, verbose_name="Lugar", on_delete=models.CASCADE)

class candycarrito(models.Model):
    id_cr = models.AutoField(primary_key=True)
    id_pd = models.ForeignKey(producto, verbose_name="producto", on_delete=models.CASCADE)
    nombre_pd = models.CharField(max_length=20, null=True)
    precio = models.FloatField(verbose_name="precio", null=True)
    id_lg = models.ForeignKey(lugar, verbose_name="Lugar", on_delete=models.CASCADE)

class armado(models.Model):
    id_ar = models.AutoField(primary_key=True)
    id_cr = models.ForeignKey(candycarrito, verbose_name="carrito", on_delete=models.CASCADE)
    id_mn = models.ForeignKey(menu, verbose_name="menu", on_delete=models.CASCADE)
    nombre_ms = models.CharField(max_length=20, null=True)
    precio = models.FloatField(null=True)
               
class entregado(models.Model):
    id_eg = models.AutoField(primary_key=True) 
    mesa =  models.CharField(max_length=50)    
    cliente = models.CharField(max_length=50, null=True)   
    id_cr = models.CharField(max_length=50, verbose_name="carrito")
    descripcion = models.CharField(max_length=100, null=True)
    precio = models.FloatField(null=True)
    preciot = models.FloatField(null=True)
    id_lg = models.ForeignKey(lugar, verbose_name="Lugar", on_delete=models.CASCADE)

class infofactura(models.Model):
    id_if = models.AutoField(primary_key=True)
    precio = models.FloatField(verbose_name="Precio")
    entregado = models.IntegerField(verbose_name="Valor entregado")
    producto = models.CharField(max_length=50, verbose_name="Producto")
    adiciones = models.CharField(max_length=50, verbose_name="Adiciones")
    fecha = models.CharField(max_length=50, verbose_name="Fecha")
    id_ft = models.IntegerField(verbose_name="Factura")
    lugar = models.CharField(max_length=50, verbose_name="Lugar")

class finanza(models.Model):
    id_fz = models.AutoField(primary_key=True)
    fecha = models.CharField(max_length=50, verbose_name="Fecha")
    id_lg = models.IntegerField(verbose_name="Lugar")
    id_hs = models.IntegerField(verbose_name="Historial")
    costot = models.FloatField(verbose_name="Costo total", null=True)
    
class historial_fz(models.Model):
    id_hf = models.AutoField(primary_key=True)
    fecha = models.CharField(max_length=50, verbose_name="Fecha")
    costot = models.FloatField(verbose_name="Costo total", null=True)
    id_lg = models.IntegerField(verbose_name="Lugar")

class historial_mp(models.Model):
    id_hp = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.CharField(max_length=50, verbose_name="Fecha")
    materiap = models.CharField(max_length=50, verbose_name="Materia prima")

class compt(models.Model):
    id_cp = models.AutoField(primary_key=True)
    servicio = models.CharField(max_length=50, verbose_name="Servicio")
    costo = models.FloatField(verbose_name="Costo")
    hora = models.CharField(max_length=50, verbose_name="Hora")
    finz = models.IntegerField(verbose_name="Cantidad")
    id_sv = models.IntegerField(verbose_name="Servicio")
    id_lg = models.IntegerField(verbose_name="Lugar")