import django_filters
from venta.models import Mensaje


class MensajeFilter(django_filters.FilterSet):
    """Filtros para el modelo Mensaje"""
    
    # Filtros por conversación
    conversacion = django_filters.NumberFilter(field_name='conversacion__id')
    
    # Filtros por remitente
    remitente = django_filters.NumberFilter(field_name='remitente__id')
    remitente_nombre = django_filters.CharFilter(field_name='remitente__nombre', lookup_expr='icontains')
    
    # Filtros por fecha
    fecha_envio_desde = django_filters.DateTimeFilter(field_name='fecha_envio', lookup_expr='gte')
    fecha_envio_hasta = django_filters.DateTimeFilter(field_name='fecha_envio', lookup_expr='lte')
    
    # Filtro por contenido
    contenido = django_filters.CharFilter(field_name='contenido', lookup_expr='icontains')
    
    class Meta:
        model = Mensaje
        fields = [
            'conversacion',
            'remitente',
            'fecha_envio',
        ]

