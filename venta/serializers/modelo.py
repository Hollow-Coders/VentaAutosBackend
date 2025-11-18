from rest_framework import serializers
from venta.models import Modelo


class ModeloSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Modelo"""
    
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    tipo_vehiculo_descripcion = serializers.CharField(source='tipo_vehiculo.descripcion', read_only=True)
    total_vehiculos = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Modelo
        fields = [
            'id',
            'marca',
            'marca_nombre',
            'nombre',
            'tipo_vehiculo',
            'tipo_vehiculo_descripcion',
            'total_vehiculos',
        ]
    
    def get_total_vehiculos(self, obj):
        """Retorna el total de vehículos del modelo"""
        return obj.vehiculos.count()

