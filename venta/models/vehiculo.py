from django.db import models


class Vehiculo(models.Model):
    usuario = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='vehiculos',
        help_text='Usuario propietario del vehículo'
    )
    marca = models.ForeignKey(
        'venta.Marca',
        on_delete=models.PROTECT,
        related_name='vehiculos',
        help_text='Marca del vehículo'
    )
    modelo = models.ForeignKey(
        'venta.Modelo',
        on_delete=models.PROTECT,
        related_name='vehiculos',
        help_text='Modelo del vehículo'
    )
    año = models.IntegerField(
        help_text='Año del vehículo'
    )
    precio = models.IntegerField(
        help_text='Precio del vehículo'
    )
    tipo_transmision = models.CharField(
        max_length=60,
        help_text='Tipo de transmisión'
    )
    tipo_combustible = models.CharField(
        max_length=60,
        help_text='Tipo de combustible'
    )
    kilometraje = models.IntegerField(
        help_text='Kilometraje del vehículo'
    )
    descripcion = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text='Descripción del vehículo'
    )
    estado = models.CharField(
        max_length=20,
        default='disponible',
        help_text='Estado del vehículo'
    )
    fecha_publicacion = models.DateField(
        auto_now_add=True,
        help_text='Fecha de publicación'
    )
    tipo_vehiculo = models.CharField(
        max_length=60,
        default='Automovil',
        help_text='Tipo de vehículo (auto, moto, etc.)'
    )
    ubicacion = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Ubicación del vehículo',
        db_index=True
    )

    class Meta:
        db_table = 'vehiculos'
        ordering = ['-fecha_publicacion']
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        indexes = [
            models.Index(fields=['ubicacion']),
            models.Index(fields=['precio']),
            models.Index(fields=['año']),
            models.Index(fields=['marca', 'modelo']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo.nombre} {self.año}"

