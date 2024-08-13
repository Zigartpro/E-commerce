"""
URL configuration for CRUD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('regpro/', views.regpro, name='articulos'),
    path('visven/', views.vistaven, name='visven'),
    path('regisven/', views.regisven, name='regisven'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('detalle_producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('agregar_comentario/<int:pk>/', views.agregar_comentario, name='agregar_comentario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/<int:NumeroDocumento>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_al_carrito/<int:pk>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar_al_carrito/<int:pk>/', views.actualizar_al_carrito, name='actualizar_al_carrito'),
    path('eliminar_del_carrito/<int:pk>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path('pago/completado/', views.pago_completado, name='pago_completado'),
    path('pago/cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('inventarios/', views.lista_inventarios, name='lista_inventarios'),
    path('inventario/agregar/', views.agregar_inventario, name='agregar_inventario'),
    path('inventario/<int:pk>/editar/', views.editar_inventario, name='editar_inventario'),
    path('inventario/<int:pk>/borrar/', views.borrar_inventario, name='borrar_inventario'),
    path('contactanos/', views.contactanos, name='contactanos'),
    path('servicios/', views.servicios, name='servicios'),
    path('factura/', views.factura, name='factura'),
    path('gerente/', views.gerente, name='gerente'),
    path('reporte/', views.reporte, name='reporte'),
    path('actividades/', views.actividades, name='actividades'),
    path('actividades/editar/<int:idactividad>/', views.editar_actividad, name='editar_actividad'),
    path('actividades/borrar/<int:idactividad>/', views.borrar_actividad, name='borrar_actividad'),
    path('lista_actividades/', views.lista_actividades, name='lista_actividades'),
    path('cambiar_estado/<int:idactividad>/', views.cambiar_estado, name='cambiar_estado'),
    path('repartidoresad/', views.list_repartidores, name='list_repartidores'),
    path('repartidores/', views.list_and_update_repartidores, name='repartidores'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
