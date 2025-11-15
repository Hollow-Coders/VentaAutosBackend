# Generated migration
from django.db import migrations, models
import django.db.models.deletion


def migrar_datos_mensajes(apps, schema_editor):
    """
    Migra los datos existentes de mensajes basados en venta
    a la nueva estructura con comprador, vendedor y vehiculo
    """
    Mensaje = apps.get_model('venta', 'Mensaje')
    Venta = apps.get_model('venta', 'Venta')
    
    # Para cada mensaje existente, obtener la venta y asignar comprador, vendedor y vehiculo
    for mensaje in Mensaje.objects.all():
        if mensaje.venta:
            mensaje.comprador = mensaje.venta.comprador
            mensaje.vendedor = mensaje.venta.vendedor
            mensaje.vehiculo = mensaje.venta.vehiculo
            mensaje.save()


def reverse_migrar_datos_mensajes(apps, schema_editor):
    """
    Función reversa: no podemos recuperar la venta original,
    así que simplemente no hacemos nada
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0005_cambiar_mensaje_a_venta'),
    ]

    operations = [
        # Paso 1: Agregar los nuevos campos como nullable temporalmente
        migrations.AddField(
            model_name='mensaje',
            name='comprador',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes_como_comprador',
                to='venta.usuario',
                help_text='Usuario comprador en la conversación'
            ),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='vendedor',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes_como_vendedor',
                to='venta.usuario',
                help_text='Usuario vendedor en la conversación'
            ),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='vehiculo',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes',
                to='venta.vehiculo',
                help_text='Vehículo sobre el que se está conversando'
            ),
        ),
        
        # Paso 2: Migrar los datos existentes
        migrations.RunPython(migrar_datos_mensajes, reverse_migrar_datos_mensajes),
        
        # Paso 3: Hacer los nuevos campos requeridos (no nullable)
        migrations.AlterField(
            model_name='mensaje',
            name='comprador',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes_como_comprador',
                to='venta.usuario',
                help_text='Usuario comprador en la conversación'
            ),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='vendedor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes_como_vendedor',
                to='venta.usuario',
                help_text='Usuario vendedor en la conversación'
            ),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='vehiculo',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes',
                to='venta.vehiculo',
                help_text='Vehículo sobre el que se está conversando'
            ),
        ),
        
        # Paso 4: Hacer venta nullable y opcional
        migrations.AlterField(
            model_name='mensaje',
            name='venta',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes',
                to='venta.venta',
                help_text='Venta asociada (opcional, para compatibilidad con datos antiguos)'
            ),
        ),
        
        # Paso 5: Eliminar el índice antiguo y agregar los nuevos
        migrations.RemoveIndex(
            model_name='mensaje',
            name='mensajes_venta_i_c01638_idx',
        ),
        migrations.AddIndex(
            model_name='mensaje',
            index=models.Index(fields=['comprador', 'vendedor', 'vehiculo'], name='mensajes_comprador_vendedor_vehiculo_idx'),
        ),
        migrations.AddIndex(
            model_name='mensaje',
            index=models.Index(fields=['fecha_envio'], name='mensajes_fecha_envio_idx'),
        ),
        migrations.AddIndex(
            model_name='mensaje',
            index=models.Index(fields=['remitente'], name='mensajes_remitente_idx'),
        ),
    ]

