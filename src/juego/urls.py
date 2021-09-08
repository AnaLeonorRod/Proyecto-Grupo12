from django.urls import path
from .views import (
			inicio,registro,loginView, 
			logout_vista,HomeUsuario, jugar,
			resultado_pregunta,tablero,crear_categoria,agregar_pregunta,
			agregar_respuesta, HomeAdministrador,ver_categoria,ver_preguntas,
			ver_respuestas,ver_estadisticas
			)

urlpatterns = [
	#urls de jugadores
	path('', inicio, name='inicio'),
	path('HomeUsuario/', HomeUsuario, name='HomeUsuario'),
	path('login/', loginView, name='login'),
	path('logout_vista/', logout_vista, name='logout_vista'),
	path('registro/', registro, name='registro'),
	path('tablero/', tablero, name='tablero'),	
	path('jugar/', jugar, name='jugar'),
	path('resultado/<int:pregunta_respondida_pk>', resultado_pregunta, name='resultado'),
	#urls de administrador 
	path('crear_categoria', crear_categoria,name='crear_categoria'),
	path('agregar_pregunta', agregar_pregunta,name='agregar_pregunta'),
	path('agregar_respuesta', agregar_respuesta,name='agregar_respuesta'),
	path('HomeAdministrador/', HomeAdministrador, name='HomeAdministrador'),
	path('ver_categoria/', ver_categoria, name='ver_categoria'),
	path('ver_preguntas/', ver_preguntas, name='ver_preguntas'),
	path('ver_respuestas/', ver_respuestas, name='ver_respuestas'),
	path('estadisticas/', ver_estadisticas, name='estadisticas'),
]