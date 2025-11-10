from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.utils import timezone

# models
from venta.models import Conversacion, Mensaje, Usuario, Venta

# serializers
from venta.serializers import (
    ConversacionSerializer, 
    ConversacionDetalleSerializer,
    MensajeSerializer,
    MensajeCreateSerializer
)

# filters
from venta.filters import ConversacionFilter


class ConversacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet de Conversaciones
    Maneja CRUD de conversaciones y mensajes
    """
    queryset = Conversacion.objects.select_related('vendedor', 'comprador', 'venta').all()
    serializer_class = ConversacionSerializer
    filterset_class = ConversacionFilter
    
    def create(self, request, *args, **kwargs):
        """
        Sobrescribe el método create para crear conversaciones basadas en ventas o usuarios
        Acepta dos formatos:
        1. {"venta": <id>} - Crea una nueva conversación única para esa venta
        2. {"vendedor": <id>, "comprador": <id>} o {"usuario1": <id>, "usuario2": <id>} - Crea/busca conversación entre usuarios
        Si se proporciona una venta, siempre se crea una nueva conversación para esa venta
        """
        venta_id = request.data.get('venta')
        vendedor_id = request.data.get('vendedor')
        comprador_id = request.data.get('comprador')
        usuario1_id = request.data.get('usuario1')
        usuario2_id = request.data.get('usuario2')
        
        try:
            # Si se proporciona una venta, crear conversación única para esa venta
            if venta_id:
                venta = Venta.objects.get(id=venta_id)
                vendedor = venta.vendedor
                comprador = venta.comprador
                
                if vendedor == comprador:
                    return Response(
                        {'error': 'El vendedor y comprador no pueden ser la misma persona'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Verificar si ya existe una conversación para esta venta
                conversacion_existente = Conversacion.objects.filter(venta=venta).first()
                
                if conversacion_existente:
                    # Si existe, reactivarla si está inactiva
                    if not conversacion_existente.activa:
                        conversacion_existente.activa = True
                        conversacion_existente.save()
                    serializer = self.get_serializer(conversacion_existente, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                # Crear nueva conversación única para esta venta
                conversacion = Conversacion.objects.create(
                    venta=venta,
                    vendedor=vendedor,
                    comprador=comprador
                )
                serializer = self.get_serializer(conversacion, context={'request': request})
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
            elif vendedor_id and comprador_id:
                # Si se proporcionan vendedor y comprador directamente (sin venta)
                vendedor = Usuario.objects.get(id=vendedor_id)
                comprador = Usuario.objects.get(id=comprador_id)
                
                if vendedor == comprador:
                    return Response(
                        {'error': 'El vendedor y comprador no pueden ser la misma persona'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Buscar conversación existente sin venta asociada o crear nueva
                conversacion = Conversacion.objects.filter(
                    vendedor=vendedor,
                    comprador=comprador,
                    venta__isnull=True
                ).first()
                
                if conversacion:
                    if not conversacion.activa:
                        conversacion.activa = True
                        conversacion.save()
                    serializer = self.get_serializer(conversacion, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                # Crear nueva conversación sin venta
                conversacion = Conversacion.objects.create(
                    vendedor=vendedor,
                    comprador=comprador
                )
                serializer = self.get_serializer(conversacion, context={'request': request})
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                
            elif usuario1_id and usuario2_id:
                # Si se proporcionan usuario1 y usuario2, buscar venta más reciente entre ellos
                usuario1 = Usuario.objects.get(id=usuario1_id)
                usuario2 = Usuario.objects.get(id=usuario2_id)
                
                # Buscar la venta más reciente entre estos usuarios
                # Intentar primero con usuario1 como vendedor y usuario2 como comprador
                venta = Venta.objects.filter(
                    vendedor=usuario1,
                    comprador=usuario2
                ).order_by('-fecha_venta').first()
                
                # Si no existe, intentar con usuario2 como vendedor y usuario1 como comprador
                if not venta:
                    venta = Venta.objects.filter(
                        vendedor=usuario2,
                        comprador=usuario1
                    ).order_by('-fecha_venta').first()
                
                if venta:
                    # Si hay una venta, crear/buscar conversación para esa venta específica
                    conversacion_existente = Conversacion.objects.filter(venta=venta).first()
                    
                    if conversacion_existente:
                        if not conversacion_existente.activa:
                            conversacion_existente.activa = True
                            conversacion_existente.save()
                        serializer = self.get_serializer(conversacion_existente, context={'request': request})
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    
                    # Crear nueva conversación para esta venta
                    conversacion = Conversacion.objects.create(
                        venta=venta,
                        vendedor=venta.vendedor,
                        comprador=venta.comprador
                    )
                    serializer = self.get_serializer(conversacion, context={'request': request})
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    # Si no hay venta, crear conversación sin venta (compatibilidad hacia atrás)
                    conversacion_existente = Conversacion.objects.filter(
                        Q(vendedor=usuario1, comprador=usuario2) | 
                        Q(vendedor=usuario2, comprador=usuario1),
                        venta__isnull=True
                    ).first()
                    
                    if conversacion_existente:
                        if not conversacion_existente.activa:
                            conversacion_existente.activa = True
                            conversacion_existente.save()
                        serializer = self.get_serializer(conversacion_existente, context={'request': request})
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    
                    # Crear nueva conversación sin venta
                    vendedor = usuario1
                    comprador = usuario2
                    conversacion = Conversacion.objects.create(
                        vendedor=vendedor,
                        comprador=comprador
                    )
                    serializer = self.get_serializer(conversacion, context={'request': request})
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response(
                    {'error': 'Se requiere "venta" o ("vendedor" y "comprador") o ("usuario1" y "usuario2")'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Venta.DoesNotExist:
            return Response(
                {'error': 'La venta no existe'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Uno o ambos usuarios no existen'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def mis_conversaciones(self, request):
        """
        Obtiene todas las conversaciones de un usuario (como vendedor o comprador)
        GET /venta/conversaciones/mis_conversaciones/?usuario_id={id}
        """
        usuario_id = request.query_params.get('usuario_id')
        
        if not usuario_id:
            return Response(
                {'error': 'usuario_id es requerido como parámetro de consulta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            conversaciones = Conversacion.objects.filter(
                Q(vendedor=usuario) | Q(comprador=usuario),
                activa=True
            ).select_related('vendedor', 'comprador', 'venta').prefetch_related('mensajes').order_by('-fecha_actualizacion')
            
            serializer = self.get_serializer(conversaciones, many=True, context={'request': request})
            return Response({
                'usuario_id': usuario.id,
                'usuario_nombre': f"{usuario.nombre} {usuario.apellido}",
                'total_conversaciones': conversaciones.count(),
                'conversaciones': serializer.data
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
    
    @action(detail=False, methods=['post'])
    def crear_conversacion(self, request):
        """
        Crea una nueva conversación basada en una venta
        POST /venta/conversaciones/crear_conversacion/
        Body: {"venta": 1}
        """
        venta_id = request.data.get('venta')
        
        if not venta_id:
            return Response(
                {'error': 'venta es requerida'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            venta = Venta.objects.get(id=venta_id)
            vendedor = venta.vendedor
            comprador = venta.comprador
            
            if vendedor == comprador:
                return Response(
                    {'error': 'El vendedor y comprador no pueden ser la misma persona'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar si ya existe una conversación para esta venta
            conversacion = Conversacion.objects.filter(venta=venta).first()
            
            if conversacion:
                # Si existe pero está inactiva, reactivarla
                if not conversacion.activa:
                    conversacion.activa = True
                    conversacion.save()
                serializer = self.get_serializer(conversacion, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Crear nueva conversación única para esta venta
            conversacion = Conversacion.objects.create(
                venta=venta,
                vendedor=vendedor,
                comprador=comprador
            )
            serializer = self.get_serializer(conversacion, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Venta.DoesNotExist:
            return Response(
                {'error': 'La venta no existe'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get', 'post'])
    def mensajes(self, request, pk=None):
        """
        Obtiene todos los mensajes de una conversación (GET)
        o crea un nuevo mensaje (POST)
        GET /venta/conversaciones/{id}/mensajes/
        POST /venta/conversaciones/{id}/mensajes/
        Body: {"remitente": 1, "contenido": "Hola"}
        """
        if request.method == 'POST':
            # Crear nuevo mensaje
            try:
                conversacion = self.get_object()
                remitente_id = request.data.get('remitente')
                contenido = request.data.get('contenido')
                
                if not remitente_id or not contenido:
                    return Response(
                        {'error': 'remitente y contenido son requeridos'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    remitente = Usuario.objects.get(id=remitente_id)
                except Usuario.DoesNotExist:
                    return Response(
                        {'error': 'Usuario remitente no encontrado'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Verificar que el remitente pertenezca a la conversación (sea vendedor o comprador)
                if remitente not in [conversacion.vendedor, conversacion.comprador]:
                    return Response(
                        {'error': 'El remitente debe ser el vendedor o comprador de la conversación'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Crear el mensaje
                mensaje = Mensaje.objects.create(
                    conversacion=conversacion,
                    remitente=remitente,
                    contenido=contenido
                )
                
                # Actualizar la fecha de actualización de la conversación
                conversacion.fecha_actualizacion = timezone.now()
                conversacion.save()
                
                serializer = MensajeSerializer(mensaje, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Conversacion.DoesNotExist:
                return Response(
                    {'error': 'Conversación no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # GET - Obtener mensajes
            try:
                conversacion = self.get_object()
                mensajes = conversacion.mensajes.select_related('remitente').order_by('fecha_envio')
                
                serializer = MensajeSerializer(mensajes, many=True, context={'request': request})
                return Response({
                    'conversacion_id': conversacion.id,
                    'total_mensajes': mensajes.count(),
                    'mensajes': serializer.data
                })
            except Conversacion.DoesNotExist:
                return Response(
                    {'error': 'Conversación no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
    @action(detail=True, methods=['post'])
    def enviar_mensaje(self, request, pk=None):
        """
        Envía un mensaje en una conversación
        POST /venta/conversaciones/{id}/enviar_mensaje/
        Body: {"remitente": 1, "contenido": "Hola, ¿cómo estás?"}
        """
        try:
            conversacion = self.get_object()
            remitente_id = request.data.get('remitente')
            contenido = request.data.get('contenido')
            
            if not remitente_id or not contenido:
                return Response(
                    {'error': 'remitente y contenido son requeridos'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                remitente = Usuario.objects.get(id=remitente_id)
            except Usuario.DoesNotExist:
                return Response(
                    {'error': 'Usuario remitente no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Verificar que el remitente pertenezca a la conversación (sea vendedor o comprador)
            if remitente not in [conversacion.vendedor, conversacion.comprador]:
                return Response(
                    {'error': 'El remitente debe ser el vendedor o comprador de la conversación'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Crear el mensaje
            mensaje = Mensaje.objects.create(
                conversacion=conversacion,
                remitente=remitente,
                contenido=contenido
            )
            
            # Actualizar la fecha de actualización de la conversación
            conversacion.fecha_actualizacion = timezone.now()
            conversacion.save()
            
            serializer = MensajeSerializer(mensaje, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Conversacion.DoesNotExist:
            return Response(
                {'error': 'Conversación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def detalle(self, request, pk=None):
        """
        Obtiene el detalle completo de una conversación con todos sus mensajes
        GET /venta/conversaciones/{id}/detalle/
        """
        try:
            conversacion = self.get_object()
            serializer = ConversacionDetalleSerializer(conversacion, context={'request': request})
            return Response(serializer.data)
        except Conversacion.DoesNotExist:
            return Response(
                {'error': 'Conversación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

