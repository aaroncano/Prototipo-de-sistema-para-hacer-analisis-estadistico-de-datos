import pandas as pd
import numpy as np

def correlacion_pearson(df, variables):
    resultado = {
        'Errores': []
    }

    # Verificar que hayan dos o más variables para analizar
    if len(variables) < 2:
        resultado['Errores'].append("Se requieren al menos dos variables para analizar la correlación.")
        return df, None, resultado
    
    try:
        # Obtener las primeras 10 filas para las columnas especificadas
        primeras_filas = df[variables].head(10)

        # Calcular la matriz de correlación de Pearson
        matriz_correlacion = df[variables].corr(method='pearson')

        reporte_data = {
            "titulo": "Reporte - Análisis de Correlación de Pearson",
            "descripcion": "Análisis de correlación de Pearson para evaluar la relación lineal entre las variables seleccionadas.",
            "tipo_analisis": "correlacion_pearson",
            "resultados": {
                "nombres_columnas": variables, 
                "primeras_filas": primeras_filas.to_dict('records'),
                "matriz_correlacion": matriz_correlacion.to_dict(),
                "graficas": []
            }
        }

        if len(variables) == 2:
            # Preparación de datos para gráfico de dispersión
            datos_dispersion = [{
                'x': row[variables[0]],
                'y': row[variables[1]]
            } for index, row in df.iterrows()]
            
            reporte_data["resultados"]["graficas"].append({
                "tipo_grafico": "diagrama_dispersion",
                "titulo": f"Dispersión entre {variables[0]} y {variables[1]}",
                "datos": datos_dispersion,
                "etiquetas_x": variables[0],
                "etiquetas_y": variables[1]
            })
        else:
            # Preparar datos para la gráfica de burbuja
            datos_positivos = []
            datos_negativos = []
            max_correlation = matriz_correlacion.abs().max().max()
            for i, variable_i in enumerate(variables):
                for j, variable_j in enumerate(variables):
                    if i != j:
                        size = np.abs(matriz_correlacion.iloc[i, j]) / max_correlation * 100
                        if matriz_correlacion.iloc[i, j] < 0:
                            color = 'rgba(255, 0, 0, 0.5)'
                            datos_negativos.append({"x": j, "y": len(variables) - i - 1, "r": size, "backgroundColor": color})
                        else:
                            color = 'rgba(0, 0, 255, 0.5)'
                            datos_positivos.append({"x": j, "y": len(variables) - i - 1, "r": size, "backgroundColor": color})
            
            reporte_data["resultados"]["graficas"].append({
                "tipo_grafico": "grafica_burbuja",
                "titulo": "Correlación de Pearson",
                "datos_positivos": datos_positivos,
                "datos_negativos": datos_negativos,
                "etiquetas_x": variables,
                "etiquetas_y": list(reversed(variables))
            })

    except Exception as e:
        resultado['Errores'].append(str(e))
        reporte_data = None
    
    return df, reporte_data, resultado



def correlacion_spearman(df, variables):
    resultado = {
        'Errores': []
    }

    if len(variables) < 2:
        resultado['Errores'].append("Se requieren al menos dos variables para analizar la correlación.")
        return df, None, resultado
    
    try:
        primeras_filas = df[variables].head(10)
        matriz_correlacion = df[variables].corr(method='spearman')

        reporte_data = {
            "titulo": "Reporte - Análisis de Correlación de Spearman",
            "descripcion": "Análisis de correlación de Spearman para evaluar la relación entre las variables seleccionadas.",
            "tipo_analisis": "correlacion_spearman",
            "resultados": {
                "nombres_columnas": variables, 
                "primeras_filas": primeras_filas.to_dict('records'),
                "matriz_correlacion": matriz_correlacion.to_dict(),
                "graficas": []
            }
        }

        if len(variables) == 2:
            datos_dispersion = [{
                'x': row[variables[0]],
                'y': row[variables[1]]
            } for index, row in df.iterrows()]
            
            reporte_data["resultados"]["graficas"].append({
                "tipo_grafico": "diagrama_dispersion",
                "titulo": f"Dispersión entre {variables[0]} y {variables[1]}",
                "datos": datos_dispersion,
                "etiquetas_x": variables[0],
                "etiquetas_y": variables[1]
            })
        else:
            datos_positivos = []
            datos_negativos = []
            max_correlation = matriz_correlacion.abs().max().max()
            for i, variable_i in enumerate(variables):
                for j, variable_j in enumerate(variables):
                    if i != j:
                        size = np.abs(matriz_correlacion.iloc[i, j]) / max_correlation * 100
                        if matriz_correlacion.iloc[i, j] < 0:
                            color = 'rgba(255, 0, 0, 0.5)'
                            datos_negativos.append({"x": j, "y": len(variables) - i - 1, "r": size, "backgroundColor": color})
                        else:
                            color = 'rgba(0, 161, 53, 0.5)'
                            datos_positivos.append({"x": j, "y": len(variables) - i - 1, "r": size, "backgroundColor": color})
            
            reporte_data["resultados"]["graficas"].append({
                "tipo_grafico": "grafica_burbuja",
                "titulo": "Correlación de Spearman",
                "datos_positivos": datos_positivos,
                "datos_negativos": datos_negativos,
                "etiquetas_x": variables,
                "etiquetas_y": list(reversed(variables))
            })

    except Exception as e:
        resultado['Errores'].append(str(e))
        reporte_data = None
    
    return df, reporte_data, resultado