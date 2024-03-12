from . import views
from django.urls import path

app_name = 'data_analysis'

urlpatterns = [
   path('estadistica_descriptiva/<str:file_name>', views.estadistica_descriptiva, name='estadistica_descriptiva'),
   path('regresion_lineal/<str:file_name>', views.regresion_lineal, name='regresion_lineal'),
   path('regresion_logistica/<str:file_name>', views.regresion_logistica, name='regresion_logistica'),
]
