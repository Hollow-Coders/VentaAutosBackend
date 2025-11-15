from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import jwt

# models
from venta.models import Mensaje, Vehiculo, Usuario

# serializers
from venta.serializers import MensajeSerializer, SolicitudMensajeSerializer


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


@api_view(['GET', 'POST'])
def mensajes(request):
    """
    Maneja tanto GET como POST para mensajes.
    GET /chat/mensajes/?comprador={id}&vendedor={id}&vehiculo={id} - Obtiene mensajes
    POST /chat/mensajes/ - Envía un nuevo mensaje
    """
    if request.method == 'GET':
        return obtener_mensajes(request)
    elif request.method == 'POST':
        return enviar_mensaje(request)


def obtener_mensajes(request):
    """
    Obtiene todos los mensajes de un chat específico.
    GET /chat/mensajes/?comprador={id}&vendedor={id}&vehiculo={id}
    """
    comprador_id = request.query_params.get('comprador')
    vendedor_id = request.query_params.get('vendedor')
    vehiculo_id = request.query_params.get('vehiculo')
    
    if not all([comprador_id, vendedor_id, vehiculo_id]):
        return Response(
            {'error': 'Faltan parámetros requeridos: comprador, vendedor, vehiculo'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        comprador_id = int(comprador_id)
        vendedor_id = int(vendedor_id)
        vehiculo_id = int(vehiculo_id)
    except ValueError:
        return Response(
            {'error': 'Los parámetros deben ser números enteros'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener el usuario autenticado
    usuario = obtener_usuario_desde_request(request)
    if not usuario:
        return Response(
            {'error': 'No autenticado'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Verificar que el usuario es parte del chat
    usuario_id = usuario.id
    if usuario_id != comprador_id and usuario_id != vendedor_id:
        return Response(
            {'error': 'No tienes permiso para ver este chat'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Obtener los mensajes del chat
    mensajes = Mensaje.objects.filter(
        comprador_id=comprador_id,
        vendedor_id=vendedor_id,
        vehiculo_id=vehiculo_id
    ).select_related('remitente', 'comprador', 'vendedor', 'vehiculo').order_by('fecha_envio')
    
    serializer = MensajeSerializer(mensajes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def enviar_mensaje(request):
    """
    Envía un nuevo mensaje en un chat.
    POST /chat/mensajes/
    """
    serializer = SolicitudMensajeSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    comprador_id = serializer.validated_data['comprador']
    vendedor_id = serializer.validated_data['vendedor']
    vehiculo_id = serializer.validated_data['vehiculo']
    contenido = serializer.validated_data['contenido']
    
    # Obtener el usuario autenticado
    usuario = obtener_usuario_desde_request(request)
    if not usuario:
        return Response(
            {'error': 'No autenticado'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Verificar que el usuario es parte del chat
    usuario_id = usuario.id
    if usuario_id != comprador_id and usuario_id != vendedor_id:
        return Response(
            {'error': 'No tienes permiso para enviar mensajes en este chat'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Verificar que el vehículo existe
    try:
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    except Vehiculo.DoesNotExist:
        return Response(
            {'error': 'El vehículo no existe'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verificar que comprador y vendedor existen
    try:
        comprador = Usuario.objects.get(id=comprador_id)
        vendedor = Usuario.objects.get(id=vendedor_id)
    except Usuario.DoesNotExist:
        return Response(
            {'error': 'El comprador o vendedor no existe'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Crear el mensaje
    mensaje = Mensaje.objects.create(
        comprador=comprador,
        vendedor=vendedor,
        vehiculo=vehiculo,
        remitente=usuario,
        contenido=contenido,
        leido=False
    )
    
    serializer = MensajeSerializer(mensaje)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def marcar_como_leidos(request):
    """
    Marca como leídos todos los mensajes de un chat que no fueron enviados por el usuario actual.
    POST /chat/marcar-leidos/
    """
    comprador_id = request.data.get('comprador')
    vendedor_id = request.data.get('vendedor')
    vehiculo_id = request.data.get('vehiculo')
    
    if not all([comprador_id, vendedor_id, vehiculo_id]):
        return Response(
            {'error': 'Faltan campos requeridos: comprador, vendedor, vehiculo'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        comprador_id = int(comprador_id)
        vendedor_id = int(vendedor_id)
        vehiculo_id = int(vehiculo_id)
    except ValueError:
        return Response(
            {'error': 'Los campos deben ser números enteros'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener el usuario autenticado
    usuario = obtener_usuario_desde_request(request)
    if not usuario:
        return Response(
            {'error': 'No autenticado'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Verificar que el usuario es parte del chat
    usuario_id = usuario.id
    if usuario_id != comprador_id and usuario_id != vendedor_id:
        return Response(
            {'error': 'No tienes permiso para marcar mensajes de este chat'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Marcar como leídos solo los mensajes que NO fueron enviados por el usuario actual
    mensajes_actualizados = Mensaje.objects.filter(
        comprador_id=comprador_id,
        vendedor_id=vendedor_id,
        vehiculo_id=vehiculo_id,
        leido=False
    ).exclude(
        remitente_id=usuario_id  # Excluir los mensajes enviados por el usuario actual
    ).update(leido=True)
    
    return Response({
        'mensaje': 'Mensajes marcados como leídos',
        'mensajes_actualizados': mensajes_actualizados
    }, status=status.HTTP_200_OK)
