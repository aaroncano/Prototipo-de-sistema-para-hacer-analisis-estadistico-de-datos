from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import os

import pandas as pd
from .forms import CargaCSVForm

def cargar_archivo(request):
    if request.method == 'POST':
        form = CargaCSVForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_csv = request.FILES['archivo_csv']
            #se guarda el file_path por si se necesita usar después
            file_path = handle_uploaded_file(archivo_csv)
            
            return redirect('file_handler:revisar_csv', file_name=archivo_csv.name)
    else:
        form = CargaCSVForm()
    return render(request, 'file_handler/cargar_archivo.html', {'form': form})

def handle_uploaded_file(f):
    with open(os.path.join(settings.MEDIA_ROOT, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
    # Retornar la ruta del archivo para usarla después si es necesario
    return os.path.join(settings.MEDIA_ROOT, f.name)

def revisar_csv(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        # Lee las primeras 20 filas para mostrar una vista previa
        df = pd.read_csv(file_path, nrows=20)
        # Convertir el DataFrame a HTML manteniendo todas las columnas
        return render(request, 'file_handler/revisar_csv.html', {'dataframe': df.to_html(index=True, classes='table table-striped'), 'file_name': file_name})
    else:
        # Maneja el caso en que el archivo no exista
        return HttpResponse("Archivo no encontrado", status=404)