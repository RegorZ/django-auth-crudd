from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.

from django.http import HttpResponse
# importar metodo que contiene formulario de django UserCreationForm
# importar metodo que contiene formulario de atentificacion AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# modelo de guardar o registrar usuarios:
from django.contrib.auth.models import User
# crear una cokkie, navegador sepa que user esta atenticado o no
from django.contrib.auth import login, logout, authenticate
# manegar integrityerror para error de integridad en base de datos se coloca como buena parctica
from django.db import IntegrityError
# importar formulario para crear tasks desde forms.py
from .forms import TaskForm
# importar modelos de las tareas
from .models import Task
#importar timezone para agregar la fecha/hora
from django.utils import timezone
#decorador de cada funcion para protegerlo
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # desde login te paso los parametros, y el usuario que queremos guardar
                login(request, user)
                return redirect('tasks')
            # integrar error, excepciones a un error en especifico
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'username already exist'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'password do not match'
        })

@login_required
def tasks(request):
    # almacenar en la variable todas las tareas del user actual,
    # .filter(datecompleted__isnull=True) podemos usarlo para mostrar solo tareas que no estan con fechasc completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    # almacenar en la variable todas las tareas del user actual,
    # .filter(datecompleted__isnull=True) podemos usarlo para mostrar solo tareas que no estan con fechasc completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')

    return render(request, 'tasks.html', {
        'tasks': tasks
    })


@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })

    else:
        try:
            # Usamos el forms que hicimos para el envio post(taksform) y lo guardamos en la variable
            form = TaskForm(request.POST)
            # guardamos en una varibale el form con el save y (commit=False) le decimos que no se guarde directamente
            # devolvemos los datos dentro del form en la variable:
            new_task = form.save(commit=False)
            # le agregamos el user con el cookkie token actual
            new_task.user = request.user
            # guarda y genera datos en la db
            new_task.save()

            return redirect('tasks')

        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'please improvide valide data'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # manera normal: obtienes el pk y la emparejas a task_id, y la guardas en task:
        # task = Task.objects.get(pk=task_id)
        # obtienes el dato pero si no hay ese objeto entonces lanza error 404:     #nos aseguramos de convalidad el ID del user activo
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # llamamos al form y le instanciamos con la variable para rellenar los datos de esa tarea y lo guardamos en una varibaole form
        form = TaskForm(instance=task)

        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:                                            #nos aseguramos de convalidad el ID del user activo
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            #tma los nuevos datos mandado desde post , lo instancia y se guarda
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')

        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'error updating task'
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'username or password is incorrect'
            })
        else:
            # save sesion user / redireccionar
            login(request, user)
            return redirect('tasks')
