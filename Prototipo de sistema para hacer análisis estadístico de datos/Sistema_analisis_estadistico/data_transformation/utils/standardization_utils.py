import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def standardization(df, alcance, tipo, columnas_a_manipular=None):
    resultado = {
        'transformadas': [],
        'errores': [],
        'no_modificadas': []
    }

    if not columnas_a_manipular or tipo == 'nombres_estandarizacion':
     resultado['Mensaje'] = "No se especificaron columnas a eliminar o tipo de estandarización PONTE PILAS ÑERO ) 8<"
     return df, resultado
    
    
    # Método MaxMin
    elif tipo == 'maxmin':
        try:
            if alcance == 'columna_especifica':
                if columnas_a_manipular:
                    scaler = MinMaxScaler()
                    df[columnas_a_manipular] = scaler.fit_transform(df[columnas_a_manipular])
                    resultado['transformadas'] += columnas_a_manipular
                else:
                    resultado['errores'].append("No se proporcionaron columnas para estandarizar.")
                
            elif alcance == 'todo':
                scaler = MinMaxScaler()
                df[df.columns] = scaler.fit_transform(df[df.columns])
                resultado['transformadas'] += list(df.columns)
        except Exception as e:
            resultado['errores'].append(f"Error al aplicar el método MaxMin: {e}")

    # Método Normalizar
    elif tipo == 'normalizar':
        try:
            if alcance == 'columna_especifica':
                if columnas_a_manipular:
                    scaler = MinMaxScaler()
                    df[columnas_a_manipular] = scaler.fit_transform(df[columnas_a_manipular])
                    resultado['transformadas'] += columnas_a_manipular
                else:
                    resultado['errores'].append("No se proporcionaron columnas para normalizar.")
                
            elif alcance == 'todo':
                scaler = MinMaxScaler()
                df[df.columns] = scaler.fit_transform(df[df.columns])
                resultado['transformadas'] += list(df.columns)
        except Exception as e:
            resultado['errores'].append(f"Error al aplicar el método de Normalización: {e}")

    # Método Estandarizar
    elif tipo == 'estandar':
        try:
            if alcance == 'columna_especifica':
                if columnas_a_manipular:
                    scaler = StandardScaler()
                    df[columnas_a_manipular] = scaler.fit_transform(df[columnas_a_manipular])
                    resultado['transformadas'] += columnas_a_manipular
                else:
                    resultado['errores'].append("No se proporcionaron columnas para estandarizar.")
                
            elif alcance == 'todo':
                scaler = StandardScaler()
                df[df.columns] = scaler.fit_transform(df[df.columns])
                resultado['transformadas'] += list(df.columns)
        except Exception as e:
            resultado['errores'].append(f"Error al aplicar el método de Estandarización: {e}")

    return df, resultado
