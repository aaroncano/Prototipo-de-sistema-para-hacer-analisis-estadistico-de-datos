from . import views
from django.urls import path

app_name = 'data_analysis'

urlpatterns = [
   path('estadistica_descriptiva/<str:file_name>', views.estadistica_descriptiva, name='estadistica_descriptiva'),
   path('regresion_lineal/<str:file_name>', views.regresion_lineal, name='regresion_lineal'),
   path('regresion_logistica/<str:file_name>', views.regresion_logistica, name='regresion_logistica'),
   path('correlacion_pearson/<str:file_name>', views.correlacion_pearson, name='correlacion_pearson'),
   path('correlacion_spearman/<str:file_name>', views.correlacion_spearman, name='correlacion_spearman'),


]
