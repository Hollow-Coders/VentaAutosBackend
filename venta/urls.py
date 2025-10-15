from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('vehiculos', views.VehiculoViewSet)
router.register('documento', views.DocumentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

