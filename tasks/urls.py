from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('task/<int:task_id>/organize/', views.organize, name='organize'),
    path('task/<int:task_id>/bemodel/', views.bemodel, name='bemodel'),
    path('task/<int:task_id>/bemodel/next/', views.next_bemodel, name='next_bemodel'),
    path('task/<int:task_id>/quiz', views.quiz, name='quiz'),
]
