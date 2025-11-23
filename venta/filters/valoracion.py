import django_filters
from venta.models import Valoracion


class ValoracionFilter(django_filters.FilterSet):
    """Filtros para el modelo Valoracion"""
    
    # Filtros por venta
    venta = django_filters.NumberFilter(field_name='venta__id')
    
    # Filtros por comprador
    comprador = django_filters.NumberFilter(field_name='comprador__id')
    
    # Filtros por vendedor (a través de la venta)
    vendedor = django_filters.NumberFilter(field_name='venta__vendedor__id')
    
    # Filtros por calificación
    calificacion_min = django_filters.NumberFilter(field_name='calificacion', lookup_expr='gte')
    calificacion_max = django_filters.NumberFilter(field_name='calificacion', lookup_expr='lte')
    
    # Filtros por fecha
    fecha_creacion_desde = django_filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='gte')
    fecha_creacion_hasta = django_filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='lte')
    
    class Meta:
        model = Valoracion
        fields = [
            'venta',
            'comprador',
            'calificacion',
            'fecha_creacion',
        ]

