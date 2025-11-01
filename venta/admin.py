from django.contrib import admin
from venta import models


@admin.register(models.Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'correo', 'rol', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('nombre', 'apellido', 'correo')
    raw_id_fields = ('rol',)


@admin.register(models.Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(models.Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca')
    list_filter = ('marca',)
    search_fields = ('nombre', 'marca__nombre')
    raw_id_fields = ('marca',)


@admin.register(models.Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo', 'año', 'precio', 'estado', 'usuario', 'fecha_publicacion')
    list_filter = ('estado', 'tipo_combustible', 'tipo_transmision', 'año', 'fecha_publicacion')
    search_fields = ('marca__nombre', 'modelo__nombre', 'descripcion', 'usuario__nombre', 'usuario__apellido')
    raw_id_fields = ('usuario', 'marca', 'modelo')


class VehiculoFotoInline(admin.TabularInline):
    model = models.VehiculoFoto
    extra = 0
    verbose_name = "Foto"
    verbose_name_plural = "Fotos del Vehículo"


@admin.register(models.VehiculoFoto)
class VehiculoFotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'url_imagen')
    search_fields = ('vehiculo__marca__nombre', 'vehiculo__modelo__nombre')
    raw_id_fields = ('vehiculo',)


class PujaInline(admin.TabularInline):
    model = models.Puja
    extra = 0
    readonly_fields = ('fecha_puja',)
    verbose_name = "Puja"
    verbose_name_plural = "Pujas de la Subasta"


@admin.register(models.Subasta)
class SubastaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'precio_inicial', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio', 'fecha_fin')
    search_fields = ('vehiculo__marca__nombre', 'vehiculo__modelo__nombre')
    raw_id_fields = ('vehiculo',)
    inlines = [PujaInline]


@admin.register(models.Puja)
class PujaAdmin(admin.ModelAdmin):
    list_display = ('id', 'subasta', 'usuario', 'monto', 'fecha_puja')
    list_filter = ('fecha_puja',)
    search_fields = ('usuario__nombre', 'usuario__apellido', 'subasta__vehiculo__marca__nombre')
    raw_id_fields = ('subasta', 'usuario')


@admin.register(models.Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'vendedor', 'comprador', 'precio_final', 'metodo_pago', 'estado', 'fecha_venta')
    list_filter = ('estado', 'metodo_pago', 'fecha_venta')
    search_fields = ('vehiculo__marca__nombre', 'vehiculo__modelo__nombre', 'comprador__nombre', 'vendedor__nombre')
    raw_id_fields = ('vehiculo', 'comprador', 'vendedor')


@admin.register(models.SolicitudVerificacion)
class SolicitudVerificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'usuario', 'estado', 'fecha_solicitud', 'fecha_respuesta')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('vehiculo__marca__nombre', 'usuario__nombre', 'usuario__apellido')
    raw_id_fields = ('vehiculo', 'usuario')


@admin.register(models.Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_documento', 'vehiculo', 'usuario', 'estado', 'fecha_subida')
    list_filter = ('estado', 'tipo_documento', 'fecha_subida')
    search_fields = ('tipo_documento', 'usuario__nombre', 'vehiculo__marca__nombre', 'comentario_admin')
    raw_id_fields = ('usuario', 'vehiculo')


@admin.register(models.LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'accion', 'fecha', 'ip')
    list_filter = ('fecha', 'accion')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'accion', 'ip')
    raw_id_fields = ('usuario',)


@admin.register(models.Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'descripcion', 'telefono', 'direccion')
    search_fields = ('usuario__nombre', 'usuario__apellido',)
    raw_id_fields = ('usuario',)

