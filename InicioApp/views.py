from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from appPreguntas.models import Pregunta



# @login_required(login_url= '/')
def inicio(request):
    return render(request, "home.html")


def registro(request):
    if request.method == "POST":
        FormReg = UserCreationForm(request.POST)
        
        if FormReg.is_valid():
            FormReg.save()
            return redirect('home')
    else:
        FormReg= UserCreationForm()

    return render(request, "registration/registro.html", {'FormReg': FormReg})


@staff_member_required
def administrador(request):
    return render(request, 'administrador/administrador_central.html')



#@login_required(login_url= '/')
def usuario(request):
    return render(request, 'jugador/jugador_central.html')

def agregar(request): 
    return render(request, 'administrador/agregar_p.html') 

def editar(request): 
    preg = Pregunta.objects.all()
    form = preg(instance=Pregunta)
    
    return(request, "editar",{'form':form})

def actualizar(request): 
    preg = Pregunta.objects.all() # debe cambiarse .all() --> .get(pk=id_preg)
    
    form = preg(request.POST, instance=Pregunta)
    if form.es_valid():
        form.save()
    preg = Pregunta.objects.all()
    return(request, "editar",{'form':form})

def ListarPreguntas(request):
    preguntas=Pregunta.objects.all()
    return render(request, "listar.html", {'preguntas':preguntas})