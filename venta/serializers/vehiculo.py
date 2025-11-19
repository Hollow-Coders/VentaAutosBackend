from rest_framework import serializers
from venta.models import Vehiculo
from django.conf import settings


class VehiculoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Vehiculo"""
    
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    modelo_nombre = serializers.CharField(source='modelo.nombre', read_only=True)
    usuario_nombre = serializers.SerializerMethodField(read_only=True)
    fotos = serializers.SerializerMethodField(read_only=True)
    total_documentos = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'usuario',
            'usuario_nombre',
            'marca',
            'marca_nombre',
            'modelo',
            'modelo_nombre',
            'año',
            'precio',
            'ubicacion',
            'tipo_transmision',
            'tipo_combustible',
            'kilometraje',
            'descripcion',
            'estado',
            'fecha_publicacion',
            'tipo_vehiculo',
            'fotos',
            'total_documentos',
        ]
        read_only_fields = ['fecha_publicacion', 'tipo_vehiculo']
    
    def get_usuario_nombre(self, obj):
        """Retorna el nombre completo del usuario propietario"""
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"
    
    def get_fotos(self, obj):
        """Retorna las URLs completas de las fotos del vehículo"""
        request = self.context.get('request')
        fotos = []
        for foto in obj.fotos.all():
            if foto.url_imagen:
                if request:
                    fotos.append(request.build_absolute_uri(foto.url_imagen.url))
                else:
                    fotos.append(f"{settings.MEDIA_URL}{foto.url_imagen.url}")
        return fotos
    
    def get_total_documentos(self, obj):
        """Retorna el total de documentos del vehículo"""
        total = getattr(obj, 'total_documentos_annotated', None)
        if total is not None:
            return total
        return obj.documentos.count()
    
    def create(self, validated_data):
        """Crea un vehículo y asigna automáticamente el tipo_vehiculo desde el modelo"""
        # Obtener el modelo para acceder a su tipo_vehiculo
        modelo = validated_data.get('modelo')
        if modelo:
            # Obtener la descripción del tipo de vehículo del modelo
            tipo_vehiculo_descripcion = modelo.tipo_vehiculo.descripcion
            # Asignar la descripción al campo tipo_vehiculo del vehículo
            validated_data['tipo_vehiculo'] = tipo_vehiculo_descripcion
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Actualiza un vehículo y actualiza el tipo_vehiculo si cambia el modelo"""
        # Si se actualiza el modelo, actualizar también el tipo_vehiculo
        modelo = validated_data.get('modelo', instance.modelo)
        if modelo:
            tipo_vehiculo_descripcion = modelo.tipo_vehiculo.descripcion
            validated_data['tipo_vehiculo'] = tipo_vehiculo_descripcion
        
        return super().update(instance, validated_data)

