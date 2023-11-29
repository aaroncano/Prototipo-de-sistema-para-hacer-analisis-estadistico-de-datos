import json
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
import os

import pandas as pd

from . import utils

# Create your views here.
def opciones_limpieza_hub(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    
    info = request.session.get('info', None) # Obtiene el mensaje de éxito o error
    request.session['info'] = None  # Borra el mensaje de la sesión

    if not os.path.exists(file_path):
        return HttpResponse("Archivo no encontrado.", status=404)
    
    df = pd.read_csv(file_path, nrows=20)  # Ajusta el número de filas según sea necesario
    df_html = df.to_html(classes='table table-striped', index=True)

    return render(request, 'data_cleaning/opciones_limpieza.html', {
        'file_name': file_name,
        'dataframe': df_html,
        'info': info
    })


def eliminar_columnas(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        return HttpResponse("Archivo no encontrado.", status=404)

    if request.method == 'POST':
        columnas_a_eliminar = request.POST.getlist('columnas_a_eliminar')  # Modificado para usar getlist

        df = pd.read_csv(file_path)
        df, resultado = utils.eliminar_columnas(df, columnas_a_eliminar)
        
        info_text = "\n".join(f"{key}: {', '.join(value) if isinstance(value, list) else value}" 
            for key, value in resultado.items() if value)
        request.session['info'] = info_text  # Guardar el texto en la sesión

        df.to_csv(file_path, index=False)  # Guarda los cambios en el archivo
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)

    # Leer las columnas para mostrarlas como checkboxes
    df = pd.read_csv(file_path, nrows=20)  # Modificado para leer solo las cabeceras
    df_html = df.to_html(classes='table table-striped', index=True)
    columnas = df.columns.tolist()
    return render(request, 'data_cleaning/limpieza_columnas.html', {
        'file_name': file_name,
        'columnas': columnas,  # Pasar la lista de columnas al template
        'dataframe': df_html
    })

def normalizar_texto(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        return HttpResponse("Archivo no encontrado.", status=404)

    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        columna_especifica = request.POST.get('columna_especifica', '') if alcance == 'columna_especifica' else None
        df = pd.read_csv(file_path)
        
        df, resultado = utils.normalizar_texto(df, alcance, columna_especifica)

        info_text = "\n".join(f"{key}: {', '.join(value) if isinstance(value, list) else value}" 
            for key, value in resultado.items() if value)
        request.session['info'] = info_text  # Guardar el texto en la sesión

        df.to_csv(file_path, index=False)  # Guarda los cambios en el archivo
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)
    
    df = pd.read_csv(file_path, nrows=20)
    df_html = df.to_html(classes='table table-striped', index=False)
    return render(request, 'data_cleaning/normalizar_texto.html', {
        'file_name': file_name,
        'dataframe': df_html
    })

def manejar_valores_vacios(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        return HttpResponse("Arcivo no encontrado.", status=404)
    
    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        columna_especifica = request.POST.get('columna_especifica', '') if alcance == 'columna_especifica' else None
        accion = request.POST.get('accion', '')
        df = pd.read_csv(file_path)

        df, resultado = utils.manejar_valores_vacios(df, alcance, columna_especifica, accion)

        info_text = "\n".join(f"{key}: {', '.join(value) if isinstance(value, list) else value}" 
            for key, value in resultado.items() if value)
        request.session['info'] = info_text  # Guardar el texto en la sesión

        df.to_csv(file_path, index=False)  # Guarda los cambios en el archivo
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)
    
    df = pd.read_csv(file_path, nrows=20)
    df_html = df.to_html(classes='table table-striped', index=False)
    return render(request, 'data_cleaning/manejar_valores_vacios.html', {
        'file_name': file_name,
        'dataframe': df_html
    })