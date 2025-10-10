from django.db import models


class Venta(models.Model):
    vehiculo = models.ForeignKey(
        'venta.Vehiculo',
        on_delete=models.CASCADE,
        related_name='ventas',
        help_text='Vehículo vendido'
    )
    comprador = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.PROTECT,
        related_name='compras',
        help_text='Comprador del vehículo'
    )
    vendedor = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.PROTECT,
        related_name='ventas_realizadas',
        help_text='Vendedor del vehículo'
    )
    fecha_venta = models.DateField(
        help_text='Fecha de la venta'
    )
    precio_final = models.IntegerField(
        help_text='Precio final de la venta'
    )
    metodo_pago = models.CharField(
        max_length=20,
        help_text='Método de pago'
    )
    estado = models.CharField(
        max_length=20,
        default='pendiente',
        help_text='Estado de la venta'
    )

    class Meta:
        db_table = 'ventas'
        ordering = ['-fecha_venta']
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Venta {self.pk} - {self.vehiculo}"

