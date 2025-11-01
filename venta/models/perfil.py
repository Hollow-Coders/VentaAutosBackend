from django.db import models


class Perfil(models.Model):
    usuario = models.OneToOneField(
        'venta.Usuario',
        on_delete=models.CASCADE,
        related_name='perfil',
        help_text='Usuario asociado al perfil'
    )
    descripcion = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        help_text='Descripción del perfil del usuario'
    )
    telefono = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='Teléfono de contacto'
    )
    direccion = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Dirección del usuario'
    )
    ciudad = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Ciudad donde reside el usuario'
    )
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        help_text='Foto de perfil del usuario'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text='Fecha de última actualización del perfil'
    )

    class Meta:
        db_table = 'perfiles'
        ordering = ['usuario']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        indexes = [
            models.Index(fields=['usuario']),
        ]

    def __str__(self):
        return f"Perfil de {self.usuario.nombre} {self.usuario.apellido}"

