from django.db import models
import random

DIFF_CHOICES = (
    ('Fácil', 'Fácil'),
    ('Medio', 'Medio'),
    ('Difícil', 'Difícil'),
)

class Cuest(models.Model):
    categoria = models.CharField(max_length=120)
    numero_de_preguntas = models.IntegerField()
    tiempo = models.IntegerField(help_text="Duración del cuestionario en minutos")
    dificultad = models.CharField(max_length=7, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.categoria}"

    def get_preguntas(self):
        preguntas = list(self.pregunta_set.all())
        random.shuffle(preguntas)
        return preguntas[:self.numero_de_preguntas]

    class Meta:
        verbose_name_plural = 'Cuestionarios'