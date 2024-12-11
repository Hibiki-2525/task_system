from django.contrib import admin
from .models import Task, SubFunction, Answer_bemodel, Answer_code, BehaviorModel_A, BehaviorModel_B, Card, SubFunctionVarValue, task_Answer_bemodel, task_Answer_code, TaskVarValue

class CardInline(admin.TabularInline):  # or admin.StackedInline
    model = Card
    extra = 1  # 新規作成フォームをいくつ表示するか（1つでよい場合）

class VarValueInline(admin.TabularInline):  # or admin.StackedInline
    model = SubFunctionVarValue
    extra = 1  # 新規作成フォームをいくつ表示するか（1つでよい場合）


class BemodelInline(admin.TabularInline):
    model = Answer_bemodel  # Answerモデルをインラインで表示
    extra = 1  # デフォルトで1つのAnswerを表示

class CodeInline(admin.TabularInline):
    model = Answer_code  # Answerモデルをインラインで表示
    extra = 1  # デフォルトで1つのAnswerを表示

class SubFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'parent')  # SubFunctionの表示項目
    inlines = [BemodelInline, VarValueInline, CodeInline]   # SubFunctionの編集画面でAnswerをインライン表示

# SubFunctionをTaskのインラインで表示する
class SubFunctionInline(admin.TabularInline):
    model = SubFunction
    extra = 1  # 新しいSubFunctionが1つ追加されるように

class TaskVarValueInline(admin.TabularInline):  # or admin.StackedInline
    model = TaskVarValue
    extra = 1  # 新規作成フォームをいくつ表示するか（1つでよい場合）


class TaskBemodelInline(admin.TabularInline):
    model = task_Answer_bemodel  # Answerモデルをインラインで表示
    extra = 1  # デフォルトで1つのAnswerを表示

class TaskCodeInline(admin.TabularInline):
    model = task_Answer_code  # Answerモデルをインラインで表示
    extra = 1  # デフォルトで1つのAnswerを表示

# Taskの編集画面にSubFunctionをインライン表示する
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Taskのリスト表示項目
    inlines = [SubFunctionInline,CardInline,TaskVarValueInline,TaskBemodelInline,TaskCodeInline]  # SubFunctionをインライン表示

admin.site.register(Task, TaskAdmin)
admin.site.register(SubFunction, SubFunctionAdmin)
admin.site.register(Answer_bemodel)
admin.site.register(Answer_code)
admin.site.register(Card)
admin.site.register(BehaviorModel_A)
admin.site.register(BehaviorModel_B)
admin.site.register(SubFunctionVarValue)
admin.site.register(task_Answer_bemodel)
admin.site.register(task_Answer_code)
admin.site.register(TaskVarValue)
