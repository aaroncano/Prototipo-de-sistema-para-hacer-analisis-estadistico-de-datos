import pandas as pd

# cosas a añadir según el requerimiento 2
# 1. Datos duplicados
# 2. Datos irrelevantes
# 3. Datos atipicos

# cosas a añadir según el requerimiento 3-4
# 1. variable categóricas a numéricas
# 2. Tratar valores nulos
# 3. Tratar outliers

#normalización:
# 1. Rango de valores
# 2. Máximo y mínimo
# 3. Escalamiento de datos

def eliminar_columnas(df, columnas_a_eliminar):
    """
    Elimina las columnas especificadas de un DataFrame de pandas.

    Parámetros:
    df (pandas.DataFrame): DataFrame del cual se eliminarán las columnas.
    columnas_a_eliminar (list): Lista de nombres de columnas a eliminar.

    Retorna:
    tuple: El DataFrame modificado y un diccionario con detalles sobre el resultado de la operación.

    La función primero imprime las columnas originales del DataFrame y las columnas solicitadas para eliminar.
    Luego, itera sobre la lista de columnas a eliminar y, si la columna existe en el DataFrame, intenta eliminarla.
    Si ocurre una excepción durante la eliminación, se captura y almacena en el diccionario de resultados.
    Finalmente, la función imprime las columnas restantes después de la eliminación y el resultado de la operación.
    """

    resultado = {
        'Eliminado': [],
        'No encontrado': [],
        'Mensaje': [],
        'Error': None
    }
    
    if not columnas_a_eliminar:
        resultado['Mensaje'] = "No se especificaron columnas a eliminar"
        return df, resultado
    
    for col in columnas_a_eliminar:
        if col in df.columns:
            try:
                df.drop(columns=[col], inplace=True)
                resultado['Eliminado'].append(col)
            except Exception as e:
                resultado['Error'] = str(e)
        else:
            resultado['No encontrado'].append(col)

    return df, resultado



def normalizar_texto(df, alcance, columna_especifica=None):
    """
    Normaliza el texto en las columnas de un DataFrame de pandas.

    Parámetros:
    df (pandas.DataFrame): DataFrame a ser procesado.
    alcance (str): Puede ser 'nombres_columnas', 'columna_especifica' o 'todo'.
    columna_especifica (str, opcional): Nombre de la columna específica a normalizar.

    Retorna:
    tuple: DataFrame modificado y un diccionario con información sobre el resultado.
    """

    resultado = {
        'normalizadas': [],
        'errores': [],
        'no_modificadas': []
    }

    def normalizar_columna(col):
        def normalizar_valor(valor):
            partes = valor.split(',')  # Divide el valor por las comas
            partes_normalizadas = [p.strip().lower().replace(' ', '_') for p in partes]  # Normaliza cada parte
            return ', '.join(partes_normalizadas)  # Une las partes nuevamente, manteniendo la coma y el espacio

        if pd.api.types.is_numeric_dtype(df[col]):
            resultado['no_modificadas'].append(f"{col} (dato numérico)")
            return

        try:
            df[col] = df[col].astype(str).apply(normalizar_valor)
            resultado['normalizadas'].append(col)
        except Exception as e:
            resultado['errores'].append(f"Error al normalizar {col}: {e}")

    if alcance == 'nombres_columnas':
        for col in df.columns:
            nuevo_nombre = col.strip().lower().replace(' ', '_', regex=True)
            df.rename(columns={col: nuevo_nombre}, inplace=True)
            resultado['normalizadas'].append(nuevo_nombre)
    elif alcance == 'columna_especifica' and columna_especifica:
        if columna_especifica in df.columns:
            normalizar_columna(columna_especifica)
        else:
            resultado['errores'].append(f"Columna {columna_especifica} no encontrada.")
    elif alcance == 'todo':
        for col in df.columns:
            normalizar_columna(col)

    return df, resultado


