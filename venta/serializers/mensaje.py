from rest_framework import serializers
from venta.models import Mensaje


class MensajeSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Mensaje"""
    
    remitente_nombre = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Mensaje
        fields = ['id', 'venta', 'remitente', 'remitente_nombre', 'contenido', 'fecha_envio', 'leido']
        read_only_fields = ['remitente', 'fecha_envio', 'leido']
    
    def get_remitente_nombre(self, obj):
        """Retorna el nombre completo del remitente"""
        if obj.remitente.nombre_completo:
            return obj.remitente.nombre_completo
        return f"{obj.remitente.nombre} {obj.remitente.apellido}"
    
    def validate_contenido(self, value):
        """Valida el contenido del mensaje"""
        contenido_limpio = value.strip()
        if not contenido_limpio:
            raise serializers.ValidationError("El contenido del mensaje no puede estar vacío")
        if len(contenido_limpio) > 5000:
            raise serializers.ValidationError("El contenido del mensaje no puede exceder 5000 caracteres")
        return contenido_limpio

