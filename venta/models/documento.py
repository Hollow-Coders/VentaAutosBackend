from django.db import models


class Documento(models.Model):
    usuario = models.ForeignKey(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='documentos',
        help_text='Usuario dueño del documento'
    )
    vehiculo = models.ForeignKey(
        'venta.Vehiculo',
        on_delete=models.CASCADE,
        related_name='documentos',
        help_text='Vehículo asociado al documento'
    )
    tipo_documento = models.CharField(
        max_length=50,
        help_text='Tipo de documento'
    )
    archivo_url = models.CharField(
        max_length=150,
        help_text='URL del archivo'
    )
    fecha_subida = models.DateField(
        auto_now_add=True,
        help_text='Fecha de subida'
    )
    estado = models.CharField(
        max_length=20,
        default='pendiente',
        help_text='Estado del documento'
    )
    comentario_admin = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Comentario del administrador'
    )

    class Meta:
        db_table = 'documentos'
        ordering = ['-fecha_subida']
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return f"{self.tipo_documento} - {self.vehiculo}"

