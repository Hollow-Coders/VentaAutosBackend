from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Rol

# utilities
from venta.serializers import RolSerializer

# filters
from venta.filters import RolFilter


class RolViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    filterset_class = RolFilter