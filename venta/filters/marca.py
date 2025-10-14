import django_filters
from venta.models.marca import Marca


class MarcaFilter(django_filters.FilterSet):
    """Filtros para el modelo Marca"""
    
    # Filtro por nombre
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtro por nombre exacto
    nombre_exacto = django_filters.CharFilter(field_name='nombre', lookup_expr='iexact')
    
    class Meta:
        model = Marca
        fields = [
            'nombre',
        ]

