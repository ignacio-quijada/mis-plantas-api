from rest_framework import serializers
from .models import Planta, EventoCuidado

class EventoCuidadoSerializer(serializers.ModelSerializer):

    tipo_detalle = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = EventoCuidado
        fields = ['id', 'planta', 'tipo', 'tipo_detalle', 'fecha', 'observaciones']

class PlantaSerializer(serializers.ModelSerializer):
    eventos = EventoCuidadoSerializer(many=True, read_only=True)

    class Meta:
        model = Planta
        fields = [
            'id', 
            'nombre_comun', 
            'nombre_cientifico', 
            'metodo_cultivo', 
            'ubicacion_casa', 
            'fecha_plantacion', 
            'eventos'
        ]