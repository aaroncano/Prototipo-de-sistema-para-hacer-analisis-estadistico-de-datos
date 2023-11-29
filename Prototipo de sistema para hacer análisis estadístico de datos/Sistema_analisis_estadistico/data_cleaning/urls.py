from . import views
from django.urls import path


app_name = 'data_cleaning'

urlpatterns = [
    path('opciones_limpieza_hub/<str:file_name>/', views.opciones_limpieza_hub, name='opciones_limpieza'),
    path('eliminar_columnas/<str:file_name>/', views.eliminar_columnas, name='eliminar_columnas'),
    path('normalizar_texto/<str:file_name>', views.normalizar_texto, name='normalizar_texto'),
    path('manejar_valores_vacios/<str:file_name>', views.manejar_valores_vacios, name='manejar_valores_vacios')
]