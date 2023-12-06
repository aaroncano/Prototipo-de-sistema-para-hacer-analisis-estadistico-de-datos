import os
import shutil
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
import pandas as pd

def handle_uploaded_file(f):
    unique_filename = str(uuid.uuid4()) + '.csv'
    file_path = os.path.join(settings.TEMP_FILES_DIR, unique_filename)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return unique_filename

def leer_csv_o_error(request, file_name):
    file_path = os.path.join(settings.TEMP_FILES_DIR, file_name)
    df, error = leer_y_verificar_csv(file_path)
    if error:
        manejar_error_csv(request, error, file_name)
        return None, error, None
    return df, None, file_path

def leer_y_verificar_csv(file_path):
    if not os.path.exists(file_path):
        return None, "Archivo no encontrado."
    try:
        df = pd.read_csv(file_path)
        if df.empty or df.columns.size == 0:
            # DataFrame está vacío
            return None, "CSV vacío"
    except pd.errors.EmptyDataError:
        # El archivo CSV está completamente vacío
        return None, "CSV vacío"
    except Exception as e:
        # Otros errores al leer el CSV
        return None, str(e)

    return df, None

def manejar_error_csv(request, error, file_name):
    if error == "CSV vacío":
        request.session['csv_vacio_mensaje'] = 'El archivo CSV está vacío. Por favor, carga un nuevo archivo.'
        return redirect('file_handler:cargar_archivo')
    else:
        return HttpResponse(error, status=404)

def guardar_csv(df, file_path):
    df.to_csv(file_path, index=False)





# VERSIONADO DE CSV
def gestionar_version_archivo(request, file_name):
    new_file_name = crear_copia_archivo(file_name)

    historial = request.session.get('file_versions', [])
    indice_actual = request.session.get('indice_version_actual', -1)

    # Elimina las versiones "futuras" si el usuario vuelve a una versión anterior 
    # y luego realiza un cambio
    historial = historial[:indice_actual + 1]

    historial.append(new_file_name)
    indice_actual = len(historial) - 1

    # Actualizar la sesión con la nueva versión del archivo
    request.session['file_versions'] = historial
    request.session['indice_version_actual'] = indice_actual
    request.session.modified = True

    # Devolver el nombre del nuevo archivo y su ruta
    new_file_path = os.path.join(settings.TEMP_FILES_DIR, new_file_name)
    return new_file_name, new_file_path


def crear_copia_archivo(file_name):
    original_file_path = os.path.join(settings.TEMP_FILES_DIR, file_name)
    new_file_name = str(uuid.uuid4()) + '.csv'
    new_file_path = os.path.join(settings.TEMP_FILES_DIR, new_file_name)
    shutil.copy2(original_file_path, new_file_path)
    return new_file_name


# funcionalidad para ir a versiones anteriores o siguientes
def ir_version_anterior(request):
    indice_actual = request.session.get('indice_version_actual', 0)
    if indice_actual > 0:
        indice_actual -= 1
        request.session['indice_version_actual'] = indice_actual
        request.session.modified = True
        return request.session['file_versions'][indice_actual]
    return None

def ir_version_siguiente(request):
    indice_actual = request.session.get('indice_version_actual', 0)
    historial = request.session.get('file_versions', [])
    if indice_actual < len(historial) - 1:
        indice_actual += 1
        request.session['indice_version_actual'] = indice_actual
        request.session.modified = True
        return request.session['file_versions'][indice_actual]
    return None