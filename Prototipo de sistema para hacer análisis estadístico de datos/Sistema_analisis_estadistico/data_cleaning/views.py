import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os

import pandas as pd

from . import utils

# Create your views here.
def opciones_limpieza_hub(request, file_name):
    df, error_response, file_path = utils.leer_csv_o_error(request, file_name)
    if error_response:
        return error_response
    df_html = utils.crear_inicio_tabla(df)
    info = request.session.get('info', None) # Obtiene el mensaje de éxito o error
    request.session['info'] = None  # Borra el mensaje de la sesión

    return render(request, 'data_cleaning/opciones_limpieza.html', {
        'file_name': file_name,
        'dataframe': df_html,
        'info': info
    })


def eliminar_columnas(request, file_name):
    df, error_response, file_path = utils.leer_csv_o_error(request, file_name)
    if error_response:
        return error_response # Si hay un error, regresa la respuesta de error
    df_html = utils.crear_inicio_tabla(df)
    columnas = df.columns.tolist()

    if request.method == 'POST':
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular') 
        df_procesado, resultado = utils.eliminar_columnas(df, columnas_a_manipular) 
        utils.guardar_resultado_en_sesion(request, resultado) 
        utils.guardar_csv(df_procesado, file_path) 
        
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)

    return render(request, 'data_cleaning/limpieza_columnas.html', {
        'file_name': file_name,
        'columnas': columnas, 
        'dataframe': df_html
    })


def normalizar_texto(request, file_name):
    df, error_response, file_path = utils.leer_csv_o_error(request, file_name)
    if error_response:
        return error_response
    df_html = utils.crear_inicio_tabla(df)
    columnas = df.select_dtypes(include=['object']).columns.tolist()

    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular') 
        df_procesado, resultado = utils.normalizar_texto(df, alcance, columnas_a_manipular)

        utils.guardar_resultado_en_sesion(request, resultado)
        utils.guardar_csv(df_procesado, file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)

    return render(request, 'data_cleaning/normalizar_texto.html', {
        'file_name': file_name,
        'columnas': columnas, 
        'dataframe': df_html
    })

def manejar_valores_vacios(request, file_name):
    df, error_response, file_path = utils.leer_csv_o_error(request, file_name)
    if error_response:
        return error_response # Si hay un error, regresa la respuesta de error
    df_html = utils.crear_inicio_tabla(df)
    columnas = df.columns.tolist()

    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        accion = request.POST.get('accion', '')
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')  
        df_procesado, resultado = utils.manejar_valores_vacios(df, alcance, columnas_a_manipular, accion)

        utils.guardar_resultado_en_sesion(request, resultado)
        utils.guardar_csv(df_procesado, file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name)

    return render(request, 'data_cleaning/manejar_valores_vacios.html', {
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })

def procesar_outliers(request, file_name):
    df, error_response, file_path = utils.leer_csv_o_error(request, file_name)
    if error_response:
        return error_response
    df_html = utils.crear_inicio_tabla(df)
    columnas = df.select_dtypes(include=['number']).columns.tolist()  # Solo columnas numéricas


    if request.method == 'POST':
        accion = request.POST.get('accion', '')
        umbral_iqr = float(request.POST.get('umbral_iqr', 1.5))
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')
        df_procesado, resultado = utils.procesar_outliers_iqr(df, columnas_a_manipular=columnas_a_manipular, umbral_iqr=umbral_iqr, accion=accion)

        utils.guardar_resultado_en_sesion(request, resultado)
        utils.guardar_csv(df_procesado, file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name) 

    return render(request, 'data_cleaning/procesar_outliers.html', {
        'file_name': file_name,
        'columnas': columnas, 
        'dataframe': df_html
    })

def filtrar_datos(request, file_name):
    df, error_response, file_path = utils.leer_csv_o_error(request, file_name)
    if error_response:
        return error_response
    df_html = utils.crear_inicio_tabla(df)
    columnas = df.select_dtypes(include=['number']).columns.tolist()  # Solo columnas numéricas

    if request.method == 'POST':
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')
        condicion_str = request.POST.get('condicion', '')
        df_procesado, resultado = utils.filtrar_filas_por_condicion(df, columnas_a_manipular, condicion_str)

        utils.guardar_resultado_en_sesion(request, resultado)
        utils.guardar_csv(df_procesado, file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=file_name) 

    return render(request, 'data_cleaning/filtrar_datos.html', { 
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })