import django_filters
from venta.models import VehiculoFoto


class VehiculoFotoFilter(django_filters.FilterSet):
    """Filtros para el modelo VehiculoFoto"""
    
    # Filtros por vehículo
    vehiculo = django_filters.NumberFilter(field_name='vehiculo__id')
    vehiculo_marca = django_filters.CharFilter(field_name='vehiculo__marca__nombre', lookup_expr='icontains')
    vehiculo_modelo = django_filters.CharFilter(field_name='vehiculo__modelo__nombre', lookup_expr='icontains')
    
    # Filtros por URL
    url_imagen = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = VehiculoFoto
        fields = [
            'vehiculo',
        ]

