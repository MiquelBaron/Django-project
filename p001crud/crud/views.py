from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
# Create your views here.

def task_list_and_create(request):
    if request.method =='POST':
        #Guardar tarea que nos envia el usuario
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_list')
    else:
        form = TaskForm()
    
    #tasks = Task.objects.all()
    
    completed_tasks= Task.objects.filter(is_created=True)
    incompleted_tasks = Task.objects.filter(is_created=False)

    return render(request, 'task_list.html', {
    'form': form, 
    #'tasks': tasks
    'completed_tasks': completed_tasks,
    'incompleted_tasks': incompleted_tasks
    })

def update_task(request,task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.is_created = not task.is_created #Si esta en true lo pone en false y viceversa
        task.save()
        return redirect('crud:crud_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    initial_data = {
        'title': task.title,
        'description': task.description
    }

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_list')
    else:
        form = TaskForm(instance=task, initial=initial_data)

    return render(request, 'edit_task.html', {'form': form})

def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('crud:crud_list')

def delete_all(request):
    if request.method == 'POST':
        Task.objects.all().delete()
    return redirect('crud:crud_list')


def navegar(request):
    return render(request, 'navegar.html')

def volver(request):
    return render(request, 'task_list.html')

    