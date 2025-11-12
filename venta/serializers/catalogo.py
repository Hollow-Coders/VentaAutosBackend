from rest_framework import serializers
from django.conf import settings
from urllib.parse import urljoin
from venta.models import Vehiculo


class CatalogoSerializer(serializers.ModelSerializer):
    """Serializer optimizado para el catálogo de vehículos"""
    
    nombre = serializers.SerializerMethodField()
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    modelo_nombre = serializers.CharField(source='modelo.nombre', read_only=True)
    foto_principal = serializers.SerializerMethodField()

    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'nombre',
            'marca_nombre',
            'modelo_nombre',
            'año',
            'precio',
            'ubicacion',
            'foto_principal',
        ]
    
    def get_nombre(self, obj):
        """Retorna el nombre completo del vehículo"""
        return f"{obj.marca.nombre} {obj.modelo.nombre} {obj.año}"
    
    def get_foto_principal(self, obj):
        """Retorna la URL completa de la primera foto del vehículo"""
        foto_path = getattr(obj, 'foto_principal_path', None)
        if not foto_path:
            return None
        
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(urljoin(settings.MEDIA_URL, foto_path))
        
        return urljoin(settings.MEDIA_URL, foto_path)

