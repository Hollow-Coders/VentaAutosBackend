import django_filters
from venta.models import Rol


class RolFilter(django_filters.FilterSet):
    """Filtros para el modelo Rol"""
    
    # Filtros por nombre
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    nombre_exacto = django_filters.CharFilter(field_name='nombre', lookup_expr='iexact')
    
    # Filtros por descripción
    descripcion = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Rol
        fields = [
            'nombre',
            'descripcion',
        ]

