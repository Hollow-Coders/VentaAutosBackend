import django_filters
from venta.models import Venta


def obtener_usuario_desde_request(request):
    """
    Obtiene el usuario desde el request.
    Intenta obtenerlo del token JWT del header Authorization, si no está disponible,
    lo obtiene de usuario_id en query params o headers.
    """
    from django.conf import settings
    import jwt
    from venta.models import Usuario
    
    # Intentar obtener del usuario autenticado (si está configurado)
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user

    # Intentar obtener del token JWT en el header Authorization
    auth_header = request.META.get('HTTP_AUTHORIZATION', '') or request.headers.get('Authorization', '')

    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]

        # Intentar decodificar el token JWT con SECRET_KEY
        try:
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


class VentaFilter(django_filters.FilterSet):
    """Filtros para el modelo Venta"""
    
    # Filtros por vehículo
    vehiculo = django_filters.NumberFilter(field_name='vehiculo__id')
    vehiculo_marca = django_filters.CharFilter(field_name='vehiculo__marca__nombre', lookup_expr='icontains')
    vehiculo_modelo = django_filters.CharFilter(field_name='vehiculo__modelo__nombre', lookup_expr='icontains')
    
    # Filtros por comprador (acepta ID numérico o "current" para el usuario actual)
    comprador = django_filters.CharFilter(method='filter_comprador')
    comprador_nombre = django_filters.CharFilter(field_name='comprador__nombre', lookup_expr='icontains')
    comprador_apellido = django_filters.CharFilter(field_name='comprador__apellido', lookup_expr='icontains')
    
    # Filtros por vendedor
    vendedor = django_filters.NumberFilter(field_name='vendedor__id')
    vendedor_nombre = django_filters.CharFilter(field_name='vendedor__nombre', lookup_expr='icontains')
    vendedor_apellido = django_filters.CharFilter(field_name='vendedor__apellido', lookup_expr='icontains')
    
    # Filtros por fecha de venta
    fecha_venta_desde = django_filters.DateFilter(field_name='fecha_venta', lookup_expr='gte')
    fecha_venta_hasta = django_filters.DateFilter(field_name='fecha_venta', lookup_expr='lte')
    
    # Filtros por precio final
    precio_final_min = django_filters.NumberFilter(field_name='precio_final', lookup_expr='gte')
    precio_final_max = django_filters.NumberFilter(field_name='precio_final', lookup_expr='lte')
    
    # Filtros por método de pago
    metodo_pago = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros por estado
    estado = django_filters.CharFilter(lookup_expr='iexact')
    
    class Meta:
        model = Venta
        fields = [
            'vehiculo',
            'comprador',
            'vendedor',
            'fecha_venta',
            'precio_final',
            'metodo_pago',
            'estado',
        ]
    
    def filter_comprador(self, queryset, name, value):
        """
        Filtra por comprador. Si el valor es "current", usa el usuario autenticado.
        Si es un número, lo trata como ID de usuario.
        """
        if value.lower() == 'current':
            # Obtener el usuario actual desde el request
            # El request está disponible cuando se usa DjangoFilterBackend con DRF
            request = getattr(self, 'request', None)
            if not request:
                # Si no hay request disponible, retornar queryset vacío
                return queryset.none()
            
            usuario = obtener_usuario_desde_request(request)
            if usuario:
                return queryset.filter(comprador=usuario)
            else:
                # Si no hay usuario autenticado, retornar queryset vacío
                return queryset.none()
        else:
            # Intentar convertir a número (ID de usuario)
            try:
                comprador_id = int(value)
                return queryset.filter(comprador__id=comprador_id)
            except (ValueError, TypeError):
                # Si no es un número válido, retornar queryset vacío
                return queryset.none()

