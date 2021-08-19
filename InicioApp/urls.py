from django.urls import path
from InicioApp import views
from django.contrib.auth import views as auth_Views


urlpatterns = [
    path('home/', views.inicio, name="home"),
    path('login/', auth_Views.LoginView.as_view(template_name= "login/login.html"), name="login"),
    path('registro/', views.registro, name="registro"),
    

]
