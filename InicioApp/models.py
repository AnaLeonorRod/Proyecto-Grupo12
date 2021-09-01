# from django import db
from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse

class Usuarios(CreateView): # modelo modificado... se tiene que hacer de nuevo la migracion :S
    model = User
    template_name = "registration/login.html"
    form_class = UserCreationForm
    success_url = reverse('home')    
    class Meta:
        db_table = 'usuarios'