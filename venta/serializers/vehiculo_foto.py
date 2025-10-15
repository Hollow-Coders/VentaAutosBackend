from rest_framework import serializers
from venta.models import VehiculoFoto


class VehiculoFotoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo VehiculoFoto"""
    
    vehiculo_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = VehiculoFoto
        fields = [
            'id',
            'vehiculo',
            'vehiculo_info',
            'url_imagen',
        ]
    
    def get_vehiculo_info(self, obj):
        """Retorna información básica del vehículo"""
        return f"{obj.vehiculo.marca.nombre} {obj.vehiculo.modelo.nombre} {obj.vehiculo.año}"

