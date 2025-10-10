from django.db import models


class Subasta(models.Model):
    vehiculo = models.ForeignKey(
        'venta.Vehiculo',
        on_delete=models.CASCADE,
        related_name='subastas',
        help_text='Vehículo en subasta'
    )
    precio_inicial = models.IntegerField(
        help_text='Precio inicial de la subasta'
    )
    fecha_inicio = models.DateField(
        help_text='Fecha de inicio de la subasta'
    )
    fecha_fin = models.DateField(
        help_text='Fecha de fin de la subasta'
    )
    estado = models.CharField(
        max_length=20,
        default='activa',
        help_text='Estado de la subasta'
    )

    class Meta:
        db_table = 'subastas'
        ordering = ['-fecha_inicio']
        verbose_name = 'Subasta'
        verbose_name_plural = 'Subastas'

    def __str__(self):
        return f"Subasta {self.pk} - {self.vehiculo}"

