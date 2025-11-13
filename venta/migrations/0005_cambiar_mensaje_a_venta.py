# Generated manually for changing Mensaje model from Conversacion to Venta

import django.db.models.deletion
from django.db import migrations, models


def migrar_mensajes_a_ventas(apps, schema_editor):
    """
    Migra los mensajes existentes de conversacion a venta.
    Si un mensaje tiene conversacion con venta asociada, usa esa venta.
    Si no tiene venta, intenta encontrar una venta relacionada o elimina el mensaje.
    """
    Mensaje = apps.get_model('venta', 'Mensaje')
    Conversacion = apps.get_model('venta', 'Conversacion')
    
    # Para cada mensaje, intentar obtener la venta desde la conversación
    for mensaje in Mensaje.objects.all():
        if mensaje.conversacion and mensaje.conversacion.venta:
            mensaje.venta_id = mensaje.conversacion.venta_id
            mensaje.save(update_fields=['venta_id'])
        else:
            # Si no hay venta asociada, eliminar el mensaje (o podrías crear una venta dummy)
            mensaje.delete()


def revertir_migracion(apps, schema_editor):
    """
    Revertir la migración no es posible sin perder datos,
    así que simplemente dejamos los mensajes sin conversación
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0004_alter_perfil_foto_perfil_and_more'),
    ]

    operations = [
        # Primero agregar el campo venta como nullable
        migrations.AddField(
            model_name='mensaje',
            name='venta',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes',
                to='venta.venta',
                help_text='Venta a la que pertenece el mensaje'
            ),
        ),
        # Migrar los datos
        migrations.RunPython(migrar_mensajes_a_ventas, revertir_migracion),
        # Hacer el campo venta no nullable
        migrations.AlterField(
            model_name='mensaje',
            name='venta',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mensajes',
                to='venta.venta',
                help_text='Venta a la que pertenece el mensaje'
            ),
        ),
        # Eliminar campos antiguos
        migrations.RemoveField(
            model_name='mensaje',
            name='conversacion',
        ),
        migrations.RemoveField(
            model_name='mensaje',
            name='fecha_lectura',
        ),
        # Agregar índice
        migrations.AddIndex(
            model_name='mensaje',
            index=models.Index(fields=['venta', 'fecha_envio'], name='mensajes_venta_i_c01638_idx'),
        ),
    ]

