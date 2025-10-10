from django.db import models


class SolicitudVerificacion(models.Model):
    vehiculo = models.ForeignKey(
        'venta.Vehiculo',
        on_delete=models.CASCADE,
        related_name='solicitudes_verificacion',
        help_text='Vehículo a verificar'
    )
    usuario = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='solicitudes_verificacion',
        help_text='Usuario que solicita la verificación'
    )
    estado = models.CharField(
        max_length=20,
        default='pendiente',
        help_text='Estado de la solicitud'
    )
    fecha_solicitud = models.DateField(
        auto_now_add=True,
        help_text='Fecha de solicitud'
    )
    fecha_respuesta = models.DateField(
        null=True,
        blank=True,
        help_text='Fecha de respuesta'
    )

    class Meta:
        db_table = 'solicitudes_verificacion'
        ordering = ['-fecha_solicitud']
        verbose_name = 'Solicitud de Verificación'
        verbose_name_plural = 'Solicitudes de Verificación'

    def __str__(self):
        return f"Solicitud {self.pk} - {self.vehiculo} - {self.estado}"

