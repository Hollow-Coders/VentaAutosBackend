from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from venta.models import Usuario
from venta.serializers.auth import RegisterSerializer, LoginSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        correo = serializer.validated_data['correo']
        contrasena = serializer.validated_data['contrasena']

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({"error": "Correo o contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(contrasena, usuario.contrasena):
            return Response({"error": "Correo o contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(usuario)
        return Response({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "correo": usuario.correo,
            "access": str(refresh.access_token)
        })
    
