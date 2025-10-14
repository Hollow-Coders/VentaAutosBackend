from rest_framework import serializers
from venta.models.marca import Marca


class MarcaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Marca"""
    
    total_modelos = serializers.SerializerMethodField(read_only=True)
    total_vehiculos = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Marca
        fields = [
            'id',
            'nombre',
            'total_modelos',
            'total_vehiculos',
        ]
    
    def get_total_modelos(self, obj):
        """Retorna el total de modelos de la marca"""
        return obj.modelos.count()
    
    def get_total_vehiculos(self, obj):
        """Retorna el total de vehículos de la marca"""
        return obj.vehiculos.count()

