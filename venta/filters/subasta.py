import django_filters
from venta.models.subasta import Subasta


class SubastaFilter(django_filters.FilterSet):
    """Filtros para el modelo Subasta"""
    
    # Filtros por vehículo
    vehiculo = django_filters.NumberFilter(field_name='vehiculo__id')
    vehiculo_marca = django_filters.CharFilter(field_name='vehiculo__marca__nombre', lookup_expr='icontains')
    vehiculo_modelo = django_filters.CharFilter(field_name='vehiculo__modelo__nombre', lookup_expr='icontains')
    
    # Filtros por precio inicial
    precio_inicial_min = django_filters.NumberFilter(field_name='precio_inicial', lookup_expr='gte')
    precio_inicial_max = django_filters.NumberFilter(field_name='precio_inicial', lookup_expr='lte')
    
    # Filtros por fechas
    fecha_inicio_desde = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte')
    fecha_inicio_hasta = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='lte')
    fecha_fin_desde = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='gte')
    fecha_fin_hasta = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='lte')
    
    # Filtros por estado
    estado = django_filters.CharFilter(lookup_expr='iexact')
    
    # Filtro para subastas activas
    activa = django_filters.BooleanFilter(method='filter_activa')
    
    class Meta:
        model = Subasta
        fields = [
            'vehiculo',
            'precio_inicial',
            'estado',
        ]
    
    def filter_activa(self, queryset, name, value):
        """Filtra subastas activas"""
        if value:
            return queryset.filter(estado='activa')
        return queryset.exclude(estado='activa')

