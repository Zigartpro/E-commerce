from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from.models import *
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email.mime.text import MIMEText
import smtplib
import json
import time
import paypalrestsdk
from django.db.models import Sum, Count
from django.conf import settings


paypalrestsdk.configure({
  "mode": "sandbox",  # O "live" si estás en producción
  "client_id": settings.PAYPAL_CLIENT_ID,
  "client_secret": settings.PAYPAL_CLIENT_SECRET
})

# Create your views here.
def inicio(request):
    if 'user_id' not in request.session:
        return redirect('login') 
    if request.method == 'POST' or request.method == 'GET':
        productos = Productos.objects.all()
        categoria = request.GET.get('categoria', None)
        termino_busqueda = request.GET.get('buscar', None)
        orden = request.GET.get('orden', None)  # Obtener el parámetro de orden

        if categoria:
            productos = Productos.objects.filter(Categoria=categoria)
        elif termino_busqueda:
            productos = Productos.objects.filter(Nombre__icontains=termino_busqueda)
        else:
            productos = Productos.objects.all()

        # Ordenar los productos según el parámetro de orden
        if orden == 'az':
            productos = productos.order_by('Nombre')  # Ordenar de A a Z
        elif orden == 'za':
            productos = productos.order_by('-Nombre')  # Ordenar de Z a A
            
    return render(request, 'shop.html', {'productos': productos})

def registro(request):
    if request.method == 'POST' or 'GET':
        try:
            usuarios = Usuarios(
                NumeroDocumento=request.POST['ID'],
                Nombre=request.POST['name'],
                Telefono=request.POST['phone'],
                Correo=request.POST['email'],
                CodigoPostal=request.POST['postal_code'],
                Municipio=request.POST['city'],
                Departamento=request.POST['department'],
                Direccion=request.POST['address'],
                Contraseña=request.POST['password'],
            )
            if Usuarios.objects.filter(NumeroDocumento=usuarios.NumeroDocumento).exists():
                JsonResponse({'error': 'Usuario ya existe'})
                return redirect('registro') 
            else:
                usuarios.save()
                messages.success(request, 'Usuario creado correctamente')
                time.sleep(2)
                return redirect('login')  # Redirecciona a donde quieras después de crear el usuario
        except KeyError:
            messages.error(request, 'Error en la creación del usuario: Faltan datos en el formulario')
            time.sleep(2)
        except IntegrityError:
            messages.error(request, 'Error en la creación del usuario: El número de documento ya está en uso')
            time.sleep(2)
    return render(request, 'registro.html')

def login(request):
    if request.method == 'POST':
        NumeroDocumento = request.POST['NumeroDocumento']
        password = request.POST['password']
        
        # Buscar al usuario por su NumeroDocumento
        try:
            usuario = Usuarios.objects.get(NumeroDocumento=NumeroDocumento, Contraseña=password)
        except Usuarios.DoesNotExist:
            usuario = None

        # Verificar si se encontró al usuario y si su contraseña es válida
        if usuario is not None:
            # Almacenar el ID de usuario y el rol en la sesión para mantenerla activa
            request.session['user_id'] = usuario.NumeroDocumento
            request.session['user_rol'] = usuario.idRol.idRoll# Asumiendo que el modelo Usuario tiene un campo 'rol'
            messages.success(request, 'Inicio de sesión exitoso')
            if usuario.idRol.idRoll == 1:
                return redirect('visven')
            elif usuario.idRol.idRoll == 2:
                return redirect('actividades')  # Nombre de la vista para administradores
            elif usuario.idRol.idRoll == 4:
                return redirect('gerente')  # Nombre de la vista para empleados
            elif usuario.idRol.idRoll == 5:
                return redirect('gerente')  # Nombre de la vista para empleados
            else:
                return HttpResponse("Rol no reconocido")
        else:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'login.html')

def logout(request):
    # Eliminar los datos de la sesión
    try:
        if 'user_id' in request.session:
            del request.session['user_id']
        if 'user_rol' in request.session:
            del request.session['user_rol']
        messages.success(request, 'Sesión cerrada con éxito')
    except:
        messages.error(request, 'No se pudo cerrar la sesión')
    return redirect('login')

