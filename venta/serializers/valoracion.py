from rest_framework import serializers
from venta.models import Valoracion


class ValoracionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Valoracion"""
    
    comprador_nombre = serializers.SerializerMethodField(read_only=True)
    vendedor_nombre = serializers.SerializerMethodField(read_only=True)
    vehiculo_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Valoracion
        fields = [
            'id',
            'venta',
            'comprador',
            'comprador_nombre',
            'vendedor_nombre',
            'vehiculo_info',
            'calificacion',
            'comentario',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = ['comprador', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_comprador_nombre(self, obj):
        """Retorna el nombre completo del comprador"""
        return f"{obj.comprador.nombre} {obj.comprador.apellido}"
    
    def get_vendedor_nombre(self, obj):
        """Retorna el nombre completo del vendedor"""
        return f"{obj.venta.vendedor.nombre} {obj.venta.vendedor.apellido}"
    
    def get_vehiculo_info(self, obj):
        """Retorna información básica del vehículo"""
        vehiculo = obj.venta.vehiculo
        return {
            'id': vehiculo.id,
            'marca': vehiculo.marca.nombre,
            'modelo': vehiculo.modelo.nombre,
            'año': vehiculo.año,
        }

