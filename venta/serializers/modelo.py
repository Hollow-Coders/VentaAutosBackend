from rest_framework import serializers
from venta.models.modelo import Modelo


class ModeloSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Modelo"""
    
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    total_vehiculos = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Modelo
        fields = [
            'id',
            'marca',
            'marca_nombre',
            'nombre',
            'total_vehiculos',
        ]
    
    def get_total_vehiculos(self, obj):
        """Retorna el total de vehículos del modelo"""
        return obj.vehiculos.count()

