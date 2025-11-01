from rest_framework import serializers
from venta.models import Perfil
from django.conf import settings


class PerfilSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Perfil"""
    
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    usuario_apellido = serializers.CharField(source='usuario.apellido', read_only=True)
    usuario_correo = serializers.EmailField(source='usuario.correo', read_only=True)
    foto_perfil_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Perfil
        fields = [
            'id',
            'usuario',
            'usuario_nombre',
            'usuario_apellido',
            'usuario_correo',
            'descripcion',
            'telefono',
            'direccion',
            'ciudad',
            'foto_perfil',
            'foto_perfil_url',
            'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_actualizacion']
    
    def get_foto_perfil_url(self, obj):
        """Retorna la URL completa de la foto de perfil"""
        if obj.foto_perfil:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_perfil.url)
            return f"{settings.MEDIA_URL}{obj.foto_perfil.url}"
        return None

