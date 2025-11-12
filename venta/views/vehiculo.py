from django.shortcuts import render

# Create your views here.
# models
from venta.models import Vehiculo, VehiculoFoto
# rest
from rest_framework import viewsets
from django.db.models import Prefetch, Count
# utilities
from venta.serializers import VehiculoSerializer
# filters
from venta.filters import VehiculoFilter
# cosa para que funcionen los filtros?
from django_filters.rest_framework import DjangoFilterBackend


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Vehiculo.objects.none()
    serializer_class = VehiculoSerializer
    filterset_class = VehiculoFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        """
        Optimiza el queryset de vehículos para evitar N+1 y reducir payload.
        """
        fotos_prefetch = Prefetch(
            'fotos',
            queryset=VehiculoFoto.objects.only('id', 'vehiculo_id', 'url_imagen').order_by('pk')
        )
        
        return (
            Vehiculo.objects.select_related('usuario', 'marca', 'modelo')
            .prefetch_related(fotos_prefetch)
            .annotate(
                total_documentos_annotated=Count('documentos', distinct=True)
            )
        )
    
    def get_serializer_context(self):
        """Agregar request al contexto del serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

