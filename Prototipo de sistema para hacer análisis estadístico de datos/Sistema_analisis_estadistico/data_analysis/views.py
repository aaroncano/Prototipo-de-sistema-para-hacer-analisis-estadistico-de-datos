import json
from django.shortcuts import render
from http.client import HTTPResponse
from django.shortcuts import redirect, render
import pandas as pd
from data_cleaning.utils import cleaning_utils
from data_cleaning.utils.views_utils import guardar_resultado_en_sesion, preparar_datos_para_get
from utils.csv_utils import gestionar_version_archivo, leer_csv_o_error, guardar_csv
from utils.tablas_utils import crear_inicio_tabla

from .utils import inferencial_utils


def estadistica_descriptiva(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return redirect('file_handler:cargar_archivo')

    # Manejo de POST
    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')

        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        df_procesado, resultado = cleaning_utils.normalizar_texto(df, alcance, columnas_a_manipular)

        guardar_resultado_en_sesion(request, resultado)
        guardar_csv(df_procesado, new_file_path)
        return redirect('file_handler:revisar_csv', file_name=new_file_name)

    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df, include_dtypes=['object'])

    return render(request, 'data_analysis/estadistica_descriptiva.html', {
        'file_name': file_name,
        'columnas': columnas, 
        'dataframe': df_html
    })

def regresion_lineal(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return redirect('file_handler:cargar_archivo')
    
    # Manejo de POST
    if request.method == 'POST':
        variable_dependiente = request.POST.get('variable_dependiente')
        variables_independientes = request.POST.getlist('variables_independientes')
        
        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        df_procesado, reporte_data = inferencial_utils.regresion_linear(df, variable_dependiente, variables_independientes)
        
        request.session['reporte_data'] = json.dumps(reporte_data)

        #guardar_resultado_en_sesion(request, resultado)

        guardar_csv(df_procesado, new_file_path)
        return redirect('report:reporte_regresion_linear', file_name=new_file_name)
    
    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df, include_dtypes=['number'])
    
    return render(request, 'data_analysis/regresion_lineal.html', {
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })

def regresion_logistica(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return redirect('file_handler:cargar_archivo')
    
    columnas_binarias = []
    columnas_numericas = df.select_dtypes(include=['float64', 'int', 'bool']).columns.tolist()

    for columna in df.columns:
        # Obtener valores únicos de la columna excluyendo NaN
        valores_unicos = pd.unique(df[columna].dropna())

        # Convertir valores únicos a strings para verificar si son numéricos
        valores_unicos_str = valores_unicos.astype(str)
        
        # Verificar si la columna tiene exactamente dos valores únicos y si son numéricos
        if len(valores_unicos) == 2 and all(valor.isnumeric() or valor.replace('.','',1).isdigit() for valor in valores_unicos_str):
            # Adicionalmente, convertir a float y verificar si esos valores son 0 y 1 para una detección más estricta de binariedad
            valores_unicos_float = valores_unicos.astype(float)
            if set(valores_unicos_float) == {0.0, 1.0}:
                columnas_binarias.append(columna)

    # Manejo de POST
    if request.method == 'POST':
        variable_dependiente = request.POST.get('variable_dependiente')
        variables_independientes = request.POST.getlist('variables_independientes')
        # Obtener el umbral del formulario, con un valor por defecto de 0.5 si no se proporciona
        umbral = float(request.POST.get('umbral', 0.5))
        
        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        df_procesado, reporte_data = inferencial_utils.regresion_logistica(df, variable_dependiente, variables_independientes, umbral)
        
        request.session['reporte_data'] = json.dumps(reporte_data)

        guardar_csv(df_procesado, new_file_path)
        return redirect('report:reporte_regresion_logistica', file_name=new_file_name)
    
    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df, include_dtypes=['number'])
    
    return render(request, 'data_analysis/regresion_logistica.html', {
        'file_name': file_name,
        'columnas_numericas': columnas_numericas,
        'columnas_binarias': columnas_binarias,
        'dataframe': df.head(20).to_html(classes='table table-striped', index=True)
    })