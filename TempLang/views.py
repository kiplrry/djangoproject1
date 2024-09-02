from django.shortcuts import render, redirect
from django.contrib.auth import get_user, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserWithEmailCreationForm, TodoForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from .models import Todo

# Create your views here.

def login_view(request: HttpRequest):
    errors = None
    if get_user(request).is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                errors = {'errors': 'invalid credentials'}
        else:
            errors = form.errors
    context = {
        'errors': errors
    }
    return render(request, 'accounts/login.jinja', context)

def register_view(request: HttpRequest):
    errors = None
    if request.method == 'POST':
        form = UserWithEmailCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect('login')
        else:
            errors = form.errors
    context = {
        'errors': errors
    }
    return render(request, 'accounts/register.jinja', context)

@login_required(login_url='login')
def home_view(request):
    return redirect('todos')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def todos_view(request: HttpRequest):
    if request.method == 'POST':
        print('hit')
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.created_by = request.user
            todo.save()
    todos = Todo.objects.filter(created_by=request.user).all()
    query = request.GET.get('q')
    if query:
        todos = todos.filter(task__icontains=query)
        context = {
            'todos': todos
        }
        return render(request, 'todos.jinja', context)
    context = {
        'todos': todos
    }
    print(todos)
    return render(request, 'accounts/todos.jinja', context)


@login_required
def one_todo_view(request, pk):
    if request.method == 'POST':
        todo = Todo.objects.filter(id=pk, created_by=request.user).first()
        if todo:
            return render(request, 'accounts/todo.jinja', {'todo': todo})
    return redirect('todos')

@login_required
def todo_action_view(request, pk, act):
    todo = Todo.objects.filter(id=pk, created_by=request.user).first()
    if not todo:
        return redirect('todos')
    if request.method == 'POST':
        if act == 'del':
            todo.delete()
        if act == 'done':
            todo.completed = not todo.completed
            todo.save()
        if act == 'edit':
            errors = None
            form = TodoForm(request.POST, instance=todo)
            if form.is_valid():
                print(form.cleaned_data)
                form.save()
                return redirect('todos')
            else:
                errors = form.errors
                return render(request, 'accounts/todo.jinja', {'todo': todo, 'errors': errors})

    return redirect('todos')


@login_required
def all_todos_view(request):
    todos = Todo.objects.filter(created_by=request.user).all()
    context = {
        'todos': todos
    }

    return render(request, 'todos.jinja', context)