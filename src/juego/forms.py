from django import forms
from .models import  Pregunta, ElegirRespuesta, PreguntasRespondidas, Categoria
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model



User = get_user_model()


class CategoriaForm(forms.ModelForm):
	class Meta:
		model=Categoria
		fields=['nombre','descripcion']


class PreguntaForm(forms.ModelForm):
	categoria=forms.ModelChoiceField(queryset=Categoria.objects.all())
	class Meta:
		model=Pregunta
		fields=[
			'texto','max_puntaje','autor'
		]
		widgets = {
            'texto': forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }


class RespuestaForm(forms.ModelForm):
	pregunta=forms.ModelChoiceField(queryset=Pregunta.objects.all())
	class Meta:
		model=ElegirRespuesta
		
		fields=[
			'pregunta','texto','correcta'
		]

		widgets = {
            'texto': forms.Textarea(attrs={'rows': 2, 'cols': 50})
        }



class ElegirInlineFormset(forms.BaseInlineFormSet):
	def clean(self):
		super(ElegirInlineFormset, self).clean()

		respuesta_correcta = 0
		for formulario in self.forms:
			if not formulario.is_valid():
				return

			if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
				respuesta_correcta += 1

		try:
			assert respuesta_correcta == Pregunta.NUMER_DE_RESPUESTAS_PERMITIDAS
		except AssertionError:
			raise forms.ValidationError('Exactamente una sola respuesta es permitida')


class UsuarioLoginFormulario(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Este usuario No existe")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("Este Usuario No esta activo")

		return super(UsuarioLoginFormulario, self).clean(*args, **kwargs)



class RegistroFormulario(UserCreationForm):
	email = forms.EmailField(required=True)
	nombre = forms.CharField(required=True)
	apellido = forms.CharField(required=True)

	class Meta:
		model = User 

		fields = [

			'nombre',
			'apellido',
			'username',
			'email',
			'password1',
			'password2'

		]