from django.db import models


class TipoDeVehiculo(models.Model):
    descripcion = models.CharField(
        max_length=60,
        unique=True,
        help_text='Descripción del tipo de vehículo (Automóvil, Motocicleta, etc.)'
    )

    class Meta:
        db_table = 'tipos_vehiculo'
        ordering = ['descripcion']
        verbose_name = 'Tipo de Vehículo'
        verbose_name_plural = 'Tipos de Vehículo'

    def __str__(self):
        return self.descripcion

