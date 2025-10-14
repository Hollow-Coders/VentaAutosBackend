from rest_framework import serializers
from venta.models.solicitud_verificacion import SolicitudVerificacion


class SolicitudVerificacionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo SolicitudVerificacion"""
    
    vehiculo_info = serializers.SerializerMethodField(read_only=True)
    usuario_nombre_completo = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = SolicitudVerificacion
        fields = [
            'id',
            'vehiculo',
            'vehiculo_info',
            'usuario',
            'usuario_nombre_completo',
            'estado',
            'fecha_solicitud',
            'fecha_respuesta',
        ]
        read_only_fields = ['fecha_solicitud']
    
    def get_vehiculo_info(self, obj):
        """Retorna información básica del vehículo"""
        return f"{obj.vehiculo.marca.nombre} {obj.vehiculo.modelo.nombre} {obj.vehiculo.año}"
    
    def get_usuario_nombre_completo(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"

