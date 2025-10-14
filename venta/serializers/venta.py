from rest_framework import serializers
from venta.models.venta import Venta


class VentaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Venta"""
    
    vehiculo_info = serializers.SerializerMethodField(read_only=True)
    comprador_nombre = serializers.SerializerMethodField(read_only=True)
    vendedor_nombre = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id',
            'vehiculo',
            'vehiculo_info',
            'comprador',
            'comprador_nombre',
            'vendedor',
            'vendedor_nombre',
            'fecha_venta',
            'precio_final',
            'metodo_pago',
            'estado',
        ]
    
    def get_vehiculo_info(self, obj):
        """Retorna información básica del vehículo"""
        vehiculo = obj.vehiculo
        return {
            'marca': vehiculo.marca.nombre,
            'modelo': vehiculo.modelo.nombre,
            'año': vehiculo.año,
        }
    
    def get_comprador_nombre(self, obj):
        """Retorna el nombre completo del comprador"""
        return f"{obj.comprador.nombre} {obj.comprador.apellido}"
    
    def get_vendedor_nombre(self, obj):
        """Retorna el nombre completo del vendedor"""
        return f"{obj.vendedor.nombre} {obj.vendedor.apellido}"

