from django.db import models


class Mensaje(models.Model):
    """
    Modelo para representar un mensaje en un chat entre comprador y vendedor sobre un vehículo.
    Cada conversación es única por la combinación de comprador, vendedor y vehículo.
    """
    # Campos principales para identificar la conversación
    comprador = models.ForeignKey(
        'venta.Usuario',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='mensajes_como_comprador',
        help_text='Usuario comprador en la conversación'
    )
    vendedor = models.ForeignKey(
        'venta.Usuario',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='mensajes_como_vendedor',
        help_text='Usuario vendedor en la conversación'
    )
    vehiculo = models.ForeignKey(
        'venta.Vehiculo',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='mensajes',
        help_text='Vehículo sobre el que se está conversando'
    )
    # Campo opcional para mantener compatibilidad con ventas existentes
    venta = models.ForeignKey(
        'venta.Venta',
        on_delete=models.CASCADE,
        related_name='mensajes',
        null=True,
        blank=True,
        help_text='Venta asociada (opcional, para compatibilidad con datos antiguos)'
    )
    remitente = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        help_text='Usuario que envió el mensaje (puede ser comprador o vendedor)'
    )
    contenido = models.TextField(
        help_text='Contenido del mensaje'
    )
    fecha_envio = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora de envío del mensaje'
    )
    leido = models.BooleanField(
        default=False,
        help_text='Indica si el mensaje ha sido leído'
    )

    class Meta:
        db_table = 'mensajes'
        ordering = ['fecha_envio']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        indexes = [
            models.Index(fields=['comprador', 'vendedor', 'vehiculo']),
            models.Index(fields=['fecha_envio']),
            models.Index(fields=['remitente']),
        ]

    def __str__(self):
        if self.venta:
            return f"Mensaje de {self.remitente} en venta {self.venta.id}"
        return f"Mensaje de {self.remitente} sobre vehículo {self.vehiculo.id}"

