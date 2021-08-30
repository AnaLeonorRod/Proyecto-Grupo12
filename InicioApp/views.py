from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



@login_required(login_url= '/')
def inicio(request):
    return render(request, "home.html")


def registro(request):
    if request.method == "POST":
        FormReg = UserCreationForm(request.POST)
        
        if FormReg.is_valid():
            FormReg.save()
            return redirect('login')
    else:
        FormReg= UserCreationForm()

    return render(request, "registration/registro.html", {'FormReg': FormReg})


@staff_member_required
def administrador(request):
    return render(request, 'administrador/administrador_central.html')



@login_required(login_url= '/')
def usuario(request):
    return render(request, 'jugador/jugador_central.html')