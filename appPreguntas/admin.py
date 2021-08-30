from django.contrib import admin
from .models import Pregunta, Respuesta

class RespuestaInline(admin.TabularInline):
    model = Respuesta

class PreguntaAdmin(admin.ModelAdmin):
    inlines = [RespuestaInline]

admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta)