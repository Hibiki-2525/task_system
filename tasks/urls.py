from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('task/<int:task_id>/organize/', views.organize, name='organize'),
    path('task/<int:task_id>/bemodel/', views.bemodel, name='bemodel'),
    path('task/<int:task_id>/next_bemodel', views.next_bemodel, name='next_bemodel'),
    path('task/<int:task_id>/quiz', views.quiz, name='quiz'),
    path('task/<int:task_id>/finalbe/', views.finalbe, name='finalbe'),
    path('task/<int:task_id>/finalquiz', views.finalquiz, name='finalquiz'),
]
