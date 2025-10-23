from rest_framework import serializers
from venta.models import Usuario
from django.contrib.auth.hashers import make_password, check_password
import jwt
from datetime import  timedelta
from django.utils import timezone
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'contrasena', 'rol']
        extra_kwargs = {
            'contrasena': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['contrasena'] = make_password(validated_data['contrasena'])
        usuario = Usuario.objects.create(**validated_data)
        return usuario

class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    contrasena = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        try:
            usuario = Usuario.objects.get(correo=data['correo'])
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Correo o contraseña incorrectos")

        if not check_password(data['contrasena'], usuario.contrasena):
            raise serializers.ValidationError("Correo o contraseña incorrectos")

        payload = {
            'usuario_id': usuario.id,
            'exp': int((timezone.now() + timedelta(days=1)).timestamp())
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        data['token'] = token
        return data
