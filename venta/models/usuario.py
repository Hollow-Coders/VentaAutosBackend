from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(
        max_length=60,
        help_text='Nombre del usuario'
    )
    apellido = models.CharField(
        max_length=60,
        help_text='Apellido del usuario'
    )
    correo = models.EmailField(
        max_length=80,
        unique=True,
        help_text='Correo electrónico del usuario'
    )
    contrasena = models.CharField(
        max_length=128,
        help_text='Contraseña del usuario'
    )
    token = models.CharField(
        max_length=256,
        help_text='Token de sesion del usuario'
    )
    fecha_creacion = models.DateField(
        auto_now_add=True,
        help_text='Fecha de creación del usuario'
    )
    estado = models.CharField(
        max_length=20,
        default='activo',
        help_text='Estado del usuario'
    )
    rol = models.ForeignKey(
        'venta.Rol',
        on_delete=models.PROTECT,
        related_name='usuarios',
        help_text='Rol del usuario'
    )

    class Meta:
        db_table = 'usuarios'
        ordering = ['pk']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
