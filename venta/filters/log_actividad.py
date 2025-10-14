import django_filters
from venta.models.log_actividad import LogActividad


class LogActividadFilter(django_filters.FilterSet):
    """Filtros para el modelo LogActividad"""
    
    # Filtros por usuario
    usuario = django_filters.NumberFilter(field_name='usuario__id')
    usuario_nombre = django_filters.CharFilter(field_name='usuario__nombre', lookup_expr='icontains')
    usuario_apellido = django_filters.CharFilter(field_name='usuario__apellido', lookup_expr='icontains')
    
    # Filtros por acción
    accion = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros por fecha
    fecha_desde = django_filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='lte')
    
    # Filtros por IP
    ip = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = LogActividad
        fields = [
            'usuario',
            'accion',
            'fecha',
            'ip',
        ]

