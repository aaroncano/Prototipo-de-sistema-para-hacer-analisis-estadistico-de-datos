import re
import pandas as pd

def eliminar_columnas(df, columnas_a_manipular):
    resultado = {
        'Eliminado': [],
        'No encontrado': [],
        'Mensaje': [],
        'Error': None
    }
    
    if not columnas_a_manipular:
        resultado['Mensaje'] = "No se especificaron columnas a eliminar"
        return df, resultado
    
    for col in columnas_a_manipular:
        if col in df.columns:
            try:
                df.drop(columns=[col], inplace=True)
                resultado['Eliminado'].append(col)
            except Exception as e:
                resultado['Error'] = str(e)
        else:
            resultado['No encontrado'].append(col)

    return df, resultado



def normalizar_texto(df, alcance, columnas_a_manipular=None):
    resultado = {
        'normalizadas': [],
        'errores': [],
        'no_modificadas': []
    }

    def normalizar_columna(col):
        # Función interna para normalizar cada valor en la columna
        def normalizar_valor(valor):
            partes = valor.split(',')  # Divide el valor por las comas
            partes_normalizadas = [p.strip().lower().replace(' ', '_') for p in partes]  # Normaliza cada parte
            return ', '.join(partes_normalizadas)  # Une las partes nuevamente
        # Saltar columnas con datos numéricos
        if pd.api.types.is_numeric_dtype(df[col]):
            resultado['no_modificadas'].append(col)
            return
        try:
            df[col] = df[col].astype(str).apply(normalizar_valor)
            resultado['normalizadas'].append(col)
        except Exception as e:
            resultado['errores'].append(f"Error al normalizar la columna '{col}': {e}")

    try:
        if alcance == 'nombres_columnas':
            for col in df.columns:
                try:
                    nuevo_nombre = re.sub(r'\s+', '_', col.strip().lower())
                    df.rename(columns={col: nuevo_nombre}, inplace=True)
                    resultado['normalizadas'].append(nuevo_nombre)
                except Exception as e:
                    resultado['errores'].append(f"Error al renombrar la columna '{col}': {e}")

        elif alcance == 'columna_especifica':
            if columnas_a_manipular:
                for columna in columnas_a_manipular:
                    if columna in df.columns:
                        normalizar_columna(columna)
                    else:
                        resultado['errores'].append(f"Columna '{columna}' no encontrada.")
            else:
                resultado['errores'].append("No se proporcionaron columnas para normalizar.")
                
        elif alcance == 'todo':
            for col in df.columns:
                normalizar_columna(col)
    except Exception as e:
        resultado['errores'].append(f"Error general al normalizar: {e}")

    return df, resultado


def manejar_valores_vacios(df, alcance, columnas_a_manipular=None, accion='eliminar'):
    resultado = {
        'modificadas': [],
        'errores': [],
        'no_modificadas': [] 
    }

    def manejar_columna(col):
        try:
            if df[col].isna().any():  # Comprobar si la columna tiene valores NaN
                if accion == 'eliminar':
                    df.dropna(subset=[col], inplace=True)
                elif accion == 'cero_no_definido':
                    reemplazo = 0 if pd.api.types.is_numeric_dtype(df[col]) else "No definido"
                    df[col].fillna(reemplazo, inplace=True)
                elif accion == 'media_mas_comun':
                    if pd.api.types.is_numeric_dtype(df[col]):
                        df[col].fillna(df[col].mean(), inplace=True)
                    else:
                        valor_mas_comun = df[col].mode()[0] if not df[col].mode().empty else "No definido"
                        df[col].fillna(valor_mas_comun, inplace=True)
                resultado['modificadas'].append(col)
            else:
                resultado['no_modificadas'].append(col)  # La columna no tiene valores NaN
        except Exception as e:
            resultado['errores'].append(f"Error al manejar valores vacíos en {col}: {str(e)}")

    try:
        if alcance == 'todo':
            for col in df.columns:
                manejar_columna(col)
        elif alcance == 'columna_especifica':
            if columnas_a_manipular:
                for columna in columnas_a_manipular:
                    if columna in df.columns:
                        manejar_columna(columna)
                    else:
                        resultado['errores'].append(f"Columna {columna} no encontrada.")
            else:
                resultado['errores'].append("No se proporcionaron columnas para manejar.")
    except Exception as e:
        resultado['errores'].append(f"Error general en el manejo de valores vacíos: {e}")

    return df, resultado


def procesar_outliers_iqr(df, columnas_a_manipular=None, umbral_iqr=1.5, accion='ajustar'):
    resultado = {'ajustados': [], 'eliminados': [], 'errores': [], 'sin_outliers': []}

    def procesar_columna(col):
        try:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - umbral_iqr * IQR
            limite_superior = Q3 + umbral_iqr * IQR

            outliers = (df[col] < limite_inferior) | (df[col] > limite_superior)

            if not outliers.any():
                resultado['sin_outliers'].append(col)
                return

            if accion == 'ajustar':
                df[col] = df[col].clip(lower=limite_inferior, upper=limite_superior)
                resultado['ajustados'].append(col)

            elif accion == 'eliminar':
                indices_eliminados = df[outliers].index
                df.drop(indices_eliminados, inplace=True)
                resultado['eliminados'].extend(indices_eliminados.tolist())

        except Exception as e:
            resultado['errores'].append(f"Error al procesar {col}: {e}")

    columnas_a_revisar = columnas_a_manipular if columnas_a_manipular else df.select_dtypes(include=['number']).columns
    for col in columnas_a_revisar:
        procesar_columna(col)

    return df, resultado

def filtrar_filas_por_condicion(df, columnas_a_manipular, condicion_str):
    resultado = {'filas_eliminadas': 0, 'errores': [], 'indices_eliminados': []}

    try:

        condicion = eval("lambda x: " + condicion_str)
    except SyntaxError as e:
        resultado['errores'].append(f"Error de sintaxis en la condición: {str(e)}")
        return df, resultado
    except Exception as e:
        resultado['errores'].append(f"Error en la condición proporcionada: {str(e)}")
        return df, resultado

    if columnas_a_manipular:
        df_inicial = df.copy()
        for columna in columnas_a_manipular:
            if columna in df.columns:
                try:
                    filtro = df[columna].apply(condicion)
                    df = df[filtro]
                except Exception as e:
                    resultado['errores'].append(f"Error al aplicar la condición en {columna}: {str(e)}")
            else:
                resultado['errores'].append(f"Columna {columna} no encontrada.")
        filas_eliminadas = df_inicial.index.difference(df.index)
        resultado['filas_eliminadas'] = len(filas_eliminadas)
        resultado['indices_eliminados'] = filas_eliminadas.tolist()
    else:
        resultado['errores'].append("No se proporcionaron columnas para filtrar.")

    return df, resultado
