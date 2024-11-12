from django.contrib import admin
from .models import Task, SubFunction

# Taskモデルを管理サイトに登録
admin.site.register(Task)
admin.site.register(SubFunction)