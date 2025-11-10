from rest_framework import serializers
from venta.models import Mensaje


class MensajeSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Mensaje"""
    
    remitente_nombre = serializers.SerializerMethodField(read_only=True)
    conversacion_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Mensaje
        fields = [
            'id',
            'conversacion',
            'conversacion_info',
            'remitente',
            'remitente_nombre',
            'contenido',
            'fecha_envio',
        ]
        read_only_fields = ['fecha_envio']
    
    def get_remitente_nombre(self, obj):
        """Retorna el nombre completo del remitente"""
        return f"{obj.remitente.nombre} {obj.remitente.apellido}"
    
    def get_conversacion_info(self, obj):
        """Retorna información básica de la conversación"""
        return {
            'id': obj.conversacion.id,
            'vendedor': obj.conversacion.vendedor.id,
            'comprador': obj.conversacion.comprador.id,
        }


class MensajeCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear un nuevo mensaje"""
    
    class Meta:
        model = Mensaje
        fields = [
            'conversacion',
            'remitente',
            'contenido',
        ]
    
    def validate(self, data):
        """Valida que el remitente pertenezca a la conversación"""
        conversacion = data.get('conversacion')
        remitente = data.get('remitente')
        
        if conversacion and remitente:
            if remitente not in [conversacion.vendedor, conversacion.comprador]:
                raise serializers.ValidationError(
                    "El remitente debe ser el vendedor o comprador de la conversación"
                )
        
        return data