def regpro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        valor = request.POST.get('valor')
        marca = request.POST.get('marca')
        descripcion = request.POST.get('descripcion')
        foto = request.FILES.get('foto')

        try:
            producto = Productos(
                Nombre=nombre,
                Categoria=categoria,
                Valor=valor,
                Marca=marca,
                Descripcion=descripcion,
                Foto=foto
            )
            producto.save()
            messages.success(request, 'Producto registrado')
            return redirect('regisven')
        except:
            messages.success(request, 'Error al registrar el producto')
            return redirect('regisven')
    return render(request, 'resgispro.html')

def vistaven(request):
    if request.method == 'POST' or request.method == 'GET':
        productos = Productos.objects.all()
        categoria = request.GET.get('categoria', None)
        termino_busqueda = request.GET.get('buscar', None)
        orden = request.GET.get('orden', None)  # Obtener el parámetro de orden

        if categoria:
            productos = Productos.objects.filter(Categoria=categoria)
        elif termino_busqueda:
            productos = Productos.objects.filter(Nombre__icontains=termino_busqueda)
        else:
            productos = Productos.objects.all()

        # Ordenar los productos según el parámetro de orden
        if orden == 'az':
            productos = productos.order_by('Nombre')  # Ordenar de A a Z
        elif orden == 'za':
            productos = productos.order_by('-Nombre')  # Ordenar de Z a A
            
    return render(request, 'shop.html', {'productos': productos})

def regisven(request):
    if request.method == 'POST' or 'GET':    
        productos = Productos.objects.all()
    return render(request, 'regisven.html', {'productos': productos})

def editar_producto(request, pk):
    # Obtener el producto correspondiente a partir de su clave primaria (pk)
    producto = get_object_or_404(Productos, idProducto=pk)
    
    if request.method == 'POST':
        # Si se envía un formulario POST, procesar la información recibida para actualizar el producto
        producto.Nombre = request.POST.get('Nombre')
        producto.Categoria = request.POST.get('Categoria')
        producto.Valor = request.POST.get('Valor')
        producto.Marca = request.POST.get('Marca')
        producto.Descripcion = request.POST.get('Descripcion')
        
        if 'Foto' in request.FILES:
            producto.Foto = request.FILES['Foto']

        # Guardar los cambios en la base de datos
        producto.save()
        
        # Redirigir al usuario a la página de detalle del producto o a donde desees
        return redirect('regisven')
    
    # Si la solicitud es GET, renderizar el formulario de edición con los datos del producto
    return render(request, 'editar_producto.html', {'producto': producto})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Productos, idProducto=pk)
    producto.delete()
    # Redirigir a donde desees después de eliminar el producto
    return redirect(to='regisven')

def detalle_producto(request, pk):
    # Obtener el producto específico
    producto = get_object_or_404(Productos, idProducto=pk)

    # Obtener todas las reseñas para el producto
    reseñas_producto = reseña.objects.filter(idproducto=producto)

    return render(request, 'shop-single.html', {'producto': producto, 'reseñas': reseñas_producto})

def agregar_comentario(request, pk):
    # Obtener el producto específico
    producto = get_object_or_404(Productos, idProducto=pk)
    # Obtener el comentario de la reseña del POST
    comentario = request.POST.get('comentario')
    nueva_reseña = reseña.objects.create(idproducto=producto, Descripcion=comentario)
    nueva_reseña.save()

    # Redireccionar a la página de detalles del producto después de agregar el comentario
    return redirect('detalle_producto', pk=pk)

def lista_usuarios(request):
    usuarios = Usuarios.objects.all()
    roles = Rol.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios, 'roles': roles})

