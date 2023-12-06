from django.shortcuts import redirect, render
from .utils.cleaning_utils import eliminar_columnas, normalizar_texto, manejar_valores_vacios, procesar_outliers_iqr, filtrar_filas_por_condicion
from .utils.views_utils import guardar_resultado_en_sesion, preparar_datos_para_get
from utils.csv_utils import gestionar_version_archivo, leer_csv_o_error, guardar_csv
from utils.tablas_utils import crear_inicio_tabla

# Create your views here.
def opciones_limpieza_hub(request, file_name):
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response
    
    df_html = crear_inicio_tabla(df)
    info = request.session.get('info', None) # Obtiene el mensaje de éxito o error
    request.session['info'] = None  # Borra el mensaje de la sesión

    return render(request, 'data_cleaning/opciones_limpieza.html', {
        'file_name': file_name,
        'dataframe': df_html,
        'info': info
    })


def eliminar_columnas(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response

    # Manejo de POST
    if request.method == 'POST':
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')
        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        
        df_procesado, resultado = eliminar_columnas(df, columnas_a_manipular)
        
        guardar_resultado_en_sesion(request, resultado)
        guardar_csv(df_procesado, new_file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=new_file_name)

    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df)

    return render(request, 'data_cleaning/limpieza_columnas.html', {
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })


def normalizar_texto(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response

    # Manejo de POST
    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')

        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        df_procesado, resultado = normalizar_texto(df, alcance, columnas_a_manipular)

        guardar_resultado_en_sesion(request, resultado)
        guardar_csv(df_procesado, new_file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=new_file_name)

    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df, include_dtypes=['object'])

    return render(request, 'data_cleaning/normalizar_texto.html', {
        'file_name': file_name,
        'columnas': columnas, 
        'dataframe': df_html
    })

def manejar_valores_vacios(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response

    # Manejo de POST
    if request.method == 'POST':
        alcance = request.POST.get('alcance', '')
        accion = request.POST.get('accion', '')
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')

        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        df_procesado, resultado = manejar_valores_vacios(df, alcance, columnas_a_manipular, accion)

        guardar_resultado_en_sesion(request, resultado)
        guardar_csv(df_procesado, new_file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=new_file_name)

    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df)

    return render(request, 'data_cleaning/manejar_valores_vacios.html', {
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })

def procesar_outliers(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response

    # Manejo de POST
    if request.method == 'POST':
        accion = request.POST.get('accion', '')
        umbral_iqr = float(request.POST.get('umbral_iqr', 1.5))
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')

        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        df_procesado, resultado = procesar_outliers_iqr(df, columnas_a_manipular=columnas_a_manipular, umbral_iqr=umbral_iqr, accion=accion)

        guardar_resultado_en_sesion(request, resultado)
        guardar_csv(df_procesado, new_file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=new_file_name)

    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df, include_dtypes=['object'])

    return render(request, 'data_cleaning/procesar_outliers.html', {
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })

def filtrar_datos(request, file_name):
    # Manejo de error y carga de DataFrame
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response

    # Manejo de POST
    if request.method == 'POST':
        columnas_a_manipular = request.POST.getlist('columnas_a_manipular')
        condicion_str = request.POST.get('condicion', '')

        new_file_name, new_file_path = gestionar_version_archivo(request, file_name)
        df_procesado, resultado = filtrar_filas_por_condicion(df, columnas_a_manipular, condicion_str)

        guardar_resultado_en_sesion(request, resultado)
        guardar_csv(df_procesado, new_file_path)
        return redirect('data_cleaning:opciones_limpieza', file_name=new_file_name)

    # Preparación para el método GET
    df_html, columnas = preparar_datos_para_get(df, include_dtypes=['object'])

    return render(request, 'data_cleaning/filtrar_datos.html', { 
        'file_name': file_name,
        'columnas': columnas,
        'dataframe': df_html
    })