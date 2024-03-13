from . import views
from django.urls import path

app_name = 'report'

urlpatterns = [
    path('reporte_regresion_linear/<str:file_name>', views.reporte_regresion_linear, name='reporte_regresion_linear'),
    path('reporte_regresion_logistica/<str:file_name>', views.reporte_regresion_logistica, name='reporte_regresion_logistica'),  
    path('reporte_estadistica_descriptiva/<str:file_name>', views.reporte_estadistica_descriptiva, name='reporte_estadistica_descriptiva'),  
]
