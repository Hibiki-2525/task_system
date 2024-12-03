from django.shortcuts import render, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Task, SubFunction, Answer_bemodel, Answer_code, BehaviorModel_A, BehaviorModel_B, Card


def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks': tasks})

def organize(request, task_id):
    # タスクの取得
    task = get_object_or_404(Task, id=task_id)
    sub_functions = task.subfunctions.filter(parent=None)
    # ルート（親なし）のサブ機能を取得して構造を作成
    correct_structure = get_correct_structure(task)
    # JSON形式で正解構造をテンプレートに渡す
    context = {
        'task': task,
        'sub_functions': sub_functions,
        'correct_structure_json': json.dumps(correct_structure, cls=DjangoJSONEncoder),
    }
    return render(request, 'tasks/organize.html', context)

# 再帰的に子サブ機能を取得する関数
def get_correct_structure(task):
    # トップレベルのサブ機能から再帰的に構造を構築
    return [
        build_structure(subfunction)
        for subfunction in task.subfunctions.filter(parent=None)
    ]

def build_structure(subfunction):
    return {
        "id": subfunction.id,
        "name": subfunction.name,
        "children": [
            build_structure(child) for child in subfunction.children.all()
        ]
    }

def bemodel(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subfunctions = get_task_order(task_id)
    a_choices = BehaviorModel_A.objects.filter(task=task)
    b_choices = BehaviorModel_B.objects.filter(task=task)
    # 最初のタスクを表示する
    current_subfunction = subfunctions.pop(0) if subfunctions else None

    request.session['remaining_tasks'] = [sf.id for sf in subfunctions]  # セッションに保存
    context = {
        'task': task,
        'current_subfunction': current_subfunction,
        'a_choices': a_choices,
        'b_choices': b_choices,
    }

    return render(request, 'tasks/bemodel.html', context)

def get_task_order(task_id):
    from collections import deque

    # タスクとその関連するSubFunctionを取得
    root_task = Task.objects.get(id=task_id)
    all_subfunctions = SubFunction.objects.filter(task=root_task)

    # 子ノードから順に処理するための順番を格納するリスト
    sorted_tasks = []

    # 再帰的に子ノードを探索する関数
    def traverse(node):
        for child in node.children.all():
            traverse(child)  # 再帰的に子を探索
        sorted_tasks.append(node)

    # ルートレベルのSubFunctionから探索を開始
    for subfunction in all_subfunctions.filter(parent=None):
        traverse(subfunction)

    return sorted_tasks

def next_bemodel(request, task_id):
    if request.method == "POST":
        # セッションから次のタスク順序を取得
        remaining_tasks = request.session.get('remaining_tasks', [])
        if not remaining_tasks:
            return redirect('quiz')  # 全てのタスクが完了したら別のビューへ

        # 次のタスクIDを取得して削除
        next_task_id = remaining_tasks.pop(0)
        request.session['remaining_tasks'] = remaining_tasks  # 更新

        # 次のタスクのSubFunctionを取得
        current_subfunction = SubFunction.objects.get(id=next_task_id)

        context = {
            'task': Task.objects.get(id=task_id),
            'current_subfunction': current_subfunction,
            'a_choices': BehaviorModel_A.objects.filter(task_id=task_id),
            'b_choices': BehaviorModel_B.objects.filter(task_id=task_id),
        }
        return render(request, 'tasks/bemodel.html', context)

def quiz(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subfunctions = get_task_order(task_id)
    current_subfunction = subfunctions.pop(0) if subfunctions else None
    cards = task.Card.filter(task=task)  # カードを取得
    context = {
        'task': task,
        'current_subfunction': current_subfunction,
        'cards': cards,
    }
    return render(request, 'tasks/quiz.html', context)