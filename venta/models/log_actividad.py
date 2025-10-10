from django.db import models


class LogActividad(models.Model):
    usuario = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='logs',
        help_text='Usuario que realizó la acción'
    )
    accion = models.CharField(
        max_length=60,
        help_text='Acción realizada'
    )
    fecha = models.DateField(
        auto_now_add=True,
        help_text='Fecha de la acción'
    )
    ip = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        help_text='Dirección IP'
    )

    class Meta:
        db_table = 'logs_actividad'
        ordering = ['-fecha']
        verbose_name = 'Log de Actividad'
        verbose_name_plural = 'Logs de Actividad'

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha}"

