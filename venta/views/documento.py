from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Documento

# utilities
from venta.serializers import DocumentoSerializer
# filters
from venta.filters import DocumentoFilter


class DocumentoViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    filterset_class = DocumentoFilter


#es una combinacion de serializer(get) y filter(filtros) se juntan en una clase para poder usar esta clase en urls.py
#usando el nombre de la clase en este caso DocumentoViewSet (aun no se como usarla pero creo que para eso es)