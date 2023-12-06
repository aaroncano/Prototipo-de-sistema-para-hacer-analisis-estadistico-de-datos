from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CargaCSVForm
from utils.tablas_utils import crear_inicio_tabla
from utils.csv_utils import leer_csv_o_error, handle_uploaded_file

def cargar_archivo(request):
    mensaje_error = request.session.get('csv_vacio_mensaje', None)
    request.session['csv_vacio_mensaje'] = None

    if request.method == 'POST':
        form = CargaCSVForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_csv = request.FILES['archivo_csv']
            unique_file_name = handle_uploaded_file(archivo_csv)
            return redirect('file_handler:revisar_csv', file_name=unique_file_name)
    else:
        form = CargaCSVForm()
    return render(request, 'file_handler/cargar_archivo.html', {
        'form': form,
        'mensaje_error': mensaje_error
    })

def revisar_csv(request, file_name):
    df, error_response, file_path = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response

    return render(request, 'file_handler/revisar_csv.html', {
        'dataframe': crear_inicio_tabla(df),
        'file_name': file_name
    })

def cargar_mas_filas(request, file_name):
    df, error_response, _ = leer_csv_o_error(request, file_name)
    if error_response:
        return error_response

    start_row = int(request.GET.get('start', 0))
    df_partial = df.iloc[start_row:start_row + 20]
    df_html = df_partial.to_html(classes='table table-striped', index=True, header=False)
    return JsonResponse({'data': df_html})