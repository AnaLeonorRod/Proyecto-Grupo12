from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def inicio(request):
    return render(request, "index.html")


def registro(request):
    if request.method == "POST":
        FormReg = UserCreationForm(request.POST)
        
        if FormReg.is_valid():
            FormReg.save()
            return redirect('login')
    else:
        FormReg= UserCreationForm()

    return render(request, "login/registro.html", {'FormReg': FormReg})