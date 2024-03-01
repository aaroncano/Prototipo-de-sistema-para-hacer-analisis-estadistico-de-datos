from django.urls import path
from . import views

app_name = 'file_handler'

urlpatterns = [
    path('', views.cargar_archivo, name='cargar_archivo'),
    path('revisar_csv/<str:file_name>/', views.revisar_csv, name='revisar_csv'),
    path('cargar_mas_filas/<str:file_name>/', views.cargar_mas_filas, name='cargar_mas_filas'),
    path('cambiar_version/', views.cambiar_version, name='cambiar_version'),
      path('descargar_csv/<str:file_name>/', views.descargar_archivo_csv, name='descargar_csv'),# 
    # Otros patrones de URL
]

