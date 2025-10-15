from rest_framework import serializers
from venta.models import LogActividad


class LogActividadSerializer(serializers.ModelSerializer):
    """Serializer para el modelo LogActividad"""
    
    usuario_nombre_completo = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LogActividad
        fields = [
            'id',
            'usuario',
            'usuario_nombre_completo',
            'accion',
            'fecha',
            'ip',
        ]
        read_only_fields = ['fecha']
    
    def get_usuario_nombre_completo(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"