def editar_usuario(request, NumeroDocumento):
    usuario = get_object_or_404(Usuarios, NumeroDocumento=NumeroDocumento)
    roles = Rol.objects.all()  # Obtener todos los roles, podrías necesitar esto para renderizar un menú desplegable en tu formulario

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        codigo_postal = request.POST['codigo_postal']
        direccion = request.POST['direccion']
        municipio = request.POST['municipio']
        departamento = request.POST['departamento']
        idRol = request.POST['rol']

        # Buscar el objeto Rol correspondiente
        rol = get_object_or_404(Rol, pk=idRol)

        # Actualizar los datos del usuario
        usuario.Nombre = nombre
        usuario.Telefono = telefono
        usuario.Correo = correo
        usuario.CodigoPostal = codigo_postal
        usuario.Direccion = direccion
        usuario.Municipio = municipio
        usuario.Departamento = departamento
        usuario.idRol = rol  # Asignar el objeto Rol, no solo el ID
        usuario.save()

        # Redireccionar a alguna página de éxito
        return redirect('lista_usuarios')  # Ajusta esto a tu URL de éxito

    return render(request, 'editar_usuario.html', {'usuario': usuario, 'roles': roles})


def eliminar_usuario(request):
    if request.method == 'POST':
        numero_documento = request.POST.get('numero_documento')
        try:
            usuario = Usuarios.objects.get(NumeroDocumento=numero_documento)
            usuario.delete()
        except Usuarios.DoesNotExist:
            # Si el usuario no existe, puedes mostrar un mensaje de error o simplemente ignorarlo
            pass
    return redirect('lista_usuarios')

def carrito(request):
    # Verificar si el usuario está autenticado mediante la sesión
    if 'user_id' not in request.session:
        return redirect('login')  # Ajusta 'login' a la URL name de tu página de inicio de sesión
    
    # Obtener todos los elementos del carrito para el usuario actual
    carrito_items = Carrito.objects.filter(idusuario=request.session['user_id'])
    
    # Calcular el total del carrito
    total = sum(item.idproducto.Valor * item.Cantidad for item in carrito_items)
    
    # Contar el número total de productos en el carrito
    total_productos = sum(item.Cantidad for item in carrito_items)

    pagototal = total + 15000
    
    context = {
        'carrito': carrito_items,
        'total': total,
        'total_productos': total_productos,
        'pagototal': pagototal
    }
    
    return render(request, 'carrito.html', context)

def agregar_al_carrito(request, pk):
    # Obtener el producto basado en su ID
    producto = get_object_or_404(Productos, idProducto=pk)
    
    # Verificar si el usuario ha iniciado sesión
    if 'user_id' in request.session:
        # Obtener el número de documento del usuario
        numero_documento = request.session['user_id']
        
        # Obtener la instancia del modelo Usuarios correspondiente al número de documento
        usuario = Usuarios.objects.get(NumeroDocumento=numero_documento)
        
        # Verificar si el producto ya está en el carrito del usuario
        carrito_existente = Carrito.objects.filter(idproducto=producto, idusuario=usuario).first()
        if carrito_existente:
            # Si el producto ya está en el carrito, simplemente incrementamos la cantidad
            carrito_existente.Cantidad += 1
            carrito_existente.save()
        else:
            # Si el producto no está en el carrito, lo agregamos
            nuevo_carrito = Carrito(Cantidad=1, idproducto=producto, idusuario=usuario)
            nuevo_carrito.save()
        
        # Redirigir a la página del detalle del producto o a donde desees
        return redirect('visven')
    else:
        # Si el usuario no ha iniciado sesión, redirigir a la página de inicio de sesión o mostrar un mensaje de error
        return redirect('login')  # Ajusta 'login' al nombre de tu vista de inicio de sesión

