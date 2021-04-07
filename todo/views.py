from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.

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

