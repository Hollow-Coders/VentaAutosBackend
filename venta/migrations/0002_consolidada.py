# Migración consolidada - Combina todas las migraciones desde 0002 hasta 0007

import django.db.models.deletion
from django.db import migrations, models


def migrar_datos_conversacion(apps, schema_editor):
    """
    Migra los datos de usuario1/usuario2 a vendedor/comprador
    Asume que usuario1 es vendedor y usuario2 es comprador
    """
    Conversacion = apps.get_model('venta', 'Conversacion')
    
    for conversacion in Conversacion.objects.all():
        # Solo migrar si tiene usuario1 y usuario2
        if hasattr(conversacion, 'usuario1_id') and hasattr(conversacion, 'usuario2_id'):
            conversacion.vendedor_id = conversacion.usuario1_id
            conversacion.comprador_id = conversacion.usuario2_id
            conversacion.save()


def revertir_migracion_conversacion(apps, schema_editor):
    """
    Revierte la migración asignando vendedor a usuario1 y comprador a usuario2
    """
    Conversacion = apps.get_model('venta', 'Conversacion')
    
    for conversacion in Conversacion.objects.all():
        if hasattr(conversacion, 'usuario1_id') and hasattr(conversacion, 'usuario2_id'):
            conversacion.usuario1_id = conversacion.vendedor_id
            conversacion.usuario2_id = conversacion.comprador_id
            conversacion.save()


def migrar_ventas_a_venta(apps, schema_editor):
    """
    Migra las ventas del ManyToMany a una sola venta en el OneToOneField
    Toma la primera venta asociada si hay múltiples
    """
    Conversacion = apps.get_model('venta', 'Conversacion')
    
    for conversacion in Conversacion.objects.all():
        # Obtener la primera venta asociada (si existe)
        # Verificar si el campo ventas existe antes de acceder
        if hasattr(conversacion, 'ventas'):
            ventas_asociadas = conversacion.ventas.all()
            if ventas_asociadas.exists():
                primera_venta = ventas_asociadas.first()
                conversacion.venta_id = primera_venta.id
                conversacion.save()


