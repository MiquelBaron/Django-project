from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login #Para autenticar al usuario
from django.http import HttpResponse #Para enviar una respuesta al usuario
from django.contrib.auth.decorators import login_required #Para proteger una vista
from .utils import get_cat_fact  # Importamos la función para obtener el dato curioso
from .forms import  UserRegistrationForm
from .models import Profile
from .forms import ProfileEditForm, UserEditForm, LoginForm
from django.contrib import messages

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


@login_required
def menu1(request):
    return render(request, 'menu1.html', {'section': 'menu1'})

@login_required
def menu2(request):
    return render(request, 'menu2.html', {'section': 'menu2'})

@login_required
def return_to_dashboard(request):
    return redirect('dashboard') #Redirigir a la vista dashboard

def cat_fact_view(request):
    fact_data = get_cat_fact()  # Llamamos a la función para obtener el dato curioso
    
    if fact_data:  # Si la respuesta es válida
        context = {
            'fact': fact_data['fact'],  # Extraemos el dato curioso
            'length': fact_data['length'],  # Longitud del dato curioso
        }
    else:
        context = {'error': 'No se pudo obtener un dato curioso.'}
    
    return render(request, 'cat_fact.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password']) #Encriptar contraseña
            new_user.save()
            Profile.objects.create(user = new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data = request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado', 'succesful')
        else:
            messages.error(request, 'Error al acualizar el perfil')
    else:
        user_form = UserEditForm(instance=request.user) #Precargando los formularios de user y profile con la informaciond de la bdd
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{
        'user_form':user_form,
        'profile_form': profile_form
    })