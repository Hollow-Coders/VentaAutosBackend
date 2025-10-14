import django_filters
from venta.models.modelo import Modelo


class ModeloFilter(django_filters.FilterSet):
    """Filtros para el modelo Modelo"""
    
    # Filtros por marca
    marca = django_filters.NumberFilter(field_name='marca__id')
    marca_nombre = django_filters.CharFilter(field_name='marca__nombre', lookup_expr='icontains')
    
    # Filtros por nombre
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    nombre_exacto = django_filters.CharFilter(field_name='nombre', lookup_expr='iexact')
    
    class Meta:
        model = Modelo
        fields = [
            'marca',
            'nombre',
        ]

