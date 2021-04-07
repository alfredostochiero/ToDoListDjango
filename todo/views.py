from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signupuser(request):
    context = {'form': UserCreationForm()}
    if request.method == 'GET':
        return render(request, 'signupuser.html',context)
    else :
        # Cria um usuário novo
        username = request.POST['username']
        first_password = request.POST['password1']
        second_password = request.POST['password2']
        if first_password == second_password:
            try:
                user = User.objects.create_user(username, password=first_password)
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                context['error'] = 'Nome de usuário já existe'
                return render(request, 'signupuser.html', context)

        else :
            context['error'] = 'Senhas não são iguais'
            # avisa o usuário que as senhas não batem
            return render(request, 'signupuser.html', context)

def currenttodos(request):
    return render(request,'currenttodos.html')

def loginuser(request):
    context = {'form': AuthenticationForm()}
    if request.method == 'GET':
        return render(request, 'loginuser.html', context)
    else:
        usenarme = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=usenarme, password=password)
        if user is None:
            context['error'] = 'Usuário ou senha errados'
            return render(request, 'loginuser.html', context)
        else :
            login(request, user)
            return redirect('currenttodos')






def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


