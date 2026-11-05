import pandas as pd
import numpy as np
from Analyzer.types_detector import columnas_textuales

def limpieza_general(df):
    #Limpiamos nombres de columnas
    df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_"))
    
    df = eliminar_duplicados(df)
    df = eliminar_nulos(df)
    df = convertir_categoricas(df, 10)
    return df

def eliminar_nulos(df):
    df = df.replace(r"^\s*$", np.nan, regex=True)# vacíos y espacios
    df = df.replace(["N/A", "NA", "-", "null"], np.nan)
    print("Filas con nulos a eliminar: ", df.isna().any(axis=1).sum())

    df = df.dropna()
    return df

def eliminar_duplicados(df):
    df.duplicated().sum()
    df = df.drop_duplicates()
    return df

def convertir_categoricas(df, cant_categorias_maximas):
    columnas_str = columnas_textuales(df)
    for columna in columnas_str:
        if(df[columna].nunique() <= cant_categorias_maximas):
            df[columna] = df[columna].astype("category")
    return df
