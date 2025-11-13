from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from django.utils import timezone

# models
from venta.models import Mensaje, Venta, Usuario

# serializers
from venta.serializers import MensajeSerializer

# filters
from venta.filters import MensajeFilter


def obtener_usuario_desde_request(request):
    """
    Obtiene el usuario desde el request.
    Intenta obtenerlo del token JWT del header Authorization, si no está disponible, 
    lo obtiene de usuario_id en query params o headers.
    """
    # Intentar obtener del usuario autenticado (si está configurado)
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    
    # Intentar obtener del token JWT en el header Authorization
    auth_header = request.META.get('HTTP_AUTHORIZATION', '') or request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            # Decodificar el token JWT con SECRET_KEY
            # SimpleJWT usa SECRET_KEY por defecto
            from django.conf import settings
            import jwt
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            usuario_id = decoded_token.get('usuario_id') or decoded_token.get('user_id')
            if usuario_id:
                try:
                    return Usuario.objects.get(id=usuario_id)
                except Usuario.DoesNotExist:
                    pass
        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
            pass
    
    # Si no está autenticado, intentar obtener de usuario_id en query params o headers
    usuario_id = request.query_params.get('usuario_id') or request.headers.get('X-User-Id')
    if usuario_id:
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            pass
    
    return None


class MensajeViewSet(viewsets.ModelViewSet):
    """
    ViewSet de Mensajes para el sistema de chat
    Maneja los mensajes relacionados con ventas
    """
    queryset = Mensaje.objects.select_related('venta', 'remitente', 'venta__vehiculo', 'venta__vehiculo__marca', 'venta__vehiculo__modelo').all()
    serializer_class = MensajeSerializer
    filterset_class = MensajeFilter
    
    def get_queryset(self):
        """Filtra los mensajes para mostrar solo los de las ventas del usuario"""
        usuario = obtener_usuario_desde_request(self.request)
        if usuario:
            # Solo ventas donde el usuario es comprador o vendedor
            ventas_usuario = Venta.objects.filter(
                Q(comprador=usuario) | Q(vendedor=usuario)
            )
            return Mensaje.objects.filter(venta__in=ventas_usuario).select_related(
                'venta', 'remitente', 'venta__vehiculo', 'venta__vehiculo__marca', 'venta__vehiculo__modelo'
            )
        return Mensaje.objects.none()
    
    def perform_create(self, serializer):
        """Crea un mensaje asignando automáticamente el remitente"""
        usuario = obtener_usuario_desde_request(self.request)
        if not usuario:
            raise PermissionDenied("Debes estar autenticado para enviar mensajes")
        
        venta = serializer.validated_data['venta']
        
        # Verificar que el usuario es parte de la venta
        if venta.comprador != usuario and venta.vendedor != usuario:
            raise PermissionDenied("No tienes permiso para enviar mensajes en esta venta")
        
        serializer.save(remitente=usuario)
