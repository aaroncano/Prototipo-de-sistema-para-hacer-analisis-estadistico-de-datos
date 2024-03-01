from . import views
from django.urls import path

app_name = 'data_analysis'

urlpatterns = [
   path('estadistica_descriptiva/<str:file_name>', views.estadistica_descriptiva, name='estadistica_descriptiva')
]
