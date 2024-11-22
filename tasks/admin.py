from django.contrib import admin
from .models import Task, SubFunction, BehaviorModel_A, BehaviorModel_B

# Taskモデルを管理サイトに登録
admin.site.register(Task)
admin.site.register(SubFunction)
admin.site.register(BehaviorModel_A)
admin.site.register(BehaviorModel_B)