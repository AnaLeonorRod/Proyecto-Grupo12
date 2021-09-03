from django.contrib import admin
from .models import Categoria, Pregunta, ElegirRespuesta, PreguntasRespondidas, QuizUsuario
from .forms import ElegirInlineFormset

class ElegirRespuestaInline(admin.TabularInline):
	model = ElegirRespuesta
	can_delete =False
	max_num = ElegirRespuesta.MAXIMO_RESPUESTA
	min_num = ElegirRespuesta.MAXIMO_RESPUESTA
	formset = ElegirInlineFormset

class PreguntaAdmin(admin.ModelAdmin):
	model = Pregunta
	inlines = (ElegirRespuestaInline, )
	list_display = ['texto','Selec_categoria']
	search_fields = ['texto', 'preguntas__texto']


class PreguntasRespondidasAdmin(admin.ModelAdmin):
	list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

	class Meta:
		model = PreguntasRespondidas

class CategoriaAdmin(admin.ModelAdmin):
	model= Categoria
	list_display=['nombre','descripcion']


admin.site.register(PreguntasRespondidas)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario)
admin.site.register(Categoria,CategoriaAdmin)