import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
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
    
    df = pd.read_csv(file_path)

    df_html = df.head(20).to_html(classes='table table-striped', index=True)
    
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

    df = pd.read_csv(file_path)
    df_html = df.head(20).to_html(classes='table table-striped', index=True)
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

    df = pd.read_csv(file_path)
    columnas = df.columns.tolist()

    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        
        if alcance == 'columna_especifica':
            columnas_a_normalizar = request.POST.getlist('columnas_a_normalizar')  # Recibir una lista de columnas
            for columna in columnas_a_normalizar:
                df, resultado = utils.normalizar_texto(df, 'columna_especifica', columna)
        else:
            df, resultado = utils.normalizar_texto(df, alcance)

        info_text = "\n".join(f"{key}: {', '.join(value) if isinstance(value, list) else value}" 
                              for key, value in resultado.items() if value)
        request.session['info'] = info_text  # Guardar el texto en la sesión

        df.to_csv(file_path, index=False)  # Guarda los cambios en el archivo
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)

    df_html = df.head(20).to_html(classes='table table-striped', index=True)
    return render(request, 'data_cleaning/normalizar_texto.html', {
        'file_name': file_name,
        'columnas': columnas,  # Pasar la lista de columnas al template
        'dataframe': df_html
    })

def manejar_valores_vacios(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        return HttpResponse("Archivo no encontrado.", status=404)

    df = pd.read_csv(file_path)
    columnas = df.columns.tolist()  # Obtener las columnas para mostrar los checkboxes

    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        accion = request.POST.get('accion', '')

        if alcance == 'columna_especifica':
            # Obtiene la lista de columnas seleccionadas cuando el alcance es 'columna_especifica'
            columnas_a_manipular = request.POST.getlist('columnas_a_manipular')
            for col in columnas_a_manipular:
                df, resultado = utils.manejar_valores_vacios(df, 'columna_especifica', col, accion)
        else:
            df, resultado = utils.manejar_valores_vacios(df, alcance, None, accion)

        info_text = "\n".join(f"{key}: {', '.join(value) if isinstance(value, list) else value}" 
                              for key, value in resultado.items() if value)
        request.session['info'] = info_text  # Guardar el texto en la sesión

        df.to_csv(file_path)  # Guarda los cambios en el archivo
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)

    df_html = df.head(20).to_html(classes='table table-striped', index=True)
    return render(request, 'data_cleaning/manejar_valores_vacios.html', {
        'file_name': file_name,
        'columnas': columnas,  # Pasar la lista de columnas al template
        'dataframe': df_html
    })

def procesar_outliers(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        return HttpResponse("Archivo no encontrado.", status=404)

    df = pd.read_csv(file_path)
    columnas = df.columns.tolist()  # Obtener las columnas para mostrar en los checkboxes

    if request.method == 'POST':
        accion = request.POST.get('accion', '')
        umbral_iqr = float(request.POST.get('umbral_iqr', 1.5))
        columnas_a_procesar = request.POST.getlist('columnas_a_procesar')

        df_procesado, resultado = utils.procesar_outliers_iqr(df, columnas=columnas_a_procesar, 
                                                              umbral_iqr=umbral_iqr, accion=accion)

        info_text = "\n".join(f"{key}: {', '.join(map(str, value)) if isinstance(value, list) else value}" 
                              for key, value in resultado.items() if value)
        request.session['info'] = info_text  # Guardar el texto en la sesión

        df_procesado.to_csv(file_path)  # Guarda los cambios en el archivo
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)  # Reemplaza 'ruta_a_tu_vista' con la ruta de tu vista

    df_html = df.head(20).to_html(classes='table table-striped', index=True)
    return render(request, 'data_cleaning/procesar_outliers.html', {  # Reemplaza 'ruta_a_tu_template.html' con la ruta de tu template
        'file_name': file_name,
        'columnas': columnas,  # Pasar la lista de columnas al template
        'dataframe': df_html
    })

def filtrar_datos(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        return HttpResponse("Archivo no encontrado.", status=404)

    df = pd.read_csv(file_path)
    columnas = df.select_dtypes(include=['number']).columns.tolist()  # Solo columnas numéricas

    if request.method == 'POST':
        columnas_a_filtrar = request.POST.getlist('columnas_a_filtrar')
        condicion_str = request.POST.get('condicion', '')

        # Convertir la cadena de la condición en una función lambda, manejando errores
        try:
            condicion = eval("lambda x: " + condicion_str)
        except Exception as e:
            return HttpResponse(f"Error en la condición proporcionada: {str(e)}", status=400)

        df_filtrado, resultado = utils.filtrar_filas_por_condicion(df, columnas_a_filtrar, condicion)

        info_text = "\n".join(f"{key}: {value}" for key, value in resultado.items() if value)
        request.session['info'] = info_text  # Guardar el texto en la sesión

        df_filtrado.to_csv(file_path)  # Guarda los cambios en el archivo
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)  # Cambia 'nombre_de_tu_vista' por el nombre de tu vista

    df_html = df.head(20).to_html(classes='table table-striped', index=True)
    return render(request, 'data_cleaning/filtrar_datos.html', {  # Cambia 'ruta_a_tu_template.html' por la ruta de tu template
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })