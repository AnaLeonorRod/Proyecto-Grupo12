from django.urls import path
from InicioApp import views
from django.contrib.auth import views as auth_Views
from appCuestionarios.views import cuest_view


urlpatterns = [
    path('home/', views.inicio, name="home"),
    path('login/', auth_Views.LoginView.as_view(template_name= "registration/login.html"), name="login"),
    path('registro/', views.registro, name="registro"),
    path('logout/', auth_Views.LogoutView.as_view(), name = 'logout'),
    path('admi/', views.administrador, name= 'admi'),
    path('user/', views.usuario, name= 'user'),
    path('<pk>/juego/', cuest_view, name='quiz-view'),
    path('agregar/', views.agregar, name= 'agregar'),
    path('editar/',views.editar, name="editar"),
    path('listar/',views.ListarPreguntas, name="listar"),
]