def actualizar_al_carrito(request, pk):
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        carrito_item = get_object_or_404(Carrito, idCarrito=pk)
        carrito_item.Cantidad = cantidad
        carrito_item.save()
        return redirect('carrito')  # Ajusta esto a la vista que muestra el carrito
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def eliminar_del_carrito(request, pk):
    if request.method == 'POST':
        # Obtener el ID del elemento del carrito desde la solicitud POST
        try:
            # Buscar el elemento del carrito por su ID y eliminarlo
            carrito_item = Carrito.objects.get(idCarrito=pk)
            carrito_item.delete()
            return redirect('carrito')
        except Carrito.DoesNotExist:
            return JsonResponse({'error': 'El producto no existe'}, status=405)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def procesar_pago(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        description = request.POST.get('description')
        
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/pago_exitoso/",
                "cancel_url": "http://localhost:8000/pago_cancelado/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Pago de productos",  # Puedes ajustar esto según sea necesario
                        "sku": "item",
                        "price": amount,  # Usa el monto del formulario
                        "currency": currency,  # Usa la moneda del formulario
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": amount,  # Usa el monto del formulario
                    "currency": currency  # Usa la moneda del formulario
                },
                "description": description  # Usa la descripción del formulario
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    return redirect(link.href)
        else:
            return HttpResponse(f'Error al procesar el pago: {payment.error}')
    else:
        return HttpResponse("Método de solicitud no permitido.")

def enviar_correo(destinatario, asunto, mensaje):
    # Configura los detalles del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # El puerto SMTP (usualmente 587 para TLS)

    # Configura el remitente y las credenciales de correo electrónico
    remitente = 'xxnetproshop@gmail.com'
    password = 'lmwp izri rzav ocfr'

    # Crea el mensaje de correo
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    # Inicia una conexión SMTP y envía el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia una conexión TLS (Transport Layer Security)
        server.login(remitente, password)
        server.sendmail(remitente, [destinatario], msg.as_string())
        server.quit()  # Cierra la conexión SMTP
        return True
    except Exception as e:
        print("Error al enviar el correo:", e)
        return False

def pago_exitoso(request):
    try:
        # Obtener el usuario a partir del ID de sesión
        user = Usuarios.objects.get(NumeroDocumento=request.session['user_id'])
        
        # Obtener el carrito del usuario
        carrito = Carrito.objects.filter(idusuario=user).select_related('idproducto')
        
        if not carrito.exists():
            return HttpResponse("El carrito está vacío.")

        venta = Ventas.objects.all()
        ventatotal = sum(item.idproducto.Valor * item.Cantidad for item in carrito)

        UV = 0

        if not venta.exists():
            numeroventa = 1 
            UV = numeroventa
            newventa = Ventas(Nventa=numeroventa, Valor=ventatotal)
            newventa.save()
        else:
            numeroventa = venta.last().Nventa + 1
            UV = numeroventa
            newventa = Ventas(Nventa=numeroventa, Valor=ventatotal)
            newventa.save()

        # Calcular el total de la compra y preparar el mensaje del correo
        total = 0
        detalles_compra = "Productos comprados:\n"
        print(UV)
        ultimaventa = Ventas.objects.get(Nventa=UV)  # Obtener la última venta creada como una única instancia
        
        for item in carrito:
            subtotal = item.idproducto.Valor * item.Cantidad
            total += subtotal
            detalles_compra += f"- {item.idproducto.Nombre}: {item.Cantidad} x ${item.idproducto.Valor:.2f} = ${subtotal:.2f}\n"
            
            # Crear las compras individuales
            compra = Compras(Cantidad=item.Cantidad, Producto=item.idproducto.idProducto, Usuario=user.NumeroDocumento, idventa=ultimaventa)  # Usar instancias completas
            compra.save()

        # Borrar el carrito de compras del usuario
        carrito.delete()

        # Preparar el correo electrónico
        destinatario = duvanfericosarmientolugo@gmail.com
        asunto = 'Confirmación de compra'
        mensaje = (
            f"Gracias por tu compra. Tu pago ha sido recibido y procesado con éxito.\n\n"
            f"{detalles_compra}\n"
            f"Valor total: ${total:.2f}\n"
        )

        # Enviar el correo de confirmación
        if enviar_correo(destinatario, asunto, mensaje):
            return redirect("factura")
        else:
            return HttpResponse("¡Pago exitoso! No se pudo enviar el correo de confirmación.")
    
    except Usuarios.DoesNotExist:
        return HttpResponse("¡Pago exitoso! No se pudo encontrar al usuario.")
    except KeyError:
        return HttpResponse("¡Pago exitoso! No se pudo obtener la dirección de correo electrónico.")
    except Exception as e:
        return HttpResponse(f"¡Ocurrió un error durante el proceso de pago: {str(e)}")
    
    except Usuarios.DoesNotExist:
        return HttpResponse("¡Pago exitoso! No se pudo encontrar al usuario.")
    except KeyError:
        return HttpResponse("¡Pago exitoso! No se pudo obtener la dirección de correo electrónico.")
    except Exception as e:
        return HttpResponse(f"¡Ocurrió un error durante el proceso de pago: {str(e)}")
    
