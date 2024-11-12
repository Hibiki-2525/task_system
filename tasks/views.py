from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, SubFunction


def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subfunctions = SubFunction.objects.filter(task=task, parent=None)

    return render(request, 'tasks/task_detail.html', {'task': task, 'subfunctions': subfunctions})