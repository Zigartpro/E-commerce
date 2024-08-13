from django.db import models
from django.utils import timezone

class Rol(models.Model):
    idRoll = models.IntegerField(primary_key=True, auto_created=True)
    Nombre = models.CharField(max_length=45)

class Usuarios(models.Model):
    NumeroDocumento = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=45)
    Telefono = models.CharField(max_length=10)
    Correo = models.CharField(max_length=45)
    CodigoPostal = models.IntegerField()
    Direccion = models.CharField(max_length=45)
    Municipio = models.CharField(max_length=20)
    Departamento = models.CharField(max_length=20)
    Contraseña = models.CharField(max_length=12)
    idRol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING, default=3)

class Productos(models.Model):
    idProducto = models.AutoField(primary_key=True, auto_created=True)
    Nombre = models.CharField(max_length=45)
    Categoria = models.CharField(max_length=45)
    Valor = models.IntegerField()
    Marca = models.CharField(max_length=15)
    Descripcion = models.CharField(max_length=120)
    Foto = models.ImageField(upload_to='productos', null=True)

class Carrito(models.Model):
    idCarrito = models.IntegerField(primary_key=True, auto_created=True)
    Cantidad = models.IntegerField()
    idproducto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING)
    idusuario = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)

class Inventarios(models.Model):
    idstock = models.IntegerField(primary_key=True, auto_created=True)
    idproducto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()

class reseña(models.Model):
    idreseña = models.IntegerField(primary_key=True, auto_created=True)
    idproducto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING)
    Descripcion = models.CharField(max_length=200)

class Ventas(models.Model):
    idVenta = models.IntegerField(primary_key=True, auto_created=True)
    Valor = models.FloatField()
    Nventa = models.IntegerField()

class Compras(models.Model):
    idCompra = models.IntegerField(primary_key=True, auto_created=True)
    Producto = models.IntegerField()
    Cantidad = models.IntegerField()
    Usuario = models.IntegerField()
    Fecha = models.DateTimeField(default=timezone.now)
    idventa = models.ForeignKey(Ventas, on_delete=models.DO_NOTHING)

class Facturas(models.Model):
    idFactura = models.IntegerField(primary_key=True, auto_created=True)
    idventa =  models.ForeignKey(Ventas, on_delete=models.DO_NOTHING)

class Actividades(models.Model):
    idactividad = models.IntegerField(primary_key=True, auto_created=True)
    asunto = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=200)
    involucrado = models.IntegerField()
    estado = models.IntegerField(default=1)

class Repartidor(models.Model):
    idrepartidor = models.IntegerField(primary_key=True, auto_created=True)
    Venta = models.ForeignKey(Ventas, on_delete=models.DO_NOTHING)
    repartidor = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)
    estador = models.IntegerField(default=1)