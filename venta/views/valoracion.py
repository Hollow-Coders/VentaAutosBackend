from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.db.models import Q

# models
from venta.models import Valoracion, Venta, Usuario

# serializers
from venta.serializers import ValoracionSerializer

# filters
from venta.filters import ValoracionFilter


def obtener_usuario_desde_request(request):
    """
    Obtiene el usuario desde el request.
    Intenta obtenerlo del token JWT del header Authorization, si no está disponible, 
    lo obtiene de usuario_id en query params o headers.
    """
    from django.conf import settings
    import jwt
    
    # Intentar obtener del usuario autenticado (si está configurado)
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    
    # Intentar obtener del token JWT en el header Authorization
    auth_header = request.META.get('HTTP_AUTHORIZATION', '') or request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            # Decodificar el token JWT con SECRET_KEY
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


class ValoracionViewSet(viewsets.ModelViewSet):
    """
    ViewSet de Valoraciones
    Maneja CRUD de valoraciones
    """
    queryset = Valoracion.objects.all()
    serializer_class = ValoracionSerializer
    filterset_class = ValoracionFilter
    
    def get_queryset(self):
        """
        Optimiza el queryset con select_related para evitar N+1
        """
        return Valoracion.objects.select_related(
            'venta', 'venta__vehiculo', 'venta__vehiculo__marca', 
            'venta__vehiculo__modelo', 'comprador', 'venta__vendedor'
        ).order_by('-fecha_creacion')
    
    @action(detail=False, methods=['get'])
    def ultimas(self, request):
        """
        Obtiene las últimas 10 valoraciones.
        GET /venta/valoraciones/ultimas/
        """
        valoraciones = self.get_queryset()[:10]
        serializer = self.get_serializer(valoraciones, many=True)
        
        return Response({
            'total': valoraciones.count(),
            'valoraciones': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def todas(self, request):
        """
        Obtiene todas las valoraciones.
        GET /venta/valoraciones/todas/
        """
        valoraciones = self.get_queryset()
        serializer = self.get_serializer(valoraciones, many=True)
        
        return Response({
            'total': valoraciones.count(),
            'valoraciones': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """
        Crea una valoración.
        Solo el comprador de la venta puede crear una valoración.
        POST /venta/valoraciones/
        """
        usuario = obtener_usuario_desde_request(request)
        
        if not usuario:
            return Response(
                {'error': 'Usuario no autenticado. Proporcione usuario_id o token de autenticación.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        venta_id = request.data.get('venta')
        if not venta_id:
            return Response(
                {'error': 'El campo venta es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            venta = Venta.objects.get(id=venta_id)
        except Venta.DoesNotExist:
            return Response(
                {'error': 'Venta no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar que el usuario es el comprador de la venta
        if venta.comprador.id != usuario.id:
            return Response(
                {'error': 'Solo el comprador de la venta puede crear una valoración'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verificar si ya existe una valoración para esta venta por este comprador
        if Valoracion.objects.filter(venta=venta, comprador=usuario).exists():
            return Response(
                {'error': 'Ya existe una valoración para esta venta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear la valoración
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(comprador=usuario)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def por_vendedor(self, request):
        """
        Obtiene todas las valoraciones de un vendedor específico.
        GET /venta/valoraciones/por_vendedor/?vendedor_id={id}
        """
        vendedor_id = request.query_params.get('vendedor_id')
        
        if not vendedor_id:
            return Response(
                {'error': 'vendedor_id es requerido como parámetro de consulta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            vendedor = Usuario.objects.get(id=vendedor_id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Vendedor no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Obtener todas las valoraciones de las ventas realizadas por este vendedor
        valoraciones = Valoracion.objects.filter(
            venta__vendedor=vendedor
        ).select_related(
            'venta', 'venta__vehiculo', 'venta__vehiculo__marca', 
            'venta__vehiculo__modelo', 'comprador', 'venta__vendedor'
        ).order_by('-fecha_creacion')
        
        serializer = self.get_serializer(valoraciones, many=True)
        
        return Response({
            'vendedor_id': vendedor.id,
            'vendedor_nombre': f"{vendedor.nombre} {vendedor.apellido}",
            'total_valoraciones': valoraciones.count(),
            'valoraciones': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def promedio_vendedor(self, request):
        """
        Calcula el promedio de calificaciones de un vendedor.
        GET /venta/valoraciones/promedio_vendedor/?vendedor_id={id}
        """
        vendedor_id = request.query_params.get('vendedor_id')
        
        if not vendedor_id:
            return Response(
                {'error': 'vendedor_id es requerido como parámetro de consulta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            vendedor = Usuario.objects.get(id=vendedor_id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Vendedor no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calcular el promedio de calificaciones
        resultado = Valoracion.objects.filter(
            venta__vendedor=vendedor
        ).aggregate(
            promedio=Avg('calificacion'),
            total_valoraciones=Count('id')
        )
        
        promedio = resultado['promedio']
        total_valoraciones = resultado['total_valoraciones']
        
        return Response({
            'vendedor_id': vendedor.id,
            'vendedor_nombre': f"{vendedor.nombre} {vendedor.apellido}",
            'promedio_calificacion': round(float(promedio), 2) if promedio else 0.0,
            'total_valoraciones': total_valoraciones
        })

