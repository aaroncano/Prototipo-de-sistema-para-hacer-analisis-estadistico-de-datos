import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, roc_curve, roc_auc_score
from sklearn.preprocessing import label_binarize

def regresion_linear(df, variable_dependiente, variables_independientes):
    # Preparar datos
    X = df[variables_independientes]
    y = df[variable_dependiente]

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inicializar y entrenar el modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Realizar predicciones con el conjunto de prueba
    y_pred = modelo.predict(X_test)

    # Calcular métricas de rendimiento
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Crear una lista para los gráficos
    graficos = []

    # Generar un gráfico para cada variable independiente
    for i, var_indep in enumerate(variables_independientes):
        # Seleccionar la columna de datos correspondiente
        X_var = X_test[var_indep].values.reshape(-1, 1)

        # Ajustar el modelo para una sola variable independiente
        modelo_var = LinearRegression()
        modelo_var.fit(X_var, y_test)
        y_pred_var = modelo_var.predict(X_var)

        # Ordenar los puntos para el gráfico de línea
        sorted_axis = np.argsort(X_var, axis=0).flatten()
        X_var_sorted = X_var[sorted_axis]
        y_pred_var_sorted = y_pred_var[sorted_axis]

        # Preparar puntos de la línea de ajuste
        puntos_linea_ajuste = [{"x": float(X_var_sorted[i]), "y": float(y_pred_var_sorted[i])} for i in range(len(X_var_sorted))]

        # Preparar puntos observados
        puntos_observados = [{"x": float(X_var[i][0]), "y": float(y_test.iloc[i])} for i in range(len(X_var))]

        # Agregar al gráfico
        graficos.append({
            "tipo_grafico": "scatter_linea",
            "titulo": f"Relación entre {var_indep} y {variable_dependiente}",
            "datos": {
                "puntos_observados": puntos_observados,
                "puntos_linea_ajuste": puntos_linea_ajuste,
            }
        })

    # Preparar el resultado para devolver
    reporte_data = {
        "titulo": "Resultados de Regresión Lineal",
        "descripcion": f"Análisis de regresión lineal para '{variable_dependiente}' con variables independientes {', '.join(variables_independientes)}.",
        "tipo_analisis": "regresion_lineal",
        "resultados": {
            "estadisticas": {
                "MSE": mse,
                "R²": r2,
            },
            "coeficientes": dict(zip(variables_independientes, modelo.coef_)),
            "intercepto": modelo.intercept_,
            "graficos": graficos
        }
    }

    return df, reporte_data


def regresion_logistica(df, variable_dependiente, variables_independientes, umbral=0.5):
    # Preparar datos
    X = df[variables_independientes]
    y = label_binarize(df[variable_dependiente].values, classes=[0, 1])[:, 0]

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inicializar y entrenar el modelo de regresión logística
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)

    # Realizar predicciones con el conjunto de prueba
    y_pred_proba = modelo.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= umbral).astype(int)

    # Calcular métricas de rendimiento
    matriz_confusion = confusion_matrix(y_test, y_pred).tolist()  # Convertir a lista para visualización

    
    acc = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Preparar datos para el gráfico de dispersión con línea de ajuste
    dispersion_data = None
    if len(variables_independientes) == 1:
        variable_indep = X_test[variables_independientes[0]]
        # Ordenar los valores para la línea
        sorted_indices = np.argsort(variable_indep)
        variable_indep_sorted = variable_indep.iloc[sorted_indices]
        y_pred_proba_sorted = y_pred_proba[sorted_indices]

        dispersion_data = {
            "x": variable_indep_sorted.tolist(),
            "y": y_test[sorted_indices].tolist(),
            "y_model": y_pred_proba_sorted.tolist()
        }

    # Generar el reporte de datos
    reporte_data = {
        "titulo": "Resultados de Regresión Logística",
        "descripcion": f"Análisis de regresión logística para '{variable_dependiente}' con variables independientes {', '.join(variables_independientes)} y umbral de {umbral}.",
        "tipo_analisis": "regresion_logistica",
        "resultados": {
            "matriz_confusion": matriz_confusion,
            "accuracy": acc,
            "recall": recall,
            "precision": precision,
            "f1_score": f1,
            "auc": roc_auc,
            "coeficientes": dict(zip(variables_independientes, modelo.coef_.flatten())),
            "intercepto": modelo.intercept_[0],
            "graficos": [
                {
                    "tipo_grafico": "curva_roc",
                    "titulo": "Curva ROC",
                    "datos": {
                        "puntos_curva_roc": [{"fpr": float(fpr[i]), "tpr": float(tpr[i])} for i in range(len(fpr))],
                        "roc_auc": roc_auc
                    }
                }
            ]
        }
    }

    if dispersion_data:
        reporte_data["resultados"]["graficos"].append({
            "tipo_grafico": "dispersion",
            "titulo": f"Gráfico de Dispersión con Línea de Ajuste para {variables_independientes[0]}",
            "datos": dispersion_data
        })

    return df, reporte_data
