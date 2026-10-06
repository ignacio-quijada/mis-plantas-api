import requests
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

        clima_actual = {}
        try:
            url_clima = "https://api.open-meteo.com/v1/forecast?latitude=-36.79&longitude=-73.12&current=temperature_2m,relative_humidity_2m"
            respuesta_clima = requests.get(url_clima, timeout=5)
            if respuesta_clima.status_code == 200:
                datos_json = respuesta_clima.json()
                clima_actual = {
                    'temperatura_c': datos_json['current']['temperature_2m'],
                    'humedad_relativa_porcentaje': datos_json['current']['relative_humidity_2m'],
                }
        except requests.RequestException:
            clima_actual = {'detalle': 'No se pudo conectar con la API meteorológica'}

        return Response({
            'condiciones_ambientales_actuales': clima_actual,
            'total_ejemplares': total_plantas,
            'distribucion_por_cultivo': por_metodo,
            'ranking_cuidados': plantas_con_mas_cuidados,
        })

    @action(detail=True, methods=['get'])
    def taxonomia_gbif(self, request, pk=None):
        planta = self.get_object()
        nombre_buscar = planta.nombre_cientifico or planta.nombre_comun

        url_gbif = "https://api.gbif.org/v1/species/match"
        parametros = {'name': nombre_buscar}

        try:
            respuesta = requests.get(url_gbif, params=parametros, timeout=5)
            datos_gbif = respuesta.json()

            return Response({
                'planta_local_sql': {
                    'id': planta.id,
                    'nombre_comun': planta.nombre_comun,
                    'nombre_cientifico_registrado': planta.nombre_cientifico,
                },
                'datos_remotos_gbif': {
                    'nombre_cientifico_validado': datos_gbif.get('scientificName'),
                    'reino': datos_gbif.get('kingdom'),
                    'filo_division': datos_gbif.get('phylum'),
                    'clase': datos_gbif.get('class'),
                    'orden': datos_gbif.get('order'),
                    'familia': datos_gbif.get('family'),
                    'genero': datos_gbif.get('genus'),
                    'confianza_coincidencia': datos_gbif.get('confidence'),
                }
            })
        except requests.RequestException:
            return Response({'error': 'No se pudo conectar con el servidor de GBIF'}, status=503)

class EventoCuidadoViewSet(viewsets.ModelViewSet):
    queryset = EventoCuidado.objects.select_related('planta').all().order_by('-fecha')
    serializer_class = EventoCuidadoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'planta']