def revertir_migracion_ventas(apps, schema_editor):
    """
    Revierte la migración moviendo la venta de vuelta al ManyToMany
    """
    Conversacion = apps.get_model('venta', 'Conversacion')
    
    for conversacion in Conversacion.objects.all():
        if conversacion.venta:
            conversacion.ventas.add(conversacion.venta)


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
    ]

    operations = [
        # ========== De 0002: Agregar campos a Usuario ==========
        migrations.AddField(
            model_name='usuario',
            name='contrasena',
            field=models.CharField(help_text='Contraseña del usuario', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='token',
            field=models.CharField(help_text='Token de sesion del usuario', max_length=256),
            preserve_default=False,
        ),
        
        # ========== De 0003: Crear Perfil y agregar campos ==========
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, help_text='Descripción del perfil del usuario', max_length=500, null=True)),
                ('telefono', models.CharField(blank=True, help_text='Teléfono de contacto', max_length=20, null=True)),
                ('direccion', models.CharField(blank=True, help_text='Dirección del usuario', max_length=200, null=True)),
                ('ciudad', models.CharField(blank=True, help_text='Ciudad donde reside el usuario', max_length=100, null=True)),
                ('foto_perfil', models.URLField(blank=True, help_text='URL de la foto de perfil', max_length=500, null=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, help_text='Fecha de última actualización del perfil')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
                'db_table': 'perfiles',
                'ordering': ['usuario'],
            },
        ),
        migrations.AddField(
            model_name='usuario',
            name='nombre_completo',
            field=models.CharField(blank=True, help_text='Nombre concatenado del usuario', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='tipo_vehiculo',
            field=models.CharField(default='Automovil', help_text='Tipo de vehículo (auto, moto, etc.)', max_length=60),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='ubicacion',
            field=models.CharField(blank=True, db_index=True, help_text='Ubicación del vehículo', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(help_text='Apellido del usuario', max_length=150),
        ),
        migrations.AddIndex(
            model_name='vehiculo',
            index=models.Index(fields=['ubicacion'], name='vehiculos_ubicaci_1ade54_idx'),
        ),
        migrations.AddIndex(
            model_name='vehiculo',
            index=models.Index(fields=['precio'], name='vehiculos_precio_a25a0b_idx'),
        ),
        migrations.AddIndex(
            model_name='vehiculo',
            index=models.Index(fields=['año'], name='vehiculos_año_c0f846_idx'),
        ),
        migrations.AddIndex(
            model_name='vehiculo',
            index=models.Index(fields=['marca', 'modelo'], name='vehiculos_marca_i_405b56_idx'),
        ),
        migrations.AddIndex(
            model_name='vehiculo',
            index=models.Index(fields=['estado'], name='vehiculos_estado_bf04b7_idx'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(help_text='Usuario asociado al perfil', on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to='venta.usuario'),
        ),
        migrations.AddIndex(
            model_name='perfil',
            index=models.Index(fields=['usuario'], name='perfiles_usuario_e55d7c_idx'),
        ),
        
        # ========== De 0004: Alterar campos de Perfil y VehiculoFoto ==========
        migrations.AlterField(
            model_name='perfil',
            name='foto_perfil',
            field=models.ImageField(
                blank=True,
                help_text='Foto de perfil del usuario',
                null=True,
                upload_to='perfiles/',
            ),
        ),
        migrations.AlterField(
            model_name='vehiculofoto',
            name='url_imagen',
            field=models.ImageField(
                blank=True,
                help_text='Imagen del vehículo',
                null=True,
                upload_to='vehiculos/',
            ),
        ),
        
        # ========== De 0004: Crear Conversacion y Mensaje (con usuario1/usuario2) ==========
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha de creación de la conversación')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, help_text='Fecha de última actualización de la conversación')),
                ('activa', models.BooleanField(default=True, help_text='Indica si la conversación está activa')),
                ('usuario1', models.ForeignKey(help_text='Primer usuario de la conversación', on_delete=django.db.models.deletion.CASCADE, related_name='conversaciones_como_usuario1', to='venta.usuario')),
                ('usuario2', models.ForeignKey(help_text='Segundo usuario de la conversación', on_delete=django.db.models.deletion.CASCADE, related_name='conversaciones_como_usuario2', to='venta.usuario')),
            ],
            options={
                'verbose_name': 'Conversación',
                'verbose_name_plural': 'Conversaciones',
                'db_table': 'conversaciones',
                'ordering': ['-fecha_actualizacion'],
                'unique_together': {('usuario1', 'usuario2')},
            },
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField(help_text='Contenido del mensaje')),
                ('fecha_envio', models.DateTimeField(auto_now_add=True, help_text='Fecha y hora de envío del mensaje')),
                ('leido', models.BooleanField(default=False, help_text='Indica si el mensaje ha sido leído')),
                ('fecha_lectura', models.DateTimeField(blank=True, help_text='Fecha y hora en que se leyó el mensaje', null=True)),
                ('conversacion', models.ForeignKey(help_text='Conversación a la que pertenece el mensaje', on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to='venta.conversacion')),
                ('remitente', models.ForeignKey(help_text='Usuario que envió el mensaje', on_delete=django.db.models.deletion.CASCADE, related_name='mensajes_enviados', to='venta.usuario')),
            ],
            options={
                'verbose_name': 'Mensaje',
                'verbose_name_plural': 'Mensajes',
                'db_table': 'mensajes',
                'ordering': ['fecha_envio'],
            },
        ),
        
        # ========== De 0005: Migrar de usuario1/usuario2 a vendedor/comprador ==========
        # Paso 1: Agregar nuevos campos como nullable temporalmente
        migrations.AddField(
            model_name='conversacion',
            name='vendedor',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='conversaciones_como_vendedor_temp',
                to='venta.usuario',
                help_text='Vendedor de la conversación'
            ),
        ),
        migrations.AddField(
            model_name='conversacion',
            name='comprador',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='conversaciones_como_comprador_temp',
                to='venta.usuario',
                help_text='Comprador de la conversación'
            ),
        ),
        # Paso 2: Migrar los datos
        migrations.RunPython(migrar_datos_conversacion, revertir_migracion_conversacion),
        # Paso 3: Hacer los campos no nullable
        migrations.AlterField(
            model_name='conversacion',
            name='vendedor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='conversaciones_como_vendedor',
                to='venta.usuario',
                help_text='Vendedor de la conversación'
            ),
        ),
        migrations.AlterField(
            model_name='conversacion',
            name='comprador',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='conversaciones_como_comprador',
                to='venta.usuario',
                help_text='Comprador de la conversación'
            ),
        ),
        # Paso 4: Agregar relación ManyToMany con Venta (temporal)
        migrations.AddField(
            model_name='conversacion',
            name='ventas',
            field=models.ManyToManyField(
                blank=True,
                related_name='conversaciones',
                to='venta.venta',
                help_text='Ventas asociadas a esta conversación'
            ),
        ),
        # Paso 5: Eliminar unique_together antiguo
        migrations.AlterUniqueTogether(
            name='conversacion',
            unique_together=set(),
        ),
        # Paso 6: Eliminar campos antiguos
        migrations.RemoveField(
            model_name='conversacion',
            name='usuario1',
        ),
        migrations.RemoveField(
            model_name='conversacion',
            name='usuario2',
        ),
        
        # ========== De 0007: Cambiar de ManyToMany a OneToOneField ==========
        # Paso 1: Eliminar unique_together de vendedor/comprador (ya está hecho arriba)
        # Paso 2: Agregar campo venta como nullable temporalmente
        migrations.AddField(
            model_name='conversacion',
            name='venta',
            field=models.OneToOneField(
                blank=True,
                help_text='Venta asociada a esta conversación',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='conversacion',
                to='venta.venta',
            ),
        ),
        # Paso 3: Migrar datos del ManyToMany al OneToOneField
        migrations.RunPython(migrar_ventas_a_venta, revertir_migracion_ventas),
        # Paso 4: Eliminar el campo ManyToMany ventas
        migrations.RemoveField(
            model_name='conversacion',
            name='ventas',
        ),
    ]

