import django_filters
from django.db.models import Q
from venta.models import Conversacion


class ConversacionFilter(django_filters.FilterSet):
    """Filtros para el modelo Conversacion"""
    
    # Filtros por vendedor
    vendedor = django_filters.NumberFilter(field_name='vendedor__id')
    vendedor_nombre = django_filters.CharFilter(field_name='vendedor__nombre', lookup_expr='icontains')
    
    # Filtros por comprador
    comprador = django_filters.NumberFilter(field_name='comprador__id')
    comprador_nombre = django_filters.CharFilter(field_name='comprador__nombre', lookup_expr='icontains')
    
    # Filtro por usuario (vendedor o comprador)
    usuario = django_filters.NumberFilter(method='filter_usuario')
    
    # Filtro por venta
    venta = django_filters.NumberFilter(field_name='venta__id')
    
    # Filtros por estado
    activa = django_filters.BooleanFilter(field_name='activa')
    
    # Filtros por fecha
    fecha_creacion_desde = django_filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='gte')
    fecha_creacion_hasta = django_filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='lte')
    fecha_actualizacion_desde = django_filters.DateTimeFilter(field_name='fecha_actualizacion', lookup_expr='gte')
    fecha_actualizacion_hasta = django_filters.DateTimeFilter(field_name='fecha_actualizacion', lookup_expr='lte')
    
    class Meta:
        model = Conversacion
        fields = [
            'vendedor',
            'comprador',
            'venta',
            'activa',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
    
    def filter_usuario(self, queryset, name, value):
        """Filtra conversaciones donde el usuario es vendedor o comprador"""
        return queryset.filter(
            Q(vendedor_id=value) | Q(comprador_id=value)
        )

