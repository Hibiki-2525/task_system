from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('task/<int:task_id>/organize/', views.organize, name='organize'),
    path('task/<int:task_id>/bemodel/', views.bemodel, name='bemodel'),
]
