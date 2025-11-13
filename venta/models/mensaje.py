from django.db import models


class Mensaje(models.Model):
    """
    Modelo para representar un mensaje en una venta
    """
    venta = models.ForeignKey(
        'venta.Venta',
        on_delete=models.CASCADE,
        related_name='mensajes',
        help_text='Venta a la que pertenece el mensaje'
    )
    remitente = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        help_text='Usuario que envió el mensaje'
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
            models.Index(fields=['venta', 'fecha_envio']),
        ]

    def __str__(self):
        return f"Mensaje de {self.remitente} en venta {self.venta.id}"

