from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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





@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html', {'form': TodoForm()})
    else :
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'createtodo.html', {'form': TodoForm(), 'error': 'Erro em um dos campos!Tente novamente'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'currenttodos.html',{'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'completedtodos.html',{'todos':todos})


@login_required
def viewtodo(request, todo_pk):

    todo = get_object_or_404(Todo, pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'viewtodo.html', {'todo': todo, 'form': form})
    else :
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'viewtodo.html', {'todo': todo, 'form': form,'error':'Erro no formulario'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


