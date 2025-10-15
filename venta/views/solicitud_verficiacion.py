from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import SolicitudVerificacion

# utilities
from venta.serializers import SolicitudVerificacionSerializer

# filters
from venta.filters import SolicitudVerificacionFilter


class SolicitudVerificacionViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = SolicitudVerificacion.objects.all()
    serializer_class = SolicitudVerificacionSerializer
    filterset_class = SolicitudVerificacionFilter