from django.db import models


class Puja(models.Model):
    subasta = models.ForeignKey(
        'venta.Subasta',
        on_delete=models.CASCADE,
        related_name='pujas',
        help_text='Subasta de la puja'
    )
    usuario = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='pujas',
        help_text='Usuario que realizó la puja'
    )
    monto = models.IntegerField(
        help_text='Monto de la puja'
    )
    fecha_puja = models.DateField(
        auto_now_add=True,
        help_text='Fecha de la puja'
    )

    class Meta:
        db_table = 'pujas'
        ordering = ['-fecha_puja']
        verbose_name = 'Puja'
        verbose_name_plural = 'Pujas'

    def __str__(self):
        return f"Puja {self.pk} - {self.usuario} - ${self.monto}"

