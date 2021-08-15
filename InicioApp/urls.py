from django.urls import path
from InicioApp import views

urlpatterns = [
    path('home/', views.inicio, name="home")
]
