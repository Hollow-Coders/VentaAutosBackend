from django.shortcuts import render

from rest_framework import viewsets
from django.db.models import Count, Max, F
from django.db.models.functions import Coalesce

# models
from venta.models import Subasta

# utilities
from venta.serializers import SubastaSerializer

# filters
from venta.filters import SubastaFilter


class SubastaViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Subasta.objects.none()
    serializer_class = SubastaSerializer
    filterset_class = SubastaFilter

    def get_queryset(self):
        """
        Optimiza el queryset con annotations para evitar consultas N+1.
        """
        return (
            Subasta.objects.select_related(
                'vehiculo',
                'vehiculo__marca',
                'vehiculo__modelo'
            )
            .annotate(
                total_pujas_annotated=Count('pujas', distinct=True),
                max_puja=Max('pujas__monto')
            )
            .annotate(
                precio_actual_annotated=Coalesce('max_puja', F('precio_inicial'))
            )
        )