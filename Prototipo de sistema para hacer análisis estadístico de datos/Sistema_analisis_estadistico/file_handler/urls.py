from django.urls import path
from . import views

app_name = 'file_handler'

urlpatterns = [
    path('', views.cargar_archivo, name='cargar_archivo'),
    path('revisar_csv/<str:file_name>/', views.revisar_csv, name='revisar_csv'),
]
