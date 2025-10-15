import django_filters
from venta.models import Puja


class PujaFilter(django_filters.FilterSet):
    """Filtros para el modelo Puja"""
    
    # Filtros por subasta
    subasta = django_filters.NumberFilter(field_name='subasta__id')
    subasta_estado = django_filters.CharFilter(field_name='subasta__estado', lookup_expr='iexact')
    
    # Filtros por usuario
    usuario = django_filters.NumberFilter(field_name='usuario__id')
    usuario_nombre = django_filters.CharFilter(field_name='usuario__nombre', lookup_expr='icontains')
    usuario_apellido = django_filters.CharFilter(field_name='usuario__apellido', lookup_expr='icontains')
    
    # Filtros por monto
    monto_min = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')
    monto_max = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')
    
    # Filtros por fecha
    fecha_puja_desde = django_filters.DateFilter(field_name='fecha_puja', lookup_expr='gte')
    fecha_puja_hasta = django_filters.DateFilter(field_name='fecha_puja', lookup_expr='lte')
    
    class Meta:
        model = Puja
        fields = [
            'subasta',
            'usuario',
            'monto',
        ]

