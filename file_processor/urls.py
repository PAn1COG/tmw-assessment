from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('status/', views.file_status, name='file_status'),
    path('all_tasks/', views.all_tasks, name='all_tasks'),
    path('renderAll_tasks/', views.renderAll_tasks, name='all_tasks'),
    path('renderStatus/', views.status, name='file_status'),
    path('delete_all_tasks/', views.delete_all_tasks, name='delete_all_tasks'),
]
