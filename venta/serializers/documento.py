from rest_framework import serializers
from venta.models import Documento


class DocumentoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Documento"""
    
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    usuario_apellido = serializers.CharField(source='usuario.apellido', read_only=True)
    vehiculo_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Documento
        fields = [
            'id',
            'usuario',
            'usuario_nombre',
            'usuario_apellido',
            'vehiculo',
            'vehiculo_info',
            'tipo_documento',
            'archivo_url',
            'fecha_subida',
            'estado',
            'comentario_admin',
        ]
        read_only_fields = ['fecha_subida']
    
    def get_vehiculo_info(self, obj):
        """Retorna información básica del vehículo"""
        return f"{obj.vehiculo.marca.nombre} {obj.vehiculo.modelo.nombre} {obj.vehiculo.año}"

