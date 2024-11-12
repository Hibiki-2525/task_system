from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]
