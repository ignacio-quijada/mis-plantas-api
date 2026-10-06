from rest_framework import viewsets
from .models import Planta, EventoCuidado
from .serializer import PlantaSerializer, EventoCuidadoSerializer

class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all().order_by('-id')
    serializer_class = PlantaSerializer

class EventoCuidadoViewSet(viewsets.ModelViewSet):
    queryset = EventoCuidado.objects.all().order_by('-fecha')
    serializer_class = EventoCuidadoSerializer
