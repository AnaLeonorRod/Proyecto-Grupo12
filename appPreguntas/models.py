from django.db import models
from appCuestionarios.models import Cuest

class Pregunta(models.Model):
    texto = models.CharField(max_length=200)
    cuest = models.ForeignKey(Cuest, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.texto)

    def get_respuestas(self):
        return self.respuesta_set.all()

class Respuesta(models.Model):
    texto = models.CharField(max_length=200)
    correcto = models.BooleanField(default=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pregunta: {self.pregunta.texto}, respuesta: {self.texto}, correcto: {self.correcto}"