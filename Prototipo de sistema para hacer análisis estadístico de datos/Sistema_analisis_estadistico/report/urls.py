from . import views
from django.urls import path

app_name = 'report'

urlpatterns = [
    path('exportar_reporte/', views.exportar_reporte, name='exportar_reporte'),

    path('reporte_regresion_linear/<str:file_name>', views.reporte_regresion_linear, name='reporte_regresion_linear'),
    path('reporte_regresion_logistica/<str:file_name>', views.reporte_regresion_logistica, name='reporte_regresion_logistica'),  
    path('reporte_estadistica_descriptiva/<str:file_name>', views.reporte_estadistica_descriptiva, name='reporte_estadistica_descriptiva'),
    path('reporte_correlacion_pearson/<str:file_name>', views.reporte_correlacion_pearson, name='reporte_correlacion_pearson'),
    path('reporte_correlacion_spearman/<str:file_name>', views.reporte_correlacion_spearman, name='reporte_correlacion_spearman'),  

]
