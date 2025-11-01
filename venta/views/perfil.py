from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# models
from venta.models import Perfil, Usuario

# serializers
from venta.serializers import PerfilSerializer


class PerfilViewSet(viewsets.ModelViewSet):
    """
    ViewSet de Perfil
    Maneja CRUD del perfil de usuario
    """
    queryset = Perfil.objects.select_related('usuario').all()
    serializer_class = PerfilSerializer
    
    @action(detail=False, methods=['get'])
    def mi_perfil(self, request):
        """
        Obtiene el perfil del usuario autenticado
        """
        try:
            # Obtener el usuario desde el token o sesión
            # Asumiendo que hay autenticación por token
            usuario_id = request.query_params.get('usuario_id')
            if not usuario_id:
                return Response(
                    {'error': 'usuario_id es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            perfil = Perfil.objects.select_related('usuario').get(usuario_id=usuario_id)
            serializer = self.get_serializer(perfil, context={'request': request})
            return Response(serializer.data)
        except Perfil.DoesNotExist:
            return Response(
                {'error': 'Perfil no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get', 'put', 'patch'])
    def actualizar_perfil(self, request, pk=None):
        """
        Actualiza el perfil del usuario
        """
        perfil = self.get_object()
        serializer = self.get_serializer(perfil, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_context(self):
        """Agregar request al contexto del serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

