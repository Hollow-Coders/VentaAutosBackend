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
            'fotos',
            'total_documentos',
        ]
        read_only_fields = ['fecha_publicacion']
    
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
        return obj.documentos.count()