def pago_cancelado(request):
    return HttpResponse("Pago cancelado.")

def factura(request):
    try:
        # Obtener el usuario con el número de documento almacenado en la sesión
        usuario = Usuarios.objects.get(NumeroDocumento=request.session['user_id'])
        
        # Obtener la última compra realizada por el usuario
        compra = Compras.objects.filter(Usuario=usuario.NumeroDocumento).last()
        
        # Verificar si el usuario tiene compras
        if compra is None:
            return render(request, 'factura.html', {'usuario': usuario, 'compras': None, 'ultimacompra': [], 'productos': []})
        
        # Obtener la venta asociada a la última compra
        venta = compra.idventa
        
        # Crear una nueva factura asociada a la venta
        nuevafactura = Facturas(idventa=venta)
        nuevafactura.save()

        # Obtener todas las compras asociadas con el id de la venta
        ultimacompra = Compras.objects.filter(idventa=venta)
        
        # Obtener todos los productos de la compra
        productos = []
        for compra in ultimacompra:
            # Aquí se asume que cada objeto de `ultimacompra` tiene un campo `Producto` que es un ID de producto
            producto = Productos.objects.get(idProducto=compra.Producto)
            productos.append({
                'nombre': producto.Nombre,
                'cantidad': compra.Cantidad,
                'precio': producto.Valor
            })
        
        return render(request, 'factura.html', {
            'usuario': usuario,
            'compras': compra,
            'ultimacompra': ultimacompra,
            'productos': productos
        })
    except Usuarios.DoesNotExist:
        return render(request, 'error.html', {'message': 'Usuario no encontrado.'})
    except Productos.DoesNotExist:
        return render(request, 'error.html', {'message': 'Producto no encontrado.'})


