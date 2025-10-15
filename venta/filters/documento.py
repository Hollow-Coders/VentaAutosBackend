import django_filters
from venta.models import Documento


class DocumentoFilter(django_filters.FilterSet):
    """Filtros para el modelo Documento"""
    
    # Filtros por usuario
    usuario = django_filters.NumberFilter(field_name='usuario__id')
    usuario_nombre = django_filters.CharFilter(field_name='usuario__nombre', lookup_expr='icontains')
    usuario_apellido = django_filters.CharFilter(field_name='usuario__apellido', lookup_expr='icontains')
    
    # Filtros por vehículo
    vehiculo = django_filters.NumberFilter(field_name='vehiculo__id')
    
    # Filtros por tipo y estado
    tipo_documento = django_filters.CharFilter(lookup_expr='icontains')
    estado = django_filters.CharFilter(lookup_expr='iexact')
    
    # Filtros por fecha
    fecha_subida_desde = django_filters.DateFilter(field_name='fecha_subida', lookup_expr='gte')
    fecha_subida_hasta = django_filters.DateFilter(field_name='fecha_subida', lookup_expr='lte')
    
    class Meta:
        model = Documento
        fields = [
            'usuario',
            'vehiculo',
            'tipo_documento',
            'estado',
        ]

