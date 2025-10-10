from django.db import models


class Rol(models.Model):
    nombre = models.CharField(
        max_length=60,
        help_text='Nombre del rol'
    )
    descripcion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Descripción del rol'
    )

    class Meta:
        db_table = 'roles'
        ordering = ['pk']
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return f"{self.nombre}"

