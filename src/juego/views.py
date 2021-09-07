from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroFormulario, UsuarioLoginFormulario, CategoriaForm,RespuestaForm, PreguntaForm
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import QuizUsuario, Pregunta, PreguntasRespondidas, Categoria ,ElegirRespuesta
from datetime import datetime
from django.urls import reverse_lazy

from django.contrib.auth.decorators import user_passes_test


def inicio(request):
	context = {
		'bienvenido': 'Bienvenido'
	}

	return render(request, 'index.html', context)

# Views del Administrador
# def es_admin(user):
# 	return user.groups.filter(name='admin').exists()


@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('HomeUsuario'))
def HomeAdministrador(request):

	return render(request, 'administrador/home_admin.html')

# @login_required()
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('HomeUsuario'))
def crear_categoria(request):
	categoriaForm=CategoriaForm()
	if request.method=='POST':
		categoriaForm=CategoriaForm(request.POST)
		if categoriaForm.is_valid():
			categoriaForm.save()
		return redirect('agregar_pregunta')
		
	return render(request, 'administrador/crear_categoria.html', {'categoriaForm': categoriaForm})


# @login_required()
# @user_passes_test(es_admin)
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('HomeUsuario'))
def agregar_pregunta(request):
    preguntaForm=PreguntaForm()
    if request.method=='POST':
        preguntaForm=PreguntaForm(request.POST)
        if preguntaForm.is_valid():
            texto=preguntaForm.save(commit=False)
            Selec_categoria=Categoria.objects.get(id=request.POST.get('categoria'))
            texto.Selec_categoria=Selec_categoria
            texto.save() 
       
    return render(request,'administrador/agregar_pregunta.html',{'preguntaForm':preguntaForm})

# @login_required()
# @user_passes_test(es_admin)
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('HomeUsuario'))
def agregar_respuesta(request):
	respuestaForm= RespuestaForm()
	if request.method=='POST':
		respuestaForm=RespuestaForm(request.POST)
		if respuestaForm.is_valid():
			texto=respuestaForm.save(commit=False)
			pregunta=Pregunta.objects.get(id=request.POST.get('pregunta'))
			texto.pregunta=pregunta
			texto.save()
	
	return render(request, 'administrador/agregar_respuesta.html', {'respuestaForm' : respuestaForm})

# @login_required()
# @user_passes_test(es_admin)
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('HomeUsuario'))
def ver_categoria(request):
	categoria=Categoria.objects.all()
	return render(request, 'administrador/ver_categoria.html',{'categoria':categoria})

# @login_required()
# @user_passes_test(es_admin)
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('HomeUsuario'))
def ver_preguntas(request):
	preguntas=Pregunta.objects.all()
	return render(request, 'administrador/ver_preguntas.html',{'preguntas':preguntas})

# @login_required()
# @user_passes_test(es_admin)
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('HomeUsuario'))
def ver_respuestas(request):
	respuesta=ElegirRespuesta.objects.all()
	return render(request, 'administrador/ver_respuestas.html',{'respuesta':respuesta})


#### desde aqui estan los views de los jugadores 

@login_required()
def HomeUsuario(request):

	return render(request, 'juego/home.html')

@login_required()
def tablero(request):
	total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
	contador = total_usaurios_quiz.count()

	context = {

		'usuario_quiz':total_usaurios_quiz,
		'contar_user':contador
	}

	return render(request, 'juego/tablero.html', context)


@login_required()
def jugar(request):

	QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)

	if request.method == 'POST':
		pregunta_pk = request.POST.get('pregunta_pk')
		pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
		respuesta_pk = request.POST.get('respuesta_pk')

		try:
			opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
		except ObjectDoesNotExist:
			raise Http404

		QuizUser.validar_intento(pregunta_respondida, opcion_selecionada)

		return redirect('resultado', pregunta_respondida.pk)

	else:
		pregunta = QuizUser.obtener_nuevas_preguntas()
		if pregunta is not None:
			QuizUser.crear_intentos(pregunta)

		context = {
			'pregunta':pregunta
		}

	return render(request, 'juego/jugar.html', context)


@login_required()
def resultado_pregunta(request, pregunta_respondida_pk):
	respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)

	context = {
		'respondida':respondida
	}
	return render(request, 'juego/resultados.html', context)

def loginView(request):
	titulo = 'login'
	form = UsuarioLoginFormulario(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		usuario = authenticate(username=username, password=password)
		login(request, usuario)
		return redirect('HomeUsuario')

	context = {
		'form':form,
		'titulo':titulo
	}

	return render(request, 'login.html', context)

def registro(request):

	titulo = 'Crear una Cuenta'
	if request.method == 'POST':
		form = RegistroFormulario(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = RegistroFormulario()

	context = {

		'form':form,
		'titulo': titulo

	}

	return render(request, 'registro.html', context)


def logout_vista(request):
	logout(request)
	return redirect('/')


    