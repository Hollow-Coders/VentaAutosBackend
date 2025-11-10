from rest_framework import viewsets

# models
from venta.models import Mensaje

# serializers
from venta.serializers import MensajeSerializer, MensajeCreateSerializer

# filters
from venta.filters import MensajeFilter


class MensajeViewSet(viewsets.ModelViewSet):
    """
    ViewSet de Mensajes
    Maneja CRUD de mensajes
    """
    queryset = Mensaje.objects.select_related('conversacion', 'remitente').all()
    serializer_class = MensajeSerializer
    filterset_class = MensajeFilter
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MensajeCreateSerializer
        return MensajeSerializer

