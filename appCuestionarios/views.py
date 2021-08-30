from django.shortcuts import render
from .models import Cuest
from django.views.generic import ListView
from django.http import JsonResponse
from appPreguntas.models import Pregunta, Respuesta
from appRespuestas.models import Result

class CuestListView(ListView):
    model = Cuest
    template_name = 'cuest/main.html'

def cuest_view(request, pk):
    cuest = Cuest.objects.get(pk=pk)
    return render(request, 'cuest/cuest.html', {'obj': cuest})

def cuest_data_view(request, pk):
    cuest = Cuest.objects.get(pk=pk)
    preguntas = []
    for q in cuest.get_preguntas():
        respuestas = []
        for a in q.get_respuestas():
            respuestas.append(a.texto)
        preguntas.append({str(q): respuestas})
    return JsonResponse({
        'data': preguntas,
        'time': cuest.tiempo,
    })


# Obtiene  una lista de las preguntas
def save_cuest_view(request, pk):
    if request.is_ajax():
        preguntas = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            pregunta = Pregunta.objects.get(texto=k)
            preguntas.append(pregunta)
        print(preguntas)

        user = request.user
        cuest = Cuest.objects.get(pk=pk)

        score = 0
        appRespuestas = []
        respuesta_correcta = None

        # Recorremos las preguntas que salen al azar del cuest
        for q in preguntas:
            respuesta_sel = request.POST.get(q.texto)

            if respuesta_sel != "":
                pregunta_respuesta = Respuesta.objects.filter(pregunta=q)

                # verificamos si es una respuesta correcta e incrementamos el contador y retornamos la respuesta correcta
                for a in pregunta_respuesta:
                    if respuesta_sel == a.texto:
                        if a.correcto:
                            score += 1
                            respuesta_correcta = a.texto
                    else:
                        if a.correcto:
                            respuesta_correcta = a.texto
                # Referimos los resultados
                appRespuestas.append({str(q): {'respuesta_correcta': respuesta_correcta, 'respondido': respuesta_sel}})
            # En el caso de no ser respondida la pregunta
            else:
                appRespuestas.append({str(q): 'no respondido'})
            
        Result.objects.create(cuest=cuest, user=user, score=score)

        return JsonResponse({'Puntaje': score, 'Resultados': appRespuestas})