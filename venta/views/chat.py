from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.conf import settings
import jwt

# models
from venta.models import Mensaje, Venta, Usuario

# serializers
from venta.serializers import MensajeSerializer


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
        
        # Intentar decodificar el token JWT
        # SimpleJWT usa SECRET_KEY por defecto, así que intentamos primero con eso
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            usuario_id = decoded_token.get('usuario_id') or decoded_token.get('user_id')
            if usuario_id:
                try:
                    return Usuario.objects.get(id=usuario_id)
                except Usuario.DoesNotExist:
                    pass
        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
            # Si falla, el token puede estar usando una clave diferente o ser inválido
            # Continuamos con el siguiente método
            pass
    
    # Si no está autenticado, intentar obtener de usuario_id en query params o headers
    usuario_id = request.query_params.get('usuario_id') or request.headers.get('X-User-Id')
    if usuario_id:
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            pass
    
    return None


@api_view(['GET'])
def mensajes_por_venta(request, venta_id):
    """
    Obtiene todos los mensajes de una venta específica.
    GET /chat/venta/{venta_id}/mensajes/
    """
    # Debug: verificar headers
    auth_header = request.META.get('HTTP_AUTHORIZATION', '') or request.headers.get('Authorization', '')
    
    usuario = obtener_usuario_desde_request(request)
    if not usuario:
        # Si no hay usuario, intentar obtener de query params como fallback temporal
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                pass
        
        if not usuario:
            return Response(
                {"error": "No autenticado", "debug": {"auth_header_present": bool(auth_header)}},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    try:
        venta = Venta.objects.select_related('vehiculo', 'comprador', 'vendedor').get(id=venta_id)
    except Venta.DoesNotExist:
        return Response(
            {"error": "Venta no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verificar permisos
    if venta.comprador != usuario and venta.vendedor != usuario:
        return Response(
            {"error": "No tienes permiso para ver estos mensajes"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    mensajes = Mensaje.objects.filter(venta=venta).select_related(
        'remitente', 'venta'
    ).order_by('fecha_envio')
    
    serializer = MensajeSerializer(mensajes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def conversaciones(request):
    """
    Obtiene todas las conversaciones (ventas) del usuario con información del último mensaje.
    GET /chat/conversaciones/
    """
    usuario = obtener_usuario_desde_request(request)
    if not usuario:
        return Response(
            {"error": "No autenticado"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    ventas = Venta.objects.filter(
        Q(comprador=usuario) | Q(vendedor=usuario)
    ).select_related(
        'vehiculo', 'vehiculo__marca', 'vehiculo__modelo', 'comprador', 'vendedor'
    )
    
    conversaciones = []
    for venta in ventas:
        try:
            ultimo_mensaje = Mensaje.objects.filter(venta=venta).select_related('remitente').last()
            mensajes_no_leidos = Mensaje.objects.filter(
                venta=venta,
                leido=False
            ).exclude(remitente=usuario).count()
            
            # Construir nombre del vehículo con manejo de errores
            try:
                vehiculo_nombre = f"{venta.vehiculo.marca.nombre} {venta.vehiculo.modelo.nombre} {venta.vehiculo.año}"
            except (AttributeError, Exception):
                vehiculo_nombre = "Vehículo no disponible"
            
            conversaciones.append({
                'venta_id': venta.id,
                'vehiculo_nombre': vehiculo_nombre,
                'ultimo_mensaje': MensajeSerializer(ultimo_mensaje).data if ultimo_mensaje else None,
                'mensajes_no_leidos': mensajes_no_leidos
            })
        except Exception:
            # Si hay un error con esta venta, continuar con la siguiente
            continue
    
    return Response(conversaciones)

