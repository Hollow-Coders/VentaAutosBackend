from rest_framework import serializers
from venta.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    nombre_completo = serializers.SerializerMethodField(read_only=True)
    total_vehiculos = serializers.SerializerMethodField(read_only=True)
    total_compras = serializers.SerializerMethodField(read_only=True)
    total_ventas = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id',
            'nombre',
            'apellido',
            'nombre_completo',
            'correo',
            'fecha_creacion',
            'estado',
            'rol',
            'rol_nombre',
            'total_vehiculos',
            'total_compras',
            'total_ventas',
        ]
        read_only_fields = ['fecha_creacion']
    
    def get_nombre_completo(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.nombre} {obj.apellido}"
    
    def get_total_vehiculos(self, obj):
        """Retorna el total de vehículos del usuario"""
        return obj.vehiculos.count()
    
    def get_total_compras(self, obj):
        """Retorna el total de compras del usuario"""
        return obj.compras.count()
    
    def get_total_ventas(self, obj):
        """Retorna el total de ventas realizadas por el usuario"""
        return obj.ventas_realizadas.count()

