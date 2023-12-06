def crear_inicio_tabla(df):
    return df.head(20).to_html(classes='table table-striped', index=True)
