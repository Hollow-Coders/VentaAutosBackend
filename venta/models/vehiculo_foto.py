from django.db import models


class VehiculoFoto(models.Model):
    vehiculo = models.ForeignKey(
        'venta.Vehiculo',
        on_delete=models.CASCADE,
        related_name='fotos',
        help_text='Vehículo de la foto'
    )
    url_imagen = models.ImageField(
        upload_to='vehiculos/',
        null=True,
        blank=True,
        help_text='Imagen del vehículo'
    )

    class Meta:
        db_table = 'vehiculo_fotos'
        ordering = ['pk']
        verbose_name = 'Foto de Vehículo'
        verbose_name_plural = 'Fotos de Vehículos'

    def __str__(self):
        return f"Foto {self.pk} - {self.vehiculo}"

