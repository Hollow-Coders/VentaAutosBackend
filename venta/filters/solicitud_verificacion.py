import django_filters
from venta.models import SolicitudVerificacion


class SolicitudVerificacionFilter(django_filters.FilterSet):
    """Filtros para el modelo SolicitudVerificacion"""
    
    # Filtros por vehículo
    vehiculo = django_filters.NumberFilter(field_name='vehiculo__id')
    
    # Filtros por usuario
    usuario = django_filters.NumberFilter(field_name='usuario__id')
    usuario_nombre = django_filters.CharFilter(field_name='usuario__nombre', lookup_expr='icontains')
    usuario_apellido = django_filters.CharFilter(field_name='usuario__apellido', lookup_expr='icontains')
    
    # Filtros por estado
    estado = django_filters.CharFilter(lookup_expr='iexact')
    
    # Filtros por fecha de solicitud
    fecha_solicitud_desde = django_filters.DateFilter(field_name='fecha_solicitud', lookup_expr='gte')
    fecha_solicitud_hasta = django_filters.DateFilter(field_name='fecha_solicitud', lookup_expr='lte')
    
    # Filtros por fecha de respuesta
    fecha_respuesta_desde = django_filters.DateFilter(field_name='fecha_respuesta', lookup_expr='gte')
    fecha_respuesta_hasta = django_filters.DateFilter(field_name='fecha_respuesta', lookup_expr='lte')
    
    # Filtro para solicitudes sin respuesta
    sin_respuesta = django_filters.BooleanFilter(field_name='fecha_respuesta', lookup_expr='isnull')
    
    class Meta:
        model = SolicitudVerificacion
        fields = [
            'vehiculo',
            'usuario',
            'estado',
        ]

