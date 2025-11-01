from rest_framework import serializers
from venta.models import VehiculoFoto
from django.conf import settings


class VehiculoFotoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo VehiculoFoto"""
    
    vehiculo_info = serializers.SerializerMethodField(read_only=True)
    url_imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = VehiculoFoto
        fields = [
            'id',
            'vehiculo',
            'vehiculo_info',
            'url_imagen',
            'url_imagen_url',
        ]
    
    def get_vehiculo_info(self, obj):
        """Retorna información básica del vehículo"""
        return f"{obj.vehiculo.marca.nombre} {obj.vehiculo.modelo.nombre} {obj.vehiculo.año}"
    
    def get_url_imagen_url(self, obj):
        """Retorna la URL completa de la imagen"""
        if obj.url_imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.url_imagen.url)
            return f"{settings.MEDIA_URL}{obj.url_imagen.url}"
        return None

