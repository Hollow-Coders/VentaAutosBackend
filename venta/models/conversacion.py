from django.db import models


class Conversacion(models.Model):
    """
    Modelo para representar una conversación asociada a una venta específica
    Cada venta tiene su propia conversación única
    """
    venta = models.OneToOneField(
        'venta.Venta',
        on_delete=models.CASCADE,
        related_name='conversacion',
        help_text='Venta asociada a esta conversación',
        null=True,
        blank=True
    )
    vendedor = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='conversaciones_como_vendedor',
        help_text='Vendedor de la conversación'
    )
    comprador = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='conversaciones_como_comprador',
        help_text='Comprador de la conversación'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación de la conversación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text='Fecha de última actualización de la conversación'
    )
    activa = models.BooleanField(
        default=True,
        help_text='Indica si la conversación está activa'
    )

    class Meta:
        db_table = 'conversaciones'
        ordering = ['-fecha_actualizacion']
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'

    def __str__(self):
        return f"Conversación de venta {self.venta.id} - {self.vendedor} y {self.comprador}"

    def get_otro_usuario(self, usuario):
        """
        Retorna el otro usuario de la conversación
        """
        if usuario == self.vendedor:
            return self.comprador
        return self.vendedor

