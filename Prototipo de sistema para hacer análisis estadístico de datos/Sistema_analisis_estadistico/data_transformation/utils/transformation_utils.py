import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def transformationStand(df, alcance, tipo, columnas_a_manipular=None):
    resultado = {
        'transformadas': [],
        'errores': [],
        'no_modificadas': []
    }

    if not columnas_a_manipular or tipo == 'nombres_transformacion':
     resultado['Mensaje'] = "No se especificaron columnas a eliminar o tipo de transformación PONTE PILAS ÑERO ) 8<"
     return df, resultado
    
    
    
    if tipo == 'labelencoder':
        try:
            if alcance == 'columna_especifica':
                if columnas_a_manipular:
                    for columna in columnas_a_manipular:
                        if columna in df.columns:
                            le = LabelEncoder()
                            df[columna] = le.fit_transform(df[columna])
                            resultado['transformadas'].append(columna)
                        else:
                            resultado['errores'].append(f"Columna '{columna}' no encontrada.")
                else:
                    resultado['errores'].append("No se proporcionaron columnas para codificar.")
            
            elif alcance == 'todo':
                columnas_categoricas = df.select_dtypes(include=['object']).columns
                for columna in columnas_categoricas:
                    le = LabelEncoder()
                    df[columna] = le.fit_transform(df[columna])
                    resultado['transformadas'].append(columna)
            
        except Exception as e:
            resultado['errores'].append(f"Error al aplicar el método de estandarización: {e}")

    elif tipo == 'one_hot':
        try:
            if alcance == 'columna_especifica':
                    
                if columnas_a_manipular:
                    for columna in columnas_a_manipular:
                        if columna in df.columns:
                            encoder = OneHotEncoder(drop='first', dtype=int)
                            encoded_cols = pd.DataFrame(encoder.fit_transform(df[[columna]]).toarray(), columns=encoder.get_feature_names_out([columna]))
                            df = pd.concat([df, encoded_cols], axis=1)
                            df.drop(columna, axis=1, inplace=True)
                            resultado['transformadas'].append(columna)
                        else:
                            resultado['errores'].append(f"Columna '{columna}' no encontrada.")
                else:
                    resultado['errores'].append("No se proporcionaron columnas para codificar.")
       
                
            elif alcance == 'todo':
                for columna in df.select_dtypes(include=['object']).columns:
                    encoder = OneHotEncoder(drop='first', dtype=int)
                    encoded_cols = pd.DataFrame(encoder.fit_transform(df[[columna]]).toarray(), columns=encoder.get_feature_names_out([columna]))
                    df = pd.concat([df, encoded_cols], axis=1)
                    df.drop(columna, axis=1, inplace=True)
                    resultado['transformadas'].append(columna)
        except Exception as e:
            resultado['errores'].append(f"Error al aplicar el método de One-Hot Encoding: {e}")

    return df, resultado
