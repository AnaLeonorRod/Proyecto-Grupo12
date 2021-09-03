from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import random


class Categoria(models.Model):
	nombre=models.CharField(max_length=100)
	descripcion=models.CharField( max_length=800)
	
	
	def __str__(self):
		return self.nombre


class Pregunta(models.Model):

	NUMER_DE_RESPUESTAS_PERMITIDAS = 1
	Selec_categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE)
	autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	texto = models.CharField(max_length=200,verbose_name='Pregunta')
	max_puntaje = models.DecimalField(verbose_name='Maximo Puntaje', default=10, decimal_places=2, max_digits=6)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return self.texto 


class ElegirRespuesta(models.Model):

	MAXIMO_RESPUESTA = 3

	pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
	correcta = models.BooleanField(verbose_name='Esta es la correcta?', default=False, null=False)
	texto = models.CharField( max_length=100,verbose_name='Respuestas')


	def __str__(self):
		return self.texto

class QuizUsuario(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	puntaje_total = models.DecimalField(verbose_name='Puntaje Total', default=0, decimal_places=2, max_digits=10)


	def crear_intentos(self, pregunta):
		intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
		intento.save()

	def obtener_nuevas_preguntas(self):
		respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
		preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
		if not preguntas_restantes.exists():
			return None
		return random.choice(preguntas_restantes)


	def validar_intento(self, pregunta_respondida, respuesta_selecionada):
		if pregunta_respondida.pregunta_id != respuesta_selecionada.pregunta_id:
			return

		pregunta_respondida.respuesta_selecionada = respuesta_selecionada
		if respuesta_selecionada.correcta is True:
			pregunta_respondida.correcta = True
			pregunta_respondida.puntaje_obtenido = respuesta_selecionada.pregunta.max_puntaje
			pregunta_respondida.respuesta = respuesta_selecionada

		else:
			pregunta_respondida.respuesta = respuesta_selecionada

		pregunta_respondida.save()

		self.actualizar_puntaje()

	def actualizar_puntaje(self):
		puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(
			models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']

		self.puntaje_total = puntaje_actualizado
		self.save()

class PreguntasRespondidas(models.Model):
	quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
	correcta  = models.BooleanField(verbose_name='¿Es esta la respuesta correcta?', default=False, null=False)
	puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)