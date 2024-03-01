from django.shortcuts import render
from http.client import HTTPResponse
from django.shortcuts import redirect, render
from data_cleaning.utils import cleaning_utils
from data_cleaning.utils.views_utils import guardar_resultado_en_sesion, preparar_datos_para_get
from utils.csv_utils import gestionar_version_archivo, leer_csv_o_error, guardar_csv
from utils.tablas_utils import crear_inicio_tabla


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

