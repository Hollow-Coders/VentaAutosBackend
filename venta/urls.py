from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import auth

router = DefaultRouter()
router.register('vehiculos', views.VehiculoViewSet)
router.register('documentos', views.DocumentoViewSet)
router.register('logs_actividad', views.LogActividadViewSet)
router.register('marcas', views.MarcaViewSet)
router.register('modelos', views.ModeloViewSet)
router.register('pujas', views.PujaViewSet)
router.register('roles', views.RolViewSet)
router.register('solicitudes_verificacion', views.SolicitudVerificacionViewSet)
router.register('subastas', views.SubastaViewSet)
router.register('usuarios', views.UsuarioViewSet)
router.register('vehiculo_fotos', views.VehiculoFotoViewSet)
router.register('ventas', views.VentaViewSet)
router.register('perfiles', views.PerfilViewSet)
router.register('catalogo', views.CatalogoViewSet, basename='catalogo')
router.register('conversaciones', views.ConversacionViewSet)
router.register('mensajes', views.MensajeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('login/', auth.LoginView.as_view(), name='login'),  
]

