from rest_framework import serializers
from venta.models.rol import Rol


class RolSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Rol"""
    
    total_usuarios = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Rol
        fields = [
            'id',
            'nombre',
            'descripcion',
            'total_usuarios',
        ]
    
    def get_total_usuarios(self, obj):
        """Retorna el total de usuarios con este rol"""
        return obj.usuarios.count()

