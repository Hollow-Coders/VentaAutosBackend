from django.db import models


class Mensaje(models.Model):
    """
    Modelo para representar un mensaje en una conversación
    """
    conversacion = models.ForeignKey(
        'venta.Conversacion',
        on_delete=models.CASCADE,
        related_name='mensajes',
        help_text='Conversación a la que pertenece el mensaje'
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
    fecha_lectura = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha y hora en que se leyó el mensaje'
    )

    class Meta:
        db_table = 'mensajes'
        ordering = ['fecha_envio']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"Mensaje de {self.remitente} en conversación {self.conversacion.id}"

    def marcar_como_leido(self):
        """
        Marca el mensaje como leído
        """
        from django.utils import timezone
        if not self.leido:
            self.leido = True
            self.fecha_lectura = timezone.now()
            self.save()

