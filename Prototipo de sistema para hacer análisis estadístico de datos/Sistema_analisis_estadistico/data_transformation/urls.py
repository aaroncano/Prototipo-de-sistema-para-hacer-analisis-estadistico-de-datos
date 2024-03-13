from . import views
from django.urls import path


app_name = 'data_transformation'

urlpatterns = [
    path('transformation/<str:file_name>', views.transformation, name='transformation'),
    path('standardization/<str:file_name>', views.standardization, name='standardization')
]