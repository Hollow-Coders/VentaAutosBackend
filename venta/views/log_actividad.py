from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import LogActividad

# utilities
from venta.serializers import LogActividadSerializer

# filters
from venta.filters import LogActividadFilter


class LogActividadViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = LogActividad.objects.all()
    serializer_class = LogActividadSerializer
    filterset_class = LogActividadFilter