@csrf_exempt
def pago_completado(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.state == 'approved':
            return HttpResponse("¡Pago completado exitosamente!")
        else:
            return HttpResponse("El pago no fue aprobado por PayPal.")
    else:
        return HttpResponse("Método de solicitud no permitido.")
        
def lista_inventarios(request):
    inventarios = Inventarios.objects.all()
    return render(request, 'lista_inventarios.html', {'inventarios': inventarios})

def agregar_inventario(request):
    if request.method == 'POST':
        idproducto = request.POST['idproducto']
        cantidad = request.POST['cantidad']
        producto = get_object_or_404(Productos, pk=idproducto)
        Inventarios.objects.create(idproducto=producto, cantidad=cantidad)
        return redirect('lista_inventarios')
    productos = Productos.objects.all()
    return render(request, 'agregar_inventario.html', {'productos': productos})

def editar_inventario(request, pk):
    inventario = get_object_or_404(Inventarios, pk=pk)
    if request.method == 'POST':
        inventario.idproducto_id = request.POST['idproducto']
        inventario.cantidad = request.POST['cantidad']
        inventario.save()
        return redirect('lista_inventarios')
    productos = Productos.objects.all()
    return render(request, 'editar_inventario.html', {'inventario': inventario, 'productos': productos})

def borrar_inventario(request, pk):
    inventario = get_object_or_404(Inventarios, pk=pk)
    if request.method == 'POST':
        inventario.delete()
        return redirect('lista_inventarios')
    return render(request, 'borrar_inventario.html', {'inventario': inventario})

def servicios(request):
    return render(request, 'servicios.html')

def contactanos(request):
    return render(request, 'contactanos.html')

def gerente(request):
    return render(request, 'gerente.html')

def reporte(request):
    # Periodo del reporte (últimos 30 días, por ejemplo)
    inicio_periodo = timezone.now() - timezone.timedelta(days=30)
    fin_periodo = timezone.now()

    # Filtrar compras por periodo
    compras_periodo = Compras.objects.filter(Fecha__range=(inicio_periodo, fin_periodo))

    # Obtener IDs de ventas relacionadas con las compras en el periodo
    ventas_ids = compras_periodo.values_list('idventa_id', flat=True).distinct()

    # Calcular total de ventas basado en los IDs obtenidos
    total_ventas = Ventas.objects.filter(idVenta__in=ventas_ids).aggregate(total=Sum('Valor'))['total'] or 0

    # Datos de compras
    total_compras = compras_periodo.aggregate(total=Sum('Cantidad'))['total'] or 0
    compras_por_producto = compras_periodo.values('Producto').annotate(total=Sum('Cantidad')).order_by('-total')

    # Datos de facturas
    total_facturas = Facturas.objects.filter(idventa__in=ventas_ids).count()
    facturas_por_periodo = Facturas.objects.filter(idventa__in=ventas_ids)

    context = {
        'inicio_periodo': inicio_periodo,
        'fin_periodo': fin_periodo,
        'total_ventas': total_ventas,
        'total_compras': total_compras,
        'total_facturas': total_facturas,
        'compras_por_producto': compras_por_producto,
        'facturas_por_periodo': facturas_por_periodo,
    }

    return render(request, 'reporte.html', context)

def actividades(request):
    if request.method == "POST":
        asunto = request.POST.get('asunto')
        descripcion = request.POST.get('descripcion')
        involucrado = request.POST.get('involucrado')
        
        nueva_actividad = Actividades(asunto=asunto, descripcion=descripcion, involucrado=involucrado)
        nueva_actividad.save()
        
        return redirect('actividades')
    
    actividades = Actividades.objects.filter(estado=1)
    return render(request, 'actividades.html', {'actividades': actividades})

def editar_actividad(request, idactividad):
    actividad = get_object_or_404(Actividades, idactividad=idactividad)
    
    if request.method == "POST":
        actividad.asunto = request.POST.get('asunto')
        actividad.descripcion = request.POST.get('descripcion')
        actividad.involucrado = request.POST.get('involucrado')
        actividad.save()
        
        return redirect('actividades')
    
    return render(request, 'editar_actividad.html', {'actividad': actividad})

def borrar_actividad(request, idactividad):
    actividad = get_object_or_404(Actividades, idactividad=idactividad)
    actividad.delete()
    return redirect('actividades')

def lista_actividades(request):
    # Obtener todas las actividades que tienen el estado 1
    actividades_estado_1 = Actividades.objects.filter(estado=1)

    # Obtener todas las actividades que tienen el estado 2
    actividades_estado_2 = Actividades.objects.filter(estado=2)

    return render(request, 'lista_actividades.html', {
        'actividades_estado_1': actividades_estado_1,
        'actividades_estado_2': actividades_estado_2
    })

def cambiar_estado(request, idactividad):
    actividad = get_object_or_404(Actividades, idactividad=idactividad)
    if request.method == 'POST':
        actividad.estado = 2
        actividad.save()
    return redirect('lista_actividades')

def list_repartidores(request):
    repartidores = Repartidor.objects.all()
    return render(request, 'repartidor_list.html', {'repartidores': repartidores})

def list_and_update_repartidores(request):
    if request.method == 'POST':
        repartidor_id = request.POST.get('repartidor_id')
        nuevo_repartidor_id = request.POST.get('nuevo_repartidor')

        if repartidor_id and nuevo_repartidor_id:
            repartidor = get_object_or_404(Repartidor, idrepartidor=repartidor_id)
            nuevo_repartidor = get_object_or_404(Usuarios, id=nuevo_repartidor_id, rol=2)
            repartidor.repartidor = nuevo_repartidor
            repartidor.save()
            return redirect('repartidor')

    repartidores = Repartidor.objects.all()
    repartidores_rol_2 = Usuarios.objects.filter(idRol=2)
    return render(request, 'repartidor.html', {
        'repartidores': repartidores,
        'repartidores_rol_2': repartidores_rol_2
    })
