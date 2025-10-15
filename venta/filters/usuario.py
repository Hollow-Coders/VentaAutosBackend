import django_filters
from venta.models import Usuario


class UsuarioFilter(django_filters.FilterSet):
    """Filtros para el modelo Usuario"""
    
    # Filtros por nombre y apellido
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(lookup_expr='icontains')
    nombre_completo = django_filters.CharFilter(method='filter_nombre_completo')
    
    # Filtros por correo
    correo = django_filters.CharFilter(lookup_expr='icontains')
    correo_exacto = django_filters.CharFilter(field_name='correo', lookup_expr='iexact')
    
    # Filtros por estado
    estado = django_filters.CharFilter(lookup_expr='iexact')
    
    # Filtros por rol
    rol = django_filters.NumberFilter(field_name='rol__id')
    rol_nombre = django_filters.CharFilter(field_name='rol__nombre', lookup_expr='icontains')
    
    # Filtros por fecha de creación
    fecha_creacion_desde = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='gte')
    fecha_creacion_hasta = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='lte')
    
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellido',
            'correo',
            'estado',
            'rol',
        ]
    
    def filter_nombre_completo(self, queryset, name, value):
        """Filtra por nombre completo (nombre + apellido)"""
        return queryset.filter(
            nombre__icontains=value
        ) | queryset.filter(
            apellido__icontains=value
        )

