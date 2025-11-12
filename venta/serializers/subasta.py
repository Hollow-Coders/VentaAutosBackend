from rest_framework import serializers
from venta.models import Subasta


class SubastaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Subasta"""
    
    vehiculo_info = serializers.SerializerMethodField(read_only=True)
    total_pujas = serializers.SerializerMethodField(read_only=True)
    precio_actual = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Subasta
        fields = [
            'id',
            'vehiculo',
            'vehiculo_info',
            'precio_inicial',
            'precio_actual',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'total_pujas',
        ]
    
    def get_vehiculo_info(self, obj):
        """Retorna información básica del vehículo"""
        vehiculo = obj.vehiculo
        return {
            'marca': vehiculo.marca.nombre,
            'modelo': vehiculo.modelo.nombre,
            'año': vehiculo.año,
            'descripcion': vehiculo.descripcion,
        }
    
    def get_total_pujas(self, obj):
        """Retorna el total de pujas"""
        total = getattr(obj, 'total_pujas_annotated', None)
        if total is not None:
            return total
        return obj.pujas.count()
    
    def get_precio_actual(self, obj):
        """Retorna el precio actual (la puja más alta)"""
        precio = getattr(obj, 'precio_actual_annotated', None)
        if precio is not None:
            return precio
        ultima_puja = obj.pujas.order_by('-monto').first()
        return ultima_puja.monto if ultima_puja else obj.precio_inicial

