from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .models import Planta, EventoCuidado
from .serializer import PlantaSerializer, EventoCuidadoSerializer

class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all().order_by('-id')
    serializer_class = PlantaSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['metodo_cultivo', 'ubicacion_casa']
    search_fields = ['nombre_comun', 'nombre_cientifico','ubicacion_casa']
    ordering_fields = ['nombre_comun', 'fecha_plantacion']

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        total_plantas = Planta.objects.count()
        
        por_metodo = (
            Planta.objects
            .values('metodo_cultivo')
            .annotate(cantidad=Count('id'))
            .order_by('-cantidad')
        )

        plantas_con_mas_cuidados = (
            Planta.objects
            .annotate(total_eventos=Count('eventos'))
            .values('nombre_comun', 'nombre_cientifico', 'total_eventos')
            .order_by('-total_eventos')
        )

        return Response({
            'total_ejemplares': total_plantas,
            'distribucion_por_cultivo': por_metodo,
            'ranking_cuidados': plantas_con_mas_cuidados,
        })


class EventoCuidadoViewSet(viewsets.ModelViewSet):
    queryset = EventoCuidado.objects.select_related('planta').all().order_by('-fecha')
    serializer_class = EventoCuidadoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'planta']
