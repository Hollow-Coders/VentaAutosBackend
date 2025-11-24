from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Valoracion(models.Model):
    venta = models.ForeignKey(
        'venta.Venta',
        on_delete=models.CASCADE,
        related_name='valoraciones',
        help_text='Venta que se está valorando'
    )
    comprador = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.PROTECT,
        related_name='valoraciones_realizadas',
        help_text='Comprador que realiza la valoración'
    )
    calificacion = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text='Calificación de 0 a 5 (ej: 1.5, 4.5)'
    )
    comentario = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        help_text='Comentario sobre la venta'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación de la valoración'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text='Fecha de última actualización'
    )

    class Meta:
        db_table = 'valoraciones'
        ordering = ['-fecha_creacion']
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'
        # Asegurar que un comprador solo pueda valorar una venta una vez
        unique_together = ['venta', 'comprador']

    def __str__(self):
        return f"Valoración {self.calificacion}/5 - Venta {self.venta.pk} - {self.comprador}"

