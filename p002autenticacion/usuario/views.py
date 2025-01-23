from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate,login #Para autenticar al usuario
from django.http import HttpResponse #Para enviar una respuesta al usuario
from django.contrib.auth.decorators import login_required #Para proteger una vista

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) #Recibir informacion
        if form.is_valid(): #Validar informacion
            cd= form.cleaned_data #Limpiar informacion
            user = authenticate(request, username=cd['username'], password=cd['password']) #Autenticar informacion
            
            if user is not None: #Si se encuentra informacion (usuario)
                if user.is_active: #Si esta activo tiene acceso a la app
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('Usuario inactivo')
            else:
                return HttpResponse('Usuario no encontrado')

    else: #GET -> enviamos el formulario de login al usuario
        form= LoginForm()

    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

    