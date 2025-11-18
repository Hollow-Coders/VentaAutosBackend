from django.db import models


class Modelo(models.Model):
    marca = models.ForeignKey(
        'venta.Marca',
        on_delete=models.CASCADE,
        related_name='modelos',
        help_text='Marca del modelo'
    )
    nombre = models.CharField(
        max_length=45,
        help_text='Nombre del modelo'
    )
    tipo_vehiculo = models.ForeignKey(
        'venta.TipoDeVehiculo',
        on_delete=models.PROTECT,
        related_name='modelos',
        help_text='Tipo de vehículo del modelo'
    )

    class Meta:
        db_table = 'modelos'
        ordering = ['nombre']
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        unique_together = ['marca', 'nombre']

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"

