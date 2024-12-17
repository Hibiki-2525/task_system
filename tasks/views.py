from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder
import json
import random
from .models import Task, SubFunction, Answer_bemodel, Answer_code, BehaviorModel_A, BehaviorModel_B, Card, SubFunctionVarValue, task_Answer_bemodel, task_Answer_code, TaskVarValue, Test, TestCard, PreTestAnswer, ProTestAnswer
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect

def home(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks/home.html',context)

def organize(request, task_id):
    request.session.clear()
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
    storage = get_messages(request)
    storage.used = True  # メッセージをクリア
    task = get_object_or_404(Task, id=task_id)
    # 振る舞いモデル選択肢
    a_choices = BehaviorModel_A.objects.filter(task=task)
    b_choices = BehaviorModel_B.objects.filter(task=task)
    a_choices_dict = {a_choice.id: a_choice.name for a_choice in a_choices}
    b_choices_dict = {b_choice.id: b_choice.name for b_choice in b_choices}

    # セッションから進行状況を取得
    remaining_tasks = request.session.get('remaining_tasks', None)
    if remaining_tasks is None:
        subfunctions = get_subfunction_order(task_id)
        request.session['remaining_tasks'] = [sf.id for sf in subfunctions]
        remaining_tasks = request.session['remaining_tasks']

    if not remaining_tasks:
        del request.session['remaining_tasks']  # セッションをクリア
        return redirect(reverse('tasks:finalbe', args=[task_id]))  # 全て完了したら終了画面へ

    # 現在のタスクを取得
    current_subfunction_id = remaining_tasks[0]
    current_subfunction = get_object_or_404(SubFunction, id=current_subfunction_id)
    
    subfunction_vars = SubFunctionVarValue.objects.filter(subfunction=current_subfunction)
    inputs = {var.var.name: var.value for var in subfunction_vars}  # var.nameをキーにしてinputsを作成
    outputs = {key: 0 for key in inputs}
    # 初回アクセス時の回答がセッションに保存されているか確認
    bemodel_answers = None
    error_flag = False
    error_message = ""
    if request.method == 'POST':
        storage = get_messages(request)
        storage.used = True 
        # ユーザーの回答を取得し、タプルとしてまとめる
        user_answers = request.POST.getlist('bemodel_answers[]')  # ユーザーの回答（リスト）
        user_answer_tuples = [(int(user_answers[i]), int(user_answers[i+1]), int(user_answers[i+2])) 
                      for i in range(0, len(user_answers), 3)]
               # a_choices と b_choices を辞書に変換し、id → name にアクセスできるようにする
        a_choices_dict = {a_choice.id: a_choice.name for a_choice in a_choices}
        b_choices_dict = {b_choice.id: b_choice.name for b_choice in b_choices}

        # ユーザーの回答（id）からnameに変換
        bemodel_answers = []
        for i in range(0, len(user_answers), 3):
            var1_id = int(user_answers[i])      # 最初の変数 (例: "min" の id)
            var2_id = int(user_answers[i+1])       # 関係 (例: "と等しい")
            relation_id = int(user_answers[i+2])    # 比較対象 (例: "a" の id)

            # idからnameに変換
            var1_name = a_choices_dict.get(var1_id, None)  # a_choices から変数名を取得
            var2_name = a_choices_dict.get(var2_id, None)  # b_choices から変数名を取得
            relation = b_choices_dict.get(relation_id, None)  # b_choices から変数名を取得
             # サブ関数の変数チェック
            if var1_name not in inputs or var2_name not in inputs:
                error_flag = True
                error_message = "選択された変数が許可されていません。"
                break
            # タプルに変換
            bemodel_answers.append((var1_name, var2_name ,relation))
        if error_flag:
            messages.error(request, error_message)
            return redirect(request.path)  # 現在のページを再読み込み
        # 計算を実行
        outputs = calculate_outputs(bemodel_answers, inputs)
        # 正解の回答を取得し、タプルとしてまとめる
        correct_answers = Answer_bemodel.objects.filter(sub_function=current_subfunction).values_list('behavior_model_a_1', 'behavior_model_a_2','behavior_model_b')
        correct_answer_tuples = [tuple(correct_answer) for correct_answer in correct_answers]

        if set(user_answer_tuples) == set(correct_answer_tuples):
            return redirect(reverse('tasks:quiz', args=[task_id]))  # 次のクイズに進む

        else:
            # 不正解の場合のフィードバック
            extra = set(user_answer_tuples) - set(correct_answer_tuples)
            missing = set(correct_answer_tuples) - set(user_answer_tuples)
            if extra or missing:
                feedback = []
                if extra:
                    feedback.append(f"余分な振る舞いモデルがあります")
                if missing:
                    feedback.append(f"足りない振る舞いモデルがあります")
                messages.error(request, "不正解です。" + " ".join(feedback))
            else:
                messages.error(request, "不正解です。もう一度試してください。")
    context = {
        'task': task,
        'current_subfunction': current_subfunction,
        'a_choices': a_choices,
        'b_choices': b_choices,
        'inputs': inputs,   # SubFunctionVarValueから取得した入力値
        'outputs': outputs, # 計算された出力
        'bemodel_answers': bemodel_answers,
    }
    return render(request, 'tasks/bemodel.html', context)

def next_bemodel(request, task_id):
    remaining_tasks = request.session.get('remaining_tasks', [])
    if remaining_tasks:
        # 次のタスクに進む
        remaining_tasks.pop(0)
        request.session['remaining_tasks'] = remaining_tasks

    # まだタスクが残っている場合は bemodel にリダイレクト
    if remaining_tasks:
        return redirect(reverse('tasks:bemodel', args=[task_id]))

    # 全て完了した場合は終了画面へ
    return redirect(reverse('tasks:finalbe', args=[task_id]))


def quiz(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # セッションから進行状況を取得
    remaining_tasks = request.session.get('remaining_tasks', None)
    if not remaining_tasks:
        return redirect(reverse('tasks:finalbe', args=[task_id]))  # 全て完了したら終了画面へ

    # 現在のタスクを取得
    current_subfunction_id = remaining_tasks[0]
    current_subfunction = get_object_or_404(SubFunction, id=current_subfunction_id)
    bemodel = Answer_bemodel.objects.filter(sub_function=current_subfunction).select_related('behavior_model_a_1', 'behavior_model_a_2', 'behavior_model_b')
    bemodel_list =[]
    for item in bemodel:
        # 各フィールドの値をリストに格納
        bemodel_list.append([item.behavior_model_a_1.name, item.behavior_model_a_2.name, item.behavior_model_b.name])    
    cards = list(Card.objects.filter(task=task))
    # カードリストをシャッフル
    random.shuffle(cards)
    # 正解のデータ（解答順）を取得
    correct_answer = Answer_code.objects.get(sub_function=current_subfunction)
    correct_answer_list = correct_answer.get_correct_answer_list()
    # フォームが送信されると次のページに遷移
    if request.method == "POST":
        return redirect(reverse('tasks:next_bemodel', args=[task.id]))

    context = {
        'task': task,
        'current_subfunction': current_subfunction,
        'cards': cards,
        'correct_answer_list': correct_answer_list,  # 正解データを送信    
        'bemodel_list': bemodel_list,
        }
    return render(request, 'tasks/quiz.html', context)

def get_subfunction_order(task_id):
    from collections import deque
    task = get_object_or_404(Task, id=task_id)
    # タスクとその関連するSubFunctionを取得
    all_subfunctions = SubFunction.objects.filter(task=task)

    # 子ノードから順に処理するための順番を格納するリスト
    sorted_tasks = []

    # 再帰的に子ノードを探索する関数
    def traverse(node):
        for child in node.children.all():
            traverse(child)  # 
        if node.is_special:
            return
        
        sorted_tasks.append(node)

    # ルートレベルのSubFunctionから探索を開始
    for subfunction in all_subfunctions.filter(parent=None):
        traverse(subfunction)

    return sorted_tasks

def finalbe(request, task_id):
    storage = get_messages(request)
    storage.used = True  # メッセージをクリア
    task = get_object_or_404(Task, id=task_id)
    # 振る舞いモデル選択肢
    a_choices = BehaviorModel_A.objects.filter(task=task)
    b_choices = BehaviorModel_B.objects.filter(task=task)
    a_choices_dict = {a_choice.id: a_choice.name for a_choice in a_choices}
    b_choices_dict = {b_choice.id: b_choice.name for b_choice in b_choices}
    
    task_vars = TaskVarValue.objects.filter(task=task)
    inputs = {var.var.name: var.value for var in task_vars}  # var.nameをキーにしてinputsを作成
    outputs = {key: 0 for key in inputs}
    # 初回アクセス時の回答がセッションに保存されているか確認
    bemodel_answers = None
    error_flag = False
    error_message = ""
    if request.method == 'POST':
        storage = get_messages(request)
        storage.used = True 
        # ユーザーの回答を取得し、タプルとしてまとめる
        user_answers = request.POST.getlist('bemodel_answers[]')  # ユーザーの回答（リスト）
        user_answer_tuples = [(int(user_answers[i]), int(user_answers[i+1]), int(user_answers[i+2])) 
                      for i in range(0, len(user_answers), 3)]
               # a_choices と b_choices を辞書に変換し、id → name にアクセスできるようにする
        a_choices_dict = {a_choice.id: a_choice.name for a_choice in a_choices}
        b_choices_dict = {b_choice.id: b_choice.name for b_choice in b_choices}

        # ユーザーの回答（id）からnameに変換
        bemodel_answers = []
        for i in range(0, len(user_answers), 3):
            var1_id = int(user_answers[i])      # 最初の変数 (例: "min" の id)
            var2_id = int(user_answers[i+1])       # 関係 (例: "と等しい")
            relation_id = int(user_answers[i+2])    # 比較対象 (例: "a" の id)

            # idからnameに変換
            var1_name = a_choices_dict.get(var1_id, None)  # a_choices から変数名を取得
            var2_name = a_choices_dict.get(var2_id, None)  # b_choices から変数名を取得
            relation = b_choices_dict.get(relation_id, None)  # b_choices から変数名を取得
             # サブ関数の変数チェック
            if var1_name not in inputs or var2_name not in inputs:
                error_flag = True
                error_message = "選択された変数が許可されていません。"
                break
            # タプルに変換
            bemodel_answers.append((var1_name, var2_name ,relation))
        if error_flag:
            messages.error(request, error_message)
            return redirect(request.path)  # 現在のページを再読み込み
        # 計算を実行
        outputs = calculate_outputs(bemodel_answers, inputs)
        # 正解の回答を取得し、タプルとしてまとめる
        correct_answers = task_Answer_bemodel.objects.filter(task=task).values_list('behavior_model_a_1', 'behavior_model_a_2','behavior_model_b')
        correct_answer_tuples = [tuple(correct_answer) for correct_answer in correct_answers]

        if set(user_answer_tuples) == set(correct_answer_tuples):
            return redirect(reverse('tasks:finalquiz', args=[task_id]))  # 次のクイズに進む

        else:
            # 不正解の場合のフィードバック
            extra = set(user_answer_tuples) - set(correct_answer_tuples)
            missing = set(correct_answer_tuples) - set(user_answer_tuples)
            if extra or missing:
                feedback = []
                if extra:
                    feedback.append(f"余分な振る舞いモデルがあります")
                if missing:
                    feedback.append(f"足りない振る舞いモデルがあります")
                messages.error(request, "不正解です。" + " ".join(feedback))
            else:
                messages.error(request, "不正解です。もう一度試してください。")
    context = {
        'task': task,
        'a_choices': a_choices,
        'b_choices': b_choices,
        'inputs': inputs,   # SubFunctionVarValueから取得した入力値
        'outputs': outputs, # 計算された出力
        'bemodel_answers': bemodel_answers,
    }
    return render(request, 'tasks/finalbe.html', context)

def finalquiz(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # クイズのカードデータを取得
    cards = list(Card.objects.filter(task=task))  # カードを取得
    random.shuffle(cards)
    # 正解のデータ（解答順）を取得
    correct_answer = task_Answer_code.objects.get(task=task)
    correct_answer_list = correct_answer.get_correct_answer_list()
    bemodel = task_Answer_bemodel.objects.filter(task=task).select_related('behavior_model_a_1', 'behavior_model_a_2', 'behavior_model_b')
    bemodel_list =[]
    for item in bemodel:
        # 各フィールドの値をリストに格納
        bemodel_list.append([item.behavior_model_a_1.name, item.behavior_model_a_2.name, item.behavior_model_b.name])    
    # フォームが送信されると次のページに遷移
    if request.method == "POST":
        return redirect('tasks:home')

    context = {
        'task': task,
        'cards': cards,
        'correct_answer_list': correct_answer_list, 
        'bemodel_list': bemodel_list,   
        }
    return render(request, 'tasks/finalquiz.html', context)

def calculate_outputs(bemodel_answers, inputs):
    outputs = {key: 0 for key in inputs} # 初期の入力値をコピー  # 初期値は全て0に設定
    for i in range(len(bemodel_answers)):  # len(bemodel_answers)回処理
        var1, var2, relation = bemodel_answers[i]

        if relation == "と等しい":
            outputs[var1] = inputs[var2]
        elif relation == "より大きい":
            outputs[var1] = max(outputs[var1], outputs[var2])
        elif relation == "より小さい":
            outputs[var1] = min(outputs[var1], outputs[var2])

    return outputs

def pre_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_name = request.session.get('user_name', '匿名ユーザー')
    next_test = Test.objects.filter(id__gt=test_id).order_by('id').first()
    # クイズのカードデータを取得
    cards = list(TestCard.objects.filter(test=test))  # カードを取得
    random.shuffle(cards)
    # フォームが送信されると次のページに遷移
    if request.method == "POST":
        print("送信されたデータ:", request.POST)
        answers = request.POST.get('answers', '')
        print("回答内容:", answers)
        PreTestAnswer.objects.create(
            user_name=user_name,  # セッションから取得
            test=test,
            answers=answers
        )
        if next_test:  # 次のテストがある場合はそのテストへ遷移
            return redirect('tasks:pre_test', test_id=next_test.id)
        else:  # 次のテストがない場合はホームページへ遷移
            return redirect('tasks:home')

    context = {
        'test': test,
        'cards': cards,
        }
    return render(request, 'tasks/pre_test.html', context)

def final_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_name = request.session.get('user_name', '匿名ユーザー')
    next_test = Test.objects.filter(id__gt=test_id).order_by('id').first()
    # クイズのカードデータを取得
    cards = list(TestCard.objects.filter(test=test))  # カードを取得
    random.shuffle(cards)
    # フォームが送信されると次のページに遷移
    if request.method == "POST":
        print("送信されたデータ:", request.POST)
        answers = request.POST.get('answers', '')
        print("回答内容:", answers)
        ProTestAnswer.objects.create(
            user_name=user_name,  # セッションから取得
            test=test,
            answers=answers
        )
        if next_test:  # 次のテストがある場合はそのテストへ遷移
            return redirect('tasks:final_test', test_id=next_test.id)
        else:  # 次のテストがない場合はホームページへ遷移
            return redirect('tasks:home')

    context = {
        'test': test,
        'cards': cards,
        }
    return render(request, 'tasks/final_test.html', context)

def pre_name(request):
    request.session.clear()
    first_test = Test.objects.order_by('id').first()

    if request.method == "POST":
        name = request.POST.get('name')
        request.session['user_name'] = name  # セッションに名前を保存
        return redirect('tasks:pre_test', test_id=first_test.id)  # 最初のテストへリダイレクト
    return render(request, 'tasks/pre_name.html')

def final_name(request):
    request.session.clear()
    first_test = Test.objects.order_by('id').first()

    if request.method == "POST":
        name = request.POST.get('name')
        request.session['user_name'] = name  # セッションに名前を保存
        return redirect('tasks:final_test', test_id=first_test.id) # 最初のテストへリダイレクト
    return render(request, 'tasks/final_name.html')

def learning_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # クイズのカードデータを取得
    cards = list(Card.objects.filter(task=task))  # カードを取得
    random.shuffle(cards)
    # 正解のデータ（解答順）を取得
    correct_answer = task_Answer_code.objects.get(task=task)
    correct_answer_list = correct_answer.get_correct_answer_list()
    # フォームが送信されると次のページに遷移
    if request.method == "POST":
        return redirect('tasks:home')

    context = {
        'task': task,
        'cards': cards,
        'correct_answer_list': correct_answer_list, 
        }
    return render(request, 'tasks/learning.html', context)