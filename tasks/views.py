from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, SubFunction, BehaviorModel_A, BehaviorModel_B


def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks': tasks})

def organize(request, task_id):
    # 指定されたtask_idに基づいてタスクを取得
    task = get_object_or_404(Task, id=task_id)
    # 関連するサブ機能を取得（親が存在しないものから始める）
    sub_functions = task.subfunctions.filter(task=task, parent=None)

    context = {
        'task': task,
        'sub_functions': sub_functions,
    }
    return render(request, 'tasks/organize.html', context)

def bemodel(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    a_choices = BehaviorModel_A.objects.filter(task=task)
    b_choices = BehaviorModel_B.objects.filter(task=task)

    context = {
        'task': task,
        'a_choices': a_choices,
        'b_choices': b_choices,
    }

    return render(request, 'tasks/bemodel.html', context)