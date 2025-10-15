import django_filters
from venta.models import Venta


class VentaFilter(django_filters.FilterSet):
    """Filtros para el modelo Venta"""
    
    # Filtros por vehículo
    vehiculo = django_filters.NumberFilter(field_name='vehiculo__id')
    vehiculo_marca = django_filters.CharFilter(field_name='vehiculo__marca__nombre', lookup_expr='icontains')
    vehiculo_modelo = django_filters.CharFilter(field_name='vehiculo__modelo__nombre', lookup_expr='icontains')
    
    # Filtros por comprador
    comprador = django_filters.NumberFilter(field_name='comprador__id')
    comprador_nombre = django_filters.CharFilter(field_name='comprador__nombre', lookup_expr='icontains')
    comprador_apellido = django_filters.CharFilter(field_name='comprador__apellido', lookup_expr='icontains')
    
    # Filtros por vendedor
    vendedor = django_filters.NumberFilter(field_name='vendedor__id')
    vendedor_nombre = django_filters.CharFilter(field_name='vendedor__nombre', lookup_expr='icontains')
    vendedor_apellido = django_filters.CharFilter(field_name='vendedor__apellido', lookup_expr='icontains')
    
    # Filtros por fecha de venta
    fecha_venta_desde = django_filters.DateFilter(field_name='fecha_venta', lookup_expr='gte')
    fecha_venta_hasta = django_filters.DateFilter(field_name='fecha_venta', lookup_expr='lte')
    
    # Filtros por precio final
    precio_final_min = django_filters.NumberFilter(field_name='precio_final', lookup_expr='gte')
    precio_final_max = django_filters.NumberFilter(field_name='precio_final', lookup_expr='lte')
    
    # Filtros por método de pago
    metodo_pago = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros por estado
    estado = django_filters.CharFilter(lookup_expr='iexact')
    
    class Meta:
        model = Venta
        fields = [
            'vehiculo',
            'comprador',
            'vendedor',
            'fecha_venta',
            'precio_final',
            'metodo_pago',
            'estado',
        ]

