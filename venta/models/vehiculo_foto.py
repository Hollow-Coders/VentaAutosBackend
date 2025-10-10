from django.db import models


class VehiculoFoto(models.Model):
    vehiculo = models.ForeignKey(
        'venta.Vehiculo',
        on_delete=models.CASCADE,
        related_name='fotos',
        help_text='Vehículo de la foto'
    )
    url_imagen = models.CharField(
        max_length=150,
        help_text='URL de la imagen'
    )

    class Meta:
        db_table = 'vehiculo_fotos'
        ordering = ['pk']
        verbose_name = 'Foto de Vehículo'
        verbose_name_plural = 'Fotos de Vehículos'

    def __str__(self):
        return f"Foto {self.pk} - {self.vehiculo}"

