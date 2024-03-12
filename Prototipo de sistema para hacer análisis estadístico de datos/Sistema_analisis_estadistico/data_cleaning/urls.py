from . import views
from django.urls import path


app_name = 'data_cleaning'

urlpatterns = [
    path('opciones_limpieza_hub/<str:file_name>/', views.opciones_limpieza_hub, name='opciones_limpieza'),
    path('eliminar_columnas/<str:file_name>/', views.eliminar_columnas, name='eliminar_columnas'),
    path('normalizar_texto/<str:file_name>', views.normalizar_texto, name='normalizar_texto'),
    path('manejar_valores_vacios/<str:file_name>', views.manejar_valores_vacios, name='manejar_valores_vacios'),
    path('procesar_outliers/<str:file_name>', views.procesar_outliers, name='procesar_outliers'),
    path('filtrar:datos/<str:file_name>', views.filtrar_datos, name='filtrar_datos'),
]