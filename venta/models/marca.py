from django.db import models


class Marca(models.Model):
    nombre = models.CharField(
        max_length=60,
        unique=True,
        help_text='Nombre de la marca'
    )

    class Meta:
        db_table = 'marcas'
        ordering = ['nombre']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre

