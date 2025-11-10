from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# models
from venta.models import Usuario, Venta

# utilities
from venta.serializers import UsuarioSerializer, VentaSerializer

# filters
from venta.filters import UsuarioFilter


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet de Usuarios
    Maneja CRUD de usuarios
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filterset_class = UsuarioFilter
    
    @action(detail=True, methods=['get'])
    def compras(self, request, pk=None):
        """
        Obtiene las compras de un usuario específico
        GET /venta/usuarios/{id}/compras/
        """
        try:
            usuario = self.get_object()
            compras = Venta.objects.filter(comprador=usuario).select_related(
                'vehiculo', 'vehiculo__marca', 'vehiculo__modelo', 
                'comprador', 'vendedor'
            ).order_by('-fecha_venta')
            
            serializer = VentaSerializer(compras, many=True, context={'request': request})
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