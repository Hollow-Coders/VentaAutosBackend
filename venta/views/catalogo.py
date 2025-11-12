from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, OuterRef, Subquery

# models
from venta.models import Vehiculo, VehiculoFoto

# serializers
from venta.serializers import CatalogoSerializer


class CatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de Catálogo
    Vista optimizada para mostrar el catálogo de vehículos
    Solo retorna los campos necesarios: nombre, precio, ubicación, modelo, marca, año
    """
    serializer_class = CatalogoSerializer
    
    def get_queryset(self):
        """
        QuerySet optimizado con select_related y solo campos necesarios
        Filtra solo vehículos disponibles
        """
        first_photo_subquery = Subquery(
            VehiculoFoto.objects.filter(
                vehiculo=OuterRef('pk')
            ).order_by('pk').values('url_imagen')[:1]
        )
        
        queryset = Vehiculo.objects.filter(
            estado='disponible'
        ).select_related(
            'marca', 'modelo'
        ).annotate(
            foto_principal_path=first_photo_subquery
        ).only(
            'id',
            'marca__nombre',
            'modelo__nombre',
            'año',
            'precio',
            'ubicacion',
            'fecha_publicacion'
        ).order_by('-fecha_publicacion')
        
        # Filtros opcionales
        marca = self.request.query_params.get('marca', None)
        modelo = self.request.query_params.get('modelo', None)
        año_min = self.request.query_params.get('año_min', None)
        año_max = self.request.query_params.get('año_max', None)
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        ubicacion = self.request.query_params.get('ubicacion', None)
        
        if marca:
            queryset = queryset.filter(marca__nombre__icontains=marca)
        if modelo:
            queryset = queryset.filter(modelo__nombre__icontains=modelo)
        if año_min:
            queryset = queryset.filter(año__gte=año_min)
        if año_max:
            queryset = queryset.filter(año__lte=año_max)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)
        if ubicacion:
            queryset = queryset.filter(ubicacion__icontains=ubicacion)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """
        Búsqueda optimizada en el catálogo
        Busca por nombre, marca, modelo, ubicación
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Parámetro de búsqueda "q" es requerido'},
                status=400
            )
        
        queryset = self.get_queryset().filter(
            Q(marca__nombre__icontains=query) |
            Q(modelo__nombre__icontains=query) |
            Q(ubicacion__icontains=query)
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

