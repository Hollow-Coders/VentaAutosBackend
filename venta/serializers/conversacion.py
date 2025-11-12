from rest_framework import serializers
from venta.models import Conversacion


class ConversacionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Conversacion"""
    
    vendedor_nombre = serializers.SerializerMethodField(read_only=True)
    comprador_nombre = serializers.SerializerMethodField(read_only=True)
    ultimo_mensaje = serializers.SerializerMethodField(read_only=True)
    cantidad_mensajes = serializers.SerializerMethodField(read_only=True)
    venta_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Conversacion
        fields = [
            'id',
            'venta',
            'venta_id',
            'vendedor',
            'vendedor_nombre',
            'comprador',
            'comprador_nombre',
            'fecha_creacion',
            'fecha_actualizacion',
            'activa',
            'ultimo_mensaje',
            'cantidad_mensajes',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_vendedor_nombre(self, obj):
        """Retorna el nombre completo del vendedor"""
        return f"{obj.vendedor.nombre} {obj.vendedor.apellido}"
    
    def get_comprador_nombre(self, obj):
        """Retorna el nombre completo del comprador"""
        return f"{obj.comprador.nombre} {obj.comprador.apellido}"
    
    def get_ultimo_mensaje(self, obj):
        """Retorna el último mensaje de la conversación"""
        mensaje_id = getattr(obj, 'ultimo_mensaje_id_annotated', None)
        if mensaje_id:
            return {
                'id': mensaje_id,
                'contenido': getattr(obj, 'ultimo_mensaje_contenido_annotated', None),
                'remitente': getattr(obj, 'ultimo_mensaje_remitente_id_annotated', None),
                'remitente_nombre': getattr(obj, 'ultimo_mensaje_remitente_nombre_annotated', None),
                'fecha_envio': getattr(obj, 'ultimo_mensaje_fecha_annotated', None),
            }
        
        ultimo_mensaje = obj.mensajes.last()
        if ultimo_mensaje:
            return {
                'id': ultimo_mensaje.id,
                'contenido': ultimo_mensaje.contenido,
                'remitente': ultimo_mensaje.remitente.id,
                'remitente_nombre': f"{ultimo_mensaje.remitente.nombre} {ultimo_mensaje.remitente.apellido}",
                'fecha_envio': ultimo_mensaje.fecha_envio,
            }
        return None
    
    def get_cantidad_mensajes(self, obj):
        """Retorna la cantidad total de mensajes en la conversación"""
        total = getattr(obj, 'total_mensajes_annotated', None)
        if total is not None:
            return total
        return obj.mensajes.count()
    
    def get_venta_id(self, obj):
        """Retorna el ID de la venta asociada"""
        return obj.venta.id if obj.venta else None

class ConversacionDetalleSerializer(serializers.ModelSerializer):
    """Serializer detallado para Conversacion que incluye todos los mensajes"""
    
    vendedor_nombre = serializers.SerializerMethodField(read_only=True)
    comprador_nombre = serializers.SerializerMethodField(read_only=True)
    mensajes = serializers.SerializerMethodField(read_only=True)
    venta_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Conversacion
        fields = [
            'id',
            'venta',
            'venta_id',
            'vendedor',
            'vendedor_nombre',
            'comprador',
            'comprador_nombre',
            'fecha_creacion',
            'fecha_actualizacion',
            'activa',
            'mensajes',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

    def get_vendedor_nombre(self, obj):
        """Retorna el nombre completo del vendedor"""
        return f"{obj.vendedor.nombre} {obj.vendedor.apellido}"
    
    def get_comprador_nombre(self, obj):
        """Retorna el nombre completo del comprador"""
        return f"{obj.comprador.nombre} {obj.comprador.apellido}"
    
    def get_mensajes(self, obj):
        """Retorna todos los mensajes de la conversación"""
        from venta.serializers.mensaje import MensajeSerializer
        mensajes = obj.mensajes.all()
        return MensajeSerializer(mensajes, many=True).data
    
    def get_venta_id(self, obj):
        """Retorna el ID de la venta asociada"""
        return obj.venta.id if obj.venta else None

