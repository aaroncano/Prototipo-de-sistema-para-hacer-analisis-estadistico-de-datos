from django.shortcuts import render
import json

def reporte_regresion_linear(request, file_name):
    # Asumiendo que los datos del reporte se almacenan en la sesión como JSON
    reporte_data_json = request.session.get('reporte_data', '{}')
    reporte_data = json.loads(reporte_data_json)
    
    # Eliminar los datos del reporte de la sesión después de usarlos
    del request.session['reporte_data']
    
    return render(request, 'report/reporte_regresion_linear.html', {
        'file_name': file_name,
        'reporte': reporte_data
    })

def reporte_regresion_logistica(request, file_name):
    # Asumiendo que los datos del reporte se almacenan en la sesión como JSON
    reporte_data_json = request.session.get('reporte_data', '{}')
    reporte_data = json.loads(reporte_data_json)
    
    # Eliminar los datos del reporte de la sesión después de usarlos
    del request.session['reporte_data']
    
    return render(request, 'report/reporte_regresion_logistica.html', {
        'file_name': file_name,
        'reporte': reporte_data
    })