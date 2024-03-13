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


def reporte_estadistica_descriptiva(request, file_name):
    # Asumiendo que los datos del reporte se almacenan en la sesión como JSON
    resultados_tendencia_central = request.session.get('resultados_tendencia_central', {})
    resultados_variabilidad = request.session.get('resultados_variabilidad', {})
    resultados_distribucion_frecuencias = request.session.get('resultados_distribucion_frecuencias', {})
    
    # Eliminar los datos del reporte de la sesión después de usarlos
    del request.session['resultados_tendencia_central']
    del request.session['resultados_variabilidad']
    del request.session['resultados_distribucion_frecuencias']
    
    # Verificar qué tipo de análisis se realizó y renderizar el template correspondiente
    if resultados_tendencia_central:
        return render(request, 'report/reporte_tendencia_central.html', {
            'file_name': file_name,
            'resultados_tendencia_central': resultados_tendencia_central
        })
    elif resultados_variabilidad:
        return render(request, 'report/reporte_variabilidad.html', {
            'file_name': file_name,
            'resultados_variabilidad': resultados_variabilidad
        })
    elif resultados_distribucion_frecuencias:
        return render(request, 'report/reporte_frecuencias.html', {
            'file_name': file_name,
            'resultados_distribucion_frecuencias': resultados_distribucion_frecuencias
        })
    else:
        # En caso de que no se haya realizado ningún análisis o haya ocurrido un error
        return render(request, 'report/error.html')