def manejar_valores_vacios(df, alcance, columna_especifica=None, accion='eliminar'):
    """
    Maneja los valores vacíos en un DataFrame de pandas.

    Parámetros:
    df (pandas.DataFrame): DataFrame a procesar.
    alcance (str): 'todo' para todo el DataFrame, 'columna_especifica' para una columna.
    columna_especifica (str, opcional): Columna específica a procesar.
    accion (str): Acción para manejar valores vacíos ('eliminar', 'cero_no_definido', 'media_mas_comun').

    Retorna:
    tuple: DataFrame modificado, diccionario con información sobre el resultado.
    """

    resultado = {
        'modificadas': [],
        'errores': []
    }

    def manejar_columna(col):
        try:
            if accion == 'eliminar':
                df.dropna(subset=[col], inplace=True)
            elif accion == 'cero_no_definido':
                reemplazo = 0 if pd.api.types.is_numeric_dtype(df[col]) else "No definido"
                df[col].fillna(reemplazo, inplace=True)
            elif accion == 'media_mas_comun':
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].mean(), inplace=True)
                else:
                    valor_mas_comun = df[col].mode()[0]
                    df[col].fillna(valor_mas_comun, inplace=True)

            resultado['modificadas'].append(col)
        except Exception as e:
            resultado['errores'].append(f"Error al manejar valores vacíos en {col}: {str(e)}")

    if alcance == 'todo':
        for col in df.columns:
            manejar_columna(col)
    elif alcance == 'columna_especifica' and columna_especifica:
        if columna_especifica in df.columns:
            manejar_columna(columna_especifica)
        else:
            resultado['errores'].append(f"Columna {columna_especifica} no encontrada.")

    return df, resultado



def procesar_outliers_iqr(df, columnas=None, umbral_iqr=1.5, accion='ajustar'):
    """
    Detecta y procesa outliers en un DataFrame de pandas utilizando el método IQR.
    Los outliers pueden ser ajustados o eliminados según el parámetro 'accion'.

    Parámetros:
    df (pandas.DataFrame): DataFrame a ser procesado.
    columnas (list, opcional): Lista de columnas a revisar. Si es None, se revisan todas las columnas numéricas.
    umbral_iqr (float): Multiplicador del IQR para definir los límites de outliers.
    accion (str): 'ajustar' para ajustar los valores de outliers, 'eliminar' para eliminar las filas con outliers.

    Retorna:
    tuple: DataFrame modificado y un diccionario con información sobre los outliers procesados.
    """

    resultado = {
        'ajustados': [],
        'eliminados': [],
        'errores': []
    }

    def procesar_columna(col):
        try:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            limite_inferior = Q1 - umbral_iqr * IQR
            limite_superior = Q3 + umbral_iqr * IQR

            if accion == 'ajustar':
                outliers_inferiores = df[col] < limite_inferior
                outliers_superiores = df[col] > limite_superior

                # Ajustar outliers
                df.loc[outliers_inferiores, col] = limite_inferior
                df.loc[outliers_superiores, col] = limite_superior

                # Agregar índices ajustados al resultado
                indices_ajustados = df[outliers_inferiores | outliers_superiores].index.tolist()
                resultado['ajustados'].extend(indices_ajustados)

            elif accion == 'eliminar':
                # Eliminar filas con outliers
                outliers = (df[col] < limite_inferior) | (df[col] > limite_superior)
                indices_eliminados = df[outliers].index
                df.drop(indices_eliminados, inplace=True)

                # Agregar índices eliminados al resultado
                resultado['eliminados'].extend(indices_eliminados.tolist())

        except Exception as e:
            resultado['errores'].append(f"Error al procesar {col}: {e}")

    # Definir columnas a revisar
    columnas_a_revisar = columnas if columnas is not None else df.select_dtypes(include=['number']).columns

    for col in columnas_a_revisar:
        procesar_columna(col)

    return df, resultado

def filtrar_filas_por_condicion(df, columnas, condicion):
    """
    Filtra filas en un DataFrame de pandas basado en una condición en columnas específicas.

    Parámetros:
    df (pandas.DataFrame): DataFrame a procesar.
    columnas (list): Lista de columnas numéricas a evaluar.
    condicion (func): Función que toma un valor y devuelve True si la fila debe mantenerse.

    Retorna:
    tuple: DataFrame modificado, diccionario con información sobre las filas eliminadas.
    """

    resultado = {
        'filas_eliminadas': 0,
        'errores': []
    }

    try:
        # Aplicar la condición a las columnas especificadas y eliminar filas que no la cumplen
        filtro = df[columnas].apply(condicion)
        filas_originales = len(df)
        df = df[filtro.all(axis=1)]
        filas_despues = len(df)

        resultado['filas_eliminadas'] = filas_originales - filas_despues

    except Exception as e:
        resultado['errores'].append(f"Error al filtrar filas: {str(e)}")

    return df, resultado