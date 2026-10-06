from django.db import models

class Planta(models.Model):
    METODO_CULTIVO =[
        ('MACETA', 'En maceta (sustrato)'),
        ('AGUA', 'En agua'),
        ('SUELO', 'Directo en suelo'),
    ]

    nombre_comun = models.CharField(max_length=100, help_text="Ejemplo: Canelo, Arrayán, Manolito, etc.")
    nombre_cientifico = models.CharField(max_length=100, help_text="Ejemplo: Drimys winteri, Luma apiculata, etc.")
    metodo_cultivo = models.CharField(max_length=20, choices=METODO_CULTIVO, help_text="Selecciona el método de cultivo de la planta.")
    ubicacion_casa = models.CharField(max_length=100, help_text="Ejemplo: Ventana, Cocina, Dormitorio, etc.")
    fecha_plantacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico or 'Sin clasificar'}))"

class EventoCuidado(models.Model):
    TIPOS_EVENTO = [
        ('RIEGO', 'Riego / Cambio de agua'),
        ('RAIZ', 'Brote de raíces nuevas'),
        ('HOJA', 'Brote de hojas nuevas'),
        ('ABONO', 'Aplicación de abono / fertilizante'),
        ('PODA', 'Poda de hojas o raíces'),
    ]

    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=20, choices=TIPOS_EVENTO, help_text="Selecciona el tipo de evento de cuidado realizado.")
    fecha = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, help_text="Ej: Salió la primera raíz de 1 cm en agua")

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.planta.nombre_comun} ({self.fecha})"