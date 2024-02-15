from django.urls import path
from . import views

app_name = 'file_handler'

urlpatterns = [
    path('prueba-base/', views.prueba_base, name='prueba_base'),
    path('', views.cargar_archivo, name='cargar_archivo'),
    path('revisar_csv/<str:file_name>/', views.revisar_csv, name='revisar_csv'),
    path('cargar_mas_filas/<str:file_name>/', views.cargar_mas_filas, name='cargar_mas_filas'),
    path('cambiar_version/', views.cambiar_version, name='cambiar_version'),
]
