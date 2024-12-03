from django.contrib import admin
from .models import Task, SubFunction, Answer_bemodel, Answer_code, BehaviorModel_A, BehaviorModel_B, Card

class CardInline(admin.TabularInline):  # or admin.StackedInline
    model = Card
    extra = 1  # 新規作成フォームをいくつ表示するか（1つでよい場合）


class BemodelInline(admin.TabularInline):
    model = Answer_bemodel  # Answerモデルをインラインで表示
    extra = 1  # デフォルトで1つのAnswerを表示

class CodeInline(admin.TabularInline):
    model = Answer_code  # Answerモデルをインラインで表示
    extra = 1  # デフォルトで1つのAnswerを表示

class SubFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'parent')  # SubFunctionの表示項目
    inlines = [BemodelInline, CodeInline]   # SubFunctionの編集画面でAnswerをインライン表示

# SubFunctionをTaskのインラインで表示する
class SubFunctionInline(admin.TabularInline):
    model = SubFunction
    extra = 1  # 新しいSubFunctionが1つ追加されるように

# Taskの編集画面にSubFunctionをインライン表示する
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Taskのリスト表示項目
    inlines = [SubFunctionInline,CardInline]  # SubFunctionをインライン表示

admin.site.register(Task, TaskAdmin)
admin.site.register(SubFunction, SubFunctionAdmin)
admin.site.register(Answer_bemodel)
admin.site.register(Answer_code)
admin.site.register(Card)
admin.site.register(BehaviorModel_A)
admin.site.register(BehaviorModel_B)
