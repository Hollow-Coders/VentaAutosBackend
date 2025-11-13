from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

# models
from venta.models import Venta, Usuario

# utilities
from venta.serializers import VentaSerializer

# filters
from venta.filters import VentaFilter


class VentaViewSet(viewsets.ModelViewSet):
    """
    View de Ventas
    Maneja CRUD
    """
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filterset_class = VentaFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_filterset(self, *args, **kwargs):
        """Pasa el request al FilterSet para que pueda acceder al usuario autenticado"""
        filterset = super().get_filterset(*args, **kwargs)
        if filterset:
            filterset.request = self.request
        return filterset
    
    @action(detail=False, methods=['get'])
    def mis_compras(self, request):
        """
        Obtiene las compras del usuario autenticado
        GET /venta/ventas/mis_compras/?usuario_id={id}
        """
        usuario_id = request.query_params.get('usuario_id')
        
        if not usuario_id:
            return Response(
                {'error': 'usuario_id es requerido como parámetro de consulta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            compras = Venta.objects.filter(comprador=usuario).select_related(
                'vehiculo', 'vehiculo__marca', 'vehiculo__modelo', 
                'comprador', 'vendedor'
            ).order_by('-fecha_venta')
            
            serializer = self.get_serializer(compras, many=True)
            return Response({
                'usuario_id': usuario.id,
                'usuario_nombre': f"{usuario.nombre} {usuario.apellido}",
                'total_compras': compras.count(),
                'compras': serializer.data
            })
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )