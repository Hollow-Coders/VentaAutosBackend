from rest_framework import serializers
from venta.models.puja import Puja


class PujaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Puja"""
    
    usuario_nombre_completo = serializers.SerializerMethodField(read_only=True)
    subasta_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Puja
        fields = [
            'id',
            'subasta',
            'subasta_info',
            'usuario',
            'usuario_nombre_completo',
            'monto',
            'fecha_puja',
        ]
        read_only_fields = ['fecha_puja']
    
    def get_usuario_nombre_completo(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"
    
    def get_subasta_info(self, obj):
        """Retorna información básica de la subasta"""
        vehiculo = obj.subasta.vehiculo
        return f"Subasta #{obj.subasta.id} - {vehiculo.marca.nombre} {vehiculo.modelo.nombre}"

