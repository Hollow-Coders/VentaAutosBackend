import django_filters
from venta.models import Vehiculo


class VehiculoFilter(django_filters.FilterSet):
    """Filtros para el modelo Vehiculo"""
    
    # Filtros por usuario
    usuario = django_filters.NumberFilter(field_name='usuario__id')
    usuario_nombre = django_filters.CharFilter(field_name='usuario__nombre', lookup_expr='icontains')
    
    # Filtros por marca y modelo
    marca = django_filters.NumberFilter(field_name='marca__id')
    marca_nombre = django_filters.CharFilter(field_name='marca__nombre', lookup_expr='icontains')
    modelo = django_filters.NumberFilter(field_name='modelo__id')
    modelo_nombre = django_filters.CharFilter(field_name='modelo__nombre', lookup_expr='icontains')
    
    # Filtros por año
    año = django_filters.NumberFilter()
    año_min = django_filters.NumberFilter(field_name='año', lookup_expr='gte')
    año_max = django_filters.NumberFilter(field_name='año', lookup_expr='lte')
    
    # Filtros por precio
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    
    # Filtros por tipo de transmisión y combustible
    tipo_transmision = django_filters.CharFilter(lookup_expr='icontains')
    tipo_combustible = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros por kilometraje
    kilometraje_min = django_filters.NumberFilter(field_name='kilometraje', lookup_expr='gte')
    kilometraje_max = django_filters.NumberFilter(field_name='kilometraje', lookup_expr='lte')
    
    # Filtros por estado
    estado = django_filters.CharFilter(lookup_expr='iexact')
    
    # Filtros por descripción
    descripcion = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros por fecha de publicación
    fecha_publicacion_desde = django_filters.DateFilter(field_name='fecha_publicacion', lookup_expr='gte')
    fecha_publicacion_hasta = django_filters.DateFilter(field_name='fecha_publicacion', lookup_expr='lte')
    
    # Filtro para vehículos disponibles
    disponible = django_filters.BooleanFilter(method='filter_disponible')
    
    # Filtro por tipo de vehículo
    tipo_vehiculo = django_filters.CharFilter(field_name='tipo_vehiculo', lookup_expr='iexact')
    
    class Meta:
        model = Vehiculo
        fields = [
            'usuario',
            'marca',
            'modelo',
            'año',
            'nota_de_administrador',
            'administrador_que_evaluo',
            'precio',
            'tipo_transmision',
            'tipo_combustible',
            'kilometraje',
            'estado',
            'tipo_vehiculo',
        ]
    
    def filter_disponible(self, queryset, name, value):
        """Filtra vehículos disponibles"""
        if value:
            return queryset.filter(estado='disponible')
        return queryset.exclude(estado='disponible')

