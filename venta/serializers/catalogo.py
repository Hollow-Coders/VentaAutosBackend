from rest_framework import serializers
from venta.models import Vehiculo


class CatalogoSerializer(serializers.ModelSerializer):
    """Serializer optimizado para el catálogo de vehículos"""
    
    nombre = serializers.SerializerMethodField()
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    modelo_nombre = serializers.CharField(source='modelo.nombre', read_only=True)
    
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
        ]
    
    def get_nombre(self, obj):
        """Retorna el nombre completo del vehículo"""
        return f"{obj.marca.nombre} {obj.modelo.nombre} {obj.año}"

